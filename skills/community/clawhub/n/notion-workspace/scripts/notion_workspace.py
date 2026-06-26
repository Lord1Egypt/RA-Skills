#!/usr/bin/env python3
"""Notion Workspace CLI — databases, pages, blocks, search."""

import os
import sys
import json
import argparse
import requests

BASE = "https://api.notion.com/v1"
VERSION = "2022-06-28"


def get_headers():
    key = os.environ.get("NOTION_API_KEY")
    if not key:
        print(json.dumps({
            "error": "NOTION_API_KEY not set",
            "setup": "export NOTION_API_KEY='secret_xxxx...'"
        }))
        sys.exit(1)
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Notion-Version": VERSION
    }


def api(method, path, **kwargs):
    r = requests.request(method, BASE + path, headers=get_headers(), **kwargs)
    if r.status_code in (200, 201):
        return r.json()
    print(json.dumps({"error": r.status_code, "detail": r.text}))
    sys.exit(1)


def get_db_id():
    db_id = os.environ.get("NOTION_DATABASE_ID")
    if not db_id:
        print(json.dumps({"error": "NOTION_DATABASE_ID not set — pass --db-id or set env var"}))
        sys.exit(1)
    return db_id


def extract_title(props):
    """Extract plain text title from Notion properties."""
    for k, v in props.items():
        if v.get("type") == "title":
            texts = v.get("title", [])
            return "".join(t.get("plain_text", "") for t in texts)
    return ""


# ── DATABASES ───────────────────────────────────────────

def db_query(args):
    db_id = args.db_id or get_db_id()
    body = {"page_size": 50}
    if args.filter_prop and args.filter_value:
        body["filter"] = {
            "property": args.filter_prop,
            "rich_text": {"contains": args.filter_value}
        }
    r = api("POST", f"/databases/{db_id}/query", json=body)
    results = []
    for page in r.get("results", []):
        results.append({
            "id": page["id"],
            "title": extract_title(page.get("properties", {})),
            "url": page.get("url"),
            "created": page.get("created_time"),
            "last_edited": page.get("last_edited_time")
        })
    print(json.dumps(results, indent=2))


def db_create(args):
    db_id = args.db_id or get_db_id()
    extra_props = json.loads(args.props) if args.props else {}
    properties = {
        "Name": {"title": [{"text": {"content": args.title}}]}
    }
    for k, v in extra_props.items():
        properties[k] = {"rich_text": [{"text": {"content": str(v)}}]}
    r = api("POST", "/pages", json={"parent": {"database_id": db_id}, "properties": properties})
    print(json.dumps({"id": r["id"], "url": r.get("url"), "title": args.title}, indent=2))


def db_update(args):
    extra_props = json.loads(args.props) if args.props else {}
    properties = {}
    for k, v in extra_props.items():
        properties[k] = {"rich_text": [{"text": {"content": str(v)}}]}
    r = api("PATCH", f"/pages/{args.page_id}", json={"properties": properties})
    print(json.dumps({"id": r["id"], "url": r.get("url"), "last_edited": r.get("last_edited_time")}, indent=2))


# ── PAGES ───────────────────────────────────────────────

def page_create(args):
    properties = {
        "title": {"title": [{"text": {"content": args.title}}]}
    }
    children = []
    if args.content:
        children.append({
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": args.content}}]}
        })
    body = {"parent": {"page_id": args.parent_id}, "properties": properties}
    if children:
        body["children"] = children
    r = api("POST", "/pages", json=body)
    print(json.dumps({"id": r["id"], "url": r.get("url")}, indent=2))


def page_read(args):
    r = api("GET", f"/pages/{args.page_id}")
    blocks = api("GET", f"/blocks/{args.page_id}/children?page_size=10")
    content_preview = []
    for b in blocks.get("results", []):
        btype = b.get("type", "")
        texts = b.get(btype, {}).get("rich_text", [])
        text = "".join(t.get("plain_text", "") for t in texts)
        if text:
            content_preview.append({"type": btype, "text": text[:200]})
    print(json.dumps({
        "id": r["id"],
        "title": extract_title(r.get("properties", {})),
        "url": r.get("url"),
        "created": r.get("created_time"),
        "last_edited": r.get("last_edited_time"),
        "content_preview": content_preview[:5]
    }, indent=2))


def page_update(args):
    properties = {}
    if args.title:
        properties["title"] = {"title": [{"text": {"content": args.title}}]}
    r = api("PATCH", f"/pages/{args.page_id}", json={"properties": properties})
    print(json.dumps({"id": r["id"], "url": r.get("url")}, indent=2))


def page_archive(args):
    r = api("PATCH", f"/pages/{args.page_id}", json={"archived": True})
    print(json.dumps({"id": r["id"], "archived": True}))


# ── BLOCKS ──────────────────────────────────────────────

def blocks_get(args):
    r = api("GET", f"/blocks/{args.block_id}/children?page_size=50")
    results = []
    for b in r.get("results", []):
        btype = b.get("type", "")
        texts = b.get(btype, {}).get("rich_text", [])
        text = "".join(t.get("plain_text", "") for t in texts)
        results.append({"id": b["id"], "type": btype, "text": text[:300]})
    print(json.dumps(results, indent=2))


def blocks_append(args):
    btype = args.type
    block = {"object": "block", "type": btype}

    rich_text = [{"type": "text", "text": {"content": args.text}}]

    if btype == "code":
        block[btype] = {
            "rich_text": rich_text,
            "language": args.language or "plain text"
        }
    elif btype == "to_do":
        block[btype] = {"rich_text": rich_text, "checked": False}
    elif btype in ("heading_1", "heading_2", "heading_3"):
        block[btype] = {"rich_text": rich_text}
    else:
        block[btype] = {"rich_text": rich_text}

    r = api("PATCH", f"/blocks/{args.block_id}/children", json={"children": [block]})
    added = r.get("results", [{}])
    print(json.dumps({"appended": len(added), "type": btype, "text": args.text[:100]}, indent=2))


# ── SEARCH ──────────────────────────────────────────────

def search(args):
    body = {"query": args.query, "page_size": 20}
    if args.filter:
        body["filter"] = {"value": args.filter, "property": "object"}
    r = api("POST", "/search", json=body)
    results = []
    for obj in r.get("results", []):
        obj_type = obj.get("object")
        title = ""
        if obj_type == "page":
            title = extract_title(obj.get("properties", {}))
            if not title:
                # fallback: try title property directly
                t = obj.get("properties", {}).get("title", {}).get("title", [])
                title = "".join(x.get("plain_text", "") for x in t)
        elif obj_type == "database":
            title_list = obj.get("title", [])
            title = "".join(t.get("plain_text", "") for t in title_list)
        results.append({
            "id": obj["id"],
            "type": obj_type,
            "title": title,
            "url": obj.get("url"),
            "last_edited": obj.get("last_edited_time")
        })
    print(json.dumps(results, indent=2))


# ── CLI ─────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Notion Workspace CLI")
    sub = p.add_subparsers(dest="cmd")

    # db-query
    dq = sub.add_parser("db-query")
    dq.add_argument("--db-id", dest="db_id")
    dq.add_argument("--filter-prop", dest="filter_prop")
    dq.add_argument("--filter-value", dest="filter_value")

    # db-create
    dc = sub.add_parser("db-create")
    dc.add_argument("--title", required=True)
    dc.add_argument("--db-id", dest="db_id")
    dc.add_argument("--props", help='JSON string: {"Status": "To Do"}')

    # db-update
    du = sub.add_parser("db-update")
    du.add_argument("--page-id", required=True, dest="page_id")
    du.add_argument("--props", required=True, help='JSON string of properties to update')

    # page-create
    pc = sub.add_parser("page-create")
    pc.add_argument("--parent-id", required=True, dest="parent_id")
    pc.add_argument("--title", required=True)
    pc.add_argument("--content")

    # page-read
    pr = sub.add_parser("page-read")
    pr.add_argument("--page-id", required=True, dest="page_id")

    # page-update
    pu = sub.add_parser("page-update")
    pu.add_argument("--page-id", required=True, dest="page_id")
    pu.add_argument("--title")

    # page-archive
    pa = sub.add_parser("page-archive")
    pa.add_argument("--page-id", required=True, dest="page_id")

    # blocks-get
    bg = sub.add_parser("blocks-get")
    bg.add_argument("--block-id", required=True, dest="block_id")

    # blocks-append
    ba = sub.add_parser("blocks-append")
    ba.add_argument("--block-id", required=True, dest="block_id")
    ba.add_argument("--text", required=True)
    ba.add_argument("--type", default="paragraph",
                    choices=["paragraph", "heading_1", "heading_2", "heading_3",
                             "bulleted_list_item", "numbered_list_item", "to_do", "code", "quote"])
    ba.add_argument("--language", default="plain text")

    # search
    sr = sub.add_parser("search")
    sr.add_argument("--query", required=True)
    sr.add_argument("--filter", choices=["page", "database"])

    args = p.parse_args()
    dispatch = {
        "db-query": db_query, "db-create": db_create, "db-update": db_update,
        "page-create": page_create, "page-read": page_read,
        "page-update": page_update, "page-archive": page_archive,
        "blocks-get": blocks_get, "blocks-append": blocks_append,
        "search": search,
    }
    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
