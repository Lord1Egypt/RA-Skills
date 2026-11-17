"""
reconstitution.py — syringe-unit math for reconstituted injectables (PR 8a, #10).

A mix is an EVENT (`reconstituted{vial_mg, diluent_ml}` in history.jsonl),
never a stored field: the latest mix at or before an instant is the one in
use, so a re-mix mid-course just works and history knows which
concentration was active for every past dose.

    conc_mg_per_mL = vial_mg / diluent_ml
    volume_mL      = dose_mcg / (conc_mg_per_mL × 1000)
    units          = volume_mL × 100 (U-100) or × 50 (U-50)

Hard line: this computes units for a dose the USER chose. It never
suggests a dose.
"""

import math
from dataclasses import dataclass
from typing import Optional

from clock import parse_instant

SYRINGE_UNITS_PER_ML = {"U-100": 100, "U-50": 50}
DEFAULT_SYRINGE = "U-100"

ROUNDING_WARN = 0.05      # warn when whole-unit rounding is off by more than 5%
VOLUME_WARN_ML = 0.5      # more than half a 1 mL syringe → double-check the mix

_MCG_PER = {"mcg": 1, "ug": 1, "µg": 1, "μg": 1, "mg": 1000}


@dataclass(frozen=True)
class Draw:
    syringe: str
    conc_mg_per_ml: float
    volume_ml: float
    exact_units: float
    units: int
    doses_per_vial: float
    warnings: tuple


def dose_mcg(med: dict) -> Optional[float]:
    """The med's prescribed dose in mcg, or None when it isn't a mass dose."""
    factor = _MCG_PER.get(str(med.get("unit", "")).strip().lower())
    if factor is None:
        return None
    try:
        amount = float(med.get("dose"))
    except (TypeError, ValueError):
        return None
    if not math.isfinite(amount) or amount <= 0:
        return None
    return amount * factor


def syringe_of(med: dict) -> str:
    return med.get("syringe") or DEFAULT_SYRINGE


def compute(dose_mcg_: float, vial_mg: float, diluent_ml: float,
            syringe: str = DEFAULT_SYRINGE) -> Draw:
    """Units to draw for dose_mcg_ from a vial_mg vial mixed with diluent_ml."""
    conc = vial_mg / diluent_ml
    volume = dose_mcg_ / (conc * 1000.0)
    # round(…, 6) strips float noise (10.000000000000002) before whole-unit rounding
    exact = round(volume * SYRINGE_UNITS_PER_ML[syringe], 6)
    units = int(math.floor(exact + 0.5))
    warnings = []
    if units == 0:
        warnings.append(f"This dose is {exact:.2f} units — too small to measure "
                        f"on a {syringe} syringe. Double-check the mix.")
    elif abs(units - exact) / exact > ROUNDING_WARN:
        warnings.append(f"Rounding to {units} units is "
                        f"{abs(units - exact) / exact:.0%} off the exact {exact:.1f}.")
    if volume > VOLUME_WARN_ML:
        warnings.append(f"That's {volume:.2f} mL per dose — more than half a 1 mL "
                        "syringe. Double-check the vial mg and diluent mL.")
    return Draw(syringe=syringe, conc_mg_per_ml=conc, volume_ml=volume,
                exact_units=exact, units=units,
                doses_per_vial=vial_mg * 1000.0 / dose_mcg_,
                warnings=tuple(warnings))


def current_mix(events, med_id: str, at=None) -> Optional[dict]:
    """The latest `reconstituted` event for med_id at or before `at`."""
    best, best_ts = None, None
    for e in events:
        if e.get("event") != "reconstituted" or e.get("med_id") != med_id:
            continue
        ts = parse_instant(e["ts_utc"])
        if at is not None and ts > at:
            continue
        if best_ts is None or ts >= best_ts:
            best, best_ts = e, ts
    return best


def med_draw(med: dict, events, at=None) -> Optional[Draw]:
    """The draw for the med's prescribed dose under its current mix, or None."""
    mcg = dose_mcg(med)
    if mcg is None:
        return None
    mix = current_mix(events, med["id"], at)
    if mix is None:
        return None
    # A malformed mix (hand-edited history) must never break the reminder
    # itself — the tick isolates faults per med, so a raise here would
    # silence every reminder for this med. Fall back to the plain dose.
    try:
        vial_mg, diluent_ml = float(mix["vial_mg"]), float(mix["diluent_ml"])
    except (KeyError, TypeError, ValueError):
        return None
    if not (math.isfinite(vial_mg) and math.isfinite(diluent_ml)
            and vial_mg > 0 and diluent_ml > 0):
        return None
    if syringe_of(med) not in SYRINGE_UNITS_PER_ML:
        return None
    return compute(mcg, vial_mg, diluent_ml, syringe_of(med))


def units_phrase(draw: Draw) -> str:
    """'10 units', or '6 units (exact 6.4)' when rounding changed the value."""
    unit_word = "unit" if draw.units == 1 else "units"
    if abs(draw.units - draw.exact_units) < 0.05:
        return f"{draw.units} {unit_word}"
    return f"{draw.units} {unit_word} (exact {draw.exact_units:.1f})"


def fmt_num(x: float, places: int = 2) -> str:
    """2.5 → '2.5', 5.0 → '5', 4.166666 → '4.17'."""
    return f"{x:.{places}f}".rstrip("0").rstrip(".")
