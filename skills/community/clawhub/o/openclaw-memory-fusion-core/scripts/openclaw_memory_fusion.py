#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


VERSION = "1.0.1"
DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace"
DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
DEFAULT_LOCAL_MODEL = "hf:ggml-org/embeddinggemma-300M-GGUF/embeddinggemma-300M-Q8_0.gguf"
SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = SKILL_ROOT / "templates"
REQUIRED_EXTRA_PATHS = ["projects", "ops", "memory_fusion/semantic"]
SYSTEM_SECTION_KEYWORDS = (
    "记忆系统",
    "自我改进",
    "token 使用量优化",
    "token",
    "工作强度",
    "heartbeat",
    "心跳",
)
PLACEHOLDER_VALUES = {"", "未指定", "待整理", "（无导入内容）", "No matching daily memory entries found."}
CORRECTION_KEYWORDS = ("纠正", "更正", "改正")
AFFIRMATION_KEYWORDS = ("认可", "采纳", "没问题", "有效", "通过")
STATUS_HINT_KEYWORDS = ("状态", "当前状态", "今日任务", "结果", "进展", "后续", "完成", "已完成", "进行中")
NEXT_STEP_KEYWORDS = ("下一步", "明日安排", "后续", "待准备", "待确认", "Next Step", "计划")
IMPORTANT_HINT_KEYWORDS = ("⚠️", "紧急", "今日任务", "明日安排", "已完成", "完成", "封装", "投标", "预算")
GENERIC_PROJECT_KEYWORDS = {"项目", "投标", "ppt", "计划", "工作", "记录", "时间", "事项", "研究", "可行性", "系统"}
SPECIAL_MATCH_TERMS = ("迁移", "升级", "试点", "汇报", "部署", "migration", "upgrade", "pilot", "report", "deployment")
SKIP_SYSTEM_SECTION_TITLES = {"统计"}
DISPLAY_ALIAS_STOPWORDS = {"项目", "计划", "工作", "研究", "系统", "示例", "demo", "test", "sample"}


@dataclass
class EventRecord:
    event_id: str
    kind: str
    scope: str
    summary: str
    created_at: str
    details: Dict[str, Any]
    project: Optional[str] = None
    source: str = "openclaw-memory-fusion"
    confidence: str = "medium"
    important: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "kind": self.kind,
            "scope": self.scope,
            "summary": self.summary,
            "created_at": self.created_at,
            "details": self.details,
            "project": self.project,
            "source": self.source,
            "confidence": self.confidence,
            "important": self.important,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventRecord":
        return cls(
            event_id=data["event_id"],
            kind=data["kind"],
            scope=data["scope"],
            summary=data["summary"],
            created_at=data["created_at"],
            details=data.get("details", {}),
            project=data.get("project"),
            source=data.get("source", "openclaw-memory-fusion"),
            confidence=data.get("confidence", "medium"),
            important=bool(data.get("important", False)),
        )

    @property
    def created_datetime(self) -> datetime:
        return datetime.fromisoformat(self.created_at)


@dataclass
class Section:
    title: str
    body: str


class Layout:
    def __init__(self, workspace: Path, config_path: Path):
        self.workspace = workspace.expanduser().resolve()
        self.config_path = config_path.expanduser().resolve()
        self.memory_dir = self.workspace / "memory"
        self.fusion_dir = self.workspace / "memory_fusion"
        self.projects_path = self.workspace / "PROJECTS.md"
        self.long_term_path = self.workspace / "MEMORY.md"
        self.improvements_path = self.workspace / "improvements.md"
        self.improvements_history_path = self.memory_dir / "improvements.md"

        self.projects_dir = self.workspace / "projects"
        self.projects_index_path = self.projects_dir / "INDEX.md"
        self.legacy_project_aliases_path = self.projects_dir / "ALIASES.md"
        self.imported_snapshots_dir = self.projects_dir / "imported_snapshots"
        self.imported_snapshots_index_path = self.imported_snapshots_dir / "INDEX.md"

        self.ops_dir = self.workspace / "ops"
        self.ops_backlog_path = self.ops_dir / "improvements_backlog.md"
        self.ops_history_path = self.ops_dir / "improvements_history.md"
        self.ops_system_projects_path = self.ops_dir / "system_projects.md"
        self.ops_tool_gotchas_path = self.ops_dir / "tool_gotchas.md"
        self.ops_upgrade_notes_path = self.ops_dir / "upgrade_notes.md"

        self.project_aliases_path = self.fusion_dir / "project_aliases.md"
        self.events_dir = self.fusion_dir / "events"
        self.archive_dir = self.fusion_dir / "archive"
        self.semantic_dir = self.fusion_dir / "semantic"
        self.manifests_dir = self.fusion_dir / "manifests"
        self.checkpoints_dir = self.fusion_dir / "checkpoints"

    def ensure_dirs(self) -> None:
        for path in [
            self.workspace,
            self.projects_dir,
            self.imported_snapshots_dir,
            self.ops_dir,
            self.fusion_dir,
            self.events_dir,
            self.archive_dir,
            self.semantic_dir,
            self.manifests_dir,
            self.checkpoints_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)


class MutationRecorder:
    def __init__(self, layout: Layout, command: str):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.layout = layout
        self.command = command
        self.manifest_id = f"{timestamp}-{command}"
        self.checkpoint_root = layout.checkpoints_dir / self.manifest_id
        self.backups: Dict[str, str] = {}
        self.created_files: List[str] = []
        self.written_files: List[str] = []
        self.skipped_files: List[str] = []
        self.unchanged_files: List[str] = []
        self.notes: List[str] = []

    def _backup_path_for(self, path: Path) -> Path:
        absolute = path.resolve().as_posix().lstrip("/")
        return self.checkpoint_root / "files" / absolute

    def backup(self, path: Path) -> None:
        key = str(path)
        if key in self.backups or not path.exists():
            return
        backup_path = self._backup_path_for(path)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_path)
        self.backups[key] = str(backup_path)

    def write_text(self, path: Path, content: str, overwrite: bool = False) -> str:
        path = path.expanduser()
        if path.exists():
            current = path.read_text(encoding="utf-8")
            if current == content:
                self.unchanged_files.append(str(path))
                return "unchanged"
            if not overwrite:
                self.skipped_files.append(str(path))
                return "skipped"
            self.backup(path)
        else:
            self.created_files.append(str(path))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        self.written_files.append(str(path))
        return "written"

    def write_json(self, path: Path, payload: Dict[str, Any], overwrite: bool = False) -> str:
        content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        return self.write_text(path, content, overwrite=overwrite)

    def finalize(self, extra: Optional[Dict[str, Any]] = None) -> Path:
        self.layout.manifests_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "id": self.manifest_id,
            "command": self.command,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "workspace": str(self.layout.workspace),
            "config_path": str(self.layout.config_path),
            "checkpoint_root": str(self.checkpoint_root),
            "backups": [
                {"path": path, "backup": backup}
                for path, backup in sorted(self.backups.items())
            ],
            "created_files": self.created_files,
            "written_files": self.written_files,
            "skipped_files": self.skipped_files,
            "unchanged_files": self.unchanged_files,
            "notes": self.notes,
            "status": "applied",
        }
        if extra:
            manifest.update(extra)
        manifest_path = self.layout.manifests_dir / f"{self.manifest_id}.json"
        manifest["manifest_path"] = str(manifest_path)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return manifest_path


class EventStore:
    def __init__(self, layout: Layout):
        self.layout = layout

    def iter_events(self, include_archive: bool = False) -> Iterable[EventRecord]:
        roots = [self.layout.events_dir]
        if include_archive:
            roots.append(self.layout.archive_dir)
        for root in roots:
            if not root.exists():
                continue
            for path in sorted(root.glob("*.jsonl")):
                with path.open("r", encoding="utf-8") as handle:
                    for line in handle:
                        line = line.strip()
                        if not line:
                            continue
                        yield EventRecord.from_dict(json.loads(line))

    def query(
        self,
        days: Optional[int] = None,
        kind: Optional[str] = None,
        project: Optional[str] = None,
        important_only: bool = False,
        include_archive: bool = False,
        limit: int = 20,
    ) -> List[EventRecord]:
        cutoff = None
        if days is not None:
            cutoff = datetime.now() - timedelta(days=days)
        events: List[EventRecord] = []
        for event in self.iter_events(include_archive=include_archive):
            if cutoff and event.created_datetime < cutoff:
                continue
            if kind and event.kind != kind:
                continue
            if project and event.project != project:
                continue
            if important_only and not event.important:
                continue
            events.append(event)
        events.sort(key=lambda item: item.created_datetime, reverse=True)
        return events[:limit]

    def record(self, event: EventRecord, recorder: MutationRecorder) -> Path:
        day = event.created_datetime.strftime("%Y-%m-%d")
        path = self.layout.events_dir / f"{day}.jsonl"
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        appended = existing + json.dumps(event.to_dict(), ensure_ascii=False) + "\n"
        recorder.write_text(path, appended, overwrite=True)
        return path

    def render_semantic_outputs(self, include_archive: bool = False) -> Dict[Path, str]:
        grouped: Dict[str, List[EventRecord]] = {}
        important_events: List[EventRecord] = []
        categories: Dict[str, int] = {}

        for event in self.iter_events(include_archive=include_archive):
            event = normalized_event(event)
            day = event.created_datetime.strftime("%Y-%m-%d")
            grouped.setdefault(day, []).append(event)
            categories[event.kind] = categories.get(event.kind, 0) + 1
            if event.important:
                important_events.append(event)

        outputs: Dict[Path, str] = {}
        for day, events in grouped.items():
            lines = [
                f"# Memory Fusion Structured Digest {day}",
                "",
                "Generated for OpenClaw memorySearch.",
                "",
            ]
            by_kind: Dict[str, List[EventRecord]] = {}
            for event in sorted(events, key=lambda item: item.created_datetime, reverse=True):
                by_kind.setdefault(event.kind, []).append(event)
            for kind in sorted(by_kind):
                lines.append(f"## {kind}")
                for event in by_kind[kind]:
                    important = " [important]" if event.important else ""
                    project = f" | project={event.project}" if event.project else ""
                    lines.append(f"- {event.created_at}{important}{project}: {event.summary}")
                    if event.details:
                        details = json.dumps(event.details, ensure_ascii=False, sort_keys=True)
                        lines.append(f"  - details: {details}")
                lines.append("")
            outputs[self.layout.semantic_dir / f"{day}.md"] = "\n".join(lines).rstrip() + "\n"

        important_events.sort(key=lambda item: item.created_datetime, reverse=True)
        important_lines = [
            "# Memory Fusion Important Events",
            "",
            "High-value structured events for semantic retrieval.",
            "",
        ]
        if important_events:
            for event in important_events[:200]:
                project = f" | project={event.project}" if event.project else ""
                important_lines.append(f"- {event.created_at} | {event.kind}{project}: {event.summary}")
        else:
            important_lines.append("No important events yet.")
        outputs[self.layout.semantic_dir / "IMPORTANT.md"] = "\n".join(important_lines).rstrip() + "\n"

        index_lines = [
            "# Memory Fusion Semantic Index",
            "",
            f"- Updated at: {datetime.now().isoformat(timespec='seconds')}",
            f"- Active digests: {len(grouped)}",
            f"- Categories: {len(categories)}",
            "",
            "## Event Kinds",
            "",
        ]
        if categories:
            for kind in sorted(categories):
                index_lines.append(f"- {kind}: {categories[kind]}")
        else:
            index_lines.append("- No structured events yet.")
        outputs[self.layout.semantic_dir / "INDEX.md"] = "\n".join(index_lines).rstrip() + "\n"
        return outputs


def resolve_workspace(value: Optional[str]) -> Path:
    if value:
        return Path(value).expanduser()
    env_value = os.environ.get("OPENCLAW_WORKSPACE")
    if env_value:
        return Path(env_value).expanduser()
    return DEFAULT_WORKSPACE


def resolve_config_path(value: Optional[str]) -> Path:
    if value:
        return Path(value).expanduser()
    env_value = os.environ.get("OPENCLAW_CONFIG")
    if env_value:
        return Path(env_value).expanduser()
    return DEFAULT_CONFIG_PATH


def load_template(name: str, fallback: str) -> str:
    path = TEMPLATES_DIR / name
    if path.exists():
        return path.read_text(encoding="utf-8")
    return fallback


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def pick_first(fields: Dict[str, str], *names: str, default: str = "未指定") -> str:
    for name in names:
        value = fields.get(name)
        if value:
            return value
    return default


def normalize_body(text: str) -> str:
    return text.strip() or "（无导入内容）"


def slugify(text: str, prefix: str) -> str:
    lowered = text.lower()
    ascii_tokens = re.findall(r"[a-z0-9]+", lowered)
    base = "-".join(ascii_tokens).strip("-")
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
    if not base:
        return f"{prefix}-{digest}"
    base = re.sub(r"-+", "-", base)
    if len(base) < 6 or re.fullmatch(r"\d+(?:-\d+)*", base):
        base = f"{base}-{digest[:6]}"
    return base[:64]


def split_sections(text: str, level: int = 2) -> List[Section]:
    pattern = re.compile(rf"(?m)^{'#' * level}\s+(.+?)\s*$")
    matches = list(pattern.finditer(text))
    sections: List[Section] = []
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        sections.append(Section(title=title, body=body))
    return sections


def extract_fields(body: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for line in body.splitlines():
        match = re.match(r"^\*\*(.+?)\*\*:\s*(.*)$", line.strip())
        if match:
            fields[match.group(1).strip()] = match.group(2).strip()
    return fields


def classify_section(section: Section) -> str:
    title = section.title.lower()
    if any(keyword in title for keyword in SYSTEM_SECTION_KEYWORDS):
        return "ops"
    return "project"


def extract_keywords(text: str) -> List[str]:
    raw_tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z0-9]{3,}", text)
    keywords: List[str] = []
    for token in raw_tokens:
        token = token.strip()
        if not token:
            continue
        if token not in keywords:
            keywords.append(token)
    return keywords[:12]


def excerpt_for_keywords(text: str, keywords: Sequence[str], max_snippets: int = 3) -> str:
    if not keywords:
        return ""
    lines = text.splitlines()
    matched_indexes = [index for index, line in enumerate(lines) if any(keyword in line for keyword in keywords)]
    if not matched_indexes:
        return ""

    snippets: List[str] = []
    seen: set = set()
    for index in matched_indexes:
        start = max(0, index - 2)
        end = min(len(lines), index + 3)
        snippet = "\n".join(lines[start:end]).strip()
        if snippet and snippet not in seen:
            seen.add(snippet)
            snippets.append(snippet)
        if len(snippets) >= max_snippets:
            break
    return "\n\n---\n\n".join(snippets)


def normalize_lookup(text: str) -> str:
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", text.lower())


def truncate_text(text: str, limit: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def clean_memory_line(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    if re.fullmatch(r"\|?[-:\s|]+\|?", text):
        return ""
    if text.startswith("|") and text.endswith("|") and "|" in text[1:-1]:
        cells = [cell.strip() for cell in text.strip("|").split("|")]
        cells = [cell for cell in cells if cell and not re.fullmatch(r"[-: ]+", cell)]
        text = " | ".join(cells)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_event_text(text: str) -> str:
    if "\n" not in text:
        return clean_memory_line(text)
    lines = [clean_memory_line(line) for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def normalize_event_details(value: Any) -> Any:
    if isinstance(value, str):
        return normalize_event_text(value)
    if isinstance(value, list):
        return [normalize_event_details(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_event_details(item) for key, item in value.items()}
    return value


def normalized_event(event: EventRecord) -> EventRecord:
    return EventRecord(
        event_id=event.event_id,
        kind=event.kind,
        scope=event.scope,
        summary=normalize_event_text(event.summary),
        created_at=event.created_at,
        details=normalize_event_details(event.details),
        project=event.project,
        source=event.source,
        confidence=event.confidence,
        important=event.important,
    )


def build_title_aliases(title: str) -> List[str]:
    aliases: List[str] = []
    raw_parts = re.split(r"[\s/（）()·\-—]+", title)
    for part in raw_parts:
        part = part.strip()
        if not part:
            continue
        aliases.append(part)
        normalized = part.replace("市", "")
        if normalized != part:
            aliases.append(normalized)
        chinese_runs = re.findall(r"[\u4e00-\u9fff]{4,}", part)
        for run in chinese_runs:
            aliases.append(run)
            run_no_city = run.replace("市", "")
            if run_no_city != run:
                aliases.append(run_no_city)
            if len(run_no_city) >= 4:
                for start in range(0, max(len(run_no_city) - 3, 1)):
                    chunk = run_no_city[start : start + 5]
                    if len(chunk) >= 4:
                        aliases.append(chunk)
    deduped: List[str] = []
    seen: set[str] = set()
    for alias in aliases:
        key = normalize_lookup(alias)
        if not key or key in seen or key in GENERIC_PROJECT_KEYWORDS:
            continue
        seen.add(key)
        deduped.append(alias)
    return deduped


def extract_org_aliases(text: str) -> List[str]:
    aliases: List[str] = []
    for match in re.findall(r"\*\*(委托方|招标方|客户|单位)\*\*:\s*([^\n]+)", text):
        org = clean_memory_line(match[1])
        if org:
            aliases.append(org)
            aliases.append(org.replace("市", ""))
    return [alias for alias in aliases if alias]


def suggested_title_aliases(title: str) -> List[str]:
    aliases: List[str] = []
    for part in re.split(r"[\s/（）()·\-—]+", title):
        cleaned = clean_memory_line(part)
        if not cleaned:
            continue
        aliases.append(cleaned)
        if "市" in cleaned:
            aliases.append(cleaned.replace("市", ""))
    chinese_phrases = re.findall(r"[\u4e00-\u9fff]{4,}", title)
    for phrase in chinese_phrases:
        cleaned = clean_memory_line(phrase)
        if cleaned:
            aliases.append(cleaned)
            if "市" in cleaned:
                aliases.append(cleaned.replace("市", ""))
    return aliases


def default_force_aliases_for_project(title: str, overview_text: str = "") -> List[str]:
    # Public package default: force aliases come from manual curation only.
    # This avoids shipping opinionated project-specific seeds in the open-source skill.
    return []


def default_aliases_for_project(title: str, overview_text: str = "") -> List[str]:
    aliases: List[str] = []
    aliases.extend(suggested_title_aliases(title))
    aliases.extend(extract_org_aliases(overview_text))

    deduped: List[str] = []
    seen: set[str] = set()
    title_key = normalize_lookup(clean_memory_line(title))
    for alias in aliases:
        cleaned = clean_memory_line(alias)
        key = normalize_lookup(cleaned)
        if not cleaned or not key or key == title_key or key in seen or key in DISPLAY_ALIAS_STOPWORDS:
            continue
        seen.add(key)
        deduped.append(cleaned)
    return deduped


def parse_alias_registry(text: str) -> Dict[str, Dict[str, Any]]:
    entries: Dict[str, Dict[str, Any]] = {}
    current_slug: Optional[str] = None
    current_section: Optional[str] = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current_slug = heading.group(1).strip()
            current_section = None
            entries.setdefault(current_slug, {"title": "", "force_aliases": [], "suggested_aliases": []})
            continue
        if not current_slug:
            continue
        if line.strip().startswith("- Title:"):
            entries[current_slug]["title"] = line.split(":", 1)[1].strip()
            current_section = None
            continue
        stripped = line.strip()
        if stripped in {"- Force aliases:", "Force aliases:"}:
            current_section = "force_aliases"
            continue
        if stripped in {"- Suggested aliases:", "Suggested aliases:"}:
            current_section = "suggested_aliases"
            continue
        if stripped in {"- Aliases:", "Aliases:"}:
            current_section = "suggested_aliases"
            continue
        alias_match = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if alias_match and current_section:
            alias = clean_memory_line(alias_match.group(1))
            if alias and alias != "Title:" and alias not in entries[current_slug][current_section]:
                entries[current_slug][current_section].append(alias)
    return entries


def render_alias_registry(entries: Sequence[Dict[str, Any]], generated_at: str) -> str:
    template = load_template(
        "project_aliases.md",
        "# Project Aliases\n\n{body}\n",
    )
    body_lines: List[str] = []
    if not entries:
        body_lines.append("No project aliases yet.")
    else:
        for entry in entries:
            body_lines.append(f"## {entry['slug']}")
            body_lines.append(f"- Title: {entry['title']}")
            body_lines.append("- Force aliases:")
            force_aliases = entry.get("force_aliases", [])
            if force_aliases:
                for alias in force_aliases:
                    body_lines.append(f"  - {alias}")
            else:
                body_lines.append("  - （手工添加）")
            body_lines.append("- Suggested aliases:")
            suggested_aliases = entry.get("suggested_aliases", [])
            if suggested_aliases:
                for alias in suggested_aliases:
                    body_lines.append(f"  - {alias}")
            else:
                body_lines.append("  - （暂无自动建议）")
            body_lines.append("")
    return template.format(generated_at=generated_at, body="\n".join(body_lines).rstrip())


def merge_alias_registry_entries(
    base: Dict[str, Dict[str, Any]],
    incoming: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    merged = {slug: {"title": data.get("title", ""), "force_aliases": list(data.get("force_aliases", [])), "suggested_aliases": list(data.get("suggested_aliases", []))} for slug, data in base.items()}
    for slug, data in incoming.items():
        entry = merged.setdefault(slug, {"title": "", "force_aliases": [], "suggested_aliases": []})
        if data.get("title"):
            entry["title"] = data["title"]
        for key in ("force_aliases", "suggested_aliases"):
            seen = {normalize_lookup(alias) for alias in entry.get(key, []) if normalize_lookup(alias)}
            for alias in data.get(key, []):
                cleaned = clean_memory_line(alias)
                normalized = normalize_lookup(cleaned)
                if not cleaned or not normalized or normalized in seen:
                    continue
                seen.add(normalized)
                entry.setdefault(key, []).append(cleaned)
    return merged


def load_alias_registry(layout: Layout) -> Dict[str, Dict[str, Any]]:
    registry: Dict[str, Dict[str, Any]] = {}
    for path in (layout.project_aliases_path, layout.legacy_project_aliases_path):
        if not path.exists():
            continue
        registry = merge_alias_registry_entries(registry, parse_alias_registry(read_text(path)))
    return registry


def build_alias_registry(layout: Layout) -> str:
    generated_at = datetime.now().isoformat(timespec="seconds")
    existing = load_alias_registry(layout)

    entries: List[Dict[str, Any]] = []
    for overview_path in sorted(layout.projects_dir.glob("*/overview.md")):
        text = read_text(overview_path)
        heading_match = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
        if not heading_match:
            continue
        slug = overview_path.parent.name
        title = heading_match.group(1).strip()
        generated_force_aliases = default_force_aliases_for_project(title, text)
        generated_suggested_aliases = default_aliases_for_project(title, text)
        manual_force_aliases = existing.get(slug, {}).get("force_aliases", [])
        manual_suggested_aliases = existing.get(slug, {}).get("suggested_aliases", [])
        merged_force: List[str] = []
        force_seen: set[str] = set()
        for alias in [*manual_force_aliases, *generated_force_aliases]:
            cleaned = clean_memory_line(alias)
            key = normalize_lookup(cleaned)
            if not cleaned or not key or key in force_seen:
                continue
            force_seen.add(key)
            merged_force.append(cleaned)

        merged_suggested: List[str] = []
        seen: set[str] = set()
        for alias in [*manual_suggested_aliases, *generated_suggested_aliases]:
            cleaned = clean_memory_line(alias)
            key = normalize_lookup(cleaned)
            if not cleaned or not key or key in seen or key in force_seen:
                continue
            seen.add(key)
            merged_suggested.append(cleaned)
        entries.append(
            {
                "slug": slug,
                "title": title,
                "force_aliases": merged_force,
                "suggested_aliases": merged_suggested,
            }
        )
    return render_alias_registry(entries, generated_at=generated_at)


def split_sections_fallback(text: str) -> List[Section]:
    sections = split_sections(text, level=2)
    if sections:
        return sections
    fallback = text.strip()
    if not fallback:
        return []
    return [Section(title="Document", body=fallback)]


def parse_file_date(path: Path) -> Optional[datetime]:
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", path.stem)
    if not match:
        return None
    return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)), 9, 0, 0)


def absolutize_relative_time(text: str, base_dt: Optional[datetime]) -> str:
    if not text or not base_dt:
        return text
    updated = text
    replacements = {
        "今天": base_dt.strftime("%Y年%-m月%-d日"),
        "今日": base_dt.strftime("%Y年%-m月%-d日"),
        "明天": (base_dt + timedelta(days=1)).strftime("%Y年%-m月%-d日"),
        "明日": (base_dt + timedelta(days=1)).strftime("%Y年%-m月%-d日"),
        "后天": (base_dt + timedelta(days=2)).strftime("%Y年%-m月%-d日"),
        "昨天": (base_dt - timedelta(days=1)).strftime("%Y年%-m月%-d日"),
        "昨日": (base_dt - timedelta(days=1)).strftime("%Y年%-m月%-d日"),
    }
    for raw, absolute in replacements.items():
        updated = updated.replace(raw, absolute)

    def replace_month_day(match: re.Match[str]) -> str:
        if match.group(1):
            return match.group(0)
        month = int(match.group(2))
        day = int(match.group(3))
        return f"{base_dt.year}年{month}月{day}日"

    updated = re.sub(r"(?:(\d{4})年)?(\d{1,2})月(\d{1,2})日", replace_month_day, updated)
    return updated


def extract_meaningful_lines(body: str, limit: int = 3, base_dt: Optional[datetime] = None) -> List[str]:
    lines: List[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#") or line == "---":
            continue
        cleaned = re.sub(r"^\-\s*", "", line)
        cleaned = re.sub(r"^\d+\.\s*", "", cleaned)
        cleaned = clean_memory_line(cleaned)
        if not cleaned:
            continue
        cleaned = absolutize_relative_time(cleaned, base_dt)
        if cleaned not in lines:
            lines.append(cleaned)
        if len(lines) >= limit:
            break
    return lines


def load_project_catalog(layout: Layout) -> List[Dict[str, Any]]:
    catalog: List[Dict[str, Any]] = []
    alias_registry = load_alias_registry(layout)
    if not layout.projects_dir.exists():
        return catalog
    for overview_path in sorted(layout.projects_dir.glob("*/overview.md")):
        text = read_text(overview_path)
        heading_match = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
        if not heading_match:
            continue
        title = heading_match.group(1).strip()
        slug = overview_path.parent.name
        keywords = extract_keywords(title)
        meaningful_keywords = [
            keyword
            for keyword in keywords
            if normalize_lookup(keyword) and normalize_lookup(keyword) not in GENERIC_PROJECT_KEYWORDS
        ]
        manual_force_aliases = alias_registry.get(slug, {}).get("force_aliases", [])
        manual_suggested_aliases = alias_registry.get(slug, {}).get("suggested_aliases", [])
        generated_force_aliases = default_force_aliases_for_project(title, text)
        generated_suggested_aliases = default_aliases_for_project(title, text)
        aliases = {normalize_lookup(title), normalize_lookup(slug)}
        aliases.update(normalize_lookup(keyword) for keyword in meaningful_keywords)
        aliases.update(normalize_lookup(alias) for alias in build_title_aliases(title))
        aliases.update(normalize_lookup(alias) for alias in manual_suggested_aliases)
        aliases.update(normalize_lookup(alias) for alias in generated_suggested_aliases)
        aliases.update(normalize_lookup(alias) for alias in generated_force_aliases)
        aliases.update(normalize_lookup(alias) for alias in manual_force_aliases)
        force_aliases = {
            normalize_lookup(alias)
            for alias in [*manual_force_aliases, *generated_force_aliases]
            if normalize_lookup(alias)
        }
        catalog.append(
            {
                "title": title,
                "slug": slug,
                "keywords": meaningful_keywords or keywords,
                "aliases": {alias for alias in aliases if alias},
                "forceAliases": force_aliases,
                "manualAliases": {
                    "force": manual_force_aliases,
                    "suggested": manual_suggested_aliases,
                },
            }
        )
    return catalog


def match_project(layout: Layout, title: str, body: str, catalog: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    haystack = normalize_lookup(title + "\n" + body)
    if not haystack:
        return None
    catalog = catalog or load_project_catalog(layout)
    force_matches: List[Tuple[int, Dict[str, Any]]] = []
    for candidate in catalog:
        for alias in candidate.get("forceAliases", set()):
            if alias and alias in haystack:
                force_matches.append((len(alias), candidate))
    if force_matches:
        force_matches.sort(key=lambda item: item[0], reverse=True)
        return force_matches[0][1]
    best: Optional[Dict[str, Any]] = None
    best_score = 0
    for candidate in catalog:
        score = 0
        title_key = normalize_lookup(candidate["title"])
        if title_key and title_key in haystack:
            score += 6
        for alias in candidate["aliases"]:
            if alias and alias in haystack:
                score += 2
        overlap = sum(1 for keyword in candidate["keywords"] if normalize_lookup(keyword) in haystack)
        score += overlap
        for term in SPECIAL_MATCH_TERMS:
            normalized_term = normalize_lookup(term)
            if normalized_term in haystack:
                if normalized_term in title_key:
                    score += 3
                else:
                    score -= 1
        if score > best_score:
            best_score = score
            best = candidate
    if best is None:
        return None
    title_key = normalize_lookup(best["title"])
    if title_key and title_key in haystack:
        return best
    matched_keywords = [keyword for keyword in best["keywords"] if normalize_lookup(keyword) in haystack]
    if len(matched_keywords) >= 2:
        return best
    if any(len(normalize_lookup(keyword)) >= 6 for keyword in matched_keywords):
        return best
    if best_score >= 5:
        return best
    if len(matched_keywords) < 1:
        return None
    return best


def collect_candidate_lines(body: str, keywords: Sequence[str], base_dt: Optional[datetime] = None) -> List[str]:
    matches: List[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if any(keyword in line for keyword in keywords):
            cleaned = re.sub(r"^\-\s*", "", line)
            cleaned = clean_memory_line(cleaned)
            if not cleaned:
                continue
            cleaned = absolutize_relative_time(cleaned, base_dt)
            if cleaned not in matches:
                matches.append(cleaned)
    return matches[:5]


def parse_overview_snapshot(text: str) -> Dict[str, str]:
    snapshot = {"goal": "", "status": "", "next_step": ""}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- Goal:"):
            snapshot["goal"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Status:"):
            snapshot["status"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Next step:"):
            snapshot["next_step"] = stripped.split(":", 1)[1].strip()
    return snapshot


def replace_overview_snapshot(text: str, status: Optional[str] = None, next_step: Optional[str] = None) -> str:
    updated = text
    if status is not None:
        cleaned_status = normalize_event_text(status)
        updated = re.sub(r"(?m)^- Status:\s*.*$", f"- Status: {cleaned_status}", updated)
    if next_step is not None:
        cleaned_next_step = normalize_event_text(next_step)
        updated = re.sub(r"(?m)^- Next step:\s*.*$", f"- Next step: {cleaned_next_step}", updated)
    return updated


def event_signature(event: EventRecord) -> str:
    payload = {
        "kind": event.kind,
        "scope": event.scope,
        "summary": event.summary,
        "created_at": event.created_at,
        "project": event.project,
        "details": event.details,
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def existing_event_signatures(layout: Layout) -> set[str]:
    store = EventStore(layout)
    return {event_signature(normalized_event(event)) for event in store.iter_events(include_archive=True)}


def collect_source_files(layout: Layout, days: int, include_ops: bool = True) -> List[Path]:
    sources: List[Path] = []
    cutoff = datetime.now() - timedelta(days=days)
    if layout.memory_dir.exists():
        for path in sorted(layout.memory_dir.glob("*.md")):
            file_dt = parse_file_date(path)
            if file_dt and file_dt < cutoff:
                continue
            sources.append(path)
    if include_ops:
        for path in [layout.improvements_path, layout.improvements_history_path]:
            if path.exists():
                sources.append(path)
    return sources


def collect_auto_capture_events(layout: Layout, days: int = 7, include_ops: bool = True) -> List[EventRecord]:
    catalog = load_project_catalog(layout)
    seen = existing_event_signatures(layout)
    candidates: List[EventRecord] = []
    source_paths = collect_source_files(layout, days=days, include_ops=include_ops)

    for path in source_paths:
        text = read_text(path)
        base_dt = parse_file_date(path)
        relative_source = str(path.relative_to(layout.workspace))

        for section in split_sections_fallback(text):
            body = section.body.strip()
            if not body:
                continue

            project = match_project(layout, section.title, body, catalog=catalog)
            status_candidates = collect_candidate_lines(body, STATUS_HINT_KEYWORDS, base_dt=base_dt)
            next_step_candidates = collect_candidate_lines(body, NEXT_STEP_KEYWORDS, base_dt=base_dt)
            excerpt = "\n".join(extract_meaningful_lines(body, limit=4, base_dt=base_dt))
            created_at = (base_dt or datetime.now()).isoformat(timespec="seconds")

            if project:
                project_excerpt = excerpt_for_keywords(body, project["keywords"], max_snippets=1)
                project_lines = extract_meaningful_lines(project_excerpt or body, limit=4, base_dt=base_dt)
                excerpt = "\n".join(project_lines)
                summary_bits = [project["title"]]
                if status_candidates:
                    summary_bits.append(status_candidates[0])
                elif project_lines:
                    summary_bits.append(project_lines[0])
                summary = truncate_text(" | ".join(summary_bits))
                important = any(keyword in body for keyword in IMPORTANT_HINT_KEYWORDS)
                event = EventRecord(
                    event_id=str(uuid.uuid4()),
                    kind="project_update",
                    scope="project",
                    summary=summary,
                    created_at=created_at,
                    details={
                        "source_path": relative_source,
                        "section_title": section.title,
                        "excerpt": excerpt,
                        "status_candidates": status_candidates,
                        "next_steps": next_step_candidates,
                    },
                    project=project["slug"],
                    source="auto-capture",
                    confidence="medium",
                    important=important,
                )
                signature = event_signature(event)
                if signature not in seen:
                    seen.add(signature)
                    candidates.append(event)
                continue

            lowered_title = section.title.lower()
            if any(keyword in lowered_title for keyword in CORRECTION_KEYWORDS):
                for line in extract_meaningful_lines(body, limit=6, base_dt=base_dt):
                    event = EventRecord(
                        event_id=str(uuid.uuid4()),
                        kind="user_correction",
                        scope="durable",
                        summary=truncate_text(line),
                        created_at=created_at,
                        details={"source_path": relative_source, "section_title": section.title},
                        source="auto-capture",
                        confidence="high",
                        important=True,
                    )
                    signature = event_signature(event)
                    if signature not in seen:
                        seen.add(signature)
                        candidates.append(event)
                continue

            if any(keyword in lowered_title for keyword in AFFIRMATION_KEYWORDS):
                for line in extract_meaningful_lines(body, limit=4, base_dt=base_dt):
                    event = EventRecord(
                        event_id=str(uuid.uuid4()),
                        kind="user_affirmation",
                        scope="durable",
                        summary=truncate_text(line),
                        created_at=created_at,
                        details={"source_path": relative_source, "section_title": section.title},
                        source="auto-capture",
                        confidence="medium",
                        important=False,
                    )
                    signature = event_signature(event)
                    if signature not in seen:
                        seen.add(signature)
                        candidates.append(event)
                continue

            if path == layout.improvements_path or path == layout.improvements_history_path:
                if section.title.strip() in SKIP_SYSTEM_SECTION_TITLES:
                    continue
                first_lines = extract_meaningful_lines(body, limit=3, base_dt=base_dt)
                if not first_lines:
                    continue
                event = EventRecord(
                    event_id=str(uuid.uuid4()),
                    kind="system_improvement",
                    scope="durable",
                    summary=truncate_text(f"{section.title}: {first_lines[0]}"),
                    created_at=created_at,
                    details={
                        "source_path": relative_source,
                        "section_title": section.title,
                        "excerpt": "\n".join(first_lines),
                    },
                    source="auto-capture",
                    confidence="medium",
                    important=any(keyword in body for keyword in IMPORTANT_HINT_KEYWORDS),
                )
                signature = event_signature(event)
                if signature not in seen:
                    seen.add(signature)
                    candidates.append(event)

    return candidates


def latest_detail_value(events: Sequence[EventRecord], key: str) -> Optional[str]:
    for event in sorted(events, key=lambda item: item.created_datetime, reverse=True):
        values = event.details.get(key)
        if isinstance(values, list) and values:
            value = normalize_event_text(str(values[0]).strip())
            if value:
                return value
    return None


def build_drift_findings(layout: Layout, days: int = 30) -> List[Dict[str, Any]]:
    store = EventStore(layout)
    findings: List[Dict[str, Any]] = []
    for overview_path in sorted(layout.projects_dir.glob("*/overview.md")):
        text = read_text(overview_path)
        snapshot = parse_overview_snapshot(text)
        title_match = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
        title = title_match.group(1).strip() if title_match else overview_path.parent.name
        slug = overview_path.parent.name
        events = [normalized_event(event) for event in store.query(days=days, project=slug, limit=20)]
        if not events:
            continue

        status_candidate = latest_detail_value(events, "status_candidates")
        next_step_candidate = latest_detail_value(events, "next_steps")
        repairs: Dict[str, str] = {}
        warnings: List[str] = []

        current_status = snapshot.get("status", "").strip()
        current_next = snapshot.get("next_step", "").strip()

        if status_candidate and current_status in PLACEHOLDER_VALUES:
            repairs["status"] = status_candidate
        elif status_candidate and current_status and current_status not in PLACEHOLDER_VALUES and normalize_lookup(current_status) != normalize_lookup(status_candidate):
            warnings.append(f"Status may have drifted: current=`{current_status}` latest=`{status_candidate}`")

        if next_step_candidate and current_next in PLACEHOLDER_VALUES:
            repairs["next_step"] = next_step_candidate
        elif next_step_candidate and current_next and current_next not in PLACEHOLDER_VALUES and normalize_lookup(current_next) != normalize_lookup(next_step_candidate):
            warnings.append(f"Next step may have drifted: current=`{current_next}` latest=`{next_step_candidate}`")

        if re.search(r"(今天|今日|明天|明日|后天|昨天|昨日)", current_status):
            repairs.setdefault("status", absolutize_relative_time(current_status, events[0].created_datetime))
        if re.search(r"(今天|今日|明天|明日|后天|昨天|昨日)", current_next):
            repairs.setdefault("next_step", absolutize_relative_time(current_next, events[0].created_datetime))

        if repairs or warnings:
            findings.append(
                {
                    "title": title,
                    "slug": slug,
                    "overview_path": str(overview_path),
                    "current": snapshot,
                    "repairs": repairs,
                    "warnings": warnings,
                    "latest_event": events[0].to_dict(),
                }
            )
    return findings


def render_drift_report(findings: Sequence[Dict[str, Any]]) -> str:
    lines = [
        "# Memory Fusion Drift Report",
        "",
        f"- Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"- Projects with findings: {len(findings)}",
        "",
    ]
    if not findings:
        lines.append("No drift findings detected.")
        return "\n".join(lines).rstrip() + "\n"

    for item in findings:
        lines.append(f"## {item['title']}")
        lines.append("")
        current = item["current"]
        lines.append(f"- Current status: {current.get('status') or '（空）'}")
        lines.append(f"- Current next step: {current.get('next_step') or '（空）'}")
        repairs = item.get("repairs", {})
        if repairs:
            if "status" in repairs:
                lines.append(f"- Suggested status repair: {repairs['status']}")
            if "next_step" in repairs:
                lines.append(f"- Suggested next-step repair: {repairs['next_step']}")
        for warning in item.get("warnings", []):
            lines.append(f"- Warning: {warning}")
        latest_event = item.get("latest_event", {})
        if latest_event:
            lines.append(f"- Latest event: {latest_event.get('created_at')} | {latest_event.get('summary')}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_dream_summary(
    auto_events: Sequence[EventRecord],
    drift_findings: Sequence[Dict[str, Any]],
    repaired_files: Sequence[str],
) -> str:
    lines = [
        "# Memory Fusion Dream Summary",
        "",
        f"- Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"- Auto-captured events: {len(auto_events)}",
        f"- Drift findings: {len(drift_findings)}",
        f"- Repaired overview files: {len(repaired_files)}",
        "",
        "## Auto-captured Events",
        "",
    ]
    if auto_events:
        for event in list(auto_events)[:20]:
            project = f" | project={event.project}" if event.project else ""
            lines.append(f"- {event.created_at} | {event.kind}{project}: {event.summary}")
    else:
        lines.append("- No new events were captured.")
    lines.append("")
    lines.append("## Drift Highlights")
    lines.append("")
    if drift_findings:
        for item in drift_findings[:20]:
            summary = []
            if item.get("repairs", {}).get("status"):
                summary.append(f"status -> {item['repairs']['status']}")
            if item.get("repairs", {}).get("next_step"):
                summary.append(f"next_step -> {item['repairs']['next_step']}")
            if item.get("warnings"):
                summary.extend(item["warnings"])
            lines.append(f"- {item['title']}: {'; '.join(summary) if summary else 'review suggested'}")
    else:
        lines.append("- No drift issues detected.")
    return "\n".join(lines).rstrip() + "\n"


def collect_timeline_entries(layout: Layout, section: Section) -> str:
    keywords = extract_keywords(section.title + "\n" + section.body)
    entries: List[str] = []
    if not layout.memory_dir.exists():
        return "No matching daily memory entries found."
    for path in sorted(layout.memory_dir.glob("*.md")):
        if path.name == "improvements.md":
            continue
        text = read_text(path)
        excerpt = excerpt_for_keywords(text, keywords)
        if excerpt:
            entries.append(f"## {path.stem}\n\nSource: `{path.relative_to(layout.workspace)}`\n\n{excerpt}")
    if not entries:
        return "No matching daily memory entries found."
    return "\n\n".join(entries)


def collect_decision_entries(section: Section) -> str:
    fields = extract_fields(section.body)
    entries: List[str] = []
    reason = pick_first(fields, "Reason", "理由", "备注", default="")
    if reason:
        entries.append(f"- Reason / note: {reason}")
    strategy = pick_first(fields, "策略", default="")
    if strategy:
        entries.append(f"- Strategy: {strategy}")
    if "决策" in section.body:
        entries.append("- Imported body contains decision-related content; review the overview and timeline.")
    if not entries:
        return "- No explicit decision lines were extracted during migration."
    return "\n".join(entries)


def collect_artifact_entries(layout: Layout, section: Section) -> Tuple[str, List[Tuple[Path, str]]]:
    keywords = extract_keywords(section.title + "\n" + section.body)
    entries = [f"- Primary source: `PROJECTS.md` section `{section.title}`"]
    imports: List[Tuple[Path, str]] = []
    for path in sorted(layout.workspace.glob("*项目情况汇总*.md")):
        text = read_text(path)
        excerpt = excerpt_for_keywords(text, keywords, max_snippets=2)
        if excerpt:
            entries.append(f"- Matching imported snapshot: `{path.name}`")
            imports.append((path, excerpt))
    return "\n".join(entries), imports


def render_project_files(layout: Layout, section: Section, migrated_at: str) -> Dict[Path, str]:
    slug = slugify(section.title, "project")
    project_dir = layout.projects_dir / slug
    fields = extract_fields(section.body)
    overview_template = load_template(
        "project_overview.md",
        "# {title}\n\n## Imported Notes\n\n{imported_body}\n",
    )
    timeline_template = load_template(
        "project_timeline.md",
        "# {title} Timeline\n\n{timeline_entries}\n",
    )
    decisions_template = load_template(
        "project_decisions.md",
        "# {title} Decisions\n\n{decision_entries}\n",
    )
    artifacts_template = load_template(
        "project_artifacts.md",
        "# {title} Artifacts\n\n{artifact_entries}\n",
    )

    goal = pick_first(fields, "Goal", "目标", "内容", "研究内容")
    status = pick_first(fields, "Status", "当前状态", "状态")
    next_step = pick_first(fields, "Next Step", "下一步", "触发条件", default="待整理")
    artifact_entries, imports = collect_artifact_entries(layout, section)
    outputs = {
        project_dir / "overview.md": overview_template.format(
            title=section.title,
            slug=slug,
            kind="project",
            source_path="PROJECTS.md",
            migrated_at=migrated_at,
            goal=goal,
            status=status,
            next_step=next_step,
            imported_body=normalize_body(section.body),
        ),
        project_dir / "timeline.md": timeline_template.format(
            title=section.title,
            slug=slug,
            migrated_at=migrated_at,
            timeline_entries=collect_timeline_entries(layout, section),
        ),
        project_dir / "decisions.md": decisions_template.format(
            title=section.title,
            slug=slug,
            migrated_at=migrated_at,
            decision_entries=collect_decision_entries(section),
        ),
        project_dir / "artifacts.md": artifacts_template.format(
            title=section.title,
            slug=slug,
            migrated_at=migrated_at,
            artifact_entries=artifact_entries,
        ),
    }

    for import_path, excerpt in imports:
        imported_slug = slugify(import_path.stem, "snapshot")
        target = layout.imported_snapshots_dir / f"{imported_slug}.md"
        outputs[target] = (
            f"# Imported Snapshot: {import_path.stem}\n\n"
            f"- Original path: `{import_path}`\n"
            f"- Imported at: {migrated_at}\n\n"
            "## Relevant Excerpt\n\n"
            f"{excerpt}\n"
        )
    return outputs


def render_projects_index(projects: List[Tuple[str, str, str]], snapshots: List[str], migrated_at: str) -> str:
    template = load_template(
        "projects_index.md",
        "# Projects Index\n\n{project_entries}\n",
    )
    if projects:
        project_entries = "\n".join(
            f"- [{title}](./{slug}/overview.md) — {status}" for title, slug, status in projects
        )
    else:
        project_entries = "- No migrated project records yet."
    if snapshots:
        snapshot_entries = "\n".join(f"- [{name}](./imported_snapshots/{name})" for name in snapshots)
    else:
        snapshot_entries = "- No imported snapshots."
    return template.format(
        migrated_at=migrated_at,
        project_entries=project_entries,
        snapshot_entries=snapshot_entries,
    )


def build_base_outputs(layout: Layout, migrated_at: str) -> Dict[Path, str]:
    outputs: Dict[Path, str] = {}
    outputs[layout.projects_index_path] = render_projects_index([], [], migrated_at)
    alias_template = load_template(
        "project_aliases.md",
        "# Project Aliases\n\n{body}\n",
    )
    outputs[layout.project_aliases_path] = alias_template.format(
        generated_at=migrated_at,
        body="No project aliases yet.",
    )
    backlog_template = load_template(
        "ops_backlog.md",
        "# Ops Improvements Backlog\n\n{imported_body}\n",
    )
    history_template = load_template(
        "ops_history.md",
        "# Ops Improvements History\n\n{imported_body}\n",
    )
    system_template = load_template(
        "ops_system_projects.md",
        "# System Projects\n\n{imported_body}\n",
    )
    outputs[layout.ops_backlog_path] = backlog_template.format(
        migrated_at=migrated_at,
        source_path="improvements.md",
        imported_body="No backlog imported yet.",
    )
    outputs[layout.ops_history_path] = history_template.format(
        migrated_at=migrated_at,
        source_path="memory/improvements.md",
        imported_body="No history imported yet.",
    )
    outputs[layout.ops_system_projects_path] = system_template.format(
        migrated_at=migrated_at,
        imported_body="No system project sections imported yet.",
    )
    outputs[layout.ops_tool_gotchas_path] = (
        "# Tool Gotchas\n\n"
        "- Add tool-specific memory retrieval quirks here.\n"
        "- This file is indexed by openclaw-memory-fusion via memorySearch extra paths.\n"
    )
    outputs[layout.ops_upgrade_notes_path] = (
        "# Upgrade Notes\n\n"
        "- Track OpenClaw version changes, migration notes, and compatibility observations here.\n"
    )
    outputs[layout.imported_snapshots_index_path] = (
        "# Imported Project Snapshots\n\n- No imported snapshots yet.\n"
    )
    return outputs


def build_migration_outputs(layout: Layout) -> Tuple[Dict[Path, str], Dict[str, Any]]:
    outputs = build_base_outputs(layout, migrated_at=datetime.now().isoformat(timespec="seconds"))
    migrated_at = datetime.now().isoformat(timespec="seconds")
    report: Dict[str, Any] = {
        "project_sections": 0,
        "ops_sections": 0,
        "snapshot_files": 0,
        "generated_files": 0,
        "projects": [],
        "snapshots": [],
    }

    project_rows: List[Tuple[str, str, str]] = []
    snapshot_names: List[str] = []
    ops_sections: List[str] = []

    if layout.projects_path.exists():
        sections = split_sections(read_text(layout.projects_path), level=2)
        for section in sections:
            kind = classify_section(section)
            if kind == "ops":
                report["ops_sections"] += 1
                ops_sections.append(f"## {section.title}\n\n{normalize_body(section.body)}")
                continue

            report["project_sections"] += 1
            project_files = render_project_files(layout, section, migrated_at)
            slug = slugify(section.title, "project")
            fields = extract_fields(section.body)
            status = pick_first(fields, "Status", "当前状态", "状态")
            project_rows.append((section.title, slug, status))
            report["projects"].append({"title": section.title, "slug": slug, "status": status})
            for path, content in project_files.items():
                outputs[path] = content
                if path.parent == layout.imported_snapshots_dir and path.name not in snapshot_names:
                    snapshot_names.append(path.name)

    if layout.improvements_path.exists():
        backlog_template = load_template("ops_backlog.md", "# Ops Improvements Backlog\n\n{imported_body}\n")
        outputs[layout.ops_backlog_path] = backlog_template.format(
            migrated_at=migrated_at,
            source_path="improvements.md",
            imported_body=normalize_body(read_text(layout.improvements_path)),
        )

    if layout.improvements_history_path.exists():
        history_template = load_template("ops_history.md", "# Ops Improvements History\n\n{imported_body}\n")
        outputs[layout.ops_history_path] = history_template.format(
            migrated_at=migrated_at,
            source_path="memory/improvements.md",
            imported_body=normalize_body(read_text(layout.improvements_history_path)),
        )

    if ops_sections:
        system_template = load_template("ops_system_projects.md", "# System Projects\n\n{imported_body}\n")
        outputs[layout.ops_system_projects_path] = system_template.format(
            migrated_at=migrated_at,
            imported_body="\n\n---\n\n".join(ops_sections),
        )

    for path in sorted(layout.workspace.glob("*项目情况汇总*.md")):
        report["snapshot_files"] += 1
        slug = slugify(path.stem, "snapshot")
        target = layout.imported_snapshots_dir / f"{slug}.md"
        outputs[target] = (
            f"# Imported Snapshot: {path.stem}\n\n"
            f"- Original path: `{path}`\n"
            f"- Imported at: {migrated_at}\n\n"
            "## Full Content\n\n"
            f"{normalize_body(read_text(path))}\n"
        )
        if target.name not in snapshot_names:
            snapshot_names.append(target.name)

    outputs[layout.projects_index_path] = render_projects_index(project_rows, snapshot_names, migrated_at)
    outputs[layout.imported_snapshots_index_path] = (
        "# Imported Project Snapshots\n\n" +
        ("\n".join(f"- [{name}](./{name})" for name in snapshot_names) if snapshot_names else "- No imported snapshots.") +
        "\n"
    )

    report["generated_files"] = len(outputs)
    report["snapshots"] = snapshot_names
    return outputs, report


def parse_details(raw: Optional[str]) -> Dict[str, Any]:
    if not raw:
        return {}
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise SystemExit("--details-json must decode to an object")
    return parsed


def inspect_memory_search(config_path: Path) -> Dict[str, Any]:
    if not config_path.exists():
        return {"config_exists": False}
    payload = read_json(config_path)
    memory_search = payload.get("agents", {}).get("defaults", {}).get("memorySearch", {})
    return {
        "config_exists": True,
        "enabled": bool(memory_search.get("enabled", False)),
        "provider": memory_search.get("provider"),
        "model": memory_search.get("model"),
        "extraPaths": memory_search.get("extraPaths", []),
        "sessionMemory": bool(memory_search.get("experimental", {}).get("sessionMemory", False)),
    }


def ensure_memory_search_config(
    config: Dict[str, Any],
    provider: str,
    model: Optional[str],
    api_key: Optional[str],
    base_url: Optional[str],
    fallback: Optional[str],
    include_sessions: bool,
) -> Dict[str, Any]:
    agents = config.setdefault("agents", {})
    defaults = agents.setdefault("defaults", {})
    memory_search = defaults.setdefault("memorySearch", {})

    memory_search["enabled"] = True
    memory_search["provider"] = provider
    if provider == "local":
        memory_search["model"] = model or "embeddinggemma-300m"
        memory_search["local"] = {"modelPath": model or DEFAULT_LOCAL_MODEL}
        memory_search["fallback"] = fallback or "none"
        memory_search.pop("remote", None)
    elif provider == "openai":
        memory_search["model"] = model or "text-embedding-3-small"
        remote = memory_search.setdefault("remote", {})
        if api_key:
            remote["apiKey"] = api_key
        if base_url:
            remote["baseUrl"] = base_url
        memory_search["fallback"] = fallback or "openai"
    elif provider == "gemini":
        memory_search["model"] = model or "gemini-embedding-001"
        remote = memory_search.setdefault("remote", {})
        if api_key:
            remote["apiKey"] = api_key
        if base_url:
            remote["baseUrl"] = base_url
        memory_search["fallback"] = fallback or "gemini"
    else:
        raise SystemExit(f"Unsupported provider: {provider}")

    extra_paths = memory_search.get("extraPaths", [])
    if not isinstance(extra_paths, list):
        extra_paths = []
    for item in REQUIRED_EXTRA_PATHS:
        if item not in extra_paths:
            extra_paths.append(item)
    memory_search["extraPaths"] = extra_paths

    sync = memory_search.setdefault("sync", {})
    sync["watch"] = True

    cache = memory_search.setdefault("cache", {})
    cache.setdefault("enabled", True)
    cache.setdefault("maxEntries", 50000)

    query = memory_search.setdefault("query", {})
    hybrid = query.setdefault("hybrid", {})
    hybrid.setdefault("enabled", True)
    hybrid.setdefault("vectorWeight", 0.7)
    hybrid.setdefault("textWeight", 0.3)
    hybrid.setdefault("candidateMultiplier", 4)

    store = memory_search.setdefault("store", {})
    store.setdefault("path", str(Path.home() / ".openclaw" / "memory" / "{agentId}.sqlite"))

    if include_sessions:
        memory_search["experimental"] = {"sessionMemory": True}
        memory_search["sources"] = ["memory", "sessions"]
        sync["sessions"] = {"deltaBytes": 100000, "deltaMessages": 50}
    return config


def apply_outputs(
    outputs: Dict[Path, str],
    recorder: MutationRecorder,
    overwrite_existing: bool = False,
) -> Dict[str, int]:
    counts = {"written": 0, "skipped": 0, "unchanged": 0}
    for path, content in outputs.items():
        result = recorder.write_text(path, content, overwrite=overwrite_existing)
        counts[result] += 1
    return counts


def sync_semantic_apply(layout: Layout, recorder: MutationRecorder, overwrite_existing: bool = True) -> Dict[str, int]:
    store = EventStore(layout)
    outputs = store.render_semantic_outputs(include_archive=False)
    return apply_outputs(outputs, recorder, overwrite_existing=overwrite_existing)


def cleanup_legacy_alias_path(layout: Layout, recorder: MutationRecorder) -> bool:
    legacy = layout.legacy_project_aliases_path
    if legacy.resolve() == layout.project_aliases_path.resolve():
        return False
    if not legacy.exists():
        return False
    recorder.backup(legacy)
    legacy.unlink()
    recorder.notes.append(f"Removed legacy indexed alias registry: {legacy}")
    return True


def latest_manifest_path(layout: Layout) -> Optional[Path]:
    if not layout.manifests_dir.exists():
        return None
    manifests = sorted(layout.manifests_dir.glob("*.json"))
    return manifests[-1] if manifests else None


def rollback_manifest(manifest_path: Path, dry_run: bool = False) -> Dict[str, Any]:
    manifest = read_json(manifest_path)
    if manifest.get("status") == "rolled_back":
        return {"rolled_back": False, "reason": "manifest already rolled back", "manifest_path": str(manifest_path)}

    deleted: List[str] = []
    restored: List[str] = []

    for path_str in reversed(manifest.get("created_files", [])):
        path = Path(path_str)
        if path.exists():
            if not dry_run:
                path.unlink()
            deleted.append(str(path))

    for item in manifest.get("backups", []):
        original = Path(item["path"])
        backup = Path(item["backup"])
        if backup.exists():
            if not dry_run:
                original.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup, original)
            restored.append(str(original))

    if not dry_run:
        manifest["status"] = "rolled_back"
        manifest["rolled_back_at"] = datetime.now().isoformat(timespec="seconds")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "rolled_back": True,
        "dry_run": dry_run,
        "manifest_path": str(manifest_path),
        "deleted_files": deleted,
        "restored_files": restored,
    }


def cmd_install(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    layout.ensure_dirs()
    migrated_at = datetime.now().isoformat(timespec="seconds")
    outputs = build_base_outputs(layout, migrated_at)

    config_change = None
    if layout.config_path.exists() and not args.no_config:
        payload = read_json(layout.config_path)
        updated = ensure_memory_search_config(
            config=payload,
            provider=args.provider,
            model=args.model,
            api_key=args.api_key,
            base_url=args.base_url,
            fallback=args.fallback,
            include_sessions=args.include_sessions,
        )
        config_change = updated

    if not args.apply:
        preview = {
            "command": "install",
            "dry_run": True,
            "would_write_files": [str(path) for path in sorted(outputs)],
            "would_update_config": bool(config_change),
            "config_path": str(layout.config_path),
            "provider": args.provider,
            "required_extra_paths": REQUIRED_EXTRA_PATHS,
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    recorder = MutationRecorder(layout, "install")
    counts = apply_outputs(outputs, recorder, overwrite_existing=False)
    if config_change and not args.no_config:
        recorder.write_json(layout.config_path, config_change, overwrite=True)
    removed_legacy_alias = cleanup_legacy_alias_path(layout, recorder)
    semantic_counts = sync_semantic_apply(layout, recorder, overwrite_existing=True)
    manifest_path = recorder.finalize(
        {
            "version": VERSION,
            "counts": counts,
            "semantic_counts": semantic_counts,
            "config_updated": bool(config_change and not args.no_config),
            "removed_legacy_alias": removed_legacy_alias,
        }
    )
    print(
        json.dumps(
            {
                "installed": True,
                "workspace": str(layout.workspace),
                "manifest_path": str(manifest_path),
                "counts": counts,
                "semantic_counts": semantic_counts,
                "config_updated": bool(config_change and not args.no_config),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_migrate(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    layout.ensure_dirs()
    outputs, report = build_migration_outputs(layout)

    if not args.apply:
        preview = {
            "command": "migrate",
            "dry_run": True,
            "workspace": str(layout.workspace),
            "report": report,
            "would_write_files": [str(path) for path in sorted(outputs)],
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    recorder = MutationRecorder(layout, "migrate")
    counts = apply_outputs(outputs, recorder, overwrite_existing=args.overwrite)
    alias_content = build_alias_registry(layout)
    recorder.write_text(layout.project_aliases_path, alias_content, overwrite=True)
    removed_legacy_alias = cleanup_legacy_alias_path(layout, recorder)
    migration_event = EventRecord(
        event_id=str(uuid.uuid4()),
        kind="system_improvement",
        scope="durable",
        summary=f"Migrated legacy OpenClaw memory into memory-fusion layout ({report['project_sections']} project sections)",
        created_at=datetime.now().isoformat(timespec="seconds"),
        details={
            "project_sections": report["project_sections"],
            "ops_sections": report["ops_sections"],
            "snapshot_files": report["snapshot_files"],
        },
        source="migrate",
        confidence="high",
        important=True,
    )
    EventStore(layout).record(migration_event, recorder)
    semantic_counts = sync_semantic_apply(layout, recorder, overwrite_existing=True)
    manifest_path = recorder.finalize(
        {
            "version": VERSION,
            "counts": counts,
            "semantic_counts": semantic_counts,
            "migration_report": report,
            "removed_legacy_alias": removed_legacy_alias,
        }
    )
    print(
        json.dumps(
            {
                "migrated": True,
                "manifest_path": str(manifest_path),
                "counts": counts,
                "semantic_counts": semantic_counts,
                "report": report,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    layout.ensure_dirs()
    recorder = MutationRecorder(layout, "capture")
    event = EventRecord(
        event_id=str(uuid.uuid4()),
        kind=args.kind,
        scope=args.scope,
        summary=args.summary,
        created_at=args.absolute_time or datetime.now().isoformat(timespec="seconds"),
        details=parse_details(args.details_json),
        project=args.project,
        source=args.source,
        confidence=args.confidence,
        important=args.important,
    )
    path = EventStore(layout).record(event, recorder)
    semantic_counts = sync_semantic_apply(layout, recorder, overwrite_existing=True)
    manifest_path = recorder.finalize(
        {"version": VERSION, "event_path": str(path), "semantic_counts": semantic_counts}
    )
    print(
        json.dumps(
            {
                "recorded": True,
                "event_id": event.event_id,
                "event_path": str(path),
                "manifest_path": str(manifest_path),
                "semantic_counts": semantic_counts,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_auto_capture(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    layout.ensure_dirs()
    events = collect_auto_capture_events(layout, days=args.days, include_ops=not args.no_ops)

    if not args.apply:
        preview = {
            "command": "auto-capture",
            "dry_run": True,
            "workspace": str(layout.workspace),
            "candidate_count": len(events),
            "sample": [event.to_dict() for event in events[:10]],
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    recorder = MutationRecorder(layout, "auto-capture")
    store = EventStore(layout)
    for event in events:
        store.record(event, recorder)
    semantic_counts = sync_semantic_apply(layout, recorder, overwrite_existing=True)
    manifest_path = recorder.finalize(
        {
            "version": VERSION,
            "captured_events": len(events),
            "semantic_counts": semantic_counts,
        }
    )
    print(
        json.dumps(
            {
                "captured": True,
                "captured_events": len(events),
                "manifest_path": str(manifest_path),
                "semantic_counts": semantic_counts,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    events = EventStore(layout).query(
        days=args.days,
        kind=args.kind,
        project=args.project,
        important_only=args.important_only,
        include_archive=args.include_archive,
        limit=args.limit,
    )
    payload = [event.to_dict() for event in events]
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_sync_aliases(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    layout.ensure_dirs()
    content = build_alias_registry(layout)
    would_remove_legacy = layout.legacy_project_aliases_path.exists() and layout.legacy_project_aliases_path.resolve() != layout.project_aliases_path.resolve()

    if not args.apply:
        preview = {
            "command": "sync-aliases",
            "dry_run": True,
            "workspace": str(layout.workspace),
            "alias_path": str(layout.project_aliases_path),
            "legacy_alias_path": str(layout.legacy_project_aliases_path),
            "would_remove_legacy_alias": would_remove_legacy,
            "preview": content,
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    recorder = MutationRecorder(layout, "sync-aliases")
    recorder.write_text(layout.project_aliases_path, content, overwrite=True)
    removed_legacy_alias = cleanup_legacy_alias_path(layout, recorder)
    manifest_path = recorder.finalize(
        {
            "version": VERSION,
            "alias_path": str(layout.project_aliases_path),
            "legacy_alias_path": str(layout.legacy_project_aliases_path),
            "removed_legacy_alias": removed_legacy_alias,
        }
    )
    print(
        json.dumps(
            {
                "synced": True,
                "alias_path": str(layout.project_aliases_path),
                "legacy_alias_path": str(layout.legacy_project_aliases_path),
                "removed_legacy_alias": removed_legacy_alias,
                "manifest_path": str(manifest_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_drift_check(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    layout.ensure_dirs()
    findings = build_drift_findings(layout, days=args.days)
    report_text = render_drift_report(findings)
    report_path = layout.semantic_dir / "DRIFT_REPORT.md"

    if not args.apply:
        preview = {
            "command": "drift-check",
            "dry_run": True,
            "workspace": str(layout.workspace),
            "findings": findings,
            "report_path": str(report_path),
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    recorder = MutationRecorder(layout, "drift-check")
    recorder.write_text(report_path, report_text, overwrite=True)
    repaired: List[str] = []
    if args.repair_placeholders:
        for item in findings:
            repairs = item.get("repairs", {})
            if not repairs:
                continue
            overview_path = Path(item["overview_path"])
            updated = replace_overview_snapshot(
                read_text(overview_path),
                status=repairs.get("status"),
                next_step=repairs.get("next_step"),
            )
            result = recorder.write_text(overview_path, updated, overwrite=True)
            if result == "written":
                repaired.append(str(overview_path))
    semantic_counts = sync_semantic_apply(layout, recorder, overwrite_existing=True)
    manifest_path = recorder.finalize(
        {
            "version": VERSION,
            "findings": len(findings),
            "repaired_files": repaired,
            "semantic_counts": semantic_counts,
        }
    )
    print(
        json.dumps(
            {
                "checked": True,
                "report_path": str(report_path),
                "findings": len(findings),
                "repaired_files": repaired,
                "manifest_path": str(manifest_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_sync_semantic(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    layout.ensure_dirs()
    outputs = EventStore(layout).render_semantic_outputs(include_archive=args.include_archive)
    if not args.apply:
        preview = {
            "command": "sync-semantic",
            "dry_run": True,
            "would_write_files": [str(path) for path in sorted(outputs)],
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    recorder = MutationRecorder(layout, "sync-semantic")
    counts = apply_outputs(outputs, recorder, overwrite_existing=True)
    manifest_path = recorder.finalize({"version": VERSION, "counts": counts})
    print(json.dumps({"synced": True, "counts": counts, "manifest_path": str(manifest_path)}, ensure_ascii=False, indent=2))
    return 0


def cmd_dream(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    layout.ensure_dirs()
    auto_events = collect_auto_capture_events(layout, days=args.days, include_ops=not args.no_ops)
    current_findings = build_drift_findings(layout, days=args.days)
    summary_path = layout.semantic_dir / "DREAM_SUMMARY.md"
    report_path = layout.semantic_dir / "DRIFT_REPORT.md"

    if not args.apply:
        preview = {
            "command": "dream",
            "dry_run": True,
            "workspace": str(layout.workspace),
            "auto_capture_candidates": len(auto_events),
            "drift_findings": len(current_findings),
            "sample_events": [event.to_dict() for event in auto_events[:8]],
            "sample_findings": current_findings[:8],
            "would_write_files": [str(summary_path), str(report_path)],
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    recorder = MutationRecorder(layout, "dream")
    store = EventStore(layout)
    for event in auto_events:
        store.record(event, recorder)

    findings = build_drift_findings(layout, days=args.days)
    recorder.write_text(report_path, render_drift_report(findings), overwrite=True)

    repaired: List[str] = []
    if args.repair_placeholders:
        for item in findings:
            repairs = item.get("repairs", {})
            if not repairs:
                continue
            overview_path = Path(item["overview_path"])
            updated = replace_overview_snapshot(
                read_text(overview_path),
                status=repairs.get("status"),
                next_step=repairs.get("next_step"),
            )
            result = recorder.write_text(overview_path, updated, overwrite=True)
            if result == "written":
                repaired.append(str(overview_path))

    recorder.write_text(summary_path, render_dream_summary(auto_events, findings, repaired), overwrite=True)
    semantic_counts = sync_semantic_apply(layout, recorder, overwrite_existing=True)
    manifest_path = recorder.finalize(
        {
            "version": VERSION,
            "auto_captured_events": len(auto_events),
            "drift_findings": len(findings),
            "repaired_files": repaired,
            "semantic_counts": semantic_counts,
        }
    )
    print(
        json.dumps(
            {
                "dreamed": True,
                "auto_captured_events": len(auto_events),
                "drift_findings": len(findings),
                "repaired_files": repaired,
                "summary_path": str(summary_path),
                "report_path": str(report_path),
                "manifest_path": str(manifest_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    latest_manifest = latest_manifest_path(layout)
    active_events = sum(1 for _ in EventStore(layout).iter_events(include_archive=False))
    archived_events = 0
    if layout.archive_dir.exists():
        for path in layout.archive_dir.glob("*.jsonl"):
            with path.open("r", encoding="utf-8") as handle:
                archived_events += sum(1 for line in handle if line.strip())
    payload = {
        "version": VERSION,
        "workspace": str(layout.workspace),
        "config_path": str(layout.config_path),
        "paths": {
            "projects_dir": layout.projects_dir.exists(),
            "ops_dir": layout.ops_dir.exists(),
            "events_dir": layout.events_dir.exists(),
            "semantic_dir": layout.semantic_dir.exists(),
            "manifests_dir": layout.manifests_dir.exists(),
        },
        "files": {
            "memory": layout.long_term_path.exists(),
            "projects": layout.projects_path.exists(),
            "projects_index": layout.projects_index_path.exists(),
            "project_aliases": layout.project_aliases_path.exists(),
            "legacy_project_aliases": layout.legacy_project_aliases_path.exists(),
            "ops_backlog": layout.ops_backlog_path.exists(),
            "ops_history": layout.ops_history_path.exists(),
        },
        "memory_search": inspect_memory_search(layout.config_path),
        "event_status": {
            "active_events": active_events,
            "archived_events": archived_events,
            "semantic_files": len(list(layout.semantic_dir.glob("*.md"))) if layout.semantic_dir.exists() else 0,
        },
        "fusion_features": {
            "auto_capture": True,
            "dream": True,
            "drift_check": True,
        },
        "latest_manifest": str(latest_manifest) if latest_manifest else None,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_upgrade_check(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    memory_search = inspect_memory_search(layout.config_path)
    warnings: List[str] = []
    compatible = True

    if not shutil.which("openclaw"):
        compatible = False
        warnings.append("`openclaw` executable is not available on PATH.")
    if not layout.config_path.exists():
        compatible = False
        warnings.append("OpenClaw config file is missing.")
    if memory_search.get("config_exists") and memory_search.get("enabled"):
        extra_paths = set(memory_search.get("extraPaths", []))
        missing = [path for path in REQUIRED_EXTRA_PATHS if path not in extra_paths]
        if missing:
            warnings.append(f"memorySearch is enabled but missing extraPaths: {missing}")
    else:
        warnings.append("memorySearch is not enabled yet.")

    payload = {
        "compatible": compatible,
        "version": VERSION,
        "workspace": str(layout.workspace),
        "config_path": str(layout.config_path),
        "memory_search": memory_search,
        "warnings": warnings,
        "checks": {
            "openclaw_on_path": bool(shutil.which("openclaw")),
            "config_exists": layout.config_path.exists(),
            "projects_index_exists": layout.projects_index_path.exists(),
            "ops_dir_exists": layout.ops_dir.exists(),
            "semantic_dir_exists": layout.semantic_dir.exists(),
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_rollback(args: argparse.Namespace) -> int:
    layout = Layout(resolve_workspace(args.workspace), resolve_config_path(args.config))
    layout.ensure_dirs()
    manifest_path = None
    if args.manifest:
        manifest_path = Path(args.manifest).expanduser()
    elif args.latest:
        manifest_path = latest_manifest_path(layout)
    if not manifest_path:
        raise SystemExit("No manifest found for rollback.")
    payload = rollback_manifest(manifest_path, dry_run=args.dry_run)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified memory manager for OpenClaw.")
    parser.add_argument("--workspace", help="Override OpenClaw workspace path.")
    parser.add_argument("--config", help="Override OpenClaw config path.")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--workspace", help="Override OpenClaw workspace path.")
    common.add_argument("--config", help="Override OpenClaw config path.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install = subparsers.add_parser("install", parents=[common], help="Prepare workspace structure and memorySearch config.")
    install.add_argument("--apply", action="store_true", help="Write files and config instead of previewing.")
    install.add_argument("--provider", choices=["local", "openai", "gemini"], default="local")
    install.add_argument("--model")
    install.add_argument("--api-key")
    install.add_argument("--base-url")
    install.add_argument("--fallback")
    install.add_argument("--include-sessions", action="store_true")
    install.add_argument("--no-config", action="store_true", help="Do not touch openclaw.json.")
    install.set_defaults(func=cmd_install)

    migrate = subparsers.add_parser("migrate", parents=[common], help="Migrate legacy project memory into fusion layout.")
    migrate.add_argument("--apply", action="store_true", help="Write migrated files instead of previewing.")
    migrate.add_argument("--overwrite", action="store_true", help="Overwrite existing generated files.")
    migrate.set_defaults(func=cmd_migrate)

    capture = subparsers.add_parser("capture", parents=[common], help="Record a structured memory event.")
    capture.add_argument("--kind", required=True)
    capture.add_argument("--scope", choices=["ephemeral", "working", "project", "durable"], required=True)
    capture.add_argument("--summary", required=True)
    capture.add_argument("--project")
    capture.add_argument("--details-json")
    capture.add_argument("--absolute-time")
    capture.add_argument("--source", default="openclaw-memory-fusion")
    capture.add_argument("--confidence", choices=["low", "medium", "high"], default="medium")
    capture.add_argument("--important", action="store_true")
    capture.set_defaults(func=cmd_capture)

    auto_capture = subparsers.add_parser("auto-capture", parents=[common], help="Extract structured events from recent working memory.")
    auto_capture.add_argument("--days", type=int, default=7)
    auto_capture.add_argument("--apply", action="store_true", help="Write captured events instead of previewing.")
    auto_capture.add_argument("--no-ops", action="store_true", help="Skip ops/improvements sources.")
    auto_capture.set_defaults(func=cmd_auto_capture)

    query = subparsers.add_parser("query", parents=[common], help="Query structured events.")
    query.add_argument("--days", type=int, default=30)
    query.add_argument("--kind")
    query.add_argument("--project")
    query.add_argument("--limit", type=int, default=20)
    query.add_argument("--important-only", action="store_true")
    query.add_argument("--include-archive", action="store_true")
    query.set_defaults(func=cmd_query)

    sync = subparsers.add_parser("sync-semantic", parents=[common], help="Regenerate semantic digests from structured events.")
    sync.add_argument("--apply", action="store_true", help="Write digest files instead of previewing.")
    sync.add_argument("--include-archive", action="store_true")
    sync.set_defaults(func=cmd_sync_semantic)

    aliases = subparsers.add_parser("sync-aliases", parents=[common], help="Generate or refresh the editable project alias registry.")
    aliases.add_argument("--apply", action="store_true", help="Write the alias registry instead of previewing.")
    aliases.set_defaults(func=cmd_sync_aliases)

    drift = subparsers.add_parser("drift-check", parents=[common], help="Detect and optionally repair memory drift in project overviews.")
    drift.add_argument("--days", type=int, default=30)
    drift.add_argument("--apply", action="store_true", help="Write the drift report instead of previewing.")
    drift.add_argument("--repair-placeholders", action="store_true", help="Fill placeholder status/next-step fields when safe.")
    drift.set_defaults(func=cmd_drift_check)

    dream = subparsers.add_parser("dream", parents=[common], help="Run a reflective memory pass with auto-capture and drift analysis.")
    dream.add_argument("--days", type=int, default=7)
    dream.add_argument("--apply", action="store_true", help="Write captured events, reports, and repairs instead of previewing.")
    dream.add_argument("--repair-placeholders", action="store_true", help="Fill placeholder status/next-step fields when safe.")
    dream.add_argument("--no-ops", action="store_true", help="Skip ops/improvements sources during auto-capture.")
    dream.set_defaults(func=cmd_dream)

    doctor = subparsers.add_parser("doctor", parents=[common], help="Inspect the current memory-fusion setup.")
    doctor.set_defaults(func=cmd_doctor)

    upgrade = subparsers.add_parser("upgrade-check", parents=[common], help="Check whether the setup is safe across OpenClaw upgrades.")
    upgrade.set_defaults(func=cmd_upgrade_check)

    rollback = subparsers.add_parser("rollback", parents=[common], help="Rollback the latest or a specific manifest.")
    rollback.add_argument("--manifest", help="Explicit manifest path.")
    rollback.add_argument("--latest", action="store_true", help="Rollback the latest manifest.")
    rollback.add_argument("--dry-run", action="store_true")
    rollback.set_defaults(func=cmd_rollback)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
