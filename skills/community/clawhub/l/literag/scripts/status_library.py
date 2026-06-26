#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from literag_common import (
    build_parser,
    connect_db,
    current_chunking_fingerprint,
    current_embedding_fingerprint,
    current_index_config_fingerprint,
    find_library,
    get_library_warning,
    get_meta,
    init_db,
    load_config,
    resolve_config_path,
    sqlite_vec_available,
    vector_backend_name,
)


def library_status(config, library) -> dict:
    sqlite_path = Path(library.sqlite_path)
    exists = sqlite_path.exists()
    payload = {
        "library": {
            "id": library.id,
            "name": library.name,
        },
        "sqlite_path": str(sqlite_path),
        "exists": exists,
        "warning": None,
        "meta": {},
        "runtime": {
            "vector_backend": vector_backend_name(conn=None),
            "sqlite_vec_available": sqlite_vec_available(),
        },
        "compatibility": {
            "embedding_fingerprint_matches": None,
            "chunking_fingerprint_matches": None,
            "index_config_fingerprint_matches": None,
            "vector_backend_matches": None,
        },
    }
    if not exists:
        payload["warning"] = "sqlite database missing; index required"
        return payload

    conn = connect_db(sqlite_path)
    try:
        init_db(conn)
        meta_keys = [
            "schema_version",
            "embedding_model",
            "embedding_base_url",
            "embedding_fingerprint",
            "index_config_fingerprint",
            "vector_backend",
            "vector_backend_runtime",
            "vector_dimensions",
            "document_count",
            "chunk_count",
            "embedding_count",
            "last_indexed_at",
        ]
        meta = {key: get_meta(conn, key) for key in meta_keys}
        payload["meta"] = meta
        indexed_embedding_fingerprint = meta.get("embedding_fingerprint")
        indexed_index_config_fingerprint = meta.get("index_config_fingerprint")
        payload["compatibility"]["embedding_fingerprint_matches"] = indexed_embedding_fingerprint == current_embedding_fingerprint(config) if indexed_embedding_fingerprint else None
        payload["compatibility"]["index_config_fingerprint_matches"] = indexed_index_config_fingerprint == current_index_config_fingerprint(config, library) if indexed_index_config_fingerprint else None
        indexed_vector_backend = meta.get("vector_backend")
        payload["compatibility"]["vector_backend_matches"] = indexed_vector_backend == vector_backend_name(conn) if indexed_vector_backend else None
        row = conn.execute(
            "SELECT chunking_fingerprint, embedding_fingerprint FROM documents WHERE chunking_fingerprint IS NOT NULL OR embedding_fingerprint IS NOT NULL LIMIT 1"
        ).fetchone()
        if row:
            doc_chunking = row[0]
            doc_embedding = row[1]
            payload["compatibility"]["chunking_fingerprint_matches"] = doc_chunking == current_chunking_fingerprint(config, library) if doc_chunking else None
            if payload["compatibility"]["embedding_fingerprint_matches"] is None:
                payload["compatibility"]["embedding_fingerprint_matches"] = doc_embedding == current_embedding_fingerprint(config) if doc_embedding else None
        payload["warning"] = get_library_warning(config, library)
        return payload
    finally:
        conn.close()


def print_text(status: dict) -> None:
    library = status["library"]
    print(f"library: {library['id']} ({library['name']})")
    print(f"sqlite_path: {status['sqlite_path']}")
    print(f"exists: {status['exists']}")
    if status.get("warning"):
        print(f"warning: {status['warning']}")
    runtime = status.get("runtime") or {}
    print(f"runtime_vector_backend: {runtime.get('vector_backend')}")
    print(f"sqlite_vec_available: {runtime.get('sqlite_vec_available')}")
    meta = status.get("meta") or {}
    if meta:
        print(f"schema_version: {meta.get('schema_version')}")
        print(f"document_count: {meta.get('document_count')}")
        print(f"chunk_count: {meta.get('chunk_count')}")
        print(f"embedding_count: {meta.get('embedding_count')}")
        print(f"embedding_model: {meta.get('embedding_model')}")
        print(f"vector_backend: {meta.get('vector_backend')}")
        print(f"vector_dimensions: {meta.get('vector_dimensions')}")
        print(f"last_indexed_at: {meta.get('last_indexed_at')}")
    compat = status.get("compatibility") or {}
    print("compatibility:")
    for key, value in compat.items():
        print(f"  - {key}: {value}")


def main() -> None:
    parser = build_parser("Show LiteRAG library status")
    parser.add_argument("library", nargs="?", help="Library id; omit to show all configured libraries")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    config = load_config(resolve_config_path(args))
    libraries = [find_library(config, args.library)] if args.library else list(config.libraries)
    payload = {
        "schema": "literag.status.v1",
        "count": len(libraries),
        "libraries": [library_status(config, library) for library in libraries],
    }

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    for idx, item in enumerate(payload["libraries"], start=1):
        if idx > 1:
            print()
        print_text(item)


if __name__ == "__main__":
    main()
