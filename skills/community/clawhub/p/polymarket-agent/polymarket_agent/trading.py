"""Order execution — always behind the guard-rails.

AUDIT FIX (Medium — "Missing User Warnings", 93%): v1.0.2 sent real market
orders with no dry-run, no limits and no record. Here NO order goes out without
passing through `guardrails.evaluate_order`, and every attempt becomes a
journal line before it is sent.

BUG FIX: `positions` and `orders` were stubs ("Coming soon") — but SKILL.md
told the agent to run `poly positions`, so it reported empty as if it were the
user's wallet. Now both query the real API.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from . import journal
from .config import (
    CLOB_HOST,
    DATA_API,
    HTTP_TIMEOUT,
    POLYGON_CHAIN_ID,
    Settings,
    load_settings,
)
from .guardrails import Decision, evaluate_order
from .keystore import KeystoreError, LoadedKey, load_key
from .paths import trade_lock


class TradingError(RuntimeError):
    """Authentication, network, or exchange-rejection failure."""


@dataclass
class OrderResult:
    ok: bool
    order_id: str = ""
    status: str = ""
    detail: str = ""
    dry_run: bool = False
    decision: Optional[Decision] = None


_CLIENT_CACHE: Dict[str, Any] = {}


def _read_session() -> requests.Session:
    sess = requests.Session()
    sess.trust_env = False
    sess.headers.update({"User-Agent": "polymarket-agent/2.0 (+openclaw skill)"})
    return sess


def get_client(settings: Optional[Settings] = None, interactive: bool = True):
    """Authenticated CLOB client. The key is only decrypted here, in memory.

    The host and chain_id are constants of the config module — they never come
    from user input, so a tampered config cannot redirect signed orders to an
    endpoint controlled by a third party.
    """
    settings = settings or load_settings()
    cache_key = f"{settings.signature_type}:{settings.funder_address}"
    if cache_key in _CLIENT_CACHE:
        return _CLIENT_CACHE[cache_key]

    try:
        from py_clob_client.client import ClobClient
    except ImportError as exc:  # pragma: no cover
        raise TradingError(
            "py-clob-client is not installed. Run `./install.sh` or "
            "`pip install -r requirements.txt`."
        ) from exc

    try:
        loaded: LoadedKey = load_key(interactive=interactive)
    except KeystoreError as exc:
        raise TradingError(str(exc)) from exc

    kwargs: Dict[str, Any] = {
        "key": loaded.private_key,
        "chain_id": POLYGON_CHAIN_ID,
    }
    # Wallets created through the Polymarket interface (email/magic or browser)
    # custody the USDC in a proxy: signing as a plain EOA would give "not enough
    # balance" even with a balance on screen.
    if settings.signature_type in (1, 2):
        if not settings.funder_address:
            raise TradingError(
                f"signature_type={settings.signature_type} requires `funder_address` "
                "(the address that holds the USDC). Configure it with:\n"
                "  poly config --key funder_address --value 0x..."
            )
        kwargs["signature_type"] = settings.signature_type
        kwargs["funder"] = settings.funder_address

    try:
        client = ClobClient(CLOB_HOST, **kwargs)
        client.set_api_creds(client.create_or_derive_api_creds())
    except Exception as exc:
        raise TradingError(f"CLOB authentication failed: {exc}") from exc

    _CLIENT_CACHE[cache_key] = client
    return client


def wallet_address(settings: Optional[Settings] = None,
                   interactive: bool = True) -> str:
    """Effective address of the funds (proxy when there is one)."""
    settings = settings or load_settings()
    if settings.signature_type in (1, 2) and settings.funder_address:
        return settings.funder_address
    from .keystore import keystore_address

    addr = keystore_address()
    if addr:
        return addr
    return load_key(interactive=interactive).address


def get_balance(settings: Optional[Settings] = None,
                interactive: bool = True) -> Optional[float]:
    """Available USDC balance (collateral). None if unavailable."""
    settings = settings or load_settings()
    client = get_client(settings, interactive)
    try:
        from py_clob_client.clob_types import AssetType, BalanceAllowanceParams

        info = client.get_balance_allowance(
            params=BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
        )
    except Exception as exc:
        raise TradingError(f"failed to query balance: {exc}") from exc

    raw = (info or {}).get("balance")
    if raw is None:
        return None
    try:
        return float(raw) / 1e6  # USDC has 6 decimals
    except (TypeError, ValueError):
        return None


def get_positions(settings: Optional[Settings] = None,
                  interactive: bool = True) -> List[Dict[str, Any]]:
    """Open positions via the Data API (public endpoint, by address)."""
    address = wallet_address(settings, interactive)
    try:
        resp = _read_session().get(
            f"{DATA_API}/positions",
            params={"user": address, "sizeThreshold": 0.1},
            timeout=HTTP_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise TradingError(f"network failure fetching positions: {exc}") from exc
    if resp.status_code != 200:
        raise TradingError(f"Data API responded HTTP {resp.status_code}")
    try:
        rows = resp.json()
    except ValueError as exc:
        raise TradingError("Data API returned a non-JSON response") from exc
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def get_open_orders(settings: Optional[Settings] = None,
                    interactive: bool = True) -> List[Dict[str, Any]]:
    client = get_client(settings, interactive)
    try:
        orders = client.get_orders()
    except Exception as exc:
        raise TradingError(f"failed to fetch open orders: {exc}") from exc
    return [o for o in orders if isinstance(o, dict)] if isinstance(orders, list) else []


def cancel_order(order_id: str, settings: Optional[Settings] = None,
                 interactive: bool = True) -> bool:
    client = get_client(settings, interactive)
    try:
        client.cancel(order_id=order_id)
    except Exception as exc:
        raise TradingError(f"failed to cancel {order_id}: {exc}") from exc
    # Close the ORIGINAL entry — writing a new line would leave the cancelled
    # order counting as open indefinitely.
    if not journal.close_by_order_id(order_id, "cancelled"):
        journal.record(
            journal.Entry(kind="order", status="cancelled", order_id=order_id,
                          detail="cancellation with no matching journal entry")
        )
    return True


def cancel_all(settings: Optional[Settings] = None,
               interactive: bool = True) -> bool:
    client = get_client(settings, interactive)
    try:
        client.cancel_all()
    except Exception as exc:
        raise TradingError(f"failed to cancel all orders: {exc}") from exc
    journal.close_all_open("cancelled", detail="cancel_all")
    return True


def place_order(
    token_id: str,
    side: str,
    price: float,
    size: float,
    settings: Optional[Settings] = None,
    market_label: str = "",
    balance_usd: Optional[float] = None,
    interactive: bool = True,
    confirmed: bool = False,
    open_orders: Optional[int] = None,
) -> OrderResult:
    """Validate, journal and (if allowed) send a limit order.

    `confirmed` represents the HUMAN decision, taken at the CLI layer. A valid
    autonomous mode is the only case in which it can be waived — and even then
    all the financial caps still apply.
    """
    settings = settings or load_settings()
    side_upper = (side or "").strip().upper()
    token_id = (token_id or "").strip()

    if not token_id or not token_id.isdigit():
        return OrderResult(
            False,
            detail=(
                "invalid token_id: use the numeric identifier of the OUTCOME "
                "(see `poly markets <search>`), not the market id."
            ),
        )

    # Evaluate-and-journal must be atomic across processes, otherwise two
    # simultaneous `poly buy` runs read the same accumulated spend and both pass.
    with trade_lock():
        return _place_order_locked(
            token_id, side_upper, price, size, settings,
            market_label, balance_usd, interactive, confirmed, open_orders,
        )


def _place_order_locked(
    token_id: str,
    side_upper: str,
    price: float,
    size: float,
    settings: Settings,
    market_label: str,
    balance_usd: Optional[float],
    interactive: bool,
    confirmed: bool,
    open_orders: Optional[int],
) -> OrderResult:
    decision = evaluate_order(
        side_upper, price, size, settings, balance_usd, open_orders
    )

    if not decision.allowed:
        journal.record(
            journal.Entry(
                status="rejected",
                side=side_upper,
                token_id=token_id,
                market=market_label,
                price=float(price),
                size=float(size),
                notional=decision.notional,
                detail=decision.blocked_summary(),
            )
        )
        return OrderResult(False, detail=decision.blocked_summary(), decision=decision)

    if decision.requires_confirmation and not confirmed:
        return OrderResult(
            False,
            detail="order requires explicit user confirmation",
            decision=decision,
        )

    if settings.dry_run:
        journal.record(
            journal.Entry(
                status="dry_run",
                side=side_upper,
                token_id=token_id,
                market=market_label,
                price=float(price),
                size=float(size),
                notional=decision.notional,
                detail="dry-run: nothing was sent to the exchange",
            )
        )
        return OrderResult(
            True,
            status="dry_run",
            detail=f"DRY-RUN: valid order (${decision.notional:.2f}), not sent.",
            dry_run=True,
            decision=decision,
        )

    # Journal the INTENT before sending: if the process dies mid-way, the spend
    # stays accounted for and the user sees that something went out.
    entry = journal.record(
        journal.Entry(
            status="submitted",
            side=side_upper,
            token_id=token_id,
            market=market_label,
            price=float(price),
            size=float(size),
            notional=decision.notional,
        )
    )

    client = get_client(settings, interactive)
    try:
        from py_clob_client.clob_types import OrderArgs, OrderType
        from py_clob_client.order_builder.constants import BUY, SELL

        signed = client.create_order(
            OrderArgs(
                token_id=token_id,
                price=float(price),
                size=float(size),
                side=BUY if side_upper == "BUY" else SELL,
            )
        )
        resp = client.post_order(signed, OrderType.GTC)
    except Exception as exc:
        journal.update_status(entry.id, "failed", detail=str(exc)[:400])
        return OrderResult(False, detail=f"exchange rejected the order: {exc}",
                           decision=decision)

    resp = resp if isinstance(resp, dict) else {}
    order_id = str(resp.get("orderID") or resp.get("orderId") or "")
    success = bool(resp.get("success", True)) and not resp.get("errorMsg")
    status = str(resp.get("status") or ("submitted" if success else "failed"))

    journal.update_status(
        entry.id,
        status if success else "failed",
        order_id=order_id,
        detail=str(resp.get("errorMsg") or "")[:400],
    )

    if not success:
        return OrderResult(
            False,
            order_id=order_id,
            status=status,
            detail=str(resp.get("errorMsg") or "order refused"),
            decision=decision,
        )

    return OrderResult(True, order_id=order_id, status=status, decision=decision)
