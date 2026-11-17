#!/usr/bin/env python3
"""Build MASTER_ARCHIVE.md from living memory index (metadata only, no secret dump)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from audit_library import resolve_base, sha256_file  # type: ignore


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=None)
    ap.add_argument("-o", "--output", default=None, help="Default: <base>/LYRA_CORE/memory/MASTER_ARCHIVE.md")
    args = ap.parse_args()

    base = resolve_base(args.base)
    idx_path = Path(__file__).resolve().parents[1] / "references" / "core_files_index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    items = idx.get("items") or []

    lines = [
        "# LYGO Master Archive (Living Memory v1.2)",
        "",
        f"**Generated UTC:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"**Authority root:** `{base}`",
        "",
        "## Indexed continuity (Max20)",
        "",
        "| Path | Role | Size | SHA256 (files) |",
        "|------|------|------|----------------|",
    ]

    for it in items:
        rel = it.get("path", "")
        role = it.get("role", "")
        p = base / rel
        if not p.exists():
            lines.append(f"| `{rel}` | {role} | MISSING | — |")
            continue
        st = p.stat()
        if p.is_file():
            digest = sha256_file(p)[:16] + "…"
            lines.append(f"| `{rel}` | {role} | {st.st_size} | `{digest}` |")
        else:
            lines.append(f"| `{rel}` | {role} | dir | — |")

    lines.extend(
        [
            "",
            "## Axioms",
            "- Small index, measured drift, user-consent mint.",
            "- Pair with lyra-brain for session snips; verify lattice before claiming ALIGNED.",
            "",
            "## Next step",
            "Mint this file via lygo-mint-verifier when user approves.",
            "",
        ]
    )

    out = Path(args.output) if args.output else base / "LYRA_CORE" / "memory" / "MASTER_ARCHIVE.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print("WROTE", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())