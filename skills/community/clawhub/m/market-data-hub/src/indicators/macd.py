"""
MACD (Moving Average Convergence Divergence) 指标计算

MACD是趋势跟踪动量指标，显示两条移动平均线之间的关系。

计算公式：
- EMA12 = 12日指数移动平均
- EMA26 = 26日指数移动平均  
- DIF = EMA12 - EMA26
- DEA = DIF的9日指数移动平均
- MACD柱状图 = (DIF - DEA) * 2
"""

import pandas as pd
import numpy as np


def calculate_macd(df: pd.DataFrame,
                   fast_period: int = 12,
                   slow_period: int = 26,
                   signal_period: int = 9,
                   column: str = 'close') -> pd.DataFrame:
    """
    计算MACD指标
    
    Args:
        df: 包含价格数据的DataFrame
        fast_period: 快线周期，默认12
        slow_period: 慢线周期，默认26
        signal_period: 信号线周期，默认9
        column: 价格列名，默认 'close'
        
    Returns:
        pd.DataFrame: 添加了MACD列的DataFrame
        新增的列：
        - MACD_DIF: DIF线（快线减慢线）
        - MACD_DEA: DEA线（DIF的信号线）
        - MACD_HIST: MACD柱状图
        - MACD_golden_cross: 金叉信号（DIF上穿DEA）
        - MACD_death_cross: 死叉信号（DIF下穿DEA）
        
    Example:
        >>> df = calculate_macd(df)
        >>> print(df[['close', 'MACD_DIF', 'MACD_DEA', 'MACD_HIST']].tail())
    """
    if column not in df.columns:
        raise ValueError(f"DataFrame中不存在列: {column}")
    
    df = df.copy()
    
    # 计算EMA
    ema_fast = df[column].ewm(span=fast_period, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow_period, adjust=False).mean()
    
    # 计算DIF
    df['MACD_DIF'] = ema_fast - ema_slow
    
    # 计算DEA（DIF的EMA）
    df['MACD_DEA'] = df['MACD_DIF'].ewm(span=signal_period, adjust=False).mean()
    
    # 计算MACD柱状图 (DIF - DEA) * 2
    df['MACD_HIST'] = (df['MACD_DIF'] - df['MACD_DEA']) * 2
    
    # 计算金叉死叉信号
    df['MACD_golden_cross'] = (df['MACD_DIF'] > df['MACD_DEA']) & \
                              (df['MACD_DIF'].shift(1) <= df['MACD_DEA'].shift(1))
    
    df['MACD_death_cross'] = (df['MACD_DIF'] < df['MACD_DEA']) & \
                             (df['MACD_DIF'].shift(1) >= df['MACD_DEA'].shift(1))
    
    return df


def calculate_macd_analysis(df: pd.DataFrame) -> dict:
    """
    分析MACD指标状态
    
    Args:
        df: 包含MACD计算的DataFrame
        
    Returns:
        dict: MACD分析结果
    """
    if 'MACD_DIF' not in df.columns or 'MACD_DEA' not in df.columns:
        raise ValueError("DataFrame中不存在MACD列，请先调用calculate_macd()")
    
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    analysis = {
        'dif': round(latest['MACD_DIF'], 4),
        'dea': round(latest['MACD_DEA'], 4),
        'hist': round(latest['MACD_HIST'], 4),
        'trend': '多头' if latest['MACD_DIF'] > latest['MACD_DEA'] else '空头',
        'histogram_trend': '扩大' if latest['MACD_HIST'] > prev['MACD_HIST'] else '缩小',
        'divergence': None,  # 背离分析需要更复杂的逻辑
        'signal': None
    }
    
    # 判断信号
    if latest['MACD_golden_cross']:
        analysis['signal'] = '金叉买入'
    elif latest['MACD_death_cross']:
        analysis['signal'] = '死叉卖出'
    
    return analysis
