"""HTTP client for the KaloData API: retries, envelope handling, error translation.

Never leaks raw upstream errors to stdout — everything is translated into
KaloError with an actionable suggestion.
"""

from __future__ import annotations

import json
import random
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

from .config import Config
from .errors import KaloError
from .onboarding import NO_KEY_MESSAGE, SETUP_LINES

_RETRIES = 3
_PARAM_HINTS = ("must be", "invalid", "required", "for input string", "parameter")

AUTH_HELP = SETUP_LINES


class _Retryable(Exception):
    pass


def _require_auth(cfg: Config) -> None:
    if not cfg.api_key:
        raise KaloError(NO_KEY_MESSAGE, kind="auth", help_lines=AUTH_HELP)


def _headers(cfg: Config, extra: dict | None) -> dict:
    h = {
        "Content-Type": "application/json;charset=UTF-8",
        "secret-key": cfg.api_key,
        "source-type": "SKILL",
    }
    if extra:
        h.update(extra)
    return h


def _translate_failure(code, message: str, empty_on_not_found: bool):
    msg = str(message or "")
    low = msg.lower()
    if empty_on_not_found and ("not found" in low or "未找到" in msg):
        return []  # definitive empty result
    code = str(code)
    if code == "2000" or "acquire connection timeout" in low:
        raise _Retryable(msg)
    if code == "2016":
        if any(k in low for k in _PARAM_HINTS):
            raise KaloError(
                f"upstream rejected a parameter: {msg}",
                kind="parameter",
                help_lines=["Adjust the offending flag and retry (see `--help` of this command)"],
            )
        raise KaloError(
            f"membership/quota limit: {msg}",
            kind="membership",
            help_lines=["Narrow --range, lower --limit/--page, or upgrade the account tier"],
        )
    raise KaloError(f"upstream error: {msg or 'unknown failure'}")


def _do_request(url: str, data: bytes | None, headers: dict, timeout: float, method: str = "POST"):
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as e:
        raise _Retryable(str(e)) from e


def request(
    cfg: Config,
    path: str,
    body: dict,
    *,
    extra_headers: dict | None = None,
    timeout: float = 30.0,
    empty_on_not_found: bool = False,
    method: str = "POST",
):
    """Call base_url+path (JSON body for POST, query params for GET); return the envelope's `data`."""
    _require_auth(cfg)
    url = cfg.base_url.rstrip("/") + path
    headers = _headers(cfg, extra_headers)
    if method == "GET":
        if body:
            url += "?" + urllib.parse.urlencode(body)
        payload = None
    else:
        payload = json.dumps(body).encode("utf-8")

    last = "unknown error"
    for attempt in range(_RETRIES):
        try:
            status, raw = _do_request(url, payload, headers, timeout, method)
            if status >= 500:
                raise _Retryable(f"HTTP {status}")
            try:
                envelope = json.loads(raw)
            except json.JSONDecodeError as e:
                raise _Retryable(f"malformed JSON from upstream: {e}") from e
            if not isinstance(envelope, dict):
                raise _Retryable("unexpected upstream payload shape")
            if envelope.get("success"):
                return envelope.get("data")
            if status in (401, 403):
                raise KaloError(
                    "authentication rejected by KaloData", kind="auth", help_lines=AUTH_HELP
                )
            return _translate_failure(
                envelope.get("code"), envelope.get("message"), empty_on_not_found
            )
        except _Retryable as e:
            last = str(e)
            if attempt < _RETRIES - 1:
                time.sleep(0.3 * (attempt + 1) + random.uniform(0, 0.2))
    raise KaloError(
        f"KaloData unreachable after {_RETRIES} attempts ({last})",
        kind="network",
        help_lines=["Retry shortly; check network access to kalodata.com"],
    )


def as_list(data) -> list:
    """Rank payloads are either a list or {'data': [...]} — accept both."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("data"), list):
        return data["data"]
    if data is None:
        return []
    return [data] if isinstance(data, dict) else []
