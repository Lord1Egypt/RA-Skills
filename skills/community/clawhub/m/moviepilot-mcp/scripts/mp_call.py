#!/usr/bin/env python3
"""MoviePilot MCP tool caller — reads config.json for server/auth.

Usage:
  mp_call.py <tool_name> '<json_args>'
  mp_call.py search_media '{"title":"The Matrix","media_type":"movie"}'
  mp_call.py query_sites '{}'
"""

import sys, json, os, subprocess

SKILL_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit("/scripts", 1)[0]
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"错误: 未找到 {CONFIG_PATH}", file=sys.stderr)
        print(f"先运行: python3 {os.path.join(SKILL_DIR, 'scripts', 'setup.py')}", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    base_url = cfg.get("base_url", "").rstrip("/")
    apikey = cfg.get("apikey", "")
    if not base_url or not apikey:
        print("错误: config.json 中 base_url 或 apikey 为空", file=sys.stderr)
        sys.exit(1)
    return base_url, apikey


def main():
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <tool_name> [json_args]", file=sys.stderr)
        print(f'示例: {sys.argv[0]} search_media \'{{"title":"三体","media_type":"tv"}}\'', file=sys.stderr)
        sys.exit(1)

    tool_name = sys.argv[1]
    args_str = sys.argv[2] if len(sys.argv) > 2 else "{}"

    try:
        arguments = json.loads(args_str)
    except json.JSONDecodeError as e:
        print(f"错误: JSON 参数格式不正确: {e}", file=sys.stderr)
        sys.exit(1)

    base_url, apikey = load_config()

    body = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
        "id": 1
    }, ensure_ascii=False)

    # Use curl subprocess for Unicode-safe URL handling
    url = f"{base_url}/api/v1/mcp?apikey={apikey}"
    proc = subprocess.run(
        ["curl", "-s", "--connect-timeout", "10", "--max-time", "45",
         "-X", "POST", url,
         "-H", "Content-Type: application/json",
         "-H", "Accept: application/json",
         "-d", body],
        capture_output=True, text=True, timeout=60
    )

    if proc.returncode != 0 and not proc.stdout:
        print(f"curl 错误 (code={proc.returncode}): {proc.stderr}", file=sys.stderr)
        sys.exit(proc.returncode)

    sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)


if __name__ == "__main__":
    main()
