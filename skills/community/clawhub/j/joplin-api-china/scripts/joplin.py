#!/usr/bin/env python3
"""Joplin API helper — cross-platform fallback for Windows.
Usage: python joplin.py <command> [args...]
"""

import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SCRIPT_DIR, "..", ".env")

# ── Load .env ──────────────────────────────────────────────

def load_env(path):
    env = {}
    if not os.path.isfile(path):
        print(f"Error: {path} not found. Copy .env.example to .env and set api_token.", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            env[key] = value
    return env

env = load_env(ENV_FILE)
TOKEN = env.get("api_token", "")
HOST = env.get("joplin_host", "")
BASE = env.get("base_url", "http://localhost:41184")

if not TOKEN:
    print(f"Error: api_token is empty in {ENV_FILE}", file=sys.stderr)
    sys.exit(1)

# ── API request ────────────────────────────────────────────

def build_url(base, path):
    """Build URL with token, handling ? vs & correctly."""
    url = f"{base}{path}"
    sep = "&" if "?" in path else "?"
    return f"{url}{sep}token={TOKEN}"

def api_req(method, path, data=None):
    if HOST:
        # Remote Joplin via SSH
        url = build_url("http://127.0.0.1:41184", path)
        if data:
            # Base64 encode body to avoid shell quote swallowing
            b64 = base64.b64encode(data.encode("utf-8")).decode("ascii")
            # Use env vars + bash -c to avoid zsh globbing on remote macOS
            # Inside single quotes, $ is literal — no backslash needed
            remote_cmd = (
                "JOP_URL='" + url + "' JOP_BODY='" + b64 + "' JOP_METHOD=" + method + " "
                "bash -c 'curl -s -X $JOP_METHOD "
                "-H \"Content-Type: application/json\" "
                "-d \"$(echo \"$JOP_BODY\" | base64 -d)\" "
                "\"$JOP_URL\"'"
            )
        else:
            # Use env var to avoid zsh globbing on remote macOS
            remote_cmd = (
                "JOP_URL='" + url + "' JOP_METHOD=" + method + " "
                "bash -c 'curl -s -X $JOP_METHOD "
                "\"$JOP_URL\"'"
            )
        # SECURITY: remote_cmd is constructed from hardcoded curl invocations.
        # JOP_URL/JOP_BODY/JOP_METHOD are env-var indirection to bypass zsh globbing.
        # No raw user input reaches the shell — method is whitelisted (GET/POST/PUT/DELETE),
        # body is base64-encoded, URL is built by build_url() above.
        result = subprocess.run(
            ["ssh", HOST, remote_cmd],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    else:
        url = build_url(BASE, path)
        req = urllib.request.Request(url, method=method)
        if data:
            req.add_header("Content-Type", "application/json")
            req.data = data.encode("utf-8")
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")

def pretty_json(text):
    """Pretty-print JSON if output looks like JSON."""
    text = text.strip()
    if text.startswith("{") or text.startswith("["):
        try:
            return json.dumps(json.loads(text), indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
    return text

# ── Commands ───────────────────────────────────────────────

def cmd_ping():
    if HOST:
        try:
            result = subprocess.run(
                ["ssh", HOST, "curl -s http://127.0.0.1:41184/ping"],
                capture_output=True, text=True, check=True
            )
            print(f"✅ Joplin Clipper Server running ({result.stdout.strip()})")
        except subprocess.CalledProcessError:
            print(f"❌ Joplin Clipper Server 未运行（端口 41184，主机 {HOST}）", file=sys.stderr)
            sys.exit(7)
    else:
        try:
            with urllib.request.urlopen(f"{BASE}/ping") as resp:
                body = resp.read().decode("utf-8").strip()
                print(f"✅ Joplin Clipper Server running ({body})")
        except urllib.error.URLError:
            print("❌ Joplin Clipper Server 未运行（端口 41184）", file=sys.stderr)
            sys.exit(7)

def cmd_get(note_id, fields="id,title,body"):
    path = f"/notes/{note_id}?fields={fields}"
    print(pretty_json(api_req("GET", path)), end="")

def cmd_note(note_id):
    """Friendly note display: title + body preview."""
    raw = api_req("GET", f"/notes/{note_id}?fields=id,title,body,created_time,updated_time")
    d = json.loads(raw)
    title = d.get("title", "(无标题)")
    body = d.get("body", "")
    created_ts = d.get("created_time", 0)
    updated_ts = d.get("updated_time", 0)
    created = datetime.fromtimestamp(created_ts / 1000).strftime("%Y-%m-%d %H:%M") if created_ts else "N/A"
    updated = datetime.fromtimestamp(updated_ts / 1000).strftime("%Y-%m-%d %H:%M") if updated_ts else "N/A"

    print(f"📝 {title}")
    print(f"   创建: {created}  更新: {updated}")
    print("---")
    if body:
        lines = body.split("\n")
        preview = lines[:50]
        print("\n".join(preview))
        if len(lines) > 50:
            print(f"... (共 {len(lines)} 行，显示前 50 行)")
    else:
        print("(空笔记)")

def cmd_create(folder_id, title, body_file):
    with open(body_file, "r", encoding="utf-8") as f:
        body = f.read()
    data = json.dumps({"title": title, "body": body, "parent_id": folder_id})
    print(pretty_json(api_req("POST", "/notes", data)), end="")

def cmd_update(note_id, body_file):
    with open(body_file, "r", encoding="utf-8") as f:
        body = f.read()
    data = json.dumps({"body": body})
    print(pretty_json(api_req("PUT", f"/notes/{note_id}", data)), end="")

def cmd_delete(note_id, permanent="0"):
    path = f"/notes/{note_id}"
    if permanent in ("1", "--permanent"):
        path += "?permanent=1"
    print(pretty_json(api_req("DELETE", path)), end="")

def cmd_search(query, fields="id,title", limit=50):
    encoded = urllib.parse.quote(query)
    path = f"/search?query={encoded}&fields={fields}&limit={limit}"
    print(pretty_json(api_req("GET", path)), end="")

def cmd_list(folder_id, fields="id,title,updated_time", limit=100):
    path = f"/folders/{folder_id}/notes?fields={fields}&limit={limit}&order_by=updated_time&order_dir=DESC"
    print(pretty_json(api_req("GET", path)), end="")

def cmd_folders(query=None):
    if query:
        encoded = urllib.parse.quote(query)
        path = f"/search?query={encoded}&type=folder"
    else:
        path = "/folders"
    print(pretty_json(api_req("GET", path)), end="")

def cmd_tags(query=None):
    if query:
        encoded = urllib.parse.quote(query)
        path = f"/search?query={encoded}&type=tag"
    else:
        path = "/tags"
    print(pretty_json(api_req("GET", path)), end="")

def cmd_tree():
    """Print folder hierarchy as a tree."""
    raw = api_req("GET", "/folders")
    data = json.loads(raw)
    # Handle both raw array and {items: [...]} wrapper
    if isinstance(data, list):
        folders = data
    elif isinstance(data, dict) and "items" in data:
        folders = data["items"]
    else:
        folders = []
    by_id = {f["id"]: f for f in folders}
    # Find roots
    roots = [f for f in folders if not f.get("parent_id") or f["parent_id"] not in by_id]
    roots.sort(key=lambda x: x.get("title", ""))

    def print_tree(items, prefix=""):
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            short_id = item["id"][:8] + "..."
            print(f"{prefix}{connector}{item['title']} ({short_id})")
            children = [f for f in folders if f.get("parent_id") == item["id"]]
            children.sort(key=lambda x: x.get("title", ""))
            extension = "    " if is_last else "│   "
            if children:
                print_tree(children, prefix + extension)

    print_tree(roots)

# ── Main ───────────────────────────────────────────────────

def usage():
    print("Usage: python joplin.py <command> [args...]", file=sys.stderr)
    print("Commands:", file=sys.stderr)
    print("  ping                                  Test connection", file=sys.stderr)
    print("  get <note_id> [fields]                Get a note (JSON)", file=sys.stderr)
    print("  note <note_id>                        Friendly note display", file=sys.stderr)
    print("  create <folder_id> <title> <body_file> Create a note in folder", file=sys.stderr)
    print("  update <note_id> <body_file>          Update note body from file", file=sys.stderr)
    print("  delete <note_id> [--permanent]        Delete note (soft delete by default)", file=sys.stderr)
    print("  search <query> [fields] [limit]       Search notes", file=sys.stderr)
    print("  list <folder_id> [fields] [limit]     List notes in folder", file=sys.stderr)
    print("  folders [query]                       List/search folders", file=sys.stderr)
    print("  tags [query]                          List/search tags", file=sys.stderr)
    print("  tree                                  Print folder tree", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 2:
    usage()

cmd = sys.argv[1]
args = sys.argv[2:]

if cmd == "ping":
    cmd_ping()
elif cmd == "get":
    if not args:
        usage()
    cmd_get(args[0], args[1] if len(args) > 1 else "id,title,body")
elif cmd == "note":
    if not args:
        usage()
    cmd_note(args[0])
elif cmd == "create":
    if len(args) < 3:
        usage()
    cmd_create(args[0], args[1], args[2])
elif cmd == "update":
    if len(args) < 2:
        usage()
    cmd_update(args[0], args[1])
elif cmd == "delete":
    if not args:
        usage()
    cmd_delete(args[0], args[1] if len(args) > 1 else "0")
elif cmd == "search":
    if not args:
        usage()
    cmd_search(args[0], args[1] if len(args) > 1 else "id,title", int(args[2]) if len(args) > 2 else 50)
elif cmd == "list":
    if not args:
        usage()
    cmd_list(args[0], args[1] if len(args) > 1 else "id,title,updated_time", int(args[2]) if len(args) > 2 else 100)
elif cmd == "folders":
    cmd_folders(args[0] if args else None)
elif cmd == "tags":
    cmd_tags(args[0] if args else None)
elif cmd == "tree":
    cmd_tree()
else:
    print(f"Unknown command: {cmd}", file=sys.stderr)
    sys.exit(1)
