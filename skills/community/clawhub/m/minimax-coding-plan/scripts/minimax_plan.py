#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

DEFAULT_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com").rstrip("/")
SOURCE_HEADER = "Minimax-MCP"
DEFAULT_PROFILE = os.environ.get("MINIMAX_AUTH_PROFILE", "minimax-portal:default")


def auth_store_candidates():
    candidates = []

    explicit = os.environ.get("OPENCLAW_AUTH_PROFILES_JSON", "").strip()
    if explicit:
        candidates.append(Path(explicit).expanduser())

    agent_dir = os.environ.get("OPENCLAW_AGENT_DIR", "").strip()
    if agent_dir:
        candidates.append(Path(agent_dir).expanduser() / "auth-profiles.json")

    openclaw_home = os.environ.get("OPENCLAW_HOME", "").strip()
    if openclaw_home:
        candidates.append(Path(openclaw_home).expanduser() / "agents" / "main" / "agent" / "auth-profiles.json")

    candidates.append(Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json")
    candidates.append(Path("/home/admin/.openclaw/agents/main/agent/auth-profiles.json"))

    seen = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        yield candidate


def load_api_key_from_store(path):
    data = json.loads(path.read_text())
    profiles = data.get("profiles") or {}
    profile = profiles.get(DEFAULT_PROFILE) or {}
    for field in ("access", "access_token", "token"):
        token = str(profile.get(field) or "").strip()
        if token:
            return token
    return ""


def load_api_key():
    env_key = os.environ.get("MINIMAX_API_KEY", "").strip()
    if env_key:
        return env_key
    for path in auth_store_candidates():
        if not path.exists():
            continue
        try:
            token = load_api_key_from_store(path)
        except Exception:
            continue
        if token:
            return token
    raise SystemExit(
        "MiniMax API key not found. Set MINIMAX_API_KEY or configure minimax-portal OAuth first."
    )


def detect_mime(path, content_type=""):
    lowered = content_type.lower()
    if "png" in lowered:
        return "image/png"
    if "webp" in lowered:
        return "image/webp"
    if "jpeg" in lowered or "jpg" in lowered:
        return "image/jpeg"
    guessed, _ = mimetypes.guess_type(path)
    if guessed in {"image/png", "image/webp", "image/jpeg"}:
        return guessed
    return "image/jpeg"


def process_image_source(image_source):
    if image_source.startswith("@"):
        image_source = image_source[1:]
    if image_source.startswith("data:"):
        return image_source
    if image_source.startswith(("http://", "https://")):
        req = urllib.request.Request(image_source, headers={"User-Agent": "OpenClaw-MiniMax-Plan/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            mime = detect_mime(image_source, resp.headers.get("Content-Type", ""))
        encoded = base64.b64encode(data).decode("utf-8")
        return "data:%s;base64,%s" % (mime, encoded)
    path = Path(image_source)
    if not path.exists():
        raise SystemExit("Image file does not exist: %s" % image_source)
    data = path.read_bytes()
    mime = detect_mime(str(path))
    encoded = base64.b64encode(data).decode("utf-8")
    return "data:%s;base64,%s" % (mime, encoded)


def post_json(endpoint, payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "%s%s" % (DEFAULT_HOST, endpoint),
        data=body,
        headers={
            "Authorization": "Bearer %s" % load_api_key(),
            "Content-Type": "application/json",
            "MM-API-Source": SOURCE_HEADER,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"error": {"http_status": exc.code, "body": body}}
        if "http_status" not in parsed:
            parsed["http_status"] = exc.code
        return parsed


def cmd_web_search(args):
    result = post_json("/v1/coding_plan/search", {"q": args.query})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_understand_image(args):
    image_url = process_image_source(args.image_source)
    result = post_json("/v1/coding_plan/vlm", {"prompt": args.prompt, "image_url": image_url})
    status = ((result.get("base_resp") or {}).get("status_code")) if isinstance(result, dict) else None
    content = result.get("content", "") if isinstance(result, dict) else ""
    if args.content_only:
        if status == 0 and content:
            print(content)
            return 0
        msg = ((result.get("base_resp") or {}).get("status_msg")) if isinstance(result, dict) else "unknown error"
        sys.stderr.write("MiniMax understand_image failed: %s\n" % (msg or "no content returned"))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="MiniMax Coding Plan wrapper")
    sub = parser.add_subparsers(dest="tool")

    web = sub.add_parser("web_search", help="Run MiniMax Coding Plan web search")
    web.add_argument("--query", required=True)
    web.set_defaults(func=cmd_web_search)

    img = sub.add_parser("understand_image", help="Run MiniMax Coding Plan image understanding")
    img.add_argument("--prompt", required=True)
    img.add_argument("--image-source", required=True)
    img.add_argument("--content-only", action="store_true")
    img.set_defaults(func=cmd_understand_image)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
