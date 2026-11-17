"""Unified credential / HTTP-config loading for huawei-cloud-voucher-send.

The KooCLI (`hcloud`) execution path never needs AK/SK here — authentication is
delegated entirely to the active hcloud profile. This module exists for the
*huaweicloudsdkbss* SDK fallback path: it centralises how the AK/SK and the
global BSS endpoint are resolved so the rest of the skill never handles
credentials directly.

Design rules:
- No credential is ever read from chat, a literal, or a file written by the
  skill; only the standard Huawei Cloud environment variables are consulted.
- The SDK (`huaweicloudsdkcore` / `huaweicloudsdkbss`) is imported lazily so
  this module stays importable (and unit-testable) in an offline environment
  where the SDK is not installed.
"""

import os

# BSS is a global (domain-level) service: the documented global endpoint.
BSS_ENDPOINT = "https://bss.myhuaweicloud.com"
DEFAULT_REGION = "cn-north-1"

# Environment-variable prefixes used by the Huawei Cloud SDK / docs.
_CREDENTIAL_PREFIXES = ("HUAWEI", "HW_", "HWC")
_AK_MARKERS = ("ACCESS_KEY", "_AK")
_SK_MARKERS = ("SECRET_KEY", "_SK")


def _env_value(markers):
    """Return the first non-empty env value whose *name* matches a marker.

    Only variables prefixed with HUAWEI / HW_ / HWC are considered, so arbitrary
    environment entries can never be mistaken for credentials.
    """
    for key, value in os.environ.items():
        upper = key.upper()
        if not upper.startswith(_CREDENTIAL_PREFIXES):
            continue
        if any(marker in upper for marker in markers) and value:
            return value
    return None


def load_ak_sk():
    """Resolve AK/SK from the standard Huawei Cloud environment variables.

    Returns ``(ak, sk)`` or ``(None, None)`` when either is absent. Callers turn
    the ``(None, None)`` result into a ConfigError with a user-facing hint; this
    function itself never prints or logs the secret values.
    """
    return _env_value(_AK_MARKERS), _env_value(_SK_MARKERS)


def resolve_region(region=None):
    """Resolve the region, falling back to the BSS default (cn-north-1)."""
    if region:
        return region
    for name in ("HUAWEI_REGION", "HW_REGION_NAME", "HWC_REGION"):
        value = os.environ.get(name)
        if value:
            return value
    return DEFAULT_REGION


def build_http_config():
    """Build an SDK HttpConfig (proxy-aware) for the fallback path.

    Imports the SDK lazily so importing this module does not require
    huaweicloudsdkcore to be installed.
    """
    from huaweicloudsdkcore.http.http_config import HttpConfig

    http_config = HttpConfig.get_default_config()
    http_config.timeout = (30, 60)
    http_config.retry_times = 3
    proxy_url = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or ""
    if proxy_url:
        from urllib.parse import urlparse

        parsed = urlparse(proxy_url)
        http_config.proxy_protocol = parsed.scheme or "http"
        http_config.proxy_host = parsed.hostname or ""
        http_config.proxy_port = parsed.port or 8080
        http_config.proxy_user = parsed.username or ""
        http_config.proxy_password = parsed.password or ""
    return http_config