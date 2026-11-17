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
import sys
from typing import Dict, List

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
        # School attribution: which classroom an email belongs to. The sender
        # address is the strong signal; teacher names are the fallback, because
        # teachers sometimes write from a shared or district address.
        self.email_sender = data.get("email_sender", "")
        self.teachers     = data.get("teachers", [])

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
        """Primary family group jid. Prefers the scalar `whatsapp.group_id`
        for backward compatibility with existing readers; falls back to
        `whatsapp.groups[0].id` when only the new shape is present.
        """
        wa = self._data.get("whatsapp", {})
        scalar = wa.get("group_id", "")
        if scalar:
            return scalar
        groups = wa.get("groups") or []
        if groups and isinstance(groups, list):
            first = groups[0] or {}
            return first.get("id", "")
        return ""

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
        # 4 days, not 2. The school runner only fires Mon-Fri, so its last
        # Friday run (20:07) sits ~60h before its first Monday one (08:07). A
        # 2-day window reaches back only to Saturday morning, which left mail
        # arriving Friday evening invisible on Monday and therefore forever.
        # Widening costs nothing: dedup is by message id against
        # processed_email_ids.json, so a longer result list re-surfaces only
        # what was genuinely never handled.
        return "(" + " OR ".join(parts) + ") newer_than:4d"

    # ── Stores ────────────────────────────────────────────────────────────────

    @property
    def indian_stores(self) -> List[str]:
        return self._data.get("stores", {}).get("indian", [])

    # ── Meals ─────────────────────────────────────────────────────────────────

    @property
    def include_dinner(self) -> bool:
        return self._data.get("meals", {}).get("include_dinner", True)

    @property
    def dinner_options(self) -> List[str]:
        return self._data.get("meals", {}).get("dinner_options", [])

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
    """Load config.json, falling back to config.example.json.

    HOMEBASE_CONFIG overrides the path outright. The test suite sets it so the
    suite runs against its own fixture instead of whatever config.json happens
    to be on the machine — without it, `config` is an import-time singleton
    bound to the maintainer's real household, and tests silently assert on real
    children's names. A missing override file is fatal on purpose: falling back
    to the real config is the failure mode this exists to prevent.
    """
    override = os.environ.get("HOMEBASE_CONFIG")
    if override:
        with open(override) as f:
            return Config(json.load(f))

    config_path  = os.path.join(SKILL_DIR, "config.json")
    example_path = os.path.join(SKILL_DIR, "config.example.json")

    if os.path.exists(config_path):
        with open(config_path) as f:
            return Config(json.load(f))
    elif os.path.exists(example_path):
        print("⚠️  config.json not found — using config.example.json (placeholders only)", file=sys.stderr)
        print("   Copy config.example.json to config.json and fill in your values.", file=sys.stderr)
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
