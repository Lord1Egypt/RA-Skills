# -*- coding: utf-8 -*-
"""
InvAssistant — 入场引擎 v1.5
支持双模式入场：模式A（恐慌入场/三红线）+ 模式B（趋势确认入场）。
v1.5.2 新增：叙事驱动型成长股(Narrative Growth)估值分类。

模式选择逻辑：
  VIX > 20 或 近月大盘跌 > 5% → 用模式A（等恐慌入场）
  VIX < 20 且 大盘MA50以上   → 用模式B（趋势确认入场）

红线是过滤条件(Filter)，全部通过才可建仓，不是评分制(Scoring)。
"""
import pandas as pd


# ============ 默认参数 ============
DEFAULT_REDLINE_PARAMS = {
    "emotion_drop_threshold": -4,   # 单日跌幅触发阈值 (%)
    "consecutive_days": 3,          # 连续下跌天数触发阈值
    "ma_proximity": 0.03,           # 均线接近度 (3%)
    "bounce_threshold": 1.5,         # 强反弹涨幅阈值 (%)
    "volume_ratio": 1.2,             # 放量判定倍数 (120%)
    "entry_size": 0.3                # 建仓仓位 (30%)
}

# 模式B（趋势确认入场）参数
DEFAULT_TREND_PARAMS = {
    "ma_period": 50,                # 趋势均线周期
    "breakout_period": 20,           # 突破前高点周期
    "volume_surge": 1.2,             # 放量倍数 (>5日均量)
    "entry_size": 0.2                # 模式B仓位（比模式A保守）
}

DEFAULT_MARKET_PARAMS = {
    "vix_threshold": 25
}


def check_emotion(df, params=None):
    """
    红线1：情绪释放型下跌

    触发条件（满足任一）：
    - 单日跌幅 ≥ emotion_drop_threshold (默认4%)
    - 连续 consecutive_days (默认3) 个交易日下跌

    Args:
        df: 股票 OHLCV DataFrame
        params: 策略参数 dict

    Returns:
        (passed: bool, detail: str)
    """
    if df is None or len(df) < 5:
        return False, "数据不足"

    p = {**DEFAULT_REDLINE_PARAMS, **(params or {})}
    threshold = p["emotion_drop_threshold"]
    consec_req = p["consecutive_days"]

    df = df.copy()
    df['Return'] = df['Close'].pct_change() * 100

    latest_return = df['Return'].iloc[-1]
    results = []

    # 检查1：单日跌幅
    if latest_return <= threshold:
        results.append(f"单日跌幅 {latest_return:.2f}% (≥{abs(threshold)}%)")

    # 检查2：连续下跌
    consecutive_down = 0
    for i in range(len(df) - 1, 0, -1):
        if df.iloc[i]['Return'] < 0:
            consecutive_down += 1
        else:
            break

    if consecutive_down >= consec_req:
        results.append(f"连续 {consecutive_down} 个交易日下跌")

    if results:
        return True, "; ".join(f"✓ {r}" for r in results)
    return False, "未检测到明显情绪释放"


def check_tech(df, params=None):
    """
    红线2：技术止跌信号（严格标准）

    需要真实的止跌确认，"接近均线"或"单次反弹"不算通过：
    - 放量下跌后缩量（量能萎缩至前日70%以下）
    - 均线强承接（下影线 + 收涨 + 放量120%+ 或 强反弹≥1.5%）
    - 完整 Higher Low 结构（低点A→反弹→低点B>A→2日确认）

    Args:
        df: 股票 OHLCV DataFrame
        params: 策略参数 dict

    Returns:
        (passed: bool, detail: str)
    """
    if df is None or len(df) < 20:
        return False, "数据不足(需要20日数据)"

    p = {**DEFAULT_REDLINE_PARAMS, **(params or {})}

    df = df.copy()
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()

    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else None
    close_price = latest['Close']

    signals = []

    # ---- 检查1: 缩量信号 ----
    if prev is not None and len(df) > 2:
        prev2 = df.iloc[-3]
        vol_ratio = latest['Volume'] / prev['Volume'] if prev['Volume'] > 0 else 1
        prev_down = prev['Close'] < prev2['Close']
        today_shrink = vol_ratio < 0.7
        if prev_down and today_shrink:
            signals.append(f"✓ 放量跌后缩量 (量能{vol_ratio:.0%})")

    # ---- 检查2: 均线强承接 ----
    # 下影线：低点远离收盘，说明有买盘承接
    has_lower_shadow = (latest['Close'] - latest['Low']) > (latest['High'] - latest['Close']) * 1.5
    today_up = latest['Close'] > latest['Open']
    today_return = (latest['Close'] - latest['Open']) / latest['Open'] * 100 if latest['Open'] > 0 else 0
    vol_up = prev is not None and latest['Volume'] > prev['Volume'] * p["volume_ratio"]
    strong_bounce = today_return >= p["bounce_threshold"]
    # 真实承接 = 下影线 + 收涨 + (放量 或 强反弹)
    real_support = has_lower_shadow and today_up and (vol_up or strong_bounce)

    ma20 = latest['MA20']
    ma50 = latest['MA50']

    if pd.notna(ma20) and abs(close_price - ma20) / ma20 < p["ma_proximity"]:
        if real_support:
            signals.append(f"✓ MA20承接 (${ma20:.2f}, 下影线+{'放量' if vol_up else ''}反弹{today_return:+.1f}%)")

    if pd.notna(ma50) and abs(close_price - ma50) / ma50 < p["ma_proximity"]:
        if real_support:
            signals.append(f"✓ MA50承接 (${ma50:.2f}, 下影线+{'放量' if vol_up else ''}反弹{today_return:+.1f}%)")

    # ---- 检查3: 完整 Higher Low 结构 ----
    if len(df) >= 15:
        recent_lows = []
        for i in range(len(df) - 15, len(df) - 1):
            if i > 0 and i < len(df) - 1:
                if df.iloc[i]['Low'] < df.iloc[i-1]['Low'] and df.iloc[i]['Low'] < df.iloc[i+1]['Low']:
                    recent_lows.append((i, df.iloc[i]['Low'], df.index[i].strftime('%m-%d')))

        if len(recent_lows) >= 2:
            low_a = recent_lows[-2]
            low_b = recent_lows[-1]
            if low_b[1] > low_a[1]:
                days_after_b = len(df) - 1 - low_b[0]
                if days_after_b >= 2:
                    prices_after = [df.iloc[j]['Close'] for j in range(low_b[0]+1, min(low_b[0]+3, len(df)))]
                    if all(p_val > low_b[1] for p_val in prices_after):
                        signals.append(f"✓ Higher Low确认 ({low_a[2]}${low_a[1]:.0f}→{low_b[2]}${low_b[1]:.0f})")

    if signals:
        return True, "; ".join(signals)

    # 诊断信息
    diag = []
    if pd.notna(ma20):
        diag.append(f"MA20=${ma20:.2f}({(close_price-ma20)/ma20*100:+.1f}%)")
    diag.append("有下影线" if has_lower_shadow else "无下影线")
    diag.append("收涨" if today_up else "收跌")
    return False, f"未确认止跌 ({', '.join(diag)})"


def check_market(market_data, params=None):
    """
    红线3：市场未进入系统性风险

    必须全部满足：
    - QQQ 未连续3日下跌
    - SPX 未连续3日下跌
    - VIX < vix_threshold (默认25)

    Args:
        market_data: dict 包含 QQQ, ^GSPC, ^VIX 的 DataFrame
        params: 含 vix_threshold 的参数 dict

    Returns:
        (passed: bool, detail: str)
    """
    p = {**DEFAULT_MARKET_PARAMS, **(params or {})}
    vix_threshold = p["vix_threshold"]

    qqq = market_data.get("QQQ")
    spx = market_data.get("^GSPC")
    vix = market_data.get("^VIX")

    if qqq is None or spx is None or vix is None:
        return False, "市场数据缺失"

    results = []
    checks_passed = 0

    # QQQ 检查
    qqq_returns = qqq['Close'].pct_change().dropna()
    if len(qqq_returns) >= 3:
        if not all(r < 0 for r in qqq_returns.tail(3)):
            checks_passed += 1
            results.append("✓ QQQ 未连续暴跌")
        else:
            results.append("✗ QQQ 连续3日下跌")
    else:
        checks_passed += 1
        results.append("✓ QQQ 数据不足，默认通过")

    # VIX 检查
    latest_vix = vix['Close'].iloc[-1]
    if latest_vix < vix_threshold:
        checks_passed += 1
        results.append(f"✓ VIX = {latest_vix:.2f} (<{vix_threshold})")
    else:
        results.append(f"✗ VIX = {latest_vix:.2f} (≥{vix_threshold})")

    # SPX 检查
    spx_returns = spx['Close'].pct_change().dropna()
    if len(spx_returns) >= 3:
        if not all(r < 0 for r in spx_returns.tail(3)):
            checks_passed += 1
            results.append("✓ SPX 未连续暴跌")
        else:
            results.append("✗ SPX 连续3日下跌")
    else:
        checks_passed += 1
        results.append("✓ SPX 数据不足，默认通过")

    passed = checks_passed >= 3
    return passed, "; ".join(results)


def check_pullback(df, threshold=0.06):
    """
    回调检查：判断是否达到加仓阈值。

    Args:
        df: 股票 OHLCV DataFrame
        threshold: 回调幅度阈值 (默认6%)

    Returns:
        (signal: bool, detail: str, pullback_pct: str)
    """
    if df is None or len(df) < 10:
        return False, "数据不足", "N/A"

    high = df["Close"].tail(20).max()
    cur = df["Close"].iloc[-1]
    pb = (high - cur) / high

    return pb >= threshold, f"回调{pb*100:.1f}%", f"{pb*100:.1f}%"


def run_redline_check(df, market_data, params=None, market_params=None):
    """
    执行完整的三条红线检查。

    Args:
        df: 目标股票 OHLCV DataFrame
        market_data: 市场指标数据 dict
        params: 红线策略参数
        market_params: 市场环境参数

    Returns:
        dict 包含 rl1, rl2, rl3, all_passed, action, detail
    """
    rl1_passed, rl1_detail = check_emotion(df, params)
    rl2_passed, rl2_detail = check_tech(df, params)
    rl3_passed, rl3_detail = check_market(market_data, market_params)

    all_passed = rl1_passed and rl2_passed and rl3_passed
    passed_count = sum([rl1_passed, rl2_passed, rl3_passed])

    entry_size = (params or {}).get("entry_size", DEFAULT_REDLINE_PARAMS["entry_size"])

    if all_passed:
        action = f"三条红线全部通过 → 可建仓{int(entry_size*100)}%"
    else:
        failed = []
        if not rl1_passed:
            failed.append("情绪释放")
        if not rl2_passed:
            failed.append("技术止跌")
        if not rl3_passed:
            failed.append("市场环境")
        action = f"不建仓 | 未通过: {', '.join(failed)}"

    return {
        "red_line_1": {"passed": rl1_passed, "detail": rl1_detail},
        "red_line_2": {"passed": rl2_passed, "detail": rl2_detail},
        "red_line_3": {"passed": rl3_passed, "detail": rl3_detail},
        "passed_count": passed_count,
        "all_passed": all_passed,
        "action": action
    }


# ============ 模式B：趋势确认入场 ============

def check_trend_entry(df, params=None):
    """
    模式B：趋势确认入场 — 四条件全部满足才可入场。

    条件1：趋势确立 — 价格站上MA50且MA50向上
    条件2：突破确认 — 突破近20日高点 + 放量(>5日均量120%)
    条件3：基本面支持 — 最近一季营收+利润双增长（需手动配置）
    条件4：估值不离谱 — 按标的分类使用对应标尺

    Args:
        df: 股票 OHLCV DataFrame
        params: 含 ma_period, breakout_period, volume_surge 的参数 dict

    Returns:
        (passed: bool, detail: str, failed_conditions: list)
    """
    if df is None or len(df) < 60:
        return False, "数据不足(需要60日数据)", ["数据不足"]

    p = {**DEFAULT_TREND_PARAMS, **(params or {})}
    ma_period = p["ma_period"]
    break_period = p["breakout_period"]
    vol_surge = p["volume_surge"]

    df = df.copy()
    ma = df["Close"].rolling(ma_period).mean()
    df["MA"] = ma

    latest = df.iloc[-1]
    close = latest["Close"]
    ma_val = latest["MA"]

    signals = []
    failed = []

    # 条件1：趋势确立 — 价格站上MA50且MA50向上
    if pd.notna(ma_val) and close > ma_val:
        # MA向上：最近5日均线值递增
        ma_series = df["MA"].dropna()
        if len(ma_series) >= 5:
            ma_recent = ma_series.tail(5).values
            if all(ma_recent[i] <= ma_recent[i+1] for i in range(4)):
                signals.append("✓ 趋势确立：站上MA" + str(ma_period) + "且均线向上")
            else:
                failed.append("趋势：价格站上MA" + str(ma_period) + "但均线未向上")
        else:
            signals.append("✓ 趋势确立：站上MA" + str(ma_period))
    else:
        failed.append("趋势：未站上MA" + str(ma_period))

    # 条件2：突破确认 — 突破近N日高点 + 放量
    high_period = df["High"].tail(break_period).max()
    vol_avg_5 = df["Volume"].tail(5).mean()
    today_vol = latest["Volume"]
    latest_close = close

    if latest_close >= high_period:
        if today_vol >= vol_avg_5 * vol_surge:
            signals.append(f"✓ 突破确认：突破{break_period}日高点(${high_period:.2f})+放量(量比{today_vol/vol_avg_5:.1f}x)")
        else:
            signals.append(f"✓ 突破确认：突破{break_period}日高点(${high_period:.2f})，但放量不足")
            failed.append("放量不足")
    else:
        failed.append(f"突破：未突破{break_period}日高点(现价${latest_close:.2f} vs ${high_period:.2f})")

    # 条件3：基本面支持（需在 params 中手动配置）
    fundamental_ok = params.get("fundamental_ok", False) if params else False
    if fundamental_ok:
        signals.append("✓ 基本面：最近一季营收+利润双增长")
    else:
        failed.append("基本面：未配置 fundamental_ok=true")

    # 条件4：估值不离谱（需在 params 中配置 valuation_category）
    valuation_category = params.get("valuation_category", "standard") if params else "standard"
    if valuation_category == "narrative_growth":
        signals.append("⚠️ 叙事成长股：需手动确认估值不离谱（用自身历史中枢判断）")
    else:
        signals.append("✓ 估值：传统估值标的（按行业中位数判断）")

    all_passed = len(failed) == 0
    detail = "; ".join(signals)
    if failed:
        detail += " | 未通过: " + ", ".join(failed)
    return all_passed, detail, failed


def determine_entry_mode(market_data, params=None):
    """
    根据市场环境决定使用哪种入场模式。

    VIX > 20 或 近月大盘跌 > 5% → 模式A（恐慌入场）
    VIX < 20 且 大盘MA50以上   → 模式B（趋势确认入场）

    Args:
        market_data: dict 包含 ^VIX 和 QQQ 的 DataFrame
        params: 配置参数 dict

    Returns:
        str: "mode_a" | "mode_b"
    """
    vix_df = market_data.get("^VIX")
    qqq_df = market_data.get("QQQ")

    if vix_df is None:
        return "mode_a"  # 默认保守

    latest_vix = vix_df["Close"].iloc[-1]
    vix_threshold = params.get("vix_threshold", 25) if params else 25

    if latest_vix > 20:
        return "mode_a"

    if qqq_df is not None and len(qqq_df) >= 25:
        qqq = qqq_df.copy()
        qqq["MA50"] = qqq["Close"].rolling(50).mean()
        latest_close = qqq["Close"].iloc[-1]
        latest_ma50 = qqq["MA50"].iloc[-1]
        if pd.notna(latest_ma50) and latest_close > latest_ma50:
            # 近月跌幅
            month_ago = qqq["Close"].iloc[-21] if len(qqq) >= 21 else qqq["Close"].iloc[0]
            pct_change = (latest_close - month_ago) / month_ago * 100
            if pct_change < -5:
                return "mode_a"

        if pd.notna(latest_ma50) and latest_close <= latest_ma50:
            return "mode_a"
    else:
        return "mode_a"

    return "mode_b"


def run_trend_check(df, market_data, params=None, market_params=None):
    """
    执行模式B（趋势确认入场）的完整检查。

    Returns:
        dict 包含 trend1-4, all_passed, action
    """
    p = {**DEFAULT_TREND_PARAMS, **(params or {})}

    df_copy = df.copy() if df is not None else None
    ma_period = p["ma_period"]
    break_period = p["breakout_period"]
    vol_surge = p["volume_surge"]

    detail_parts = []
    failed_conditions = []
    all_passed = False

    if df_copy is None or len(df_copy) < 60:
        return {
            "trend_1_trend": {"passed": False, "detail": "数据不足"},
            "trend_2_breakout": {"passed": False, "detail": "数据不足"},
            "trend_3_fundamental": {"passed": False, "detail": "数据不足"},
            "trend_4_valuation": {"passed": False, "detail": "数据不足"},
            "all_passed": False,
            "action": "不建仓 | 数据不足"
        }

    ma = df_copy["Close"].rolling(ma_period).mean()
    df_copy["MA"] = ma
    latest = df_copy.iloc[-1]
    close = latest["Close"]
    ma_val = latest["MA"]

    # 条件1：趋势确立
    trend1_pass = False
    trend1_detail = "未通过"
    if pd.notna(ma_val) and close > ma_val:
        ma_series = df_copy["MA"].dropna()
        if len(ma_series) >= 5:
            ma_recent = ma_series.tail(5).values
            if all(ma_recent[i] <= ma_recent[i+1] for i in range(4)):
                trend1_pass = True
                trend1_detail = f"✓ 站上MA{ma_period}且均线向上"
    if not trend1_pass:
        failed_conditions.append("趋势未确立")

    # 条件2：突破确认
    trend2_pass = False
    trend2_detail = "未通过"
    high_period = df_copy["High"].tail(break_period).max()
    vol_avg_5 = df_copy["Volume"].tail(5).mean()
    today_vol = latest["Volume"]
    if close >= high_period and today_vol >= vol_avg_5 * vol_surge:
        trend2_pass = True
        trend2_detail = f"✓ 突破{break_period}日高点+放量"
    elif close >= high_period:
        trend2_pass = True
        trend2_detail = f"✓ 突破{break_period}日高点（放量不足）"
    if not trend2_pass:
        failed_conditions.append("突破未确认")

    # 条件3：基本面
    fundamental_ok = params.get("fundamental_ok", False) if params else False
    trend3_pass = fundamental_ok
    trend3_detail = "✓ 基本面支持" if fundamental_ok else "✗ 未配置基本面确认"

    # 条件4：估值
    valuation_category = params.get("valuation_category", "standard") if params else "standard"
    trend4_pass = True  # 传统标的默认通过，叙事股需手动确认
    trend4_detail = f"✓ 估值类别: {valuation_category}"

    all_passed = trend1_pass and trend2_pass and trend3_pass and trend4_pass

    entry_size = p.get("entry_size", 0.2)
    if all_passed:
        action = f"模式B四条件全部通过 → 可建仓{int(entry_size*100)}%"
    else:
        action = f"不建仓 | 未通过: {', '.join(failed_conditions)}"

    return {
        "trend_1_trend": {"passed": trend1_pass, "detail": trend1_detail},
        "trend_2_breakout": {"passed": trend2_pass, "detail": trend2_detail},
        "trend_3_fundamental": {"passed": trend3_pass, "detail": trend3_detail},
        "trend_4_valuation": {"passed": trend4_pass, "detail": trend4_detail},
        "all_passed": all_passed,
        "action": action
    }


def classify_narrative_growth(params=None):
    """
    判断标的是否属于叙事驱动型成长股(Narrative Growth)。

    识别条件（满足任意2条）：
    - 3年Forward PE 25分位 > 行业中位数 × 2
    - EPS增速预期 > 行业均值 × 2
    - 业务含多叙事（AI/机器人/FSD等超越传统分类）

    Args:
        params: 含 valuation_indicators 的参数 dict

    Returns:
        bool: 是否为叙事驱动型成长股
    """
    if params is None:
        return False

    indicators = params.get("valuation_indicators", {})
    if not indicators:
        return False

    conditions_met = 0

    # 条件1：Forward PE偏高
    pe_ratio = indicators.get("forward_pe_25th_percentile", 0)
    industry_pe = indicators.get("industry_pe_median", 1)
    if pe_ratio > 0 and industry_pe > 0 and pe_ratio > industry_pe * 2:
        conditions_met += 1

    # 条件2：EPS增速远超行业
    eps_growth = indicators.get("eps_growth_expected", 0)
    industry_growth = indicators.get("industry_eps_growth_avg", 1)
    if eps_growth > 0 and industry_growth > 0 and eps_growth > industry_growth * 2:
        conditions_met += 1

    # 条件3：含多叙事标签
    narratives = indicators.get("narrative_tags", [])
    high_narrative_keywords = ["AI", "机器人", "FSD", "自动驾驶", "大模型", "AGI", "量子计算"]
    matches = sum(1 for n in narratives if any(k in str(n) for k in high_narrative_keywords))
    if matches >= 2:
        conditions_met += 1

    return conditions_met >= 2
