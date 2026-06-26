"""
RSI (Relative Strength Index) 相对强弱指标计算

RSI是衡量价格变动速度和变化的动量震荡指标。
数值范围0-100，通常70以上为超买，30以下为超卖。

计算公式：
RSI = 100 - (100 / (1 + RS))
RS = 平均上涨幅度 / 平均下跌幅度
"""

import pandas as pd
import numpy as np


def calculate_rsi(df: pd.DataFrame,
                  period: int = 14,
                  column: str = 'close') -> pd.DataFrame:
    """
    计算RSI指标
    
    Args:
        df: 包含价格数据的DataFrame
        period: RSI计算周期，默认14
        column: 价格列名，默认 'close'
        
    Returns:
        pd.DataFrame: 添加了RSI列的DataFrame
        新增的列：
        - RSI: RSI值（0-100）
        - RSI_oversold: 超卖信号（RSI < 30）
        - RSI_overbought: 超买信号（RSI > 70）
        
    Example:
        >>> df = calculate_rsi(df, period=14)
        >>> print(df[['close', 'RSI']].tail())
    """
    if column not in df.columns:
        raise ValueError(f"DataFrame中不存在列: {column}")
    
    df = df.copy()
    
    # 计算价格变化
    delta = df[column].diff()
    
    # 分离上涨和下跌
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # 计算平均上涨和平均下跌（使用指数移动平均）
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    
    # 计算RS和RSI
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 超买超卖信号
    df['RSI_oversold'] = df['RSI'] < 30
    df['RSI_overbought'] = df['RSI'] > 70
    
    return df


def calculate_rsi_multiple(df: pd.DataFrame,
                           periods: list = [6, 12, 24],
                           column: str = 'close') -> pd.DataFrame:
    """
    计算多周期RSI
    
    通常使用RSI6、RSI12、RSI24三个周期进行分析
    
    Args:
        df: 包含价格数据的DataFrame
        periods: RSI周期列表，默认 [6, 12, 24]
        column: 价格列名
        
    Returns:
        pd.DataFrame: 添加了多周期RSI的DataFrame
    """
    df = df.copy()
    
    for period in periods:
        df = calculate_rsi(df, period=period, column=column)
        df = df.rename(columns={
            'RSI': f'RSI{period}',
            'RSI_oversold': f'RSI{period}_oversold',
            'RSI_overbought': f'RSI{period}_overbought'
        })
    
    return df


def calculate_rsi_divergence(df: pd.DataFrame,
                             period: int = 14,
                             lookback: int = 20) -> pd.DataFrame:
    """
    检测RSI背离
    
    顶背离：价格创新高，RSI未创新高
    底背离：价格创新低，RSI未创新低
    
    Args:
        df: 包含价格数据和RSI的DataFrame
        period: RSI周期
        lookback: 回溯周期数
        
    Returns:
        pd.DataFrame: 添加了背离信号的DataFrame
    """
    if 'RSI' not in df.columns:
        df = calculate_rsi(df, period=period)
    
    df = df.copy()
    
    # 寻找局部极值
    df['price_high'] = df['high'] == df['high'].rolling(window=lookback, center=True).max()
    df['price_low'] = df['low'] == df['low'].rolling(window=lookback, center=True).min()
    
    df['RSI_high'] = df['RSI'] == df['RSI'].rolling(window=lookback, center=True).max()
    df['RSI_low'] = df['RSI'] == df['RSI'].rolling(window=lookback, center=True).min()
    
    # 顶背离：价格新高但RSI未新高
    df['bearish_divergence'] = df['price_high'] & ~df['RSI_high']
    
    # 底背离：价格新低但RSI未新低
    df['bullish_divergence'] = df['price_low'] & ~df['RSI_low']
    
    return df


def analyze_rsi_zone(rsi_value: float) -> dict:
    """
    分析RSI数值区间
    
    Args:
        rsi_value: RSI数值
        
    Returns:
        dict: 分析结果
    """
    if rsi_value >= 80:
        return {
            'zone': '严重超买',
            'suggestion': '考虑卖出',
            'strength': 5,
            'color': 'red'
        }
    elif rsi_value >= 70:
        return {
            'zone': '超买区',
            'suggestion': '谨慎追高',
            'strength': 4,
            'color': 'orange'
        }
    elif rsi_value >= 50:
        return {
            'zone': '多头区',
            'suggestion': '趋势偏多',
            'strength': 3,
            'color': 'lightgreen'
        }
    elif rsi_value >= 30:
        return {
            'zone': '空头区',
            'suggestion': '趋势偏空',
            'strength': 2,
            'color': 'lightblue'
        }
    elif rsi_value >= 20:
        return {
            'zone': '超卖区',
            'suggestion': '谨慎杀跌',
            'strength': 1,
            'color': 'blue'
        }
    else:
        return {
            'zone': '严重超卖',
            'suggestion': '考虑买入',
            'strength': 0,
            'color': 'green'
        }
