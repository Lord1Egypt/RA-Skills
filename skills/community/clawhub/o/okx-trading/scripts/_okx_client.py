"""Shared OKX client factory. Reads env vars and returns python-okx API objects.

OKX_DEMO_MODE=1 (default) routes to OKX's demo trading environment via flag='1'.
Set OKX_DEMO_MODE=0 only when you have intentionally decided to trade real money.

Imports `requests` / `httpx` at module load and monkey-patches a default HTTP
timeout (15s, override with `OKX_HTTP_TIMEOUT_S`). python-okx itself doesn't
set a default request timeout — without this patch, when OKX rate-limits or
silently drops a TCP connection, the script hangs until the agent's exec wall
(typically 120s) kills it. The patch makes hangs fail fast with a clean
`ReadTimeout`/`ConnectTimeout` the agent can surface and retry.
"""
from __future__ import annotations

import os
import sys

# ── Default HTTP timeout for python-okx ───────────────────────────────────
_HTTP_TIMEOUT_S = float(os.environ.get("OKX_HTTP_TIMEOUT_S", "15"))

try:
    import requests  # python-okx uses this; patch its Session.request
    _orig_requests_request = requests.Session.request

    def _requests_with_timeout(self, method, url, **kwargs):
        kwargs.setdefault("timeout", _HTTP_TIMEOUT_S)
        return _orig_requests_request(self, method, url, **kwargs)

    requests.Session.request = _requests_with_timeout
except ImportError:
    pass

try:
    # python-okx in newer versions uses httpx under the hood (older versions
    # use requests). Patch the Client constructors so any Client built after
    # this module loads gets a sane default timeout. We do NOT patch
    # Client.send() — httpx puts timeout on the Client/Request, not on send,
    # so passing it through send() raises `TypeError: Client.send() got an
    # unexpected keyword argument 'timeout'` (this was the v0.3.2 bug).
    import httpx
    _orig_httpx_client_init = httpx.Client.__init__
    _orig_httpx_async_init = httpx.AsyncClient.__init__

    def _httpx_client_init_with_timeout(self, *args, **kwargs):
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = _HTTP_TIMEOUT_S
        _orig_httpx_client_init(self, *args, **kwargs)

    def _httpx_async_init_with_timeout(self, *args, **kwargs):
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = _HTTP_TIMEOUT_S
        _orig_httpx_async_init(self, *args, **kwargs)

    httpx.Client.__init__ = _httpx_client_init_with_timeout
    httpx.AsyncClient.__init__ = _httpx_async_init_with_timeout
except ImportError:
    pass


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.stderr.write(f"Missing required environment variable: {name}\n")
        sys.exit(2)
    return value


def is_demo() -> bool:
    return os.environ.get("OKX_DEMO_MODE", "1") not in ("0", "false", "False", "")


def _flag() -> str:
    return "1" if is_demo() else "0"


def _creds() -> tuple[str, str, str, str]:
    api_key = _require_env("OKX_API_KEY")
    secret_key = _require_env("OKX_API_SECRET")
    passphrase = _require_env("OKX_API_PASSPHRASE")
    return api_key, secret_key, passphrase, _flag()


def account_api():
    from okx.Account import AccountAPI

    api_key, secret_key, passphrase, flag = _creds()
    return AccountAPI(api_key, secret_key, passphrase, False, flag)


def trade_api():
    from okx.Trade import TradeAPI

    api_key, secret_key, passphrase, flag = _creds()
    return TradeAPI(api_key, secret_key, passphrase, False, flag)


def market_api():
    """Public market data — auth not strictly required, but keys are accepted."""
    from okx.MarketData import MarketAPI

    api_key, secret_key, passphrase, flag = _creds()
    return MarketAPI(api_key, secret_key, passphrase, False, flag)


def public_api():
    from okx.PublicData import PublicAPI

    api_key, secret_key, passphrase, flag = _creds()
    return PublicAPI(api_key, secret_key, passphrase, False, flag)


def inst_type_for(inst_id: str) -> str:
    """Derive OKX instType from an instId string.

    BTC-USDT          -> SPOT
    BTC-USDT-SWAP     -> SWAP
    BTC-USDT-251227   -> FUTURES (date-suffixed)
    BTC-USD-251227-90000-C -> OPTION
    """
    parts = inst_id.split("-")
    if len(parts) == 2:
        return "SPOT"
    if len(parts) == 3 and parts[2] == "SWAP":
        return "SWAP"
    if len(parts) == 3 and parts[2].isdigit():
        return "FUTURES"
    if len(parts) == 5 and parts[-1] in ("C", "P"):
        return "OPTION"
    raise ValueError(f"Unrecognised instId format: {inst_id}")


def env_summary() -> str:
    return f"OKX env: {'DEMO' if is_demo() else 'LIVE'} (flag={_flag()})"
