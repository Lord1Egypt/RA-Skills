#!/usr/bin/env python3
"""Shared helpers for n8n-master toolbox scripts."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Mapping


SENSITIVE_KEY_PARTS = (
    "authorization",
    "cookie",
    "token",
    "secret",
    "password",
    "passwd",
    "api_key",
    "apikey",
    "x-api-key",
)


class ToolboxError(RuntimeError):
    """Expected user-facing toolbox error."""


def die(message: str, code: int = 2) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def is_sensitive_key(key: Any) -> bool:
    text = str(key).lower().replace("-", "_")
    return text == "key" or any(part in text for part in SENSITIVE_KEY_PARTS)


def redact(value: Any, key_hint: str | None = None) -> Any:
    if key_hint and is_sensitive_key(key_hint):
        return "<redacted>"
    if isinstance(value, Mapping):
        return {str(k): redact(v, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(item, key_hint) for item in value]
    if isinstance(value, tuple):
        return [redact(item, key_hint) for item in value]
    if isinstance(value, str):
        text = re.sub(
            r"(?i)\b(bearer|basic)\s+[A-Za-z0-9._~+/=-]+",
            r"\1 <redacted>",
            value,
        )
        text = re.sub(
            r"(?i)(api[_-]?key|token|secret|password)=([^&\s]+)",
            r"\1=<redacted>",
            text,
        )
        return text
    return value


def load_text_arg(value: str, label: str) -> str:
    if value.startswith("@"):
        path = value[1:]
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return handle.read()
        except OSError as exc:
            raise ToolboxError(f"failed to read {label} file {path!r}: {exc}") from exc
    return value


def load_json_arg(value: str | None, label: str, default: Any = None) -> Any:
    if value is None:
        return default
    raw = load_text_arg(value, label)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ToolboxError(f"{label} must be valid JSON: {exc}") from exc


def read_json_file(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except OSError as exc:
        raise ToolboxError(f"failed to read JSON file {path!r}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ToolboxError(f"invalid JSON file {path!r}: {exc}") from exc


def write_text(path: str | None, text: str) -> None:
    if path:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
    else:
        print(text)


def json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)


def merge_query(url: str, query: Mapping[str, Any] | None) -> str:
    if not query:
        return url
    parsed = urllib.parse.urlsplit(url)
    existing = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    extra: list[tuple[str, str]] = []
    for key, value in query.items():
        if value is None:
            continue
        if isinstance(value, list):
            extra.extend((str(key), str(item)) for item in value)
        else:
            extra.append((str(key), str(value)))
    new_query = urllib.parse.urlencode(existing + extra, doseq=True)
    return urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, new_query, parsed.fragment)
    )


def request_json(
    method: str,
    url: str,
    headers: Mapping[str, str] | None = None,
    payload: Any = None,
    timeout: float = 30.0,
) -> Any:
    body: bytes | None = None
    req_headers = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(
        url,
        data=body,
        headers=req_headers,
        method=method.upper(),
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise ToolboxError(
            f"HTTP {exc.code} from {redact(url)}: {json_dumps(redact(parse_json_maybe(raw)))}"
        ) from exc
    except urllib.error.URLError as exc:
        raise ToolboxError(f"request failed for {redact(url)}: {exc.reason}") from exc

    data = parse_json_maybe(raw)
    if not isinstance(data, (dict, list)):
        raise ToolboxError(f"expected JSON response from {url}, got text: {raw[:500]}")
    return data


def parse_json_maybe(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ToolboxError(f"missing required environment variable {name}")
    return value
