#!/usr/bin/env python3
"""
量价评分引擎（100 分制）V3.0
=============================
V3.0: 阶段3 评分根据形态变体动态调整

五大模块:
  一、放量质量（30 分）: 放量倍数 + 拉升幅度 + 60日新高 —— 所有变体共享
  二、缩量质量（20 分）: 缩量深度 + 缩量天数 —— 共享；变体D适配
  三、变体质量（25 分）: 根据变体类型动态计算
  四、趋势与量能（15 分）: 平台突破 + 均线支撑 + 量能均线多头 —— 共享
  五、加分信号（10 分）: 连续3日量价齐升 + 连续3日量缩价跌 —— 共享

输出分层:
  >=80  强势形态
  60-80 标准形态
  <60   关注形态
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from pattern_detect import PatternResult, DEFAULT_PARAMS, get_rise_threshold


@dataclass
class ScoreResult:
    total: float = 0.0
    level: str = "关注形态"
    # 分模块明细
    vol_score: float = 0.0        # 放量质量 30
    shrink_score: float = 0.0     # 缩量质量 20
    variant_score: float = 0.0    # 变体质量 25（替代原 consolidation_score）
    trend_score: float = 0.0      # 趋势量能 15
    bonus_score: float = 0.0      # 加分 10
    details: Dict[str, Any] = field(default_factory=dict)


def score_pattern(result: PatternResult,
                  params: Optional[Dict[str, Any]] = None) -> ScoreResult:
    """对命中形态进行量价评分（100 分制，V3.0 变体感知）"""
    p = dict(DEFAULT_PARAMS)
    if params:
        p.update(params)

    sr = ScoreResult()

    # ---------- 一、放量质量（30 分）— 所有变体共享 ----------
    vr = result.volume_ratio
    if vr >= 3.0:
        vol_multi = 15.0
        vol_multi_tag = ">=3倍"
    elif vr >= 2.0:
        vol_multi = 12.0
        vol_multi_tag = "2~3倍"
    else:
        vol_multi = 8.0
        vol_multi_tag = "1.5~2倍"

    rise_th, _ = get_rise_threshold(result.code, p)
    surge_base = 5.0
    extra = max(0.0, result.surge_pct - rise_th)
    surge_score = min(10.0, surge_base + int(extra) * 2.0)

    breakout_score = 5.0 if result.breakout_60d else 0.0
    sr.vol_score = min(30.0, vol_multi + surge_score + breakout_score)
    sr.details["vol_multi"] = vol_multi
    sr.details["vol_multi_tag"] = vol_multi_tag
    sr.details["surge_score"] = surge_score
    sr.details["breakout_60d_score"] = breakout_score

    # ---------- 二、缩量质量（20 分）— 共享；变体D适配 ----------
    variant = result.pattern_variant
    sr.details["variant"] = variant

    if variant == "D":
        # 突破延续：缩量可能很少或没有，评分打折
        depth = result.shrink_depth
        if depth > 0 and depth < 0.5:
            depth_score = 6.0
            depth_tag = "<50%"
        elif depth > 0 and depth <= 0.7:
            depth_score = 4.0
            depth_tag = "50%~70%"
        elif depth > 0:
            depth_score = 2.0
            depth_tag = ">70%"
        else:
            depth_score = 2.0   # 无缩量，给基础分
            depth_tag = "无缩量(强势)"

        sd = result.shrink_days
        if sd >= 2:
            days_score = min(5.0, sd * 1.5)
        else:
            days_score = 0.0
        sr.shrink_score = min(20.0, depth_score + days_score)
    else:
        # 变体A/B/C: 标准缩量评分
        depth = result.shrink_depth
        if depth < 0.3:
            depth_score = 10.0
            depth_tag = "<30%"
        elif depth < 0.5:
            depth_score = 8.0
            depth_tag = "30%~50%"
        elif depth <= 0.7:
            depth_score = 5.0
            depth_tag = "50%~70%"
        else:
            depth_score = 3.0
            depth_tag = ">70%"

        sd = result.shrink_days
        if 2 <= sd <= 3:
            days_score = 3.0
        elif 4 <= sd <= 6:
            days_score = 5.0
        elif 7 <= sd <= 8:
            days_score = 4.0
        else:
            days_score = 0.0
        sr.shrink_score = min(20.0, depth_score + days_score)

    sr.details["shrink_depth"] = result.shrink_depth
    sr.details["shrink_depth_tag"] = depth_tag
    sr.details["shrink_days"] = result.shrink_days
    sr.details["shrink_days_score"] = days_score

    # ---------- 三、变体质量（25 分）— 变体相关 ----------
    if result.is_reversal:
        _score_reversal(sr, result)
    elif variant == "D":
        _score_variant_d(sr, result)
    elif variant == "C":
        _score_variant_c(sr, result)
    elif variant == "E":
        _score_variant_e(sr, result)
    elif variant == "B":
        _score_variant_b(sr, result)
    else:
        _score_variant_a(sr, result)

    # ---------- 四、趋势与量能（15 分）— V3.1 前高突破权重提升 ----------
    t_breakout = 10.0 if result.breakout_60d else 0.0  # V3.1: 8→10
    t_ma = 4.0 if result.ma_support else 0.0
    t_volma = 3.0 if result.vol_ma_bull else 0.0
    sr.trend_score = min(15.0, t_breakout + t_ma + t_volma)
    sr.details["trend_breakout"] = result.breakout_60d
    sr.details["trend_ma_support"] = result.ma_support
    sr.details["trend_vol_ma_bull"] = result.vol_ma_bull

    # ---------- 五、加分信号（10 分 + 蓄力加成）— V3.1 ----------
    bonus = 0.0
    if result.conc_rise_3d:
        bonus += 5.0
    if result.conc_fall_3d:
        bonus += 5.0
    # V3.1 连阳蓄力：≥3日 +3分，≥5日 +5分
    if result.pre_surge_days >= 5:
        bonus += 5.0
    elif result.pre_surge_3d:
        bonus += 3.0
    sr.bonus_score = min(15.0, bonus)  # V3.1: 上限从10提到15
    sr.details["conc_rise_3d"] = result.conc_rise_3d
    sr.details["conc_fall_3d"] = result.conc_fall_3d
    sr.details["pre_surge_days"] = result.pre_surge_days

    # ---------- V3.5 多因子融合（额外20分）— 市值 + 波动率 + 趋势强度 ----------
    factor_score = _multi_factor_score(result, sr.details)
    sr.details["multi_factor_score"] = factor_score

    # ---------- V3.5 关注池曝光度（0~5分）— 近50日历史命中次数 ----------
    recurrence_count, recurrence_score = _recurrence_lookup(result.code)
    sr.details["recurrence_count"] = recurrence_count
    sr.details["recurrence_score"] = recurrence_score

    # ---------- V3.5 多周期确认（-5 ~ +10分）— 周线趋势验证 ----------
    weekly_bonus = result.weekly_score_bonus
    if weekly_bonus == 0 and not result.is_reversal:
        # 未预计算时尝试实时检查（仅非反转形态）
        try:
            from pattern_detect import check_weekly_trend
            pure = ''.join(c for c in result.code if c.isdigit())
            setcode = '1' if pure.startswith(('60','68')) else '0'
            weekly_info = check_weekly_trend(pure, setcode)
            weekly_bonus = weekly_info.get('score_bonus', 0)
            result.weekly_confirmed = weekly_info.get('confirmed', False)
            result.weekly_trend = weekly_info.get('trend', '')
        except Exception:
            pass
    sr.details["weekly_bonus"] = weekly_bonus
    sr.details["weekly_trend"] = result.weekly_trend

    # ---------- 总分（V3.5: 130分制 + 曝光度5分 = 135分制） ----------
    raw_total = (sr.vol_score + sr.shrink_score + sr.variant_score +
                 sr.trend_score + sr.bonus_score + factor_score +
                 recurrence_score + weekly_bonus)
    # ---------- V3.5 权重校准（基于回测特征重要性动态调整） ----------
    sr.total = round(_calibrate_weight(raw_total, result, sr), 1)

    # ═══ V3.7: 背离预警扣分（横盘期放量滞涨=出货嫌疑） ═══
    sr.divergence_penalty = 0
    if result.divergence_warning:
        sr.divergence_penalty = -10.0
        sr.total = round(sr.total + sr.divergence_penalty, 1)
        if not hasattr(sr, 'details'):
            sr.details = {}
        sr.details['divergence_penalty'] = sr.divergence_penalty

    # ---------- 分层（V3.5: 130分制） ----------
    if sr.total >= 100:
        sr.level = "强势形态"
    elif sr.total >= 75:
        sr.level = "标准形态"
    else:
        sr.level = "关注形态"
    return sr


# ============================================================
# 变体评分子函数
# ============================================================

def _score_variant_a(sr: ScoreResult, r: PatternResult):
    """变体A: 标准横盘（现有逻辑）"""
    if r.amplitude <= 5.0:
        amp_score = 10.0
    else:
        amp_score = 7.0

    pos_score = {"upper": 8.0, "mid": 5.0, "lower": 3.0}.get(r.range_position, 5.0)

    pr = r.pullback_ratio
    if pr <= 0.5:
        pullback_score = 5.0
    elif pr <= 2.0 / 3.0:
        pullback_score = 2.0
    else:
        pullback_score = 0.0

    low_rise_score = 2.0 if r.low_point_rise else 0.0
    new_high_bonus = 2.0 if r.breakout_60d else 0.0  # V3.1
    sr.variant_score = min(25.0, amp_score + pos_score + pullback_score + low_rise_score + new_high_bonus)
    sr.details["amplitude_score"] = amp_score
    sr.details["position_score"] = pos_score
    sr.details["position"] = r.range_position
    sr.details["pullback_ratio"] = r.pullback_ratio
    sr.details["pullback_score"] = pullback_score
    sr.details["low_point_rise"] = r.low_point_rise


def _score_variant_b(sr: ScoreResult, r: PatternResult):
    """变体B: 高位平台"""
    # 振幅得分：振幅越小越好
    if r.amplitude <= 5.0:
        amp_score = 10.0
    elif r.amplitude <= 8.0:
        amp_score = 8.0
    else:
        amp_score = 6.0

    # 高位占比得分
    hpr = r.high_platform_ratio
    if hpr >= 0.9:
        platform_score = 8.0
    elif hpr >= 0.75:
        platform_score = 6.0
    else:
        platform_score = 4.0

    # 距高点距离得分：距离越大说明强势程度越高
    dist = r.dist_from_anchor_high
    if dist >= 5.0:
        dist_score = 5.0
    elif dist >= 2.0:
        dist_score = 3.0
    else:
        dist_score = 1.0

    low_rise_score = 2.0 if r.low_point_rise else 0.0
    new_high_bonus_b = 2.0 if r.breakout_60d else 0.0  # V3.1
    sr.variant_score = min(25.0, amp_score + platform_score + dist_score + low_rise_score + new_high_bonus_b)
    sr.details["amplitude_score"] = amp_score
    sr.details["platform_ratio"] = r.high_platform_ratio
    sr.details["platform_score"] = platform_score
    sr.details["dist_from_high"] = r.dist_from_anchor_high
    sr.details["dist_score"] = dist_score
    sr.details["low_point_rise"] = r.low_point_rise


def _score_variant_c(sr: ScoreResult, r: PatternResult):
    """变体C: 回踩确认"""
    # 回踩精准度：越接近放量日高点越好（理想是刚好踩到）
    depth = r.pullback_depth_pct
    if depth <= 1.005:
        precision_score = 10.0   # 精准回踩
    elif depth <= 1.01:
        precision_score = 8.0    # 非常接近
    elif depth <= 1.02:
        precision_score = 6.0    # 接近
    else:
        precision_score = 3.0    # 偏差较大

    # 反弹力度：回踩后收盘站稳程度
    recovery_score = 8.0 if r.pullback_recovery else 0.0

    # 振幅得分
    if r.amplitude <= 5.0:
        amp_score = 5.0
    else:
        amp_score = 3.0

    low_rise_score = 2.0 if r.low_point_rise else 0.0
    new_high_bonus_c = 2.0 if r.breakout_60d else 0.0  # V3.1
    sr.variant_score = min(25.0, precision_score + recovery_score + amp_score + low_rise_score + new_high_bonus_c)
    sr.details["pullback_precision"] = depth
    sr.details["precision_score"] = precision_score
    sr.details["recovery_score"] = recovery_score
    sr.details["amplitude_score"] = amp_score
    sr.details["low_point_rise"] = r.low_point_rise


def _score_variant_d(sr: ScoreResult, r: PatternResult):
    """变体D: 突破延续"""
    # 累计涨幅得分（新阈值从5%起步）
    gain = r.continuation_gain
    if gain >= 15.0:
        gain_score = 10.0
    elif gain >= 10.0:
        gain_score = 8.0
    elif gain >= 7.0:
        gain_score = 6.0
    else:
        gain_score = 4.0   # 5%~7%

    # 阳线占比得分
    pr_val = r.continuation_positive_ratio
    if pr_val >= 0.8:
        bull_score = 8.0
    elif pr_val >= 0.7:
        bull_score = 6.0
    else:
        bull_score = 4.0

    # 拒绝回调得分
    breakdown_score = 5.0 if r.continuation_no_breakdown else 0.0

    # 创60日新高加分
    new_high_bonus = 2.0 if r.breakout_60d else 0.0
    sr.variant_score = min(25.0, gain_score + bull_score + breakdown_score + new_high_bonus)
    sr.details["continuation_gain"] = r.continuation_gain
    sr.details["gain_score"] = gain_score
    sr.details["bull_ratio"] = r.continuation_positive_ratio
    sr.details["bull_score"] = bull_score
    sr.details["no_breakdown"] = r.continuation_no_breakdown
    sr.details["breakdown_score"] = breakdown_score


def _score_reversal(sr: ScoreResult, r: PatternResult):
    """V3.1 底部量价反转评分"""
    decline = abs(r.reversal_decline)
    if decline >= 30.0:
        decline_score = 8.0
    elif decline >= 20.0:
        decline_score = 6.0
    else:
        decline_score = 4.0

    dry = r.reversal_volume_dry
    if dry <= 0.3:
        dry_score = 10.0
    elif dry <= 0.5:
        dry_score = 7.0
    else:
        dry_score = 4.0

    vr = r.volume_ratio
    if vr >= 4.0:
        vr_score = 5.0
    elif vr >= 3.0:
        vr_score = 3.0
    else:
        vr_score = 1.0

    new_high_bonus = 2.0 if r.breakout_60d else 0.0
    sr.variant_score = min(25.0, decline_score + dry_score + vr_score + new_high_bonus)
    sr.details["reversal_decline"] = r.reversal_decline
    sr.details["reversal_volume_dry"] = r.reversal_volume_dry
    sr.details["decline_score"] = decline_score
    sr.details["dry_score"] = dry_score


def _score_variant_e(sr: ScoreResult, r: PatternResult):
    """V3.5 变体E: 蓄力突破评分

    评分维度: 蓄力质量(10) + 振幅(5) + 位置(5) + 蓄力天数(5)
    """
    # 蓄力阳线天数得分
    days = r.pre_surge_days
    if days >= 8:
        days_score = 5.0
    elif days >= 6:
        days_score = 4.0
    else:
        days_score = 3.0

    # 振幅得分
    if r.amplitude <= 5.0:
        amp_score = 5.0
    elif r.amplitude <= 8.0:
        amp_score = 4.0
    else:
        amp_score = 2.0

    # 整理期阳线质量
    pr_val = r.continuation_positive_ratio
    if pr_val >= 0.7:
        quality_score = 8.0
    elif pr_val >= 0.6:
        quality_score = 6.0
    else:
        quality_score = 4.0

    # 高位占比
    hpr = r.high_platform_ratio
    if hpr >= 0.7:
        position_score = 5.0
    elif hpr >= 0.5:
        position_score = 3.0
    else:
        position_score = 1.0

    new_high_bonus = 2.0 if r.breakout_60d else 0.0
    sr.variant_score = min(25.0, days_score + amp_score + quality_score + position_score + new_high_bonus)
    sr.details["pre_surge_days_e"] = days
    sr.details["days_score_e"] = days_score
    sr.details["amplitude_score"] = amp_score
    sr.details["quality_score_e"] = quality_score
    sr.details["position_score_e"] = position_score


def _multi_factor_score(r: PatternResult, details: dict) -> float:
    """V3.5 多因子融合评分（额外20分）

    三大因子:
      1. 市值因子 (7分): 日均成交额标准化，流动性越好分越高
      2. 波动率因子 (7分): 20日ATR，适中的波动率最优
      3. 趋势强度因子 (6分): 放量日前趋势斜率，上升趋势加分
    """
    score = 0.0

    # 市值/流动性因子（用20日均量代理）
    vol_ma20 = r.vol_ma20
    if vol_ma20 > 0:
        if vol_ma20 >= 2000000:  # 大盘，流动性极好
            mkt_score = 7.0
        elif vol_ma20 >= 500000:  # 中盘
            mkt_score = 5.0
        elif vol_ma20 >= 100000:  # 小盘
            mkt_score = 3.0
        else:
            mkt_score = 1.0
    else:
        mkt_score = 3.0
    score += mkt_score
    details["mkt_factor_score"] = mkt_score
    details["vol_ma20"] = vol_ma20

    # 波动率因子（振幅代理ATR）
    amp = r.amplitude
    if 3.0 <= amp <= 8.0:
        vol_score = 7.0  # 适中波动最优
    elif amp <= 12.0:
        vol_score = 5.0
    elif amp > 12.0:
        vol_score = 2.0  # 过大波动可能不稳
    else:
        vol_score = 3.0  # 太小波动缺乏弹性
    score += vol_score
    details["vol_factor_score"] = vol_score

    # 趋势强度因子
    breakout = r.breakout_60d
    ma_support = r.ma_support
    if breakout and ma_support:
        trend_score = 6.0
    elif breakout or ma_support:
        trend_score = 3.0
    else:
        trend_score = 1.0
    score += trend_score
    details["trend_factor_score"] = trend_score

    return min(20.0, score)


def _recurrence_lookup(code: str, lookback: int = 50) -> tuple:
    """V3.5 查询股票近N日关注池曝光次数并评分

    Returns:
        (count, score): count为出现次数, score为0~5分
    """
    try:
        from signal_history import get_recurrence
        freq = get_recurrence(lookback)
        count = freq.get(code, 0)
        # 缓存以减少重复读取
        _recurrence_lookup._cache = getattr(_recurrence_lookup, '_cache', {})
        if not _recurrence_lookup._cache:
            _recurrence_lookup._cache = freq
        else:
            count = _recurrence_lookup._cache.get(code, 0)
    except Exception:
        count = 0

    if count >= 8:
        score = 5.0   # 频繁出现 → 主力持续运作
    elif count >= 5:
        score = 4.0
    elif count >= 3:
        score = 3.0   # 多次出现 → 值得关注
    elif count >= 1:
        score = 1.0
    else:
        score = 0.0   # 首次出现

    return count, score


def _calibrate_weight(raw_total: float, r: PatternResult, sr) -> float:
    """V3.5 权重校准：基于回测特征重要性动态调整

    校准逻辑:
      - 突破延续(D/E): 趋势+放量权重更高，回调容忍度更大
      - 回踩确认(C): 精准度优先，缩量质量权重更高
      - 标准横盘(A/B): 均衡权重
      - 反转(R): 放量+地量权重最高

    回测结论: 放量质量/趋势强度对5日超额贡献最大，
    变体质量对20日贡献有限 → 对标准横盘形态适当降低变体权重
    """
    variant = r.pattern_variant
    calibrated = raw_total

    # 标准横盘/高位平台：变体质量对超额贡献有限，轻微打折
    if variant in ("A", "B"):
        calibrated = sr.vol_score + sr.shrink_score + sr.variant_score * 0.85 + sr.trend_score + sr.bonus_score
        calibrated += sr.details.get("multi_factor_score", 0) + sr.details.get("weekly_bonus", 0)
        calibrated += sr.details.get("recurrence_score", 0)

    # 底部反转：放量质量权重提升
    elif variant == "R":
        calibrated = sr.vol_score * 1.15 + sr.shrink_score + sr.variant_score + sr.trend_score + sr.bonus_score
        calibrated += sr.details.get("multi_factor_score", 0) + sr.details.get("weekly_bonus", 0)
        calibrated += sr.details.get("recurrence_score", 0)

    # D/E/C 保持原权

    return round(calibrated, 1)


if __name__ == "__main__":
    print("scoring 模块已加载。")
