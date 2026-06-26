#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一评分系统 v3.0
====================
将「趋势启动评分」和「卖出信号评分」合并为一套评分。

设计原则：
- 满分 100，只有一个分数
- 基础分（0-85）：技术面强度 → 越高越好
- 调整项（±15）：持仓风险 → 扣分项
- 分数越高越好，方向明确

评分档位：
  ≥85  🔥 强烈看多（买入信号）
  70-84 🟢 看多（持有/关注）
  50-69 🟡 中性（谨慎观望）
  35-49 🟠 偏弱（减仓/止损）
  <35   🔴 看空（止损/回避）
"""

import numpy as np
import pandas as pd


def calc_unified_score(df, buy_price=None):
    """
    统一评分 v3.0
    
    基础分（技术面强度）：
      MACD动能    : 0-25分
      均线结构    : 0-20分
      RSI强度     : 0-20分
      量价配合    : 0-20分
      ─────────────
      基础分合计  : 0-85分
    
    调整项（持仓风险，有买入价才计算）：
      从高点回落  : -5 ~ -15分
      浮亏        : -3 ~ -15分
      ─────────────
      最终得分    : 0-100分
    
    参数:
        df: K线数据（含指标，由 add_indicators 生成）
        buy_price: 买入价格（可选，有则计算持仓风险）
    
    返回:
        dict: 包含分数、描述、档位、扣分原因
    """
    if df is None or len(df) < 25:
        return None

    last = df.iloc[-1]
    prev3 = df.iloc[-4:-1]
    prev5 = df.iloc[-6:-1]
    prev10 = df.iloc[-11:-1]

    close = last['close']
    ma5 = last['ma5']
    ma10 = last['ma10']
    ma20 = last['ma20']
    rsi = last['rsi']
    hist = last['hist']
    dif = last['dif']
    dea = last['dea']
    vol_ratio = last['vol_ratio']
    boll_pos = last['boll_pos']

    # ─────────────────────────────────────────
    # ⭐ 新增：超跌关注信号检测 (独立于基础分之外)
    # 条件：RSI < 48（从45放宽到48，更灵敏捕捉底部）
    # ─────────────────────────────────────────
    oversold_signal = False
    oversold_bonus = 0
    if rsi < 48 and dif > dea and hist > 0:
        oversold_signal = True
        rsi_gap = 48 - rsi        # RSI=43时gap=5，RSI=38时gap=10，RSI=30时gap=18
        if rsi_gap >= 18 and rsi < 32:
            oversold_bonus = 12   # 极超跌（RSI<32）
        elif rsi_gap >= 10:
            oversold_bonus = 8    # 明显超跌（RSI 32-38）
        elif rsi_gap >= 5:
            oversold_bonus = 5    # 轻度超跌（RSI 38-43）
        elif rsi_gap >= 2:
            oversold_bonus = 3    # 刚刚进入超跌（RSI 43-46）

    # ─────────────────────────────────────────
    # 基础分 Part 1：MACD动能 (0-25)
    # ─────────────────────────────────────────
    macd_base = 0

    # A1. MACD柱线强度 (0-10)
    hist_max = df['hist'].rolling(20).max().iloc[-1]
    if hist > 0:
        ratio = hist / (hist_max + 1e-9)
        if ratio > 0.7:
            macd_base += 10
        elif ratio > 0.3:
            macd_base += 7
        else:
            macd_base += 4
    # 0 if hist <= 0

    # A2. MACD柱线动能：当前hist vs 5日均值 (0-10)
    # 旧方法"连续N天上升"同样太敏感
    # 新方法：hist高于5日均值=MACD动能增强
    hist_5d = prev5['hist'].dropna().values
    if len(hist_5d) >= 3 and hist > 0:
        hist_avg5 = np.mean(hist_5d)
        if hist_avg5 > 0:
            hist_ratio = hist / hist_avg5  # 当前hist / 5日均值
            if hist_ratio > 2.0:
                macd_base += 10  # 动能暴增
            elif hist_ratio > 1.5:
                macd_base += 8   # 动能明显增强
            elif hist_ratio > 1.2:
                macd_base += 6   # 动能温和增强
            elif hist_ratio > 1.0:
                macd_base += 4   # 动能略增
            else:
                macd_base += 2   # 动能减弱但仍为正
        else:
            macd_base += 6   # 5日均值为负但当前为正→转强

    # A3. DIF 在 DEA 上方 (0-5)
    if dif > dea:
        macd_base += 5

    macd_score = min(macd_base, 25)

    # ─────────────────────────────────────────
    # 基础分 Part 2：均线结构 (0-20)
    # ─────────────────────────────────────────
    ma_base = 0

    # B1. 价格与 MA20 的关系 (0-8)
    if close > ma20:
        dist_pct = (close - ma20) / ma20 * 100
        if 1 <= dist_pct <= 8:
            ma_base += 8    # 刚突破，最佳位置
        elif dist_pct < 1:
            ma_base += 5    # 紧贴 MA20
        elif dist_pct <= 15:
            ma_base += 4    # 已涨一段
        else:
            ma_base += 1    # 涨太多，追高风险
    else:
        ma_base += 0

    # B2. 均线多头排列 (0-7)
    if ma5 > ma10 > ma20:
        gap1 = (ma5 - ma10) / ma10 * 100
        gap2 = (ma10 - ma20) / ma20 * 100
        if gap1 > 0.5 and gap2 > 0.5:
            ma_base += 7
        else:
            ma_base += 4
    elif ma5 > ma10:
        ma_base += 2
    # else 0

    # B3. MA5 上升斜率 (0-5)
    ma5_vals = prev5['ma5'].dropna().values
    if len(ma5_vals) >= 3:
        slope = np.polyfit(np.arange(len(ma5_vals)), ma5_vals, 1)[0]
        slope_pct = slope / ma5_vals[-1] * 100
        if slope_pct > 0.3:
            ma_base += 5
        elif slope_pct > 0.1:
            ma_base += 3
        elif slope_pct > 0:
            ma_base += 1

    ma_score = min(ma_base, 20)

    # ─────────────────────────────────────────
    # 基础分 Part 3：RSI 强度 (0-20)
    # ─────────────────────────────────────────
    rsi_base = 0

    # C1. RSI 绝对值 (0-15) —— 重构：识别趋势阶段
    if 45 <= rsi < 55:
        rsi_base += 14  # ★ 启动期：即将启动/刚启动，上涨空间大
    elif 55 <= rsi <= 68:
        rsi_base += 10  # 最佳区间：强势不过热
    elif 50 <= rsi < 55:
        rsi_base += 8
    elif 40 <= rsi < 45:
        rsi_base += 12  # 超跌蓄力区，反弹空间大
    elif 30 <= rsi < 40:
        rsi_base += 14  # 深超卖，即将/正在反弹
    elif rsi < 30:
        rsi_base += 15  # 极超卖，极佳买点
    elif 68 < rsi <= 75:
        rsi_base += 4   # 偏热，追高风险
    elif rsi > 75:
        rsi_base += 1   # 过热，高风险

    # C2. RSI 动能：当前RSI vs 5日均值 (0-10)
    rsi_5d = prev5['rsi'].dropna().values
    if len(rsi_5d) >= 3:
        rsi_avg5 = np.mean(rsi_5d)
        rsi_diff = rsi - rsi_avg5
        if rsi_diff > 10:
            rsi_base += 10   # 强势上攻
        elif rsi_diff > 5:
            rsi_base += 8    # 上升动能明确
        elif rsi_diff > 2:
            rsi_base += 6    # 温和上升
        elif rsi_diff > 0:
            rsi_base += 4    # 微弱上升
        elif rsi_diff > -2:
            rsi_base += 2    # 基本持平
        elif rsi_diff >= -5:
            rsi_base += 1    # 略弱但正常

    rsi_score = min(rsi_base, 20)

    # ─────────────────────────────────────────
    # 基础分 Part 4：量价配合 (0-20)
    # ─────────────────────────────────────────
    vol_base = 0

    # D1. 量比 (0-10)
    if 1.5 <= vol_ratio <= 3.0:
        vol_base += 10
    elif 1.2 <= vol_ratio < 1.5:
        vol_base += 7
    elif 1.0 <= vol_ratio < 1.2:
        vol_base += 4
    elif vol_ratio > 3.0:
        vol_base += 2   # 过度放量
    # else 0 缩量

    # D2. 价涨量增（近5天）(0-10)
    price_up_days = 0
    price_vol_match = 0
    if len(prev5) >= 3:
        for i in range(1, len(prev5)):
            price_up = prev5['close'].iloc[i] > prev5['close'].iloc[i - 1]
            vol_up = prev5['volume'].iloc[i] > prev5['volume'].iloc[i - 1]
            if price_up:
                price_up_days += 1
            if price_up and vol_up:
                price_vol_match += 1
        match_ratio = price_vol_match / max(price_up_days, 1)
        if match_ratio >= 0.8:
            vol_base += 10
        elif match_ratio >= 0.6:
            vol_base += 7
        elif match_ratio >= 0.4:
            vol_base += 4
        else:
            vol_base += 0

    vol_score = min(vol_base, 20)

    # ─────────────────────────────────────────
    # 基础分合计（0-85）+ 超跌加成
    # ─────────────────────────────────────────
    base_score = macd_score + ma_score + rsi_score + vol_score + oversold_bonus

    # ─────────────────────────────────────────
    # 调整项：持仓风险（有买入价才计算）(±15)
    # ─────────────────────────────────────────
    adjustments = []
    adj_total = 0

    if buy_price:
        # 1. 从高点回落
        high_10 = df['high'].tail(10).max()
        high_20 = df['high'].tail(20).max()
        drop_10 = (close - high_10) / high_10 * 100
        drop_20 = (close - high_20) / high_20 * 100

        if drop_10 <= -8:
            adjustments.append(f'距10日高点仅-{abs(drop_10):.0f}%，强势' if drop_10 > -2 else f'从10日高点回落 {abs(drop_10):.0f}%，减-5')
            if drop_10 < -5:
                adj_total -= 5
        if drop_20 <= -12:
            adjustments.append(f'从20日高点回落 {abs(drop_20):.0f}%，减-10')
            adj_total -= 10
        elif drop_20 <= -8:
            adjustments.append(f'从20日高点回落 {abs(drop_20):.0f}%，减-5')
            adj_total -= 5

        # 2. 浮亏
        profit_pct = (close - buy_price) / buy_price * 100
        if profit_pct < -10:
            adjustments.append(f'浮亏 {profit_pct:.1f}%，止损信号，减-15')
            adj_total -= 15
        elif profit_pct < -7:
            adjustments.append(f'浮亏 {profit_pct:.1f}%，减-10')
            adj_total -= 10
        elif profit_pct < -5:
            adjustments.append(f'浮亏 {profit_pct:.1f}%，减-5')
            adj_total -= 5
        elif profit_pct > 20:
            adjustments.append(f'获利 {profit_pct:.0f}%，注意止盈，减-3')
            adj_total -= 3
        elif profit_pct > 15:
            adjustments.append(f'获利 {profit_pct:.0f}%，减-1')
            adj_total -= 1

        # 3. 跌破均线（有持仓时更敏感）
        if close < ma10:
            adjustments.append(f'跌破MA10，减-5')
            adj_total -= 5
        elif close < ma5:
            adjustments.append(f'跌破MA5，减-2')
            adj_total -= 2

        # 4. 量价背离（有持仓时减分）
        if len(prev5) >= 3:
            recent_vol = prev5['volume'].tail(3).mean()
            early_vol = prev5['volume'].head(3).mean()
            vol_trend = (recent_vol - early_vol) / early_vol * 100 if early_vol > 0 else 0
            price_trend = (close - prev5['close'].iloc[0]) / prev5['close'].iloc[0] * 100
            if price_trend > 0 and vol_trend < -30:
                adjustments.append(f'价涨量缩({vol_trend:.0f}%)，减-5')
                adj_total -= 5

    # ─────────────────────────────────────────
    # 最终得分（0-100）
    # ─────────────────────────────────────────
    base_for_final = macd_score + ma_score + rsi_score + vol_score  # 不含超跌加成
    final_score = max(0, min(100, base_for_final + adj_total + oversold_bonus))

    # ─────────────────────────────────────────
    # 信号类型 + 档位判断
    # ─────────────────────────────────────────
    # 阶段标注：判断追高风险
    if rsi < 40:
        rsi_stage = '极超跌'
    elif rsi < 48:
        rsi_stage = '超跌'
    elif rsi < 55:
        rsi_stage = '启动'  # ★ 最佳买点区间
    elif rsi <= 68:
        rsi_stage = '趋势'
    elif rsi <= 75:
        rsi_stage = '偏热'
    else:
        rsi_stage = '过热'

    # 基础信号类型
    if rsi < 50 and hist > 0:
        # RSI弱势 + MACD转正 = 超跌信号
        signal_type = '超跌关注'
        level = '超跌关注'
        emoji = '🔵'
    elif rsi < 50 and hist <= 0:
        signal_type = '弱势未企稳'
        level = '弱势'
        emoji = '🔴'
    elif rsi_stage in ('偏热', '过热'):
        signal_type = '高位风险' if rsi_stage == '过热' else '谨慎追高'
        level = '偏热' if rsi_stage == '偏热' else '过热'
        emoji = '🟡' if rsi_stage == '偏热' else '🔴'
    elif final_score >= 85:
        signal_type = '强烈看多'
        level = '强烈看多'
        emoji = '🔥'
    elif final_score >= 70:
        signal_type = '看多'
        level = '看多'
        emoji = '🟢'
    elif final_score >= 50:
        signal_type = '中性'
        level = '中性'
        emoji = '🟡'
    elif final_score >= 35:
        signal_type = '偏弱'
        level = '偏弱'
        emoji = '🟠'
    else:
        signal_type = '看空'
        level = '看空'
        emoji = '🔴'

    return {
        'final_score': final_score,
        'base_score': base_score,
        'adj_total': adj_total,
        'level': level,
        'emoji': emoji,
        'signal_type': signal_type,
        'oversold_signal': oversold_signal,
        'oversold_bonus': oversold_bonus,
        'rsi_stage': rsi_stage,  # 新增：阶段标注（极超跌/超跌/启动/趋势/偏热/过热）
        'macd_score': macd_score,
        'ma_score': ma_score,
        'rsi_score': rsi_score,
        'vol_score': vol_score,
        'close': round(float(close), 2),
        'buy_price': round(float(buy_price), 2) if buy_price else None,
        'profit_pct': round(float((close - buy_price) / buy_price * 100), 2) if buy_price else None,
        'rsi': round(float(rsi), 1),
        'macd_hist': round(float(hist), 4),
        'ma5': round(float(ma5), 2),
        'ma10': round(float(ma10), 2),
        'ma20': round(float(ma20), 2),
        'vol_ratio': round(float(vol_ratio), 2),
        'boll_pos': round(float(boll_pos), 2),
        'gain_5d': round(float((close / df.iloc[-6]['close'] - 1) * 100), 2) if len(df) >= 6 else 0,
        'gain_10d': round(float((close / df.iloc[-11]['close'] - 1) * 100), 2) if len(df) >= 11 else 0,
        'adjustments': adjustments,
        'reason': _build_reason(last, prev5, df, buy_price),
        # 兼容旧显示格式的列
        'ma_bullish': 1 if ma5 > ma10 > ma20 else 0,
        'macd_hist_pos': 1 if hist > 0 else 0,
        'above_ma20': 1 if close > ma20 else 0,
        'rsi_rising': 1 if (len(prev5) >= 1 and rsi > prev5['rsi'].dropna().values[-1]) else 0,
        'rsi_above50': 1 if rsi > 50 else 0,
        'price_rising': 1 if (len(prev5) >= 3 and slope > 0) else 0,
        'macd_hist_rising': 1 if (len(prev5) >= 1 and hist > prev5['hist'].dropna().values[-1]) else 0,
    }


def _build_reason(last, prev5, df, buy_price):
    """生成简明判断理由"""
    reasons = []
    close = last['close']
    hist = last['hist']
    rsi = last['rsi']
    ma5 = last['ma5']
    ma10 = last['ma10']
    ma20 = last['ma20']

    # 利好信号
    if hist > 0:
        reasons.append('MACD柱线为正')
    if close > ma20 and close > ma10 and close > ma5:
        reasons.append('三线多头')
    if rsi > 50 and rsi > prev5['rsi'].iloc[0]:
        reasons.append('RSI上升')
    if last['vol_ratio'] >= 1.5:
        reasons.append('量能放大')

    # 风险信号
    if close < ma20:
        reasons.append('跌破MA20')
    if close < ma10:
        reasons.append('跌破MA10')
    if rsi > 70:
        reasons.append('RSI超买')
    if hist < 0:
        reasons.append('MACD柱线为负')

    if buy_price:
        profit = (close - buy_price) / buy_price * 100
        if profit < -5:
            reasons.append(f'浮亏{profit:.1f}%')
        elif profit > 10:
            reasons.append(f'获利{profit:.0f}%')

    return '，'.join(reasons) if reasons else '技术面中性'


def format_unified_report(score_data, code=None, name=None):
    """格式化统一评分报告"""
    if score_data is None:
        return f"{code or ''} {name or ''}: 数据不足，无法评分"

    fs = score_data['final_score']
    bs = score_data['base_score']
    adj = score_data['adj_total']
    emoji = score_data['emoji']
    signal_type = score_data['signal_type']

    name_str = f"{code} {name}" if code or name else ''
    header = f"{emoji} {name_str} {signal_type} {fs}分"
    if score_data['buy_price']:
        profit = score_data['profit_pct']
        profit_str = f'+{profit:.1f}%' if profit > 0 else f'{profit:.1f}%'
        header += f" | 持仓{profit_str}"

    lines = [header]
    lines.append(f"  ─── 基础分 {bs}分 ───")
    lines.append(f"  MACD动能  {score_data['macd_score']:>2}/25")
    lines.append(f"  均线结构  {score_data['ma_score']:>2}/20")
    lines.append(f"  RSI强度   {score_data['rsi_score']:>2}/20")
    lines.append(f"  量价配合  {score_data['vol_score']:>2}/20")

    if score_data.get('oversold_signal'):
        lines.append(f"  ⭐ 超跌加成 +{score_data['oversold_bonus']}分 (RSI={score_data['rsi']:.1f}，底部信号)")

    if score_data['buy_price']:
        adj_str = f'{adj:+d}分' if adj != 0 else '无调整'
        lines.append(f"  ─── 持仓调整 {adj_str} ───")
        for adj_reason in score_data['adjustments']:
            lines.append(f"  {adj_reason}")

    lines.append(f"  ──────────────")
    lines.append(f"  总分: {fs}分  [{score_data['level']}]")
    lines.append(f"  现价: {score_data['close']} | RSI: {score_data['rsi']} | MA20: {score_data['ma20']}")
    lines.append(f"  5日涨幅: {score_data['gain_5d']:+.1f}% | 10日涨幅: {score_data['gain_10d']:+.1f}%")
    lines.append(f"  判断: {score_data['reason']}")

    return '\n'.join(lines)


if __name__ == '__main__':
    print("统一评分系统 v3.0 加载成功")
    print("使用方法: calc_unified_score(df, buy_price)")
    print("buy_price 有值时计算持仓风险调整，无值时只返回技术面基础分")
