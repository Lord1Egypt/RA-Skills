#!/usr/bin/env python3
"""
External sync PLAN (dry-run by default). Lists free-server / internet surfaces and required human steps.

With --i-consent --execute-local-only: refreshes sovereign snapshot under docs/ (no git push, no HF).
Never auto-publishes to the public internet.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SIG = "Delta9Phi963-EXTERNAL-LATTICE-ANCHOR-v1.1"


def stack_root() -> Path:
    env = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "docs" / "network_builder" / "IMMUTABLE_ANCHORS.json").is_file():
            return p
    return Path.cwd()


def consent(ok: bool) -> bool:
    if ok:
        return True
    return os.environ.get("LYGO_EXTERNAL_SYNC_CONSENT", "").lower() in ("1", "yes", "true")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-consent", action="store_true")
    ap.add_argument("--execute-local-only", action="store_true", help="Copy sovereign seeds → docs snapshot only")
    ap.add_argument("--stack-root", default="")
    args = ap.parse_args()
    stack = Path(args.stack_root).resolve() if args.stack_root else stack_root()

    plan = {
        "signature": SIG,
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": "EXECUTE_LOCAL_ONLY" if args.execute_local_only else "DRY_PLAN",
        "user_protection": {
            "external_mirrors_are_not_authority": True,
            "local_A_B_verify_first": True,
            "human_must_push_git": True,
            "human_must_upload_hf": True,
            "star_chart_ingest_requires_consent": True,
        },
        "steps": [
            {
                "id": 1,
                "action": "verify_local_layers",
                "cmd": "python tools/verify_all_kernel_layers.py --json",
                "auto": True,
            },
            {
                "id": 2,
                "action": "build_public_verify_manifest",
                "cmd": "python docs/skills/lygo-external-lattice-anchor/scripts/build_public_verify_manifest.py",
                "auto": True,
            },
            {
                "id": 3,
                "action": "map_eggs_to_star_chart",
                "cmd": "python docs/skills/lygo-external-lattice-anchor/scripts/map_eggs_to_star_chart.py",
                "auto": True,
            },
            {
                "id": 4,
                "action": "snapshot_sovereign_to_docs",
                "cmd": "sync_external_plan.py --i-consent --execute-local-only",
                "auto": False,
                "consent": True,
            },
            {
                "id": 5,
                "action": "classic_plant_surfaces",
                "skill": "lygo-kernel-egg-planter",
                "cmd": "python scripts/plant_with_consent.py --i-consent --surfaces local,registry,pages,turbo",
                "auto": False,
                "consent": True,
                "note": "Free/public: pages JSON after git push; turbo Arweave ≤100KiB",
            },
            {
                "id": 6,
                "action": "git_push_pages",
                "cmd": "git push origin main  # human only",
                "auto": False,
                "publishes": ["github_pages", "raw_github"],
            },
            {
                "id": 7,
                "action": "hf_dataset_push",
                "cmd": "python tools/hf_push_dataset.py  # maintainer + user ask",
                "auto": False,
                "publishes": ["huggingface"],
            },
            {
                "id": 8,
                "action": "public_http_verify",
                "cmd": "python docs/skills/lygo-external-lattice-anchor/scripts/verify_public_anchors.py",
                "auto": True,
                "network": True,
            },
            {
                "id": 9,
                "action": "star_chart_steward_ingest",
                "skill": "lygo-haven-star-chart",
                "input": "docs/star_chart_egg_map_proposals.json",
                "auto": False,
                "consent": True,
                "grows_world_map": True,
            },
        ],
        "free_internet_surfaces": [
            "GitHub Pages (deepseekoracle.github.io/lygo-protocol-stack)",
            "GitHub raw IMMUTABLE_ANCHORS + sovereign snapshot",
            "Hugging Face datasets (stack + music stream)",
            "Arweave Turbo (optional small anchors)",
            "ClawHub skill registry (metadata)",
            "Haven Star Chart live HTML",
            "Eternalhaven.ca / asiancoastline.com hubs",
        ],
    }

    print(json.dumps(plan, indent=2))

    if args.execute_local_only:
        if not consent(args.i_consent):
            print("CONSENT_REQUIRED for --execute-local-only", file=sys.stderr)
            return 2
        src = stack / "data" / "sovereign_seeds"
        dst = stack / "docs" / "sovereign_seeds_snapshot"
        if not (src / "registry.json").is_file():
            print("No local sovereign registry to snapshot", file=sys.stderr)
            return 1
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / "registry.json", dst / "registry.json")
        eggs = src / "eggs"
        if eggs.is_dir():
            for f in eggs.glob("*.egg.json"):
                shutil.copy2(f, dst / f.name)
        print(json.dumps({"status": "SNAPSHOT_OK", "dst": str(dst)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
