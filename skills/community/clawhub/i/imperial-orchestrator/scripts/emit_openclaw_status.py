#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib import load_json


def parse_args():
    p = argparse.ArgumentParser(description="Emit compact status for wrappers or shell scripts.")
    p.add_argument("--state-file", type=Path, default=Path(".imperial_state.json"))
    return p.parse_args()


def main() -> int:
    state = load_json(parse_args().state_file)
    summary = {
        "models": {
            ref: {
                "provider": data.get("provider"),
                "auth_group": data.get("auth_group"),
                "status": data.get("health", {}).get("status", "unknown"),
                "cooldown_until": data.get("health", {}).get("cooldown_until"),
            }
            for ref, data in state.get("models", {}).items()
        },
        "providers": state.get("providers", {}),
        "auth_groups": state.get("auth_groups", {}),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
