from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .analysis import safe_text, unique_strings
from .models import PipelineReport, SearchRequest
from .source_registry import is_implemented_source, normalize_source_hint, source_profile


PROFILE_FILENAME = "profile.md"
PROFILE_MARKER_START = "<!-- property-advisor-profile-json"
PROFILE_MARKER_END = "-->"


@dataclass
class UserProfile:
    role: str = ""
    country: str = ""
    city: str = ""
    destination: str = ""
    budget_min: float | None = None
    budget_max: float | None = None
    bedrooms: float | None = None
    preferred_sources: list[str] = field(default_factory=list)
    hard_requirements: list[str] = field(default_factory=list)
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "UserProfile":
        return cls(
            role=safe_text(payload.get("role")),
            country=safe_text(payload.get("country")),
            city=safe_text(payload.get("city")),
            destination=safe_text(payload.get("destination")),
            budget_min=_as_float(payload.get("budget_min")),
            budget_max=_as_float(payload.get("budget_max")),
            bedrooms=_as_float(payload.get("bedrooms")),
            preferred_sources=[normalize_source_hint(item) for item in _as_list(payload.get("preferred_sources"))],
            hard_requirements=[safe_text(item) for item in _as_list(payload.get("hard_requirements")) if safe_text(item)],
            updated_at=safe_text(payload.get("updated_at")),
        )


class ProfileStore:
    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root).expanduser() if root else Path.home() / "property-advisor"
        self.profile_path = self.root / PROFILE_FILENAME
        self.searches_dir = self.root / "searches"
        self.watched_dir = self.root / "watched"
        self.alerts_dir = self.root / "alerts"

    def load(self) -> UserProfile:
        if not self.profile_path.exists():
            return UserProfile()
        text = self.profile_path.read_text(encoding="utf-8")
        payload = _extract_json_payload(text)
        if payload:
            try:
                return UserProfile.from_dict(json.loads(payload))
            except json.JSONDecodeError:
                pass
        return _parse_legacy_markdown(text)

    def save(self, profile: UserProfile) -> None:
        self._ensure_dirs()
        profile.updated_at = _utc_now()
        payload = json.dumps(profile.to_dict(), ensure_ascii=False, indent=2)
        self.profile_path.write_text(_render_profile(profile, payload), encoding="utf-8")

    def apply_to_request(self, request: SearchRequest, profile: UserProfile | None = None) -> SearchRequest:
        profile = profile or self.load()
        if not safe_text(profile.country) and not safe_text(profile.city) and profile.budget_max is None:
            return request
        applied = SearchRequest(**request.to_dict())
        if applied.country_is_default and profile.country:
            applied.country = profile.country
            applied.country_is_default = False
        if applied.city_is_default and profile.city:
            applied.city = profile.city
            applied.city_is_default = False
        if not safe_text(applied.destination) and profile.destination:
            applied.destination = profile.destination
        if applied.budget_min is None and profile.budget_min is not None:
            applied.budget_min = profile.budget_min
        if applied.budget_max is None and profile.budget_max is not None:
            applied.budget_max = profile.budget_max
        if applied.bedrooms is None and profile.bedrooms is not None:
            applied.bedrooms = profile.bedrooms
        if safe_text(applied.source_hint).lower() in {"", "auto"}:
            implemented_preferences = [
                source
                for source in profile.preferred_sources
                if is_implemented_source(source) and _source_matches_country(source, applied.country)
            ]
            if implemented_preferences:
                applied.source_hint = implemented_preferences[0]
        if profile.hard_requirements:
            applied.user_priorities = unique_strings([*applied.user_priorities, *profile.hard_requirements])
        return applied

    def update_from_request(self, profile: UserProfile, request: SearchRequest) -> UserProfile:
        changed = False
        if not request.country_is_default and safe_text(request.country):
            profile.country = safe_text(request.country)
            changed = True
        if not request.city_is_default and safe_text(request.city):
            profile.city = safe_text(request.city)
            changed = True
        if safe_text(request.destination):
            profile.destination = safe_text(request.destination)
            changed = True
        if request.budget_min is not None:
            profile.budget_min = request.budget_min
            changed = True
        if request.budget_max is not None:
            profile.budget_max = request.budget_max
            changed = True
        if request.bedrooms is not None:
            profile.bedrooms = request.bedrooms
            changed = True
        explicit_source = normalize_source_hint(request.source_hint)
        if explicit_source != "auto":
            profile.preferred_sources = unique_strings([explicit_source, *profile.preferred_sources])
            changed = True
        if request.user_priorities:
            profile.hard_requirements = unique_strings([*profile.hard_requirements, *request.user_priorities])
            changed = True
        if changed:
            self.save(profile)
        return profile

    def record_search(self, request: SearchRequest, report: PipelineReport | None = None) -> Path:
        self._ensure_dirs()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = self.searches_dir / f"{stamp}.json"
        payload: dict[str, Any] = {
            "created_at": _utc_now(),
            "request": request.to_dict(),
        }
        if report:
            payload["summary"] = dict(report.summary)
            payload["selected_source"] = report.selected_source
            payload["selected_runtime_mode"] = report.selected_runtime_mode
            payload["routing"] = dict(report.routing)
            payload["candidate_count"] = len(report.candidate_rows)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def watch_listing(self, *, url: str, title: str = "", source_id: str = "", note: str = "") -> Path:
        self._ensure_dirs()
        slug = _slugify(title or url)
        path = self.watched_dir / f"{slug}.json"
        payload = {
            "created_at": _utc_now(),
            "title": safe_text(title),
            "url": safe_text(url),
            "source_id": normalize_source_hint(source_id) if source_id else "",
            "note": safe_text(note),
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def _ensure_dirs(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.searches_dir.mkdir(parents=True, exist_ok=True)
        self.watched_dir.mkdir(parents=True, exist_ok=True)
        self.alerts_dir.mkdir(parents=True, exist_ok=True)


def _render_profile(profile: UserProfile, payload: str) -> str:
    preferred = ", ".join(profile.preferred_sources) if profile.preferred_sources else ""
    requirements = "\n".join(f"- {item}" for item in profile.hard_requirements) or "- "
    return f"""# Property Advisor Profile

{PROFILE_MARKER_START}
{payload}
{PROFILE_MARKER_END}

role: {profile.role}
country: {profile.country}
city: {profile.city}
destination: {profile.destination}
budget_min: {_format_optional(profile.budget_min)}
budget_max: {_format_optional(profile.budget_max)}
bedrooms: {_format_optional(profile.bedrooms)}
preferred_sources: {preferred}
updated_at: {profile.updated_at}

## Hard Requirements
{requirements}
"""


def _extract_json_payload(text: str) -> str:
    start = text.find(PROFILE_MARKER_START)
    if start < 0:
        return ""
    start += len(PROFILE_MARKER_START)
    end = text.find(PROFILE_MARKER_END, start)
    if end < 0:
        return ""
    return text[start:end].strip()


def _parse_legacy_markdown(text: str) -> UserProfile:
    values: dict[str, Any] = {}
    hard_requirements: list[str] = []
    in_requirements = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.lower().startswith("## hard requirements"):
            in_requirements = True
            continue
        if line.startswith("## "):
            in_requirements = False
        if in_requirements and line.startswith("-"):
            item = safe_text(line[1:])
            if item:
                hard_requirements.append(item)
            continue
        if ":" in line and not line.startswith("#"):
            key, value = line.split(":", 1)
            values[key.strip().lower()] = value.strip()
    values["hard_requirements"] = hard_requirements
    return UserProfile.from_dict(values)


def _as_float(value: Any) -> float | None:
    try:
        if value in {None, ""}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [safe_text(item) for item in value if safe_text(item)]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [safe_text(value)] if safe_text(value) else []


def _format_optional(value: float | None) -> str:
    if value is None:
        return ""
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", safe_text(value).lower()).strip("-")
    return slug[:80] or "listing"


def _source_matches_country(source_id: str, country: str) -> bool:
    profile = source_profile(source_id)
    normalized_country = safe_text(country).lower()
    if not profile or not normalized_country:
        return True
    return any(region in normalized_country or normalized_country in region for region in profile.regions)
