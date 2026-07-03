#!/usr/bin/env python3
"""Build + anchor ClawHub public catalog egg (metadata only)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import zlib
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SIGNATURE = "Δ9Φ963-CLAWHUB-CATALOG-EGG-v1"


def require_consent(flag: bool) -> None:
    if flag or os.environ.get("LYGO_EGG_PLANT_CONSENT", "").lower() in ("yes", "1", "true"):
        return
    raise SystemExit(2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-consent", action="store_true")
    ap.add_argument("--stack-root", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    require_consent(args.i_consent)

    stack = Path(args.stack_root).resolve()
    skills_path = stack / "clawhub" / "skills.json"
    if not skills_path.is_file():
        raise SystemExit(f"Missing {skills_path}")

    catalog = json.loads(skills_path.read_text(encoding="utf-8"))
    entries = []
    for sk in catalog.get("skills", []):
        if not sk.get("published", True):
            continue
        entries.append(
            {
                "slug": sk.get("slug"),
                "name": sk.get("name"),
                "version": sk.get("version"),
                "clawhub_url": sk.get("clawhub_url"),
                "summary": (sk.get("summary") or "")[:200],
            }
        )
    egg = {
        "signature": SIGNATURE,
        "egg_id": "clawhub-lattice-catalog",
        "built_utc": time.time(),
        "publisher": catalog.get("publisher"),
        "skill_count": len(entries),
        "install_template": catalog.get("install_template"),
        "skills": entries,
        "note": "Public ClawHub index only — install skills via clawhub; verify via kernel eggs.",
    }
    raw = json.dumps(egg, sort_keys=True, separators=(",", ":")).encode("utf-8")
    transport = zlib.compress(raw, level=9)
    build_dir = stack / "data" / "kernel_eggs" / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    (build_dir / "clawhub-lattice-catalog.json").write_text(json.dumps(egg, indent=2), encoding="utf-8")
    (build_dir / "clawhub-lattice-catalog.bin").write_bytes(transport)
    print(f"[clawhub] catalog egg {len(transport)} bytes, {len(entries)} skills")

    if args.dry_run:
        return 0

    sys.path.insert(0, str(stack / "tools"))
    from lygo_anchor import MultiAnchor  # noqa: E402
    from lygo_anchor_config import AnchorProfile  # noqa: E402

    multi = MultiAnchor(AnchorProfile.load(), stack)
    result = multi.anchor_bytes(transport, "kernel_egg_clawhub-lattice-catalog", description="CLAWHUB_CATALOG_EGG")
    print(f"[clawhub] anchored service={result.service} url={result.url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())