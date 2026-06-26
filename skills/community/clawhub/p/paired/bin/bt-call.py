#!/usr/bin/env python3
"""bt-call — Make a call through a paired phone (HFP via ofono).

LOW-LEVEL PRIMITIVE. Most callers should use ~/bin/paired-call instead, which
adds JSON output, modem auto-resolution, and Telegram replies.

v1.0.4: gated by trusted-numbers allowlist. To dial a number that is not in
`~/.config/paired/trusted-numbers.conf`, pass --confirm. This addresses the
OpenClaw scanner finding that the low-level dial primitive accepted arbitrary
numbers without a safety check.

Examples:
  bt-call 07911123456                          # only if trusted, else refuses
  bt-call 07911123456 --confirm                # one-shot override
  bt-call 07911123456 --modem AA:BB:CC:DD:EE:FF
  bt-call --hangup                             # hang up everything
  bt-call --status                             # show current calls
"""
from __future__ import annotations
import argparse, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_telephony as bt

TRUSTED_NUMBERS_FILE = Path.home() / ".config" / "paired" / "trusted-numbers.conf"


def _normalize_uk(num: str) -> str:
    """Normalise a UK number for trusted-list comparison."""
    n = num.strip().replace(" ", "").replace("-", "")
    if n.startswith("+44"):
        n = "0" + n[3:]
    elif n.startswith("0044"):
        n = "0" + n[4:]
    elif n.startswith("44") and len(n) == 12:
        n = "0" + n[2:]
    return n


def _load_trusted() -> set[str]:
    s: set[str] = set()
    if not TRUSTED_NUMBERS_FILE.exists():
        return s
    try:
        for line in TRUSTED_NUMBERS_FILE.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            tok = line.split()[0] if line.split() else ""
            if tok:
                s.add(_normalize_uk(tok))
    except OSError:
        pass
    return s


def _is_trusted(number: str) -> bool:
    return _normalize_uk(number) in _load_trusted()


def _resolve_modem(mac_arg: str | None) -> dict | None:
    modems = bt.list_modems()
    if not modems:
        return None
    if mac_arg:
        return bt.modem_for_mac(mac_arg)
    return modems[0]


def main() -> int:
    ap = argparse.ArgumentParser(description="Make / answer / hang up calls (LOW-LEVEL; prefer paired-call)")
    ap.add_argument("number", nargs="?", help="Phone number to dial")
    ap.add_argument("--modem", help="Specific paired phone MAC (default: first modem)")
    ap.add_argument("--answer", action="store_true", help="Answer incoming call")
    ap.add_argument("--hangup", action="store_true", help="Hang up all calls")
    ap.add_argument("--status", action="store_true", help="Show current calls")
    ap.add_argument("--hide-id", action="store_true", help="Hide caller ID")
    ap.add_argument("--confirm", action="store_true",
                    help="Override trusted-numbers gate for this dial")
    args = ap.parse_args()

    modem = _resolve_modem(args.modem)
    if modem is None:
        sys.stderr.write("No ofono modem available. Pair a phone with HFP first:\n")
        sys.stderr.write("  bt-pair <phone-mac> --connect\n")
        return 2

    path = modem["path"]

    if args.status:
        calls = bt.list_calls(path)
        if not calls:
            print(f"{path}: no active calls")
            return 0
        for c in calls:
            print(f"  {c.get('LineIdentification', '?')} state={c.get('State', '?')}")
        return 0

    if args.hangup:
        n = bt.hangup_all(path)
        print(f"hung up {n} call(s)")
        return 0

    if args.answer:
        cp = bt.answer_first(path)
        if cp:
            print(f"answered {cp}")
            return 0
        print("no incoming call to answer")
        return 1

    if not args.number:
        sys.stderr.write("error: number required (or use --hangup / --answer / --status)\n")
        return 2

    # v1.0.4: trust gating. Refuse to dial untrusted numbers without --confirm.
    if not _is_trusted(args.number) and not args.confirm:
        sys.stderr.write(
            f"REFUSING: {args.number} is not in {TRUSTED_NUMBERS_FILE}.\n"
            "To dial: either (a) add it via `paired-trusted add <number>`,\n"
            "or (b) pass --confirm to override for this one call.\n"
        )
        return 2

    print(f"dialing {args.number} via {path}...")
    try:
        cp = bt.dial(path, args.number, hide_caller_id=args.hide_id)
    except Exception as e:
        sys.stderr.write(f"DIAL FAILED: {e}\n")
        return 1
    print(f"call started: {cp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
