"""
市场环境判断模块 v3
综合11个指标判断当前是牛市/震荡市/熊市
v2新增: 隔夜美股(标普/纳斯达克)影响 + 恒生同日联动
v3新增: 外部情绪聚合(YouTube/东方财富/财经新闻/热股动量)
"""
from typing import List, Dict, Tuple
import math


def calc_ma(prices: List[float], period: int) -> float:
    """计算移动平均"""
    if len(prices) < period:
        return sum(prices) / len(prices) if prices else 0
    return sum(prices[:period]) / period


def calc_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[float, float, float]:
    """计算MACD (DIF, DEA, MACD柱)"""
    if len(prices) < slow + signal:
        return (0, 0, 0)
    
    # EMA计算（prices倒序，需要反转）
    p = list(reversed(prices))
    
    def ema(data, period):
        k = 2 / (period + 1)
        result = [data[0]]
        for i in range(1, len(data)):
            result.append(data[i] * k + result[-1] * (1 - k))
        return result
    
    ema_fast = ema(p, fast)
    ema_slow = ema(p, slow)
    
    dif = [f - s for f, s in zip(ema_fast, ema_slow)]
    dea = ema(dif, signal)
    macd_bar = [(d - e) * 2 for d, e in zip(dif, dea)]
    
    # 返回最新值（最后一个）
    return (dif[-1], dea[-1], macd_bar[-1])


def judge_market_regime(index_daily: List[Dict], north_data: List[Dict],
                         limit_data_recent: List[Dict] = None,
                         us_index_daily: List[Dict] = None,
                         hk_index_daily: List[Dict] = None,
                         external_sentiment: Dict = None) -> Dict:
    """
    综合判断市场环境 (v3: 含外部情绪)
    
    参数:
        index_daily: 上证指数日线（至少120天），倒序（最新在前）
        north_data: 北向资金（至少20天）
        limit_data_recent: 最近一天的涨跌停数据
        us_index_daily: 美股指数数据
        hk_index_daily: 恒生指数数据
        external_sentiment: 外部情绪聚合结果 (来自 sentiment_aggregator)
    
    返回:
        {
            "regime": "BULL" / "NEUTRAL" / "BEAR",
            "regime_score": -100 ~ +100,
            "regime_label": "🐂 牛市" / "⚖️ 震荡" / "🐻 熊市",
            "details": {...各指标详情...},
            "distribution_threshold_adjust": float  # 出货阈值调整值
        }
    """
    if not index_daily or len(index_daily) < 60:
        return {"regime": "NEUTRAL", "regime_score": 0, "regime_label": "⚖️ 数据不足",
                "details": {}, "distribution_threshold_adjust": 0}
    
    closes = [float(d.get("close", 0) or 0) for d in index_daily]
    current = closes[0]
    
    score = 0
    details = {}
    
    # === 指标1: 均线多空排列 (权重22%) ===
    ma5 = calc_ma(closes, 5)
    ma20 = calc_ma(closes, 20)
    ma60 = calc_ma(closes, 60)
    ma120 = calc_ma(closes, 120) if len(closes) >= 120 else calc_ma(closes, len(closes))
    
    ma_score = 0
    ma_reason = ""
    # 完美多头排列
    if ma5 > ma20 > ma60 > ma120:
        ma_score = 100
        ma_reason = f"完美多头排列 MA5>{ma5:.0f} > MA20>{ma20:.0f} > MA60>{ma60:.0f}"
    elif ma5 > ma20 > ma60:
        ma_score = 70
        ma_reason = f"短中期多头 MA5>MA20>MA60"
    elif ma5 > ma20:
        ma_score = 30
        ma_reason = f"短期多头 MA5>MA20"
    elif ma5 < ma20 < ma60 < ma120:
        ma_score = -100
        ma_reason = f"完美空头排列"
    elif ma5 < ma20 < ma60:
        ma_score = -70
        ma_reason = f"短中期空头"
    elif ma5 < ma20:
        ma_score = -30
        ma_reason = f"短期空头 MA5<MA20"
    else:
        ma_score = 0
        ma_reason = "均线交织"
    
    # 年线位置
    if current > ma120 * 1.05:
        ma_score += 10
        ma_reason += "，站稳年线上方"
    elif current < ma120 * 0.95:
        ma_score -= 10
        ma_reason += "，跌破年线"
    
    details["ma_alignment"] = {"score": min(100, max(-100, ma_score)), "reason": ma_reason, "weight": 0.20}
    score += ma_score * 0.20
    
    # === 指标2: MACD趋势 (权重18%) ===
    dif, dea, macd_bar = calc_macd(closes)
    
    macd_score = 0
    if dif > 0 and dea > 0 and macd_bar > 0:
        macd_score = 80
        macd_reason = f"MACD双线在零轴上方，红柱({macd_bar:.1f})"
    elif dif > dea and macd_bar > 0:
        macd_score = 50
        macd_reason = f"MACD金叉，红柱扩大"
    elif dif > dea:
        macd_score = 20
        macd_reason = f"DIF>DEA但柱缩小"
    elif dif < 0 and dea < 0 and macd_bar < 0:
        macd_score = -80
        macd_reason = f"MACD双线在零轴下方，绿柱"
    elif dif < dea and macd_bar < 0:
        macd_score = -50
        macd_reason = f"MACD死叉，绿柱扩大"
    else:
        macd_score = 0
        macd_reason = "MACD中性"
    
    details["macd"] = {"score": macd_score, "reason": macd_reason, "weight": 0.16}
    score += macd_score * 0.16
    
    # === 指标3: 指数位置(距250日高低点) (权重12%) ===
    if len(closes) >= 120:
        period_high = max(closes[:120])
        period_low = min(closes[:120])
    else:
        period_high = max(closes)
        period_low = min(closes)
    
    from_high = (current - period_high) / period_high * 100 if period_high > 0 else 0
    from_low = (current - period_low) / period_low * 100 if period_low > 0 else 0
    pos_pct = (current - period_low) / (period_high - period_low) * 100 if period_high > period_low else 50
    
    if pos_pct > 80:
        pos_score = 60
        pos_reason = f"接近区间高位({pos_pct:.0f}%)，可能过热"
    elif pos_pct > 60:
        pos_score = 40
        pos_reason = f"中偏高位置({pos_pct:.0f}%)"
    elif pos_pct > 40:
        pos_score = 10
        pos_reason = f"中间位置({pos_pct:.0f}%)"
    elif pos_pct > 20:
        pos_score = -30
        pos_reason = f"中偏低位置({pos_pct:.0f}%)"
    else:
        pos_score = -60
        pos_reason = f"接近区间低位({pos_pct:.0f}%)"
    
    details["index_position"] = {"score": pos_score, "reason": pos_reason, "weight": 0.11}
    score += pos_score * 0.11
    
    # === 指标4: 北向资金20日趋势 (权重13%) ===
    north_score = 0
    north_reason = "无北向数据"
    if north_data and len(north_data) >= 5:
        # 计算20日累计
        total_north = sum(float(d.get("north_money", 0) or 0) for d in north_data[:20])
        total_north_yi = total_north / 10000  # 万→亿
        consec_in = sum(1 for d in north_data[:10] if float(d.get("north_money", 0) or 0) > 0)
        
        if total_north_yi > 300:
            north_score = 80
            north_reason = f"北向20日累计+{total_north_yi:.0f}亿，强势流入"
        elif total_north_yi > 100:
            north_score = 40
            north_reason = f"北向20日累计+{total_north_yi:.0f}亿"
        elif total_north_yi > 0:
            north_score = 15
            north_reason = f"北向20日小幅流入{total_north_yi:.0f}亿"
        elif total_north_yi > -100:
            north_score = -15
            north_reason = f"北向20日小幅流出{total_north_yi:.0f}亿"
        elif total_north_yi > -300:
            north_score = -40
            north_reason = f"北向20日流出{total_north_yi:.0f}亿"
        else:
            north_score = -80
            north_reason = f"北向20日累计{total_north_yi:.0f}亿，大幅撤退"
    
    details["north_trend"] = {"score": north_score, "reason": north_reason, "weight": 0.12}
    score += north_score * 0.12
    
    # === 指标5: 成交额趋势 (权重8%) ===
    amounts = [float(d.get("amount", 0) or 0) for d in index_daily[:20]]
    vol_score = 0
    if amounts and sum(amounts) > 0:
        avg_amount_5 = sum(amounts[:5]) / 5 if len(amounts) >= 5 else amounts[0]
        avg_amount_20 = sum(amounts[:20]) / len(amounts[:20])
        
        if avg_amount_5 > avg_amount_20 * 1.3:
            vol_score = 60
            vol_reason = f"成交额近5日放大(5日均/20日均={avg_amount_5/avg_amount_20:.2f})"
        elif avg_amount_5 > avg_amount_20:
            vol_score = 20
            vol_reason = "成交额温和放大"
        elif avg_amount_5 < avg_amount_20 * 0.7:
            vol_score = -40
            vol_reason = "成交额大幅萎缩"
        else:
            vol_score = 0
            vol_reason = "成交额正常"
    else:
        vol_reason = "无成交数据"
    
    details["volume_trend"] = {"score": vol_score, "reason": vol_reason, "weight": 0.08}
    score += vol_score * 0.08
    
    # === 指标6: 涨跌停比 (权重8%) ===
    limit_score = 0
    limit_reason = "无涨跌停数据"
    if limit_data_recent:
        up_limit = sum(1 for x in limit_data_recent if x.get("limit") == "U")
        dn_limit = sum(1 for x in limit_data_recent if x.get("limit") == "D")
        
        if up_limit > 80 and dn_limit < 15:
            limit_score = 70
            limit_reason = f"涨停{up_limit}只/跌停{dn_limit}只，赚钱效应好"
        elif up_limit > 50:
            limit_score = 40
            limit_reason = f"涨停{up_limit}只/跌停{dn_limit}只"
        elif dn_limit > 50:
            limit_score = -60
            limit_reason = f"跌停{dn_limit}只/涨停{up_limit}只，恐慌"
        elif dn_limit > up_limit:
            limit_score = -20
            limit_reason = f"跌停多于涨停({dn_limit}/{up_limit})"
        else:
            limit_score = 10
            limit_reason = f"涨跌停正常({up_limit}/{dn_limit})"
    
    details["limit_ratio"] = {"score": limit_score, "reason": limit_reason, "weight": 0.08}
    score += limit_score * 0.08
    
    # === 指标7: 近期涨跌幅(动量) (权重6%) ===
    if len(closes) >= 20:
        mom_20d = (closes[0] - closes[19]) / closes[19] * 100
    else:
        mom_20d = 0
    
    if mom_20d > 10:
        mom_score = 70
        mom_reason = f"20日涨{mom_20d:.1f}%，强势"
    elif mom_20d > 3:
        mom_score = 30
        mom_reason = f"20日涨{mom_20d:.1f}%"
    elif mom_20d > -3:
        mom_score = 0
        mom_reason = f"20日变动{mom_20d:.1f}%，震荡"
    elif mom_20d > -10:
        mom_score = -30
        mom_reason = f"20日跌{mom_20d:.1f}%"
    else:
        mom_score = -70
        mom_reason = f"20日跌{mom_20d:.1f}%，弱势"
    
    details["momentum"] = {"score": mom_score, "reason": mom_reason, "weight": 0.06}
    score += mom_score * 0.06
    
    # === 指标8 (v2新增): 隔夜美股影响 (权重5%) ===
    us_score = 0
    us_reason = "无美股数据"
    if us_index_daily and len(us_index_daily) >= 2:
        # 最新一天的美股涨跌幅
        us_latest = us_index_daily[0]
        us_close = float(us_latest.get("close", 0) or 0)
        us_prev = float(us_index_daily[1].get("close", 0) or 0)
        if us_close > 0 and us_prev > 0:
            us_chg = (us_close - us_prev) / us_prev * 100
            us_name = us_latest.get("ts_code", "美股")
            
            if us_chg < -3:
                us_score = -80
                us_reason = f"隔夜{us_name}{us_chg:+.1f}%暴跌！A股低开概率大"
            elif us_chg < -2:
                us_score = -50
                us_reason = f"隔夜{us_name}{us_chg:+.1f}%大跌"
            elif us_chg < -1:
                us_score = -20
                us_reason = f"隔夜{us_name}{us_chg:+.1f}%下跌"
            elif us_chg > 3:
                us_score = 50
                us_reason = f"隔夜{us_name}{us_chg:+.1f}%大涨"
            elif us_chg > 2:
                us_score = 30
                us_reason = f"隔夜{us_name}{us_chg:+.1f}%上涨"
            elif us_chg > 1:
                us_score = 10
                us_reason = f"隔夜{us_name}{us_chg:+.1f}%小涨"
            else:
                us_score = 0
                us_reason = f"隔夜{us_name}{us_chg:+.1f}%平稳"
    
    details["us_overnight"] = {"score": us_score, "reason": us_reason, "weight": 0.05}
    score += us_score * 0.05
    
    # === 指标9 (v2新增): 恒生指数同日联动 (权重5%) ===
    hk_score = 0
    hk_reason = "无港股数据"
    if hk_index_daily and len(hk_index_daily) >= 2:
        hk_latest = hk_index_daily[0]
        hk_close = float(hk_latest.get("close", 0) or 0)
        hk_prev = float(hk_index_daily[1].get("close", 0) or 0)
        if hk_close > 0 and hk_prev > 0:
            hk_chg = (hk_close - hk_prev) / hk_prev * 100
            
            if hk_chg < -3:
                hk_score = -70
                hk_reason = f"恒生{hk_chg:+.1f}%大跌(联动r=0.69)"
            elif hk_chg < -1.5:
                hk_score = -40
                hk_reason = f"恒生{hk_chg:+.1f}%下跌"
            elif hk_chg > 3:
                hk_score = 50
                hk_reason = f"恒生{hk_chg:+.1f}%大涨"
            elif hk_chg > 1.5:
                hk_score = 30
                hk_reason = f"恒生{hk_chg:+.1f}%上涨"
            else:
                hk_score = 0
                hk_reason = f"恒生{hk_chg:+.1f}%平稳"
    
    details["hk_linkage"] = {"score": hk_score, "reason": hk_reason, "weight": 0.05}
    score += hk_score * 0.05
    
    # === 指标10 (v3新增): 外部情绪聚合 (权重8%) ===
    ext_score = 0
    ext_reason = "无外部情绪数据"
    if external_sentiment and external_sentiment.get("sentiment_score") is not None:
        raw_ext = external_sentiment["sentiment_score"]
        ext_confidence = external_sentiment.get("confidence", 50)
        
        # 根据置信度折扣
        confidence_factor = min(1.0, ext_confidence / 80)  # 80%置信度时达到满权重
        ext_score = raw_ext * confidence_factor
        
        ext_label = external_sentiment.get("sentiment_label", "")
        ext_reason = f"{ext_label}(原始{raw_ext:+.0f},置信{ext_confidence:.0f}%)"
        
        # 附加关键信号到reason
        key_sigs = external_sentiment.get("key_signals", [])
        if key_sigs:
            ext_reason += f"；{key_sigs[0][:30]}"
    
    details["external_sentiment"] = {"score": round(ext_score), "reason": ext_reason, "weight": 0.08}
    score += ext_score * 0.08
    
    # === 最终判定 ===
    score = round(max(-100, min(100, score)))
    
    if score >= 40:
        regime = "BULL"
        label = "🐂 牛市"
        # 牛市：提高出货阈值（不轻易发卖出信号）
        dist_adjust = 15  # 出货阈值提高15分
    elif score >= -20:
        regime = "NEUTRAL"
        label = "⚖️ 震荡市"
        dist_adjust = 0
    else:
        regime = "BEAR"
        label = "🐻 熊市"
        # 熊市：降低出货阈值（更敏感地发卖出信号）
        dist_adjust = -15  # 出货阈值降低15分
    
    return {
        "regime": regime,
        "regime_score": score,
        "regime_label": label,
        "details": details,
        "distribution_threshold_adjust": dist_adjust,
    }
