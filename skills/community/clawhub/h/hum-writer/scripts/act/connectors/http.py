"""Shared HTTP helper for platform connectors.

Provides a single ``http_request`` function that wraps ``urllib`` and is used
by all connectors in this package.  It returns parsed JSON for JSON responses
and raw bytes for everything else.

Error safety:
- Raw response bodies in error messages are truncated to 200 chars max.
- Authorization header *values* are never included in exception text.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Callable


def http_request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    body: bytes | None = None,
    exc_factory: Callable[[str], Exception] = RuntimeError,
) -> tuple[int, dict[str, Any] | bytes, dict[str, str]]:
    """Make an HTTP request and return ``(status, body, response_headers)``.

    - If ``payload`` is provided it is JSON-serialised and sent as the request
      body.  ``body`` (raw bytes) takes precedence if both are supplied.
    - When the response Content-Type includes ``application/json`` the body is
      parsed and returned as a ``dict``.  Otherwise raw ``bytes`` are returned.
    - On HTTP / URL errors a sanitised exception is raised via ``exc_factory``
      (defaults to ``RuntimeError``).  Response bodies are truncated to 200
      chars and Authorization header values are never included in the message.
    """
    req_headers: dict[str, str] = dict(headers or {})
    req_body: bytes | None = body

    if req_body is None and payload is not None:
        req_body = json.dumps(payload).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")

    req = urllib.request.Request(url, data=req_body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw_bytes: bytes = resp.read()
            content_type: str = resp.headers.get("Content-Type", "")
            resp_headers: dict[str, str] = dict(resp.headers.items())
            if "application/json" in content_type:
                raw_str = raw_bytes.decode("utf-8")
                data: dict[str, Any] = json.loads(raw_str) if raw_str else {}
                return resp.status, data, resp_headers
            return resp.status, raw_bytes, resp_headers
    except urllib.error.HTTPError as err:
        raw = err.read().decode("utf-8", errors="replace")
        truncated = raw[:200] + ("…" if len(raw) > 200 else "")
        try:
            err_data = json.loads(raw) if raw else {}
            err_body = json.dumps(err_data)[:200] + ("…" if len(json.dumps(err_data)) > 200 else "")
        except json.JSONDecodeError:
            err_body = truncated
        raise exc_factory(f"{method} {url} → {err.code}: {err_body}") from err
    except urllib.error.URLError as err:
        raise exc_factory(f"{method} {url} → {err.reason}") from err
