#!/usr/bin/env python3
"""Create Feishu/Lark Bitable fields from a schema JSON, dry-run by default."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from _common import ToolboxError, die, json_dumps, read_json_file, redact, request_json, require_env


TOKEN_PATH = "/open-apis/auth/v3/tenant_access_token/internal"
FIELDS_PATH = "/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
READ_ONLY_OR_SYSTEM_TYPES = {1001, 1002, 1003, 1004, 1005}
UNSUPPORTED_UI_TYPES = {"not_support", "dynamic"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate or execute Feishu Bitable field creation requests.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--schema", required=True, help="Schema JSON file from feishu_get_bitable_schema.py")
    parser.add_argument("--app-token", required=True, help="Target Bitable app_token/base token")
    parser.add_argument("--table-id", required=True, help="Target Bitable table_id")
    parser.add_argument("--base-url", default="https://open.feishu.cn", help="Feishu OpenAPI base URL")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout seconds")
    parser.add_argument("--execute", action="store_true", help="Actually create fields. Default is dry-run.")
    parser.add_argument(
        "--include-system-types",
        action="store_true",
        help="Do not skip read-only/system field types such as created_time.",
    )
    parser.add_argument(
        "--include-unsupported-ui-types",
        action="store_true",
        help="Do not skip fields whose ui_type says dynamic/not_support.",
    )
    parser.add_argument(
        "--no-skip-existing",
        action="store_true",
        help="When executing, do not prefetch existing field names for duplicate skipping.",
    )
    return parser


def get_tenant_access_token(base_url: str, timeout: float) -> str:
    app_id = require_env("FEISHU_APP_ID")
    app_secret = require_env("FEISHU_APP_SECRET")
    data = request_json(
        "POST",
        base_url.rstrip("/") + TOKEN_PATH,
        payload={"app_id": app_id, "app_secret": app_secret},
        timeout=timeout,
    )
    if not isinstance(data, dict) or data.get("code") not in (0, None):
        raise ToolboxError(f"failed to get tenant_access_token: {json_dumps(redact(data))}")
    token = data.get("tenant_access_token")
    if not token:
        raise ToolboxError(f"tenant_access_token missing in response: {json_dumps(redact(data))}")
    return str(token)


def extract_fields(schema: Any) -> list[dict[str, Any]]:
    if isinstance(schema, list):
        fields = schema
    elif isinstance(schema, dict):
        if isinstance(schema.get("fields"), list):
            fields = schema["fields"]
        elif isinstance(schema.get("items"), list):
            fields = schema["items"]
        elif isinstance(schema.get("data"), dict) and isinstance(schema["data"].get("items"), list):
            fields = schema["data"]["items"]
        else:
            raise ToolboxError("schema JSON must contain fields, items, or data.items")
    else:
        raise ToolboxError("schema JSON must be an object or array")
    return [field for field in fields if isinstance(field, dict)]


def make_create_body(field: dict[str, Any]) -> dict[str, Any]:
    body = {
        "field_name": field.get("field_name"),
        "type": field.get("type"),
    }
    if "property" in field and field.get("property") not in (None, {}, []):
        body["property"] = field.get("property")
    if not body["field_name"]:
        raise ToolboxError(f"field missing field_name: {json_dumps(redact(field))}")
    if body["type"] is None:
        raise ToolboxError(f"field missing type: {json_dumps(redact(field))}")
    return body


def should_skip(field: dict[str, Any], args: argparse.Namespace) -> str | None:
    field_type = field.get("type")
    try:
        normalized_type = int(field_type)
    except (TypeError, ValueError):
        normalized_type = field_type
    ui_type = str(field.get("ui_type", "")).lower()
    if not args.include_system_types and normalized_type in READ_ONLY_OR_SYSTEM_TYPES:
        return f"system/read-only type {field_type}"
    if not args.include_unsupported_ui_types and any(part in ui_type for part in UNSUPPORTED_UI_TYPES):
        return f"unsupported ui_type {ui_type}"
    return None


def fields_endpoint(args: argparse.Namespace) -> str:
    path = FIELDS_PATH.format(app_token=args.app_token, table_id=args.table_id)
    return args.base_url.rstrip("/") + path


def fetch_existing_names(args: argparse.Namespace, token: str) -> set[str]:
    names: set[str] = set()
    page_token = ""
    while True:
        query = "?page_size=100"
        if page_token:
            query += f"&page_token={page_token}"
        data = request_json(
            "GET",
            fields_endpoint(args) + query,
            headers={"Authorization": f"Bearer {token}"},
            timeout=args.timeout,
        )
        if not isinstance(data, dict) or data.get("code") not in (0, None):
            raise ToolboxError(f"failed to list existing fields: {json_dumps(redact(data))}")
        payload = data.get("data", {})
        items = payload.get("items", []) if isinstance(payload, dict) else []
        for item in items:
            if isinstance(item, dict) and item.get("field_name"):
                names.add(str(item["field_name"]))
        if not payload.get("has_more"):
            return names
        page_token = str(payload.get("page_token") or "")
        if not page_token:
            raise ToolboxError("existing field list has_more=true but page_token is empty")


def run(args: argparse.Namespace) -> int:
    schema = read_json_file(args.schema)
    fields = extract_fields(schema)
    planned: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for field in fields:
        reason = should_skip(field, args)
        if reason:
            skipped.append({"field_name": str(field.get("field_name", "")), "reason": reason})
            continue
        planned.append(make_create_body(field))

    if not args.execute:
        print(
            json_dumps(
                {
                    "dry_run": True,
                    "target": {"app_token": "<redacted>", "table_id": args.table_id},
                    "endpoint": fields_endpoint(args).replace(args.app_token, "<redacted>"),
                    "planned_requests": redact(planned),
                    "skipped": skipped,
                    "note": "No network write was performed. Add --execute to create fields.",
                }
            )
        )
        return 0

    token = get_tenant_access_token(args.base_url, args.timeout)
    existing = set() if args.no_skip_existing else fetch_existing_names(args, token)
    created: list[dict[str, Any]] = []
    execute_skipped = list(skipped)
    for body in planned:
        name = str(body["field_name"])
        if existing and name in existing:
            execute_skipped.append({"field_name": name, "reason": "already exists"})
            continue
        data = request_json(
            "POST",
            fields_endpoint(args),
            headers={"Authorization": f"Bearer {token}"},
            payload=body,
            timeout=args.timeout,
        )
        if not isinstance(data, dict) or data.get("code") not in (0, None):
            raise ToolboxError(f"failed to create field {name!r}: {json_dumps(redact(data))}")
        created.append({"field_name": name, "response": redact(data.get("data", data))})

    print(
        json_dumps(
            {
                "dry_run": False,
                "target": {"app_token": "<redacted>", "table_id": args.table_id},
                "created_count": len(created),
                "created": created,
                "skipped": execute_skipped,
            }
        )
    )
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
