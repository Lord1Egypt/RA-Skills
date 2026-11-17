"""Unified credential / HTTP-config loading for huawei-cloud-voucher-claim.

The KooCLI (`hcloud`) execution path never needs AK/SK here — authentication is
delegated entirely to the active hcloud profile. This module exists for the
*huaweicloudsdkbss* SDK fallback path: it centralises how the AK/SK and the
global BSS endpoint are resolved so the rest of the skill never handles
credentials directly.

Design rules:
- Credentials are read only from a fixed, explicit allow-list of environment
  variable *names*: each name is looked up **verbatim** (`os.environ.get(<exact
  name>)`). The process environment is never enumerated, copied or matched by
  prefix/substring, so an unrelated environment entry can never be picked up as
  a secret.
- No credential is ever read from chat, a literal, or a file written by the
  skill.
- The SDK (`huaweicloudsdkcore` / `huaweicloudsdkbss`) is imported lazily so
  this module stays importable (and unit-testable) in an offline environment
  where the SDK is not installed.
"""

import os

# BSS is a global (domain-level) service: the documented global endpoint.
BSS_ENDPOINT = "https://bss.myhuaweicloud.com"
DEFAULT_REGION = "cn-north-1"

# Exact, documented environment-variable names for the SDK fallback credential
# source. Only these complete names are ever looked up, one by one, verbatim.
_AK_ENV_VAR_NAMES = ("HUAWEICLOUD_SDK_AK",)
_SK_ENV_VAR_NAMES = ("HUAWEICLOUD_SDK_SK",)


def _first_env_value(names):
    """Return the value of the first present, non-empty variable in *names*.

    *names* is a fixed allow-list of **exact** variable names. Each name is
    looked up by its complete name via ``os.environ.get(name)``; the environment
    is never iterated and no prefix/substring matching is done, so only the
    documented variables can ever be read.
    """
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def load_ak_sk():
    """Resolve AK/SK from the documented Huawei Cloud environment variables.

    Returns ``(ak, sk)`` or ``(None, None)`` when either is absent. Callers turn
    the ``(None, None)`` result into a ConfigError with a user-facing hint; this
    function itself never prints or logs the secret values.
    """
    return _first_env_value(_AK_ENV_VAR_NAMES), _first_env_value(_SK_ENV_VAR_NAMES)


def resolve_region(region=None):
    """Resolve the region, falling back to the BSS default (cn-north-1)."""
    if region:
        return region
    value = _first_env_value(("HUAWEI_REGION", "HW_REGION_NAME", "HWC_REGION"))
    return value or DEFAULT_REGION


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