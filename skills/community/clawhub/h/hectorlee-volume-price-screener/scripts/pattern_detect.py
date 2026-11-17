#!/usr/bin/env python3
"""
纯量价形态识别引擎 - 四阶段判定 (V3.0)
=========================================
放量拉升 → 缩量确认 → 多形态变体（阶段3）

V3.0 新增: 阶段3 扩展为四种形态变体，按强度排序：
  D: 突破延续（最强，不需缩量）> C: 回踩确认 > B: 高位平台 > A: 标准横盘

判定阶段：
  阶段1: 定位放量拉升日（涨幅 + 量比双条件，取最近锚点）—— 共享
  阶段2: 缩量计算（变体A/B/C需要 ≥2日缩量；变体D不强制）—— 共享计算
  阶段3: 多分支判定（按 D>C>B>A 优先级）
  阶段4: 质量加分信号（连续3日量价齐升 / 连续3日量缩价跌）—— 共享

纯逻辑模块，不依赖网络，可单测。
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


# ============================================================
# 数据结构
# ============================================================

@dataclass
class Bar:
    """单根 K 线"""
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float          # 成交量（手）
    turnover: Optional[float] = None   # 换手率(%)，可缺省


@dataclass
class PatternResult:
    """形态识别结果 (V3.0)

    阶段3 扩展为四种形态变体（A/B/C/D），按强度排序：
      D: 突破延续（最强）> C: 回踩确认 > B: 高位平台 > A: 标准横盘（基础）
    """
    # 基本
    code: str = ""
    anchor_idx: int = -1             # 放量拉升日索引（bars 内）
    anchor_date: str = ""
    # 形态变体
    pattern_variant: str = ""        # "A"/"B"/"C"/"D"，空字符串表示未识别
    pattern_label: str = ""          # 中文标签
    # 阶段1
    surge_pct: float = 0.0           # 放量日涨幅(%)
    volume_ratio: float = 0.0        # 量比 = 放量日量 / 前20日均量
    vol_ma20: float = 0.0
    # 阶段2
    shrink_days: int = 0             # 最长连续缩量天数（变体D可能为0）
    shrink_depth: float = 0.0        # 缩量深度 = 缩量段均量 / 放量日量
    shrink_avg_vol: float = 0.0
    # 阶段3 — 通用
    amplitude: float = 0.0           # 放量日后整体振幅(%)
    range_ratio: float = 0.0         # 收盘价落在锚点高低点区间内的占比
    range_position: str = "mid"      # upper / lower / mid（横盘主体位置）
    pullback_ratio: float = 0.0      # 回调深度 = 回撤幅度 / 拉升幅度
    low_point_rise: bool = False     # 低点是否抬高
    # 阶段3 — 高位平台（变体B）
    high_platform_ratio: float = 0.0 # 收盘价高于放量日高点的占比
    dist_from_anchor_high: float = 0.0  # 收盘均值距放量日高点的距离(%)
    # 阶段3 — 回踩确认（变体C）
    pullback_touch: bool = False     # 是否回踩到放量日高点附近
    pullback_recovery: bool = False  # 回踩后是否恢复并站稳
    pullback_depth_pct: float = 0.0  # 回踩深度（最低/放量日高点）
    # 阶段3 — 突破延续（变体D）
    continuation_gain: float = 0.0   # 放量日后累计涨幅(%)
    continuation_positive_ratio: float = 0.0  # 放量日后收阳占比
    continuation_no_breakdown: bool = False   # 未跌破放量日开盘价
    # 阶段4（加分信号）
    conc_rise_3d: bool = False       # 连续3日量价齐升
    conc_fall_3d: bool = False       # 连续3日量缩价跌
    # 趋势结构
    breakout_60d: bool = False       # 放量日创60日新高
    ma_support: bool = False         # 最新收盘站稳 MA10 且 MA20
    vol_ma_bull: bool = False        # 5日均量 > 10日均量
    # 风险
    divergence_warning: bool = False # 横盘期放量滞涨（出货嫌疑）
    # V3.1 连阳蓄力
    pre_surge_3d: bool = False       # 放量日前 ≥3日连续阳线蓄力
    pre_surge_days: int = 0          # 蓄力阳线天数
    # V3.1 底部反转
    is_reversal: bool = False        # 是否为底部量价反转形态
    reversal_decline: float = 0.0    # 前20日累计跌幅(%)
    reversal_volume_dry: float = 0.0 # 地量程度（前5日均量/20日均量）
    # V3.5 变体E — 蓄力突破
    pre_surge_5d: bool = False       # 放量前 ≥5日阳线蓄力（变体E触发条件）
    # V3.5 多周期确认
    weekly_confirmed: bool = False   # 周线确认（MACD金叉+站上MA10）
    weekly_score_bonus: int = 0      # 多周期加减分（-5 ~ +10）
    weekly_trend: str = ""           # 周线趋势描述
    # 参数快照
    params: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# 默认参数
# ============================================================

DEFAULT_PARAMS: Dict[str, Any] = {
    "window": 20,               # 形态窗口（最近20个交易日）
    "vol_ma_n": 20,             # 均量周期
    "rise_pct_main": 5.0,       # 主板涨幅阈值(%)
    "rise_pct_gem": 6.0,          # 创业板涨幅阈值(%) V3.4: 8→6，量比同步提升
    "vol_ratio_gem": 2.0,          # 创业板放量倍数下限 V3.4
    "vol_ratio_min": 1.5,       # 放量倍数下限
    "vol_ratio_opt": 2.0,       # 放量倍数"更优"线
    "shrink_min_days": 2,       # 最小连续缩量天数（变体A/B/C）
    "amp_max": 10.0,            # 横盘最大振幅(%)
    "range_ratio_min": 0.6,     # 收盘价落在锚点高低点区间内的占比下限
    "shrink_days_best": (4, 6), # 缩量天数最优区间（评分用）
    "shrink_depth_best": 0.5,   # 缩量深度最优线（<=50% 更优）
    "pullback_best": 0.5,       # 回调深度最优线（<=1/2 拉升幅度）
    "trend_check_days": 10,     # 跌势检查天数
    "trend_drop_pct": -10.0,    # 跌势阈值(%)
    "limit_pct_main": 9.8,      # 主板涨停阈值(%)
    "limit_pct_gem": 19.8,      # 创业板/科创板涨停阈值(%)
    "ma_n1": 10,                # 均线1
    "ma_n2": 20,                # 均线2
    "vol_ma_short": 5,          # 量能短均线
    "vol_ma_long": 10,          # 量能长均线
    # V3.0 变体阈值
    "variant_d_gain_min": 5.0,  # 突破延续最小累计涨幅(%)，给B留 0-5% 空间
    "variant_d_bull_ratio": 0.6, # 突破延续最小阳线占比
    "variant_c_touch_th": 1.02,  # 回踩确认：最低价/放量日高点 上限
    "variant_b_above_ratio": 0.6, # 高位平台：高于放量日高点占比下限
    # V3.2 市值分档降阈值
    "avg_vol_large": 1000000.0,    # 大盘股日均量阈值（手），>此值用3%涨幅+2.0量比
    "avg_vol_mid": 300000.0,       # 中盘股日均量阈值（手），>此值用4%涨幅+1.8量比
    "rise_pct_large": 3.0,         # 大盘股涨幅阈值(%)
    "rise_pct_mid": 4.0,           # 中盘股涨幅阈值(%)
    "vol_ratio_large": 2.0,        # 大盘股放量倍数下限
    "vol_ratio_mid": 1.8,          # 中盘股放量倍数下限
}


# ============================================================
# 板块判定
# ============================================================

def is_gem(code: str) -> bool:
    """创业板(300/301)/科创板(688) 判定"""
    pure = _pure(code)
    return pure.startswith(("300", "301", "688"))


def is_star(code: str) -> bool:
    """科创板(688) 判定"""
    return _pure(code).startswith("688")


def is_bj(code: str) -> bool:
    """北交所(4/8/920) 判定"""
    return _pure(code).startswith(("4", "8", "920"))


def get_rise_threshold(code: str, params: Dict[str, Any], avg_vol: float = 0.0) -> tuple:
    """放量拉升阈值（板块差异化 + V3.2 市值分档 + V3.3 科创板/北交所）

    返回: (涨幅阈值%, 量比下限)
    """
    # V3.3 科创板独立阈值：4%涨幅+2.5量比
    if is_star(code):
        return (float(params.get("rise_pct_star", 4.0)),
                float(params.get("vol_ratio_star", 2.0)))

    # V3.3 北交所独立阈值：5%涨幅+3.0量比（极高量过滤噪声）
    if is_bj(code):
        return (float(params.get("rise_pct_bj", 5.0)),
                float(params.get("vol_ratio_bj", 3.0)))

    # V3.4 GEM(300/301): 6%涨幅+2.0量比（8→6%降阈，1.5→2.0提量保质量）
    if is_gem(code):
        return (float(params.get("rise_pct_gem", 6.0)),
                float(params.get("vol_ratio_gem", 2.0)))

    # V3.2 主板市值分档降阈值
    avg_vol_large = float(params.get("avg_vol_large", 1000000.0))
    avg_vol_mid = float(params.get("avg_vol_mid", 300000.0))

    if avg_vol >= avg_vol_large:
        return (float(params.get("rise_pct_large", 3.0)),
                float(params.get("vol_ratio_large", 2.0)))
    elif avg_vol >= avg_vol_mid:
        return (float(params.get("rise_pct_mid", 4.0)),
                float(params.get("vol_ratio_mid", 1.8)))

    return (float(params.get("rise_pct_main", 5.0)),
            float(params.get("vol_ratio_min", 1.5)))


# 保留向后兼容的旧签名
def get_rise_threshold_legacy(code: str, params: Dict[str, Any]) -> float:
    """放量拉升涨幅阈值（板块差异化）— 旧版兼容"""
    rise_th, _ = get_rise_threshold(code, params)
    return rise_th


def get_limit_pct(code: str, params: Dict[str, Any]) -> float:
    """涨停阈值（板块差异化）"""
    if is_bj(code):
        return 29.8
    if is_star(code) or is_gem(code):
        return float(params.get("limit_pct_gem", 19.8))
    return float(params.get("limit_pct_main", 9.8))


def _pure(code: str) -> str:
    """提取纯数字代码"""
    return "".join(ch for ch in code if ch.isdigit())


# ============================================================
# 核心识别 (V3.0 多变体)
# ============================================================

def detect_pattern(bars: List[Bar], code: str = "", params: Optional[Dict[str, Any]] = None) -> Optional[PatternResult]:
    """四阶段形态识别（V3.0 多形态变体）

    阶段1: 定位放量拉升日（共享）
    阶段2: 缩量计算（共享计算；A/B/C需要 ≥2日，D 不强制）
    阶段3: 多分支判定，按 D>C>B>A 优先级
    阶段4: 加分信号 + 趋势结构（共享，通过 _finalize_result 填充）

    输入: bars - Bar 列表（升序，建议 >=60 根）
    输出: PatternResult 或 None（不命中）
    """
    p = dict(DEFAULT_PARAMS)
    if params:
        p.update(params)
    window = int(p["window"])
    vol_ma_n = int(p["vol_ma_n"])
    vol_ratio_min = float(p["vol_ratio_min"])
    shrink_min_days = int(p["shrink_min_days"])
    amp_max = float(p["amp_max"])
    range_ratio_min = float(p["range_ratio_min"])

    n = len(bars)
    if n < vol_ma_n + 5:
        return None

    # ============================================================
    # 阶段1: 定位放量拉升日（V3.2 市值分档阈值）
    # ============================================================
    # 计算该股日均量用于分档
    stock_avg_vol = sum(b.volume for b in bars[-vol_ma_n:]) / vol_ma_n if n >= vol_ma_n else 0
    rise_th, vol_ratio_min_tier = get_rise_threshold(code, p, avg_vol=stock_avg_vol)

    anchor_idx = -1
    for i in range(n - window, n):
        if i < vol_ma_n:
            continue
        prev_close = bars[i - 1].close
        if prev_close <= 0:
            continue
        surge = (bars[i].close - prev_close) / prev_close * 100.0
        vol_ma = sum(b.volume for b in bars[i - vol_ma_n:i]) / vol_ma_n
        if vol_ma <= 0:
            continue
        vratio = bars[i].volume / vol_ma
        if surge >= rise_th - 1e-9 and vratio >= vol_ratio_min_tier - 1e-9:
            anchor_idx = i
    if anchor_idx < 0:
        return None

    anchor = bars[anchor_idx]

    # 锚点之后必须有交易日
    if anchor_idx + 1 >= n:
        return None

    # ============================================================
    # 阶段2: 缩量计算（只计算指标，不在此处判定）
    # ============================================================
    shrink_days = 0
    cur = 0
    shrink_end_idx = anchor_idx
    for j in range(anchor_idx + 1, n):
        if bars[j].volume < anchor.volume:
            cur += 1
            if cur >= shrink_days:
                shrink_days = cur
                shrink_end_idx = j
        else:
            cur = 0

    shrink_depth = 0.0
    shrink_avg_vol = 0.0
    if shrink_days > 0:
        sh_vols = [bars[j].volume for j in range(shrink_end_idx - shrink_days + 1, shrink_end_idx + 1)]
        shrink_avg_vol = sum(sh_vols) / len(sh_vols)
        shrink_depth = shrink_avg_vol / anchor.volume if anchor.volume > 0 else 1.0

    has_shrink = shrink_days >= shrink_min_days  # A/B/C 需要

    # ============================================================
    # 阶段3 公共数据准备
    # ============================================================
    post = bars[anchor_idx + 1:]
    post_n = len(post)
    anchor_high = anchor.high
    anchor_low = anchor.low

    # 振幅
    max_high = max(b.high for b in post)
    min_low = min(b.low for b in post)
    base = min_low if min_low > 0 else 1
    amplitude = (max_high - min_low) / base * 100.0

    # ═══ V3.6: 自适应进攻型振幅阈值 ═══
    # 当趋势斜率陡峭时，自动放宽振幅上限（进攻型股票振幅天然更大）
    adaptive_amp_max = amp_max
    if len(bars) >= 20:
        closes_all = [b.close for b in bars]
        n_all = len(closes_all)
        # 内联简单SMA
        ma20 = [0.0] * n_all
        for i in range(19, n_all):
            ma20[i] = sum(closes_all[i-19:i+1]) / 20.0
        ma60 = [0.0] * n_all
        for i in range(59, n_all):
            ma60[i] = sum(closes_all[i-59:i+1]) / 60.0

        if ma20[-1] > 0:
            ma20_slope = (ma20[-1] - ma20[-6]) / ma20[-6] * 100 if n_all >= 6 and ma20[-6] > 0 else 0
            ma60_slope = 0
            if ma60[-1] > 0 and n_all >= 6 and ma60[-6] > 0:
                ma60_slope = (ma60[-1] - ma60[-6]) / ma60[-6] * 100

            # MA20陡峭上升(≥1.5%)或MA60上升且MA20逼近MA60 → 进攻型
            ma20_approaching = (ma60[-1] > 0 and closes_all[-1] > ma60[-1] and
                                ma20[-1] < ma60[-1] and
                                (ma60[-1] - ma20[-1]) / ma60[-1] < 0.10)

            if ma20_slope >= 1.0 or (ma60_slope >= 0.3 and ma20_approaching):
                adaptive_amp_max = max(amp_max, 15.0)
                # 不打印日志，静默调整

    # 区间占比
    in_range = sum(1 for b in post if anchor_low - 1e-9 <= b.close <= anchor_high + 1e-9)
    range_ratio = in_range / post_n

    # 高于高点的占比
    above_high = sum(1 for b in post if b.close > anchor_high)
    above_ratio = above_high / post_n

    # 横盘主体位置
    mid = (anchor_high + anchor_low) / 2.0
    avg_close = sum(b.close for b in post) / post_n
    if avg_close >= mid:
        range_position = "upper"
    elif avg_close <= (anchor.open + anchor.close) / 2.0:
        range_position = "lower"
    else:
        range_position = "mid"

    # 回调深度
    surge_amt = anchor.close - bars[anchor_idx - 1].close
    pullback_ratio = 0.0
    if surge_amt > 0:
        pullback_ratio = max(0.0, (anchor.close - min_low) / surge_amt)

    # 低点抬高
    low_point_rise = False
    half = post_n // 2
    if half >= 1:
        first_half_min = min(b.low for b in post[:half])
        second_half_min = min(b.low for b in post[half:])
        low_point_rise = second_half_min > first_half_min

    # ============================================================
    # V3.5 提前检测连阳蓄力（变体E需要）
    # ============================================================
    pre_surge_days_cnt, pre_surge_3d_flag = _check_pre_surge(bars, anchor_idx)

    # ============================================================
    # 阶段3 变体D: 突破延续（最强，不强制缩量）
    # ============================================================
    variant_d = _try_variant_d(anchor, bars, anchor_idx, post, post_n, amplitude, p, code)
    if variant_d is not None:
        return _finalize_result(
            variant_d, bars, anchor_idx, n, window, p,
            shrink_days, shrink_depth, shrink_avg_vol,
            amplitude, range_ratio, range_position,
            pullback_ratio, low_point_rise)

    # ============================================================
    # V3.5 变体E: 蓄力突破（pre_surge≥5日 + 标准形态）
    # ============================================================
    if has_shrink and pre_surge_days_cnt >= 5:
        variant_e = _try_variant_e(anchor, post, post_n, amplitude, adaptive_amp_max, p,
                                   pre_surge_days_cnt, range_ratio, above_ratio)
        if variant_e is not None:
            result = _finalize_result(
                variant_e, bars, anchor_idx, n, window, p,
                shrink_days, shrink_depth, shrink_avg_vol,
                amplitude, range_ratio, range_position,
                pullback_ratio, low_point_rise, code)
            result.pre_surge_5d = True
            return result

    # ============================================================
    # 阶段3 变体C: 回踩确认（需要缩量）
    # ============================================================
    if has_shrink:
        variant_c = _try_variant_c(anchor, post, post_n, amplitude, adaptive_amp_max, p)
        if variant_c is not None:
            return _finalize_result(
                variant_c, bars, anchor_idx, n, window, p,
                shrink_days, shrink_depth, shrink_avg_vol,
                amplitude, range_ratio, range_position,
                pullback_ratio, low_point_rise, code)

    # ============================================================
    # 阶段3 变体B: 高位平台（需要缩量）
    # ============================================================
    if has_shrink:
        variant_b = _try_variant_b(anchor, post, post_n, amplitude, adaptive_amp_max,
                                   above_ratio, avg_close, p)
        if variant_b is not None:
            return _finalize_result(
                variant_b, bars, anchor_idx, n, window, p,
                shrink_days, shrink_depth, shrink_avg_vol,
                amplitude, range_ratio, range_position,
                pullback_ratio, low_point_rise, code)

    # ============================================================
    # 阶段3 变体A: 标准横盘（需要缩量）
    # ============================================================
    if has_shrink:
        variant_a = _try_variant_a(anchor, post, post_n, amplitude, adaptive_amp_max,
                                   range_ratio, range_ratio_min, p)
        if variant_a is not None:
            return _finalize_result(
                variant_a, bars, anchor_idx, n, window, p,
                shrink_days, shrink_depth, shrink_avg_vol,
                amplitude, range_ratio, range_position,
                pullback_ratio, low_point_rise, code)

    return None


# ============================================================
# 变体检测子函数
# ============================================================

def _try_variant_d(anchor: Bar, bars: List[Bar], anchor_idx: int,
                   post: List[Bar], post_n: int, amplitude: float,
                   params: Dict[str, Any], code: str = "") -> Optional[PatternResult]:
    """变体D: 突破延续 — 放量后持续上涨，拒绝回调，不需缩量"""
    if post_n < 1:
        return None

    # V3.3: 科创板用3%门槛，其他用5%
    gain_min = (float(params.get("variant_d_gain_star", 3.0))
                if is_star(code)
                else float(params.get("variant_d_gain_min", 5.0)))
    bull_ratio_min = float(params.get("variant_d_bull_ratio", 0.6))

    # 条件1: 累计涨幅 ≥ 3%
    cumulative_gain = (post[-1].close - anchor.close) / anchor.close * 100.0
    if cumulative_gain < gain_min:
        return None

    # 条件2: ≥60% 交易日收阳
    positive_days = sum(1 for b in post if b.close >= b.open)
    positive_ratio = positive_days / post_n
    if positive_ratio < bull_ratio_min:
        return None

    # 条件3: 放量日后最低价 > 放量日开盘价（拒绝回调至成本区）
    no_breakdown = min(b.low for b in post) > anchor.open

    # 条件4: 振幅 ≤ 15%（比标准横盘宽松，因为是上涨趋势）
    if amplitude > 15.0:
        return None

    r = PatternResult(
        code="", anchor_idx=anchor_idx, anchor_date=anchor.date,
        pattern_variant="D", pattern_label="突破延续",
        amplitude=amplitude,
        continuation_gain=cumulative_gain,
        continuation_positive_ratio=positive_ratio,
        continuation_no_breakdown=no_breakdown,
    )
    r.anchor_high = anchor.high
    r.anchor_low = anchor.low
    return r


def _try_variant_c(anchor: Bar, post: List[Bar], post_n: int,
                   amplitude: float, amp_max: float,
                   params: Dict[str, Any]) -> Optional[PatternResult]:
    """变体C: 回踩确认 — 缩量回踩放量日高点不破，而后反弹站稳"""
    if post_n < 1:
        return None

    # 条件1: 整体振幅 ≤ 10%
    if amplitude > amp_max:
        return None

    touch_th = float(params.get("variant_c_touch_th", 1.02))

    # 条件2: 至少1日最低价回踩到放量日高点附近（偏差 ≤2%）
    pullback_touch = False
    pullback_day_idx = -1
    pullback_depth_pct = 1.0
    for i, b in enumerate(post):
        if anchor.high > 0:
            low_ratio = b.low / anchor.high
            if low_ratio <= touch_th:
                pullback_touch = True
                pullback_day_idx = i
                pullback_depth_pct = low_ratio
                break

    if not pullback_touch:
        return None

    # 条件3: 回踩日之后至少1日收盘价站稳在放量日高点之上
    pullback_recovery = False
    for i in range(pullback_day_idx + 1, post_n):
        if post[i].close > anchor.high:
            pullback_recovery = True
            break

    if not pullback_recovery:
        return None

    r = PatternResult(
        code="", pattern_variant="C", pattern_label="回踩确认",
        amplitude=amplitude,
        pullback_touch=pullback_touch,
        pullback_recovery=pullback_recovery,
        pullback_depth_pct=pullback_depth_pct,
    )
    r.anchor_high = anchor.high
    r.anchor_low = anchor.low
    return r


def _try_variant_b(anchor: Bar, post: List[Bar], post_n: int,
                   amplitude: float, amp_max: float,
                   above_ratio: float, avg_close: float,
                   params: Dict[str, Any]) -> Optional[PatternResult]:
    """变体B: 高位平台 — 价格运行在放量日区间上方，窄幅整理（国电南瑞类型）"""
    if post_n < 1:
        return None

    above_ratio_min = float(params.get("variant_b_above_ratio", 0.6))

    # 条件1: 振幅 ≤ 10%
    if amplitude > amp_max:
        return None

    # 条件2: ≥60% 交易日收盘价 > 放量日高点
    if above_ratio < above_ratio_min:
        return None

    # 条件3: 收盘均价在放量日高点之上
    if avg_close <= anchor.high:
        return None

    dist = (avg_close - anchor.high) / anchor.high * 100.0 if anchor.high > 0 else 0.0

    r = PatternResult(
        code="", pattern_variant="B", pattern_label="高位平台",
        amplitude=amplitude,
        high_platform_ratio=above_ratio,
        dist_from_anchor_high=dist,
    )
    r.anchor_high = anchor.high
    r.anchor_low = anchor.low
    return r


def _try_variant_a(anchor: Bar, post: List[Bar], post_n: int,
                   amplitude: float, amp_max: float,
                   range_ratio: float, range_ratio_min: float,
                   params: Dict[str, Any]) -> Optional[PatternResult]:
    """变体A: 标准横盘 — 价格在放量日区间内横盘整理（现有逻辑）"""
    # 条件1: 振幅 ≤ 10%
    if amplitude > amp_max:
        return None

    # 条件2: ≥60% 交易日收盘价落在放量日区间内
    if range_ratio < range_ratio_min:
        return None

    r = PatternResult(
        code="", pattern_variant="A", pattern_label="标准横盘",
        amplitude=amplitude,
        range_ratio=range_ratio,
    )
    r.anchor_high = anchor.high
    r.anchor_low = anchor.low
    return r


def _try_variant_e(anchor: Bar, post: List[Bar], post_n: int,
                   amplitude: float, amp_max: float,
                   params: Dict[str, Any],
                   pre_surge_days_cnt: int,
                   range_ratio: float, above_ratio: float) -> Optional[PatternResult]:
    """V3.5 变体E: 蓄力突破 — 放量前连续5日+阳线蓄力 + 标准缩量整理

    条件：
      1. pre_surge_days ≥ 5（已由调用方保证）
      2. 振幅 ≤ 10%
      3. 收盘价或在上方运行或区间内横盘（above_ratio ≥ 0.4 或 range_ratio ≥ 0.5）
      4. 收阳占比 ≥ 0.5（放量日后仍维持偏多氛围）
    """
    if post_n < 3:
        return None

    # 振幅约束
    if amplitude > amp_max + 2.0:  # 略放宽到12%，蓄力突破后可容忍稍大波动
        return None

    # 位置验证：蓄力突破不需要严格回踩，价格在高位或横盘均可
    if above_ratio < 0.3 and range_ratio < 0.5:
        return None

    # 阳线占比
    positive = sum(1 for b in post if b.close > b.open)
    bull_ratio = positive / post_n if post_n > 0 else 0
    if bull_ratio < 0.45:
        return None

    r = PatternResult(
        code="", pattern_variant="E", pattern_label="蓄力突破",
        amplitude=amplitude,
        range_ratio=range_ratio,
        high_platform_ratio=above_ratio,
        pre_surge_days=pre_surge_days_cnt,
        pre_surge_5d=True,
        continuation_positive_ratio=bull_ratio,
    )
    r.anchor_high = anchor.high
    r.anchor_low = anchor.low
    return r


def check_weekly_trend(code: str, setcode: str = "1") -> dict:
    """V3.5 多周期确认：检查周线趋势

    Returns:
      {"confirmed": bool, "score_bonus": int, "trend": str}
        score_bonus: +10(金叉+站上MA10), +5(仅站上MA10), 0(中性), -5(死叉)
    """
    try:
        from data_provider import get_kline
    except ImportError:
        return {"confirmed": False, "score_bonus": 0, "trend": "数据不可用"}

    # 获取周线K线：优先 hithink 本地库聚合（无 WAF/无网络），失败再 TDX
    weekly = None
    try:
        import hithink_provider
        if hithink_provider.available():
            weekly = hithink_provider.get_hithink_weekly(code, want_num=30)
    except Exception:
        weekly = None
    if not weekly:
        try:
            import tdx_data_provider as tdp
            weekly = tdp.get_tdx_kline(code, setcode, want_num=30)
        except Exception:
            weekly = None

    if not weekly or len(weekly) < 15:
        return {"confirmed": False, "score_bonus": 0, "trend": "周线数据不足"}

    # 计算周线指标
    closes = [k['close'] for k in weekly]
    # MA10
    if len(closes) >= 10:
        ma10 = sum(closes[-10:]) / 10
        price_above_ma10 = closes[-1] > ma10
    else:
        price_above_ma10 = False

    # 简化MACD：DIF = EMA12 - EMA26, Signal = EMA9(DIF)
    if len(closes) >= 26:
        ema12 = closes[0]
        ema26 = closes[0]
        k12 = 2 / 13
        k26 = 2 / 27
        difs = []
        for c in closes[1:]:
            ema12 = c * k12 + ema12 * (1 - k12)
            ema26 = c * k26 + ema26 * (1 - k26)
            difs.append(ema12 - ema26)

        # Signal = EMA9 of DIF
        signal = difs[0]
        deas = []
        k9 = 2 / 10
        for d in difs[1:]:
            signal = d * k9 + signal * (1 - k9)
            deas.append(signal)

        # MACD柱
        if len(difs) >= 2 and len(deas) >= 2:
            macd_curr = difs[-1] - deas[-1]
            macd_prev = difs[-2] - deas[-2]
            golden_cross = macd_prev <= 0 and macd_curr > 0  # 金叉
            dead_cross = macd_prev >= 0 and macd_curr < 0    # 死叉
        else:
            golden_cross = False
            dead_cross = False
    else:
        golden_cross = False
        dead_cross = False

    # 判定
    if golden_cross and price_above_ma10:
        return {"confirmed": True, "score_bonus": 10, "trend": "周线金叉+多头排列"}
    elif golden_cross:
        return {"confirmed": True, "score_bonus": 7, "trend": "周线MACD金叉"}
    elif price_above_ma10:
        return {"confirmed": True, "score_bonus": 5, "trend": "站上周线MA10"}
    elif dead_cross:
        return {"confirmed": False, "score_bonus": -5, "trend": "周线MACD死叉预警"}
    else:
        return {"confirmed": False, "score_bonus": 0, "trend": "周线震荡"}


# ============================================================
# 结果填充（共享尾部逻辑）
# ============================================================

def _finalize_result(result: PatternResult, bars: List[Bar],
                     anchor_idx: int, n: int, window: int,
                     params: Dict[str, Any],
                     shrink_days: int, shrink_depth: float, shrink_avg_vol: float,
                     amplitude: float, range_ratio: float, range_position: str,
                     pullback_ratio: float, low_point_rise: bool,
                     code: str = "") -> PatternResult:
    """填充所有共享字段 + 阶段4/趋势分析，返回完整的 PatternResult"""
    result.code = code
    anchor = bars[anchor_idx]
    result.anchor_idx = anchor_idx
    result.anchor_date = anchor.date
    result.anchor_high = anchor.high
    result.anchor_low = anchor.low

    # 阶段1
    result.surge_pct = (anchor.close - bars[anchor_idx - 1].close) / bars[anchor_idx - 1].close * 100.0
    result.volume_ratio = anchor.volume / (sum(b.volume for b in bars[anchor_idx - int(params.get('vol_ma_n', 20)):anchor_idx]) / int(params.get('vol_ma_n', 20)))
    result.vol_ma20 = sum(b.volume for b in bars[anchor_idx - int(params.get('vol_ma_n', 20)):anchor_idx]) / int(params.get('vol_ma_n', 20))

    # 阶段2
    result.shrink_days = shrink_days
    result.shrink_depth = shrink_depth
    result.shrink_avg_vol = shrink_avg_vol

    # 阶段3 通用
    result.amplitude = amplitude
    result.range_ratio = range_ratio
    result.range_position = range_position
    result.pullback_ratio = pullback_ratio
    result.low_point_rise = low_point_rise

    result.params = params

    # 阶段4: 加分信号
    win_start = max(0, n - window)
    result.conc_rise_3d = _check_consecutive(bars, win_start, n, "rise")
    result.conc_fall_3d = _check_consecutive(bars, win_start, n, "fall")

    # 趋势与结构
    lookback = min(60, anchor_idx)
    if lookback > 0:
        hist_high = max(b.high for b in bars[anchor_idx - lookback:anchor_idx])
        result.breakout_60d = anchor.high > hist_high
    if n >= 20:
        ma10 = sum(b.close for b in bars[-10:]) / 10.0
        ma20 = sum(b.close for b in bars[-20:]) / 20.0
        result.ma_support = bars[-1].close > ma10 and bars[-1].close > ma20
    if n >= 10:
        v5 = sum(b.volume for b in bars[-5:]) / 5.0
        v10 = sum(b.volume for b in bars[-10:]) / 10.0
        result.vol_ma_bull = v5 > v10

    # 背离预警
    result.divergence_warning = _check_divergence(bars, anchor_idx, params)

    # V3.1 连阳蓄力检测：放量日前 ≥3 日连续阳线
    result.pre_surge_days, result.pre_surge_3d = _check_pre_surge(bars, anchor_idx)

    return result


# ============================================================
# 辅助函数
# ============================================================

def _check_consecutive(bars: List[Bar], start: int, end: int, mode: str) -> bool:
    """窗口内是否存在连续3日 量价齐升(mode=rise) / 量缩价跌(mode=fall)"""
    if end - start < 3:
        return False
    for i in range(start + 2, end):
        if mode == "rise":
            if (bars[i].volume > bars[i-1].volume > bars[i-2].volume and
                    bars[i].close > bars[i-1].close > bars[i-2].close):
                return True
        else:
            if (bars[i].volume < bars[i-1].volume < bars[i-2].volume and
                    bars[i].close < bars[i-1].close < bars[i-2].close):
                return True
    return False


def _check_divergence(bars: List[Bar], anchor_idx: int, params: Dict[str, Any]) -> bool:
    """背离预警：锚点日之后出现 成交量>5日均量*1.5 且 当日涨幅<1% 的交易日"""
    n = len(bars)
    for j in range(anchor_idx + 1, n):
        lookback = min(5, j)
        if lookback == 0:
            continue
        v5 = sum(b.volume for b in bars[j - lookback:j]) / lookback
        if v5 <= 0:
            continue
        change = (bars[j].close - bars[j-1].close) / bars[j-1].close * 100.0 if bars[j-1].close > 0 else 0
        if bars[j].volume > v5 * 1.5 and change < 1.0:
            return True
    return False


def _check_pre_surge(bars: List[Bar], anchor_idx: int) -> tuple:
    """V3.1 连阳蓄力检测：放量日前 ≥3日连续阳线（收盘>开盘，收盘递增，量温和）

    返回: (max_consecutive_days, has_3d)
    """
    if anchor_idx < 3:
        return 0, False

    max_cons = 0
    cur = 0
    # 从放量日前一天往前扫描连续阳线
    for i in range(anchor_idx - 1, max(0, anchor_idx - 10), -1):
        bar = bars[i]
        prev_bar = bars[i - 1] if i > 0 else None
        # 阳线：收盘 > 开盘
        if bar.close > bar.open:
            # 收盘价递增（相对前一根阳线）
            if prev_bar and bar.close >= prev_bar.close * 0.98:  # 允许小幅回落
                cur += 1
                if cur > max_cons:
                    max_cons = cur
            else:
                cur = 1
                if cur > max_cons:
                    max_cons = cur
        else:
            break  # 阴线打断连续

    return max_cons, max_cons >= 3


# ============================================================
# V3.1 底部量价反转
# ============================================================

def detect_reversal(bars: List[Bar], code: str = "",
                    params: Optional[Dict[str, Any]] = None) -> Optional[PatternResult]:
    """底部量价反转形态检测（独立于四阶段框架）

    条件1: 前20日累计跌幅 > 15%
    条件2: 前5日均量 < 前20日均量 × 50%（地量止跌）
    条件3: 最新日为放量拉升日（涨幅≥5%/8%，量比≥2）
    """
    p = dict(DEFAULT_PARAMS)
    if params:
        p.update(params)
    vol_ma_n = int(p["vol_ma_n"])

    n = len(bars)
    if n < vol_ma_n + 5:
        return None

    # 取最近20个交易日
    window = min(20, n - 1)
    recent = bars[-window:]

    # 条件1: 前20日累计跌幅 > 15%（最近日之前）
    if len(recent) < 10:
        return None
    prior_start_close = recent[0].close
    # 取最近日的前一天收盘（不含当日）
    prior_end_close = recent[-2].close if len(recent) >= 2 else recent[-1].close
    if prior_start_close <= 0:
        return None
    decline_pct = (prior_end_close - prior_start_close) / prior_start_close * 100.0
    if decline_pct > -15.0:  # 跌幅不够
        return None

    # 条件2: 前5日均量 < 20日均量 × 50%（地量）
    pre_period = recent[:-1]  # 不包括最近日
    if len(pre_period) < 5:
        return None
    vol_5 = sum(b.volume for b in pre_period[-5:]) / 5.0
    vol_20 = sum(b.volume for b in pre_period[-20:]) / min(20, len(pre_period))
    if vol_20 <= 0:
        return None
    volume_dry = vol_5 / vol_20
    if volume_dry > 0.5:  # 不够地量
        return None

    # 条件3: 最近日为放量拉升日
    last_bar = bars[-1]
    if last_bar.volume <= 0:
        return None
    prev_close = bars[-2].close if len(bars) >= 2 else 0
    if prev_close <= 0:
        return None
    surge = (last_bar.close - prev_close) / prev_close * 100.0
    rise_th, _ = get_rise_threshold(code, p)
    if surge < rise_th:
        return None

    # 量比 ≥ 2（地量反转要求更高放量）
    ma20_vol = sum(b.volume for b in bars[-vol_ma_n-1:-1]) / vol_ma_n
    if ma20_vol <= 0:
        return None
    vratio = last_bar.volume / ma20_vol
    if vratio < 2.0:
        return None

    # 构造结果
    r = PatternResult(
        code=code, anchor_idx=n - 1, anchor_date=last_bar.date,
        pattern_variant="R", pattern_label="底部反转",
        is_reversal=True,
        reversal_decline=decline_pct,
        reversal_volume_dry=volume_dry,
        surge_pct=surge,
        volume_ratio=vratio,
        vol_ma20=ma20_vol,
        amplitude=0.0,  # N/A for reversal
        params=params,
    )
    r.anchor_high = last_bar.high
    r.anchor_low = last_bar.low

    # 趋势信号
    lookback = min(60, n - 1)
    if lookback > 0:
        hist_high = max(b.high for b in bars[n - 1 - lookback:n - 1])
        r.breakout_60d = last_bar.high > hist_high

    return r


# ============================================================
# 便捷入口
# ============================================================

def detect_from_klines(klines: List[dict], code: str = "", params: Optional[Dict[str, Any]] = None) -> Optional[PatternResult]:
    """从字典格式 K 线（腾讯 API 输出）检测形态

    klines: [{date, open, close, high, low, volume}, ...] 升序
    """
    bars = [
        Bar(date=k["date"], open=float(k["open"]), high=float(k["high"]),
            low=float(k["low"]), close=float(k["close"]), volume=float(k["volume"]))
        for k in klines
    ]
    return detect_pattern(bars, code=code, params=params)


if __name__ == "__main__":
    print("pattern_detect 模块已加载。")
