#!/usr/bin/env python3
"""形态识别引擎单元测试（TDD 用例库，对应设计方案 6.1 节）"""
import pytest

from pattern_detect import detect_pattern, Bar, DEFAULT_PARAMS, is_gem, get_rise_threshold
from conftest import build_kline


# ============================================================
# 1. 标准命中
# ============================================================

def test_standard_hit(standard_bars, mainboard_code):
    """标准形态：第45日放量+7%（量比2.2），后14日缩量横盘 → 命中"""
    r = detect_pattern(standard_bars, code=mainboard_code)
    assert r is not None
    assert r.anchor_idx == 45
    assert r.surge_pct == pytest.approx(7.0, abs=0.1)
    assert r.volume_ratio == pytest.approx(2.2, abs=0.1)
    assert r.shrink_days >= 2
    assert r.amplitude <= 10.0
    assert r.range_ratio >= 0.6
    assert r.anchor_date == "2026-01-46"


# ============================================================
# 2. 放量不足（量比 < 1.5）
# ============================================================

def test_insufficient_volume():
    """涨幅+5%达标但量比1.2 → 阶段1拦截"""
    bars = build_kline(vol_ratio=1.2)
    r = detect_pattern(bars, code="000001")
    assert r is None


# ============================================================
# 3. 涨幅不足
# ============================================================

def test_insufficient_surge():
    """量比2.5但涨幅+3% → 阶段1拦截"""
    bars = build_kline(surge_pct=3.0, vol_ratio=2.5)
    r = detect_pattern(bars, code="000001")
    assert r is None


# ============================================================
# 4. 缩量不足（仅1日缩量）
# ============================================================

def test_insufficient_shrink():
    """放量后仅1日缩量 → 阶段2拦截"""
    bars = build_kline()
    # 手动改：放量后第2根起恢复放量（只有第1根缩量）
    anchor_vol = bars[45].volume
    for b in bars[47:]:
        b.volume = anchor_vol * 1.2
    r = detect_pattern(bars, code="000001")
    assert r is None


# ============================================================
# 5. 振幅过大（>10%）
# ============================================================

def test_excessive_amplitude():
    """横盘期振幅15% → 阶段3拦截"""
    bars = build_kline()
    # 在第47日制造一根振幅15%的K线
    b = bars[47]
    close_p = bars[45].close
    b.high = close_p * 1.10
    b.low = close_p * 0.95
    b.close = close_p * 1.02
    r = detect_pattern(bars, code="000001")
    assert r is None


# ============================================================
# 6. 板块阈值差异化
# ============================================================

def test_gem_threshold():
    """创业板涨幅5.5%（<6%新阈值）→ 不命中；同条件主板5.5%（>5%）→ 命中"""
    bars = build_kline(surge_pct=5.5, vol_ratio=2.2)
    r_gem = detect_pattern(bars, code="300001")
    assert r_gem is None  # 5.5 < 6% GEM threshold
    r_main = detect_pattern(bars, code="000001")
    assert r_main is not None  # 5.5 > 5% main threshold


def test_gem_threshold_v34():
    """V3.4: 创业板6.5%+量比2.2 → 命中（新阈值6%+2.0）"""
    bars = build_kline(surge_pct=6.5, vol_ratio=2.2)
    r = detect_pattern(bars, code="300001")
    assert r is not None


def test_gem_threshold_boundary():
    """科创板恰好+4% → 命中（V3.3 含等号+量比2.5）"""
    bars = build_kline(surge_pct=4.0, vol_ratio=2.5)
    r = detect_pattern(bars, code="688001")
    assert r is not None
    assert r is not None


# ============================================================
# 7. 边界值（恰好1.5倍量 + 恰好5%涨幅）
# ============================================================

def test_boundary_values():
    """恰好达标 → 命中（阈值含等号）"""
    bars = build_kline(surge_pct=5.0, vol_ratio=1.5)
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.surge_pct == pytest.approx(5.0, abs=0.01)
    assert r.volume_ratio == pytest.approx(1.5, abs=0.01)


# ============================================================
# 8. 多放量日（取最近锚点）
# ============================================================

def test_multiple_anchors():
    """窗口内2根放量日 → 取最近一根作为锚点"""
    bars = build_kline()
    # 在第50日再制造一根放量日（更近），并让后续横盘段围绕新锚点区间运行
    prev = bars[49].close
    bars[50].open = prev * 1.02
    bars[50].close = prev * 1.09
    bars[50].high = prev * 1.095
    bars[50].low = prev * 1.005
    bars[50].volume = 2500.0
    # 51-59 横盘段：收盘价落在新锚点 [low, high] 区间内
    new_low, new_high = bars[50].low, bars[50].high
    for i in range(51, 60):
        frac = ((i * 7) % 10) / 10.0
        bars[i].close = new_low + (new_high - new_low) * (0.3 + 0.4 * frac)
        bars[i].open = bars[i].close * 0.999
        bars[i].high = bars[i].close * 1.001
        bars[i].low = bars[i].close * 0.999
        bars[i].volume = 600.0
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.anchor_idx == 50
    assert r.surge_pct == pytest.approx(9.0, abs=0.1)


# ============================================================
# 9. 数据不足
# ============================================================

def test_insufficient_data():
    """K线不足（<25根）→ 不命中"""
    bars = build_kline(n=20, anchor=15)
    r = detect_pattern(bars, code="000001")
    assert r is None


# ============================================================
# 10. 板块判定辅助函数
# ============================================================

def test_is_gem():
    assert is_gem("300001")
    assert is_gem("301001")
    assert is_gem("688001")
    assert not is_gem("000001")
    assert not is_gem("600000")
    assert not is_gem("601001")


def test_rise_threshold():
    p = dict(DEFAULT_PARAMS)
    rise_th, vol_min = get_rise_threshold("000001", p)
    assert rise_th == 5.0
    assert vol_min == 1.5
    rise_th_gem, vol_min_gem = get_rise_threshold("300001", p)
    assert rise_th_gem == 6.0
    assert vol_min_gem == 2.0
    rise_th_688, vol_688 = get_rise_threshold("688001", p)
    assert rise_th_688 == 4.0   # V3.3 科创板独立阈值
    assert vol_688 == 2.0


# ============================================================
# 11. 加分信号检测
# ============================================================

def test_consecutive_signals():
    """构造连续3日量价齐升 + 连续3日量缩价跌场景"""
    bars = build_kline()
    # 在窗口内(40-59)构造：第40-42日连续量价齐升（涨幅<5%不构成新锚点）
    for i, extra in [(40, 0.01), (41, 0.015), (42, 0.02)]:
        bars[i].close = bars[i - 1].close * (1 + extra)
        bars[i].volume = bars[i - 1].volume * 1.2
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.conc_rise_3d is True


# ============================================================
# 12. 背离预警
# ============================================================

def test_divergence_warning():
    """横盘期出现放量滞涨 → divergence_warning=True"""
    bars = build_kline()
    # 第48日: 量放大到5日均量的2倍，但价格几乎不动
    bars[48].volume = 5000.0
    bars[48].close = bars[47].close * 1.002
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.divergence_warning is True


# ============================================================
# 13. 低点抬高
# ============================================================

def test_low_point_rise():
    """横盘期后半段低点高于前半段 → low_point_rise=True"""
    bars = build_kline()
    anchor_low = bars[45].low
    # 前半段(46-52)低点贴近锚点低点，后半段(53-59)低点抬高
    for i in range(46, 53):
        bars[i].low = anchor_low * 1.001
    for i in range(53, 60):
        bars[i].low = anchor_low * 1.02
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.low_point_rise is True


# ============================================================
# V3.0: 新形态变体测试
# ============================================================

def test_variant_b_high_platform():
    """变体B 高位平台：放量后价格在放量日区间上方窄幅运行"""
    bars = build_kline(n=60, anchor=45, surge_pct=6.0, vol_ratio=2.0)
    anchor = bars[45]
    ah = anchor.high
    # close=ah*1.025 → 累计涨≈2.8%<3%(不触发D), low=close*0.996 → low/ah≈1.021>1.02(不触发C)
    for i in range(46, 60):
        bars[i].close = ah * 1.025
        bars[i].open = bars[i].close * 0.998
        bars[i].high = bars[i].close * 1.005
        bars[i].low = bars[i].close * 0.996
        bars[i].volume = anchor.volume * 0.3
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.pattern_variant == "B"
    assert r.pattern_label == "高位平台"
    assert r.high_platform_ratio >= 0.6
    assert r.amplitude <= 10.0


def test_variant_c_pullback_confirm():
    """变体C 回踩确认：缩量后回踩放量日高点，然后反弹站稳"""
    bars = build_kline(n=60, anchor=45, surge_pct=6.0, vol_ratio=2.0)
    anchor = bars[45]
    ah = anchor.high
    # 第1-2日: 缩量在放量日高点上方
    bars[46].close = ah * 1.01
    bars[46].low = ah * 1.005
    bars[46].volume = anchor.volume * 0.4
    bars[47].close = ah * 1.015
    bars[47].low = ah * 1.008
    bars[47].volume = anchor.volume * 0.35
    # 第3日: 回踩到放量日高点附近（low=ah*1.005）
    bars[48].close = ah * 0.995
    bars[48].low = ah * 0.99
    bars[48].high = ah * 1.02
    bars[48].volume = anchor.volume * 0.3
    # 第4-5日: 反弹站稳在放量日高点上方
    for i in range(49, 52):
        bars[i].close = ah * 1.02
        bars[i].low = ah * 1.005
        bars[i].high = ah * 1.035
        bars[i].volume = anchor.volume * 0.4
    # 剩余日: 维持在上方窄幅波动
    for i in range(52, 60):
        bars[i].close = ah * (1.015 + 0.003 * ((i % 2)))
        bars[i].low = ah * 1.005
        bars[i].high = ah * 1.03
        bars[i].volume = anchor.volume * 0.3
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.pattern_variant == "C"
    assert r.pattern_label == "回踩确认"
    assert r.pullback_touch is True
    assert r.pullback_recovery is True


def test_variant_d_continuation():
    """变体D 突破延续：放量后持续上涨，拒绝回调，不强制缩量"""
    bars = build_kline(n=60, anchor=45, surge_pct=6.0, vol_ratio=2.0,
                       post_days=14)
    anchor = bars[45]
    # 放量日后：持续上涨，大部分收阳，累计涨幅≥5%
    price = anchor.close
    for i in range(46, 60):
        price *= 1.007  # 每天涨0.7%，14天累计~10%
        bars[i].open = price * 0.998
        bars[i].close = price
        bars[i].high = price * 1.01
        bars[i].low = min(bars[i].open, bars[i].close) * 0.997
        bars[i].volume = anchor.volume * (0.5 + 0.3 * ((i % 3) / 3.0))
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.pattern_variant == "D"
    assert r.pattern_label == "突破延续"
    assert r.continuation_gain >= 5.0
    assert r.continuation_positive_ratio >= 0.6


def test_variant_d_no_shrink_ok():
    """变体D 即使无缩量也命中（不需要≥2日缩量）"""
    bars = build_kline(n=60, anchor=45, surge_pct=8.0, vol_ratio=2.5)
    anchor = bars[45]
    price = anchor.close
    for i in range(46, 60):
        price *= 1.006  # 每天涨0.6%，14天累计~8.7%，振幅不超15%
        bars[i].open = price * 0.999
        bars[i].close = price
        bars[i].high = price * 1.008
        bars[i].low = min(bars[i].open, bars[i].close) * 0.998
        bars[i].volume = anchor.volume * 1.1
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.pattern_variant == "D"
    assert r.shrink_days == 0


def test_variant_priority():
    """多形态可能同时命中时，优先级 D > C > B > A"""
    bars = build_kline(n=60, anchor=45, surge_pct=10.0, vol_ratio=2.5)
    anchor = bars[45]
    price = anchor.close
    for i in range(46, 60):
        price *= 1.008  # 较大涨幅触发D
        bars[i].open = price * 0.999
        bars[i].close = price
        bars[i].high = price * 1.01
        bars[i].low = min(bars[i].open, bars[i].close) * 0.998
        bars[i].volume = anchor.volume * 0.4
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.pattern_variant == "D"


# ============================================================
# V3.5 测试
# ============================================================

def test_variant_e_pre_surge():
    """V3.5 变体E: 蓄力突破"""
    bars = build_kline(n=60, anchor=45, surge_pct=6.0, vol_ratio=2.0,
                       post_vol_ratio=0.3, post_amp=0.003)
    anchor = bars[45]
    for i in range(40, 45):
        if bars[i].close <= bars[i].open:
            bars[i].close = bars[i].open * 1.005
            bars[i].high = bars[i].close * 1.002
            bars[i].low = bars[i].open * 0.998
    for i in range(46, 60):
        bars[i].close = anchor.high * (1.02 + 0.003 * ((i % 3) / 3.0))
        bars[i].open = bars[i].close * 0.997
        bars[i].high = bars[i].close * 1.004
        bars[i].low = bars[i].close * 0.996
        bars[i].volume = anchor.volume * 0.3
    r = detect_pattern(bars, code="000001")
    assert r is not None
    assert r.pattern_variant == "E"
    assert r.pattern_label == "蓄力突破"
    assert r.pre_surge_5d is True


def test_variant_e_needs_5_days():
    """变体E 默认数据不触发 pre_surge≥5"""
    bars = build_kline(n=60, anchor=45, surge_pct=7.0, vol_ratio=2.0)
    r = detect_pattern(bars, code="000001")
    if r is not None:
        assert r.pattern_variant != "E"


def test_get_rise_threshold_v35():
    """V3.5 板块阈值全面验证"""
    p = dict(DEFAULT_PARAMS)
    assert get_rise_threshold("688001", p) == (4.0, 2.0)
    assert get_rise_threshold("300001", p) == (6.0, 2.0)
    assert get_rise_threshold("430001", p) == (5.0, 3.0)
