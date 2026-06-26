#!/usr/bin/env python3
"""
health_tracker.py — Sick-Kid Medication & Symptom Tracker

Tracks as-needed medication doses, fever readings, and symptoms for each child.
All data stored in household/:
  health_config.json — kid profiles (name, weight) — updatable via WhatsApp
  health_log.json    — append-only chronological event log per child

No external dependencies beyond the Python standard library.

Medications supported:
  - Tylenol / acetaminophen: 10–15 mg/kg, every 4h min, max 5 doses/24h
      Children's: 160 mg / 5 mL  (32 mg/mL)
      Infants':    80 mg / 0.8 mL (100 mg/mL) ← more concentrated, separate variant
  - Ibuprofen / Motrin / Advil: 5–10 mg/kg, every 6h min, max 4 doses/24h
      Children's: 100 mg / 5 mL  (20 mg/mL)

Units: parents give doses in mL; internals store mg. Both always shown in output.
"""
from __future__ import annotations

import json
import os
import re

from utils import write_json_atomic
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo


# ─── Paths ─────────────────────────────────────────────────────────────────────

from core.config_loader import SKILL_DIR
HOUSEHOLD_DIR   = os.path.join(SKILL_DIR, "household")
HEALTH_CFG_PATH = os.path.join(HOUSEHOLD_DIR, "health_config.json")
HEALTH_LOG_PATH = os.path.join(HOUSEHOLD_DIR, "health_log.json")


# ─── Timezone helper ───────────────────────────────────────────────────────────

def _tz() -> ZoneInfo:
    try:
        from core.config_loader import config  # noqa: PLC0415
        return ZoneInfo(config.timezone)
    except Exception:
        return ZoneInfo("America/Los_Angeles")


def _now() -> datetime:
    return datetime.now(_tz())


# ─── Medication Definitions ────────────────────────────────────────────────────
#
# Each medication has a `concentrations` dict keyed by variant name.
# "default" points to the variant to use when the parent's phrasing is ambiguous.
# mg_per_ml is the authoritative conversion factor for that variant.

MEDICATIONS: dict = {
    "acetaminophen": {
        "canonical":       "Tylenol",
        "dose_min_per_kg": 10,
        "dose_max_per_kg": 15,
        "interval_hours":  4,
        "max_doses_24h":   5,
        "alternate":       "ibuprofen",
        "concentrations": {
            "children": {
                "mg_per_ml": 32.0,           # 160 mg / 5 mL
                "label":     "Children's Tylenol (160mg/5mL)",
                "short":     "Children's",
            },
            "infants": {
                "mg_per_ml": 100.0,          # 80 mg / 0.8 mL
                "label":     "Infants' Tylenol (80mg/0.8mL)",
                "short":     "Infants'",
            },
            "default": "children",
        },
        "synonyms": [
            "tylenol", "tylenol kids", "children's tylenol", "childrens tylenol",
            "children tylenol", "kids tylenol", "acetaminophen", "paracetamol",
            "infant tylenol", "infants tylenol", "infants' tylenol", "baby tylenol",
        ],
    },
    "ibuprofen": {
        "canonical":       "Ibuprofen",
        "dose_min_per_kg": 5,
        "dose_max_per_kg": 10,
        "interval_hours":  6,
        "max_doses_24h":   4,
        "alternate":       "acetaminophen",
        "concentrations": {
            "children": {
                "mg_per_ml": 20.0,           # 100 mg / 5 mL
                "label":     "Children's Ibuprofen (100mg/5mL)",
                "short":     "Children's",
            },
            "default": "children",
        },
        "synonyms": [
            "ibuprofen", "motrin", "advil", "children's motrin", "childrens motrin",
            "children motrin", "children's advil", "childrens advil", "children advil",
            "kids motrin", "kids advil", "ibuprofen kids", "infant motrin", "infant advil",
        ],
    },
}


def _normalize_med(name: str) -> Optional[str]:
    """Map any synonym → canonical key ('acetaminophen' or 'ibuprofen')."""
    nl = name.lower().strip()
    for key, med in MEDICATIONS.items():
        if nl == key or nl in med["synonyms"]:
            return key
    # Fuzzy substring fallback
    for key, med in MEDICATIONS.items():
        for syn in med["synonyms"]:
            if syn in nl or nl in syn:
                return key
    return None


def _get_concentration(med_key: str, medication_name: str) -> dict:
    """
    Return the concentration dict for a medication given the parent's phrasing.
    Detects 'infant' / 'infants' in the name to select the more-concentrated
    Infants' Tylenol variant; everything else uses the default (Children's).
    """
    med   = MEDICATIONS[med_key]
    concs = med.get("concentrations", {})
    nl    = medication_name.lower()
    if med_key == "acetaminophen" and re.search(r"\binfant", nl):
        return concs["infants"]
    return concs.get(concs["default"], {})


def _ml_to_mg(ml: float, conc: dict) -> float:
    return ml * conc["mg_per_ml"]


def _mg_to_ml(mg: float, conc: dict) -> float:
    return mg / conc["mg_per_ml"]


def _fmt_dose(dose_mg: float, dose_ml: Optional[float], conc: dict,
              ml_primary: bool = True) -> str:
    """
    Format a dose for display, always showing both units when possible.
    ml_primary=True  → "5mL (160mg)"  (parent said mL)
    ml_primary=False → "160mg (5mL)"  (parent said mg)
    Falls back to mg-only if no concentration data.
    """
    if dose_ml is not None:
        if ml_primary:
            return f"{_fmt_ml(dose_ml)} ({dose_mg:.0f}mg)"
        return f"{dose_mg:.0f}mg ({_fmt_ml(dose_ml)})"
    if conc:
        ml = _mg_to_ml(dose_mg, conc)
        return f"{dose_mg:.0f}mg ({_fmt_ml(ml)})"
    return f"{dose_mg:.0f}mg"


def _fmt_ml(ml: float) -> str:
    """Format mL cleanly: '5mL' not '5.000mL', '0.8mL' not '0.80000mL'."""
    if ml == int(ml):
        return f"{int(ml)}mL"
    return f"{ml:.1f}mL"


# ─── Config I/O ────────────────────────────────────────────────────────────────

def _load_cfg() -> dict:
    """Load children from the unified config.json or health_config.json fallback."""
    # Preferred: Load children from config.json
    try:
        from core.config_loader import config
        children = {}
        for kid in getattr(config, "family", {}).get("kids", []):
            key = kid["name"].lower()
            # Try to get weight from health_config.json if it exists, otherwise default
            weight = 0.0
            if os.path.exists(HEALTH_CFG_PATH):
                with open(HEALTH_CFG_PATH) as f:
                    old_cfg = json.load(f)
                    weight = old_cfg.get("children", {}).get(key, {}).get("weight_kg", 0.0)
            
            children[key] = {"name": kid["name"], "weight_kg": weight}
        if children:
            return {"children": children}
    except Exception:
        pass

    # Fallback: Load from health_config.json
    if os.path.exists(HEALTH_CFG_PATH):
        with open(HEALTH_CFG_PATH) as f:
            return json.load(f)
    
    return {"children": {}}


def _save_cfg(cfg: dict) -> None:
    """Save weights specifically to health_config.json (config.json is for static rules)."""
    write_json_atomic(HEALTH_CFG_PATH, cfg)


def _tracked_names() -> str:
    """Return comma-separated display names of configured children."""
    cfg = _load_cfg()
    names = [d["name"] for d in cfg.get("children", {}).values()]
    return ", ".join(names) if names else "no children configured"


def _resolve_child(name: str) -> Optional[str]:
    """
    Return lowercase config key for a child name, or None if not found.
    Tries: exact key match → display name match → 3-char prefix match.
    """
    nl  = name.lower().strip()
    cfg = _load_cfg()
    ch  = cfg.get("children", {})
    if not ch:
        return None
    if nl in ch:
        return nl
    for key, data in ch.items():
        if data["name"].lower() == nl:
            return key
    # Prefix match
    for key in ch:
        if nl and len(nl) >= 2 and key.startswith(nl[:3]):
            return key
    return None


# ─── Log I/O ───────────────────────────────────────────────────────────────────

def _load_log() -> dict:
    os.makedirs(HOUSEHOLD_DIR, exist_ok=True)
    if os.path.exists(HEALTH_LOG_PATH):
        with open(HEALTH_LOG_PATH) as f:
            return json.load(f)
    return {}


def _save_log(log: dict) -> None:
    write_json_atomic(HEALTH_LOG_PATH, log)


def _append_event(child_key: str, event: dict) -> None:
    log = _load_log()
    if child_key not in log:
        log[child_key] = []
    log[child_key].append(event)
    _save_log(log)


def _child_events(child_key: str) -> list:
    return _load_log().get(child_key, [])


# ─── Timestamp Helpers ─────────────────────────────────────────────────────────

def _parse_ts(ts_str: Optional[str]) -> datetime:
    """
    Parse a loose timestamp string to a timezone-aware datetime.
    Accepts: None (→ now), ISO strings, "10:00 AM", "10am", "10:00", etc.
    Time-only strings are anchored to today's date.
    """
    if not ts_str:
        return _now()

    tz  = _tz()
    now = _now()
    s   = ts_str.strip()

    for fmt in (
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=tz)
        except ValueError:
            pass

    # "10:30 AM" / "10:30am" / "10:30"
    m = re.match(r"^(\d{1,2}):(\d{2})\s*(am|pm)?$", s, re.IGNORECASE)
    if m:
        h, mn = int(m.group(1)), int(m.group(2))
        ap = (m.group(3) or "").lower()
        if ap == "pm" and h < 12:
            h += 12
        elif ap == "am" and h == 12:
            h = 0
        return now.replace(hour=h, minute=mn, second=0, microsecond=0)

    # "10am" / "10pm" / bare "10"
    m = re.match(r"^(\d{1,2})\s*(am|pm)?$", s, re.IGNORECASE)
    if m:
        h  = int(m.group(1))
        ap = (m.group(2) or "").lower()
        if ap == "pm" and h < 12:
            h += 12
        elif ap == "am" and h == 12:
            h = 0
        return now.replace(hour=h, minute=0, second=0, microsecond=0)

    return now  # fallback


def _fmt_time(dt: datetime) -> str:
    """Format as '10:05 AM'."""
    return dt.strftime("%-I:%M %p")


def _fmt_dt_short(dt: datetime) -> str:
    """Format as 'Mar 25, 10:05 AM'."""
    return dt.strftime("%b %-d, %-I:%M %p")


# ─── Medication Lookup Helpers ─────────────────────────────────────────────────

def _last_dose_dt(child_key: str, med_key: str) -> Optional[datetime]:
    """Return most recent dose datetime for a medication, or None."""
    tz = _tz()
    for ev in reversed(_child_events(child_key)):
        if ev.get("type") == "medication" and ev.get("medication") == med_key:
            dt = datetime.fromisoformat(ev["timestamp"])
            return dt if dt.tzinfo else dt.replace(tzinfo=tz)
    return None


def _doses_in_24h(child_key: str, med_key: str) -> int:
    """Count doses of a medication logged in the past 24 hours."""
    tz     = _tz()
    cutoff = _now() - timedelta(hours=24)
    count  = 0
    for ev in _child_events(child_key):
        if ev.get("type") == "medication" and ev.get("medication") == med_key:
            dt = datetime.fromisoformat(ev["timestamp"])
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=tz)
            if dt >= cutoff:
                count += 1
    return count


def _high_fever_readings_24h(child_key: str) -> list:
    """Return list of confirmed fever events ≥103°F in the past 24 hours."""
    tz     = _tz()
    cutoff = _now() - timedelta(hours=24)
    result = []
    for ev in _child_events(child_key):
        if (ev.get("type") == "fever"
                and not ev.get("subjective", False)
                and (ev.get("temp_f") or 0) >= 103.0):
            dt = datetime.fromisoformat(ev["timestamp"])
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=tz)
            if dt >= cutoff:
                result.append(ev)
    return result


# ─── Tool: log_medication ──────────────────────────────────────────────────────

def log_medication(
    child: str,
    medication: str,
    dose_mg: Optional[float] = None,
    dose_ml: Optional[float] = None,
    timestamp: Optional[str] = None,
) -> str:
    """
    Log a medication dose for a child.

    Accepts dose in mg OR mL — converts automatically using standard concentrations:
      - Children's Tylenol:   160 mg / 5 mL (32 mg/mL)
      - Infants' Tylenol:      80 mg / 0.8 mL (100 mg/mL)
      - Children's Ibuprofen: 100 mg / 5 mL (20 mg/mL)

    All safety checks are done in mg. All output shows BOTH units.
    Dose is ALWAYS logged — warnings are advisory only.

    Returns WhatsApp-ready response with:
      - ✅ Confirmation with both units
      - ⏰ Next safe window
      - Alternate med availability
      - 💊 Dosage range in both units (if dose missing, too low, or too high)
      - ⚠️ Early-dose warning if given before safe window
    """
    child_key = _resolve_child(child)
    if not child_key:
        return f"❓ Unknown child: *{child}*. Tracked: {_tracked_names()}."

    med_key = _normalize_med(medication)
    if not med_key:
        return (
            f"❓ Unknown medication: *{medication}*.\n"
            "Supported: Tylenol / acetaminophen, Ibuprofen / Motrin / Advil."
        )

    cfg        = _load_cfg()
    child_data = cfg["children"][child_key]
    child_name = child_data["name"]
    weight_kg  = child_data.get("weight_kg") or 0.0
    med        = MEDICATIONS[med_key]
    conc       = _get_concentration(med_key, medication)
    ts         = _parse_ts(timestamp)
    now        = _now()
    warnings   = []

    # ── No dose at all: ask for amount ────────────────────────────────────────
    if dose_mg is None and dose_ml is None:
        conc_label = conc.get("label", med["canonical"])
        example_ml = 5.0
        example_mg = _ml_to_mg(example_ml, conc) if conc else None
        ex_str = (f"{_fmt_ml(example_ml)}" +
                  (f" or {example_mg:.0f}mg" if example_mg else ""))
        return (
            f"How much {med['canonical']} did you give {child_name}? "
            f"(e.g. {ex_str} — using {conc_label})"
        )

    # ── Unit conversion ────────────────────────────────────────────────────────
    # Track which unit the parent originally used so we can format output correctly.
    # ml_primary=True  → parent said mL → display "5mL (160mg)"
    # ml_primary=False → parent said mg → display "160mg (5mL)"
    ml_primary = dose_ml is not None

    if dose_ml is not None and dose_mg is None:
        # Parent gave mL → convert to mg for all safety maths
        if not conc:
            return (
                f"⚠️ Can't convert mL: no concentration data for *{medication}*. "
                f"Please give the dose in mg."
            )
        dose_mg = _ml_to_mg(dose_ml, conc)
    elif dose_mg is not None and dose_ml is None:
        # Parent gave mg → derive mL for display (if we have concentration data)
        if conc:
            dose_ml = _mg_to_ml(dose_mg, conc)

    # ── Early-dose check (advisory) ────────────────────────────────────────────
    last = _last_dose_dt(child_key, med_key)
    if last:
        safe_at = last + timedelta(hours=med["interval_hours"])
        if ts < safe_at:
            elapsed     = ts - last
            elapsed_h   = int(elapsed.total_seconds() // 3600)
            elapsed_m   = int((elapsed.total_seconds() % 3600) // 60)
            elapsed_str = f"{elapsed_h}h {elapsed_m}m" if elapsed_m else f"{elapsed_h}h"
            warnings.append(
                f"⚠️ Last {med['canonical']} was only {elapsed_str} ago — "
                f"safe window opens at *{_fmt_time(safe_at)}*"
            )

    # ── Dosage range note (in both units) ──────────────────────────────────────
    dose_note: Optional[str] = None
    if weight_kg:
        min_mg = weight_kg * med["dose_min_per_kg"]
        max_mg = weight_kg * med["dose_max_per_kg"]

        # Build the range string with both units
        if conc:
            min_ml = _mg_to_ml(min_mg, conc)
            max_ml = _mg_to_ml(max_mg, conc)
            range_str = (
                f"{min_mg:.0f}–{max_mg:.0f}mg "
                f"({_fmt_ml(min_ml)}–{_fmt_ml(max_ml)} of {conc['label']})"
            )
        else:
            range_str = f"{min_mg:.0f}–{max_mg:.0f}mg"

        # Format the actual logged dose with both units
        logged_str = _fmt_dose(dose_mg, dose_ml, conc, ml_primary=ml_primary)

        if dose_mg < min_mg:
            # Special case: if parent gave a suspiciously small number (e.g. "5mg"
            # when they likely meant "5mL"), nudge them toward the mL reading.
            if conc and dose_mg < 10 and dose_ml is None:
                # Their "5mg" is tiny — they almost certainly meant 5mL
                intended_ml  = dose_mg          # treat the number as mL
                intended_mg  = _ml_to_mg(intended_ml, conc)
                dose_note = (
                    f"💊 For {child_name} ({weight_kg}kg): safe dose is {range_str}. "
                    f"You gave {logged_str} — that's below the typical range. "
                    f"Did you mean *{_fmt_ml(intended_ml)} ({intended_mg:.0f}mg)*?"
                )
            else:
                dose_note = (
                    f"💊 For {child_name} ({weight_kg}kg): safe dose is {range_str}. "
                    f"You gave {logged_str} — below the typical range. "
                    f"Did you mean *{min_mg:.0f}mg "
                    f"({_fmt_ml(min_ml) if conc else ''})*?"
                    if conc else
                    f"💊 For {child_name} ({weight_kg}kg): safe dose is {range_str}. "
                    f"You gave {logged_str} — below the typical range."
                )
        elif dose_mg > max_mg:
            dose_note = (
                f"⚠️ For {child_name} ({weight_kg}kg): safe dose is {range_str}. "
                f"You gave {logged_str} — *above* the typical range."
            )
        # (In-range: no note unless dose was absent — handled above)
    else:
        # No weight on record — just show what was logged
        pass

    # ── Log the event (ALWAYS — warnings advisory only) ────────────────────────
    _append_event(child_key, {
        "timestamp":  ts.isoformat(),
        "type":       "medication",
        "medication": med_key,
        "canonical":  med["canonical"],
        "dose_mg":    dose_mg,
        "dose_ml":    dose_ml,
        "conc_label": conc.get("label") if conc else None,
    })

    # ── Next window for this medication ────────────────────────────────────────
    next_this     = ts + timedelta(hours=med["interval_hours"])
    next_this_str = _fmt_time(next_this)

    # ── Alternate medication availability ──────────────────────────────────────
    alt_key  = med["alternate"]
    alt_med  = MEDICATIONS[alt_key]
    alt_last = _last_dose_dt(child_key, alt_key)
    if alt_last:
        alt_next = alt_last + timedelta(hours=alt_med["interval_hours"])
        if now >= alt_next:
            alt_line = f"{alt_med['canonical']} available *now* if needed."
        else:
            alt_line = (
                f"{alt_med['canonical']} available at "
                f"*{_fmt_time(alt_next)}* if needed."
            )
    else:
        alt_line = (
            f"{alt_med['canonical']} available *now* if needed "
            f"(no recent dose on record)."
        )

    # ── Assemble response ──────────────────────────────────────────────────────
    dose_display = _fmt_dose(dose_mg, dose_ml, conc, ml_primary=ml_primary)

    # Surface concentration variant label for non-default (e.g. Infants' Tylenol)
    conc_note: Optional[str] = None
    if conc:
        default_variant = med["concentrations"]["default"]
        # If the variant name doesn't match the default, flag it
        used_variant = next(
            (k for k, v in med["concentrations"].items()
             if k != "default" and v is conc),
            None,
        )
        if used_variant and used_variant != default_variant:
            conc_note = f"_(using {conc['label']})_"

    lines: list[str] = []

    if warnings:
        lines.extend(warnings)
        lines.append("")

    lines.append(
        f"✅ Logged {child_name}: {med['canonical']} {dose_display} at {_fmt_time(ts)}"
    )
    lines.append(f"⏰ Next {med['canonical']} earliest at *{next_this_str}*.")
    lines.append(alt_line)

    if dose_note:
        lines.append(dose_note)

    if conc_note:
        lines.append(conc_note)

    if not warnings:
        lines.append(f"\nWant a reminder at {next_this_str}? Reply *yes* to set it.")

    return "\n".join(lines)


# ─── Tool: log_fever ──────────────────────────────────────────────────────────

def log_fever(
    child: str,
    temp_f: Optional[float] = None,
    subjective: bool = False,
    timestamp: Optional[str] = None,
) -> str:
    """
    Log a fever reading (confirmed or subjective).

    - Confirmed: temp_f provided, subjective=False
    - Subjective: "feels warm" / "seems feverish" → subjective=True, no temp

    Safety warnings (advisory — always logged):
      - ≥104°F: consider calling pediatrician
      - ≥103°F × 3 readings in 24h: fever elevated for 24h+
    """
    child_key = _resolve_child(child)
    if not child_key:
        return f"❓ Unknown child: *{child}*. Tracked: {_tracked_names()}."

    cfg        = _load_cfg()
    child_name = cfg["children"][child_key]["name"]
    ts         = _parse_ts(timestamp)

    # Log first so high-fever count includes this reading
    _append_event(child_key, {
        "timestamp":  ts.isoformat(),
        "type":       "fever",
        "temp_f":     temp_f,
        "subjective": subjective,
    })

    warnings: list[str] = []

    if temp_f and temp_f >= 104.0:
        warnings.append(
            "⚠️ High fever — consider calling your pediatrician "
            "if it doesn't come down within an hour."
        )

    if temp_f and temp_f >= 103.0:
        if len(_high_fever_readings_24h(child_key)) >= 3:
            warnings.append(
                "🌡️ Fever has been elevated for over 24h — worth a call to the doctor."
            )

    time_str = _fmt_time(ts)
    if subjective:
        log_line = f"✅ Logged {child_name}: feels warm (unconfirmed fever) at {time_str}"
    elif temp_f:
        log_line = f"✅ Logged {child_name}: {temp_f}°F fever at {time_str}"
    else:
        log_line = f"✅ Logged {child_name}: fever noted at {time_str}"

    lines = [log_line]
    if warnings:
        lines.append("")
        lines.extend(warnings)

    lines.append(
        "\n_Any other symptoms? (vomiting, rash, etc.) — reply if so, no need otherwise._"
    )
    return "\n".join(lines)


# ─── Tool: log_symptom ────────────────────────────────────────────────────────

def log_symptom(
    child: str,
    symptoms: str,
    timestamp: Optional[str] = None,
) -> str:
    """Log a free-text symptom note for a child (vomiting, rash, no appetite, etc.)."""
    child_key = _resolve_child(child)
    if not child_key:
        return f"❓ Unknown child: *{child}*. Tracked: {_tracked_names()}."

    cfg        = _load_cfg()
    child_name = cfg["children"][child_key]["name"]
    ts         = _parse_ts(timestamp)

    _append_event(child_key, {
        "timestamp": ts.isoformat(),
        "type":      "symptom",
        "symptoms":  symptoms,
    })

    return f"✅ Logged {child_name}: {symptoms} at {_fmt_time(ts)}"


# ─── Tool: update_child_weight ────────────────────────────────────────────────

def update_child_weight(child: str, weight_kg: float) -> str:
    """Update a child's weight in health_config.json."""
    child_key = _resolve_child(child)
    if not child_key:
        return f"❓ Unknown child: *{child}*. Tracked: {_tracked_names()}."

    cfg   = _load_cfg()
    old_w = cfg["children"][child_key].get("weight_kg", "?")
    cfg["children"][child_key]["weight_kg"] = weight_kg
    _save_cfg(cfg)

    child_name = cfg["children"][child_key]["name"]
    return (
        f"✅ Updated *{child_name}'s* weight: {old_w}kg → {weight_kg}kg\n"
        f"_Dosage calculations will now use {weight_kg}kg._"
    )


# ─── Tool: get_health_summary ─────────────────────────────────────────────────

def get_health_summary(child: str, days: int = 3) -> str:
    """
    Generate a clean, doctor-friendly chronological health summary.
    Shows fever readings, medications (with both units), and symptoms grouped by day.
    """
    child_key = _resolve_child(child)
    if not child_key:
        return f"❓ Unknown child: *{child}*. Tracked: {_tracked_names()}."

    cfg        = _load_cfg()
    child_data = cfg["children"][child_key]
    child_name = child_data["name"]
    weight_kg  = child_data.get("weight_kg", "?")
    tz         = _tz()
    cutoff     = _now() - timedelta(days=days)
    events     = _child_events(child_key)

    dated: list[tuple[datetime, dict]] = []
    for ev in events:
        dt = datetime.fromisoformat(ev["timestamp"])
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz)
        if dt >= cutoff:
            dated.append((dt, ev))

    if not dated:
        return (
            f"📋 No health events logged for *{child_name}* "
            f"in the past {days} day(s)."
        )

    dated.sort(key=lambda x: x[0])

    by_date: dict = defaultdict(list)
    for dt, ev in dated:
        by_date[dt.strftime("%b %-d")].append((dt, ev))

    med_counts: dict              = {}
    last_fever_reading: Optional[tuple] = None

    start_dt = dated[0][0]
    end_dt   = dated[-1][0]
    period   = (
        start_dt.strftime("%b %-d, %Y")
        if start_dt.date() == end_dt.date()
        else f"{start_dt.strftime('%b %-d')}–{end_dt.strftime('%b %-d, %Y')}"
    )

    lines = [
        f"🏥 *Health Log — {child_name}* ({weight_kg}kg)",
        f"*Period: {period}*",
        "",
    ]

    for date_label, day_events in by_date.items():
        lines.append(f"*{date_label}*")
        for dt, ev in day_events:
            t  = dt.strftime("%-I:%M %p")
            et = ev.get("type", "")

            if et == "fever":
                if ev.get("subjective"):
                    lines.append(f"  {t} — Feels warm (unconfirmed fever)")
                elif ev.get("temp_f"):
                    temp = ev["temp_f"]
                    lines.append(f"  {t} — Fever {temp}°F")
                    last_fever_reading = (dt, temp)
                else:
                    lines.append(f"  {t} — Fever (temp not recorded)")

            elif et == "medication":
                name = ev.get("canonical", ev.get("medication", "Medication"))
                d_mg = ev.get("dose_mg")
                d_ml = ev.get("dose_ml")
                if d_mg and d_ml:
                    ds = f" {d_ml:.0f}mL ({d_mg:.0f}mg)"  if d_ml == int(d_ml) else f" {d_ml:.1f}mL ({d_mg:.0f}mg)"
                elif d_mg:
                    ds = f" {d_mg:.0f}mg"
                else:
                    ds = ""
                lines.append(f"  {t} — {name}{ds} given")
                med_counts[name] = med_counts.get(name, 0) + 1

            elif et == "symptom":
                sym = ev.get("symptoms", "")
                lines.append(f"  {t} — {sym.capitalize()}")

        lines.append("")

    if med_counts:
        med_str = ", ".join(f"{n} ×{c}" for n, c in sorted(med_counts.items()))
        lines.append(f"*Medications given:* {med_str}")

    if last_fever_reading:
        fdt, fval = last_fever_reading
        lines.append(
            f"*Last fever reading:* {fval}°F "
            f"({fdt.strftime('%b %-d, %-I:%M %p')})"
        )

    return "\n".join(lines)


# ─── Tool: schedule_medication_reminder ───────────────────────────────────────

def schedule_medication_reminder(
    child: str,
    medication: str,
    remind_at: str,
) -> str:
    """
    Return a structured reminder payload as JSON for the OpenClaw agent to schedule.

    Python does NOT call `at`, does NOT run shell commands, and does NOT send
    WhatsApp messages. The agent reads this output and creates an OpenClaw cron
    job (via `openclaw cron add ...`) which, when it fires, has the agent post
    the message to the family group via `openclaw message send` itself. Same
    architecture as every other delivery in this skill (see CLAUDE.md rule #7).
    """
    child_key = _resolve_child(child)
    if not child_key:
        return f"❓ Unknown child: *{child}*."

    med_key = _normalize_med(medication)
    if not med_key:
        return f"❓ Unknown medication: *{medication}*."

    cfg        = _load_cfg()
    child_name = cfg["children"][child_key]["name"]
    med_name   = MEDICATIONS[med_key]["canonical"]
    ts         = _parse_ts(remind_at)
    at_time    = _fmt_time(ts)

    return json.dumps({
        "status":           "reminder_pending",
        "child":            child_name,
        "medication":       med_name,
        "remind_at_human":  at_time,
        "remind_at_iso":    ts.isoformat(),
        "suggested_message": (
            f"⏰ {child_name}'s {med_name} window is open — "
            f"safe to give next dose now."
        ),
    })
