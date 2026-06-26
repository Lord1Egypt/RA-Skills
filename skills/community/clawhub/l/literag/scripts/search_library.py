#!/usr/bin/env python3
from __future__ import annotations

from literag_common import (
    build_parser,
    detect_workspace_root,
    find_library,
    load_config,
    print_results,
    resolve_config_path,
    search_library,
)


def main() -> None:
    parser = build_parser("Search one LiteRAG library")
    parser.add_argument("library")
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--mode", choices=["hybrid", "fts", "vector"], default="hybrid")
    parser.add_argument("--format", choices=["agent", "json", "jsonl", "text"], default="agent")
    parser.add_argument("--group-by", choices=["none", "path"], default="path")
    parser.add_argument("--merge-adjacent", action="store_true", default=True)
    parser.add_argument("--no-merge-adjacent", dest="merge_adjacent", action="store_false")
    parser.add_argument("--snippet-chars", type=int, default=220)
    parser.add_argument("--text-chars", type=int, default=1200)
    parser.add_argument("--no-text", action="store_true", help="Omit chunk text from structured output")
    args = parser.parse_args()

    workspace = detect_workspace_root(args.workspace)
    config = load_config(resolve_config_path(args))
    library = find_library(config, args.library)
    results = search_library(config, library, args.query, limit=args.limit, mode=args.mode)
    print_results(
        results,
        format=args.format,
        library_id=library.id,
        library_name=library.name,
        query=args.query,
        mode=args.mode,
        limit=args.limit,
        workspace=workspace,
        source_roots=[entry.get("path") for entry in library.paths if entry.get("path")],
        snippet_chars=max(40, args.snippet_chars),
        text_chars=max(80, args.text_chars),
        include_text=not args.no_text,
        group_by=args.group_by,
        merge_adjacent=args.merge_adjacent,
    )


if __name__ == "__main__":
    main()
