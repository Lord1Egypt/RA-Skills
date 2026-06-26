#!/usr/bin/env python3
"""Small helper for calling the supported Dream Weaver photo and billing endpoints."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


ENDPOINT_RULES = (
    ("/api/v2/generate-image", "user-key", "TUQU_BASE_URL", "https://photo.tuqu.ai"),
    ("/api/v2/apply-preset", "user-key", "TUQU_BASE_URL", "https://photo.tuqu.ai"),
    ("/api/v2/generate-for-character", "user-key", "TUQU_BASE_URL", "https://photo.tuqu.ai"),
    ("/api/billing/balance", "user-key", "TUQU_BASE_URL", "https://photo.tuqu.ai"),
    ("/api/characters", "api-key", "TUQU_BASE_URL", "https://photo.tuqu.ai"),
    ("/api/history", "api-key", "TUQU_BASE_URL", "https://photo.tuqu.ai"),
    ("/api/enhance-prompt", "none", "TUQU_BASE_URL", "https://photo.tuqu.ai"),
    ("/api/catalog", "none", "TUQU_BASE_URL", "https://photo.tuqu.ai"),
    ("/api/model-costs", "none", "TUQU_BASE_URL", "https://photo.tuqu.ai"),
    ("/api/pricing-config", "none", "TUQU_BASE_URL", "https://photo.tuqu.ai"),
    (
        "/api/v1/recharge/plans",
        "service-key",
        "TUQU_BILLING_BASE_URL",
        "https://billing.tuqu.ai",
    ),
    (
        "/api/v1/recharge/wechat",
        "service-key",
        "TUQU_BILLING_BASE_URL",
        "https://billing.tuqu.ai",
    ),
    (
        "/api/v1/recharge/stripe",
        "service-key",
        "TUQU_BILLING_BASE_URL",
        "https://billing.tuqu.ai",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call supported Dream Weaver endpoints with the correct auth mode."
    )
    parser.add_argument("method", help="HTTP method, for example GET or POST")
    parser.add_argument("path", help="API path such as /api/catalog")
    parser.add_argument(
        "--base-url",
        help=(
            "Base URL for the API. If omitted, the helper picks the photo or billing host "
            "based on the endpoint path."
        ),
    )
    parser.add_argument(
        "--query",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Query parameter, repeat as needed",
    )
    parser.add_argument("--json", help="Inline JSON body string")
    parser.add_argument("--body-file", help="Path to a JSON file used as the request body")
    parser.add_argument(
        "--service-key",
        help=(
            "Credential supplied explicitly by the caller for authenticated endpoints. "
            "The helper maps it to body userKey, header x-api-key, or bearer auth "
            "based on the endpoint."
        ),
    )
    parser.add_argument(
        "--auth-mode",
        choices=("auto", "none", "user-key", "api-key", "service-key"),
        default="auto",
        help="Authentication mode. Auto detects for the endpoints covered by this skill.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Request timeout in seconds",
    )
    return parser.parse_args()


def parse_query_items(items: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid --query value '{item}'. Use KEY=VALUE.")
        key, value = item.split("=", 1)
        pairs.append((key, value))
    return pairs


def load_body(args: argparse.Namespace) -> Any | None:
    if args.json and args.body_file:
        raise ValueError("Use either --json or --body-file, not both.")

    if args.json:
        return json.loads(args.json)

    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as handle:
            return json.load(handle)

    return None


def normalize_path(path: str) -> str:
    parsed = urllib.parse.urlparse(path)
    if parsed.scheme and parsed.netloc:
        return parsed.path or "/"
    return path.split("?", 1)[0]


def match_endpoint_rule(path: str) -> tuple[str, str, str, str]:
    lookup_path = normalize_path(path)
    for rule in ENDPOINT_RULES:
        prefix = rule[0]
        if lookup_path == prefix or lookup_path.startswith(prefix + "/"):
            return rule
    raise ValueError(
        "This path is not covered by the helper. Pass --base-url and --auth-mode explicitly."
    )


def detect_auth_mode(path: str) -> str:
    return match_endpoint_rule(path)[1]


def detect_base_url(path: str) -> str:
    _, _, env_name, default_base_url = match_endpoint_rule(path)
    return os.environ.get(env_name, default_base_url)


def resolve_query_value(query_items: list[tuple[str, str]], key: str) -> str | None:
    for query_key, query_value in query_items:
        if query_key == key and query_value:
            return query_value
    return None


def resolve_service_key(
    explicit_service_key: str | None,
    body: Any | None,
    query_items: list[tuple[str, str]],
) -> str | None:
    if explicit_service_key:
        return explicit_service_key

    if isinstance(body, dict):
        for key in ("serviceKey", "userKey"):
            value = body.get(key)
            if isinstance(value, str) and value:
                return value

    for key in ("serviceKey", "userKey"):
        query_value = resolve_query_value(query_items, key)
        if query_value:
            return query_value

    return None


def prepare_body(auth_mode: str, body: Any | None, service_key: str | None = None) -> Any | None:
    if auth_mode == "service-key":
        if body is None:
            return None
        if not isinstance(body, dict):
            raise ValueError("Service-key endpoints require a JSON object body when a body is sent.")
        if "serviceKey" not in body and "userKey" in body:
            body["serviceKey"] = body.pop("userKey")
        return body

    if auth_mode != "user-key":
        return body

    if body is None:
        body = {}

    if not isinstance(body, dict):
        raise ValueError("Body-auth endpoints require a JSON object body.")

    if "userKey" not in body:
        if not service_key:
            raise ValueError(
                "Missing service key. Pass --service-key or provide userKey in the JSON body."
            )
        body["userKey"] = service_key

    return body


def build_url(base_url: str, path: str, query_items: list[tuple[str, str]]) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        base = path
    else:
        base = urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))

    if not query_items:
        return base

    separator = "&" if urllib.parse.urlparse(base).query else "?"
    return base + separator + urllib.parse.urlencode(query_items)


def dump_response(payload: bytes) -> None:
    text = payload.decode("utf-8", errors="replace")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        print(text)
        return

    print(json.dumps(parsed, indent=2, ensure_ascii=False))


def main() -> int:
    try:
        args = parse_args()
        query_items = parse_query_items(args.query)
        body = load_body(args)

        auth_mode = args.auth_mode
        if auth_mode == "auto":
            auth_mode = detect_auth_mode(args.path)

        body = prepare_body(auth_mode, body, args.service_key)
        base_url = args.base_url or detect_base_url(args.path)

        headers = {
            "Accept": "application/json",
        }

        if auth_mode == "api-key":
            if not args.service_key:
                raise ValueError("Missing service key. Pass --service-key for this endpoint.")
            headers["x-api-key"] = args.service_key

        if auth_mode == "service-key":
            service_key = resolve_service_key(args.service_key, body, query_items)
            if not service_key:
                raise ValueError(
                    "Missing service key. Pass --service-key, pass --query "
                    "serviceKey=..., or provide serviceKey in the JSON body."
                )
            headers["Authorization"] = f"Bearer {service_key}"

        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body).encode("utf-8")

        url = build_url(base_url, args.path, query_items)
        request = urllib.request.Request(
            url=url,
            data=data,
            headers=headers,
            method=args.method.upper(),
        )

        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            dump_response(response.read())
            return 0
    except urllib.error.HTTPError as exc:
        sys.stderr.write(f"HTTP {exc.code}\n")
        dump_response(exc.read())
        return 1
    except urllib.error.URLError as exc:
        sys.stderr.write(f"Request failed: {exc.reason}\n")
        return 1
    except Exception as exc:  # pylint: disable=broad-except
        sys.stderr.write(f"{exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
