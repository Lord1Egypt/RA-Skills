"""
动量形态识别引擎 V1.0
12种形态：6持有 + 5预警 + 4卖出
纯量价逻辑，每个形态独立检测函数
"""

from typing import List, Dict, Optional, Tuple
import math
from utils import sma

# ─── 通用工具函数 ───

def _max_idx(arr: List[float]) -> int:
    return max(range(len(arr)), key=lambda i: arr[i])

def _min_idx(arr: List[float]) -> int:
    return min(range(len(arr)), key=lambda i: arr[i])


# ═══════════════════════════════════════════
#  M1 底部启动加速 🚀
# ═══════════════════════════════════════════

def detect_m1_bottom_breakout(kline: List[dict], params: dict = None) -> dict:
    """
    长期低量→底部启动加速，两种路径：
    路径A：连续3日放量阳线+收盘逐日抬高+站上MA20
    路径B：近5日4日阳线+最后一日放量突破MA20（底部温和反转）
    """
    p = params or {}
    window = p.get('window', 20)
    ma_trend = p.get('ma_trend', 60)
    vol_ratio_min = p.get('vol_ratio_min', 1.5)
    
    if len(kline) < ma_trend + 5:
        return {'hit': False, 'name': 'M1底部启动加速', 'tag': '🚀', 'type': 'hold'}
    
    closes = [k['close'] for k in kline]
    opens = [k['open'] for k in kline]
    vols = [k['volume'] for k in kline]
    ma60 = sma(closes, ma_trend)
    n = len(kline)
    
    # ═══ 路径A：严格3连阳 ═══
    for i in range(n-3, n-window-3, -1):
        pre_gain = (closes[i] - closes[max(0, i-window)]) / closes[max(0, i-window)] * 100
        if pre_gain > 5:
            continue
        
        if not (closes[i] > opens[i] and closes[i+1] > opens[i+1] and closes[i+2] > opens[i+2]):
            continue
        if not (closes[i+2] > closes[i+1] > closes[i]):
            continue
        if not (vols[i+2] > vols[i+1] > vols[i]):
            continue
        
        ma20 = sma(closes[:(i+3)], 20)
        if closes[i+2] <= ma20[-1]:
            continue
        
        avg_vol = sum(vols[max(0,i-20):i]) / min(20, i)
        if vols[i+2] < avg_vol * vol_ratio_min:
            continue
        
        bonus = 0
        if closes[i+2] > ma60[i+2]:
            bonus += 3
        if opens[i+2] > closes[i+1]:
            bonus += 2
        if abs(closes[i+2] - kline[i+2]['high']) < 0.01 * closes[i+2]:
            bonus += 1
        
        ma_status = '突破MA60+MA20' if closes[i+2] > ma60[i+2] else '站上MA20'
        return {
            'hit': True, 'name': 'M1底部启动加速', 'tag': '🚀', 'type': 'hold',
            'score_base': 15 + bonus, 'anchor_date': kline[i+2]['date'],
            'detail': f'连续3日放量阳线+{ma_status}，放量日{kline[i+2]["date"]}'
        }
    
    # ═══ 路径B：5日4阳，温和反转 ═══
    bullish_count = sum(1 for j in range(n-5, n) if closes[j] > opens[j])
    if bullish_count < 4:
        return {'hit': False, 'name': 'M1底部启动加速', 'tag': '🚀', 'type': 'hold'}
    
    # 5日累计涨幅 > 3% 且最后一日为阳线
    if closes[-1] <= opens[-1]:
        return {'hit': False, 'name': 'M1底部启动加速', 'tag': '🚀', 'type': 'hold'}
    
    gain_5 = (closes[-1] - closes[-5]) / closes[-5] * 100
    if gain_5 <= 3:
        return {'hit': False, 'name': 'M1底部启动加速', 'tag': '🚀', 'type': 'hold'}
    
    # 最后一日突破MA20
    ma20 = sma(closes, 20)
    if closes[-1] <= ma20[-1]:
        return {'hit': False, 'name': 'M1底部启动加速', 'tag': '🚀', 'type': 'hold'}
    
    # 放量确认：近3日峰值>前5-15日基线1.5倍，或最后一日>近5日均量1.3倍
    baseline_vol = sum(vols[max(0,n-15):n-5]) / min(10, n-5 - max(0, n-15)) if n > 15 else sum(vols[:-5]) / max(1, n-5)
    max_vol_recent = max(vols[-3:]) if len(vols) >= 3 else vols[-1]
    avg_vol_5 = sum(vols[-6:-1]) / 5 if n >= 6 else max_vol_recent
    
    if not (max_vol_recent > baseline_vol * 1.5 or vols[-1] > avg_vol_5 * 1.3):
        return {'hit': False, 'name': 'M1底部启动加速', 'tag': '🚀', 'type': 'hold'}
    
    # 前置底部确认
    pre_gain = (closes[-6] - closes[max(0, n-26)]) / closes[max(0, n-26)] * 100
    if pre_gain > 15:
        return {'hit': False, 'name': 'M1底部启动加速', 'tag': '🚀', 'type': 'hold'}
    
    bonus = 0
    if closes[-1] > ma60[-1]:
        bonus += 3
    if gain_5 > 8:
        bonus += 1
    
    ma_status = '突破MA60+MA20' if closes[-1] > ma60[-1] else '站上MA20'
    return {
        'hit': True, 'name': 'M1底部启动加速', 'tag': '🚀', 'type': 'hold',
        'score_base': 13 + bonus, 'anchor_date': kline[-1]['date'],
        'detail': f'5日4阳温和反转+{ma_status}(+{gain_5:.1f}%)，突破日{kline[-1]["date"]}'
    }


# ═══════════════════════════════════════════
#  M2 均线多头发散 📈
# ═══════════════════════════════════════════

def detect_m2_bullish_alignment(kline: List[dict], params: dict = None) -> dict:
    """
    MA5>MA10>MA20>MA60，量能温和放大，沿MA5上行
    """
    p = params or {}
    
    if len(kline) < 60:
        return {'hit': False, 'name': 'M2均线多头发散', 'tag': '📈', 'type': 'hold'}
    
    closes = [k['close'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    ma5 = sma(closes, 5)
    ma10 = sma(closes, 10)
    ma20 = sma(closes, 20)
    ma60 = sma(closes, 60)
    
    # 严格多头排列
    if not (ma5[-1] > ma10[-1] > ma20[-1] > ma60[-1]):
        return {'hit': False, 'name': 'M2均线多头发散', 'tag': '📈', 'type': 'hold'}
    
    # 价格沿MA5上行（近5日中≥4日收于MA5之上）
    above_ma5_count = sum(1 for i in range(n-5, n) if closes[i] > ma5[i])
    if above_ma5_count < 4:
        return {'hit': False, 'name': 'M2均线多头发散', 'tag': '📈', 'type': 'hold'}
    
    # 量能温和放大
    vol_recent_5 = sum(vols[-5:]) / 5
    vol_prev_20 = sum(vols[-25:-5]) / 20
    if vol_recent_5 < vol_prev_20:
        return {'hit': False, 'name': 'M2均线多头发散', 'tag': '📈', 'type': 'hold'}
    
    bonus = 0
    if (ma5[-1] - ma10[-1]) > (ma5[-6] - ma10[-6]):
        bonus += 2
    if (ma10[-1] - ma20[-1]) > (ma10[-6] - ma20[-6]):
        bonus += 1
    
    return {
        'hit': True, 'name': 'M2均线多头发散', 'tag': '📈', 'type': 'hold',
        'score_base': 13 + bonus,
        'detail': f'四线多头排列，MA5={ma5[-1]:.2f}>MA10={ma10[-1]:.2f}>MA20={ma20[-1]:.2f}>MA60={ma60[-1]:.2f}'
    }


# ═══════════════════════════════════════════
#  M3 趋势中继加速 🔥
# ═══════════════════════════════════════════

def detect_m3_trend_acceleration(kline: List[dict], params: dict = None) -> dict:
    """
    上升通道中，短暂回调不破MA10后再次放量阳线
    """
    if len(kline) < 20:
        return {'hit': False, 'name': 'M3趋势中继加速', 'tag': '🔥', 'type': 'hold'}
    
    closes = [k['close'] for k in kline]
    highs = [k['high'] for k in kline]
    lows = [k['low'] for k in kline]
    vols = [k['volume'] for k in kline]
    opens = [k['open'] for k in kline]
    n = len(kline)
    
    ma10 = sma(closes, 10)
    
    # 近20日累计涨幅 > 5%
    gain_20 = (closes[-1] - closes[-20]) / closes[-20] * 100 if n >= 20 else 0
    if gain_20 <= 5:
        return {'hit': False, 'name': 'M3趋势中继加速', 'tag': '🔥', 'type': 'hold'}
    
    # 找近5日回调低点，不破MA10
    recent_lows = lows[-5:]
    min_idx = _min_idx(recent_lows) + (n - 5)
    if lows[min_idx] < ma10[min_idx]:
        return {'hit': False, 'name': 'M3趋势中继加速', 'tag': '🔥', 'type': 'hold'}
    
    # 回调后出现放量阳线
    for i in range(min_idx + 1, n):
        body = closes[i] - opens[i]
        if body <= 0:
            continue
        avg_vol_5 = sum(vols[max(0,i-5):i]) / min(5, i)
        if vols[i] < avg_vol_5 * 1.3:
            continue
        # 突破回调前最高收盘价
        pre_high = max(highs[max(0, min_idx-3):min_idx+1])
        if closes[i] <= pre_high:
            continue
        
        # 回调缩量加分
        callback_vol = sum(vols[min_idx-2:min_idx+1]) / min(3, min_idx+1)
        peak_vol = max(vols[max(0, min_idx-10):min_idx])
        bonus = 2 if callback_vol < peak_vol * 0.5 else 0
        
        return {
            'hit': True, 'name': 'M3趋势中继加速', 'tag': '🔥', 'type': 'hold',
            'score_base': 12 + bonus,
            'anchor_date': kline[i]['date'],
            'detail': f'回调不破MA10后放量突破，加速日{kline[i]["date"]}'
        }
    
    return {'hit': False, 'name': 'M3趋势中继加速', 'tag': '🔥', 'type': 'hold'}


# ═══════════════════════════════════════════
#  M4 缩量回踩支撑 🎯
# ═══════════════════════════════════════════

def detect_m4_pullback_support(kline: List[dict], params: dict = None) -> dict:
    """
    拉升后缩量回踩MA20/MA60，触及即反弹收阳
    """
    if len(kline) < 60:
        return {'hit': False, 'name': 'M4缩量回踩支撑', 'tag': '🎯', 'type': 'hold'}
    
    closes = [k['close'] for k in kline]
    lows = [k['low'] for k in kline]
    vols = [k['volume'] for k in kline]
    opens = [k['open'] for k in kline]
    n = len(kline)
    
    ma20 = sma(closes, 20)
    ma60 = sma(closes, 60)
    
    # 此前10日有拉升（单日涨幅>3%）
    has_rally = False
    for i in range(n-10, n-1):
        chg = (closes[i] - closes[i-1]) / closes[i-1] * 100
        if chg > 3:
            has_rally = True
            break
    if not has_rally:
        return {'hit': False, 'name': 'M4缩量回踩支撑', 'tag': '🎯', 'type': 'hold'}
    
    # 近3日有回踩MA20或MA60，收阳线反弹
    for i in range(n-3, n):
        body = closes[i] - opens[i]
        if body <= 0:
            continue
        # 回踩均线（最低价接近均线）
        touch_ma20 = abs(lows[i] - ma20[i]) / ma20[i] < 0.02
        touch_ma60 = abs(lows[i] - ma60[i]) / ma60[i] < 0.02
        if not (touch_ma20 or touch_ma60):
            continue
        
        # 缩量
        avg_vol_5 = sum(vols[max(0,i-5):i]) / min(5, i)
        if vols[i] > avg_vol_5 * 0.7:
            continue
        
        bonus = 2 if lows[i] > ma20[i] else 0
        
        support_name = 'MA20' if touch_ma20 else 'MA60'
        return {
            'hit': True, 'name': 'M4缩量回踩支撑', 'tag': '🎯', 'type': 'hold',
            'score_base': 10 + bonus,
            'anchor_date': kline[i]['date'],
            'detail': f'缩量回踩{support_name}({ma20[i] if touch_ma20 else ma60[i]:.2f})不破收阳，回踩日{kline[i]["date"]}'
        }
    
    return {'hit': False, 'name': 'M4缩量回踩支撑', 'tag': '🎯', 'type': 'hold'}


# ═══════════════════════════════════════════
#  M5 上升旗形整理 🏴
# ═══════════════════════════════════════════

def detect_m5_flag_consolidation(kline: List[dict], params: dict = None) -> dict:
    """
    拉升后斜向下收敛震荡，缩量，整理幅度<拉升1/2
    """
    if len(kline) < 30:
        return {'hit': False, 'name': 'M5上升旗形整理', 'tag': '🏴', 'type': 'hold'}
    
    closes = [k['close'] for k in kline]
    highs = [k['high'] for k in kline]
    lows = [k['low'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    # 找此前拉升段（旗杆）：扩展搜索范围至n-25
    rally_gain = 0
    rally_start = n - 1
    for i in range(n-20, max(1, n-25), -1):
        if i < 5:
            continue
        gain = (closes[i] - closes[i-5]) / closes[i-5] * 100
        if gain > 10:
            rally_gain = gain
            rally_start = i
            break
    
    if rally_gain == 0:
        # 放宽：也检查单日大涨>5%
        for i in range(n-20, max(1, n-25), -1):
            chg = (closes[i] - closes[i-1]) / closes[i-1] * 100 if i > 0 else 0
            if chg > 5:
                # 用当日及前后2日构建旗杆区间
                rally_gain = (closes[min(i+2, n-1)] - closes[max(0, i-3)]) / closes[max(0, i-3)] * 100
                if rally_gain > 8:
                    rally_start = i - 2
                    break
    
    if rally_gain == 0:
        return {'hit': False, 'name': 'M5上升旗形整理', 'tag': '🏴', 'type': 'hold'}
    
    # 整理期：rally_start 之后到当前
    consol_highs = highs[rally_start:]
    consol_lows = lows[rally_start:]
    
    if len(consol_highs) < 5:
        return {'hit': False, 'name': 'M5上升旗形整理', 'tag': '🏴', 'type': 'hold'}
    
    # V1.3.5: 用线性回归斜率判断整理期高低点趋势（替代前后半均值比较）
    def _slope(arr):
        """计算线性回归斜率"""
        n_pts = len(arr)
        if n_pts < 3:
            return 0
        x_mean = (n_pts - 1) / 2
        y_mean = sum(arr) / n_pts
        num = sum((i - x_mean) * (arr[i] - y_mean) for i in range(n_pts))
        den = sum((i - x_mean) ** 2 for i in range(n_pts))
        return num / den if den != 0 else 0
    
    high_slope = _slope(consol_highs)
    low_slope = _slope(consol_lows)
    
    # 旗形整理：高点和低点均向下倾斜（斜率<0 或 接近0的横盘）
    if not (high_slope < consol_highs[0] * 0.003 and low_slope < consol_highs[0] * 0.003):
        return {'hit': False, 'name': 'M5上升旗形整理', 'tag': '🏴', 'type': 'hold'}
    
    # 缩量
    rally_vol = sum(vols[max(0,rally_start-3):rally_start+1]) / min(4, rally_start+1)
    consol_vol = sum(vols[rally_start:]) / len(vols[rally_start:])
    if consol_vol > rally_vol * 0.5:
        return {'hit': False, 'name': 'M5上升旗形整理', 'tag': '🏴', 'type': 'hold'}
    
    # 整理幅度 < 旗杆 1/2
    consol_range = (max(consol_highs) - min(consol_lows)) / min(consol_lows) * 100
    if consol_range > rally_gain * 0.5:
        return {'hit': False, 'name': 'M5上升旗形整理', 'tag': '🏴', 'type': 'hold'}
    
    bonus = 2 if vols[-1] == min(consol_vol, min(vols[rally_start:])) else 0
    
    return {
        'hit': True, 'name': 'M5上升旗形整理', 'tag': '🏴', 'type': 'hold',
        'score_base': 10 + bonus,
        'detail': f'上升旗形，旗杆涨幅{rally_gain:.1f}%，整理幅度{consol_range:.1f}%'
    }


# ═══════════════════════════════════════════
#  M6 阶梯横盘蓄力 🪜
# ═══════════════════════════════════════════

def detect_m6_staircase_consolidation(kline: List[dict], params: dict = None) -> dict:
    """
    拉升后窄幅横盘（振幅<12%，科创板688代码<15%），缩量，≥60%收盘在上半部
    """
    if len(kline) < 20:
        return {'hit': False, 'name': 'M6阶梯横盘蓄力', 'tag': '🪜', 'type': 'hold'}
    
    closes = [k['close'] for k in kline]
    highs = [k['high'] for k in kline]
    lows = [k['low'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    # 找放量拉升日
    breakout_idx = -1
    for i in range(n-20, n):
        chg = (closes[i] - closes[i-1]) / closes[i-1] * 100 if i > 0 else 0
        avg_vol_20 = sum(vols[max(0,i-20):i]) / min(20, i)
        if chg > 3 and vols[i] > avg_vol_20 * 1.5:
            breakout_idx = i
            break
    
    if breakout_idx == -1 or breakout_idx >= n - 3:
        return {'hit': False, 'name': 'M6阶梯横盘蓄力', 'tag': '🪜', 'type': 'hold'}
    
    # 横盘期：放量日后
    consol_kline = kline[breakout_idx+1:]
    
    # 振幅阈值：普通股<12%，科创板(688)<15%
    p = params or {}
    code = p.get('code', '')
    amp_threshold = 15 if str(code).startswith('688') else 12
    
    consol_high = max(k['high'] for k in consol_kline)
    consol_low = min(k['low'] for k in consol_kline)
    amplitude = (consol_high - consol_low) / consol_low * 100
    if amplitude > amp_threshold:
        return {'hit': False, 'name': 'M6阶梯横盘蓄力', 'tag': '🪜', 'type': 'hold'}
    
    # 缩量
    consol_vol = sum(k['volume'] for k in consol_kline) / len(consol_kline)
    if consol_vol > vols[breakout_idx] * 0.5:
        return {'hit': False, 'name': 'M6阶梯横盘蓄力', 'tag': '🪜', 'type': 'hold'}
    
    # ≥60%收盘在上半部
    range_mid = (consol_high + consol_low) / 2
    upper_count = sum(1 for k in consol_kline if k['close'] > range_mid)
    if upper_count / len(consol_kline) < 0.6:
        return {'hit': False, 'name': 'M6阶梯横盘蓄力', 'tag': '🪜', 'type': 'hold'    }
    
    bonus = 2 if all(
        consol_kline[i]['low'] >= consol_kline[i-1]['low']
        for i in range(1, min(5, len(consol_kline)))
    ) else 0
    
    return {
        'hit': True, 'name': 'M6阶梯横盘蓄力', 'tag': '🪜', 'type': 'hold',
        'score_base': 8 + bonus,
        'detail': f'放量日后横盘{len(consol_kline)}日，振幅{amplitude:.1f}%，缩量蓄力'
    }


# ═══════════════════════════════════════════
#  M12 V形反转 ⚡ (V1.3.5 新增)
# ═══════════════════════════════════════════

def detect_m12_v_reversal(kline: List[dict], params: dict = None) -> dict:
    """
    V形反转：急跌后快速反弹，收复大部分失地。
    
    触发条件：
    1. 近15日最大回撤 > 15%（急跌段）
    2. 回撤低点后3日内反弹，收复跌幅 > 50%
    3. 反弹段放量（近3日均量 > 前10日均量）
    4. 当前收盘 > MA20（趋势确认）
    
    强度：★★★☆（强反转信号）
    """
    if len(kline) < 25:
        return {'hit': False, 'name': 'M12 V形反转', 'tag': '⚡', 'type': 'hold'}
    
    closes = [k['close'] for k in kline]
    highs = [k['high'] for k in kline]
    lows = [k['low'] for k in kline]
    vols = [k['volume'] for k in kline]
    opens = [k['open'] for k in kline]
    n = len(kline)
    
    # 找近15日最高点和其后最低点
    window = 15
    peak_val = max(highs[-window:])
    peak_idx = n - window + highs[-window:].index(peak_val)
    
    # 找峰值后的最低点
    trough_val = min(lows[peak_idx:])
    trough_idx = peak_idx + lows[peak_idx:].index(trough_val)
    
    # 条件1：回撤 > 15%
    drawdown = (trough_val - peak_val) / peak_val * 100
    if drawdown > -15:
        return {'hit': False, 'name': 'M12 V形反转', 'tag': '⚡', 'type': 'hold'}
    
    # 条件2：低点后3日内反弹收复 > 50%跌幅
    if trough_idx >= n - 3:
        return {'hit': False, 'name': 'M12 V形反转', 'tag': '⚡', 'type': 'hold'}
    
    recovery = (closes[-1] - trough_val) / (peak_val - trough_val) * 100
    if recovery < 50:
        return {'hit': False, 'name': 'M12 V形反转', 'tag': '⚡', 'type': 'hold'}
    
    # 条件3：反弹放量
    vol_recent_3 = sum(vols[trough_idx+1:]) / max(1, n - trough_idx - 1)
    vol_prev_10 = sum(vols[max(0, trough_idx-10):trough_idx+1]) / min(10, trough_idx+1)
    if vol_recent_3 < vol_prev_10:
        return {'hit': False, 'name': 'M12 V形反转', 'tag': '⚡', 'type': 'hold'}
    
    # 条件4：站上MA20
    ma20 = sma(closes, 20)
    if closes[-1] <= ma20[-1]:
        return {'hit': False, 'name': 'M12 V形反转', 'tag': '⚡', 'type': 'hold'}
    
    # 当日收阳加分
    bonus = 2 if closes[-1] > opens[-1] else 0
    
    return {
        'hit': True, 'name': 'M12 V形反转', 'tag': '⚡', 'type': 'hold',
        'score_base': 11 + bonus,
        'detail': f'回撤{abs(drawdown):.1f}%后收复{recovery:.0f}%，反弹放量{vol_recent_3/vol_prev_10:.1f}x'
    }


# ═══════════════════════════════════════════
#  M13 双底/W底 🔄 (V1.3.5 新增)
# ═══════════════════════════════════════════

def detect_m13_double_bottom(kline: List[dict], params: dict = None) -> dict:
    """
    双底/W底：两次探底不破前低，第二次缩量，放量突破颈线确认。
    
    触发条件：
    1. 近30日有两个低点，间距 ≥ 5日
    2. 两低点价格差异 < 3%（不破前低）
    3. 第二次探底缩量（量 < 第一次探底量的70%）
    4. 当前收盘 > 两低点之间的颈线（反弹高点）
    5. 突破日放量
    
    强度：★★★★（确认度高的反转信号）
    """
    if len(kline) < 35:
        return {'hit': False, 'name': 'M13 双底反转', 'tag': '🔄', 'type': 'hold'}
    
    closes = [k['close'] for k in kline]
    highs = [k['high'] for k in kline]
    lows = [k['low'] for k in kline]
    vols = [k['volume'] for k in kline]
    opens = [k['open'] for k in kline]
    n = len(kline)
    
    # 找近30日的两个显著低点
    window = 30
    search_lows = lows[-window:]
    
    # 用谷底检测：找局部极小值（比左右2日都低）
    troughs = []
    for i in range(2, window - 2):
        idx = n - window + i
        if lows[idx] <= min(lows[idx-2], lows[idx-1], lows[idx+1], lows[idx+2]):
            troughs.append({
                'idx': idx,
                'low': lows[idx],
                'vol': vols[idx],
                'close': closes[idx],
            })
    
    if len(troughs) < 2:
        return {'hit': False, 'name': 'M13 双底反转', 'tag': '🔄', 'type': 'hold'}
    
    # 找最近两个低点，间距 ≥ 5日
    troughs.sort(key=lambda t: t['idx'], reverse=True)
    
    best_pair = None
    for i in range(len(troughs)):
        for j in range(i+1, len(troughs)):
            t1, t2 = troughs[i], troughs[j]  # t1更近
            if t2['idx'] >= t1['idx'] - 4:
                continue  # 太近，不算双底
            if t1['idx'] - t2['idx'] > 25:
                continue  # 太远
            
            # 条件2：两低点差异 < 3%
            diff = abs(t1['low'] - t2['low']) / max(t1['low'], t2['low']) * 100
            if diff > 3:
                continue
            
            # 条件3：第二次探底缩量
            if t1['vol'] > t2['vol'] * 0.7:
                continue
            
            best_pair = (t2, t1)  # (较早, 较近)
            break
        if best_pair:
            break
    
    if not best_pair:
        return {'hit': False, 'name': 'M13 双底反转', 'tag': '🔄', 'type': 'hold'}
    
    t_first, t_second = best_pair
    
    # 颈线 = 两次低点之间的反弹高点
    neckline = max(highs[t_first['idx']:t_second['idx']+1]) if t_first['idx'] < t_second['idx'] else closes[-1]
    
    # 条件4：当前收盘 > 颈线
    if closes[-1] <= neckline:
        return {'hit': False, 'name': 'M13 双底反转', 'tag': '🔄', 'type': 'hold'}
    
    # 条件5：突破放量
    avg_vol_10 = sum(vols[-15:-5]) / 10 if n >= 15 else vols[-1]
    if vols[-1] < avg_vol_10 * 1.2:
        return {'hit': False, 'name': 'M13 双底反转', 'tag': '🔄', 'type': 'hold'}
    
    # 突破幅度
    breakout_pct = (closes[-1] - neckline) / neckline * 100
    
    bonus = 0
    if breakout_pct > 3:
        bonus += 2
    if closes[-1] > opens[-1]:
        bonus += 1
    
    return {
        'hit': True, 'name': 'M13 双底反转', 'tag': '🔄', 'type': 'hold',
        'score_base': 12 + bonus,
        'detail': (f'双底{t_first["low"]:.2f}→{t_second["low"]:.2f}不破前低'
                   f'+颈线{neckline:.2f}突破{breakout_pct:+.1f}%')
    }


# ═══════════════════════════════════════════
#  B1 反包阳线 🔄
# ═══════════════════════════════════════════

def detect_b1_reversal_bar(kline: List[dict], params: dict = None) -> dict:
    """
    前日阴线 + 当日阳线实体完全吞没前日实体，当日量 > 前日量1.2x
    """
    if len(kline) < 3:
        return {'hit': False, 'name': 'B1反包阳线', 'tag': '🔄', 'type': 'buy'}
    
    opens = [k['open'] for k in kline]
    closes = [k['close'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    prev_body = closes[-2] - opens[-2]
    curr_body = closes[-1] - opens[-1]
    
    # 前日阴线
    if prev_body >= 0:
        return {'hit': False, 'name': 'B1反包阳线', 'tag': '🔄', 'type': 'buy'}
    
    # 当日阳线
    if curr_body <= 0:
        return {'hit': False, 'name': 'B1反包阳线', 'tag': '🔄', 'type': 'buy'}
    
    # 完全吞没：当日最低 < 前日最低 且 当日最高 > 前日最高
    if not (kline[-1]['low'] <= kline[-2]['low'] and kline[-1]['high'] >= kline[-2]['high']):
        # 放宽条件：实体吞没即可（收盘>前日开盘，开盘<前日收盘）
        if not (closes[-1] > opens[-2] and opens[-1] < closes[-2]):
            return {'hit': False, 'name': 'B1反包阳线', 'tag': '🔄', 'type': 'buy'}
    
    # 放量
    if vols[-1] < vols[-2] * 1.2:
        return {'hit': False, 'name': 'B1反包阳线', 'tag': '🔄', 'type': 'buy'}
    
    engulf_ratio = abs(curr_body) / abs(prev_body) if prev_body != 0 else 0
    return {
        'hit': True, 'name': 'B1反包阳线', 'tag': '🔄', 'type': 'buy',
        'anchor_date': kline[-1]['date'],
        'detail': f'{kline[-1]["date"]}阳线反包前日阴线，放量{vols[-1]/vols[-2]:.1f}x，吞没比{engulf_ratio:.1f}'
    }


# ═══════════════════════════════════════════
#  B2 回踩确认 🎯
# ═══════════════════════════════════════════

def detect_b2_pullback_confirm(kline: List[dict], params: dict = None) -> dict:
    """
    回踩MA20/MA60不破 + 缩量 + 当日放量阳线反弹确认
    """
    if len(kline) < 25:
        return {'hit': False, 'name': 'B2回踩确认', 'tag': '🎯', 'type': 'buy'}
    
    closes = [k['close'] for k in kline]
    lows = [k['low'] for k in kline]
    vols = [k['volume'] for k in kline]
    opens = [k['open'] for k in kline]
    n = len(kline)
    
    ma20 = sma(closes, 20)
    ma60 = sma(closes, 60)
    
    # 当日必须是放量阳线
    curr_body = closes[-1] - opens[-1]
    if curr_body <= 0:
        return {'hit': False, 'name': 'B2回踩确认', 'tag': '🎯', 'type': 'buy'}
    
    avg_vol_5 = sum(vols[max(0,n-6):n-1]) / min(5, n-1)
    if vols[-1] < avg_vol_5 * 1.2:
        return {'hit': False, 'name': 'B2回踩确认', 'tag': '🎯', 'type': 'buy'}
    
    # 检查近3日是否有回踩动作（最低价接近均线）
    # V1.3.8 修复：回踩日必须是"回踩"而非"突破"或"破位"——
    #   ① 收盘价站回均线上方（未破位，排除"盘中触及后收盘跌破"的假回踩）
    #   ② 低点低于开盘价（有下探动作，排除"低开高走/突破大阳线"被误判为回踩）
    touch_found = False
    touch_ma = ''
    touch_idx = n - 1
    for i in range(n-3, n-1):
        dist20 = (lows[i] - ma20[i]) / ma20[i] * 100 if ma20[i] > 0 else 100
        dist60 = (lows[i] - ma60[i]) / ma60[i] * 100 if ma60[i] > 0 else 100
        
        if -2 < dist20 < 1 and closes[i] >= ma20[i] and lows[i] < opens[i]:
            touch_found = True
            touch_ma = 'MA20'
            touch_idx = i
            break
        if -2 < dist60 < 1 and closes[i] >= ma60[i] and lows[i] < opens[i]:
            touch_found = True
            touch_ma = 'MA60'
            touch_idx = i
            break
    
    if not touch_found:
        return {'hit': False, 'name': 'B2回踩确认', 'tag': '🎯', 'type': 'buy'}
    
    # 回踩日缩量（V1.3.8：记录回踩日量比，供 detail 参考；不强制缩量——放量回踩确认同样健康）
    touch_vol = vols[touch_idx]
    touch_vol_ratio = vols[touch_idx] / avg_vol_5 if avg_vol_5 > 0 else 1
    
    return {
        'hit': True, 'name': 'B2回踩确认', 'tag': '🎯', 'type': 'buy',
        'anchor_date': kline[-1]['date'],
        'detail': f'回踩{touch_ma}({ma20[-1] if touch_ma=="MA20" else ma60[-1]:.2f})不破+放量阳线确认，量比{vols[-1]/avg_vol_5:.1f}x'
    }


# ═══════════════════════════════════════════
#  B3 整理突破 🚩
# ═══════════════════════════════════════════

def detect_b3_consolidation_breakout(kline: List[dict], hold_patterns: List[dict] = None, params: dict = None) -> dict:
    """
    M5旗形/M6横盘整理末端，放量突破整理上轨
    前置：已命中M5或M6
    """
    if not hold_patterns:
        return {'hit': False, 'name': 'B3整理突破', 'tag': '🚩', 'type': 'buy'}
    
    has_consolidation = any(p['name'] in ('M5上升旗形整理', 'M6阶梯横盘蓄力') for p in hold_patterns)
    if not has_consolidation:
        return {'hit': False, 'name': 'B3整理突破', 'tag': '🚩', 'type': 'buy'}
    
    closes = [k['close'] for k in kline]
    highs = [k['high'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    # 当日放量突破近期高点
    recent_high = max(highs[-5:-1]) if n >= 5 else closes[-1]
    avg_vol_5 = sum(vols[max(0,n-6):n-1]) / min(5, n-1)
    
    if closes[-1] <= recent_high:
        return {'hit': False, 'name': 'B3整理突破', 'tag': '🚩', 'type': 'buy'}
    if vols[-1] < avg_vol_5 * 1.3:
        return {'hit': False, 'name': 'B3整理突破', 'tag': '🚩', 'type': 'buy'}
    
    return {
        'hit': True, 'name': 'B3整理突破', 'tag': '🚩', 'type': 'buy',
        'anchor_date': kline[-1]['date'],
        'detail': f'整理末端放量突破上轨{recent_high:.2f}，量比{vols[-1]/avg_vol_5:.1f}x'
    }


# ═══════════════════════════════════════════
#  B4 缩尽首阳 🌅
# ═══════════════════════════════════════════

def detect_b4_exhaustion_reversal(kline: List[dict], params: dict = None) -> dict:
    """
    连续3日+缩量阴线后，出现放量阳线（量>前5日均量1.5x + 涨幅>2%）
    """
    if len(kline) < 10:
        return {'hit': False, 'name': 'B4缩尽首阳', 'tag': '🌅', 'type': 'buy'}
    
    closes = [k['close'] for k in kline]
    opens = [k['open'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    # V1.3.5: 检查前面是否有≥3日连续阴线（不要求每日严格缩量递减）
    # 改为：连续≥3日阴线 + 最后3日平均量 < 前5日均量80%
    bear_streak = 0
    for i in range(n-2, max(0, n-10), -1):
        body = closes[i] - opens[i]
        if body >= 0:
            break
        bear_streak += 1
    
    if bear_streak < 3:
        return {'hit': False, 'name': 'B4缩尽首阳', 'tag': '🌅', 'type': 'buy'}
    
    # 缩量检查：最后3日（含缩量阴线区间）平均量 < 前5日均量 * 0.8
    vol_last_3 = sum(vols[max(0,n-4):n-1]) / min(3, n-1 - max(0, n-4))
    vol_prev_5 = sum(vols[max(0,n-9):max(0,n-4)]) / min(5, n-4 - max(0, n-9))
    if vol_last_3 > vol_prev_5 * 0.8:
        return {'hit': False, 'name': 'B4缩尽首阳', 'tag': '🌅', 'type': 'buy'}
    
    # 当日放量阳线
    curr_body = closes[-1] - opens[-1]
    if curr_body <= 0:
        return {'hit': False, 'name': 'B4缩尽首阳', 'tag': '🌅', 'type': 'buy'}
    
    day_chg = (closes[-1] - closes[-2]) / closes[-2] * 100
    if day_chg < 2:
        return {'hit': False, 'name': 'B4缩尽首阳', 'tag': '🌅', 'type': 'buy'}
    
    avg_vol_5 = sum(vols[max(0,n-6):n-1]) / min(5, n-1)
    if vols[-1] < avg_vol_5 * 1.5:
        return {'hit': False, 'name': 'B4缩尽首阳', 'tag': '🌅', 'type': 'buy'}
    
    return {
        'hit': True, 'name': 'B4缩尽首阳', 'tag': '🌅', 'type': 'buy',
        'anchor_date': kline[-1]['date'],
        'detail': f'连续{bear_streak}日缩量阴线后放量首阳，涨幅{day_chg:.1f}%，量比{vols[-1]/avg_vol_5:.1f}x'
    }


# ═══════════════════════════════════════════
#  M7 高位搏杀 ⚡
# ═══════════════════════════════════════════

def detect_m7_high_stakes(kline: List[dict], turnover: float = None, params: dict = None) -> dict:
    """
    累计涨幅>30% + 爆量/涨停 + 换手>20% + 量能峰值后衰减
    """
    if len(kline) < 30:
        return {'hit': False, 'name': 'M7高位搏杀', 'tag': '⚡', 'type': 'warning'}
    
    closes = [k['close'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    gain_30 = (closes[-1] - closes[-30]) / closes[-30] * 100
    if gain_30 <= 30:
        return {'hit': False, 'name': 'M7高位搏杀', 'tag': '⚡', 'type': 'warning'}
    
    # 量能峰值后衰减
    vol_peak = max(vols[-10:])
    vol_peak_idx = vols.index(vol_peak, n-10, n)
    vol_recent = sum(vols[vol_peak_idx+1:]) / max(1, n - vol_peak_idx - 1)
    if vol_recent > vol_peak * 0.7:
        return {'hit': False, 'name': 'M7高位搏杀', 'tag': '⚡', 'type': 'warning'}
    
    # 换手检查（如果提供了）
    if turnover and turnover < 20:
        return {'hit': False, 'name': 'M7高位搏杀', 'tag': '⚡', 'type': 'warning'}
    
    return {
        'hit': True, 'name': 'M7高位搏杀', 'tag': '⚡', 'type': 'warning',
        'detail': f'30日涨{gain_30:.1f}%，量能峰值{vols[vol_peak_idx]/100:.0f}手后衰减，高换手博弈'
    }


# ═══════════════════════════════════════════
#  W1 涨幅过热 🌡️ / W2 乖离过大 📏 / W3 上影频现 📌 / W4 量能背离 📉
# ═══════════════════════════════════════════

def detect_warnings(kline: List[dict], params: dict = None) -> List[dict]:
    """检测所有预警信号"""
    warnings = []
    p = params or {}
    
    if len(kline) < 20:
        return warnings
    
    closes = [k['close'] for k in kline]
    opens = [k['open'] for k in kline]
    highs = [k['high'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    # W1 涨幅过热：区分趋势加速 vs 超跌修复
    gain_20 = (closes[-1] - closes[-20]) / closes[-20] * 100 if n >= 20 else 0
    gain_10 = (closes[-1] - closes[-10]) / closes[-10] * 100 if n >= 10 else 0
    
    # 距60日高点回撤>40% → 超跌修复场景，阈值放宽
    peak_60 = max(highs[-min(60, n):]) if n >= 20 else closes[-1]
    dd_from_peak = (closes[-1] - peak_60) / peak_60 * 100 if peak_60 > 0 else 0
    is_bounce = dd_from_peak < -40  # 超跌修复标志
    
    w1_gain20_threshold = 35 if is_bounce else 20
    w1_gain10_threshold = 25 if is_bounce else 15
    
    if gain_20 > w1_gain20_threshold or gain_10 > w1_gain10_threshold:
        scenario_note = "(超跌修复放宽)" if is_bounce else "(超阈值)"
        warnings.append({
            'hit': True, 'name': 'W1涨幅过热', 'tag': '🌡️', 'type': 'warning',
            'detail': f'20日涨{gain_20:.1f}%{f"({w1_gain20_threshold}%阈值)" if gain_20>w1_gain20_threshold else ""}'
                     f'{" | " if gain_20>w1_gain20_threshold and gain_10>w1_gain10_threshold else ""}'
                     f'{"10日涨"+str(round(gain_10,1))+"%("+str(w1_gain10_threshold)+"%阈值)" if gain_10>w1_gain10_threshold else ""}'
                     f' | {scenario_note}'
        })
    
    # W2 乖离过大
    ma20 = sma(closes, 20)
    deviation = (closes[-1] - ma20[-1]) / ma20[-1] * 100
    if deviation > 15:
        warnings.append({
            'hit': True, 'name': 'W2乖离过大', 'tag': '📏', 'type': 'warning',
            'detail': f'偏离MA20({ma20[-1]:.2f})已达{deviation:.1f}%(超15%阈值)'
        })
    
    # W3 上影频现
    upper_count = 0
    for i in range(n-5, n):
        upper = (highs[i] - max(closes[i], opens[i])) / highs[i] * 100 if highs[i] > 0 else 0
        if upper > 3:
            upper_count += 1
    if upper_count >= 3:
        max_upper = max(
            (highs[i] - max(closes[i], opens[i])) / highs[i] * 100
            for i in range(n-5, n) if highs[i] > 0
        )
        warnings.append({
            'hit': True, 'name': 'W3上影频现', 'tag': '📌', 'type': 'warning',
            'detail': f'近5日{upper_count}天上影>3%，最大{max_upper:.1f}%'
        })
    
    # W4 量能背离
    vol_recent_5 = sum(vols[-5:]) / 5
    vol_prev_5 = sum(vols[-10:-5]) / 5
    if vol_recent_5 < vol_prev_5 * 0.8 and closes[-1] >= max(closes[-10:]) * 0.95:
        warnings.append({
            'hit': True, 'name': 'W4量能背离', 'tag': '📉', 'type': 'warning',
            'detail': f'价格高位但量能下降{(1-vol_recent_5/vol_prev_5)*100:.0f}%'
        })
    
    return warnings


# ═══════════════════════════════════════════
#  M8 高开诱多 🪤
# ═══════════════════════════════════════════

def detect_m8_gap_trap(kline: List[dict], params: dict = None) -> dict:
    """
    高开(开>昨收+2%)但收盘涨幅<1%，量>昨量70%
    """
    if len(kline) < 3:
        return {'hit': False, 'name': 'M8高开诱多', 'tag': '🪤', 'type': 'sell'}
    
    opens = [k['open'] for k in kline]
    closes = [k['close'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    # 检查近3日
    for i in range(n-3, n):
        gap = (opens[i] - closes[i-1]) / closes[i-1] * 100 if i > 0 else 0
        if gap < 2:
            continue
        day_chg = (closes[i] - closes[i-1]) / closes[i-1] * 100
        if day_chg >= 1:
            continue
        if vols[i] < vols[i-1] * 0.7:
            continue
        
        return {
            'hit': True, 'name': 'M8高开诱多', 'tag': '🪤', 'type': 'sell',
            'anchor_date': kline[i]['date'],
            'detail': f'{kline[i]["date"]}高开{gap:.1f}%收{day_chg:+.1f}%，诱多出货'
        }
    
    return {'hit': False, 'name': 'M8高开诱多', 'tag': '🪤', 'type': 'sell'}


# ═══════════════════════════════════════════
#  M9 缩量连阴 🌧️
# ═══════════════════════════════════════════

def detect_m9_volume_dry_up(kline: List[dict], params: dict = None) -> dict:
    """
    连续2日阴线 + 每日量<前5日均量70%
    """
    if len(kline) < 7:
        return {'hit': False, 'name': 'M9缩量连阴', 'tag': '🌧️', 'type': 'sell'}
    
    closes = [k['close'] for k in kline]
    opens = [k['open'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    d1_body = closes[-2] - opens[-2]
    d2_body = closes[-1] - opens[-1]
    
    if d1_body >= 0 or d2_body >= 0:
        return {'hit': False, 'name': 'M9缩量连阴', 'tag': '🌧️', 'type': 'sell'}
    
    avg_vol_5 = sum(vols[max(0,n-7):n-2]) / min(5, n-2)
    if vols[-2] > avg_vol_5 * 0.7 or vols[-1] > avg_vol_5 * 0.7:
        return {'hit': False, 'name': 'M9缩量连阴', 'tag': '🌧️', 'type': 'sell'}
    
    return {
        'hit': True, 'name': 'M9缩量连阴', 'tag': '🌧️', 'type': 'sell',
        'detail': f'连续2日缩量阴线，量比均<前5日均量70%，多头弃守'
    }


# ═══════════════════════════════════════════
#  M10 峰值回撤 ⛔
# ═══════════════════════════════════════════

def detect_m10_peak_drawdown(kline: List[dict], params: dict = None) -> dict:
    """
    从近20日高点回撤>8%，近3日无反弹阳线
    """
    if len(kline) < 20:
        return {'hit': False, 'name': 'M10峰值回撤', 'tag': '⛔', 'type': 'sell'}
    
    closes = [k['close'] for k in kline]
    highs = [k['high'] for k in kline]
    opens = [k['open'] for k in kline]
    n = len(kline)
    
    peak_close = max(closes[-20:])
    drawdown = (closes[-1] - peak_close) / peak_close * 100
    
    if drawdown > -8:
        return {'hit': False, 'name': 'M10峰值回撤', 'tag': '⛔', 'type': 'sell'}
    
    # V1.3.7: 近3日无反弹阳线 —— 文档语义修正。原"≥2日阴线"无法区分
    # "昨日大阳反弹+今日缩量回踩"与"阴跌中继"，会误杀见底反弹股。
    # 若近3日出现涨幅≥2%的阳线，说明已有反弹，不触发M10。
    for i in range(n-3, n):
        if i <= 0:
            continue
        _day_chg = (closes[i] - closes[i-1]) / closes[i-1] * 100
        if closes[i] > opens[i] and _day_chg >= 2:
            return {'hit': False, 'name': 'M10峰值回撤', 'tag': '⛔', 'type': 'sell'}
    
    # 近3日至少2日阴线（无反弹阳线的前提下，仍需确认弱势）
    bearish_count = sum(1 for i in range(n-3, n) if closes[i] < opens[i])
    if bearish_count < 2:
        return {'hit': False, 'name': 'M10峰值回撤', 'tag': '⛔', 'type': 'sell'}
    
    return {
        'hit': True, 'name': 'M10峰值回撤', 'tag': '⛔', 'type': 'sell',
        'detail': f'从高点{peak_close:.2f}回撤{abs(drawdown):.1f}%，近3日{bearish_count}日阴线'
    }


# ═══════════════════════════════════════════
#  M11 趋势破位 💀
# ═══════════════════════════════════════════

def detect_m11_trend_break(kline: List[dict], params: dict = None) -> dict:
    """
    收盘跌破MA20且连续2日未收回
    """
    if len(kline) < 22:
        return {'hit': False, 'name': 'M11趋势破位', 'tag': '💀', 'type': 'sell'}
    
    closes = [k['close'] for k in kline]
    ma20 = sma(closes, 20)
    n = len(kline)
    
    if closes[-1] >= ma20[-1]:
        return {'hit': False, 'name': 'M11趋势破位', 'tag': '💀', 'type': 'sell'}
    if closes[-2] >= ma20[-2]:
        return {'hit': False, 'name': 'M11趋势破位', 'tag': '💀', 'type': 'sell'}
    
    return {
        'hit': True, 'name': 'M11趋势破位', 'tag': '💀', 'type': 'sell',
        'detail': f'连续2日收盘低于MA20({ma20[-1]:.2f})，趋势破位确认'
    }


# ═══════════════════════════════════════════
#  Pre-M11 预破位预警 ⚠️
# ═══════════════════════════════════════════

def detect_pre_m11_warning(kline: List[dict], params: dict = None) -> Optional[dict]:
    """
    M11趋势破位前置预警：价格逼近MA20 + 缩量下行，可能在1-3日内触发正式破位。
    
    触发条件（全部满足）：
    1. 价格在MA20上方但距离<3%（逼近破位线）
    2. 近5日均量 < 前20日均量（缩量，多头无力）
    3. 近3日价格趋势向下或横盘（无反弹动能）
    4. MA20斜率趋平或下行（均线拐头）
    
    返回: dict or None
    """
    p = params or {}
    
    if len(kline) < 25:
        return None
    
    closes = [k['close'] for k in kline]
    highs = [k['high'] for k in kline]
    vols = [k['volume'] for k in kline]
    opens = [k['open'] for k in kline]
    n = len(kline)
    
    ma20 = sma(closes, 20)
    
    # V1.3.6: 今日放量阳线反弹豁免 —— 最新日放量阳线(涨≥2%且量≥1.1x)且站上MA20时，
    # 属于向上收复而非向下逼近MA20，方向相反，不构成"预破位"预警。
    if n >= 2:
        _last_chg = (closes[-1] - closes[-2]) / closes[-2] * 100 if closes[-2] > 0 else 0
        _vol_r = vols[-1] / vols[-2] if vols[-2] > 0 else 1
        if closes[-1] > opens[-1] and _last_chg >= 2 and _vol_r >= 1.1 and closes[-1] > ma20[-1]:
            return None
    
    # 条件1：价格在MA20上方但距离<3%
    dist_to_ma20 = (closes[-1] - ma20[-1]) / ma20[-1] * 100 if ma20[-1] > 0 else 100
    if dist_to_ma20 < 0:
        return None  # 已经跌破，该触发M11而非Pre-M11
    if dist_to_ma20 > 3:
        return None  # 距离太远，不构成迫近威胁
    
    # 条件2：缩量（近5日均量 < 前20日均量*0.85）
    vol_5 = sum(vols[-5:]) / 5
    vol_20 = sum(vols[-25:-5]) / 20 if n >= 25 else vol_5
    if vol_20 == 0:
        return None
    if vol_5 > vol_20 * 0.85:
        return None
    
    # 条件3：近3日趋势向下（收盘价未创新高，至少2日收阴或十字星）
    bearish_count = sum(1 for i in range(n-3, n) if closes[i] <= opens[i])
    recent_high = max(highs[-3:])
    if closes[-1] >= recent_high * 0.99:  # 还在尝试创新高，不算破位预警
        return None
    if bearish_count < 2:
        return None
    
    # 条件4：MA20斜率趋平或向下（近5日MA20变化 < 0.5% 或 负增长）
    ma20_5d_ago = ma20[-6] if len(ma20) >= 6 else ma20[0]
    ma20_slope = (ma20[-1] - ma20_5d_ago) / ma20_5d_ago * 100 if ma20_5d_ago > 0 else 0
    if ma20_slope > 0.5:
        return None  # MA20还在明显上行，支撑力强
    
    # 严重程度打分 (0-100, 越高越危险)
    severity = 0
    # 距离越近越危险：3%→30分，1%→70分
    severity += int(max(0, 100 - dist_to_ma20 * 25))
    # 缩量越严重越危险：85%→30分，50%→60分
    vol_ratio = vol_5 / vol_20
    severity += int(max(0, 80 - vol_ratio * 80))
    # MA20斜率越负越危险
    if ma20_slope < -0.5:
        severity += 15
    elif ma20_slope < 0:
        severity += 5
    severity = min(100, severity)
    
    urgency = '高' if severity >= 60 else '中' if severity >= 40 else '低'
    
    return {
        'hit': True,
        'name': 'Pre-M11预破位预警',
        'tag': '⚠️',
        'type': 'warning',
        'severity': severity,
        'detail': (
            f'距MA20({ma20[-1]:.2f})仅{dist_to_ma20:.1f}%，'
            f'量缩至{vol_ratio:.0%}，'
            f'MA20斜率{ma20_slope:+.1f}%，'
            f'近3日{bearish_count}日收阴，'
            f'危险度{severity}分({urgency})'
        ),
    }


# ═══════════════════════════════════════════
#  反弹博弈信号 R1~R3 🎲
#  仅在 M10/M11 卖出信号触发后检测，
#  识别潜在的短线技术反弹机会。
#  ⚠️ 高风险投机信号，非趋势反转确认！
# ═══════════════════════════════════════════

def detect_r1_panic_rebound(kline: List[dict], params: dict = None) -> Optional[dict]:
    """
    R1 恐慌抛售反弹 🩸
    
    触发条件：
    1. 20日回撤 > 20%（深度超卖）
    2. 当日成交量 > 2x 20日均量（恐慌抛售峰值）
    3. 收盘 > 开盘（日内反转，多头反扑）
    4. 下影线 > 实体 * 1.5（锤子线形态）
    
    逻辑：恐慌盘出清后的技术反弹
    强度：★★★（最强反弹信号）
    """
    if len(kline) < 25:
        return None
    
    closes = [k['close'] for k in kline]
    opens = [k['open'] for k in kline]
    highs = [k['high'] for k in kline]
    lows = [k['low'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    # 条件1：深度回撤
    peak_20 = max(highs[-20:])
    dd = (closes[-1] - peak_20) / peak_20 * 100
    if dd > -20:
        return None
    
    # 条件2：恐慌量
    avg_vol_20 = sum(vols[-25:-5]) / 20 if n >= 25 else sum(vols[-20:]) / 20
    if vols[-1] < avg_vol_20 * 2.0:
        return None
    
    # 条件3：日内反转（收阳）
    body = closes[-1] - opens[-1]
    if body <= 0:
        return None
    
    # 条件4：锤子线（下影 > 实体 * 1.5）
    lower_shadow = min(closes[-1], opens[-1]) - lows[-1]
    upper_shadow = highs[-1] - max(closes[-1], opens[-1])
    if lower_shadow < abs(body) * 1.5:
        return None
    
    # 质量评分
    quality = 0
    quality += min(15, int(abs(dd) - 20))  # 回撤越深越好
    quality += min(10, int(lower_shadow / abs(body) * 3))  # 下影越长越好
    quality += min(10, int(vols[-1] / avg_vol_20))  # 量越大越恐慌
    quality += 5 if upper_shadow < abs(body) * 0.3 else 0  # 几乎无上影
    quality = min(100, quality * 2)
    
    return {
        'hit': True, 'name': 'R1恐慌抛售反弹', 'tag': '🩸', 'type': 'rebound',
        'anchor_date': kline[-1]['date'],
        'quality': quality,
        'detail': (
            f'回撤{abs(dd):.1f}%+恐慌量{vols[-1]/avg_vol_20:.1f}x'
            f'+锤子线(下影/实体={lower_shadow/abs(body):.1f})，'
            f'质量{quality}分'
        ),
    }


def detect_r2_exhaustion_rebound(kline: List[dict], params: dict = None) -> Optional[dict]:
    """
    R2 缩量衰竭反弹 🌑
    
    触发条件：
    1. 20日回撤 > 25%
    2. 近3日均量 < 20日均量 * 50%（量能枯竭）
    3. 今日跌幅 < 昨日跌幅（跌速放缓）
    4. 连续≥4日阴线后出现小实体（力量耗尽）
    
    逻辑：卖盘力量耗尽，买方开始试探
    强度：★★（中等反弹信号）
    """
    if len(kline) < 25:
        return None
    
    closes = [k['close'] for k in kline]
    opens = [k['open'] for k in kline]
    highs = [k['high'] for k in kline]
    lows = [k['low'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    # 条件1：深度回撤
    peak_20 = max(highs[-20:])
    dd = (closes[-1] - peak_20) / peak_20 * 100
    if dd > -25:
        return None
    
    # 条件2：量能枯竭（放宽容忍度：近3日均量 < 20日均量 * 0.6）
    avg_vol_20 = sum(vols[-25:-5]) / 20 if n >= 25 else sum(vols[-20:]) / 20
    vol_3 = sum(vols[-3:]) / 3
    if vol_3 > avg_vol_20 * 0.6:
        return None
    
    # 条件3：跌速放缓
    chg_today = (closes[-1] - closes[-2]) / closes[-2] * 100
    chg_yesterday = (closes[-2] - closes[-3]) / closes[-3] * 100
    if chg_today < chg_yesterday:  # 今天跌得比昨天还多
        return None
    
    # 条件4：连续阴线后力量耗尽（≥4日阴线，最后一日为小实体或十字星）
    bear_streak = 0
    for i in range(n-1, max(0, n-10), -1):
        if closes[i] < opens[i]:
            bear_streak += 1
        else:
            break
    if bear_streak < 4:
        return None
    
    # 最后一根K线实体较小（振幅 < 前3日平均振幅的70%）
    today_range = (highs[-1] - lows[-1]) / closes[-1] * 100
    avg_range_3 = sum((highs[i] - lows[i]) / closes[i] * 100 for i in range(n-4, n-1)) / 3
    if today_range > avg_range_3 * 0.7:
        return None
    
    # 质量评分
    quality = 0
    quality += min(15, int(abs(dd) - 25))
    quality += min(15, int((1 - vol_3 / avg_vol_20) * 30))
    quality += min(10, bear_streak * 2)
    quality += 10 if chg_today > -3 else (5 if chg_today > -5 else 0)
    quality = min(100, quality * 2)
    
    return {
        'hit': True, 'name': 'R2缩量衰竭反弹', 'tag': '🌑', 'type': 'rebound',
        'anchor_date': kline[-1]['date'],
        'quality': quality,
        'detail': (
            f'回撤{abs(dd):.1f}%+量缩至{vol_3/avg_vol_20:.0%}'
            f'+连阴{bear_streak}日，跌速放缓，质量{quality}分'
        ),
    }


def detect_r3_oversold_mean_reversion(kline: List[dict], params: dict = None) -> Optional[dict]:
    """
    R3 超跌均值回归 🎯
    
    触发条件：
    1. 20日回撤 > 30%（极端超卖）
    2. 价格偏离MA20 > 12%（V1.3.2下调，原20%太苛刻，MA20下行时乖离难以追赶跌幅）
    3. 今日收阳 或 出现十字星
    4. 近3日至少1日收阳（有资金开始试探）
    
    逻辑：极端超卖后的统计性回归
    强度：★（最弱反弹信号，纯统计意义）
    """
    if len(kline) < 25:
        return None
    
    closes = [k['close'] for k in kline]
    opens = [k['open'] for k in kline]
    highs = [k['high'] for k in kline]
    lows = [k['low'] for k in kline]
    n = len(kline)
    
    ma20 = sma(closes, 20)
    
    # 条件1：极端回撤
    peak_20 = max(highs[-20:])
    dd = (closes[-1] - peak_20) / peak_20 * 100
    if dd > -30:
        return None
    
    # 条件2：超卖乖离（V1.3.2: -20→-12）
    deviation = (closes[-1] - ma20[-1]) / ma20[-1] * 100
    if deviation > -12:
        return None
    
    # 条件3：今日止跌信号（收阳 或 十字星）
    body = closes[-1] - opens[-1]
    today_range = highs[-1] - lows[-1]
    is_bullish = body > 0
    is_doji = today_range > 0 and abs(body) / today_range < 0.3
    if not (is_bullish or is_doji):
        return None
    
    # 条件4：近3日有试探资金（至少1日收阳）
    recent_bullish = sum(1 for i in range(n-3, n) if closes[i] > opens[i])
    if recent_bullish == 0:
        return None
    
    # 质量评分（V1.3.2: 乖离评分基准从-20调整为-12）
    quality = 0
    quality += min(20, int(abs(dd) - 30))
    quality += min(15, int(abs(deviation) - 12))
    quality += 10 if is_bullish else 5
    quality += recent_bullish * 5
    quality = min(100, quality * 2)
    
    return {
        'hit': True, 'name': 'R3超跌均值回归', 'tag': '🎯', 'type': 'rebound',
        'anchor_date': kline[-1]['date'],
        'quality': quality,
        'detail': (
            f'回撤{abs(dd):.1f}%+乖离{abs(deviation):.1f}%'
            f'+{"收阳" if is_bullish else "十字星"}止跌，'
            f'质量{quality}分'
        ),
    }


def detect_rebound_signals(kline: List[dict], params: dict = None) -> List[dict]:
    """检测所有反弹博弈信号（仅在卖出形态已触发时调用）"""
    p = params or {}
    signals = []
    
    for detector in [detect_r1_panic_rebound, detect_r2_exhaustion_rebound, detect_r3_oversold_mean_reversion]:
        result = detector(kline, p)
        if result:
            signals.append(result)
    
    # 按质量排序
    signals.sort(key=lambda s: s.get('quality', 0), reverse=True)
    return signals


# ═══════════════════════════════════════════
#  总控：并行检测所有形态
# ═══════════════════════════════════════════

def detect_all(kline: List[dict], turnover: float = None, params: dict = None, code: str = '') -> dict:
    """
    并行检测所有12种形态，返回完整结果。
    
    参数:
        code: 股票代码，用于区分科创板(688)等特殊品种
    
    返回格式:
    {
        'hold_patterns': [...],
        'warnings': [...],
        'sell_signals': [...],
        'primary': {...},       # 最重要的信号（卖出 > 预警 > 持有）
        'all_signals': [...],   # 所有命中信号
    }
    """
    p = dict(params or {})
    p['code'] = code  # 注入代码给各探测器使用
    
    hold_detectors = [
        detect_m1_bottom_breakout,
        detect_m2_bullish_alignment,
        detect_m3_trend_acceleration,
        detect_m4_pullback_support,
        detect_m5_flag_consolidation,
        detect_m6_staircase_consolidation,
        detect_m12_v_reversal,
        detect_m13_double_bottom,
    ]
    
    sell_detectors = [
        detect_m8_gap_trap,
        detect_m9_volume_dry_up,
        detect_m10_peak_drawdown,
        detect_m11_trend_break,
    ]
    
    hold_patterns = [d(kline, p) for d in hold_detectors if d(kline, p)['hit']]
    warnings = detect_warnings(kline, p)
    # M7 高位搏杀
    m7 = detect_m7_high_stakes(kline, turnover, p)
    if m7['hit']:
        warnings.append(m7)
    # Pre-M11 预破位预警（在正式M11前发出警报）
    pre_m11 = detect_pre_m11_warning(kline, p)
    if pre_m11:
        warnings.append(pre_m11)
    
    sell_signals = [d(kline, p) for d in sell_detectors if d(kline, p)['hit']]
    
    # V1.3.6: 今日放量反弹覆盖 —— 最新日为放量反弹阳线且收复MA20时，
    # 基于"弱势/回撤/诱多"的卖出信号(M8/M9/M10)被反弹证伪，予以清除。
    # 趋势破位M11要求连续2日跌破MA20，今日阳线站上时天然不触发，无需处理。
    # 设计依据：V1.3.4"深度回撤+阳线=止跌信号，不应机械卖出"哲学的上位统一。
    if sell_signals:
        _cl = [k['close'] for k in kline]
        _op = [k['open'] for k in kline]
        _vo = [k['volume'] for k in kline]
        _nn = len(kline)
        _ma20_arr = sma(_cl, 20)
        _last_chg = (_cl[-1] - _cl[-2]) / _cl[-2] * 100 if _nn >= 2 else 0
        _vol_ratio = _vo[-1] / _vo[-2] if _nn >= 2 and _vo[-2] > 0 else 1
        _is_bull = _cl[-1] > _op[-1]
        _above_ma20 = _cl[-1] > _ma20_arr[-1] if _ma20_arr else False
        _today_rebound = _is_bull and _last_chg >= 2 and _vol_ratio >= 1.1 and _above_ma20
        if _today_rebound:
            _override = {'M8高开诱多', 'M9缩量连阴', 'M10峰值回撤'}
            _kept = [s for s in sell_signals if s['name'] not in _override]
            if _kept != sell_signals:
                sell_signals = _kept
    
    # B1~B4 加仓信号检测（只有非卖出区间才检测）
    buy_signals = []
    if not sell_signals:
        b1 = detect_b1_reversal_bar(kline, p)
        b2 = detect_b2_pullback_confirm(kline, p)
        b3 = detect_b3_consolidation_breakout(kline, hold_patterns, p)
        b4 = detect_b4_exhaustion_reversal(kline, p)
        for b in [b1, b2, b3, b4]:
            if b['hit']:
                buy_signals.append(b)
    
    # R1~R3 反弹博弈信号（仅卖出区间检测）
    rebound_signals = []
    if sell_signals:
        rebound_signals = detect_rebound_signals(kline, p)
    
    # 确定主信号：卖出 > 预警 > 持有
    all_signals = sell_signals + warnings + hold_patterns
    
    if sell_signals:
        # M11 > M10 > M9 > M8
        priority = {'M11趋势破位': 0, 'M10峰值回撤': 1, 'M9缩量连阴': 2, 'M8高开诱多': 3}
        primary = min(sell_signals, key=lambda s: priority.get(s['name'], 99))
        decision = 'sell'
    elif warnings:
        # M1底部康复场景：若M1活跃且仅有温和小警告，以M1为主信号
        has_m1 = any('M1' in h.get('name', '') or '底部启动' in h.get('name', '') for h in hold_patterns)
        warn_names = [w['name'] for w in warnings if w.get('hit')]
        # Pre-M11高危险度 → 优先展示
        has_pre_m11_high = any(
            w.get('name') == 'Pre-M11预破位预警' and w.get('severity', 0) >= 50
            for w in warnings
        )
        mild_warns = all(name.startswith('W1') or name.startswith('W2') for name in warn_names)
        
        if has_pre_m11_high and not mild_warns:
            # Pre-M11高危 = 准卖出信号，优先显示
            primary = [w for w in warnings if w.get('name') == 'Pre-M11预破位预警'][0]
            decision = 'reduce'
        elif has_m1 and mild_warns:
            primary = min(hold_patterns, key=lambda h: 0 if 'M1' in h.get('name', '') or '底部启动' in h.get('name', '') else 99)
            decision = 'hold'
        else:
            primary = warnings[0]
            decision = 'reduce'
    elif hold_patterns:
        # M1 > M2 > M3 > M12 > M13 > M4 > M5 > M6
        priority = {
            'M1底部启动加速': 0, 'M2均线多头发散': 1, 'M3趋势中继加速': 2,
            'M12 V形反转': 3, 'M13 双底反转': 4,
            'M4缩量回踩支撑': 5, 'M5上升旗形整理': 6, 'M6阶梯横盘蓄力': 7
        }
        primary = min(hold_patterns, key=lambda h: priority.get(h['name'], 99))
        decision = 'hold'
    else:
        primary = {'hit': False, 'name': '无形态', 'tag': '❓', 'type': 'none', 'detail': '趋势不明'}
        decision = 'reduce'
    
    return {
        'hold_patterns': hold_patterns,
        'warnings': warnings,
        'sell_signals': sell_signals,
        'buy_signals': buy_signals,
        'rebound_signals': rebound_signals,
        'primary': primary,
        'all_signals': all_signals,
        'decision': decision,
    }
