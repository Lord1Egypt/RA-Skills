#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Dict, Any
import importlib.util

import chromadb

ROOT = Path(os.environ.get("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw" / "workspace")))
MEMORY_DIR = ROOT / "memory"
INDEX_DIR = MEMORY_DIR / "index"
DAILY_DIR = MEMORY_DIR / "daily"
EPISODIC_DIR = MEMORY_DIR / "episodic"
SEMANTIC_DIR = MEMORY_DIR / "semantic"
PROCEDURAL_DIR = MEMORY_DIR / "procedural"
REPORTS_DIR = MEMORY_DIR / "reports"
STRUCTURED_DIR = MEMORY_DIR / "structured"
RAW_SUMMARY_DIR = MEMORY_DIR / "archive" / "raw-summaries"
JSONL_PATH = INDEX_DIR / "memory-records.jsonl"
MANIFEST_PATH = INDEX_DIR / "manifest.json"
SYNC_STATE_PATH = INDEX_DIR / "sync-state.json"
GC_POLICY_PATH = MEMORY_DIR / "GC_POLICY.md"
DEFAULT_REMOTE_URL = os.environ.get("MEMORY_REMOTE_URL", "")
DEFAULT_REMOTE_COLLECTION = os.environ.get("MEMORY_REMOTE_COLLECTION", "conversation-index")
DEFAULT_TENANT = os.environ.get("MEMORY_REMOTE_TENANT", "default_tenant")
DEFAULT_DATABASE = os.environ.get("MEMORY_REMOTE_DATABASE", "default_database")

# ChromaDB availability check
_CHROMADB_AVAILABLE = False
try:
    import chromadb
    _CHROMADB_AVAILABLE = True
except ImportError:
    pass
MEM0_DEFAULT_QUERY_LIMIT = 10
MEM0_SYNC_STATE_PATH = INDEX_DIR / "mem0-sync-state.json"
MEM0_ALLOWED_TYPES = {"preference", "decision", "project-state", "entity"}
MEM0_MIN_IMPORTANCE = 0.88

MAX_BULLETS = 8
MAX_BULLET_CHARS = 180
MAX_SUMMARY_CHARS = 900
HYBRID_DEFAULT_LIMIT = 8
BENCHMARK_DEFAULT_LIMIT = 5
GC_BLOCKED_SOURCE_PATTERNS = [
    "memory/SCHEMA.md",
    "memory/PIPELINE.md",
    "memory/POLICY.md",
    "memory/semantic/SCHEMA.md",
    "memory/semantic/POLICY.md",
    "memory/procedural/PIPELINE.md",
]
GC_BLOCKED_FILE_GLOBS = [
    "memory/semantic/SCHEMA.md",
    "memory/semantic/POLICY.md",
    "memory/procedural/PIPELINE.md",
    "memory/structured/*/*canonical-record*.md",
]


@dataclass
class Record:
    id: str
    type: str
    source_path: str
    title: str
    summary: str
    tags: List[str]
    importance: float
    timestamp: str
    content_hash: str
    sensitivity: str = "internal"
    status: str = "active"
    project: str = "memory-system"
    entities: List[str] | None = None
    source_kind: str = "compressed-summary"
    record_class: str = "compact"
    sync_policy: str = "remote-compact"
    vector_profile: str = "compacted"
    salience_level: str = "warm"
    retention_tier: str = "compact"
    delta_from: str | None = None

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "source_path": self.source_path,
            "title": self.title,
            "summary": self.summary,
            "tags": self.tags,
            "importance": self.importance,
            "timestamp": self.timestamp,
            "content_hash": self.content_hash,
            "sensitivity": self.sensitivity,
            "status": self.status,
            "project": self.project,
            "entities": self.entities or [],
            "source_kind": self.source_kind,
            "record_class": self.record_class,
            "sync_policy": self.sync_policy,
            "vector_profile": self.vector_profile,
            "salience_level": self.salience_level,
            "retention_tier": self.retention_tier,
            "delta_from": self.delta_from,
        }


def ensure_dirs() -> None:
    for path in [
        INDEX_DIR,
        DAILY_DIR,
        EPISODIC_DIR,
        SEMANTIC_DIR,
        PROCEDURAL_DIR,
        REPORTS_DIR,
        STRUCTURED_DIR / "decisions",
        STRUCTURED_DIR / "todos",
        STRUCTURED_DIR / "preferences",
        STRUCTURED_DIR / "entities",
        STRUCTURED_DIR / "project-state",
        STRUCTURED_DIR / "incidents",
        RAW_SUMMARY_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def now_local_date() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d")


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff._-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"


def clamp_line(line: str, max_chars: int = MAX_BULLET_CHARS) -> str:
    line = re.sub(r"^[-*]\s*", "", line.strip())
    line = re.sub(r"\s+", " ", line)
    return line if len(line) <= max_chars else line[: max_chars - 1].rstrip() + "…"


def extract_sections(text: str) -> List[tuple[str, List[str]]]:
    sections: List[tuple[str, List[str]]] = []
    current_title = "總覽"
    current_lines: List[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#"):
            if current_lines:
                sections.append((current_title, current_lines))
            current_title = re.sub(r"^#+\s*", "", line) or "未命名"
            current_lines = []
            continue
        if not line:
            continue
        current_lines.append(line)
    if current_lines:
        sections.append((current_title, current_lines))
    return sections


def summarize_markdown(text: str) -> Dict[str, Any]:
    text = clean_text(text)
    sections = extract_sections(text)
    highlights: List[str] = []
    titles: List[str] = []

    for title, lines in sections:
        titles.append(title)
        bullet_candidates: List[str] = []
        for line in lines:
            if line.startswith(("-", "*", "✅", "⚠️", "🚨")):
                bullet_candidates.append(clamp_line(line))
            elif len(bullet_candidates) < 2 and len(line) > 12:
                bullet_candidates.append(clamp_line(line))
        if bullet_candidates:
            highlights.append(f"{title}：" + "；".join(bullet_candidates[:2]))
        if len(highlights) >= MAX_BULLETS:
            break

    if not highlights:
        highlights = [clamp_line(x) for x in text.splitlines() if x.strip()][:MAX_BULLETS]

    summary = "\n".join(f"- {line}" for line in highlights[:MAX_BULLETS])
    summary = summary[:MAX_SUMMARY_CHARS].rstrip()
    return {"summary": summary, "titles": titles[:12], "highlights": highlights[:MAX_BULLETS]}


def infer_tags(path: Path, text: str, titles: Iterable[str]) -> List[str]:
    tags = {path.parent.name.lower(), path.stem.lower()}
    corpus = " ".join(list(titles)) + " " + text[:1000]
    keyword_map = {
        "chromadb": ["chromadb", "vector", "embedding", "collection"],
        "token": ["token", "context", "compaction"],
        "web": ["crawler", "playwright", "scrapling", "fetch"],
        "memory": ["memory", "episodic", "semantic", "procedural"],
        "sync": ["sync", "remote", "replica", "mirror"],
        "decision": ["decision", "decisions", "decided", "選擇", "決定"],
        "todo": ["todo", "next", "next steps", "待辦", "下一步"],
        "preference": ["prefer", "preference", "喜歡", "偏好", "avoid", "不要"],
        "incident": ["error", "issue", "warning", "failed", "失敗", "風險"],
    }
    lowered = corpus.lower()
    for tag, words in keyword_map.items():
        if any(w in lowered for w in words):
            tags.add(tag)
    return sorted(t for t in tags if t and t != "index")[:16]


def classify(path: Path, text: str) -> str:
    name = path.name.lower()
    body = text.lower()
    if re.match(r"\d{4}-\d{2}-\d{2}\.md$", name):
        return "episodic"
    if "steps:" in body or re.search(r"^\d+\.\s", text, flags=re.M):
        return "procedural"
    if any(k in body for k in ["decision", "decisions", "key facts", "learn", "knowledge", "建議"]):
        return "semantic"
    return "episodic"


def infer_sensitivity(text: str) -> str:
    lowered = text.lower()
    secret_markers = ["api key", "token", "password", "private key", "bearer ", "ssh "]
    private_markers = ["192.168.", "10.", "172.16.", "internal", "vpn", "firewall"]
    if any(marker in lowered for marker in secret_markers):
        return "secret"
    if any(marker in lowered for marker in private_markers):
        return "private"
    return "internal"


def extract_entities(text: str) -> List[str]:
    entities = set()
    patterns = [
        r"\b[A-Z][A-Za-z0-9_-]{2,}\b",
        r"\b(?:ChromaDB|Playwright|OpenClaw|Scrapling|StealthyFetcher)\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
    ]
    blocked = {"False", "True", "Only", "Memory", "Remote", "Record", "Rules", "Schema", "Structured", "Canonical", "Extraction", "Eligibility"}
    for pattern in patterns:
        for match in re.findall(pattern, text):
            if match not in blocked:
                entities.add(match)
    return sorted(entities)[:12]


def importance_for(record_type: str, path: Path, text: str) -> float:
    base = {"semantic": 0.9, "procedural": 0.92, "episodic": 0.7}.get(record_type, 0.65)
    lowered = text.lower()
    if "todo" in lowered or "next" in lowered or "下一步" in text:
        base += 0.03
    if any(x in lowered for x in ["decision", "決定", "preference", "偏好"]):
        base += 0.03
    if path.parent.name == "reports":
        base += 0.02
    return min(base, 0.99)


def load_module(module_name: str, relative_path: str):
    engine_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, engine_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {engine_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_retention_engine():
    return load_module("retention_policy", "scripts/retention-policy.py")


def rebuild_micro_index() -> Dict[str, Any]:
    module = load_module("micro_index_builder", "scripts/micro-index-builder.py")
    builder = module.MicroIndexBuilder(ROOT / "memory" / "index" / "shards")
    return builder.build(ROOT / "memory" / "index" / "memory-master-index.json", ROOT / "memory" / "index" / "thin-index.json", 100)


def rebuild_delta_summaries() -> Dict[str, Any]:
    module = load_module("delta_summary_builder", "scripts/delta-summary-builder.py")
    records = module.load_records()
    payload = module.build_deltas(records)
    output = ROOT / "memory" / "index" / "delta-summaries.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "records": len(records),
        "delta_count": payload.get("delta_count", 0),
        "output": str(output),
    }


def rebuild_hypermemory_report() -> Dict[str, Any]:
    module = load_module("hypermemory_report", "scripts/hypermemory-report.py")
    module.main()
    report_path = ROOT / "memory" / "reports" / f"hypermemory-report-{now_local_date()}.md"
    return {
        "report": str(report_path),
        "exists": report_path.exists(),
    }


def rebuild_hm4d_benchmark() -> Dict[str, Any]:
    module = load_module("hm4d_benchmark", "scripts/hm4d-benchmark.py")
    payload = module.run()
    module.write_report(payload)
    report_path = ROOT / "memory" / "reports" / f"hm4d-benchmark-{now_local_date()}.md"
    return {
        "report": str(report_path),
        "score": payload.get("score"),
        "max_score": payload.get("max_score"),
        "exists": report_path.exists(),
    }


def rebuild_phase2_artifacts() -> Dict[str, Any]:
    compression = load_module("phase2_retrieval_compression", "scripts/phase2-retrieval-compression.py")
    compression.main()
    pointer_pack = load_module("phase2_pointer_pack", "scripts/phase2-pointer-pack.py")
    pointer_pack.main()
    hot_only = load_module("phase2_hot_only_view", "scripts/phase2-hot-only-view.py")
    hot_only.main()
    packed_compare = load_module("phase2_packed_compare", "scripts/phase2-packed-compare.py")
    packed_compare.main()
    hot_compare = load_module("phase2_hot_compare", "scripts/phase2-hot-compare.py")
    hot_compare.main()
    dual_report = load_module("phase2_dual_path_report", "scripts/phase2-dual-path-report.py")
    dual_report.main()
    route_sim = load_module("phase2_route_simulator", "scripts/phase2-route-simulator.py")
    route_sim.main()
    compact_report = load_module("phase2_compact_report", "scripts/phase2-compact-report.py")
    compact_report.main()
    orchestrator = load_module("phase2b_orchestrator", "scripts/phase2b-orchestrator.py")
    orchestrator.main()
    incremental = load_module("phase2b_incremental_rebuild", "scripts/phase2b-incremental-rebuild.py")
    incremental.main()
    summary = load_module("phase2b_summary", "scripts/phase2b-summary.py")
    summary.main()
    phase3_router = load_module("phase3_query_router", "scripts/phase3-query-router.py")
    phase3_router.main()
    phase3_recovery = load_module("phase3_miss_recovery", "scripts/phase3-miss-recovery.py")
    phase3_recovery.main()
    phase3_benchmark = load_module("phase3_router_benchmark", "scripts/phase3-router-benchmark.py")
    phase3_benchmark.main()
    phase3_adaptive = load_module("phase3_adaptive_report", "scripts/phase3-adaptive-report.py")
    phase3_adaptive.main()
    phase3_integration = load_module("phase3_pipeline_integration", "scripts/phase3-pipeline-integration.py")
    phase3_integration.main()
    return {
        "retrieval_view": str(ROOT / "memory" / "index" / "retrieval-view.json"),
        "retrieval_view_packed": str(ROOT / "memory" / "index" / "retrieval-view-packed.json"),
        "retrieval_view_hot": str(ROOT / "memory" / "index" / "retrieval-view-hot.json"),
        "phase2_report": str(ROOT / "memory" / "reports" / f"phase2-compact-report-{now_local_date()}.md"),
        "phase2b_report": str(ROOT / "memory" / "reports" / f"phase2b-summary-{now_local_date()}.md"),
        "phase3_report": str(ROOT / "memory" / "reports" / f"phase3-adaptive-report-{now_local_date()}.md"),
    }


def reclassify_hm4d() -> Dict[str, Any]:
    module = load_module("reclassify_hm4d", "scripts/reclassify-hm4d.py")
    module.main()
    records = load_records()
    classified = sum(1 for item in records if item.get("salience_level") and item.get("retention_tier"))
    return {
        "records": len(records),
        "classified": classified,
    }


def dedupe_hm4d() -> Dict[str, Any]:
    module = load_module("dedupe_hm4d", "scripts/dedupe-hm4d.py")
    records = module.load_records()
    before = len(records)
    kept, removed = module.dedupe(records)
    module.write_records(kept)
    return {
        "before": before,
        "after": len(kept),
        "removed": len(removed),
    }


def canonicalize_auto_daily() -> Dict[str, Any]:
    module = load_module("canonicalize_auto_daily", "scripts/canonicalize-auto-daily.py")
    records = module.load_records()
    before = len(records)
    kept, removed = module.canonicalize(records)
    module.write_records(kept)
    return {
        "before": before,
        "after": len(kept),
        "removed": len(removed),
    }


def canonicalize_session_bootstrap() -> Dict[str, Any]:
    module = load_module("canonicalize_session_bootstrap", "scripts/canonicalize-session-bootstrap.py")
    records = module.load_records()
    before = len(records)
    kept, removed = module.canonicalize(records)
    module.write_records(kept)
    return {
        "before": before,
        "after": len(kept),
        "removed": len(removed),
    }


def infer_salience_and_retention(record_type: str, rel_path: str, importance: float, text: str) -> tuple[str, str]:
    module = load_retention_engine()
    result = module.evaluate({
        "type": record_type,
        "importance": importance,
        "source_path": rel_path,
        "summary": text,
    })
    return result["salience_level"], result["retention_tier"]


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def load_existing_hashes() -> Dict[str, Dict[str, Any]]:
    records: Dict[str, Dict[str, Any]] = {}
    if not JSONL_PATH.exists():
        return records
    with JSONL_PATH.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                if "content_hash" in item:
                    records[item["content_hash"]] = item
            except json.JSONDecodeError:
                continue
    return records


def load_records() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    if not JSONL_PATH.exists():
        return items
    with JSONL_PATH.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items


def append_records(records: List[Record]) -> None:
    if not records:
        return
    with JSONL_PATH.open("a", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record.to_json(), ensure_ascii=False) + "\n")


def build_memory_master_index() -> Dict[str, Any]:
    records = load_records()
    by_class: Dict[str, int] = {}
    by_type: Dict[str, int] = {}
    by_sync: Dict[str, int] = {}
    by_salience: Dict[str, int] = {}
    by_retention: Dict[str, int] = {}
    latest: List[Dict[str, Any]] = []
    for item in records:
        by_class[item.get("record_class", "unknown")] = by_class.get(item.get("record_class", "unknown"), 0) + 1
        by_type[item.get("type", "unknown")] = by_type.get(item.get("type", "unknown"), 0) + 1
        by_sync[item.get("sync_policy", "unknown")] = by_sync.get(item.get("sync_policy", "unknown"), 0) + 1
        by_salience[item.get("salience_level", "unknown")] = by_salience.get(item.get("salience_level", "unknown"), 0) + 1
        by_retention[item.get("retention_tier", "unknown")] = by_retention.get(item.get("retention_tier", "unknown"), 0) + 1
    latest = records[-20:]
    payload = {
        "updated_at": utc_now(),
        "total_records": len(records),
        "by_record_class": by_class,
        "by_type": by_type,
        "by_sync_policy": by_sync,
        "by_salience_level": by_salience,
        "by_retention_tier": by_retention,
        "latest_records": [
            {
                "id": item.get("id"),
                "title": item.get("title"),
                "brief": (item.get("summary") or "")[:120],
                "type": item.get("type"),
                "record_class": item.get("record_class"),
                "source_path": item.get("source_path"),
                "sync_policy": item.get("sync_policy"),
                "vector_profile": item.get("vector_profile"),
                "salience_level": item.get("salience_level"),
                "retention_tier": item.get("retention_tier"),
                "delta_from": item.get("delta_from"),
                "priority": 5,
            }
            for item in latest
        ],
    }
    master_path = INDEX_DIR / "memory-master-index.json"
    master_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def write_manifest(scanned: int, added: int, structured_added: int = 0) -> None:
    manifest = {
        "updated_at": utc_now(),
        "scanned_files": scanned,
        "indexed_records": sum(1 for _ in JSONL_PATH.open("r", encoding="utf-8")) if JSONL_PATH.exists() else 0,
        "last_added": added,
        "last_structured_added": structured_added,
        "strategy": {
            "store_raw_transcript": False,
            "max_summary_chars": MAX_SUMMARY_CHARS,
            "max_bullets": MAX_BULLETS,
            "local_primary": True,
            "remote_replica": True,
            "structured_extraction": True,
            "incremental_sync": True,
            "hybrid_retrieval": True,
            "gc_policy_enabled": True,
            "retrieval_benchmark_enabled": True,
            "index_first": True,
            "compact_first": True,
            "vector_quantization_ready": True,
            "hm4d_enabled": True,
        },
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    reclassify_hm4d()
    dedupe_hm4d()
    canonicalize_auto_daily()
    canonicalize_session_bootstrap()
    build_memory_master_index()
    rebuild_micro_index()
    rebuild_delta_summaries()
    rebuild_hypermemory_report()
    rebuild_hm4d_benchmark()
    rebuild_phase2_artifacts()


def write_sync_state(remote_enabled: bool = False) -> None:
    payload = load_json(
        SYNC_STATE_PATH,
        {
            "last_local_upsert_at": None,
            "last_remote_upsert_at": None,
            "remote_enabled": remote_enabled,
            "remote_url": DEFAULT_REMOTE_URL,
            "remote_collection": DEFAULT_REMOTE_COLLECTION,
            "remote_tenant": DEFAULT_TENANT,
            "remote_database": DEFAULT_DATABASE,
            "pending_remote": [],
            "failed_remote": [],
            "last_remote_status": "never",
            "last_remote_sync_index": 0,
            "last_remote_sync_ids": [],
        },
    )
    payload.setdefault("remote_url", DEFAULT_REMOTE_URL)
    payload.setdefault("remote_collection", DEFAULT_REMOTE_COLLECTION)
    payload.setdefault("remote_tenant", DEFAULT_TENANT)
    payload.setdefault("remote_database", DEFAULT_DATABASE)
    payload.setdefault("last_remote_sync_index", 0)
    payload.setdefault("last_remote_sync_ids", [])
    payload["last_local_upsert_at"] = utc_now()
    payload["remote_enabled"] = remote_enabled
    SYNC_STATE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def target_markdown_path(record_type: str, source_path: Path) -> Path:
    stem = source_path.stem
    if record_type == "episodic":
        return DAILY_DIR / f"{stem}.summary.md"
    if record_type == "semantic":
        return SEMANTIC_DIR / f"{stem}.md"
    return PROCEDURAL_DIR / f"{stem}.md"


def render_markdown(record: Record, highlights: List[str]) -> str:
    lines = [
        f"# {record.title}",
        "",
        f"- 類型：{record.type}",
        f"- 來源：{record.source_path}",
        f"- 重要度：{record.importance}",
        f"- 敏感度：{record.sensitivity}",
        f"- 時間：{record.timestamp}",
        "",
        "## 壓縮摘要",
        record.summary,
        "",
    ]
    if highlights:
        lines.extend(["## 重點", *[f"- {h}" for h in highlights], ""])
    if record.entities:
        lines.extend(["## 實體", *[f"- {entity}" for entity in record.entities], ""])
    return "\n".join(lines).rstrip() + "\n"


def should_skip(path: Path) -> bool:
    rel = str(path.relative_to(ROOT)) if path.is_absolute() else str(path)
    skip_patterns = [
        "memory/index/",
        "memory/archive/",
        "memory/daily/",
        "memory/PIPELINE.md",
        "memory/POLICY.md",
        "memory/SCHEMA.md",
        "memory/GC_POLICY.md",
        "memory/reports/",
        "memory/structured/",
        "memory/vector-db-",
        "README.md",
        ".summary.md",
    ]
    return any(pattern in rel for pattern in skip_patterns)


def build_record(path: Path) -> tuple[Record, List[str], str] | None:
    if not path.is_file() or path.suffix.lower() != ".md":
        return None
    if should_skip(path):
        return None
    text = clean_text(path.read_text(encoding="utf-8"))
    if not text:
        return None
    summarized = summarize_markdown(text)
    record_type = classify(path, text)
    content_hash = sha(text)
    title = summarized["titles"][0] if summarized["titles"] else path.stem
    record_id = f"mem_{path.stem}_{content_hash[:12]}"
    rel_path = str(path.relative_to(ROOT))
    record_class = "compact"
    sync_policy = "remote-compact"
    vector_profile = "compacted"
    source_kind = "compressed-summary"
    if rel_path.startswith("memory/reports/"):
        source_kind = "compact-report"
        record_class = "compact"
        sync_policy = "remote-compact"
        vector_profile = "compacted"
    elif rel_path.startswith("memory/structured/"):
        source_kind = "structured-memory"
        record_class = "structured"
        sync_policy = "remote-structured"
        vector_profile = "compacted"
    elif rel_path.startswith("memory/"):
        source_kind = "compressed-summary"
        record_class = "compact"
        sync_policy = "remote-compact"
        vector_profile = "standard"

    importance = importance_for(record_type, path, text)
    salience_level, retention_tier = infer_salience_and_retention(record_type, rel_path, importance, text)
    record = Record(
        id=record_id,
        type=record_type,
        source_path=rel_path,
        title=title,
        summary=summarized["summary"],
        tags=infer_tags(path, text, summarized["titles"]),
        importance=importance,
        timestamp=utc_now(),
        content_hash=content_hash,
        sensitivity=infer_sensitivity(text),
        entities=extract_entities(text),
        source_kind=source_kind,
        record_class=record_class,
        sync_policy=sync_policy,
        vector_profile=vector_profile,
        salience_level=salience_level,
        retention_tier=retention_tier,
    )
    return record, summarized["highlights"], text


def scan_targets(paths: List[Path]) -> List[Path]:
    discovered: List[Path] = []
    for path in paths:
        if path.is_file():
            discovered.append(path)
        elif path.is_dir():
            discovered.extend(sorted(p for p in path.rglob("*.md") if not should_skip(p)))
    deduped = []
    seen = set()
    for p in discovered:
        rp = str(p.resolve())
        if rp not in seen:
            seen.add(rp)
            deduped.append(p)
    return deduped


def extract_structured_memory(record: Record, full_text: str) -> List[Record]:
    outputs: List[Record] = []
    lowered = full_text.lower()
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]

    def make(kind: str, title: str, summary: str, suffix: str, importance: float | None = None) -> Record:
        content_hash = sha(f"{record.content_hash}:{kind}:{summary}")
        return Record(
            id=f"{record.id}_{suffix}_{content_hash[:8]}",
            type=kind,
            source_path=record.source_path,
            title=title,
            summary=summary[:MAX_SUMMARY_CHARS],
            tags=sorted(set(record.tags + [kind])),
            importance=min(importance or max(record.importance, 0.88), 0.99),
            timestamp=record.timestamp,
            content_hash=content_hash,
            sensitivity=record.sensitivity,
            entities=record.entities,
            source_kind="structured-memory",
            record_class="structured",
            sync_policy="remote-structured",
            vector_profile="compacted",
            salience_level="hot",
            retention_tier="structured",
            delta_from=record.id,
        )

    decision_lines = [clamp_line(line) for line in lines if re.search(r"decision|decisions|decided|建議|決定", line, flags=re.I)]
    todo_lines = [clamp_line(line) for line in lines if re.search(r"todo|next|next steps|待辦|下一步", line, flags=re.I)]
    pref_lines = [clamp_line(line) for line in lines if re.search(r"prefer|preference|avoid|style|偏好|不要", line, flags=re.I)]
    incident_lines = [clamp_line(line) for line in lines if re.search(r"error|issue|warning|failed|失敗|風險|警告", line, flags=re.I)]
    project_state_lines = [clamp_line(line) for line in lines if line.startswith(("-", "*", "✅", "⚠️", "🚨"))][:6]
    entities = record.entities or []

    if decision_lines:
        outputs.append(make("decision", f"決策 · {record.title}", "\n".join(f"- {x}" for x in decision_lines[:6]), "decision", 0.93))
    if todo_lines:
        outputs.append(make("todo", f"待辦 · {record.title}", "\n".join(f"- {x}" for x in todo_lines[:8]), "todo", 0.91))
    if pref_lines:
        outputs.append(make("preference", f"偏好 · {record.title}", "\n".join(f"- {x}" for x in pref_lines[:6]), "preference", 0.94))
    if incident_lines:
        outputs.append(make("incident", f"事件 · {record.title}", "\n".join(f"- {x}" for x in incident_lines[:8]), "incident", 0.9))
    if project_state_lines and any(key in lowered for key in ["status", "state", "完成", "運行", "正常", "測試"]):
        outputs.append(make("project-state", f"專案狀態 · {record.title}", "\n".join(f"- {x}" for x in project_state_lines), "state", 0.9))
    if entities:
        outputs.append(make("entity", f"實體 · {record.title}", "\n".join(f"- {x}" for x in entities), "entity", 0.88))
    return outputs


def structured_target_path(record: Record) -> Path:
    mapping = {
        "decision": STRUCTURED_DIR / "decisions",
        "todo": STRUCTURED_DIR / "todos",
        "preference": STRUCTURED_DIR / "preferences",
        "entity": STRUCTURED_DIR / "entities",
        "project-state": STRUCTURED_DIR / "project-state",
        "incident": STRUCTURED_DIR / "incidents",
    }
    return mapping[record.type] / f"{slugify(record.title)}.md"


def write_structured_record(record: Record) -> None:
    structured_target_path(record).write_text(render_markdown(record, []), encoding="utf-8")


def ingest(paths: List[Path], remote_enabled: bool = False) -> Dict[str, int]:
    ensure_dirs()
    write_sync_state(remote_enabled=remote_enabled)
    existing = load_existing_hashes()
    scanned = 0
    added = 0
    structured_added = 0
    new_records: List[Record] = []

    for path in scan_targets(paths):
        scanned += 1
        built = build_record(path)
        if not built:
            continue
        record, highlights, full_text = built
        if record.content_hash in existing:
            continue
        target = target_markdown_path(record.type, path)
        target.write_text(render_markdown(record, highlights), encoding="utf-8")
        raw_target = RAW_SUMMARY_DIR / f"{path.stem}.{record.content_hash[:10]}.txt"
        raw_target.write_text(record.summary + "\n", encoding="utf-8")
        new_records.append(record)
        existing[record.content_hash] = record.to_json()
        added += 1

        for structured in extract_structured_memory(record, full_text):
            if structured.content_hash in existing:
                continue
            write_structured_record(structured)
            new_records.append(structured)
            existing[structured.content_hash] = structured.to_json()
            structured_added += 1

    append_records(new_records)
    write_manifest(scanned, added, structured_added)
    return {"added": added, "structured_added": structured_added}


def compute_stats() -> Dict[str, Any]:
    ensure_dirs()
    counts: Dict[str, int] = {}
    chars: Dict[str, int] = {}
    directories = {
        "daily": DAILY_DIR,
        "episodic": EPISODIC_DIR,
        "semantic": SEMANTIC_DIR,
        "procedural": PROCEDURAL_DIR,
        "reports": REPORTS_DIR,
        "structured_decisions": STRUCTURED_DIR / "decisions",
        "structured_todos": STRUCTURED_DIR / "todos",
        "structured_preferences": STRUCTURED_DIR / "preferences",
        "structured_entities": STRUCTURED_DIR / "entities",
        "structured_project_state": STRUCTURED_DIR / "project-state",
        "structured_incidents": STRUCTURED_DIR / "incidents",
    }
    for name, path in directories.items():
        files = list(path.glob("*.md"))
        counts[name] = len(files)
        chars[name] = sum(f.stat().st_size for f in files if f.is_file())
    total_chars = sum(chars.values())
    estimated_tokens = max(total_chars // 4, 0)
    budget = 128000
    usage_pct = round((estimated_tokens / budget) * 100, 2) if budget else 0
    return {"counts": counts, "chars": chars, "estimated_tokens": estimated_tokens, "token_budget": budget, "usage_pct": usage_pct}


def generate_report() -> Path:
    stats = compute_stats()
    today = now_local_date()
    report_path = REPORTS_DIR / f"daily-{today}.md"
    records = load_records()
    recent = records[-10:]
    by_type: Dict[str, int] = {}
    for item in records:
        by_type[item.get("type", "unknown")] = by_type.get(item.get("type", "unknown"), 0) + 1
    sync_state = load_json(SYNC_STATE_PATH, {})
    lines = [
        f"# 記憶管線報表 · {today}",
        "",
        "## 摘要",
        f"- 已索引記錄數：{len(records)}",
        f"- 預估工作集 Token：{stats['estimated_tokens']} / {stats['token_budget']}",
        f"- 使用率：{stats['usage_pct']}%",
        f"- 上次遠端同步索引：{sync_state.get('last_remote_sync_index', 0)}",
        f"- 上次遠端狀態：{sync_state.get('last_remote_status', 'never')}",
        "",
        "## 類型分佈",
    ]
    for key in sorted(by_type):
        lines.append(f"- {key}：{by_type[key]}")
    lines.extend(["", "## 最近記錄"])
    for item in recent:
        lines.append(f"- [{item.get('type')}] {item.get('title')}（{item.get('sensitivity', 'internal')}）")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def parse_remote_url(remote_url: str) -> Dict[str, Any]:
    parsed = urllib.parse.urlparse(remote_url)
    host = parsed.hostname or remote_url.replace("http://", "").replace("https://", "").split(":")[0]
    port = parsed.port or (443 if parsed.scheme == "https" else 8000)
    ssl = parsed.scheme == "https"
    base = f"{'https' if ssl else 'http'}://{host}:{port}"
    return {"host": host, "port": port, "ssl": ssl, "base": base}


def make_remote_client(remote_url: str):
    conn = parse_remote_url(remote_url)
    return chromadb.HttpClient(host=conn["host"], port=conn["port"], ssl=conn["ssl"])


def remote_healthcheck(remote_url: str = DEFAULT_REMOTE_URL, collection: str = DEFAULT_REMOTE_COLLECTION) -> Dict[str, Any]:
    conn = parse_remote_url(remote_url)
    base = conn["base"]
    heartbeat_candidates = [
        f"{base}/api/v2/heartbeat",
        f"{base}/api/v1/heartbeat",
        f"{base}/api/v2/version",
        f"{base}/api/v1/version",
    ]
    heartbeat = {"ok": False, "url": None, "status": None, "body": None, "error": None}
    for url in heartbeat_candidates:
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                body = r.read(200).decode("utf-8", "ignore")
                heartbeat = {"ok": True, "url": url, "status": r.status, "body": body, "error": None}
                break
        except urllib.error.HTTPError as e:
            if e.code in {200}:
                heartbeat = {"ok": True, "url": url, "status": e.code, "body": "", "error": None}
                break
            heartbeat = {"ok": False, "url": url, "status": e.code, "body": None, "error": str(e)}
            if e.code not in {404, 410}:
                break
        except Exception as e:
            heartbeat = {"ok": False, "url": url, "status": None, "body": None, "error": str(e)}

    client = None
    collection_ok = False
    collection_error = None
    collection_count = None
    try:
        client = make_remote_client(remote_url)
        col = client.get_or_create_collection(name=collection)
        collection_ok = True
        try:
            collection_count = col.count()
        except Exception:
            collection_count = None
    except Exception as e:
        collection_error = str(e)

    return {
        "remote_url": remote_url,
        "collection": collection,
        "connection": conn,
        "heartbeat": heartbeat,
        "client_ok": client is not None,
        "collection_ok": collection_ok,
        "collection_count": collection_count,
        "collection_error": collection_error,
        "ok": collection_ok,
    }


def eligible_for_remote(record: Dict[str, Any]) -> bool:
    if record.get("sensitivity") not in {"public", "internal"}:
        return False
    if record.get("status", "active") != "active":
        return False
    source_kind = str(record.get("source_kind", ""))
    source_path = str(record.get("source_path", ""))
    allowed_kinds = {"compressed-summary", "structured-memory", "compact-report"}
    if source_kind in allowed_kinds:
        return True
    if source_path.startswith("memory/reports/"):
        return True
    return False


def remote_sync(remote_url: str = DEFAULT_REMOTE_URL, collection: str = DEFAULT_REMOTE_COLLECTION, force: bool = False) -> Dict[str, Any]:
    ensure_dirs()
    state = load_json(SYNC_STATE_PATH, {
        "last_local_upsert_at": None,
        "last_remote_upsert_at": None,
        "remote_enabled": True,
        "remote_url": remote_url,
        "remote_collection": collection,
        "remote_tenant": DEFAULT_TENANT,
        "remote_database": DEFAULT_DATABASE,
        "pending_remote": [],
        "failed_remote": [],
        "last_remote_status": "never",
        "last_remote_sync_index": 0,
        "last_remote_sync_ids": [],
        "last_remote_validation": None,
    })
    state["remote_enabled"] = True
    state["remote_url"] = remote_url
    state["remote_collection"] = collection

    all_records = load_records()
    filtered = [record for record in all_records if eligible_for_remote(record)]
    sync_index = 0 if force else int(state.get("last_remote_sync_index", 0))
    delta = filtered[sync_index:]

    validation = remote_healthcheck(remote_url=remote_url, collection=collection)
    state["last_remote_validation"] = validation
    if not validation.get("ok"):
        state["last_remote_status"] = "error:validation_failed"
        state["failed_remote"] = [{"at": utc_now(), "error": validation.get("collection_error") or validation.get("heartbeat", {}).get("error") or "remote validation failed", "records": len(delta), "start_index": sync_index}]
        state["pending_remote"] = [item.get("id") for item in delta[:100]]
        SYNC_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {"ok": False, "error": "remote validation failed", "validation": validation, "records": len(delta), "total_eligible": len(filtered), "collection": collection, "remote_url": remote_url}

    try:
        client = make_remote_client(remote_url)
        remote_collection_obj = client.get_or_create_collection(name=collection)

        ids = [item["id"] for item in delta]
        documents = [item["summary"] for item in delta]
        metadatas = [{
            "type": item.get("type", "unknown"),
            "source_path": item.get("source_path", ""),
            "importance": float(item.get("importance", 0.0)),
            "timestamp": item.get("timestamp", ""),
            "sensitivity": item.get("sensitivity", "internal"),
            "project": item.get("project", "memory-system"),
            "source_kind": item.get("source_kind", "compressed-summary"),
            "content_hash": item.get("content_hash", ""),
            "tags": ",".join(item.get("tags", [])[:16]),
            "entities": ",".join(item.get("entities", [])[:12]),
            "force_sync": str(bool(force)).lower(),
        } for item in delta]

        if ids:
            remote_collection_obj.upsert(ids=ids, documents=documents, metadatas=metadatas)

        state["last_remote_upsert_at"] = utc_now()
        state["remote_enabled"] = True
        state["last_remote_status"] = "ok:chromadb-httpclient"
        state["pending_remote"] = []
        state["failed_remote"] = []
        state["last_remote_sync_index"] = len(filtered)
        state["last_remote_sync_ids"] = ids[-20:]
        SYNC_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {
            "ok": True,
            "status": "已上傳",
            "records": len(delta),
            "total_eligible": len(filtered),
            "collection": collection,
            "remote_url": remote_url,
            "incremental": not force,
            "start_index": sync_index,
            "end_index": len(filtered),
        }
    except Exception as exc:
        state["last_remote_status"] = f"error:{exc.__class__.__name__}"
        state["failed_remote"] = [{"at": utc_now(), "error": str(exc), "records": len(delta), "start_index": sync_index}]
        state["pending_remote"] = [item.get("id") for item in delta[:100]]
        SYNC_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {"ok": False, "error": str(exc), "records": len(delta), "total_eligible": len(filtered), "collection": collection, "remote_url": remote_url}


def load_index_hits(query: str, limit: int = HYBRID_DEFAULT_LIMIT) -> List[Dict[str, Any]]:
    terms = [t.lower() for t in re.findall(r"\w+|[\u4e00-\u9fff]+", query) if t.strip()]
    candidates: List[Dict[str, Any]] = []
    index_files = [
        ROOT / "memory/index/memory-master-index.json",
        ROOT / "docs/index/workspace-md-index.json",
        ROOT / "docs/index/skills-catalog.json",
    ]
    for path in index_files:
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        items = payload.get("items") if isinstance(payload, dict) else None
        if items is None and path.name == "memory-master-index.json":
            items = payload.get("latest_records", []) if isinstance(payload, dict) else []
        if not isinstance(items, list):
            continue
        for item in items:
            haystack = json.dumps(item, ensure_ascii=False).lower()
            score = sum(2 for term in terms if term in haystack)
            if score <= 0:
                continue
            candidates.append({
                "source": "index",
                "score": float(score) + 1.0,
                "record": {
                    "id": item.get("id") or item.get("path") or item.get("name") or sha(haystack)[:12],
                    "type": item.get("type", "index"),
                    "title": item.get("title") or item.get("name") or item.get("path", path.name),
                    "summary": item.get("summary") or item.get("brief") or item.get("path", ""),
                    "source_path": item.get("path") or item.get("skill_path") or str(path.relative_to(ROOT)),
                    "record_class": item.get("record_class", "index"),
                    "source_kind": item.get("source_kind", "index"),
                },
            })
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:limit]


def local_search(query: str, limit: int = HYBRID_DEFAULT_LIMIT, preferred_types: List[str] | None = None) -> List[Dict[str, Any]]:
    terms = [t.lower() for t in re.findall(r"\w+|[\u4e00-\u9fff]+", query) if t.strip()]
    records = load_records()
    blocked_sources = {"memory/SCHEMA.md", "memory/PIPELINE.md", "memory/POLICY.md"}
    scored: List[Dict[str, Any]] = []
    type_priority = {"preference": 6, "decision": 5, "todo": 5, "project-state": 4, "entity": 4, "semantic": 3, "procedural": 3, "episodic": 2, "incident": 4}

    for record in records:
        if record.get("status", "active") != "active":
            continue
        if record.get("source_path") in blocked_sources:
            continue
        haystack = " ".join([
            record.get("title", ""),
            record.get("summary", ""),
            " ".join(record.get("tags", [])),
            " ".join(record.get("entities", [])),
            record.get("type", ""),
            record.get("record_class", ""),
        ]).lower()
        match_score = sum(3 for term in terms if term in record.get("title", "").lower())
        match_score += sum(2 for term in terms if term in record.get("summary", "").lower())
        match_score += sum(1 for term in terms if term in haystack)
        if preferred_types and record.get("type") in preferred_types:
            match_score += 2
        if record.get("record_class") == "structured":
            match_score += 2
        elif record.get("record_class") == "compact":
            match_score += 1
        if match_score <= 0:
            continue
        final_score = match_score + float(record.get("importance", 0.0)) * 4 + type_priority.get(record.get("type", ""), 0)
        scored.append({"source": "local", "score": round(final_score, 3), "record": record})

    scored = load_index_hits(query, limit=limit) + scored
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]


def remote_search(query: str, remote_url: str, collection: str, limit: int = HYBRID_DEFAULT_LIMIT) -> List[Dict[str, Any]]:
    try:
        client = make_remote_client(remote_url)
        col = client.get_collection(name=collection)
        result = col.query(query_texts=[query], n_results=limit)
        ids = (result.get("ids") or [[]])[0]
        docs = (result.get("documents") or [[]])[0]
        metas = (result.get("metadatas") or [[]])[0]
        distances = (result.get("distances") or [[]])[0]
        items: List[Dict[str, Any]] = []
        for idx, rec_id in enumerate(ids):
            meta = metas[idx] if idx < len(metas) and metas[idx] else {}
            distance = distances[idx] if idx < len(distances) else 999.0
            score = round(max(0.0, 10.0 - float(distance)), 3)
            items.append({
                "source": "remote",
                "score": score,
                "record": {
                    "id": rec_id,
                    "type": meta.get("type", "unknown"),
                    "title": meta.get("source_path", rec_id),
                    "summary": docs[idx] if idx < len(docs) else "",
                    "source_path": meta.get("source_path", ""),
                    "importance": meta.get("importance", 0.0),
                    "sensitivity": meta.get("sensitivity", "internal"),
                    "entities": (meta.get("entities", "") or "").split(",") if meta.get("entities") else [],
                    "tags": (meta.get("tags", "") or "").split(",") if meta.get("tags") else [],
                    "timestamp": meta.get("timestamp", ""),
                    "project": meta.get("project", "memory-system"),
                    "source_kind": meta.get("source_kind", "remote"),
                },
            })
        return items
    except Exception:
        return []


def hybrid_search(query: str, limit: int = HYBRID_DEFAULT_LIMIT, remote_url: str = DEFAULT_REMOTE_URL, collection: str = DEFAULT_REMOTE_COLLECTION) -> Dict[str, Any]:
    ql = query.lower()
    preferred_types = []
    if any(x in ql for x in ["preference", "prefer", "偏好"]):
        preferred_types = ["preference", "decision"]
    elif any(x in ql for x in ["todo", "next", "待辦", "下一步"]):
        preferred_types = ["todo", "project-state"]
    elif any(x in ql for x in ["decision", "decide", "決定"]):
        preferred_types = ["decision", "project-state"]

    local_results = local_search(query, limit=limit, preferred_types=preferred_types)
    remote_results = remote_search(query, remote_url=remote_url, collection=collection, limit=limit)

    merged: Dict[str, Dict[str, Any]] = {}
    for item in local_results + remote_results:
        rec = item["record"]
        rec_id = rec.get("id") or sha(json.dumps(rec, ensure_ascii=False))[:12]
        if rec_id not in merged or item["score"] > merged[rec_id]["score"]:
            merged[rec_id] = item

    ranked = sorted(merged.values(), key=lambda x: x["score"], reverse=True)[:limit]
    return {
        "query": query,
        "local_count": len(local_results),
        "remote_count": len(remote_results),
        "results": ranked,
    }


def remote_search_multi(query: str, remote_url: str, collections: List[str], limit: int = HYBRID_DEFAULT_LIMIT) -> List[Dict[str, Any]]:
    merged: Dict[str, Dict[str, Any]] = {}
    for collection in collections:
        items = remote_search(query, remote_url=remote_url, collection=collection, limit=limit)
        for item in items:
            rec = item["record"]
            rec_id = rec.get("id") or sha(json.dumps(rec, ensure_ascii=False))[:12]
            rec["collection"] = collection
            boost = 0.0
            if collection == "openclaw_memory_compacted":
                boost = 1.5
            elif collection == "openclaw_memory":
                boost = 0.7
            item["score"] = round(float(item["score"]) + boost, 3)
            if rec_id not in merged or item["score"] > merged[rec_id]["score"]:
                merged[rec_id] = item
    return sorted(merged.values(), key=lambda x: x["score"], reverse=True)[:limit]


def hybrid_search_fallback(
    query: str,
    limit: int = HYBRID_DEFAULT_LIMIT,
    remote_url: str = DEFAULT_REMOTE_URL,
    collections: List[str] | None = None,
) -> Dict[str, Any]:
    preferred = collections or ["openclaw_memory_compacted", "openclaw_memory", "conversation-index"]
    local_results = local_search(query, limit=limit)
    remote_results = remote_search_multi(query, remote_url=remote_url, collections=preferred, limit=limit)

    merged: Dict[str, Dict[str, Any]] = {}
    for item in local_results + remote_results:
        rec = item["record"]
        rec_id = rec.get("id") or sha(json.dumps(rec, ensure_ascii=False))[:12]
        if rec_id not in merged or item["score"] > merged[rec_id]["score"]:
            merged[rec_id] = item

    ranked = sorted(merged.values(), key=lambda x: x["score"], reverse=True)[:limit]
    return {
        "query": query,
        "collections": preferred,
        "local_count": len(local_results),
        "remote_count": len(remote_results),
        "results": ranked,
    }


def benchmark_queries() -> List[Dict[str, Any]]:
    return [
        {"query": "ChromaDB 狀態", "expected_types": ["project-state", "entity", "episodic"]},
        {"query": "SSL 失敗 問題", "expected_types": ["incident", "episodic"]},
        {"query": "Playwright 已安裝", "expected_types": ["project-state", "entity"]},
    ]


def run_benchmark(limit: int = BENCHMARK_DEFAULT_LIMIT, remote_url: str = DEFAULT_REMOTE_URL, collection: str = DEFAULT_REMOTE_COLLECTION) -> Path:
    report_path = REPORTS_DIR / f"retrieval-benchmark-{now_local_date()}.md"
    cases = benchmark_queries()
    results = []
    pass_count = 0

    for case in cases:
        res = hybrid_search(case["query"], limit=limit, remote_url=remote_url, collection=collection)
        top_types = [item["record"].get("type", "unknown") for item in res["results"][:3]]
        hit = any(t in case["expected_types"] for t in top_types)
        if hit:
            pass_count += 1
        results.append({
            "query": case["query"],
            "expected_types": case["expected_types"],
            "top_types": top_types,
            "hit": hit,
            "local_count": res["local_count"],
            "remote_count": res["remote_count"],
        })

    score = round((pass_count / len(cases)) * 100, 2) if cases else 0.0
    lines = [
        f"# 混合檢索基準報表 · {now_local_date()}",
        "",
        "## 摘要",
        f"- 測試案例數：{len(cases)}",
        f"- 命中案例數：{pass_count}",
        f"- Recall 命中率：{score}%",
        "",
        "## 明細",
    ]
    for item in results:
        lines.extend([
            f"### 查詢：{item['query']}",
            f"- 預期類型：{', '.join(item['expected_types'])}",
            f"- Top 類型：{', '.join(item['top_types']) if item['top_types'] else '無'}",
            f"- 命中：{'是' if item['hit'] else '否'}",
            f"- 本地結果數：{item['local_count']}",
            f"- 遠端結果數：{item['remote_count']}",
            "",
        ])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def write_gc_policy() -> None:
    content = """# Memory GC Policy

## 目標
避免 schema / policy / 報表 / 衍生摘要污染正式記憶索引與混合檢索結果。

## 自動清理範圍
- schema / policy / pipeline 類文件衍生記憶
- `*canonical-record*.md` 類衍生記憶
- 不應進入索引的控制文件副本
- 已知污染來源對應的 JSONL 記錄

## 阻擋來源
- `memory/SCHEMA.md`
- `memory/POLICY.md`
- `memory/PIPELINE.md`
- `memory/GC_POLICY.md`
- `memory/semantic/SCHEMA.md`
- `memory/semantic/POLICY.md`
- `memory/procedural/PIPELINE.md`

## 清理規則
1. 先刪除污染檔案。
2. 重建 `memory/index/memory-records.jsonl`。
3. 重建 `memory/daily/` 與 `memory/structured/`。
4. 若需要，使用 `sync-remote --force` 重建遠端 collection。
5. 重新執行 retrieval benchmark 驗證品質。

## 觸發時機
- 每日維護後執行一次快速 GC 檢查
- 每週執行一次完整 GC + benchmark
- 發現 hybrid retrieval 結果異常時立即執行
"""
    GC_POLICY_PATH.write_text(content, encoding="utf-8")


def gc_cleanup() -> Dict[str, Any]:
    ensure_dirs()
    write_gc_policy()
    removed_files: List[str] = []

    for pattern in GC_BLOCKED_FILE_GLOBS:
        for path in ROOT.glob(pattern):
            if path.exists() and path.is_file():
                removed_files.append(str(path.relative_to(ROOT)))
                path.unlink()

    records = load_records()
    cleaned = []
    removed_records = 0
    for item in records:
        source_path = item.get("source_path", "")
        title = item.get("title", "")
        if any(pattern == source_path for pattern in GC_BLOCKED_SOURCE_PATTERNS):
            removed_records += 1
            continue
        if "canonical record" in title.lower():
            removed_records += 1
            continue
        cleaned.append(item)

    with JSONL_PATH.open("w", encoding="utf-8") as fh:
        for item in cleaned:
            fh.write(json.dumps(item, ensure_ascii=False) + "\n")

    return {
        "removed_files": removed_files,
        "removed_file_count": len(removed_files),
        "removed_record_count": removed_records,
        "remaining_records": len(cleaned),
    }


def load_mem0_sync_state() -> Dict[str, Any]:
    return load_json(MEM0_SYNC_STATE_PATH, {
        "last_synced_index": 0,
        "last_synced_ids": [],
        "last_synced_at": None,
        "last_status": "never",
        "last_error": None,
    })


def write_mem0_sync_state(state: Dict[str, Any]) -> None:
    MEM0_SYNC_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def mem0_sync(limit: int = MEM0_DEFAULT_QUERY_LIMIT, force: bool = False) -> Dict[str, Any]:
    ensure_dirs()
    state = load_mem0_sync_state()
    records = load_records()
    eligible = [
        record for record in records
        if record.get("type") in MEM0_ALLOWED_TYPES
        and float(record.get("importance", 0.0)) >= MEM0_MIN_IMPORTANCE
        and record.get("status", "active") == "active"
        and record.get("sensitivity", "internal") in {"public", "internal"}
        and record.get("source_kind") == "structured-memory"
    ]

    start_index = 0 if force else int(state.get("last_synced_index", 0))
    delta = eligible[start_index:]
    synced = []
    skipped = []

    for record in delta:
        memory_text = f"[{record.get('type')}] {record.get('title')}: {record.get('summary')}"
        cmd = [
            "openclaw", "mem0", "store", memory_text,
            "--metadata", json.dumps({
                "source_path": record.get("source_path", ""),
                "importance": record.get("importance", 0.0),
                "source_kind": record.get("source_kind", "structured-memory"),
                "project": record.get("project", "memory-system"),
                "content_hash": record.get("content_hash", ""),
            }, ensure_ascii=False),
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode == 0:
                synced.append(record.get("id"))
            else:
                skipped.append({"id": record.get("id"), "error": result.stderr.strip() or result.stdout.strip()})
        except Exception as exc:
            skipped.append({"id": record.get("id"), "error": str(exc)})

    state["last_synced_index"] = start_index + len(delta)
    state["last_synced_ids"] = synced[-20:]
    state["last_synced_at"] = utc_now()
    state["last_status"] = "ok" if not skipped else "partial"
    state["last_error"] = skipped[:5] if skipped else None
    write_mem0_sync_state(state)

    return {
        "eligible": len(eligible),
        "attempted": len(delta),
        "synced": len(synced),
        "skipped": skipped[:10],
        "incremental": not force,
        "start_index": start_index,
        "end_index": start_index + len(delta),
        "allowed_types": sorted(MEM0_ALLOWED_TYPES),
    }


def remote_sync_multi(
    remote_url: str = DEFAULT_REMOTE_URL,
    collections: List[str] | None = None,
    force: bool = False,
) -> Dict[str, Any]:
    targets = collections or ["conversation-index", "openclaw_memory", "openclaw_memory_compacted"]
    results = []
    ok = True
    for name in targets:
        result = remote_sync(remote_url=remote_url, collection=name, force=force)
        results.append(result)
        if not result.get("ok"):
            ok = False
    return {
        "ok": ok,
        "remote_url": remote_url,
        "collections": targets,
        "results": results,
    }


def print_stats() -> int:
    print(json.dumps(compute_stats(), ensure_ascii=False, indent=2))
    return 0


def optimize(paths: List[Path], remote_enabled: bool = False) -> int:
    result = ingest(paths, remote_enabled=remote_enabled)
    stats = compute_stats()
    print(json.dumps({**result, "stats": stats, "quality_guard": {"derived_files_indexed": False, "raw_transcripts_default": False, "structured_extraction": True, "incremental_sync": True, "hybrid_retrieval": True, "gc_policy_enabled": True, "retrieval_benchmark_enabled": True}}, ensure_ascii=False, indent=2))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="低 Token 記憶管線")
    sub = parser.add_subparsers(dest="cmd", required=True)

    ingest_p = sub.add_parser("ingest", help="將 markdown 匯入壓縮記憶")
    ingest_p.add_argument("paths", nargs="*", default=[str(MEMORY_DIR)])
    ingest_p.add_argument("--remote-enabled", action="store_true")

    optimize_p = sub.add_parser("optimize", help="執行壓縮記憶優化並輸出統計")
    optimize_p.add_argument("paths", nargs="*", default=[str(MEMORY_DIR)])
    optimize_p.add_argument("--remote-enabled", action="store_true")

    sync_p = sub.add_parser("sync-remote", help="將安全記憶同步到遠端副本")
    sync_p.add_argument("--url", default=DEFAULT_REMOTE_URL)
    sync_p.add_argument("--collection", default=DEFAULT_REMOTE_COLLECTION)
    sync_p.add_argument("--force", action="store_true")

    sync_multi_p = sub.add_parser("sync-remote-multi", help="同步到多個遠端 collections")
    sync_multi_p.add_argument("--url", default=DEFAULT_REMOTE_URL)
    sync_multi_p.add_argument("--collections", nargs="*", default=["conversation-index", "openclaw_memory", "openclaw_memory_compacted"])
    sync_multi_p.add_argument("--force", action="store_true")

    report_p = sub.add_parser("report", help="產生日報表")
    report_p.add_argument("--print", action="store_true")

    hybrid_p = sub.add_parser("hybrid-search", help="執行本地+遠端混合檢索")
    hybrid_p.add_argument("query")
    hybrid_p.add_argument("--limit", type=int, default=HYBRID_DEFAULT_LIMIT)
    hybrid_p.add_argument("--url", default=DEFAULT_REMOTE_URL)
    hybrid_p.add_argument("--collection", default=DEFAULT_REMOTE_COLLECTION)

    hybrid_fb_p = sub.add_parser("hybrid-search-fallback", help="優先查 compacted/openclaw/conversation 三層 fallback")
    hybrid_fb_p.add_argument("query")
    hybrid_fb_p.add_argument("--limit", type=int, default=HYBRID_DEFAULT_LIMIT)
    hybrid_fb_p.add_argument("--url", default=DEFAULT_REMOTE_URL)
    hybrid_fb_p.add_argument("--collections", nargs="*", default=["openclaw_memory_compacted", "openclaw_memory", "conversation-index"])

    validate_p = sub.add_parser("validate-remote", help="驗證中央向量資料庫連線與 collection 狀態")
    validate_p.add_argument("--url", default=DEFAULT_REMOTE_URL)
    validate_p.add_argument("--collection", default=DEFAULT_REMOTE_COLLECTION)

    benchmark_p = sub.add_parser("benchmark", help="產生混合檢索基準報表")
    benchmark_p.add_argument("--limit", type=int, default=BENCHMARK_DEFAULT_LIMIT)
    benchmark_p.add_argument("--url", default=DEFAULT_REMOTE_URL)
    benchmark_p.add_argument("--collection", default=DEFAULT_REMOTE_COLLECTION)

    mem0_p = sub.add_parser("sync-mem0", help="將白名單 structured memory 同步到 Mem0")
    mem0_p.add_argument("--limit", type=int, default=MEM0_DEFAULT_QUERY_LIMIT)
    mem0_p.add_argument("--force", action="store_true")

    sub.add_parser("gc", help="執行污染記憶自動清理")
    sub.add_parser("stats", help="輸出記憶統計")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.cmd == "stats":
        return print_stats()
    if args.cmd == "report":
        report = generate_report()
        payload = {"report": str(report.relative_to(ROOT))}
        if args.print:
            payload["content"] = report.read_text(encoding="utf-8")
        print(json.dumps(payload, ensure_ascii=False))
        return 0
    if args.cmd == "benchmark":
        report = run_benchmark(limit=args.limit, remote_url=args.url, collection=args.collection)
        print(json.dumps({"report": str(report.relative_to(ROOT)), "content": report.read_text(encoding="utf-8")}, ensure_ascii=False))
        return 0
    if args.cmd == "validate-remote":
        result = remote_healthcheck(remote_url=args.url, collection=args.collection)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 2
    if args.cmd == "gc":
        result = gc_cleanup()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "sync-mem0":
        result = mem0_sync(limit=args.limit, force=args.force)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if not result.get("skipped") else 2
    if args.cmd == "ingest":
        print(json.dumps(ingest([Path(p) for p in args.paths], remote_enabled=args.remote_enabled), ensure_ascii=False))
        return 0
    if args.cmd == "optimize":
        return optimize([Path(p) for p in args.paths], remote_enabled=args.remote_enabled)
    if args.cmd == "sync-remote":
        result = remote_sync(args.url, args.collection, args.force)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 2
    if args.cmd == "sync-remote-multi":
        result = remote_sync_multi(remote_url=args.url, collections=args.collections, force=args.force)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 2
    if args.cmd == "hybrid-search":
        result = hybrid_search(args.query, limit=args.limit, remote_url=args.url, collection=args.collection)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "hybrid-search-fallback":
        result = hybrid_search_fallback(args.query, limit=args.limit, remote_url=args.url, collections=args.collections)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
