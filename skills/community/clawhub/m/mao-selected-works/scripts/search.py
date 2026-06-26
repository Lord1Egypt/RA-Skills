#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from common import ROOT, chinese_numeral_to_int, cosine_similarity, embed_texts, http_json, load_config, normalize_volume_label, rerank_documents, resolve_service_config


def open_db(config: dict[str, Any], db_override: str) -> sqlite3.Connection:
    db_path = Path(db_override).expanduser().resolve() if db_override else (ROOT / config.get("database_path", "index/search.sqlite")).resolve()
    if not db_path.exists():
        print(f"索引文件不存在，正在自动创建...")
        import subprocess
        result = subprocess.run(["python", "scripts/build_index.py"], cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            raise SystemExit(f"创建索引失败:\n{result.stderr}")
        print("索引创建完成。")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def build_filters(volume: str | None, chapter: int | None, title: str | None) -> tuple[str, list[str | int]]:
    clauses: list[str] = []
    values: list[str | int] = []
    if volume:
        normalized_volume = normalize_volume_label(volume) or volume
        clauses.append("(d.volume = ? OR d.volume_no = ?)")
        values.extend([normalized_volume, _coerce_volume_number(volume)])
    if chapter:
        clauses.append("d.article_no = ?")
        values.append(chapter)
    if title:
        clauses.append("(d.article_title LIKE ? OR d.aliases_json LIKE ?)")
        values.extend([f"%{title}%", f"%{title}%"])
    return (" AND ".join(clauses), values)


def _coerce_volume_number(value: str | None) -> int:
    if not value:
        return -1
    digits = "".join(char for char in value if char.isdigit())
    if digits:
        return int(digits)
    normalized = normalize_volume_label(value) or value
    match = normalized.replace("第", "").replace("卷", "")
    number = chinese_numeral_to_int(match)
    if number is not None:
        return number
    digits = "".join(char for char in normalized if char.isdigit())
    return int(digits) if digits else -1


def command_catalog(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config).expanduser().resolve())
    conn = open_db(config, args.db)
    where_sql, where_values = build_filters(args.volume, args.chapter, args.title)
    sql = """
        SELECT d.id, d.volume, d.volume_no, d.article_no, d.article_title, d.date, d.source_path
        FROM documents d
    """
    if where_sql:
        sql += f" WHERE {where_sql}"
    sql += " ORDER BY d.volume_no IS NULL, d.volume_no, d.article_no IS NULL, d.article_no, d.article_title"
    rows = [dict(row) for row in conn.execute(sql, where_values).fetchall()]
    payload = {"mode": "catalog", "filters": {"volume": args.volume, "chapter": args.chapter, "title": args.title}, "results": rows}
    emit(payload, args.json)
    return 0


def command_show(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config).expanduser().resolve())
    conn = open_db(config, args.db)
    row = None
    if args.doc_id:
        row = conn.execute("SELECT * FROM documents WHERE id = ?", (args.doc_id,)).fetchone()
    elif args.volume and args.chapter:
        normalized_volume = normalize_volume_label(args.volume) or args.volume
        row = conn.execute(
            """
            SELECT * FROM documents
            WHERE (volume = ? OR volume_no = ?)
              AND article_no = ?
            ORDER BY article_title
            LIMIT 1
            """,
            (normalized_volume, _coerce_volume_number(args.volume), args.chapter),
        ).fetchone()
    elif args.title:
        row = conn.execute(
            """
            SELECT * FROM documents
            WHERE article_title LIKE ? OR aliases_json LIKE ?
            ORDER BY volume_no IS NULL, volume_no, article_no IS NULL, article_no, article_title
            LIMIT 1
            """,
            (f"%{args.title}%", f"%{args.title}%"),
        ).fetchone()
    else:
        raise SystemExit("show requires --doc-id, --title, or --volume with --chapter")

    if row is None:
        payload = {"mode": "show", "result": None}
    else:
        payload = {"mode": "show", "result": dict(row)}
    emit(payload, args.json)
    return 0


def lexical_candidates(
    conn: sqlite3.Connection,
    query: str,
    volume: str | None,
    chapter: int | None,
    title: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    filters, values = build_filters(volume, chapter, title)
    sql = """
        SELECT
            p.id AS passage_id,
            d.id AS doc_id,
            d.volume,
            d.volume_no,
            d.article_no,
            d.article_title,
            d.date,
            d.source_path,
            p.content AS snippet,
            bm25(passage_fts) AS score
        FROM passage_fts
        JOIN passages p ON p.id = passage_fts.rowid
        JOIN documents d ON d.id = p.document_id
        WHERE passage_fts MATCH ?
    """
    params: list[Any] = [query]
    if filters:
        sql += f" AND {filters}"
        params.extend(values)
    sql += " ORDER BY score LIMIT ?"
    params.append(limit)
    rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
    for row in rows:
        row["retrieval"] = "lexical"
        row["score"] = -float(row["score"])
    fallback_rows = fallback_candidates(conn, query, volume, chapter, title, limit)
    combined: dict[int, dict[str, Any]] = {row["passage_id"]: row for row in rows}
    for rank, row in enumerate(fallback_rows, start=1):
        if row["passage_id"] in combined:
            continue
        row["score"] = max(0.05, 1.0 - rank * 0.01)
        combined[row["passage_id"]] = row
    results = list(combined.values())
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]


def fallback_candidates(
    conn: sqlite3.Connection,
    query: str,
    volume: str | None,
    chapter: int | None,
    title: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    filters, values = build_filters(volume, chapter, title)
    sql = """
        SELECT
            p.id AS passage_id,
            d.id AS doc_id,
            d.volume,
            d.volume_no,
            d.article_no,
            d.article_title,
            d.date,
            d.source_path,
            p.content AS snippet
        FROM passages p
        JOIN documents d ON d.id = p.document_id
        WHERE (p.content LIKE ? OR d.article_title LIKE ? OR d.aliases_json LIKE ?)
    """
    params: list[Any] = [f"%{query}%", f"%{query}%", f"%{query}%"]
    if filters:
        sql += f" AND {filters}"
        params.extend(values)
    sql += " ORDER BY d.volume_no IS NULL, d.volume_no, d.article_no IS NULL, d.article_no, p.passage_index LIMIT ?"
    params.append(limit)
    rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
    for row in rows:
        row["retrieval"] = "lexical-like"
        row["score"] = 0.1
    return rows


def vector_candidates(
    conn: sqlite3.Connection,
    query: str,
    config: dict[str, Any],
    volume: str | None,
    chapter: int | None,
    title: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    query_vector = embed_texts([query], config)[0]
    filters, values = build_filters(volume, chapter, title)
    sql = """
        SELECT
            pv.passage_id,
            pv.embedding_json,
            d.id AS doc_id,
            d.volume,
            d.volume_no,
            d.article_no,
            d.article_title,
            d.date,
            d.source_path,
            p.content AS snippet
        FROM passage_vectors pv
        JOIN passages p ON p.id = pv.passage_id
        JOIN documents d ON d.id = p.document_id
    """
    if filters:
        sql += f" WHERE {filters}"
    candidates = []
    for row in conn.execute(sql, values).fetchall():
        embedding = json.loads(row["embedding_json"])
        score = cosine_similarity(query_vector, embedding)
        item = dict(row)
        item.pop("embedding_json", None)
        item["score"] = float(score)
        item["retrieval"] = "vector"
        candidates.append(item)
    candidates.sort(key=lambda item: item["score"], reverse=True)
    return candidates[:limit]


def fuse_results(lexical: list[dict[str, Any]], vector: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
    combined: dict[int, dict[str, Any]] = {}
    for rank, item in enumerate(lexical, start=1):
        entry = combined.setdefault(item["passage_id"], dict(item))
        entry["score"] = entry.get("score", 0.0) + 1.0 / (60 + rank)
        entry["retrieval"] = "hybrid"
    for rank, item in enumerate(vector, start=1):
        entry = combined.setdefault(item["passage_id"], dict(item))
        entry["score"] = entry.get("score", 0.0) + 1.0 / (60 + rank)
        entry["retrieval"] = "hybrid"
    results = list(combined.values())
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


def maybe_rerank(query: str, items: list[dict[str, Any]], config: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    rerank_cfg = config.get("rag", {}).get("rerank", {})
    if not rerank_cfg.get("enabled") or not items:
        return items[:limit]
    documents = [item["snippet"] for item in items]
    reranked = rerank_documents(query, documents, config, top_n=limit)
    remapped: list[dict[str, Any]] = []
    for item in reranked:
        candidate = dict(items[item["index"]])
        candidate["score"] = float(item["score"])
        candidate["retrieval"] = "hybrid-rerank"
        remapped.append(candidate)
    return remapped


def command_search(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config).expanduser().resolve())
    conn = open_db(config, args.db)
    search_cfg = config.get("search", {})
    default_limit = int(search_cfg.get("default_limit", 8))
    candidate_limit = int(search_cfg.get("hybrid_candidate_limit", 24))
    limit = args.limit or default_limit
    mode = args.mode

    lexical = lexical_candidates(conn, args.query, args.volume, args.chapter, args.title, max(limit, candidate_limit))
    results: list[dict[str, Any]]

    rag_enabled = bool(config.get("rag", {}).get("enabled"))
    if mode == "lexical" or (mode == "auto" and not rag_enabled):
        results = lexical[:limit]
        resolved_mode = "lexical"
    else:
        if not rag_enabled:
            raise SystemExit("Hybrid retrieval requested but rag.enabled is false in config.")
        vector = vector_candidates(conn, args.query, config, args.volume, args.chapter, args.title, candidate_limit)
        results = fuse_results(lexical, vector, candidate_limit)
        results = maybe_rerank(args.query, results, config, limit)
        resolved_mode = "hybrid"

    payload = {
        "query": args.query,
        "mode": resolved_mode,
        "filters": {"volume": args.volume, "chapter": args.chapter, "title": args.title},
        "results": results,
    }
    emit(payload, args.json)
    return 0


def require_service_config(config: dict[str, Any], section: str) -> tuple[str, str, str | None]:
    service_cfg = resolve_service_config(config, section)
    base_url = str(service_cfg.get("base_url", "")).rstrip("/")
    model = str(service_cfg.get("model", "")).strip()
    api_key_env = str(service_cfg.get("api_key_env", "")).strip()

    if not base_url:
        raise SystemExit(
            f"{section} test aborted: missing base_url. Please set rag.api.base_url or rag.{section}.base_url in config/search.json."
        )
    if not model:
        raise SystemExit(
            f"{section} test aborted: missing model. Please set rag.{section}.model in config/search.json."
        )
    if not api_key_env:
        raise SystemExit(
            f"{section} test aborted: missing api_key_env. Please set rag.api.api_key_env or rag.{section}.api_key_env in config/search.json."
        )
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise SystemExit(
            f"{section} test aborted: environment variable {api_key_env} is not set. Please export {api_key_env}=<your_api_key>."
        )
    return base_url, model, api_key


def test_embedding(config: dict[str, Any]) -> dict[str, Any]:
    base_url, model, api_key = require_service_config(config, "embedding")
    payload = {"input": ["ping"], "model": model}
    response = http_json(f"{base_url}/embeddings", payload, api_key=api_key)
    if not response.get("data"):
        raise SystemExit("embedding test failed: no data returned from /embeddings")
    return {
        "target": "embedding",
        "success": True,
        "message": f"Embedding model {model} responded successfully.",
    }


def test_rerank(config: dict[str, Any]) -> dict[str, Any]:
    base_url, model, api_key = require_service_config(config, "rerank")
    payload = {
        "model": model,
        "query": "调查研究",
        "documents": ["没有调查，没有发言权。", "星星之火，可以燎原。"],
        "top_n": 1,
    }
    response = http_json(f"{base_url}/rerank", payload, api_key=api_key)
    results = response.get("results") or response.get("data") or []
    if not results:
        raise SystemExit("rerank test failed: no results returned from /rerank")
    return {
        "target": "rerank",
        "success": True,
        "message": f"Rerank model {model} responded successfully.",
    }


def command_test_model(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config).expanduser().resolve())
    target = args.target
    if target == "embedding":
        payload = test_embedding(config)
    else:
        payload = test_rerank(config)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload["message"])
    return 0


def emit(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if payload.get("mode") == "show":
        result = payload.get("result")
        if not result:
            print("No document found.")
            return
        chapter = result.get("article_no")
        chapter_label = f" 第{chapter}篇" if chapter else ""
        print(f"[{result.get('volume') or '未分卷'}{chapter_label}] {result['article_title']}")
        if result.get("date"):
            print(result["date"])
        print(result["source_path"])
        print()
        print(result["content"])
        return

    for item in payload.get("results", []):
        title = item.get("article_title") or "未命名文章"
        volume = item.get("volume") or "未分卷"
        chapter = item.get("article_no")
        chapter_label = f" 第{chapter}篇" if chapter else ""
        print(f"[{volume}{chapter_label}] {title}")
        if item.get("source_path"):
            print(item["source_path"])
        if item.get("snippet"):
            print(item["snippet"][:240].strip())
        print(f"retrieval={item.get('retrieval')} score={item.get('score')}")
        print()
    if not payload.get("results"):
        print("No results found.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search Mao Selected Works corpus")
    parser.add_argument(
        "--config",
        default=str(ROOT / "config" / "search.json"),
        help="Search configuration file. Falls back to config/search.example.json when missing.",
    )
    parser.add_argument("--db", default="", help="Override database path")

    subparsers = parser.add_subparsers(dest="command", required=True)

    catalog = subparsers.add_parser("catalog", help="List articles by volume or title")
    catalog.add_argument("--volume", default=None, help="Volume label or number, e.g. 第一卷 / 1 / 01")
    catalog.add_argument("--chapter", type=int, default=0, help="Article number within a volume, e.g. 3")
    catalog.add_argument("--title", default=None, help="Partial article title match")
    catalog.add_argument("--json", action="store_true", help="Emit JSON")
    catalog.set_defaults(func=command_catalog)

    show = subparsers.add_parser("show", help="Display a single article")
    show.add_argument("--doc-id", type=int, default=0, help="Document ID from catalog/search")
    show.add_argument("--volume", default=None, help="Volume label or number, used with --chapter")
    show.add_argument("--chapter", type=int, default=0, help="Article number within a volume")
    show.add_argument("--title", default=None, help="Partial article title match")
    show.add_argument("--json", action="store_true", help="Emit JSON")
    show.set_defaults(func=command_show)

    search = subparsers.add_parser("search", help="Full text or hybrid search")
    search.add_argument("query", help="Search query")
    search.add_argument("--volume", default=None, help="Filter by volume label or number")
    search.add_argument("--chapter", type=int, default=0, help="Filter by article number within a volume")
    search.add_argument("--title", default=None, help="Filter by partial article title")
    search.add_argument("--mode", choices=["auto", "lexical", "hybrid"], default="auto")
    search.add_argument("--limit", type=int, default=0, help="Result limit")
    search.add_argument("--json", action="store_true", help="Emit JSON")
    search.set_defaults(func=command_search)

    test_model = subparsers.add_parser("test-model", help="Test embedding or rerank endpoint connectivity")
    test_model.add_argument("--target", choices=["embedding", "rerank"], default="embedding")
    test_model.add_argument("--json", action="store_true", help="Emit JSON")
    test_model.set_defaults(func=command_test_model)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
