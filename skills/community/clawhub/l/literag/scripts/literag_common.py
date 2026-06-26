#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import math
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ALL_COMPLETED, FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Sequence

try:
    import sqlite_vec as _sqlite_vec_module
except Exception:
    _sqlite_vec_module = None

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$", re.MULTILINE)
WHITESPACE_RE = re.compile(r"\s+")
WORKSPACE_SENTINELS = ("AGENTS.md", "SOUL.md", "USER.md", "MEMORY.md")
DEFAULT_CONFIG_RELATIVE_PATH = Path(".literag/knowledge-libs.json")
SQLITE_VEC_TABLE = "chunk_vec"


@dataclass
class LibraryConfig:
    id: str
    name: str
    sqlite_path: Path
    paths: list[dict]
    chunk_max_chars: int | None = None
    chunk_overlap_chars: int | None = None
    chunk_min_chars: int | None = None
    prefer_headings: bool | None = None
    vector_top_k: int | None = None
    hybrid_fts_weight: float | None = None
    hybrid_vector_weight: float | None = None
    hybrid_rrf_k: int | None = None
    ranking_references_penalty: float | None = None
    ranking_navigation_penalty: float | None = None
    ranking_table_penalty: float | None = None
    ranking_heading_term_boost: float | None = None
    ranking_text_term_boost: float | None = None


@dataclass
class AppConfig:
    root: Path
    workspace_root: Path
    chunk_max_chars: int
    chunk_overlap_chars: int
    chunk_min_chars: int
    prefer_headings: bool
    fts_enabled: bool
    vector_enabled: bool
    vector_top_k: int
    hybrid_enabled: bool
    hybrid_fts_weight: float
    hybrid_vector_weight: float
    hybrid_rrf_k: int
    ranking_references_penalty: float
    ranking_navigation_penalty: float
    ranking_table_penalty: float
    ranking_heading_term_boost: float
    ranking_text_term_boost: float
    embedding_base_url: str
    embedding_api_key: str | None
    embedding_model: str
    embedding_timeout_ms: int
    embedding_batch_size: int
    embedding_max_concurrency: int
    embedding_max_retries: int
    embedding_retry_backoff_ms: int
    libraries: list[LibraryConfig]


def detect_workspace_root(start: str | Path | None = None) -> Path:
    candidates: list[Path] = []
    env_workspace = os.environ.get("OPENCLAW_WORKSPACE") or os.environ.get("WORKSPACE")
    if env_workspace:
        candidates.append(Path(env_workspace).expanduser())
    if start is not None:
        candidates.append(Path(start).expanduser())
    candidates.extend([Path.cwd(), Path(__file__).resolve()])

    seen: set[Path] = set()
    for candidate in candidates:
        current = candidate.resolve()
        if current.is_file():
            current = current.parent
        for probe in (current, *current.parents):
            if probe in seen:
                continue
            seen.add(probe)
            if all((probe / marker).exists() for marker in WORKSPACE_SENTINELS):
                return probe
    raise SystemExit(
        "could not detect OpenClaw workspace root; set OPENCLAW_WORKSPACE or run inside the workspace"
    )


def default_config_path() -> Path:
    return detect_workspace_root() / DEFAULT_CONFIG_RELATIVE_PATH


def resolve_path(value: str | Path, *, base_dir: Path) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (base_dir / path).resolve()


def default_sqlite_path(workspace_root: Path, library_id: str) -> Path:
    return workspace_root / ".literag" / f"{library_id}.sqlite"


def load_config(config_path: str | Path) -> AppConfig:
    config_path = Path(config_path).expanduser().resolve()
    workspace_root = detect_workspace_root(config_path)
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    defaults = raw.get("defaults", {})
    chunking = defaults.get("chunking", {})
    retrieval = defaults.get("retrieval", {})
    fts = retrieval.get("fts", {})
    vector = retrieval.get("vector", {})
    hybrid = retrieval.get("hybrid", {})
    ranking = defaults.get("ranking", raw.get("ranking", {}))
    embedding = raw.get("embedding", {})

    libraries = []
    for lib in raw.get("libraries", []):
        lib_chunking = lib.get("chunking", {})
        lib_retrieval = lib.get("retrieval", {})
        lib_vector = lib_retrieval.get("vector", {})
        lib_hybrid = lib_retrieval.get("hybrid", {})
        lib_ranking = lib.get("ranking", {})
        source_paths = []
        for source in lib.get("paths", []):
            source_paths.append(
                {
                    "path": str(resolve_path(source["path"], base_dir=config_path.parent)),
                    "include": source.get("include") or ["**/*"],
                    "exclude": source.get("exclude") or [],
                }
            )
        libraries.append(
            LibraryConfig(
                id=lib["id"],
                name=lib.get("name", lib["id"]),
                sqlite_path=resolve_path(lib.get("sqlitePath") or default_sqlite_path(workspace_root, lib["id"]), base_dir=config_path.parent),
                paths=source_paths,
                chunk_max_chars=int(lib_chunking["maxChars"]) if "maxChars" in lib_chunking else None,
                chunk_overlap_chars=int(lib_chunking["overlapChars"]) if "overlapChars" in lib_chunking else None,
                chunk_min_chars=int(lib_chunking["minChars"]) if "minChars" in lib_chunking else None,
                prefer_headings=bool(lib_chunking["preferHeadings"]) if "preferHeadings" in lib_chunking else None,
                vector_top_k=int(lib_vector["topK"]) if "topK" in lib_vector else None,
                hybrid_fts_weight=float(lib_hybrid["ftsWeight"]) if "ftsWeight" in lib_hybrid else None,
                hybrid_vector_weight=float(lib_hybrid["vectorWeight"]) if "vectorWeight" in lib_hybrid else None,
                hybrid_rrf_k=int(lib_hybrid["rrfK"]) if "rrfK" in lib_hybrid else None,
                ranking_references_penalty=float(lib_ranking["referencesPenalty"]) if "referencesPenalty" in lib_ranking else None,
                ranking_navigation_penalty=float(lib_ranking["navigationPenalty"]) if "navigationPenalty" in lib_ranking else None,
                ranking_table_penalty=float(lib_ranking["tablePenalty"]) if "tablePenalty" in lib_ranking else None,
                ranking_heading_term_boost=float(lib_ranking["headingTermBoost"]) if "headingTermBoost" in lib_ranking else None,
                ranking_text_term_boost=float(lib_ranking["textTermBoost"]) if "textTermBoost" in lib_ranking else None,
            )
        )

    return AppConfig(
        root=config_path.parent,
        workspace_root=workspace_root,
        chunk_max_chars=int(chunking.get("maxChars", 2200)),
        chunk_overlap_chars=int(chunking.get("overlapChars", 250)),
        chunk_min_chars=int(chunking.get("minChars", 180)),
        prefer_headings=bool(chunking.get("preferHeadings", True)),
        fts_enabled=bool(fts.get("enabled", True)),
        vector_enabled=bool(vector.get("enabled", True)),
        vector_top_k=int(vector.get("topK", 24)),
        hybrid_enabled=bool(hybrid.get("enabled", True)),
        hybrid_fts_weight=float(hybrid.get("ftsWeight", 0.4)),
        hybrid_vector_weight=float(hybrid.get("vectorWeight", 0.6)),
        hybrid_rrf_k=int(hybrid.get("rrfK", 60)),
        ranking_references_penalty=float(ranking.get("referencesPenalty", 0.18)),
        ranking_navigation_penalty=float(ranking.get("navigationPenalty", 0.12)),
        ranking_table_penalty=float(ranking.get("tablePenalty", 0.08)),
        ranking_heading_term_boost=float(ranking.get("headingTermBoost", 0.03)),
        ranking_text_term_boost=float(ranking.get("textTermBoost", 0.01)),
        embedding_base_url=str(embedding.get("baseUrl", "http://localhost:11434/v1/")).rstrip("/"),
        embedding_api_key=embedding.get("apiKey"),
        embedding_model=str(embedding.get("model")),
        embedding_timeout_ms=int(embedding.get("timeoutMs", 120000)),
        embedding_batch_size=max(1, int(embedding.get("batchSize", 16))),
        embedding_max_concurrency=max(1, int(embedding.get("maxConcurrency", 1))),
        embedding_max_retries=max(0, int(embedding.get("maxRetries", 2))),
        embedding_retry_backoff_ms=max(0, int(embedding.get("retryBackoffMs", 750))),
        libraries=libraries,
    )


def find_library(config: AppConfig, library_id: str) -> LibraryConfig:
    for lib in config.libraries:
        if lib.id == library_id:
            return lib
    raise SystemExit(f"unknown library: {library_id}")


def matches_globs(rel_path: str, patterns: Sequence[str]) -> bool:
    for pattern in patterns:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
        if pattern.startswith("**/") and fnmatch.fnmatch(rel_path, pattern[3:]):
            return True
    return False


def iter_library_files(library: LibraryConfig) -> Iterator[Path]:
    seen: set[Path] = set()
    for source in library.paths:
        root = Path(source["path"]).expanduser()
        include = source.get("include") or ["**/*"]
        exclude = source.get("exclude") or []
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if not matches_globs(rel, include):
                continue
            if exclude and matches_globs(rel, exclude):
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield resolved


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def normalize_text(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def extract_query_terms(query: str) -> list[str]:
    seen: set[str] = set()
    terms: list[str] = []
    for term in re.findall(r"[a-zA-Z0-9_]{2,}", query.lower()):
        if term in seen:
            continue
        seen.add(term)
        terms.append(term)
    return terms


def build_fts_match_query(query: str) -> str:
    terms = extract_query_terms(query)
    if not terms:
        normalized = normalize_text(query)
        if not normalized:
            return '""'
        escaped = normalized.replace('"', ' ')
        return f'"{escaped}"'
    return " AND ".join(f'"{term}"' for term in terms)


def effective_chunk_max_chars(config: AppConfig, library: LibraryConfig) -> int:
    return library.chunk_max_chars if library.chunk_max_chars is not None else config.chunk_max_chars


def effective_chunk_overlap_chars(config: AppConfig, library: LibraryConfig) -> int:
    return library.chunk_overlap_chars if library.chunk_overlap_chars is not None else config.chunk_overlap_chars


def effective_chunk_min_chars(config: AppConfig, library: LibraryConfig) -> int:
    return library.chunk_min_chars if library.chunk_min_chars is not None else config.chunk_min_chars


def effective_prefer_headings(config: AppConfig, library: LibraryConfig) -> bool:
    return library.prefer_headings if library.prefer_headings is not None else config.prefer_headings


def effective_vector_top_k(config: AppConfig, library: LibraryConfig) -> int:
    return library.vector_top_k if library.vector_top_k is not None else config.vector_top_k


def effective_hybrid_fts_weight(config: AppConfig, library: LibraryConfig) -> float:
    return library.hybrid_fts_weight if library.hybrid_fts_weight is not None else config.hybrid_fts_weight


def effective_hybrid_vector_weight(config: AppConfig, library: LibraryConfig) -> float:
    return library.hybrid_vector_weight if library.hybrid_vector_weight is not None else config.hybrid_vector_weight


def effective_hybrid_rrf_k(config: AppConfig, library: LibraryConfig) -> int:
    return library.hybrid_rrf_k if library.hybrid_rrf_k is not None else config.hybrid_rrf_k


def rerank_adjustment(config: AppConfig, library: LibraryConfig, query: str, heading: str, text: str) -> float:
    heading_norm = normalize_text(heading).lower()
    text_norm = normalize_text(text).lower()
    adjustment = 0.0
    references_penalty = library.ranking_references_penalty if library.ranking_references_penalty is not None else config.ranking_references_penalty
    navigation_penalty = library.ranking_navigation_penalty if library.ranking_navigation_penalty is not None else config.ranking_navigation_penalty
    table_penalty = library.ranking_table_penalty if library.ranking_table_penalty is not None else config.ranking_table_penalty
    heading_term_boost = library.ranking_heading_term_boost if library.ranking_heading_term_boost is not None else config.ranking_heading_term_boost
    text_term_boost = library.ranking_text_term_boost if library.ranking_text_term_boost is not None else config.ranking_text_term_boost
    if heading_norm == "references":
        adjustment -= references_penalty
    elif heading_norm in {"see also", "related", "navigation", "links"}:
        adjustment -= navigation_penalty
    if "| --- | --- |" in text or text_norm.startswith("## references | | | | --- | --- |"):
        adjustment -= table_penalty
    query_terms = extract_query_terms(query)
    if query_terms:
        heading_hits = sum(1 for term in query_terms if term in heading_norm)
        text_hits = sum(1 for term in query_terms if term in text_norm)
        adjustment += heading_hits * heading_term_boost
        adjustment += min(text_hits, 3) * text_term_boost
    return adjustment


def sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()


def split_sections(text: str) -> list[tuple[str, str]]:
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        cleaned = text.strip()
        return [("", cleaned)] if cleaned else []
    sections: list[tuple[str, str]] = []
    for idx, match in enumerate(matches):
        heading = match.group(2).strip()
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        section_text = text[start:end].strip()
        if section_text:
            sections.append((heading, section_text))
    prefix = text[: matches[0].start()].strip()
    if prefix:
        sections.insert(0, ("", prefix))
    return sections


def chunk_text(
    text: str,
    max_chars: int,
    overlap_chars: int,
    prefer_headings: bool = True,
    min_chars: int = 180,
) -> list[tuple[str, str]]:
    sections = split_sections(text) if prefer_headings else [("", text.strip())]
    chunks: list[tuple[str, str]] = []
    for heading, section_text in sections:
        cleaned = section_text.strip()
        if not cleaned:
            continue
        if len(cleaned) <= max_chars:
            chunks.append((heading, cleaned))
            continue
        start = 0
        while start < len(cleaned):
            end = min(len(cleaned), start + max_chars)
            if end < len(cleaned):
                boundary = cleaned.rfind("\n", start, end)
                if boundary > start + max_chars // 2:
                    end = boundary
                else:
                    boundary = cleaned.rfind(" ", start, end)
                    if boundary > start + max_chars // 2:
                        end = boundary
            piece = cleaned[start:end].strip()
            if piece:
                if chunks and len(normalize_text(piece)) < min_chars:
                    prev_heading, prev_piece = chunks[-1]
                    if prev_heading == heading or not heading:
                        chunks[-1] = (prev_heading, f"{prev_piece}\n\n{piece}".strip())
                    else:
                        chunks.append((heading, piece))
                else:
                    chunks.append((heading, piece))
            if end >= len(cleaned):
                break
            start = max(0, end - overlap_chars)
    return chunks


def sqlite_vec_available(conn: sqlite3.Connection | None = None) -> bool:
    if _sqlite_vec_module is None:
        return False
    if conn is None:
        return True
    return hasattr(conn, "enable_load_extension") and hasattr(conn, "load_extension")


def load_sqlite_vec(conn: sqlite3.Connection) -> bool:
    if not sqlite_vec_available(conn):
        return False
    try:
        conn.enable_load_extension(True)
        _sqlite_vec_module.load(conn)
        conn.enable_load_extension(False)
        return True
    except Exception:
        try:
            conn.enable_load_extension(False)
        except Exception:
            pass
        return False


def vector_backend_name(conn: sqlite3.Connection | None = None) -> str:
    return "sqlite-vec" if sqlite_vec_available(conn) else "python-scan"


def connect_db(sqlite_path: Path) -> sqlite3.Connection:
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA temp_store=MEMORY")
    load_sqlite_vec(conn)
    return conn


def ensure_sqlite_vec_table(conn: sqlite3.Connection, dimension: int) -> bool:
    if not sqlite_vec_available(conn) or dimension <= 0:
        return False
    existing_dimension = get_meta(conn, "vector_dimensions")
    if existing_dimension and int(existing_dimension) != int(dimension):
        conn.execute(f"DROP TABLE IF EXISTS {SQLITE_VEC_TABLE}")
    conn.execute(
        f"CREATE VIRTUAL TABLE IF NOT EXISTS {SQLITE_VEC_TABLE} USING vec0(chunk_id INTEGER PRIMARY KEY, embedding FLOAT[{int(dimension)}])"
    )
    return True


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            path TEXT NOT NULL UNIQUE,
            mtime REAL NOT NULL,
            size INTEGER NOT NULL,
            sha1 TEXT NOT NULL,
            indexed_at REAL NOT NULL,
            chunking_fingerprint TEXT,
            embedding_fingerprint TEXT
        );

        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            document_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            heading TEXT NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE CASCADE,
            UNIQUE(document_id, chunk_index)
        );

        CREATE TABLE IF NOT EXISTS embeddings (
            chunk_id INTEGER PRIMARY KEY,
            vector TEXT NOT NULL,
            FOREIGN KEY(chunk_id) REFERENCES chunks(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);
        """
    )
    document_columns = {str(row[1]) for row in conn.execute("PRAGMA table_info(documents)").fetchall()}
    if "chunking_fingerprint" not in document_columns:
        conn.execute("ALTER TABLE documents ADD COLUMN chunking_fingerprint TEXT")
    if "embedding_fingerprint" not in document_columns:
        conn.execute("ALTER TABLE documents ADD COLUMN embedding_fingerprint TEXT")
    existing_fts = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'chunks_fts'"
    ).fetchone()
    existing_fts_sql = existing_fts[0] if existing_fts else None
    dropped_fts = False
    if existing_fts_sql and "content=''" in existing_fts_sql.replace(' ', '').lower():
        conn.execute("DROP TABLE IF EXISTS chunks_fts")
        dropped_fts = True
    conn.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
            heading,
            text,
            path UNINDEXED,
            tokenize='unicode61'
        )
        """
    )
    chunk_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    fts_count = conn.execute("SELECT COUNT(*) FROM chunks_fts").fetchone()[0]
    if dropped_fts or fts_count != chunk_count:
        conn.execute("DELETE FROM chunks_fts")
        conn.executemany(
            "INSERT INTO chunks_fts(rowid, heading, text, path) VALUES (?, ?, ?, ?)",
            conn.execute(
                "SELECT c.id, c.heading, c.text, d.path FROM chunks c JOIN documents d ON d.id = c.document_id ORDER BY c.id"
            ).fetchall(),
        )
    conn.commit()


def delete_document_rows(conn: sqlite3.Connection, document_id: int) -> None:
    chunk_ids = [row[0] for row in conn.execute("SELECT id FROM chunks WHERE document_id = ?", (document_id,))]
    if chunk_ids:
        conn.executemany("DELETE FROM embeddings WHERE chunk_id = ?", ((chunk_id,) for chunk_id in chunk_ids))
        conn.executemany("DELETE FROM chunks_fts WHERE rowid = ?", ((chunk_id,) for chunk_id in chunk_ids))
        if conn.execute("SELECT 1 FROM sqlite_master WHERE name = ? LIMIT 1", (SQLITE_VEC_TABLE,)).fetchone():
            conn.executemany(f"DELETE FROM {SQLITE_VEC_TABLE} WHERE chunk_id = ?", ((chunk_id,) for chunk_id in chunk_ids))
    conn.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
    conn.execute("DELETE FROM documents WHERE id = ?", (document_id,))


def set_meta(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO meta(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value),
    )


def get_meta(conn: sqlite3.Connection, key: str) -> str | None:
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    if not row:
        return None
    return str(row[0])


def current_embedding_fingerprint(config: AppConfig) -> str:
    payload = {
        "base_url": config.embedding_base_url,
        "model": config.embedding_model,
        "vector_enabled": config.vector_enabled,
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def current_chunking_fingerprint(config: AppConfig, library: LibraryConfig) -> str:
    payload = {
        "max_chars": effective_chunk_max_chars(config, library),
        "overlap_chars": effective_chunk_overlap_chars(config, library),
        "min_chars": effective_chunk_min_chars(config, library),
        "prefer_headings": effective_prefer_headings(config, library),
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def current_index_config_fingerprint(config: AppConfig, library: LibraryConfig) -> str:
    payload = {
        "library_id": library.id,
        "paths": [
            {
                "path": str(entry.get("path") or ""),
                "include": list(entry.get("include") or []),
                "exclude": list(entry.get("exclude") or []),
            }
            for entry in library.paths
        ],
        "chunking": json.loads(current_chunking_fingerprint(config, library)),
        "retrieval": {
            "vector_top_k": effective_vector_top_k(config, library),
            "hybrid_fts_weight": effective_hybrid_fts_weight(config, library),
            "hybrid_vector_weight": effective_hybrid_vector_weight(config, library),
            "hybrid_rrf_k": effective_hybrid_rrf_k(config, library),
        },
        "ranking": {
            "references_penalty": library.ranking_references_penalty if library.ranking_references_penalty is not None else config.ranking_references_penalty,
            "navigation_penalty": library.ranking_navigation_penalty if library.ranking_navigation_penalty is not None else config.ranking_navigation_penalty,
            "table_penalty": library.ranking_table_penalty if library.ranking_table_penalty is not None else config.ranking_table_penalty,
            "heading_term_boost": library.ranking_heading_term_boost if library.ranking_heading_term_boost is not None else config.ranking_heading_term_boost,
            "text_term_boost": library.ranking_text_term_boost if library.ranking_text_term_boost is not None else config.ranking_text_term_boost,
        },
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def embedding_mismatch_warning(conn: sqlite3.Connection, config: AppConfig) -> str | None:
    indexed_model = get_meta(conn, "embedding_model")
    indexed_fingerprint = get_meta(conn, "embedding_fingerprint")
    if not indexed_model and not indexed_fingerprint:
        return None
    warnings: list[str] = []
    if indexed_model and indexed_model != config.embedding_model:
        warnings.append(f"embedding model mismatch: indexed={indexed_model} current={config.embedding_model}")
    current_fingerprint = current_embedding_fingerprint(config)
    if indexed_fingerprint and indexed_fingerprint != current_fingerprint:
        warnings.append("embedding config fingerprint changed; reindex recommended")
    if not warnings:
        return None
    return "; ".join(warnings)


def get_library_warning(config: AppConfig, library: LibraryConfig) -> str | None:
    conn = connect_db(library.sqlite_path)
    try:
        init_db(conn)
        warnings: list[str] = []
        embedding_warning = embedding_mismatch_warning(conn, config)
        if embedding_warning:
            warnings.append(embedding_warning)
        indexed_index_config_fingerprint = get_meta(conn, "index_config_fingerprint")
        current_index_fingerprint = current_index_config_fingerprint(config, library)
        if indexed_index_config_fingerprint and indexed_index_config_fingerprint != current_index_fingerprint:
            warnings.append("index config changed (paths/chunking/retrieval/ranking); reindex recommended")
        if not warnings:
            return None
        return "; ".join(warnings)
    finally:
        conn.close()


def is_retryable_embedding_error(err: Exception) -> bool:
    if isinstance(err, urllib.error.HTTPError):
        return err.code in {408, 409, 425, 429, 500, 502, 503, 504}
    if isinstance(err, urllib.error.URLError):
        return True
    if isinstance(err, TimeoutError):
        return True
    reason = getattr(err, "reason", None)
    return isinstance(reason, TimeoutError)


def request_embeddings(config: AppConfig, texts: Sequence[str]) -> list[list[float]]:
    if not texts:
        return []
    payload = json.dumps({"model": config.embedding_model, "input": list(texts)}).encode("utf-8")
    req = urllib.request.Request(
        url=f"{config.embedding_base_url}/embeddings",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.embedding_api_key or 'local-noauth'}",
        },
        method="POST",
    )
    timeout = max(1, config.embedding_timeout_ms / 1000)
    attempts = max(1, config.embedding_max_retries + 1)
    last_err: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
            items = data.get("data", [])
            vectors = [item["embedding"] for item in items]
            if len(vectors) != len(texts):
                raise RuntimeError(f"embedding count mismatch: expected {len(texts)} got {len(vectors)}")
            return vectors
        except Exception as err:
            last_err = err
            if attempt >= attempts or not is_retryable_embedding_error(err):
                raise
            backoff_s = (config.embedding_retry_backoff_ms / 1000.0) * attempt
            if backoff_s > 0:
                time.sleep(backoff_s)
    if last_err is not None:
        raise last_err
    return []


def build_embedding_input(row: sqlite3.Row) -> str:
    return f"{row['heading']}\n\n{row['text']}" if row["heading"] else str(row["text"])


def flush_embedding_futures(
    conn: sqlite3.Connection,
    futures: list[Future[tuple[list[sqlite3.Row], list[list[float]]]]],
    *,
    wait_for_all: bool,
) -> tuple[int, str | None, int | None]:
    if not futures:
        return 0, None, None
    done, pending = wait(futures, return_when=ALL_COMPLETED if wait_for_all else FIRST_COMPLETED)
    for future in done:
        futures.remove(future)
    embeddings_indexed = 0
    active_vector_backend: str | None = None
    vector_dimensions: int | None = None
    for future in done:
        inserted, vectors = future.result()
        if not vectors:
            continue
        vector_dimensions = len(vectors[0])
        active_vector_backend = upsert_embedding_rows(conn, vectors, inserted)
        embeddings_indexed += len(vectors)
    if embeddings_indexed:
        conn.commit()
    return embeddings_indexed, active_vector_backend, vector_dimensions


def batch_iter(items: Sequence[str], batch_size: int) -> Iterator[Sequence[str]]:
    for idx in range(0, len(items), batch_size):
        yield items[idx : idx + batch_size]


def upsert_embedding_rows(conn: sqlite3.Connection, vectors: Sequence[Sequence[float]], inserted: Sequence[sqlite3.Row]) -> str:
    if not vectors or not inserted:
        return "python-scan"
    conn.executemany(
        "INSERT OR REPLACE INTO embeddings(chunk_id, vector) VALUES (?, ?)",
        ((int(row["id"]), json.dumps(vector)) for row, vector in zip(inserted, vectors)),
    )
    if sqlite_vec_available(conn) and ensure_sqlite_vec_table(conn, len(vectors[0])):
        conn.executemany(
            f"INSERT OR REPLACE INTO {SQLITE_VEC_TABLE}(chunk_id, embedding) VALUES (?, ?)",
            ((int(row["id"]), _sqlite_vec_module.serialize_float32(vector)) for row, vector in zip(inserted, vectors)),
        )
        return "sqlite-vec"
    return "python-scan"


def upsert_document(
    conn: sqlite3.Connection,
    path: Path,
    text: str,
    *,
    chunking_fingerprint: str,
    embedding_fingerprint: str,
) -> tuple[int, bool, str]:
    stat = path.stat()
    sha1 = sha1_text(text)
    existing = conn.execute(
        "SELECT id, mtime, size, sha1, chunking_fingerprint, embedding_fingerprint FROM documents WHERE path = ?",
        (str(path),),
    ).fetchone()
    if existing:
        unchanged_content = (
            float(existing["mtime"]) == stat.st_mtime
            and int(existing["size"]) == stat.st_size
            and str(existing["sha1"]) == sha1
        )
        unchanged_index_shape = (
            str(existing["chunking_fingerprint"] or "") == chunking_fingerprint
            and str(existing["embedding_fingerprint"] or "") == embedding_fingerprint
        )
        if unchanged_content and unchanged_index_shape:
            return int(existing["id"]), False, "unchanged"
        document_id = int(existing["id"])
        reason = "content" if not unchanged_content else "config"
        delete_document_rows(conn, document_id)
        conn.execute(
            "INSERT INTO documents(id, path, mtime, size, sha1, indexed_at, chunking_fingerprint, embedding_fingerprint) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (document_id, str(path), stat.st_mtime, stat.st_size, sha1, time.time(), chunking_fingerprint, embedding_fingerprint),
        )
        return document_id, True, reason
    cur = conn.execute(
        "INSERT INTO documents(path, mtime, size, sha1, indexed_at, chunking_fingerprint, embedding_fingerprint) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (str(path), stat.st_mtime, stat.st_size, sha1, time.time(), chunking_fingerprint, embedding_fingerprint),
    )
    return int(cur.lastrowid), True, "new"


def index_library(
    config: AppConfig,
    library: LibraryConfig,
    limit_files: int | None = None,
    batch_size: int = 16,
    embedding_batch_size: int | None = None,
    progress_callback: Callable[[dict], None] | None = None,
) -> dict:
    conn = connect_db(library.sqlite_path)
    try:
        init_db(conn)
        set_meta(conn, "schema_version", "3")
        set_meta(conn, "embedding_model", config.embedding_model)
        set_meta(conn, "embedding_base_url", config.embedding_base_url)
        set_meta(conn, "embedding_fingerprint", current_embedding_fingerprint(config))
        set_meta(conn, "index_config_fingerprint", current_index_config_fingerprint(config, library))
        set_meta(conn, "vector_backend_runtime", vector_backend_name(conn))
        set_meta(conn, "last_indexed_at", str(int(time.time())))
        conn.commit()
        current_paths = []
        chunking_fingerprint = current_chunking_fingerprint(config, library)
        embedding_fingerprint = current_embedding_fingerprint(config)
        files = list(iter_library_files(library))
        if limit_files is not None:
            files = files[:limit_files]
        for path in files:
            current_paths.append(str(path))

        stale_paths: list[str] = []
        if limit_files is None:
            existing_paths = {row[0] for row in conn.execute("SELECT path FROM documents")}
            stale_paths = sorted(existing_paths - set(current_paths))
            for stale in stale_paths:
                row = conn.execute("SELECT id FROM documents WHERE path = ?", (stale,)).fetchone()
                if row:
                    delete_document_rows(conn, int(row[0]))

        docs_indexed = 0
        docs_reindexed_content = 0
        docs_reindexed_config = 0
        docs_indexed_new = 0
        chunks_indexed = 0
        embeds_indexed = 0
        active_vector_backend = get_meta(conn, "vector_backend") or (vector_backend_name(conn) if config.vector_enabled else "disabled")
        existing_vector_dimensions = get_meta(conn, "vector_dimensions")
        vector_dimensions: int | None = int(existing_vector_dimensions) if existing_vector_dimensions else None
        total_files = len(files)
        max_workers = max(1, config.embedding_max_concurrency if config.vector_enabled else 1)
        effective_embedding_batch_size = max(1, embedding_batch_size or config.embedding_batch_size)
        pending_embedding_rows: list[sqlite3.Row] = []
        embedding_futures: list[Future[tuple[list[sqlite3.Row], list[list[float]]]]] = []
        embedding_future_sizes: dict[Future[tuple[list[sqlite3.Row], list[list[float]]]], int] = {}

        def submit_pending_rows(executor: ThreadPoolExecutor) -> None:
            nonlocal pending_embedding_rows
            while len(pending_embedding_rows) >= effective_embedding_batch_size:
                batch_rows = pending_embedding_rows[:effective_embedding_batch_size]
                pending_embedding_rows = pending_embedding_rows[effective_embedding_batch_size:]
                texts = [build_embedding_input(row) for row in batch_rows]
                future = executor.submit(lambda rows=batch_rows, values=texts: (rows, request_embeddings(config, values)))
                embedding_futures.append(future)
                embedding_future_sizes[future] = len(batch_rows)

        def flush_completed_embeddings(*, wait_for_all: bool) -> None:
            nonlocal embeds_indexed, active_vector_backend, vector_dimensions
            completed = [future for future in embedding_futures if future.done()] if not wait_for_all else list(embedding_futures)
            added_embeddings, backend, dimensions = flush_embedding_futures(conn, embedding_futures, wait_for_all=wait_for_all)
            for future in completed:
                embedding_future_sizes.pop(future, None)
            embeds_indexed += added_embeddings
            if backend:
                active_vector_backend = backend
            if dimensions is not None:
                vector_dimensions = dimensions

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for file_index, path in enumerate(files, start=1):
                text = read_text_file(path)
                doc_id, changed, changed_reason = upsert_document(
                    conn,
                    path,
                    text,
                    chunking_fingerprint=chunking_fingerprint,
                    embedding_fingerprint=embedding_fingerprint,
                )
                if changed:
                    docs_indexed += 1
                    if changed_reason == "content":
                        docs_reindexed_content += 1
                    elif changed_reason == "config":
                        docs_reindexed_config += 1
                    elif changed_reason == "new":
                        docs_indexed_new += 1
                    chunks = chunk_text(
                        text,
                        max_chars=effective_chunk_max_chars(config, library),
                        overlap_chars=effective_chunk_overlap_chars(config, library),
                        prefer_headings=effective_prefer_headings(config, library),
                        min_chars=effective_chunk_min_chars(config, library),
                    )
                    rows = []
                    for idx, (heading, chunk) in enumerate(chunks):
                        rows.append((doc_id, idx, heading or "", chunk))
                    conn.executemany(
                        "INSERT INTO chunks(document_id, chunk_index, heading, text) VALUES (?, ?, ?, ?)",
                        rows,
                    )
                    inserted = conn.execute(
                        "SELECT id, heading, text FROM chunks WHERE document_id = ? ORDER BY chunk_index ASC",
                        (doc_id,),
                    ).fetchall()
                    conn.executemany(
                        "INSERT INTO chunks_fts(rowid, heading, text, path) VALUES (?, ?, ?, ?)",
                        ((int(row["id"]), str(row["heading"]), str(row["text"]), str(path)) for row in inserted),
                    )
                    chunks_indexed += len(inserted)
                    if config.vector_enabled and inserted:
                        pending_embedding_rows.extend(inserted)
                        submit_pending_rows(executor)
                        while len(embedding_futures) >= max_workers * 2:
                            flush_completed_embeddings(wait_for_all=False)
                    conn.commit()

                if progress_callback is not None:
                    inflight_batches = len(embedding_futures)
                    inflight_embeddings = sum(embedding_future_sizes.get(future, 0) for future in embedding_futures)
                    progress_callback(
                        {
                            "library": library.id,
                            "current": file_index,
                            "total": total_files,
                            "path": str(path),
                            "changed": changed,
                            "changed_reason": changed_reason,
                            "docs_reindexed": docs_indexed,
                            "docs_indexed_new": docs_indexed_new,
                            "docs_reindexed_content": docs_reindexed_content,
                            "docs_reindexed_config": docs_reindexed_config,
                            "chunks_indexed": chunks_indexed,
                            "embeddings_indexed": embeds_indexed,
                            "embeddings_buffered": len(pending_embedding_rows),
                            "embeddings_inflight": inflight_embeddings,
                            "embedding_batches_inflight": inflight_batches,
                            "embeddings_outstanding": len(pending_embedding_rows) + inflight_embeddings,
                        }
                    )

            if pending_embedding_rows:
                batch_rows = pending_embedding_rows[:]
                pending_embedding_rows = []
                texts = [build_embedding_input(row) for row in batch_rows]
                future = executor.submit(lambda rows=batch_rows, values=texts: (rows, request_embeddings(config, values)))
                embedding_futures.append(future)
                embedding_future_sizes[future] = len(batch_rows)
            flush_completed_embeddings(wait_for_all=True)

        total_docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        total_chunks = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        total_embeddings = conn.execute("SELECT COUNT(*) FROM embeddings").fetchone()[0]
        has_vec_table = bool(conn.execute("SELECT 1 FROM sqlite_master WHERE name = ? LIMIT 1", (SQLITE_VEC_TABLE,)).fetchone())
        if config.vector_enabled:
            active_vector_backend = "sqlite-vec" if has_vec_table else "python-scan"
        else:
            active_vector_backend = "disabled"
        set_meta(conn, "document_count", str(int(total_docs)))
        set_meta(conn, "chunk_count", str(int(total_chunks)))
        set_meta(conn, "embedding_count", str(int(total_embeddings)))
        set_meta(conn, "vector_backend", active_vector_backend)
        if vector_dimensions is not None:
            set_meta(conn, "vector_dimensions", str(int(vector_dimensions)))
        set_meta(conn, "last_indexed_at", str(int(time.time())))
        conn.commit()
        return {
            "library": library.id,
            "files_seen": len(files),
            "docs_reindexed": docs_indexed,
            "docs_indexed_new": docs_indexed_new,
            "docs_reindexed_content": docs_reindexed_content,
            "docs_reindexed_config": docs_reindexed_config,
            "chunks_indexed": chunks_indexed,
            "embeddings_indexed": embeds_indexed,
            "stale_removed": len(stale_paths),
            "total_docs": total_docs,
            "total_chunks": total_chunks,
            "total_embeddings": total_embeddings,
            "sqlite_path": str(library.sqlite_path),
            "incremental": True,
            "batch_size": batch_size,
            "embedding_batch_size": effective_embedding_batch_size,
            "vector_backend": active_vector_backend if config.vector_enabled else "disabled",
            "reindex_recommended": bool(get_library_warning(config, library)),
        }
    finally:
        conn.close()


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vector dimension mismatch")
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def fetch_document_chunks(
    library: LibraryConfig,
    *,
    path: str,
    start_chunk_index: int | None = None,
    end_chunk_index: int | None = None,
    chunk_ids: Sequence[int] | None = None,
) -> list[dict]:
    conn = connect_db(library.sqlite_path)
    try:
        init_db(conn)
        clauses = ["d.path = ?"]
        params: list[Any] = [path]
        if chunk_ids:
            placeholders = ",".join("?" for _ in chunk_ids)
            clauses.append(f"c.id IN ({placeholders})")
            params.extend(int(value) for value in chunk_ids)
        else:
            if start_chunk_index is not None:
                clauses.append("c.chunk_index >= ?")
                params.append(int(start_chunk_index))
            if end_chunk_index is not None:
                clauses.append("c.chunk_index <= ?")
                params.append(int(end_chunk_index))
        rows = conn.execute(
            "SELECT c.id AS chunk_id, c.document_id, c.chunk_index, c.heading, c.text, d.path FROM chunks c JOIN documents d ON d.id = c.document_id WHERE " + " AND ".join(clauses) + " ORDER BY c.chunk_index ASC",
            tuple(params),
        ).fetchall()
        return [
            {
                "chunk_id": int(row["chunk_id"]),
                "document_id": int(row["document_id"]),
                "chunk_index": int(row["chunk_index"]),
                "heading": str(row["heading"] or ""),
                "text": str(row["text"]),
                "path": str(row["path"]),
            }
            for row in rows
        ]
    finally:
        conn.close()


def search_library(
    config: AppConfig,
    library: LibraryConfig,
    query: str,
    limit: int = 8,
    mode: str = "hybrid",
) -> list[dict]:
    conn = connect_db(library.sqlite_path)
    try:
        init_db(conn)
        results: dict[int, dict] = {}
        fts_rank: dict[int, int] = {}
        vec_rank: dict[int, int] = {}
        warning = embedding_mismatch_warning(conn, config)

        if mode in {"fts", "hybrid"} and config.fts_enabled:
            fts_query = build_fts_match_query(query)
            rows = conn.execute(
                "SELECT c.id AS chunk_id, c.document_id, c.chunk_index, c.heading, c.text, d.path, bm25(chunks_fts) AS score FROM chunks_fts JOIN chunks c ON c.id = chunks_fts.rowid JOIN documents d ON d.id = c.document_id WHERE chunks_fts MATCH ? ORDER BY score LIMIT ?",
                (fts_query, max(limit * 4, 20)),
            ).fetchall()
            for idx, row in enumerate(rows, start=1):
                chunk_id = int(row["chunk_id"])
                fts_rank[chunk_id] = idx
                results.setdefault(
                    chunk_id,
                    {
                        "chunk_id": chunk_id,
                        "document_id": int(row["document_id"]),
                        "chunk_index": int(row["chunk_index"]),
                        "path": str(row["path"]),
                        "heading": str(row["heading"] or ""),
                        "text": str(row["text"]),
                        "fts_score": float(row["score"]),
                        "vector_score": None,
                    },
                )

        if mode in {"vector", "hybrid"} and config.vector_enabled:
            query_vector = request_embeddings(config, [query])[0]
            vector_limit = max(effective_vector_top_k(config, library), limit * 4)
            used_sqlite_vec = False
            if sqlite_vec_available(conn) and conn.execute("SELECT 1 FROM sqlite_master WHERE name = ? LIMIT 1", (SQLITE_VEC_TABLE,)).fetchone():
                try:
                    rows = conn.execute(
                        f"SELECT v.chunk_id, v.distance, c.document_id, c.chunk_index, c.heading, c.text, d.path FROM {SQLITE_VEC_TABLE} v JOIN chunks c ON c.id = v.chunk_id JOIN documents d ON d.id = c.document_id WHERE v.embedding MATCH ? AND k = ? ORDER BY v.distance",
                        (_sqlite_vec_module.serialize_float32(query_vector), vector_limit),
                    ).fetchall()
                    for idx, row in enumerate(rows, start=1):
                        chunk_id = int(row["chunk_id"])
                        score = 1.0 / (1.0 + float(row["distance"]))
                        vec_rank[chunk_id] = idx
                        entry = results.setdefault(
                            chunk_id,
                            {
                                "chunk_id": chunk_id,
                                "document_id": int(row["document_id"]),
                                "chunk_index": int(row["chunk_index"]),
                                "path": str(row["path"]),
                                "heading": str(row["heading"] or ""),
                                "text": str(row["text"]),
                                "fts_score": None,
                                "vector_score": score,
                            },
                        )
                        entry["vector_score"] = score
                    used_sqlite_vec = True
                except Exception:
                    used_sqlite_vec = False
            if not used_sqlite_vec:
                rows = conn.execute(
                    "SELECT e.chunk_id, e.vector, c.document_id, c.chunk_index, c.heading, c.text, d.path FROM embeddings e JOIN chunks c ON c.id = e.chunk_id JOIN documents d ON d.id = c.document_id"
                ).fetchall()
                scored = []
                for row in rows:
                    score = cosine_similarity(query_vector, json.loads(row["vector"]))
                    scored.append((score, int(row["chunk_id"]), int(row["document_id"]), int(row["chunk_index"]), str(row["path"]), str(row["heading"] or ""), str(row["text"])))
                scored.sort(key=lambda item: item[0], reverse=True)
                for idx, (score, chunk_id, document_id, chunk_index, path, heading, text) in enumerate(scored[:vector_limit], start=1):
                    vec_rank[chunk_id] = idx
                    entry = results.setdefault(
                        chunk_id,
                        {
                            "chunk_id": chunk_id,
                            "document_id": document_id,
                            "chunk_index": chunk_index,
                            "path": path,
                            "heading": heading,
                            "text": text,
                            "fts_score": None,
                            "vector_score": score,
                        },
                    )
                    entry["vector_score"] = score

        if mode == "fts":
            ordered = sorted(results.values(), key=lambda item: item.get("fts_score", float("inf")))
            for item in ordered:
                base_score = -(item.get("fts_score") or 0.0)
                item["score"] = base_score + rerank_adjustment(config, library, query, str(item.get("heading") or ""), str(item.get("text") or ""))
                if warning:
                    item["warning"] = warning
            ordered.sort(key=lambda item: item["score"], reverse=True)
            return ordered[:limit]
        if mode == "vector":
            ordered = sorted(results.values(), key=lambda item: item.get("vector_score", float("-inf")), reverse=True)
            for item in ordered:
                base_score = item.get("vector_score") or 0.0
                item["score"] = base_score + rerank_adjustment(config, library, query, str(item.get("heading") or ""), str(item.get("text") or ""))
                if warning:
                    item["warning"] = warning
            ordered.sort(key=lambda item: item["score"], reverse=True)
            return ordered[:limit]

        fused = []
        for chunk_id, item in results.items():
            score = 0.0
            if chunk_id in fts_rank:
                score += effective_hybrid_fts_weight(config, library) / (effective_hybrid_rrf_k(config, library) + fts_rank[chunk_id])
            if chunk_id in vec_rank:
                score += effective_hybrid_vector_weight(config, library) / (effective_hybrid_rrf_k(config, library) + vec_rank[chunk_id])
            score += rerank_adjustment(config, library, query, str(item.get("heading") or ""), str(item.get("text") or ""))
            item["score"] = score
            fused.append(item)
        fused.sort(key=lambda item: item["score"], reverse=True)
        for item in fused[:limit]:
            if warning:
                item["warning"] = warning
        return fused[:limit]
    finally:
        conn.close()


def compact_snippet(text: str, max_chars: int = 220) -> str:
    text = normalize_text(text)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def group_search_results(
    results: Sequence[dict],
    *,
    group_by: str = "none",
    merge_adjacent: bool = False,
) -> list[dict]:
    if group_by == "none":
        return [dict(item) for item in results]
    if group_by != "path":
        raise ValueError(f"unsupported group_by: {group_by}")

    grouped: list[dict] = []
    for item in sorted(results, key=lambda row: (-float(row.get("score") or 0.0), str(row.get("path") or ""), int(row.get("chunk_index") or 0))):
        if not grouped or grouped[-1]["path"] != item["path"]:
            grouped.append(
                {
                    "document_id": item.get("document_id"),
                    "path": item["path"],
                    "score": float(item.get("score") or 0.0),
                    "best_chunk_id": int(item["chunk_id"]),
                    "headings": [item.get("heading") or ""],
                    "chunks": [dict(item)],
                }
            )
            continue
        group = grouped[-1]
        group["score"] = max(float(group["score"]), float(item.get("score") or 0.0))
        if (item.get("heading") or "") and item.get("heading") not in group["headings"]:
            group["headings"].append(item.get("heading") or "")
        group["chunks"].append(dict(item))

    for rank, group in enumerate(grouped, start=1):
        chunks = sorted(group["chunks"], key=lambda row: int(row.get("chunk_index") or 0))
        merged_ranges: list[dict[str, Any]] = []
        if merge_adjacent and chunks:
            current = {
                "start_chunk_index": int(chunks[0].get("chunk_index") or 0),
                "end_chunk_index": int(chunks[0].get("chunk_index") or 0),
                "chunk_ids": [int(chunks[0]["chunk_id"])],
                "headings": [chunks[0].get("heading") or ""],
                "texts": [str(chunks[0]["text"])],
                "score": float(chunks[0].get("score") or 0.0),
            }
            for chunk in chunks[1:]:
                chunk_index = int(chunk.get("chunk_index") or 0)
                if chunk_index <= current["end_chunk_index"] + 1:
                    current["end_chunk_index"] = chunk_index
                    current["chunk_ids"].append(int(chunk["chunk_id"]))
                    if (chunk.get("heading") or "") and chunk.get("heading") not in current["headings"]:
                        current["headings"].append(chunk.get("heading") or "")
                    current["texts"].append(str(chunk["text"]))
                    current["score"] = max(float(current["score"]), float(chunk.get("score") or 0.0))
                else:
                    merged_ranges.append(current)
                    current = {
                        "start_chunk_index": chunk_index,
                        "end_chunk_index": chunk_index,
                        "chunk_ids": [int(chunk["chunk_id"])],
                        "headings": [chunk.get("heading") or ""],
                        "texts": [str(chunk["text"])],
                        "score": float(chunk.get("score") or 0.0),
                    }
            merged_ranges.append(current)
        else:
            for chunk in chunks:
                merged_ranges.append(
                    {
                        "start_chunk_index": int(chunk.get("chunk_index") or 0),
                        "end_chunk_index": int(chunk.get("chunk_index") or 0),
                        "chunk_ids": [int(chunk["chunk_id"])],
                        "headings": [chunk.get("heading") or ""],
                        "texts": [str(chunk["text"])],
                        "score": float(chunk.get("score") or 0.0),
                    }
                )
        group["rank"] = rank
        group["chunk_count"] = len(chunks)
        group["merged_ranges"] = merged_ranges
    grouped.sort(key=lambda row: float(row["score"]), reverse=True)
    for rank, group in enumerate(grouped, start=1):
        group["rank"] = rank
    return grouped


def _result_record(
    item: dict,
    *,
    rank: int,
    workspace: str | Path | None = None,
    source_roots: Sequence[str | Path] = (),
    snippet_chars: int = 220,
    text_chars: int = 1200,
    include_text: bool = True,
) -> dict[str, Any]:
    path = Path(str(item["path"]))
    record: dict[str, Any] = {
        "rank": rank,
        "chunk_id": int(item["chunk_id"]),
        "score": round(float(item["score"]), 6),
        "path": str(path),
        "heading": item.get("heading") or "",
        "snippet": compact_snippet(str(item["text"]), max_chars=snippet_chars),
        "fts_score": item.get("fts_score"),
        "vector_score": item.get("vector_score"),
    }
    if workspace:
        workspace_path = Path(workspace).expanduser().resolve()
        try:
            record["rel_path"] = path.resolve().relative_to(workspace_path).as_posix()
        except Exception:
            record["rel_path"] = None
    source_rel_path = None
    source_root_match = None
    for root in source_roots:
        try:
            resolved_root = Path(root).expanduser().resolve()
            source_rel_path = path.resolve().relative_to(resolved_root).as_posix()
            source_root_match = str(resolved_root)
            break
        except Exception:
            continue
    record["source_rel_path"] = source_rel_path
    record["source_root"] = source_root_match
    if include_text:
        normalized_text = normalize_text(str(item["text"]))
        record["text"] = compact_snippet(normalized_text, max_chars=text_chars)
        record["text_truncated"] = len(normalized_text) > text_chars
    return record


def build_results_payload(
    results: Sequence[dict],
    *,
    library_id: str,
    library_name: str,
    query: str,
    mode: str,
    limit: int,
    workspace: str | Path | None = None,
    source_roots: Sequence[str | Path] = (),
    snippet_chars: int = 220,
    text_chars: int = 1200,
    include_text: bool = True,
    group_by: str = "none",
    merge_adjacent: bool = False,
    warning: str | None = None,
) -> dict[str, Any]:
    grouped = group_search_results(results, group_by=group_by, merge_adjacent=merge_adjacent)
    rendered_results: list[dict[str, Any]] = []
    if group_by == "none":
        rendered_results = [
            _result_record(
                item,
                rank=idx,
                workspace=workspace,
                source_roots=source_roots,
                snippet_chars=snippet_chars,
                text_chars=text_chars,
                include_text=include_text,
            )
            for idx, item in enumerate(grouped, start=1)
        ]
    else:
        for group in grouped:
            path = Path(str(group["path"]))
            rel_path = None
            if workspace:
                try:
                    rel_path = path.resolve().relative_to(Path(workspace).expanduser().resolve()).as_posix()
                except Exception:
                    rel_path = None
            source_rel_path = None
            source_root_match = None
            for root in source_roots:
                try:
                    resolved_root = Path(root).expanduser().resolve()
                    source_rel_path = path.resolve().relative_to(resolved_root).as_posix()
                    source_root_match = str(resolved_root)
                    break
                except Exception:
                    continue
            merged_ranges = []
            for block in group["merged_ranges"]:
                text = "\n\n".join(part for part in block["texts"] if part)
                merged_record = {
                    "start_chunk_index": block["start_chunk_index"],
                    "end_chunk_index": block["end_chunk_index"],
                    "chunk_ids": block["chunk_ids"],
                    "heading": next((h for h in block["headings"] if h), ""),
                    "headings": [h for h in block["headings"] if h],
                    "score": round(float(block["score"]), 6),
                    "snippet": compact_snippet(text, max_chars=snippet_chars),
                }
                if include_text:
                    normalized_text = normalize_text(text)
                    merged_record["text"] = compact_snippet(normalized_text, max_chars=text_chars)
                    merged_record["text_truncated"] = len(normalized_text) > text_chars
                merged_ranges.append(merged_record)
            rendered_results.append(
                {
                    "rank": group["rank"],
                    "document_id": group.get("document_id"),
                    "best_chunk_id": group["best_chunk_id"],
                    "score": round(float(group["score"]), 6),
                    "path": str(path),
                    "rel_path": rel_path,
                    "source_rel_path": source_rel_path,
                    "source_root": source_root_match,
                    "heading": next((h for h in group["headings"] if h), ""),
                    "headings": [h for h in group["headings"] if h],
                    "chunk_count": group["chunk_count"],
                    "range_count": len(merged_ranges),
                    "ranges": merged_ranges,
                    "snippet": merged_ranges[0]["snippet"] if merged_ranges else "",
                }
            )
    return {
        "schema": "literag.search.v2",
        "library": {
            "id": library_id,
            "name": library_name,
            "source_roots": [str(Path(root).expanduser()) for root in source_roots],
        },
        "query": query,
        "mode": mode,
        "limit": limit,
        "group_by": group_by,
        "merge_adjacent": merge_adjacent,
        "warning": warning,
        "count": len(rendered_results),
        "results": rendered_results,
    }


def print_results(
    results: Sequence[dict],
    *,
    format: str = "text",
    library_id: str = "",
    library_name: str = "",
    query: str = "",
    mode: str = "hybrid",
    limit: int = 8,
    workspace: str | Path | None = None,
    source_roots: Sequence[str | Path] = (),
    snippet_chars: int = 220,
    text_chars: int = 1200,
    include_text: bool = True,
    group_by: str = "none",
    merge_adjacent: bool = False,
) -> None:
    if format == "text":
        if not results:
            print("no results")
            return
        if group_by == "none":
            for idx, item in enumerate(results, start=1):
                heading = item.get("heading") or "(no heading)"
                print(f"[{idx}] score={item['score']:.6f}")
                print(f"path: {item['path']}")
                print(f"heading: {heading}")
                print(f"snippet: {compact_snippet(item['text'], max_chars=snippet_chars)}")
                print()
            return

        payload = build_results_payload(
            results,
            library_id=library_id,
            library_name=library_name,
            query=query,
            mode=mode,
            limit=limit,
            workspace=workspace,
            source_roots=source_roots,
            snippet_chars=snippet_chars,
            text_chars=text_chars,
            include_text=include_text,
            group_by=group_by,
            merge_adjacent=merge_adjacent,
            warning=next((item.get("warning") for item in results if item.get("warning")), None),
        )
        if payload.get("warning"):
            print(f"warning: {payload['warning']}")
            print()
        for item in payload["results"]:
            heading = item.get("heading") or "(no heading)"
            print(f"[{item['rank']}] score={item['score']:.6f}")
            print(f"path: {item['path']}")
            print(f"heading: {heading}")
            print(f"ranges: {item['range_count']} (chunks={item['chunk_count']})")
            print(f"snippet: {item['snippet']}")
            print()
        return

    payload = build_results_payload(
        results,
        library_id=library_id,
        library_name=library_name,
        query=query,
        mode=mode,
        limit=limit,
        workspace=workspace,
        source_roots=source_roots,
        snippet_chars=snippet_chars,
        text_chars=text_chars,
        include_text=include_text,
        group_by=group_by,
        merge_adjacent=merge_adjacent,
        warning=next((item.get("warning") for item in results if item.get("warning")), None),
    )

    if format in {"agent", "json"}:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if format == "jsonl":
        header = {k: v for k, v in payload.items() if k != "results"}
        print(json.dumps({"type": "meta", **header}, ensure_ascii=False))
        for row in payload["results"]:
            print(json.dumps({"type": "result", **row}, ensure_ascii=False))
        return
    raise ValueError(f"unsupported output format: {format}")


def build_inspect_payload(
    chunks: Sequence[dict],
    *,
    library_id: str,
    library_name: str,
    path: str,
    workspace: str | Path | None = None,
    source_roots: Sequence[str | Path] = (),
    text_chars: int = 4000,
    warning: str | None = None,
) -> dict[str, Any]:
    doc_path = Path(path)
    rel_path = None
    if workspace:
        try:
            rel_path = doc_path.resolve().relative_to(Path(workspace).expanduser().resolve()).as_posix()
        except Exception:
            rel_path = None
    source_rel_path = None
    source_root_match = None
    for root in source_roots:
        try:
            resolved_root = Path(root).expanduser().resolve()
            source_rel_path = doc_path.resolve().relative_to(resolved_root).as_posix()
            source_root_match = str(resolved_root)
            break
        except Exception:
            continue
    merged_text = "\n\n".join(str(chunk["text"]) for chunk in chunks)
    normalized_text = normalize_text(merged_text)
    return {
        "schema": "literag.inspect.v1",
        "library": {
            "id": library_id,
            "name": library_name,
            "source_roots": [str(Path(root).expanduser()) for root in source_roots],
        },
        "path": str(doc_path),
        "warning": warning,
        "rel_path": rel_path,
        "source_rel_path": source_rel_path,
        "source_root": source_root_match,
        "chunk_count": len(chunks),
        "start_chunk_index": min((int(chunk["chunk_index"]) for chunk in chunks), default=None),
        "end_chunk_index": max((int(chunk["chunk_index"]) for chunk in chunks), default=None),
        "chunk_ids": [int(chunk["chunk_id"]) for chunk in chunks],
        "headings": [str(chunk.get("heading") or "") for chunk in chunks if str(chunk.get("heading") or "")],
        "text": compact_snippet(normalized_text, max_chars=text_chars),
        "text_truncated": len(normalized_text) > text_chars,
        "chunks": [
            {
                "chunk_id": int(chunk["chunk_id"]),
                "chunk_index": int(chunk["chunk_index"]),
                "heading": str(chunk.get("heading") or ""),
                "snippet": compact_snippet(str(chunk["text"]), max_chars=min(500, text_chars)),
            }
            for chunk in chunks
        ],
    }


def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--workspace", default=None, help="Workspace root; auto-detected when omitted")
    parser.add_argument("--config", default=None, help="Path to knowledge-libs.json; defaults to <workspace>/.literag/knowledge-libs.json")
    return parser


def resolve_config_path(args: argparse.Namespace) -> Path:
    if getattr(args, "config", None):
        return Path(args.config).expanduser().resolve()
    workspace = detect_workspace_root(getattr(args, "workspace", None))
    return workspace / DEFAULT_CONFIG_RELATIVE_PATH
