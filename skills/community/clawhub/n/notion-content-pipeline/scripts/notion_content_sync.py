#!/usr/bin/env python3
"""Notion Content Sync — push/pull blog drafts between local .md files and Notion.

Usage:
  python3 notion_content_sync.py push content/my-post.md
  python3 notion_content_sync.py push-all
  python3 notion_content_sync.py pull content/my-post.md
  python3 notion_content_sync.py list

Configuration (env vars):
  NOTION_API_KEY        Notion integration token (required)
  NOTION_PARENT_PAGE_ID Parent page ID for the sandbox (required for push/push-all)
  NOTION_SYNC_MAP       Path to sync map JSON (default: notion_sync_map.json)
  CONTENT_DIR           Directory with .md files (default: ./content)

CLI overrides:
  --sandbox-id    Override NOTION_PARENT_PAGE_ID
  --sync-map      Override NOTION_SYNC_MAP path
  --no-overwrite  Don't re-push if already tracked
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

NOTION_VERSION = "2022-06-28"
NOTION_API = "https://api.notion.com/v1"


# ── Config helpers ────────────────────────────────────────────────────────────

def _get_notion_key() -> str:
    key = os.environ.get("NOTION_API_KEY") or os.environ.get("NOTION_KEY")
    if key:
        return key
    raise RuntimeError(
        "No Notion API key found. Set NOTION_API_KEY env var.\n"
        "Get one at https://www.notion.so/my-integrations"
    )


def _get_parent_page_id(override: Optional[str] = None) -> str:
    page_id = override or os.environ.get("NOTION_PARENT_PAGE_ID")
    if not page_id:
        raise RuntimeError(
            "No parent page ID found. Set NOTION_PARENT_PAGE_ID env var or pass --sandbox-id."
        )
    return page_id


def _get_sync_map_path(override: Optional[str] = None) -> Path:
    path = override or os.environ.get("NOTION_SYNC_MAP", "notion_sync_map.json")
    return Path(path)


def _get_content_dir() -> Path:
    return Path(os.environ.get("CONTENT_DIR", "content"))


# ── Notion API helpers ────────────────────────────────────────────────────────

def _headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _req(method: str, url: str, key: str, **kwargs) -> dict:
    import requests
    resp = getattr(requests, method)(f"{NOTION_API}{url}", headers=_headers(key), **kwargs)
    if not resp.ok:
        print(f"Notion API error {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
        resp.raise_for_status()
    return resp.json()


def _append_blocks(page_id: str, blocks: list[dict], key: str) -> None:
    """Append blocks in batches of 100 (Notion API limit)."""
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i + 100]
        _req("patch", f"/blocks/{page_id}/children", key,
             json={"children": batch}, timeout=30)
        if i + 100 < len(blocks):
            time.sleep(0.3)


def _archive_page(page_id: str, key: str) -> None:
    _req("patch", f"/pages/{page_id}", key,
         json={"archived": True}, timeout=15)


# ── Markdown → Notion blocks ──────────────────────────────────────────────────

def _rich_text(text: str) -> list[dict]:
    """Parse inline markdown (bold, italic, inline code) into Notion rich_text."""
    if not text:
        return [{"type": "text", "text": {"content": ""}}]

    pattern = re.compile(r'(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*|_[^_]+_)')
    parts = pattern.split(text)
    result = []
    for part in parts:
        if not part:
            continue
        ann = {"bold": False, "italic": False, "code": False,
               "strikethrough": False, "underline": False, "color": "default"}
        content = part
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            content = part[1:-1]
            ann["code"] = True
        elif part.startswith("**") and part.endswith("**") and len(part) > 3:
            content = part[2:-2]
            ann["bold"] = True
        elif ((part.startswith("*") and part.endswith("*") and len(part) > 1) or
              (part.startswith("_") and part.endswith("_") and len(part) > 1)):
            content = part[1:-1]
            ann["italic"] = True
        for chunk in _chunk_text(content, 1900):
            result.append({
                "type": "text",
                "text": {"content": chunk},
                "annotations": ann.copy(),
            })
    return result or [{"type": "text", "text": {"content": text}}]


def _chunk_text(text: str, max_len: int) -> list[str]:
    if len(text) <= max_len:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:max_len])
        text = text[max_len:]
    return chunks


def md_to_blocks(markdown: str) -> list[dict]:
    """Convert markdown string to Notion block objects."""
    blocks: list[dict] = []
    lines = markdown.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code_body = "\n".join(code_lines)
            for chunk in _chunk_text(code_body, 1900):
                blocks.append({
                    "object": "block", "type": "code",
                    "code": {
                        "language": lang,
                        "rich_text": [{"type": "text", "text": {"content": chunk}}],
                    },
                })
            i += 1
            continue

        if re.match(r"^-{3,}$", line.strip()):
            blocks.append({"object": "block", "type": "divider", "divider": {}})
            i += 1
            continue

        m = re.match(r"^(#{1,3})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            btype = f"heading_{level}"
            blocks.append({
                "object": "block", "type": btype,
                btype: {"rich_text": _rich_text(text)},
            })
            i += 1
            continue

        if line.startswith("> "):
            blocks.append({
                "object": "block", "type": "quote",
                "quote": {"rich_text": _rich_text(line[2:])},
            })
            i += 1
            continue

        m = re.match(r"^[-*]\s+(.*)", line)
        if m:
            blocks.append({
                "object": "block", "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": _rich_text(m.group(1))},
            })
            i += 1
            continue

        m = re.match(r"^\d+\.\s+(.*)", line)
        if m:
            blocks.append({
                "object": "block", "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": _rich_text(m.group(1))},
            })
            i += 1
            continue

        if not line.strip():
            i += 1
            continue

        # Paragraph (accumulate until blank line or structural element)
        para_lines = []
        while i < len(lines) and lines[i].strip() and \
              not lines[i].strip().startswith("#") and \
              not lines[i].strip().startswith("```") and \
              not lines[i].strip().startswith("---") and \
              not re.match(r"^[-*]\s", lines[i]) and \
              not re.match(r"^\d+\.\s", lines[i]) and \
              not lines[i].startswith("> "):
            para_lines.append(lines[i])
            i += 1

        text = " ".join(para_lines)
        if text.strip():
            for chunk in _chunk_text(text, 1900):
                blocks.append({
                    "object": "block", "type": "paragraph",
                    "paragraph": {"rich_text": _rich_text(chunk)},
                })

    return blocks


# ── Notion → Markdown ─────────────────────────────────────────────────────────

def _rt_to_md(rich_text: list[dict]) -> str:
    result = []
    for rt in rich_text:
        content = rt.get("text", {}).get("content", "")
        ann = rt.get("annotations", {})
        if ann.get("code"):
            content = f"`{content}`"
        if ann.get("bold"):
            content = f"**{content}**"
        if ann.get("italic"):
            content = f"_{content}_"
        result.append(content)
    return "".join(result)


def blocks_to_md(blocks: list[dict]) -> str:
    lines = []
    for block in blocks:
        btype = block.get("type", "")
        content = block.get(btype, {})
        if btype == "heading_1":
            lines.append(f"# {_rt_to_md(content.get('rich_text', []))}")
        elif btype == "heading_2":
            lines.append(f"## {_rt_to_md(content.get('rich_text', []))}")
        elif btype == "heading_3":
            lines.append(f"### {_rt_to_md(content.get('rich_text', []))}")
        elif btype == "paragraph":
            text = _rt_to_md(content.get("rich_text", []))
            lines.append(text if text.strip() else "")
        elif btype == "bulleted_list_item":
            lines.append(f"- {_rt_to_md(content.get('rich_text', []))}")
        elif btype == "numbered_list_item":
            lines.append(f"1. {_rt_to_md(content.get('rich_text', []))}")
        elif btype == "code":
            lang = content.get("language", "")
            code = _rt_to_md(content.get("rich_text", []))
            lines.append(f"```{lang}\n{code}\n```")
        elif btype == "divider":
            lines.append("---")
        elif btype == "quote":
            lines.append(f"> {_rt_to_md(content.get('rich_text', []))}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


# ── Sync map helpers ──────────────────────────────────────────────────────────

def _load_map(sync_map_path: Path) -> dict:
    if sync_map_path.exists():
        return json.loads(sync_map_path.read_text())
    return {}


def _save_map(m: dict, sync_map_path: Path) -> None:
    sync_map_path.write_text(json.dumps(m, indent=2))


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_push(file_path: Path, key: str, sandbox_id: str,
             sync_map_path: Path, overwrite: bool = True) -> str:
    sync_map = _load_map(sync_map_path)
    rel = str(file_path)
    md = file_path.read_text()

    title = file_path.stem.replace("-", " ").title()
    for line in md.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    blocks = md_to_blocks(md)
    existing_id = sync_map.get(rel)

    if existing_id and overwrite:
        print(f"  Archiving existing page {existing_id}, creating fresh...")
        _archive_page(existing_id, key)
        time.sleep(0.5)

    page = _req("post", "/pages", key, json={
        "parent": {"page_id": sandbox_id},
        "properties": {
            "title": {"title": [{"text": {"content": title}}]},
        },
        "children": blocks[:100],
    }, timeout=30)
    page_id = page["id"]
    if len(blocks) > 100:
        _append_blocks(page_id, blocks[100:], key)
    print(f"  Created {len(blocks)} blocks → page {page_id}")

    sync_map[rel] = page_id
    _save_map(sync_map, sync_map_path)
    return page_id


def cmd_pull(file_path: Path, key: str, sync_map_path: Path) -> None:
    sync_map = _load_map(sync_map_path)
    rel = str(file_path)
    page_id = sync_map.get(rel)
    if not page_id:
        print(f"No tracked Notion page for {rel}. Run push first.", file=sys.stderr)
        sys.exit(1)

    all_blocks = []
    cursor = None
    while True:
        params = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        data = _req("get", f"/blocks/{page_id}/children", key,
                    params=params, timeout=15)
        all_blocks.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data["next_cursor"]

    md = blocks_to_md(all_blocks)
    file_path.write_text(md)
    print(f"  Pulled {len(all_blocks)} blocks → {file_path}")


def cmd_list(sync_map_path: Path) -> None:
    sync_map = _load_map(sync_map_path)
    if not sync_map:
        print("No tracked pages yet.")
        return
    for rel, page_id in sync_map.items():
        url = f"https://notion.so/{page_id.replace('-', '')}"
        print(f"  {rel}")
        print(f"    ID:  {page_id}")
        print(f"    URL: {url}")


def cmd_push_all(key: str, sandbox_id: str, sync_map_path: Path,
                 content_dir: Path) -> None:
    files = sorted(content_dir.glob("*.md"))
    if not files:
        print(f"No .md files found in {content_dir}")
        return
    for f in files:
        print(f"\nPushing {f.name}...")
        page_id = cmd_push(f, key, sandbox_id, sync_map_path)
        url = f"https://notion.so/{page_id.replace('-', '')}"
        print(f"  → {url}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Notion ↔ Markdown content sync")
    parser.add_argument("command", choices=["push", "push-all", "pull", "list"])
    parser.add_argument("file", nargs="?", help="Path to .md file")
    parser.add_argument("--sandbox-id", help="Override NOTION_PARENT_PAGE_ID")
    parser.add_argument("--sync-map", help="Override NOTION_SYNC_MAP path")
    parser.add_argument("--no-overwrite", action="store_true")
    args = parser.parse_args()

    key = _get_notion_key()
    sync_map_path = _get_sync_map_path(args.sync_map)
    content_dir = _get_content_dir()

    if args.command == "list":
        cmd_list(sync_map_path)

    elif args.command == "push-all":
        sandbox_id = _get_parent_page_id(args.sandbox_id)
        cmd_push_all(key, sandbox_id, sync_map_path, content_dir)

    elif args.command == "push":
        if not args.file:
            parser.error("push requires a file argument")
        f = Path(args.file)
        if not f.exists():
            print(f"File not found: {f}", file=sys.stderr)
            sys.exit(1)
        sandbox_id = _get_parent_page_id(args.sandbox_id)
        page_id = cmd_push(f, key, sandbox_id, sync_map_path,
                            overwrite=not args.no_overwrite)
        url = f"https://notion.so/{page_id.replace('-', '')}"
        print(f"  → {url}")

    elif args.command == "pull":
        if not args.file:
            parser.error("pull requires a file argument")
        cmd_pull(Path(args.file), key, sync_map_path)


if __name__ == "__main__":
    main()
