"""
AKShare数据源策略

使用AKShare库获取A股实时行情、历史K线、财务数据等。
AKShare是一个开源的金融数据接口库，数据源来自东方财富、新浪财经等。
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import pandas as pd
import numpy as np

from .base_strategy import DataSourceStrategy


class AKShareStrategy(DataSourceStrategy):
    """
    AKShare数据源策略实现
    
    支持获取：
    - 实时行情数据
    - 历史K线数据（日线、周线、月线、分钟线）
    - 资金流向数据
    - 龙虎榜数据
    """
    
    def __init__(self):
        """初始化AKShare策略"""
        self._ak = None
        self._try_import()
    
    def _try_import(self) -> bool:
        """
        尝试导入akshare库
        
        Returns:
            bool: 导入成功返回True
        """
        try:
            import akshare as ak
            self._ak = ak
            return True
        except ImportError:
            return False
    
    def get_name(self) -> str:
        """获取数据源名称"""
        return "akshare"
    
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        return self._ak is not None
    
    def _normalize_symbol_for_akshare(self, symbol: str) -> str:
        """
        将股票代码转换为AKShare格式
        
        Args:
            symbol: 股票代码，如 '300502'
            
        Returns:
            str: 带交易所前缀的代码，如 'sz300502'
        """
        symbol = self.normalize_symbol(symbol)
        
        # 判断交易所
        if symbol.startswith('6'):
            return f"sh{symbol}"  # 上海
        else:
            return f"sz{symbol}"  # 深圳（包括300、000、002等）
    
    def get_realtime_quote(self, symbol: str) -> Dict:
        """
        获取实时行情数据
        
        Args:
            symbol: 股票代码，如 '300502'
            
        Returns:
            Dict: 实时行情数据
        """
        if not self.is_available():
            raise Exception("AKShare未安装或导入失败")
        
        symbol = self.normalize_symbol(symbol)
        ak_symbol = self._normalize_symbol_for_akshare(symbol)
        
        try:
            # 使用AKShare获取实时行情
            df = self._ak.stock_bid_ask_em(symbol=symbol)
            
            if df is None or df.empty:
                raise Exception(f"无法获取股票 {symbol} 的实时行情")
            
            # 解析买卖盘数据获取当前价格
            sell_1_price = float(df[df['item'] == '卖一']['value'].values[0]) if '卖一' in df['item'].values else 0
            buy_1_price = float(df[df['item'] == '买一']['value'].values[0]) if '买一' in df['item'].values else 0
            
            # 使用卖一和买一中间价作为当前价格
            current_price = (sell_1_price + buy_1_price) / 2 if sell_1_price and buy_1_price else sell_1_price or buy_1_price
            
            # 尝试获取更多行情信息
            try:
                # 使用stock_zh_a_spot_em获取详细行情
                spot_df = self._ak.stock_zh_a_spot_em()
                spot_row = spot_df[spot_df['代码'] == symbol]
                
                if not spot_row.empty:
                    row = spot_row.iloc[0]
                    return {
                        'symbol': symbol,
                        'name': str(row.get('名称', '')),
                        'price': float(row.get('最新价', current_price)) if pd.notna(row.get('最新价')) else current_price,
                        'change': float(row.get('涨跌额', 0)) if pd.notna(row.get('涨跌额')) else 0,
                        'change_pct': float(row.get('涨跌幅', 0)) if pd.notna(row.get('涨跌幅')) else 0,
                        'volume': float(row.get('成交量', 0)) if pd.notna(row.get('成交量')) else 0,
                        'amount': float(row.get('成交额', 0)) if pd.notna(row.get('成交额')) else 0,
                        'open': float(row.get('开盘价', 0)) if pd.notna(row.get('开盘价')) else 0,
                        'high': float(row.get('最高价', 0)) if pd.notna(row.get('最高价')) else 0,
                        'low': float(row.get('最低价', 0)) if pd.notna(row.get('最低价')) else 0,
                        'pre_close': float(row.get('昨收', 0)) if pd.notna(row.get('昨收')) else 0,
                        'timestamp': datetime.now().isoformat(),
                        'source': 'akshare'
                    }
            except Exception:
                pass
            
            # 简化版返回
            return {
                'symbol': symbol,
                'name': '',
                'price': current_price,
                'change': 0,
                'change_pct': 0,
                'volume': 0,
                'amount': 0,
                'open': 0,
                'high': 0,
                'low': 0,
                'pre_close': 0,
                'timestamp': datetime.now().isoformat(),
                'source': 'akshare'
            }
            
        except Exception as e:
            raise Exception(f"获取实时行情失败: {str(e)}")
    
    def get_kline(self, symbol: str, period: str = 'day',
                  start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        获取K线历史数据
        
        Args:
            symbol: 股票代码
            period: 周期类型：day, week, month, hour, minute
            start_date: 开始日期 YYYY-MM-DD
            end_date: 结束日期 YYYY-MM-DD
            
        Returns:
            pd.DataFrame: K线数据
        """
        if not self.is_available():
            raise Exception("AKShare未安装或导入失败")
        
        symbol = self.normalize_symbol(symbol)
        ak_symbol = self._normalize_symbol_for_akshare(symbol)
        
        # 设置默认日期
        if end_date is None:
            end_date = datetime.now().strftime('%Y%m%d')
        else:
            end_date = end_date.replace('-', '')
        
        if start_date is None:
            start = datetime.strptime(end_date, '%Y%m%d') - timedelta(days=365)
            start_date = start.strftime('%Y%m%d')
        else:
            start_date = start_date.replace('-', '')
        
        try:
            # 根据周期选择不同的接口
            if period == 'day':
                df = self._ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust="qfq"  # 前复权
                )
            elif period == 'week':
                df = self._ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="weekly",
                    start_date=start_date,
                    end_date=end_date,
                    adjust="qfq"
                )
            elif period == 'month':
                df = self._ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="monthly",
                    start_date=start_date,
                    end_date=end_date,
                    adjust="qfq"
                )
            elif period == 'hour':
                # 使用分钟线数据聚合
                df = self._ak.stock_zh_a_hist_min_em(symbol=ak_symbol, period='60')
                # 限制日期范围
                if '时间' in df.columns:
                    df['日期'] = pd.to_datetime(df['时间']).dt.date
                    df = df[(df['日期'] >= pd.to_datetime(start_date).date()) & 
                            (df['日期'] <= pd.to_datetime(end_date).date())]
            elif period == 'minute':
                df = self._ak.stock_zh_a_hist_min_em(symbol=ak_symbol, period='1')
                if '时间' in df.columns:
                    df['日期'] = pd.to_datetime(df['时间']).dt.date
                    df = df[(df['日期'] >= pd.to_datetime(start_date).date()) & 
                            (df['日期'] <= pd.to_datetime(end_date).date())]
            else:
                raise ValueError(f"不支持的周期类型: {period}")
            
            # 标准化列名
            column_mapping = {
                '日期': 'date',
                '时间': 'datetime',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume',
                '成交额': 'amount',
                '振幅': 'amplitude',
                '涨跌幅': 'change_pct',
                '涨跌额': 'change',
                '换手率': 'turnover'
            }
            
            df = df.rename(columns=column_mapping)
            
            # 确保必要的列存在
            required_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
            for col in required_cols:
                if col not in df.columns and col != 'date':
                    df[col] = 0
            
            return df
            
        except Exception as e:
            raise Exception(f"获取K线数据失败: {str(e)}")
    
    def get_capital_flow(self, symbol: str) -> Dict:
        """
        获取资金流向数据
        
        Args:
            symbol: 股票代码
            
        Returns:
            Dict: 资金流向数据
        """
        if not self.is_available():
            raise Exception("AKShare未安装或导入失败")
        
        symbol = self.normalize_symbol(symbol)
        
        try:
            # 获取个股资金流
            df = self._ak.stock_individual_fund_flow(stock=symbol, market="zh")
            
            if df is None or df.empty:
                raise Exception("无法获取资金流向数据")
            
            # 获取最新数据
            latest = df.iloc[0]
            
            return {
                'symbol': symbol,
                'date': str(latest.get('日期', '')),
                'main_inflow': float(latest.get('主力净流入', 0)),
                'main_inflow_pct': float(latest.get('主力净流入占比', 0)),
                'retail_inflow': float(latest.get('散户净流入', 0)),
                'retail_inflow_pct': float(latest.get('散户净流入占比', 0)),
                'super_large_inflow': float(latest.get('超大单净流入', 0)),
                'large_inflow': float(latest.get('大单净流入', 0)),
                'medium_inflow': float(latest.get('中单净流入', 0)),
                'small_inflow': float(latest.get('小单净流入', 0)),
                'close': float(latest.get('收盘价', 0)),
                'change_pct': float(latest.get('涨跌幅', 0)),
                'source': 'akshare'
            }
            
        except Exception as e:
            raise Exception(f"获取资金流向失败: {str(e)}")
    
    def get_lhb_data(self, trade_date: str = None) -> pd.DataFrame:
        """
        获取龙虎榜数据
        
        Args:
            trade_date: 交易日期 YYYY-MM-DD，默认最新
            
        Returns:
            pd.DataFrame: 龙虎榜数据
        """
        if not self.is_available():
            raise Exception("AKShare未安装或导入失败")
        
        try:
            if trade_date:
                date_str = trade_date.replace('-', '')
                df = self._ak.stock_lhb_detail_em(start_date=date_str, end_date=date_str)
            else:
                # 获取最近交易日数据
                df = self._ak.stock_lhb_em()
            
            return df
            
        except Exception as e:
            raise Exception(f"获取龙虎榜数据失败: {str(e)}")
