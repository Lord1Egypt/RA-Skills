#!/usr/bin/env python3
"""Small direct-HTTP Open Plantbook CLI helper for the Open Plantbook skill.

Supported commands:
  search QUERY
  detail PID_OR_SCIENTIFIC_NAME
  create --from-dossier DOSSIER.json

Credentials may be provided through process environment variables or an explicit
private env file. The helper never depends on openplantbook-sdk.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


DEFAULT_API_BASE = "https://open.plantbook.io"
USER_AGENT = "openplantbook-agent-skill/1.0 (+https://open.plantbook.io/docs/)"


def _parse_env_value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _load_private_env_file() -> None:
    env_file = os.getenv("OPENPLANTBOOK_ENV_FILE", "").strip()
    if not env_file:
        return
    path = Path(env_file).expanduser()
    if not path.is_file():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped[len("export ") :].lstrip()
        if "=" not in stripped:
            continue
        key, raw_value = stripped.split("=", 1)
        key = key.strip()
        if key in {
            "OPENPLANTBOOK_CLIENT_ID",
            "OPENPLANTBOOK_CLIENT_SECRET",
            "OPENPLANTBOOK_OAUTH_CREDENTIALS",
            "OPENPLANTBOOK_API_KEY",
        }:
            os.environ.setdefault(key, _parse_env_value(raw_value))


def _get_oauth_credentials() -> tuple[str | None, str | None]:
    client_id = os.getenv("OPENPLANTBOOK_CLIENT_ID")
    client_secret = os.getenv("OPENPLANTBOOK_CLIENT_SECRET")
    if client_id and client_secret:
        return client_id, client_secret

    bundled = os.getenv("OPENPLANTBOOK_OAUTH_CREDENTIALS", "").strip()
    if not bundled:
        return client_id, client_secret

    if bundled.startswith("{"):
        try:
            parsed = json.loads(bundled)
        except json.JSONDecodeError as exc:
            print("OPENPLANTBOOK_OAUTH_CREDENTIALS contains invalid JSON.", file=sys.stderr)
            raise SystemExit(2) from exc
        return parsed.get("client_id"), parsed.get("client_secret")

    if ":" in bundled:
        bundled_client_id, bundled_client_secret = bundled.split(":", 1)
        return bundled_client_id.strip(), bundled_client_secret.strip()

    print(
        "OPENPLANTBOOK_OAUTH_CREDENTIALS must be JSON with client_id/client_secret "
        "or a colon-separated client_id:client_secret pair.",
        file=sys.stderr,
    )
    raise SystemExit(2)


def _get_api_key() -> str | None:
    _load_private_env_file()
    api_key = os.getenv("OPENPLANTBOOK_API_KEY")
    if api_key:
        return api_key
    return None


def _api_base() -> str:
    return DEFAULT_API_BASE


def _request_json(
    method: str,
    path: str,
    *,
    headers: dict[str, str] | None = None,
    query: dict[str, str] | None = None,
    body: bytes | None = None,
    allow_http_error: bool = False,
    return_status: bool = False,
) -> Any:
    url = f"{_api_base()}{path}"
    if query:
        clean_query = {key: value for key, value in query.items() if value is not None}
        if clean_query:
            url = f"{url}?{urlencode(clean_query)}"
    request = Request(
        url,
        data=body,
        method=method,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
            **(headers or {}),
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            status = response.status
            payload = response.read().decode("utf-8")
    except HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        if allow_http_error:
            data = _parse_json_response(body_text)
            if return_status:
                return exc.code, data
            return data
        print(f"Open Plantbook API returned HTTP {exc.code}: {body_text}", file=sys.stderr)
        raise SystemExit(1) from exc
    except URLError as exc:
        print(f"Open Plantbook API request failed: {exc.reason}", file=sys.stderr)
        raise SystemExit(1) from exc
    if not payload:
        data = None
    else:
        data = json.loads(payload)
    if return_status:
        return status, data
    return data


def _parse_json_response(payload: str) -> Any:
    if not payload:
        return None
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return payload


def _oauth_token() -> str | None:
    _load_private_env_file()
    client_id, client_secret = _get_oauth_credentials()
    if not client_id or not client_secret:
        return None
    body = urlencode(
        {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
    ).encode("utf-8")
    data = _request_json(
        "POST",
        "/api/v1/token/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        body=body,
    )
    token = data.get("access_token") if isinstance(data, dict) else None
    if not token:
        print("Open Plantbook OAuth token response did not include access_token.", file=sys.stderr)
        raise SystemExit(1)
    return token


def _auth_headers() -> dict[str, str]:
    api_key = _get_api_key()
    if api_key:
        return {"Authorization": f"Token {api_key}"}

    token = _oauth_token()
    if token:
        return {"Authorization": f"Bearer {token}"}

    print(
        "Set OPENPLANTBOOK_API_KEY, or set OPENPLANTBOOK_CLIENT_ID and "
        "OPENPLANTBOOK_CLIENT_SECRET. Supported sources: process environment "
        "or explicit OPENPLANTBOOK_ENV_FILE. Do not use public Browse DB HTML "
        "as a fallback.",
        file=sys.stderr,
    )
    raise SystemExit(2)


def _oauth_auth_headers() -> dict[str, str]:
    token = _oauth_token()
    if token:
        return {"Authorization": f"Bearer {token}"}

    print(
        "Create requires OAuth credentials. Set OPENPLANTBOOK_CLIENT_ID and "
        "OPENPLANTBOOK_CLIENT_SECRET in the process environment or explicit "
        "OPENPLANTBOOK_ENV_FILE.",
        file=sys.stderr,
    )
    raise SystemExit(2)


def _schema_component(schema: dict[str, Any], name: str) -> dict[str, Any]:
    component = schema.get("components", {}).get("schemas", {}).get(name)
    if not isinstance(component, dict):
        print(f"Open Plantbook schema did not include components.schemas.{name}.", file=sys.stderr)
        raise SystemExit(1)
    return component


def _coerce_schema_value(field: str, value: Any, spec: dict[str, Any]) -> Any:
    if value is None:
        if spec.get("nullable"):
            return None
        raise ValueError(f"{field} is not nullable")

    field_type = spec.get("type")
    if field_type == "string":
        if not isinstance(value, str):
            raise ValueError(f"{field} must be a string")
        return value

    if field_type == "integer":
        if isinstance(value, bool):
            raise ValueError(f"{field} must be an integer")
        if isinstance(value, int):
            coerced = value
        elif isinstance(value, float) and value.is_integer():
            coerced = int(value)
        elif isinstance(value, str) and value.strip().lstrip("-").isdigit():
            coerced = int(value.strip())
        else:
            raise ValueError(f"{field} must be an integer")

        minimum = spec.get("minimum")
        maximum = spec.get("maximum")
        if minimum is not None and coerced < minimum:
            raise ValueError(f"{field} is below schema minimum {minimum}")
        if maximum is not None and coerced > maximum:
            raise ValueError(f"{field} is above schema maximum {maximum}")
        return coerced

    return value


def _build_create_payload(
    dossier: dict[str, Any],
    create_schema: dict[str, Any],
    *,
    truncate: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    properties = create_schema.get("properties", {})
    if not isinstance(properties, dict):
        print("PlantCreateRequest schema did not include a properties object.", file=sys.stderr)
        raise SystemExit(1)

    payload: dict[str, Any] = {}
    errors: list[str] = []
    truncated: dict[str, dict[str, int]] = {}

    for field, raw_spec in properties.items():
        if field not in dossier:
            continue
        spec = raw_spec if isinstance(raw_spec, dict) else {}
        try:
            value = _coerce_schema_value(field, dossier[field], spec)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        max_length = spec.get("maxLength")
        if isinstance(value, str) and isinstance(max_length, int) and len(value) > max_length:
            if not truncate:
                errors.append(f"{field} length {len(value)} exceeds maxLength {max_length}")
                continue
            original_length = len(value)
            value = value[:max_length].rstrip()
            truncated[field] = {"from": original_length, "to": len(value)}
        payload[field] = value

    required = create_schema.get("required", [])
    for field in required if isinstance(required, list) else []:
        if field not in payload:
            errors.append(f"{field} is required by PlantCreateRequest")

    if errors:
        for error in errors:
            print(f"Invalid dossier payload: {error}", file=sys.stderr)
        raise SystemExit(2)

    ignored_fields = sorted(set(dossier) - set(properties))
    report = {
        "payload_keys": sorted(payload),
        "ignored_fields": ignored_fields,
        "truncated_fields": truncated,
    }
    return payload, report


def _print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))


async def _search(args: argparse.Namespace) -> None:
    query = {"alias": args.query}
    if args.userplant is not None:
        query["userplant"] = str(args.userplant).lower()
    if args.limit is not None:
        query["limit"] = str(args.limit)
    if args.offset is not None:
        query["offset"] = str(args.offset)
    results = _request_json("GET", "/api/v1/plant/search", headers=_auth_headers(), query=query)
    _print_json(results)


async def _detail(args: argparse.Namespace) -> None:
    query = {}
    if args.lang:
        query["lang"] = args.lang
    if args.include:
        query["include"] = args.include
    details = _request_json(
        "GET",
        f"/api/v1/plant/detail/{quote(args.plant, safe='')}/",
        headers=_auth_headers(),
        query=query,
    )
    _print_json(details)


async def _create(args: argparse.Namespace) -> None:
    dossier_path = Path(args.from_dossier).expanduser()
    try:
        dossier = json.loads(dossier_path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"Could not read dossier {dossier_path}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    except json.JSONDecodeError as exc:
        print(f"Dossier {dossier_path} is not valid JSON: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    if not isinstance(dossier, dict):
        print("Dossier JSON must be an object.", file=sys.stderr)
        raise SystemExit(2)

    schema = _request_json("GET", "/api/schema/")
    create_schema = _schema_component(schema, "PlantCreateRequest")
    payload, report = _build_create_payload(dossier, create_schema, truncate=not args.no_truncate)

    if args.dry_run:
        _print_json({"dry_run": True, "payload": payload, **report})
        return

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    status, result = _request_json(
        "POST",
        "/api/v1/plant/create",
        headers={**_oauth_auth_headers(), "Content-Type": "application/json"},
        body=body,
        allow_http_error=True,
        return_status=True,
    )
    output = {"status": status, "result": result, **report}
    _print_json(output)
    if status not in {200, 201}:
        raise SystemExit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Open Plantbook direct-HTTP helper CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search plants by name")
    search.add_argument("query", help="Plant search query, e.g. abelia")
    search.add_argument("--userplant", choices=("true", "false"), help="Scope search to user/public plants")
    search.add_argument("--limit", type=int, help="Optional result limit")
    search.add_argument("--offset", type=int, help="Optional result offset")
    search.set_defaults(func=_search)

    detail = subparsers.add_parser("detail", help="Get plant details by PID/scientific name")
    detail.add_argument("plant", help="Plant PID or scientific name, e.g. 'abelia chinensis'")
    detail.add_argument("--lang", help="Optional ISO 639-1 language code, e.g. en, de, es")
    detail.add_argument("--include", help="Optional include value such as care, care,poison, or *")
    detail.set_defaults(func=_detail)

    create = subparsers.add_parser("create", help="Create a user plant from a schema-aligned dossier JSON")
    create.add_argument("--from-dossier", required=True, help="Path to an Open Plantbook dossier JSON")
    create.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the outgoing create payload without calling the create endpoint",
    )
    create.add_argument(
        "--no-truncate",
        action="store_true",
        help="Fail instead of truncating overlong string fields to schema maxLength",
    )
    create.set_defaults(func=_create)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if isinstance(getattr(args, "userplant", None), str):
        args.userplant = args.userplant == "true"
    asyncio.run(args.func(args))


if __name__ == "__main__":
    main()
