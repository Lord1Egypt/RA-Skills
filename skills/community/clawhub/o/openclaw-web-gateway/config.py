from __future__ import annotations

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _slugify(value: str) -> str:
    value = str(value or "").strip().lower()
    value = re.sub(r"[^\w\-]+", "_", value, flags=re.UNICODE)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "unknown"


class Settings:
    def __init__(self):
        participants_path = BASE_DIR / "config" / "participants.json"

        self.app_title = os.getenv("APP_TITLE", "OpenClaw Web Gateway")
        self.app_subtitle = os.getenv("APP_SUBTITLE", "Multi-user household interface")

        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "5002"))
        self.debug = _bool_env("DEBUG", False)

        self.openclaw_base = os.getenv("OPENCLAW_BASE", "http://127.0.0.1:18789").rstrip("/")
        self.agent = os.getenv("OPENCLAW_AGENT", "main")
        self.token = os.getenv("OPENCLAW_TOKEN", "")

        self.channel = os.getenv("OPENCLAW_CHANNEL", "web-gateway")
        self.model = os.getenv("OPENCLAW_MODEL", "default")

        self.google_maps_embed_api_key = os.getenv("GOOGLE_MAPS_EMBED_API_KEY", "")

        self.memory_root = Path(os.getenv("MEMORY_ROOT", str(BASE_DIR / "memory")))
        self.users_dir = self.memory_root / "users"
        self.facts_file = self.memory_root / "facts.json"
        self.state_file = self.memory_root / "state.json"

        self.participants = self._load_participants(participants_path)
        if not self.participants:
            raise RuntimeError("No participants found in config/participants.json")

        self.users = [p["display_name"] for p in self.participants]

        self.display_to_participant = {
            p["display_name"].lower(): p for p in self.participants
        }

        self.alias_to_display: dict[str, str] = {}
        self.key_to_display: dict[str, str] = {}

        for participant in self.participants:
            display_name = participant["display_name"]
            key = participant["key"]

            self.key_to_display[key.lower()] = display_name
            self.alias_to_display[display_name.lower()] = display_name
            self.alias_to_display[key.lower()] = display_name

            for alias in participant.get("aliases", []):
                self.alias_to_display[str(alias).strip().lower()] = display_name

        self.default_user = self._resolve_default_user(
            os.getenv("DEFAULT_USER", self.participants[0]["display_name"])
        )

    def _load_participants(self, path: Path) -> list[dict]:
        if not path.exists():
            raise RuntimeError(f"participants.json not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            participants = data.get("participants", [])
        elif isinstance(data, list):
            participants = data
        else:
            raise RuntimeError(
                "participants.json must contain either a list or a dict with a 'participants' key"
            )

        normalized = []
        for i, participant in enumerate(participants):
            if not isinstance(participant, dict):
                raise RuntimeError(f"Participant entry #{i} is not an object")

            display_name = str(
                participant.get("display_name") or participant.get("name") or ""
            ).strip()
            if not display_name:
                raise RuntimeError(f"Participant entry #{i} is missing 'display_name'")

            key = str(participant.get("key") or _slugify(display_name)).strip()
            aliases = participant.get("aliases", [])
            if not isinstance(aliases, list):
                aliases = []

            normalized.append(
                {
                    "key": key,
                    "display_name": display_name,
                    "aliases": [str(a).strip() for a in aliases if str(a).strip()],
                }
            )

        return normalized

    def _resolve_default_user(self, raw: str) -> str:
        if not raw:
            return self.participants[0]["display_name"]

        canonical = self.alias_to_display.get(raw.strip().lower())
        if canonical:
            return canonical

        return str(raw).strip()


settings = Settings()

APP_TITLE = settings.app_title
APP_SUBTITLE = settings.app_subtitle

HOST = settings.host
PORT = settings.port
DEBUG = settings.debug

OPENCLAW_BASE = settings.openclaw_base
OPENCLAW_AGENT = settings.agent
OPENCLAW_TOKEN = settings.token
OPENCLAW_CHANNEL = settings.channel
OPENCLAW_MODEL = settings.model

CHANNEL = OPENCLAW_CHANNEL
MODEL = OPENCLAW_MODEL

GOOGLE_MAPS_EMBED_API_KEY = settings.google_maps_embed_api_key

MEMORY_ROOT = settings.memory_root
USERS_DIR = settings.users_dir
FACTS_FILE = settings.facts_file
STATE_FILE = settings.state_file

DEFAULT_USER = settings.default_user
USERS = settings.users
PARTICIPANTS = settings.participants
DISPLAY_TO_PARTICIPANT = settings.display_to_participant
ALIAS_TO_DISPLAY = settings.alias_to_display


def canonical_user(value: str | None) -> str:
    if not value:
        return DEFAULT_USER
    raw = str(value).strip()
    return ALIAS_TO_DISPLAY.get(raw.lower(), raw)


def normalize_user_key(value: str | None) -> str:
    canonical = canonical_user(value)
    participant = DISPLAY_TO_PARTICIPANT.get(canonical.lower())
    if participant:
        return participant["key"]
    return _slugify(canonical)


def user_slug(value: str | None) -> str:
    return normalize_user_key(value)


def participant_aliases() -> dict[str, str]:
    return dict(ALIAS_TO_DISPLAY)
