#!/usr/bin/env python3
"""
Notion API tool for OpenClaw.
Provides search, read, create, update, query operations via CLI.
API key is read from openclaw.json → skills.entries.notion.apiKey or NOTION_API_KEY env var.
"""

import argparse
import json
import os
import pathlib
import sys
import time
import urllib.request
import urllib.error

NOTION_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2025-09-03"
MAX_RETRIES = 3


def load_api_key():
    """Load Notion API key from openclaw.json or env.

    Priority: openclaw.json (notion-pro → notion) > NOTION_API_KEY env var.
    Config file takes precedence to prevent stale env vars from overriding
    freshly updated config values.
    """
    # Try openclaw.json first (authoritative source)
    config_path = pathlib.Path.home() / ".openclaw" / "openclaw.json"
    if config_path.exists():
        try:
            cfg = json.loads(config_path.read_text(encoding="utf-8"))
            entries = cfg.get("skills", {}).get("entries", {})
            # Check both "notion-pro" and "notion" entries
            for skill_name in ("notion-pro", "notion"):
                key = entries.get(skill_name, {}).get("apiKey")
                if key:
                    return key.strip()
        except Exception:
            pass

    # Fall back to env var
    key = os.environ.get("NOTION_API_KEY")
    if key:
        return key.strip()

    return None


def _headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _request(method: str, url: str, key: str, body: dict = None) -> dict:
    """Make an HTTP request to Notion API with automatic 429 retry."""
    data = json.dumps(body).encode("utf-8") if body else None

    for attempt in range(MAX_RETRIES + 1):
        req = urllib.request.Request(
            url,
            data=data,
            headers=_headers(key),
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            # Handle 429 rate limit with retry
            if e.code == 429 and attempt < MAX_RETRIES:
                retry_after = int(e.headers.get("Retry-After", 1))
                print(f"[rate-limited] waiting {retry_after}s (attempt {attempt + 1}/{MAX_RETRIES})", file=sys.stderr)
                e.read()  # drain response
                time.sleep(retry_after)
                continue

            body_text = e.read().decode("utf-8", errors="replace") if e.fp else ""
            try:
                err = json.loads(body_text)
            except Exception:
                err = {"raw": body_text[:500]}
            raise SystemExit(
                json.dumps({"error": True, "status": e.code, "message": str(e), "details": err}, ensure_ascii=False)
            )


def _simplify_search_results(results: list) -> list:
    """Extract simplified info from search result items."""
    items = []
    for r in results:
        obj_type = r.get("object", "unknown")
        title_parts = []

        if obj_type == "page":
            props = r.get("properties", {})
            for pname, pval in props.items():
                if pval.get("type") == "title":
                    for t in pval.get("title", []):
                        title_parts.append(t.get("plain_text", ""))
        elif obj_type in ("database", "data_source"):
            for t in r.get("title", []):
                title_parts.append(t.get("plain_text", ""))

        items.append({
            "id": r.get("id"),
            "object": obj_type,
            "title": "".join(title_parts) or "(untitled)",
            "url": r.get("url"),
            "last_edited": r.get("last_edited_time"),
        })
    return items


def cmd_search(key: str, query: str, filter_type: str = None,
               page_size: int = 10, start_cursor: str = None,
               fetch_all: bool = False) -> dict:
    """Search pages and data sources with pagination support."""
    payload = {"query": query, "page_size": min(page_size, 100)}
    if filter_type in ("page", "database", "data_source"):
        # API 2025-09-03: "database" renamed to "data_source"
        api_filter = "data_source" if filter_type == "database" else filter_type
        payload["filter"] = {"value": api_filter, "property": "object"}
    if start_cursor:
        payload["start_cursor"] = start_cursor

    result = _request("POST", f"{NOTION_BASE}/search", key, payload)
    all_items = _simplify_search_results(result.get("results", []))

    # Auto-paginate if --all
    if fetch_all:
        while result.get("has_more") and result.get("next_cursor"):
            payload["start_cursor"] = result["next_cursor"]
            time.sleep(0.35)  # respect rate limit
            result = _request("POST", f"{NOTION_BASE}/search", key, payload)
            all_items.extend(_simplify_search_results(result.get("results", [])))

    return {
        "query": query,
        "results": all_items,
        "total": len(all_items),
        "has_more": result.get("has_more", False),
        "next_cursor": result.get("next_cursor"),
    }


def cmd_get_page(key: str, page_id: str) -> dict:
    """Get page metadata."""
    return _request("GET", f"{NOTION_BASE}/pages/{page_id}", key)


def _simplify_block(b: dict) -> dict:
    """Extract simplified info from a block object."""
    btype = b.get("type", "unknown")
    block_info = {"id": b["id"], "type": btype}

    content_obj = b.get(btype, {})
    if "rich_text" in content_obj:
        texts = [t.get("plain_text", "") for t in content_obj["rich_text"]]
        block_info["text"] = "".join(texts)
    elif "text" in content_obj:
        texts = [t.get("plain_text", "") for t in content_obj["text"]]
        block_info["text"] = "".join(texts)

    if b.get("has_children"):
        block_info["has_children"] = True

    return block_info


def cmd_get_blocks(key: str, block_id: str, page_size: int = 100,
                   start_cursor: str = None, recursive: bool = False,
                   _depth: int = 0) -> dict:
    """Get child blocks (page content) with optional recursion."""
    url = f"{NOTION_BASE}/blocks/{block_id}/children?page_size={page_size}"
    if start_cursor:
        url += f"&start_cursor={start_cursor}"

    result = _request("GET", url, key)

    blocks = []
    for b in result.get("results", []):
        block_info = _simplify_block(b)

        # Recursively fetch children if requested
        if recursive and b.get("has_children") and _depth < 5:
            time.sleep(0.35)
            child_result = cmd_get_blocks(key, b["id"], page_size,
                                          recursive=True, _depth=_depth + 1)
            block_info["children"] = child_result.get("blocks", [])

        blocks.append(block_info)

    # Auto-paginate within same level
    while result.get("has_more") and result.get("next_cursor"):
        time.sleep(0.35)
        url = f"{NOTION_BASE}/blocks/{block_id}/children?page_size={page_size}&start_cursor={result['next_cursor']}"
        result = _request("GET", url, key)
        for b in result.get("results", []):
            block_info = _simplify_block(b)
            if recursive and b.get("has_children") and _depth < 5:
                time.sleep(0.35)
                child_result = cmd_get_blocks(key, b["id"], page_size,
                                              recursive=True, _depth=_depth + 1)
                block_info["children"] = child_result.get("blocks", [])
            blocks.append(block_info)

    return {"blocks": blocks, "total": len(blocks), "has_more": False}


def _simplify_page_properties(page: dict) -> dict:
    """Extract simplified properties from a page object."""
    item = {"id": page.get("id"), "url": page.get("url")}
    props = page.get("properties", {})
    simplified_props = {}
    for pname, pval in props.items():
        ptype = pval.get("type", "")
        if ptype == "title":
            simplified_props[pname] = "".join(t.get("plain_text", "") for t in pval.get("title", []))
        elif ptype == "rich_text":
            simplified_props[pname] = "".join(t.get("plain_text", "") for t in pval.get("rich_text", []))
        elif ptype == "select":
            sel = pval.get("select")
            simplified_props[pname] = sel.get("name") if sel else None
        elif ptype == "multi_select":
            simplified_props[pname] = [s.get("name") for s in pval.get("multi_select", [])]
        elif ptype == "number":
            simplified_props[pname] = pval.get("number")
        elif ptype == "checkbox":
            simplified_props[pname] = pval.get("checkbox")
        elif ptype == "date":
            d = pval.get("date")
            simplified_props[pname] = d.get("start") if d else None
        elif ptype == "url":
            simplified_props[pname] = pval.get("url")
        elif ptype == "email":
            simplified_props[pname] = pval.get("email")
        elif ptype == "status":
            s = pval.get("status")
            simplified_props[pname] = s.get("name") if s else None
        elif ptype == "phone_number":
            simplified_props[pname] = pval.get("phone_number")
        elif ptype == "relation":
            simplified_props[pname] = [r.get("id") for r in pval.get("relation", [])]
        elif ptype == "people":
            simplified_props[pname] = [p.get("id") for p in pval.get("people", [])]
        else:
            simplified_props[pname] = f"({ptype})"
    item["properties"] = simplified_props
    return item


def cmd_query_database(key: str, database_id: str, filter_json: str = None,
                       sorts_json: str = None, page_size: int = 50,
                       start_cursor: str = None, fetch_all: bool = False) -> dict:
    """Query a data source (database) with pagination support."""
    payload = {"page_size": min(page_size, 100)}

    if filter_json:
        payload["filter"] = json.loads(filter_json)
    if sorts_json:
        payload["sorts"] = json.loads(sorts_json)
    if start_cursor:
        payload["start_cursor"] = start_cursor

    # Try data_sources endpoint first (2025-09-03), fall back to databases
    try:
        result = _request("POST", f"{NOTION_BASE}/data_sources/{database_id}/query", key, payload)
    except SystemExit:
        result = _request("POST", f"{NOTION_BASE}/databases/{database_id}/query", key, payload)

    all_items = [_simplify_page_properties(p) for p in result.get("results", [])]

    # Auto-paginate if --all
    if fetch_all:
        while result.get("has_more") and result.get("next_cursor"):
            payload["start_cursor"] = result["next_cursor"]
            time.sleep(0.35)
            try:
                result = _request("POST", f"{NOTION_BASE}/data_sources/{database_id}/query", key, payload)
            except SystemExit:
                result = _request("POST", f"{NOTION_BASE}/databases/{database_id}/query", key, payload)
            all_items.extend([_simplify_page_properties(p) for p in result.get("results", [])])

    return {
        "database_id": database_id,
        "results": all_items,
        "total": len(all_items),
        "has_more": result.get("has_more", False),
        "next_cursor": result.get("next_cursor"),
    }


def cmd_create_page(key: str, parent_id: str, parent_type: str,
                    properties_json: str, children_json: str = None) -> dict:
    """Create a new page."""
    payload = {"properties": json.loads(properties_json)}

    if parent_type == "database":
        payload["parent"] = {"database_id": parent_id}
    else:
        payload["parent"] = {"page_id": parent_id}

    if children_json:
        payload["children"] = json.loads(children_json)

    result = _request("POST", f"{NOTION_BASE}/pages", key, payload)
    return {"id": result.get("id"), "url": result.get("url"), "created": True}


def cmd_update_page(key: str, page_id: str, properties_json: str) -> dict:
    """Update page properties."""
    payload = {"properties": json.loads(properties_json)}
    result = _request("PATCH", f"{NOTION_BASE}/pages/{page_id}", key, payload)
    return {"id": result.get("id"), "url": result.get("url"), "updated": True}


def cmd_append_blocks(key: str, block_id: str, children_json: str,
                      after_block_id: str = None) -> dict:
    """Append child blocks to a page/block, optionally after a specific block."""
    children = json.loads(children_json)
    payload = {"children": children}
    if after_block_id:
        payload["after"] = after_block_id
    result = _request("PATCH", f"{NOTION_BASE}/blocks/{block_id}/children", key, payload)
    new_blocks = [{"id": b.get("id"), "type": b.get("type")} for b in result.get("results", [])]
    # When using --after, API returns the new block(s) + all subsequent blocks;
    # report the actual number of blocks we appended, not the API result count
    return {"parent_id": block_id, "appended": len(children), "blocks": new_blocks[:len(children)]}


def cmd_delete_block(key: str, block_id: str) -> dict:
    """Archive (soft-delete) a block."""
    _request("DELETE", f"{NOTION_BASE}/blocks/{block_id}", key)
    return {"id": block_id, "archived": True}


def main():
    ap = argparse.ArgumentParser(description="Notion API tool for OpenClaw")
    sub = ap.add_subparsers(dest="command", required=True)

    # search
    p = sub.add_parser("search", help="Search pages and databases")
    p.add_argument("--query", required=True)
    p.add_argument("--filter", choices=["page", "database", "data_source"])
    p.add_argument("--page-size", type=int, default=10)
    p.add_argument("--start-cursor", help="Pagination cursor from previous response")
    p.add_argument("--all", action="store_true", dest="fetch_all",
                   help="Auto-paginate to fetch all results")

    # get-page
    p = sub.add_parser("get-page", help="Get page metadata")
    p.add_argument("--page-id", required=True)

    # get-blocks
    p = sub.add_parser("get-blocks", help="Get page/block children (content)")
    p.add_argument("--block-id", required=True)
    p.add_argument("--page-size", type=int, default=100)
    p.add_argument("--start-cursor", help="Pagination cursor")
    p.add_argument("--recursive", action="store_true",
                   help="Recursively fetch nested blocks (max depth 5)")

    # query-database
    p = sub.add_parser("query-database", help="Query a database/data source")
    p.add_argument("--database-id", required=True)
    p.add_argument("--filter", dest="filter_json", help="JSON filter object")
    p.add_argument("--sorts", dest="sorts_json", help="JSON sorts array")
    p.add_argument("--page-size", type=int, default=50)
    p.add_argument("--start-cursor", help="Pagination cursor from previous response")
    p.add_argument("--all", action="store_true", dest="fetch_all",
                   help="Auto-paginate to fetch all results")

    # create-page
    p = sub.add_parser("create-page", help="Create a new page")
    p.add_argument("--parent-id", required=True)
    p.add_argument("--parent-type", choices=["database", "page"], default="database")
    p.add_argument("--properties", required=True, help="JSON properties object")
    p.add_argument("--children", help="JSON children blocks array")

    # update-page
    p = sub.add_parser("update-page", help="Update page properties")
    p.add_argument("--page-id", required=True)
    p.add_argument("--properties", required=True, help="JSON properties object")

    # append-blocks
    p = sub.add_parser("append-blocks", help="Append blocks to a page")
    p.add_argument("--block-id", required=True)
    p.add_argument("--children", required=True, help="JSON children blocks array")
    p.add_argument("--after", help="Insert after this block ID instead of at end")

    # delete-block
    p = sub.add_parser("delete-block", help="Archive a block")
    p.add_argument("--block-id", required=True)

    args = ap.parse_args()

    key = load_api_key()
    if not key:
        raise SystemExit("Missing Notion API key. Set NOTION_API_KEY env var or configure skills.entries.notion.apiKey in openclaw.json")

    if args.command == "search":
        result = cmd_search(key, args.query, args.filter, args.page_size,
                            args.start_cursor, args.fetch_all)
    elif args.command == "get-page":
        result = cmd_get_page(key, args.page_id)
    elif args.command == "get-blocks":
        result = cmd_get_blocks(key, args.block_id, args.page_size,
                                args.start_cursor, args.recursive)
    elif args.command == "query-database":
        result = cmd_query_database(key, args.database_id, args.filter_json,
                                     args.sorts_json, args.page_size,
                                     args.start_cursor, args.fetch_all)
    elif args.command == "create-page":
        result = cmd_create_page(key, args.parent_id, args.parent_type,
                                  args.properties, args.children)
    elif args.command == "update-page":
        result = cmd_update_page(key, args.page_id, args.properties)
    elif args.command == "append-blocks":
        result = cmd_append_blocks(key, args.block_id, args.children, args.after)
    elif args.command == "delete-block":
        result = cmd_delete_block(key, args.block_id)
    else:
        raise SystemExit(f"Unknown command: {args.command}")

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
