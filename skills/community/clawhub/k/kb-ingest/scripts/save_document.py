from __future__ import annotations

import argparse
from pathlib import Path

import catalog
import gitea_api as g
import kb_schema
from path_utils import sanitize_filename


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary_file", required=True)
    parser.add_argument("--type_key", default="doc")
    parser.add_argument("--source_id", default="")
    parser.add_argument("--source_file_id", default="")
    parser.add_argument("--source_path", default="")
    parser.add_argument("--archived_source_path", default="")
    args = parser.parse_args()
    content = Path(args.summary_file).read_text(encoding="utf-8")
    folder = kb_schema.folder_for(args.type_key)
    path = f"{folder}/{sanitize_filename(args.title)}.md"
    g.put_file(args.owner, args.repo, path, content, f"research-kb ingest: {args.title}")
    cat = catalog.read(args.owner, args.repo)
    replaced = catalog.upsert_document(cat, {
        "title": args.title,
        "file": path,
        "type_key": args.type_key,
        "brief": args.title,
        "source_id": args.source_id,
        "source_file_id": args.source_file_id,
        "source_path": args.source_path,
        "archived_source_path": args.archived_source_path,
    })
    catalog.write(args.owner, args.repo, cat)
    catalog.regen_index(args.owner, args.repo, args.repo, cat)
    print({"success": True, "path": path, "replaced": replaced})


if __name__ == "__main__":
    main()
