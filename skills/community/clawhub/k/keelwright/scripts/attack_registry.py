#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""attack_registry.py — append-only JSONL log of agent attacks for keelwright.

WHY: a safety engine must leave an evidence trail. When an attack is caught, the operator
needs: (1) an immediate chat signal, (2) a durable record of who/what/when, (3) a rollup
to spot repeat offenders. This script is the durable record.

DESIGN RULES (do not weaken):
- Append-only JSONL. Never overwrite or delete historical lines (incident evidence).
- Stdlib only (no pip installs) — runs on Windows/MSYS and Linux.
- Always exits 0 on read; --add exits non-zero only if required fields missing (so a broken
  call surfaces, but normal logging never aborts the agent's run).
- Source: github.com/gweber/hermes-injection-guard (SPDX-License-Identifier: MIT)
  + scastile/hermes-agent-defense (SPDX-License-Identifier: MIT)
  + web-agent-security-gate (SPDX-License-Identifier: MIT-0, ClawHub / OpenClaw community)
  — all in the commercial-use-without-attribution white list. Technique adapted in
  operator's own words; no verbatim copy.
- Retention: entries older than 30 days are purged on --cleanup (non-blocking).
- Redaction: query parameters stripped from source_url before logging (no secrets in logs).
- Opt-in: logging only happens if KEELWRIGHT_ATTACK_REGISTRY=1 or explicit --add call.

USAGE:
  python attack_registry.py --add --channel web_extract --source-url https://x --attack-type \
    indirect-prompt-injection --severity HIGH --detected-by injection-guard --action-taken \
    blocked --outcome blocked-success --model-provider nous/tencent-hy3 --notes "..."
  python attack_registry.py --tail 20
  python attack_registry.py --stats
  python attack_registry.py --cleanup          # remove entries older than 30 days
  python attack_registry.py --cleanup --force  # force cleanup even if not opted in
"""
import argparse
import datetime
import json
import os
import re
import sys
from urllib.parse import urlparse, urlunparse

DEFAULT_PATH = os.path.join(
    os.path.expanduser("~"), ".keelwright", "attack_registry.jsonl"
)

REQUIRED_ADD = ["channel", "attack_type", "severity", "detected_by", "action_taken", "outcome"]
RETENTION_DAYS = 30

# Opt-in check: logging only if env var set or explicit --force-add
def is_opted_in() -> bool:
    return os.environ.get("KEELWRIGHT_ATTACK_REGISTRY", "0") == "1"


def redact_url(url: str) -> str:
    """Strip query parameters, fragment, AND userinfo from URL to avoid logging secrets."""
    if not url:
        return ""
    try:
        parsed = urlparse(url)
        # T13 (v1.8.0): drop userinfo (user:pass@) — urlunparse keeps netloc verbatim,
        # so a URL like https://user:pass@host/path would otherwise log credentials.
        netloc = parsed.hostname or parsed.netloc
        if parsed.port:
            netloc = f"{netloc}:{parsed.port}"
        clean = urlunparse((parsed.scheme, netloc, parsed.path, "", "", ""))
        return clean
    except Exception:
        return url


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=DEFAULT_PATH)
    ap.add_argument("--add", action="store_true", help="append a new attack record")
    ap.add_argument("--force-add", action="store_true", help="append even if not opted in")
    ap.add_argument("--channel")
    ap.add_argument("--source-url", default="")
    ap.add_argument("--attack-type")
    ap.add_argument("--severity")
    ap.add_argument("--detected-by", dest="detected_by")
    ap.add_argument("--action-taken", dest="action_taken")
    ap.add_argument("--outcome")
    ap.add_argument("--model-provider", dest="model_provider", default="")
    ap.add_argument("--notes", default="")
    ap.add_argument("--tail", type=int, default=0, help="print last N records")
    ap.add_argument("--stats", action="store_true", help="print count by attack_type")
    ap.add_argument("--cleanup", action="store_true", help="remove entries older than 30 days")
    ap.add_argument("--force", action="store_true", help="force cleanup even if not opted in")
    args = ap.parse_args()

    # Cleanup mode
    if args.cleanup:
        if not args.force and not is_opted_in():
            print("Registry not opted in (set KEELWRIGHT_ATTACK_REGISTRY=1). Use --force to override.", file=sys.stderr)
            return 0
        try:
            if not os.path.exists(args.path):
                print("no registry yet")
                return 0
            cutoff = datetime.datetime.now() - datetime.timedelta(days=RETENTION_DAYS)
            kept = 0
            removed = 0
            with open(args.path, encoding="utf-8") as f:
                lines = [l for l in f if l.strip()]
            with open(args.path, "w", encoding="utf-8") as f:
                for line in lines:
                    try:
                        r = json.loads(line)
                        ts_str = r.get("timestamp", "")
                        if ts_str:
                            ts = datetime.datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                            if ts >= cutoff:
                                f.write(line)
                                kept += 1
                            else:
                                removed += 1
                        else:
                            f.write(line)  # keep malformed entries
                            kept += 1
                    except Exception:
                        f.write(line)  # keep unparseable entries
                        kept += 1
            print(f"Cleanup: kept {kept}, removed {removed} (older than {RETENTION_DAYS} days)")
            return 0
        except Exception as e:
            print(f"Cleanup error: {e}", file=sys.stderr)
            return 0

    # Add mode
    if args.add or args.force_add:
        if not args.force_add and not is_opted_in():
            print("Registry not opted in (set KEELWRIGHT_ATTACK_REGISTRY=1). Use --force-add to override.", file=sys.stderr)
            return 0

        rec = {
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
            "channel": args.channel,
            "source_url": redact_url(args.source_url),
            "attack_type": args.attack_type,
            "severity": args.severity,
            "detected_by": args.detected_by,
            "action_taken": args.action_taken,
            "outcome": args.outcome,
            "model_provider": args.model_provider,
            "notes": args.notes,
        }
        missing = [k for k in REQUIRED_ADD if not rec.get(k)]
        if missing:
            print(f"FAIL: missing required fields: {', '.join(missing)}", file=sys.stderr)
            return 2
        os.makedirs(os.path.dirname(args.path), exist_ok=True)
        with open(args.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"LOGGED: {rec['attack_type']} from {rec['source_url'] or 'n/a'} "
              f"[{rec['severity']}] -> {rec['outcome']}")
        return 0

    # Stats mode
    if args.stats:
        counts = {}
        try:
            with open(args.path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    k = r.get("attack_type", "unknown")
                    counts[k] = counts.get(k, 0) + 1
        except FileNotFoundError:
            print("no registry yet")
            return 0
        for k, v in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"{v:>4}  {k}")
        return 0

    # Default: --tail or full read
    try:
        with open(args.path, encoding="utf-8") as f:
            lines = [l for l in f if l.strip()]
    except FileNotFoundError:
        print("no registry yet")
        return 0
    show = lines[-args.tail:] if args.tail else lines
    for l in show:
        print(l.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())