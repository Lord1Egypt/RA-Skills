#!/usr/bin/env python3
import argparse
import json
import os
import sys
import subprocess
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_CACHE = os.path.join(SCRIPT_DIR, ".token_cache.json")
TIMEOUT = 30


def load_config(config_path, platform_id=None):
    if not config_path or not os.path.exists(config_path):
        return None
    with open(config_path, "r", encoding="utf-8-sig") as f:
        cfg = json.load(f)
    pid = platform_id or cfg.get("active_platform")
    if not pid or pid not in cfg.get("platforms", {}):
        return None
    p = cfg["platforms"][pid]
    p["_id"] = pid
    return p


def get_cached_token(platform_id):
    if not os.path.exists(TOKEN_CACHE):
        return None
    with open(TOKEN_CACHE, "r", encoding="utf-8-sig") as f:
        cache = json.load(f)
    return cache.get(platform_id, {}).get("token")


def build_headers(plat, extra_headers=None):
    headers = {}
    if plat:
        for k, v in plat.get("default_headers", {}).items():
            headers[k] = v
        auth_cfg = plat.get("auth", {})
        token = get_cached_token(plat["_id"])
        if token:
            header_name = auth_cfg.get("token_header", "Authorization")
            prefix = auth_cfg.get("token_prefix", "Bearer ")
            headers[header_name] = f"{prefix}{token}"
    if "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"
    if extra_headers:
        if isinstance(extra_headers, str):
            extra_headers = json.loads(extra_headers)
        headers.update(extra_headers)
    return headers


def resolve_url(args, plat):
    if args.url:
        return args.url
    if args.endpoint and plat:
        gateway = plat.get("gateway", "").rstrip("/")
        endpoint = args.endpoint if args.endpoint.startswith("/") else f"/{args.endpoint}"
        return f"{gateway}{endpoint}"
    sys.exit("[ERROR] You must provide --url or --endpoint (with --config).")


def execute_request(method, url, headers, body=None, params=None, timeout=30):
    method = method.upper()
    kwargs = {"headers": headers, "timeout": timeout}
    if body:
        kwargs["json"] = body if isinstance(body, dict) else json.loads(body)
    if params:
        kwargs["params"] = params if isinstance(params, dict) else json.loads(params)

    resp = getattr(requests, method.lower())(url, **kwargs)

    print(f"[{method}] {url}")
    print(f"Status: {resp.status_code}")

    renewal = resp.headers.get("x-token-renewal")
    if renewal == "1":
        print("[WARN] Server indicates token renewal is required")

    try:
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except ValueError:
        print(f"Response: {resp.text[:2000]}")

    return resp.status_code


def re_auth(config_path, platform_id=None):
    auth_script = os.path.join(SCRIPT_DIR, "auth_manager.py")
    if not os.path.exists(auth_script):
        return False
    cmd = [sys.executable, auth_script, "--config", config_path, "--force-login"]
    if platform_id:
        cmd.extend(["--platform", platform_id])
    print("[AUTO] Triggering re-authentication...")
    subprocess.run(cmd)
    return True


def main():
    parser = argparse.ArgumentParser(description="Generic HTTP executor")
    parser.add_argument("--config", help="Platform config file path")
    parser.add_argument("--platform", help="Specify platform ID")
    parser.add_argument("--method", required=True, choices=["GET", "POST", "PUT", "DELETE", "PATCH"])
    parser.add_argument("--url", help="Complete request URL")
    parser.add_argument("--endpoint", help="API endpoint path")
    parser.add_argument("--json-body", help="Request body as JSON string", default=None)
    parser.add_argument("--json-file", help="Request body JSON file path", default=None)
    parser.add_argument("--params", help="Query params JSON string", default=None)
    parser.add_argument("--headers", help="Extra headers JSON string", default=None)
    parser.add_argument("--timeout", type=int, default=TIMEOUT)
    args = parser.parse_args()

    plat = load_config(args.config, args.platform) if args.config else None
    url = resolve_url(args, plat)
    headers = build_headers(plat, args.headers)

    body = args.json_body
    if args.json_file:
        import json as _j
        with open(args.json_file, "r", encoding="utf-8-sig") as _f:
            body = _j.load(_f)
    status = execute_request(args.method, url, headers, body, args.params, args.timeout)

    if status == 401 and plat and args.config:
        if re_auth(args.config, args.platform):
            headers = build_headers(plat, args.headers)
            print("[RETRY] Retrying with new token...\n")
            execute_request(args.method, url, headers, args.json_body, args.params, args.timeout)


if __name__ == "__main__":
    main()
