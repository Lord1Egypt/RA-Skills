"""
移动平均线 (Moving Average) 指标计算

提供多种移动平均线的计算：
- 简单移动平均线 (SMA)
- 指数移动平均线 (EMA)
- 加权移动平均线 (WMA)
"""

import pandas as pd
import numpy as np
from typing import List, Union


def calculate_sma(data: pd.Series, period: int) -> pd.Series:
    """
    计算简单移动平均线 (SMA)
    
    Args:
        data: 价格数据序列
        period: 计算周期
        
    Returns:
        pd.Series: SMA值
    """
    return data.rolling(window=period, min_periods=1).mean()


def calculate_ema(data: pd.Series, period: int) -> pd.Series:
    """
    计算指数移动平均线 (EMA)
    
    Args:
        data: 价格数据序列
        period: 计算周期
        
    Returns:
        pd.Series: EMA值
    """
    return data.ewm(span=period, adjust=False).mean()


def calculate_wma(data: pd.Series, period: int) -> pd.Series:
    """
    计算加权移动平均线 (WMA)
    
    给予近期数据更高的权重
    
    Args:
        data: 价格数据序列
        period: 计算周期
        
    Returns:
        pd.Series: WMA值
    """
    weights = np.arange(1, period + 1)
    return data.rolling(window=period).apply(
        lambda x: np.dot(x, weights) / weights.sum(), raw=True
    )


def calculate_ma(df: pd.DataFrame, 
                 periods: List[int] = None,
                 column: str = 'close',
                 ma_type: str = 'sma') -> pd.DataFrame:
    """
    计算移动平均线
    
    在DataFrame中添加移动平均线列
    
    Args:
        df: 包含价格数据的DataFrame
        periods: 计算周期列表，默认 [5, 10, 20, 60]
        column: 用于计算的价格列名，默认 'close'
        ma_type: 均线类型，'sma'(简单), 'ema'(指数), 'wma'(加权)
        
    Returns:
        pd.DataFrame: 添加了MA列的DataFrame
        
    Example:
        >>> df = calculate_ma(df, periods=[5, 10, 20])
        >>> print(df[['close', 'MA5', 'MA10', 'MA20']].tail())
    """
    if periods is None:
        periods = [5, 10, 20, 60]
    
    if column not in df.columns:
        raise ValueError(f"DataFrame中不存在列: {column}")
    
    df = df.copy()
    
    # 选择计算函数
    ma_func = {
        'sma': calculate_sma,
        'ema': calculate_ema,
        'wma': calculate_wma
    }.get(ma_type.lower())
    
    if ma_func is None:
        raise ValueError(f"不支持的均线类型: {ma_type}")
    
    # 计算各周期均线
    for period in periods:
        col_name = f"MA{period}" if ma_type == 'sma' else f"{ma_type.upper()}{period}"
        df[col_name] = ma_func(df[column], period)
    
    return df


def calculate_ma_cross(df: pd.DataFrame, 
                       fast_period: int = 5,
                       slow_period: int = 20,
                       column: str = 'close') -> pd.DataFrame:
    """
    计算均线交叉信号
    
    生成金叉（快线上穿慢线）和死叉（快线下穿慢线）信号
    
    Args:
        df: 包含价格数据的DataFrame
        fast_period: 快线周期
        slow_period: 慢线周期
        column: 价格列名
        
    Returns:
        pd.DataFrame: 添加了交叉信号的DataFrame
    """
    df = df.copy()
    
    # 计算两条均线
    df[f'MA{fast_period}'] = calculate_sma(df[column], fast_period)
    df[f'MA{slow_period}'] = calculate_sma(df[column], slow_period)
    
    # 计算金叉和死叉
    df['MA_diff'] = df[f'MA{fast_period}'] - df[f'MA{slow_period}']
    df['golden_cross'] = (df['MA_diff'] > 0) & (df['MA_diff'].shift(1) <= 0)
    df['death_cross'] = (df['MA_diff'] < 0) & (df['MA_diff'].shift(1) >= 0)
    
    return df
