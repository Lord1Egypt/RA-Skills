#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from literag_common import build_parser, connect_db, find_library, get_meta, init_db, load_config, resolve_config_path


def library_meta(library) -> dict:
    sqlite_path = Path(library.sqlite_path)
    payload = {
        "library": {
            "id": library.id,
            "name": library.name,
        },
        "sqlite_path": str(sqlite_path),
        "exists": sqlite_path.exists(),
        "meta": {},
    }
    if not sqlite_path.exists():
        return payload
    conn = connect_db(sqlite_path)
    try:
        init_db(conn)
        rows = conn.execute("SELECT key, value FROM meta ORDER BY key ASC").fetchall()
        payload["meta"] = {str(row[0]): str(row[1]) for row in rows}
        return payload
    finally:
        conn.close()


def main() -> None:
    parser = build_parser("Show raw LiteRAG sqlite meta records")
    parser.add_argument("library", nargs="?", help="Library id; omit to show all configured libraries")
    args = parser.parse_args()

    config = load_config(resolve_config_path(args))
    libraries = [find_library(config, args.library)] if args.library else list(config.libraries)
    payload = {
        "schema": "literag.meta.v1",
        "count": len(libraries),
        "libraries": [library_meta(library) for library in libraries],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
