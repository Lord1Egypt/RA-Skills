#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publish KeplerJAI bulletin candidates with a local script instead of relying on
an end-to-end OpenClaw tool loop.

Input:
- JSON or YAML file
- or a text file that contains a fenced YAML/JSON block

Expected candidate shape:
{
  "items": [
    {
      "rank": 1,
      "english_title": "...",
      "chinese_title": "...",
      "source_url": "...",
      "english_body_raw": "..."
    }
  ]
}
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - handled at runtime
    yaml = None

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


DEFAULT_API_URL = "https://www.keplerjai.com/api/content/bulletin"
DEFAULT_FRONTEND_URL = "https://www.keplerjai.com/bulletin?id={bulletin_id}"
PREFERRED_BEARER_ENV_KEYS = ("KEPLERAI_API_KEY", "KEPLERJAI_BEARER_TOKEN")
PREFERRED_COOKIE_ENV_KEYS = ("KEPLERAI_COOKIE", "KEPLERJAI_COOKIE")


def fail(message: str, exit_code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(exit_code)


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def parse_json_or_yaml(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    if yaml is not None:
        try:
            return yaml.safe_load(raw)
        except Exception:
            pass

    return None


def extract_fenced_block(raw: str) -> str | None:
    pattern = re.compile(r"```(?:yaml|yml|json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)
    match = pattern.search(raw)
    if match:
        return match.group(1).strip()
    return None


def extract_first_json_object(raw: str) -> str | None:
    start = raw.find("{")
    if start < 0:
        return None

    depth = 0
    in_string = False
    escape = False

    for idx in range(start, len(raw)):
        ch = raw[idx]

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return raw[start : idx + 1]

    return None


def extract_items_block(raw: str) -> str | None:
    lines = raw.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.strip().startswith("items:") or line.strip().startswith("brief_date:"):
            start = idx
            break
    if start is None:
        return None
    return "\n".join(lines[start:]).strip()


def load_structured_input(path: Path) -> dict[str, Any]:
    raw = read_text(path)

    candidates = [raw]
    fenced = extract_fenced_block(raw)
    if fenced:
        candidates.append(fenced)
    extracted_json = extract_first_json_object(raw)
    if extracted_json:
        candidates.append(extracted_json)

    for candidate in candidates:
        parsed = parse_json_or_yaml(candidate)
        if isinstance(parsed, dict):
            return parsed

    items_block = extract_items_block(raw)
    if items_block:
        parsed = parse_json_or_yaml(items_block)
        if isinstance(parsed, dict):
            return parsed

    fail(
        "无法解析输入文件。请提供 JSON / YAML，或包含结构化 YAML / JSON 代码块的文本文件。"
    )


def normalize_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    items = payload.get("items")
    if not isinstance(items, list) or not items:
        fail("输入数据缺少 items 数组，或 items 为空。")

    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            fail(f"第 {index} 条候选不是对象。")

        english_title = str(item.get("english_title", "")).strip()
        chinese_title = str(item.get("chinese_title", "")).strip()
        source_url = str(item.get("source_url", "")).strip()
        content = str(item.get("english_body_raw", "")).strip()

        if not english_title:
            fail(f"第 {index} 条候选缺少 english_title。")
        if not chinese_title:
            fail(f"第 {index} 条候选缺少 chinese_title。")
        if not source_url:
            fail(f"第 {index} 条候选缺少 source_url。")
        if not content:
            fail(f"第 {index} 条候选缺少 english_body_raw。")

        normalized.append(
            {
                "rank": item.get("rank", index),
                "english_title": english_title,
                "chinese_title": chinese_title,
                "source_url": source_url,
                "content": content,
            }
        )

    return normalized


def build_headers(args: argparse.Namespace) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
    }

    if args.bearer_token:
        headers["Authorization"] = f"Bearer {args.bearer_token}"
    if args.cookie:
        headers["Cookie"] = args.cookie

    for entry in args.header:
        if ":" not in entry:
            fail(f"无效 header: {entry}。格式必须是 Key: Value")
        key, value = entry.split(":", 1)
        headers[key.strip()] = value.strip()

    return headers


def build_payload(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": item["english_title"],
        "url": item["source_url"],
        "content": item["content"],
    }


def create_ssl_context(insecure: bool) -> ssl.SSLContext | None:
    if not insecure:
        return None
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context


def post_json(
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    timeout: int,
    insecure: bool,
) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    context = create_ssl_context(insecure)

    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        fail(f"HTTP {exc.code}: {body[:400] or exc.reason}")
    except urllib.error.URLError as exc:
        fail(f"请求失败: {exc.reason}")

    try:
        parsed = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        fail(f"接口返回了非 JSON 内容: {raw[:400]}")

    if not isinstance(parsed, dict):
        fail("接口返回的 JSON 不是对象。")
    return parsed


def extract_bulletin_id(response_json: dict[str, Any]) -> int | None:
    if str(response_json.get("resultCode", "")).strip() != "OK":
        return None

    bulletin = response_json.get("bulletin")
    if isinstance(bulletin, dict):
        value = bulletin.get("id")
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)

    value = response_json.get("bulletin_id")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def first_nonempty_env(keys: tuple[str, ...]) -> str:
    for key in keys:
        value = os.getenv(key, "").strip()
        if value:
            return value
    return ""


def load_auth_defaults() -> dict[str, str]:
    """Load auth from OpenClaw environment variables."""
    auth: dict[str, str] = {}

    env_token = first_nonempty_env(PREFERRED_BEARER_ENV_KEYS)
    env_cookie = first_nonempty_env(PREFERRED_COOKIE_ENV_KEYS)
    if env_token:
        auth["bearer_token"] = env_token
    if env_cookie:
        auth["cookie"] = env_cookie

    return auth


def main() -> int:
    parser = argparse.ArgumentParser(description="批量发布 KeplerJAI bulletin。")
    parser.add_argument("input", help="stage1 输出文件路径，支持 JSON / YAML / 含代码块文本")
    parser.add_argument(
        "-o",
        "--output",
        help="发布结果 JSON 输出路径，默认写到输入文件同目录 publish-result.json",
    )
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help="发布接口地址")
    parser.add_argument(
        "--frontend-url",
        default=DEFAULT_FRONTEND_URL,
        help="前台链接模板，默认 https://www.keplerjai.com/bulletin?id={bulletin_id}",
    )
    parser.add_argument("--bearer-token", help="可选 Bearer Token")
    parser.add_argument("--cookie", help="可选 Cookie 头")
    parser.add_argument(
        "--header",
        action="append",
        default=[],
        help="附加请求头，格式为 'Key: Value'，可重复使用",
    )
    parser.add_argument("--timeout", type=int, default=30, help="单次请求超时秒数")
    parser.add_argument("--insecure", action="store_true", help="忽略 HTTPS 证书校验")
    parser.add_argument("--dry-run", action="store_true", help="只生成请求载荷，不真正发请求")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        fail(f"输入文件不存在: {input_path}")

    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else input_path.with_name("publish-result.json")
    )

    payload = load_structured_input(input_path)
    candidates = normalize_candidates(payload)

    # Fallback: load auth from OpenClaw env if not provided via CLI
    auth_defaults = load_auth_defaults()
    if not args.bearer_token and auth_defaults.get("bearer_token"):
        args.bearer_token = auth_defaults["bearer_token"]
    if not args.cookie and auth_defaults.get("cookie"):
        args.cookie = auth_defaults["cookie"]

    headers = build_headers(args)

    result_items: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for item in candidates:
        request_payload = build_payload(item)
        record: dict[str, Any] = {
            "rank": item["rank"],
            "english_title": item["english_title"],
            "chinese_title": item["chinese_title"],
            "source_url": item["source_url"],
            "request_payload": request_payload,
        }

        if args.dry_run:
            record["status"] = "dry_run"
            result_items.append(record)
            continue

        response_json = post_json(
            url=args.api_url,
            payload=request_payload,
            headers=headers,
            timeout=args.timeout,
            insecure=args.insecure,
        )
        record["response"] = response_json

        bulletin_id = extract_bulletin_id(response_json)
        if bulletin_id is None:
            record["status"] = "failed"
            record["error"] = "resultCode 不是 OK，或未返回有效 bulletin.id"
            errors.append(
                {
                    "rank": item["rank"],
                    "english_title": item["english_title"],
                    "response": response_json,
                }
            )
        else:
            record["status"] = "published"
            record["bulletin_id"] = bulletin_id
            record["frontend_url"] = args.frontend_url.format(bulletin_id=bulletin_id)

        result_items.append(record)

    published_count = sum(1 for item in result_items if item.get("status") == "published")
    final_payload = {
        "input_file": str(input_path),
        "api_url": args.api_url,
        "published_count": published_count,
        "total_count": len(result_items),
        "items": result_items,
        "errors": errors,
    }

    write_json(output_path, final_payload)
    print(f"结果已写入: {output_path}")
    print(f"成功发布: {published_count}/{len(result_items)}")

    return 0 if (args.dry_run or published_count == len(result_items)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
