#!/usr/bin/env python3
"""iq-core: high-level reasoning scaffold + evidence-rank logger.

Usage:
    python3 reasoning_log.py decompose "bug" "sub1" "sub2"
    python3 reasoning_log.py evidence "direct data" "assumption"
    python3 reasoning_log.py critique "simpler solution exists? no invented data?"

Operationalizes iq-core: deep understanding, problem decomposition, multi-path
reasoning, evidence ranking, contradiction/adversarial check, self-critic, and
anti-hallucination. Pure local helper; writes a JSONL notebook next to the
script (set IQ_CORE_LOG_PATH to override). No secrets, no network.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iq_core_log.jsonl")

EVIDENCE_ORDER = [
    "direct data", "measured evidence", "trusted source", "context",
    "knowledge", "inference", "assumption",
]


def _now():
    return datetime.now(timezone.utc).isoformat()


def log_entry(kind, payload, log_path):
    record = {"ts": _now(), "skill": "iq-core", "kind": kind, "payload": payload}
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as e:
        print(f"[iq-core] WARNING could not write log: {e}", file=sys.stderr)
    return record


def cmd_decompose(args):
    parts = [s.strip() for s in args.parts]
    rec = log_entry("decompose", {"problem": args.problem, "subproblems": parts}, args.log)
    print(f"[decompose] {args.problem}")
    for i, p in enumerate(parts, 1):
        print(f"  {i}. {p}")


def cmd_evidence(args):
    items = [s.strip() for s in args.items]
    ranked = sorted(items, key=lambda x: EVIDENCE_ORDER.index(x.lower()) if x.lower() in EVIDENCE_ORDER else 99)
    rec = log_entry("evidence", {"items": ranked}, args.log)
    print("[evidence ranking] (high -> low certainty)")
    for it in ranked:
        print(f"  - {it}")


def cmd_critique(args):
    items = [s.strip() for s in args.items.split(";") if s.strip()]
    flags = []
    for it in items:
        low = it.lower()
        bad = any(w in low for w in ["no ", "not ", "invent", "fabricat", "fail", "missing", "assumption"])
        flags.append({"critique": it, "ok": not bad})
    rec = log_entry("critique", {"items": flags}, args.log)
    problems = [f for f in flags if not f["ok"]]
    verdict = "CLEAN" if not problems else f"NEEDS WORK ({len(problems)} issue(s))"
    print(f"[self-critic] {verdict}")
    for f in flags:
        print(f"  {'OK ' if f['ok'] else 'XX '}{f['critique']}")
    return 1 if problems else 0


def main(argv=None):
    p = argparse.ArgumentParser(description="iq-core reasoning scaffold")
    p.add_argument("--log", default=os.environ.get("IQ_CORE_LOG_PATH", DEFAULT_LOG))
    sub = p.add_subparsers(dest="cmd", required=True)

    pd = sub.add_parser("decompose")
    pd.add_argument("--problem", required=True)
    pd.add_argument("parts", nargs="+", help="subproblems")
    pd.set_defaults(func=cmd_decompose)

    pe = sub.add_parser("evidence")
    pe.add_argument("items", nargs="+", help="evidence items (ranked by certainty keyword)")
    pe.set_defaults(func=cmd_evidence)

    pc = sub.add_parser("critique")
    pc.add_argument("--items", required=True, help="checks separated by ;")
    pc.set_defaults(func=cmd_critique)

    args = p.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
