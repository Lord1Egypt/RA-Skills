"""
config_loader.py — Centralized Configuration

Single source of truth for all skill settings.
Reads from config.json (user's real config, gitignored).
Falls back to config.example.json for missing values.

Usage:
    from core.config_loader import config
    group_id = config.whatsapp_group
    members  = config.family_members
"""

from __future__ import annotations
import json
import os
from typing import Dict, List, Optional

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FamilyMember:
    def __init__(self, data: dict):
        self.name  = data["name"]
        self.phone = data.get("phone", "")

    def __repr__(self):
        return f"FamilyMember({self.name})"


class Kid:
    def __init__(self, data: dict):
        self.name       = data["name"]
        self.emoji      = data.get("emoji", "child")
        self.age_years  = data.get("age_years")
        self.age_months = data.get("age_months")
        self.age_desc   = data.get("age_desc", "")
        self.meals      = data.get("meals", {})

    @property
    def emoji_char(self) -> str:
        return {"boy": "\U0001F466", "girl": "\U0001F467"}.get(self.emoji, "\U0001F9D2")

    def slot(self, slot_name: str) -> dict:
        """Return the structured config for a meal slot ('breakfast'/'lunch'/'sides')."""
        return self.meals.get(slot_name, {}) or {}

    def __repr__(self):
        return f"Kid({self.name})"


class Config:
    """
    Typed configuration object.
    All values come from config.json — no hardcoded values elsewhere.
    """

    def __init__(self, data: dict):
        self._data = data

    # ── App ──────────────────────────────────────────────────────────────────

    @property
    def app_name(self) -> str:
        return self._data.get("app", {}).get("name", "Homebase")

    @property
    def owner_phone(self) -> str:
        return self._data.get("app", {}).get("owner_phone", "")

    # ── Location ─────────────────────────────────────────────────────────────

    @property
    def city(self) -> str:
        return self._data.get("location", {}).get("city", "")

    @property
    def latitude(self) -> float:
        return self._data.get("location", {}).get("latitude", 0.0)

    @property
    def longitude(self) -> float:
        return self._data.get("location", {}).get("longitude", 0.0)

    @property
    def timezone(self) -> str:
        return self._data.get("location", {}).get("timezone", "America/Los_Angeles")

    # ── WhatsApp ──────────────────────────────────────────────────────────────

    @property
    def whatsapp_group(self) -> str:
        return self._data.get("whatsapp", {}).get("group_id", "")

    @property
    def whatsapp_agent_number(self) -> str:
        return self._data.get("whatsapp", {}).get("agent_number", "")

    # ── Family ────────────────────────────────────────────────────────────────

    @property
    def family_members(self) -> List[FamilyMember]:
        raw = self._data.get("family", {}).get("members", [])
        # Handle both formats: list of dicts [{"name": ..., "phone": ...}]
        # and phone→name dict {"+1234": "Name"}
        if isinstance(raw, dict):
            return [FamilyMember({"name": name, "phone": phone})
                    for phone, name in raw.items()]
        return [FamilyMember(m) for m in raw]

    @property
    def family_members_dict(self) -> Dict[str, str]:
        """Phone → Name mapping for sender identification."""
        return {m.phone: m.name for m in self.family_members if m.phone}

    @property
    def kids(self) -> List[Kid]:
        return [Kid(k) for k in self._data.get("family", {}).get("kids", [])]

    @property
    def kid_names(self) -> List[str]:
        return [k.name for k in self.kids]

    # ── Calendar ──────────────────────────────────────────────────────────────

    @property
    def calendar_id(self) -> str:
        return self._data.get("calendar", {}).get("id", "")

    # ── School ────────────────────────────────────────────────────────────────

    @property
    def school_name(self) -> str:
        return self._data.get("school", {}).get("name", "")

    @property
    def school_email_domains(self) -> List[str]:
        return self._data.get("school", {}).get("email_domains", [])

    @property
    def school_email_addresses(self) -> List[str]:
        return self._data.get("school", {}).get("email_addresses", [])

    @property
    def school_email_query(self) -> str:
        """Build Gmail search query from school email config."""
        parts = []
        for domain in self.school_email_domains:
            parts.append(f"from:{domain}")
        for addr in self.school_email_addresses:
            parts.append(f"from:{addr}")
        if not parts:
            return ""
        return "(" + " OR ".join(parts) + ") newer_than:2d"

    # ── Stores ────────────────────────────────────────────────────────────────

    @property
    def indian_stores(self) -> List[str]:
        return self._data.get("stores", {}).get("indian", [])

    @property
    def bulk_stores(self) -> List[str]:
        return self._data.get("stores", {}).get("bulk", ["Costco"])

    @property
    def all_store_keywords(self) -> Dict[str, List[str]]:
        """Returns store keyword mapping for shopping_list.py."""
        indian = [s.lower() for s in self.indian_stores]
        bulk   = [s.lower() for s in self.bulk_stores]
        return {
            "costco":  bulk + ["costco", "cost co"],
            "indian":  indian + ["indian", "desi", "indian store",
                                  "indian grocery", "subzi", "bazaar"],
            "target":  ["target", "walmart", "wal-mart", "safeway",
                         "kroger", "vons", "ralphs"],
        }

    # ── Meals ─────────────────────────────────────────────────────────────────

    @property
    def include_dinner(self) -> bool:
        return self._data.get("meals", {}).get("include_dinner", True)

    @property
    def dinner_options(self) -> List[str]:
        return self._data.get("meals", {}).get("dinner_options", [])

    # ── Briefing ──────────────────────────────────────────────────────────────

    @property
    def briefing_time(self) -> str:
        return self._data.get("briefing", {}).get("time", "07:00")

    @property
    def briefing_weather_enabled(self) -> bool:
        return self._data.get("briefing", {}).get("weather", True)

    @property
    def briefing_positive_message(self) -> bool:
        return self._data.get("briefing", {}).get("positive_message", True)

    # ── Validation ────────────────────────────────────────────────────────────

    def validate(self) -> List[str]:
        """
        Validate config completeness.
        Returns list of error messages (empty = valid).
        """
        errors = []
        if not self.whatsapp_group:
            errors.append("whatsapp.group_id is required")
        if not self.calendar_id:
            errors.append("calendar.id is required")
        if not self.family_members:
            errors.append("family.members must have at least one entry")
        if not self.kids:
            errors.append("family.kids must have at least one entry")
        if not self.latitude or not self.longitude:
            errors.append("location.latitude and location.longitude are required")
        return errors


# ─── Loader ───────────────────────────────────────────────────────────────────

def _load_config() -> Config:
    """Load config.json, falling back to config.example.json."""
    config_path  = os.path.join(SKILL_DIR, "config.json")
    example_path = os.path.join(SKILL_DIR, "config.example.json")

    if os.path.exists(config_path):
        with open(config_path) as f:
            return Config(json.load(f))
    elif os.path.exists(example_path):
        print("⚠️  config.json not found — using config.example.json (placeholders only)")
        print("   Copy config.example.json to config.json and fill in your values.")
        with open(example_path) as f:
            return Config(json.load(f))
    else:
        raise FileNotFoundError(
            "Neither config.json nor config.example.json found.\n"
            "Run: cp config.example.json config.json\n"
            "Then edit config.json with your settings."
        )


# Singleton — import this everywhere
config = _load_config()


# ─── CLI validation ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    errors = config.validate()
    if errors:
        print("❌ Config validation failed:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("✅ Config valid!")
        print(f"  Location:     {config.city} ({config.latitude}, {config.longitude})")
        print(f"  Group:        {config.whatsapp_group}")
        print(f"  Calendar:     {config.calendar_id[:20]}...")
        print(f"  Family:       {[m.name for m in config.family_members]}")
        print(f"  Kids:         {config.kid_names}")
        print(f"  School:       {config.school_name}")
        print(f"  Indian stores:{config.indian_stores}")
