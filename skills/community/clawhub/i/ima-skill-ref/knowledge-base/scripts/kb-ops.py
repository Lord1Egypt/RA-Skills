#!/usr/bin/env python3
import os
import sys
import json
import requests
from pathlib import Path

BASE_HOST = "ima.qq.com"
API_BASE = "/openapi/wiki/v1"


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
        "list": """Usage: python3 kb-ops.py list --kb-id <知识库ID> [--query <搜索词>] [--cursor ""] [--limit 50] [--json]

Examples:
  python3 kb-ops.py list --kb-id "kb_xxx"
  python3 kb-ops.py list --kb-id "kb_xxx" --query "产品"
  python3 kb-ops.py list --kb-id "kb_xxx" --limit 100 --json""",
        "search": """Usage: python3 kb-ops.py search --kb-id <知识库ID> --query <搜索词> [--cursor ""] [--limit 20] [--json]

Examples:
  python3 kb-ops.py search --kb-id "kb_xxx" --query "文档"
  python3 kb-ops.py search --kb-id "kb_xxx" --query "设计" --json""",
        "get-kb": """Usage: python3 kb-ops.py get-kb --kb-id <知识库ID> [--json]

Examples:
  python3 kb-ops.py get-kb --kb-id "kb_xxx"
  python3 kb-ops.py get-kb --kb-id "kb_xxx" --json""",
        "list-kbs": """Usage: python3 kb-ops.py list-kbs [--query <搜索词>] [--json]

Examples:
  python3 kb-ops.py list-kbs
  python3 kb-ops.py list-kbs --query "产品"
  python3 kb-ops.py list-kbs --json""",
        "add-urls": """Usage: python3 kb-ops.py add-urls --kb-id <知识库ID> --urls <url1,url2> [--folder-id <folderID>] [--json]

Examples:
  python3 kb-ops.py add-urls --kb-id "kb_xxx" --urls "https://example.com"
  python3 kb-ops.py add-urls --kb-id "kb_xxx" --urls "url1,url2" --folder-id "folder_xxx" --json""",
        "add-note": """Usage: python3 kb-ops.py add-note --kb-id <知识库ID> --doc-id <笔记ID> --title <标题> [--folder-id <folderID>] [--json]

Examples:
  python3 kb-ops.py add-note --kb-id "kb_xxx" --doc-id "doc_xxx" --title "工作日志"
  python3 kb-ops.py add-note --kb-id "kb_xxx" --doc-id "doc_xxx" --title "日志" --json"""
    }
    print("\n" + (cmds.get(cmd, "Unknown command. Use: list|search|get-kb|list-kbs|add-urls|add-note")))
    print("\nGlobal options: --json (output full response)\n")


async def cmd_list(args):
    creds = load_creds()
    kb_id = args.get("kb-id") or args.get("kb_id")
    if not kb_id:
        print("Error: --kb-id is required")
        sys.exit(1)
    body = {
        "knowledge_base_id": kb_id,
        "cursor": args.get("cursor", ""),
        "limit": int(args.get("limit", 50))
    }
    if args.get("query"):
        body["query"] = args.get("query")
    result = api_request("/get_knowledge_list", body, creds)
    items = result.get("data", {}).get("knowledge_list", [])
    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        print(f"知识库内容（共 {len(items)} 项）：\n")
        for i, item in enumerate(items):
            is_folder = item.get("title", "").startswith("📁") or (item.get("media_id") or "").startswith("folder_")
            print(f"{i+1}. {item.get('title', '未命名')} {'(文件夹)' if is_folder else ''}")
            print(f"   ID: {item.get('media_id')}")
            if item.get("highlight_content"):
                print(f"   摘要: {item.get('highlight_content')[:100]}...")
            print()


async def cmd_search(args):
    creds = load_creds()
    kb_id = args.get("kb-id") or args.get("kb_id")
    query = args.get("query") or args.get("q")
    if not kb_id or not query:
        print("Error: --kb-id and --query are required")
        sys.exit(1)
    body = {
        "knowledge_base_id": kb_id,
        "query": query,
        "cursor": args.get("cursor", ""),
        "limit": int(args.get("limit", 20))
    }
    result = api_request("/search_knowledge", body, creds)
    items = result.get("data", {}).get("info_list", [])
    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        print(f"搜索「{query}」找到 {len(items)} 项：\n")
        for i, item in enumerate(items):
            print(f"{i+1}. {item.get('title', '未命名')}")
            print(f"   ID: {item.get('media_id')}")
            if item.get("highlight_content"):
                print(f"   {item.get('highlight_content')}...")
            print()


async def cmd_get_kb(args):
    creds = load_creds()
    kb_id = args.get("kb-id") or args.get("kb_id")
    if not kb_id:
        print("Error: --kb-id is required")
        sys.exit(1)
    body = {"ids": [kb_id]}
    result = api_request("/get_knowledge_base", body, creds)
    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        infos = result.get("data", {}).get("infos", {})
        kb = infos.get(kb_id, {})
        print(f"📚 {kb.get('name', '未命名')}")
        if kb.get("description"):
            print(f"   {kb.get('description')}")
        print(f"   ID: {kb.get('id')}")


async def cmd_list_kbs(args):
    creds = load_creds()
    body = {"limit": 50}
    if args.get("query"):
        body["query"] = args.get("query")
    result = api_request("/search_knowledge_base", body, creds)
    kbs = result.get("data", {}).get("info_list", [])
    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        print(f"知识库列表（共 {len(kbs)} 个）：\n")
        for i, kb in enumerate(kbs):
            print(f"{i+1}. {kb.get('name', '未命名')}")
            if kb.get("description"):
                print(f"   {kb.get('description')}")
            print(f"   ID: {kb.get('id')}")
            print()


async def cmd_add_urls(args):
    creds = load_creds()
    kb_id = args.get("kb-id") or args.get("kb_id")
    urls = args.get("urls")
    if not kb_id or not urls:
        print("Error: --kb-id and --urls are required")
        sys.exit(1)
    body = {
        "knowledge_base_id": kb_id,
        "urls": [u.strip() for u in urls.split(",")]
    }
    if args.get("folder-id") or args.get("folder_id"):
        body["folder_id"] = args.get("folder-id") or args.get("folder_id")
    result = api_request("/import_urls", body, creds)
    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        results_dict = result.get("data", {}).get("results", {})
        success = 0
        failed = 0
        for url, info in results_dict.items():
            if info.get("ret_code") == 0:
                success += 1
                print(f"✅ {url}")
            else:
                failed += 1
                print(f"❌ {url}: {info.get('ret_msg', '失败')}")
        print(f"\n添加完成：{success} 成功，{failed} 失败")


async def cmd_add_note(args):
    creds = load_creds()
    kb_id = args.get("kb-id") or args.get("kb_id")
    doc_id = args.get("doc-id") or args.get("doc_id")
    title = args.get("title")
    if not kb_id or not doc_id or not title:
        print("Error: --kb-id, --doc-id, and --title are required")
        sys.exit(1)
    body = {
        "media_type": 11,
        "note_info": {"content_id": doc_id},
        "title": title,
        "knowledge_base_id": kb_id
    }
    if args.get("folder-id") or args.get("folder_id"):
        body["folder_id"] = args.get("folder-id") or args.get("folder_id")
    result = api_request("/add_knowledge", body, creds)
    if args.get("json"):
        print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
    else:
        media_id = result.get("data", {}).get("media_id")
        print(f"✅ 笔记「{title}」已添加到知识库")
        print(f"   Media ID: {media_id}")


async def main():
    args = parse_args()
    if args.get("help") or args.get("h"):
        print_usage(args.get("_", [None])[0])
        return

    cmd = args.get("_", [None])[0]
    if not cmd:
        print_usage("list")
        return

    switch = {
        "list": cmd_list,
        "search": cmd_search,
        "get-kb": cmd_get_kb,
        "list-kbs": cmd_list_kbs,
        "add-urls": cmd_add_urls,
        "add-note": cmd_add_note
    }

    if cmd in switch:
        await switch[cmd](args)
    else:
        print_usage("list")


if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
