import numpy as np
import pandas as pd
import torch
import torch.utils.data as Data
from torch.utils.data.dataset import Dataset
import sys
import os
import copy
import csv
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from utility.CsvUtility import CsvUtility

origin_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]


def load_data(word_num_max=50000, sequence_max=100):
    x = CsvUtility.read_array_from_csv(origin_path + '/data/', 'x_train.csv').flatten()
    # print x[0]
    data = []
    for x_item in x:
        doc_data = []
        x_list = x_item.split('], [')
        x_list = [i.replace('[', '').replace(']', '') for i in x_list]
        # print x_list
        for seb_i, sen in enumerate(x_list):
            sen_list = [int(i) for i in sen.split(', ')]
            feature = [0.0] * word_num_max
            for i, item in enumerate(sen_list):
                if item < word_num_max:
                    feature[item] += 1
            doc_data.append(feature)
        if len(doc_data) < sequence_max:
            for _ in range(sequence_max - len(doc_data)):
                doc_data.append([0.0] * word_num_max)
        else:
            doc_data = doc_data[: sequence_max]
        # print doc_data
        data.append(doc_data)
    print 'shape of x: ', np.array(data).shape
    y = np.array(pd.read_csv(origin_path + '/data/y_train.csv', index_col=None, header=None))
    print 'shape of y: ', y.shape
    # print y
    train_data = Data.TensorDataset(data_tensor=torch.from_numpy(np.array(data)),
                                    target_tensor=torch.from_numpy(y))
    print 'Done'

    return train_data