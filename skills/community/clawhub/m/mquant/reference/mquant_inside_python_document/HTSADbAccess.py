#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: HTSADbAccess.py
from abc import ABCMeta, abstractmethod


# 返回数据库连接
class HtDbConnection(metaclass=ABCMeta):
    # __metaclass__ = ABCMeta
    """docstring for ClassName"""

    # def __init__(self):
    # super(HtSqliteConnection, self).__init__()

    ###执行sql语句，支持使用?作为替代符，替代的参数依次放入parameters列表中
    @abstractmethod
    def excutesql(self, sql, parameters=[]):
        # print(sql)
        pass

    # raise AttributeError('子类必须实现')

    ###开始事务
    @abstractmethod
    def transaction(self):
        pass

    ###提交事务
    @abstractmethod
    def commit(self):
        pass

    ###回滚到上次提交之前
    @abstractmethod
    def rollback(self):
        pass

    ###获取查询结果
    @abstractmethod
    def fetchall():
        pass

    @abstractmethod
    def fetchone():
        pass

    @abstractmethod
    def fetchmany(self, num):
        pass
