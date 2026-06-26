from abc import ABCMeta
from HTSACsvReaderImpl import *


class CsvReader(metaclass=ABCMeta):
    """
    csv文件读取类
    """

    def __init__(self, file_path, encodeing='utf-8'):
        """
        :param file_path:
        :param encodeing:
        """
        super(CsvReader, self).__init__()
        self.reader = CsvReaderImpl(file_path, encodeing)

    # 支持iterable
    def __iter__(self):
        return self.reader

    def __del__(self):
        if self.reader is not None:
            self.reader.__del__()
            self.reader = None

    # 获取一行数据，返回list
    # 默认获取下一行数据（rowNum=0）
    # 可以获取指定行数据，但是效率较低
    # 建议通过 for row in CsvReader:的方式获取数据
    def getRow(self, rowNum=0):
        if self.reader is None:
            return []
        else:
            self.reset()
            return self.reader.getRow(rowNum)

    # 关闭csv文件读取对象，可以不调用，但是如果需要在同一作用域内打开多个csv文件，建议读取完成就调用关闭函数释放资源
    def close(self):
        self.__del__()

    def reset(self):
        if self.reader is not None:
            return self.reader.reset()
