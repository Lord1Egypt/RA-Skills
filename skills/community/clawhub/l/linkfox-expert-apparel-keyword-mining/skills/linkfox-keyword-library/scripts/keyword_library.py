#!/usr/bin/env python3
"""
词库查询 - LinkFox Skill
调用 mind-x-tools-common-server 的词库查询接口。

Usage:
  python keyword_library.py '{"action": "listLibraries", "uid": "xxx"}'
  python keyword_library.py '{"action": "listLibraries", "uid": "xxx", "name": "品牌"}'
  python keyword_library.py '{"action": "getWords", "uid": "xxx", "libraryId": "abc123"}'
  python keyword_library.py '{"action": "getWords", "uid": "xxx", "libraryName": "品牌风险词"}'
"""

import json
import os
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


SLUG = "linkfox-keyword-library"

API_PATHS = {
    "listLibraries": "/common/keyword/listLibraries",
    "getWords": "/common/keyword/getWords",
}


def get_api_base():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared"))
    from linkfox_paths import get_api_base
    return get_api_base()


def get_api_key():
    key = os.environ.get("LINKFOX_AGENT_API_KEY")
    if not key:
        print(
            "API Key not configured. Please complete authorization first:\n"
            "1. Visit https://skill.linkfox.com/linkfoxskills/guide.htm to obtain your Key\n"
            "2. Set the environment variable: export LINKFOX_AGENT_API_KEY=your-key-here",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def call_api(action, params):
    api_path = API_PATHS.get(action)
    if not api_path:
        print("Unknown action: " + action + ". Supported: " + str(list(API_PATHS.keys())), file=sys.stderr)
        sys.exit(1)

    api_url = get_api_base() + api_path
    api_key = get_api_key()

    request_body = {k: v for k, v in params.items() if k != "action"}

    data = json.dumps(request_body).encode("utf-8")
    req = Request(
        api_url,
        data=data,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "User-Agent": "LinkFox-Skill/2.0",
            "SESSION_ID": os.environ.get("SESSION_ID", ""),
        "MESSAGE_ID": os.environ.get("MESSAGE_ID", ""),
            "MODE_ID": os.environ.get("MODE_ID", ""),
        "APP_NAME": os.environ.get("APP_NAME", ""),
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        try:
            return json.loads(body) if body else {"error": "HTTP " + str(e.code) + ": " + str(e.reason)}
        except Exception:
            return {"error": "HTTP " + str(e.code) + ": " + str(e.reason), "details": body}
    except URLError as e:
        return {"error": "Connection failed: " + str(e.reason)}


def summarize(result):
    if not isinstance(result, dict):
        print("Response type: " + type(result).__name__)
        print(json.dumps(result, ensure_ascii=False)[:500])
        return

    print("Top-level keys: " + str(list(result.keys())))

    for k in ("errcode", "errorCode", "code", "errmsg", "msg",
              "total", "totalCount", "count", "costToken", "success"):
        if k in result:
            v = result[k]
            if isinstance(v, (int, float, bool, str)):
                print("  " + k + ": " + str(v))

    for list_key in ("libraries", "words"):
        if list_key in result and isinstance(result[list_key], list):
            items = result[list_key]
            print("\n" + list_key + " (length=" + str(len(items)) + "):")
            sample = items[:5]
            print("Sample (first " + str(len(sample)) + " of " + str(len(items)) + "):")
            print(json.dumps(sample, indent=2, ensure_ascii=False))


def _resolve_output_path(ts):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared"))
    from linkfox_paths import resolve_data_path
    return resolve_data_path(SLUG, ts)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: keyword_library.py '<JSON parameters>'\n"
            "  action: listLibraries | getWords",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print("Invalid parameter format: " + str(e), file=sys.stderr)
        sys.exit(1)

    action = params.get("action")
    if not action:
        print("Missing 'action' field. Supported: listLibraries, getWords", file=sys.stderr)
        sys.exit(1)

    result = call_api(action, params)

    serialized = json.dumps(result, ensure_ascii=False, indent=2)

    ts = int(time.time())
    out_path = _resolve_output_path(ts)
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(serialized)
        print("Saved full response: " + out_path + " (" + str(len(serialized)) + " bytes)")
    except OSError as e:
        print("Failed to save to " + out_path + ": " + str(e), file=sys.stderr)

    summarize(result)


if __name__ == "__main__":
    main()
