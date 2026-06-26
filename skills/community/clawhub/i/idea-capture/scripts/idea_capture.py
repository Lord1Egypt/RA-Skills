#!/usr/bin/env python3
import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
IDEAS_DIR = ROOT / "ideas"
SUMMARIES_DIR = IDEAS_DIR / "summaries"
CATALOG_PATH = IDEAS_DIR / "catalog.json"
INDEX_PATH = IDEAS_DIR / "INDEX.md"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "idea"


def now_parts():
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y%m%d-%H%M%S")


def ensure_dirs():
    IDEAS_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)


def load_catalog():
    if CATALOG_PATH.exists():
        return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return {"ideas": []}


def save_catalog(catalog):
    CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_idea(catalog, idea_id=None, title=None):
    if idea_id:
        for item in catalog["ideas"]:
            if item["id"] == idea_id:
                return item
    if title:
        slug = slugify(title)
        for item in catalog["ideas"]:
            if item["id"] == slug or item.get("title", "").strip().lower() == title.strip().lower():
                return item
    return None


def parse_tags(raw):
    if not raw:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


def render_idea_doc(meta, latest_summary, notes, open_questions, next_steps, update_entry):
    tags_yaml = ", ".join(meta["tags"])
    oq = "\n".join(f"- {x}" for x in open_questions) or "- 暂无"
    ns = "\n".join(f"- {x}" for x in next_steps) or "- 暂无"
    updates = update_entry.rstrip()
    return f"""---
id: {meta['id']}
title: {meta['title']}
status: {meta['status']}
tags: [{tags_yaml}]
created: {meta['created']}
updated: {meta['updated']}
source: {meta.get('source', 'unknown')}
---

# {meta['title']}

## 一句话
{latest_summary}

## 当前理解
{notes}

## Open Questions
{oq}

## Next Steps
{ns}

## Update Log
{updates}
"""


def update_existing_doc(path: Path, summary: str, notes: str, open_questions, next_steps, update_entry: str, updated_at: str):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(^updated:\s*)(.+)$", rf"\g<1>{updated_at}", text, flags=re.M)
    text = re.sub(r"(## 一句话\n)(.*?)(\n## 当前理解\n)", rf"\1{summary}\3", text, flags=re.S)
    text = re.sub(r"(## 当前理解\n)(.*?)(\n## Open Questions\n)", rf"\1{notes}\3", text, flags=re.S)
    oq = "\n".join(f"- {x}" for x in open_questions) or "- 暂无"
    ns = "\n".join(f"- {x}" for x in next_steps) or "- 暂无"
    text = re.sub(r"(## Open Questions\n)(.*?)(\n## Next Steps\n)", rf"\1{oq}\3", text, flags=re.S)
    text = re.sub(r"(## Next Steps\n)(.*?)(\n## Update Log\n)", rf"\1{ns}\3", text, flags=re.S)
    if "## Update Log\n" in text:
        text += "\n" + update_entry.rstrip() + "\n"
    path.write_text(text, encoding="utf-8")


def write_summary(idea_id: str, title: str, source: str, summary: str, notes: str, open_questions, next_steps, stamp: str):
    target_dir = SUMMARIES_DIR / idea_id
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{stamp}.md"
    oq = "\n".join(f"- {x}" for x in open_questions) or "- 暂无"
    ns = "\n".join(f"- {x}" for x in next_steps) or "- 暂无"
    content = f"""# {title} - 会话纪要

- idea_id: `{idea_id}`
- source: {source}
- timestamp: {stamp}

## 本次讨论重点
{summary}

## 详细补充
{notes}

## 待定问题
{oq}

## 下次可继续
{ns}
"""
    path.write_text(content, encoding="utf-8")
    return path


def rebuild_index(catalog):
    lines = ["# Ideas Index", ""]
    for item in sorted(catalog["ideas"], key=lambda x: x.get("updated", ""), reverse=True):
        tags = ", ".join(item.get("tags", []))
        lines.extend([
            f"- **{item['title']}** (`{item['id']}`)",
            f"  - status: {item.get('status', 'unknown')}",
            f"  - updated: {item.get('updated', '')}",
            f"  - tags: {tags or 'none'}",
            f"  - file: `ideas/{item['id']}.md`",
            "",
        ])
    INDEX_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--notes", required=True)
    parser.add_argument("--tags", default="")
    parser.add_argument("--mode", choices=["auto", "create", "update"], default="auto")
    parser.add_argument("--idea-id", default="")
    parser.add_argument("--source", default="manual")
    parser.add_argument("--open-question", action="append", default=[])
    parser.add_argument("--next-step", action="append", default=[])
    args = parser.parse_args()

    ensure_dirs()
    catalog = load_catalog()
    today, updated_at, stamp = now_parts()
    tags = parse_tags(args.tags)
    idea = None

    if args.mode in ("auto", "update"):
        idea = find_idea(catalog, args.idea_id or None, args.title)
        if args.mode == "update" and not idea:
            raise SystemExit("Requested update, but no matching idea found.")

    if args.mode == "create":
        idea = None

    update_entry = f"### {updated_at}\n- summary: {args.summary}\n- notes: {args.notes}\n"
    if args.open_question:
        update_entry += "- open_questions:\n" + "\n".join(f"  - {x}" for x in args.open_question) + "\n"
    if args.next_step:
        update_entry += "- next_steps:\n" + "\n".join(f"  - {x}" for x in args.next_step) + "\n"

    action = "updated"
    if idea is None:
        idea_id = args.idea_id or slugify(args.title)
        idea_path = IDEAS_DIR / f"{idea_id}.md"
        meta = {
            "id": idea_id,
            "title": args.title,
            "status": "active",
            "tags": tags,
            "created": today,
            "updated": updated_at,
            "source": args.source,
        }
        idea_path.write_text(
            render_idea_doc(meta, args.summary, args.notes, args.open_question, args.next_step, update_entry),
            encoding="utf-8",
        )
        catalog["ideas"].append(meta)
        action = "created"
    else:
        idea_id = idea["id"]
        idea_path = IDEAS_DIR / f"{idea_id}.md"
        merged_tags = sorted(set(idea.get("tags", [])) | set(tags))
        idea["tags"] = merged_tags
        idea["updated"] = updated_at
        update_existing_doc(idea_path, args.summary, args.notes, args.open_question, args.next_step, update_entry, updated_at)

    summary_path = write_summary(idea_id, args.title if action == "created" else idea["title"], args.source, args.summary, args.notes, args.open_question, args.next_step, stamp)
    save_catalog(catalog)
    rebuild_index(catalog)

    print(json.dumps({
        "status": "ok",
        "action": action,
        "idea_id": idea_id,
        "idea_file": str(idea_path.relative_to(ROOT)),
        "summary_file": str(summary_path.relative_to(ROOT)),
        "catalog_file": str(CATALOG_PATH.relative_to(ROOT)),
        "index_file": str(INDEX_PATH.relative_to(ROOT)),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
