#!/usr/bin/env python3
"""Unified CLI for the Image Vault — import, search, describe, serve."""

import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from image_db import get_db, init_db, search_images, get_stats, update_image, get_image_by_id


def cmd_import(args):
    from image_import import import_single, import_directory
    init_db()
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
    auto_tag = getattr(args, "auto_tag", False)
    if os.path.isdir(args.path):
        result = import_directory(args.path, source=args.source, category=args.category,
                                  description=args.description, tags=tags, copy=not args.move)
        print(f"Imported: {result['imported']}, Skipped: {result['skipped']}, Errors: {result['errors']}")
    else:
        result = import_single(args.path, source=args.source, category=args.category,
                               description=args.description, tags=tags, copy=not args.move,
                               auto_tag=auto_tag)
        print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_search(args):
    init_db()
    conn = get_db()
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
    results = search_images(conn, query=args.query, category=args.category, source=args.source,
                            date_from=args.date_from, date_to=args.date_to, tags=tags, limit=args.limit)
    conn.close()
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"Found {len(results)} image(s):\n")
        for img in results:
            img_tags = ", ".join(json.loads(img.get("tags", "[]"))) if img.get("tags") else ""
            date = (img.get("taken_at") or img.get("created_at", ""))[:10]
            print(f"  [{img['id']}] {img['filename']}")
            print(f"      {img['category']} | {img['source']} | {date}")
            if img.get("description"):
                print(f"      {img['description'][:100]}")
            if img_tags:
                print(f"      Tags: {img_tags}")
            print()


def cmd_describe(args):
    """Update description and tags for an image."""
    init_db()
    conn = get_db()
    kwargs = {}
    if args.description:
        kwargs["description"] = args.description
    if args.tags:
        kwargs["tags"] = [t.strip() for t in args.tags.split(",")]
    if args.category:
        kwargs["category"] = args.category
    if kwargs:
        update_image(conn, args.id, **kwargs)
        print(f"Updated image [{args.id}]")
    img = get_image_by_id(conn, args.id)
    if img:
        print(json.dumps(img, ensure_ascii=False, indent=2))
    conn.close()


def cmd_stats(args):
    init_db()
    conn = get_db()
    stats = get_stats(conn)
    conn.close()
    print(f"Total: {stats['total']} images")
    print("\nCategories:")
    for cat, count in stats["categories"].items():
        print(f"  {cat}: {count}")
    print("\nSources:")
    for src, count in stats["sources"].items():
        print(f"  {src}: {count}")


def cmd_album(args):
    from image_db import create_album, list_albums, get_album_images, add_to_album
    init_db()
    conn = get_db()
    sub = args.album_cmd

    if sub == "create":
        aid = create_album(conn, args.name, args.description or "")
        print(json.dumps({"id": aid, "name": args.name}, ensure_ascii=False))
    elif sub == "list":
        albums = list_albums(conn)
        for a in albums:
            print(f"  [{a['id']}] {a['name']} ({a['image_count']} photos) — {a.get('description','')}")
    elif sub == "add":
        for img_id in args.image_ids:
            add_to_album(conn, args.album_id, img_id)
        print(f"Added {len(args.image_ids)} image(s) to album {args.album_id}")
    elif sub == "show":
        images = get_album_images(conn, args.album_id)
        for img in images:
            print(f"  [{img['id']}] {img['filename']} — {img.get('description','')[:50]}")
    conn.close()


def cmd_serve(args):
    from web_server import app, init_db as web_init
    web_init()
    print(f"Image Vault Gallery: http://localhost:{args.port}")
    host = os.environ.get("IMAGE_VAULT_HOST", "127.0.0.1")
    app.run(host=host, port=args.port, debug=False)


def main():
    parser = argparse.ArgumentParser(description="Image Vault CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_import = sub.add_parser("import", help="Import images")
    p_import.add_argument("path", help="File or directory")
    p_import.add_argument("--source", "-s")
    p_import.add_argument("--category", "-c")
    p_import.add_argument("--description", "-d")
    p_import.add_argument("--tags", "-t")
    p_import.add_argument("--move", action="store_true")
    p_import.add_argument("--auto-tag", action="store_true", dest="auto_tag",
                          help="AI auto-recognize description/tags on import")

    p_search = sub.add_parser("search", help="Search images")
    p_search.add_argument("query", nargs="?")
    p_search.add_argument("--category", "-c")
    p_search.add_argument("--source", "-s")
    p_search.add_argument("--from", dest="date_from")
    p_search.add_argument("--to", dest="date_to")
    p_search.add_argument("--tags", "-t")
    p_search.add_argument("--limit", "-l", type=int, default=50)
    p_search.add_argument("--json", action="store_true")

    p_desc = sub.add_parser("describe", help="Update image description/tags")
    p_desc.add_argument("id", type=int)
    p_desc.add_argument("--description", "-d")
    p_desc.add_argument("--tags", "-t")
    p_desc.add_argument("--category", "-c")

    sub.add_parser("stats", help="Vault statistics")

    p_album = sub.add_parser("album", help="Manage albums")
    album_sub = p_album.add_subparsers(dest="album_cmd")
    pa_create = album_sub.add_parser("create")
    pa_create.add_argument("name")
    pa_create.add_argument("--description", "-d", default="")
    pa_list = album_sub.add_parser("list")
    pa_add = album_sub.add_parser("add")
    pa_add.add_argument("album_id", type=int)
    pa_add.add_argument("image_ids", type=int, nargs="+")
    pa_show = album_sub.add_parser("show")
    pa_show.add_argument("album_id", type=int)

    p_serve = sub.add_parser("serve", help="Start web gallery")
    p_serve.add_argument("--port", "-p", type=int, default=9876)

    args = parser.parse_args()
    cmds = {"import": cmd_import, "search": cmd_search, "describe": cmd_describe,
            "stats": cmd_stats, "album": cmd_album, "serve": cmd_serve}

    if args.cmd in cmds:
        cmds[args.cmd](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
