from __future__ import annotations

import argparse
import json
from pathlib import Path

import catalog
import gitea_api as g
import kb_schema as schema
from utils import json_fail, now_str, sanitize_filename, today_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def build_name(title: str, type_key: str) -> str:
    safe = sanitize_filename(title)
    if schema.DOC_TYPES.get(type_key, {}).get("dated"):
        return f"{today_str()} {safe}"
    return safe


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary_file", required=True)
    parser.add_argument("--type_key", default="doc")
    parser.add_argument("--brief", default="")
    parser.add_argument("--keywords", default="")
    parser.add_argument("--scope", default="personal", choices=["personal", "team"])
    parser.add_argument("--team_id", default="")
    parser.add_argument("--project_id", default="")
    parser.add_argument("--people", default="", help="逗号分隔")
    parser.add_argument("--source_type", default="manual")
    parser.add_argument("--source_id", default="")
    parser.add_argument("--source_path", default="")
    parser.add_argument("--source_url", default="")
    parser.add_argument("--source_commit", default="")
    parser.add_argument("--source_file_path", default="", help="本地原始文件路径，提供时归档到 source_files/")
    args = parser.parse_args()

    src = Path(args.summary_file)
    if not src.exists():
        out(json_fail("summary_file_not_found", f"找不到 summary 文件：{src}"))
        return
    type_key = schema.resolve_type(args.type_key)
    folder = schema.folder_of(type_key)
    fname = build_name(args.title, type_key)
    path = f"summaries/{folder}/{fname}.md"
    content = src.read_text(encoding="utf-8")
    try:
        g.put_file(args.owner, args.repo, path, content, f"paper-kb ingest: {fname}")
        archived_path = ""
        archived_url = ""
        if args.source_file_path:
            raw_path = Path(args.source_file_path)
            if raw_path.exists():
                ext = raw_path.suffix.lower()
                if ext == ".pdf":
                    folder_name = "pdfs"
                elif ext in {".docx", ".doc"}:
                    folder_name = "docs"
                elif ext in {".xlsx", ".xls"}:
                    folder_name = "sheets"
                elif ext in {".txt", ".md", ".markdown"}:
                    folder_name = "text"
                else:
                    folder_name = "other"
                archived_path = f"source_files/{folder_name}/{fname}{ext or '.bin'}"
                g.put_file_bytes(args.owner, args.repo, archived_path, raw_path.read_bytes(), f"paper-kb archive source: {fname}")
                archived_url = f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/{archived_path}"

        cat = catalog.read(args.owner, args.repo)
        entry = {
            "title": args.title,
            "file": path,
            "type_key": type_key,
            "doc_type": schema.DOC_TYPES[type_key]["cn"],
            "brief": args.brief,
            "keywords": [x.strip() for x in args.keywords.split(",") if x.strip()],
            "scope": args.scope,
            "team_id": args.team_id,
            "project_id": args.project_id,
            "people": [x.strip() for x in args.people.split(",") if x.strip()],
            "source_type": args.source_type,
            "source_id": args.source_id,
            "source_path": args.source_path,
            "source_url": args.source_url,
            "source_commit": args.source_commit,
            "archived_source_path": archived_path,
            "created_at": now_str(),
            "updated_at": now_str(),
        }
        replaced = catalog.upsert_document(cat, entry)
        catalog.write(args.owner, args.repo, cat)
        catalog.regen_index(args.owner, args.repo, args.repo, cat)
    except Exception as exc:
        out(json_fail("save_document_failed", str(exc)))
        return
    out({
        "success": True,
        "replaced": replaced,
        "path": path,
        "page_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/{path}",
        "archived_source_path": archived_path,
        "archived_source_url": archived_url,
    })


if __name__ == "__main__":
    main()
