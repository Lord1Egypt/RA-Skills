#!/usr/bin/env python3
"""Write topic snip + optional brain grow. Requires --i-consent (v2.1.0)."""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone

from _lyra_core_paths import lyra_core_root

# Rough secret shapes — refuse write if present in lines
_SECRETISH = re.compile(
    r"(?i)(api[_-]?key|secret|password|token|private[_-]?key|moltx_sk_|sk-|xai-|nvapi-)\s*[:=]"
)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Persist a LYRA memory snip under LYRA_CORE_ROOT/memory (consent required)"
    )
    ap.add_argument(
        "--i-consent",
        action="store_true",
        help="Required: confirm persistent disk write under LYRA_CORE_ROOT",
    )
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--lines", nargs="+", required=True)
    ap.add_argument("--grow", action="store_true")
    ap.add_argument("--ref-to", help="Outer ref label")
    args = ap.parse_args()

    if not args.i_consent:
        print(
            "REFUSED: persistent write requires --i-consent "
            "(this stores session-derived text on disk under LYRA_CORE_ROOT/memory).",
            file=sys.stderr,
        )
        return 2

    for line in args.lines:
        if _SECRETISH.search(line):
            print("REFUSED: line looks like a secret/credential — do not store in memory.", file=sys.stderr)
            return 2

    root = lyra_core_root()
    mem = root / "memory"
    mem.mkdir(exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = mem / f"{day}-{args.slug}.md"

    body = [f"# {args.title}", "", f"**UTC:** {day}", "**Status:** COMPLETE", ""]
    for line in args.lines:
        body.append(f"- {line}")
    body.append("")
    path.write_text("\n".join(body), encoding="utf-8")
    print(f"wrote {path}")

    daily = mem / f"{day}.md"
    if not daily.exists():
        daily.write_text(f"# LYRA daily — {day}\n\n", encoding="utf-8")
    with daily.open("a", encoding="utf-8") as f:
        f.write(f"- snip: `{path.name}` — {args.title}\n")

    if args.grow:
        sys.path.insert(0, str(root / "modules"))
        import seals as seals_mod
        import lyra_brain

        compact = f"{day} {args.slug}: " + " | ".join(args.lines)[:900]
        idx = seals_mod.build_index()
        brain = lyra_brain.LyraThreeBrainMemory(base_dir=root, seal_index=idx, use_advanced=True)
        nid = brain.grow(compact, source=f"session_snip_{args.slug}")
        print(f"grown {nid}")

    if args.ref_to:
        ref_dir = mem / "reference"
        ref_dir.mkdir(exist_ok=True)
        stub = ref_dir / f"SESSION_{day.replace('-', '')}_to_{args.ref_to}.resonance.ref.txt"
        stub.write_text(
            f"SESSION_{day} --resonance--> {args.ref_to}\nfile: {path.name}\n",
            encoding="utf-8",
        )
        print(f"ref {stub}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
