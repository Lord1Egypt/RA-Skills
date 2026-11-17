"""
inventory.py — derived inventory and refill tracking (PR 8b, #10).

Never a stored counter: what is on hand is always DERIVED from events —

    restocked{qty}  qty inventory units added (the first one starts tracking)
    counted{qty}    absolute recount: on hand is qty at that instant
    taken           each effective dose consumes inventory (an undone taken
                    stops counting, so undo restores stock automatically;
                    skipped and missed consume nothing)

Inventory is kept in the med's `inventory_unit` (vial, tablet, pen, mL, …).
What one prescribed dose consumes, in that unit, comes from (first match):

    1. doses_per_unit (explicit)                → 1 / doses_per_unit
    2. dose unit == inventory_unit (2 tablet)   → the dose amount
    3. dose in syringe units, inventory in mL   → units / units-per-mL
    4. inventory in vials, dose in mcg/mg, and a
       logged mix (reconstitution)              → dose mcg / vial mcg

A partial dose (`--dose-taken 10units`) consumes its share of a full one.
"""

import math
import re
from typing import Optional

import reconstitution
from clock import parse_instant

# "10units", "10 units", "250mcg", "0.25 mg", "2" — a number, optional unit
_AMOUNT = re.compile(r"^\s*(\d+(?:\.\d+)?|\.\d+)\s*([^\d\s.][^\d]*)?\s*$")

_ALIASES = {
    "u": "units", "unit": "units", "units": "units",
    "ml": "ml", "milliliter": "ml", "milliliters": "ml",
    "mcg": "mcg", "ug": "mcg", "µg": "mcg", "μg": "mcg", "mg": "mg",
    "tab": "tablet", "tabs": "tablet", "tablet": "tablet", "tablets": "tablet",
    "pill": "pill", "pills": "pill", "capsule": "capsule", "capsules": "capsule",
    "vial": "vial", "vials": "vial", "pen": "pen", "pens": "pen",
}
_MCG_PER = {"mcg": 1.0, "mg": 1000.0}


def norm_unit(unit) -> Optional[str]:
    if unit is None:
        return None
    u = str(unit).strip().lower()
    if not u:
        return None
    if u in _ALIASES:
        return _ALIASES[u]
    return u[:-1] if u.endswith("s") and len(u) > 1 else u


def parse_amount(text) -> Optional[tuple]:
    """'10 units' → (10.0, 'units'); '250mcg' → (250.0, 'mcg'); '2' → (2.0, None)."""
    m = _AMOUNT.match(str(text or ""))
    if not m:
        return None
    value = float(m.group(1))
    if not math.isfinite(value) or value <= 0:
        return None
    return value, norm_unit(m.group(2))


def _prescribed(med: dict) -> Optional[tuple]:
    p = parse_amount(med.get("dose"))
    if p is None:
        return None
    return p[0], norm_unit(med.get("unit"))


def taken_scale(med: dict, dose_taken) -> float:
    """Share of the prescribed dose actually taken: 1.0 when no amount was
    given, or when it can't be compared with the prescription."""
    if not dose_taken:
        return 1.0
    got, presc = parse_amount(dose_taken), _prescribed(med)
    if got is None or presc is None:
        return 1.0
    amount, unit = got
    unit = unit or presc[1]
    if unit in _MCG_PER and presc[1] in _MCG_PER:
        return amount * _MCG_PER[unit] / (presc[0] * _MCG_PER[presc[1]])
    if unit == presc[1]:
        return amount / presc[0]
    return 1.0


def per_dose(med: dict, events, at=None) -> Optional[float]:
    """Inventory units one prescribed dose consumes at `at`, or None when
    it can't be worked out (the line then asks for doses_per_unit)."""
    inv = norm_unit(med.get("inventory_unit"))
    if inv is None:
        return None
    dpu = med.get("doses_per_unit")
    if dpu:
        return 1.0 / float(dpu)
    presc = _prescribed(med)
    if presc is None:
        return None
    amount, unit = presc
    if unit == inv:
        return amount
    if inv == "ml" and unit == "units":
        upm = reconstitution.SYRINGE_UNITS_PER_ML.get(reconstitution.syringe_of(med))
        return amount / upm if upm else None
    if inv == "vial":
        mcg = reconstitution.dose_mcg(med)
        mix = reconstitution.current_mix(events, med["id"], at)
        if mcg is not None and mix is not None:
            try:
                vial_mcg = float(mix["vial_mg"]) * 1000.0
            except (KeyError, TypeError, ValueError):
                return None
            return mcg / vial_mcg if vial_mcg > 0 else None
    return None


def _ts(e):
    return parse_instant(e["ts_utc"])


def on_hand(med: dict, events, now) -> Optional[float]:
    """Inventory units on hand at `now`, or None when the med isn't tracked
    (no inventory_unit or no restock/count yet) or a dose can't be costed."""
    if not med.get("inventory_unit"):
        return None
    mid = med["id"]
    stock = sorted((e for e in events
                    if e.get("med_id") == mid
                    and e.get("event") in ("restocked", "counted")
                    and _ts(e) <= now), key=_ts)
    if not stock:
        return None
    counts = [i for i, e in enumerate(stock) if e["event"] == "counted"]
    if counts:
        base = stock[counts[-1]]
        start, qty, later = _ts(base), float(base["qty"]), stock[counts[-1] + 1:]
    else:
        start, qty, later = _ts(stock[0]), 0.0, stock
    qty += sum(float(e["qty"]) for e in later if e["event"] == "restocked")

    undone = {e.get("ref") for e in events
              if e.get("event") == "undone" and e.get("med_id") == mid}
    # history is never trimmed: cost each dose against this med's mixes
    # only, not a rescan of every event
    mixes = [e for e in events
             if e.get("event") == "reconstituted" and e.get("med_id") == mid]
    for e in events:
        if e.get("event") != "taken" or e.get("med_id") != mid or e.get("id") in undone:
            continue
        at = parse_instant(e.get("taken_at_utc") or e["ts_utc"])
        if not (start <= at <= now):
            continue
        cost = per_dose(med, mixes, at)
        if cost is None:
            return None
        qty -= cost * taken_scale(med, e.get("dose_taken"))
    return qty


def doses_per_day(med: dict) -> Optional[float]:
    sched = med.get("schedule") or {}
    freq = sched.get("frequency")
    if freq == "interval":
        return 24.0 / float(sched["interval_hours"])
    if freq in ("once_daily", "twice_daily"):
        return float(len(sched.get("times") or []))
    if freq == "weekly":
        days = sched.get("day_of_week") or []
        n_days = 1 if isinstance(days, str) else len(days)
        return len(sched.get("times") or []) * n_days / 7.0
    return None   # as_needed: no steady burn rate


def days_left(med: dict, events, now) -> Optional[float]:
    qty = on_hand(med, events, now)
    cost = per_dose(med, events, now)
    rate = doses_per_day(med)
    if qty is None or not cost or not rate:
        return None
    return max(qty, 0.0) / (cost * rate)


def _fmt(x: float) -> str:
    return f"{x:.1f}".rstrip("0").rstrip(".")


def _unit_label(unit: str, qty: float) -> str:
    if abs(qty - 1) < 1e-9 or unit.lower() == "ml" or unit.endswith("s"):
        return unit
    return unit + "s"


def status_line(med: dict, events, now) -> Optional[str]:
    """'~1.4 vials left (~28 days) — reorder', or None when untracked."""
    if not med.get("inventory_unit"):
        return None
    if not any(e.get("med_id") == med["id"] and e.get("event") in ("restocked", "counted")
               and _ts(e) <= now for e in events):
        return None
    qty = on_hand(med, events, now)
    unit = med["inventory_unit"]
    if qty is None or per_dose(med, events, now) is None:
        hint = "log the vial mix or " if norm_unit(unit) == "vial" else ""
        return f"can't tell how much a dose uses — {hint}set doses_per_unit"
    if qty <= 1e-9:
        return f"out of {_unit_label(unit, 2)} — restock"
    line = f"~{_fmt(qty)} {_unit_label(unit, qty)} left"
    days = days_left(med, events, now)
    if days is not None:
        line += f" (~{int(days)} days)"
        threshold = med.get("reorder_when_below_days")
        if threshold and days < threshold:
            line += " — reorder"
    return line
