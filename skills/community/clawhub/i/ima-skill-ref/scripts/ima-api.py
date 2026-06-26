#!/usr/bin/env python3
import os
import sys
import json
import requests
from pathlib import Path

BASE_HOST = "ima.qq.com"
BASE_PATH = "/"


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
        raise Exception("Missing IMA credentials")

    url = f"https://{BASE_HOST}/{api_path.lstrip('/')}"
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
    args = {}
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
            i += 1
    return args


def main():
    args = parse_args()
    if args.get("help") or args.get("h"):
        print("""
ima-api.py - IMA OpenAPI 调用工具

用法:
  python3 ima-api.py --path <api路径> --body <json字符串> [选项]

必需参数:
  --path    API路径，如 openapi/note/v1/search_note_book
  --body    请求体JSON字符串

可选参数:
  --json    输出完整响应JSON（默认只输出data字段）

示例:
  python3 ima-api.py --path openapi/note/v1/search_note_book --body '{"search_type":0,"query_info":{"title":"工作"},"start":0,"end":20}'
        """)
        return

    api_path = args.get("path")
    body_str = args.get("body")
    if not api_path or not body_str:
        print("Error: --path and --body are required")
        sys.exit(1)

    try:
        body = json.loads(body_str)
    except Exception as e:
        print(f"Error: --body must be valid JSON: {e}")
        sys.exit(1)

    creds = load_creds()
    result = api_request(api_path, body, creds)

    if args.get("json"):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif result.get("data") is not None:
        print(json.dumps(result["data"], indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)
