"""nano-invoice create|check|receipt|verify|refund-hint|show -- JSON on stdout."""
import argparse
import json
import os
import sys

from . import account as acct
from . import core
from .rpc import DEFAULT_RPC, Rpc


def _out(obj):
    json.dump(obj, sys.stdout, indent=2, sort_keys=False, default=str)
    sys.stdout.write("\n")


def _not_income(args):
    table = {}
    if args.not_income_file:
        with open(args.not_income_file) as f:
            table.update(json.load(f))
    for item in args.not_income or ():
        account, _, reason = item.partition("=")
        table[account] = reason or "listed as not income"
    return table


def build_parser():
    p = argparse.ArgumentParser(prog="nano-invoice", description=__doc__)
    p.add_argument("--db", default=os.environ.get("NANO_INVOICE_DB", "nano-invoice.db"),
                   help="SQLite store (default ./nano-invoice.db or $NANO_INVOICE_DB)")
    p.add_argument("--rpc", default=os.environ.get("NANO_INVOICE_RPC", DEFAULT_RPC),
                   help=f"public Nano RPC, read-only (default {DEFAULT_RPC})")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create", help="create (or return the existing) invoice for an order")
    c.add_argument("--merchant", required=True)
    amt = c.add_mutually_exclusive_group(required=True)
    amt.add_argument("--amount-raw", help="price in raw, an integer (1 XNO = 10**30 raw)")
    amt.add_argument("--amount-xno", help="price in XNO as an exact decimal string, e.g. 0.25")
    c.add_argument("--order-key", required=True)
    c.add_argument("--expires-s", type=int, default=3600)

    k = sub.add_parser("check", help="read the ledger and settle the invoice")
    k.add_argument("--invoice", required=True)
    k.add_argument("--own", action="append", help="another account of the merchant (never income)")
    k.add_argument("--not-income", action="append", metavar="ACCOUNT[=REASON]",
                   help="faucet / test / internal account whose blocks never pay an invoice")
    k.add_argument("--not-income-file", help="JSON object {account: reason}")
    k.add_argument("--max-blocks", type=int, default=1000)

    r = sub.add_parser("receipt", help="print a receipt a stranger can re-check")
    r.add_argument("--invoice", required=True)

    v = sub.add_parser("verify", help="re-check a receipt from the public ledger alone")
    v.add_argument("--receipt", required=True, help="receipt JSON file, or - for stdin")

    h = sub.add_parser("refund-hint", help="refund instructions (never sends)")
    h.add_argument("--invoice", required=True)
    h.add_argument("--claimed-payer", help="shown only to say it was ignored")

    s = sub.add_parser("show", help="print the stored invoice and its recorded blocks")
    s.add_argument("--invoice", required=True)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    rpc = Rpc(args.rpc)
    try:
        if args.cmd == "verify":
            src = sys.stdin if args.receipt == "-" else open(args.receipt)
            with src:
                result = core.verify_receipt(json.load(src), rpc=rpc)
            _out(result)
            return 0 if result["ok"] else 1
        store = core.Store(args.db)
        if args.cmd == "create":
            raw = int(args.amount_raw) if args.amount_raw is not None else core.xno_to_raw(args.amount_xno)
            inv = core.create_invoice(args.merchant, raw, args.order_key, args.expires_s, store=store)
            _out(dict(inv.to_dict(), instruction=f"send exactly {inv.pay_raw} raw to {inv.merchant}"))
        elif args.cmd == "check":
            _out(core.check_invoice(args.invoice, rpc=rpc, store=store, own_accounts=args.own or (),
                                    not_income=_not_income(args), max_blocks=args.max_blocks))
        elif args.cmd == "receipt":
            _out(core.receipt(args.invoice, store=store))
        elif args.cmd == "refund-hint":
            hints = core.refund_hints(store, store.get(args.invoice).id)
            if args.claimed_payer:
                claimed = args.claimed_payer
                if acct.is_valid(claimed):
                    claimed = acct.normalise(claimed)
                for h in hints:
                    if h["to"] != claimed:
                        h["ignored_claimed_payer"] = args.claimed_payer
            _out({"invoice_id": args.invoice, "refunds": hints})
        elif args.cmd == "show":
            inv = store.get(args.invoice)
            _out({"invoice": inv.to_dict(),
                  "blocks": [dict(p, amount_raw=str(p["amount_raw"])) for p in store.payments_for(inv.id)]})
        return 0
    except (core.InvoiceError, ValueError) as e:
        _out({"error": type(e).__name__, "message": str(e)})
        return 2
    except Exception as e:  # RPC failures and the like
        _out({"error": type(e).__name__, "message": str(e)})
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
