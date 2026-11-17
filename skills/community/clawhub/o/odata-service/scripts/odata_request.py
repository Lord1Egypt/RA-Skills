#!/usr/bin/env python3
"""Guarded, dependency-free HTTP executor for OData v4 services."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from odata_profiles import resolve_profile_args  # noqa: E402


SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
CONDITIONAL_METHODS = {"PATCH", "PUT", "DELETE"}
VISIBLE_HEADERS = {
    "content-type",
    "content-length",
    "odata-version",
    "etag",
    "location",
    "odata-entityid",
    "preference-applied",
    "retry-after",
    "asyncresult",
}
USER_AGENT = "odata-service-skill/1.0"


def origin(url: str) -> tuple[str, str, int | None]:
    parsed = urllib.parse.urlsplit(url)
    scheme = parsed.scheme.lower()
    port = parsed.port
    if port is None:
        port = 443 if scheme == "https" else 80 if scheme == "http" else None
    return scheme, (parsed.hostname or "").lower(), port


def validate_service_root(root: str) -> str:
    parsed = urllib.parse.urlsplit(root)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("service root must be an absolute HTTP(S) URL")
    if parsed.query or parsed.fragment:
        raise ValueError("service root must not contain a query string or fragment")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("service root must not contain embedded credentials")
    return root.rstrip("/") + "/"


def resolve_path(root: str, path: str) -> str:
    service_root = validate_service_root(root)
    parsed = urllib.parse.urlsplit(path)
    if parsed.scheme or parsed.netloc:
        if origin(path) != origin(service_root):
            raise ValueError("absolute OData resource URLs must use the service-root origin")
        return path
    return urllib.parse.urljoin(service_root, path.lstrip("/"))


def add_query(url: str, raw_pairs: list[str]) -> str:
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for raw in raw_pairs:
        if "=" not in raw:
            raise ValueError("--query must be NAME=VALUE")
        name, value = raw.split("=", 1)
        if not name:
            raise ValueError("query option name cannot be empty")
        comparison = name.lower() if name.startswith("$") else name
        if comparison in seen:
            raise ValueError(f"query option {name!r} was specified more than once")
        seen.add(comparison)
        pairs.append((name, value))
    if not pairs:
        return url
    separator = "&" if urllib.parse.urlsplit(url).query else "?"
    return url + separator + urllib.parse.urlencode(pairs, safe="$@(),'/:")


def headers_from_args(args: argparse.Namespace) -> tuple[dict[str, str], bool]:
    headers = {
        "Accept": args.accept,
        "OData-Version": args.odata_version,
        "OData-MaxVersion": "4.01",
        "User-Agent": USER_AGENT,
    }
    sensitive = False
    if args.bearer_env and (args.basic_user_env or args.basic_password_env):
        raise ValueError("choose either bearer or basic authentication, not both")
    if args.bearer_env:
        token = os.environ.get(args.bearer_env)
        if not token:
            raise ValueError(f"environment variable {args.bearer_env!r} is empty or unset")
        headers["Authorization"] = "Bearer " + token
        sensitive = True
    if args.basic_user_env or args.basic_password_env:
        if not (args.basic_user_env and args.basic_password_env):
            raise ValueError("basic authentication requires both environment-variable options")
        user = os.environ.get(args.basic_user_env)
        password = os.environ.get(args.basic_password_env)
        if user is None or password is None:
            raise ValueError("a basic-auth environment variable is unset")
        headers["Authorization"] = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()
        sensitive = True
    for item in args.header_env:
        if "=" not in item:
            raise ValueError("--header-env must be NAME=ENV_VAR")
        name, env_name = item.split("=", 1)
        if not name.strip() or not env_name.strip():
            raise ValueError("--header-env must be NAME=ENV_VAR")
        value = os.environ.get(env_name)
        if value is None:
            raise ValueError(f"environment variable {env_name!r} is unset")
        headers[name.strip()] = value
        sensitive = True
    if args.if_match:
        headers["If-Match"] = args.if_match
    if args.if_none_match:
        headers["If-None-Match"] = args.if_none_match
    if args.prefer:
        headers["Prefer"] = ", ".join(args.prefer)
    return headers, sensitive


class ControlledRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, allow_public_cross_origin: bool, sensitive: bool):
        super().__init__()
        self.allow_public_cross_origin = allow_public_cross_origin
        self.sensitive = sensitive

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        resolved = urllib.parse.urljoin(req.full_url, newurl)
        if origin(resolved) == origin(req.full_url):
            return super().redirect_request(req, fp, code, msg, headers, resolved)
        if self.sensitive or req.get_method() not in {"GET", "HEAD"}:
            raise urllib.error.HTTPError(req.full_url, code, "Refusing cross-origin redirect", headers, fp)
        if not self.allow_public_cross_origin:
            raise urllib.error.HTTPError(req.full_url, code, "Cross-origin redirect requires explicit opt-in", headers, fp)
        safe_headers = {
            key: value
            for key, value in req.headers.items()
            if key.lower() in {"accept", "user-agent"}
        }
        return urllib.request.Request(resolved, headers=safe_headers, method=req.get_method())


def read_limited(response, limit: int) -> bytes:  # noqa: ANN001
    body = response.read(limit + 1)
    if len(body) > limit:
        raise RuntimeError(f"response exceeds --max-response-bytes ({limit})")
    return body


def perform(
    url: str,
    method: str,
    headers: dict[str, str],
    body: bytes | None,
    timeout: float,
    max_bytes: int,
    allow_cross_origin: bool,
    sensitive: bool,
) -> tuple[int, dict[str, str], bytes, str]:
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    opener = urllib.request.build_opener(ControlledRedirectHandler(allow_cross_origin, sensitive))
    try:
        with opener.open(request, timeout=timeout) as response:
            return response.status, dict(response.headers.items()), read_limited(response, max_bytes), response.geturl()
    except urllib.error.HTTPError as exc:
        response_body = read_limited(exc, max_bytes)
        return exc.code, dict(exc.headers.items()) if exc.headers else {}, response_body, exc.geturl()
    except urllib.error.URLError as exc:
        raise RuntimeError(f"request failed: {exc.reason}") from exc


def load_body(args: argparse.Namespace, method: str) -> bytes | None:
    if args.body_file and args.empty_body:
        raise ValueError("choose --body-file or --empty-body, not both")
    if method in SAFE_METHODS | {"DELETE"} and (args.body_file or args.empty_body):
        raise ValueError(f"{method} requests must not include a body in this helper")
    if method in {"POST", "PATCH", "PUT"} and not (args.body_file or args.empty_body):
        raise ValueError(f"{method} requires --body-file or --empty-body")
    if args.empty_body:
        return b""
    if not args.body_file:
        return None
    body = Path(args.body_file).read_bytes()
    if "json" in args.content_type.lower():
        try:
            json.loads(body)
        except json.JSONDecodeError as exc:
            raise ValueError(f"body file is not valid JSON: {exc}") from exc
    return body


def validate_mutation(args: argparse.Namespace, method: str) -> None:
    if method not in SAFE_METHODS and not args.allow_write:
        raise ValueError(f"{method} is state-changing; repeat with --allow-write after confirming the target")
    if method in CONDITIONAL_METHODS and not args.if_match and not args.allow_unconditional:
        raise ValueError(
            f"{method} requires --if-match with the current ETag, or --allow-unconditional after accepting overwrite risk"
        )


def visible_headers(headers: dict[str, str]) -> dict[str, str]:
    return {key: value for key, value in headers.items() if key.lower() in VISIBLE_HEADERS}


def redact_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    sensitive_fragments = ("token", "secret", "password", "signature", "sig", "key", "code")
    pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    redacted = [
        (name, "REDACTED" if any(fragment in name.lower() for fragment in sensitive_fragments) else value)
        for name, value in pairs
    ]
    query = urllib.parse.urlencode(redacted, doseq=True, safe="$@(),'/:")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query, ""))


def decoded_body(body: bytes, content_type: str) -> Any:
    if not body:
        return None
    if "json" in content_type.lower():
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"invalidJsonPreview": body[:2000].decode("utf-8", errors="replace")}
    if content_type.lower().startswith("text/") or "xml" in content_type.lower():
        return body.decode("utf-8", errors="replace")
    return {"binaryBytes": len(body), "note": "use --output-body to save binary content"}


def error_summary(body: bytes, content_type: str) -> Any:
    if "json" in content_type.lower():
        try:
            payload = json.loads(body)
            error = payload.get("error") if isinstance(payload, dict) else None
            if isinstance(error, dict):
                return {
                    key: error[key]
                    for key in ("code", "message", "target", "details")
                    if key in error
                }
        except json.JSONDecodeError:
            pass
    preview = " ".join(body.decode("utf-8", errors="replace").split())[:2000]
    return {"preview": preview} if preview else None


def write_json(value: Any) -> None:
    json.dump(value, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def execute_request(args: argparse.Namespace) -> None:
    method = args.method.upper()
    validate_mutation(args, method)
    url = add_query(resolve_path(args.service_root, args.path), args.query)
    headers, sensitive = headers_from_args(args)
    if sensitive and urllib.parse.urlsplit(url).scheme.lower() != "https":
        raise ValueError("refusing to send environment-provided credentials or headers over plain HTTP")
    body = load_body(args, method)
    if body is not None:
        headers["Content-Type"] = args.content_type
    status, response_headers, response_body, final_url = perform(
        url,
        method,
        headers,
        body,
        args.timeout,
        args.max_response_bytes,
        args.allow_public_cross_origin_redirect,
        sensitive,
    )
    if args.output_body:
        Path(args.output_body).write_bytes(response_body)
        rendered_body: Any = {"savedTo": str(Path(args.output_body)), "bytes": len(response_body)}
    else:
        content_type = response_headers.get("Content-Type", "")
        rendered_body = (
            error_summary(response_body, content_type)
            if status >= 400
            else decoded_body(response_body, content_type)
        )
    write_json(
        {
            "status": status,
            "url": redact_url(final_url),
            "headers": visible_headers(response_headers),
            "body": rendered_body,
        }
    )


def continuation(payload: Any, name: str) -> str | None:
    if not isinstance(payload, dict):
        return None
    return payload.get(f"@odata.{name}") or payload.get(f"@{name}")


def execute_pages(args: argparse.Namespace) -> None:
    url = add_query(resolve_path(args.service_root, args.path), args.query)
    headers, sensitive = headers_from_args(args)
    if sensitive and urllib.parse.urlsplit(url).scheme.lower() != "https":
        raise ValueError("refusing to send environment-provided credentials or headers over plain HTTP")
    expected_origin = origin(url)
    seen: set[str] = set()
    items: list[Any] = []
    pages = 0
    truncated = False
    context = count = delta_link = None
    while True:
        if url in seen:
            raise RuntimeError("the service returned a repeated next link")
        if origin(url) != expected_origin:
            raise RuntimeError("refusing a cross-origin next link")
        seen.add(url)
        status, response_headers, body, final_url = perform(
            url, "GET", headers, None, args.timeout, args.max_response_bytes, False, sensitive
        )
        if status < 200 or status >= 300:
            write_json(
                {
                    "status": status,
                    "url": redact_url(final_url),
                    "headers": visible_headers(response_headers),
                    "body": error_summary(body, response_headers.get("Content-Type", "")),
                }
            )
            return
        payload = decoded_body(body, response_headers.get("Content-Type", ""))
        if not isinstance(payload, dict) or not isinstance(payload.get("value"), list):
            raise RuntimeError("pages requires an OData JSON collection with a value array")
        pages += 1
        context = context or payload.get("@odata.context") or payload.get("@context")
        count = count if count is not None else payload.get("@odata.count", payload.get("@count"))
        page_items = payload["value"]
        remaining = args.max_items - len(items)
        items.extend(page_items[:remaining])
        next_link = continuation(payload, "nextLink")
        delta_link = continuation(payload, "deltaLink") or delta_link
        if len(page_items) > remaining:
            truncated = True
            break
        if not next_link:
            break
        if pages >= args.max_pages or len(items) >= args.max_items:
            truncated = True
            break
        url = urllib.parse.urljoin(final_url, next_link)
    result: dict[str, Any] = {"value": items, "_retrieval": {"pages": pages, "items": len(items), "truncated": truncated}}
    if context is not None:
        result["@odata.context"] = context
    if count is not None:
        result["@odata.count"] = count
    if delta_link is not None and not truncated:
        result["@odata.deltaLink"] = delta_link
    write_json(result)


def add_transport_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--service-root", help="absolute service root; use --profile or the configured default otherwise")
    parser.add_argument("--profile", help="saved service profile; omit to use the configured default")
    parser.add_argument("--config", help="profile config path")
    parser.add_argument("--path", default="", help="relative resource path or a same-origin absolute OData URL")
    parser.add_argument("--query", action="append", default=[], metavar="NAME=VALUE")
    parser.add_argument("--odata-version", choices=("4.0", "4.01"), default=None)
    parser.add_argument("--accept", default="application/json;odata.metadata=minimal")
    parser.add_argument("--bearer-env", metavar="ENV_VAR")
    parser.add_argument("--basic-user-env", metavar="ENV_VAR")
    parser.add_argument("--basic-password-env", metavar="ENV_VAR")
    parser.add_argument("--header-env", action="append", default=[], metavar="NAME=ENV_VAR")
    parser.add_argument("--if-match")
    parser.add_argument("--if-none-match")
    parser.add_argument("--prefer", action="append", default=[])
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--max-response-bytes", type=int, default=10_000_000)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    request = subparsers.add_parser("request", help="issue one guarded OData request")
    add_transport_options(request)
    request.add_argument("--method", choices=("GET", "HEAD", "OPTIONS", "POST", "PATCH", "PUT", "DELETE"), default="GET")
    request.add_argument("--body-file")
    request.add_argument("--empty-body", action="store_true")
    request.add_argument("--content-type", default="application/json")
    request.add_argument("--output-body", help="save the raw response body to this file")
    request.add_argument("--allow-write", action="store_true", help="required for state-changing methods")
    request.add_argument("--allow-unconditional", action="store_true", help="allow PATCH/PUT/DELETE without If-Match")
    request.add_argument(
        "--allow-public-cross-origin-redirect",
        action="store_true",
        help="follow a cross-origin GET/HEAD redirect only when no environment-provided headers are present",
    )
    request.set_defaults(handler=execute_request)

    pages = subparsers.add_parser("pages", help="retrieve bounded top-level JSON collection pages")
    add_transport_options(pages)
    pages.add_argument("--max-pages", type=int, default=100)
    pages.add_argument("--max-items", type=int, default=10_000)
    pages.set_defaults(handler=execute_pages)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    for name in ("timeout", "max_response_bytes", "max_pages", "max_items"):
        value = getattr(args, name, 1)
        if value <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    try:
        resolve_profile_args(args)
        args.handler(args)
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
