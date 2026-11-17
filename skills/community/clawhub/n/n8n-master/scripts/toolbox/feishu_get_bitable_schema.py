#!/usr/bin/env python3
"""Fetch a Feishu/Lark Bitable field schema without printing secrets."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from _common import ToolboxError, die, json_dumps, redact, request_json, require_env, write_text


TOKEN_PATH = "/open-apis/auth/v3/tenant_access_token/internal"
FIELDS_PATH = "/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch Feishu Bitable field schema as Markdown or JSON.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--app-token", required=True, help="Bitable app_token/base token")
    parser.add_argument("--table-id", required=True, help="Bitable table_id")
    parser.add_argument("--base-url", default="https://open.feishu.cn", help="Feishu OpenAPI base URL")
    parser.add_argument("--page-size", type=int, default=100, help="Fields page size")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout seconds")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format")
    parser.add_argument("--output", help="Write output to file instead of stdout")
    return parser


def get_tenant_access_token(base_url: str, timeout: float) -> str:
    app_id = require_env("FEISHU_APP_ID")
    app_secret = require_env("FEISHU_APP_SECRET")
    url = base_url.rstrip("/") + TOKEN_PATH
    data = request_json(
        "POST",
        url,
        payload={"app_id": app_id, "app_secret": app_secret},
        timeout=timeout,
    )
    if not isinstance(data, dict) or data.get("code") not in (0, None):
        raise ToolboxError(f"failed to get tenant_access_token: {json_dumps(redact(data))}")
    token = data.get("tenant_access_token")
    if not token:
        raise ToolboxError(f"tenant_access_token missing in response: {json_dumps(redact(data))}")
    return str(token)


def fetch_fields(args: argparse.Namespace, token: str) -> list[dict[str, Any]]:
    fields: list[dict[str, Any]] = []
    page_token = ""
    while True:
        path = FIELDS_PATH.format(app_token=args.app_token, table_id=args.table_id)
        url = args.base_url.rstrip("/") + path
        query = f"?page_size={args.page_size}"
        if page_token:
            query += f"&page_token={page_token}"
        data = request_json(
            "GET",
            url + query,
            headers={"Authorization": f"Bearer {token}"},
            timeout=args.timeout,
        )
        if not isinstance(data, dict) or data.get("code") not in (0, None):
            raise ToolboxError(f"field list request failed: {json_dumps(redact(data))}")
        payload = data.get("data", {})
        items = payload.get("items", []) if isinstance(payload, dict) else []
        if not isinstance(items, list):
            raise ToolboxError(f"unexpected field list shape: {json_dumps(redact(data))}")
        fields.extend(item for item in items if isinstance(item, dict))
        if not payload.get("has_more"):
            break
        page_token = str(payload.get("page_token") or "")
        if not page_token:
            raise ToolboxError("response has_more=true but page_token is empty")
    return fields


def compact_property(value: Any) -> str:
    if value in (None, {}, []):
        return ""
    text = json_dumps(redact(value)).replace("\n", " ")
    return text[:220] + ("..." if len(text) > 220 else "")


def fields_to_markdown(fields: list[dict[str, Any]], args: argparse.Namespace) -> str:
    lines = [
        "# Feishu Bitable Field Schema",
        "",
        f"- app_token: `{redact(args.app_token, 'token')}`",
        f"- table_id: `{args.table_id}`",
        f"- fields: {len(fields)}",
        "",
        "| field_name | field_id | type | ui_type | property |",
        "|---|---|---:|---|---|",
    ]
    for field in fields:
        name = str(field.get("field_name", "")).replace("|", "\\|")
        field_id = str(field.get("field_id", "")).replace("|", "\\|")
        field_type = field.get("type", "")
        ui_type = str(field.get("ui_type", "")).replace("|", "\\|")
        prop = compact_property(field.get("property")).replace("|", "\\|")
        lines.append(f"| {name} | `{field_id}` | {field_type} | {ui_type} | `{prop}` |")
    return "\n".join(lines) + "\n"


def fields_to_json(fields: list[dict[str, Any]], args: argparse.Namespace) -> str:
    payload = {
        "source": {
            "app_token": "<redacted>",
            "table_id": args.table_id,
            "base_url": args.base_url,
        },
        "fields": redact(fields),
    }
    return json_dumps(payload) + "\n"


def run(args: argparse.Namespace) -> int:
    token = get_tenant_access_token(args.base_url, args.timeout)
    fields = fetch_fields(args, token)
    if args.format == "json":
        output = fields_to_json(fields, args)
    else:
        output = fields_to_markdown(fields, args)
    write_text(args.output, output)
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run(args)
    except ToolboxError as exc:
        die(str(exc))
    except KeyboardInterrupt:
        die("interrupted", 130)
    return 1


if __name__ == "__main__":
    sys.exit(main())
