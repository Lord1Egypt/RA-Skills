from __future__ import annotations

import os
import re
from pathlib import Path

from .utils import SoulProfile

DEFAULT_NAMES = {"zh": "未命名龙虾", "en": "Unnamed Lobster"}
DEFAULT_TAGS = ["adaptive"]
DEFAULT_PERSONALITY = "steady and curious"
SOUL_FILENAMES = ("SOUL.md", "soul.md")
IDENTITY_FILENAMES = ("IDENTITY.md", "identity.md")
SOUL_ENV_VARS = (
    "OPENCLAW_ROOT",
    "OPENCLAW_HOME",
    "OPENCLAW_WORKSPACE",
    "OPENCLAW_PROJECT_ROOT",
    "OPENCLAW_DIR",
)
SOUL_ROOT_HINTS = ("openclaw", "claw", "workspace", "projects")
TAG_SECTION_HINTS = {"tag", "tags", "traits", "标签", "人格标签", "风格标签"}
PERSONALITY_SECTION_HINTS = {
    "personality",
    "profile",
    "persona",
    "intro",
    "summary",
    "简介",
    "人格",
    "设定",
    "性格",
    "说明",
}
NAME_KEYS = {"name", "lobster_name", "agent_name", "title", "名字", "名称", "龙虾名"}
TAG_KEYS = {"tags", "labels", "traits", "风格标签", "人格标签", "标签"}
PERSONALITY_KEYS = {"personality", "profile", "summary", "简介", "人格", "性格", "设定"}
FILE_STYLE_HEADING = re.compile(r"^[A-Za-z0-9._/-]+\.(?:md|markdown|txt)\b", re.IGNORECASE)
MARKDOWN_BOLD_KEY_VALUE = re.compile(r"^\s*[-*]?\s*\*\*(?P<key>[^*:：]+)\s*[:：]?\*\*\s*[:：]?\s*(?P<value>.+?)\s*$")


def _default_profile(lang: str) -> SoulProfile:
    return SoulProfile(
        name=DEFAULT_NAMES.get(lang, DEFAULT_NAMES["zh"]),
        tags=list(DEFAULT_TAGS),
        personality=DEFAULT_PERSONALITY,
    )


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path.expanduser())
        if key in seen:
            continue
        seen.add(key)
        unique.append(path.expanduser())
    return unique


def _candidate_roots(repo_root: Path) -> list[Path]:
    roots: list[Path] = []

    for env_name in SOUL_ENV_VARS:
        value = os.getenv(env_name)
        if value:
            roots.append(Path(value))

    roots.extend([repo_root, repo_root.parent, Path.cwd()])
    roots.extend(list(Path.cwd().parents)[:4])
    roots.extend(list(repo_root.parents)[:3])

    home = Path.home()
    roots.extend(
        [
            home / "OpenClaw",
            home / "openclaw",
            home / ".openclaw",
            home / "Documents" / "OpenClaw",
            home / "workspace" / "openclaw",
        ]
    )

    return _dedupe_paths(roots)


def _candidate_files(repo_root: Path) -> list[Path]:
    candidates: list[Path] = []
    for root in _candidate_roots(repo_root):
        for filename in SOUL_FILENAMES:
            candidates.append(root / filename)
            candidates.append(root / "workspace" / filename)
            candidates.append(root / "projects" / filename)

        root_name = root.name.lower()
        if any(hint in root_name for hint in SOUL_ROOT_HINTS) and root.exists():
            try:
                for child in root.iterdir():
                    if child.is_dir():
                        for filename in SOUL_FILENAMES:
                            candidates.append(child / filename)
            except OSError:
                continue

    return _dedupe_paths(candidates)


def _candidate_identity_files(repo_root: Path, soul_path: Path | None = None) -> list[Path]:
    candidates: list[Path] = []
    if soul_path:
        candidates.extend(soul_path.parent / filename for filename in IDENTITY_FILENAMES)
    for root in _candidate_roots(repo_root):
        for filename in IDENTITY_FILENAMES:
            candidates.append(root / filename)
            candidates.append(root / "workspace" / filename)
            candidates.append(root / "projects" / filename)
    return _dedupe_paths(candidates)


def find_soul_md_path(repo_root: Path) -> Path | None:
    return next((candidate for candidate in _candidate_files(repo_root) if candidate.exists()), None)


def find_identity_md_path(repo_root: Path, soul_path: Path | None = None) -> Path | None:
    return next((candidate for candidate in _candidate_identity_files(repo_root, soul_path) if candidate.exists()), None)


def _parse_key_value(line: str) -> tuple[str, str] | None:
    markdown_match = MARKDOWN_BOLD_KEY_VALUE.match(line)
    if markdown_match:
        return markdown_match.group("key").strip().lower(), markdown_match.group("value").strip()
    if ":" not in line and "：" not in line:
        return None
    normalized = line.replace("：", ":", 1)
    key, value = normalized.split(":", 1)
    return key.strip().lower(), value.strip()


def _split_tags(value: str) -> list[str]:
    parts = re.split(r"[，,、/|；;]+", value)
    return [part.strip().lstrip("-*").strip() for part in parts if part.strip()]


def _normalize_section_name(raw: str) -> str:
    return raw.replace("：", "").replace(":", "").strip().lower()


def _clean_personality_line(line: str) -> str:
    stripped = line.strip().lstrip("-*").strip()
    stripped = re.sub(r"^>\s*", "", stripped)
    return stripped


def _looks_like_document_heading(value: str) -> bool:
    normalized = value.strip()
    if not normalized:
        return False
    return bool(FILE_STYLE_HEADING.match(normalized))


def _parse_identity_name(identity_path: Path) -> str | None:
    for raw_line in identity_path.read_text(encoding="utf-8").splitlines():
        parsed = _parse_key_value(raw_line.strip())
        if not parsed:
            continue
        key, value = parsed
        if key in NAME_KEYS and value:
            return value.strip()
    return None


def parse_soul_md(repo_root: Path, lang: str = "zh") -> SoulProfile:
    soul_path = find_soul_md_path(repo_root)
    default_name = DEFAULT_NAMES.get(lang, DEFAULT_NAMES["zh"])
    name = default_name
    tags: list[str] = []
    personality_lines: list[str] = []
    current_section = ""
    in_code_fence = False

    if soul_path:
        for raw_line in soul_path.read_text(encoding="utf-8").splitlines():
            stripped = raw_line.strip()
            if stripped.startswith("```"):
                in_code_fence = not in_code_fence
                continue
            if in_code_fence or not stripped:
                continue

            if stripped.startswith("#"):
                section_name = _normalize_section_name(stripped.lstrip("#").strip())
                current_section = section_name
                if stripped.startswith("# ") and name == default_name:
                    heading_name = stripped[2:].strip()
                    if heading_name and not _looks_like_document_heading(heading_name):
                        name = heading_name
                continue

            parsed = _parse_key_value(stripped)
            if parsed:
                key, value = parsed
                if key in NAME_KEYS and value:
                    name = value
                    continue
                if key in TAG_KEYS and value:
                    tags.extend(_split_tags(value))
                    continue
                if key in PERSONALITY_KEYS and value:
                    personality_lines.append(value)
                    continue

            if stripped.startswith(("- ", "* ")):
                item = _clean_personality_line(stripped)
                if current_section in TAG_SECTION_HINTS:
                    tags.append(item)
                elif current_section in PERSONALITY_SECTION_HINTS:
                    personality_lines.append(item)
                elif len(item) <= 18 and len(tags) < 8:
                    tags.append(item)
                else:
                    personality_lines.append(item)
                continue

            if current_section in TAG_SECTION_HINTS:
                tags.extend(_split_tags(stripped))
                continue

            personality_lines.append(_clean_personality_line(stripped))

    if name == default_name:
        identity_path = find_identity_md_path(repo_root, soul_path)
        if identity_path:
            identity_name = _parse_identity_name(identity_path)
            if identity_name:
                name = identity_name

    deduped_tags: list[str] = []
    seen_tags: set[str] = set()
    for tag in tags:
        cleaned = tag.strip()
        if not cleaned or cleaned.lower() in seen_tags:
            continue
        seen_tags.add(cleaned.lower())
        deduped_tags.append(cleaned)

    personality = " ".join(line for line in personality_lines[:8] if line).strip()
    return SoulProfile(
        name=name or default_name,
        tags=deduped_tags or list(DEFAULT_TAGS),
        personality=personality or DEFAULT_PERSONALITY,
    )
