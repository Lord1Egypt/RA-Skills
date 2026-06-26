"""Shared IBKR client factory.

Connects to IB Gateway running locally (typically inside a Docker container
managed by gnzsnz/ib-gateway-docker). The gateway authenticates against IBKR
using your username/password + 2FA mobile push.

Mode selection:
  IBKR_LIVE_MODE=0  (default) → paper trading, port 4002
  IBKR_LIVE_MODE=1            → live trading, port 4001

Override the host/port if your Gateway runs elsewhere:
  IBKR_HOST=127.0.0.1
  IBKR_PORT=<override>

The client is configured `readonly=True` by default. Trade-placing scripts
(ibkr_execute_trade.py) explicitly opt in to a non-readonly session.
"""
from __future__ import annotations

import os
import sys

# Default ports for gnzsnz/ib-gateway-docker:
#   live  → 4001 (TWS port 7496 mapped)
#   paper → 4002 (TWS port 7497 mapped)
DEFAULT_LIVE_PORT = 4001
DEFAULT_PAPER_PORT = 4002


def is_live() -> bool:
    return os.environ.get("IBKR_LIVE_MODE", "0") in ("1", "true", "True")


def _host() -> str:
    return os.environ.get("IBKR_HOST", "127.0.0.1")


def _port() -> int:
    custom = os.environ.get("IBKR_PORT")
    if custom:
        try:
            return int(custom)
        except ValueError:
            pass
    return DEFAULT_LIVE_PORT if is_live() else DEFAULT_PAPER_PORT


def _client_id() -> int:
    """A non-1 client id keeps us from conflicting with TWS-attached sessions
    that often default to 0 or 1. Override with IBKR_CLIENT_ID."""
    raw = os.environ.get("IBKR_CLIENT_ID", "97")
    try:
        return int(raw)
    except ValueError:
        return 97


def env_summary() -> str:
    return f"IBKR env: {'LIVE' if is_live() else 'PAPER'} ({_host()}:{_port()})"


def connect(readonly: bool = True, timeout: float = 12.0):
    """Connect to IB Gateway. Returns an IB instance ready for queries.

    Caller MUST disconnect via `ib.disconnect()` (use try/finally or
    `with` if you want to be cute, but ib_async's IB doesn't implement
    the context-manager protocol).
    """
    try:
        from ib_async import IB
    except ImportError:
        sys.stderr.write(
            "Missing dependency: ib_async. Install with:\n"
            "  pip install -r skills/aeon/ibkr-investing/requirements.txt\n"
        )
        sys.exit(2)

    ib = IB()
    try:
        ib.connect(_host(), _port(), clientId=_client_id(), readonly=readonly, timeout=timeout)
    except Exception as e:
        sys.stderr.write(
            f"Failed to connect to IB Gateway at {_host()}:{_port()}: {e}\n"
            f"Is the Gateway running? Check with: docker ps | grep ib-gateway\n"
        )
        sys.exit(1)
    return ib


def smart_stock(symbol: str, exchange: str | None = None, currency: str | None = None):
    """Build a Stock contract with sensible defaults (US ETF on SMART/USD)."""
    from ib_async import Stock

    return Stock(
        symbol,
        exchange or os.environ.get("IBKR_DEFAULT_EXCHANGE", "SMART"),
        currency or os.environ.get("IBKR_DEFAULT_CURRENCY", "USD"),
    )
