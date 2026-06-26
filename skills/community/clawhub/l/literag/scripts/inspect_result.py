#!/usr/bin/env python3
from __future__ import annotations

import json

from literag_common import (
    build_inspect_payload,
    build_parser,
    detect_workspace_root,
    fetch_document_chunks,
    find_library,
    get_library_warning,
    load_config,
    resolve_config_path,
)


def main() -> None:
    parser = build_parser("Inspect LiteRAG search hits by path/chunk range")
    parser.add_argument("library")
    parser.add_argument("path")
    parser.add_argument("--start", type=int, default=None, help="Start chunk_index inclusive")
    parser.add_argument("--end", type=int, default=None, help="End chunk_index inclusive")
    parser.add_argument("--chunk-id", type=int, action="append", dest="chunk_ids", default=None)
    parser.add_argument("--text-chars", type=int, default=4000)
    args = parser.parse_args()

    workspace = detect_workspace_root(args.workspace)
    config = load_config(resolve_config_path(args))
    library = find_library(config, args.library)
    chunks = fetch_document_chunks(
        library,
        path=args.path,
        start_chunk_index=args.start,
        end_chunk_index=args.end,
        chunk_ids=args.chunk_ids,
    )
    payload = build_inspect_payload(
        chunks,
        library_id=library.id,
        library_name=library.name,
        path=args.path,
        workspace=workspace,
        source_roots=[entry.get("path") for entry in library.paths if entry.get("path")],
        text_chars=max(200, args.text_chars),
        warning=get_library_warning(config, library),
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
