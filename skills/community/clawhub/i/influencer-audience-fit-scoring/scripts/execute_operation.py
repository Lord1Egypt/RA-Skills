#!/usr/bin/env python3
"""Self-contained operation runner for this skill."""
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict

OPERATIONS_PATH = Path(__file__).resolve().parents[1] / "references" / "operations.json"
SKILL_ROOT = Path(__file__).resolve().parents[1]


def _install_id() -> str:
    """匿名安装 ID（IP 会随 WorkBuddy 出口变，用它做稳定统计/限额单位）。
    优先写用户主目录(活过重装、多 skill 共用)，退回 skill 目录；用户手动删才重置。"""
    import uuid
    paths = [Path.home() / ".scrumball_install_id", SKILL_ROOT / ".install_id"]
    for p in paths:
        try:
            if p.exists():
                v = p.read_text(encoding="utf-8").strip()
                if v:
                    return v
        except Exception:
            pass
    new_id = uuid.uuid4().hex
    for p in paths:
        try:
            p.write_text(new_id, encoding="utf-8")
            return new_id
        except Exception:
            continue
    return new_id
FOLLOW_UP_HINTS = {
    "channel_id": "What YouTube channel_id should I use?",
    "media_code": "What Instagram media_code should I use?",
    "monitor_id": "What monitor_id should I use?",
    "product_id": "What TikTok product_id should I use?",
    "query": "What keyword, brand, or niche should I search for?",
    "region": "Which region code should I use, for example US?",
    "uid": "What platform uid should I use?",
    "unique_id": "What TikTok unique_id or handle should I use?",
    "user_id": "What user_id should I use?",
    "username": "What username should I use?",
    "video_code": "What Instagram video_code should I use?",
    "video_id": "What video_id should I use?",
}


def load_operations() -> Dict[str, Dict[str, Any]]:
    with OPERATIONS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_json_arg(raw: str | None, label: str) -> Dict[str, Any]:
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON for {label}: {e}") from e
    if not isinstance(data, dict):
        raise ValueError(f"{label} must be a JSON object")
    return data


def apply_path_params(path: str, path_params: Dict[str, Any]) -> str:
    rendered = path
    for k, v in path_params.items():
        rendered = rendered.replace("{" + k + "}", str(v))
    return rendered


def build_follow_up(required: list[str], any_of: bool = False) -> str:
    if not required:
        return ""
    if any_of:
        joined = ", ".join(required)
        example = FOLLOW_UP_HINTS.get(required[0], f"What {required[0]} should I use?")
        return f" Follow-up: ask for any one of {joined}. Example: {example}"
    prompts = [FOLLOW_UP_HINTS.get(name, f"What {name} should I use?") for name in required]
    if len(prompts) == 1:
        return f" Follow-up: ask the user: {prompts[0]}"
    return " Follow-up: ask for these fields: " + " | ".join(prompts)


def validate_required(required: list[str], payload: Dict[str, Any], label: str) -> None:
    missing = [k for k in required if k not in payload or payload[k] in (None, "")]
    if missing:
        raise ValueError(f"Missing required {label}: {', '.join(missing)}.{build_follow_up(missing)}")


def validate_required_any(required_any: list[str], payload: Dict[str, Any], label: str) -> None:
    if not required_any:
        return
    present = any(k in payload and payload[k] not in (None, "") for k in required_any)
    if not present:
        joined = ", ".join(required_any)
        raise ValueError(f"Missing required {label}: at least one of {joined}.{build_follow_up(required_any, any_of=True)}")


def auth_header_value(api_key: str) -> str:
    prefix = os.getenv("SCRUMBALL_AUTH_PREFIX", "").strip()
    return f"{prefix} {api_key}" if prefix else api_key


def load_env_file(path: Path) -> None:
    if not path.exists() or not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        key = k.strip()
        if not key:
            continue
        val = v.strip().strip('"').strip("'")
        if key not in os.environ:
            os.environ[key] = val


def resolve_and_load_env(env_file_arg: str | None) -> Path | None:
    candidates = []
    if env_file_arg:
        candidates.append(Path(env_file_arg).expanduser())
    elif os.getenv("SCRUMBALL_ENV_FILE"):
        candidates.append(Path(os.getenv("SCRUMBALL_ENV_FILE", "")).expanduser())
    else:
        candidates.append(Path.cwd() / ".env")
        candidates.append(SKILL_ROOT / ".env")

    for p in candidates:
        if p.exists() and p.is_file():
            load_env_file(p)
            return p
    return None


def call_operation(op: Dict[str, Any], query: Dict[str, Any], body: Dict[str, Any], headers: Dict[str, Any], path_params: Dict[str, Any]) -> Dict[str, Any]:
    # 默认走托管网关（agent.scdata.cc）：调用方零配置、无需自带 key。
    # 网关服务端持有 Firebox key 并注入，故 SCRUMBALL_API_KEY 可留空。
    base_url = os.getenv("SCRUMBALL_BASE_URL", "").strip() or "https://agent.scdata.cc"
    api_key = os.getenv("SCRUMBALL_API_KEY", "").strip()
    timeout = int(os.getenv("SCRUMBALL_TIMEOUT_SECONDS", "30"))

    validate_required(op.get("required_query", []), query, "query parameters")
    validate_required_any(op.get("required_any_query", []), query, "query parameters")
    validate_required(op.get("required_path", []), path_params, "path parameters")
    validate_required(op.get("required_body", []), body, "body fields")

    url = base_url.rstrip("/") + apply_path_params(op["path"], path_params)
    if query:
        q = {k: v for k, v in query.items() if v is not None}
        if q:
            url += "?" + urllib.parse.urlencode(q, doseq=True)

    req_headers = {
        "authorization": auth_header_value(api_key),
        "accept": "application/json",
        "x-install-id": _install_id(),
    }
    req_headers.update(op.get("default_headers", {}))
    req_headers.update({k: str(v) for k, v in headers.items()})

    data = None
    if body:
        req_headers["content-type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url=url, method=op["method"], headers=req_headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            try:
                payload = json.loads(raw) if raw else None
            except json.JSONDecodeError:
                payload = raw
            return {"ok": True, "status": resp.getcode(), "url": url, "data": payload}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace") if e.fp else ""
        try:
            payload = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            payload = raw
        return {"ok": False, "status": e.code, "url": url, "error": payload}
    except urllib.error.URLError as e:
        raise ValueError(f"Network error: {e}") from e


def default_ping_operation() -> Dict[str, Any]:
    return {
        "method": "GET",
        "path": "/api/ping",
        "summary": "ping",
        "tags": ["health"],
        "required_query": [],
        "required_any_query": [],
        "required_path": [],
        "required_body": [],
        "default_headers": {},
    }


def run_doctor(ops: Dict[str, Dict[str, Any]], skip_ping: bool, loaded_env: Path | None) -> int:
    base_url = os.getenv("SCRUMBALL_BASE_URL", "").strip()
    api_key = os.getenv("SCRUMBALL_API_KEY", "").strip()
    result: Dict[str, Any] = {
        "ok": bool(base_url and api_key),
        "env_file": str(loaded_env) if loaded_env else None,
        "base_url_configured": bool(base_url),
        "api_key_configured": bool(api_key),
        "base_url": base_url or None,
        "auth_prefix": os.getenv("SCRUMBALL_AUTH_PREFIX", "").strip() or None,
        "timeout_seconds": int(os.getenv("SCRUMBALL_TIMEOUT_SECONDS", "30")),
    }

    if skip_ping:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1

    if result["ok"]:
        ping_op = ops.get("ping", default_ping_operation())
        try:
            result["ping"] = call_operation(ping_op, {}, {}, {}, {})
            result["ok"] = bool(result["ok"] and result["ping"].get("ok"))
        except ValueError as exc:
            result["ok"] = False
            result["ping"] = {"ok": False, "error": str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run operations for this skill")
    parser.add_argument("--env-file", help="Optional .env file path; if omitted, auto-tries ./.env then <skill-root>/.env")

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--tag")

    p_doctor = sub.add_parser("doctor")
    p_doctor.add_argument("--skip-ping", action="store_true")

    p_call = sub.add_parser("call")
    p_call.add_argument("--operation", required=True)
    p_call.add_argument("--query")
    p_call.add_argument("--body")
    p_call.add_argument("--headers")
    p_call.add_argument("--path-params")

    args = parser.parse_args()
    loaded_env = resolve_and_load_env(args.env_file)
    ops = load_operations()

    if args.cmd == "list":
        rows = [(oid, meta) for oid, meta in ops.items()]
        rows.sort(key=lambda x: (x[1]["path"], x[1]["method"]))
        if args.tag:
            rows = [x for x in rows if args.tag in (x[1].get("tags") or [])]
        for oid, meta in rows:
            print(f"{oid}\t{meta['method']}\t{meta['path']}\t{','.join(meta.get('tags') or [])}\t{meta.get('summary','')}")
        print(f"TOTAL\t{len(rows)}")
        return 0

    if args.cmd == "doctor":
        return run_doctor(ops, args.skip_ping, loaded_env)

    try:
        op = ops[args.operation]
    except KeyError:
        print(f"ERROR: Unknown operationId: {args.operation}")
        return 1

    try:
        query = parse_json_arg(args.query, "--query")
        body = parse_json_arg(args.body, "--body")
        headers = parse_json_arg(args.headers, "--headers")
        path_params = parse_json_arg(args.path_params, "--path-params")
        res = call_operation(op, query, body, headers, path_params)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res.get("ok") else 2
    except ValueError as e:
        print(f"ERROR: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
