#!/usr/bin/env python3
"""jerith-skill — OpenClaw skill CLI for JerithChain (JER).

Application-layer client of a JER node. Signs locally; the secret key
never leaves this machine and is never printed. Every monetary value in
output comes from the node — nothing here is invented.

Subcommands:
  wallet-create                      create the local wallet (once)
  wallet                             address + balance + network summary
  address                            receiving address
  balance                            confirmed balance + height
  history [--limit N]                recent transactions for the wallet
  status                             network status summary
  send <amount_jer> <address> [--memo M] [--yes]
  block <height> | blockhash <height>
  tx <txid> | confirmations <txid>
  mine [--source explicit|passive] [--message-id ID] [--guild-id G] [--channel-id C]

Output: human-readable by default, --json for structured results.
Exit codes: 0 ok, 1 error, 2 usage, 3 confirmation required.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

from jerith_client import Client, NodeError            # noqa: E402
from jerith_config import load_config, uj_to_jer       # noqa: E402
import jerith_transactions as tx_mod                   # noqa: E402
from jerith_mining import MiningDisabled, mine         # noqa: E402
from jerith_transactions import (                      # noqa: E402
    SpendError, _ConfirmNeeded, send, validate_address)
from jerith_wallet import (                            # noqa: E402
    create_wallet, load_wallet, wallet_exists)


def _out(d, as_json: bool):
    if as_json:
        print(json.dumps(d, indent=2))
    else:
        for k, v in d.items():
            print(f"{k}: {v}")


def _fail(msg: str, code: int = 1):
    print(f"jerith: {msg}", file=sys.stderr)
    sys.exit(code)


def cmd_wallet_create(cfg, args):
    rec = create_wallet(cfg)
    _out({"created": True, "address": rec["address"],
          "note": "secret key stored encrypted locally; back up "
                  "~/.config/jerith/ (wallet + key file) to keep access"},
         args.json)


def cmd_wallet(cfg, args):
    client = Client(cfg)
    wallet = load_wallet(cfg)
    bal = client.balance(wallet["address"])
    ch = client.chain()
    _out({"address": wallet["address"],
          "confirmed_balance_jer": uj_to_jer(bal.get("balance_uj", 0)),
          "nonce": bal.get("nonce", 0),
          "pending_mempool": bal.get("pending_mempool", 0),
          "height": ch.get("height"), "network": cfg["network"]}, args.json)


def cmd_address(cfg, args):
    _out({"address": load_wallet(cfg)["address"]}, args.json)


def cmd_balance(cfg, args):
    client = Client(cfg)
    wallet = load_wallet(cfg)
    bal = client.balance(wallet["address"])
    ch = client.chain()
    _out({"address": wallet["address"],
          "confirmed_balance_uj": bal.get("balance_uj", 0),
          "confirmed_balance_jer": uj_to_jer(bal.get("balance_uj", 0)),
          "pending_mempool": bal.get("pending_mempool", 0),
          "height": ch.get("height")}, args.json)


def cmd_estimate_fee(cfg, args):
    """What will sending amount_jer actually cost (fee + total, and whether
    it needs confirmation)? Pure node-ledger math; sends nothing."""
    from jerith_config import jer_to_uj
    from jerith_wallet import wallet_exists
    amount_uj = jer_to_uj(args.amount)
    fee_uj = 100_000  # 0.1 JER — flat node fee (node also enforces)
    client = Client(cfg)
    have = None
    if wallet_exists(cfg):
        have = int(client.balance(load_wallet(cfg)["address"]).get(
            "balance_uj", 0))
    total = amount_uj + fee_uj
    # confirmation gate mirrors enforce_limits without recording state
    sp = cfg["spending"]
    needs_conf = bool(sp.get("require_confirmation")) and \
        amount_uj > round(sp["automatic_send_limit_jer"] * 1_000_000)
    over_daily = (tx_mod._daily_sent_uj() + amount_uj >
                  round(sp["daily_limit_jer"] * 1_000_000))
    _out({"amount_jer": uj_to_jer(amount_uj), "fee_jer": uj_to_jer(fee_uj),
          "total_jer": uj_to_jer(total),
          **({"balance_jer": uj_to_jer(have),
              "affordable": have >= total} if have is not None else {}),
          "needs_confirmation": needs_conf,
          "within_daily_limit": not over_daily,
          "sendable_now": ((have is not None and have >= total)
                           and not needs_conf and not over_daily)},
         args.json)


def cmd_netinfo(cfg, args):
    """Node diagnostics mirror (peer-facing info from /x/networkinfo)."""
    _out(Client(cfg).networkinfo(), args.json)


def cmd_status(cfg, args):
    client = Client(cfg)
    ch = client.chain()
    wallet = load_wallet(cfg)
    bal = client.balance(wallet["address"])
    _out({"connected": True, "network": cfg["network"],
          "protocol_version": ch.get("protocol_version"),
          "height": ch.get("height"),
          "best_block_hash": ch.get("best_block_hash"),
          "difficulty_bits": ch.get("difficulty_bits"),
          "chain_work": ch.get("chain_work"),
          "mempool_size": ch.get("mempool_size"),
          "standard_confirmations": ch.get("standard_confirmations"),
          "wallet_address": wallet["address"],
          "wallet_balance_jer": uj_to_jer(bal.get("balance_uj", 0))}, args.json)


def cmd_history(cfg, args):
    """Indexed history via the explorer API (fast, address-keyed). Falls
    back to reporting the explorer as unavailable."""
    client = Client(cfg)
    wallet = load_wallet(cfg)
    try:
        hist = client.address_history(wallet["address"], cfg)
    except NodeError as e:
        _out({"address": wallet["address"], "transactions": [],
              "note": f"history unavailable ({e.detail})"}, args.json)
        return
    ch = client.chain()
    tip = int(ch.get("height", 0))
    txs = [{
        "txid": t["txid"],
        "direction": "out" if t.get("sender") == wallet["address"] else "in",
        "amount_jer": uj_to_jer(t.get("amount_uj", 0)),
        "counterparty": (t.get("recipient") if t.get("sender") == wallet["address"]
                         else t.get("sender")),
        "height": t.get("height"),
        "confirmations": max(tip - int(t.get("height") or 0) + 1, 0)
                          if t.get("height") is not None else None,
        "timestamp": t.get("timestamp"),
        "kind": t.get("kind"),
        "memo": t.get("memo", ""),
    } for t in hist.get("transactions", [])[:args.limit]]
    _out({"address": wallet["address"], "transactions": txs}, args.json)


def cmd_supply(cfg, args):
    """Supply accounting from the explorer (emitted / burned / circulating
    / remaining / next-halving info)."""
    client = Client(cfg)
    st = client.explorer_status(cfg)
    ch = client.chain()
    circ = int(st.get("circulating_uj", 0))
    premine = int(st.get("premine_uj", 0))
    max_uj = int(st.get("max_supply_uj", 0))
    height = int(st.get("height", 0))
    reward = int(st.get("block_reward_uj", 0))
    halving = 210_000
    next_h = ((height // halving) + 1) * halving
    _out({"height": height,
          "circulating_jer": uj_to_jer(circ),
          "emitted_jer": uj_to_jer(circ),       # no fee burn observed yet
          "max_supply_jer": uj_to_jer(max_uj),
          "remaining_jer": uj_to_jer(max_uj - circ),
          "premine_jer": uj_to_jer(premine),
          "mined_since_genesis_jer": uj_to_jer(circ - premine),
          "current_reward_jer": uj_to_jer(reward),
          "next_halving_height": next_h,
          "blocks_to_next_halving": max(next_h - height, 0)}, args.json)


def cmd_watch(cfg, args):
    """Poll a txid until it reaches --target confirmations (or timeout).
    Returns the final confirmation state — never claims confirmed early."""
    import time as _t
    client = Client(cfg)
    deadline = _t.time() + args.timeout
    last = None
    while _t.time() < deadline:
        try:
            last = client.confirmations(args.txid)
            if last.get("confirmations", 0) >= args.target:
                break
        except NodeError as e:
            if e.kind not in ("http",):   # 404 = not yet in a block; keep waiting
                raise
            last = {"txid": args.txid, "confirmations": 0, "state": "pending"}
        _t.sleep(args.interval)
    if last is None:
        last = {"txid": args.txid, "confirmations": 0, "state": "timeout"}
    last["reached_target"] = last.get("confirmations", 0) >= args.target
    last["state"] = ("confirmed-at-target" if last["reached_target"]
                     else f"pending ({last.get('confirmations', 0)} confirmations)" \
                          if last.get("confirmations") else "not yet in a block")
    _out(last, args.json)


def cmd_send(cfg, args):
    try:
        res = send(cfg, args.address, args.amount, memo=args.memo,
                   confirmed=args.yes)
    except _ConfirmNeeded as e:
        _out({"status": "confirmation_required",
              "summary": f"Send {args.amount:g} JER",
              "to": validate_address(args.address),
              "fee_jer": 0.1,
              "total_jer": args.amount + 0.1,
              "instruction": "Ask the user to confirm, then re-run with --yes"},
             args.json)
        sys.exit(3)
    except SpendError as e:
        _out({"success": False, "error": str(e)}, args.json)
        sys.exit(1)
    _out(res, args.json)


def cmd_block(cfg, args):
    _out(Client(cfg).block(args.height), args.json)


def cmd_blockhash(cfg, args):
    _out(Client(cfg).blockhash(args.height), args.json)


def cmd_tx(cfg, args):
    _out(Client(cfg).tx(args.txid), args.json)


def cmd_confirmations(cfg, args):
    _out(Client(cfg).confirmations(args.txid), args.json)


def cmd_mine(cfg, args):
    did = args.discord_id or cfg.get("default_discord_id", "")
    if not did:
        _fail("mining requires --discord-id (the identity the node credits)")
    try:
        res = mine(cfg, did, source=args.source, guild_id=args.guild_id,
                   channel_id=args.channel_id, message_id=args.message_id)
    except MiningDisabled as e:
        _out({"ok": False, "reason": "disabled", "message": str(e)}, args.json)
        sys.exit(1)
    except NodeError as e:
        _out({"ok": False, "reason": e.kind, "message": e.detail}, args.json)
        sys.exit(1)
    if not res.get("ok") and res.get("reason") == "cooldown" and args.wait:
        # cooldown-aware retry: the node says 300 s after success; poll
        # sparingly (never tighter than 30 s) until the window opens
        import time as _t
        waited = 0
        while waited < args.wait:
            _t.sleep(min(30, args.wait - waited))
            waited += min(30, args.wait)
            res = mine(cfg, did, source=args.source, guild_id=args.guild_id,
                       channel_id=args.channel_id, message_id=args.message_id)
            if res.get("ok") or res.get("reason") != "cooldown":
                break
        res["waited_seconds"] = waited
    _out(res, args.json)


def cmd_backup(cfg, args):
    """Write an ENCRYPTED backup bundle (wallet + keyfile) to the given
    path. Never writes plaintext secrets. Restorable via wallet-restore."""
    from jerith_wallet import wallet_path, _keydir
    wp = wallet_path(cfg)
    kf = _keydir() / "wallet.key"
    if not wp.exists() or not kf.exists():
        _fail("no wallet to back up")
    import tarfile
    out = Path(args.out).expanduser()
    if out.exists() and not args.force:
        _fail(f"{out} exists (use --force to overwrite)")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(out, "w:gz") as tar:
        tar.add(wp, arcname="skill-wallet.json")
        tar.add(kf, arcname="wallet.key")
    os.chmod(out, 0o600)
    _out({"backed_up": True, "path": str(out),
          "warning": "whoever holds this file controls the wallet's JER — "
                     "store it offline", "encrypted_at_rest": True},
         args.json)


def cmd_restore(cfg, args):
    """Restore a backup bundle made by wallet-backup. Refuses to clobber an
    existing wallet without --force."""
    from jerith_wallet import wallet_path, _keydir
    src = Path(args.src).expanduser()
    if not src.exists():
        _fail(f"backup not found: {src}")
    wp = wallet_path(cfg)
    if wp.exists() and not args.force:
        _fail("wallet already exists — use --force to replace it")
    import tarfile
    with tarfile.open(src, "r:gz") as tar:
        members = {m.name: m for m in tar.getmembers()}
        for need in ("skill-wallet.json", "wallet.key"):
            m = members.get(need)
            if m is None or not m.isfile() or m.name != need:
                _fail(f"backup member {need!r} missing or unsafe "
                      f"(not a jerith backup?)")
        # read ONLY the two expected members (no extractall — a crafted
        # archive can never write outside this process's temp dir)
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            for need in ("skill-wallet.json", "wallet.key"):
                f_in = tar.extractfile(members[need])
                (td / need).write_bytes(f_in.read())
            wp.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy(td / "skill-wallet.json", wp)
            shutil.copy(td / "wallet.key", _keydir() / "wallet.key")
    os.chmod(wp, 0o600)
    os.chmod(_keydir() / "wallet.key", 0o600)
    rec = json.loads(wp.read_text())
    _out({"restored": True, "address": rec.get("address")}, args.json)


def cmd_validate(cfg, args):
    """Check whether a string is a well-formed JER address (no node needed)."""
    try:
        validate_address(args.address)
        _out({"valid": True, "address": args.address}, args.json)
    except SpendError as e:
        _out({"valid": False, "error": str(e)}, args.json)
        sys.exit(1)


def main() -> int:
    ap = argparse.ArgumentParser(prog="jerith-skill")
    ap.add_argument("--json", action="store_true", help="structured JSON output")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("wallet-create").set_defaults(fn=cmd_wallet_create)
    sub.add_parser("wallet").set_defaults(fn=cmd_wallet)
    sub.add_parser("address").set_defaults(fn=cmd_address)
    sub.add_parser("balance").set_defaults(fn=cmd_balance)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    p = sub.add_parser("history"); p.add_argument("--limit", type=int, default=10)
    p.set_defaults(fn=cmd_history)
    p = sub.add_parser("send")
    p.add_argument("amount", type=float); p.add_argument("address")
    p.add_argument("--memo", default=""); p.add_argument("--yes", action="store_true")
    p.set_defaults(fn=cmd_send)
    p = sub.add_parser("block"); p.add_argument("height", type=int)
    p.set_defaults(fn=cmd_block)
    p = sub.add_parser("blockhash"); p.add_argument("height", type=int)
    p.set_defaults(fn=cmd_blockhash)
    p = sub.add_parser("tx"); p.add_argument("txid")
    p.set_defaults(fn=cmd_tx)
    p = sub.add_parser("confirmations"); p.add_argument("txid")
    p.set_defaults(fn=cmd_confirmations)
    p = sub.add_parser("estimate-fee")
    p.add_argument("amount", type=float, help="amount in JER")
    p.set_defaults(fn=cmd_estimate_fee)
    p = sub.add_parser("netinfo").set_defaults(fn=cmd_netinfo)
    p = sub.add_parser("mine")
    p.add_argument("--source", default="explicit", choices=["explicit", "passive"])
    p.add_argument("--discord-id", default="")
    p.add_argument("--message-id", default="")
    p.add_argument("--guild-id", default="")
    p.add_argument("--channel-id", default="")
    p.add_argument("--wait", type=int, default=0,
                   help="if cooldown, retry for up to N seconds (30s poll)")
    p.set_defaults(fn=cmd_mine)
    p = sub.add_parser("supply").set_defaults(fn=cmd_supply)
    p = sub.add_parser("watch")
    p.add_argument("txid")
    p.add_argument("--target", type=int, default=1)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--interval", type=float, default=5.0)
    p.set_defaults(fn=cmd_watch)
    p = sub.add_parser("wallet-backup")
    p.add_argument("out"); p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_backup)
    p = sub.add_parser("wallet-restore")
    p.add_argument("src"); p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_restore)
    p = sub.add_parser("validate"); p.add_argument("address")
    p.set_defaults(fn=cmd_validate)

    args = ap.parse_args()
    cfg = load_config()
    try:
        args.fn(cfg, args)
    except NodeError as e:
        _out({"error": e.kind, "detail": e.detail, "node": cfg["rpc_url"]},
             getattr(args, "json", False))
        _fail(e.detail if not getattr(args, "json", False) else "", 1)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 — never leak tracebacks to chat
        _fail(f"unexpected error: {type(e).__name__}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
