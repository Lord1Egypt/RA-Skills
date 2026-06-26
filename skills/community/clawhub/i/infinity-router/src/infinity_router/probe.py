"""
probe.py — HTTP health-check and latency measurement for OpenRouter models.

Public API
----------
health_check(api_key, model_id, timeout=15) -> tuple[bool, str | None]
    Returns (ok, error_code).  error_code is None on success.

bench_model(api_key, model_id) -> tuple[bool, int, str | None]
    Returns (ok, latency_ms, error_code).
"""

import time
from typing import Optional

import requests


CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"

_HEADERS_BASE = {
    "Content-Type": "application/json",
    "X-Title": "infinity-router/probe",
}

_PAYLOAD = {
    "messages": [{"role": "user", "content": "ping"}],
    "max_tokens": 1,
}


def health_check(
    api_key: str,
    model_id: str,
    timeout: int = 15,
) -> tuple[bool, Optional[str]]:
    """
    Send a minimal request to verify a model is reachable.

    Returns
    -------
    (True, None)            model responded OK
    (False, "rate_limit")   HTTP 429
    (False, "unavailable")  HTTP 503
    (False, "http_NNN")     other HTTP error
    (False, "timeout")      request timed out
    (False, "conn_error")   network-level failure
    """
    headers = {**_HEADERS_BASE, "Authorization": f"Bearer {api_key}"}
    payload = {**_PAYLOAD, "model": model_id}

    try:
        r = requests.post(CHAT_URL, headers=headers, json=payload, timeout=timeout)
        if r.status_code == 200:
            return True, None
        if r.status_code == 429:
            return False, "rate_limit"
        if r.status_code == 503:
            return False, "unavailable"
        return False, f"http_{r.status_code}"
    except requests.Timeout:
        return False, "timeout"
    except requests.RequestException:
        return False, "conn_error"


def bench_model(
    api_key: str,
    model_id: str,
    timeout: int = 20,
) -> tuple[bool, int, Optional[str]]:
    """
    health_check with round-trip latency measurement.

    Returns
    -------
    (ok, latency_ms, error_code)
    """
    t0 = time.monotonic()
    ok, err = health_check(api_key, model_id, timeout=timeout)
    ms = int((time.monotonic() - t0) * 1000)
    return ok, ms, err


def validate_models(
    api_key: str,
    model_ids: list[str],
    timeout: int = 10,
    verbose: bool = False,
) -> list[str]:
    """
    Filter model_ids to only those that respond successfully.
    Probes each in sequence; returns the IDs that pass.
    """
    valid = []
    for mid in model_ids:
        if verbose:
            label = mid[:60]
            print(f"    probing {label:<60}", end="", flush=True)
        ok, err = health_check(api_key, mid, timeout=timeout)
        if ok:
            valid.append(mid)
            if verbose:
                print("  ✓")
        else:
            if verbose:
                print(f"  ✗  {err}")
    return valid
