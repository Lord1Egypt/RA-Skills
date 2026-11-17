#!/usr/bin/env python3
"""Dependency-free, read-only OData v4 metadata and JSON query helper."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from odata_profiles import resolve_profile_args  # noqa: E402


USER_AGENT = "odata-query-skill/1.0"


def origin(url: str) -> tuple[str, str, int | None]:
    parsed = urllib.parse.urlsplit(url)
    scheme = parsed.scheme.lower()
    port = parsed.port
    if port is None:
        port = 443 if scheme == "https" else 80 if scheme == "http" else None
    return scheme, (parsed.hostname or "").lower(), port


class SameOriginRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        resolved = urllib.parse.urljoin(req.full_url, newurl)
        if origin(resolved) != origin(req.full_url):
            raise urllib.error.HTTPError(
                req.full_url,
                code,
                "Refusing credential-bearing cross-origin redirect",
                headers,
                fp,
            )
        return super().redirect_request(req, fp, code, msg, headers, resolved)


def service_url(root: str, resource: str) -> str:
    parsed = urllib.parse.urlsplit(root)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("service root must be an absolute HTTP(S) URL")
    if parsed.query or parsed.fragment:
        raise ValueError("service root must not contain a query string or fragment")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("service root must not contain embedded credentials")
    return root.rstrip("/") + "/" + resource.lstrip("/")


def headers_from_args(args: argparse.Namespace) -> dict[str, str]:
    headers = {
        "Accept": "application/json;odata.metadata=minimal",
        "OData-Version": args.odata_version,
        "OData-MaxVersion": "4.01",
        "User-Agent": USER_AGENT,
    }
    if args.bearer_env and (args.basic_user_env or args.basic_password_env):
        raise ValueError("choose either bearer or basic authentication, not both")
    if args.bearer_env:
        token = os.environ.get(args.bearer_env)
        if not token:
            raise ValueError(f"environment variable {args.bearer_env!r} is empty or unset")
        headers["Authorization"] = "Bearer " + token
    if args.basic_user_env or args.basic_password_env:
        if not (args.basic_user_env and args.basic_password_env):
            raise ValueError("basic authentication requires both environment-variable options")
        user = os.environ.get(args.basic_user_env)
        password = os.environ.get(args.basic_password_env)
        if user is None or password is None:
            raise ValueError("a basic-auth environment variable is unset")
        encoded = base64.b64encode(f"{user}:{password}".encode()).decode("ascii")
        headers["Authorization"] = "Basic " + encoded
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
    return headers


def require_secure_auth(root: str, args: argparse.Namespace) -> None:
    if urllib.parse.urlsplit(root).scheme.lower() == "https":
        return
    if args.bearer_env or args.basic_user_env or args.basic_password_env or args.header_env:
        raise ValueError("refusing to send environment-provided credentials or headers over plain HTTP")


def open_url(url: str, headers: dict[str, str], timeout: float) -> tuple[int, dict[str, str], bytes, str]:
    request = urllib.request.Request(url, headers=headers, method="GET")
    opener = urllib.request.build_opener(SameOriginRedirectHandler())
    try:
        with opener.open(request, timeout=timeout) as response:
            return response.status, dict(response.headers.items()), response.read(), response.geturl()
    except urllib.error.HTTPError as exc:
        body = exc.read(65536)
        detail = error_detail(body, exc.headers.get("Content-Type", "") if exc.headers else "")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"request failed: {exc.reason}") from exc


def error_detail(body: bytes, content_type: str) -> str:
    if "json" in content_type.lower():
        try:
            payload = json.loads(body)
            error = payload.get("error") if isinstance(payload, dict) else None
            if isinstance(error, dict):
                code = error.get("code")
                message = error.get("message")
                parts = [str(value) for value in (code, message) if value not in (None, "")]
                if parts:
                    return ": ".join(parts)[:2000]
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    text = body.decode("utf-8", errors="replace")
    return " ".join(text.split())[:2000] or "empty response body"


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def annotation_value(element: ET.Element) -> Any:
    for key in ("Bool", "String", "EnumMember", "Int", "Decimal"):
        if key in element.attrib:
            return element.attrib[key]
    children = list(element)
    if not children:
        text = (element.text or "").strip()
        return text if text else True
    if local_name(element.tag) == "Collection":
        return [annotation_value(child) for child in children]
    values: dict[str, Any] = {}
    for child in children:
        key = child.attrib.get("Property") or local_name(child.tag)
        values[key] = annotation_value(child)
    return values


def summarize_metadata(xml_bytes: bytes) -> dict[str, Any]:
    root = ET.fromstring(xml_bytes)
    summary: dict[str, Any] = {
        "schemas": [],
        "containers": [],
        "types": [],
        "operations": [],
        "annotations": [],
    }
    for schema in (node for node in root.iter() if local_name(node.tag) == "Schema"):
        namespace = schema.attrib.get("Namespace", "")
        summary["schemas"].append(namespace)
        for child in schema:
            kind = local_name(child.tag)
            if kind in {"EntityType", "ComplexType"}:
                item: dict[str, Any] = {
                    "kind": kind,
                    "name": f"{namespace}.{child.attrib.get('Name', '')}".strip("."),
                    "properties": [],
                    "navigationProperties": [],
                }
                for attribute in ("BaseType", "Abstract", "OpenType"):
                    if attribute in child.attrib:
                        item[attribute[0].lower() + attribute[1:]] = child.attrib[attribute]
                key_names = [
                    ref.attrib.get("Name")
                    for key in child
                    if local_name(key.tag) == "Key"
                    for ref in key
                    if local_name(ref.tag) == "PropertyRef"
                ]
                if key_names:
                    item["keys"] = key_names
                for member in child:
                    member_kind = local_name(member.tag)
                    if member_kind == "Property":
                        prop = {"name": member.attrib.get("Name"), "type": member.attrib.get("Type")}
                        if "Nullable" in member.attrib:
                            prop["nullable"] = member.attrib["Nullable"] != "false"
                        item["properties"].append(prop)
                    elif member_kind == "NavigationProperty":
                        item["navigationProperties"].append(
                            {"name": member.attrib.get("Name"), "type": member.attrib.get("Type")}
                        )
                summary["types"].append(item)
            elif kind == "EnumType":
                summary["types"].append(
                    {
                        "kind": kind,
                        "name": f"{namespace}.{child.attrib.get('Name', '')}".strip("."),
                        "underlyingType": child.attrib.get("UnderlyingType", "Edm.Int32"),
                        "isFlags": child.attrib.get("IsFlags", "false") == "true",
                        "members": [
                            {"name": member.attrib.get("Name"), "value": member.attrib.get("Value")}
                            for member in child
                            if local_name(member.tag) == "Member"
                        ],
                    }
                )
            elif kind == "TypeDefinition":
                summary["types"].append(
                    {
                        "kind": kind,
                        "name": f"{namespace}.{child.attrib.get('Name', '')}".strip("."),
                        "underlyingType": child.attrib.get("UnderlyingType"),
                    }
                )
            elif kind in {"Function", "Action"}:
                summary["operations"].append(
                    {
                        "kind": kind,
                        "name": f"{namespace}.{child.attrib.get('Name', '')}".strip("."),
                        "isBound": child.attrib.get("IsBound", "false") == "true",
                        "parameters": [
                            {"name": node.attrib.get("Name"), "type": node.attrib.get("Type")}
                            for node in child
                            if local_name(node.tag) == "Parameter"
                        ],
                        "returnType": next(
                            (
                                node.attrib.get("Type")
                                for node in child
                                if local_name(node.tag) == "ReturnType"
                            ),
                            None,
                        ),
                    }
                )
            elif kind == "EntityContainer":
                container: dict[str, Any] = {
                    "name": f"{namespace}.{child.attrib.get('Name', '')}".strip("."),
                    "resources": [],
                }
                for resource in child:
                    resource_kind = local_name(resource.tag)
                    if resource_kind not in {"EntitySet", "Singleton", "FunctionImport", "ActionImport"}:
                        continue
                    entry: dict[str, Any] = {
                        "kind": resource_kind,
                        "name": resource.attrib.get("Name"),
                        "type": resource.attrib.get("EntityType")
                        or resource.attrib.get("Type")
                        or resource.attrib.get("Function")
                        or resource.attrib.get("Action"),
                    }
                    capabilities = {}
                    for annotation in resource.iter():
                        if local_name(annotation.tag) != "Annotation":
                            continue
                        term = annotation.attrib.get("Term", "")
                        if "Capabilities.V1" in term:
                            capabilities[term] = annotation_value(annotation)
                    if capabilities:
                        entry["capabilities"] = capabilities
                    bindings = [
                        {"path": node.attrib.get("Path"), "target": node.attrib.get("Target")}
                        for node in resource
                        if local_name(node.tag) == "NavigationPropertyBinding"
                    ]
                    if bindings:
                        entry["navigationPropertyBindings"] = bindings
                    container["resources"].append(entry)
                summary["containers"].append(container)
            elif kind == "Annotations":
                target = child.attrib.get("Target")
                for annotation in child:
                    if local_name(annotation.tag) != "Annotation":
                        continue
                    summary["annotations"].append(
                        {
                            "target": target,
                            "term": annotation.attrib.get("Term"),
                            "qualifier": annotation.attrib.get("Qualifier"),
                            "value": annotation_value(annotation),
                        }
                    )
    return summary


def query_pairs(args: argparse.Namespace) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for name in ("select", "filter", "orderby", "top", "skip", "count", "expand", "search"):
        value = getattr(args, name)
        if value is not None:
            pairs.append(("$" + name, str(value).lower() if isinstance(value, bool) else str(value)))
    seen = {key for key, _ in pairs}
    for raw in args.query:
        if "=" not in raw:
            raise ValueError("--query must be NAME=VALUE")
        key, value = raw.split("=", 1)
        if not key:
            raise ValueError("--query name cannot be empty")
        if key in seen:
            raise ValueError(f"query option {key!r} was specified more than once")
        seen.add(key)
        pairs.append((key, value))
    return pairs


def write_output(value: Any, output: str | None) -> None:
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if output:
        with open(output, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    else:
        sys.stdout.write(text)


def command_metadata(args: argparse.Namespace) -> None:
    url = service_url(args.service_root, "$metadata")
    require_secure_auth(args.service_root, args)
    headers = headers_from_args(args)
    headers["Accept"] = "application/xml"
    _, _, body, _ = open_url(url, headers, args.timeout)
    if args.raw:
        if args.output:
            with open(args.output, "wb") as handle:
                handle.write(body)
        else:
            sys.stdout.buffer.write(body)
        return
    write_output(summarize_metadata(body), args.output)


def command_service(args: argparse.Namespace) -> None:
    url = args.service_root.rstrip("/") + "/"
    service_url(args.service_root, "")
    require_secure_auth(args.service_root, args)
    headers = headers_from_args(args)
    _, response_headers, body, _ = open_url(url, headers, args.timeout)
    write_output(decode_json(body, response_headers.get("Content-Type", "")), args.output)


def decode_json(body: bytes, content_type: str) -> Any:
    if "json" not in content_type.lower():
        preview = body[:200].decode("utf-8", errors="replace")
        raise RuntimeError(f"expected JSON but received {content_type or 'unknown content type'}: {preview}")
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON response: {exc}") from exc


def next_link(payload: Any) -> str | None:
    if not isinstance(payload, dict):
        return None
    return payload.get("@odata.nextLink") or payload.get("@nextLink")


def command_get(args: argparse.Namespace) -> None:
    base = service_url(args.service_root, args.resource)
    require_secure_auth(args.service_root, args)
    pairs = query_pairs(args)
    separator = "&" if urllib.parse.urlsplit(base).query else "?"
    url = base + (separator + urllib.parse.urlencode(pairs, safe="$(),'/:") if pairs else "")
    headers = headers_from_args(args)
    initial_origin = origin(url)
    pages = 0
    items: list[Any] = []
    first_payload: Any = None
    seen_urls: set[str] = set()
    truncated = False

    while True:
        if url in seen_urls:
            raise RuntimeError("the service returned a repeated next link")
        if origin(url) != initial_origin:
            raise RuntimeError("refusing a cross-origin next link while credentials may be attached")
        seen_urls.add(url)
        _, response_headers, body, final_url = open_url(url, headers, args.timeout)
        if origin(final_url) != initial_origin:
            raise RuntimeError("request redirected to a different origin")
        payload = decode_json(body, response_headers.get("Content-Type", ""))
        pages += 1
        if first_payload is None:
            first_payload = payload
        if not args.all_pages:
            write_output(payload, args.output)
            return
        if not isinstance(payload, dict) or not isinstance(payload.get("value"), list):
            raise RuntimeError("--all-pages requires a collection payload with a value array")
        remaining = args.max_items - len(items)
        page_items = payload["value"]
        items.extend(page_items[:remaining])
        link = next_link(payload)
        if len(page_items) > remaining:
            truncated = True
            break
        if not link:
            break
        if pages >= args.max_pages or len(items) >= args.max_items:
            truncated = True
            break
        url = urllib.parse.urljoin(final_url, link)

    result = dict(first_payload)
    result["value"] = items
    result.pop("@odata.nextLink", None)
    result.pop("@nextLink", None)
    result["_retrieval"] = {"pages": pages, "items": len(items), "truncated": truncated}
    write_output(result, args.output)


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--service-root", help="absolute OData v4 service root URL; overrides no profile")
    parser.add_argument("--profile", help="saved service profile; omit to use the configured default")
    parser.add_argument("--config", help="profile config path")
    parser.add_argument("--odata-version", choices=("4.0", "4.01"), default=None)
    parser.add_argument("--bearer-env", metavar="ENV_VAR", help="read a bearer token from this environment variable")
    parser.add_argument("--basic-user-env", metavar="ENV_VAR")
    parser.add_argument("--basic-password-env", metavar="ENV_VAR")
    parser.add_argument(
        "--header-env",
        action="append",
        default=[],
        metavar="NAME=ENV_VAR",
        help="add a header whose value is read from an environment variable; repeatable",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="per-request timeout in seconds")
    parser.add_argument("--output", help="write output to this file instead of stdout")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    metadata = subparsers.add_parser("metadata", help="fetch and summarize $metadata")
    add_common_options(metadata)
    metadata.add_argument("--raw", action="store_true", help="emit raw XML instead of a JSON summary")
    metadata.set_defaults(handler=command_metadata)

    service = subparsers.add_parser("service", help="fetch the JSON service document")
    add_common_options(service)
    service.set_defaults(handler=command_service)

    get = subparsers.add_parser("get", help="perform a JSON GET query")
    add_common_options(get)
    get.add_argument("--resource", required=True, help="resource path relative to the service root")
    get.add_argument("--select")
    get.add_argument("--filter")
    get.add_argument("--orderby")
    get.add_argument("--top", type=int)
    get.add_argument("--skip", type=int)
    get.add_argument("--count", action=argparse.BooleanOptionalAction, default=None)
    get.add_argument("--expand")
    get.add_argument("--search")
    get.add_argument("--query", action="append", default=[], metavar="NAME=VALUE", help="extra query option; repeatable")
    get.add_argument("--all-pages", action="store_true", help="follow top-level server next links")
    get.add_argument("--max-pages", type=int, default=100)
    get.add_argument("--max-items", type=int, default=10000)
    get.set_defaults(handler=command_get)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if getattr(args, "max_pages", 1) < 1 or getattr(args, "max_items", 1) < 1:
        parser.error("page and item limits must be positive")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    try:
        resolve_profile_args(args)
        args.handler(args)
    except (ValueError, RuntimeError, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
