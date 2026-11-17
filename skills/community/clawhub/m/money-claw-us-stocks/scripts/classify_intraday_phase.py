#!/usr/bin/env python3
"""Classify the live 5-minute phase of an extreme-move U.S. stock.

This module is a second-stage execution gate. Run score_candidates.py first;
technical strength must never override a halt, dilution overhang, or an
upstream status other than EXECUTE.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable

from score_candidates import (
    InputError,
    load_rows,
    parse_bool,
    parse_dilution_risk,
    parse_number,
    pct_change,
)


PHASES = {
    "WAIT_DATA",
    "HALTED",
    "OPEN_CONFIRMATION",
    "TREND_EXPANSION",
    "CONTROLLED_PULLBACK",
    "PARABOLIC_EXTENSION",
    "BLOW_OFF_DISTRIBUTION",
    "FAILED_TREND",
}

ENTRY_ACTIONS = {
    "ENTER_ON_RETEST",
    "WAIT_RETEST",
    "WAIT_CONFIRMATION",
    "NO_NEW_ENTRY",
}

POSITION_ACTIONS = {
    "FLAT",
    "WAIT",
    "HOLD_TRAIL",
    "REDUCE_TO_CORE",
    "SCALE_OUT_50_80",
    "EXIT_RUNNER",
    "EXIT",
    "RECHECK_AFTER_RESUME",
}

MAX_SPREAD_PCT = 2.50
RISK_FRACTION = 0.0025


def normalize_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip().upper()


def catalyst_stage(row: dict[str, Any]) -> tuple[str, list[str]]:
    """Return a simple catalyst-fermentation stage and its risk flags."""
    official = parse_bool(row.get("official_primary_source"))
    age_minutes = parse_number(row.get("catalyst_age_minutes"))
    flags: list[str] = []

    if official is False:
        flags.append("CATALYST_UNVERIFIED")
        return "UNVERIFIED", flags
    if official is None or age_minutes is None:
        flags.append("CATALYST_DATA_MISSING")
        return "UNKNOWN", flags
    if age_minutes < 0:
        flags.append("CATALYST_TIME_INVALID")
        return "UNKNOWN", flags
    if age_minutes <= 30:
        return "FRESH", flags
    if age_minutes <= 120:
        return "FERMENTING", flags
    return "CROWDED", flags


def safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def position_size(
    account_equity: float | None,
    entry_price: float | None,
    stop_price: float | None,
) -> dict[str, float | int] | None:
    """Size by a 0.25% account-risk budget."""
    if (
        account_equity is None
        or entry_price is None
        or stop_price is None
        or account_equity <= 0
        or entry_price <= stop_price
    ):
        return None
    risk_budget = account_equity * RISK_FRACTION
    risk_per_share = entry_price - stop_price
    shares = math.floor(risk_budget / risk_per_share)
    if shares <= 0:
        return None
    return {
        "risk_budget": round(risk_budget, 2),
        "risk_per_share": round(risk_per_share, 4),
        "shares": shares,
        "notional": round(shares * entry_price, 2),
    }


def classify(row: dict[str, Any]) -> dict[str, Any]:
    symbol = normalize_text(row.get("symbol"), "UNKNOWN")
    candidate_status = normalize_text(row.get("candidate_status"), "UNKNOWN")
    position_state = normalize_text(row.get("position_state"), "FLAT")

    prev_close = parse_number(row.get("prev_close"))
    open_price = parse_number(row.get("open_price"))
    last_price = parse_number(row.get("last_price"))
    high_price = parse_number(row.get("high_price"))
    vwap = parse_number(row.get("vwap"))
    bid = parse_number(row.get("bid"))
    ask = parse_number(row.get("ask"))
    ma5 = parse_number(row.get("ma5"))
    ma10 = parse_number(row.get("ma10"))
    ma20 = parse_number(row.get("ma20"))
    current_bar_volume = parse_number(row.get("current_bar_volume"))
    bar_volume_ma5 = parse_number(row.get("bar_volume_ma5"))
    macd_hist = parse_number(row.get("macd_hist"))
    halted = parse_bool(row.get("halted"))
    dilution = parse_dilution_risk(row.get("dilution_overhang"))
    premarket_supply_raw = row.get("premarket_supply_risk")
    premarket_supply_risk = parse_dilution_risk(premarket_supply_raw)
    if dilution is True or premarket_supply_risk is True:
        effective_supply_risk = True
    elif premarket_supply_raw in (None, ""):
        effective_supply_risk = dilution
    else:
        effective_supply_risk = premarket_supply_risk
    turnover_expanding = parse_bool(row.get("turnover_expanding"))
    retest_confirmed = parse_bool(row.get("retest_confirmed"))

    day_gain_pct = pct_change(last_price, prev_close)
    official_gap_pct = pct_change(open_price, prev_close)
    from_open_pct = pct_change(last_price, open_price)
    vwap_extension_pct = pct_change(last_price, vwap)
    high_fade_pct = pct_change(last_price, high_price)
    ma5_extension_pct = pct_change(last_price, ma5)
    volume_impulse = safe_ratio(current_bar_volume, bar_volume_ma5)
    spread_pct = None
    if bid is not None and ask is not None and bid > 0 and ask >= bid:
        midpoint = (bid + ask) / 2
        spread_pct = (ask - bid) / midpoint * 100

    catalyst, catalyst_flags = catalyst_stage(row)
    risk_flags = list(catalyst_flags)
    missing = [
        name
        for name, value in {
            "prev_close": prev_close,
            "last_price": last_price,
            "high_price": high_price,
            "vwap": vwap,
        }.items()
        if value is None
    ]

    if halted is True:
        phase = "HALTED"
        risk_flags.append("HALTED")
    elif missing:
        phase = "WAIT_DATA"
        risk_flags.append("MISSING_DATA")
    elif (
        day_gain_pct is not None
        and day_gain_pct >= 250
        and high_fade_pct is not None
        and high_fade_pct <= -10
        and volume_impulse is not None
        and volume_impulse >= 2
        and (
            (ma5 is not None and last_price is not None and last_price < ma5)
            or (macd_hist is not None and macd_hist <= 0)
        )
    ):
        phase = "BLOW_OFF_DISTRIBUTION"
    elif (
        day_gain_pct is not None
        and day_gain_pct >= 150
        and (
            (vwap_extension_pct is not None and vwap_extension_pct >= 40)
            or (ma5_extension_pct is not None and ma5_extension_pct >= 12)
        )
    ):
        phase = "PARABOLIC_EXTENSION"
    elif (
        (last_price is not None and vwap is not None and last_price < vwap)
        or (high_fade_pct is not None and high_fade_pct <= -30)
    ):
        phase = "FAILED_TREND"
    elif (
        day_gain_pct is not None
        and day_gain_pct >= 50
        and high_fade_pct is not None
        and -25 <= high_fade_pct <= -8
        and last_price is not None
        and vwap is not None
        and last_price >= vwap
        and (ma20 is None or last_price >= ma20)
        and (ma5 is None or last_price < ma5)
    ):
        phase = "CONTROLLED_PULLBACK"
    elif (
        last_price is not None
        and vwap is not None
        and ma5 is not None
        and ma10 is not None
        and ma20 is not None
        and last_price >= vwap
        and last_price >= ma5 >= ma10 >= ma20
        and turnover_expanding is True
    ):
        phase = "TREND_EXPANSION"
    else:
        phase = "OPEN_CONFIRMATION"

    if dilution is True:
        risk_flags.append("DILUTION_OVERHANG")
    elif dilution is None:
        risk_flags.append("DILUTION_UNKNOWN")
    if effective_supply_risk is True:
        risk_flags.append("SUPPLY_RISK_CONFIRMED")
    elif effective_supply_risk is None:
        risk_flags.append("SUPPLY_RISK_UNKNOWN")
    if spread_pct is None:
        risk_flags.append("SPREAD_UNKNOWN")
    elif spread_pct > MAX_SPREAD_PCT:
        risk_flags.append("WIDE_SPREAD")

    hard_block = (
        candidate_status != "EXECUTE"
        or halted is True
        or effective_supply_risk is not False
        or catalyst == "UNVERIFIED"
        or phase in {
            "WAIT_DATA",
            "HALTED",
            "PARABOLIC_EXTENSION",
            "BLOW_OFF_DISTRIBUTION",
            "FAILED_TREND",
        }
    )
    if hard_block:
        entry_action = "NO_NEW_ENTRY"
    elif phase in {"TREND_EXPANSION", "CONTROLLED_PULLBACK"}:
        if (
            retest_confirmed is True
            and spread_pct is not None
            and spread_pct <= MAX_SPREAD_PCT
        ):
            entry_action = "ENTER_ON_RETEST"
        else:
            entry_action = "WAIT_RETEST"
    else:
        entry_action = "WAIT_CONFIRMATION"

    if position_state not in {"LONG", "OPEN"}:
        position_action = "FLAT"
    elif phase == "HALTED":
        position_action = "RECHECK_AFTER_RESUME"
    elif phase == "BLOW_OFF_DISTRIBUTION":
        position_action = "EXIT_RUNNER"
    elif phase == "PARABOLIC_EXTENSION":
        position_action = "SCALE_OUT_50_80"
    elif phase == "FAILED_TREND":
        position_action = "EXIT"
    elif phase == "CONTROLLED_PULLBACK":
        position_action = "REDUCE_TO_CORE"
    elif phase == "TREND_EXPANSION":
        position_action = "HOLD_TRAIL"
    else:
        position_action = "WAIT"

    sizing = position_size(
        parse_number(row.get("account_equity")),
        parse_number(row.get("entry_price")),
        parse_number(row.get("stop_price")),
    )

    return {
        "symbol": symbol,
        "timestamp": row.get("timestamp") or "UNKNOWN",
        "candidate_status": candidate_status,
        "phase": phase,
        "catalyst_stage": catalyst,
        "entry_action": entry_action,
        "position_action": position_action,
        "metrics": {
            "day_gain_pct": day_gain_pct,
            "official_gap_pct": official_gap_pct,
            "from_open_pct": from_open_pct,
            "vwap_extension_pct": vwap_extension_pct,
            "high_fade_pct": high_fade_pct,
            "ma5_extension_pct": ma5_extension_pct,
            "volume_impulse": volume_impulse,
            "spread_pct": spread_pct,
        },
        "position_size": sizing,
        "risk_flags": sorted(set(risk_flags)),
        "missing": missing,
    }


def fmt(value: float | None, suffix: str = "") -> str:
    return "UNKNOWN" if value is None else f"{value:,.2f}{suffix}"


def markdown(results: Iterable[dict[str, Any]]) -> str:
    output = [
        "| Symbol | Time | Phase | Catalyst | Entry | Position | Gain | High fade | VWAP ext. | Vol impulse | Spread | Risks |",
        "|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in results:
        metrics = item["metrics"]
        output.append(
            "| {symbol} | {time} | {phase} | {catalyst} | {entry} | {position} | {gain} | {fade} | {vwap} | {volume} | {spread} | {risks} |".format(
                symbol=item["symbol"],
                time=item["timestamp"],
                phase=item["phase"],
                catalyst=item["catalyst_stage"],
                entry=item["entry_action"],
                position=item["position_action"],
                gain=fmt(metrics["day_gain_pct"], "%"),
                fade=fmt(metrics["high_fade_pct"], "%"),
                vwap=fmt(metrics["vwap_extension_pct"], "%"),
                volume=fmt(metrics["volume_impulse"], "x"),
                spread=fmt(metrics["spread_pct"], "%"),
                risks=", ".join(item["risk_flags"]) or "-",
            )
        )
    return "\n".join(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="CSV or JSON snapshot file")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        rows = load_rows(args.input)
        if not rows:
            raise InputError("input contains no snapshot rows")
        results = [classify(row) for row in rows]
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(markdown(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
