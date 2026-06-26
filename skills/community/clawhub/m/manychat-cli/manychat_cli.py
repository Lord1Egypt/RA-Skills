#!/usr/bin/env python3
"""ManyChat CLI for automation-friendly workflows.

Designed for agentic usage (OpenClaw/other AI agents):
- deterministic JSON output
- explicit exit codes
- thin wrapper over official ManyChat API endpoints
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib import error, request

DEFAULT_BASE_URL = "https://api.manychat.com"
ENV_API_KEY = "MANYCHAT_API_KEY"
ENV_BASE_URL = "MANYCHAT_BASE_URL"


class CLIError(Exception):
    """Expected CLI error with a user-facing message."""


@dataclass
class ManyChatClient:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    timeout_seconds: int = 30

    def call(self, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint

        url = f"{self.base_url.rstrip('/')}{endpoint}"
        body = json.dumps(payload or {}).encode("utf-8")

        req = request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as resp:
                raw = resp.read().decode("utf-8")
        except error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            raise CLIError(f"HTTP {exc.code} from ManyChat: {raw}") from exc
        except error.URLError as exc:
            raise CLIError(f"Network error calling ManyChat: {exc.reason}") from exc

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise CLIError(f"ManyChat returned non-JSON response: {raw}") from exc

        status = parsed.get("status")
        if status and status != "success":
            # Preserve full payload for debugging in caller output.
            raise CLIError(f"ManyChat returned error status: {status}")

        return parsed


_TEMPLATE_RE = re.compile(r"\{\{([^{}]+)\}\}")


def _lookup_path(data: Any, path: str) -> Any:
    """Resolve dotted paths with optional numeric indexes, e.g. step1.data.0.id."""
    current = data
    for part in path.split("."):
        part = part.strip()
        if part == "":
            continue
        if isinstance(current, list):
            if not part.isdigit():
                raise CLIError(f"Template path expects list index but got key '{part}'")
            idx = int(part)
            try:
                current = current[idx]
            except IndexError as exc:
                raise CLIError(f"Template list index out of range: {part}") from exc
            continue
        if isinstance(current, dict):
            if part not in current:
                raise CLIError(f"Template key not found: {part}")
            current = current[part]
            continue
        raise CLIError(f"Template path cannot continue through non-container at '{part}'")
    return current


def _render_node(node: Any, context: Dict[str, Any]) -> Any:
    """Render strings containing {{path}} tokens against context recursively."""
    if isinstance(node, dict):
        return {k: _render_node(v, context) for k, v in node.items()}
    if isinstance(node, list):
        return [_render_node(v, context) for v in node]
    if not isinstance(node, str):
        return node

    matches = list(_TEMPLATE_RE.finditer(node))
    if not matches:
        return node

    # If the whole string is a single token, preserve original type.
    if len(matches) == 1 and matches[0].span() == (0, len(node)):
        path = matches[0].group(1).strip()
        return _lookup_path(context, path)

    rendered = node
    for m in matches:
        raw = m.group(0)
        path = m.group(1).strip()
        value = _lookup_path(context, path)
        rendered = rendered.replace(raw, str(value))
    return rendered


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-key", help=f"ManyChat API key (fallback: ${ENV_API_KEY})")
    parser.add_argument("--base-url", default=None, help=f"API base URL (default: {DEFAULT_BASE_URL} or ${ENV_BASE_URL})")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds (default: 30)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="manychat",
        description="Automation-friendly CLI for ManyChat API.",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # Generic endpoint passthrough to future-proof automation scripts.
    p_raw = sub.add_parser("raw", help="Call any ManyChat endpoint directly")
    add_common_args(p_raw)
    p_raw.add_argument("endpoint", help="Endpoint path, e.g. /fb/page/getInfo")
    p_raw.add_argument("--data", default="{}", help="Raw JSON payload string")

    p_playbook = sub.add_parser("playbook-run", help="Run a JSON playbook with template variables")
    add_common_args(p_playbook)
    p_playbook.add_argument("--file", required=True, help="Path to playbook JSON file")
    p_playbook.add_argument(
        "--vars-json",
        default="{}",
        help='Optional JSON object for playbook vars, e.g. {"email":"lead@example.com"}',
    )

    p_ping = sub.add_parser("ping", help="Validate API token with /fb/page/getInfo")
    add_common_args(p_ping)

    p_page_tags = sub.add_parser("page-tags", help="Get page tags")
    add_common_args(p_page_tags)

    p_page_fields = sub.add_parser("page-fields", help="Get page custom fields")
    add_common_args(p_page_fields)

    p_page_flows = sub.add_parser("page-flows", help="Get page flows")
    add_common_args(p_page_flows)

    p_sub_info = sub.add_parser("sub-info", help="Get subscriber info")
    add_common_args(p_sub_info)
    p_sub_info.add_argument("--subscriber-id", required=True, type=int)

    p_find_system = sub.add_parser("find-system", help="Find subscriber by system field")
    add_common_args(p_find_system)
    p_find_system.add_argument("--field-name", required=True, help="System field name (e.g. email, phone)")
    p_find_system.add_argument("--field-value", required=True)

    p_find_custom = sub.add_parser("find-custom", help="Find subscribers by custom field")
    add_common_args(p_find_custom)
    p_find_custom.add_argument("--field-id", required=True, type=int)
    p_find_custom.add_argument("--field-value", required=True)

    p_add_tag = sub.add_parser("tag-add", help="Add tag to subscriber")
    add_common_args(p_add_tag)
    p_add_tag.add_argument("--subscriber-id", required=True, type=int)
    tag_group_add = p_add_tag.add_mutually_exclusive_group(required=True)
    tag_group_add.add_argument("--tag-id", type=int)
    tag_group_add.add_argument("--tag-name")

    p_remove_tag = sub.add_parser("tag-remove", help="Remove tag from subscriber")
    add_common_args(p_remove_tag)
    p_remove_tag.add_argument("--subscriber-id", required=True, type=int)
    tag_group_remove = p_remove_tag.add_mutually_exclusive_group(required=True)
    tag_group_remove.add_argument("--tag-id", type=int)
    tag_group_remove.add_argument("--tag-name")

    p_set_cf = sub.add_parser("field-set", help="Set a single custom field for subscriber")
    add_common_args(p_set_cf)
    p_set_cf.add_argument("--subscriber-id", required=True, type=int)
    cf_group = p_set_cf.add_mutually_exclusive_group(required=True)
    cf_group.add_argument("--field-id", type=int)
    cf_group.add_argument("--field-name")
    p_set_cf.add_argument("--value", required=True, help="Field value (string, number, bool, or null)")
    p_set_cf.add_argument("--value-json", action="store_true", help="Parse --value as raw JSON")

    p_set_cfs = sub.add_parser("fields-set", help="Set multiple custom fields for subscriber")
    add_common_args(p_set_cfs)
    p_set_cfs.add_argument("--subscriber-id", required=True, type=int)
    p_set_cfs.add_argument(
        "--fields-json",
        required=True,
        help='JSON array, e.g. [{"field_id":123,"field_value":"abc"}]',
    )

    p_flow = sub.add_parser("flow-send", help="Send flow to subscriber")
    add_common_args(p_flow)
    p_flow.add_argument("--subscriber-id", required=True, type=int)
    p_flow.add_argument("--flow-ns", required=True, help="Flow namespace (flow_ns)")

    p_content = sub.add_parser("content-send", help="Send dynamic content payload to subscriber")
    add_common_args(p_content)
    p_content.add_argument("--subscriber-id", required=True, type=int)
    p_content.add_argument("--data-json", required=True, help="Raw content data JSON")
    p_content.add_argument("--message-tag", default="")

    p_create = sub.add_parser("sub-create", help="Create a subscriber")
    add_common_args(p_create)
    p_create.add_argument("--phone")
    p_create.add_argument("--email")
    p_create.add_argument("--first-name", default=None)
    p_create.add_argument("--last-name", default=None)
    p_create.add_argument("--gender", default=None)
    p_create.add_argument("--has-opt-in-sms", action="store_true")
    p_create.add_argument("--has-opt-in-email", action="store_true")
    p_create.add_argument("--consent-phrase", default="")

    p_update = sub.add_parser("sub-update", help="Update a subscriber")
    add_common_args(p_update)
    p_update.add_argument("--subscriber-id", required=True, type=int)
    p_update.add_argument("--data-json", required=True, help="Raw subscriber update JSON")

    return parser


def get_client(args: argparse.Namespace) -> ManyChatClient:
    api_key = args.api_key or os.getenv(ENV_API_KEY)
    if not api_key:
        raise CLIError(f"Missing API key. Pass --api-key or set {ENV_API_KEY}.")
    base_url = args.base_url or os.getenv(ENV_BASE_URL) or DEFAULT_BASE_URL
    return ManyChatClient(api_key=api_key, base_url=base_url, timeout_seconds=args.timeout)


def parse_value(raw: str, value_json: bool) -> Any:
    if value_json:
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise CLIError(f"Invalid JSON passed to --value: {raw}") from exc

    lowered = raw.strip().lower()
    if lowered == "null":
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False

    # Attempt numeric parsing for convenience.
    try:
        if "." in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        return raw


def run(args: argparse.Namespace) -> Dict[str, Any]:
    client = get_client(args)

    if args.command == "raw":
        payload = json.loads(args.data)
        return client.call(args.endpoint, payload)

    if args.command == "playbook-run":
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                playbook = json.load(f)
        except OSError as exc:
            raise CLIError(f"Unable to read playbook file: {args.file}") from exc
        except json.JSONDecodeError as exc:
            raise CLIError(f"Invalid playbook JSON in file: {args.file}") from exc

        try:
            vars_json = json.loads(args.vars_json)
        except json.JSONDecodeError as exc:
            raise CLIError("Invalid JSON passed to --vars-json") from exc

        if not isinstance(playbook, dict):
            raise CLIError("Playbook root must be a JSON object")
        steps = playbook.get("steps")
        if not isinstance(steps, list) or not steps:
            raise CLIError("Playbook must include a non-empty steps array")

        context: Dict[str, Any] = {
            "vars": vars_json if isinstance(vars_json, dict) else {},
            "results": {},
        }
        results: list[Dict[str, Any]] = []

        for i, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                raise CLIError(f"Step {i} must be an object")
            endpoint = step.get("endpoint")
            if not isinstance(endpoint, str) or not endpoint.strip():
                raise CLIError(f"Step {i} missing endpoint")
            step_id = step.get("id") or f"step{i}"
            payload = _render_node(step.get("payload", {}), context)
            response = client.call(endpoint, payload)
            step_result = {
                "id": step_id,
                "endpoint": endpoint,
                "request": payload,
                "response": response,
            }
            results.append(step_result)
            context["results"][step_id] = response

        return {"playbook_file": args.file, "steps": results}

    if args.command == "ping":
        return client.call("/fb/page/getInfo")

    if args.command == "page-tags":
        return client.call("/fb/page/getTags")

    if args.command == "page-fields":
        return client.call("/fb/page/getCustomFields")

    if args.command == "page-flows":
        return client.call("/fb/page/getFlows")

    if args.command == "sub-info":
        return client.call("/fb/subscriber/getInfo", {"subscriber_id": args.subscriber_id})

    if args.command == "find-system":
        return client.call(
            "/fb/subscriber/findBySystemField",
            {"field_name": args.field_name, "field_value": args.field_value},
        )

    if args.command == "find-custom":
        return client.call(
            "/fb/subscriber/findByCustomField",
            {"field_id": args.field_id, "field_value": args.field_value},
        )

    if args.command == "tag-add":
        if args.tag_id is not None:
            return client.call(
                "/fb/subscriber/addTag",
                {"subscriber_id": args.subscriber_id, "tag_id": args.tag_id},
            )
        return client.call(
            "/fb/subscriber/addTagByName",
            {"subscriber_id": args.subscriber_id, "tag_name": args.tag_name},
        )

    if args.command == "tag-remove":
        if args.tag_id is not None:
            return client.call(
                "/fb/subscriber/removeTag",
                {"subscriber_id": args.subscriber_id, "tag_id": args.tag_id},
            )
        return client.call(
            "/fb/subscriber/removeTagByName",
            {"subscriber_id": args.subscriber_id, "tag_name": args.tag_name},
        )

    if args.command == "field-set":
        value = parse_value(args.value, args.value_json)
        if args.field_id is not None:
            return client.call(
                "/fb/subscriber/setCustomField",
                {
                    "subscriber_id": args.subscriber_id,
                    "field_id": args.field_id,
                    "field_value": value,
                },
            )
        return client.call(
            "/fb/subscriber/setCustomFieldByName",
            {
                "subscriber_id": args.subscriber_id,
                "field_name": args.field_name,
                "field_value": value,
            },
        )

    if args.command == "fields-set":
        try:
            fields = json.loads(args.fields_json)
        except json.JSONDecodeError as exc:
            raise CLIError("Invalid JSON passed to --fields-json") from exc
        if not isinstance(fields, list):
            raise CLIError("--fields-json must be a JSON array")
        return client.call(
            "/fb/subscriber/setCustomFields",
            {"subscriber_id": args.subscriber_id, "fields": fields},
        )

    if args.command == "flow-send":
        return client.call(
            "/fb/sending/sendFlow",
            {"subscriber_id": args.subscriber_id, "flow_ns": args.flow_ns},
        )

    if args.command == "content-send":
        try:
            data = json.loads(args.data_json)
        except json.JSONDecodeError as exc:
            raise CLIError("Invalid JSON passed to --data-json") from exc
        payload = {
            "subscriber_id": args.subscriber_id,
            "data": data,
        }
        if args.message_tag:
            payload["message_tag"] = args.message_tag
        return client.call("/fb/sending/sendContent", payload)

    if args.command == "sub-create":
        if not args.phone and not args.email:
            raise CLIError("sub-create requires at least one of --phone or --email")

        payload: Dict[str, Any] = {
            "phone": args.phone,
            "email": args.email,
            "first_name": args.first_name,
            "last_name": args.last_name,
            "gender": args.gender,
            "has_opt_in_sms": args.has_opt_in_sms,
            "has_opt_in_email": args.has_opt_in_email,
            "consent_phrase": args.consent_phrase,
        }
        payload = {k: v for k, v in payload.items() if v is not None and v != ""}
        return client.call("/fb/subscriber/createSubscriber", payload)

    if args.command == "sub-update":
        try:
            body = json.loads(args.data_json)
        except json.JSONDecodeError as exc:
            raise CLIError("Invalid JSON passed to --data-json") from exc
        payload = {"subscriber_id": args.subscriber_id}
        payload.update(body)
        return client.call("/fb/subscriber/updateSubscriber", payload)

    raise CLIError(f"Unknown command: {args.command}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        response = run(args)
    except CLIError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(json.dumps({"ok": False, "error": f"Invalid JSON argument: {exc}"}, indent=2), file=sys.stderr)
        return 2
    except Exception as exc:  # defensive fallback for automation logs
        print(json.dumps({"ok": False, "error": f"Unexpected error: {exc}"}, indent=2), file=sys.stderr)
        return 1

    if args.pretty:
        print(json.dumps({"ok": True, "result": response}, indent=2))
    else:
        print(json.dumps({"ok": True, "result": response}))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
