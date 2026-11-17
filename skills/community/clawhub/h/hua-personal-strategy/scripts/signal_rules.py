#!/usr/bin/env python3
"""Deterministic personal mutual-fund signal rules. No network access."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, time
from pathlib import Path
from statistics import mean
from typing import Any
from zoneinfo import ZoneInfo


MODE_COEFFICIENT = {"BULL": 0.05, "BEAR": 0.03, "RANGE": 0.04}
# 基金轮动以近 1 月、近 3 月为主；近 6 月和近 1 年用于趋势稳定性和防止追旧热点。
MOMENTUM_WEIGHTS = {"r20": 0.45, "r60": 0.35, "r120": 0.15, "r250": 0.05}
MODE_ENTER_THRESHOLD_PCT = 2.2
MODE_EXIT_THRESHOLD_PCT = 1.8
MIN_FUND_HISTORY_POINTS = 60
DEFAULT_INCREMENTAL_CASH = 3000.0
VALID_MODES = {"BULL", "BEAR", "RANGE"}
CHASE_RISK_PCT = 2.0
STRONG_TREND_FOLLOW_PCT = 3.0
PULLBACK_ENTRY_PCT = -1.5
BREAKDOWN_RISK_PCT = -3.0
DEFAULT_MARKET_TIMEZONE = "Asia/Shanghai"
DEFAULT_TRADE_CUTOFF = "15:00"


def number(value: Any, default: float | None = None) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return result if math.isfinite(result) else default


def parse_cutoff(value: Any) -> time:
    text = str(value or DEFAULT_TRADE_CUTOFF).strip()
    try:
        hour, minute = text.split(":", 1)
        return time(int(hour), int(minute[:2]))
    except (ValueError, TypeError):
        return time(15, 0)


def parse_run_datetime(value: Any, tz_name: str) -> datetime | None:
    if not value:
        return None
    text = str(value).strip()
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = ZoneInfo(DEFAULT_MARKET_TIMEZONE)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt.astimezone(tz)


def execution_window(payload: dict[str, Any]) -> dict[str, Any]:
    """Resolve whether same-day fund trading is still possible.

    China mutual-fund subscription/redemption requests submitted after the usual
    15:00 cutoff belong to the next trading day.  The engine therefore must not
    output "today buy/sell" amounts after cutoff; signals can still be archived
    and reviewed for the next trading day.
    """

    raw = payload.get("execution") if isinstance(payload.get("execution"), dict) else {}
    timestamps = payload.get("timestamps") if isinstance(payload.get("timestamps"), dict) else {}
    tz_name = str(raw.get("market_timezone") or raw.get("timezone") or DEFAULT_MARKET_TIMEZONE)
    cutoff_text = str(raw.get("trade_cutoff_time") or raw.get("cutoff_time") or DEFAULT_TRADE_CUTOFF)
    run_at_raw = (
        raw.get("run_at")
        or raw.get("generated_at")
        or timestamps.get("run_at")
        or timestamps.get("generated_at")
        or timestamps.get("market")
        or payload.get("generated_at")
    )
    run_at = parse_run_datetime(run_at_raw, tz_name)
    if run_at is None:
        try:
            run_at = datetime.now(ZoneInfo(tz_name))
        except Exception:
            run_at = datetime.now(ZoneInfo(DEFAULT_MARKET_TIMEZONE))
    cutoff = parse_cutoff(cutoff_text)
    is_trading_day_raw = raw.get("is_trading_day")
    is_trading_day = True if is_trading_day_raw is None else bool(is_trading_day_raw)
    after_cutoff = bool(run_at and run_at.time() >= cutoff)
    same_day_executable = bool(is_trading_day and not after_cutoff)
    if not is_trading_day:
        blocker = "non_trading_day"
        status = "非交易日"
    elif after_cutoff:
        blocker = "trade_window_closed"
        status = "交易窗口已关闭"
    else:
        blocker = None
        status = "交易窗口开放"
    return {
        "run_at": run_at.isoformat() if run_at else str(run_at_raw or ""),
        "market_timezone": tz_name,
        "trade_cutoff_time": cutoff_text,
        "is_trading_day": is_trading_day,
        "after_cutoff": after_cutoff,
        "same_day_executable": same_day_executable,
        "next_trading_day": raw.get("next_trading_day") or raw.get("next_trade_date") or raw.get("nextTradingDay"),
        "status": status,
        "blocker": blocker,
        "source": raw.get("source") or "execution/get_status/calculate_trading_dates",
    }


def ordered_values(history: Any, keys: tuple[str, ...]) -> list[float]:
    return list(dated_series(history, keys).values())


def dated_series(history: Any, keys: tuple[str, ...]) -> dict[str, float]:
    rows: list[tuple[str, float]] = []
    for index, item in enumerate(history or []):
        if not isinstance(item, dict):
            continue
        value = next((number(item.get(key)) for key in keys if number(item.get(key)) is not None), None)
        if value is None or value <= 0:
            continue
        date = str(item.get("date") or item.get("day") or item.get("timestamp") or index)
        rows.append((date, value))
    rows.sort(key=lambda row: row[0])
    return dict(rows)


def pct_return(values: list[float], periods: int) -> float | None:
    if len(values) <= periods or values[-periods - 1] == 0:
        return None
    return (values[-1] / values[-periods - 1] - 1.0) * 100.0


def moving_average(values: list[float], periods: int, end_offset: int = 0) -> float | None:
    end = len(values) - end_offset
    start = end - periods
    if start < 0 or end <= 0:
        return None
    return mean(values[start:end])


def metrics(values: list[float]) -> dict[str, float | None]:
    current = values[-1] if values else None
    ma5 = moving_average(values, 5)
    ma20 = moving_average(values, 20)
    ma60 = moving_average(values, 60)
    prev_ma20 = moving_average(values, 20, 1)
    prev_ma60 = moving_average(values, 60, 1)
    max_drawdown = None
    annualized_volatility = None
    if values:
        peak = values[0]
        worst = 0.0
        for value in values:
            peak = max(peak, value)
            if peak > 0:
                worst = min(worst, (value / peak - 1.0) * 100.0)
        max_drawdown = worst
    if len(values) >= 2:
        daily_returns = [
            values[index] / values[index - 1] - 1.0
            for index in range(1, len(values))
            if values[index - 1] > 0
        ]
        if len(daily_returns) >= 2:
            avg = mean(daily_returns)
            variance = sum((item - avg) ** 2 for item in daily_returns) / (len(daily_returns) - 1)
            annualized_volatility = math.sqrt(variance) * math.sqrt(252.0) * 100.0
    r20 = pct_return(values, 20)
    r60 = pct_return(values, 60)
    r120 = pct_return(values, 120)
    r250 = pct_return(values, 250)
    rotation_acceleration_1m_vs_3m = (
        r20 - r60 / 3.0
        if r20 is not None and r60 is not None
        else None
    )
    rotation_acceleration_3m_vs_6m = (
        r60 - r120 / 2.0
        if r60 is not None and r120 is not None
        else None
    )
    return {
        "points": float(len(values)),
        "current": current,
        "ma20": ma20,
        "ma60": ma60,
        "bias5": ((current / ma5 - 1) * 100) if current and ma5 else None,
        "bias10": ((current / moving_average(values, 10) - 1) * 100) if current and moving_average(values, 10) else None,
        "bias20": ((current / ma20 - 1) * 100) if current and ma20 else None,
        "r5": pct_return(values, 5),
        "r10": pct_return(values, 10),
        "r20": r20,
        "r60": r60,
        "r120": r120,
        "r250": r250,
        "rotation_acceleration_1m_vs_3m": rotation_acceleration_1m_vs_3m,
        "rotation_acceleration_3m_vs_6m": rotation_acceleration_3m_vs_6m,
        "max_drawdown_pct": max_drawdown,
        "annualized_volatility_pct": annualized_volatility,
        "cross_down": bool(
            ma20 is not None
            and ma60 is not None
            and prev_ma20 is not None
            and prev_ma60 is not None
            and ma20 < ma60
            and prev_ma20 >= prev_ma60
        ),
    }


def metric_snapshot(base: dict[str, Any], overrides: Any) -> dict[str, Any]:
    """Merge externally precomputed official metrics into computed metrics.

    The preferred path is still full official NAV history.  This fallback exists
    for MCP/server builders that already computed the same fields from official
    data and pass a compact audited snapshot.
    """

    result = dict(base)
    if not isinstance(overrides, dict):
        return result
    allowed = {
        "points",
        "current",
        "ma20",
        "ma60",
        "bias5",
        "bias10",
        "bias20",
        "r5",
        "r10",
        "r20",
        "r60",
        "r120",
        "r250",
        "rotation_acceleration_1m_vs_3m",
        "rotation_acceleration_3m_vs_6m",
        "max_drawdown_pct",
        "annualized_volatility_pct",
    }
    for key in allowed:
        value = number(overrides.get(key))
        if value is not None:
            result[key] = value
    if "cross_down" in overrides:
        result["cross_down"] = bool(overrides.get("cross_down"))
    if result.get("rotation_acceleration_1m_vs_3m") is None:
        r20 = number(result.get("r20"))
        r60 = number(result.get("r60"))
        if r20 is not None and r60 is not None:
            result["rotation_acceleration_1m_vs_3m"] = r20 - r60 / 3.0
    if result.get("rotation_acceleration_3m_vs_6m") is None:
        r60 = number(result.get("r60"))
        r120 = number(result.get("r120"))
        if r60 is not None and r120 is not None:
            result["rotation_acceleration_3m_vs_6m"] = r60 - r120 / 2.0
    return result


def normalize_mode(value: Any) -> str | None:
    mode = str(value or "").upper()
    return mode if mode in VALID_MODES else None


def market_mode(benchmark_metrics: dict[str, Any], previous_mode: str | None = None) -> tuple[str, float | None, str]:
    ma20 = number(benchmark_metrics.get("ma20"))
    ma60 = number(benchmark_metrics.get("ma60"))
    if ma20 is None or ma60 in (None, 0) or number(benchmark_metrics.get("points"), 0) < 60:
        return "UNKNOWN", None, "insufficient_benchmark_history"
    gap = (ma20 - ma60) / ma60 * 100.0
    previous = normalize_mode(previous_mode)
    abs_gap = abs(gap)
    if abs_gap < MODE_EXIT_THRESHOLD_PCT:
        return "RANGE", gap, "inside_range_band"
    if abs_gap >= MODE_ENTER_THRESHOLD_PCT:
        return ("BULL" if gap > 0 else "BEAR"), gap, "outside_trend_entry_band"
    if (gap > 0 and previous == "BULL") or (gap < 0 and previous == "BEAR"):
        return previous, gap, "hysteresis_keep_previous_mode"
    if previous:
        return "RANGE", gap, "hysteresis_direction_changed_or_previous_range"
    return "RANGE", gap, "hysteresis_no_previous_mode_defaults_range"


# ============================================================================
# ADAPTIVE STRATEGY MODULE
# 波动率市场状态检测 + 自适应调仓频率 + 波动率调整仓位
# ============================================================================

def compute_rolling_volatility(daily_returns: list[float], window: int = 20) -> float | None:
    """Compute annualized rolling volatility from daily percentage returns."""
    if len(daily_returns) < window:
        return None
    subset = daily_returns[-window:]
    mean_ret = sum(subset) / len(subset)
    variance = sum((r - mean_ret) ** 2 for r in subset) / (len(subset) - 1)
    daily_std = math.sqrt(variance)
    return daily_std * math.sqrt(252)


def detect_volatility_regime(annualized_vol: float) -> str:
    """Classify market volatility regime: LOW/NORMAL/HIGH/EXTREME."""
    if annualized_vol < 12:
        return "LOW"
    elif annualized_vol < 20:
        return "NORMAL"
    elif annualized_vol < 32:
        return "HIGH"
    else:
        return "EXTREME"


def detect_trend_regime(benchmark_ma20: float | None, benchmark_ma60: float | None, 
                         benchmark_price: float | None) -> str:
    """Classify market trend: STRONG_UP/UP/SIDEWAYS/DOWN/STRONG_DOWN."""
    if None in (benchmark_ma20, benchmark_ma60, benchmark_price):
        return "UNKNOWN"
    ma_gap_pct = (benchmark_ma20 - benchmark_ma60) / benchmark_ma60 * 100 if benchmark_ma60 else 0
    price_vs_ma20 = (benchmark_price - benchmark_ma20) / benchmark_ma20 * 100 if benchmark_ma20 else 0
    if ma_gap_pct > 2.0 and price_vs_ma20 > 1.0:
        return "STRONG_UP"
    elif ma_gap_pct > 0.5:
        return "UP"
    elif ma_gap_pct < -2.0 and price_vs_ma20 < -1.0:
        return "STRONG_DOWN"
    elif ma_gap_pct < -0.5:
        return "DOWN"
    else:
        return "SIDEWAYS"


def compute_adaptive_frequency(vol_regime: str, trend_regime: str) -> dict[str, Any]:
    """Compute adaptive trading parameters based on market regime."""
    vol_params = {
        "LOW":    {"min_deviation": 8.0, "max_position": 0.08, "confidence": 55, "urgency": 3},
        "NORMAL": {"min_deviation": 5.0, "max_position": 0.06, "confidence": 50, "urgency": 5},
        "HIGH":   {"min_deviation": 3.0, "max_position": 0.04, "confidence": 45, "urgency": 7},
        "EXTREME":{"min_deviation": 2.0, "max_position": 0.02, "confidence": 40, "urgency": 9},
    }
    params = vol_params.get(vol_regime, vol_params["NORMAL"]).copy()
    if trend_regime in ("STRONG_UP", "STRONG_DOWN"):
        params["min_deviation"] *= 0.8
        params["confidence"] -= 5
        params["urgency"] += 1
    elif trend_regime == "SIDEWAYS":
        params["min_deviation"] *= 1.2
        params["confidence"] += 5
        params["urgency"] -= 1
    return params


def compute_portfolio_weighted_index(indices_data: dict[str, list[dict]], weights: dict[str, float]) -> dict[str, Any]:
    """Compute weighted portfolio index from multiple indices.
    
    indices_data: {index_code: [{"date": "...", "change": ...}, ...]}
    weights: {index_code: weight} (should sum to 1.0)
    
    Returns: {"daily_returns": [...], "ann_vol": ..., "ma20": ..., "ma60": ..., "price": ...}
    """
    # Align dates across all indices
    all_dates = set()
    for code, data in indices_data.items():
        for item in data:
            all_dates.add(item.get("date", ""))
    all_dates = sorted(all_dates)
    
    # Build aligned return series
    aligned_returns = []
    for date in all_dates:
        weighted_return = 0.0
        total_weight = 0.0
        for code, data in indices_data.items():
            weight = weights.get(code, 0.0)
            if weight <= 0:
                continue
            for item in data:
                if item.get("date") == date:
                    change = number(item.get("change"))
                    if change is not None:
                        weighted_return += change * weight
                        total_weight += weight
                    break
        if total_weight > 0:
            aligned_returns.append(weighted_return / total_weight)
    
    # Compute volatility
    ann_vol = compute_rolling_volatility(aligned_returns, window=20) if len(aligned_returns) >= 20 else None
    
    # Compute MA from cumulative returns
    cumulative = []
    cum = 100.0
    for r in aligned_returns:
        cum *= (1 + r / 100.0)
        cumulative.append(cum)
    
    # Simple MA approximation
    if len(cumulative) >= 20:
        ma20 = sum(cumulative[-20:]) / 20
    else:
        ma20 = None
    if len(cumulative) >= 60:
        ma60 = sum(cumulative[-60:]) / 60
    else:
        ma60 = None
    
    return {
        "daily_returns": aligned_returns,
        "ann_vol": ann_vol,
        "ma20": ma20,
        "ma60": ma60,
        "price": cumulative[-1] if cumulative else None,
        "dates": all_dates,
    }


def adaptive_frequency_gate(
    benchmark_history: list[dict],
    benchmark_metrics: dict,
    portfolio_drawdown: float | None,
    last_signal_date: str | None = None,
    current_date: str = "",
    portfolio_indices: dict[str, list[dict]] | None = None,
    index_weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Determine if today is a good day to trade based on adaptive frequency.
    
    If portfolio_indices is provided, uses weighted multi-index instead of single benchmark.
    """
    # Use weighted multi-index if available (more representative of actual holdings)
    if portfolio_indices and index_weights:
        weighted = compute_portfolio_weighted_index(portfolio_indices, index_weights)
        daily_returns = weighted["daily_returns"]
        ann_vol = weighted["ann_vol"]
        ma20 = weighted["ma20"]
        ma60 = weighted["ma60"]
        price = weighted["price"]
        benchmark_source = "weighted_multi_index"
    else:
        # Fallback to single benchmark
        daily_returns = []
        for item in benchmark_history:
            change = number(item.get("change"))
            if change is not None:
                daily_returns.append(change)
        ann_vol = compute_rolling_volatility(daily_returns, window=20)
        ma20 = number(benchmark_metrics.get("ma20"))
        ma60 = number(benchmark_metrics.get("ma60"))
        price = number(benchmark_metrics.get("price")) or (benchmark_history[-1]["value"] if benchmark_history else None)
        benchmark_source = "single_benchmark"
    
    if ann_vol is None:
        return {
            "should_trade": True, "vol_regime": "UNKNOWN", "trend_regime": "UNKNOWN",
            "adaptive_params": compute_adaptive_frequency("NORMAL", "SIDEWAYS"),
            "reason": "insufficient_history, defaulting to normal mode"
        }
    
    vol_regime = detect_volatility_regime(ann_vol)
    trend_regime = detect_trend_regime(ma20, ma60, price)
    adaptive_params = compute_adaptive_frequency(vol_regime, trend_regime)
    
    should_trade = True
    reason_parts = [f"vol={ann_vol:.1f}%({vol_regime})", f"trend={trend_regime}"]
    
    if portfolio_drawdown is not None:
        abs_dd = abs(portfolio_drawdown)
        if abs_dd > 12:
            adaptive_params["confidence"] += 15
            adaptive_params["max_position"] *= 0.5
            reason_parts.append(f"dd={abs_dd:.1f}%(strict)")
        elif abs_dd > 8:
            adaptive_params["confidence"] += 8
            adaptive_params["max_position"] *= 0.7
            reason_parts.append(f"dd={abs_dd:.1f}%(cautious)")
        else:
            reason_parts.append(f"dd={abs_dd:.1f}%(normal)")
    
    if last_signal_date and current_date:
        try:
            last_dt = datetime.datetime.strptime(last_signal_date, "%Y-%m-%d")
            curr_dt = datetime.datetime.strptime(current_date, "%Y-%m-%d")
            days_since = (curr_dt - last_dt).days
            min_days = {"LOW": 20, "NORMAL": 10, "HIGH": 5, "EXTREME": 3}.get(vol_regime, 7)
            if days_since < min_days:
                should_trade = False
                reason_parts.append(f"freq_gate({days_since}<{min_days}d)")
            else:
                reason_parts.append(f"freq_ok({days_since}d)")
        except (ValueError, TypeError):
            pass
    
    return {
        "should_trade": should_trade,
        "vol_regime": vol_regime,
        "trend_regime": trend_regime,
        "annualized_vol": ann_vol,
        "adaptive_params": adaptive_params,
        "reason": "; ".join(reason_parts),
    }


def volatility_adjusted_position_size(
    base_amount: float,
    vol_regime: str,
    portfolio_drawdown: float | None,
    fund_volatility: float | None = None,
) -> float:
    """Adjust position size based on volatility and risk state."""
    vol_scale = {"LOW": 1.3, "NORMAL": 1.0, "HIGH": 0.7, "EXTREME": 0.4}.get(vol_regime, 1.0)
    dd_scale = 1.0
    if portfolio_drawdown is not None:
        abs_dd = abs(portfolio_drawdown)
        if abs_dd > 12: dd_scale = 0.4
        elif abs_dd > 8: dd_scale = 0.6
        elif abs_dd > 5: dd_scale = 0.8
    fund_scale = 1.0
    if fund_volatility is not None:
        if fund_volatility > 40: fund_scale = 0.6
        elif fund_volatility > 25: fund_scale = 0.8
        elif fund_volatility < 15: fund_scale = 1.2
    return round(base_amount * vol_scale * dd_scale * fund_scale, 2)




def determine_execution_data_source(is_qdii: bool) -> dict[str, Any]:
    """Determine which data sources matter for buy decisions.
    
    QDII 有三套日期/数据口径，不能简化成“昨天/今天”：

    - D 日：基金公司官方净值日，原始 NAV 历史必须保留 D 日。
    - G 日：HuahuaDaily 把该笔官方涨跌计入日历、组合复盘和回测的收益归属日。
      普通基金通常 G=D；QDII/T+N 基金按后端确认的 displayDate/publish_date/D→G 配对。
    - 执行层：今天 15:00 前申赎要参考今天之后仍会变化的海外市场，优先使用
      get_night_estimate 返回的持仓穿透夜盘估算、汇率、覆盖率和新鲜度。

    get_item_estimate 可解释已公布或当前估算的归属收益；但 QDII 今日申赎参考
    必须来自 get_night_estimate。NQF 只能是纳指/海外科技相关 QDII 的辅助
    跨市场因子，不能替代夜盘接口的持仓穿透和汇率折算。
    """
    if is_qdii:
        return {
            "buy_data_source": "get_night_estimate",
            "buy_explanation": "QDII 今日申赎参考夜盘接口：持仓穿透个股涨跌、汇率、覆盖率和校准结果；普通估值只解释归属收益",
            "nav_display_source": "item_estimate",
            "intraday_leaders": ["NQF", "HSTECH", "KS11"],
            "attribution_terms": ["D=净值日", "G=收益归属日", "night=执行层"],
        }
    else:
        return {
            "buy_data_source": "item_estimate",
            "buy_explanation": "今天买A股基金，收盘净值就是你能吃到的",
            "intraday_leaders": ["KS11"],  # KOSPI对A股半导体是实时领先指标
        }


def kospi_intraday_signal(kospi_change_pct: float, a_share_semiconductor_change_pct: float) -> dict[str, Any]:
    """Generate signal from KOSPI-A-share semiconductor correlation.
    
    KOSPI is a real-time leading indicator for A-share semiconductor:
    - If KOSPI is up but A-share semiconductor is down → potential mean reversion buy
    - If KOSPI is down and A-share semiconductor is down → confirm downtrend, wait
    - If KOSPI is up and A-share semiconductor is up → momentum confirmation
    """
    divergence = kospi_change_pct - a_share_semiconductor_change_pct
    
    if divergence > 3:
        # KOSPI significantly outperforming A-share semiconductor
        return {
            "signal": "mean_reversion_opportunity",
            "strength": "strong",
            "note": f"KOSPI +{kospi_change_pct:.1f}% vs A-share semiconductor {a_share_semiconductor_change_pct:+.1f}%, divergence {divergence:+.1f}%"
        }
    elif divergence < -3:
        # A-share semiconductor outperforming KOSPI (unusual)
        return {
            "signal": "caution",
            "strength": "medium", 
            "note": f"A-share semiconductor {a_share_semiconductor_change_pct:+.1f}% outperforming KOSPI {kospi_change_pct:+.1f}%, unusual divergence"
        }
    else:
        return {
            "signal": "aligned",
            "strength": "weak",
            "note": f"KOSPI and A-share semiconductor moving in sync (divergence {divergence:+.1f}%)"
        }

def direction_quality_score(
    direction_row: dict,
    benchmark_r10: float | None = None,
) -> float:
    """Score direction momentum quality (0-100). Higher = more reliable."""
    score = 50.0
    r20 = number(direction_row.get("r20"))
    r60 = number(direction_row.get("r60"))
    accel = number(direction_row.get("acceleration"))
    
    if r20 is None or r60 is None:
        return score
    
    # Consistency
    if r20 > 0 and r60 > 0: score += 10
    elif r20 < 0 and r60 < 0: score -= 10
    elif r20 > 0 and r60 < 0: score += 5
    else: score -= 5
    
    # Acceleration
    if accel is not None:
        if accel > 5: score += 15
        elif accel > 0: score += 5
        elif accel < -5: score -= 15
        elif accel < 0: score -= 5
    
    # Relative strength
    if benchmark_r10 is not None and r20 is not None:
        if r20 > benchmark_r10 + 3: score += 10
        elif r20 > benchmark_r10: score += 5
        elif r20 < benchmark_r10 - 3: score -= 10
        elif r20 < benchmark_r10: score -= 5
    
    # Momentum magnitude
    if r20 > 15: score += 5
    elif r20 < -15: score -= 5
    
    return max(0.0, min(100.0, score))


def transaction_cost_aware(amount: float, fund_fees: dict, portfolio_total: float) -> dict[str, Any]:
    """Check if trade is worth executing after costs."""
    purchase_fee_rate = number(fund_fees.get("purchase_fee_rate"), 0.0015)
    confirm_days = number(fund_fees.get("confirm_days"), 1)
    daily_opp_cost = portfolio_total * 0.0002
    opportunity_cost = daily_opp_cost * confirm_days
    purchase_fee = amount * purchase_fee_rate
    total_cost = purchase_fee + opportunity_cost
    if total_cost > amount * 0.005:
        return {"justified": False, "net_benefit": -total_cost,
                "reason": f"costs({total_cost:.0f}) > 0.5% of amount({amount:.0f})"}
    return {"justified": True, "net_benefit": amount * 0.01 - total_cost,
            "reason": f"costs({total_cost:.0f}) acceptable"}
def percentile(values: list[float], value: float) -> float:
    if len(values) <= 1:
        return 50.0
    below = sum(1 for item in values if item < value)
    equal = sum(1 for item in values if item == value)
    return (below + 0.5 * equal) / len(values) * 100.0


def build_direction_scores(funds: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for fund in funds:
        direction = str(fund.get("direction") or "unknown").strip() or "unknown"
        grouped.setdefault(direction, []).append(fund["metrics"])

    aggregates: dict[str, dict[str, float | None]] = {}
    for direction, items in grouped.items():
        aggregates[direction] = {}
        for key in MOMENTUM_WEIGHTS:
            valid = [number(item.get(key)) for item in items]
            valid = [item for item in valid if item is not None]
            aggregates[direction][key] = mean(valid) if valid else None
        for key in ("rotation_acceleration_1m_vs_3m", "rotation_acceleration_3m_vs_6m"):
            valid = [number(item.get(key)) for item in items]
            valid = [item for item in valid if item is not None]
            aggregates[direction][key] = mean(valid) if valid else None

    scores: dict[str, dict[str, Any]] = {}
    for direction, aggregate in aggregates.items():
        weighted = 0.0
        used_weight = 0.0
        for key, weight in MOMENTUM_WEIGHTS.items():
            value = number(aggregate.get(key))
            universe = [number(row.get(key)) for row in aggregates.values()]
            universe = [item for item in universe if item is not None]
            if value is None or not universe:
                continue
            weighted += percentile(universe, value) * weight
            used_weight += weight
        acceleration = number(aggregate.get("rotation_acceleration_1m_vs_3m"))
        acceleration_universe = [number(row.get("rotation_acceleration_1m_vs_3m")) for row in aggregates.values()]
        acceleration_universe = [item for item in acceleration_universe if item is not None]
        if acceleration is not None and acceleration_universe:
            weighted += percentile(acceleration_universe, acceleration) * 0.15
            used_weight += 0.15
        scores[direction] = {
            "score": weighted / used_weight if used_weight else None,
            "returns": aggregate,
        }

    ranked = sorted(
        ((direction, row["score"]) for direction, row in scores.items() if row["score"] is not None),
        key=lambda item: item[1],
        reverse=True,
    )
    for rank, (direction, _) in enumerate(ranked, 1):
        scores[direction]["rank"] = rank
    for direction in scores:
        scores[direction].setdefault("rank", None)
    return scores


def strength(technical: bool, momentum: bool, flow: bool) -> float:
    count = sum((technical, momentum, flow))
    return 1.0 if count == 3 else 0.6 if count == 2 else 0.3 if count == 1 else 0.0


def factor_score(status: Any, mapping: dict[str, float], default: float = 0.0) -> float:
    return mapping.get(str(status or "").lower(), default)


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return min(high, max(low, value))


def signal_strength_with_context(
    base: float,
    news_factor: dict[str, Any],
    sentiment_factor: dict[str, Any],
    style: str = "trend",
) -> float:
    """Adjust a price-derived signal by context evidence.

    The base signal must come from price/risk rules first.  News and sentiment
    only calibrate strength.  Sentiment is deliberately style-aware:
    - trend: risk-on confirms trend-following, risk-off slightly weakens it.
    - contrarian: risk-off can confirm panic/mean-reversion tests.
    - reduce: negative/crowded/risk-off conditions increase reduce urgency.
    """

    style = style if style in {"trend", "contrarian", "reduce"} else "trend"
    news_mappings = {
        "trend": {"supportive": 0.10, "neutral": 0.0, "negative": -0.15, "stale": -0.05, "unknown": 0.0},
        "contrarian": {"supportive": 0.05, "neutral": 0.0, "negative": -0.05, "stale": -0.05, "unknown": 0.0},
        "reduce": {"supportive": -0.05, "neutral": 0.0, "negative": 0.15, "stale": 0.0, "unknown": 0.0},
    }
    sentiment_mappings = {
        "trend": {"risk_on": 0.10, "neutral": 0.0, "risk_off": -0.05, "crowded": -0.10, "unknown": 0.0},
        "contrarian": {"risk_on": 0.0, "neutral": 0.0, "risk_off": 0.15, "crowded": -0.10, "unknown": 0.0},
        "reduce": {"risk_on": -0.05, "neutral": 0.0, "risk_off": 0.10, "crowded": 0.15, "unknown": 0.0},
    }
    news_bonus = factor_score(news_factor.get("status"), news_mappings[style])
    sentiment_bonus = factor_score(sentiment_factor.get("status"), sentiment_mappings[style])
    if str(news_factor.get("strength") or "").lower() == "strong":
        news_bonus *= 1.5
    if str(sentiment_factor.get("strength") or "").lower() == "strong":
        sentiment_bonus *= 1.5
    return clamp(base + news_bonus + sentiment_bonus)


def evidence_positive(flow_three_positive: bool, news_factor: dict[str, Any], sentiment_factor: dict[str, Any]) -> bool:
    return (
        flow_three_positive
        or str(news_factor.get("status") or "").lower() == "supportive"
        or str(sentiment_factor.get("status") or "").lower() == "risk_on"
    )


def bias_score(metrics_row: dict[str, Any], mode: str) -> tuple[float, str]:
    """Score price deviation without turning it into a mechanical trade."""

    bias20 = number(metrics_row.get("bias20"))
    bias10 = number(metrics_row.get("bias10"))
    bias5 = number(metrics_row.get("bias5"))
    if bias20 is None and bias10 is None and bias5 is None:
        return 50.0, "BIAS 缺失，均值回归因子中性处理"
    ref = bias20 if bias20 is not None else bias10 if bias10 is not None else bias5
    assert ref is not None
    if mode == "BULL":
        if -6 <= ref <= 3:
            return 78.0, "趋势环境下偏离温和，具备分批条件"
        if ref > 8:
            return 35.0, "趋势环境下短线偏热，降低追高意愿"
        if ref < -12:
            return 45.0, "偏离过深，需确认是否破位"
        return 60.0, "BIAS 未处于极端区间"
    if mode == "BEAR":
        if ref < -10:
            return 70.0, "弱市超跌，只有恐慌测试价值"
        if ref > 5:
            return 35.0, "弱市反弹偏热，降低继续持有评分"
        return 52.0, "弱市 BIAS 中性"
    if -8 <= ref <= -1:
        return 78.0, "震荡市回落到均值下方，均值回归分较高"
    if ref > 8:
        return 32.0, "震荡市偏离过高，追涨风险较大"
    if ref < -12:
        return 55.0, "震荡市明显超跌，但需确认没有破位"
    return 55.0, "震荡市 BIAS 中性"


def fund_multifactor_score(
    fund: dict[str, Any],
    metrics_row: dict[str, Any],
    mode: str,
    direction_score: float | None,
    news_factor: dict[str, Any],
    sentiment_factor: dict[str, Any],
    flow_three_positive: bool,
    flow_latest_negative: bool,
    history_ok: bool,
    purchasable: bool,
    qdii_blocked: bool,
    risk_veto: bool,
    news_veto: bool,
    sentiment_veto: bool,
) -> dict[str, Any]:
    """White-box 0-100 score used by the action layer.

    The score ranks opportunity quality.  It cannot bypass hard gates.  Missing
    BIAS or compact metric snapshots lower data quality instead of being guessed.
    """

    r20 = number(metrics_row.get("r20"))
    r60 = number(metrics_row.get("r60"))
    r120 = number(metrics_row.get("r120"))
    r250 = number(metrics_row.get("r250"))
    accel = number(metrics_row.get("rotation_acceleration_1m_vs_3m"))
    trend = trend_ok(metrics_row)
    price_score = (
        score_from_pct(r20, -10, 20) * 0.28
        + score_from_pct(r60, -20, 55) * 0.24
        + score_from_pct(r120, -30, 90) * 0.14
        + score_from_pct(r250, -40, 180) * 0.08
        + score_from_pct(accel, -15, 15) * 0.16
        + (75.0 if trend else 35.0) * 0.10
    )
    if direction_score is not None:
        price_score = price_score * 0.72 + direction_score * 0.28

    reversion, reversion_note = bias_score(metrics_row, mode)

    drawdown = abs(number(fund.get("max_drawdown_pct"), number(metrics_row.get("max_drawdown_pct"), 25.0)) or 25.0)
    volatility = number(fund.get("volatility_pct"), number(metrics_row.get("annualized_volatility_pct"), 25.0))
    risk_score = (
        score_from_pct(drawdown, 35, 5) * 0.58
        + score_from_pct(volatility, 45, 10) * 0.42
    )

    change = realtime_value(fund)
    freshness = realtime_freshness(fund)
    execution_score = 50.0
    execution_note = "实时/夜盘未形成明显执行修正"
    if freshness == "stale":
        execution_score, execution_note = 20.0, "实时/夜盘过期，不能执行新增"
    elif change is None:
        execution_score, execution_note = 42.0, "缺少实时/夜盘涨跌，执行层降级"
    elif change >= CHASE_RISK_PCT and mode != "BULL":
        execution_score, execution_note = 35.0, "震荡/弱市实时涨幅偏大，追涨风险高"
    elif change >= CHASE_RISK_PCT and trend:
        execution_score, execution_note = 58.0, "实时涨幅偏大但趋势仍在，只能降档"
    elif change <= BREAKDOWN_RISK_PCT and (flow_latest_negative or not trend):
        execution_score, execution_note = 28.0, "实时跌幅较大且趋势/资金转弱，破位风险上升"
    elif change <= PULLBACK_ENTRY_PCT and trend:
        execution_score, execution_note = 72.0, "趋势未坏且实时回落，执行窗口较好"
    elif -1.5 < change < 2:
        execution_score, execution_note = 60.0, "实时涨跌温和，执行层中性偏可用"

    ctx, ctx_notes = context_score(news_factor, sentiment_factor, {})
    if flow_three_positive:
        ctx = min(100.0, ctx + 6.0)
    if flow_latest_negative:
        ctx = max(0.0, ctx - 6.0)

    liquidity_score = 80.0 if purchasable else 0.0
    fees = fund.get("fees") if isinstance(fund.get("fees"), dict) else {}
    limit = number(fees.get("daily_purchase_limit"))
    if limit is not None and limit <= 100:
        liquidity_score = min(liquidity_score, 45.0)
    elif limit is not None and limit <= 500:
        liquidity_score = min(liquidity_score, 60.0)

    data_score = 100.0 if history_ok else 25.0
    data_notes = []
    if number(metrics_row.get("bias20")) is None:
        data_score = min(data_score, 70.0)
        data_notes.append("缺少 BIAS20，通常表示未传完整净值序列")
    if qdii_blocked:
        data_score = min(data_score, 45.0)
        data_notes.append("QDII 夜盘缺失或过期")

    total = (
        price_score * 0.30
        + reversion * 0.15
        + risk_score * 0.15
        + execution_score * 0.15
        + ctx * 0.15
        + liquidity_score * 0.05
        + data_score * 0.05
    )
    hard_penalties = []
    if risk_veto:
        hard_penalties.append("Serenity 风险否决")
    if news_veto:
        hard_penalties.append("消息重大反证")
    if sentiment_veto:
        hard_penalties.append("情绪重大风险")
    if hard_penalties:
        total = min(total, 35.0)

    return {
        "total": round(max(0.0, min(100.0, total)), 2),
        "price": round(price_score, 2),
        "reversion": round(reversion, 2),
        "risk": round(risk_score, 2),
        "execution": round(execution_score, 2),
        "evidence": round(ctx, 2),
        "liquidity": round(liquidity_score, 2),
        "data": round(data_score, 2),
        "notes": [reversion_note, execution_note, *ctx_notes, *data_notes, *hard_penalties],
    }


def realtime_value(fund: dict[str, Any]) -> float | None:
    realtime = fund.get("realtime") if isinstance(fund.get("realtime"), dict) else {}
    if is_qdii(fund):
        # QDII 今日申赎执行层只能看 get_night_estimate 的夜盘估算。
        # get_item_estimate 可解释官方/估算归属收益，但不能替代夜盘作为买卖时点。
        return number(realtime.get("qdii_night_estimated_change_pct"))
    qdii_change = number(realtime.get("qdii_night_estimated_change_pct"))
    if qdii_change is not None:
        return qdii_change
    return number(realtime.get("estimate_change_pct"))


def realtime_freshness(fund: dict[str, Any]) -> str:
    realtime = fund.get("realtime") if isinstance(fund.get("realtime"), dict) else {}
    freshness = str(realtime.get("estimate_freshness") or "").lower()
    qdii_status = str(realtime.get("qdii_night_status") or fund.get("night_status") or "").lower()
    if is_qdii(fund):
        qdii_freshness = str(realtime.get("qdii_night_freshness") or realtime.get("night_freshness") or "").lower()
        if qdii_status != "ready":
            return "stale"
        if number(realtime.get("qdii_night_estimated_change_pct")) is None:
            return "stale"
        if qdii_freshness in {"stale", "expired"}:
            return "stale"
        if qdii_freshness == "fresh":
            return "fresh"
        return "unknown"
    if qdii_status and qdii_status != "ready":
        return "stale"
    if qdii_status == "ready" and number(realtime.get("qdii_night_estimated_change_pct")) is None:
        return "stale"
    return freshness if freshness in {"fresh", "stale", "unknown"} else "unknown"


def realtime_execution_layer(
    fund: dict[str, Any],
    metrics_row: dict[str, Any],
    mode: str,
    signal: str,
    add_signal: bool,
    flow_latest_negative: bool,
    news_factor: dict[str, Any],
    sentiment_factor: dict[str, Any],
) -> dict[str, Any]:
    """Execution filter for intraday estimate / QDII night moves.

    It never creates ADD or REDUCE by itself.  It only changes timing and size
    for an already price-derived signal, so the historical factor model remains
    auditable while avoiding naive chase/sell rules.
    """

    change = realtime_value(fund)
    freshness = realtime_freshness(fund)
    trend_is_ok = trend_ok(metrics_row)
    sentiment_status = str(sentiment_factor.get("status") or "").lower()
    news_status = str(news_factor.get("status") or "").lower()
    positive_context = news_status == "supportive" or sentiment_status == "risk_on"
    negative_context = (
        news_status == "negative"
        or sentiment_status in {"risk_off", "crowded"}
        or flow_latest_negative
        or bool(metrics_row.get("cross_down"))
    )

    result = {
        "is_qdii": is_qdii(fund),
        "change_pct": change,
        "estimate_change_pct": number((fund.get("realtime") if isinstance(fund.get("realtime"), dict) else {}).get("estimate_change_pct")),
        "qdii_night_change_pct": number((fund.get("realtime") if isinstance(fund.get("realtime"), dict) else {}).get("qdii_night_estimated_change_pct")),
        "qdii_night_freshness": str((fund.get("realtime") if isinstance(fund.get("realtime"), dict) else {}).get("qdii_night_freshness") or freshness),
        "freshness": freshness,
        "state": "no_realtime_data" if change is None else "neutral",
        "modifier": "none",
        "size_multiplier": 1.0,
        "note": "无有效实时估值/夜盘数据，按历史价格因子处理" if change is None else "盘中/夜盘未改变结论",
    }

    if change is None:
        return result
    if freshness == "stale":
        result.update({
            "state": "stale",
            "modifier": "block_add" if add_signal else "none",
            "size_multiplier": 0.0 if add_signal else 1.0,
            "note": "实时估值/夜盘数据过期或缺少关键字段，不能增强买入",
        })
        return result

    if add_signal and change >= CHASE_RISK_PCT:
        if mode == "BULL" and trend_is_ok and positive_context:
            result.update({
                "state": "trend_follow_confirmed",
                "modifier": "reduce_size",
                "size_multiplier": 0.5 if change < STRONG_TREND_FOLLOW_PCT else 0.35,
                "note": "实时涨幅较大但趋势和证据确认，保留趋势追随并降低金额",
            })
        else:
            result.update({
                "state": "chase_risk",
                "modifier": "wait_pullback",
                "size_multiplier": 0.0,
                "note": "实时涨幅较大且缺少趋势确认，等待回落避免追涨",
            })
    elif add_signal and change <= PULLBACK_ENTRY_PCT:
        if trend_is_ok and not negative_context:
            result.update({
                "state": "pullback_entry",
                "modifier": "allow",
                "size_multiplier": 1.0,
                "note": "实时回落但中期趋势未破坏，可视为回落执行窗口",
            })
        elif negative_context and change <= BREAKDOWN_RISK_PCT:
            result.update({
                "state": "breakdown_risk",
                "modifier": "block_add",
                "size_multiplier": 0.0,
                "note": "实时跌幅较大且伴随破位/负面证据，暂停新增",
            })
    elif signal in {"REDUCE_REVIEW", "ROTATE_REVIEW"} and change <= BREAKDOWN_RISK_PCT and negative_context:
        result.update({
            "state": "breakdown_risk",
            "modifier": "reduce_review",
            "size_multiplier": 1.0,
            "note": "实时跌幅较大且负面证据增强，今天不加仓；若已有明确替代方向再考虑调出",
        })
    elif signal in {"REDUCE_REVIEW", "ROTATE_REVIEW"} and change >= CHASE_RISK_PCT and trend_is_ok:
        result.update({
            "state": "trend_repair",
            "modifier": "reduce_size",
            "size_multiplier": 0.5,
            "note": "实时转强且趋势未坏，降低减仓紧迫度",
        })

    return result


def is_qdii(fund: dict[str, Any]) -> bool:
    realtime = fund.get("realtime") if isinstance(fund.get("realtime"), dict) else {}
    return (
        number(realtime.get("qdii_night_estimated_change_pct")) is not None
        or str(realtime.get("qdii_night_status") or fund.get("night_status") or "").lower() == "ready"
        or "qdii" in str(fund.get("type") or fund.get("fund_type") or fund.get("name") or "").lower()
    )


def qdii_night_ready(fund: dict[str, Any]) -> bool:
    if not is_qdii(fund):
        return True
    realtime = fund.get("realtime") if isinstance(fund.get("realtime"), dict) else {}
    status = str(realtime.get("qdii_night_status") or fund.get("night_status") or "").lower()
    freshness = str(realtime.get("qdii_night_freshness") or realtime.get("night_freshness") or "").lower()
    if status != "ready":
        return False
    if number(realtime.get("qdii_night_estimated_change_pct")) is None:
        return False
    if freshness in {"stale", "expired"}:
        return False
    return True


def today_action(
    fund: dict[str, Any],
    signal: str,
    amount: float,
    blockers: list[str],
    realtime_execution: dict[str, Any],
    metrics_row: dict[str, Any],
) -> tuple[str, str]:
    """Translate deterministic signal + execution filter into user-facing action."""

    change = number(realtime_execution.get("change_pct"))
    modifier = str(realtime_execution.get("modifier") or "")
    state = str(realtime_execution.get("state") or "")
    holding_return = number(fund.get("holding_return_pct"))
    trend_bad = bool(metrics_row.get("cross_down")) or not trend_ok(metrics_row)
    qdii = is_qdii(fund)
    hard_add_blocked = bool(set(blockers) & {
        "portfolio_drawdown_above_limit",
        "portfolio_execution_drawdown_above_limit",
        "context_not_ready_for_analysis",
        "context_not_ready_for_action",
        "incremental_cash_unavailable",
        "fund_history_below_60",
        "fund_bias20_unavailable",
        "fund_not_purchasable",
        "qdii_night_data_not_ready",
        "news_factor_veto",
        "sentiment_factor_veto",
        "serenity_risk_veto",
    })

    if signal == "FORCED_REVIEW":
        return "不动", "单只持有收益触发风险线，但系统没有自动止损权限；今天不自动卖出，也不新增。"
    if signal in {"REDUCE_REVIEW", "ROTATE_REVIEW"}:
        if modifier == "reduce_size":
            return "暂不卖出", f"{realtime_execution.get('note') or '实时修复降低卖出必要'}。"
        if signal == "ROTATE_REVIEW":
            return "不动", "当前方向相对弱，但没有生成明确可替代方向和交易金额；今天不卖、不换、不新增。"
        return "不动", "价格或风险因子转弱，但没有形成可执行卖出方案；今天不自动卖出，也不新增。"
    if signal == "ADD" and amount > 0:
        if modifier == "reduce_size":
            return "可小额新增", f"{realtime_execution.get('note') or '信号有效但执行层降档'}，按小额方式处理。"
        return "可小额新增", "价格信号、数据质量和风控门禁通过；仍需用户确认后才可提交交易。"
    if signal == "CONDITIONAL_ADD" or hard_add_blocked:
        if qdii and change is not None and change >= 2:
            return "不追涨", "QDII 夜盘涨幅较大且存在风控/数据门禁，今天不追加。"
        return "不新增", "存在组合回撤、资金、数据或申购门禁，今天不给可执行新增金额。"
    if qdii and change is not None:
        if change <= -3 and (trend_bad or holding_return is not None and holding_return < -10):
            return "不动", "QDII 夜盘明显转弱且风险偏高，但系统没有形成可执行卖出方案；今天不自动卖出，也不新增。"
        if holding_return is not None and holding_return < -10 and change > 0:
            return "暂不卖出", "QDII 夜盘修复降低今天卖出必要；若后续转弱或亏损扩大，再由新报告给出明确动作。"
        if change >= 2:
            return "不追涨", "QDII 夜盘强修复，但没有新增门禁通过或已有在途/仓位约束，今天不追。"
        return "继续持有", "QDII 夜盘未给出明确加减仓触发，维持持有并等待官方净值确认。"
    if state == "chase_risk":
        return "不追涨", "盘中涨幅较大且缺少趋势确认，等待回落。"
    if state == "breakdown_risk":
        return "不动", "盘中跌幅较大且伴随破位或负面证据，但没有形成可执行卖出方案；今天不自动卖出。"
    return "继续持有", "没有满足新增、卖出或轮动的确定性条件。"


def trade_action(
    fund: dict[str, Any],
    signal: str,
    amount: float,
    blockers: list[str],
    realtime_execution: dict[str, Any],
    metrics_row: dict[str, Any],
    base_action: str,
    base_reason: str,
) -> dict[str, Any]:
    """Build the user-facing trading action object.

    Internal signals may be ADD / REDUCE_REVIEW / ROTATE_REVIEW, but the final
    report should express a concrete trading decision: buy, wait, hold, reduce,
    rotate, or no-trade.  "Review" is not a user action.
    """

    modifier = str(realtime_execution.get("modifier") or "")
    state = str(realtime_execution.get("state") or "")
    qdii = is_qdii(fund)
    blocker_set = set(blockers)
    data_blocked = bool(blocker_set & {
        "fund_history_below_60",
        "fund_bias20_unavailable",
        "portfolio_drawdown_unknown",
        "market_mode_unknown",
        "total_market_value_invalid",
        "qdii_night_data_not_ready",
        "context_not_ready_for_analysis",
        "context_not_ready_for_action",
    })
    risk_blocked = bool(blocker_set & {
        "portfolio_drawdown_above_limit",
        "portfolio_execution_drawdown_above_limit",
        "news_factor_veto",
        "sentiment_factor_veto",
        "serenity_risk_veto",
    })
    cash_blocked = "incremental_cash_unavailable" in blocker_set
    purchase_blocked = "fund_not_purchasable" in blocker_set
    trade_window_blocked = bool(blocker_set & {"trade_window_closed", "non_trading_day"})
    buy_amount = 0.0
    sell_amount = 0.0
    category = "hold"
    code = "HOLD_STAY"
    label = "持仓不动"
    instruction = "今天不买、不卖、不换。"

    if trade_window_blocked:
        category = "blocked"
        code = "REPLAY_ONLY"
        label = "只复盘"
        if "non_trading_day" in blocker_set:
            instruction = "当前不是交易日，今天不提交买入或卖出；下一交易日重新确认。"
        else:
            instruction = "交易窗口已关闭，今天不提交买入或卖出；下一交易日重新确认。"
    elif signal == "ADD":
        if amount > 0:
            buy_amount = amount
            category = "buy"
            if modifier == "reduce_size":
                code = "BUY_SMALL_REDUCED"
                label = "小额新增"
                instruction = f"可新增 {amount:.0f} 元，因执行层偏热已降档；需要你确认后才提交。"
            else:
                code = "BUY_SMALL"
                label = "小额新增"
                instruction = f"可新增 {amount:.0f} 元；需要你确认后才提交。"
        elif state == "chase_risk" or modifier == "wait_pullback":
            category = "wait"
            code = "BUY_WAIT_PULLBACK"
            label = "回落再买"
            instruction = "价格信号存在，但盘中/夜盘偏热；今天不买，等回落后再确认。"
        else:
            category = "blocked"
            code = "BUY_BLOCKED"
            label = "禁止新增"
            instruction = "买入信号未通过执行或风控门禁，今天不买。"
    elif signal == "CONDITIONAL_ADD":
        category = "blocked"
        buy_amount = 0.0
        if state == "chase_risk" or modifier == "wait_pullback":
            code = "BUY_WAIT_PULLBACK"
            label = "回落再买"
            instruction = "价格信号被追涨风险压制，今天不买，等回落后再确认。"
        elif qdii and number(realtime_execution.get("change_pct")) is not None and number(realtime_execution.get("change_pct")) >= 2:
            code = "NO_CHASE"
            label = "不追涨"
            instruction = "QDII 夜盘或实时涨幅偏高，今天不追加。"
        else:
            code = "BUY_BLOCKED"
            label = "禁止新增"
            instruction = "新增被组合回撤、资金、数据或申购门禁阻断，今天不买。"
    elif signal == "REDUCE_REVIEW":
        if amount > 0 and not data_blocked:
            sell_amount = amount
            category = "sell"
            code = "REDUCE_EXPOSURE"
            label = "降低暴露"
            instruction = f"可调出约 {amount:.0f} 元；需要你确认后才提交。"
        elif amount > 0:
            category = "hold"
            code = "REDUCE_WAIT_DATA"
            label = "暂不调出"
            instruction = "风险信号存在，但数据门禁不完整；今天不卖，等完整净值后再确认。"
        else:
            category = "hold"
            code = "HOLD_RISK"
            label = "持仓不动"
            instruction = "风险信号存在，但没有形成可执行卖出金额；今天不卖、不新增。"
    elif signal == "ROTATE_REVIEW":
        if amount > 0 and not data_blocked and not risk_blocked:
            sell_amount = amount
            category = "rotate"
            code = "ROTATE_OUT"
            label = "换出到强势方向"
            instruction = f"可从弱势方向调出约 {amount:.0f} 元；只有存在明确迁入方向时才执行。"
        elif amount > 0:
            category = "hold"
            code = "ROTATE_WAIT_DATA"
            label = "暂不调出"
            instruction = "方向偏弱，但数据或风控门禁不完整；今天不卖、不换。"
        else:
            category = "hold"
            code = "HOLD_WEAK_DIRECTION"
            label = "持仓不动"
            instruction = "方向偏弱，但没有生成明确替代方向和交易金额；今天不卖、不换、不新增。"
    elif signal == "FORCED_REVIEW":
        category = "blocked"
        code = "RISK_NO_AUTO_SELL"
        label = "只复盘"
        instruction = "触发风险线，但系统不自动止损；今天不自动卖出，也不新增。"
    elif base_action == "不追涨":
        category = "wait"
        code = "NO_CHASE"
        label = "不追涨"
        instruction = "盘中/夜盘偏热且没有新增门禁通过，今天不买。"
    elif base_action == "暂不卖出":
        category = "hold"
        code = "HOLD_NO_SELL"
        label = "暂不卖出"
        instruction = "短线修复降低卖出必要；今天不卖。"
    elif base_action == "只复盘" or data_blocked:
        category = "blocked"
        code = "REPLAY_ONLY"
        label = "只复盘"
        instruction = "关键数据不完整，今天不输出可执行交易。"
    elif cash_blocked or purchase_blocked or risk_blocked:
        category = "blocked"
        code = "BUY_BLOCKED"
        label = "禁止新增"
        instruction = "资金、申购或风控门禁未通过，今天不买。"
    else:
        category = "hold"
        code = "HOLD_STAY"
        label = "继续持有"
        instruction = "没有满足买入、卖出或轮动的确定性条件；今天持有不动。"

    reasons = [str(item).strip() for item in [base_reason] if str(item or "").strip()]
    blocker_labels = {
        "market_mode_unknown": "市场状态不可判断",
        "portfolio_drawdown_unknown": "组合回撤不可计算",
        "portfolio_drawdown_above_limit": "组合回撤超过风控线",
        "portfolio_execution_drawdown_above_limit": "盘中执行回撤估算超过风控线",
        "incremental_cash_unavailable": "可用增量资金不足",
        "direction_mapping_incomplete": "方向映射不完整",
        "total_market_value_invalid": "组合市值无效",
        "fund_history_below_60": "净值历史不足",
        "fund_bias20_unavailable": "本轮缺逐日净值",
        "fund_not_purchasable": "当前不可申购",
        "qdii_night_data_not_ready": "QDII 夜盘未就绪",
        "news_factor_veto": "消息面重大反证",
        "sentiment_factor_veto": "情绪面重大风险",
        "serenity_risk_veto": "Serenity 风险否决",
        "trade_window_closed": "交易窗口已关闭",
        "non_trading_day": "非交易日",
        "context_not_ready_for_analysis": "聚合上下文不可分析",
        "context_not_ready_for_action": "聚合上下文不可执行",
    }
    if blockers:
        reasons.append("阻断项：" + "、".join(blocker_labels.get(item, item) for item in blockers))

    return {
        "code": code,
        "label": label,
        "category": category,
        "buy_amount": round(buy_amount, 2),
        "sell_amount": round(sell_amount, 2),
        "net_amount": round(buy_amount - sell_amount, 2),
        "instruction": instruction,
        "reason": "；".join(reasons),
    }


def trend_ok(metrics_row: dict[str, Any]) -> bool:
    ma20 = number(metrics_row.get("ma20"))
    ma60 = number(metrics_row.get("ma60"))
    current = number(metrics_row.get("current"))
    r20 = number(metrics_row.get("r20"))
    if ma20 is not None and ma60 is not None:
        return ma20 > ma60
    return bool(current is not None and ma20 is not None and current >= ma20 and (r20 is None or r20 > 0))


def factor_snapshot(
    fund: dict[str, Any],
    metrics_row: dict[str, Any],
    direction_score: float | None,
    direction_rank: int | None,
    flow_three_positive: bool,
    flow_latest_negative: bool,
    history_ok: bool,
    purchasable: bool,
    qdii_blocked: bool,
    risk_veto: bool,
    news_veto: bool,
    sentiment_veto: bool,
    realtime_execution: dict[str, Any],
    scorecard: dict[str, Any],
) -> dict[str, Any]:
    fees = fund.get("fees") if isinstance(fund.get("fees"), dict) else {}
    news_factor = fund.get("news_factor") if isinstance(fund.get("news_factor"), dict) else {}
    sentiment_factor = fund.get("sentiment_factor") if isinstance(fund.get("sentiment_factor"), dict) else {}
    return {
        "core": {
            "r20": number(metrics_row.get("r20")),
            "r60": number(metrics_row.get("r60")),
            "r120": number(metrics_row.get("r120")),
            "r250": number(metrics_row.get("r250")),
            "rotation_acceleration_1m_vs_3m": number(metrics_row.get("rotation_acceleration_1m_vs_3m")),
            "rotation_acceleration_3m_vs_6m": number(metrics_row.get("rotation_acceleration_3m_vs_6m")),
            "bias5": number(metrics_row.get("bias5")),
            "bias10": number(metrics_row.get("bias10")),
            "bias20": number(metrics_row.get("bias20")),
            "ma20": number(metrics_row.get("ma20")),
            "ma60": number(metrics_row.get("ma60")),
            "trend_above_ma60": (
                number(metrics_row.get("ma20")) is not None
                and number(metrics_row.get("ma60")) is not None
                and number(metrics_row.get("ma20")) > number(metrics_row.get("ma60"))
            ),
            "cross_down": bool(metrics_row.get("cross_down")),
            "momentum_score": direction_score,
            "momentum_rank": direction_rank,
        },
        "scorecard": scorecard,
        "risk": {
            "holding_return_pct": number(fund.get("holding_return_pct")),
            "purchasable": purchasable,
            "daily_purchase_limit": number(fees.get("daily_purchase_limit")),
            "confirm_days": number(fees.get("confirm_days")),
            "qdii_blocked": qdii_blocked,
            "serenity_risk_veto": risk_veto,
            "news_veto": news_veto,
            "sentiment_veto": sentiment_veto,
        },
        "news": {
            "status": str(news_factor.get("status") or "unknown").lower(),
            "strength": str(news_factor.get("strength") or "weak").lower(),
            "veto": news_veto,
            "sources": news_factor.get("sources") if isinstance(news_factor.get("sources"), list) else [],
            "note": news_factor.get("note") or "",
        },
        "sentiment": {
            "status": str(sentiment_factor.get("status") or "unknown").lower(),
            "strength": str(sentiment_factor.get("strength") or "weak").lower(),
            "veto": sentiment_veto,
            "note": sentiment_factor.get("note") or "",
        },
        "evidence": {
            "flow_three_positive": flow_three_positive,
            "flow_latest_negative": flow_latest_negative,
            "catalyst_status": str(fund.get("catalyst_status") or "none").lower(),
            "evidence_strength": str(fund.get("evidence_strength") or "weak").lower(),
            "eastmoney_checks": fund.get("eastmoney_checks") if isinstance(fund.get("eastmoney_checks"), dict) else {},
            "serenity_checks": fund.get("serenity_checks") if isinstance(fund.get("serenity_checks"), dict) else {},
        },
        "execution": realtime_execution,
        "data_quality": {
            "history_points": number(metrics_row.get("points"), 0),
            "history_ok": history_ok,
            "history_complete": bool(fund.get("history_complete")) if "history_complete" in fund else None,
            "coverage_start": fund.get("coverage_start"),
            "coverage_end": fund.get("coverage_end"),
            "history_source": fund.get("history_source") or "get_batch_fund_nav_history",
        },
    }


def action_amount(
    total: float,
    mode: str,
    signal_strength: float,
    available_cash: float | None,
    rule_cap: float | None,
    add: bool,
    holding_value: float,
    daily_purchase_limit: float | None = None,
    vol_regime: str | None = None,
    portfolio_drawdown: float | None = None,
) -> float:
    coefficient = MODE_COEFFICIENT.get(mode, 0.0)
    amount = min(total * coefficient * signal_strength, total * 0.08)
    if rule_cap is not None:
        amount = min(amount, rule_cap)
    if add:
        amount = min(amount, max(0.0, available_cash or 0.0))
        # Enforce daily purchase limit (限购)
        if daily_purchase_limit is not None and daily_purchase_limit > 0:
            amount = min(amount, daily_purchase_limit)
        # Volatility-adjusted position sizing
        if vol_regime is not None:
            amount = volatility_adjusted_position_size(amount, vol_regime, portfolio_drawdown)
    else:
        amount = min(amount, max(0.0, holding_value))
    return round(max(0.0, amount), 2)


def fund_daily_return_map(fund: dict[str, Any]) -> dict[str, float]:
    series = dated_series(fund.get("history"), ("nav", "close", "value", "unit_nav"))
    dates = sorted(series)
    returns: dict[str, float] = {}
    for index in range(1, len(dates)):
        prev = series.get(dates[index - 1])
        curr = series.get(dates[index])
        if prev and curr:
            returns[dates[index]] = curr / prev - 1.0
    return returns


def pearson_correlation(left: dict[str, float], right: dict[str, float]) -> float | None:
    common = sorted(set(left) & set(right))
    if len(common) < 20:
        return None
    xs = [left[date] for date in common]
    ys = [right[date] for date in common]
    x_avg = mean(xs)
    y_avg = mean(ys)
    x_var = sum((x - x_avg) ** 2 for x in xs)
    y_var = sum((y - y_avg) ** 2 for y in ys)
    if x_var <= 0 or y_var <= 0:
        return None
    cov = sum((x - x_avg) * (y - y_avg) for x, y in zip(xs, ys))
    return cov / math.sqrt(x_var * y_var)


def drawdown_response(drawdown_pct: float | None, limit_pct: float | None) -> dict[str, Any]:
    """Progressive portfolio-risk response before the hard drawdown line."""
    if drawdown_pct is None:
        return {
            "level": "unknown",
            "position_multiplier": 0.0,
            "action": "组合回撤不可计算，禁止新增",
            "usage_pct": None,
        }
    dd = abs(drawdown_pct)
    if limit_pct and limit_pct > 0:
        usage = dd / limit_pct
        if usage >= 1.0:
            level, multiplier, action = "breached", 0.0, "已触发回撤门禁，停止新增"
        elif usage >= 0.8:
            level, multiplier, action = "critical", 0.2, "接近回撤门禁，只允许极小仓位或停止新增"
        elif usage >= 0.67:
            level, multiplier, action = "defensive", 0.4, "回撤压力偏高，新增大幅降档"
        elif usage >= 0.53:
            level, multiplier, action = "cautious", 0.6, "回撤进入谨慎区，新增降档"
        elif usage >= 0.33:
            level, multiplier, action = "watch", 0.8, "回撤进入观察区，控制新增节奏"
        else:
            level, multiplier, action = "normal", 1.0, "回撤压力正常"
        return {
            "level": level,
            "position_multiplier": multiplier,
            "action": action,
            "usage_pct": round(usage * 100.0, 2),
        }

    if dd >= 12:
        level, multiplier, action = "defensive", 0.4, "未设置硬阈值，但回撤已高，新增大幅降档"
    elif dd >= 10:
        level, multiplier, action = "cautious", 0.6, "未设置硬阈值，按绝对回撤进入谨慎区"
    elif dd >= 5:
        level, multiplier, action = "watch", 0.8, "未设置硬阈值，按绝对回撤进入观察区"
    else:
        level, multiplier, action = "normal", 1.0, "回撤压力正常"
    return {
        "level": level,
        "position_multiplier": multiplier,
        "action": action,
        "usage_pct": None,
    }


def execution_change_pct(fund: dict[str, Any]) -> float | None:
    """Return the price move that should be used for execution-risk stress.

    Official portfolio drawdown is audited and must not mix intraday estimates.
    Execution risk is different: it answers whether today's estimated move has
    already pushed the portfolio into a defensive state.  For QDII, use the
    night estimate when available; the ordinary estimate is attribution/display,
    not the best same-day subscription/redemption anchor.
    """
    realtime = fund.get("realtime") if isinstance(fund.get("realtime"), dict) else {}
    is_qdii_flag = is_qdii(fund)
    if is_qdii_flag:
        night = number(realtime.get("qdii_night_estimated_change_pct"))
        return night
    return number(realtime.get("estimate_change_pct"))


def portfolio_execution_risk(
    funds: list[dict[str, Any]],
    total_market_value: float,
    official_current_drawdown_pct: float | None,
    official_max_drawdown_pct: float | None,
) -> dict[str, Any]:
    """Estimate drawdown for execution gating without changing official P&L.

    The result is intentionally labelled estimated.  It should be used to block
    new risk and trigger defensive posture, but never be reported as audited
    portfolio return or saved as official drawdown.
    """
    if total_market_value <= 0:
        return {
            "estimated_today_return_pct": None,
            "execution_drawdown_pct": None,
            "official_current_drawdown_pct": official_current_drawdown_pct,
            "official_max_drawdown_pct": official_max_drawdown_pct,
            "source": "unavailable:total_market_value_invalid",
            "used_funds": 0,
            "missing_funds": 0,
        }

    weighted_return = 0.0
    used = 0
    missing = 0
    for fund in funds:
        market_value = number(fund.get("market_value"), 0.0) or 0.0
        if market_value <= 0:
            continue
        change = execution_change_pct(fund)
        if change is None:
            missing += 1
            continue
        weighted_return += market_value / total_market_value * change
        used += 1

    if used == 0:
        return {
            "estimated_today_return_pct": None,
            "execution_drawdown_pct": None,
            "official_current_drawdown_pct": official_current_drawdown_pct,
            "official_max_drawdown_pct": official_max_drawdown_pct,
            "source": "unavailable:no_realtime_or_qdii_night",
            "used_funds": 0,
            "missing_funds": missing,
        }

    base_current = abs(official_current_drawdown_pct) if official_current_drawdown_pct is not None else (
        abs(official_max_drawdown_pct) if official_max_drawdown_pct is not None else None
    )
    if base_current is None:
        execution_dd = None
    else:
        # A negative estimated return deepens current drawdown; a positive move
        # can relieve current drawdown but cannot erase the historical max line.
        execution_dd = max(0.0, base_current - weighted_return)
        if official_max_drawdown_pct is not None:
            execution_dd = max(execution_dd, abs(official_max_drawdown_pct))

    return {
        "estimated_today_return_pct": round(weighted_return, 4),
        "execution_drawdown_pct": round(execution_dd, 4) if execution_dd is not None else None,
        "official_current_drawdown_pct": official_current_drawdown_pct,
        "official_max_drawdown_pct": official_max_drawdown_pct,
        "source": "weighted_realtime_estimate_qdii_night_for_execution_only",
        "used_funds": used,
        "missing_funds": missing,
    }


def portfolio_risk_exposure(funds: list[dict[str, Any]], total_market_value: float) -> dict[str, Any]:
    """Estimate direction risk contribution and correlation concentration.

    This is a diagnostic layer, not a trading engine. It helps the report answer
    whether many funds are really the same risk source.
    """
    rows: list[dict[str, Any]] = []
    returns_by_code: dict[str, dict[str, float]] = {}
    for fund in funds:
        code = str(fund.get("code") or "")
        weight_pct = (number(fund.get("market_value"), 0.0) or 0.0) / total_market_value * 100.0 if total_market_value else 0.0
        vol = number(fund.get("volatility_pct"), number(fund.get("metrics", {}).get("annualized_volatility_pct") if isinstance(fund.get("metrics"), dict) else None))
        direction = str(fund.get("direction") or "unknown")
        returns_by_code[code] = fund_daily_return_map(fund)
        rows.append({
            "code": code,
            "name": fund.get("name") or "",
            "direction": direction,
            "weight_pct": weight_pct,
            "volatility_pct": vol,
        })

    direction_bucket: dict[str, dict[str, Any]] = {}
    for row in rows:
        bucket = direction_bucket.setdefault(row["direction"], {
            "direction": row["direction"],
            "weight_pct": 0.0,
            "weighted_vol_sum": 0.0,
            "vol_weight": 0.0,
            "fund_count": 0,
            "codes": [],
        })
        weight = number(row.get("weight_pct"), 0.0) or 0.0
        vol = number(row.get("volatility_pct"))
        bucket["weight_pct"] += weight
        bucket["fund_count"] += 1
        bucket["codes"].append(row["code"])
        if vol is not None and weight > 0:
            bucket["weighted_vol_sum"] += vol * weight
            bucket["vol_weight"] += weight

    directions: list[dict[str, Any]] = []
    inverse_vol_sum = 0.0
    for bucket in direction_bucket.values():
        avg_vol = bucket["weighted_vol_sum"] / bucket["vol_weight"] if bucket["vol_weight"] else None
        bucket["avg_volatility_pct"] = avg_vol
        bucket["risk_contribution_score"] = (bucket["weight_pct"] * avg_vol / 100.0) if avg_vol is not None else None
        if avg_vol and avg_vol > 0:
            inverse_vol_sum += 1.0 / avg_vol
        directions.append(bucket)

    for bucket in directions:
        avg_vol = number(bucket.get("avg_volatility_pct"))
        if avg_vol and inverse_vol_sum > 0:
            target = (1.0 / avg_vol) / inverse_vol_sum * 100.0
            bucket["risk_parity_target_pct"] = round(target, 2)
            bucket["risk_parity_gap_pct"] = round((number(bucket.get("weight_pct"), 0.0) or 0.0) - target, 2)
        else:
            bucket["risk_parity_target_pct"] = None
            bucket["risk_parity_gap_pct"] = None
        bucket["weight_pct"] = round(number(bucket.get("weight_pct"), 0.0) or 0.0, 2)
        if bucket.get("avg_volatility_pct") is not None:
            bucket["avg_volatility_pct"] = round(number(bucket.get("avg_volatility_pct")) or 0.0, 2)
        if bucket.get("risk_contribution_score") is not None:
            bucket["risk_contribution_score"] = round(number(bucket.get("risk_contribution_score")) or 0.0, 2)
        bucket.pop("weighted_vol_sum", None)
        bucket.pop("vol_weight", None)

    high_corr_pairs: list[dict[str, Any]] = []
    for i, left in enumerate(rows):
        for right in rows[i + 1:]:
            corr = pearson_correlation(returns_by_code.get(left["code"], {}), returns_by_code.get(right["code"], {}))
            if corr is not None and corr >= 0.8:
                high_corr_pairs.append({
                    "left": left["code"],
                    "right": right["code"],
                    "corr": round(corr, 3),
                    "combined_weight_pct": round((number(left.get("weight_pct"), 0.0) or 0.0) + (number(right.get("weight_pct"), 0.0) or 0.0), 2),
                    "note": "高相关持仓，视为同一风险源的一部分",
                })
    high_corr_pairs.sort(key=lambda item: (-(number(item.get("combined_weight_pct"), 0.0) or 0.0), -(number(item.get("corr"), 0.0) or 0.0)))
    directions.sort(key=lambda item: -(number(item.get("risk_contribution_score"), 0.0) or 0.0))
    return {
        "directions": directions,
        "high_correlation_pairs": high_corr_pairs[:12],
        "method": "方向权重×年化波动估算风险贡献；基金净值日收益计算相关性；风险平价目标按1/波动率分配",
        "data_quality": {
            "funds_with_return_series": sum(1 for row in returns_by_code.values() if len(row) >= 20),
            "correlation_min_points": 20,
        },
    }


def score_from_pct(value: float | None, low: float, high: float, inverse: bool = False) -> float:
    if value is None:
        return 50.0
    if high == low:
        return 50.0
    raw = (value - low) / (high - low) * 100.0
    score = 100.0 - raw if inverse else raw
    return max(0.0, min(100.0, score))


def context_score(news_factor: dict[str, Any], sentiment_factor: dict[str, Any], serenity_checks: dict[str, Any]) -> tuple[float, list[str]]:
    notes: list[str] = []
    news = str(news_factor.get("status") or "unknown").lower()
    sentiment = str(sentiment_factor.get("status") or "unknown").lower()
    serenity_strength = str(serenity_checks.get("evidence_strength") or "weak").lower()
    score = 50.0
    score += {"supportive": 12, "neutral": 0, "negative": -20, "stale": -8, "unknown": 0}.get(news, 0)
    score += {"risk_on": 10, "neutral": 0, "risk_off": -8, "crowded": -18, "unknown": 0}.get(sentiment, 0)
    score += {"strong": 10, "medium": 5, "weak": 0}.get(serenity_strength, 0)
    if bool(news_factor.get("veto")):
        notes.append("消息面重大反证")
    if bool(sentiment_factor.get("veto")):
        notes.append("情绪面重大风险")
    if bool(serenity_checks.get("risk_veto")):
        notes.append("Serenity 风险否决")
    return max(0.0, min(100.0, score)), notes


def evaluate_direction_opportunities(
    payload: dict[str, Any],
    mode: str,
    global_blocks: list[str],
    direction_weights: dict[str, float],
) -> list[dict[str, Any]]:
    pool = payload.get("opportunity_pool") if isinstance(payload.get("opportunity_pool"), dict) else {}
    rows: list[dict[str, Any]] = []
    candidates = pool.get("directions") or []
    for raw in candidates:
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("name") or raw.get("direction") or "").strip()
        if not name:
            continue
        history = ordered_values(raw.get("history"), ("close", "value", "nav"))
        m = metrics(history)
        points = number(m.get("points"), 0) or 0
        news_factor = raw.get("news_factor") if isinstance(raw.get("news_factor"), dict) else {}
        sentiment_factor = raw.get("sentiment_factor") if isinstance(raw.get("sentiment_factor"), dict) else {}
        serenity_checks = raw.get("serenity_checks") if isinstance(raw.get("serenity_checks"), dict) else {}
        ctx, ctx_notes = context_score(news_factor, sentiment_factor, serenity_checks)
        r20 = number(m.get("r20"))
        r60 = number(m.get("r60"))
        r120 = number(m.get("r120"))
        acceleration = number(m.get("rotation_acceleration_1m_vs_3m"))
        trend = trend_ok(m)
        momentum = (
            score_from_pct(r20, -10, 10) * 0.38
            + score_from_pct(r60, -20, 25) * 0.32
            + score_from_pct(r120, -30, 40) * 0.12
            + score_from_pct(acceleration, -8, 8) * 0.08
            + (75.0 if trend else 35.0) * 0.10
        )
        valuation_pct = number(raw.get("valuation_percentile"))
        valuation = score_from_pct(valuation_pct, 85, 15, inverse=False) if valuation_pct is not None else 50.0
        flow_score = score_from_pct(number(raw.get("flow_5d_pct")), -5, 5)
        crowding = number(raw.get("crowding_percentile"))
        crowding_penalty = max(0.0, (crowding or 0.0) - 75.0) * 0.35
        current_weight = number(raw.get("current_weight_pct"), direction_weights.get(name, 0.0)) or 0.0
        concentration_penalty = 12.0 if current_weight >= 35 else 0.0
        score = (
            momentum * 0.42
            + valuation * 0.16
            + flow_score * 0.14
            + ctx * 0.20
            + score_from_pct(number(raw.get("max_drawdown_pct")), 35, 5, inverse=False) * 0.08
            - crowding_penalty
            - concentration_penalty
        )
        blockers = []
        if points < MIN_FUND_HISTORY_POINTS:
            blockers.append("opportunity_history_below_60")
        if any(item in global_blocks for item in ("market_mode_unknown", "total_market_value_invalid")):
            blockers.append("portfolio_data_gate")
        blockers.extend(ctx_notes)
        if str(raw.get("status") or "").lower() in {"avoid", "blocked"}:
            blockers.append("方向被外部证据标记为暂不纳入")
        if blockers:
            action = "AVOID"
            reason = "数据或证据门禁未通过"
        elif score >= 72 and mode in {"BULL", "RANGE"}:
            action = "PRIORITY_RESEARCH"
            reason = "趋势、估值、资金或证据综合评分较高，可进入优先研究"
        elif score >= 58:
            action = "WATCH"
            reason = "有一定相对优势，但等待价格或证据进一步确认"
        else:
            action = "AVOID"
            reason = "综合优势不足，暂不作为迁移方向"
        rows.append({
            "name": name,
            "asset_class": raw.get("asset_class") or "场外基金方向",
            "current_weight_pct": round(current_weight, 2),
            "score": round(max(0.0, min(100.0, score)), 2),
            "action": action,
            "reason": reason,
            "blockers": blockers,
            "factors": {
                "r20": r20,
                "r60": r60,
                "r120": r120,
                "rotation_acceleration_1m_vs_3m": acceleration,
                "trend_ok": trend,
                "valuation_percentile": valuation_pct,
                "flow_5d_pct": number(raw.get("flow_5d_pct")),
                "crowding_percentile": crowding,
                "context_score": round(ctx, 2),
                "history_points": points,
            },
            "evidence": {
                "news": news_factor,
                "sentiment": sentiment_factor,
                "serenity": serenity_checks,
            },
        })
    rows.sort(key=lambda item: (item["action"] != "PRIORITY_RESEARCH", -item["score"]))
    return rows


def evaluate_fund_candidates(
    payload: dict[str, Any],
    direction_opportunities: list[dict[str, Any]],
    global_blocks: list[str],
) -> list[dict[str, Any]]:
    # 自然语言全市场选基模块已停用。
    # 当前东财 skill 对“已知代码查数”可用，但不稳定承担全市场基金筛选；
    # 因此引擎不再生成系统候选基金池。用户点名基金应在报告层单独比较。
    return []
    pool = payload.get("opportunity_pool") if isinstance(payload.get("opportunity_pool"), dict) else {}
    direction_scores = {item["name"]: item["score"] for item in direction_opportunities}
    direction_actions = {item["name"]: item["action"] for item in direction_opportunities}
    rows: list[dict[str, Any]] = []
    for raw in pool.get("fund_candidates") or []:
        if not isinstance(raw, dict):
            continue
        code = str(raw.get("code") or "").strip()
        name = str(raw.get("name") or "").strip()
        direction = str(raw.get("direction") or "unknown").strip() or "unknown"
        candidate_source = str(raw.get("candidate_source") or "").strip().lower()
        if not code and not name:
            continue
        history = ordered_values(raw.get("history"), ("nav", "close", "value", "unit_nav"))
        m = metrics(history)
        points = number(m.get("points"), 0) or 0
        fees = raw.get("fees") if isinstance(raw.get("fees"), dict) else {}
        purchasable = fees.get("purchasable", raw.get("purchasable")) is not False
        news_factor = raw.get("news_factor") if isinstance(raw.get("news_factor"), dict) else {}
        sentiment_factor = raw.get("sentiment_factor") if isinstance(raw.get("sentiment_factor"), dict) else {}
        serenity_checks = raw.get("serenity_checks") if isinstance(raw.get("serenity_checks"), dict) else {}
        ctx, ctx_notes = context_score(news_factor, sentiment_factor, serenity_checks)
        momentum = (
            score_from_pct(number(m.get("r20")), -10, 10) * 0.30
            + score_from_pct(number(m.get("r60")), -20, 25) * 0.30
            + score_from_pct(number(m.get("r120")), -30, 40) * 0.20
            + (75.0 if trend_ok(m) else 35.0) * 0.20
        )
        drawdown_score = score_from_pct(abs(number(raw.get("max_drawdown_pct"), 25.0) or 25.0), 35, 5, inverse=False)
        volatility_score = score_from_pct(number(raw.get("volatility_pct"), 25.0), 35, 8, inverse=False)
        scale = number(raw.get("scale_billion"))
        scale_score = score_from_pct(scale, 1, 80) if scale is not None else 50.0
        age = number(raw.get("age_years"))
        age_score = score_from_pct(age, 0.5, 5) if age is not None else 50.0
        fee_score = score_from_pct(number(raw.get("fee_rate_pct")), 2.0, 0.1, inverse=False)
        overlap = number(raw.get("overlap_with_holdings_pct"))
        overlap_penalty = max(0.0, (overlap or 0.0) - 60.0) * 0.25
        direction_score = direction_scores.get(direction, 50.0)
        score = (
            direction_score * 0.22
            + momentum * 0.22
            + drawdown_score * 0.14
            + volatility_score * 0.10
            + scale_score * 0.08
            + age_score * 0.08
            + fee_score * 0.06
            + ctx * 0.10
            - overlap_penalty
        )
        blockers = []
        if candidate_source != "mx-finance-data":
            if candidate_source == "user_named":
                blockers.append("candidate_user_named_not_eastmoney_screened")
            else:
                blockers.append("candidate_source_not_eastmoney")
        if points < MIN_FUND_HISTORY_POINTS:
            blockers.append("fund_history_below_60")
        if not purchasable:
            blockers.append("fund_not_purchasable")
        if direction_actions.get(direction) == "AVOID":
            blockers.append("direction_not_approved")
        if any(item in global_blocks for item in ("market_mode_unknown", "portfolio_drawdown_unknown", "total_market_value_invalid")):
            blockers.append("portfolio_data_gate")
        blockers.extend(ctx_notes)
        if blockers:
            action = "AVOID"
            reason = "数据、方向或交易门禁未通过"
        elif score >= 72:
            action = "PRIORITY_RESEARCH"
            reason = "方向质量、基金质量和证据综合排名靠前，可作为优先研究候选"
        elif score >= 58:
            action = "BACKUP_RESEARCH"
            reason = "可作为候选跟踪，等待更好价格或证据确认"
        else:
            action = "AVOID"
            reason = "综合性价比不足，暂不纳入候选池"
        rows.append({
            "code": code,
            "name": name,
            "direction": direction,
            "fund_type": raw.get("fund_type") or raw.get("type") or "unknown",
            "candidate_source": candidate_source or "unknown",
            "score": round(max(0.0, min(100.0, score)), 2),
            "action": action,
            "reason": reason,
            "blockers": blockers,
            "factors": {
                "direction_score": round(direction_score, 2),
                "r20": number(m.get("r20")),
                "r60": number(m.get("r60")),
                "r120": number(m.get("r120")),
                "trend_ok": trend_ok(m),
                "max_drawdown_pct": number(raw.get("max_drawdown_pct")),
                "volatility_pct": number(raw.get("volatility_pct")),
                "scale_billion": scale,
                "age_years": age,
                "fee_rate_pct": number(raw.get("fee_rate_pct")),
                "overlap_with_holdings_pct": overlap,
                "context_score": round(ctx, 2),
                "history_points": points,
            },
        })
    rows.sort(key=lambda item: (item["action"] not in {"PRIORITY_RESEARCH", "BACKUP_RESEARCH"}, -item["score"]))
    return rows


def dca_plans_from_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Read user-configured scheduled investments from normalized input.

    定投是未来现金流计划，不属于 get_portfolio_nav_history 的组合净值涨幅。
    The engine must not invent it.  If the App/MCP does not pass plans, report
    that DCA policy is unavailable instead of guessing.
    """

    portfolio = payload.get("portfolio") if isinstance(payload.get("portfolio"), dict) else {}
    candidates = (
        portfolio.get("dca_plans"),
        portfolio.get("scheduled_investments"),
        payload.get("dca_plans"),
        payload.get("scheduled_investments"),
    )
    def frequency_text(value: Any) -> str:
        raw = str(value or "").strip()
        mapping = {
            "DAILY": "每日",
            "WEEKLY": "每周",
            "BIWEEKLY": "每两周",
            "MONTHLY": "每月",
            "EVERY_TRADING_DAY": "每个交易日",
        }
        return mapping.get(raw.upper(), raw)

    plans: list[dict[str, Any]] = []
    for candidate in candidates:
        if not isinstance(candidate, list):
            continue
        for raw in candidate:
            if isinstance(raw, dict):
                code = str(raw.get("code") or raw.get("fund_code") or "").strip()
                plans.append({
                    "code": code,
                    "name": raw.get("name") or raw.get("fund_name") or "",
                    "group_name": raw.get("group_name") or raw.get("account_group") or "",
                    "amount": number(raw.get("amount") or raw.get("scheduled_amount")),
                    "frequency": frequency_text(raw.get("frequency") or raw.get("cycle") or ""),
                    "next_date": raw.get("next_date") or raw.get("next_run_date") or "",
                    "status": raw.get("status") or raw.get("enabled") or "",
                    "source": raw.get("source") or "HuahuaDaily",
                })
        if plans:
            break

    # HuahuaDaily cloud sync stores per-fund scheduled investments as
    # funds[].autoInvestConfig.  Normalizers should prefer converting them to
    # portfolio.dca_plans, but the engine accepts the source field directly so
    # Hermes can stay robust while MCP/get_records evolves.
    for raw in payload.get("funds") or []:
        if not isinstance(raw, dict):
            continue
        cfg = raw.get("autoInvestConfig") or raw.get("auto_invest_config") or raw.get("auto_invest")
        if not isinstance(cfg, dict):
            continue
        enabled = cfg.get("enabled")
        status = "active" if enabled is True else "paused" if enabled is False else str(cfg.get("status") or "")
        code = str(raw.get("code") or cfg.get("code") or "").strip()
        if not code:
            continue
        plan_id = str(cfg.get("id") or "")
        if any(str(plan.get("id") or "") == plan_id and plan_id for plan in plans):
            continue
        plans.append({
            "id": plan_id,
            "code": code,
            "name": raw.get("name") or cfg.get("name") or "",
            "group_name": raw.get("group_name") or raw.get("groupName") or raw.get("groupId") or cfg.get("group_name") or "",
            "amount": number(cfg.get("amount") or cfg.get("scheduled_amount")),
            "frequency": frequency_text(cfg.get("frequency") or cfg.get("cycle") or ""),
            "next_date": cfg.get("next_date") or cfg.get("nextRunDate") or cfg.get("next_run_date") or "",
            "status": status,
            "source": "HuahuaDaily.autoInvestConfig",
            "time_mode": cfg.get("timeMode") or cfg.get("time_mode") or "",
            "fee_rate": number(cfg.get("feeRate") or cfg.get("fee_rate")),
        })
    return plans


def build_portfolio_advice(
    payload: dict[str, Any],
    funds: list[dict[str, Any]],
    direction_opportunities: list[dict[str, Any]],
    global_blocks: list[str],
    direction_weights: dict[str, float],
) -> dict[str, Any]:
    """Portfolio-manager layer above per-fund scores.

    It answers: which positions drag portfolio NAV growth, whether scheduled
    investments should keep flowing, and where new/discretionary money should
    or should not go.  It does not create trades outside the deterministic
    per-fund action model.
    """

    dca_plans = dca_plans_from_payload(payload)
    plan_by_code: dict[str, list[dict[str, Any]]] = {}
    for plan in dca_plans:
        if plan.get("code"):
            plan_by_code.setdefault(str(plan["code"]), []).append(plan)

    nav_return_note = (
        "组合净值涨幅来自 get_portfolio_nav_history 的单位净值口径，只衡量真实组合净值表现；"
        "它不是交易收益、不是定投收益，也不包含盘中估值或 QDII 夜盘。"
    )

    drag_funds: list[dict[str, Any]] = []
    direction_bucket: dict[str, dict[str, Any]] = {}
    for fund in funds:
        factors = fund.get("factors") if isinstance(fund.get("factors"), dict) else {}
        core = factors.get("core") if isinstance(factors.get("core"), dict) else {}
        scorecard = factors.get("scorecard") if isinstance(factors.get("scorecard"), dict) else fund.get("scorecard") if isinstance(fund.get("scorecard"), dict) else {}
        direction = str(fund.get("direction") or "unknown")
        weight = number(fund.get("weight_pct"), 0.0) or 0.0
        total_score = number(scorecard.get("total"), 50.0) or 50.0
        price_score = number(scorecard.get("price"), 50.0) or 50.0
        risk_score = number(scorecard.get("risk"), 50.0) or 50.0
        r20 = number(core.get("r20"))
        r60 = number(core.get("r60"))
        r120 = number(core.get("r120"))
        r250 = number(core.get("r250"))
        accel = number(core.get("rotation_acceleration_1m_vs_3m"))
        drawdown = number(fund.get("max_drawdown_pct"))
        volatility = number(fund.get("annualized_volatility_pct"))
        blockers = set(str(item) for item in fund.get("blockers") or [])

        bucket = direction_bucket.setdefault(direction, {
            "direction": direction,
            "weight_pct": 0.0,
            "weighted_score_sum": 0.0,
            "weak_weight_pct": 0.0,
            "drag_count": 0,
        })
        bucket["weight_pct"] += weight
        bucket["weighted_score_sum"] += total_score * weight
        if total_score < 50 or (r60 is not None and r60 < 0) or (r120 is not None and r120 < 0):
            bucket["weak_weight_pct"] += weight

        points = 0
        reasons: list[str] = []
        if weight >= 5:
            points += 1
            reasons.append(f"组合权重{round(weight, 2)}%，对组合净值有实际影响")
        if r120 is not None and r120 < 0:
            points += 2
            reasons.append(f"近6月为{round(r120, 2)}%，长期段拖累净值")
        if r250 is not None and r250 < 0:
            points += 2
            reasons.append(f"近1年为{round(r250, 2)}%，年度维度拖累净值")
        if r60 is not None and r60 < 0:
            points += 1
            reasons.append(f"近3月为{round(r60, 2)}%，轮动期偏弱")
        if accel is not None and accel < -2:
            points += 1
            reasons.append(f"轮动加速度{round(accel, 2)}%，近1月继续失速")
        if total_score < 45 or price_score < 40:
            points += 1
            reasons.append(f"综合分{round(total_score, 1)}、价格分{round(price_score, 0)}，价格因子偏弱")
        if drawdown is not None and abs(drawdown) >= 12:
            points += 1
            reasons.append(f"单基金回撤{round(abs(drawdown), 2)}%，风险拖累偏高")
        if volatility is not None and volatility >= 28:
            reasons.append(f"年化波动{round(volatility, 2)}%，持有体验不稳")
        if "fund_bias20_unavailable" in blockers or "fund_history_below_60" in blockers:
            reasons.append("本轮逐日净值/BIAS 不完整，不能把拖累判断升级为可执行调仓")

        if points >= 3:
            bucket["drag_count"] += 1
            if points >= 5:
                severity = "高"
                recommendation = "停止新增和定投流入；若完整净值与替代方向同时确认，再考虑调出。"
            elif points >= 4:
                severity = "中"
                recommendation = "不再追加；若该基金有定投，先暂停或转向更强方向。"
            else:
                severity = "低"
                recommendation = "暂不新增，等待完整净值后再确认。"
            drag_funds.append({
                "code": fund.get("code"),
                "name": fund.get("name"),
                "direction": direction,
                "weight_pct": round(weight, 2),
                "score": round(total_score, 1),
                "severity": severity,
                "reasons": reasons[:5],
                "recommendation": recommendation,
            })

    drag_funds.sort(key=lambda item: ({"高": 0, "中": 1, "低": 2}.get(str(item.get("severity")), 3), -(number(item.get("weight_pct"), 0.0) or 0.0)))

    direction_advice: list[dict[str, Any]] = []
    for direction, row in direction_bucket.items():
        weight = number(row.get("weight_pct"), 0.0) or 0.0
        avg_score = row["weighted_score_sum"] / weight if weight > 0 else None
        weak_weight = number(row.get("weak_weight_pct"), 0.0) or 0.0
        if direction == "unknown" or weight <= 0:
            continue
        if weight >= 25 and avg_score is not None and avg_score < 50:
            action = "降低新增暴露"
            reason = f"方向权重{round(weight, 2)}%，加权综合分{round(avg_score, 1)}，弱势权重{round(weak_weight, 2)}%。"
        elif weak_weight >= 8:
            action = "暂停额外新增"
            reason = f"方向内弱势持仓权重{round(weak_weight, 2)}%，先停止新增流入。"
        else:
            action = "维持配置"
            reason = f"方向权重{round(weight, 2)}%，暂未识别为组合层拖累。"
        direction_advice.append({
            "direction": direction,
            "weight_pct": round(weight, 2),
            "avg_score": round(avg_score, 1) if avg_score is not None else None,
            "action": action,
            "reason": reason,
        })
    direction_advice.sort(key=lambda item: (item["action"] == "维持配置", -(number(item.get("weight_pct"), 0.0) or 0.0)))

    dca_suggestions: list[dict[str, Any]] = []
    for fund in funds:
        plans = plan_by_code.get(str(fund.get("code") or ""), [])
        if not plans:
            continue
        trade = fund.get("trade_action") if isinstance(fund.get("trade_action"), dict) else {}
        label = str(trade.get("label") or fund.get("today_action") or "")
        drag = next((item for item in drag_funds if item.get("code") == fund.get("code")), None)
        active_plans = [plan for plan in plans if str(plan.get("status") or "").lower() not in {"paused", "false", "disabled", "停用", "暂停"}]
        if not active_plans:
            action = "已暂停定投"
            reason = "App 中该定投计划当前未启用，不产生未来自动流入。"
        elif drag:
            action = "暂停定投流入"
            reason = "该基金被组合层识别为净值拖累，定投不应继续自动流入。"
        elif label == "小额新增":
            action = "维持定投"
            reason = "价格、风控、执行和申购门禁通过，定投可作为新增执行方式之一。"
        elif label in {"回落再买", "不追涨"}:
            action = "定投顺延"
            reason = "价格或夜盘偏热，今天不追，用下一次完整数据决定是否恢复。"
        elif label in {"禁止新增", "只复盘"}:
            action = "暂停定投"
            reason = "新增被数据、组合回撤、资金或申购门禁阻断。"
        else:
            action = "维持原定投但不额外加码"
            reason = "未触发新增或调出；定投不作为额外追涨资金。"
        dca_suggestions.append({
            "code": fund.get("code"),
            "name": fund.get("name"),
            "plans": plans,
            "action": action,
            "reason": reason,
        })

    dca_policy = {
        "status": "provided" if dca_plans else "not_provided",
        "message": (
            "已按输入中的定投计划逐只给出处理。"
            if dca_plans
            else "本轮未发现定投计划，不能判断定投是否暂停、顺延或转向。"
        ),
        "plans_count": len(dca_plans),
        "suggestions": dca_suggestions,
    }

    improvement_actions: list[str] = []
    if "portfolio_drawdown_above_limit" in global_blocks:
        improvement_actions.append("组合回撤门禁优先：停止所有自由新增资金，定投也应降级为暂停或等待用户重新确认。")
    if drag_funds:
        top = "、".join(f"{item['code']} {item['name']}" for item in drag_funds[:3])
        improvement_actions.append(f"优先处理净值拖累持仓：{top}；先停止新增流入，再等待完整净值与替代方向确认。")
    else:
        improvement_actions.append("本轮未识别出高置信长期拖累基金；若缺逐日净值，只能维持组合层风险控制，不能强行调仓。")
    priority_directions = [item.get("name") for item in direction_opportunities if item.get("action") == "PRIORITY_RESEARCH"]
    if priority_directions:
        improvement_actions.append("新增资金只允许在通过门禁的优先方向中择机执行：" + "、".join(str(item) for item in priority_directions[:3]) + "。")
    else:
        improvement_actions.append("本轮没有通过门禁的迁入方向，存量轮动不执行。")
    if not dca_plans:
        improvement_actions.append("定投计划未接入前，报告只能管理自由新增资金；不能替你判断既有定投是否继续扣款。")

    return {
        "nav_return_note": nav_return_note,
        "drag_funds": drag_funds[:8],
        "direction_advice": direction_advice[:8],
        "dca": dca_policy,
        "improvement_actions": improvement_actions,
    }


def normalize_quant_strategy_context(payload: dict[str, Any]) -> dict[str, Any]:
    """Adapt HuahuaDaily get_quant_strategy_context() output to engine input.

    The MCP aggregation endpoint is now the preferred strategy input.  It
    already contains audited compact metrics, execution window, DCA, pending
    buys, QDII night execution data, portfolio G-day risk and audit metadata.
    This adapter keeps the deterministic engine compatible with the older
    hand-built schema while avoiding fragile LLM-side field stitching.
    """

    if str(payload.get("schemaVersion") or "") != "quant_strategy_context.v1":
        return payload

    portfolio = payload.get("portfolio") if isinstance(payload.get("portfolio"), dict) else {}
    risk = portfolio.get("risk") if isinstance(portfolio.get("risk"), dict) else {}
    market = payload.get("market") if isinstance(payload.get("market"), dict) else {}
    audit = payload.get("audit") if isinstance(payload.get("audit"), dict) else {}
    execution = payload.get("execution") if isinstance(payload.get("execution"), dict) else {}
    dca = payload.get("dca") if isinstance(payload.get("dca"), dict) else {}
    pending = payload.get("pendingTransactions") if isinstance(payload.get("pendingTransactions"), dict) else {}
    data_quality = payload.get("dataQuality") if isinstance(payload.get("dataQuality"), dict) else {}

    hs300 = market.get("hs300") if isinstance(market.get("hs300"), dict) else {}
    cross_quotes = market.get("crossMarketQuotes") if isinstance(market.get("crossMarketQuotes"), list) else []
    indices: dict[str, list[dict[str, Any]]] = {}
    for item in cross_quotes:
        if not isinstance(item, dict):
            continue
        code = str(item.get("code") or "").strip()
        if not code:
            continue
        indices.setdefault(code, []).append({
            "date": str(item.get("asOf") or payload.get("asOfDate") or ""),
            "value": item.get("value"),
            "change": item.get("changePct"),
        })

    funds: list[dict[str, Any]] = []
    for raw in portfolio.get("holdings") or []:
        if not isinstance(raw, dict):
            continue
        code = str(raw.get("code") or "")
        metrics_row = raw.get("metrics") if isinstance(raw.get("metrics"), dict) else {}
        realtime = raw.get("realtime") if isinstance(raw.get("realtime"), dict) else {}
        qdii_night = raw.get("qdiiNight") if isinstance(raw.get("qdiiNight"), dict) else {}
        constraints = raw.get("tradeConstraints") if isinstance(raw.get("tradeConstraints"), dict) else {}
        groups = raw.get("groups") if isinstance(raw.get("groups"), list) else []
        group_name = " / ".join(
            str(group.get("groupName") or group.get("groupId") or "")
            for group in groups
            if isinstance(group, dict) and (group.get("groupName") or group.get("groupId"))
        )
        purchasable_text = str(constraints.get("purchaseStatus") or "")
        daily_limit = constraints.get("dailyPurchaseLimit")
        if constraints.get("dailyPurchaseLimited") and daily_limit is None:
            daily_limit = 0

        funds.append({
            "code": code,
            "name": raw.get("name") or "",
            "group_name": group_name,
            "direction": raw.get("direction") or raw.get("directionHint") or "unknown",
            "type": raw.get("type") or raw.get("typeHint") or "",
            "market_value": raw.get("marketValue"),
            "holding_return_pct": raw.get("holdingReturnPct"),
            "inTransitAmount": raw.get("inTransitBuyAmount"),
            "history_source": metrics_row.get("source") or "get_quant_strategy_context",
            "history_complete": metrics_row.get("complete"),
            "coverage_start": metrics_row.get("coverageStart"),
            "coverage_end": metrics_row.get("coverageEnd"),
            "metric_overrides": {
                "points": metrics_row.get("navPoints"),
                "r20": metrics_row.get("r20Pct"),
                "r60": metrics_row.get("r60Pct"),
                "r120": metrics_row.get("r120Pct"),
                "r250": metrics_row.get("r250Pct"),
                "ma20": metrics_row.get("ma20"),
                "ma60": metrics_row.get("ma60"),
                "bias20": metrics_row.get("bias20Pct"),
                "max_drawdown_pct": metrics_row.get("maxDrawdownPct"),
                "annualized_volatility_pct": metrics_row.get("annualizedVolatilityPct"),
            },
            "realtime": {
                "estimate_change_pct": realtime.get("estimatedChangePct"),
                "estimate_as_of": realtime.get("estimateTime"),
                "estimate_source": realtime.get("source"),
                "estimate_freshness": realtime.get("freshness"),
                "estimate_nav_date": raw.get("officialNavDate"),
                "qdii_night_status": qdii_night.get("status"),
                "qdii_night_estimated_change_pct": qdii_night.get("changePct"),
                "qdii_night_quote_as_of": qdii_night.get("time"),
                "qdii_night_actual_session_date": qdii_night.get("sessionDate"),
                "qdii_night_freshness": qdii_night.get("freshness"),
                "qdii_night_coverage_pct": qdii_night.get("coveragePct"),
                "qdii_night_availability": qdii_night.get("availability") or qdii_night.get("available"),
                "qdii_night_reason": qdii_night.get("reason"),
                "qdii_night_fx": {"status": qdii_night.get("fxStatus")},
                "qdii_night_holdings": [],
            },
            "fees": {
                "purchasable": constraints.get("available") is not False and "暂停" not in purchasable_text,
                "daily_purchase_limit": daily_limit,
                "confirm_days": constraints.get("confirmDays") or raw.get("confirmDays"),
                "minimum_purchase_amount": constraints.get("minimumPurchaseAmount"),
            },
            "news_factor": {"status": "unknown", "strength": "weak", "veto": False, "sources": [], "note": "外部消息由东财 skill 补充，本 MCP 聚合上下文不包含"},
            "sentiment_factor": {"status": "unknown", "strength": "weak", "veto": False, "note": "外部情绪由东财 skill 补充，本 MCP 聚合上下文不包含"},
            "serenity_checks": {"evidence_strength": "unknown", "risk_veto": False, "summary": "Serenity 证据由 Agent 按需补充"},
            "catalyst_status": "none",
            "evidence_strength": "unknown",
            "risk_veto": False,
        })

    plans = []
    for plan in dca.get("plans") or []:
        if not isinstance(plan, dict):
            continue
        plans.append({
            "code": plan.get("code"),
            "name": plan.get("name"),
            "group_name": plan.get("groupId"),
            "amount": plan.get("amount"),
            "frequency": plan.get("cycle"),
            "next_date": plan.get("nextRunDate"),
            "status": "active",
            "planned_amount_next_30_days": plan.get("plannedAmountNext30Days"),
            "source": "get_quant_strategy_context.dca",
        })

    return {
        "as_of": payload.get("asOfDate"),
        "strategy": {"id": "hua-personal-strategy", "version": "quant-context-v1"},
        "timestamps": {
            "portfolio": audit.get("recordsDataUpdatedAt"),
            "portfolio_history": risk.get("dataAsOf") or audit.get("navCutoffDate"),
            "market": audit.get("marketDataAsOf"),
            "news": None,
            "run_at": execution.get("serverTime"),
        },
        "execution": {
            "run_at": execution.get("serverTime"),
            "market_timezone": "Asia/Shanghai",
            "trade_cutoff_time": str(execution.get("cutoffTime") or "15:00:00+08:00")[:5],
            "is_trading_day": execution.get("isTradingDay"),
            "next_trading_day": execution.get("nextTradingDay"),
            "source": "get_quant_strategy_context.execution",
        },
        "provenance": {
            "sync_updated_at": audit.get("recordsDataUpdatedAt"),
            "sync_etag": audit.get("portfolioEtag"),
            "records_data_updated_at": audit.get("recordsDataUpdatedAt"),
            "records_etag": audit.get("portfolioEtag"),
            "strategy_preferences_source": "get_quant_strategy_context.portfolio.risk.configuredMaxDrawdownLimitPct",
            "input_built_at": audit.get("contextBuiltAt"),
            "context_id": payload.get("contextId"),
            "context_hash": payload.get("contextHash"),
            "builder_version": audit.get("builderVersion"),
            "portfolio_methodology_version": audit.get("portfolioMethodologyVersion"),
        },
        "benchmark": {
            "code": "sh000300",
            "metric_overrides": {
                "points": hs300.get("validPoints"),
                "ma20": hs300.get("ma20"),
                "ma60": hs300.get("ma60"),
                "current": hs300.get("latestValue"),
            },
            "history": [],
        },
        "market": {
            "previous_mode": None,
            "indices": indices,
            "sector_flow": market.get("sectorFundFlow"),
            "regime_label_owner": market.get("regimeLabelOwner"),
        },
        "portfolio": {
            "total_market_value": portfolio.get("totalMarketValue"),
            "total_cost": portfolio.get("totalCost"),
            "holding_profit": portfolio.get("holdingProfit"),
            "holding_return_pct": portfolio.get("holdingReturnPct"),
            "portfolio_drawdown_pct": risk.get("maxDrawdownPct"),
            "current_drawdown_pct": risk.get("currentDrawdownPct"),
            "official_max_drawdown_pct": risk.get("maxDrawdownPct"),
            "official_current_drawdown_pct": risk.get("currentDrawdownPct"),
            "max_drawdown_limit_pct": risk.get("configuredMaxDrawdownLimitPct"),
            "portfolio_drawdown_source": risk.get("source") or "get_quant_strategy_context.portfolio.risk",
            "portfolio_nav_coverage_pct": risk.get("coveragePct"),
            "portfolio_nav_warnings": payload.get("warnings") or [],
            "cumulative_return_pct": risk.get("cumulativeReturnPct"),
            "annualized_volatility_pct": risk.get("annualizedVolatilityPct"),
            "benchmark_return_pct": risk.get("benchmarkReturnPct"),
            "relative_benchmark_return_pct": risk.get("relativeReturnPct"),
            "incremental_cash_available": None,
            "dca_plans": plans,
            "planned_inflow_next_30_days": dca.get("plannedInflowNext30Days"),
            "pending_buy_amount": pending.get("pendingBuyAmount"),
            "risk_exposure_overrides": portfolio.get("exposure"),
            "context_ready_for_analysis": payload.get("readyForAnalysis"),
            "context_ready_for_action": payload.get("readyForAction"),
            "context_blocking_reasons": payload.get("blockingReasons") or [],
        },
        "funds": funds,
        "opportunity_pool": {"directions": [], "fund_candidates": []},
        "data_quality": data_quality,
        "action_readiness": payload.get("actionReadiness"),
    }


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    payload = normalize_quant_strategy_context(payload)
    exec_window = execution_window(payload)
    benchmark_input = payload.get("benchmark") if isinstance(payload.get("benchmark"), dict) else {}
    benchmark_values = ordered_values(benchmark_input.get("history"), ("close", "value", "nav"))
    benchmark_metrics = metric_snapshot(metrics(benchmark_values), benchmark_input.get("metric_overrides"))
    market_input = payload.get("market") if isinstance(payload.get("market"), dict) else {}
    mode, gap, mode_rule = market_mode(benchmark_metrics, market_input.get("previous_mode"))

    portfolio = payload.get("portfolio") if isinstance(payload.get("portfolio"), dict) else {}
    total = number(portfolio.get("total_market_value"), 0.0) or 0.0
    exact_drawdown = number(portfolio.get("portfolio_drawdown_pct"))
    official_current_drawdown = number(portfolio.get("current_drawdown_pct"), number(portfolio.get("official_current_drawdown_pct")))
    official_max_drawdown = number(portfolio.get("official_max_drawdown_pct"), exact_drawdown)
    max_drawdown_limit = number(portfolio.get("max_drawdown_limit_pct"))
    exact_drawdown_source = str(portfolio.get("portfolio_drawdown_source") or "get_portfolio_nav_history")
    portfolio_nav_coverage = number(portfolio.get("portfolio_nav_coverage_pct"))
    portfolio_cumulative_return = number(portfolio.get("cumulative_return_pct"))
    portfolio_annualized_volatility = number(portfolio.get("annualized_volatility_pct"))
    portfolio_benchmark_return = number(portfolio.get("benchmark_return_pct"))
    portfolio_relative_return = number(portfolio.get("relative_benchmark_return_pct"))
    portfolio_nav_warnings = [
        str(item) for item in (portfolio.get("portfolio_nav_warnings") or []) if str(item).strip()
    ]
    available_cash = number(portfolio.get("incremental_cash_available"))
    cash_was_defaulted = available_cash is None
    if cash_was_defaulted:
        available_cash = DEFAULT_INCREMENTAL_CASH

    funds: list[dict[str, Any]] = []
    for raw in payload.get("funds") or []:
        if not isinstance(raw, dict):
            continue
        row = dict(raw)
        row["code"] = str(row.get("code") or "")
        row["direction"] = str(row.get("direction") or "unknown").strip() or "unknown"
        row["market_value"] = number(row.get("market_value"), 0.0) or 0.0
        computed_metrics = metrics(ordered_values(row.get("history"), ("nav", "close", "value", "unit_nav")))
        row["metrics"] = metric_snapshot(computed_metrics, row.get("metric_overrides"))
        funds.append(row)

    direction_scores = build_direction_scores(funds)
    direction_values: dict[str, float] = {}
    for fund in funds:
        direction_values[fund["direction"]] = direction_values.get(fund["direction"], 0.0) + fund["market_value"]
    direction_weights = {
        direction: (value / total * 100.0 if total else 0.0)
        for direction, value in direction_values.items()
    }
    risk_exposure = portfolio_risk_exposure(funds, total)
    execution_risk = portfolio_execution_risk(
        funds,
        total,
        official_current_drawdown,
        official_max_drawdown,
    )
    execution_drawdown = number(execution_risk.get("execution_drawdown_pct"))

    global_blocks: list[str] = []
    warnings: list[str] = []
    if exec_window.get("blocker"):
        global_blocks.append(str(exec_window["blocker"]))
    if execution_drawdown is not None:
        drawdown = abs(execution_drawdown)
        drawdown_source = "盘中执行回撤估算；真实收益仍以官方净值回撤为准"
        warnings.append("execution_drawdown_estimated:not_official_return")
    elif exact_drawdown is not None:
        drawdown = abs(exact_drawdown)
        drawdown_source = exact_drawdown_source
    else:
        drawdown = None
        drawdown_source = "unknown"
    warnings.extend(f"portfolio_nav_history:{item}" for item in portfolio_nav_warnings)
    if mode == "UNKNOWN":
        global_blocks.append("market_mode_unknown")
    if portfolio.get("context_ready_for_analysis") is False:
        global_blocks.append("context_not_ready_for_analysis")
    if portfolio.get("context_ready_for_action") is False:
        global_blocks.append("context_not_ready_for_action")
        for item in portfolio.get("context_blocking_reasons") or []:
            reason_text = str(item).strip()
            if reason_text:
                warnings.append(f"context_blocking_reason:{reason_text}")
    if drawdown is None:
        global_blocks.append("portfolio_drawdown_unknown")
    if max_drawdown_limit is None:
        warnings.append("max_drawdown_limit_unknown")
    elif max_drawdown_limit > 0 and drawdown is not None and drawdown > max_drawdown_limit:
        if execution_drawdown is not None:
            global_blocks.append("portfolio_execution_drawdown_above_limit")
        else:
            global_blocks.append("portfolio_drawdown_above_limit")
    drawdown_policy = drawdown_response(drawdown, max_drawdown_limit)
    if number(drawdown_policy.get("position_multiplier"), 1.0) == 0.0:
        global_blocks.append("drawdown_response_stop_add")
    elif number(drawdown_policy.get("position_multiplier"), 1.0) is not None and number(drawdown_policy.get("position_multiplier"), 1.0) < 1.0:
        warnings.append(f"drawdown_response:{drawdown_policy.get('level')}")
    
    # --- Adaptive frequency gate ---
    benchmark_history_for_gate = payload.get("benchmark", {}).get("history", []) if isinstance(payload.get("benchmark"), dict) else []
    # Build multi-index data from portfolio holdings
    # Map direction → index code for regime detection
    # Map direction → list of (index_code, weight_within_direction) for regime detection
    # QDII needs multiple global indices (NASDAQ, KOSPI, Hang Seng Tech)
    # A-share tech/semiconductor directions include global factors (NDX, KS11)
    # because A-share is deeply integrated into global semiconductor supply chain
    # Samsung/SK Hynix/NVIDIA/TSMC set the cycle, A-share follows 70-80% of the time
    portfolio_index_map = {
        "科创50": [("000688", 0.6), ("NDX", 0.2), ("KS11", 0.2)],   # 60% domestic + 20% NASDAQ + 20% KOSPI
        "半导体": [("512480", 0.5), ("NDX", 0.25), ("KS11", 0.25)], # 50% A-share + 25% NASDAQ + 25% KOSPI
        "海外科技": [("NDX", 0.4), ("HSTECH", 0.3), ("KS11", 0.3)], # 纳指40% + 恒生科技30% + 韩国30%
        "宽基": [("000300", 1.0)],
        "量化": [("000300", 0.6), ("000688", 0.4)],
    }
    
    # Extract index history from payload if available. Expected shapes:
    # payload.market.indices = {"NDX": [...], "KS11": [...]} or payload.indices.
    raw_indices = market_input.get("indices") if isinstance(market_input.get("indices"), dict) else payload.get("indices")
    portfolio_indices = raw_indices if isinstance(raw_indices, dict) else {}
    index_weights = {}
    
    # Use direction weights as proxy for index weights, split across sub-indices
    for direction, weight in direction_weights.items():
        index_list = portfolio_index_map.get(direction, [])
        if weight > 0 and index_list:
            dir_weight = weight / 100.0
            for idx_code, idx_share in index_list:
                index_weights[idx_code] = index_weights.get(idx_code, 0.0) + dir_weight * idx_share
    
    # Normalize weights to sum to 1.0
    total_weight = sum(index_weights.values())
    if total_weight > 0:
        index_weights = {k: v / total_weight for k, v in index_weights.items()}
    
    adaptive_gate = adaptive_frequency_gate(
        benchmark_history_for_gate,
        benchmark_metrics,
        drawdown,
        current_date=str(payload.get("as_of", "")),
        portfolio_indices=portfolio_indices if portfolio_indices else None,
        index_weights=index_weights if index_weights else None,
    )
    vol_regime = adaptive_gate.get("vol_regime", "NORMAL")
    trend_regime = adaptive_gate.get("trend_regime", "SIDEWAYS")
    adaptive_params = adaptive_gate.get("adaptive_params", {})
    if not adaptive_gate.get("should_trade", True):
        global_blocks.append("adaptive_frequency_gate_blocked")
    
    regime_info = {
        "vol_regime": vol_regime,
        "trend_regime": trend_regime,
        "annualized_vol": adaptive_gate.get("annualized_vol"),
        "should_trade": adaptive_gate.get("should_trade", True),
        "gate_reason": adaptive_gate.get("reason", ""),
        "adaptive_params": adaptive_params,
    }
    
    if available_cash is None or available_cash <= 0:
        global_blocks.append("incremental_cash_unavailable")
    if cash_was_defaulted:
        warnings.append("incremental_cash_defaulted_to_3000")
    if direction_weights.get("unknown", 0.0) > 10:
        global_blocks.append("direction_mapping_incomplete")
    if total <= 0:
        global_blocks.append("total_market_value_invalid")

    concentration_actions = []
    for direction, weight in direction_weights.items():
        if direction != "unknown" and weight > 45 and total > 0:
            concentration_actions.append({
                "direction": direction,
                "weight_pct": round(weight, 2),
                "target_pct": 35.0,
                "reduce_amount": round(max(0.0, direction_values[direction] - total * 0.35), 2),
                "rule": "RISK-DIRECTION-45",
            })

    benchmark_r10 = number(benchmark_metrics.get("r10"))
    ranked_count = sum(1 for row in direction_scores.values() if row.get("rank") is not None)
    results = []

    for fund in funds:
        m = fund["metrics"]
        direction_row = direction_scores.get(fund["direction"], {})
        rank = direction_row.get("rank")
        score = number(direction_row.get("score"))
        top_two = rank is not None and rank <= 2 and ranked_count >= 3
        bottom_two = rank is not None and rank > max(1, ranked_count - 2) and ranked_count >= 4
        flow_values = [number(value) for value in fund.get("flow_3d") or []]
        flow_values = [value for value in flow_values if value is not None]
        flow_three_positive = len(flow_values) >= 3 and all(value > 0 for value in flow_values[-3:])
        flow_latest_negative = bool(flow_values and flow_values[-1] < 0)
        catalyst = str(fund.get("catalyst_status") or "none").lower()
        risk_veto = bool(fund.get("risk_veto"))
        news_factor = fund.get("news_factor") if isinstance(fund.get("news_factor"), dict) else {}
        sentiment_factor = fund.get("sentiment_factor") if isinstance(fund.get("sentiment_factor"), dict) else {}
        news_veto = bool(news_factor.get("veto"))
        sentiment_veto = bool(sentiment_factor.get("veto"))
        fees = fund.get("fees") if isinstance(fund.get("fees"), dict) else {}
        purchasable = fees.get("purchasable") is not False
        daily_purchase_limit = number(fees.get("daily_purchase_limit"))
        history_ok = number(m.get("points"), 0) >= MIN_FUND_HISTORY_POINTS
        realtime = fund.get("realtime") if isinstance(fund.get("realtime"), dict) else {}
        qdii_blocked = is_qdii(fund) and not qdii_night_ready(fund)
        blockers = list(global_blocks)
        if not history_ok:
            blockers.append("fund_history_below_60")
        if not purchasable:
            blockers.append("fund_not_purchasable")
        if risk_veto:
            blockers.append("serenity_risk_veto")
        if news_veto:
            blockers.append("news_factor_veto")
        if sentiment_veto:
            blockers.append("sentiment_factor_veto")
        if qdii_blocked:
            blockers.append("qdii_night_data_not_ready")
        if number(m.get("bias20")) is None:
            blockers.append("fund_bias20_unavailable")

        scorecard = fund_multifactor_score(
            fund,
            m,
            mode,
            score,
            news_factor,
            sentiment_factor,
            flow_three_positive,
            flow_latest_negative,
            history_ok,
            purchasable,
            qdii_blocked,
            risk_veto,
            news_veto,
            sentiment_veto,
        )
        total_score = number(scorecard.get("total"), 50.0) or 50.0
        price_score = number(scorecard.get("price"), 50.0) or 50.0
        reversion_score = number(scorecard.get("reversion"), 50.0) or 50.0
        execution_score = number(scorecard.get("execution"), 50.0) or 50.0
        data_score = number(scorecard.get("data"), 50.0) or 50.0

        signal = "HOLD"
        rule = "DEFAULT-HOLD"
        reason = "未触发确定性规则"
        amount = 0.0
        signal_strength = 0.0
        add_signal = False

        holding_return = number(fund.get("holding_return_pct"))
        if holding_return is not None and holding_return < -15:
            signal, rule = "FORCED_REVIEW", "RISK-FUND-LOSS-15"
            reason = "单只基金持有收益率低于 -15%，强制检视但不自动止损"
        elif mode == "BULL" and history_ok:
            pullback = number(m.get("r5")) is not None and number(m.get("r5")) <= -3
            trend_up = trend_ok(m)
            positive_evidence = evidence_positive(flow_three_positive, news_factor, sentiment_factor)
            if pullback and trend_up and catalyst != "rejected":
                signal, rule, add_signal = "ADD", "BULL-PULLBACK", True
                reason = "5日回撤超过3%、基金趋势向上且无重大反证"
                signal_strength = signal_strength_with_context(
                    strength(True, top_two, positive_evidence),
                    news_factor,
                    sentiment_factor,
                    "contrarian",
                )
                amount = action_amount(total, mode, signal_strength, available_cash, 2000, True, fund["market_value"], daily_purchase_limit, vol_regime, drawdown)
            elif top_two and trend_up and positive_evidence and catalyst != "rejected":
                signal, rule, add_signal = "ADD", "BULL-CONFIRM", True
                reason = "方向动量前2、趋势向上且消息/情绪/资金流至少一项确认"
                signal_strength = signal_strength_with_context(strength(True, True, True), news_factor, sentiment_factor, "trend")
                amount = action_amount(total, mode, signal_strength, available_cash, 2000, True, fund["market_value"], daily_purchase_limit, vol_regime, drawdown)
            elif bottom_two and benchmark_r10 is not None and number(m.get("r10")) is not None and number(m.get("r10")) - benchmark_r10 < -3:
                signal, rule = "ROTATE_REVIEW", "BULL-RELATIVE-WEAK"
                reason = "方向动量后2且近10日跑输沪深300超过3个百分点"
                signal_strength = strength(True, False, not flow_latest_negative)
                amount = action_amount(total, mode, signal_strength, None, None, False, fund["market_value"])
        elif mode == "BEAR" and history_ok:
            if bool(m.get("cross_down")):
                signal, rule = "REDUCE_REVIEW", "BEAR-CROSS-DOWN"
                reason = "基金MA20确认下穿MA60"
                signal_strength = signal_strength_with_context(
                    strength(True, not bottom_two, not flow_latest_negative),
                    news_factor,
                    sentiment_factor,
                    "reduce",
                )
                amount = action_amount(total, mode, signal_strength, None, None, False, fund["market_value"])
            elif number(m.get("bias5")) is not None and number(m.get("bias5")) > 5 and flow_latest_negative:
                signal, rule = "REDUCE_REVIEW", "BEAR-REBOUND-REDUCE"
                reason = "BIAS5超过5%且最新资金流为负"
                signal_strength = signal_strength_with_context(
                    strength(True, not bottom_two, False),
                    news_factor,
                    sentiment_factor,
                    "reduce",
                )
                amount = action_amount(total, mode, signal_strength, None, None, False, fund["market_value"])
            elif (
                number(m.get("bias20")) is not None
                and number(m.get("bias20")) < -10
                and (flow_three_positive or str(sentiment_factor.get("status") or "").lower() == "risk_off")
                and catalyst != "rejected"
            ):
                signal, rule, add_signal = "ADD", "BEAR-PANIC-TEST", True
                reason = "BIAS20低于-10%且资金流转正或情绪进入恐慌，作为小额逆向测试"
                signal_strength = signal_strength_with_context(
                    strength(True, not bottom_two, True),
                    news_factor,
                    sentiment_factor,
                    "contrarian",
                )
                amount = action_amount(total, mode, signal_strength, available_cash, 1000, True, fund["market_value"], daily_purchase_limit, vol_regime, drawdown)
        elif mode == "RANGE" and history_ok:
            bias5 = number(m.get("bias5"))
            bias10 = number(m.get("bias10"))
            reversion_bias = (bias5 is not None and bias5 < 0) or (bias10 is not None and bias10 < -1)
            if reversion_bias and score is not None and score >= 50 and catalyst != "rejected":
                signal, rule, add_signal = "ADD", "RANGE-MEAN-REVERT", True
                reason = "BIAS5低于0或BIAS10低于-1%，且方向动量不低于中位数"
                signal_strength = signal_strength_with_context(
                    strength(True, score >= 70, evidence_positive(flow_three_positive, news_factor, sentiment_factor)),
                    news_factor,
                    sentiment_factor,
                    "contrarian",
                )
                amount = action_amount(total, mode, signal_strength, available_cash, 1500, True, fund["market_value"], daily_purchase_limit, vol_regime, drawdown)
            elif number(m.get("bias5")) is not None and number(m.get("bias5")) > 10 and catalyst != "confirmed":
                signal, rule = "REDUCE_REVIEW", "RANGE-HIGH-BIAS"
                reason = "BIAS5超过10%且无已确认强催化"
                signal_strength = signal_strength_with_context(
                    strength(True, not bottom_two, not flow_latest_negative),
                    news_factor,
                    sentiment_factor,
                    "reduce",
                )
                amount = action_amount(total, mode, signal_strength, None, None, False, fund["market_value"])
            elif bottom_two:
                signal, rule = "ROTATE_REVIEW", "RANGE-BOTTOM-MOMENTUM"
                reason = "方向动量位于后2，今天不动，等待更明确的替代方向"

        if signal == "HOLD" and history_ok:
            if (
                total_score >= 72
                and price_score >= 62
                and execution_score >= 45
                and data_score >= 80
                and purchasable
                and not qdii_blocked
                and catalyst != "rejected"
                and mode in {"BULL", "RANGE"}
            ):
                signal, rule, add_signal = "ADD", "SCORE-MULTIFACTOR-ADD", True
                reason = "综合多因子评分达到新增区间，且价格、执行、数据和申购门禁通过"
                signal_strength = signal_strength_with_context(
                    clamp((total_score - 60.0) / 30.0),
                    news_factor,
                    sentiment_factor,
                    "trend" if mode == "BULL" else "contrarian",
                )
                amount = action_amount(total, mode, signal_strength, available_cash, 1500, True, fund["market_value"], daily_purchase_limit, vol_regime, drawdown)
            elif total_score <= 38 and price_score <= 42 and execution_score <= 45:
                signal, rule = "REDUCE_REVIEW", "SCORE-MULTIFACTOR-REDUCE"
                reason = "综合多因子评分进入风险区间，且价格或执行层同时转弱"
                signal_strength = clamp((45.0 - total_score) / 30.0)
                amount = action_amount(total, mode, signal_strength, None, None, False, fund["market_value"])
            elif total_score <= 45 and (bottom_two or reversion_score <= 35):
                signal, rule = "ROTATE_REVIEW", "SCORE-MULTIFACTOR-WEAK"
                reason = "综合多因子评分偏弱，今天不动，等待更明确的替代方向"

        realtime_execution = realtime_execution_layer(
            fund,
            m,
            mode,
            signal,
            add_signal,
            flow_latest_negative,
            news_factor,
            sentiment_factor,
        )
        if add_signal and realtime_execution.get("modifier") in {"wait_pullback", "block_add"}:
            blockers.append(f"realtime_{realtime_execution.get('state')}")
        elif amount and realtime_execution.get("modifier") == "reduce_size":
            amount = round(amount * number(realtime_execution.get("size_multiplier"), 1.0), 2)
            reason += f"；{realtime_execution.get('note')}"

        if add_signal and blockers:
            signal = "CONDITIONAL_ADD"
            amount = 0.0
            reason += "；新增金额被数据或风控门禁阻断"
            if realtime_execution.get("modifier") in {"wait_pullback", "block_add"}:
                reason += f"；{realtime_execution.get('note')}"

        factors = factor_snapshot(
            fund,
            m,
            round(score, 2) if score is not None else None,
            rank,
            flow_three_positive,
            flow_latest_negative,
            history_ok,
            purchasable,
            qdii_blocked,
            risk_veto,
            news_veto,
            sentiment_veto,
            realtime_execution,
            scorecard,
        )
        action_blockers = sorted(set(blockers))
        action, action_reason = today_action(
            fund,
            signal,
            amount,
            action_blockers,
            realtime_execution,
            m,
        )
        trade = trade_action(
            fund,
            signal,
            amount,
            action_blockers,
            realtime_execution,
            m,
            action,
            action_reason,
        )

        results.append({
            "code": fund["code"],
            "name": fund.get("name") or "",
            "group_name": fund.get("group_name") or "",
            "direction": fund["direction"],
            "weight_pct": round(fund["market_value"] / total * 100.0, 2) if total else None,
            "momentum_score": round(score, 2) if score is not None else None,
            "momentum_rank": rank,
            "bias5": round(number(m.get("bias5")), 2) if number(m.get("bias5")) is not None else None,
            "bias20": round(number(m.get("bias20")), 2) if number(m.get("bias20")) is not None else None,
            "max_drawdown_pct": round(number(fund.get("max_drawdown_pct"), number(m.get("max_drawdown_pct"))), 2) if number(fund.get("max_drawdown_pct"), number(m.get("max_drawdown_pct"))) is not None else None,
            "annualized_volatility_pct": round(number(fund.get("volatility_pct"), number(m.get("annualized_volatility_pct"))), 2) if number(fund.get("volatility_pct"), number(m.get("annualized_volatility_pct"))) is not None else None,
            "today_action": trade["label"],
            "today_action_reason": trade["instruction"],
            "trade_action": trade,
            "signal": signal,
            "amount": amount,
            "rule": rule,
            "reason": reason,
            "blockers": action_blockers,
            "signal_strength": signal_strength,
            "scorecard": scorecard,
            "factors": factors,
        })

    direction_opportunities = evaluate_direction_opportunities(payload, mode, global_blocks, direction_weights)
    fund_candidates = evaluate_fund_candidates(payload, direction_opportunities, global_blocks)
    portfolio_advice = build_portfolio_advice(
        payload,
        results,
        direction_opportunities,
        sorted(set(global_blocks)),
        direction_weights,
    )

    # Post-process: suppress buy signals for funds identified as drag
    # This prevents contradictions like "建议新增" and "暂停定投" for the same fund
    drag_codes = {item.get("code") for item in portfolio_advice.get("drag_funds", []) if item.get("code")}
    if drag_codes:
        for result in results:
            trade = result.get("trade_action") or {}
            if trade.get("category") == "buy" and result.get("code") in drag_codes:
                # Downgrade: buy signal conflicts with drag identification
                result["signal"] = "CONDITIONAL_ADD"
                result["amount"] = 0.0
                result["rule"] = "DRAG-SUPPRESS"
                result["reason"] = (
                    f"组合层识别为净值拖累方向，新增信号被压制；"
                    f"原信号：{result.get('rule', '')}。"
                    f"{result.get('reason', '')}"
                )
                result["trade_action"] = {
                    "code": "BUY_SUPPRESSED_DRAG",
                    "label": "禁止新增",
                    "category": "blocked",
                    "buy_amount": 0.0,
                    "sell_amount": 0.0,
                    "net_amount": 0.0,
                    "instruction": "该基金被组合层识别为净值拖累方向，新增信号被压制，等待替代方向确认。",
                    "reason": result["reason"],
                }
                result["today_action"] = "禁止新增"
                result["today_action_reason"] = result["trade_action"]["instruction"]
                result["blockers"] = sorted(set(result.get("blockers", []) + ["drag_fund_suppress"]))

    # Merge regime_info into output
    if "regime" not in direction_scores:
        direction_scores["regime"] = regime_info
    
    return {
        "as_of": payload.get("as_of"),
        "timestamps": payload.get("timestamps") or {},
        "execution_window": exec_window,
        "market": {
            "mode": mode,
            "mode_rule": mode_rule,
            "mode_enter_threshold_pct": MODE_ENTER_THRESHOLD_PCT,
            "mode_exit_threshold_pct": MODE_EXIT_THRESHOLD_PCT,
            "previous_mode": normalize_mode(market_input.get("previous_mode")),
            "ma20": benchmark_metrics.get("ma20"),
            "ma60": benchmark_metrics.get("ma60"),
            "gap_pct": gap,
            "benchmark_r10": benchmark_r10,
        },
        "portfolio": {
            "total_market_value": total,
            "portfolio_drawdown_pct": drawdown,
            "official_max_drawdown_pct": abs(official_max_drawdown) if official_max_drawdown is not None else None,
            "official_current_drawdown_pct": abs(official_current_drawdown) if official_current_drawdown is not None else None,
            "execution_estimated_today_return_pct": execution_risk.get("estimated_today_return_pct"),
            "execution_drawdown_pct": execution_risk.get("execution_drawdown_pct"),
            "execution_drawdown_source": execution_risk.get("source"),
            "execution_drawdown_used_funds": execution_risk.get("used_funds"),
            "execution_drawdown_missing_funds": execution_risk.get("missing_funds"),
            "max_drawdown_limit_pct": max_drawdown_limit,
            "portfolio_drawdown_source": drawdown_source,
            "cumulative_return_pct": portfolio_cumulative_return,
            "annualized_volatility_pct": portfolio_annualized_volatility,
            "benchmark_return_pct": portfolio_benchmark_return,
            "relative_benchmark_return_pct": portfolio_relative_return,
            "portfolio_nav_coverage_pct": portfolio_nav_coverage,
            "portfolio_nav_warnings": portfolio_nav_warnings,
            "incremental_cash_available": available_cash,
            "incremental_cash_defaulted": cash_was_defaulted,
            "drawdown_response": drawdown_policy,
            "risk_exposure": risk_exposure,
            "global_blocks": sorted(set(global_blocks)),
            "warnings": warnings,
        },
        "provenance": payload.get("provenance") or {},
        "direction_scores": direction_scores,
        "concentration_actions": concentration_actions,
        "opportunity_pool": {
            "directions": direction_opportunities,
            "fund_candidates": fund_candidates,
            "note": "机会池只输出方向迁移结论；自然语言全市场选基模块已停用，不生成系统候选基金池。",
        },
        "portfolio_advice": portfolio_advice,
        "funds": results,
        "disclaimer": "研究与组合复盘用途，不构成收益承诺；任何交易请求仍需你在花花日记 App 中确认。",
    }


def fmt(value: Any, suffix: str = "") -> str:
    return "不可计算" if value is None else f"{value:.2f}{suffix}" if isinstance(value, float) else f"{value}{suffix}"


MODE_LABELS = {
    "BULL": "偏强",
    "BEAR": "偏弱",
    "RANGE": "震荡",
    "UNKNOWN": "不可判断",
}

MODE_RULE_LABELS = {
    "inside_range_band": "MA20 与 MA60 差值小于 1.8%，按震荡处理",
    "outside_trend_entry_band": "MA20 与 MA60 差值超过 2.2%，进入趋势状态",
    "hysteresis_keep_previous_mode": "处于缓冲区，延续上次同方向趋势",
    "hysteresis_direction_changed_or_previous_range": "处于缓冲区且方向未延续，按震荡处理",
    "hysteresis_no_previous_mode_defaults_range": "处于缓冲区且没有上次状态，按震荡处理",
    "insufficient_benchmark_history": "基准历史不足，暂不判断市场状态",
}

SIGNAL_LABELS = {
    "ADD": "可考虑加仓",
    "CONDITIONAL_ADD": "禁止新增",
    "HOLD": "继续持有",
    "ROTATE_REVIEW": "不动",
    "REDUCE_REVIEW": "不动",
    "FORCED_REVIEW": "不动",
}

RULE_LABELS = {
    "DEFAULT-HOLD": "未触发买卖规则",
    "RISK-FUND-LOSS-15": "单只持有亏损超过 15%",
    "BULL-PULLBACK": "偏强市场里的短线回撤",
    "BULL-CONFIRM": "偏强市场里的趋势确认",
    "BULL-RELATIVE-WEAK": "偏强市场里的相对弱势",
    "BEAR-CROSS-DOWN": "偏弱市场里的趋势转弱",
    "BEAR-REBOUND-REDUCE": "偏弱市场里的反弹偏热",
    "BEAR-PANIC-TEST": "偏弱市场里的小额恐慌测试",
    "RANGE-MEAN-REVERT": "震荡市场里的均值回归",
    "RANGE-HIGH-BIAS": "震荡市场里的短线过热",
    "RANGE-BOTTOM-MOMENTUM": "震荡市场里的弱势方向",
    "RISK-DIRECTION-45": "单一方向仓位过高",
}

BLOCKER_LABELS = {
    "market_mode_unknown": "市场状态不可判断",
    "portfolio_drawdown_unknown": "组合真实回撤不可计算",
    "portfolio_drawdown_above_limit": "组合真实最大回撤超过用户设置的回撤风控线",
    "portfolio_execution_drawdown_above_limit": "盘中执行回撤估算超过用户设置的回撤风控线",
    "incremental_cash_unavailable": "本月可用增量资金不足",
    "direction_mapping_incomplete": "部分基金方向无法可靠识别",
    "total_market_value_invalid": "组合总市值不可用",
    "fund_history_below_60": "基金官方净值历史不足 60 个有效点",
    "fund_bias20_unavailable": "缺少完整净值序列，BIAS20/MA 因子不可计算",
    "fund_not_purchasable": "基金当前不可申购",
    "serenity_risk_veto": "Serenity 证据审视出现重大风险否决",
    "news_factor_veto": "消息面出现重大反证",
    "sentiment_factor_veto": "情绪面出现重大风险",
    "qdii_night_data_not_ready": "QDII 夜盘数据未就绪",
    "realtime_chase_risk": "盘中/夜盘涨幅较大，等待回落避免追涨",
    "realtime_breakdown_risk": "盘中/夜盘跌幅较大且伴随破位或负面证据",
    "realtime_stale": "盘中/夜盘数据过期或缺少关键字段",
    "realtime_no_realtime_data": "缺少有效盘中/夜盘数据",
    "opportunity_history_below_60": "方向历史数据不足 60 个有效点",
    "portfolio_data_gate": "组合基础数据门禁未通过",
    "drawdown_response_stop_add": "回撤渐进响应进入停止新增档",
    "adaptive_frequency_gate_blocked": "自适应调仓频率门禁阻断",
    "drag_fund_suppress": "组合层净值拖累压制新增",
    "direction_not_approved": "所属方向未通过机会池筛选",
    "candidate_source_not_eastmoney": "候选基金不是东财基金筛选结果",
    "candidate_user_named_not_eastmoney_screened": "用户点名基金，未作为东财初筛结果处理",
}

OPPORTUNITY_LABELS = {
    "PRIORITY_RESEARCH": "优先研究",
    "BACKUP_RESEARCH": "备选研究",
    "WATCH": "候选跟踪",
    "AVOID": "暂不纳入",
}


def label(mapping: dict[str, str], key: Any) -> str:
    return mapping.get(str(key or ""), str(key or "未标注"))


def label_many(mapping: dict[str, str], keys: list[str]) -> str:
    return "、".join(label(mapping, key) for key in keys)


def markdown(result: dict[str, Any]) -> str:
    market = result["market"]
    portfolio = result["portfolio"]
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    timestamps = result.get("timestamps") if isinstance(result.get("timestamps"), dict) else {}
    mode_text = label(MODE_LABELS, market["mode"])
    mode_rule_text = label(MODE_RULE_LABELS, market["mode_rule"])
    lines = [
        f"# 个人基金量化复盘 — {result.get('as_of') or '未指定日期'}",
        "",
        "## 数据指纹",
        f"- 云同步：{provenance.get('sync_updated_at') or timestamps.get('portfolio') or '未记录'}；etag：{provenance.get('sync_etag') or '未记录'}",
        f"- 持仓数据：{provenance.get('records_data_updated_at') or timestamps.get('portfolio') or '未记录'}",
        f"- 组合历史：{timestamps.get('portfolio_history') or '未记录'}；行情：{timestamps.get('market') or '未记录'}；资讯：{timestamps.get('news') or '未使用'}",
        f"- 回撤阈值来源：{provenance.get('strategy_preferences_source') or 'get_records.strategyPreferences'}；阈值：{fmt(portfolio.get('max_drawdown_limit_pct'), '%')}",
        "",
        f"市场模式：**{mode_text}**（MA20 {fmt(market['ma20'])} / MA60 {fmt(market['ma60'])} / 差值 {fmt(market['gap_pct'], '%')}；{mode_rule_text}）",
        f"组合总市值：{fmt(portfolio['total_market_value'])}；官方最大回撤：{fmt(portfolio.get('official_max_drawdown_pct'), '%')}；盘中执行回撤估算：{fmt(portfolio.get('execution_drawdown_pct'), '%')}；回撤阈值：{fmt(portfolio.get('max_drawdown_limit_pct'), '%')}",
        f"- 口径说明：官方回撤用于真实收益/审计；盘中执行回撤用实时估值和 QDII 夜盘做风控门禁，不计入真实收益。",
        f"- 盘中估算冲击：{fmt(portfolio.get('execution_estimated_today_return_pct'), '%')}；覆盖基金 {portfolio.get('execution_drawdown_used_funds') or 0} 只，缺失 {portfolio.get('execution_drawdown_missing_funds') or 0} 只。",
        f"组合历史覆盖率：{fmt(portfolio.get('portfolio_nav_coverage_pct'), '%')}",
        "",
        "## 风险门禁",
    ]
    blocks = portfolio.get("global_blocks") or []
    lines.append("- 通过" if not blocks else "- 阻断：" + label_many(BLOCKER_LABELS, blocks))
    if portfolio.get("portfolio_nav_warnings"):
        lines.append("- 组合历史警告：" + "、".join(portfolio["portfolio_nav_warnings"]))
    drawdown_response_row = portfolio.get("drawdown_response") if isinstance(portfolio.get("drawdown_response"), dict) else {}
    if drawdown_response_row:
        lines.append(
            f"- 回撤响应：{drawdown_response_row.get('action') or '未记录'}；仓位系数 {fmt(drawdown_response_row.get('position_multiplier'))}；阈值使用率 {fmt(drawdown_response_row.get('usage_pct'), '%')}"
        )
    risk_exposure = portfolio.get("risk_exposure") if isinstance(portfolio.get("risk_exposure"), dict) else {}
    if risk_exposure.get("directions"):
        lines.extend(["", "## 组合风险暴露", "| 方向 | 权重 | 平均波动 | 风险贡献 | 风险平价目标 | 偏离 |", "|---|---:|---:|---:|---:|---:|"])
        for item in risk_exposure.get("directions")[:8]:
            lines.append(
                f"| {item.get('direction')} | {fmt(item.get('weight_pct'), '%')} | {fmt(item.get('avg_volatility_pct'), '%')} | {fmt(item.get('risk_contribution_score'))} | {fmt(item.get('risk_parity_target_pct'), '%')} | {fmt(item.get('risk_parity_gap_pct'), '%')} |"
            )
    if risk_exposure.get("high_correlation_pairs"):
        pairs = [
            f"{item.get('left')}/{item.get('right')} corr={item.get('corr')} 合计{item.get('combined_weight_pct')}%"
            for item in risk_exposure.get("high_correlation_pairs")[:5]
        ]
        lines.append("- 高相关持仓：" + "；".join(pairs))
    if result.get("concentration_actions"):
        for item in result["concentration_actions"]:
            lines.append(f"- {item['direction']} 当前 {item['weight_pct']}%，方向占比偏高；若有明确替代方向，可参考调出 {item['reduce_amount']:.2f} 元")

    lines.extend([
        "",
        "## 持仓信号",
        "| 基金 | 方向 | 权重 | 回撤 | 波动 | 动量排名 | BIAS20 | 今日动作 | 信号 | 金额 | 核心因子 | 说明 |",
        "|---|---|---:|---:|---:|---:|---:|---|---|---:|---|---|",
    ])
    for fund in result.get("funds") or []:
        rank = fund.get("momentum_rank")
        rank_text = "-" if rank is None else str(rank)
        blockers = "；限制原因：" + label_many(BLOCKER_LABELS, fund["blockers"]) if fund.get("blockers") else ""
        core = fund.get("factors", {}).get("core", {}) if isinstance(fund.get("factors"), dict) else {}
        factor_text = (
            f"近1月 {fmt(core.get('r20'), '%')} / 近3月 {fmt(core.get('r60'), '%')} / "
            f"近6月 {fmt(core.get('r120'), '%')} / 轮动加速度 {fmt(core.get('rotation_acceleration_1m_vs_3m'), '%')} / "
            f"BIAS5 {fmt(core.get('bias5'), '%')}"
        )
        signal_text = label(SIGNAL_LABELS, fund.get("signal"))
        rule_text = label(RULE_LABELS, fund.get("rule"))
        lines.append(
            f"| {fund['name']} ({fund['code']}) | {fund['direction']} | {fmt(fund['weight_pct'], '%')} | {fmt(fund.get('max_drawdown_pct'), '%')} | {fmt(fund.get('annualized_volatility_pct'), '%')} | {rank_text} | {fmt(fund['bias20'], '%')} | {fund.get('today_action') or '继续持有'} | {signal_text} | {fund['amount']:.2f} | {factor_text} | {rule_text}：{fund.get('today_action_reason') or fund['reason']}{blockers} |"
        )
    opportunities = result.get("opportunity_pool") if isinstance(result.get("opportunity_pool"), dict) else {}
    directions = opportunities.get("directions") or []
    if directions:
        lines.extend([
            "",
            "## 板块迁移机会池",
            "| 方向 | 当前权重 | 评分 | 结论 | 核心依据 |",
            "|---|---:|---:|---|---|",
        ])
        for item in directions:
            factors = item.get("factors") if isinstance(item.get("factors"), dict) else {}
            blockers = "；限制：" + label_many(BLOCKER_LABELS, item.get("blockers") or []) if item.get("blockers") else ""
            basis = (
                f"近1月 {fmt(factors.get('r20'), '%')} / 近3月 {fmt(factors.get('r60'), '%')} / "
                f"轮动加速度 {fmt(factors.get('rotation_acceleration_1m_vs_3m'), '%')} / "
                f"估值分位 {fmt(factors.get('valuation_percentile'), '%')} / 证据分 {fmt(factors.get('context_score'))}"
            )
            lines.append(
                f"| {item['name']} | {fmt(item.get('current_weight_pct'), '%')} | {fmt(item.get('score'))} | {label(OPPORTUNITY_LABELS, item.get('action'))} | {item.get('reason')}{blockers}；{basis} |"
            )
    lines.extend(["", result["disclaimer"]])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run deterministic personal fund signals")
    parser.add_argument("input", help="Input JSON path")
    parser.add_argument("--format", choices=("json", "md", "both"), default="both")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("Input JSON must be an object")
    result = evaluate(payload)
    if args.format in ("json", "both"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.format == "both":
        print("\n---\n")
    if args.format in ("md", "both"):
        print(markdown(result), end="")


if __name__ == "__main__":
    main()
