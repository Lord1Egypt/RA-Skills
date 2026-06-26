#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""卖出信号分析模块
分析已买入股票的卖出时机
"""

import pandas as pd
import numpy as np

def calc_sell_score(df, buy_price=None, buy_date=None):
    """
    计算卖出信号评分
    
    参数:
        df: K线数据（需包含指标）
        buy_price: 买入价格（可选，用于计算收益）
        buy_date: 买入日期（可选，用于计算持有天数）
    
    返回:
        dict: 卖出评分和信号详情
    """
    if df is None or len(df) < 20:
        return None
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    # ========== 卖出信号评分 ==========
    sell_signals = []
    warning_signals = []
    hold_signals = []
    
    total_score = 0  # 卖出倾向得分（越高越该卖）
    
    # 1. MACD死叉信号（权重最高）
    macd_hist = latest.get('macd_hist', 0)
    macd_hist_prev = prev.get('macd_hist', 0)
    
    if macd_hist < 0 and macd_hist_prev > 0:
        # MACD柱线由正转负（死叉）
        sell_signals.append(('MACD死叉', 25))
        total_score += 25
    elif macd_hist < 0:
        # MACD柱线持续为负
        sell_signals.append(('MACD柱线为负', 15))
        total_score += 15
    elif macd_hist > 0 and macd_hist < macd_hist_prev * 0.5:
        # MACD柱线快速萎缩
        warning_signals.append(('MACD动能衰减', 10))
        total_score += 10
    
    # 2. 均线破位信号
    close = latest['close']
    ma5 = latest.get('ma5', close)
    ma10 = latest.get('ma10', close)
    ma20 = latest.get('ma20', close)
    
    if close < ma20:
        sell_signals.append(('跌破MA20', 20))
        total_score += 20
    elif close < ma10:
        warning_signals.append(('跌破MA10', 10))
        total_score += 10
    elif close < ma5:
        warning_signals.append(('跌破MA5', 5))
        total_score += 5
    
    # 3. RSI超买回落信号
    rsi = latest.get('rsi', 50)
    rsi_prev = prev.get('rsi', 50)
    
    if rsi > 80:
        sell_signals.append(('RSI严重超买(>80)', 15))
        total_score += 15
    elif rsi > 70 and rsi < rsi_prev:
        # RSI从超买区回落
        sell_signals.append(('RSI超买回落', 12))
        total_score += 12
    elif rsi > 70:
        warning_signals.append(('RSI超买(>70)', 8))
        total_score += 8
    
    # 4. 量价背离信号
    volume = latest.get('volume', 0)
    vol_ma5 = df['volume'].tail(5).mean() if 'volume' in df.columns else volume
    
    # 检查最近5日走势
    recent_close = df['close'].tail(5)
    recent_volume = df['volume'].tail(5)
    
    # 价涨量缩
    if recent_close.iloc[-1] > recent_close.iloc[0]:
        avg_vol_recent = recent_volume.tail(3).mean()
        avg_vol_early = recent_volume.head(3).mean()
        if avg_vol_recent < avg_vol_early * 0.7:
            sell_signals.append(('价涨量缩(量价背离)', 15))
            total_score += 15
    
    # 放量滞涨
    if volume > vol_ma5 * 1.5:
        # 放量但涨幅小
        if abs(latest['close'] - prev['close']) / prev['close'] < 0.02:
            sell_signals.append(('放量滞涨', 12))
            total_score += 12
    
    # 5. 趋势破坏信号
    # 检查最近N日最高价
    high_10 = df['high'].tail(10).max()
    high_20 = df['high'].tail(20).max()
    
    if close < high_10 * 0.95:
        # 从10日高点回落超过5%
        warning_signals.append(('从高点回落>5%', 8))
        total_score += 8
    
    if close < high_20 * 0.90:
        # 从20日高点回落超过10%
        sell_signals.append(('从高点回落>10%', 15))
        total_score += 15
    
    # 6. 持有收益信号（如果有买入价）
    profit_pct = None
    hold_days = None
    
    if buy_price:
        profit_pct = (close - buy_price) / buy_price * 100
        
        if profit_pct > 20:
            sell_signals.append(('获利>20%', 10))
            total_score += 10
        elif profit_pct > 15:
            warning_signals.append(('获利>15%', 5))
            total_score += 5
        elif profit_pct < -10:
            sell_signals.append(('止损触发(-10%)', 25))
            total_score += 25
        elif profit_pct < -5:
            warning_signals.append(('浮亏>5%', 10))
            total_score += 10
    
    if buy_date:
        try:
            buy_dt = pd.to_datetime(buy_date)
            latest_dt = pd.to_datetime(latest['date'])
            hold_days = (latest_dt - buy_dt).days
        except:
            pass
    
    # ========== 综合判断 ==========
    if total_score >= 40:
        action = '🔴 建议卖出'
        action_score = total_score
    elif total_score >= 25:
        action = '🟡 警惕风险'
        action_score = total_score
    else:
        action = '🟢 继续持有'
        action_score = total_score
    
    return {
        'action': action,
        'sell_score': total_score,
        'sell_signals': sell_signals,
        'warning_signals': warning_signals,
        'hold_signals': hold_signals,
        'close': close,
        'rsi': round(rsi, 1),
        'macd_hist': round(macd_hist, 4) if macd_hist else 0,
        'ma20': round(ma20, 2),
        'profit_pct': round(profit_pct, 2) if profit_pct else None,
        'hold_days': hold_days,
        'buy_price': buy_price
    }


def analyze_portfolio(portfolio, df_dict):
    """
    分析持仓组合的卖出信号
    
    参数:
        portfolio: list of dict, [{'code': '000001', 'name': '平安银行', 'buy_price': 10.5, 'buy_date': '2026-04-01'}, ...]
        df_dict: dict, {code: DataFrame}
    
    返回:
        list: 每只股票的卖出分析结果
    """
    results = []
    
    for stock in portfolio:
        code = stock['code']
        name = stock.get('name', code)
        buy_price = stock.get('buy_price')
        buy_date = stock.get('buy_date')
        
        df = df_dict.get(code)
        if df is None:
            results.append({
                'code': code,
                'name': name,
                'error': '无K线数据'
            })
            continue
        
        # 添加指标
        df = add_indicators(df)
        result = calc_sell_score(df, buy_price, buy_date)
        
        if result:
            result['code'] = code
            result['name'] = name
            results.append(result)
    
    # 按卖出评分排序
    results.sort(key=lambda x: x.get('sell_score', 0), reverse=True)
    
    return results


def add_indicators(df):
    """添加技术指标"""
    if df is None or len(df) < 20:
        return df
    
    df = df.copy()
    
    # 均线
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # MACD
    ema12 = df['close'].ewm(span=12).mean()
    ema26 = df['close'].ewm(span=26).mean()
    df['macd'] = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']
    
    return df


def format_sell_report(result):
    """格式化卖出分析报告"""
    if not result:
        return "无分析结果"
    
    if 'error' in result:
        return f"{result['code']} {result['name']}: {result['error']}"
    
    lines = []
    lines.append(f"**{result['code']} {result['name']}**")
    lines.append(f"操作建议: {result['action']}")
    lines.append(f"卖出评分: {result['sell_score']}分")
    lines.append(f"现价: {result['close']}元 | RSI: {result['rsi']} | MA20: {result['ma20']}")
    
    if result.get('profit_pct') is not None:
        profit_str = f"+{result['profit_pct']}%" if result['profit_pct'] > 0 else f"{result['profit_pct']}%"
        lines.append(f"持有收益: {profit_str}")
        if result.get('hold_days'):
            lines.append(f"持有天数: {result['hold_days']}天")
    
    if result['sell_signals']:
        lines.append("\n🔴 卖出信号:")
        for signal, score in result['sell_signals']:
            lines.append(f"  - {signal} (+{score}分)")
    
    if result['warning_signals']:
        lines.append("\n🟡 警告信号:")
        for signal, score in result['warning_signals']:
            lines.append(f"  - {signal} (+{score}分)")
    
    return '\n'.join(lines)


# 测试
if __name__ == '__main__':
    print("卖出信号分析模块已加载")
    print("使用方法:")
    print("1. 单股分析: calc_sell_score(df, buy_price, buy_date)")
    print("2. 持仓分析: analyze_portfolio(portfolio, df_dict)")
