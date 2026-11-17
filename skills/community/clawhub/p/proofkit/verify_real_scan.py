#!/usr/bin/env python3
"""verify_real_scan.py — static fake-success / dry-run scanner for a target file.

Backs /verify-real: before trusting a "it works" claim, scan the code for the
markers that let something REPORT success without a real side effect. This is a
STATIC pre-filter — a clean scan does NOT prove the thing runs; /verify-real
still demands a live-execution artifact. A dirty scan is a real red flag.

Usage: python3 scripts/verify_real_scan.py <file> [<file> ...]
"""
from __future__ import annotations
import re, sys, json
from pathlib import Path

# (regex, tag, why-it-matters). Ordered most-damning first.
PATTERNS = [
    (r"\breturn\s+True\b(?![^\n]*#\s*real)", "returns_true_literal", "may report success unconditionally"),
    (r'(?<![\w])["\']?(success|succeeded|placed|sent|posted|delivered)["\']?\s*[:=]\s*True\b',
     "success_true_literal", "hardcoded success flag"),
    (r"\bmessage_id\b\s*[:=]\s*0\b", "message_id_zero", "fake Telegram delivery (msgid 0 = not sent)"),
    (r"\brandom\.(random|randint|choice|uniform|gauss)\b", "random_simulator", "fabricated/random result"),
    (r"\b(TODO|FIXME|NotImplementedError|raise NotImplementedError)\b", "stub_todo", "unimplemented path"),
    (r"^\s*(pass|\.\.\.)\s*$", "empty_body", "empty/placeholder body"),
    (r"\b(demo|sample|example|fixture|dummy|mock|stub|placeholder)[_\-]?(data|key|token|result|row)?\b",
     "demo_sample_data", "sample/demo data may masquerade as live"),
    (r"except[^:]*:\s*(pass|return\s+True|return\s+\{[^}]*success)", "swallow_then_success",
     "swallows error then reports success"),
    (r"--dry-run|dry_run\s*=\s*True|DRY[_ ]RUN", "dry_run_default", "dry-run path — confirm the LIVE path ran"),
    (r"\bhardcoded|HARDCODED\b|mover_list\s*=\s*\[", "hardcoded_list", "hardcoded values used as if computed"),
]


def scan(path: Path) -> dict:
    try:
        text = path.read_text(errors="ignore")
    except Exception as e:
        return {"file": str(path), "error": str(e)}
    lines = text.splitlines()
    hits = []
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("#") or s.startswith("//"):
            continue
        for rx, tag, why in PATTERNS:
            if re.search(rx, line):
                hits.append({"line": i, "tag": tag, "why": why, "code": s[:100]})
    # de-dupe by tag for the headline, keep all for detail
    tags = sorted({h["tag"] for h in hits})
    return {"file": str(path), "flags": len(hits), "tags": tags, "hits": hits[:40]}


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: verify_real_scan.py <file> [<file> ...]", file=sys.stderr)
        return 2
    results = [scan(Path(p)) for p in sys.argv[1:]]
    for r in results:
        if r.get("error"):
            print(f"\n{r['file']}: ERROR {r['error']}"); continue
        verdict = "CLEAN (static)" if r["flags"] == 0 else f"{r['flags']} FAKE-SUCCESS FLAGS"
        print(f"\n{r['file']} — {verdict}")
        if r["tags"]:
            print("  tags:", ", ".join(r["tags"]))
        for h in r["hits"]:
            print(f"    L{h['line']:<5} [{h['tag']}] {h['code']}")
    print("\nNOTE: a clean STATIC scan does NOT prove it runs — /verify-real must still capture a "
          "LIVE-execution artifact (real output, real msgid, real file, real DB row).")
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
