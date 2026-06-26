from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from config import FACTS_FILE, MEMORY_ROOT, USERS_DIR


MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
USERS_DIR.mkdir(parents=True, exist_ok=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slugify(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^\w\-]+", "_", value, flags=re.UNICODE)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "unknown"


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


@dataclass
class MemoryHit:
    source: str
    subject: str
    field: str
    value: Any
    updated_at: Optional[str] = None


class MemoryStore:
    def _user_file(self, user: str) -> Path:
        return USERS_DIR / f"{_slugify(user)}.json"

    def load_facts(self) -> dict[str, Any]:
        return _read_json(FACTS_FILE, {"subjects": {}, "history": []})

    def save_facts(self, data: dict[str, Any]) -> None:
        _write_json(FACTS_FILE, data)

    def load_user_profile(self, user: str) -> dict[str, Any]:
        return _read_json(
            self._user_file(user),
            {
                "user": user,
                "aliases": [],
                "profile": {},
                "preferences": {},
                "devices": [],
                "notes": [],
                "updated_at": None,
            },
        )

    def save_user_profile(self, user: str, data: dict[str, Any]) -> None:
        data["user"] = user
        data["updated_at"] = _now_iso()
        _write_json(self._user_file(user), data)

    def remember_fact(
        self,
        subject: str,
        field: str,
        value: Any,
        source_user: str | None = None,
        confidence: float = 1.0,
    ) -> dict[str, Any]:
        subject_key = _slugify(subject)
        facts = self.load_facts()
        subjects = facts.setdefault("subjects", {})
        subject_entry = subjects.setdefault(subject_key, {"display_name": subject, "facts": {}, "updated_at": None})
        subject_entry["display_name"] = subject
        subject_entry["facts"][field] = {
            "value": value,
            "updated_at": _now_iso(),
            "source_user": source_user,
            "confidence": confidence,
        }
        subject_entry["updated_at"] = _now_iso()
        facts.setdefault("history", []).append(
            {
                "type": "fact_upsert",
                "subject": subject,
                "field": field,
                "value": value,
                "source_user": source_user,
                "confidence": confidence,
                "timestamp": _now_iso(),
            }
        )
        self.save_facts(facts)
        return subject_entry

    def fact_exists(self, subject: str, field: str, value: Any | None = None) -> bool:
        entry = self.load_facts().get("subjects", {}).get(_slugify(subject))
        if not entry:
            return False
        fact = entry.get("facts", {}).get(field)
        if not fact:
            return False
        return value is None or fact.get("value") == value

    def append_note(self, user: str, note: str) -> dict[str, Any]:
        profile = self.load_user_profile(user)
        profile.setdefault("notes", []).append({"text": note, "created_at": _now_iso()})
        self.save_user_profile(user, profile)
        return profile

    def search(self, query: str, limit: int = 5) -> list[MemoryHit]:
        q = str(query or "").strip().lower()
        hits: list[MemoryHit] = []
        if not q:
            return hits

        facts = self.load_facts()
        for subject_key, subject_entry in facts.get("subjects", {}).items():
            display_name = subject_entry.get("display_name", subject_key)
            if q in subject_key or q in str(display_name).lower():
                for field, fact in subject_entry.get("facts", {}).items():
                    hits.append(MemoryHit("facts", display_name, field, fact.get("value"), fact.get("updated_at")))
                continue
            for field, fact in subject_entry.get("facts", {}).items():
                value_str = json.dumps(fact.get("value", ""), ensure_ascii=False).lower()
                if q in field.lower() or q in value_str:
                    hits.append(MemoryHit("facts", display_name, field, fact.get("value"), fact.get("updated_at")))

        for path in USERS_DIR.glob("*.json"):
            profile = _read_json(path, {})
            user = profile.get("user", path.stem)
            for section_name in ("profile", "preferences"):
                section = profile.get(section_name, {})
                if isinstance(section, dict):
                    for key, value in section.items():
                        blob = f"{user} {section_name} {key} {value}".lower()
                        if q in blob:
                            hits.append(MemoryHit(f"user:{user}", user, f"{section_name}.{key}", value, profile.get("updated_at")))
            for note in profile.get("notes", []):
                text = str(note.get("text", ""))
                if q in text.lower():
                    hits.append(MemoryHit(f"user:{user}", user, "note", text, note.get("created_at")))

        return hits[:limit]

    def get_subject_summary(self, subject: str) -> dict[str, Any]:
        entry = self.load_facts().get("subjects", {}).get(_slugify(subject))
        if not entry:
            return {"subject": subject, "facts": {}, "found": False}
        return {
            "subject": entry.get("display_name", subject),
            "facts": {field: fact.get("value") for field, fact in entry.get("facts", {}).items()},
            "found": True,
            "updated_at": entry.get("updated_at"),
        }

    def build_context_for_user(self, user: str) -> str:
        profile = self.load_user_profile(user)
        lines: list[str] = [f"Current user: {profile.get('user', user)}"]
        if profile.get("profile"):
            lines.append("User profile:")
            for key, value in profile["profile"].items():
                lines.append(f"- {key}: {value}")
        if profile.get("preferences"):
            lines.append("Preferences:")
            for key, value in profile["preferences"].items():
                lines.append(f"- {key}: {value}")
        notes = profile.get("notes", [])[-5:]
        if notes:
            lines.append("Recent notes:")
            for note in notes:
                lines.append(f"- {note.get('text')}")
        summary = self.get_subject_summary(user)
        if summary.get("found"):
            lines.append("Known facts for this user:")
            for key, value in summary.get("facts", {}).items():
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)
