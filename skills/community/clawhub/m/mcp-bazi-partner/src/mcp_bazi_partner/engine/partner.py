"""Partner matching engine for OpenClaw integration."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from .constants import TIANGAN_WUXING, STATUS_DISPLAY

logger = logging.getLogger(__name__)

# Data directory inside this package
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Wuxing generation cycle: 木→火→土→金→水→木
WUXING_CYCLE = ["木", "火", "土", "金", "水"]

# Ten God → Wuxing offset in generation cycle
_SHISHEN_OFFSET = {
    "比劫": 0,
    "食伤": 1,
    "财星": 2,
    "官杀": 3,
    "印星": 4,
}

# Rescue god → partner shishen (strengthen the rescue)
_RESCUE_TO_PARTNER = {
    "印": "印星",
    "食": "食伤",
    "伤": "食伤",
    "比": "比劫",
    "劫": "比劫",
    "财": "财星",
    "官": "官杀",
    "煞": "官杀",
}

# Defeat god → partner shishen (counter the attacker)
_DEFEAT_GOD_COUNTER = {
    "财": "比劫",
    "印": "财星",
    "比": "官杀",
    "劫": "官杀",
    "食": "印星",
    "伤": "印星",
    "官": "食伤",
    "煞": "食伤",
}

# Phase 1 estimated status ratios for L3 probability
_STATUS_RATIO = {"成格": 0.35, "败格有救": 0.40, "败格无救": 0.25}

# Wuxing element → system name
_WUXING_SYS = {"木": "木系", "火": "火系", "土": "土系", "金": "金系", "水": "水系"}

# L1 → most common L2 fallback (used when agent passes L1 pattern name)
_L1_TO_L2_FALLBACK = {
    "七杀格": "煞印相生",
    "伤官格": "伤官生财",
    "印格": "印绶用官",
    "食神格": "食神生财",
    "财格": "财旺生官",
    "正官格": "正官格",
    "建禄月劫格": "禄劫用财",
    "阳刃格": "阳刃用煞",
}

# Cached data
_mapping: dict | None = None
_intros: dict | None = None
_prompts: dict | None = None
_l2_prob: dict | None = None


def _load_json(filename: str) -> dict:
    path = DATA_DIR / filename
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    logger.error("Data file not found: %s (DATA_DIR=%s)", filename, DATA_DIR)
    return {}


def _load_mapping() -> dict:
    global _mapping
    if _mapping is None:
        _mapping = _load_json("partner_mapping.json")
    return _mapping


def _load_intros() -> dict:
    global _intros
    if _intros is None:
        _intros = _load_json("partner_intros.json")
    return _intros


def _load_prompts() -> dict:
    global _prompts
    if _prompts is None:
        _prompts = _load_json("partner_prompts.json")
    return _prompts


def _load_l2_prob() -> dict:
    global _l2_prob
    if _l2_prob is None:
        path = DATA_DIR / "geju_probability_l2.json"
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            flat = {}
            for entries in raw.values():
                for sub_type, data in entries.items():
                    if not sub_type.endswith("_未分类"):
                        flat[sub_type] = data.get("percentage", 0)
            _l2_prob = flat
        else:
            _l2_prob = {}
    return _l2_prob


def get_partner_element(day_master: str, partner_shishen: str) -> str:
    """Compute partner's wuxing element from day master + partner shishen."""
    dm_wuxing = TIANGAN_WUXING[day_master]
    dm_idx = WUXING_CYCLE.index(dm_wuxing)
    offset = _SHISHEN_OFFSET[partner_shishen]
    return WUXING_CYCLE[(dm_idx + offset) % 5]


def _extract_shishen(text: str, table: dict) -> str | None:
    """Extract partner shishen from free-text rescue/defeat_god description."""
    for keyword, shishen in table.items():
        if keyword in text:
            return shishen
    return None


def _get_partner_shishen(
    sub_type: str, status: str,
    rescue: str | None, defeat_god: str | None,
) -> str | None:
    """Determine partner shishen based on status and context."""
    if status == "成格":
        mapping = _load_mapping()
        entry = mapping.get(sub_type)
        if entry:
            return entry.get("partner_shishen")
        return "印星"  # fallback for unmapped成格

    if status == "败格有救":
        if rescue:
            result = _extract_shishen(rescue, _RESCUE_TO_PARTNER)
            if result:
                return result
        # H4 fix: use generic败格有救 mapping, NOT成格 mapping
        generic = _load_mapping().get("_generic_败格有救", {})
        return generic.get("partner_shishen") or "印星"

    if status == "败格无救":
        if defeat_god:
            result = _extract_shishen(defeat_god, _DEFEAT_GOD_COUNTER)
            if result:
                return result
        # H4 fix: use generic败格无救 mapping, NOT成格 mapping
        generic = _load_mapping().get("_generic_败格无救", {})
        return generic.get("partner_shishen") or "印星"

    return "印星"  # ultimate fallback


def get_l3_probability(sub_type: str, status: str) -> float | None:
    """Estimate L3 probability from L2 data and fixed status ratios."""
    l2 = _load_l2_prob()
    l2_pct = l2.get(sub_type)
    if l2_pct is None:
        return None
    ratio = _STATUS_RATIO.get(status, 0.33)
    return round(l2_pct * ratio, 2)


def get_partner(
    sub_type: str, status: str, day_master: str,
    rescue: str | None = None, defeat_god: str | None = None,
) -> dict | None:
    """Match partner based on pattern determination result."""
    # L1→L2 fallback: if sub_type is a broad L1 name, map to most common L2
    mapping = _load_mapping()
    if sub_type not in mapping and sub_type in _L1_TO_L2_FALLBACK:
        original = sub_type
        sub_type = _L1_TO_L2_FALLBACK[sub_type]
        logger.warning("L1→L2 fallback: %s → %s", original, sub_type)

    partner_shishen = _get_partner_shishen(sub_type, status, rescue, defeat_god)
    if not partner_shishen:
        return None

    element = get_partner_element(day_master, partner_shishen)
    element_sys = _WUXING_SYS[element]

    mapping = _load_mapping()
    intros = _load_intros()
    prompts = _load_prompts()

    # For成格, use sub_type key; for败格, use generic template
    if status == "成格":
        entry = mapping.get(sub_type, {})
        partner_name = entry.get("partner_name")
        intro = intros.get(sub_type)
        prompt = prompts.get(sub_type)
    else:
        generic_key = f"_generic_{status}"
        entry = mapping.get(generic_key, {})
        partner_name = entry.get("partner_name")
        intro = intros.get(generic_key)
        prompt = prompts.get(generic_key)

    # Use L2 probability (consistent with card display)
    l2 = _load_l2_prob()
    prob = l2.get(sub_type)
    rarity_str = f"{prob}" if prob else "?"

    if intro:
        intro = intro.replace("{partner_shishen}", partner_shishen)
        intro = intro.replace("{defeat_god}", defeat_god or "未知")
        intro = intro.replace("X%", f"{rarity_str}%")
        intro = intro.replace("{rarity}", rarity_str)
    if prompt:
        prompt = prompt.replace("{partner_shishen}", partner_shishen)

    if partner_name:
        partner_type = f"{element_sys} · {partner_name}"
    else:
        partner_type = f"{element_sys} · {partner_shishen}型搭档"
        partner_name = f"{partner_shishen}型搭档"

    status_display, status_color = STATUS_DISPLAY.get(status, ("", ""))

    return {
        "your_pattern": sub_type,
        "your_status": status,
        "status_display": status_display,
        "status_color": status_color,
        "partner_name": partner_name,
        "partner_type": partner_type,
        "partner_element": element,
        "partner_shishen": partner_shishen,
        "rarity": prob if status == "成格" else None,
        "rarity_display": f"全球仅 {rarity_str}% 的人同款" if prob and status == "成格" else None,
        "partner_intro": intro,
        "system_prompt": prompt,
    }
