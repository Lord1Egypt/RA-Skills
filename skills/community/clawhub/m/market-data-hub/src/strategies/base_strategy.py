"""
策略模式基类定义

定义数据源策略的抽象接口，所有具体数据源策略必须实现这些方法。
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, List
import pandas as pd


class DataSourceStrategy(ABC):
    """
    数据源策略抽象基类
    
    定义获取股票行情数据的标准接口，具体数据源策略需要实现这些方法。
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """
        获取数据源名称
        
        Returns:
            str: 数据源名称标识
        """
        pass
    
    @abstractmethod
    def get_realtime_quote(self, symbol: str) -> Dict:
        """
        获取实时行情数据
        
        Args:
            symbol: 股票代码，如 '300502'
            
        Returns:
            Dict: 包含实时行情数据的字典，至少包含以下字段：
                - symbol: 股票代码
                - name: 股票名称
                - price: 当前价格
                - change: 涨跌额
                - change_pct: 涨跌幅(%)
                - volume: 成交量
                - amount: 成交金额
                - open: 开盘价
                - high: 最高价
                - low: 最低价
                - pre_close: 昨收价
                - timestamp: 数据时间戳
                
        Raises:
            Exception: 获取数据失败时抛出异常
        """
        pass
    
    @abstractmethod
    def get_kline(self, symbol: str, period: str = 'day',
                  start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        获取K线历史数据
        
        Args:
            symbol: 股票代码，如 '300502'
            period: 周期类型，支持 'day'(日线), 'week'(周线), 'month'(月线), 
                   'hour'(小时线), 'minute'(分钟线)
            start_date: 开始日期，格式 'YYYY-MM-DD'，默认为30天前
            end_date: 结束日期，格式 'YYYY-MM-DD'，默认为今天
            
        Returns:
            pd.DataFrame: K线数据，包含列：
                - date: 日期
                - open: 开盘价
                - high: 最高价
                - low: 最低价
                - close: 收盘价
                - volume: 成交量
                - amount: 成交金额（部分数据源可能缺失）
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        检查数据源是否可用
        
        Returns:
            bool: 数据源可用返回True，否则返回False
        """
        pass
    
    def normalize_symbol(self, symbol: str) -> str:
        """
        标准化股票代码格式
        
        Args:
            symbol: 原始股票代码
            
        Returns:
            str: 标准化后的股票代码
        """
        # 移除空格和特殊字符
        symbol = symbol.strip().replace('sz', '').replace('sh', '')
        return symbol
    
    def get_capital_flow(self, symbol: str) -> Dict:
        """
        获取资金流向数据（可选实现）
        
        Args:
            symbol: 股票代码
            
        Returns:
            Dict: 资金流向数据
            
        Raises:
            NotImplementedError: 如果数据源不支持此功能
        """
        raise NotImplementedError(f"{self.get_name()} 不支持资金流向查询")
    
    def get_lhb_data(self, trade_date: str = None) -> pd.DataFrame:
        """
        获取龙虎榜数据（可选实现）
        
        Args:
            trade_date: 交易日期，格式 'YYYY-MM-DD'，默认最新日期
            
        Returns:
            pd.DataFrame: 龙虎榜数据
            
        Raises:
            NotImplementedError: 如果数据源不支持此功能
        """
        raise NotImplementedError(f"{self.get_name()} 不支持龙虎榜查询")
