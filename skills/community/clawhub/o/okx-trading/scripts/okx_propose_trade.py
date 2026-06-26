#!/usr/bin/env python3
"""Step 1 of the trade gate: propose, do not execute.

Resolves the user's natural sizing (--quote-sz $USDT or --base-sz coins) into the
exact OKX `place_order` parameters, validates guardrails, writes a pending JSON,
and prints the proposal id.

The confirmation_token is generated and stored ONLY in the pending file — never
printed to stdout, never returned to the LLM. The LLM has to read the pending
file via the file_read tool to discover the token, which means an attacker who
sees only chat history cannot forge an execute call.
"""
from __future__ import annotations

import argparse
import sys

from _guardrails import GuardrailError, check_all
from _okx_client import inst_type_for, market_api, public_api
from _pending import PENDING_DIR, save_pending


def _ref_price(inst_id: str, ord_type: str, px: str | None) -> float:
    if ord_type == "limit" and px:
        return float(px)
    resp = market_api().get_ticker(instId=inst_id)
    if resp.get("code") != "0" or not resp.get("data"):
        raise RuntimeError(f"Could not fetch ticker for {inst_id}: {resp.get('msg')!r}")
    return float(resp["data"][0]["last"])


def _ct_val(inst_type: str, inst_id: str) -> float:
    """Contract value (in base ccy) for swap/futures/option. SPOT returns 1."""
    if inst_type == "SPOT":
        return 1.0
    resp = public_api().get_instruments(instType=inst_type, instId=inst_id)
    if resp.get("code") != "0" or not resp.get("data"):
        raise RuntimeError(f"Could not fetch instrument metadata for {inst_id}")
    return float(resp["data"][0].get("ctVal", "1") or "1")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--instId", required=True)
    p.add_argument("--side", choices=["buy", "sell"], required=True)
    sizing = p.add_mutually_exclusive_group(required=True)
    sizing.add_argument("--quote-sz", type=float, help="USDT-quoted size, e.g. 25")
    sizing.add_argument("--base-sz", type=float, help="Base-currency size, e.g. 0.001")
    p.add_argument("--ord-type", choices=["market", "limit"], default="market")
    p.add_argument("--px", default=None, help="Required for --ord-type limit")
    p.add_argument("--td-mode", default=None, help="cash|cross|isolated; default cash for SPOT, cross otherwise")
    p.add_argument("--pos-side", default=None, help="long|short — required for swap/futures in long/short mode")
    p.add_argument("--ccy", default=None, help="Margin ccy (margin trading only)")
    p.add_argument("--lever", default=None, help="Leverage for swap/futures (set on the instrument first if needed)")
    p.add_argument("--note", default="", help="Free-text note shown in the proposal")
    args = p.parse_args()

    try:
        inst_type = inst_type_for(args.instId)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2

    if args.ord_type == "limit" and not args.px:
        print("--px is required for limit orders", file=sys.stderr)
        return 2

    td_mode = args.td_mode or ("cash" if inst_type == "SPOT" else "cross")

    # Reference price (for sizing math + notional estimate).
    try:
        ref_px = _ref_price(args.instId, args.ord_type, args.px)
        ct_val = _ct_val(inst_type, args.instId)
    except Exception as e:
        print(f"Pre-trade lookup failed: {e}", file=sys.stderr)
        return 1

    # ── Resolve OKX place_order params ─────────────────────────────────
    api_params: dict = {
        "instId": args.instId,
        "tdMode": td_mode,
        "side": args.side,
        "ordType": args.ord_type,
    }
    if args.pos_side:
        api_params["posSide"] = args.pos_side
    if args.ccy:
        api_params["ccy"] = args.ccy
    if args.ord_type == "limit":
        api_params["px"] = str(args.px)

    if inst_type == "SPOT":
        # Spot market buy with USDT amount uses tgtCcy='quote_ccy' so OKX
        # interprets `sz` as the quote currency; sells/limits always use base.
        if args.quote_sz is not None:
            if args.ord_type == "market" and args.side == "buy":
                api_params["tgtCcy"] = "quote_ccy"
                api_params["sz"] = str(args.quote_sz)
                base_sz = args.quote_sz / ref_px
                notional = float(args.quote_sz)
            else:
                base_sz = args.quote_sz / ref_px
                api_params["sz"] = f"{base_sz:.8f}".rstrip("0").rstrip(".")
                notional = base_sz * ref_px
        else:
            base_sz = float(args.base_sz)
            api_params["sz"] = f"{base_sz:.8f}".rstrip("0").rstrip(".")
            notional = base_sz * ref_px
    else:
        # Non-spot: sz is in contracts; convert from quote/base via ctVal.
        if args.quote_sz is not None:
            contracts = args.quote_sz / (ct_val * ref_px)
        else:
            contracts = float(args.base_sz) / ct_val
        api_params["sz"] = f"{contracts:.8f}".rstrip("0").rstrip(".")
        notional = contracts * ct_val * ref_px

    # ── Guardrails ─────────────────────────────────────────────────────
    try:
        check_all(args.instId, notional)
    except GuardrailError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 3

    # ── Save pending ───────────────────────────────────────────────────
    payload = {
        "instType": inst_type,
        "instId": args.instId,
        "side": args.side,
        "ord_type": args.ord_type,
        "td_mode": td_mode,
        "ref_price": ref_px,
        "notional_usdt": round(notional, 4),
        "api_params": api_params,
        "note": args.note,
    }
    pid, _token = save_pending("trade", payload)
    pending_path = PENDING_DIR / f"{pid}.json"

    print(f"Proposal id: {pid}")
    print(f"Pending file: {pending_path}")
    print(f"  {args.side.upper()} {args.instId} ({inst_type})")
    print(f"  ord_type   : {args.ord_type}{' @ ' + str(args.px) if args.ord_type == 'limit' else ''}")
    if inst_type == "SPOT" and args.ord_type == "market" and args.side == "buy" and args.quote_sz is not None:
        print(f"  size       : {args.quote_sz} USDT (market buy, quote-sized)")
    else:
        print(f"  size       : {api_params['sz']} {'contracts' if inst_type != 'SPOT' else 'base'}")
    print(f"  ref price  : {ref_px}")
    print(f"  notional   : ~{notional:.2f} USDT")
    if args.note:
        print(f"  note       : {args.note}")
    print()
    print(f"To confirm in chat, ask the user to reply: YES {pid}")
    print(f"To discard, the user can reply: NO {pid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
