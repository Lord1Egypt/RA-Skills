#!/usr/bin/env python3
"""paired-call — High-level call control for Agent.

Wraps bt-call with auto-modem-resolution. Designed for Agent to invoke:

    paired-call status                  # active calls (or none)
    paired-call dial 07911123456        # initiate outbound
    paired-call answer                  # answer first incoming
    paired-call hangup                  # end all calls

Returns clean JSON with --json. Calls go through ofono HFP via the connected
phone; audio routes through the phone earpiece (two-way SCO over BT is a
known architectural block, see bluetooth skill notes).
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
_HOME = str(Path.home())

VALID_ACTIONS = {"status", "dial", "answer", "hangup"}


def call_bt_call(args: list[str], timeout=20) -> tuple[int, str, str]:
    p = subprocess.run([f"{_HOME}/bin/bt-call"] + args,
                       capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def parse_status(text: str) -> dict:
    """Parse bt-call --status output into structured form.
    Examples:
      '/hfp/org/bluez/hci1/dev_AA_BB_CC_DD_EE_FF: no active calls'
      '  +447911123456 state=incoming'
    """
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    out = {"modem": None, "calls": []}
    for ln in lines:
        if ln.startswith("/hfp/") or "/dev_" in ln:
            # modem header
            parts = ln.split(":", 1)
            out["modem"] = parts[0].strip()
        elif "state=" in ln:
            # call line: '+447911123456 state=incoming'
            number, _, state = ln.rpartition("state=")
            out["calls"].append({
                "number": number.strip(),
                "state": state.strip(),
            })
    return out


def emit(success: bool, action: str, stdout: str, stderr: str,
        as_json: bool, extra: dict | None = None):
    if as_json:
        payload = {
            "ok": success,
            "action": action,
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
        }
        if extra:
            payload.update(extra)
        print(json.dumps(payload, indent=2))
    else:
        if stdout.strip():
            print(stdout.rstrip())
        if not success and stderr.strip():
            print(f"warn: {stderr.strip()}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="High-level call control for Agent (status/dial/answer/hangup).")
    ap.add_argument("action", choices=sorted(VALID_ACTIONS),
                    help="status, dial, answer, hangup")
    ap.add_argument("number", nargs="?", default=None,
                    help="For 'dial': phone number to call")
    ap.add_argument("--modem",
                    help="Specific phone MAC (default: first paired ofono modem)")
    ap.add_argument("--hide-id", action="store_true",
                    help="Hide caller ID for outbound (CLIR) — for dial only")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    base = []
    if args.modem:
        base += ["--modem", args.modem]

    if args.action == "status":
        rc, out, err = call_bt_call(base + ["--status"])
        parsed = parse_status(out)
        emit(rc == 0, "status", out, err, args.json,
             {"parsed": parsed})
        return rc

    if args.action == "answer":
        rc, out, err = call_bt_call(base + ["--answer"])
        emit(rc == 0, "answer", out, err, args.json)
        return rc

    if args.action == "hangup":
        rc, out, err = call_bt_call(base + ["--hangup"])
        emit(rc == 0, "hangup", out, err, args.json)
        return rc

    if args.action == "dial":
        if not args.number:
            ap.error("dial requires a number")
        dial_args = base + [args.number]
        if args.hide_id:
            dial_args.append("--hide-id")
        rc, out, err = call_bt_call(dial_args, timeout=30)
        emit(rc == 0, "dial", out, err, args.json,
             {"number": args.number})
        return rc

    return 2


if __name__ == "__main__":
    sys.exit(main())
