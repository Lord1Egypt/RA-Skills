#!/usr/bin/env python3
"""Publish simple articles to Notion without MCP.

This CLI is intentionally dependency-free so it can run in clients that support
shell commands but do not provide Notion MCP tools.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


CONFIG_DIR = Path.home() / ".notion_publish"
CONFIG_PATH = CONFIG_DIR / "notion-publisher-config.json"
DEFAULT_CONFIG = {
    "default_status": "Draft",
    "template_strategy": "ask_each_time",
}
DEFAULT_SCHEMA = {
    "title": {"type": "title"},
    "status": {"type": "select"},
    "type": {"type": "select"},
    "category": {"type": "select"},
    "tags": {"type": "multi_select"},
    "slug": {"type": "rich_text"},
    "summary": {"type": "rich_text"},
    "date": {"type": "date"},
}
NOTION_VERSION = os.environ.get("NOTION_VERSION", "2026-03-11")
API_BASE = "https://api.notion.com/v1"


class NotionError(RuntimeError):
    pass


def load_config() -> dict[str, Any]:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, indent=2) + "\n", encoding="utf-8")
        return dict(DEFAULT_CONFIG)

    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid config JSON: {CONFIG_PATH}: {exc}") from exc

    changed = False
    for key, value in DEFAULT_CONFIG.items():
        if key not in data:
            data[key] = value
            changed = True
    if changed:
        CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return data


def save_config(config: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_env_file() -> None:
    env_path = CONFIG_DIR / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def parse_notion_id(value: str) -> str:
    """Extract a Notion UUID from an ID or URL."""
    text = value.strip()
    if not text:
        return ""

    parsed = urllib.parse.urlparse(text)
    query = urllib.parse.parse_qs(parsed.query)
    if text.startswith("collection://"):
        text = text.removeprefix("collection://")
    elif query.get("p"):
        text = query["p"][0]
    else:
        text = (parsed.netloc or parsed.path.rsplit("/", 1)[-1]) if parsed.scheme else text

    text = text.split("?")[0].replace("-", "")
    match = re.search(r"([0-9a-fA-F]{32})", text)
    if not match:
        raise ValueError(f"Could not find a Notion ID in: {value}")
    raw = match.group(1).lower()
    return f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"


class NotionClient:
    def __init__(self, token: str) -> None:
        self.token = token

    def request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{API_BASE}{path}",
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise NotionError(f"Notion API {exc.code} {exc.reason}: {body}") from exc
        except urllib.error.URLError as exc:
            raise NotionError(f"Network error calling Notion API: {exc}") from exc

    def get_database(self, database_id: str) -> dict[str, Any]:
        return self.request("GET", f"/databases/{database_id}")

    def get_data_source(self, data_source_id: str) -> dict[str, Any]:
        return self.request("GET", f"/data_sources/{data_source_id}")

    def query_data_source(self, data_source_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", f"/data_sources/{data_source_id}/query", payload)

    def query_database(self, database_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", f"/databases/{database_id}/query", payload)

    def create_page(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/pages", payload)

    def get_page(self, page_id: str) -> dict[str, Any]:
        return self.request("GET", f"/pages/{page_id}")

    def update_page(self, page_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("PATCH", f"/pages/{page_id}", payload)

    def list_block_children(self, block_id: str, start_cursor: str | None = None) -> dict[str, Any]:
        suffix = f"?start_cursor={urllib.parse.quote(start_cursor)}" if start_cursor else ""
        return self.request("GET", f"/blocks/{block_id}/children{suffix}")

    def append_block_children(self, block_id: str, children: list[dict[str, Any]]) -> dict[str, Any]:
        return self.request("PATCH", f"/blocks/{block_id}/children", {"children": children})

    def delete_block(self, block_id: str) -> dict[str, Any]:
        return self.request("DELETE", f"/blocks/{block_id}")


def plain_text(text: str) -> list[dict[str, Any]]:
    return [{"type": "text", "text": {"content": text[:2000]}}] if text else []


def paragraph_block(text: str) -> dict[str, Any]:
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": plain_text(text)}}


def heading_block(level: int, text: str) -> dict[str, Any]:
    block_type = f"heading_{min(max(level, 1), 3)}"
    return {"object": "block", "type": block_type, block_type: {"rich_text": plain_text(text)}}


def image_block(caption: str, url: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "image",
        "image": {
            "type": "external",
            "external": {"url": url},
            "caption": plain_text(caption),
        },
    }


def callout_block(text: str, icon: str = "💡", color: str = "blue_background") -> dict[str, Any]:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": plain_text(text),
            "icon": {"type": "emoji", "emoji": icon},
            "color": color,
        },
    }


def code_block(language: str, code: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": plain_text(code[:2000]),
            "language": language or "plain text",
        },
    }


def normalize_color(color: str | None) -> str:
    if not color:
        return "blue_background"
    return color.replace("_bg", "_background")


def markdown_to_blocks(markdown: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    lines = markdown.splitlines()
    i = 0
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(paragraph_block(" ".join(part.strip() for part in paragraph).strip()))
            paragraph = []

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if not stripped or stripped == "<empty-block/>":
            flush_paragraph()
            i += 1
            continue

        if stripped.startswith("<callout"):
            flush_paragraph()
            icon_match = re.search(r'icon="([^"]+)"', stripped)
            color_match = re.search(r'color="([^"]+)"', stripped)
            icon = icon_match.group(1) if icon_match else "💡"
            color = normalize_color(color_match.group(1) if color_match else None)
            collected: list[str] = []
            i += 1
            while i < len(lines) and "</callout>" not in lines[i]:
                content = lines[i].strip()
                if content:
                    collected.append(content)
                i += 1
            blocks.append(callout_block(" ".join(collected), icon=icon, color=color))
            i += 1
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            language = stripped.removeprefix("```").strip() or "plain text"
            collected = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                collected.append(lines[i])
                i += 1
            blocks.append(code_block(language, "\n".join(collected)))
            i += 1
            continue

        image_match = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
        if image_match:
            flush_paragraph()
            blocks.append(image_block(image_match.group(1), image_match.group(2)))
            i += 1
            continue

        heading_match = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading_match:
            flush_paragraph()
            blocks.append(heading_block(len(heading_match.group(1)), heading_match.group(2)))
            i += 1
            continue

        bullet_match = re.match(r"^[-*]\s+(.+)$", stripped)
        if bullet_match:
            flush_paragraph()
            text = bullet_match.group(1)
            blocks.append({"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": plain_text(text)}})
            i += 1
            continue

        numbered_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if numbered_match:
            flush_paragraph()
            text = numbered_match.group(1)
            blocks.append({"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": plain_text(text)}})
            i += 1
            continue

        paragraph.append(stripped)
        i += 1

    flush_paragraph()
    return blocks


def property_payload(prop: dict[str, Any], value: Any) -> dict[str, Any] | None:
    if value is None or value == "":
        return None
    prop_type = prop.get("type")
    if prop_type == "title":
        return {"title": plain_text(str(value))}
    if prop_type == "rich_text":
        return {"rich_text": plain_text(str(value))}
    if prop_type == "select":
        return {"select": {"name": str(value)}}
    if prop_type == "multi_select":
        if isinstance(value, str):
            items = [item.strip() for item in value.split(",") if item.strip()]
        else:
            items = [str(item) for item in value]
        return {"multi_select": [{"name": item} for item in items]}
    if prop_type == "date":
        return {"date": {"start": str(value)}}
    if prop_type == "url":
        return {"url": str(value)}
    if prop_type == "email":
        return {"email": str(value)}
    if prop_type == "phone_number":
        return {"phone_number": str(value)}
    if prop_type == "checkbox":
        return {"checkbox": bool(value)}
    return None


def build_properties(
    schema: dict[str, Any],
    args: argparse.Namespace,
    config: dict[str, Any],
    *,
    include_defaults: bool = True,
) -> dict[str, Any]:
    values = {
        "title": args.title,
        "status": args.status or (config.get("default_status", "Draft") if include_defaults else None),
        "type": args.type if args.type is not None else ("Post" if include_defaults else None),
        "category": args.category,
        "tags": args.tags,
        "slug": args.slug,
        "summary": args.summary,
        "date": args.date,
    }
    payload: dict[str, Any] = {}
    for name, prop in schema.items():
        if name in values:
            value = values[name]
            encoded = property_payload(prop, value)
            if encoded is not None:
                payload[name] = encoded
    return payload


def schema_from_page(client: NotionClient, page: dict[str, Any]) -> dict[str, Any]:
    parent = page.get("parent", {})
    parent_type = parent.get("type")
    if parent_type == "data_source_id":
        return client.get_data_source(parent["data_source_id"])["properties"]
    if parent_type == "database_id":
        return client.get_database(parent["database_id"])["properties"]
    return DEFAULT_SCHEMA


def append_children_in_chunks(client: NotionClient, block_id: str, children: list[dict[str, Any]]) -> None:
    for index in range(0, len(children), 100):
        client.append_block_children(block_id, children[index : index + 100])


def archive_existing_children(client: NotionClient, block_id: str) -> int:
    archived = 0
    cursor = None
    while True:
        result = client.list_block_children(block_id, cursor)
        for child in result.get("results", []):
            client.delete_block(child["id"])
            archived += 1
        if not result.get("has_more"):
            return archived
        cursor = result.get("next_cursor")


def resolve_parent_and_schema(
    client: NotionClient,
    database_or_url: str,
    data_source_id: str | None,
) -> tuple[dict[str, str], dict[str, Any]]:
    if data_source_id:
        resolved_data_source_id = parse_notion_id(data_source_id)
        data_source = client.get_data_source(resolved_data_source_id)
        return {"type": "data_source_id", "data_source_id": resolved_data_source_id}, data_source["properties"]

    if database_or_url.strip().startswith("collection://"):
        resolved_data_source_id = parse_notion_id(database_or_url)
        data_source = client.get_data_source(resolved_data_source_id)
        return {"type": "data_source_id", "data_source_id": resolved_data_source_id}, data_source["properties"]

    database_id = parse_notion_id(database_or_url)
    database = client.get_database(database_id)
    data_sources = database.get("data_sources") or []
    if data_sources:
        resolved_data_source_id = data_sources[0]["id"]
        data_source = client.get_data_source(resolved_data_source_id)
        return {"type": "data_source_id", "data_source_id": resolved_data_source_id}, data_source["properties"]

    # Legacy API fallback for older Notion-Version behavior.
    return {"database_id": database_id}, database["properties"]


def prompt_missing(args: argparse.Namespace, config: dict[str, Any]) -> None:
    if not args.database_id and not getattr(args, "data_source_id", None):
        suggested = config.get("last_database_id", "")
        prompt = "Notion database/data source ID or URL"
        if suggested:
            prompt += f" [{suggested}]"
        value = input(f"{prompt}: ").strip()
        args.database_id = value or suggested
    if not args.title:
        args.title = input("Title: ").strip()
    if not args.body_file and not args.body:
        print("Paste article Markdown. End with Ctrl-D:")
        args.body = sys.stdin.read()


def get_body(args: argparse.Namespace) -> str:
    if args.body_file:
        return Path(args.body_file).read_text(encoding="utf-8")
    body = args.body or ""
    if "\\n" in body and "\n" not in body:
        body = body.replace("\\n", "\n").replace("\\t", "\t")
    return body


def command_publish(args: argparse.Namespace) -> int:
    read_env_file()
    config = load_config()
    prompt_missing(args, config)

    target_input = args.data_source_id or args.database_id
    database_id = parse_notion_id(target_input)
    if args.save_database:
        config["last_database_id"] = database_id
        save_config(config)

    token = args.token or os.environ.get("NOTION_TOKEN")
    if token:
        client = NotionClient(token)
        parent, schema = resolve_parent_and_schema(client, args.database_id, args.data_source_id)
    elif args.dry_run:
        schema = DEFAULT_SCHEMA
        if args.data_source_id or target_input.strip().startswith("collection://"):
            parent = {"type": "data_source_id", "data_source_id": parse_notion_id(target_input)}
        else:
            parent = {"database_id": database_id}
    else:
        raise SystemExit("Missing NOTION_TOKEN. Set it in the environment or ~/.notion_publish/.env.")

    properties = build_properties(schema, args, config, include_defaults=True)
    body = get_body(args)
    children = markdown_to_blocks(body)
    if not children:
        children = [paragraph_block("")]

    payload: dict[str, Any] = {
        "parent": parent,
        "properties": properties,
        "children": children[:100],
    }
    if args.cover:
        payload["cover"] = {"type": "external", "external": {"url": args.cover}}

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    client = NotionClient(token)
    page = client.create_page(payload)
    print(json.dumps({"id": page["id"], "url": page.get("url")}, indent=2, ensure_ascii=False))
    return 0


def command_update(args: argparse.Namespace) -> int:
    read_env_file()
    config = load_config()
    token = args.token or os.environ.get("NOTION_TOKEN")
    page_id = parse_notion_id(args.page_id)
    body = get_body(args)
    children = markdown_to_blocks(body) if body else []

    if args.dry_run:
        properties = build_properties(DEFAULT_SCHEMA, args, config, include_defaults=False)
        payload: dict[str, Any] = {}
        if properties:
            payload["properties"] = properties
        if args.cover:
            payload["cover"] = {"type": "external", "external": {"url": args.cover}}
        print(json.dumps({"page_id": page_id, "mode": args.mode, "page_update": payload, "children": children}, indent=2, ensure_ascii=False))
        return 0

    if not token:
        raise SystemExit("Missing NOTION_TOKEN. Set it in the environment or ~/.notion_publish/.env.")

    client = NotionClient(token)
    page = client.get_page(page_id)
    schema = schema_from_page(client, page)
    properties = build_properties(schema, args, config, include_defaults=False)

    page_payload: dict[str, Any] = {}
    if properties:
        page_payload["properties"] = properties
    if args.cover:
        page_payload["cover"] = {"type": "external", "external": {"url": args.cover}}
    if page_payload:
        client.update_page(page_id, page_payload)

    archived = 0
    if children:
        if args.mode == "replace":
            archived = archive_existing_children(client, page_id)
        append_children_in_chunks(client, page_id, children)

    print(json.dumps({"id": page_id, "url": page.get("url"), "mode": args.mode, "archived_children": archived, "appended_children": len(children)}, indent=2, ensure_ascii=False))
    return 0


def command_scan_drafts(args: argparse.Namespace) -> int:
    read_env_file()
    config = load_config()
    if not args.database_id and not args.data_source_id:
        args.database_id = input("Notion database/data source ID or URL: ").strip() or config.get("last_database_id", "")
    token = args.token or os.environ.get("NOTION_TOKEN")
    if not token:
        raise SystemExit("Missing NOTION_TOKEN. Set it in the environment or ~/.notion_publish/.env.")
    client = NotionClient(token)
    parent, _schema = resolve_parent_and_schema(client, args.database_id or "", args.data_source_id)
    target_id = parent.get("data_source_id") or parent.get("database_id")
    client = NotionClient(token)
    if parent.get("data_source_id"):
        result = client.query_data_source(target_id, {"filter": {"property": "status", "select": {"equals": "Draft"}}, "page_size": 100})
    else:
        result = client.query_database(target_id, {"filter": {"property": "status", "select": {"equals": "Draft"}}, "page_size": 100})
    rows = []
    for page in result.get("results", []):
        props = page.get("properties", {})
        title_prop = props.get("title", {}).get("title", [])
        title = "".join(part.get("plain_text", "") for part in title_prop) or page["id"]
        rows.append({"id": page["id"], "title": title, "url": page.get("url")})
    print(json.dumps(rows, indent=2, ensure_ascii=False))
    return 0


def title_from_page(page: dict[str, Any]) -> str:
    props = page.get("properties", {})
    title_prop = props.get("title", {}).get("title", [])
    return "".join(part.get("plain_text", "") for part in title_prop) or page.get("id", "")


def simple_prop_value(prop: dict[str, Any]) -> Any:
    prop_type = prop.get("type")
    value = prop.get(prop_type, None)
    if prop_type == "title":
        return "".join(part.get("plain_text", "") for part in value or [])
    if prop_type == "rich_text":
        return "".join(part.get("plain_text", "") for part in value or [])
    if prop_type == "select":
        return (value or {}).get("name")
    if prop_type == "multi_select":
        return [item.get("name") for item in value or []]
    if prop_type == "date":
        return (value or {}).get("start")
    if prop_type in {"url", "email", "phone_number", "checkbox", "number"}:
        return value
    return None


def row_from_page(page: dict[str, Any]) -> dict[str, Any]:
    props = page.get("properties", {})
    return {
        "id": page.get("id"),
        "title": title_from_page(page),
        "status": simple_prop_value(props.get("status", {})),
        "type": simple_prop_value(props.get("type", {})),
        "category": simple_prop_value(props.get("category", {})),
        "slug": simple_prop_value(props.get("slug", {})),
        "date": simple_prop_value(props.get("date", {})),
        "url": page.get("url"),
    }


def page_matches_query(page: dict[str, Any], query: str) -> bool:
    if not query:
        return True
    needle = query.casefold()
    props = page.get("properties", {})
    haystack_parts = [title_from_page(page)]
    for name in ["summary", "slug", "status", "type", "category", "tags"]:
        value = simple_prop_value(props.get(name, {}))
        if isinstance(value, list):
            haystack_parts.extend(str(item) for item in value)
        elif value is not None:
            haystack_parts.append(str(value))
    return needle in " ".join(haystack_parts).casefold()


def build_search_filter(args: argparse.Namespace) -> dict[str, Any] | None:
    conditions = []
    if args.status:
        conditions.append({"property": "status", "select": {"equals": args.status}})
    if args.type:
        conditions.append({"property": "type", "select": {"equals": args.type}})
    if args.category:
        conditions.append({"property": "category", "select": {"equals": args.category}})
    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"and": conditions}


def command_search(args: argparse.Namespace) -> int:
    read_env_file()
    config = load_config()
    if not args.database_id and not args.data_source_id:
        args.database_id = input("Notion database/data source ID or URL: ").strip() or config.get("last_database_id", "")
    token = args.token or os.environ.get("NOTION_TOKEN")
    if not token:
        raise SystemExit("Missing NOTION_TOKEN. Set it in the environment or ~/.notion_publish/.env.")

    client = NotionClient(token)
    parent, _schema = resolve_parent_and_schema(client, args.database_id or "", args.data_source_id)
    target_id = parent.get("data_source_id") or parent.get("database_id")
    payload: dict[str, Any] = {"page_size": min(max(args.page_size, 1), 100)}
    filter_payload = build_search_filter(args)
    if filter_payload:
        payload["filter"] = filter_payload
    if args.sort_by_date:
        payload["sorts"] = [{"property": "date", "direction": "descending"}]

    rows = []
    cursor = None
    while True:
        request_payload = dict(payload)
        if cursor:
            request_payload["start_cursor"] = cursor
        if parent.get("data_source_id"):
            result = client.query_data_source(target_id, request_payload)
        else:
            result = client.query_database(target_id, request_payload)
        for page in result.get("results", []):
            if page_matches_query(page, args.query or ""):
                rows.append(row_from_page(page))
                if len(rows) >= args.limit:
                    print(json.dumps(rows, indent=2, ensure_ascii=False))
                    return 0
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")

    print(json.dumps(rows, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Publish articles to Notion without MCP.")
    parser.add_argument("--token", help="Notion integration token. Defaults to NOTION_TOKEN.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    publish = subparsers.add_parser("publish", help="Create a Notion database page.")
    publish.add_argument("--database-id", help="Notion database ID or URL. Prompted when omitted.")
    publish.add_argument("--data-source-id", help="Notion data source ID or collection:// URL. Overrides --database-id parent resolution.")
    publish.add_argument("--save-database", action="store_true", help="Save this database as a local prompt default.")
    publish.add_argument("--title", help="Article title. Prompted when omitted.")
    publish.add_argument("--body-file", help="Markdown file to publish.")
    publish.add_argument("--body", help="Markdown body string.")
    publish.add_argument("--status", help="Notion status option. Defaults to config default_status.")
    publish.add_argument("--type", default="Post", help="Notion type option.")
    publish.add_argument("--category", help="Notion category option.")
    publish.add_argument("--tags", help="Comma-separated Notion tag options.")
    publish.add_argument("--slug", help="Article slug.")
    publish.add_argument("--summary", help="Article summary.")
    publish.add_argument("--date", help="Publish date, YYYY-MM-DD.")
    publish.add_argument("--cover", help="External cover image URL.")
    publish.add_argument("--dry-run", action="store_true", help="Print the Notion API payload without creating a page.")
    publish.set_defaults(func=command_publish)

    update = subparsers.add_parser("update", help="Update an existing Notion page.")
    update.add_argument("--page-id", required=True, help="Notion page ID or URL.")
    update.add_argument("--mode", choices=["replace", "append"], default="replace", help="Replace existing content or append new content.")
    update.add_argument("--title", help="Article title.")
    update.add_argument("--body-file", help="Markdown file to write.")
    update.add_argument("--body", help="Markdown body string.")
    update.add_argument("--status", help="Notion status option.")
    update.add_argument("--type", help="Notion type option.")
    update.add_argument("--category", help="Notion category option.")
    update.add_argument("--tags", help="Comma-separated Notion tag options.")
    update.add_argument("--slug", help="Article slug.")
    update.add_argument("--summary", help="Article summary.")
    update.add_argument("--date", help="Publish date, YYYY-MM-DD.")
    update.add_argument("--cover", help="External cover image URL.")
    update.add_argument("--dry-run", action="store_true", help="Print the Notion API payload without updating the page.")
    update.set_defaults(func=command_update)

    scan = subparsers.add_parser("scan-drafts", help="List Draft pages in a database.")
    scan.add_argument("--database-id", help="Notion database ID or URL. Prompted when omitted.")
    scan.add_argument("--data-source-id", help="Notion data source ID or collection:// URL. Overrides --database-id parent resolution.")
    scan.set_defaults(func=command_scan_drafts)

    search = subparsers.add_parser("search", help="Search/list pages in a Notion database and return page IDs.")
    search.add_argument("--database-id", help="Notion database ID or URL. Prompted when omitted.")
    search.add_argument("--data-source-id", help="Notion data source ID or collection:// URL. Overrides --database-id parent resolution.")
    search.add_argument("--query", default="", help="Keyword filter applied locally to title, summary, slug, status, type, category, and tags.")
    search.add_argument("--status", help="Filter by status select option.")
    search.add_argument("--type", help="Filter by type select option.")
    search.add_argument("--category", help="Filter by category select option.")
    search.add_argument("--limit", type=int, default=25, help="Maximum matching rows to print.")
    search.add_argument("--page-size", type=int, default=100, help="Notion API query page size.")
    search.add_argument("--sort-by-date", action="store_true", help="Sort by date descending when the database has a date property.")
    search.set_defaults(func=command_search)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (NotionError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
