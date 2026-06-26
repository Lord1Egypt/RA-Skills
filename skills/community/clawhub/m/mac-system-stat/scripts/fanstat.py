#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from _common import json_dump, machine_meta
from _swift_helper import emit_failure, run_helper


def main() -> int:
    root = Path(__file__).resolve().parent
    try:
        data = run_helper(root, "fanstat", timeout=30)
        json_dump({**machine_meta(), **data})
        return 0
    except Exception as e:
        return emit_failure(
            "fanstat",
            f"Swift AppleSMC helper failed to build or run: {e}",
            [
                "Verify Command Line Tools / swiftc availability.",
                "If AppleSMC opens but key layout changes on future SoCs, re-check the F* key set.",
            ],
        )


if __name__ == "__main__":
    raise SystemExit(main())
