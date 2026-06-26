"""
腾讯数据源策略

使用腾讯财经接口获取实时行情数据，接口速度快、稳定性高。
接口地址: https://qt.gtimg.cn/q=
"""

import json
import time
from datetime import datetime
from typing import Dict, Optional, List
import pandas as pd
import requests

from .base_strategy import DataSourceStrategy


class TencentStrategy(DataSourceStrategy):
    """
    腾讯财经数据源策略实现
    
    特点：
    - 接口响应速度快
    - 支持批量查询
    - 数据更新实时
    - 无需认证
    
    支持获取：
    - 实时行情数据
    - 基础K线数据（通过其他接口）
    """
    
    # 腾讯接口基础URL
    BASE_URL = "https://qt.gtimg.cn/q="
    
    # 字段映射（腾讯返回的是按顺序的数组）
    FIELD_MAPPING = {
        0: 'name',          # 股票名称
        1: 'code',          # 股票代码
        2: 'price',         # 当前价格
        3: 'pre_close',     # 昨收
        4: 'open',          # 开盘价
        5: 'volume',        # 成交量（手）
        6: 'outer_disc',    # 外盘
        7: 'inner_disc',    # 内盘
        8: 'buy_1_volume',  # 买一量
        9: 'buy_1_price',   # 买一价
        10: 'buy_2_volume',
        11: 'buy_2_price',
        12: 'buy_3_volume',
        13: 'buy_3_price',
        14: 'buy_4_volume',
        15: 'buy_4_price',
        16: 'buy_5_volume',
        17: 'buy_5_price',
        18: 'sell_1_volume',
        19: 'sell_1_price',
        20: 'sell_2_volume',
        21: 'sell_2_price',
        22: 'sell_3_volume',
        23: 'sell_3_price',
        24: 'sell_4_volume',
        25: 'sell_4_price',
        26: 'sell_5_volume',
        27: 'sell_5_price',
        28: 'recent_trade', # 最近逐笔成交
        29: 'time',         # 时间
        30: 'change',       # 涨跌
        31: 'change_pct',   # 涨跌幅%
        32: 'high',         # 最高价
        33: 'low',          # 最低价
        34: 'price_volume', # 价格/成交量（手）/成交额
        35: 'volume_hand',  # 成交量（手）
        36: 'amount',       # 成交金额（万）
        37: 'turnover',     # 换手率%
        38: 'pe',           # 市盈率
        39: 'unknown',
        40: 'high_limit',   # 涨停价
        41: 'low_limit',    # 跌停价
        44: 'total_cap',    # 总市值
        45: 'float_cap',    # 流通市值
        46: 'pb',           # 市净率
        47: 'amplitude',    # 涨跌幅度%
        51: 'main_business', # 主营收入
        52: 'main_profit',  # 主营利润
        55: 'eps',          # 每股收益
    }
    
    def __init__(self, timeout: int = 10):
        """
        初始化腾讯策略
        
        Args:
            timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_name(self) -> str:
        """获取数据源名称"""
        return "tencent"
    
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        try:
            # 尝试获取一个已知股票的数据
            response = self._session.get(
                f"{self.BASE_URL}sh600519",
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def _get_exchange_prefix(self, symbol: str) -> str:
        """
        获取交易所前缀
        
        Args:
            symbol: 股票代码
            
        Returns:
            str: 带前缀的代码，如 'sh600519' 或 'sz300502'
        """
        symbol = self.normalize_symbol(symbol)
        
        # 根据代码判断交易所
        if symbol.startswith('6'):
            return f"sh{symbol}"
        elif symbol.startswith('0') or symbol.startswith('3'):
            return f"sz{symbol}"
        elif symbol.startswith('4') or symbol.startswith('8'):
            return f"bj{symbol}"  # 北交所
        else:
            # 默认深圳
            return f"sz{symbol}"
    
    def _parse_response(self, text: str, symbol: str) -> Dict:
        """
        解析腾讯接口返回的数据
        
        Args:
            text: 接口返回的文本
            symbol: 股票代码
            
        Returns:
            Dict: 解析后的数据
        """
        # 腾讯返回格式: v_sh600519="1~贵州茅台~600519~...";
        try:
            # 提取引号内的内容
            start = text.find('"')
            end = text.rfind('"')
            if start == -1 or end == -1 or start == end:
                raise Exception("Invalid response format")
            
            data_str = text[start + 1:end]
            fields = data_str.split('~')
            
            # 解析数据
            result = {
                'symbol': symbol,
                'name': fields[1] if len(fields) > 1 else '',
                'code': fields[2] if len(fields) > 2 else symbol,
                'price': float(fields[3]) if len(fields) > 3 and fields[3] else 0,
                'pre_close': float(fields[4]) if len(fields) > 4 and fields[4] else 0,
                'open': float(fields[5]) if len(fields) > 5 and fields[5] else 0,
                'volume': float(fields[6]) if len(fields) > 6 and fields[6] else 0,
                'high': float(fields[33]) if len(fields) > 33 and fields[33] else 0,
                'low': float(fields[34]) if len(fields) > 34 and fields[34] else 0,
                'change': float(fields[31]) if len(fields) > 31 and fields[31] else 0,
                'change_pct': float(fields[32]) if len(fields) > 32 and fields[32] else 0,
                'amount': float(fields[37]) if len(fields) > 37 and fields[37] else 0,
                'turnover': float(fields[38]) if len(fields) > 38 and fields[38] else 0,
                'pe': float(fields[39]) if len(fields) > 39 and fields[39] else 0,
                'pb': float(fields[46]) if len(fields) > 46 and fields[46] else 0,
                'total_cap': float(fields[44]) if len(fields) > 44 and fields[44] else 0,
                'float_cap': float(fields[45]) if len(fields) > 45 and fields[45] else 0,
                'high_limit': float(fields[47]) if len(fields) > 47 and fields[47] else 0,
                'low_limit': float(fields[48]) if len(fields) > 48 and fields[48] else 0,
                'timestamp': datetime.now().isoformat(),
                'source': 'tencent'
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"解析响应数据失败: {str(e)}")
    
    def get_realtime_quote(self, symbol: str) -> Dict:
        """
        获取实时行情数据
        
        Args:
            symbol: 股票代码，如 '300502'
            
        Returns:
            Dict: 实时行情数据
        """
        symbol = self.normalize_symbol(symbol)
        full_code = self._get_exchange_prefix(symbol)
        
        try:
            url = f"{self.BASE_URL}{full_code}"
            response = self._session.get(url, timeout=self.timeout)
            response.encoding = 'gbk'
            
            if response.status_code != 200:
                raise Exception(f"HTTP错误: {response.status_code}")
            
            return self._parse_response(response.text, symbol)
            
        except Exception as e:
            raise Exception(f"获取实时行情失败: {str(e)}")
    
    def get_batch_quotes(self, symbols: List[str]) -> List[Dict]:
        """
        批量获取实时行情
        
        Args:
            symbols: 股票代码列表
            
        Returns:
            List[Dict]: 行情数据列表
        """
        if not symbols:
            return []
        
        # 转换所有代码
        full_codes = [self._get_exchange_prefix(s) for s in symbols]
        codes_str = ','.join(full_codes)
        
        try:
            url = f"{self.BASE_URL}{codes_str}"
            response = self._session.get(url, timeout=self.timeout)
            response.encoding = 'gbk'
            
            if response.status_code != 200:
                raise Exception(f"HTTP错误: {response.status_code}")
            
            # 解析多条数据
            results = []
            lines = response.text.strip().split(';')
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line or 'v_' not in line:
                    continue
                
                try:
                    # 提取代码
                    code_start = line.find('_') + 1
                    code_end = line.find('=')
                    if code_start > 0 and code_end > code_start:
                        full_code = line[code_start:code_end]
                        symbol = full_code[2:]  # 移除前缀
                        result = self._parse_response(line, symbol)
                        results.append(result)
                except Exception:
                    continue
            
            return results
            
        except Exception as e:
            raise Exception(f"批量获取行情失败: {str(e)}")
    
    def get_kline(self, symbol: str, period: str = 'day',
                  start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        获取K线数据
        
        腾讯接口限制，仅支持获取日K线数据
        
        Args:
            symbol: 股票代码
            period: 周期（仅支持day）
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            pd.DataFrame: K线数据
        """
        symbol = self.normalize_symbol(symbol)
        full_code = self._get_exchange_prefix(symbol)
        
        try:
            # 使用腾讯的K线接口
            url = f"https://web.ifzq.gtimg.cn/appstock/finance/daytrade/{full_code}"
            
            # 备用：使用另一个接口获取历史数据
            url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
            
            params = {
                'param': f"{full_code},day,,,10000,qfq"  # 前复权日线数据
            }
            
            response = self._session.get(url, params=params, timeout=self.timeout)
            data = response.json()
            
            # 解析数据
            kline_key = f"{full_code}"
            if 'data' in data and kline_key in data['data']:
                kline_data = data['data'][kline_key].get('day', [])
                
                if not kline_data:
                    raise Exception("无K线数据")
                
                # 转换为DataFrame
                df = pd.DataFrame(kline_data, columns=['date', 'open', 'close', 'low', 'high', 'volume'])
                
                # 转换数据类型
                for col in ['open', 'close', 'low', 'high', 'volume']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # 日期过滤
                if start_date:
                    df = df[df['date'] >= start_date.replace('-', '')]
                if end_date:
                    df = df[df['date'] <= end_date.replace('-', '')]
                
                # 标准化日期格式
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
                
                return df
            else:
                raise Exception("无法获取K线数据")
                
        except Exception as e:
            raise Exception(f"获取K线数据失败: {str(e)}")
