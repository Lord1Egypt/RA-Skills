"""
Baostock数据源策略

使用Baostock库获取A股历史数据、复权因子等。
Baostock是一个开源的金融数据接口库，提供高质量的历史数据。
"""

import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import pandas as pd

from .base_strategy import DataSourceStrategy


class BaostockStrategy(DataSourceStrategy):
    """
    Baostock数据源策略实现
    
    特点：
    - 高质量的历史数据
    - 支持多种复权方式
    - 数据完整性好
    
    支持获取：
    - 历史K线数据（日线、周线、月线）
    - 复权因子
    - 指数数据
    """
    
    def __init__(self):
        """初始化Baostock策略"""
        self._bs = None
        self._logged_in = False
        self._try_import()
    
    def _try_import(self) -> bool:
        """
        尝试导入baostock库
        
        Returns:
            bool: 导入成功返回True
        """
        try:
            import baostock as bs
            self._bs = bs
            return True
        except ImportError:
            return False
    
    def _ensure_login(self) -> None:
        """确保已登录"""
        if not self._logged_in:
            if not self.is_available():
                raise Exception("Baostock未安装或导入失败")
            
            # 登录
            result = self._bs.login()
            if result.error_code != '0':
                raise Exception(f"登录失败: {result.error_msg}")
            
            self._logged_in = True
    
    def _logout(self) -> None:
        """登出"""
        if self._logged_in and self._bs:
            self._bs.logout()
            self._logged_in = False
    
    def get_name(self) -> str:
        """获取数据源名称"""
        return "baostock"
    
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        return self._bs is not None
    
    def _normalize_symbol(self, symbol: str) -> str:
        """
        将股票代码转换为Baostock格式
        
        Args:
            symbol: 股票代码，如 '300502'
            
        Returns:
            str: 带交易所前缀的代码，如 'sz.300502'
        """
        symbol = super().normalize_symbol(symbol)
        
        # 判断交易所
        if symbol.startswith('6'):
            return f"sh.{symbol}"
        else:
            return f"sz.{symbol}"
    
    def get_realtime_quote(self, symbol: str) -> Dict:
        """
        获取实时行情数据
        
        Baostock主要提供历史数据，实时数据需要通过最近日K获取
        
        Args:
            symbol: 股票代码
            
        Returns:
            Dict: 行情数据（基于最近日K）
        """
        # 获取最近两天的K线数据
        try:
            df = self.get_kline(symbol, period='day', start_date=None, end_date=None)
            
            if df.empty:
                raise Exception("无法获取行情数据")
            
            # 获取最新一条
            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else latest
            
            return {
                'symbol': symbol,
                'name': '',
                'price': float(latest['close']),
                'open': float(latest['open']),
                'high': float(latest['high']),
                'low': float(latest['low']),
                'pre_close': float(prev['close']),
                'change': float(latest['close']) - float(prev['close']),
                'change_pct': ((float(latest['close']) - float(prev['close'])) / float(prev['close']) * 100) if float(prev['close']) > 0 else 0,
                'volume': float(latest['volume']),
                'amount': float(latest.get('amount', 0)),
                'timestamp': datetime.now().isoformat(),
                'source': 'baostock'
            }
            
        except Exception as e:
            raise Exception(f"获取实时行情失败: {str(e)}")
    
    def get_kline(self, symbol: str, period: str = 'day',
                  start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        获取K线历史数据
        
        Args:
            symbol: 股票代码
            period: 周期类型：day, week, month
            start_date: 开始日期 YYYY-MM-DD
            end_date: 结束日期 YYYY-MM-DD
            
        Returns:
            pd.DataFrame: K线数据
        """
        self._ensure_login()
        
        symbol = super().normalize_symbol(symbol)
        bs_symbol = self._normalize_symbol(symbol)
        
        # 设置默认日期
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        if start_date is None:
            start = datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=365)
            start_date = start.strftime('%Y-%m-%d')
        
        # 周期映射
        frequency_map = {
            'day': 'd',
            'week': 'w',
            'month': 'm',
        }
        
        if period not in frequency_map:
            raise ValueError(f"Baostock不支持的周期类型: {period}")
        
        frequency = frequency_map[period]
        
        try:
            # 查询K线数据
            rs = self._bs.query_history_k_data_plus(
                bs_symbol,
                "date,code,open,high,low,close,preclose,volume,amount,turn,pctChg",
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
                adjustflag="3"  # 3表示前复权
            )
            
            if rs.error_code != '0':
                raise Exception(f"查询失败: {rs.error_msg}")
            
            # 转换为DataFrame
            data_list = []
            while (rs.error_code == '0') and rs.next():
                data_list.append(rs.get_row_data())
            
            if not data_list:
                return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume', 'amount'])
            
            df = pd.DataFrame(data_list, columns=rs.fields)
            
            # 转换数据类型
            numeric_cols = ['open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'turn', 'pctChg']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 标准化列名
            df = df.rename(columns={
                'preclose': 'pre_close',
                'pctChg': 'change_pct',
                'turn': 'turnover'
            })
            
            return df
            
        except Exception as e:
            raise Exception(f"获取K线数据失败: {str(e)}")
    
    def get_adjustment_factors(self, symbol: str) -> pd.DataFrame:
        """
        获取复权因子
        
        Args:
            symbol: 股票代码
            
        Returns:
            pd.DataFrame: 复权因子数据
        """
        self._ensure_login()
        
        symbol = super().normalize_symbol(symbol)
        bs_symbol = self._normalize_symbol(symbol)
        
        try:
            rs = self._bs.query_adjust_factor(code=bs_symbol)
            
            if rs.error_code != '0':
                raise Exception(f"查询失败: {rs.error_msg}")
            
            data_list = []
            while (rs.error_code == '0') and rs.next():
                data_list.append(rs.get_row_data())
            
            if not data_list:
                return pd.DataFrame()
            
            df = pd.DataFrame(data_list, columns=rs.fields)
            return df
            
        except Exception as e:
            raise Exception(f"获取复权因子失败: {str(e)}")
    
    def get_index_data(self, index_code: str = "sh.000001") -> pd.DataFrame:
        """
        获取指数数据
        
        Args:
            index_code: 指数代码，如 'sh.000001'（上证指数）
            
        Returns:
            pd.DataFrame: 指数数据
        """
        self._ensure_login()
        
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            
            rs = self._bs.query_history_k_data_plus(
                index_code,
                "date,code,open,high,low,close,preclose,volume,amount,turn,pctChg",
                start_date=start_date,
                end_date=end_date,
                frequency="d"
            )
            
            if rs.error_code != '0':
                raise Exception(f"查询失败: {rs.error_msg}")
            
            data_list = []
            while (rs.error_code == '0') and rs.next():
                data_list.append(rs.get_row_data())
            
            df = pd.DataFrame(data_list, columns=rs.fields)
            return df
            
        except Exception as e:
            raise Exception(f"获取指数数据失败: {str(e)}")
    
    def __del__(self):
        """析构时登出"""
        self._logout()
