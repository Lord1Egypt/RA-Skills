"""
KDJ (随机指标) 计算

KDJ是一种技术分析指标，用于判断超买超卖状态。

计算公式：
- RSV = (收盘价 - N日内最低价) / (N日内最高价 - N日内最低价) * 100
- K值 = 2/3 * 昨日K值 + 1/3 * 当日RSV
- D值 = 2/3 * 昨日D值 + 1/3 * 当日K值
- J值 = 3 * K值 - 2 * D值

默认参数：N=9, M1=3, M2=3
"""

import pandas as pd
import numpy as np


def calculate_kdj(df: pd.DataFrame,
                  n_period: int = 9,
                  m1: int = 3,
                  m2: int = 3) -> pd.DataFrame:
    """
    计算KDJ指标
    
    Args:
        df: 包含OHLC数据的DataFrame，需要有high, low, close列
        n_period: RSV计算周期，默认9
        m1: K值平滑系数，默认3
        m2: D值平滑系数，默认3
        
    Returns:
        pd.DataFrame: 添加了KDJ列的DataFrame
        新增的列：
        - KDJ_K: K值
        - KDJ_D: D值
        - KDJ_J: J值
        - KDJ_golden_cross: 金叉信号（K上穿D）
        - KDJ_death_cross: 死叉信号（K下穿D）
        - KDJ_overbought: 超买信号（K > 80）
        - KDJ_oversold: 超卖信号（K < 20）
        
    Example:
        >>> df = calculate_kdj(df, n_period=9)
        >>> print(df[['close', 'KDJ_K', 'KDJ_D', 'KDJ_J']].tail())
    """
    required_cols = ['high', 'low', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"DataFrame缺少必要列: {col}")
    
    df = df.copy()
    
    # 计算N日内的最高最低价
    low_list = df['low'].rolling(window=n_period, min_periods=1).min()
    high_list = df['high'].rolling(window=n_period, min_periods=1).max()
    
    # 计算RSV
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    rsv = rsv.fillna(50)  # 处理除零情况
    
    # 计算K值（平滑移动平均）
    # K = 2/3 * 昨日K + 1/3 * 当日RSV
    k = pd.Series(index=df.index, dtype=float)
    k.iloc[0] = 50  # 初始值
    
    for i in range(1, len(df)):
        k.iloc[i] = (2/3) * k.iloc[i-1] + (1/3) * rsv.iloc[i]
    
    df['KDJ_K'] = k
    
    # 计算D值（K的平滑移动平均）
    # D = 2/3 * 昨日D + 1/3 * 当日K
    d = pd.Series(index=df.index, dtype=float)
    d.iloc[0] = 50  # 初始值
    
    for i in range(1, len(df)):
        d.iloc[i] = (2/3) * d.iloc[i-1] + (1/3) * k.iloc[i]
    
    df['KDJ_D'] = d
    
    # 计算J值
    # J = 3K - 2D
    df['KDJ_J'] = 3 * df['KDJ_K'] - 2 * df['KDJ_D']
    
    # 金叉死叉信号
    df['KDJ_golden_cross'] = (df['KDJ_K'] > df['KDJ_D']) & \
                             (df['KDJ_K'].shift(1) <= df['KDJ_D'].shift(1))
    
    df['KDJ_death_cross'] = (df['KDJ_K'] < df['KDJ_D']) & \
                            (df['KDJ_K'].shift(1) >= df['KDJ_D'].shift(1))
    
    # 超买超卖信号
    df['KDJ_overbought'] = df['KDJ_K'] > 80
    df['KDJ_oversold'] = df['KDJ_K'] < 20
    df['KDJ_extreme_overbought'] = df['KDJ_J'] > 100
    df['KDJ_extreme_oversold'] = df['KDJ_J'] < 0
    
    return df


def analyze_kdj(df: pd.DataFrame) -> dict:
    """
    分析KDJ指标状态
    
    Args:
        df: 包含KDJ计算的DataFrame
        
    Returns:
        dict: KDJ分析结果
    """
    if 'KDJ_K' not in df.columns or 'KDJ_D' not in df.columns:
        raise ValueError("DataFrame中不存在KDJ列，请先调用calculate_kdj()")
    
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    analysis = {
        'k': round(latest['KDJ_K'], 2),
        'd': round(latest['KDJ_D'], 2),
        'j': round(latest['KDJ_J'], 2),
        'trend': '偏多' if latest['KDJ_K'] > latest['KDJ_D'] else '偏空',
        'zone': None,
        'signal': None,
        'strength': '弱'
    }
    
    # 判断区域
    if latest['KDJ_J'] > 100:
        analysis['zone'] = '严重超买'
        analysis['signal'] = '卖出信号'
    elif latest['KDJ_K'] > 80:
        analysis['zone'] = '超买区'
        analysis['signal'] = '谨慎'
    elif latest['KDJ_J'] < 0:
        analysis['zone'] = '严重超卖'
        analysis['signal'] = '买入信号'
    elif latest['KDJ_K'] < 20:
        analysis['zone'] = '超卖区'
        analysis['signal'] = '关注'
    else:
        analysis['zone'] = '震荡区'
        analysis['signal'] = '观望'
    
    # 金叉死叉判断
    if latest['KDJ_golden_cross']:
        analysis['cross_signal'] = '金叉买入'
        if latest['KDJ_K'] < 50:
            analysis['strength'] = '强'
    elif latest['KDJ_death_cross']:
        analysis['cross_signal'] = '死叉卖出'
        if latest['KDJ_K'] > 50:
            analysis['strength'] = '强'
    else:
        analysis['cross_signal'] = None
    
    # J值偏离度
    j_deviation = abs(latest['KDJ_J'] - 50)
    if j_deviation > 50:
        analysis['j_deviation'] = '极端'
    elif j_deviation > 30:
        analysis['j_deviation'] = '显著'
    else:
        analysis['j_deviation'] = '正常'
    
    return analysis
