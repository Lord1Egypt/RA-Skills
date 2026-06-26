#!/usr/bin/env python3
"""Discover models from openclaw.json and build initial health state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib import (
    Registry,
    build_initial_state,
    read_openclaw_config,
    refresh_group_summaries,
    save_json,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Discover models and build health state.")
    p.add_argument("--openclaw-config", type=Path, default=None,
                   help="Path to openclaw.json (auto-searches ~/.openclaw/ if omitted)")
    p.add_argument("--write-state", type=Path, default=Path(".imperial_state.json"),
                   help="Write state to this file")
    p.add_argument("--summary", action="store_true", help="Print human-readable summary")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    reg = Registry(root)
    cfg = read_openclaw_config(args.openclaw_config)

    if not cfg:
        print("❌ Could not find openclaw.json")
        return 1

    state = build_initial_state(reg, cfg)
    refresh_group_summaries(state)
    save_json(args.write_state, state)

    models = state.get("models", {})
    providers = state.get("providers", {})

    print(f"✅ Discovered {len(models)} chat models from {len(providers)} providers")
    print(f"📄 State written to {args.write_state}")

    if args.summary:
        print("\n--- Models ---")
        for ref, data in sorted(models.items()):
            local = "🏠" if data.get("local") else "☁️"
            cost = data.get("cost_tier", "?")
            caps = ", ".join(data.get("capabilities", [])[:3])
            roles = ", ".join(data.get("roles", [])[:3])
            src = data.get("source", "?")
            print(f"  {local} {ref} [{cost}] caps=[{caps}] roles=[{roles}] ({src})")

        print("\n--- Providers ---")
        for prov, info in sorted(providers.items()):
            print(f"  {prov}: {info['healthy_models']} healthy / {len(info['models'])} total")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
