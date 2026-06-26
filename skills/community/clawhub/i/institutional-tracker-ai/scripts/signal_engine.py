"""
多信号评分引擎 v8 - 论文方法论改进
v8变更:
  - 资金流按市值归一化 (论文: Kang 2025)
  - 反转量价逻辑: 放量上涨降权、缩量企稳加权 (论文: 量价趋势2023, 国金2022)
  - 散户反向过滤: 小单净流入反向信号 (论文: 上交大2019, Ravina 2023)
v7: 新增 detect_distribution_v2() 多条件组合确认出货
v6: 筹码分布(获利盘/套牢盘)、OBV能量潮背离、结构破裂BOS/CHoCH、CMF蔡金资金流
参考: github.com/liumenglife/ChipDistribution, github.com/Siva7891/smart-money-concepts, ta library
"""
from typing import Dict, List, Tuple
import math


# ============================================================
# 辅助函数：从 GitHub 开源算法移植的技术指标
# ============================================================

def calc_obv(daily: List[Dict]) -> List[float]:
    """OBV (On-Balance Volume) 能量潮指标
    参考: github.com/build-web/ta
    逻辑: 上涨日成交量累加，下跌日成交量累减
    """
    if not daily:
        return []
    obv = [0.0]
    for i in range(1, len(daily)):
        close_today = float(daily[i-1].get("close", 0) or 0)  # daily倒序
        close_prev = float(daily[i].get("close", 0) or 0)
        vol = float(daily[i-1].get("vol", 0) or 0)
        if close_today > close_prev:
            obv.append(obv[-1] + vol)
        elif close_today < close_prev:
            obv.append(obv[-1] - vol)
        else:
            obv.append(obv[-1])
    return obv


def calc_cmf(daily: List[Dict], period: int = 20) -> float:
    """CMF (Chaikin Money Flow) 蔡金资金流指标
    参考: github.com/build-web/ta
    逻辑: 基于收盘价在日内区间中的位置加权成交量
    范围: -1 到 +1, 正值=资金流入, 负值=资金流出
    """
    if len(daily) < period:
        return 0.0
    mfv_sum = 0.0
    vol_sum = 0.0
    for d in daily[:period]:
        high = float(d.get("high", 0) or 0)
        low = float(d.get("low", 0) or 0)
        close = float(d.get("close", 0) or 0)
        vol = float(d.get("vol", 0) or 0)
        if high != low:
            mfm = ((close - low) - (high - close)) / (high - low)  # Money Flow Multiplier
        else:
            mfm = 0
        mfv_sum += mfm * vol
        vol_sum += vol
    return mfv_sum / vol_sum if vol_sum > 0 else 0


def calc_chip_distribution(daily: List[Dict], decay: float = 0.95) -> Dict:
    """简化版筹码分布计算
    参考: github.com/liumenglife/ChipDistribution
    计算获利盘比例、筹码集中度
    """
    if len(daily) < 10:
        return {"profit_ratio": 50, "concentration": 50, "avg_cost": 0}

    # 用三角分布简化：每天的成交量按(最低价, 均价, 最高价)三角分布
    # 用衰减系数让近期交易权重更高
    price_chips = {}  # price -> chip_count
    total_chips = 0

    for i, d in enumerate(daily):
        high = float(d.get("high", 0) or 0)
        low = float(d.get("low", 0) or 0)
        close = float(d.get("close", 0) or 0)
        vol = float(d.get("vol", 0) or 0)
        avg_price = (high + low + close) / 3

        if high <= low or vol <= 0:
            continue

        # 衰减权重：越近的交易日权重越大
        weight = decay ** i
        weighted_vol = vol * weight

        # 三角分布：在 [low, avg, high] 上分配筹码
        step = max(0.1, (high - low) / 20)
        price = low
        while price <= high:
            # 三角分布密度
            if price <= avg_price:
                density = (price - low) / (avg_price - low) if avg_price > low else 1
            else:
                density = (high - price) / (high - avg_price) if high > avg_price else 1
            density = max(0, density)

            p_key = round(price, 1)
            chip_count = weighted_vol * density * step / (high - low)
            price_chips[p_key] = price_chips.get(p_key, 0) + chip_count
            total_chips += chip_count
            price += step

    if total_chips == 0:
        return {"profit_ratio": 50, "concentration": 50, "avg_cost": 0}

    # 当前价格
    current_price = float(daily[0].get("close", 0) or 0)

    # 获利盘比例 = 当前价格以下的筹码占比
    profit_chips = sum(v for p, v in price_chips.items() if p <= current_price)
    profit_ratio = profit_chips / total_chips * 100

    # 加权平均成本
    total_cost = sum(p * v for p, v in price_chips.items())
    avg_cost = total_cost / total_chips if total_chips > 0 else current_price

    # 筹码集中度: 70%筹码所在的价格区间宽度 / 当前价格
    sorted_chips = sorted(price_chips.items(), key=lambda x: x[1], reverse=True)
    cumul = 0
    prices_70 = []
    for p, v in sorted_chips:
        cumul += v
        prices_70.append(p)
        if cumul >= total_chips * 0.7:
            break
    if prices_70:
        chip_range = max(prices_70) - min(prices_70)
        concentration = (1 - chip_range / current_price) * 100 if current_price > 0 else 50
    else:
        concentration = 50

    return {
        "profit_ratio": round(profit_ratio, 1),
        "concentration": round(max(0, min(100, concentration)), 1),
        "avg_cost": round(avg_cost, 2)
    }


def detect_structure_break(daily: List[Dict], lookback: int = 20) -> Tuple[str, float]:
    """简化版 BOS/CHoCH 结构破裂检测
    参考: github.com/Siva7891/smart-money-concepts
    检测近期是否发生了市场结构的变化(趋势反转信号)
    """
    if len(daily) < lookback + 2:
        return ("NONE", 0)

    # 找近期的 Swing High 和 Swing Low
    prices_close = [float(d.get("close", 0) or 0) for d in daily[:lookback]]
    prices_high = [float(d.get("high", 0) or 0) for d in daily[:lookback]]
    prices_low = [float(d.get("low", 0) or 0) for d in daily[:lookback]]

    if not prices_close:
        return ("NONE", 0)

    current = prices_close[0]

    # 找5日内的swing high/low
    swing_high = max(prices_high[:5]) if len(prices_high) >= 5 else max(prices_high)
    swing_low = min(prices_low[:5]) if len(prices_low) >= 5 else min(prices_low)

    # 找10-20日前的swing high/low（前一个结构点）
    prev_swing_high = max(prices_high[5:15]) if len(prices_high) >= 15 else max(prices_high[5:]) if len(prices_high) > 5 else swing_high
    prev_swing_low = min(prices_low[5:15]) if len(prices_low) >= 15 else min(prices_low[5:]) if len(prices_low) > 5 else swing_low

    # BOS (Break of Structure): 突破前一个结构高/低点
    if current > prev_swing_high:
        return ("BULLISH_BOS", (current - prev_swing_high) / prev_swing_high * 100)

    # CHoCH (Change of Character): 跌破前一个结构低点 = 趋势反转
    if current < prev_swing_low:
        return ("BEARISH_CHOCH", (current - prev_swing_low) / prev_swing_low * 100)

    return ("NONE", 0)


def detect_obv_divergence(daily: List[Dict]) -> Tuple[str, str]:
    """OBV 量价背离检测
    逻辑: 价格创新高但OBV没有 = 顶部背离(卖出信号)
          价格创新低但OBV没有 = 底部背离(买入信号)
    """
    if len(daily) < 10:
        return ("NONE", "数据不足")

    obv = calc_obv(daily)
    if len(obv) < 10:
        return ("NONE", "OBV计算失败")

    # 比较近5日 vs 前5-10日
    recent_price_high = max(float(d.get("high", 0) or 0) for d in daily[:5])
    prev_price_high = max(float(d.get("high", 0) or 0) for d in daily[5:10])
    recent_obv_high = max(obv[:5])
    prev_obv_high = max(obv[5:10])

    recent_price_low = min(float(d.get("low", 999999) or 999999) for d in daily[:5])
    prev_price_low = min(float(d.get("low", 999999) or 999999) for d in daily[5:10])
    recent_obv_low = min(obv[:5])
    prev_obv_low = min(obv[5:10])

    # 顶背离: 价格新高但OBV没有
    if recent_price_high > prev_price_high and recent_obv_high < prev_obv_high * 0.95:
        return ("BEARISH_DIV", "价格新高但OBV下降=顶背离(出货信号)")

    # 底背离: 价格新低但OBV没有
    if recent_price_low < prev_price_low and recent_obv_low > prev_obv_low * 1.05:
        return ("BULLISH_DIV", "价格新低但OBV上升=底背离(吸筹信号)")

    return ("NONE", "无量价背离")


# ============================================================
# 日内分钟线分析 (v11新增 - 利用Level-2分钟数据)
# ============================================================

def analyze_intraday_pattern(mins_data: List[Dict]) -> Tuple[float, str]:
    """分析日内分钟线数据，识别机构建仓模式
    
    论文支撑:
    - 机构通常在开盘30分钟和收盘30分钟集中操作(Campbell 2009)
    - 机构使用VWAP/TWAP算法，成交分布均匀(Kang 2025)
    - 尾盘异常放量是机构行为的关键特征(开源金工2023)
    
    参数:
        mins_data: 分钟K线列表(倒序，最新在前)，字段包含trade_time/close/open/high/low/vol/amount
    
    返回:
        (score, reason): -30~+30 的加成分数 + 原因
    """
    if not mins_data or len(mins_data) < 20:
        return (0, "")
    
    score = 0
    reasons = []
    
    # 按时间分段: 开盘30分(9:30-10:00), 盘中(10:00-14:30), 尾盘30分(14:30-15:00)
    open_bars = []
    mid_bars = []
    close_bars = []
    
    for bar in mins_data:
        t = bar.get("trade_time", "")
        vol = float(bar.get("vol", 0) or 0)
        amount = float(bar.get("amount", 0) or 0)
        if not t or vol <= 0:
            continue
        
        time_part = t.split(" ")[1] if " " in t else ""
        if time_part >= "09:30" and time_part < "10:00":
            open_bars.append({"vol": vol, "amount": amount, "close": float(bar.get("close", 0) or 0)})
        elif time_part >= "14:30" and time_part <= "15:00":
            close_bars.append({"vol": vol, "amount": amount, "close": float(bar.get("close", 0) or 0)})
        else:
            mid_bars.append({"vol": vol, "amount": amount, "close": float(bar.get("close", 0) or 0)})
    
    total_vol = sum(b["vol"] for b in open_bars + mid_bars + close_bars)
    if total_vol == 0:
        return (0, "")
    
    # 1. 尾盘放量检测（机构尾盘建仓信号）
    close_vol = sum(b["vol"] for b in close_bars)
    close_pct = close_vol / total_vol * 100 if total_vol > 0 else 0
    
    if close_pct > 35:
        # 尾盘成交量占比>35% = 强机构建仓信号
        score += 20
        reasons.append(f"尾盘放量{close_pct:.0f}%(机构集中操作)")
    elif close_pct > 25:
        score += 10
        reasons.append(f"尾盘偏重{close_pct:.0f}%")
    
    # 2. 开盘放量检测（机构开盘抢筹或出货）
    open_vol = sum(b["vol"] for b in open_bars)
    open_pct = open_vol / total_vol * 100 if total_vol > 0 else 0
    
    if open_pct > 30:
        # 开盘放量需结合价格方向判断
        if open_bars and close_bars:
            open_avg_price = sum(b["close"] for b in open_bars) / len(open_bars)
            close_avg_price = sum(b["close"] for b in close_bars) / len(close_bars)
            if close_avg_price > open_avg_price * 1.005:
                # 开盘放量+全天上涨 = 抢筹
                score += 10
                reasons.append(f"开盘抢筹{open_pct:.0f}%+全天上涨")
            elif close_avg_price < open_avg_price * 0.995:
                # 开盘放量+全天下跌 = 出货
                score -= 15
                reasons.append(f"开盘放量{open_pct:.0f}%+全天下跌(出货)")
    
    # 3. 成交均匀度检测（VWAP算法特征）
    # 机构算法交易的特征是成交量分布均匀（不会集中在某一段）
    if mid_bars and len(mid_bars) >= 10:
        mid_vols = [b["vol"] for b in mid_bars]
        avg_mid_vol = sum(mid_vols) / len(mid_vols)
        if avg_mid_vol > 0:
            cv = (sum((v - avg_mid_vol) ** 2 for v in mid_vols) / len(mid_vols)) ** 0.5 / avg_mid_vol
            # CV(变异系数) < 0.5 = 非常均匀 = 算法交易
            if cv < 0.4:
                score += 10
                reasons.append(f"盘中成交极均匀(CV={cv:.2f},疑似算法建仓)")
            elif cv < 0.6:
                score += 5
                reasons.append(f"盘中成交偏均匀(CV={cv:.2f})")
    
    # 4. 日内VWAP偏离
    total_amount = sum(b["amount"] for b in open_bars + mid_bars + close_bars)
    if total_vol > 0 and total_amount > 0:
        vwap = total_amount / total_vol
        last_close = mins_data[0].get("close", 0)
        if isinstance(last_close, (int, float)) and last_close > 0 and vwap > 0:
            vwap_dev = (last_close - vwap) / vwap * 100
            if vwap_dev > 1.5:
                # 收盘价高于VWAP = 买方主导
                score += 5
                reasons.append(f"收盘>VWAP{vwap_dev:+.1f}%(买方主导)")
            elif vwap_dev < -1.5:
                score -= 5
                reasons.append(f"收盘<VWAP{vwap_dev:+.1f}%(卖方主导)")
    
    score = max(-30, min(30, score))
    return (score, "；".join(reasons))


# ============================================================
# 五大维度评分函数
# ============================================================

def score_fund_flow(moneyflow: List[Dict], total_mv: float = 0) -> Tuple[float, str]:
    """维度A: 资金结构分析 + CMF蔡金资金流 + 市值归一化(Kang 2025) + 散户反向(上交大2019)"""
    if not moneyflow:
        return (0, "无资金流向数据")

    latest = moneyflow[0]
    buy_elg = float(latest.get("buy_elg_amount", 0) or 0)
    sell_elg = float(latest.get("sell_elg_amount", 0) or 0)
    buy_lg = float(latest.get("buy_lg_amount", 0) or 0)
    sell_lg = float(latest.get("sell_lg_amount", 0) or 0)
    buy_md = float(latest.get("buy_md_amount", 0) or 0)
    sell_md = float(latest.get("sell_md_amount", 0) or 0)
    buy_sm = float(latest.get("buy_sm_amount", 0) or 0)
    sell_sm = float(latest.get("sell_sm_amount", 0) or 0)

    net_elg = buy_elg - sell_elg
    net_lg = buy_lg - sell_lg
    net_main = net_elg + net_lg
    total = buy_elg + sell_elg + buy_lg + sell_lg + buy_md + sell_md + buy_sm + sell_sm

    if total == 0:
        return (0, "成交额为零")

    elg_pct = (buy_elg + sell_elg) / total * 100
    lg_pct = (buy_lg + sell_lg) / total * 100
    sm_pct = (buy_sm + sell_sm) / total * 100
    net_main_yi = net_main / 1e5

    # v8: 市值归一化评分 (Kang 2025)
    if total_mv > 0:
        mv_yi = total_mv / 1e4  # 万→亿
        norm_ratio = net_main_yi / mv_yi * 100  # 净流入占市值百分比
        if norm_ratio > 0:
            base = min(90, 20 + 35 * math.log10(max(0.001, norm_ratio) * 100))
        elif norm_ratio < 0:
            base = -min(90, 20 + 35 * math.log10(max(0.001, abs(norm_ratio)) * 100))
        else:
            base = 0
    else:
        # fallback 用原来的绝对金额逻辑
        if net_main_yi > 0:
            base = min(90, 15 + 25 * math.log10(max(0.01, net_main_yi) * 10))
        elif net_main_yi < 0:
            base = -min(90, 15 + 25 * math.log10(max(0.01, abs(net_main_yi)) * 10))
        else:
            base = 0

    # 超大单占比加成
    elg_bonus = (elg_pct - 20) * 0.8

    # 主力vs散户
    if sm_pct > 0:
        dom = (elg_pct + lg_pct) / sm_pct
        dom_bonus = 8 if dom > 5 else 4 if dom > 3 else -5 if dom < 1 else 0
    else:
        dom_bonus = 5

    score = base + elg_bonus + dom_bonus

    # 连续性
    if len(moneyflow) >= 3:
        consec = 0
        for day in moneyflow[:5]:
            d_net = (float(day.get("buy_elg_amount",0) or 0) - float(day.get("sell_elg_amount",0) or 0) +
                    float(day.get("buy_lg_amount",0) or 0) - float(day.get("sell_lg_amount",0) or 0))
            if d_net > 0:
                consec += 1
            else:
                break
        if consec >= 4: score += 15
        elif consec >= 3: score += 10
        elif consec >= 2: score += 5

        # 加速
        if len(moneyflow) >= 2:
            prev = moneyflow[1]
            prev_net = (float(prev.get("buy_elg_amount",0) or 0) - float(prev.get("sell_elg_amount",0) or 0) +
                       float(prev.get("buy_lg_amount",0) or 0) - float(prev.get("sell_lg_amount",0) or 0))
            if net_main > 0 and prev_net > 0 and net_main > prev_net * 1.3:
                score += 5

    score = max(-100, min(100, round(score)))

    parts = [f"主力{net_main_yi:+.1f}亿", f"超大{elg_pct:.0f}%/大{lg_pct:.0f}%/小{sm_pct:.0f}%"]
    if total_mv > 0:
        mv_yi = total_mv / 1e4
        parts.append(f"归一化{net_main_yi/mv_yi*100:.2f}%")
    if len(moneyflow) >= 3:
        consec_str = sum(1 for d in moneyflow[:5] if (float(d.get("buy_elg_amount",0) or 0) - float(d.get("sell_elg_amount",0) or 0)) > 0)
        if consec_str >= 2:
            parts.append(f"连续{consec_str}日超大单净流入")

    # v8: 散户反向过滤 (上交大2019, Ravina 2023)
    net_sm = buy_sm - sell_sm
    net_sm_yi = net_sm / 1e5
    if net_sm_yi > 0 and net_main_yi > 0:
        # 散户和主力同向买入 → 可能是FOMO末端，降权
        if net_sm_yi > abs(net_main_yi) * 0.5:
            score -= 15
            parts.append(f"⚠️散户跟风买入{net_sm_yi:.1f}亿(降权)")
    elif net_sm_yi < 0 and net_main_yi > 0:
        # 主力买入+散户卖出 = 经典吸筹模式，加分
        score += 10
        parts.append(f"主力吸筹+散户离场")

    score = max(-100, min(100, score))

    return (score, "，".join(parts))


def score_volume_price(daily: List[Dict], daily_basic: List[Dict]) -> Tuple[float, str]:
    """维度B: 量价形态 + OBV背离 + CMF"""
    if not daily:
        return (0, "无行情数据")

    latest = daily[0]
    pct_chg = float(latest.get("pct_chg", 0) or 0)
    volume = float(latest.get("vol", 0) or 0)
    close = float(latest.get("close", 0) or 0)
    open_p = float(latest.get("open", 0) or 0)
    high = float(latest.get("high", 0) or 0)
    low = float(latest.get("low", 0) or 0)

    vr = float(daily_basic[0].get("volume_ratio", 1) or 1) if daily_basic else 1
    tr = float(daily_basic[0].get("turnover_rate", 0) or 0) if daily_basic else 0

    body = abs(close - open_p)
    upper_shadow = high - max(close, open_p)
    lower_shadow = min(close, open_p) - low
    total_range = high - low if high > low else 0.01

    score = 0
    reason = ""

    # 模式识别
    if pct_chg >= 9.9:
        score = 50; reason = f"涨停({pct_chg:+.1f}%)"
    elif pct_chg <= -9.9:
        score = -80; reason = f"跌停({pct_chg:+.1f}%)"
    elif vr > 2.0 and -0.5 < pct_chg < 1.5:
        is_high = True
        if len(daily) >= 10:
            rh = [float(d.get("high",0) or 0) for d in daily[:10]]
            if rh and close > 0: is_high = close >= max(rh) * 0.97
        if is_high:
            score = -65; reason = f"高位巨量(量比{vr:.1f})滞涨({pct_chg:+.1f}%)，出货"
        else:
            score = 40; reason = f"低位放量(量比{vr:.1f})小涨({pct_chg:+.1f}%)，吸筹"
    elif vr > 1.5 and pct_chg < -5:
        score = -75; reason = f"放量暴跌({pct_chg:+.1f}%,量比{vr:.1f})"
    elif upper_shadow > body * 2.5 and upper_shadow > total_range * 0.5 and pct_chg < 2:
        score = -45; reason = f"长上影线，上方抛压重"
    elif vr > 1.4 and 0.3 < pct_chg < 3.5:
        # v8: 放量温和上涨降权(量价趋势2023)——A股放量上涨预测反转
        score = 30; reason = f"放量(量比{vr:.1f})温和上涨({pct_chg:+.1f}%)，反转风险"
    elif vr > 1.2 and pct_chg > 5:
        score = 55; reason = f"放量大涨({pct_chg:+.1f}%)"
    elif lower_shadow > body * 2 and lower_shadow > total_range * 0.4:
        score = 45; reason = f"长下影线，资金托底"
    elif vr < 0.7 and abs(pct_chg) < 1:
        # v8: 缩量横盘加权(国金2022)——安静吸筹
        score = 55; reason = f"缩量横盘({pct_chg:+.1f}%)，安静吸筹"
    elif vr < 0.85 and -4 < pct_chg < -0.3:
        # v8: 缩量小跌加权(国金2022)——洗盘吸筹
        score = 45; reason = f"缩量小跌({pct_chg:+.1f}%)，洗盘吸筹"
    elif pct_chg > 0:
        score = round(10 + min(30, pct_chg * 6)); reason = f"上涨({pct_chg:+.1f}%)"
    elif pct_chg < 0:
        score = round(-10 + max(-30, pct_chg * 6)); reason = f"下跌({pct_chg:+.1f}%)"
    else:
        score = 0; reason = "平盘"

    # v6新增: OBV背离检测
    obv_signal, obv_reason = detect_obv_divergence(daily)
    if obv_signal == "BEARISH_DIV":
        score -= 20
        reason += f"，OBV顶背离!"
    elif obv_signal == "BULLISH_DIV":
        score += 15
        reason += f"，OBV底背离(吸筹)"

    # v6新增: CMF蔡金资金流
    cmf = calc_cmf(daily)
    if cmf > 0.15:
        score += 10; reason += f"，CMF={cmf:.2f}(强流入)"
    elif cmf < -0.15:
        score -= 10; reason += f"，CMF={cmf:.2f}(流出)"

    # v8: 放量大涨后第2天缩量模式 (量价趋势2023)
    # 拉升后主力控盘不出货 → 正面信号
    if len(daily) >= 2 and daily_basic and len(daily_basic) >= 2:
        prev_pct = float(daily[1].get("pct_chg", 0) or 0)
        prev_vr = float(daily_basic[1].get("volume_ratio", 1) or 1)
        if prev_pct > 5 and prev_vr > 1.2 and vr < 0.85:
            score += 50
            reason += f"，放量大涨后缩量(主力控盘)"

    # 多日形态
    if len(daily) >= 3:
        consec_up = sum(1 for d in daily[:5] if float(d.get("pct_chg",0) or 0) > 0)
        consec_dn = sum(1 for d in daily[:5] if float(d.get("pct_chg",0) or 0) < 0)
        if consec_up >= 4: score += 8; reason += f"，{consec_up}连阳"
        if consec_dn >= 4: score -= 8; reason += f"，{consec_dn}连阴"

    if tr > 20: score -= 10; reason += f"，换手{tr:.0f}%极高"

    return (max(-100, min(100, round(score))), reason)


def score_position(daily: List[Dict], daily_basic: List[Dict]) -> Tuple[float, str]:
    """维度C: 位置分析 + 筹码分布(获利盘/集中度) + 结构破裂"""
    if not daily:
        return (0, "无历史数据")

    close = float(daily[0].get("close", 0) or 0)
    if close == 0:
        return (0, "价格为零")

    highs = [float(d.get("high",0) or 0) for d in daily if d.get("high")]
    lows = [float(d.get("low",999999) or 999999) for d in daily if d.get("low")]
    if not highs: return (0, "无有效价格")

    period_high = max(highs)
    period_low = min(lows)
    days = len(daily)
    from_high = ((close - period_high) / period_high * 100) if period_high > 0 else 0
    pos_pct = ((close - period_low) / (period_high - period_low) * 100) if period_high > period_low else 50

    # MA20偏离
    ma20 = sum(float(d.get("close",0) or 0) for d in daily[:20]) / min(20, len(daily))
    ma_dev = ((close - ma20) / ma20 * 100) if ma20 > 0 else 0

    pe = float(daily_basic[0].get("pe_ttm", 0) or 0) if daily_basic else 0

    score = 0; reasons = []

    # 位置评分
    if from_high < -35: score = 50; reasons.append(f"距高点{from_high:.0f}%，深度回调")
    elif from_high < -20: score = round(15 + (-from_high - 20) * 2.3); reasons.append(f"距高点{from_high:.0f}%，低位")
    elif from_high < -10: score = round(5 + (-from_high - 10)); reasons.append(f"距高点{from_high:.0f}%")
    elif from_high < -3: score = 0; reasons.append(f"距高点{from_high:.0f}%")
    else: score = round(-10 - (3 + from_high) * 3); reasons.append(f"接近高位({from_high:+.0f}%)")

    if pos_pct < 25: score += 12; reasons.append(f"区间底部({pos_pct:.0f}%)")
    elif pos_pct > 85: score -= 12; reasons.append(f"区间顶部({pos_pct:.0f}%)")

    if ma_dev < -8: score += 8; reasons.append(f"低于MA20({ma_dev:+.1f}%)")
    elif ma_dev > 15: score -= 8; reasons.append(f"高于MA20({ma_dev:+.1f}%)")

    if pe > 0:
        if pe < 12: score += 8; reasons.append(f"PE{pe:.0f}低估")
        elif pe > 100: score -= 8; reasons.append(f"PE{pe:.0f}高估")

    # v6新增: 筹码分布分析
    chip = calc_chip_distribution(daily)
    profit = chip["profit_ratio"]
    conc = chip["concentration"]
    avg_cost = chip["avg_cost"]

    if profit > 90:
        score -= 10; reasons.append(f"获利盘{profit:.0f}%(几乎全获利，抛压大)")
    elif profit < 30:
        score += 10; reasons.append(f"获利盘仅{profit:.0f}%(深套，抛压小)")
    if conc > 80:
        score += 5; reasons.append(f"筹码集中度{conc:.0f}%(高度集中)")
    if avg_cost > 0:
        cost_dev = (close - avg_cost) / avg_cost * 100
        if cost_dev < -10:
            score += 5; reasons.append(f"低于平均成本{cost_dev:.0f}%")

    # v6新增: 结构破裂检测
    struct, strength = detect_structure_break(daily)
    if struct == "BEARISH_CHOCH":
        score -= 15; reasons.append(f"趋势反转CHoCH({strength:+.1f}%)")
    elif struct == "BULLISH_BOS":
        score += 10; reasons.append(f"向上突破BOS({strength:+.1f}%)")

    return (max(-100, min(100, round(score))), "；".join(reasons))


def score_north_margin(north_top10: List[Dict], margin_data: List[Dict],
                       ts_code: str, north_global: List[Dict]) -> Tuple[float, str]:
    """维度D: 北向+融资融券"""
    score = 0; reasons = []

    is_top = False
    for item in north_top10:
        if item.get("ts_code") == ts_code:
            is_top = True
            net = float(item.get("net_amount", 0) or 0)
            if net > 10000: score += 45; reasons.append(f"北向十大净买{net/10000:.1f}亿")
            elif net > 0: score += 30; reasons.append(f"北向十大净买{net:.0f}万")
            elif net < -10000: score -= 35; reasons.append(f"北向十大净卖{net/10000:.1f}亿")
            else: score -= 15; reasons.append(f"北向十大净卖{abs(net):.0f}万")
            break

    if not is_top and north_global:
        ci = sum(1 for d in north_global[:7] if float(d.get("north_money",0) or 0) > 0)
        if ci >= 5: score += 12; reasons.append(f"北向连续{ci}日净流入(市场级)")
        elif ci >= 3: score += 6; reasons.append(f"北向偏正面({ci}/7天)")
        elif ci <= 1: score -= 8; reasons.append("北向偏弱")

    if margin_data and len(margin_data) >= 2:
        rz_l = float(margin_data[0].get("rzye",0) or 0)
        rz_p = float(margin_data[1].get("rzye",0) or 0)
        rz_c = rz_l - rz_p
        if rz_c > 5e6: score += 18; reasons.append(f"融资增{rz_c/1e4:.0f}万")
        elif rz_c > 1e6: score += 10; reasons.append(f"融资增{rz_c/1e4:.0f}万")
        elif rz_c < -5e6: score -= 18; reasons.append(f"融资减{abs(rz_c)/1e4:.0f}万")
        elif rz_c < -1e6: score -= 10; reasons.append(f"融资减{abs(rz_c)/1e4:.0f}万")

        if len(margin_data) >= 4:
            trend = sum(1 if float(margin_data[i].get("rzye",0) or 0) > float(margin_data[i+1].get("rzye",0) or 0) else -1
                       for i in range(min(4, len(margin_data)-1)))
            if trend >= 3: score += 8; reasons.append("融资连增")
            elif trend <= -3: score -= 8; reasons.append("融资连减")

        rq_l = float(margin_data[0].get("rqye",0) or 0)
        rq_p = float(margin_data[1].get("rqye",0) or 0)
        if rq_l > rq_p * 1.3 and rq_l > 1e6:
            score -= 12; reasons.append("融券激增")

    if not reasons: reasons = ["无北向/两融数据"]
    return (max(-100, min(100, score)), "；".join(reasons))


def score_limit_event(limit_data: List[Dict], ts_code: str,
                      daily: List[Dict] = None, daily_basic: List[Dict] = None,
                      margin_data: List[Dict] = None) -> Tuple[float, str]:
    """维度E: 事件/异动"""
    score = 0; reasons = []

    for item in limit_data:
        if item.get("ts_code") == ts_code:
            lt = item.get("limit", "")
            if lt == "U":
                ot = int(item.get("open_times", 0) or 0)
                if ot == 0: score += 60; reasons.append("涨停封板")
                elif ot <= 2: score += 35; reasons.append(f"涨停(开板{ot}次)")
                else: score += 15; reasons.append(f"涨停反复开板{ot}次")
            elif lt == "D": score -= 70; reasons.append("跌停")
            break

    if daily and len(daily) >= 3:
        cu = sum(1 for d in daily[:5] if float(d.get("pct_chg",0) or 0) > 0)
        cd = sum(1 for d in daily[:5] if float(d.get("pct_chg",0) or 0) < 0)
        if cu >= 5: score += 20; reasons.append("五连阳")
        elif cu >= 3: score += 10; reasons.append("三连阳")
        if cd >= 5: score -= 20; reasons.append("五连阴")
        elif cd >= 3: score -= 10; reasons.append("三连阴")

    if daily_basic and len(daily_basic) >= 2:
        tr_l = float(daily_basic[0].get("turnover_rate",0) or 0)
        tr_p = float(daily_basic[1].get("turnover_rate",0) or 0)
        if tr_l > 0 and tr_p > 0 and tr_l / tr_p > 3:
            chg = float(daily[0].get("pct_chg",0) or 0) if daily else 0
            score += (10 if chg > 0 else -15)
            reasons.append(f"换手暴增{tr_l/tr_p:.1f}x")

    if margin_data and len(margin_data) >= 2:
        rz_l = float(margin_data[0].get("rzye",0) or 0)
        rz_p = float(margin_data[1].get("rzye",0) or 0)
        if rz_p > 0:
            pct = (rz_l - rz_p) / rz_p * 100
            if pct > 5: score += 12; reasons.append(f"融资急增{pct:.1f}%")
            elif pct < -5: score -= 12; reasons.append(f"融资急减{pct:.1f}%")

    if daily and len(daily) >= 5:
        amounts = [float(d.get("amount",0) or 0) for d in daily[:5]]
        avg_a = sum(amounts) / len(amounts) if amounts else 0
        today_a = float(daily[0].get("amount",0) or 0)
        if avg_a > 0 and today_a > avg_a * 2.5:
            chg = float(daily[0].get("pct_chg",0) or 0)
            if chg > 3: score += 10; reasons.append(f"成交额暴增{today_a/avg_a:.1f}x+涨")
            elif chg < -3: score -= 10; reasons.append(f"成交额暴增+跌")

    if daily and len(daily) >= 2:
        tc = float(daily[0].get("pct_chg",0) or 0)
        yc = float(daily[1].get("pct_chg",0) or 0)
        tv = float(daily[0].get("vol",0) or 0)
        yv = float(daily[1].get("vol",0) or 0)
        if yc < -2 and tc > 1 and yv > 0 and tv > yv * 1.3:
            score += 8; reasons.append("底部反转")
        elif yc > 2 and tc < -1 and yv > 0 and tv > yv * 1.3:
            score -= 8; reasons.append("顶部反转")

    if not reasons: reasons = ["无异动"]
    return (max(-100, min(100, score)), "；".join(reasons))


def compute_total_score(scores: Dict[str, Tuple[float, str]],
                        weights: Dict[str, float]) -> Tuple[float, dict]:
    """计算加权总分 + 信号冲突检测"""
    total = 0; details = {}
    for dim, (raw, reason) in scores.items():
        w = weights.get(dim, 0)
        ws = raw * w
        total += ws
        details[dim] = {"raw_score": raw, "weight": w, "weighted_score": round(ws, 1), "reason": reason}

    ff = scores.get("fund_flow", (0,""))[0]
    vp = scores.get("volume_price", (0,""))[0]
    if (ff > 30 and vp < -30) or (ff < -30 and vp > 30):
        total *= 0.7
        details["_conflict"] = {"raw_score": 0, "weight": 0, "weighted_score": 0,
                                "reason": f"⚠️ 资金({ff:+.0f})与量价({vp:+.0f})矛盾，置信度-30%"}

    return (round(total, 1), details)


def detect_distribution_v2(daily: List[Dict], moneyflow: List[Dict],
                           daily_basic: List[Dict],
                           margin_data: List[Dict]) -> Tuple[bool, List[str]]:
    """多条件组合确认出货信号 (v7)

    核心条件（至少满足2/3）:
      1. 资金流反转: 连续3天主力净流出（超大单+大单）且流出加速
      2. 量价背离: 价格在高位(距60日高点<5%)但OBV或CMF显示资金流出
      3. 筹码获利盘>85%: 几乎所有人都赚钱=抛压极大

    辅助确认条件（至少满足1/2）:
      4. 换手率突增(>前5日均值2倍) + 涨幅放缓或下跌
      5. 融券余额增加>20% 或 融资余额连降

    Returns:
        (is_distribution, reasons): 是否确认出货 + 触发原因列表
    """
    core_hits = 0
    aux_hits = 0
    reasons = []

    # ---- 核心条件1: 资金流反转 ----
    # 连续3天主力(超大单+大单)净流出，且流出加速
    if moneyflow and len(moneyflow) >= 3:
        net_main_list = []
        for day in moneyflow[:5]:
            buy_elg = float(day.get("buy_elg_amount", 0) or 0)
            sell_elg = float(day.get("sell_elg_amount", 0) or 0)
            buy_lg = float(day.get("buy_lg_amount", 0) or 0)
            sell_lg = float(day.get("sell_lg_amount", 0) or 0)
            net_main_list.append((buy_elg - sell_elg) + (buy_lg - sell_lg))

        # 检查连续3天净流出
        consec_outflow = 0
        for net in net_main_list:
            if net < 0:
                consec_outflow += 1
            else:
                break

        if consec_outflow >= 3:
            # 检查流出是否加速（最近一天流出量 > 前一天流出量，即更负）
            accelerating = (len(net_main_list) >= 2
                           and net_main_list[0] < net_main_list[1] < 0)
            if accelerating:
                core_hits += 1
                reasons.append(
                    f"主力连续{consec_outflow}天净流出且加速"
                    f"(今{net_main_list[0] / 1e5:+.1f}亿"
                    f" vs 昨{net_main_list[1] / 1e5:+.1f}亿)")
            elif consec_outflow >= 4:
                # 连续4天以上即使不加速也算
                core_hits += 1
                reasons.append(f"主力连续{consec_outflow}天净流出")

    # ---- 核心条件2: 量价背离 ----
    # 价格在高位(距60日高点<5%)但OBV或CMF显示资金流出
    if daily and len(daily) >= 10:
        close = float(daily[0].get("close", 0) or 0)
        lookback = min(60, len(daily))
        high_60d = max(float(d.get("high", 0) or 0)
                       for d in daily[:lookback])

        if high_60d > 0 and close > 0:
            pct_from_high = (high_60d - close) / high_60d * 100
            near_high = pct_from_high < 5  # 距60日高点不到5%

            if near_high:
                obv_signal, _ = detect_obv_divergence(daily)
                obv_bearish = (obv_signal == "BEARISH_DIV")
                cmf = calc_cmf(daily)
                cmf_bearish = (cmf < -0.05)

                if obv_bearish or cmf_bearish:
                    core_hits += 1
                    parts = []
                    if obv_bearish:
                        parts.append("OBV顶背离")
                    if cmf_bearish:
                        parts.append(f"CMF={cmf:.2f}")
                    reasons.append(
                        f"高位(距60日顶{pct_from_high:.1f}%)"
                        f"+{'&'.join(parts)}")

    # ---- 核心条件3: 筹码获利盘>85% ----
    if daily and len(daily) >= 10:
        chip = calc_chip_distribution(daily)
        profit_ratio = chip["profit_ratio"]
        if profit_ratio > 85:
            core_hits += 1
            reasons.append(f"获利盘{profit_ratio:.0f}%(抛压极大)")

    # ---- 辅助条件4: 换手率突增 + 涨幅放缓或下跌 ----
    if daily_basic and len(daily_basic) >= 6 and daily:
        tr_today = float(daily_basic[0].get("turnover_rate", 0) or 0)
        tr_prev_5 = [
            float(daily_basic[i].get("turnover_rate", 0) or 0)
            for i in range(1, min(6, len(daily_basic)))
        ]
        avg_tr_5 = (sum(tr_prev_5) / len(tr_prev_5)) if tr_prev_5 else 0
        pct_chg = float(daily[0].get("pct_chg", 0) or 0)

        if avg_tr_5 > 0 and tr_today > avg_tr_5 * 2 and pct_chg < 2:
            aux_hits += 1
            reasons.append(
                f"换手率突增({tr_today:.1f}% vs 均{avg_tr_5:.1f}%)"
                f"+涨幅仅{pct_chg:+.1f}%")

    # ---- 辅助条件5: 融券余额增加>20% 或 融资余额连降 ----
    if margin_data and len(margin_data) >= 2:
        rq_latest = float(margin_data[0].get("rqye", 0) or 0)
        rq_prev = float(margin_data[1].get("rqye", 0) or 0)
        if rq_prev > 0 and rq_latest > rq_prev * 1.2 and rq_latest > 1e5:
            aux_hits += 1
            rq_chg_pct = (rq_latest - rq_prev) / rq_prev * 100
            reasons.append(f"融券余额增加{rq_chg_pct:.0f}%")
        elif len(margin_data) >= 4:
            # 融资余额连降（3天以上）
            rz_decreasing = 0
            for i in range(min(4, len(margin_data) - 1)):
                rz_cur = float(margin_data[i].get("rzye", 0) or 0)
                rz_nxt = float(margin_data[i + 1].get("rzye", 0) or 0)
                if rz_cur < rz_nxt:
                    rz_decreasing += 1
                else:
                    break
            if rz_decreasing >= 3:
                aux_hits += 1
                reasons.append(f"融资余额连降{rz_decreasing}天")

    # ---- 组合判定 ----
    # 核心>=2 且 辅助>=1 → 确认出货
    is_distribution = (core_hits >= 2 and aux_hits >= 1)
    # 核心条件全满足(3/3)时，辅助条件可放宽
    if core_hits >= 3:
        is_distribution = True

    return (is_distribution, reasons)


def determine_state(total_score: float, regime_adjust: float = 0,
                    regime: str = "NEUTRAL",
                    daily: List[Dict] = None, moneyflow: List[Dict] = None,
                    daily_basic: List[Dict] = None,
                    margin_data: List[Dict] = None) -> Tuple[str, str, str]:
    """
    根据总分判定状态 (v11: 砍掉卖出预测，改为机械止损)

    核心改动(基于16503信号回测):
    - 卖出信号41.9%正确率 = 比抛硬币还差，完全砍掉
    - 改为在买入信号中附带止损建议: "持有10日，止损-15%"
    - 论文支撑: 预测顶部比预测趋势难一个数量级(Campbell 2009)
    - 保留 detect_distribution_v2 代码（不删除，但不再调用）
    
    信号体系:
    - MARKUP: 已在拉升中，持有
    - ACCUMULATION: ★ 买入信号（核心价值，10日P=0.015）
    - WASHOUT: 洗盘，持有/加仓
    - NEUTRAL: 观望
    - DISTRIBUTION: 不再输出（改为CAUTION警示）
    """
    # 动态阈值
    accumulation_th = 30 + regime_adjust * 0.3
    markup_th = 50 + regime_adjust * 0.3

    # === Regime过滤器 (v10: BEAR完全禁入) ===
    if regime == "BEAR":
        accumulation_th = 999
        markup_th = 999
    
    # v9: NEUTRAL→BULL转折区间降低吸筹门槛
    if regime == "NEUTRAL" and regime_adjust >= -5:
        accumulation_th = min(accumulation_th, 25)

    # === 买入/持有判定 ===
    if total_score >= markup_th:
        return ("MARKUP", "🚀 拉升期", "持有观望，趋势向上。止损线: 回撤-15%")
    elif total_score >= accumulation_th:
        return ("ACCUMULATION", "⭐ 吸筹期", "★ 买入信号：机构正在收集筹码。建议持有10个交易日，止损线-15%")
    elif total_score >= 10:
        return ("WASHOUT", "💎 洗盘期", "持有/加仓：短期波动属正常洗盘")

    # === v11: 不再输出卖出信号，改为风险警示 ===
    # 当分数极低时给出警示（但不作为交易信号）
    if total_score < -20:
        return ("CAUTION", "⚠️ 风险警示", "资金流出明显，建议关注但不构成卖出依据。如已持仓请执行止损纪律(-15%)")

    # 观望
    return ("NEUTRAL", "⚪ 观望区", "暂无明确方向")
