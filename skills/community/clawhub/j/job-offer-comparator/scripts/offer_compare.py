#!/usr/bin/env python3
"""offer_compare.py — apples-to-apples comparison of job offers.

Salary alone lies: a $95k remote offer can beat a $115k offer with a
4h/day commute, no 401(k) match, and $600/mo health premiums. This tool
computes TRUE total compensation —

    base + expected bonus + retirement match (capped) + equity
    (risk-discounted) + other benefits + relocation (one-time)
    − health premiums − commute cost, then ÷ cost-of-living index —

plus effective hourly rate on REAL hours (contracted + overtime norm +
commute), PTO valuation, and a break-even base salary usable as a
negotiation target. Every assumption is printed, never hidden.

Deterministic, stdlib-only, no network. Gross-of-tax comparison model —
not tax advice.

Usage:
    python3 scripts/offer_compare.py compare --file offers.json [--json]
    python3 scripts/offer_compare.py compare \
        --offer '{"name":"A","base":95000}' \
        --offer '{"name":"B","base":115000,"col_index":115}'
    python3 scripts/offer_compare.py breakeven --file offers.json [--json]
    python3 scripts/offer_compare.py annotate
    python3 scripts/offer_compare.py example > offers.json
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Optional

__version__ = "1.0.0"

# ---------------------------------------------------------------------------
# Model constants — printed in every report, never hidden.
# ---------------------------------------------------------------------------
WEEKS_PER_YEAR = 52
WORK_DAYS_PER_WEEK = 5
WORK_DAYS_PER_YEAR = WEEKS_PER_YEAR * WORK_DAYS_PER_WEEK  # 260
AVG_COMMUTE_SPEED_KMH = 28.0        # door-to-door average, incl. stops/lights
DEFAULT_COMMUTE_COST_PER_KM = 0.30  # IRS-style all-in car running cost
DEFAULT_EQUITY_RISK = 0.50          # illiquid private-company grant discount

ASSUMPTIONS = [
    f"Commute time = 2 x days/week x (km each way / {AVG_COMMUTE_SPEED_KMH:.0f} km/h "
    f"door-to-door average speed).",
    f"Commute cost = km x 2 x days x {WEEKS_PER_YEAR} x cost-per-km "
    f"(default ${DEFAULT_COMMUTE_COST_PER_KM:.2f}/km) + monthly parking/transit x 12.",
    "Bonus = base x bonus_pct. Enter the EXPECTED/target number, not the "
    "'up to' maximum (a 10% target with 50% attainment ≈ 5% expected).",
    "Retirement match = min(base x match_pct, annual cap). Caps bind on high "
    "salaries — 6% of $115k is $6,900 but a $4,000 cap pays $4,000.",
    f"Equity expected value = annual grant value x (1 - risk). Risk defaults to "
    f"{DEFAULT_EQUITY_RISK:.2f} (private/illiquid); use ~0.0-0.2 for liquid "
    "public-company RSUs.",
    "Cost of living: true comp = regional comp / (col_index / 100). "
    "100 = your baseline city; 115 = 15% pricier.",
    f"Year = {WEEKS_PER_YEAR} working weeks, {WORK_DAYS_PER_YEAR} working days "
    f"({WEEKS_PER_YEAR} x {WORK_DAYS_PER_WEEK}).",
    "PTO value = PTO days x true daily rate. Informational only — leave is "
    "already paid inside base — use it to price PTO differences between offers.",
    "Relocation bonus is one-time; counted in first-year gross (flagged in the table).",
    "Gross-of-tax model: taxes, vesting schedules, and benefits quality are NOT "
    "modeled. This compares offers; it is not tax or investment advice.",
]

# ---------------------------------------------------------------------------
# Field registry — single source of truth for defaults, validation,
# `annotate` output, and the SKILL.md field table.
# Each: key, default, typical, where to find it, note.
# ---------------------------------------------------------------------------
FIELDS: list[dict[str, Any]] = [
    {"key": "name", "default": "REQUIRED", "typical": '"RemoteCo" / "BigCityBank"',
     "where": "Top of the offer letter (or invent a short label).",
     "note": "Must be unique across offers."},
    {"key": "base", "default": "REQUIRED", "typical": "60,000–250,000",
     "where": "The fixed annual salary line in the letter.",
     "note": "Annual gross base, before bonus/equity."},
    {"key": "bonus_pct", "default": "0.0", "typical": "0.05–0.20",
     "where": "Bonus section: 'target annual bonus of 10%'.",
     "note": "Fraction of base (0.10 = 10%). Use the expected/target value, not 'up to'."},
    {"key": "equity_annual_value", "default": "0", "typical": "0–40,000/yr",
     "where": "Equity section: annual RSU/option grant value at current valuation.",
     "note": "Per-year value of the grant (total grant ÷ vest years), $ per year."},
    {"key": "equity_risk", "default": "0.5", "typical": "0.0–0.8",
     "where": "Your judgment: 0.0–0.2 liquid public RSUs, 0.5 late private, "
              "0.8+ early startup.",
     "note": "Fraction of equity value you discount for illiquidity/failure risk."},
    {"key": "retirement_match_pct", "default": "0.0", "typical": "0.03–0.06",
     "where": "401(k)/pension: 'we match 100% of your first 6%'.",
     "note": "Match as a fraction of base (0.06 = 6%)."},
    {"key": "retirement_match_cap", "default": "none (uncapped)", "typical": "2,000–10,000",
     "where": "'up to $X per year' — often in the plan document, not the letter. Ask HR.",
     "note": "Annual $ cap on the employer match. Omit if none."},
    {"key": "health_premium_monthly", "default": "0.0", "typical": "50–800",
     "where": "Benefits sheet: YOUR monthly share (employee contribution) for your tier.",
     "note": "Monthly $ you pay, not the total premium. Per paycheck x paychecks works too."},
    {"key": "other_benefits_monthly", "default": "0.0", "typical": "0–500",
     "where": "Stipends: home office, phone, meals, commuter benefit, HSA seed.",
     "note": "Monthly $ value of recurring cash-ish perks you will actually use."},
    {"key": "pto_days", "default": "20", "typical": "10–30",
     "where": "'25 days of paid vacation'.",
     "note": "Use what you'll realistically take — 'unlimited' often means fewer."},
    {"key": "holidays", "default": "10", "typical": "8–15",
     "where": "The paid public holidays list.",
     "note": "Paid days off that don't come out of PTO."},
    {"key": "hours_per_week", "default": "40", "typical": "35–40",
     "where": "Contracted hours in the letter.",
     "note": "The contracted number; add reality via overtime_hours_per_week."},
    {"key": "overtime_hours_per_week", "default": "0", "typical": "0–15",
     "where": "Not in the letter — ask the team what a normal week looks like.",
     "note": "The unwritten overtime norm (unpaid or 'expected')."},
    {"key": "commute_km_each_way", "default": "0", "typical": "0–50",
     "where": "Map your door-to-door route at rush hour.",
     "note": "0 for fully remote. Metric: miles x 1.609."},
    {"key": "commute_days_per_week", "default": "5 if km>0 else 0", "typical": "3–5",
     "where": "Your schedule — hybrid? Count office days only.",
     "note": "Days you actually make the round trip."},
    {"key": "commute_cost_per_km", "default": "0.30", "typical": "0.05 (transit) – 0.50 (SUV)",
     "where": "Fuel + tires + service + depreciation per km; transit: fare ÷ km.",
     "note": "IRS-style all-in car rate ≈ $0.30/km is a fair default."},
    {"key": "monthly_parking_or_transit", "default": "0.0", "typical": "0–400",
     "where": "Parking spot price or monthly transit pass at the office.",
     "note": "Monthly $ on top of per-km cost."},
    {"key": "col_index", "default": "100", "typical": "85 (rural) – 130+ (SF/NYC)",
     "where": "Numbeo/BEA cost-of-living index, offer city vs your baseline = 100.",
     "note": "100 = baseline. 115 means the city is 15% pricier overall."},
    {"key": "relocation_bonus", "default": "0.0", "typical": "0–20,000",
     "where": "'One-time signing/relocation bonus' line.",
     "note": "One-time; included in first-year gross and flagged as such."},
]


class OfferError(Exception):
    """User-facing input error — printed cleanly, exit code 2."""


# ---------------------------------------------------------------------------
# Input normalization & validation
# ---------------------------------------------------------------------------
def _num(raw: dict[str, Any], key: str, default: Optional[float], *,
         lo: Optional[float] = 0.0, hi: Optional[float] = None,
         required: bool = False, ctx: str = "") -> Optional[float]:
    """Fetch key as a non-bool number, applying range/default rules."""
    label = f"{ctx}{key}" if ctx else key
    if key not in raw or raw[key] is None:
        if required:
            raise OfferError(f"{label}: required field is missing")
        return default
    v = raw[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise OfferError(f"{label}: must be a number, got {v!r}")
    v = float(v)
    if lo is not None and v < lo:
        raise OfferError(f"{label}: must be >= {lo}, got {v}")
    if hi is not None and v > hi:
        raise OfferError(f"{label}: must be <= {hi}, got {v}")
    return v


def normalize_offer(raw: Any, index: int) -> dict[str, Any]:
    """Validate one offer dict and apply all defaults. Returns a clean dict."""
    ctx = f"offer[{index}] " if index is not None else ""
    if not isinstance(raw, dict):
        raise OfferError(f"{ctx}must be a JSON object, got {type(raw).__name__}")

    name = raw.get("name")
    if not isinstance(name, str) or not name.strip():
        raise OfferError(f"{ctx}name: required non-empty string")
    name = name.strip()
    ctx = f"offer '{name}': "

    base = _num(raw, "base", None, required=True, lo=1.0, ctx=ctx)

    bonus_pct = _num(raw, "bonus_pct", 0.0, lo=0.0, hi=1.0, ctx=ctx)
    equity_val = _num(raw, "equity_annual_value", 0.0, lo=0.0, ctx=ctx)
    # equity_risk only matters when there IS equity; default discounts illiquid grants.
    equity_risk = _num(raw, "equity_risk", DEFAULT_EQUITY_RISK if equity_val > 0 else 0.0,
                       lo=0.0, hi=1.0, ctx=ctx)
    match_pct = _num(raw, "retirement_match_pct", 0.0, lo=0.0, hi=1.0, ctx=ctx)
    match_cap = _num(raw, "retirement_match_cap", None, lo=0.0, ctx=ctx)
    health_mo = _num(raw, "health_premium_monthly", 0.0, lo=0.0, ctx=ctx)
    other_mo = _num(raw, "other_benefits_monthly", 0.0, lo=0.0, ctx=ctx)
    pto = _num(raw, "pto_days", 20.0, lo=0.0, hi=366.0, ctx=ctx)
    holidays = _num(raw, "holidays", 10.0, lo=0.0, hi=366.0, ctx=ctx)
    hours = _num(raw, "hours_per_week", 40.0, lo=1.0, hi=168.0, ctx=ctx)
    overtime = _num(raw, "overtime_hours_per_week", 0.0, lo=0.0, hi=100.0, ctx=ctx)
    km = _num(raw, "commute_km_each_way", 0.0, lo=0.0, hi=20000.0, ctx=ctx)
    days_default = 5.0 if km > 0 else 0.0
    days = _num(raw, "commute_days_per_week", days_default, lo=0.0, hi=7.0, ctx=ctx)
    cost_km = _num(raw, "commute_cost_per_km", DEFAULT_COMMUTE_COST_PER_KM,
                   lo=0.0, hi=100.0, ctx=ctx)
    parking = _num(raw, "monthly_parking_or_transit", 0.0, lo=0.0, ctx=ctx)
    col = _num(raw, "col_index", 100.0, lo=1.0, hi=1000.0, ctx=ctx)
    relo = _num(raw, "relocation_bonus", 0.0, lo=0.0, ctx=ctx)

    if km > 0 and days == 0:
        raise OfferError(f"{ctx}commute_km_each_way > 0 but commute_days_per_week "
                         f"is 0 — set the days you commute")

    return {
        "name": name, "base": base, "bonus_pct": bonus_pct,
        "equity_annual_value": equity_val, "equity_risk": equity_risk,
        "retirement_match_pct": match_pct, "retirement_match_cap": match_cap,
        "health_premium_monthly": health_mo, "other_benefits_monthly": other_mo,
        "pto_days": pto, "holidays": holidays, "hours_per_week": hours,
        "overtime_hours_per_week": overtime, "commute_km_each_way": km,
        "commute_days_per_week": days, "commute_cost_per_km": cost_km,
        "monthly_parking_or_transit": parking, "col_index": col,
        "relocation_bonus": relo,
    }


def load_offers(file_path: Optional[str], inline: list[str],
                min_count: int = 2, exact: Optional[int] = None) -> list[dict]:
    """Load offers from --file (JSON array or {"offers": [...]}) plus any
    number of --offer inline JSON objects; validate and normalize."""
    raws: list[Any] = []
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as e:
            raise OfferError(f"--file {file_path}: not valid JSON ({e})")
        except OSError as e:
            raise OfferError(f"--file {file_path}: cannot read ({e.strerror})")
        if isinstance(data, dict) and "offers" in data:
            data = data["offers"]
        if not isinstance(data, list):
            raise OfferError(f"--file {file_path}: expected a JSON array of offers "
                             f"or an object with an 'offers' array")
        raws.extend(data)
    for i, blob in enumerate(inline):
        try:
            raws.append(json.loads(blob))
        except json.JSONDecodeError as e:
            raise OfferError(f"--offer #{i + 1}: not valid JSON ({e})")

    offers = [normalize_offer(r, i) for i, r in enumerate(raws)]

    if exact is not None and len(offers) != exact:
        raise OfferError(f"expected exactly {exact} offers, got {len(offers)}")
    if len(offers) < min_count:
        raise OfferError(f"need at least {min_count} offers to compare, got {len(offers)}")

    names = [o["name"] for o in offers]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise OfferError(f"duplicate offer names: {', '.join(sorted(dupes))} "
                         f"— names must be unique")
    return offers


# ---------------------------------------------------------------------------
# Compensation model — see references/compensation-model.md
# ---------------------------------------------------------------------------
def compute_offer(o: dict[str, Any]) -> dict[str, Any]:
    """All comp lines and derived metrics for one normalized offer."""
    base = o["base"]

    bonus = base * o["bonus_pct"]
    match_uncapped = base * o["retirement_match_pct"]
    cap = o["retirement_match_cap"]
    match = match_uncapped if cap is None else min(match_uncapped, cap)
    match_capped = cap is not None and match_uncapped > cap
    equity_ev = o["equity_annual_value"] * (1.0 - o["equity_risk"])
    other_annual = o["other_benefits_monthly"] * 12.0
    relo = o["relocation_bonus"]

    gross = base + bonus + match + equity_ev + other_annual + relo

    health_annual = o["health_premium_monthly"] * 12.0
    km2 = o["commute_km_each_way"] * 2.0
    commute_km_annual = km2 * o["commute_days_per_week"] * WEEKS_PER_YEAR
    commute_transport = commute_km_annual * o["commute_cost_per_km"]
    commute_parking = o["monthly_parking_or_transit"] * 12.0
    commute_cost = commute_transport + commute_parking
    commute_hours_week = (2.0 * o["commute_days_per_week"]
                          * (o["commute_km_each_way"] / AVG_COMMUTE_SPEED_KMH))

    risk_adjusted = gross - health_annual - commute_cost
    col_factor = o["col_index"] / 100.0
    true_comp = risk_adjusted / col_factor

    work_hours_week = o["hours_per_week"] + o["overtime_hours_per_week"]
    real_hours_week = work_hours_week + commute_hours_week
    effective_hourly = true_comp / (WEEKS_PER_YEAR * real_hours_week)

    true_daily_rate = true_comp / WORK_DAYS_PER_YEAR
    pto_value = o["pto_days"] * true_daily_rate

    return {
        "bonus": bonus,
        "retirement_match": match, "retirement_match_uncapped": match_uncapped,
        "match_capped": match_capped,
        "equity_ev": equity_ev,
        "other_benefits_annual": other_annual, "relocation_bonus": relo,
        "gross": gross,
        "health_annual": health_annual,
        "commute_km_annual": commute_km_annual,
        "commute_transport_annual": commute_transport,
        "commute_parking_annual": commute_parking,
        "commute_cost_annual": commute_cost,
        "commute_hours_week": commute_hours_week,
        "risk_adjusted": risk_adjusted,
        "col_factor": col_factor,
        "true_comp": true_comp,
        "work_hours_week": work_hours_week,
        "real_hours_week": real_hours_week,
        "effective_hourly": effective_hourly,
        "true_daily_rate": true_daily_rate,
        "pto_value": pto_value,
    }


def true_comp_at_base(offer: dict[str, Any], base: float) -> float:
    """True comp of `offer` if its base were `base` (all else equal).
    Monotone non-decreasing in base."""
    alt = dict(offer)
    alt["base"] = base
    return compute_offer(alt)["true_comp"]


def solve_breakeven_base(offer: dict[str, Any], target: float) -> float:
    """Bisection: base at which `offer` reaches `target` true comp.
    Handles the match-cap kink without closed-form tricks."""
    lo, hi = 1.0, max(offer["base"] * 3.0, 1_000_000.0)
    while true_comp_at_base(offer, hi) < target:
        hi *= 2.0
        if hi > 1e12:
            raise OfferError(f"offer '{offer['name']}': no sane base reaches the "
                             f"target true comp (check for huge deductions)")
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if true_comp_at_base(offer, mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------
def build_verdict(offers: list[dict], comps: list[dict]) -> dict[str, Any]:
    money_w = max(range(len(offers)), key=lambda i: comps[i]["true_comp"])
    hours_w = min(range(len(offers)), key=lambda i: comps[i]["real_hours_week"])
    hourly_w = max(range(len(offers)), key=lambda i: comps[i]["effective_hourly"])

    m, h = money_w, hours_w
    d_comp = comps[m]["true_comp"] - comps[h]["true_comp"]
    d_hours = comps[m]["real_hours_week"] - comps[h]["real_hours_week"]

    if m == h:
        trade_type = "dominates"
        marginal = None
    elif d_hours > 1e-9:
        trade_type = "sells_hours"
        marginal = d_comp / (WEEKS_PER_YEAR * d_hours)
    elif d_hours < -1e-9:
        trade_type = "wins_both"
        marginal = None
    else:
        trade_type = "money_at_equal_hours"
        marginal = None

    return {
        "money_winner": offers[m]["name"],
        "money_winner_true_comp": comps[m]["true_comp"],
        "hours_winner": offers[h]["name"],
        "hours_winner_real_week": comps[h]["real_hours_week"],
        "hourly_winner": offers[hourly_w]["name"],
        "hourly_winner_rate": comps[hourly_w]["effective_hourly"],
        "trade": {
            "type": trade_type,
            "delta_comp_per_year": d_comp,
            "delta_hours_per_week": d_hours,
            "marginal_hourly": marginal,
        },
    }


def verdict_text(offers: list[dict], comps: list[dict], v: dict[str, Any]) -> str:
    by_name = {offers[i]["name"]: comps[i] for i in range(len(offers))}
    mw, hw, ow = v["money_winner"], v["hours_winner"], v["hourly_winner"]
    lines = ["=== Verdict ==="]

    runner = min((c["true_comp"] for n, c in by_name.items() if n != mw), default=0.0)
    lines.append(f"Money (true comp): {mw} — ${by_name[mw]['true_comp']:,.0f}/yr "
                 f"(+${runner and (by_name[mw]['true_comp'] - runner) or 0:,.0f} vs best alternative)")

    hrs = sorted(by_name.items(), key=lambda kv: kv[1]["real_hours_week"])
    hrs_str = ", ".join(f"{n} {c['real_hours_week']:.1f}" for n, c in hrs)
    lines.append(f"Hours/life: {hw} — real h/week ranked: {hrs_str}")

    effs = sorted(by_name.items(), key=lambda kv: -kv[1]["effective_hourly"])
    effs_str = ", ".join(f"{n} ${c['effective_hourly']:,.2f}/h" for n, c in effs)
    lines.append(f"Effective hourly: {effs_str}")

    t = v["trade"]
    if t["type"] == "sells_hours":
        lines.append(
            f"The trade: {mw} pays +${t['delta_comp_per_year']:,.0f}/yr true comp but costs "
            f"{t['delta_hours_per_week']:.1f} h/week more of your life "
            f"= ${t['marginal_hourly']:,.2f}/h marginal — take it only if that "
            f"rate beats what an hour is worth to you.")
    elif t["type"] == "wins_both":
        lines.append(
            f"The trade: {mw} wins on money AND time (+${t['delta_comp_per_year']:,.0f}/yr "
            f"true comp, {-t['delta_hours_per_week']:.1f} h/week less than {hw}) — "
            f"it dominates on both axes.")
    elif t["type"] == "money_at_equal_hours":
        lines.append(
            f"The trade: {mw} pays +${t['delta_comp_per_year']:,.0f}/yr true comp "
            f"at essentially equal hours — take the money.")
    else:  # dominates (money winner is also hours winner)
        lines.append(
            f"The trade: {mw} leads on true comp, hours, and effective hourly — "
            f"the other offer needs non-money reasons (title, tech, people) to win.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def money(x: float) -> str:
    return ("-" if x < 0 else "") + f"${abs(x):,.0f}"


def hourly(x: float) -> str:
    return f"${x:,.2f}/h"


def render_table(headers: list[str], rows: list[tuple[str, list[str]]]) -> str:
    """Left-aligned label column, right-aligned value columns."""
    cols = len(headers) - 1
    widths = [len(headers[0])] + [len(headers[i + 1]) for i in range(cols)]
    for _label, vals in rows:
        widths[0] = max(widths[0], len(_label))
        for i, v in enumerate(vals):
            widths[i + 1] = max(widths[i + 1], len(v))
    sep = "  "
    out = [sep.join(headers[i].rjust(widths[i]) if i else headers[i].ljust(widths[i])
                    for i in range(cols + 1))]
    out.append(sep.join("-" * w for w in widths))
    for label, vals in rows:
        cells = [label.ljust(widths[0])] + [vals[i].rjust(widths[i + 1])
                                            for i in range(cols)]
        out.append(sep.join(cells))
    return "\n".join(out)


def render_compare(offers: list[dict], comps: list[dict]) -> str:
    names = [o["name"] for o in offers]
    headers = ["Annual $" ] + names
    out: list[str] = []

    out.append(f"=== Offer comparison: {len(offers)} offers ===\n")
    out.append("Assumptions (all inputs to the model):")
    for i, a in enumerate(ASSUMPTIONS, 1):
        out.append(f"  {i}. {a}")
    out.append("")

    def row(label, fn):
        return (label, [fn(c, o) for c, o in zip(comps, offers)])

    rows = [
        row("Base salary", lambda c, o: money(o["base"])),
        row("Bonus (expected)", lambda c, o: money(c["bonus"])),
        row("Retirement match (capped)",
            lambda c, o: money(c["retirement_match"]) + ("*" if c["match_capped"] else "")),
        row("Equity (risk-adjusted)", lambda c, o: money(c["equity_ev"])),
        row("Other benefits", lambda c, o: money(c["other_benefits_annual"])),
        row("Relocation (one-time)", lambda c, o: money(c["relocation_bonus"])),
        row("GROSS COMPENSATION", lambda c, o: money(c["gross"])),
        row("Health premiums", lambda c, o: money(-c["health_annual"])),
        row("Commute: transport", lambda c, o: money(-c["commute_transport_annual"])),
        row("Commute: parking/transit", lambda c, o: money(-c["commute_parking_annual"])),
        row("RISK-ADJUSTED COMP", lambda c, o: money(c["risk_adjusted"])),
        row("Cost-of-living index", lambda c, o: f"{o['col_index']:.0f}"),
        row("TRUE COMP (COL-adjusted)", lambda c, o: money(c["true_comp"])),
    ]
    out.append(render_table(headers, rows))
    out.append("* employer match capped below base x match_pct — the cap binds.\n")

    headers2 = ["Metric"] + names
    rows2 = [
        row("Work h/week (contract+OT)", lambda c, o: f"{c['work_hours_week']:.1f}"),
        row("Commute h/week", lambda c, o: f"{c['commute_hours_week']:.1f}"),
        row("REAL h/week (work+commute)", lambda c, o: f"{c['real_hours_week']:.1f}"),
        row("Effective hourly (true comp)", lambda c, o: hourly(c["effective_hourly"])),
        row("PTO days / holidays",
            lambda c, o: f"{o['pto_days']:.0f} / {o['holidays']:.0f}"),
        row("True daily rate", lambda c, o: money(c["true_daily_rate"])),
        row("PTO value @ true daily rate", lambda c, o: money(c["pto_value"])),
    ]
    out.append(render_table(headers2, rows2))
    out.append("")
    out.append(verdict_text(offers, comps, build_verdict(offers, comps)))
    return "\n".join(out)


def render_breakeven(offers: list[dict], comps: list[dict]) -> str:
    """Two offers: the base the lower-money offer needs to match the higher."""
    hi, lo = sorted(range(2), key=lambda i: -comps[i]["true_comp"])
    winner, loser = offers[hi], offers[lo]
    target = comps[hi]["true_comp"]
    need = solve_breakeven_base(loser, target)

    lines = ["=== Break-even: the negotiation target number ==="]
    lines.append(
        f"Goal: {loser['name']} must match {winner['name']}'s true comp of "
        f"{money(target)}/yr (COL-adjusted).")
    lines.append("")
    lines.append(f"  {loser['name']} currently: base {money(loser['base'])} "
                 f"-> true comp {money(comps[lo]['true_comp'])}/yr "
                 f"(COL index {loser['col_index']:.0f})")
    lines.append(f"  TARGET BASE: {money(need)}  "
                 f"({money(need - loser['base'])} / "
                 f"{(need / loser['base'] - 1) * 100:+.1f}% vs current base)")
    lines.append("")
    lines.append("  Verification: at that base,")
    alt = dict(loser)
    alt["base"] = need
    altc = compute_offer(alt)
    lines.append(f"    bonus {money(altc['bonus'])} + match {money(altc['retirement_match'])}"
                 + (" (still capped)" if altc["match_capped"] else "")
                 + f" -> true comp {money(altc['true_comp'])}/yr == target ✓")
    lines.append("")
    lines.append(
        f"  Say it out loud: \u201cMy other offer is worth {money(target)}/yr to me. "
        f"I need {money(need)} base to say yes.\u201d")

    # Symmetric info: how low could the winner go and still match the loser?
    floor = solve_breakeven_base(winner, comps[lo]["true_comp"])
    lines.append("")
    lines.append(
        f"  (Conversely, {winner['name']} could drop to {money(floor)} base and "
        f"still match {loser['name']} — anything above that is margin.)")
    lines.append("")
    lines.append("Notes: target is in the LOSER's city dollars (its COL index "
                 "already applied). Bonus %, match %/cap, and deductions are held "
                 "constant; taxes ignored.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
EXAMPLE_OFFERS: list[dict[str, Any]] = [
    {
        "name": "RemoteRocket",
        "base": 95000,
        "bonus_pct": 0.10,
        "equity_annual_value": 12000,
        "equity_risk": 0.5,
        "retirement_match_pct": 0.04,
        "retirement_match_cap": 10000,
        "health_premium_monthly": 150,
        "other_benefits_monthly": 100,
        "pto_days": 25,
        "holidays": 12,
        "hours_per_week": 40,
        "overtime_hours_per_week": 0,
        "commute_km_each_way": 0,
        "commute_days_per_week": 0,
        "commute_cost_per_km": 0.30,
        "monthly_parking_or_transit": 0,
        "col_index": 100,
        "relocation_bonus": 0,
    },
    {
        "name": "BigCityBank",
        "base": 115000,
        "bonus_pct": 0.15,
        "equity_annual_value": 0,
        "retirement_match_pct": 0.06,
        "retirement_match_cap": 4000,
        "health_premium_monthly": 600,
        "other_benefits_monthly": 0,
        "pto_days": 15,
        "holidays": 10,
        "hours_per_week": 40,
        "overtime_hours_per_week": 5,
        "commute_km_each_way": 30,
        "commute_days_per_week": 5,
        "commute_cost_per_km": 0.30,
        "monthly_parking_or_transit": 250,
        "col_index": 115,
        "relocation_bonus": 8000,
    },
]


def cmd_example(_args: argparse.Namespace) -> int:
    print(json.dumps(EXAMPLE_OFFERS, indent=2))
    return 0


def cmd_annotate(_args: argparse.Namespace) -> int:
    print("=== Offer field reference ===")
    print("Fill one JSON object per offer (see `example` for a filled sample).")
    print("Only `name` and `base` are required; everything else has a default.\n")
    for f in FIELDS:
        print(f"  {f['key']}")
        print(f"    default:  {f['default']}")
        print(f"    typical:  {f['typical']}")
        print(f"    find it:  {f['where']}")
        print(f"    note:     {f['note']}")
    print("\nReading an offer letter like an analyst:")
    print("  - Bonus: the letter says 'up to 15%'. History pays 60% of target ->")
    print("    enter 0.09, not 0.15. Expected value, not the brochure.")
    print("  - Retirement match: '100% match on first 6%, max $4,000/yr' ->")
    print("    retirement_match_pct 0.06, retirement_match_cap 4000. The cap is")
    print("    usually in the plan summary, not the letter — ask HR.")
    print("  - Health premiums: use YOUR monthly share (box on the benefits")
    print("    sheet), not the total plan premium. $600/mo = $7,200/yr pre-tax.")
    print("  - Equity: private company? equity_risk 0.5-0.8. Liquid RSUs that")
    print("    vest monthly? 0.0-0.1. You are pricing illiquidity + failure risk.")
    print("  - Commute: door-to-door at rush hour, both ways, metric km.")
    print("  - COL index: pick YOUR baseline city = 100 (usually where you live")
    print("    now), then index each offer city against it (Numbeo is fine).")
    return 0


def _round_floats(obj: Any) -> Any:
    if isinstance(obj, float):
        return round(obj, 4)
    if isinstance(obj, dict):
        return {k: _round_floats(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_round_floats(v) for v in obj]
    return obj


def cmd_compare(args: argparse.Namespace) -> int:
    offers = load_offers(args.file, args.offer, min_count=2)
    comps = [compute_offer(o) for o in offers]
    if args.json:
        payload = {
            "meta": {"version": __version__, "assumptions": ASSUMPTIONS},
            "offers": [dict(o, **_round_floats(c)) for o, c in zip(offers, comps)],
            "verdict": _round_floats(build_verdict(offers, comps)),
        }
        print(json.dumps(_round_floats(payload), indent=2))
    else:
        print(render_compare(offers, comps))
    return 0


def cmd_breakeven(args: argparse.Namespace) -> int:
    offers = load_offers(args.file, args.offer, min_count=2, exact=2)
    comps = [compute_offer(o) for o in offers]
    hi, lo = sorted(range(2), key=lambda i: -comps[i]["true_comp"])
    winner, loser = offers[hi], offers[lo]
    target = comps[hi]["true_comp"]
    need = solve_breakeven_base(loser, target)
    floor = solve_breakeven_base(winner, comps[lo]["true_comp"])
    if args.json:
        payload = {
            "meta": {"version": __version__, "assumptions": ASSUMPTIONS},
            "target_true_comp": round(target, 2),
            "winner": winner["name"],
            "loser": loser["name"],
            "loser_current_base": loser["base"],
            "loser_target_base": round(need, 2),
            "raise_needed": round(need - loser["base"], 2),
            "raise_needed_pct": round(need / loser["base"] - 1, 6),
            "winner_floor_base": round(floor, 2),
        }
        print(json.dumps(payload, indent=2))
    else:
        print(render_breakeven(offers, comps))
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="offer_compare.py",
        description="Apples-to-apples job offer comparison: true total comp, "
                    "effective hourly on real hours, break-even negotiation target.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("compare", help="side-by-side true-comp comparison (min 2 offers)")
    _add_input_args(sp)
    sp.add_argument("--json", action="store_true", help="machine-readable output")

    sp = sub.add_parser("breakeven", help="base the lower offer needs to match (exactly 2)")
    _add_input_args(sp)
    sp.add_argument("--json", action="store_true", help="machine-readable output")

    sub.add_parser("annotate", help="explain every field + where to find it in the letter")
    sub.add_parser("example", help="print a filled sample offers.json to copy")

    args = p.parse_args(argv)
    try:
        if args.cmd == "compare":
            return cmd_compare(args)
        if args.cmd == "breakeven":
            return cmd_breakeven(args)
        if args.cmd == "annotate":
            return cmd_annotate(args)
        if args.cmd == "example":
            return cmd_example(args)
    except OfferError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


def _add_input_args(sp: argparse.ArgumentParser) -> None:
    sp.add_argument("--file", metavar="OFFERS.json",
                    help="JSON file: array of offer objects (or {'offers': [...]})")
    sp.add_argument("--offer", action="append", default=[], metavar="JSON",
                    help="one offer as inline JSON; repeat the flag (min 2 offers)")


if __name__ == "__main__":
    sys.exit(main())
