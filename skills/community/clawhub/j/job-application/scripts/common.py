from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
BUNDLED_PROFILE_DIR = SKILL_DIR / "assets" / "profile"


def _default_private_data_dir() -> Path:
    """Choose a per-user data root that is never inside the installed skill."""
    configured = os.environ.get("JOB_APPLICATION_DATA_DIR")
    if configured:
        return Path(configured)
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    base = Path(xdg_data_home) if xdg_data_home else Path.home() / ".local" / "share"
    return base / "openclaw" / "job-application"


PRIVATE_DATA_DIR = _default_private_data_dir().expanduser().resolve()
PROFILE_DIR = Path(os.environ.get("JOB_APPLICATION_PROFILE_DIR", BUNDLED_PROFILE_DIR)).expanduser().resolve()
OUTPUT_DIR = Path(os.environ.get("JOB_APPLICATION_OUTPUT_DIR", PRIVATE_DATA_DIR / "applications")).expanduser().resolve()
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"

CV_SCHEMA_VERSION = 2
CONTENT_SCHEMA_VERSION = 2
DEFAULT_CV_LIMITS = {
    "skills": 5,
    "experience": 3,
    "education": 2,
    "projects": 1,
    "languages": 3,
    "achievement_sentences_per_experience": 2,
}
CV_COLLECTIONS = {
    "skills": "skills.json",
    "experience": "experience.json",
    "education": "education.json",
    "projects": "projects.json",
    "languages": "languages.json",
}
TOKEN_PATTERN = re.compile(r"__[A-Za-z][A-Za-z0-9_]*__|\{\{[^}\n]+\}\}")
SAFE_SIGNATURE_PATH_PATTERN = re.compile(r"^[^{}\\\n\r%#$&~^]+$")


class ValidationError(ValueError):
    """An input file is well-formed JSON but does not meet the skill contract."""


def load_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as error:
        raise ValidationError(f"JSON file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValidationError(f"Invalid JSON in {path}: {error.msg} (line {error.lineno})") from error


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def latex_escape(value: Any) -> str:
    text = str(value or "")
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def public_location(profile: dict[str, Any]) -> str:
    """Return the candidate's preferred contact location, including an address when supplied."""
    address_lines = profile.get("address_lines")
    if isinstance(address_lines, list):
        lines = [str(line).strip() for line in address_lines if str(line).strip()]
        if lines:
            return ", ".join(lines)
    for field in ("location", "address", "public_location", "city"):
        value = str(profile.get(field, "")).strip()
        if value:
            return value
    return ""


def by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item["id"]): item for item in items}


def replace_tokens(template: str, values: dict[str, str]) -> str:
    unresolved = sorted(set(TOKEN_PATTERN.findall(template)) - set(values))
    if unresolved:
        raise ValidationError(f"Unresolved template tokens: {', '.join(unresolved)}")
    for token, value in values.items():
        template = template.replace(token, value)
    return template


def resolve_profile_asset(profile_dir: Path, value: str) -> Path | None:
    if not value:
        return None
    configured = Path(value).expanduser()
    candidates = [configured] if configured.is_absolute() else [
        profile_dir / configured,
        profile_dir.parent / configured,
        SKILL_DIR / configured,
    ]
    return next((candidate.resolve() for candidate in candidates if candidate.is_file()), None)


def resolve_signature_asset(content_path: Path, value: Any) -> str | None:
    """Resolve an explicitly requested cover-letter signature image safely."""
    if value is None:
        return None
    raw = _nonempty_string(value, "cover_letter.signature_image")
    configured = Path(raw).expanduser()
    candidates = [configured] if configured.is_absolute() else [content_path.parent / configured]
    asset = next((candidate.resolve() for candidate in candidates if candidate.is_file()), None)
    if asset is None:
        raise ValidationError("cover_letter.signature_image must reference an existing image file")
    if asset.suffix.lower() not in {".png", ".jpg", ".jpeg", ".pdf"}:
        raise ValidationError("cover_letter.signature_image must be a PNG, JPG, JPEG, or PDF file")
    latex_path = asset.as_posix()
    if not SAFE_SIGNATURE_PATH_PATTERN.fullmatch(latex_path):
        raise ValidationError("cover_letter.signature_image path contains unsupported LaTeX characters")
    return latex_path


def load_cv_limits(raw: Any = None) -> dict[str, int]:
    """Merge user limits with v1-compatible defaults and reject ambiguous values."""
    if raw is None:
        return dict(DEFAULT_CV_LIMITS)
    if not isinstance(raw, dict):
        raise ValidationError("limits must be a JSON object")
    unknown = sorted(set(raw) - set(DEFAULT_CV_LIMITS))
    if unknown:
        raise ValidationError(f"Unknown CV limit fields: {', '.join(unknown)}")
    limits = dict(DEFAULT_CV_LIMITS)
    for name, value in raw.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValidationError(f"limits.{name} must be a non-negative integer")
        limits[name] = value
    return limits


def load_limit_file(path: Path) -> dict[str, int]:
    raw = load_json(path)
    if isinstance(raw, dict) and "limits" in raw:
        raw = raw["limits"]
    return load_cv_limits(raw)


def _nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} must be a non-empty string")
    return value.strip()


def validate_cv_selection(choice: Any, profile_dir: Path) -> dict[str, Any]:
    """Validate and normalize a v1/v2 selection without changing its chosen order."""
    if not isinstance(choice, dict):
        raise ValidationError("cv_selection.json must contain a JSON object")
    version = choice.get("schema_version", 1)
    if version not in (1, CV_SCHEMA_VERSION):
        raise ValidationError(f"Unsupported cv_selection schema_version: {version}")
    profile = load_json(profile_dir / "master_profile.json")
    result = dict(choice)
    result["schema_version"] = CV_SCHEMA_VERSION
    result["target_title"] = _nonempty_string(
        result.get("target_title", profile.get("default_target_title")), "target_title"
    )
    result["language"] = _nonempty_string(
        result.get("language", profile.get("default_language")), "language"
    )
    about_me = result.get("about_me", "")
    if not isinstance(about_me, str):
        raise ValidationError("about_me must be a string")
    raw_limits = result.get("limits")
    # Some pre-v2 application folders were produced with reviewed selections
    # beyond the old bundled defaults. Keep those legacy choices readable when
    # they are used as a derivation base; new v2 files still enforce defaults
    # whenever they omit explicit limits.
    if version == 1 and raw_limits is None:
        raw_limits = dict(DEFAULT_CV_LIMITS)
        for field in CV_COLLECTIONS:
            legacy_ids = result.get(field, [])
            if isinstance(legacy_ids, list):
                raw_limits[field] = max(raw_limits[field], len(legacy_ids))
    result["limits"] = load_cv_limits(raw_limits)
    for field, filename in CV_COLLECTIONS.items():
        ids = result.get(field, [])
        if not isinstance(ids, list) or any(not isinstance(item, str) or not item for item in ids):
            raise ValidationError(f"{field} must be a list of non-empty profile IDs")
        if len(ids) != len(set(ids)):
            raise ValidationError(f"{field} must not contain duplicate profile IDs")
        if len(ids) > result["limits"][field]:
            raise ValidationError(
                f"{field} contains {len(ids)} records but limits.{field} is {result['limits'][field]}"
            )
        available = by_id(load_json(profile_dir / filename))
        unknown = [record_id for record_id in ids if record_id not in available]
        if unknown:
            raise ValidationError(f"Unknown IDs in {filename}: {', '.join(unknown)}")
    return result


def selection_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require_object(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{field} must be a JSON object")
    return value


def _required_paragraphs(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValidationError(f"{field} must contain at least one paragraph")
    paragraphs = [_nonempty_string(item, f"{field}[{index}]") for index, item in enumerate(value)]
    return paragraphs


def _required_lines(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValidationError(f"{field} must contain at least one line")
    return [_nonempty_string(item, f"{field}[{index}]") for index, item in enumerate(value)]


def _comparison_key(value: str) -> str:
    """Normalize display text before detecting duplicated address-block values."""
    return " ".join(re.sub(r"[^\w]+", " ", value.casefold()).split())


def _normalize_v2_content(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValidationError("application_content.json must contain a JSON object")
    if data.get("schema_version") != CONTENT_SCHEMA_VERSION:
        raise ValidationError(
            f"application_content.json must use schema_version {CONTENT_SCHEMA_VERSION}"
        )
    job = _require_object(data.get("job"), "job")
    cover = _require_object(data.get("cover_letter"), "cover_letter")
    plain = _require_object(data.get("plain_text"), "plain_text")
    signature_image = cover.get("signature_image")
    if signature_image is not None:
        signature_image = _nonempty_string(signature_image, "cover_letter.signature_image")
    company = _nonempty_string(job.get("company"), "job.company")
    recipient = _nonempty_string(cover.get("recipient"), "cover_letter.recipient")
    company_address = _required_lines(cover.get("company_address"), "cover_letter.company_address")
    company_key = _comparison_key(company)
    recipient_key = _comparison_key(recipient)
    if recipient_key == company_key or recipient_key.startswith(f"{company_key} "):
        raise ValidationError(
            "cover_letter.recipient must not repeat job.company; the template renders the company separately"
        )
    if any(_comparison_key(line) == company_key for line in company_address):
        raise ValidationError(
            "cover_letter.company_address must not repeat job.company; the template renders the company separately"
        )
    return {
        "schema_version": CONTENT_SCHEMA_VERSION,
        "job": {
            "company": company,
            "role": _nonempty_string(job.get("role"), "job.role"),
            "language": _nonempty_string(job.get("language"), "job.language"),
        },
        "cover_letter": {
            "recipient": recipient,
            "company_address": company_address,
            "date": _nonempty_string(cover.get("date"), "cover_letter.date"),
            "subject": _nonempty_string(cover.get("subject"), "cover_letter.subject"),
            "salutation": _nonempty_string(cover.get("salutation"), "cover_letter.salutation"),
            "paragraphs": _required_paragraphs(cover.get("paragraphs"), "cover_letter.paragraphs"),
            "closing": _nonempty_string(cover.get("closing"), "cover_letter.closing"),
            "signatory": _nonempty_string(cover.get("signatory"), "cover_letter.signatory"),
            "signature_image": signature_image,
        },
        "plain_text": {
            "subject": _nonempty_string(plain.get("subject"), "plain_text.subject"),
            "salutation": _nonempty_string(plain.get("salutation"), "plain_text.salutation"),
            "paragraphs": _required_paragraphs(plain.get("paragraphs"), "plain_text.paragraphs"),
            "closing": _nonempty_string(plain.get("closing"), "plain_text.closing"),
            "signatory": _nonempty_string(plain.get("signatory"), "plain_text.signatory"),
        },
    }


def legacy_cover_to_content(data: Any, profile: dict[str, Any], job: dict[str, Any] | None = None) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValidationError("Legacy cover-letter content must contain a JSON object")
    job = job or {}
    company = job.get("company") or data.get("company")
    return _normalize_v2_content({
        "schema_version": CONTENT_SCHEMA_VERSION,
        "job": {
            "company": company,
            "role": job.get("role") or profile.get("default_target_title"),
            "language": job.get("language") or profile.get("default_language"),
        },
        "cover_letter": {
            "recipient": data.get("recipient", "Recruiting-Team"),
            "company_address": data.get("company_address", []),
            "date": data.get("date"),
            "subject": data.get("subject"),
            "salutation": data.get("salutation", "Guten Tag,"),
            "paragraphs": data.get("paragraphs", []),
            "closing": data.get("closing", "Mit freundlichen Grüßen"),
            "signatory": data.get("signatory") or profile.get("full_name"),
        },
        "plain_text": {
            "subject": data.get("subject"),
            "salutation": data.get("salutation", "Guten Tag,"),
            "paragraphs": data.get("paragraphs", []),
            "closing": data.get("closing", "Mit freundlichen Grüßen"),
            "signatory": data.get("signatory") or profile.get("full_name"),
        },
    })


def legacy_plain_to_content(data: Any, profile: dict[str, Any], job: dict[str, Any] | None = None) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValidationError("Legacy plain-text content must contain a JSON object")
    job = job or {}
    company = job.get("company") or "Unbekannt"
    return _normalize_v2_content({
        "schema_version": CONTENT_SCHEMA_VERSION,
        "job": {
            "company": company,
            "role": job.get("role") or profile.get("default_target_title"),
            "language": job.get("language") or profile.get("default_language"),
        },
        "cover_letter": {
            "recipient": "Recruiting-Team",
            "company_address": ["Nicht angegeben"],
            "date": "Nicht angegeben",
            "subject": data.get("headline"),
            "salutation": "Guten Tag,",
            "paragraphs": data.get("paragraphs", []),
            "closing": "Mit freundlichen Grüßen",
            "signatory": profile.get("full_name"),
        },
        "plain_text": {
            "subject": data.get("headline"),
            "salutation": data.get("salutation", "Guten Tag,"),
            "paragraphs": data.get("paragraphs", []),
            "closing": data.get("closing", "Mit freundlichen Grüßen"),
            "signatory": data.get("signatory") or profile.get("full_name"),
        },
    })


def load_application_content(path: Path, profile: dict[str, Any], legacy_kind: str | None = None,
                             job: dict[str, Any] | None = None) -> dict[str, Any]:
    data = load_json(path)
    if isinstance(data, dict) and data.get("schema_version") == CONTENT_SCHEMA_VERSION:
        return _normalize_v2_content(data)
    if legacy_kind == "cover_letter":
        return legacy_cover_to_content(data, profile, job)
    if legacy_kind == "plain_text":
        return legacy_plain_to_content(data, profile, job)
    raise ValidationError(
        "Content is not application_content.json schema_version 2; use convert_application_content.py"
    )
