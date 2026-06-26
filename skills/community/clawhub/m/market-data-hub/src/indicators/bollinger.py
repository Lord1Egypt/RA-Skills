"""
布林带 (Bollinger Bands) 指标计算

布林带是基于移动平均线和标准差的技术指标，用于衡量价格波动性。

计算公式：
- 中轨 (MB) = N日简单移动平均线
- 上轨 (UP) = 中轨 + k * N日标准差
- 下轨 (DN) = 中轨 - k * N日标准差

默认参数：N=20, k=2
"""

import pandas as pd
import numpy as np


def calculate_bollinger_bands(df: pd.DataFrame,
                              period: int = 20,
                              std_multiplier: float = 2.0,
                              column: str = 'close') -> pd.DataFrame:
    """
    计算布林带指标
    
    Args:
        df: 包含价格数据的DataFrame
        period: 计算周期，默认20
        std_multiplier: 标准差倍数，默认2.0
        column: 价格列名，默认 'close'
        
    Returns:
        pd.DataFrame: 添加了布林带列的DataFrame
        新增的列：
        - BB_MIDDLE: 中轨（移动平均线）
        - BB_UPPER: 上轨
        - BB_LOWER: 下轨
        - BB_WIDTH: 带宽（(上轨-下轨)/中轨）
        - BB_POSITION: 价格在带内的位置（0-1）
        - BB_percent_b: %B指标（(价格-下轨)/(上轨-下轨)）
        
    Example:
        >>> df = calculate_bollinger_bands(df, period=20)
        >>> print(df[['close', 'BB_MIDDLE', 'BB_UPPER', 'BB_LOWER']].tail())
    """
    if column not in df.columns:
        raise ValueError(f"DataFrame中不存在列: {column}")
    
    df = df.copy()
    
    # 计算中轨（简单移动平均线）
    df['BB_MIDDLE'] = df[column].rolling(window=period, min_periods=1).mean()
    
    # 计算标准差
    rolling_std = df[column].rolling(window=period, min_periods=1).std()
    
    # 计算上轨和下轨
    df['BB_UPPER'] = df['BB_MIDDLE'] + (rolling_std * std_multiplier)
    df['BB_LOWER'] = df['BB_MIDDLE'] - (rolling_std * std_multiplier)
    
    # 计算带宽（相对带宽）
    df['BB_WIDTH'] = (df['BB_UPPER'] - df['BB_LOWER']) / df['BB_MIDDLE']
    
    # 计算价格在带内的位置 (%B)
    df['BB_percent_b'] = (df[column] - df['BB_LOWER']) / (df['BB_UPPER'] - df['BB_LOWER'])
    
    # 判断价格在布林带中的位置
    df['BB_above_upper'] = df[column] > df['BB_UPPER']
    df['BB_below_lower'] = df[column] < df['BB_LOWER']
    df['BB_touch_upper'] = np.abs(df[column] - df['BB_UPPER']) / df['BB_UPPER'] < 0.001
    df['BB_touch_lower'] = np.abs(df[column] - df['BB_LOWER']) / df['BB_LOWER'] < 0.001
    
    return df


def calculate_bandwidth(df: pd.DataFrame) -> pd.Series:
    """
    计算布林带宽度指标
    
    带宽收缩表示波动性降低，可能预示即将突破
    带宽扩张表示波动性增加
    
    Args:
        df: 包含布林带数据的DataFrame
        
    Returns:
        pd.Series: 带宽变化率
    """
    if 'BB_WIDTH' not in df.columns:
        raise ValueError("DataFrame中不存在BB_WIDTH列，请先调用calculate_bollinger_bands()")
    
    # 带宽变化率
    return df['BB_WIDTH'].pct_change()


def analyze_bollinger_squeeze(df: pd.DataFrame, 
                              lookback: int = 120) -> dict:
    """
    分析布林带挤压（Bollinger Squeeze）
    
    当带宽处于历史低位时，表示波动性压缩，可能即将有大行情
    
    Args:
        df: 包含布林带数据的DataFrame
        lookback: 回溯周期
        
    Returns:
        dict: 挤压分析结果
    """
    if 'BB_WIDTH' not in df.columns:
        raise ValueError("请先计算布林带")
    
    current_width = df['BB_WIDTH'].iloc[-1]
    min_width = df['BB_WIDTH'].tail(lookback).min()
    max_width = df['BB_WIDTH'].tail(lookback).max()
    
    # 计算带宽在历史区间的位置
    width_percentile = (current_width - min_width) / (max_width - min_width) if max_width > min_width else 0
    
    is_squeeze = width_percentile < 0.1  # 带宽处于历史底部10%
    
    return {
        'is_squeeze': is_squeeze,
        'current_width': round(current_width, 4),
        'min_width_120d': round(min_width, 4),
        'max_width_120d': round(max_width, 4),
        'width_percentile': round(width_percentile * 100, 2),
        'suggestion': '可能即将突破' if is_squeeze else '正常波动'
    }


def get_bollinger_signals(df: pd.DataFrame) -> dict:
    """
    获取布林带交易信号
    
    Args:
        df: 包含布林带数据的DataFrame
        
    Returns:
        dict: 当前信号分析
    """
    if 'BB_UPPER' not in df.columns:
        raise ValueError("请先计算布林带")
    
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    signals = {
        'price': round(latest['close'], 2),
        'upper_band': round(latest['BB_UPPER'], 2),
        'middle_band': round(latest['BB_MIDDLE'], 2),
        'lower_band': round(latest['BB_LOWER'], 2),
        'percent_b': round(latest['BB_percent_b'] * 100, 2),
        'position': None,
        'signal': None
    }
    
    # 判断位置
    if latest['BB_percent_b'] > 1:
        signals['position'] = '上轨外'
        if prev['close'] <= prev['BB_UPPER']:
            signals['signal'] = '突破上轨'
    elif latest['BB_percent_b'] < 0:
        signals['position'] = '下轨外'
        if prev['close'] >= prev['BB_LOWER']:
            signals['signal'] = '突破下轨'
    elif latest['BB_percent_b'] > 0.8:
        signals['position'] = '上轨附近'
    elif latest['BB_percent_b'] < 0.2:
        signals['position'] = '下轨附近'
    else:
        signals['position'] = '中轨附近'
    
    # 判断趋势
    if latest['close'] > latest['BB_MIDDLE']:
        signals['trend'] = '偏多'
    else:
        signals['trend'] = '偏空'
    
    return signals
