# -*- coding: utf-8 -*-
"""
InvAssistant — 退出引擎 (Exit Engine)
减仓与清仓信号检查，包含多种退出条件。

退出信号类型：
  1. 止盈减仓 — 涨幅达目标后分批减仓锁利
  2. 止损清仓 — 跌破止损线立即清仓
  3. 趋势破位 — 跌破关键均线且无承接
  4. 系统性风险防守 — VIX飙升 + 市场连续暴跌
  5. 动量衰竭 — 上涨趋势中动量减弱（缩量创新高、MACD顶背离）

重要：退出信号同样是纪律驱动（Discipline），不是情绪驱动。
"""
import pandas as pd
import numpy as np


# ============ 默认退出参数 ============
DEFAULT_EXIT_PARAMS = {
    # --- 止盈减仓 ---
    "take_profit_enabled": True,
    "take_profit_tiers": [
        {"gain_pct": 20, "action": "减仓1/3", "reduce_pct": 33, "label": "第一阶梯止盈"},
        {"gain_pct": 40, "action": "再减1/3", "reduce_pct": 33, "label": "第二阶梯止盈"},
        {"gain_pct": 80, "action": "仅保留底仓", "reduce_pct": 50, "label": "大幅止盈"}
    ],

    # --- 止损清仓 ---
    "stop_loss_enabled": True,
    "stop_loss_pct": -15,              # 亏损超过此比例触发清仓 (%)
    "stop_loss_action": "清仓",

    # --- 趋势破位 ---
    "trend_break_enabled": True,
    "trend_break_ma": 50,              # 观测均线周期
    "trend_break_confirm_days": 3,     # 破位确认天数
    "trend_break_no_support": True,    # 需要同时确认无承接
    "trend_break_action": "减仓50%",
    "trend_break_reduce_pct": 50,

    # --- 动量衰竭 ---
    "momentum_fade_enabled": True,
    "momentum_volume_shrink_days": 5,  # 连续缩量天数阈值
    "momentum_new_high_shrink": True,  # 创新高但缩量
    "momentum_action": "减仓1/3",
    "momentum_reduce_pct": 33,

    # --- 成本基准 (需用户配置) ---
    "cost_basis": 0,                   # 持仓成本价 ($)
    "position_size": 0                 # 当前持仓数量 (股)
}

# 系统性风险退出参数（全组合层级）
DEFAULT_SYSTEMIC_RISK_PARAMS = {
    "enabled": True,
    "vix_panic_threshold": 30,         # VIX恐慌阈值
    "vix_extreme_threshold": 40,       # VIX极端阈值
    "market_consecutive_drop_days": 3, # 市场连续下跌天数
    "market_drop_magnitude": -2,       # 单日跌幅算暴跌阈值 (%)
    "panic_action": "非核心仓减半",
    "extreme_action": "全组合减至50%"
}


def check_take_profit(df, params=None):
    """
    止盈减仓检查：当前价格相对成本的涨幅是否触达阶梯止盈线。

    逻辑：
    - 根据 cost_basis（持仓成本）计算当前浮盈比例
    - 按阶梯止盈表逐级检查，返回最高触达的阶梯

    Args:
        df: 股票 OHLCV DataFrame
        params: 含 cost_basis, take_profit_tiers 的参数 dict

    Returns:
        (signal: bool, detail: str, tier: dict|None)
    """
    p = {**DEFAULT_EXIT_PARAMS, **(params or {})}

    if not p["take_profit_enabled"]:
        return False, "止盈检查已禁用", None

    cost_basis = p.get("cost_basis", 0)
    if cost_basis <= 0:
        return False, "未配置持仓成本(cost_basis)，跳过止盈检查", None

    if df is None or len(df) < 1:
        return False, "数据不足", None

    current_price = df["Close"].iloc[-1]
    gain_pct = (current_price - cost_basis) / cost_basis * 100

    tiers = p.get("take_profit_tiers", DEFAULT_EXIT_PARAMS["take_profit_tiers"])
    # 从高到低检查阶梯
    triggered_tier = None
    for tier in sorted(tiers, key=lambda x: x["gain_pct"], reverse=True):
        if gain_pct >= tier["gain_pct"]:
            triggered_tier = tier
            break

    if triggered_tier:
        detail = (
            f"当前浮盈 {gain_pct:+.1f}% (成本${cost_basis:.2f} → 现价${current_price:.2f}) | "
            f"触达{triggered_tier['label']}({triggered_tier['gain_pct']}%) → {triggered_tier['action']}"
        )
        return True, detail, triggered_tier

    detail = f"当前浮盈 {gain_pct:+.1f}% (成本${cost_basis:.2f} → 现价${current_price:.2f}) | 未触达止盈线"
    return False, detail, None


def check_stop_loss(df, params=None):
    """
    止损清仓检查：当前价格相对成本的亏损是否触达止损线。

    Args:
        df: 股票 OHLCV DataFrame
        params: 含 cost_basis, stop_loss_pct 的参数 dict

    Returns:
        (signal: bool, detail: str)
    """
    p = {**DEFAULT_EXIT_PARAMS, **(params or {})}

    if not p["stop_loss_enabled"]:
        return False, "止损检查已禁用"

    cost_basis = p.get("cost_basis", 0)
    if cost_basis <= 0:
        return False, "未配置持仓成本(cost_basis)，跳过止损检查"

    if df is None or len(df) < 1:
        return False, "数据不足"

    current_price = df["Close"].iloc[-1]
    loss_pct = (current_price - cost_basis) / cost_basis * 100
    threshold = p["stop_loss_pct"]

    if loss_pct <= threshold:
        return True, (
            f"⚠️ 触发止损！亏损 {loss_pct:.1f}% (止损线{threshold}%) | "
            f"成本${cost_basis:.2f} → 现价${current_price:.2f} → {p['stop_loss_action']}"
        )

    if loss_pct < 0:
        distance = abs(loss_pct - threshold)
        return False, f"浮亏 {loss_pct:.1f}%，距止损线({threshold}%)还有 {distance:.1f}%"

    return False, f"浮盈 {loss_pct:+.1f}%，无止损风险"


def check_trend_break(df, params=None):
    """
    趋势破位检查：价格是否有效跌破关键均线。

    有效破位定义（避免假突破）：
    - 收盘价连续 N 日（默认3）低于指定均线
    - 期间无明显承接信号（无放量长下影线反弹）
    - 均线本身拐头向下

    Args:
        df: 股票 OHLCV DataFrame
        params: 含 trend_break_ma, trend_break_confirm_days 的参数 dict

    Returns:
        (signal: bool, detail: str)
    """
    p = {**DEFAULT_EXIT_PARAMS, **(params or {})}

    if not p["trend_break_enabled"]:
        return False, "趋势破位检查已禁用"

    ma_period = p["trend_break_ma"]
    confirm_days = p["trend_break_confirm_days"]

    if df is None or len(df) < ma_period + 5:
        return False, f"数据不足(需要{ma_period + 5}日以上数据)"

    df = df.copy()
    ma_col = f"MA{ma_period}"
    df[ma_col] = df["Close"].rolling(ma_period).mean()

    # 检查最近 confirm_days 是否连续收于均线下方
    recent = df.tail(confirm_days)
    if recent[ma_col].isna().any():
        return False, f"{ma_col}计算数据不足"

    below_ma = all(
        recent.iloc[i]["Close"] < recent.iloc[i][ma_col]
        for i in range(len(recent))
    )

    if not below_ma:
        current_close = df["Close"].iloc[-1]
        current_ma = df[ma_col].iloc[-1]
        if pd.notna(current_ma):
            distance = (current_close - current_ma) / current_ma * 100
            return False, f"未破位 | 收盘价${current_close:.2f} vs {ma_col}=${current_ma:.2f} ({distance:+.1f}%)"
        return False, "未破位"

    # 检查均线是否拐头向下
    ma_values = df[ma_col].dropna()
    if len(ma_values) >= 3:
        ma_slope = ma_values.iloc[-1] - ma_values.iloc[-3]
        ma_turning_down = ma_slope < 0
    else:
        ma_turning_down = False

    # 检查是否有承接信号（如果要求的话）
    has_support = False
    if p.get("trend_break_no_support", True):
        for i in range(-confirm_days, 0):
            row = df.iloc[i]
            prev_row = df.iloc[i - 1] if abs(i - 1) < len(df) else None
            # 承接信号：下影线 + 收涨 + 放量
            lower_shadow = (row["Close"] - row["Low"]) > (row["High"] - row["Close"]) * 1.5
            closed_up = row["Close"] > row["Open"]
            vol_up = prev_row is not None and row["Volume"] > prev_row["Volume"] * 1.2
            if lower_shadow and closed_up and vol_up:
                has_support = True
                break

    if has_support:
        return False, (
            f"价格低于{ma_col}但期间有承接信号（下影线+收涨+放量），暂不判定破位"
        )

    current_close = df["Close"].iloc[-1]
    current_ma = df[ma_col].iloc[-1]
    break_depth = (current_close - current_ma) / current_ma * 100

    detail_parts = [
        f"⚠️ {ma_col}破位确认",
        f"连续{confirm_days}日收于{ma_col}下方",
        f"收盘${current_close:.2f} vs {ma_col}=${current_ma:.2f} ({break_depth:.1f}%)"
    ]
    if ma_turning_down:
        detail_parts.append("均线拐头向下")
    detail_parts.append(f"→ {p['trend_break_action']}")

    return True, " | ".join(detail_parts)


def check_momentum_fade(df, params=None):
    """
    动量衰竭检查：上涨趋势中出现动量减弱信号。

    检查条件：
    - 创新高但成交量显著萎缩（量价背离）
    - 连续多日上涨但量能递减
    - MACD 顶背离（价格新高但 MACD 柱缩短）

    Args:
        df: 股票 OHLCV DataFrame
        params: 含 momentum_volume_shrink_days 等的参数 dict

    Returns:
        (signal: bool, detail: str)
    """
    p = {**DEFAULT_EXIT_PARAMS, **(params or {})}

    if not p["momentum_fade_enabled"]:
        return False, "动量衰竭检查已禁用"

    if df is None or len(df) < 30:
        return False, "数据不足(需要30日数据)"

    df = df.copy()
    signals = []

    # ---- 检查1: 创新高但缩量 ----
    high_20d = df["Close"].tail(20).max()
    current_close = df["Close"].iloc[-1]
    is_near_high = current_close >= high_20d * 0.98  # 距20日高点2%以内

    if is_near_high and p.get("momentum_new_high_shrink", True):
        # 检查最近几天的量能趋势
        recent_vol = df["Volume"].tail(5)
        vol_avg_20 = df["Volume"].tail(20).mean()
        recent_avg = recent_vol.mean()
        if recent_avg < vol_avg_20 * 0.7:
            signals.append(
                f"创新高/近高点但量能萎缩 (近5日均量仅为20日均量的{recent_avg/vol_avg_20*100:.0f}%)"
            )

    # ---- 检查2: 连续缩量 ----
    shrink_days = p.get("momentum_volume_shrink_days", 5)
    consecutive_shrink = 0
    for i in range(len(df) - 1, max(0, len(df) - shrink_days - 1), -1):
        if i > 0 and df["Volume"].iloc[i] < df["Volume"].iloc[i - 1]:
            consecutive_shrink += 1
        else:
            break

    if consecutive_shrink >= shrink_days:
        signals.append(f"连续{consecutive_shrink}日量能递减")

    # ---- 检查3: MACD 顶背离 ----
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd_hist = macd_line - signal_line

    # 寻找最近两个价格高点
    if len(df) >= 20:
        price_highs = []
        for i in range(len(df) - 15, len(df) - 1):
            if i > 0 and i < len(df) - 1:
                if df["Close"].iloc[i] > df["Close"].iloc[i-1] and df["Close"].iloc[i] > df["Close"].iloc[i+1]:
                    price_highs.append((i, df["Close"].iloc[i], macd_hist.iloc[i]))

        if len(price_highs) >= 2:
            ph1 = price_highs[-2]
            ph2 = price_highs[-1]
            # 价格新高但 MACD 柱缩短 = 顶背离
            if ph2[1] > ph1[1] and ph2[2] < ph1[2] and ph2[2] > 0:
                signals.append(
                    f"MACD顶背离 (价格${ph1[1]:.0f}→${ph2[1]:.0f}↑ 但MACD柱{ph1[2]:.2f}→{ph2[2]:.2f}↓)"
                )

    if signals:
        detail = " | ".join([f"✓ {s}" for s in signals])
        return True, f"{detail} → {p['momentum_action']}"

    return False, "动量正常，无衰竭信号"


def check_systemic_risk_exit(market_data, params=None):
    """
    系统性风险防守退出检查（全组合层级）。

    当市场进入系统性风险状态时，无论个股表现如何，都应启动防守机制。
    这是唯一一个可以覆盖「永久 HOLD」策略的退出条件。

    条件：
    - VIX ≥ 恐慌阈值 (30) → 非核心仓减半
    - VIX ≥ 极端阈值 (40) → 全组合减至50%
    - QQQ/SPX 连续3日暴跌（每日跌幅≥2%）→ 触发防守

    Args:
        market_data: dict 包含 QQQ, ^GSPC, ^VIX 的 DataFrame
        params: 系统性风险参数 dict

    Returns:
        (signal_level: str, detail: str)
        signal_level: "none" / "warning" / "panic" / "extreme"
    """
    p = {**DEFAULT_SYSTEMIC_RISK_PARAMS, **(params or {})}

    if not p.get("enabled", True):
        return "none", "系统性风险退出检查已禁用"

    vix_df = market_data.get("^VIX")
    qqq_df = market_data.get("QQQ")
    spx_df = market_data.get("^GSPC")

    if vix_df is None:
        return "none", "VIX数据缺失，无法评估系统性风险"

    latest_vix = vix_df["Close"].iloc[-1]
    panic_th = p["vix_panic_threshold"]
    extreme_th = p["vix_extreme_threshold"]
    drop_days = p["market_consecutive_drop_days"]
    drop_mag = p["market_drop_magnitude"]

    details = []
    level = "none"

    # VIX 检查
    if latest_vix >= extreme_th:
        level = "extreme"
        details.append(f"🔴 VIX={latest_vix:.1f} (≥极端阈值{extreme_th})")
    elif latest_vix >= panic_th:
        level = "panic"
        details.append(f"🟠 VIX={latest_vix:.1f} (≥恐慌阈值{panic_th})")
    elif latest_vix >= panic_th * 0.85:
        level = "warning"
        details.append(f"🟡 VIX={latest_vix:.1f} (接近恐慌阈值{panic_th})")
    else:
        details.append(f"✅ VIX={latest_vix:.1f} (<{panic_th})")

    # QQQ 连续暴跌检查
    if qqq_df is not None and len(qqq_df) >= drop_days + 1:
        qqq_returns = qqq_df["Close"].pct_change().dropna() * 100
        recent_qqq = qqq_returns.tail(drop_days)
        qqq_consecutive_drop = all(r <= drop_mag for r in recent_qqq)
        if qqq_consecutive_drop:
            if level in ("none", "warning"):
                level = "panic"
            details.append(
                f"🔴 QQQ连续{drop_days}日暴跌 ({', '.join(f'{r:.1f}%' for r in recent_qqq)})"
            )
        else:
            details.append("✅ QQQ未连续暴跌")

    # SPX 连续暴跌检查
    if spx_df is not None and len(spx_df) >= drop_days + 1:
        spx_returns = spx_df["Close"].pct_change().dropna() * 100
        recent_spx = spx_returns.tail(drop_days)
        spx_consecutive_drop = all(r <= drop_mag for r in recent_spx)
        if spx_consecutive_drop:
            if level in ("none", "warning"):
                level = "panic"
            details.append(
                f"🔴 SPX连续{drop_days}日暴跌 ({', '.join(f'{r:.1f}%' for r in recent_spx)})"
            )
        else:
            details.append("✅ SPX未连续暴跌")

    # 汇总
    if level == "extreme":
        details.append(f"→ 行动: {p['extreme_action']}")
    elif level == "panic":
        details.append(f"→ 行动: {p['panic_action']}")
    elif level == "warning":
        details.append("→ 行动: 提高警惕，准备防守方案")

    return level, " | ".join(details)


def run_exit_check(df, params=None):
    """
    执行完整的单标的退出信号检查。

    按优先级依次检查：止损 > 止盈 > 趋势破位 > 动量衰竭。
    止损是最高优先级，一旦触发不再检查其他条件。

    Args:
        df: 目标股票 OHLCV DataFrame
        params: 退出参数 dict

    Returns:
        dict 包含各检查项结果、最终行动建议
    """
    p = {**DEFAULT_EXIT_PARAMS, **(params or {})}

    result = {
        "has_exit_signal": False,
        "priority_action": None,
        "checks": {}
    }

    # 1. 止损检查 (最高优先级)
    sl_signal, sl_detail = check_stop_loss(df, p)
    result["checks"]["stop_loss"] = {"signal": sl_signal, "detail": sl_detail}
    if sl_signal:
        result["has_exit_signal"] = True
        result["priority_action"] = {
            "type": "stop_loss",
            "urgency": "CRITICAL",
            "action": p.get("stop_loss_action", "清仓"),
            "detail": sl_detail
        }
        # 止损触发后不再检查其他条件
        return result

    # 2. 止盈检查
    tp_signal, tp_detail, tp_tier = check_take_profit(df, p)
    result["checks"]["take_profit"] = {
        "signal": tp_signal,
        "detail": tp_detail,
        "tier": tp_tier
    }
    if tp_signal:
        result["has_exit_signal"] = True
        result["priority_action"] = {
            "type": "take_profit",
            "urgency": "HIGH",
            "action": tp_tier.get("action", "减仓") if tp_tier else "减仓",
            "reduce_pct": tp_tier.get("reduce_pct", 33) if tp_tier else 33,
            "detail": tp_detail
        }

    # 3. 趋势破位检查
    tb_signal, tb_detail = check_trend_break(df, p)
    result["checks"]["trend_break"] = {"signal": tb_signal, "detail": tb_detail}
    if tb_signal and not result["has_exit_signal"]:
        result["has_exit_signal"] = True
        result["priority_action"] = {
            "type": "trend_break",
            "urgency": "HIGH",
            "action": p.get("trend_break_action", "减仓50%"),
            "reduce_pct": p.get("trend_break_reduce_pct", 50),
            "detail": tb_detail
        }

    # 4. 动量衰竭检查
    mf_signal, mf_detail = check_momentum_fade(df, p)
    result["checks"]["momentum_fade"] = {"signal": mf_signal, "detail": mf_detail}
    if mf_signal and not result["has_exit_signal"]:
        result["has_exit_signal"] = True
        result["priority_action"] = {
            "type": "momentum_fade",
            "urgency": "MEDIUM",
            "action": p.get("momentum_action", "减仓1/3"),
            "reduce_pct": p.get("momentum_reduce_pct", 33),
            "detail": mf_detail
        }

    return result
