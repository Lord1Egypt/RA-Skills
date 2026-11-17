#!/usr/bin/env python3
"""
风险硬过滤模块（评分前执行，最高优先级）
=========================================
- ST/*ST 及退市风险股
- 次新股（上市不足60日，K线不足即视为次新）
- 一字板（放量日 high==low，无法买入）
- 连板股（放量日前连续>=2日涨停）
- 跌势反弹（放量日前10日累计跌幅超阈值 → 诱多假形态）
- 换手率下限（放量日换手 < 3% 剔除；数据缺失则跳过并标注）

输入: 股票名称/代码 + K线 + 形态结果（可选）
输出: (exclude: bool, reason: str)
"""

from typing import Optional, Tuple, List
from pattern_detect import Bar, get_limit_pct, DEFAULT_PARAMS


# ============================================================
# 名称级过滤
# ============================================================

def is_st_name(name: str) -> bool:
    """ST / *ST 名称判定"""
    return "ST" in name.upper()


def check_st(name: str) -> Tuple[bool, str]:
    if is_st_name(name):
        return True, "ST/*ST 股票"
    return False, ""


# ============================================================
# 退市风险（财务信号；依赖 akshare 时启用，否则降级）
# ============================================================

def check_delist_risk(code: str, quote: Optional[dict] = None) -> Tuple[bool, str]:
    """退市风险硬过滤

    - 优先: 实时行情中带风险警示标记
    - 增强: 财务数据（akshare），不可用时降级跳过（不拦截）
    """
    if quote:
        name = quote.get("name", "")
        if is_st_name(name):
            return True, "ST/*ST 股票"
        # 腾讯行情风险标记（部分行情含风险提示字段）
        risk_flag = quote.get("risk_flag", "")
        if risk_flag:
            return True, f"退市风险警示: {risk_flag}"
    return False, ""


# ============================================================
# K线级过滤
# ============================================================

def check_new_stock(bars: List[Bar], min_days: int = 60, code: str = "") -> Tuple[bool, str]:
    """次新股：K线数量不足 min_days 视为上市未满
    
    V3.3: 北交所自动使用 90 日最低K线要求
    """
    from pattern_detect import is_bj
    if is_bj(code):
        min_days = max(min_days, 90)
    if len(bars) < min_days:
        return True, f"次新股（K线仅{len(bars)}根 < {min_days}）"
    return False, ""


def check_one_word_limit(bars: List[Bar], anchor_idx: int, code: str,
                         params: Optional[dict] = None) -> Tuple[bool, str]:
    """一字板：放量日 high == low（一字涨停无法买入）
    
    V3.2: 高量一字板（量比≥2）不拦截——放量一字板说明有充分换手可参与
    """
    if anchor_idx < 0 or anchor_idx >= len(bars):
        return False, ""
    bar = bars[anchor_idx]
    if bar.high != bar.low:   # 非一字板
        return False, ""
    
    p = dict(DEFAULT_PARAMS)
    if params:
        p.update(params)
    
    # V3.2: 计算量比，高量一字板放行
    vol_ma_n = int(p.get("vol_ma_n", 20))
    if anchor_idx >= vol_ma_n:
        vol_ma = sum(b.volume for b in bars[anchor_idx - vol_ma_n:anchor_idx]) / vol_ma_n
        if vol_ma > 0:
            vratio = bar.volume / vol_ma
            if vratio >= 2.0:
                return False, ""  # 放量一字板，有充分换手
    
    limit_pct = get_limit_pct(code, p)
    prev_close = bars[anchor_idx - 1].close if anchor_idx > 0 else 0
    if prev_close > 0 and (bar.close - prev_close) / prev_close * 100.0 >= limit_pct - 0.5:
        return True, f"无量一字涨停（无法买入）涨幅{(bar.close - prev_close) / prev_close * 100.0:.1f}%"
    return False, ""


def check_consecutive_limit(bars: List[Bar], anchor_idx: int, code: str,
                            params: Optional[dict] = None) -> Tuple[bool, str]:
    """连板股：放量日前连续 >=2 日涨停（T+1无法参与）"""
    p = dict(DEFAULT_PARAMS)
    if params:
        p.update(params)
    limit_pct = get_limit_pct(code, p)
    consecutive = 0
    for i in range(anchor_idx - 1, max(0, anchor_idx - 5), -1):
        prev_close = bars[i - 1].close if i > 0 else 0
        if prev_close <= 0:
            break
        chg = (bars[i].close - prev_close) / prev_close * 100.0
        if chg >= limit_pct - 0.5:
            consecutive += 1
        else:
            break
    if consecutive >= 2:
        return True, f"放量日前连续{consecutive}日涨停（连板）"
    return False, ""


def check_downtrend_rebound(bars: List[Bar], anchor_idx: int,
                            params: Optional[dict] = None) -> Tuple[bool, str]:
    """跌势反弹：放量日前10日累计跌幅 < -10% → 诱多假形态"""
    p = dict(DEFAULT_PARAMS)
    if params:
        p.update(params)
    check_days = int(p.get("trend_check_days", 10))
    drop_pct = float(p.get("trend_drop_pct", -10.0))
    start = anchor_idx - check_days
    if start < 0 or bars[start].close <= 0:
        return False, ""
    cum_change = (bars[anchor_idx - 1].close - bars[start].close) / bars[start].close * 100.0
    if cum_change < drop_pct:
        return True, f"放量前{check_days}日累计跌幅{cum_change:.1f}%（跌势反弹，诱多风险）"
    return False, ""


def check_turnover(anchor_turnover: Optional[float], min_turnover: float = 3.0) -> Tuple[bool, str]:
    """换手率下限：放量日换手 < 3% 剔除

    腾讯日K无历史换手率，data_provider 会尽力从实时行情补充；
    数据缺失时返回 (False, '') 并置 skip 标记，不误杀。
    """
    if anchor_turnover is None:
        return False, ""   # 数据缺失，跳过
    if anchor_turnover < min_turnover:
        return True, f"放量日换手率{anchor_turnover:.1f}% < {min_turnover}%（流动性不足）"
    return False, ""


# ============================================================
# 综合过滤
# ============================================================

def comprehensive_filter(code: str, name: str, bars: List[Bar], anchor_idx: int,
                         anchor_turnover: Optional[float] = None,
                         quote: Optional[dict] = None,
                         params: Optional[dict] = None,
                         min_days: int = 60, min_turnover: float = 3.0) -> Tuple[bool, str, bool]:
    """综合风险过滤

    返回: (exclude, reason, skipped)
        exclude: 是否剔除
        reason: 剔除原因
        skipped: 是否有检查项因数据缺失被跳过（提示用）
    """
    checks = [
        check_st(name),
        check_delist_risk(code, quote),
        check_new_stock(bars, min_days, code=code),
        check_one_word_limit(bars, anchor_idx, code, params),
        check_consecutive_limit(bars, anchor_idx, code, params),
        check_downtrend_rebound(bars, anchor_idx, params),
    ]
    for excluded, reason in checks:
        if excluded:
            return True, reason, False

    # 换手率：单独处理缺失情况
    excluded, reason = check_turnover(anchor_turnover, min_turnover)
    if excluded:
        return True, reason, False
    skipped = anchor_turnover is None
    return False, "", skipped


if __name__ == "__main__":
    print("risk_filter 模块已加载。")
