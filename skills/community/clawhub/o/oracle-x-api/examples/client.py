#!/usr/bin/env python3
"""The client the other examples import.

Everything an Oracle-X call needs that is not the path itself lives here: the
base URL, the optional token, and the three failure modes worth distinguishing
(no instance, unresolved symbol, missing credential). Keeping them in one place
means the callers below read as a list of questions rather than a pile of
error handling.

Run it directly for a connectivity check:

    python client.py
"""

from __future__ import annotations

import os
from typing import Any

import httpx

BASE_URL = os.environ.get("ORACLE_X_URL", "http://localhost:8000").rstrip("/")
TOKEN = os.environ.get("ORACLE_X_TOKEN")

# Market calls are cached server-side and answer fast; LLM-backed ones do not.
DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=5.0)


class OracleXError(RuntimeError):
    """Raised when the instance cannot answer — never when it answers 'no'."""


class NotFound(OracleXError):
    """The symbol or resource could not be resolved.

    Distinct from a transport failure on purpose: Oracle-X refuses to emit a
    placeholder price or a placeholder technical payload, so a 404 here is a
    real answer — "this instance has no data for that" — and should be
    reported as such rather than retried or filled in from elsewhere.
    """


def _headers(authenticated: bool) -> dict[str, str]:
    if not authenticated:
        return {}
    if not TOKEN:
        raise OracleXError(
            "This endpoint needs a signed-in user. Set ORACLE_X_TOKEN to a "
            "Supabase access token (see references/auth.md)."
        )
    return {"Authorization": f"Bearer {TOKEN}"}


def get(
    path: str,
    params: dict[str, Any] | None = None,
    *,
    authenticated: bool = False,
    client: httpx.Client | None = None,
) -> Any:
    """GET one endpoint and return the decoded JSON."""
    owned = client is None
    client = client or httpx.Client(base_url=BASE_URL, timeout=DEFAULT_TIMEOUT)
    try:
        response = client.get(path, params=params, headers=_headers(authenticated))
    except httpx.ConnectError as exc:
        raise OracleXError(
            f"No Oracle-X instance answering at {BASE_URL}. Start the terminal "
            "or set ORACLE_X_URL."
        ) from exc
    finally:
        if owned:
            client.close()
    return _decode(response, path)


def post(
    path: str,
    body: dict[str, Any] | None = None,
    *,
    authenticated: bool = False,
    client: httpx.Client | None = None,
) -> Any:
    """POST one endpoint and return the decoded JSON."""
    owned = client is None
    client = client or httpx.Client(base_url=BASE_URL, timeout=DEFAULT_TIMEOUT)
    try:
        response = client.post(path, json=body, headers=_headers(authenticated))
    except httpx.ConnectError as exc:
        raise OracleXError(f"No Oracle-X instance answering at {BASE_URL}.") from exc
    finally:
        if owned:
            client.close()
    return _decode(response, path)


def _decode(response: httpx.Response, path: str) -> Any:
    if response.status_code == 404:
        raise NotFound(f"{path}: the instance has no data for that request")
    if response.status_code == 401:
        raise OracleXError(f"{path}: ORACLE_X_TOKEN is missing or expired")
    if response.status_code == 503:
        raise OracleXError(f"{path}: no provider is currently serving this endpoint")
    if response.status_code == 422:
        # FastAPI's validation error. Almost always a required query parameter
        # the caller did not know about — check references/endpoints.md for the
        # route rather than retrying the same call.
        raise OracleXError(f"{path}: rejected the parameters — {response.text[:200]}")
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        # Everything reaches the caller as an OracleXError so that a partial
        # failure inside a concurrent fan-out can be recorded as one, rather
        # than tearing down the whole batch with a transport-library traceback.
        raise OracleXError(f"{path}: HTTP {response.status_code}") from exc
    return response.json()


def health() -> dict[str, Any]:
    """Per-category health of the instance's upstreams.

    Passive on the server side — it reports what the last real call to each
    provider did and issues none of its own — so it is safe to call first every
    time, and a degraded category here explains an empty payload later.
    """
    return get("/api/system/health")


if __name__ == "__main__":
    print(f"instance: {BASE_URL}")
    print(f"token:    {'set' if TOKEN else 'not set (public endpoints only)'}")
    try:
        report = health()
    except OracleXError as exc:
        raise SystemExit(f"unreachable: {exc}") from exc

    print(f"status:   {report.get('status', '?')}")
    for category in report.get("categories", []):
        label = category.get("label", category.get("key", "?"))
        state = category.get("state", "?")
        # `idle` is not a fault: the category simply has not been called since
        # the process started. Reporting it as a failure would send a caller
        # chasing an outage that is really a cold cache.
        critical = " (critical)" if category.get("critical") else ""
        detail = f" — {category['detail']}" if category.get("detail") else ""
        print(f"  {label:<20} {state}{critical}{detail}")
