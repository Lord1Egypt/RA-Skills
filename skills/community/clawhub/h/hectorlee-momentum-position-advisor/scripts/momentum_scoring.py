"""
多维评分引擎 V1.3.5
100分制：趋势强度25 + 量能健康度20 + 衰竭信号25 + 均线支撑15 + 形态匹配15
         + 加仓信号10 + 量价共振10 + 持仓成本±8 + 资金流向8(可选)
新增：决策滞回(Hysteresis) + 减仓比例建议(Position Sizing) + 市场自适应
"""

from typing import List, Dict, Optional, Tuple
from utils import sma, bar_chart
def _bar(score: int, max_score: int, width: int = 10) -> str:
    """绘制进度条"""
    return bar_chart(score, max_score, width)


def score_trend_strength(kline: List[dict], params: dict = None, detect_result: dict = None) -> dict:
    """趋势强度 25分 + 底部反转额外加分"""
    p = params or {}
    max_score = 25
    score = 0
    details = []
    
    if len(kline) < 60:
        return {'score': 0, 'max': max_score, 'label': '趋势强度', 'details': ['K线不足60日']}
    
    closes = [k['close'] for k in kline]
    lows = [k['low'] for k in kline]
    opens = [k['open'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    ma5 = sma(closes, 5)
    ma10 = sma(closes, 10)
    ma20 = sma(closes, 20)
    ma60 = sma(closes, 60)
    
    # MA多头排列 +15
    if ma5[-1] > ma10[-1] > ma20[-1] > ma60[-1]:
        score += 15
        details.append('四线多头排列(+15)')
    elif ma10[-1] > ma20[-1] > ma60[-1]:
        score += 10
        details.append('MA10>20>60多头(+10)')
    elif ma20[-1] > ma60[-1]:
        score += 5
        details.append('MA20>MA60(+5)')
    
    # 站上MA20 +5
    if closes[-1] > ma20[-1]:
        score += 5
        details.append(f'站上MA20({ma20[-1]:.2f})(+5)')
    else:
        score -= 10
        details.append(f'跌破MA20({ma20[-1]:.2f})(-10)')
    
    # 站上MA60 +5（M1康复中跌破MA60仅轻罚）
    if closes[-1] > ma60[-1]:
        score += 5
        details.append(f'站上MA60({ma60[-1]:.2f})(+5)')
    else:
        # M1康复场景：轻罚
        m1_hold = False
        if detect_result:
            hold = detect_result.get('hold_patterns', [])
            m1_hold = any('M1' in h.get('name', '') or '底部启动' in h.get('name', '') for h in hold)
        
        if m1_hold and closes[-1] > ma20[-1]:
            score -= 5
            details.append(f'M1康复中跌破MA60({ma60[-1]:.2f})轻罚(-5)')
        elif closes[-1] > ma10[-1] and closes[-1] > ma20[-1]:
            # V1.3.2: 站上MA10+MA20双支撑时，跌破MA60仅减半罚
            # 短期趋势完好，MA60在上方属正常整理/横盘状态
            score -= 10
            details.append(f'跌破MA60({ma60[-1]:.2f})但MA10/20双支撑(-10)')
        else:
            score -= 15
            details.append(f'跌破MA60({ma60[-1]:.2f})(-15)')
    
    # === 底部反转加分：距60日低点<15%出现放量阳线 +10 ===
    low_60 = min(lows[-min(60, n):])
    dist_from_low = (closes[-1] - low_60) / low_60 * 100 if low_60 > 0 else 100
    is_bullish = closes[-1] > opens[-1]
    avg_vol_5 = sum(vols[-6:-1]) / 5 if n >= 6 else vols[-1]
    is_volume_break = vols[-1] > avg_vol_5 * 1.3
    
    if dist_from_low < 15 and is_bullish and is_volume_break:
        score += 10
        details.append(f'底部反转：距60日低{low_60:.2f}仅{dist_from_low:.1f}%放量阳线(+10)')
    
    score = max(0, min(max_score, score))
    return {'score': score, 'max': max_score, 'label': '趋势强度', 'details': details}


def score_volume_health(kline: List[dict], params: dict = None) -> dict:
    """量能健康度 20分"""
    max_score = 20
    score = 0
    details = []
    
    if len(kline) < 10:
        return {'score': 0, 'max': max_score, 'label': '量能健康度', 'details': ['K线不足']}
    
    closes = [k['close'] for k in kline]
    opens = [k['open'] for k in kline]
    vols = [k['volume'] for k in kline]
    n = len(kline)
    
    # 温和放量 +10（近5日均量 > 前20日均量，但不爆量<3x）
    vol_5 = sum(vols[-5:]) / 5
    vol_20 = sum(vols[-25:-5]) / 20 if n >= 25 else vol_5
    if vol_5 > vol_20 and vol_5 < vol_20 * 3:
        score += 10
        details.append('温和放量(+10)')
    elif vol_5 > vol_20 * 3:
        score += 5
        details.append(f'爆量({vol_5/vol_20:.1f}x)(+5)')
    else:
        details.append(f'量能萎缩({vol_5/vol_20:.1f}x)')
    
    # 上涨放量下跌缩量 +10
    up_vol = 0
    down_vol = 0
    up_count = 0
    down_count = 0
    for i in range(n-5, n):
        if closes[i] > opens[i]:
            up_vol += vols[i]
            up_count += 1
        else:
            down_vol += vols[i]
            down_count += 1
    
    if up_count > 0 and down_count > 0:
        avg_up = up_vol / up_count
        avg_down = down_vol / down_count
        if avg_up > avg_down:
            score += 10
            details.append('涨放量跌缩量(+10)')
        else:
            score -= 5
            details.append('量价背离(-5)')
    elif up_count > 0:
        score += 5
        details.append('近5日全阳(+5)')
    
    # 放量滞涨检查 -8
    for i in range(n-3, n):
        chg = abs(closes[i] - opens[i]) / opens[i] * 100
        avg_vol_5 = sum(vols[max(0,i-5):i]) / min(5, i)
        if vols[i] > avg_vol_5 * 2 and chg < 1:
            score -= 8
            details.append(f'{kline[i]["date"]}放量滞涨(-8)')
            break
    
    score = max(0, min(max_score, score))
    return {'score': score, 'max': max_score, 'label': '量能健康度', 'details': details}


def score_exhaustion(kline: List[dict], params: dict = None, detect_result: dict = None) -> dict:
    """衰竭信号 25分"""
    max_score = 25
    score = 25  # 满分开始，逐个扣
    details = []
    
    if len(kline) < 20:
        return {'score': 0, 'max': max_score, 'label': '衰竭信号', 'details': ['K线不足']}
    
    closes = [k['close'] for k in kline]
    opens = [k['open'] for k in kline]
    highs = [k['high'] for k in kline]
    n = len(kline)
    ma20 = sma(closes, 20)
    ma60 = sma(closes, 60) if n >= 60 else [0]
    
    # M1早期康复豁免：M1活跃且价格<MA60时，初期拉升是康复而非过热
    m1_active = False
    below_ma60 = ma60[-1] > 0 and closes[-1] < ma60[-1]
    if detect_result:
        hold = detect_result.get('hold_patterns', [])
        m1_hits = [h for h in hold if 'M1' in h.get('name', '') or '底部启动' in h.get('name', '')]
        m1_active = len(m1_hits) > 0
    
    m1_recovery = m1_active and below_ma60
    
    
    # 涨幅过热 -10（区分趋势加速 vs 超跌修复 vs M1早期康复）
    gain_20 = (closes[-1] - closes[-20]) / closes[-20] * 100
    gain_10 = (closes[-1] - closes[-10]) / closes[-10] * 100
    
    # 距60日高点回撤>40% -> 超跌修复场景，阈值放宽
    peak_60 = max(highs[-min(60, n):])
    dd_from_peak = (closes[-1] - peak_60) / peak_60 * 100 if peak_60 > 0 else 0
    is_bounce = dd_from_peak < -40
    
    # M1早期康复：底部启动的初期拉升是康复表现，豁免过热/加速惩罚
    if m1_recovery:
        score += 3
        details.append(f'M1底部康复(+3，涨幅{gain_10:.1f}%为正常修复)')
    else:
        gain20_threshold = 35 if is_bounce else 20
        gain10_threshold = 25 if is_bounce else 15
        
        if gain_20 > gain20_threshold:
            score -= 10
            scenario = "(超跌修复放宽)" if is_bounce else ""
            details.append(f'20日涨{gain_20:.1f}%过热{scenario}(-10)')
        elif gain_10 > gain10_threshold:
            score -= 5
            scenario = "(超跌修复放宽)" if is_bounce else ""
            details.append(f'10日涨{gain_10:.1f}%加速{scenario}(-5)')
        elif gain_20 < 5 and gain_10 < 3:
            score += 5
            details.append(f'涨幅适中(+5)')
    
    # 上影频繁 -8
    upper_count = 0
    for i in range(n-5, n):
        upper = (highs[i] - max(closes[i], opens[i])) / highs[i] * 100 if highs[i] > 0 else 0
        if upper > 3:
            upper_count += 1
    if upper_count >= 3:
        score -= 8
        details.append(f'上影频繁({upper_count}/5日)(-8)')
    elif upper_count == 0:
        score += 3
        details.append('无上影线(+3)')
    
    # 乖离过大 -7（M1早期康复免罚：底部拉升高乖离为正常表现）
    deviation = (closes[-1] - ma20[-1]) / ma20[-1] * 100
    if deviation > 15:
        if m1_recovery:
            score += 2
            details.append(f'M1康复乖离{deviation:.1f}%无需惩罚(+2)')
        else:
            score -= 7
            details.append(f'乖离{deviation:.1f}%(-7)')
    elif deviation < -10:
        score -= 5
        details.append(f'负乖离{deviation:.1f}%(-5)')
    
    # 回撤
    peak_10 = max(closes[-10:])
    dd = (closes[-1] - peak_10) / peak_10 * 100
    if dd > -3:
        score += 3
        details.append('回撤小(+3)')
    elif dd < -10:
        score -= 5
        details.append(f'回撤{abs(dd):.1f}%(-5)')
    
    score = max(0, min(max_score, score))
    return {'score': score, 'max': max_score, 'label': '衰竭信号', 'details': details}


def score_ma_support(kline: List[dict], params: dict = None, detect_result: dict = None) -> dict:
    """均线支撑 15分"""
    max_score = 15
    score = 0
    details = []
    
    if len(kline) < 60:
        return {'score': 0, 'max': max_score, 'label': '均线支撑', 'details': ['K线不足']}
    
    closes = [k['close'] for k in kline]
    n = len(kline)
    ma10 = sma(closes, 10)
    ma20 = sma(closes, 20)
    ma60 = sma(closes, 60)
    
    supports = [
        ('MA10', ma10[-1], closes[-1] > ma10[-1]),
        ('MA20', ma20[-1], closes[-1] > ma20[-1]),
        ('MA60', ma60[-1], closes[-1] > ma60[-1]),
    ]
    
    for name, ma_val, above in supports:
        if above:
            score += 5
            details.append(f'{name}({ma_val:.2f})支撑(+5)')
    
    if score == 0:
        details.append('无近端均线支撑(0)')
    
    return {'score': score, 'max': max_score, 'label': '均线支撑', 'details': details}


def score_pattern_match(detect_result: dict, params: dict = None, kline: list = None, vp_result: dict = None) -> dict:
    """形态匹配 15分"""
    max_score = 15
    score = 0
    details = []
    
    hold = detect_result.get('hold_patterns', [])
    sell = detect_result.get('sell_signals', [])
    
    if sell:
        score = 0
        details.append(f'卖出信号触发 → 0分')
        return {'score': score, 'max': max_score, 'label': '形态匹配', 'details': details}
    
    if hold:
        # 取最强的持有形态
        best = max(hold, key=lambda h: h.get('score_base', 0))
        base = best.get('score_base', 8)
        # M1~M3/M12~M13: 12~15分; M4~M6: 8~12分; M0: 8分
        score = min(max_score, max(8, base - 2))
        details.append(f'{best["name"]}({best["tag"]}) 基础分{base} → 匹配{score}/{max_score}')
        return {'score': score, 'max': max_score, 'label': '形态匹配', 'details': details}
    
    # V1.3.2: 无M1-M6命中时，检测 M0 横盘整理通用形态
    # 条件：站上MA10+MA20 + VP横盘确认
    if kline and vp_result:
        closes = [k['close'] for k in kline]
        n = len(kline)
        
        def sma(arr, w):
            r = []
            for i in range(len(arr)):
                if i < w-1:
                    r.append(sum(arr[:i+1])/(i+1))
                else:
                    r.append(sum(arr[i-w+1:i+1])/w)
            return r
        
        ma10 = sma(closes, 10)
        ma20 = sma(closes, 20)
        above_ma10 = closes[-1] > ma10[-1]
        above_ma20 = closes[-1] > ma20[-1]
        vp_hit = vp_result.get('hit', False)
        vp_confirmed = vp_hit and not vp_result.get('warning')
        
        if above_ma10 and above_ma20 and vp_confirmed:
            score = 8
            details.append(f'M0横盘整理 🪜 站上MA10({ma10[-1]:.2f})/MA20({ma20[-1]:.2f})+VP确认 → 匹配{score}/{max_score}')
            return {'score': score, 'max': max_score, 'label': '形态匹配', 'details': details}
    
    score = 0
    details.append('无持有形态命中 → 0分')
    return {'score': score, 'max': max_score, 'label': '形态匹配', 'details': details}


def score_buy_signals(detect_result: dict, vp_result: dict = None, params: dict = None) -> dict:
    """加仓信号评分 0-10分"""
    max_score = 10
    score = 0
    details = []
    
    buy = detect_result.get('buy_signals', [])
    sell = detect_result.get('sell_signals', [])
    
    # 卖出区间不加仓
    if sell:
        return {'score': 0, 'max': max_score, 'label': '加仓信号', 
                'details': ['卖出信号触发，不加仓'], 'buy_advice': None}
    
    if not buy:
        return {'score': 0, 'max': max_score, 'label': '加仓信号',
                'details': ['无加仓信号'], 'buy_advice': None}
    
    # VP背离 → 否决加仓
    if vp_result and vp_result.get('warning'):
        return {'score': 0, 'max': max_score, 'label': '加仓信号',
                'details': [f'VP背离预警({vp_result["warning"]})，否决加仓'], 'buy_advice': None}
    
    buy_count = len(buy)
    buy_names = [b['name'] for b in buy]
    
    has_b3 = any(b['name'] == 'B3整理突破' for b in buy)
    has_b2 = any(b['name'] == 'B2回踩确认' for b in buy)
    has_b1 = any(b['name'] == 'B1反包阳线' for b in buy)
    has_b4 = any(b['name'] == 'B4缩尽首阳' for b in buy)
    
    if has_b3 or buy_count >= 2:
        grade = 3
        score = 8
        grade_label = '强烈建议加仓'
    elif has_b2 or (has_b1 and vp_result and vp_result.get('score', 0) >= 60):
        grade = 2
        score = 5
        grade_label = '建议加仓'
    elif has_b1 or has_b4:
        grade = 1
        score = 3
        grade_label = '可轻仓试探'
    else:
        grade = 0
        grade_label = ''
        score = 0
    
    # VP共振加成
    if vp_result and vp_result.get('score', 0) >= 80:
        if grade < 3:
            grade += 1
        score += 2
        details.append(f'VP{vp_result["variant"]}{vp_result["label"]}>=80分 → 信号升级')
    elif vp_result and vp_result.get('score', 0) >= 60 and score > 0:
        score += 2
        details.append(f'VP{vp_result["variant"]}{vp_result["label"]}共振(+2)')
    
    stars = '⭐' * grade if grade > 0 else ''
    detail_line = f'{"+".join(buy_names)} {stars} {grade_label}'
    details.insert(0, detail_line)
    
    score = min(max_score, score)
    
    return {
        'score': score, 'max': max_score, 'label': '加仓信号',
        'details': details,
        'buy_advice': grade_label if grade_label else None,
        'buy_grade': grade,
    }


def compute_cost_factor(price: float, cost: float) -> dict:
    """持仓成本因子：根据盈亏幅度调整决策紧迫度（-8 ~ +8分）
    
    逻辑：
    - 大盈(≥30%) → +8：利润厚，可以等，不急着卖
    - 中盈(≥15%) → +5
    - 小盈(0-15%) → 0
    - 小亏(0~-10%) → -3：开始浮亏，要注意
    - 大亏(≤-10%) → -8：止损优先，果断卖出
    """
    if cost is None or cost <= 0 or price <= 0:
        return {'score': 0, 'max': 8, 'label': '持仓成本', 
                'details': ['无成本数据'], 'pnl_pct': None}
    
    pnl_pct = (price - cost) / cost * 100
    
    if pnl_pct >= 30:
        score = 8
        reason = f'大幅盈利{pnl_pct:+.1f}%，利润缓冲充裕(+8)'
    elif pnl_pct >= 15:
        score = 5
        reason = f'稳健盈利{pnl_pct:+.1f}%，可从容决策(+5)'
    elif pnl_pct >= 5:
        score = 2
        reason = f'小幅盈利{pnl_pct:+.1f}%，略有缓冲(+2)'
    elif pnl_pct >= -3:
        score = 0
        reason = f'盈亏平衡{pnl_pct:+.1f}%(0)'
    elif pnl_pct >= -10:
        score = -3
        reason = f'小幅浮亏{pnl_pct:+.1f}%，关注风险(-3)'
    else:
        score = -8
        reason = f'大幅亏损{pnl_pct:+.1f}%，止损优先级高(-8)'
    
    return {
        'score': score, 
        'max': 8, 
        'label': '持仓成本',
        'details': [reason],
        'pnl_pct': round(pnl_pct, 1),
    }


def score_fund_flow(fund_flow: dict = None) -> dict:
    """资金流向维度 0-8分（可选数据源：DPP/westockdata）
    
    当 fund_flow 为 None 时返回 0 分（数据不可用，不扣分）
    
    fund_flow 格式:
    {
        'main_net_inflow_5d': 1.25,    # 近5日主力净流入(亿)，正=流入
        'main_net_inflow_today': 0.35,  # 今日主力净流入(亿)
        'retail_net_outflow_5d': -0.8,  # 近5日散户净流出(亿)
        'big_order_ratio': 0.15,        # 大单比例
    }
    """
    max_score = 8
    if fund_flow is None:
        return {'score': 0, 'max': max_score, 'label': '资金流向',
                'details': ['无资金数据'], 'active': False}
    
    score = 0
    details = []
    active = True
    
    inflow_5d = fund_flow.get('main_net_inflow_5d', 0)
    inflow_today = fund_flow.get('main_net_inflow_today', 0)
    big_order = fund_flow.get('big_order_ratio', 0)
    
    # 近5日主力持续流入
    if inflow_5d > 0.5:
        score += 5
        details.append(f'近5日主力净流入{inflow_5d:.2f}亿(+5)')
    elif inflow_5d > 0:
        score += 3
        details.append(f'近5日主力小幅净流入{inflow_5d:.2f}亿(+3)')
    elif inflow_5d < -1.0:
        score -= 5
        details.append(f'近5日主力净流出{abs(inflow_5d):.2f}亿(-5)')
    elif inflow_5d < 0:
        score -= 2
        details.append(f'近5日主力小幅净流出{abs(inflow_5d):.2f}亿(-2)')
    
    # 今日扭转 vs 5日趋势
    if inflow_5d < 0 and inflow_today > 0.3:
        score += 3
        details.append(f'主力方向扭转：今日净流入{inflow_today:.2f}亿(+3)')
    elif inflow_5d > 0 and inflow_today < -0.3:
        score -= 3
        details.append(f'主力方向逆转：今日净流出{abs(inflow_today):.2f}亿(-3)')
    
    # 大单比例
    if big_order > 0.2:
        score += 3
        details.append(f'大单占比{big_order:.0%}偏高(+3)')
    elif big_order < 0.05 and inflow_5d > 0:
        details.append(f'大单占比{big_order:.0%}偏低，散户主导')
    
    score = max(-8, min(max_score, score))
    return {'score': score, 'max': max_score, 'label': '资金流向',
            'details': details, 'active': active}


def compute_position_size(decision: str, total: int, base_total: int,
                          cost_factor: dict = None, sector_downgraded: bool = False,
                          ma_healthy_pullback: bool = False) -> dict:
    """减仓比例建议 V1.3.5
    
    不影响方向性判断，纯粹基于分数区间+上下文给出定量建议。
    
    返回:
    {
        'action': 'hold' | 'reduce' | 'sell',
        'ratio': 0.0 ~ 1.0,     # 建议调整比例（对现有持仓）
        'label': '持有不动' | '减仓20%' | '清仓' 等,
        'reason': '...',
    }
    """
    pnl_pct = cost_factor.get('pnl_pct') if cost_factor else None
    
    if decision in ('hold', 'hold_buy'):
        return {'action': 'hold', 'ratio': 0, 'label': '持有不动',
                'reason': '动量评分健康，无需减仓'}
    
    if decision == 'watch':
        return {'action': 'watch', 'ratio': 0, 'label': '观望不动',
                'reason': '边界信号，观望等方向确认'}
    
    # === REDUCE 场景 ===
    if decision == 'reduce':
        if total >= 60:
            ratio = 0.25  # 减25%
            label = '减仓25%'
            reason = '偏持有观望，轻仓试探性减仓'
        elif total >= 50:
            ratio = 0.50  # 减50%
            label = '减仓50%'
            reason = '偏谨慎，保留半仓等确认'
        elif total >= 40:
            ratio = 0.65  # 减65%
            label = '减仓65%'
            reason = '弱势整理，大幅度减仓避险'
        else:
            ratio = 0.80
            label = '减仓80%'
            reason = '深度弱势，接近清仓'
        
        # MA多头回调 → 减仓比例下调10%
        if ma_healthy_pullback:
            ratio = max(0.1, ratio - 0.10)
            reason += '；均线多头回调，比例下调10%'
        
        # 板块共振 → 减仓比例上浮15%
        if sector_downgraded:
            ratio = min(1.0, ratio + 0.15)
            reason += '；板块共振，比例上浮15%'
        
        # 大盈缓冲 → 减仓比例下调
        if pnl_pct and pnl_pct >= 30:
            ratio = max(0.05, ratio - 0.15)
            reason += f'；大盈{pnl_pct:+.1f}%缓冲，比例再降15%'
        elif pnl_pct and pnl_pct >= 15:
            ratio = max(0.05, ratio - 0.05)
            reason += f'；中盈{pnl_pct:+.1f}%，比例微降5%'
        
        # 大亏 → 减仓优先级高
        if pnl_pct and pnl_pct <= -10:
            ratio = min(1.0, ratio + 0.10)
            reason += f'；大亏{pnl_pct:+.1f}%，止损优先，比例上浮10%'
        
        ratio = round(ratio, 2)
        label = f'减仓{int(ratio*100)}%'
        
        return {'action': 'reduce', 'ratio': ratio, 'label': label, 'reason': reason}
    
    # === SELL 场景 ===
    if decision == 'sell':
        if total >= 30:
            ratio = 0.80
            label = '减仓80%'
            reason = '破位卖出，留少量观察仓'
        else:
            ratio = 1.0
            label = '清仓'
            reason = '深度破位，建议清仓'
        
        # 大盈 → 可留观察仓
        if pnl_pct and pnl_pct >= 30 and ratio == 1.0:
            ratio = 0.90
            label = '减仓90%'
            reason += f'；大盈{pnl_pct:+.1f}%，可留观察仓'
        
        return {'action': 'sell', 'ratio': ratio, 'label': label, 'reason': reason}
    
    return {'action': 'unknown', 'ratio': 0, 'label': '未知', 'reason': ''}


def calculate_score(kline: List[dict], detect_result: dict, 
                    vp_bonus: int = 0, vp_reason: str = '',
                    vp_result: dict = None,
                    cost: float = None, latest_price: float = None,
                    params: dict = None,
                    prev_decision: str = None,
                    fund_flow: dict = None,
                    market_regime: str = None,
                    code: str = '',
                    fundamental: dict = None,
                    events: list = None) -> dict:
    """
    计算完整的多维评分 + 量价共振加成 + 持仓成本因子 + 资金流向 + 决策滞回
    
    参数:
        vp_bonus: 量价收敛共振加成 (-10 ~ +12)
        vp_reason: 加成理由
        cost: 持仓成本价
        latest_price: 最新价格（用于成本计算）
        prev_decision: 前日决策（用于滞回防震荡）
        fund_flow: 资金流向数据（可选）
        market_regime: 大盘环境 'bull'/'sideways'/'bear'（可选）
    
    返回:
    {
        'total': 82,
        'base_total': 80,
        'max_total': 108,      # 含资金流向8分
        'decision': 'hold' | 'reduce' | 'sell' | 'watch',
        'dimensions': [...],
        'vp_dim': {...},
        'cost_dim': {...},
        'fund_flow_dim': {...},
        'vp_reason': '...',
        'position_size': {...},  # V1.3.5 新增
        'hysteresis_applied': False,  # V1.3.5 新增
    }
    """
    p = params or {}
    
    dims = [
        score_trend_strength(kline, p, detect_result),
        score_volume_health(kline, p),
        score_exhaustion(kline, p, detect_result),
        score_ma_support(kline, p, detect_result),
        score_pattern_match(detect_result, p, kline, vp_result),
    ]
    
    base_total = sum(d['score'] for d in dims)
    
    # 加仓信号评分
    buy_dim = score_buy_signals(detect_result, vp_result, p)
    dims.append(buy_dim)
    
    # 持仓成本因子
    cost_dim = compute_cost_factor(latest_price or 0, cost or 0)
    
    # 资金流向维度（可选数据源，无数据时自动跳过）
    fund_flow_dim = score_fund_flow(fund_flow)
    
    total = base_total + vp_bonus + buy_dim['score'] + cost_dim['score'] + fund_flow_dim['score']
    total = max(0, min(108, total))
    
    # 量价共振维度（先构建，用于质量置信度计算）
    vp_dim = {
        'score': max(0, vp_bonus + 5),
        'max': 10,
        'label': '量价共振',
        'details': [vp_reason] if vp_reason else ['无共振信号'],
        'raw_bonus': vp_bonus,
    }
    
    # === V1.3.2: 质量置信度 + MA结构检测 ===
    all_dims = dims + [vp_dim, fund_flow_dim]
    healthy_count = sum(1 for d in all_dims if d['max'] > 0 and d['score'] >= d['max'] * 0.6)
    
    # MA多头结构检测（均线排列健康，即使价格暂时跌破）
    def _sma(arr, w):
        r = []
        for i in range(len(arr)):
            if i < w-1: r.append(sum(arr[:i+1])/(i+1))
            else: r.append(sum(arr[i-w+1:i+1])/w)
        return r
    closes_kl = [k['close'] for k in kline]
    ma10_arr = _sma(closes_kl, 10)
    ma20_arr = _sma(closes_kl, 20)
    ma60_arr = _sma(closes_kl, 60)
    
    ma_bullish = (ma10_arr[-1] > ma20_arr[-1] > ma60_arr[-1])  # MA多头排列
    ma_broken = closes_kl[-1] < ma20_arr[-1]                     # 价格跌破MA20
    ma_healthy_pullback = ma_bullish and ma_broken               # 均线多头但价格回调

    # V1.3.3: 双支撑弱势整理检测
    # 股价站上MA10+MA20但跌破MA60 → 短期有支撑，中期未修复，窄幅整理特征
    price = closes_kl[-1]
    ma1020_double_support = (price > ma10_arr[-1]) and (price > ma20_arr[-1])
    ma60_broken = price < ma60_arr[-1]
    double_support_weak = ma1020_double_support and ma60_broken and not ma_bullish

    # V1.3.4: 深度回撤+阳线检测（底部反弹初期判断）
    # 回撤>20% + 收阳 → 止跌信号，非趋势延续。底部反弹初期天然缩量，不做量能要求
    highs_kl = [k['high'] for k in kline]
    opens_kl = [k['open'] for k in kline]
    peak20 = max(highs_kl[-20:]) if len(highs_kl) >= 20 else max(highs_kl)
    drawdown = (price / peak20 - 1) * 100
    is_bullish_day = (closes_kl[-1] > opens_kl[-1])
    deep_rebound_watch = (drawdown < -20) and is_bullish_day
    
    # 信号提取
    detect_result = detect_result or {}
    hold = detect_result.get('hold_patterns', [])
    has_m1 = any('M1' in h.get('name', '') or '底部启动' in h.get('name', '') for h in hold)
    exhaust_dim = [d for d in dims if d['label'] == '衰竭信号']
    exhaust_healthy = exhaust_dim and exhaust_dim[0]['score'] >= 23
    rebound = detect_result.get('rebound_signals', [])
    has_rebound = bool(rebound)
    sell_signals = detect_result.get('sell_signals', [])
    has_sell_signal = bool(sell_signals)  # V1.3.3: 是否有明确卖出形态触发
    
    # === V1.3.5: 市场环境自适应阈值调整 ===
    # 牛市放宽阈值（持股更宽容），熊市收紧阈值（卖出更敏感）
    regime_shift = 0
    regime_note = ''
    if market_regime == 'bull':
        regime_shift = -5  # 所有阈值降低5分，更容易HOLD
        regime_note = '牛市环境，阈值-5(宽容持股)'
    elif market_regime == 'bear':
        regime_shift = +5  # 所有阈值提高5分，更容易SELL
        regime_note = '熊市环境，阈值+5(谨慎减仓)'
    # 'sideways' 或 None → 标准阈值，shift=0
    
    # 应用阈值偏移（所有边界减regime_shift）
    t_high = 75 + regime_shift
    t_upper = 65 + regime_shift
    t_mid = 50 + regime_shift
    t_low = 35 + regime_shift
    
    # === 决策引擎 V1.3.2 重构 ===
    if total >= t_high:
        decision = 'hold'
        quality_note = f'HOLD 标准持有 {healthy_count}/{len(all_dims)}维健康'
        
    elif total >= t_upper:
        # M1 康复场景：放宽至 65
        if has_m1 and exhaust_healthy:
            decision = 'hold'
            quality_note = f'HOLD M1康复 {healthy_count}/{len(all_dims)}维健康'
        # 质量升级：4维+健康 → HOLD（但 MA 多头回调降为 REDUCE）
        elif healthy_count >= 4:
            if ma_healthy_pullback:
                decision = 'reduce'
                quality_note = f'REDUCE MA多头回调 {healthy_count}/{len(all_dims)}维健康'
            else:
                decision = 'hold'
                quality_note = f'HOLD 质量升级 {healthy_count}/{len(all_dims)}维健康'
        else:
            decision = 'reduce'
            quality_note = f'REDUCE 偏谨慎 {healthy_count}/{len(all_dims)}维健康'
        
    elif total >= t_mid:
        # 反弹信号或 M1 活跃或底部反弹 → WATCH
        if has_rebound:
            decision = 'watch'
            quality_note = f'WATCH 反弹博弈 {healthy_count}/{len(all_dims)}维健康'
        elif deep_rebound_watch:
            decision = 'watch'
            quality_note = f'WATCH 底部反弹 {healthy_count}/{len(all_dims)}维健康'
        elif has_m1:
            decision = 'watch'
            quality_note = f'WATCH M1康复观察 {healthy_count}/{len(all_dims)}维健康'
        elif healthy_count >= 4:
            decision = 'reduce'
            quality_note = f'REDUCE 偏持有观望 {healthy_count}/{len(all_dims)}维健康'
        else:
            decision = 'reduce'
            quality_note = f'REDUCE 偏谨慎 {healthy_count}/{len(all_dims)}维健康'
        
    elif total >= t_low:
        # 反弹信号 → WATCH
        if has_rebound:
            decision = 'watch'
            quality_note = f'WATCH 超跌反弹 {healthy_count}/{len(all_dims)}维健康'
        # V1.3.5-fix: 底部反弹保护同样适用于35-49区间（之前仅<35有效，边界震荡会漏判）
        elif deep_rebound_watch:
            decision = 'watch'
            quality_note = f'WATCH 底部反弹 {healthy_count}/{len(all_dims)}维健康'
        # 均线多头结构 → 涨多回调，不卖出
        elif ma_bullish:
            decision = 'reduce'
            quality_note = f'REDUCE 均线多头回调 {healthy_count}/{len(all_dims)}维健康'
        # V1.3.3: MA10/20双支撑+跌破MA60+无明确卖出信号 → 弱势整理，WATCH
        elif double_support_weak and not has_sell_signal:
            decision = 'watch'
            quality_note = f'WATCH 弱势整理 {healthy_count}/{len(all_dims)}维健康'
        else:
            decision = 'sell'
            quality_note = f'SELL 弱势破位 {healthy_count}/{len(all_dims)}维健康'
    
    else:
        # <35 深度破位，但反弹信号可降级为 WATCH
        if has_rebound:
            decision = 'watch'
            quality_note = f'WATCH 超跌反弹 {healthy_count}/{len(all_dims)}维健康'
        # V1.3.4: 深度回撤+阳线 → 反弹初期，升级WATCH
        elif deep_rebound_watch:
            decision = 'watch'
            quality_note = f'WATCH 底部反弹 {healthy_count}/{len(all_dims)}维健康'
        else:
            decision = 'sell'
            quality_note = f'SELL 深度破位 {healthy_count}/{len(all_dims)}维健康'
    
    # 加仓信号覆盖：≥60分基础 + 加仓≥2星 → 升级持有
    buy_grade = buy_dim.get('buy_grade', 0)
    if base_total >= 60 and buy_grade >= 2 and decision in ('reduce', 'watch'):
        decision = 'hold_buy'
        quality_note += ' → 加仓升级HOLD'
    
    # === V1.3.5: 决策滞回(Hysteresis) —— 防止边界震荡 ===
    hysteresis_applied = False
    hysteresis_zone = 5  # 边界缓冲区宽度
    
    if prev_decision and prev_decision not in ('', 'unknown'):
        # 当分数在边界附近时，维持前日决策
        # 需要连续2日突破阈值才改变方向
        def _decision_rank(d):
            return {'hold': 0, 'hold_buy': 0, 'watch': 1, 'reduce': 2, 'sell': 3}.get(d, 99)
        
        curr_rank = _decision_rank(decision)
        prev_rank = _decision_rank(prev_decision)
        
        # 同级别决策区间映射（用于判断是否在滞回区内）
        # 每个决策对应的阈值区间
        if decision != prev_decision:
            boundary_check = False
            
            # 检查是否在滞回边界
            if prev_decision == 'reduce' and decision in ('watch', 'hold'):
                # 从reduce上调到watch/hold，检查分数是否在t_mid+hysteresis_zone范围内
                if total < t_mid + hysteresis_zone:
                    boundary_check = True
            elif prev_decision == 'watch' and decision in ('sell', 'reduce'):
                # 从watch下调到sell/reduce
                if total > t_low - hysteresis_zone:
                    boundary_check = True
            elif prev_decision == 'sell' and decision == 'watch':
                # 从sell上调到watch（反弹）
                if total < t_low + hysteresis_zone:
                    boundary_check = True
            elif prev_decision == 'hold' and decision in ('reduce', 'watch'):
                if total > t_upper - hysteresis_zone:
                    boundary_check = True
            elif prev_decision == 'reduce' and decision == 'sell':
                if total > t_low - hysteresis_zone:
                    boundary_check = True
            
            if boundary_check:
                decision = prev_decision
                hysteresis_applied = True
                quality_note += f' [滞回: 维持{prev_decision.upper()}，{total}分在边界±{hysteresis_zone}内]'
    
    # === V1.4.0: 逻辑覆盖层 —— 四层判断框架最终裁决 ===
    # 纯量价决策之后，叠加：逻辑证伪/量价破坏分级/资金承接/事件日历
    overlay_notes = []
    if fundamental is not None or events:
        try:
            from logic_overlay import apply_logic_overlay
            decision, quality_note, overlay_notes = apply_logic_overlay(
                decision, quality_note, code=code,
                kline=kline, detect_result=detect_result,
                fundamental=fundamental or {}, events=events or [])
        except Exception as e:
            import sys as _sys
            print(f'[logic_overlay] 覆盖层执行失败，退回纯量价决策: {e}', file=_sys.stderr)

    # === V1.3.5: 减仓比例建议 ===
    sector_downgraded = False  # 板块共振标记（由外部设置）
    position_size = compute_position_size(
        decision, total, base_total,
        cost_dim, sector_downgraded, ma_healthy_pullback
    )
    
    return {
        'total': total,
        'base_total': base_total,
        'max_total': 108,
        'decision': decision,
        'dimensions': dims,
        'vp_dim': vp_dim,
        'cost_dim': cost_dim,
        'fund_flow_dim': fund_flow_dim,
        'vp_reason': vp_reason,
        'buy_advice': buy_dim.get('buy_advice'),
        'buy_grade': buy_dim.get('buy_grade', 0),
        'quality_note': quality_note,
        'healthy_count': healthy_count,
        'position_size': position_size,
        'hysteresis_applied': hysteresis_applied,
        'regime_note': regime_note,
        'market_regime': market_regime,
        'overlay_notes': overlay_notes,
    }


def compute_trend_duration(kline: List[dict]) -> str:
    """计算趋势持续时间统计"""
    if not kline or len(kline) < 20:
        return ''
    
    closes = [k['close'] for k in kline]
    opens = [k['open'] for k in kline]
    highs = [k['high'] for k in kline]
    n = len(kline)
    ma20 = sma(closes, 20)
    ma60 = sma(closes, 60) if n >= 60 else [0]
    
    # 连续站上MA20天数
    above_ma20_days = 0
    for i in range(n-1, -1, -1):
        if closes[i] > ma20[i]:
            above_ma20_days += 1
        else:
            break
    
    # 连续阳线天数
    bull_days = 0
    for i in range(n-1, -1, -1):
        if closes[i] > opens[i]:
            bull_days += 1
        else:
            break
    
    # 距20日高点天数
    peak_20 = max(highs[-20:])
    peak_20_idx = n - 1
    for i in range(n-1, n-21, -1):
        if highs[i] == peak_20:
            peak_20_idx = i
            break
    days_from_peak = n - 1 - peak_20_idx
    
    # 距60日高点天数
    peak_60_idx = n - 1
    if n >= 60:
        peak_60 = max(highs[-60:])
        for i in range(n-1, n-61, -1):
            if highs[i] == peak_60:
                peak_60_idx = i
                break
    
    parts = []
    if above_ma20_days >= 3:
        parts.append(f'MA20+{above_ma20_days}d')
    else:
        parts.append(f'BELOW MA20')
    
    if bull_days >= 2:
        parts.append(f'{bull_days}bull')
    
    if days_from_peak <= 3 and closes[-1] >= peak_20 * 0.98:
        parts.append(f'near peak')
    elif days_from_peak > 0:
        dd_pct = (closes[-1] - peak_20) / peak_20 * 100
        parts.append(f'peak{days_from_peak}d ago {dd_pct:+.1f}%')
    
    return ' | '.join(parts)


def format_score_output(score_result: dict, detect_result: dict, 
                         name: str = '', code: str = '',
                         cost: float = None, latest_price: float = None,
                         kline: List[dict] = None) -> str:
    """格式化评分为可打印文本"""
    lines = []
    
    # 头部
    lines.append("=== Momentum Position Advisor -- " + name + "(" + code + ") ===")
    
    # 价格行 + 趋势统计
    price_line = f"Price: {latest_price:.2f}" if latest_price else ""
    if cost and latest_price:
        pnl = (latest_price - cost) / cost * 100
        price_line += f" | Cost: {cost:.2f} | PnL: {pnl:+.1f}%"
    lines.append(price_line)
    
    # 趋势持续时间
    trend_stats = compute_trend_duration(kline)
    if trend_stats:
        lines.append(f"Trend: {trend_stats}")
    lines.append("")
    
    # 形态命中
    decision_tag = {'hold': 'HOLD', 'hold_buy': 'HOLD +BUY', 'reduce_watch': 'REDUCE+', 'reduce': 'REDUCE', 'watch': 'WATCH', 'sell': 'SELL'}
    primary = detect_result.get('primary', {})
    
    base = score_result.get('base_total', score_result['total'])
    vp_bonus_raw = score_result.get('vp_dim', {}).get('raw_bonus', 0)
    cost_bonus = score_result.get('cost_dim', {}).get('score', 0)
    
    bonus_parts = []
    if vp_bonus_raw != 0:
        bonus_parts.append(f"VP{'+' if vp_bonus_raw > 0 else ''}{vp_bonus_raw}")
    if cost_bonus != 0:
        bonus_parts.append(f"成本{'+' if cost_bonus > 0 else ''}{cost_bonus}")
    
    bonus_str = f"({' '.join(bonus_parts)})" if bonus_parts else ""
    if bonus_str:
        lines.append(f"Decision: {decision_tag.get(score_result['decision'], '?')}  {score_result['total']}/{score_result['max_total']}pts ({base}{bonus_str})")
    else:
        lines.append(f"Decision: {decision_tag.get(score_result['decision'], '?')}  {score_result['total']}/{score_result['max_total']}pts")
    lines.append("Primary: " + primary.get('name', 'None') + " " + primary.get('tag', ''))
    
    warnings = detect_result.get('warnings', [])
    if warnings:
        warn_names = ' | '.join(f"{w['tag']} {w['name']}" for w in warnings if w.get('hit'))
        lines.append("  WARN: " + warn_names)
    
    lines.append("")
    
    # 五维评分
    for dim in score_result['dimensions']:
        bar = _bar(dim['score'], dim['max'])
        lines.append(f"{dim['label']:<8} {bar} {dim['score']}/{dim['max']}")
        for d in dim.get('details', []):
            lines.append(f"  {d}")
    
    # 量价共振维度
    vp_dim = score_result.get('vp_dim')
    if vp_dim:
        bar = _bar(vp_dim['score'], vp_dim['max'])
        bonus_str = f"(+{vp_dim['raw_bonus']})" if vp_dim['raw_bonus'] > 0 else f"({vp_dim['raw_bonus']})" if vp_dim['raw_bonus'] < 0 else ""
        lines.append(f"{vp_dim['label']:<8} {bar} {vp_dim['score']}/{vp_dim['max']} {bonus_str}")
        for d in vp_dim.get('details', []):
            lines.append(f"  {d}")
    
    # 持仓成本维度
    cost_dim = score_result.get('cost_dim')
    if cost_dim and cost_dim.get('score', 0) != 0:
        bar = _bar(max(0, cost_dim['score'] + 8), 16)  # 偏移展示
        lines.append(f"{cost_dim['label']:<8} {bar} {cost_dim['score']:+.0f}/±8")
        for d in cost_dim.get('details', []):
            lines.append(f"  {d}")
    
    # 资金流向维度
    fund_flow_dim = score_result.get('fund_flow_dim')
    if fund_flow_dim and fund_flow_dim.get('active'):
        bar = _bar(max(0, fund_flow_dim['score'] + 8), 16)  # 偏移展示
        lines.append(f"{fund_flow_dim['label']:<8} {bar} {fund_flow_dim['score']:+.0f}/{fund_flow_dim['max']}")
        for d in fund_flow_dim.get('details', []):
            lines.append(f"  {d}")
    
    lines.append("")
    
    # 反弹博弈信号 🎲
    rebound = detect_result.get('rebound_signals', [])
    if rebound:
        risk_level = {'R1恐慌抛售反弹': '高确定性', 'R2缩量衰竭反弹': '中等概率', 'R3超跌均值回归': '纯统计'}
        lines.append("─── 🎲 反弹博弈信号 (高风险投机) ───")
        for r in rebound:
            quality = r.get('quality', 0)
            stars = '★★★' if quality >= 60 else '★★' if quality >= 40 else '★'
            risk = risk_level.get(r['name'], '未知')
            lines.append(f"  {r['tag']} {r['name']} {stars} 质量{quality}分 [{risk}]")
            lines.append(f"     {r['detail']}")
        lines.append("  ⚠️ 反弹博弈 ≠ 趋势反转，建议严格止损(入场价-5%)")
        lines.append("")
    
    # 决策建议
    quality_note = score_result.get('quality_note', '')
    lines.append(f"Advice: {quality_note}")
    
    # 减仓比例建议
    position_size = score_result.get('position_size')
    if position_size and position_size.get('action') in ('reduce', 'sell'):
        lines.append(f"Position: {position_size['label']} ({position_size['reason']})")
    
    # 滞回标记
    if score_result.get('hysteresis_applied'):
        lines.append(f"Hysteresis: 边界震荡保护已激活，维持前日决策")
    
    # 市场环境
    regime_note = score_result.get('regime_note')
    if regime_note:
        lines.append(f"Regime: {regime_note}")
    
    lines.append("")
    
    return '\n'.join(lines)


def format_score_compact(score_result: dict, detect_result: dict,
                          name: str, code: str) -> str:
    """简洁单行输出"""
    decision_icons = {'hold': '[HOLD]', 'hold_buy': '[HOLD+BUY]', 'reduce_watch': '[REDUCE+]', 'reduce': '[REDUCE]', 'watch': '[WATCH]', 'sell': '[SELL]'}
    icon = decision_icons.get(score_result['decision'], '[?]')
    primary = detect_result.get('primary', {})
    warnings = detect_result.get('warnings', [])
    warn_str = ''
    if warnings:
        warn_names = [w['name'] for w in warnings if w.get('hit')]
        if warn_names:
            warn_str = f"  ⚠{'|'.join(warn_names)}"
    
    # 减仓比例
    pos_str = ''
    pos = score_result.get('position_size')
    if pos and pos.get('action') in ('reduce', 'sell'):
        pos_str = f"  [{pos['label']}]"
    
    # 滞回标记
    hyst_str = ' [滞回]' if score_result.get('hysteresis_applied') else ''
    
    return f"  {icon} {name}({code})  {score_result['decision']}  {score_result['total']}分  {primary.get('name', '无形态')}{pos_str}{warn_str}{hyst_str}"
