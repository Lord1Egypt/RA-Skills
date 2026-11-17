#!/usr/bin/env python3
"""用结构化扫描和语义抽样评估 Obsidian/个人知识库健康度。"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "0.5.0"
SEMANTIC_SCORE_SCHEMA_VERSION = "semantic-scores-v0.2"
DEFAULT_TOOL_NAME = "workbuddy"

SCHEMA_FILES = ["AGENTS.md", "RULES.md"]
OPTIONAL_NAVIGATION_FILES = ["index.md", "核心文件索引.md"]
MAINTENANCE_FILES = ["log.md"]
ROOT_SIGNAL_FILES = SCHEMA_FILES + OPTIONAL_NAVIGATION_FILES + MAINTENANCE_FILES

DIMENSION_WEIGHTS = {
    "llm_wiki_architecture_fit": 20,
    "source_traceability": 20,
    "schema_governance_quality": 15,
    "knowledge_sedimentation_effectiveness": 25,
    "retrieval_answerability": 10,
    "maintenance_evolution": 10,
}

DIMENSION_LABELS = {
    "llm_wiki_architecture_fit": "LLM Wiki 架构符合度",
    "source_traceability": "来源可追溯性",
    "schema_governance_quality": "Schema 治理质量",
    "knowledge_sedimentation_effectiveness": "知识沉淀有效性",
    "retrieval_answerability": "检索与回答可用性",
    "maintenance_evolution": "维护与演化健康度",
}

DIMENSION_EVALUATES = {
    "llm_wiki_architecture_fit": "raw/wiki/schema 三层、ingest/query/lint 操作、关系维护和可演化组织方式是否成形。",
    "source_traceability": "wiki 结论能否回到 raw/source/core note，证据链是否足够细、可恢复、可核验。",
    "schema_governance_quality": "AGENTS/RULES 等 schema 是否清晰、一致、完整、可验证、可追溯、可维护。",
    "knowledge_sedimentation_effectiveness": "最新 wiki 沉淀是否忠实、完整、连贯、可复用，并能把原始资料压缩为长期知识。",
    "retrieval_answerability": "未来查询能否快速定位上下文，并产出相关、忠实、可引用的答案。",
    "maintenance_evolution": "日志、lint、过期检测、冲突处理和修复流程能否支撑知识库持续演化。",
}

SEMANTIC_BLEND_WEIGHTS = {
    "llm_wiki_architecture_fit": {"structural": 0.45, "semantic": 0.55},
    "source_traceability": {"structural": 0.45, "semantic": 0.55},
    "schema_governance_quality": {"structural": 0.35, "semantic": 0.65},
    "knowledge_sedimentation_effectiveness": {"structural": 0.25, "semantic": 0.75},
    "retrieval_answerability": {"structural": 0.40, "semantic": 0.60},
    "maintenance_evolution": {"structural": 0.45, "semantic": 0.55},
}

SEMANTIC_CRITERIA = {
    "llm_wiki_architecture_fit": [
        "raw_wiki_schema_layering",
        "ingest_query_lint_operations",
        "agent_operationalization",
        "modularity_and_adaptability",
    ],
    "source_traceability": [
        "provenance_coverage",
        "claim_source_alignment",
        "citation_granularity",
        "source_recoverability",
    ],
    "schema_governance_quality": [
        "completeness",
        "consistency",
        "unambiguity",
        "verifiability",
        "traceability",
        "maintainability",
    ],
    "knowledge_sedimentation_effectiveness": [
        "groundedness",
        "completeness",
        "relevance_actionability",
        "coherence_readability",
        "source_integration",
        "freshness_conflict_handling",
    ],
    "retrieval_answerability": [
        "navigation_findability",
        "question_context_precision",
        "answer_faithfulness",
        "answer_relevance",
    ],
    "maintenance_evolution": [
        "logging_freshness",
        "staleness_detection",
        "conflict_handling",
        "repair_workflow",
    ],
}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
RAW_LINK_HINT_RE = re.compile(r"\[\[(?:raw/|[^|\]]*\.core(?:\||\]\]))")
SOURCE_CITATION_HINT_RE = re.compile(
    r"\[\[(?:raw/|[^|\]]*\.core(?:\||\]\]))"
    r"|\[[^\]]+\]\((?:\.\./)?raw/[^)]+\)"
    r"|(?:source|sources|citation|provenance|来源|出处|引用)\s*[:：]",
    re.IGNORECASE,
)
SOURCE_SCOPE_RE = re.compile(r"(?im)^source_scope\s*:\s*(.*)$")
SOURCE_MANIFEST_NAME_RE = re.compile(
    r"(?:source[-_ ]?manifest|provenance|source[-_ ]?(?:index|map|catalog|registry)|(?:download|image|asset|file)[-_ ]?manifest|来源(?:清单|索引)|源(?:清单|索引))",
    re.IGNORECASE,
)
SOURCE_MANIFEST_SUFFIXES = {".json", ".jsonl", ".yaml", ".yml", ".csv", ".tsv", ".md"}
EXTERNAL_INDEX_SUFFIXES = {".sqlite", ".sqlite3", ".db", ".duckdb", ".parquet"}
EXTERNAL_INDEX_HINT_RE = re.compile(r"(?:external[-_ ]?index|vector|embedding|semantic|metadata|index)", re.IGNORECASE)
DATE_HINT_RE = re.compile(r"\b(20\d{2})[-/.](0?[1-9]|1[0-2])[-/.](0?[1-9]|[12]\d|3[01])\b")
GENERATED_CORE_BLOCK_RE = re.compile(
    r"<!--\s*CORE_[A-Z0-9_]+:START\s*-->.*?<!--\s*CORE_[A-Z0-9_]+:END\s*-->",
    re.DOTALL,
)
OPERATION_HINT_RE = re.compile(
    r"ingest|query|lint|validate|refresh|reconcile|日志|查询|沉淀|维护|验证|取信",
    re.IGNORECASE,
)
RELATION_PROTOCOL_RE = re.compile(
    r"CORE_RELATIONSHIPS_V1|obsidian-core-notes|Core Notes|关系维护|关系块|backlink|graph",
    re.IGNORECASE,
)
TOOL_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
CRITERIA_SCORE_TOLERANCE = 25.0
STRUCTURAL_SEMANTIC_WARNING_THRESHOLD = 35.0


@dataclass
class MarkdownFile:
    path: Path
    text: str
    modified: datetime


class SemanticScoreError(ValueError):
    """Raised when LLM semantic score input is incomplete or invalid."""


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def ratio_score(numerator: int | float, denominator: int | float, empty_score: float = 0.0) -> float:
    if denominator <= 0:
        return empty_score
    return clamp((numerator / denominator) * 100.0)


def weighted_average(parts: list[tuple[float, float]]) -> float:
    total_weight = sum(weight for _, weight in parts)
    if total_weight == 0:
        return 0.0
    return clamp(sum(score * weight for score, weight in parts) / total_weight)


def read_text(path: Path, limit_chars: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if limit_chars is not None:
        return text[:limit_chars]
    return text


def normalize_tool_name(tool_name: str | None) -> str:
    clean = (tool_name or DEFAULT_TOOL_NAME).strip().lstrip(".")
    if not TOOL_NAME_RE.match(clean):
        raise ValueError("tool_name must contain only letters, numbers, underscore, or hyphen.")
    return clean


def default_artifact_paths(
    root: str | Path,
    output_format: str,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> dict[str, Path]:
    root_path = Path(root).expanduser().resolve()
    if artifact_dir is None:
        artifacts = root_path / f".{normalize_tool_name(tool_name)}" / "llm-wiki-health"
    else:
        artifacts = Path(artifact_dir).expanduser().resolve()
    if output_format == "json":
        report_name = "llm-wiki-health-report.json"
    elif output_format == "markdown":
        report_name = "llm-wiki-health-report.md"
    else:
        raise ValueError(f"不支持的输出格式：{output_format}")
    return {
        "artifact_dir": artifacts,
        "report": artifacts / report_name,
        "semantic_template": artifacts / "semantic_scores.json",
    }


def path_is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def artifact_skip_paths(
    root: str | Path,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> list[Path]:
    root_path = Path(root).expanduser().resolve()
    paths = [default_artifact_paths(root_path, "markdown", tool_name=tool_name)["artifact_dir"]]
    if artifact_dir is not None:
        paths.append(Path(artifact_dir).expanduser().resolve())
    return [path for path in paths if path == root_path or path_is_relative_to(path, root_path)]


def iter_files(
    root: Path,
    subdir: str | None = None,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> list[Path]:
    root_path = root.expanduser().resolve()
    base = root_path / subdir if subdir else root_path
    if not base.exists():
        return []
    skipped_dirs = {
        ".obsidian",
        ".workbuddy",
        f".{normalize_tool_name(tool_name)}",
        ".git",
        ".trash",
        "__pycache__",
    }
    skipped_paths = artifact_skip_paths(root_path, tool_name=tool_name, artifact_dir=artifact_dir)
    files: list[Path] = []
    for path in base.rglob("*"):
        rel_parts = path.relative_to(root_path).parts if path_is_relative_to(path, root_path) else path.parts
        if any(part in skipped_dirs for part in rel_parts):
            continue
        if any(path == skipped or path_is_relative_to(path, skipped) for skipped in skipped_paths):
            continue
        if path.is_file():
            files.append(path)
    return files


def load_markdown_files(paths: list[Path]) -> list[MarkdownFile]:
    files = []
    for path in paths:
        if path.suffix.lower() != ".md" or not path.exists():
            continue
        files.append(
            MarkdownFile(
                path=path,
                text=read_text(path),
                modified=datetime.fromtimestamp(path.stat().st_mtime),
            )
        )
    return files


def relative(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def has_frontmatter(text: str) -> bool:
    return bool(FRONTMATTER_RE.search(text))


def frontmatter_text(text: str) -> str:
    match = FRONTMATTER_RE.search(text)
    return match.group(0) if match else ""


def has_frontmatter_source_scope(text: str) -> bool:
    frontmatter = frontmatter_text(text)
    match = SOURCE_SCOPE_RE.search(frontmatter)
    if not match:
        return False
    value = match.group(1).strip().strip("'\"")
    if value and value.lower() not in {"null", "none", "[]", "{}"}:
        return True
    remainder = frontmatter[match.end() :]
    return bool(re.search(r"(?m)^\s+-\s+\S+", remainder)) or "raw/" in remainder[:500]


def extract_wikilinks(text: str) -> list[str]:
    links = []
    for match in WIKILINK_RE.findall(text):
        target = match.split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            links.append(target)
    return links


def strip_generated_blocks(text: str) -> str:
    return GENERATED_CORE_BLOCK_RE.sub("", text)


def is_source_manifest_file(path: Path) -> bool:
    if path.name.endswith(".core.md"):
        return False
    return path.suffix.lower() in SOURCE_MANIFEST_SUFFIXES and bool(SOURCE_MANIFEST_NAME_RE.search(path.stem))


def is_external_index_file(root: Path, path: Path) -> bool:
    if path.suffix.lower() not in EXTERNAL_INDEX_SUFFIXES:
        return False
    rel = relative(root, path).replace("\\", "/")
    return bool(EXTERNAL_INDEX_HINT_RE.search(rel))


def collect_external_index_files(
    root: Path,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> list[Path]:
    skipped_dirs = {
        ".obsidian",
        ".workbuddy",
        f".{normalize_tool_name(tool_name)}",
        ".git",
        ".trash",
        "__pycache__",
    }
    skipped_paths = artifact_skip_paths(root, tool_name=tool_name, artifact_dir=artifact_dir)
    files: list[Path] = []
    try:
        children = list(root.iterdir())
    except OSError:
        return files
    for child in children:
        if child.name in skipped_dirs:
            continue
        if any(child == skipped or path_is_relative_to(child, skipped) for skipped in skipped_paths):
            continue
        if child.is_file():
            if is_external_index_file(root, child):
                files.append(child)
            continue
        if child.is_dir() and EXTERNAL_INDEX_HINT_RE.search(child.name):
            for path in child.rglob("*"):
                if path.is_file() and path.suffix.lower() in EXTERNAL_INDEX_SUFFIXES:
                    files.append(path)
    return files


def add_link_index_key(index: dict[str, list[Path]], key: str, path: Path) -> None:
    normalized = key.replace("\\", "/").strip("/")
    if not normalized:
        return
    paths = index.setdefault(normalized, [])
    if path not in paths:
        paths.append(path)


def build_link_index(root: Path, md_files: list[MarkdownFile]) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for item in md_files:
        rel = relative(root, item.path)
        stem_rel = rel[:-3] if rel.endswith(".md") else rel
        add_link_index_key(index, rel, item.path)
        add_link_index_key(index, stem_rel, item.path)
        add_link_index_key(index, item.path.stem, item.path)
        parts = stem_rel.split("/")
        for start in range(1, len(parts)):
            add_link_index_key(index, "/".join(parts[start:]), item.path)
    return index


def wikilink_candidate_keys(target: str, root: Path | None = None, source_path: Path | None = None) -> list[str]:
    normalized = target.split("|", 1)[0].split("#", 1)[0].replace("\\", "/").strip("/")
    if not normalized:
        return []
    no_ext = normalized[:-3] if normalized.endswith(".md") else normalized
    candidates = [no_ext, normalized]
    if normalized.endswith(".md"):
        candidates.append(normalized[:-3])
    else:
        candidates.append(f"{normalized}.md")
    if normalized.endswith(".core"):
        candidates.append(f"{normalized}.md")
    if root is not None and source_path is not None and "/" in no_ext and not no_ext.startswith(("raw/", "wiki/")):
        source_dir = relative(root, source_path.parent)
        if source_dir != ".":
            candidates.insert(0, f"{source_dir}/{no_ext}")
            candidates.insert(1, f"{source_dir}/{normalized}")

    deduped: list[str] = []
    for candidate in candidates:
        cleaned = candidate.replace("\\", "/").strip("/")
        if cleaned and cleaned not in deduped:
            deduped.append(cleaned)
    return deduped


def resolve_wikilink(
    target: str,
    link_index: dict[str, list[Path]],
    root: Path | None = None,
    source_path: Path | None = None,
) -> dict[str, Any]:
    for candidate in wikilink_candidate_keys(target, root=root, source_path=source_path):
        matches = link_index.get(candidate, [])
        if len(matches) == 1:
            return {"status": "resolved", "path": matches[0], "candidate": candidate}
        if len(matches) > 1:
            return {"status": "ambiguous", "paths": matches, "candidate": candidate}
    return {"status": "dangling", "candidate": target}


def link_exists(target: str, link_index: dict[str, list[Path]]) -> bool:
    return resolve_wikilink(target, link_index)["status"] == "resolved"


def collect_stats(
    root: Path,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(root).expanduser().resolve()
    raw_files = iter_files(root, "raw", tool_name=tool_name, artifact_dir=artifact_dir)
    wiki_files = iter_files(root, "wiki", tool_name=tool_name, artifact_dir=artifact_dir)
    root_signal_paths = [root / name for name in ROOT_SIGNAL_FILES if (root / name).is_file()]
    root_note_paths = [
        path
        for path in root.glob("*.md")
        if path.is_file() and path.name not in ROOT_SIGNAL_FILES
    ]
    all_md = load_markdown_files(root_signal_paths + root_note_paths + raw_files + wiki_files)
    raw_md = [item for item in all_md if "raw" in item.path.relative_to(root).parts]
    wiki_md = [item for item in all_md if "wiki" in item.path.relative_to(root).parts]
    root_notes_md = [item for item in all_md if item.path.parent == root and item.path.name not in ROOT_SIGNAL_FILES]
    core_md = [item for item in raw_md if item.path.name.endswith(".core.md")]
    non_core_raw_files = [path for path in raw_files if not path.name.endswith(".core.md")]
    non_md_raw_sources = [path for path in non_core_raw_files if path.suffix.lower() != ".md"]
    source_manifest_candidates = raw_files + wiki_files + root_signal_paths + root_note_paths
    source_manifest_files = [path for path in source_manifest_candidates if is_source_manifest_file(path)]
    external_index_files = collect_external_index_files(root, tool_name=tool_name, artifact_dir=artifact_dir)
    link_index = build_link_index(root, all_md)

    wiki_pages_with_raw_links = 0
    wiki_pages_with_source_citations = 0
    wiki_pages_with_source_scope = 0
    wiki_pages_with_frontmatter = 0
    total_wiki_links = 0
    dangling_links = 0
    ambiguous_links = 0
    inbound_counts: dict[Path, int] = {item.path: 0 for item in all_md}
    wiki_body_text = {item.path: strip_generated_blocks(item.text) for item in wiki_md}

    for item in wiki_md:
        body_text = wiki_body_text[item.path]
        if has_frontmatter(item.text):
            wiki_pages_with_frontmatter += 1
        if has_frontmatter_source_scope(item.text):
            wiki_pages_with_source_scope += 1
        if RAW_LINK_HINT_RE.search(body_text):
            wiki_pages_with_raw_links += 1
        if SOURCE_CITATION_HINT_RE.search(body_text):
            wiki_pages_with_source_citations += 1
        links = extract_wikilinks(body_text)
        total_wiki_links += len(links)
        for target in links:
            resolution = resolve_wikilink(target, link_index, root=root, source_path=item.path)
            if resolution["status"] == "dangling":
                dangling_links += 1
                continue
            if resolution["status"] == "ambiguous":
                ambiguous_links += 1
                continue
            linked_path = resolution.get("path")
            if linked_path in inbound_counts:
                inbound_counts[linked_path] += 1

    latest_wiki_pages = sorted(wiki_md, key=lambda item: item.modified, reverse=True)[:10]
    latest_source_backed = sum(1 for item in latest_wiki_pages if RAW_LINK_HINT_RE.search(wiki_body_text[item.path]))
    root_markdown_samples = [
        relative(root, item.path) for item in sorted(root_notes_md, key=lambda item: item.modified, reverse=True)[:10]
    ]

    orphan_wiki_pages = 0
    for item in wiki_md:
        links = extract_wikilinks(wiki_body_text[item.path])
        if not links and inbound_counts.get(item.path, 0) == 0:
            orphan_wiki_pages += 1

    now = datetime.now()
    stale_wiki_pages = sum((now - item.modified).days > 180 for item in wiki_md)
    core_auto_summary_count = sum("CORE_AUTO_SUMMARY_V1" in item.text for item in core_md)
    relationship_marker_count = sum("CORE_RELATIONSHIPS_V1" in item.text for item in all_md)
    role_tagged_wiki_pages = sum("doc_role:" in item.text for item in wiki_md)
    substantive_wiki_pages = sum(len(item.text.strip()) >= 800 for item in wiki_md)
    multi_source_wiki_pages = sum(
        len(re.findall(r"\[\[(?:raw/|[^|\]]*\.core(?:\||\]\]))", wiki_body_text[item.path])) >= 2
        for item in wiki_md
    )

    root_text = {name: read_text(root / name, 400_000) for name in ROOT_SIGNAL_FILES}
    machine_index_text = root_text.get("核心文件索引.md", "")
    machine_index_source_link_count = len(RAW_LINK_HINT_RE.findall(machine_index_text))
    schema_text = "\n".join(root_text.get(name, "") for name in SCHEMA_FILES)
    all_file_count = len(raw_files) + len(wiki_files) + len(root_signal_paths) + len(root_note_paths)

    return {
        "all_file_count": all_file_count,
        "raw_file_count": len(raw_files),
        "wiki_file_count": len(wiki_files),
        "raw_markdown_count": len(raw_md),
        "wiki_markdown_count": len(wiki_md),
        "root_markdown_samples": root_markdown_samples,
        "core_markdown_count": len(core_md),
        "non_core_raw_file_count": len(non_core_raw_files),
        "non_md_raw_source_count": len(non_md_raw_sources),
        "wiki_pages_with_frontmatter": wiki_pages_with_frontmatter,
        "wiki_pages_with_raw_links": wiki_pages_with_raw_links,
        "wiki_pages_with_source_citations": wiki_pages_with_source_citations,
        "wiki_pages_with_source_scope": wiki_pages_with_source_scope,
        "source_manifest_file_count": len(source_manifest_files),
        "source_manifest_files": [relative(root, path) for path in source_manifest_files[:20]],
        "machine_index_source_link_count": machine_index_source_link_count,
        "external_index_file_count": len(external_index_files),
        "external_index_files": [relative(root, path) for path in external_index_files[:20]],
        "latest_wiki_pages": [relative(root, item.path) for item in latest_wiki_pages],
        "latest_source_backed_count": latest_source_backed,
        "total_wiki_links": total_wiki_links,
        "dangling_wiki_links": dangling_links,
        "ambiguous_wiki_links": ambiguous_links,
        "orphan_wiki_pages": orphan_wiki_pages,
        "stale_wiki_pages": stale_wiki_pages,
        "core_auto_summary_count": core_auto_summary_count,
        "relationship_marker_count": relationship_marker_count,
        "role_tagged_wiki_pages": role_tagged_wiki_pages,
        "substantive_wiki_pages": substantive_wiki_pages,
        "multi_source_wiki_pages": multi_source_wiki_pages,
        "root_text": root_text,
        "schema_text": schema_text,
    }


def assess_architecture(root: Path, stats: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, blocking: bool, evidence: str, note: str = "") -> None:
        checks.append(
            {
                "id": check_id,
                "passed": passed,
                "blocking": blocking,
                "evidence": evidence,
                "note": note,
            }
        )

    raw_dir = root / "raw"
    wiki_dir = root / "wiki"
    schema_files_present = all((root / name).is_file() for name in SCHEMA_FILES)
    schema_text = stats["schema_text"]
    declares_layers = "raw/" in schema_text and "wiki/" in schema_text
    declares_operations = bool(OPERATION_HINT_RE.search(schema_text))
    relationship_protocol = bool(RELATION_PROTOCOL_RE.search(schema_text))
    log_nonempty = (root / "log.md").is_file() and (root / "log.md").stat().st_size > 0
    index_nonempty = (root / "index.md").is_file() and (root / "index.md").stat().st_size > 0
    machine_index_nonempty = (root / "核心文件索引.md").is_file() and (root / "核心文件索引.md").stat().st_size > 0

    add("raw_layer_exists", raw_dir.is_dir(), False, str(raw_dir), "卡帕西式核心分层信号。")
    add("wiki_layer_exists", wiki_dir.is_dir(), False, str(wiki_dir), "卡帕西式核心分层信号。")
    add("schema_files_present", schema_files_present, False, "AGENTS.md, RULES.md", "Schema 信号。")
    add(
        "schema_declares_raw_wiki_layers",
        declares_layers,
        False,
        "AGENTS.md/RULES.md",
        "显式分层规则；缺失会降低分数，但不停止评分。",
    )
    add(
        "schema_declares_operations",
        declares_operations,
        False,
        "AGENTS.md/RULES.md",
        "检查是否声明 ingest/query/lint/validate/logging 等操作语言。",
    )
    add(
        "relationship_protocol_evidence",
        relationship_protocol,
        False,
        "AGENTS.md/RULES.md",
        "只采纳确定性证据；LLM 后续只评价清晰度，不决定是否通过。",
    )
    add("maintenance_log_present", log_nonempty, False, "log.md", "维护证据。")
    add("human_entry_index_present", index_nonempty, False, "index.md", "可选导航信号。")
    add("machine_index_present", machine_index_nonempty, False, "核心文件索引.md", "可选机器索引信号。")

    karpathy_core_present = raw_dir.is_dir() and wiki_dir.is_dir() and schema_files_present and declares_layers
    return {
        "karpathy_core_present": karpathy_core_present,
        "blocking_issues": [],
        "checks": checks,
    }


def dimension_base(name: str, structural_score: float, metrics: dict[str, Any], evidence: list[str]) -> dict[str, Any]:
    return {
        "label": DIMENSION_LABELS[name],
        "weight": DIMENSION_WEIGHTS[name],
        "evaluates": DIMENSION_EVALUATES[name],
        "structural_score": round(clamp(structural_score), 2),
        "metrics": metrics,
        "evidence": evidence,
    }


def score_llm_wiki_architecture_fit(assessment: dict[str, Any], stats: dict[str, Any]) -> dict[str, Any]:
    checks = {check["id"]: check["passed"] for check in assessment["checks"]}
    optional_navigation_score = weighted_average(
        [
            (100.0 if checks.get("human_entry_index_present") else 0.0, 1),
            (100.0 if checks.get("machine_index_present") else 0.0, 1),
        ]
    )
    parts = [
        (100.0 if checks.get("raw_layer_exists") else 0.0, 15),
        (100.0 if checks.get("wiki_layer_exists") else 0.0, 15),
        (100.0 if checks.get("schema_files_present") else 0.0, 15),
        (100.0 if checks.get("schema_declares_raw_wiki_layers") else 0.0, 15),
        (100.0 if checks.get("schema_declares_operations") else 0.0, 15),
        (100.0 if checks.get("relationship_protocol_evidence") else 0.0, 10),
        (100.0 if checks.get("maintenance_log_present") else 0.0, 10),
        (optional_navigation_score, 5),
    ]
    return dimension_base(
        "llm_wiki_architecture_fit",
        weighted_average(parts),
        {
            "karpathy_core_present": assessment["karpathy_core_present"],
            "raw_file_count": stats["raw_file_count"],
            "wiki_file_count": stats["wiki_file_count"],
            "optional_navigation_files": OPTIONAL_NAVIGATION_FILES,
        },
        ["raw/", "wiki/", "AGENTS.md", "RULES.md", "log.md", "index.md", "核心文件索引.md"],
    )


def score_source_traceability(stats: dict[str, Any]) -> dict[str, Any]:
    sidecar_score = ratio_score(
        stats["core_markdown_count"],
        stats["non_md_raw_source_count"],
        100.0 if stats["non_core_raw_file_count"] == 0 and stats["raw_file_count"] > 0 else 0.0,
    )
    wiki_raw_link_score = ratio_score(
        stats["wiki_pages_with_raw_links"],
        stats["wiki_markdown_count"],
        0.0,
    )
    source_citation_score = ratio_score(
        stats.get("wiki_pages_with_source_citations", stats["wiki_pages_with_raw_links"]),
        stats["wiki_markdown_count"],
        0.0,
    )
    frontmatter_source_scope_score = ratio_score(
        stats.get("wiki_pages_with_source_scope", 0),
        stats["wiki_markdown_count"],
        0.0,
    )
    manifest_score = 100.0 if stats.get("source_manifest_file_count", 0) > 0 else 0.0
    machine_index_score = 100.0 if stats.get("machine_index_source_link_count", 0) > 0 else 0.0
    external_index_score = 100.0 if stats.get("external_index_file_count", 0) > 0 else 0.0
    source_recoverability_score = weighted_average(
        [
            (sidecar_score, 30),
            (manifest_score, 15),
            (frontmatter_source_scope_score, 20),
            (source_citation_score, 20),
            (machine_index_score, 10),
            (external_index_score, 5),
        ]
    )
    core_summary_score = ratio_score(
        stats["core_auto_summary_count"],
        stats["core_markdown_count"],
        0.0,
    )
    parts = [
        (source_recoverability_score, 70),
        (core_summary_score, 15),
        (100.0 if stats["raw_file_count"] > 0 else 0.0, 15),
    ]
    return dimension_base(
        "source_traceability",
        weighted_average(parts),
        {
            "raw_file_count": stats["raw_file_count"],
            "non_md_raw_source_count": stats["non_md_raw_source_count"],
            "core_markdown_count": stats["core_markdown_count"],
            "core_auto_summary_count": stats["core_auto_summary_count"],
            "sidecar_score": round(sidecar_score, 2),
            "source_recoverability_score": round(source_recoverability_score, 2),
            "source_recoverability_components": {
                "sidecar_score": round(sidecar_score, 2),
                "manifest_score": round(manifest_score, 2),
                "frontmatter_source_scope_score": round(frontmatter_source_scope_score, 2),
                "source_citation_score": round(source_citation_score, 2),
                "machine_index_score": round(machine_index_score, 2),
                "external_index_score": round(external_index_score, 2),
            },
            "wiki_pages_with_raw_links": stats["wiki_pages_with_raw_links"],
            "wiki_pages_with_source_citations": stats.get(
                "wiki_pages_with_source_citations",
                stats["wiki_pages_with_raw_links"],
            ),
            "wiki_pages_with_source_scope": stats.get("wiki_pages_with_source_scope", 0),
            "source_manifest_file_count": stats.get("source_manifest_file_count", 0),
            "source_manifest_files": stats.get("source_manifest_files", []),
            "machine_index_source_link_count": stats.get("machine_index_source_link_count", 0),
            "external_index_file_count": stats.get("external_index_file_count", 0),
            "external_index_files": stats.get("external_index_files", []),
            "wiki_markdown_count": stats["wiki_markdown_count"],
        },
        ["raw/", "wiki/", "核心文件索引.md"],
    )


def score_schema_governance_quality(assessment: dict[str, Any], stats: dict[str, Any]) -> dict[str, Any]:
    checks = {check["id"]: check["passed"] for check in assessment["checks"]}
    schema_text = stats["schema_text"]
    parts = [
        (100.0 if checks.get("schema_files_present") else 0.0, 20),
        (100.0 if checks.get("schema_declares_raw_wiki_layers") else 0.0, 15),
        (100.0 if checks.get("relationship_protocol_evidence") else 0.0, 15),
        (100.0 if "取信" in schema_text or "authority" in schema_text else 0.0, 15),
        (100.0 if "验证" in schema_text or "validate" in schema_text else 0.0, 15),
        (100.0 if "冲突" in schema_text or "conflict" in schema_text else 0.0, 10),
        (ratio_score(stats["relationship_marker_count"], 3, 100.0), 10),
    ]
    return dimension_base(
        "schema_governance_quality",
        weighted_average(parts),
        {
            "schema_files": SCHEMA_FILES,
            "relationship_marker_count": stats["relationship_marker_count"],
            "has_trust_policy": "取信" in schema_text or "authority" in schema_text,
            "has_validation_policy": "验证" in schema_text or "validate" in schema_text,
            "has_conflict_policy": "冲突" in schema_text or "conflict" in schema_text,
        },
        SCHEMA_FILES,
    )


def score_knowledge_sedimentation_effectiveness(stats: dict[str, Any]) -> dict[str, Any]:
    parts = [
        (ratio_score(stats["wiki_pages_with_frontmatter"], stats["wiki_markdown_count"], 0.0), 15),
        (ratio_score(stats["role_tagged_wiki_pages"], stats["wiki_markdown_count"], 0.0), 15),
        (ratio_score(stats["wiki_pages_with_raw_links"], stats["wiki_markdown_count"], 0.0), 20),
        (ratio_score(stats["latest_source_backed_count"], len(stats["latest_wiki_pages"]), 0.0), 20),
        (ratio_score(stats["multi_source_wiki_pages"], stats["wiki_markdown_count"], 0.0), 15),
        (ratio_score(stats["substantive_wiki_pages"], stats["wiki_markdown_count"], 0.0), 15),
    ]
    return dimension_base(
        "knowledge_sedimentation_effectiveness",
        weighted_average(parts),
        {
            "wiki_markdown_count": stats["wiki_markdown_count"],
            "wiki_pages_with_frontmatter": stats["wiki_pages_with_frontmatter"],
            "role_tagged_wiki_pages": stats["role_tagged_wiki_pages"],
            "wiki_pages_with_raw_links": stats["wiki_pages_with_raw_links"],
            "latest_wiki_pages": stats["latest_wiki_pages"],
            "latest_source_backed_count": stats["latest_source_backed_count"],
            "multi_source_wiki_pages": stats["multi_source_wiki_pages"],
            "substantive_wiki_pages": stats["substantive_wiki_pages"],
        },
        stats["latest_wiki_pages"][:10] or stats["root_markdown_samples"][:10],
    )


def score_retrieval_answerability(stats: dict[str, Any]) -> dict[str, Any]:
    index_text = stats["root_text"].get("index.md", "")
    machine_index_text = stats["root_text"].get("核心文件索引.md", "")
    link_issue_count = stats["dangling_wiki_links"] + stats.get("ambiguous_wiki_links", 0)
    broken_link_rate_score = 100.0 - ratio_score(link_issue_count, stats["total_wiki_links"], 100.0)
    orphan_rate_score = 100.0 - ratio_score(stats["orphan_wiki_pages"], stats["wiki_markdown_count"], 100.0)
    parts = [
        (100.0 if "[[" in index_text or "wiki/" in index_text else 0.0, 20),
        (100.0 if "[[" in machine_index_text or "wiki/" in machine_index_text else 0.0, 15),
        (broken_link_rate_score, 25),
        (orphan_rate_score, 20),
        (100.0 if stats["wiki_markdown_count"] > 0 else 0.0, 10),
        (ratio_score(stats["total_wiki_links"], max(stats["wiki_markdown_count"], 1), 0.0), 10),
    ]
    return dimension_base(
        "retrieval_answerability",
        weighted_average(parts),
        {
            "has_human_entry_links": "[[" in index_text or "wiki/" in index_text,
            "has_machine_index_links": "[[" in machine_index_text or "wiki/" in machine_index_text,
            "total_wiki_links": stats["total_wiki_links"],
            "dangling_wiki_links": stats["dangling_wiki_links"],
            "ambiguous_wiki_links": stats.get("ambiguous_wiki_links", 0),
            "orphan_wiki_pages": stats["orphan_wiki_pages"],
            "wiki_markdown_count": stats["wiki_markdown_count"],
        },
        ["index.md", "核心文件索引.md", "wiki/"],
    )


def score_maintenance_evolution(stats: dict[str, Any]) -> dict[str, Any]:
    log_text = stats["root_text"].get("log.md", "")
    schema_text = stats["schema_text"]
    link_issue_count = stats["dangling_wiki_links"] + stats.get("ambiguous_wiki_links", 0)
    broken_link_rate_score = 100.0 - ratio_score(link_issue_count, stats["total_wiki_links"], 100.0)
    stale_rate_score = 100.0 - ratio_score(stats["stale_wiki_pages"], stats["wiki_markdown_count"], 100.0)
    frontmatter_score = ratio_score(stats["wiki_pages_with_frontmatter"], stats["wiki_markdown_count"], 0.0)
    log_freshness_score = date_freshness_score(log_text)
    parts = [
        (100.0 if len(log_text.strip()) > 0 else 0.0, 20),
        (log_freshness_score, 15),
        (100.0 if OPERATION_HINT_RE.search(schema_text) else 0.0, 20),
        (broken_link_rate_score, 15),
        (stale_rate_score, 15),
        (frontmatter_score, 15),
    ]
    return dimension_base(
        "maintenance_evolution",
        weighted_average(parts),
        {
            "log_nonempty": len(log_text.strip()) > 0,
            "log_latest_date": latest_date_text(log_text),
            "log_freshness_score": log_freshness_score,
            "has_operation_policy": bool(OPERATION_HINT_RE.search(schema_text)),
            "dangling_wiki_links": stats["dangling_wiki_links"],
            "ambiguous_wiki_links": stats.get("ambiguous_wiki_links", 0),
            "stale_wiki_pages": stats["stale_wiki_pages"],
            "wiki_markdown_count": stats["wiki_markdown_count"],
        },
        ["log.md", "AGENTS.md", "RULES.md", "wiki/"],
    )


def extract_dates(text: str) -> list[datetime]:
    dates: list[datetime] = []
    for year, month, day in DATE_HINT_RE.findall(text):
        try:
            dates.append(datetime(int(year), int(month), int(day)))
        except ValueError:
            continue
    return dates


def latest_date_text(text: str) -> str | None:
    dates = extract_dates(text)
    if not dates:
        return None
    return max(dates).strftime("%Y-%m-%d")


def date_freshness_score(text: str, now: datetime | None = None) -> float:
    dates = extract_dates(text)
    if not dates:
        return 0.0
    current = now or datetime.now()
    latest = max(dates)
    age_days = (current.date() - latest.date()).days
    if age_days <= 90:
        return 100.0
    if age_days <= 180:
        return 75.0
    if age_days <= 365:
        return 50.0
    if age_days <= 730:
        return 25.0
    return 0.0


def build_dimensions(assessment: dict[str, Any], stats: dict[str, Any]) -> dict[str, Any]:
    return {
        "llm_wiki_architecture_fit": score_llm_wiki_architecture_fit(assessment, stats),
        "source_traceability": score_source_traceability(stats),
        "schema_governance_quality": score_schema_governance_quality(assessment, stats),
        "knowledge_sedimentation_effectiveness": score_knowledge_sedimentation_effectiveness(stats),
        "retrieval_answerability": score_retrieval_answerability(stats),
        "maintenance_evolution": score_maintenance_evolution(stats),
    }


def build_semantic_audit_plan(
    root: Path,
    stats: dict[str, Any],
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> dict[str, Any]:
    schema_samples = [file for file in SCHEMA_FILES + MAINTENANCE_FILES if (root / file).is_file()]
    navigation_samples = [file for file in OPTIONAL_NAVIGATION_FILES if (root / file).is_file()]
    wiki_samples = stats["latest_wiki_pages"][:5] or stats["root_markdown_samples"][:5]
    raw_samples = []
    raw_base = root / "raw"
    if raw_base.exists():
        raw_candidates = sorted(
            [
                path
                for path in iter_files(root, "raw", tool_name=tool_name, artifact_dir=artifact_dir)
                if path.suffix.lower() == ".md"
            ],
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        raw_samples = [relative(root, path) for path in raw_candidates[:5]]

    dimension_samples = {
        "llm_wiki_architecture_fit": schema_samples + navigation_samples + ["raw/", "wiki/"],
        "source_traceability": raw_samples + wiki_samples,
        "schema_governance_quality": schema_samples,
        "knowledge_sedimentation_effectiveness": wiki_samples,
        "retrieval_answerability": navigation_samples + wiki_samples,
        "maintenance_evolution": schema_samples + wiki_samples,
    }
    return {
        "status": "pending_llm_review",
        "dimension_samples": dimension_samples,
        "instruction": (
            "阅读 references/scoring_model.md、references/dimension_design_rationale.md "
            "和 references/probe_questions.md。逐维度检查列出的样本及其直接证据，"
            "并用固定探针问题形成可复核的语义评分。"
        ),
    }


def build_semantic_score_template(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("status") == "unscorable":
        raise SemanticScoreError("Cannot build semantic template for an unreadable or missing root.")
    audit = result.get("semantic_audit", {})
    dimension_samples = audit.get("dimension_samples", {})
    return {
        "schema_version": SEMANTIC_SCORE_SCHEMA_VERSION,
        "root": result.get("root"),
        "score_context": {
            "score_type": result.get("score_type"),
            "probe_question_reference": "references/probe_questions.md",
            "instructions": [
                "评分前阅读 references/scoring_model.md、references/dimension_design_rationale.md 和探针问题集。",
                "逐一读取样本文件，并读取验证结论所需的 source 文件。",
                "维度分使用 0-100，细项分使用 0-5。",
                "每个维度必须提供带 file 和 note 的证据；没有证据不得形成最终分。",
                "使用 references/probe_questions.md 中的固定探针问题，保持不同轮次评分可比较。",
                "不要让大模型在缺少文件证据时开放式判断架构等价性。",
            ],
        },
        "dimensions": {
            name: {
                "label": DIMENSION_LABELS[name],
                "weight": DIMENSION_WEIGHTS[name],
                "evaluates": DIMENSION_EVALUATES[name],
                "score": None,
                "criteria": {criterion: None for criterion in SEMANTIC_CRITERIA[name]},
                "samples": [
                    {"file": sample, "score": None, "evidence": [], "risks": []}
                    for sample in dimension_samples.get(name, [])
                ],
                "evidence": [],
                "risks": [],
            }
            for name in DIMENSION_WEIGHTS
        },
    }


def load_semantic_scores(path: str | Path) -> dict[str, Any]:
    path = Path(path).expanduser().resolve()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SemanticScoreError(f"Semantic score JSON is invalid: {exc}") from exc
    except OSError as exc:
        raise SemanticScoreError(f"Cannot read semantic score file: {path}") from exc


def validate_score(value: Any, field: str, issues: list[str]) -> None:
    if not isinstance(value, (int, float)):
        issues.append(f"{field} must be a number between 0 and 100.")
        return
    if value < 0 or value > 100:
        issues.append(f"{field} must be between 0 and 100.")


def validate_criteria(criteria: Any, required: list[str], field: str, issues: list[str]) -> None:
    if not isinstance(criteria, dict):
        issues.append(f"{field}.criteria must be an object.")
        return
    for name in required:
        value = criteria.get(name)
        if not isinstance(value, (int, float)) or value < 0 or value > 5:
            issues.append(f"{field}.criteria.{name} must be a number between 0 and 5.")


def criteria_average_score(criteria: Any, required: list[str]) -> float | None:
    if not isinstance(criteria, dict):
        return None
    values = [criteria.get(name) for name in required]
    if any(not isinstance(value, (int, float)) or value < 0 or value > 5 for value in values):
        return None
    return sum(float(value) for value in values) / len(values) * 20.0


def validate_score_criteria_alignment(
    score: Any,
    criteria: Any,
    required: list[str],
    field: str,
    issues: list[str],
) -> None:
    if not isinstance(score, (int, float)):
        return
    average = criteria_average_score(criteria, required)
    if average is None:
        return
    if abs(float(score) - average) > CRITERIA_SCORE_TOLERANCE:
        issues.append(
            f"{field}.score differs from criteria average by more than {CRITERIA_SCORE_TOLERANCE} points."
        )


def validate_evidence(evidence: Any, field: str, issues: list[str]) -> None:
    if not isinstance(evidence, list) or not evidence:
        issues.append(f"{field}.evidence must contain at least one evidence item.")
        return
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            issues.append(f"{field}.evidence[{index}] must be an object.")
            continue
        if not str(item.get("file", "")).strip():
            issues.append(f"{field}.evidence[{index}].file is required.")
        if not str(item.get("note", "")).strip():
            issues.append(f"{field}.evidence[{index}].note is required.")


def validate_semantic_scores(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if payload.get("schema_version") != SEMANTIC_SCORE_SCHEMA_VERSION:
        issues.append(f"schema_version must be {SEMANTIC_SCORE_SCHEMA_VERSION}.")
    dimensions = payload.get("dimensions")
    if not isinstance(dimensions, dict):
        return issues + ["dimensions must be an object."]
    for dimension_name, criteria in SEMANTIC_CRITERIA.items():
        field = f"dimensions.{dimension_name}"
        dimension = dimensions.get(dimension_name)
        if not isinstance(dimension, dict):
            issues.append(f"{field} is required.")
            continue
        validate_score(dimension.get("score"), field + ".score", issues)
        validate_criteria(dimension.get("criteria"), criteria, field, issues)
        validate_score_criteria_alignment(dimension.get("score"), dimension.get("criteria"), criteria, field, issues)
        validate_evidence(dimension.get("evidence"), field, issues)
        samples = dimension.get("samples", [])
        if samples is not None and not isinstance(samples, list):
            issues.append(f"{field}.samples must be a list when present.")
        if isinstance(samples, list):
            for sample_index, sample in enumerate(samples):
                sample_field = f"{field}.samples[{sample_index}]"
                if not isinstance(sample, dict):
                    issues.append(f"{sample_field} must be an object.")
                    continue
                if sample.get("score") is not None:
                    validate_score(sample.get("score"), sample_field + ".score", issues)
                if sample.get("criteria") is not None:
                    validate_criteria(sample.get("criteria"), criteria, sample_field, issues)
                    validate_score_criteria_alignment(
                        sample.get("score"),
                        sample.get("criteria"),
                        criteria,
                        sample_field,
                        issues,
                    )
                if sample.get("evidence"):
                    validate_evidence(sample.get("evidence"), sample_field, issues)
    return issues


def recompute_total_score(dimensions: dict[str, Any]) -> float:
    return round(
        sum(dimensions[name]["score"] * (DIMENSION_WEIGHTS[name] / 100.0) for name in DIMENSION_WEIGHTS),
        2,
    )


def apply_semantic_scores(result: dict[str, Any], semantic_scores: dict[str, Any]) -> dict[str, Any]:
    if result.get("status") == "unscorable":
        raise SemanticScoreError("Cannot apply semantic scores to an unreadable or missing root.")
    issues = validate_semantic_scores(semantic_scores)
    if issues:
        raise SemanticScoreError("; ".join(issues))

    final = json.loads(json.dumps(result, ensure_ascii=False))
    review_warnings: dict[str, list[str]] = {}
    for dimension_name, blend in SEMANTIC_BLEND_WEIGHTS.items():
        dimension = final["dimensions"][dimension_name]
        structural_score = float(dimension["structural_score"])
        semantic_dimension = semantic_scores["dimensions"][dimension_name]
        semantic_score = float(semantic_dimension["score"])
        blended_score = round(
            structural_score * blend["structural"] + semantic_score * blend["semantic"],
            2,
        )
        dimension["score"] = blended_score
        dimension["score_type"] = "integrated_structural_semantic"
        dimension["score_basis"] = {
            "objective_signals_weight": blend["structural"],
            "semantic_sampling_weight": blend["semantic"],
        }
        dimension["semantic_criteria"] = semantic_dimension["criteria"]
        dimension["semantic_evidence"] = semantic_dimension["evidence"]
        dimension["semantic_samples"] = semantic_dimension.get("samples", [])
        dimension["semantic_risks"] = semantic_dimension.get("risks", [])
        difference = abs(structural_score - semantic_score)
        if difference > STRUCTURAL_SEMANTIC_WARNING_THRESHOLD:
            warning = (
                f"结构信号 {round(structural_score, 2)} 与语义抽样 {round(semantic_score, 2)} "
                f"相差 {round(difference, 2)} 分，建议复核该维度的证据和样本选择。"
            )
            dimension.setdefault("review_warnings", []).append(warning)
            review_warnings.setdefault(dimension_name, []).append(warning)

    final["score"] = recompute_total_score(final["dimensions"])
    final["status"] = "scored"
    final["score_type"] = "final_integrated_semantic_sampling"
    final["semantic_input_validation"] = {
        "passed": True,
        "schema_version": semantic_scores.get("schema_version"),
        "validated_dimensions": list(SEMANTIC_BLEND_WEIGHTS),
    }
    if review_warnings:
        final["semantic_input_validation"]["review_warnings"] = review_warnings
    final["semantic_scores"] = semantic_scores
    final["recommendations"] = build_recommendations(final["dimensions"])
    return final


def unscorable_result(root: Path, reason: str) -> dict[str, Any]:
    return {
        "skill": "llm-wiki-health-score",
        "schema_version": SCHEMA_VERSION,
        "root": str(root),
        "status": "unscorable",
        "score": None,
        "score_type": "root_unreadable",
        "weights": DIMENSION_WEIGHTS,
        "architecture_assessment": {
            "karpathy_core_present": False,
            "blocking_issues": [
                {"id": "root_readable", "passed": False, "blocking": True, "evidence": str(root), "note": reason}
            ],
            "checks": [
                {"id": "root_readable", "passed": False, "blocking": True, "evidence": str(root), "note": reason}
            ],
        },
        "dimensions": {},
        "recommendations": ["请提供可读取的知识库根目录后再评分。"],
    }


def score_vault(
    root: str | Path,
    semantic_scores: dict[str, Any] | None = None,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        return unscorable_result(root, "根路径不是可读取目录。")

    stats = collect_stats(root, tool_name=tool_name, artifact_dir=artifact_dir)
    if stats["all_file_count"] == 0:
        return unscorable_result(root, "根目录没有可读取文件。")

    assessment = assess_architecture(root, stats)
    dimensions = build_dimensions(assessment, stats)
    result = {
        "skill": "llm-wiki-health-score",
        "schema_version": SCHEMA_VERSION,
        "root": str(root),
        "status": "needs_semantic_sampling",
        "score": None,
        "score_type": "semantic_sampling_required",
        "weights": DIMENSION_WEIGHTS,
        "architecture_assessment": assessment,
        "dimensions": dimensions,
        "semantic_audit": build_semantic_audit_plan(
            root,
            stats,
            tool_name=tool_name,
            artifact_dir=artifact_dir,
        ),
        "recommendations": build_recommendations(dimensions),
    }
    if semantic_scores is not None:
        return apply_semantic_scores(result, semantic_scores)
    return result


def build_recommendations(dimensions: dict[str, Any]) -> list[str]:
    if not dimensions:
        return []
    score_key = "score" if all("score" in dimension for dimension in dimensions.values()) else "structural_score"
    weak = sorted(dimensions.items(), key=lambda item: item[1].get(score_key, 0.0))[:2]
    recommendations = []
    for name, dimension in weak:
        label = dimension.get("label", name)
        value = dimension.get(score_key, 0.0)
        recommendations.append(f"优先改进 {label}: 当前信号分 {value}.")
    if score_key == "structural_score":
        recommendations.append("继续执行 LLM 语义抽样；没有语义输入时不要报告最终总分。")
    return recommendations


def render_markdown(result: dict[str, Any]) -> str:
    score_text = "`待语义抽样`" if result["score"] is None else f"`{result['score']}`"
    lines = [
        "# LLM Wiki 知识库评分",
        "",
        f"- 根目录: `{result['root']}`",
        f"- 状态: `{result['status']}`",
        f"- 分数: {score_text}",
        f"- 评分类型: `{result['score_type']}`",
        "",
        "## 架构信号",
    ]
    for check in result["architecture_assessment"]["checks"]:
        mark = "PASS" if check["passed"] else "FAIL"
        blocking = "阻塞项" if check["blocking"] else "评分信号"
        lines.append(f"- {mark} `{check['id']}` ({blocking}): {check['evidence']} - {check.get('note', '')}")

    if result["status"] == "semantic_input_invalid":
        issues = result.get("semantic_input_validation", {}).get("issues", [])
        lines.extend(["", "## 结果", "语义评分 JSON 不合规，最终评分未生成。"])
        for issue in issues:
            lines.append(f"- {issue}")
        return "\n".join(lines) + "\n"

    if result["status"] == "unscorable":
        lines.extend(["", "## 结果", "根路径不可读或没有可解析文件，无法评分。"])
        return "\n".join(lines) + "\n"

    lines.extend(["", "## 维度"])
    for name, dimension in result["dimensions"].items():
        if result["status"] == "scored":
            detail_score = f"{dimension['score']} / 100"
        else:
            detail_score = "待语义抽样"
        lines.append(f"- `{name}` {dimension['label']}: {detail_score}, 权重 {dimension['weight']}%")
        lines.append(f"  - 评估对象: {dimension['evaluates']}")
        if result["status"] == "scored":
            evidence = dimension.get("semantic_evidence", [])
            evidence_text = "; ".join(
                f"{item.get('file')}: {item.get('note')}" for item in evidence[:3] if isinstance(item, dict)
            )
            if evidence_text:
                lines.append(f"  - 语义依据: {evidence_text}")

    if result.get("score_type") == "final_integrated_semantic_sampling":
        validation = result.get("semantic_input_validation", {})
        lines.extend(["", "## 语义抽样"])
        lines.append(f"- 校验通过: `{validation.get('passed')}`")
        lines.append("- 已校验维度: " + ", ".join(f"`{item}`" for item in validation.get("validated_dimensions", [])))
    else:
        lines.extend(["", "## 语义抽样计划"])
        audit = result.get("semantic_audit", {})
        dimension_samples = audit.get("dimension_samples", {})
        for name, samples in dimension_samples.items():
            display = ", ".join(f"`{item}`" for item in samples[:8])
            lines.append(f"- `{name}` 样本: {display}")
        lines.append("- 评分模型: `references/scoring_model.md`")
        lines.append("- 维度设计依据: `references/dimension_design_rationale.md`")
        lines.append("- 固定探针问题: `references/probe_questions.md`")

    lines.extend(["", "## 建议"])
    for item in result.get("recommendations", []):
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def render_report(result: dict[str, Any], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)
    if output_format == "markdown":
        return render_markdown(result)
    raise ValueError(f"不支持的输出格式：{output_format}")


def report_artifact_path(
    result: dict[str, Any],
    output_format: str,
    out_path: str | Path | None,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> Path:
    if out_path is not None:
        return Path(out_path).expanduser().resolve()
    return default_artifact_paths(
        result["root"],
        output_format,
        tool_name=tool_name,
        artifact_dir=artifact_dir,
    )["report"]


def semantic_template_artifact_path(
    result: dict[str, Any],
    template_path: str | Path | None,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> Path:
    if template_path is not None:
        return Path(template_path).expanduser().resolve()
    return default_artifact_paths(
        result["root"],
        "markdown",
        tool_name=tool_name,
        artifact_dir=artifact_dir,
    )["semantic_template"]


def write_report_artifact(
    result: dict[str, Any],
    output_format: str,
    out_path: str | Path | None,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> Path:
    target = report_artifact_path(
        result,
        output_format,
        out_path,
        tool_name=tool_name,
        artifact_dir=artifact_dir,
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_report(result, output_format), encoding="utf-8")
    return target


def write_semantic_template_artifact(
    result: dict[str, Any],
    template_path: str | Path | None,
    tool_name: str | None = DEFAULT_TOOL_NAME,
    artifact_dir: str | Path | None = None,
) -> Path:
    target = semantic_template_artifact_path(
        result,
        template_path,
        tool_name=tool_name,
        artifact_dir=artifact_dir,
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(build_semantic_score_template(result), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="评估 Obsidian/个人知识库的 LLM Wiki 健康度。")
    parser.add_argument("--root", required=True, help="被评估知识库根目录。")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--out", help="可选报告文件；默认写入 <root>/.<tool-name>/llm-wiki-health/。")
    parser.add_argument("--artifact-dir", help="可选产物目录；覆盖 <root>/.<tool-name>/llm-wiki-health/。")
    parser.add_argument("--tool-name", default=DEFAULT_TOOL_NAME, help="用于默认产物目录的工具名。")
    parser.add_argument("--no-report-artifact", action="store_true", help="只打印标准输出，不写报告产物。")
    parser.add_argument("--no-artifacts", action="store_true", help="只打印标准输出，不写任何产物。")
    parser.add_argument("--semantic-input", help="由语义评审填写的 semantic_scores.json 路径。")
    parser.add_argument(
        "--require-final",
        action="store_true",
        help="未生成最终分时返回非 0 退出码。",
    )
    parser.add_argument(
        "--semantic-template-out",
        help="可选语义评分空模板路径；首轮扫描默认写入产物目录。",
    )
    return parser.parse_args()


def exit_code_for_result(result: dict[str, Any], require_final: bool = False) -> int:
    status = result.get("status")
    if status == "unscorable":
        return 2
    if status == "semantic_input_invalid":
        return 3
    if require_final and status != "scored":
        return 4
    return 0


def main() -> int:
    args = parse_args()
    semantic_scores = load_semantic_scores(args.semantic_input) if args.semantic_input else None
    template_source = score_vault(
        args.root,
        tool_name=args.tool_name,
        artifact_dir=args.artifact_dir,
    )
    try:
        result = apply_semantic_scores(template_source, semantic_scores) if semantic_scores else template_source
    except SemanticScoreError as exc:
        result = template_source
        result["status"] = "semantic_input_invalid"
        result["score"] = None
        result["score_type"] = "semantic_input_invalid"
        result["semantic_input_validation"] = {"passed": False, "issues": str(exc).split("; ")}
    artifact_paths: dict[str, str] = {}
    should_write_template = not args.no_artifacts and (
        args.semantic_template_out or (not args.semantic_input and template_source.get("status") != "unscorable")
    )
    should_write_report = not args.no_artifacts and (args.out or not args.no_report_artifact)
    if should_write_template:
        artifact_paths["semantic_template"] = str(
            semantic_template_artifact_path(
                template_source,
                args.semantic_template_out,
                tool_name=args.tool_name,
                artifact_dir=args.artifact_dir,
            )
        )
    if should_write_report:
        artifact_paths["report"] = str(
            report_artifact_path(
                result,
                args.format,
                args.out,
                tool_name=args.tool_name,
                artifact_dir=args.artifact_dir,
            )
        )
    if artifact_paths:
        result["artifacts"] = artifact_paths
    if should_write_template:
        write_semantic_template_artifact(
            template_source,
            args.semantic_template_out,
            tool_name=args.tool_name,
            artifact_dir=args.artifact_dir,
        )
    if should_write_report:
        write_report_artifact(
            result,
            args.format,
            args.out,
            tool_name=args.tool_name,
            artifact_dir=args.artifact_dir,
        )
    rendered = render_report(result, args.format)
    print(rendered)
    return exit_code_for_result(result, require_final=args.require_final)


if __name__ == "__main__":
    raise SystemExit(main())
