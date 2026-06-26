"""
remote_client.py — L3 HTTP client

Responsibilities:
- Communicate with L2 API (Manifest, download, remote execution)
- Unified timeout and error handling
- Auto-follow 302 redirects (urllib default behavior)
"""

import json
import os
import urllib.error
import urllib.request
from typing import Optional

from lib.schemas import CURRENT_VERSION, NetworkError, get_client_timezone

DEFAULT_SERVICE_URL = os.getenv("AINEWS_SERVICE_URL", "https://api.ainewparadigm.cn")
DEFAULT_TIMEOUT = 30  # Downloads may take longer


def _build_headers(
    api_key: Optional[str] = None,
    include_engagement: bool = True,
    include_timezone: bool = False,
) -> dict:
    headers = {
        "X-Client": "ai-daily-news-l3",
        "X-Client-Version": CURRENT_VERSION,
        "Accept": "application/json",
    }
    if include_engagement:
        try:
            from lib.engagement_state import get_client_capabilities, get_or_create_install_id

            headers["X-Client-Install-Id"] = get_or_create_install_id()
            headers["X-Client-Capabilities"] = get_client_capabilities()
        except Exception:
            # Engagement headers are best-effort. Never block core news requests.
            pass
    if include_timezone:
        try:
            headers["X-Client-Timezone"] = get_client_timezone()
        except Exception:
            pass
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def _read_json_response(resp) -> dict:
    return json.loads(resp.read().decode("utf-8"))


def fetch_manifest(
    base_url: Optional[str] = None,
    timeout: int = 10,
) -> dict:
    """Fetch Manifest"""
    url = f"{base_url or DEFAULT_SERVICE_URL}/v1/manifest"
    try:
        req = urllib.request.Request(url, headers=_build_headers())
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return _read_json_response(resp)
    except urllib.error.HTTPError as e:
        raise NetworkError(f"Manifest HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Manifest error: {e}")


def download_dataset(
    date: str,
    tier: str = "guest",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> bytes:
    """
    Download dataset file.

    Returns gzip-compressed byte data.
    Auto-follow L2's 302 redirects to CDN.
    """
    url = (
        f"{base_url or DEFAULT_SERVICE_URL}/v1/data/download"
        f"?product_name=news_dataset&schema_version=v1"
        f"&date={date}&tier={tier}"
    )

    headers = _build_headers(api_key)
    try:
        req = urllib.request.Request(url, headers=headers)
        # urllib.request.urlopen defaults allow_redirects=True
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise NetworkError(f"Dataset not found for date={date}, tier={tier}")
        raise NetworkError(f"Download HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Download error: {e}")


def download_pro_dataset(
    date: str,
    tier: str = "pro_core",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> bytes:
    """Download paid dataset (requires Token)"""
    url = (
        f"{base_url or DEFAULT_SERVICE_URL}/v1/data/download/pro"
        f"?product_name=news_dataset&schema_version=v1"
        f"&date={date}&tier={tier}"
    )

    headers = _build_headers(api_key)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise NetworkError("Invalid or missing access token")
        if e.code == 403:
            raise NetworkError(f"Tier {tier} not included in your subscription")
        if e.code == 404:
            raise NetworkError(f"Dataset not found for date={date}, tier={tier}")
        raise NetworkError(f"Pro download HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Pro download error: {e}")


def invoke_capability(
    capability_name: str,
    params: dict,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 60,
) -> dict:
    """Invoke remote capability"""
    url = f"{base_url or DEFAULT_SERVICE_URL}/v1/execute"
    payload = json.dumps({"capability_name": capability_name, "params": params}).encode("utf-8")

    headers = _build_headers(api_key)
    headers["Content-Type"] = "application/json"

    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return _read_json_response(resp)
    except urllib.error.HTTPError as e:
        raise NetworkError(f"Execute HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Execute error: {e}")


def resolve_latest(
    tier: str = "guest",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """
    Resolve the latest available date and get freshness metadata only.

    Returns metadata without actual data. Then call download_dataset with
    the resolved_date to get the actual data.

    DEPRECATED: Use resolve_latest_enhanced instead for local time support.
    """
    if tier == "guest":
        url = (
            f"{base_url or DEFAULT_SERVICE_URL}/v1/data/resolve-latest"
            f"?product_name=news_dataset&schema_version=v1&tier={tier}"
        )
    else:
        url = (
            f"{base_url or DEFAULT_SERVICE_URL}/v1/data/resolve-latest/pro"
            f"?product_name=news_dataset&schema_version=v1&tier={tier}"
        )

    headers = _build_headers(api_key)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return _read_json_response(resp)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise NetworkError("Invalid or missing access token")
        if e.code == 403:
            raise NetworkError(f"Tier {tier} not included in your subscription")
        if e.code == 404:
            raise NetworkError("No available dataset found")
        raise NetworkError(f"Resolve latest HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Resolve latest error: {e}")


def resolve_latest_enhanced(
    tier: str = "guest",
    client_timezone: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """
    Resolve the latest available date with optional local time enhancement.

    Returns metadata without actual data. Then call download_dataset with
    the resolved_source_date to get the actual data.
    """
    if tier == "guest":
        url = (
            f"{base_url or DEFAULT_SERVICE_URL}/v1/data/resolve-latest"
            f"?product_name=news_dataset&schema_version=v1&tier={tier}"
        )
        if client_timezone:
            url += f"&client_timezone={client_timezone}"
    else:
        url = (
            f"{base_url or DEFAULT_SERVICE_URL}/v1/data/resolve-latest/pro"
            f"?product_name=news_dataset&schema_version=v1&tier={tier}"
        )
        if client_timezone:
            url += f"&client_timezone={client_timezone}"

    headers = _build_headers(api_key)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return _read_json_response(resp)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise NetworkError("Invalid or missing access token")
        if e.code == 403:
            raise NetworkError(f"Tier {tier} not included in your subscription")
        if e.code == 404:
            raise NetworkError("No available dataset found")
        raise NetworkError(f"Resolve latest HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Resolve latest error: {e}")


def resolve_date(
    local_date: str,
    client_timezone: str,
    tier: str = "guest",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """
    Resolve a user's local date to the appropriate canonical dataset.

    Returns metadata about the matching dataset. Then call download_dataset with
    the resolved_source_date to get the actual data.
    """
    if tier == "guest":
        url = (
            f"{base_url or DEFAULT_SERVICE_URL}/v1/data/resolve-date"
            f"?product_name=news_dataset&schema_version=v1"
            f"&local_date={local_date}&client_timezone={client_timezone}&tier={tier}"
        )
    else:
        url = (
            f"{base_url or DEFAULT_SERVICE_URL}/v1/data/resolve-date/pro"
            f"?product_name=news_dataset&schema_version=v1"
            f"&local_date={local_date}&client_timezone={client_timezone}&tier={tier}"
        )

    headers = _build_headers(api_key)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return _read_json_response(resp)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise NetworkError("Invalid or missing access token")
        if e.code == 403:
            raise NetworkError(f"Tier {tier} not included in your subscription")
        if e.code == 404:
            raise NetworkError("No matching dataset found for the requested local date")
        raise NetworkError(f"Resolve date HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Resolve date error: {e}")


def submit_engagement(
    payload: dict,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 20,
) -> dict:
    """Submit user feedback or a survey response to L2."""
    url = f"{base_url or DEFAULT_SERVICE_URL}/v1/engagement/submit"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = _build_headers(api_key, include_engagement=True, include_timezone=True)
    headers["Content-Type"] = "application/json"

    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return _read_json_response(resp)
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8")
        except Exception:
            detail = ""
        if e.code in (400, 422):
            raise NetworkError(f"Engagement submit validation error: {detail or e.code}")
        if e.code in (401, 403):
            raise NetworkError(f"Engagement submit authorization error: {e.code}")
        if e.code == 404:
            raise NetworkError("Engagement submit endpoint not found")
        raise NetworkError(f"Engagement submit HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Engagement submit error: {e}")
