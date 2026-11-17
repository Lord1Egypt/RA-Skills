"""Workspace report filename stems. Reads only regular files inside the workspace."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path

import yaml

_SEP = "－"
_MAX_BYTES = 200
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# Control characters plus characters that are illegal in file names.
_UNSAFE = re.compile(r"[\x00-\x1f\x7f-\x9f\u2028\u2029\ufeff\\/:*?\"<>|]")
_MODES = {
    "discover": "岗位推荐报告",
    "assess": "岗位评估报告",
    "apply": "投递建议报告",
    "interview": "面试复盘报告",
}
_LEGACY = "求职建议报告"
_PROFILE_FILES = ("candidate-profile.yaml", "tailored-profile.yaml", "profile.yaml")


def report_stem(workspace: Path, mode: str) -> str:
    """Build a UTF-8 filename stem of at most 200 bytes.

    Name comes from the first readable profile ``meta.name``. Context comes from
    ``posting.yaml`` (company plus role_title, otherwise title), or else from up
    to three ``brief.yaml`` locations plus the brief's ``report_label`` (a short
    reader-facing direction), falling back to its first target title. The date is the
    first YYYY-MM-DD in ``workspace.name``. Missing pieces are left out. With
    neither a name nor a context, the legacy stem is returned.
    """
    workspace = Path(workspace)
    name = _person_name(workspace)
    context = _context(workspace)
    if not name and not context:
        return _LEGACY
    found = _DATE.search(workspace.name)
    parts = [name, context, found.group(0) if found else None, _report_type(mode)]
    return _fit(_SEP.join(part for part in parts if part))


def _report_type(mode: str) -> str:
    return _MODES.get(mode, _LEGACY)


def _person_name(workspace: Path) -> str | None:
    for filename in _PROFILE_FILES:
        data = _mapping(workspace, filename)
        if data is None:
            continue
        meta = data.get("meta")
        if not isinstance(meta, dict):
            continue
        cleaned = _clean(meta.get("name"))
        if cleaned:
            return cleaned
    return None


def _context(workspace: Path) -> str | None:
    posting = _mapping(workspace, "posting.yaml")
    if posting is not None:
        company = _clean(posting.get("company"))
        role = _clean(posting.get("role_title")) or _clean(posting.get("title"))
        parts = [part for part in (company, role) if part]
        if parts:
            return _SEP.join(parts)
    brief = _mapping(workspace, "brief.yaml")
    if brief is None:
        return None
    # target_titles are search queries, written in both market languages and in
    # run order. Measured 2026-11-01, three of them made a 180-byte name mixing
    # English and Dutch query variants ("…medical imaging AI－medische
    # beeldvorming－LLM engineer…"). A brief names its direction once, in the
    # reader's words, through report_label; otherwise the first, most specific
    # query stands for the round.
    direction = _clean(brief.get("report_label"))
    parts = _strings(brief.get("locations")) + (
        [direction] if direction else _strings(brief.get("target_titles"), limit=1))
    if not parts:
        return None
    return _SEP.join(parts)


def _strings(value: object, limit: int = 3) -> list[str]:
    if not isinstance(value, list):
        return []
    found: list[str] = []
    for item in value:
        cleaned = _clean(item)
        if not cleaned:
            continue
        found.append(cleaned)
        if len(found) >= limit:
            break
    return found


def _clean(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    text = _UNSAFE.sub("", value)
    text = "".join(char for char in text if unicodedata.category(char) not in {"Cc", "Cf", "Cs"}).strip(" .")
    return text or None


def _mapping(workspace: Path, filename: str) -> dict | None:
    """Load one mapping from a regular file. Symlinks and bad YAML are skipped."""
    path = workspace / filename
    try:
        if path.is_symlink() or not path.is_file():
            return None
        raw = path.read_bytes()
    except OSError:
        return None
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def _fit(stem: str) -> str:
    if len(stem.encode("utf-8")) <= _MAX_BYTES:
        return stem
    prefix, _, suffix = stem.rpartition(_SEP)
    if not suffix:
        suffix = _LEGACY
        prefix = stem
    digest = hashlib.sha256(stem.encode("utf-8")).hexdigest()[:8]
    tail = f"{_SEP}{digest}{_SEP}{suffix}"
    room = _MAX_BYTES - len(tail.encode("utf-8"))
    if room <= 0:
        return _truncate(f"{digest}{_SEP}{suffix}", _MAX_BYTES)
    head = _truncate(prefix, room).rstrip(f" {_SEP}.")
    if not head:
        return f"{digest}{_SEP}{suffix}"
    return head + tail


def _truncate(text: str, max_bytes: int) -> str:
    raw = text.encode("utf-8")
    if len(raw) <= max_bytes:
        return text
    raw = raw[:max_bytes]
    while raw:
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            raw = raw[:-1]
    return ""
