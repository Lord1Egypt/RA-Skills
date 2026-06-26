#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional

DEFAULT_FEED_URL = "https://www.linkedin.com/feed/?shareActive=true"


def load_token(config_path: Optional[str]) -> str:
    env_token = os.environ.get("OPENCLAW_GATEWAY_TOKEN")
    if env_token:
        return env_token

    if config_path is None:
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    data = json.loads(Path(config_path).read_text())
    token = data.get("gateway", {}).get("auth", {}).get("token")
    if not token:
        raise SystemExit(
            "No gateway token found. Set OPENCLAW_GATEWAY_TOKEN or provide --config pointing to openclaw.json"
        )
    return token


def run_browser(args: List[str], token: str, profile: str) -> str:
    env = os.environ.copy()
    env["OPENCLAW_GATEWAY_TOKEN"] = token
    cmd = ["openclaw", "browser", "--browser-profile", profile, *args]
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if res.returncode != 0:
        raise SystemExit((res.stderr or res.stdout or "browser command failed").strip())
    return res.stdout.strip()


def parse_target_id(output: str) -> str:
    m = re.search(r"\bid:\s*([A-Z0-9]+)", output)
    if not m:
        raise SystemExit(f"Could not find target id in output:\n{output}")
    return m.group(1)


def parse_ref(snapshot: str, patterns: List[str], label: str) -> str:
    for pattern in patterns:
        m = re.search(pattern, snapshot, re.IGNORECASE)
        if m:
            return m.group(1)
    raise SystemExit(f"Could not find {label} ref in snapshot")


def read_content(path: Optional[str]) -> str:
    if path:
        return Path(path).read_text().strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise SystemExit("Provide post content with --content-file or stdin")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare or publish a LinkedIn feed post through OpenClaw browser CLI")
    parser.add_argument("--content-file", help="Path to UTF-8 text file containing the post body")
    parser.add_argument("--config", help="Optional path to openclaw.json for gateway token lookup when OPENCLAW_GATEWAY_TOKEN is not already set")
    parser.add_argument("--profile", default="openclaw", help="OpenClaw browser profile name, already logged into LinkedIn")
    parser.add_argument("--open-url", default=DEFAULT_FEED_URL, help="URL to open for the share modal")
    parser.add_argument("--target-id", help="Existing tab target id. Skip opening a new share modal when provided")
    parser.add_argument("--publish", action="store_true", help="Click the final Post button after filling content")
    parser.add_argument("--wait-seconds", type=float, default=2.0, help="Wait between open/fill/click steps")
    args = parser.parse_args()

    content = read_content(args.content_file)
    token = load_token(args.config)

    run_browser(["start"], token, args.profile)

    if args.target_id:
        target_id = args.target_id
    else:
        opened = run_browser(["open", args.open_url], token, args.profile)
        target_id = parse_target_id(opened)
        time.sleep(args.wait_seconds)

    snapshot = run_browser(["snapshot", "--target-id", target_id, "--limit", "300", "--format", "ai"], token, args.profile)
    textbox_ref = parse_ref(
        snapshot,
        [
            r'textbox "Text editor for creating content" \[ref=(e\d+)\]',
            r'textbox "[^\"]*creating content[^\"]*" \[ref=(e\d+)\]',
            r'textbox "[^\"]*What do you want to talk about\?[^\"]*" \[ref=(e\d+)\]',
        ],
        "textbox",
    )

    fields = json.dumps([{"ref": textbox_ref, "value": content}], ensure_ascii=False)
    run_browser(["fill", "--fields", fields, "--target-id", target_id], token, args.profile)
    time.sleep(args.wait_seconds)

    result = {
        "target_id": target_id,
        "textbox_ref": textbox_ref,
        "mode": "prepared",
    }

    if args.publish:
        post_snapshot = run_browser(["snapshot", "--target-id", target_id, "--limit", "220", "--format", "ai"], token, args.profile)
        post_ref = parse_ref(
            post_snapshot,
            [
                r'button "Post" \[ref=(e\d+)\]',
                r'button "게시" \[ref=(e\d+)\]',
            ],
            "Post button",
        )
        run_browser(["click", post_ref, "--target-id", target_id], token, args.profile)
        time.sleep(args.wait_seconds)
        result["mode"] = "published"
        result["post_ref"] = post_ref

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
