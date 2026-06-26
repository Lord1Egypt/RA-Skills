"""
Market Data Hub - 市场数据统一入口

提供股票行情数据的统一获取接口，支持多个数据源，自动切换和降级。

特性：
- 多数据源策略（AKShare、腾讯、Baostock）
- 自动限流控制
- 指数退避重试
- 故障自动切换
- 技术指标计算
"""

import os
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Union, Any
import pandas as pd
import numpy as np

# 处理相对导入和绝对导入
try:
    from .strategies import (
        DataSourceStrategy,
        AKShareStrategy,
        TencentStrategy,
        BaostockStrategy
    )
    from .limiter import TokenBucket
    from .retry import RetryStrategy, CircuitBreaker
    from .indicators import (
        calculate_ma,
        calculate_macd,
        calculate_rsi,
        calculate_bollinger_bands,
        calculate_kdj
    )
except ImportError:
    from strategies import (
        DataSourceStrategy,
        AKShareStrategy,
        TencentStrategy,
        BaostockStrategy
    )
    from limiter import TokenBucket
    from retry import RetryStrategy, CircuitBreaker
    from indicators import (
        calculate_ma,
        calculate_macd,
        calculate_rsi,
        calculate_bollinger_bands,
        calculate_kdj
    )


class MarketDataHub:
    """
    市场数据统一入口类
    
    整合多个数据源，提供统一的行情数据获取接口，
    自动处理限流、重试、故障切换等。
    
    Attributes:
        strategies: 数据源策略字典
        rate_limiters: 限流器字典
        retry_strategy: 重试策略
        circuit_breakers: 熔断器字典
        source_priority: 数据源优先级列表
    """
    
    # 默认限流配置
    DEFAULT_RATE_LIMITS = {
        'akshare': {'rate': 0.5, 'capacity': 10},   # 每2秒1次，突发10次
        'tencent': {'rate': 2.0, 'capacity': 20},   # 每秒2次，突发20次
        'baostock': {'rate': 1.0, 'capacity': 10}   # 每秒1次，突发10次
    }
    
    # 默认数据源优先级（调整后：Baostock优先，腾讯次之，AKShare最后）
    # 原因：Baostock数据质量高且稳定，腾讯实时性好，AKShare作为备选
    DEFAULT_SOURCE_PRIORITY = ['baostock', 'tencent', 'akshare']
    
    def __init__(self,
                 rate_limits: Optional[Dict] = None,
                 source_priority: Optional[List[str]] = None,
                 enable_rate_limit: bool = True,
                 enable_retry: bool = True,
                 enable_circuit_breaker: bool = True):
        """
        初始化MarketDataHub
        
        Args:
            rate_limits: 自定义限流配置，格式：{'source': {'rate': 2.0, 'capacity': 20}}
            source_priority: 数据源优先级列表，如 ['tencent', 'akshare', 'baostock']
            enable_rate_limit: 是否启用限流，默认True
            enable_retry: 是否启用重试，默认True
            enable_circuit_breaker: 是否启用熔断器，默认True
        """
        # 初始化数据源策略
        self.strategies: Dict[str, DataSourceStrategy] = {
            'akshare': AKShareStrategy(),
            'tencent': TencentStrategy(),
            'baostock': BaostockStrategy()
        }
        
        # 设置数据源优先级
        self.source_priority = source_priority or self.DEFAULT_SOURCE_PRIORITY.copy()
        
        # 初始化限流器
        self.enable_rate_limit = enable_rate_limit
        self.rate_limiters: Dict[str, TokenBucket] = {}
        limits = rate_limits or self.DEFAULT_RATE_LIMITS
        
        for source, config in limits.items():
            self.rate_limiters[source] = TokenBucket(
                rate=config['rate'],
                capacity=config['capacity']
            )
        
        # 初始化重试策略
        self.enable_retry = enable_retry
        self.retry_strategy = RetryStrategy(
            max_retries=3,
            base_delay=1.0,
            jitter=True
        )
        
        # 初始化熔断器
        self.enable_circuit_breaker = enable_circuit_breaker
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        
        if enable_circuit_breaker:
            for source in self.strategies.keys():
                self.circuit_breakers[source] = CircuitBreaker(
                    failure_threshold=5,
                    recovery_timeout=30.0
                )
        
        # 使用统计
        self._usage_stats = {
            'requests': {s: 0 for s in self.strategies.keys()},
            'failures': {s: 0 for s in self.strategies.keys()},
            'last_used': {s: None for s in self.strategies.keys()}
        }
    
    def _acquire_rate_limit(self, source: str) -> bool:
        """
        获取限流令牌
        
        Args:
            source: 数据源名称
            
        Returns:
            bool: 是否成功获取令牌
        """
        if not self.enable_rate_limit:
            return True
        
        limiter = self.rate_limiters.get(source)
        if limiter:
            return limiter.acquire()
        return True
    
    def _wait_for_rate_limit(self, source: str, timeout: float = 10.0) -> bool:
        """
        等待限流令牌
        
        Args:
            source: 数据源名称
            timeout: 最大等待时间
            
        Returns:
            bool: 是否成功获取令牌
        """
        if not self.enable_rate_limit:
            return True
        
        limiter = self.rate_limiters.get(source)
        if limiter:
            return limiter.acquire(blocking=True, timeout=timeout)
        return True
    
    def _check_circuit_breaker(self, source: str) -> bool:
        """
        检查熔断器状态
        
        Args:
            source: 数据源名称
            
        Returns:
            bool: 可以执行返回True
        """
        if not self.enable_circuit_breaker:
            return True
        
        cb = self.circuit_breakers.get(source)
        if cb:
            return cb.can_execute()
        return True
    
    def _record_success(self, source: str) -> None:
        """记录成功"""
        if self.enable_circuit_breaker:
            cb = self.circuit_breakers.get(source)
            if cb:
                cb.record_success()
        
        self._usage_stats['requests'][source] += 1
        self._usage_stats['last_used'][source] = datetime.now()
    
    def _record_failure(self, source: str) -> None:
        """记录失败"""
        if self.enable_circuit_breaker:
            cb = self.circuit_breakers.get(source)
            if cb:
                cb.record_failure()
        
        self._usage_stats['failures'][source] += 1
    
    def _execute_with_retry(self, func, source: str, *args, **kwargs) -> Any:
        """
        使用重试策略执行函数
        
        Args:
            func: 要执行的函数
            source: 数据源名称
            
        Returns:
            Any: 函数执行结果
        """
        def wrapper():
            return func(*args, **kwargs)
        
        if self.enable_retry:
            return self.retry_strategy.execute(wrapper)
        else:
            return wrapper()
    
    def _try_source(self, source: str, operation: str, *args, **kwargs) -> Any:
        """
        尝试从指定数据源获取数据
        
        Args:
            source: 数据源名称
            operation: 操作类型（如 'get_realtime_quote', 'get_kline'）
            *args, **kwargs: 操作参数
            
        Returns:
            Any: 操作结果
            
        Raises:
            Exception: 获取失败时抛出异常
        """
        strategy = self.strategies.get(source)
        if not strategy:
            raise ValueError(f"未知数据源: {source}")
        
        if not strategy.is_available():
            raise Exception(f"数据源 {source} 不可用")
        
        # 检查熔断器
        if not self._check_circuit_breaker(source):
            raise Exception(f"数据源 {source} 熔断器打开")
        
        # 等待限流令牌
        if not self._wait_for_rate_limit(source):
            raise Exception(f"数据源 {source} 限流")
        
        try:
            # 执行操作
            func = getattr(strategy, operation)
            result = self._execute_with_retry(func, source, *args, **kwargs)
            
            self._record_success(source)
            return result
            
        except Exception as e:
            self._record_failure(source)
            raise e
    
    def get_realtime_quote(self, symbol: str, source: str = 'auto') -> Dict:
        """
        获取实时行情数据
        
        Args:
            symbol: 股票代码，如 '300502'
            source: 数据源名称，'auto'表示自动选择
                   可选: 'akshare', 'tencent', 'baostock'
            
        Returns:
            Dict: 实时行情数据，包含以下字段：
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
                - source: 数据来源
                
        Example:
            >>> hub = MarketDataHub()
            >>> quote = hub.get_realtime_quote('300502')
            >>> print(f"当前价格: {quote['price']}, 涨跌幅: {quote['change_pct']}%")
        """
        symbol = str(symbol).strip()
        
        if source == 'auto':
            # 按优先级尝试各数据源
            errors = []
            for src in self.source_priority:
                try:
                    return self._try_source(src, 'get_realtime_quote', symbol)
                except Exception as e:
                    errors.append(f"{src}: {str(e)}")
                    continue
            
            raise Exception(f"所有数据源均失败: {'; '.join(errors)}")
        else:
            return self._try_source(source, 'get_realtime_quote', symbol)
    
    def get_kline(self, symbol: str, period: str = 'day',
                  start_date: str = None, end_date: str = None,
                  source: str = 'auto') -> pd.DataFrame:
        """
        获取K线历史数据
        
        Args:
            symbol: 股票代码，如 '300502'
            period: 周期类型，支持 'day'(日线), 'week'(周线), 'month'(月线)
            start_date: 开始日期，格式 'YYYY-MM-DD'，默认为90天前
            end_date: 结束日期，格式 'YYYY-MM-DD'，默认为今天
            source: 数据源名称，'auto'表示自动选择
            
        Returns:
            pd.DataFrame: K线数据，包含列：
                - date: 日期
                - open: 开盘价
                - high: 最高价
                - low: 最低价
                - close: 收盘价
                - volume: 成交量
                - amount: 成交金额
                
        Example:
            >>> df = hub.get_kline('300502', period='day', start_date='2024-01-01')
            >>> print(df.tail())
        """
        symbol = str(symbol).strip()
        
        # 设置默认日期
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        if start_date is None:
            start = datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=90)
            start_date = start.strftime('%Y-%m-%d')
        
        if source == 'auto':
            errors = []
            # K线数据优先使用Baostock（数据质量高），其次腾讯，最后AKShare
            for src in ['baostock', 'tencent', 'akshare']:
                try:
                    return self._try_source(src, 'get_kline', symbol, period, start_date, end_date)
                except Exception as e:
                    errors.append(f"{src}: {str(e)}")
                    continue
            
            raise Exception(f"所有数据源均失败: {'; '.join(errors)}")
        else:
            return self._try_source(source, 'get_kline', symbol, period, start_date, end_date)
    
    def get_capital_flow(self, symbol: str, source: str = 'akshare') -> Dict:
        """
        获取资金流向数据
        
        Args:
            symbol: 股票代码
            source: 数据源，默认'akshare'（只有AKShare支持）
            
        Returns:
            Dict: 资金流向数据
        """
        symbol = str(symbol).strip()
        return self._try_source(source, 'get_capital_flow', symbol)
    
    def get_lhb_data(self, trade_date: str = None, source: str = 'akshare') -> pd.DataFrame:
        """
        获取龙虎榜数据
        
        Args:
            trade_date: 交易日期 YYYY-MM-DD，默认最新
            source: 数据源，默认'akshare'
            
        Returns:
            pd.DataFrame: 龙虎榜数据
        """
        return self._try_source(source, 'get_lhb_data', trade_date)
    
    def get_batch_quotes(self, symbols: List[str], source: str = 'tencent') -> List[Dict]:
        """
        批量获取实时行情
        
        Args:
            symbols: 股票代码列表
            source: 数据源，默认'tencent'（支持批量查询）
            
        Returns:
            List[Dict]: 行情数据列表
        """
        if source == 'tencent':
            strategy = self.strategies.get('tencent')
            if strategy and hasattr(strategy, 'get_batch_quotes'):
                if not self._wait_for_rate_limit('tencent'):
                    raise Exception("限流")
                
                try:
                    result = strategy.get_batch_quotes(symbols)
                    self._record_success('tencent')
                    return result
                except Exception as e:
                    self._record_failure('tencent')
                    raise e
        
        # 其他数据源逐个获取
        results = []
        for symbol in symbols:
            try:
                quote = self.get_realtime_quote(symbol, source=source if source != 'tencent' else 'auto')
                results.append(quote)
            except Exception:
                continue
        
        return results
    
    # ========== 技术指标计算方法 ==========
    
    def calculate_ma(self, df: pd.DataFrame, 
                     periods: List[int] = None,
                     column: str = 'close',
                     ma_type: str = 'sma') -> pd.DataFrame:
        """
        计算移动平均线
        
        Args:
            df: K线数据DataFrame
            periods: 周期列表，默认 [5, 10, 20, 60]
            column: 价格列名
            ma_type: 均线类型，'sma'/'ema'/'wma'
            
        Returns:
            pd.DataFrame: 添加了MA列的DataFrame
        """
        return calculate_ma(df, periods=periods, column=column, ma_type=ma_type)
    
    def calculate_macd(self, df: pd.DataFrame,
                       fast_period: int = 12,
                       slow_period: int = 26,
                       signal_period: int = 9,
                       column: str = 'close') -> pd.DataFrame:
        """
        计算MACD指标
        
        Args:
            df: K线数据DataFrame
            fast_period: 快线周期
            slow_period: 慢线周期
            signal_period: 信号线周期
            column: 价格列名
            
        Returns:
            pd.DataFrame: 添加了MACD列的DataFrame
        """
        return calculate_macd(df, fast_period, slow_period, signal_period, column)
    
    def calculate_rsi(self, df: pd.DataFrame,
                      period: int = 14,
                      column: str = 'close') -> pd.DataFrame:
        """
        计算RSI指标
        
        Args:
            df: K线数据DataFrame
            period: RSI周期
            column: 价格列名
            
        Returns:
            pd.DataFrame: 添加了RSI列的DataFrame
        """
        return calculate_rsi(df, period, column)
    
    def calculate_bollinger_bands(self, df: pd.DataFrame,
                                  period: int = 20,
                                  std_multiplier: float = 2.0,
                                  column: str = 'close') -> pd.DataFrame:
        """
        计算布林带指标
        
        Args:
            df: K线数据DataFrame
            period: 计算周期
            std_multiplier: 标准差倍数
            column: 价格列名
            
        Returns:
            pd.DataFrame: 添加了布林带列的DataFrame
        """
        return calculate_bollinger_bands(df, period, std_multiplier, column)
    
    def calculate_kdj(self, df: pd.DataFrame,
                      n_period: int = 9,
                      m1: int = 3,
                      m2: int = 3) -> pd.DataFrame:
        """
        计算KDJ指标
        
        Args:
            df: K线数据DataFrame，需要有high, low, close列
            n_period: RSV计算周期
            m1: K值平滑系数
            m2: D值平滑系数
            
        Returns:
            pd.DataFrame: 添加了KDJ列的DataFrame
        """
        return calculate_kdj(df, n_period, m1, m2)
    
    def get_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算所有技术指标
        
        Args:
            df: K线数据DataFrame
            
        Returns:
            pd.DataFrame: 添加了所有技术指标的DataFrame
        """
        # 确保有high, low列用于KDJ计算
        if 'high' not in df.columns or 'low' not in df.columns:
            # 如果没有high/low，用open/close估算
            df = df.copy()
            if 'high' not in df.columns:
                df['high'] = df['close']
            if 'low' not in df.columns:
                df['low'] = df['close']
        
        df = self.calculate_ma(df)
        df = self.calculate_macd(df)
        df = self.calculate_rsi(df)
        df = self.calculate_bollinger_bands(df)
        df = self.calculate_kdj(df)
        
        return df
    
    def get_usage_stats(self) -> Dict:
        """
        获取使用统计
        
        Returns:
            Dict: 各数据源的使用统计
        """
        return {
            'requests': self._usage_stats['requests'].copy(),
            'failures': self._usage_stats['failures'].copy(),
            'last_used': {k: str(v) if v else None 
                         for k, v in self._usage_stats['last_used'].items()}
        }
    
    def get_available_sources(self) -> List[str]:
        """
        获取可用的数据源列表
        
        Returns:
            List[str]: 可用的数据源名称列表
        """
        available = []
        for name, strategy in self.strategies.items():
            if strategy.is_available():
                available.append(name)
        return available
    
    def reset_circuit_breakers(self) -> None:
        """重置所有熔断器"""
        if self.enable_circuit_breaker:
            for cb in self.circuit_breakers.values():
                cb.record_success()  # 重置到关闭状态
