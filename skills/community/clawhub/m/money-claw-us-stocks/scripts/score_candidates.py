#!/usr/bin/env python3
"""Deterministic screener for U.S. extreme-move candidates.

The evidence score ranks the completeness and strength of observed factors. It
is not a probability forecast. Missing fields remain unknown and never silently
become zero.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable


VALID_SECURITY_TOKENS = (
    "common stock",
    "common shares",
    "ordinary shares",
    "ordinary share",
    "adr",
    "ads",
)
INVALID_SECURITY_TOKENS = (
    "etf",
    "warrant",
    "right",
    "unit",
    "preferred",
    "bond",
    "note",
)
TRUE_VALUES = {"true", "1", "yes", "y", "是"}
FALSE_VALUES = {"false", "0", "no", "n", "否"}
UNKNOWN_VALUES = {"na", "n/a", "none", "null", "unknown", "-", "未知"}
DILUTION_CLEAR_VALUES = {
    "clear",
    "cleared",
    "no known",
    "no known dilution",
    "no active dilution",
    "无",
    "无已知稀释",
}
CONFIRMED_VALUES = {"confirmed", "confirm", "pass", "passed", "valid", "hold", "通过", "确认"}
FAILED_VALUES = {"failed", "fail", "invalid", "lost", "失效", "失败"}
VALID_STATUSES = {"EXECUTE", "WAIT_OPEN", "WAIT_DATA", "WATCH", "EXCLUDE"}
VALID_PATH_TYPES = {
    "CONVENTIONAL_GAP",
    "CPHI_SUBTYPE",
    "AFTER_HOURS_EARNINGS",
    "AFTER_HOURS_LOW_SUPPLY",
    "NONE",
}


class InputError(ValueError):
    """Raised when candidate input cannot be parsed safely."""


def parse_number(value: Any) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        result = float(value)
        return result if math.isfinite(result) else None
    text = str(value).strip().replace(",", "").replace("$", "").replace("%", "")
    if not text or text.lower() in UNKNOWN_VALUES:
        return None
    multipliers = {"k": 1_000.0, "m": 1_000_000.0, "b": 1_000_000_000.0}
    multiplier = multipliers.get(text[-1:].lower(), 1.0)
    if multiplier != 1.0:
        text = text[:-1]
    try:
        result = float(text) * multiplier
    except ValueError as exc:
        raise InputError(f"invalid numeric value: {value!r}") from exc
    return result if math.isfinite(result) else None


def parse_bool(value: Any) -> bool | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    if text in UNKNOWN_VALUES:
        return None
    raise InputError(f"invalid boolean value: {value!r}")


def parse_dilution_risk(value: Any) -> bool | None:
    """Normalize a boolean or descriptive dilution-overhang field.

    Any non-empty descriptive text that is not an explicit clear/unknown value
    is treated conservatively as an unresolved dilution risk.
    """

    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES or text in DILUTION_CLEAR_VALUES:
        return False
    if text in UNKNOWN_VALUES:
        return None
    return True


def safe_div(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def pct_change(current: float | None, base: float | None) -> float | None:
    ratio = safe_div(current, base)
    return None if ratio is None else (ratio - 1.0) * 100.0


def first_positive(*values: float | None) -> float | None:
    return next((value for value in values if value is not None and value > 0), None)


def normalize_security(value: Any) -> tuple[bool | None, str]:
    if value is None or not str(value).strip():
        return None, "UNKNOWN"
    text = str(value).strip().lower()
    if any(token in text for token in INVALID_SECURITY_TOKENS):
        return False, str(value).strip()
    if any(token in text for token in VALID_SECURITY_TOKENS):
        return True, str(value).strip()
    return None, str(value).strip()


def parse_confirmation(value: Any) -> bool | None:
    if value is None or not str(value).strip():
        return None
    text = str(value).strip().lower()
    if text in CONFIRMED_VALUES:
        return True
    if text in FAILED_VALUES:
        return False
    if text in UNKNOWN_VALUES:
        return None
    raise InputError(f"invalid first_5m_structure value: {value!r}")


def add_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def gate(value: bool | None, name: str, passed: list[str], failed: list[str], unknown: list[str]) -> None:
    if value is True:
        add_unique(passed, name)
    elif value is False:
        add_unique(failed, name)
    else:
        add_unique(unknown, name)


def evaluate_required_gates(
    gates: dict[str, bool | None],
    passed: list[str],
    failed: list[str],
    unknown: list[str],
) -> tuple[bool, bool, bool]:
    for name, value in gates.items():
        gate(value, name, passed, failed, unknown)
    values = tuple(gates.values())
    return all(value is True for value in values), any(value is False for value in values), any(
        value is None for value in values
    )


def classify(row: dict[str, Any]) -> dict[str, Any]:
    symbol = str(row.get("symbol") or "").strip().upper()
    if not symbol:
        raise InputError("every row requires a non-empty symbol")

    security_ok, security_label = normalize_security(row.get("security_type"))
    listed_days = parse_number(row.get("listed_days"))
    prev_close = parse_number(row.get("prev_close"))
    pre_price = parse_number(row.get("pre_price"))
    pre_high = parse_number(row.get("pre_high"))
    pre_volume = parse_number(row.get("pre_volume"))
    bid = parse_number(row.get("bid"))
    ask = parse_number(row.get("ask"))
    market_cap = parse_number(row.get("market_cap"))
    total_shares = parse_number(row.get("total_shares"))
    float_shares = parse_number(row.get("float_shares"))
    median_dollar_volume_20 = parse_number(row.get("median_dollar_volume_20"))
    avg_volume_20 = parse_number(row.get("avg_volume_20"))
    split_today = parse_bool(row.get("split_today"))
    post_split = parse_bool(row.get("post_split"))
    halted = parse_bool(row.get("halted"))
    dilution_risk = parse_dilution_risk(row.get("dilution_overhang"))
    premarket_supply_raw = row.get("premarket_supply_risk")
    premarket_supply_risk = parse_dilution_risk(premarket_supply_raw)
    supply_risk_type = str(row.get("supply_risk_type") or "UNKNOWN").strip()
    supply_risk_source = str(row.get("supply_risk_source") or "UNKNOWN").strip()
    supply_risk_checked_at = str(row.get("supply_risk_checked_at") or "UNKNOWN").strip()
    open_price = parse_number(row.get("open_price"))
    last_price = parse_number(row.get("last_price"))
    regular_volume = parse_number(row.get("regular_volume"))
    vwap = parse_number(row.get("vwap"))
    first_5m_confirmed = parse_confirmation(row.get("first_5m_structure"))
    prior_warmup = parse_bool(row.get("prior_abnormal_volume_warmup"))
    turnover_expanding = parse_bool(row.get("turnover_expanding"))
    regular_close = parse_number(row.get("regular_close"))
    after_price = parse_number(row.get("after_price"))
    after_high = parse_number(row.get("after_high"))
    after_volume = parse_number(row.get("after_volume"))
    after_bid = parse_number(row.get("after_bid"))
    after_ask = parse_number(row.get("after_ask"))
    after_catalyst_quality = str(row.get("after_hours_catalyst_quality") or "UNKNOWN").strip().upper()
    after_supply_thesis = str(row.get("after_hours_supply_thesis") or "UNKNOWN").strip().upper()
    market_status_text = str(row.get("market_status") or "").strip().lower()
    is_after_hours = any(token in market_status_text for token in ("after", "post", "盘后"))

    valuation_price = first_positive(last_price, after_price, pre_price, regular_close, prev_close)
    implied_total_shares = safe_div(market_cap, valuation_price)
    supply_shares = first_positive(float_shares, total_shares, implied_total_shares)
    supply_source = (
        "float_shares"
        if float_shares is not None and float_shares > 0
        else "total_shares"
        if total_shares is not None and total_shares > 0
        else "implied_total_shares"
        if implied_total_shares is not None
        else "UNKNOWN"
    )

    pre_gap_pct = pct_change(pre_price, prev_close)
    official_gap_pct = pct_change(open_price, prev_close)
    spread_pct = None
    if bid is not None and ask is not None and ask >= bid and (ask + bid) > 0:
        spread_pct = (ask - bid) / ((ask + bid) / 2.0) * 100.0
    pre_turnover = safe_div(pre_volume, supply_shares)
    pre_rv20 = safe_div(pre_volume, avg_volume_20)
    pre_high_fade_pct = pct_change(pre_price, pre_high)
    pre_dollar_volume = None if pre_price is None or pre_volume is None else pre_price * pre_volume
    regular_turnover = safe_div(regular_volume, supply_shares)
    after_gap_pct = pct_change(after_price, regular_close)
    after_turnover = safe_div(after_volume, supply_shares)
    after_high_fade_pct = pct_change(after_price, after_high)
    after_spread_pct = None
    if after_bid is not None and after_ask is not None and after_ask >= after_bid and (after_ask + after_bid) > 0:
        after_spread_pct = (after_ask - after_bid) / ((after_ask + after_bid) / 2.0) * 100.0

    passed: list[str] = []
    failed: list[str] = []
    unknown: list[str] = []
    risk_flags: list[str] = []

    if float_shares is not None and float_shares > 0:
        supply_gate = float_shares <= 15_000_000
    elif total_shares is not None and total_shares > 0:
        supply_gate = total_shares <= 10_000_000
    elif implied_total_shares is not None:
        supply_gate = implied_total_shares <= 10_000_000
    else:
        supply_gate = None

    structure_gates = {
        "security_type": security_ok,
        "listed_days>=20": None if listed_days is None else listed_days >= 20,
        "no_split_today": None if split_today is None else not split_today,
        "prev_close_0.30_5.00": None if prev_close is None else 0.30 <= prev_close <= 5.00,
        "median_dollar_volume_20<=1m": (
            None if median_dollar_volume_20 is None else median_dollar_volume_20 <= 1_000_000
        ),
        "tight_supply": supply_gate,
    }
    structure_ready, structure_failed, structure_unknown = evaluate_required_gates(
        structure_gates, passed, failed, unknown
    )

    # The new premarket field represents a point-in-time news/filing review. For
    # backward compatibility, old datasets may fall back to dilution_overhang.
    # A confirmed legacy dilution flag still overrides a clean premarket flag.
    supply_risk_fallback = premarket_supply_raw in (None, "")
    if dilution_risk is True or premarket_supply_risk is True:
        effective_supply_risk = True
    elif supply_risk_fallback:
        effective_supply_risk = dilution_risk
    else:
        effective_supply_risk = premarket_supply_risk

    hard_exclude = security_ok is False or split_today is True or effective_supply_risk is True
    above_vwap = None if last_price is None or vwap is None else last_price >= vwap
    execution_liquid = None if spread_pct is None else spread_pct <= 2.50
    regular_supply_confirmed = None if regular_turnover is None else regular_turnover >= 1.00
    supply_risk_clear = None if effective_supply_risk is None else not effective_supply_risk

    earnings_supported = after_catalyst_quality in {"EARNINGS_SUPPORTED", "OFFICIAL_EARNINGS", "EARNINGS"}
    low_supply_supported = after_supply_thesis in {"VERIFIED_LOW_SUPPLY", "LOW_SUPPLY_VERIFIED"}

    if is_after_hours:
        if earnings_supported:
            path_type = "AFTER_HOURS_EARNINGS"
        elif low_supply_supported:
            path_type = "AFTER_HOURS_LOW_SUPPLY"
        else:
            path_type = "NONE"
    elif official_gap_pct is not None and official_gap_pct >= 100:
        path_type = "CONVENTIONAL_GAP"
    elif official_gap_pct is not None and official_gap_pct < 20:
        path_type = "CPHI_SUBTYPE"
    elif official_gap_pct is None and pre_gap_pct is not None and pre_gap_pct >= 100:
        path_type = "CONVENTIONAL_GAP"
    else:
        path_type = "NONE"

    evidence_score = 0
    active_gap = official_gap_pct if official_gap_pct is not None else pre_gap_pct
    if active_gap is not None:
        evidence_score += 40 if active_gap >= 100 else 25 if active_gap >= 50 else 10 if active_gap >= 20 else 0
    if median_dollar_volume_20 is not None and median_dollar_volume_20 <= 1_000_000:
        evidence_score += 15
    if supply_gate is True:
        evidence_score += 20
    if pre_turnover is not None and pre_turnover >= 0.50:
        evidence_score += 15
    if spread_pct is not None and spread_pct <= 2.50:
        evidence_score += 10
    if is_after_hours and after_gap_pct is not None:
        evidence_score += 15 if after_gap_pct >= 50 else 10 if after_gap_pct >= 15 else 0
    if is_after_hours and after_turnover is not None and after_turnover >= 0.25:
        evidence_score += 10
    if earnings_supported or low_supply_supported:
        evidence_score += 10
    evidence_score = min(evidence_score, 100)
    if hard_exclude:
        evidence_score = 0

    if effective_supply_risk is True:
        status = "EXCLUDE"
        reason = "confirmed premarket share-supply risk"
    elif hard_exclude or structure_failed:
        status = "EXCLUDE"
        reason = "security type, split, or structural gate failed"
    elif halted is True:
        status = "WATCH"
        reason = "trading is halted; wait for resumption and rebuild execution gates"
    elif effective_supply_risk is None:
        status = "WAIT_DATA"
        reason = "premarket share-supply review is missing or unresolved"
    elif is_after_hours:
        after_hours_gates = {
            "after_gap>=15%": None if after_gap_pct is None else after_gap_pct >= 15.00,
            "after_turnover>=0.25": None if after_turnover is None else after_turnover >= 0.25,
            "after_spread<=3.5%": None if after_spread_pct is None else after_spread_pct <= 3.50,
            "after_high_fade>=-20%": (
                None if after_high_fade_pct is None else after_high_fade_pct >= -20.00
            ),
            "after_hours_route_verified": earnings_supported or low_supply_supported,
            "supply_risk_clear": supply_risk_clear,
        }
        after_ready, after_failed, after_unknown = evaluate_required_gates(
            after_hours_gates, passed, failed, unknown
        )
        if structure_ready and after_ready:
            status = "WATCH"
            reason = "qualified after-hours discovery; revalidate news, supply, spread, VWAP, and opening structure next session"
        elif after_failed:
            status = "WATCH"
            reason = "after-hours discovery has a failed liquidity, fade, catalyst, or supply-thesis gate"
        elif structure_unknown or after_unknown:
            status = "WAIT_DATA"
            reason = "after-hours discovery requires complete structure, liquidity, catalyst, and supply evidence"
        else:
            status = "WATCH"
            reason = "after-hours discovery is not eligible for direct execution"
    elif open_price is not None:
        if path_type == "CONVENTIONAL_GAP":
            execution_gates = {
                "last_price>=vwap": above_vwap,
                "regular_turnover>=1": regular_supply_confirmed,
                "spread<=2.5%": execution_liquid,
                "first_5m_structure": first_5m_confirmed,
                "supply_risk_clear": supply_risk_clear,
            }
            execution_ready, execution_failed, execution_unknown = evaluate_required_gates(
                execution_gates, passed, failed, unknown
            )
            if structure_ready and execution_ready:
                status = "EXECUTE"
                reason = "conventional official-gap and execution gates confirmed"
            elif execution_failed:
                status = "WATCH"
                reason = "conventional path has a failed execution or supply-risk gate"
            elif structure_unknown or execution_unknown:
                status = "WAIT_DATA"
                reason = "conventional path requires additional structure or execution data"
            else:
                status = "WATCH"
                reason = "conventional path is not executable"
        elif path_type == "CPHI_SUBTYPE":
            cphi_gates = {
                "last_price>=vwap": above_vwap,
                "regular_turnover>=1": regular_supply_confirmed,
                "turnover_expanding": turnover_expanding,
                "prior_abnormal_volume_warmup": prior_warmup,
                "spread<=2.5%": execution_liquid,
                "first_5m_structure": first_5m_confirmed,
                "supply_risk_clear": supply_risk_clear,
            }
            cphi_ready, cphi_failed, cphi_unknown = evaluate_required_gates(
                cphi_gates, passed, failed, unknown
            )
            if structure_ready and cphi_ready:
                status = "EXECUTE"
                reason = "CPHI subtype and execution gates confirmed"
            elif cphi_failed:
                status = "WATCH"
                reason = "CPHI subtype has a failed execution, warm-up, or supply-risk gate"
            elif structure_unknown or cphi_unknown:
                status = "WAIT_DATA"
                reason = "CPHI subtype requires additional warm-up, turnover, or execution data"
            else:
                status = "WATCH"
                reason = "CPHI subtype is not executable"
        elif structure_unknown:
            status = "WAIT_DATA"
            reason = "official gap is outside supported paths and structure data is incomplete"
        else:
            status = "WATCH"
            reason = "official gap is between CPHI and conventional model ranges"
    elif structure_unknown:
        status = "WAIT_DATA"
        reason = "required structural fields are missing"
    elif pre_gap_pct is None:
        status = "WAIT_DATA"
        reason = "premarket price or previous close is missing"
    elif pre_gap_pct >= 100:
        premarket_gates = {
            "pre_turnover>=0.5": None if pre_turnover is None else pre_turnover >= 0.50,
            "spread<=2.5%": execution_liquid,
            "pre_high_fade>=-20%": (
                None if pre_high_fade_pct is None else pre_high_fade_pct >= -20.00
            ),
            "supply_risk_clear": supply_risk_clear,
        }
        premarket_ready, premarket_failed, premarket_unknown = evaluate_required_gates(
            premarket_gates, passed, failed, unknown
        )
        if structure_ready and premarket_ready:
            status = "WAIT_OPEN"
            reason = "strong premarket candidate; wait for official-open confirmation"
        elif premarket_failed:
            status = "WATCH"
            reason = "strong pre-gap has a failed quality or supply-risk gate"
        elif premarket_unknown:
            status = "WAIT_DATA"
            reason = "strong pre-gap requires turnover, spread, fade, or dilution data"
        else:
            status = "WATCH"
            reason = "premarket path is not ready"
    elif pre_gap_pct >= 50:
        status = "WATCH"
        reason = "partial premarket candidate below the strong-gap threshold"
    else:
        status = "EXCLUDE"
        reason = "known event-strength gate failed"

    if halted is True:
        add_unique(risk_flags, "HALTED")
    if dilution_risk is True:
        add_unique(risk_flags, "DILUTION_OVERHANG")
    elif dilution_risk is None:
        add_unique(risk_flags, "DILUTION_UNKNOWN")
    if effective_supply_risk is True:
        add_unique(risk_flags, "SUPPLY_RISK_CONFIRMED")
        if premarket_supply_risk is True:
            add_unique(risk_flags, "PREMARKET_SUPPLY_RISK")
    elif effective_supply_risk is None:
        add_unique(risk_flags, "SUPPLY_RISK_UNKNOWN")
    if supply_risk_fallback:
        add_unique(risk_flags, "SUPPLY_RISK_LEGACY_FALLBACK")
    if is_after_hours:
        add_unique(risk_flags, "AFTER_HOURS_SIGNAL")
        if not earnings_supported and not low_supply_supported:
            add_unique(risk_flags, "AFTER_HOURS_UNVERIFIED_ROUTE")
        if after_spread_pct is not None and after_spread_pct > 3.50:
            add_unique(risk_flags, "AFTER_HOURS_WIDE_SPREAD")
    if post_split is True:
        add_unique(risk_flags, "POST_SPLIT")
    if supply_source != "float_shares":
        add_unique(risk_flags, "SUPPLY_PROXY")
    if unknown:
        add_unique(risk_flags, "MISSING_DATA")

    if status not in VALID_STATUSES:
        raise RuntimeError(f"internal error: invalid status {status!r}")
    if path_type not in VALID_PATH_TYPES:
        raise RuntimeError(f"internal error: invalid path type {path_type!r}")

    return {
        "symbol": symbol,
        "timestamp": row.get("timestamp") or "UNKNOWN",
        "market_status": row.get("market_status") or "UNKNOWN",
        "security_type": security_label,
        "status": status,
        "path_type": path_type,
        "reason": reason,
        "evidence_score": evidence_score,
        "pre_gap_pct": pre_gap_pct,
        "official_gap_pct": official_gap_pct,
        "pre_turnover": pre_turnover,
        "regular_turnover": regular_turnover,
        "after_gap_pct": after_gap_pct,
        "after_turnover": after_turnover,
        "after_spread_pct": after_spread_pct,
        "after_high_fade_pct": after_high_fade_pct,
        "spread_pct": spread_pct,
        "pre_high_fade_pct": pre_high_fade_pct,
        "pre_dollar_volume": pre_dollar_volume,
        "pre_rv20": pre_rv20,
        "supply_shares": supply_shares,
        "supply_source": supply_source,
        "passed": passed,
        "failed": failed,
        "unknown": unknown,
        "risk_flags": risk_flags,
        "premarket_supply_risk": (
            row.get("premarket_supply_risk")
            if row.get("premarket_supply_risk") not in (None, "")
            else "UNKNOWN"
        ),
        "effective_supply_risk": effective_supply_risk,
        "supply_risk_type": supply_risk_type,
        "supply_risk_source": supply_risk_source,
        "supply_risk_checked_at": supply_risk_checked_at,
        "dilution_overhang": row.get("dilution_overhang") if row.get("dilution_overhang") not in (None, "") else "UNKNOWN",
        "catalyst": row.get("catalyst") or "UNKNOWN",
    }


def load_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or not path.is_file():
        raise InputError(f"input file does not exist: {path}")
    suffix = path.suffix.lower()
    try:
        if suffix == ".csv":
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                return list(csv.DictReader(handle))
        if suffix == ".json":
            with path.open("r", encoding="utf-8-sig") as handle:
                data = json.load(handle)
            if isinstance(data, dict) and isinstance(data.get("candidates"), list):
                data = data["candidates"]
            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                raise InputError("JSON must be a list of objects or {'candidates': [...]} ")
            return data
    except (OSError, csv.Error, json.JSONDecodeError) as exc:
        raise InputError(f"failed to read {path}: {exc}") from exc
    raise InputError("input must be .csv or .json")


def fmt(value: float | None, suffix: str = "") -> str:
    return "UNKNOWN" if value is None else f"{value:,.2f}{suffix}"


def markdown(results: Iterable[dict[str, Any]]) -> str:
    rows = sorted(results, key=lambda item: (-item["evidence_score"], item["symbol"]))
    output = [
        "| Symbol | Status | Path | Score | Pre-gap | Open-gap | After-gap | Pre-turnover | After-turnover | Spread | After-spread | Risks | Unknown |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for item in rows:
        output.append(
            "| {symbol} | {status} | {path} | {score} | {pre_gap} | {open_gap} | {after_gap} | {turnover} | {after_turnover} | {spread} | {after_spread} | {risks} | {unknown} |".format(
                symbol=item["symbol"],
                status=item["status"],
                path=item["path_type"],
                score=item["evidence_score"],
                pre_gap=fmt(item["pre_gap_pct"], "%"),
                open_gap=fmt(item["official_gap_pct"], "%"),
                after_gap=fmt(item["after_gap_pct"], "%"),
                turnover=fmt(item["pre_turnover"], "x"),
                after_turnover=fmt(item["after_turnover"], "x"),
                spread=fmt(item["spread_pct"], "%"),
                after_spread=fmt(item["after_spread_pct"], "%"),
                risks=", ".join(item["risk_flags"]) or "-",
                unknown=", ".join(item["unknown"]) or "-",
            )
        )
    return "\n".join(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="CSV or JSON candidate file")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        rows = load_rows(args.input)
        if not rows:
            raise InputError("input contains no candidate rows")
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
