#!/usr/bin/env python3
import os
import sys
import json
import requests
from pathlib import Path

BASE_HOST = "ima.qq.com"
API_BASE = "/openapi/note/v1"


def load_creds():
    home = os.environ.get("HOME", os.environ.get("USERPROFILE", ""))
    conf_dir = Path(home) / ".config" / "ima"
    client_id = os.environ.get("IMA_OPENAPI_CLIENTID", "").strip()
    api_key = os.environ.get("IMA_OPENAPI_APIKEY", "").strip()

    if not client_id and (conf_dir / "client_id").exists():
        content = (conf_dir / "client_id").read_bytes()
        # 检测UTF-16 BOM
        if content.startswith(b"\xff\xfe"):
            client_id = content.decode("utf-16le").replace("\ufeff", "").strip()
        elif content.startswith(b"\xfe\xff"):
            client_id = content.decode("utf-16be").replace("\ufeff", "").strip()
        else:
            client_id = content.decode("utf8").replace("\ufeff", "").strip()
    if not api_key and (conf_dir / "api_key").exists():
        content = (conf_dir / "api_key").read_bytes()
        # 检测UTF-16 BOM
        if content.startswith(b"\xff\xfe"):
            api_key = content.decode("utf-16le").replace("\ufeff", "").strip()
        elif content.startswith(b"\xfe\xff"):
            api_key = content.decode("utf-16be").replace("\ufeff", "").strip()
        else:
            api_key = content.decode("utf8").replace("\ufeff", "").strip()
    return {"client_id": client_id, "api_key": api_key}


def api_request(api_path, body, creds):
    client_id = creds.get("client_id")
    api_key = creds.get("api_key")
    if not client_id or not api_key:
        raise Exception("Missing IMA credentials. Please set IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY environment variables or create ~/.config/ima/client_id and ~/.config/ima/api_key files.")

    url = f"https://{BASE_HOST}/{API_BASE.lstrip('/')}/{api_path.lstrip('/')}"
    headers = {
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json; charset=utf-8"
    }
    resp = requests.post(url, json=body, headers=headers, timeout=30)
    resp.raise_for_status()
    result = resp.json()

    if result.get("code") != 0:
        print(f"IMA API Error [{result.get('code')}]: {result.get('msg')}")
        sys.exit(result.get("code", 1))
    return result


def parse_args():
    args = {"_": []}
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].startswith("--"):
            k = sys.argv[i][2:]
            if k in ("json", "h", "help"):
                args[k] = True
                i += 1
                continue
            if i + 1 >= len(sys.argv) or sys.argv[i + 1].startswith("--"):
                args[k] = True
            else:
                args[k] = sys.argv[i + 1]
                i += 2
        else:
            args["_"].append(sys.argv[i])
            i += 1
    return args


def print_usage(cmd=None):
    cmds = {
        "search": """Usage: python3 notes-ops.py search --query <关键词> [--type title|content] [--start 0] [--end 20] [--json]

Examples:
  python3 notes-ops.py search --query "工作日志"
  python3 notes-ops.py search --query "会议" --type content --json""",
        "list-folders": """Usage: python3 notes-ops.py list-folders [--cursor "0"] [--limit 20] [--json]

Examples:
  python3 notes-ops.py list-folders
  python3 notes-ops.py list-folders --limit 50 --json""",
        "list-notes": """Usage: python3 notes-ops.py list-notes [--folder-id <id>] [--cursor ""] [--limit 20] [--json]

Examples:
  python3 notes-ops.py list-notes
  python3 notes-ops.py list-notes --folder-id "folder_xxx" --json""",
        "read": """Usage: python3 notes-ops.py read --doc-id <id> [--format 0] [--json]

Examples:
  python3 notes-ops.py read --doc-id "doc_xxx"
  python3 notes-ops.py read --doc-id "doc_xxx" --format 0 --json""",
        "create": """Usage: python3 notes-ops.py create --content <markdown> [--title <标题>] [--json]

Examples:
  python3 notes-ops.py create --content "# 今天的工作\n\n完成了..."
  python3 notes-ops.py create --title "工作日志" --content "# 今天..." --json""",
        "append": """Usage: python3 notes-ops.py append --doc-id <id> --content <追加内容> [--json]

Examples:
  python3 notes-ops.py append --doc-id "doc_xxx" --content "\n\n## 补充\n新内容"
  python3 notes-ops.py append --doc-id "doc_xxx" --content "追加内容" --json"""
    }
    print("\n" + (cmds.get(cmd, "Unknown command. Use: search|list-folders|list-notes|read|create|append")))
    print("\nGlobal options: --json (output full response)\n")


async def cmd_search(args):
    creds = load_creds()
    query = args.get("query") or args.get("q")
    if not query:
        print("Error: --query is required")
        sys.exit(1)

    search_type = 1 if args.get("type") == "content" else 0
    body = {
        "search_type": search_type,
        "query_info": {"title": query, "content": query},
        "start": int(args.get("start", 0)),
        "end": int(args.get("end", 20))
    }
    if search_type == 0:
        body["query_info"] = {"title": query}
    else:
        body["query_info"] = {"content": query}

    result = api_request("/search_note_book", body, creds)
    docs = result.get("data", {}).get("docs", [])

    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        print(f"找到 {len(docs)} 篇笔记：\n")
        for i, d in enumerate(docs):
            info = d.get("doc", {}).get("basic_info", {})
            print(f"{i+1}. {info.get('title', '无标题')}")
            print(f"   ID: {info.get('docid')}")
            if info.get("summary"):
                print(f"   摘要: {info.get('summary')[:100]}...")
            print()


async def cmd_list_folders(args):
    creds = load_creds()
    body = {
        "cursor": args.get("cursor", "0"),
        "limit": int(args.get("limit", 20))
    }
    result = api_request("/list_note_folder_by_cursor", body, creds)
    folders = result.get("data", {}).get("note_book_folders", [])

    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        print(f"笔记本列表（共 {len(folders)} 个）：\n")
        for i, f in enumerate(folders):
            info = f.get("folder", {}).get("basic_info", {})
            print(f"{i+1}. {info.get('name', '未命名')} ({info.get('folder_type')})")
            print(f"   ID: {info.get('folder_id')}")
            print()


async def cmd_list_notes(args):
    creds = load_creds()
    body = {
        "folder_id": args.get("folder-id") or args.get("folder_id", ""),
        "cursor": args.get("cursor", ""),
        "limit": int(args.get("limit", 20))
    }
    result = api_request("/list_note_by_folder_id", body, creds)
    notes = result.get("data", {}).get("note_book_list", [])
    is_end = result.get("data", {}).get("is_end", True)

    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        print(f"笔记列表（共 {len(notes)} 篇）：\n")
        for i, n in enumerate(notes):
            info = n.get("basic_info", {}).get("basic_info", {})
            print(f"{i+1}. {info.get('title', '无标题')}")
            print(f"   ID: {info.get('docid')}")
            if info.get("summary"):
                print(f"   摘要: {info.get('summary')[:80]}...")
            print()
        if not is_end:
            print(f"(还有更多，使用 --cursor {result.get('data', {}).get('next_cursor', '')} 获取)")


async def cmd_read(args):
    creds = load_creds()
    doc_id = args.get("doc-id") or args.get("doc_id")
    if not doc_id:
        print("Error: --doc-id is required")
        sys.exit(1)

    body = {
        "doc_id": doc_id,
        "target_content_format": int(args.get("format", 0))
    }
    result = api_request("/get_doc_content", body, creds)

    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        content = result.get("data", {}).get("content", "")
        print(content)


async def cmd_create(args):
    creds = load_creds()
    content = args.get("content")
    if not content:
        print("Error: --content is required")
        sys.exit(1)

    final_content = f"# {args['title']}\n\n{content}" if args.get("title") else content
    body = {"content_format": 1, "content": final_content}
    result = api_request("/import_doc", body, creds)
    doc_id = result.get("data", {}).get("doc_id")

    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        print(f"✅ 笔记创建成功")
        print(f"   ID: {doc_id}")


async def cmd_append(args):
    creds = load_creds()
    doc_id = args.get("doc-id") or args.get("doc_id")
    content = args.get("content")
    if not doc_id or not content:
        print("Error: --doc-id and --content are required")
        sys.exit(1)

    body = {"doc_id": doc_id, "content_format": 1, "content": content}
    result = api_request("/append_doc", body, creds)

    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        print(f"✅ 内容已追加到笔记 {doc_id}")


async def main():
    args = parse_args()
    if args.get("help") or args.get("h"):
        print_usage()
        return

    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "help":
        print_usage()
        return

    switch = {
        "search": cmd_search,
        "list-folders": cmd_list_folders,
        "list-notes": cmd_list_notes,
        "read": cmd_read,
        "create": cmd_create,
        "append": cmd_append
    }

    if cmd in switch:
        await switch[cmd](args)
    else:
        print_usage("search")


if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
