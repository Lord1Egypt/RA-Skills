#!/usr/bin/env python3
"""Step 1 of the IBKR trade gate: propose, do not execute.

Resolves the user's natural sizing (--quote-sz USD or --shares) into the
exact IBKR order parameters, validates guardrails, writes a pending JSON,
and prints the proposal id.

Stocks/ETFs default to SMART exchange + USD currency. Override via flags
or env vars (IBKR_DEFAULT_EXCHANGE, IBKR_DEFAULT_CURRENCY).

Fractional shares are accepted by IBKR for eligible securities; pass
--allow-fractional (default true). Set --no-fractional to round down to
the nearest whole share before placing the order.
"""
from __future__ import annotations

import argparse
import sys

from _audit import append as audit_append
from _guardrails import GuardrailError, check_all
from _ibkr_client import connect, env_summary, smart_stock
from _pending import PENDING_DIR, save_pending


def _ref_price(ib, contract, ord_type: str, lmt_price: float | None) -> float:
    """Use the user's limit if present; else delayed-frozen last/close."""
    if ord_type == "LMT" and lmt_price:
        return float(lmt_price)
    ib.reqMarketDataType(4)  # delayed-frozen
    t = ib.reqMktData(contract, "", False, False)
    ib.sleep(2.5)
    px = t.last or t.close or t.bid or t.ask
    ib.cancelMktData(contract)
    if not px or px != px:  # NaN check
        raise RuntimeError(f"Could not fetch reference price for {contract.symbol}")
    return float(px)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", required=True, help="e.g. VOO, SPY, AAPL")
    p.add_argument("--side", choices=["BUY", "SELL"], required=True)
    sizing = p.add_mutually_exclusive_group(required=True)
    sizing.add_argument("--quote-sz", type=float, help="Sized in USD (will compute shares from current price)")
    sizing.add_argument("--shares", type=float, help="Exact share quantity (supports fractional)")
    p.add_argument("--ord-type", choices=["MKT", "LMT"], default="MKT")
    p.add_argument("--lmt-price", type=float, default=None, help="Required for --ord-type LMT")
    p.add_argument("--exchange", default=None)
    p.add_argument("--currency", default=None)
    p.add_argument("--allow-fractional", dest="fractional", action="store_true", default=True,
                   help="Allow fractional shares for eligible securities (default).")
    p.add_argument("--no-fractional", dest="fractional", action="store_false",
                   help="Round share quantity down to the nearest whole share.")
    p.add_argument("--note", default="")
    args = p.parse_args()

    if args.ord_type == "LMT" and args.lmt_price is None:
        print("--lmt-price is required for --ord-type LMT", file=sys.stderr)
        return 2

    ib = connect()
    try:
        contract = smart_stock(args.symbol, args.exchange, args.currency)
        qualified = ib.qualifyContracts(contract)
        if not qualified:
            print(f"Could not qualify contract for {args.symbol}", file=sys.stderr)
            return 1
        contract = qualified[0]

        try:
            ref_px = _ref_price(ib, contract, args.ord_type, args.lmt_price)
        except RuntimeError as e:
            print(str(e), file=sys.stderr)
            return 1

        # Resolve quantity.
        if args.shares is not None:
            shares = float(args.shares)
        else:
            shares = float(args.quote_sz) / ref_px

        if not args.fractional:
            shares = float(int(shares))  # round down to whole

        if shares <= 0:
            print(f"Computed shares = {shares}; quote-sz too small for current price ${ref_px}", file=sys.stderr)
            return 2

        notional = shares * ref_px

        try:
            check_all(args.symbol, notional)
        except GuardrailError as e:
            print(f"REFUSED: {e}", file=sys.stderr)
            return 3

        # Build the order params we'll replay verbatim at execute time.
        order_params = {
            "action": args.side,
            "totalQuantity": shares,
            "orderType": args.ord_type,
            "outsideRth": False,
            "tif": "DAY",
            "transmit": True,
        }
        if args.ord_type == "LMT":
            order_params["lmtPrice"] = float(args.lmt_price)

        contract_params = {
            "symbol": contract.symbol,
            "secType": contract.secType,
            "exchange": contract.exchange,
            "currency": contract.currency,
            "primaryExchange": getattr(contract, "primaryExchange", "") or "",
            "conId": int(contract.conId or 0),
        }

        payload = {
            "symbol": args.symbol.upper(),
            "side": args.side,
            "ord_type": args.ord_type,
            "shares": round(shares, 8),
            "ref_price": round(ref_px, 6),
            "notional_usd": round(notional, 4),
            "fractional": bool(args.fractional),
            "contract": contract_params,
            "order": order_params,
            "note": args.note,
        }
        pid, _token = save_pending("trade", payload)
        pending_path = PENDING_DIR / f"{pid}.json"

        audit_append(
            "proposal_created",
            id=pid,
            symbol=args.symbol.upper(),
            side=args.side,
            shares=round(shares, 8),
            notional_usd=round(notional, 4),
        )

        print(env_summary())
        print(f"Proposal id: {pid}")
        print(f"Pending file: {pending_path}")
        print(f"  {args.side} {args.symbol.upper()}  {shares:.6f} shares")
        print(f"  ord_type   : {args.ord_type}{' @ ' + str(args.lmt_price) if args.ord_type == 'LMT' else ''}")
        print(f"  ref price  : ${ref_px:.4f}")
        print(f"  notional   : ~${notional:.2f}")
        print(f"  fractional : {'yes' if args.fractional else 'no'}")
        if args.note:
            print(f"  note       : {args.note}")
        print()
        print(f"To confirm in chat, ask the user to reply: YES {pid}")
        print(f"To discard, the user can reply: NO {pid}")
    finally:
        ib.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
