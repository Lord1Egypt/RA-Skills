#!/usr/bin/env python3
"""ClawHub mirror — delegate to stack joy_loop_planter."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _stack_paths import stack_root  # noqa: E402

import os

ROOT = stack_root()
if os.environ.get("LYGO_JOY_PLANT_CONSENT") != "yes":
    print(
        "Refusing plant: human consent required. "
        "After the user agrees, run with LYGO_JOY_PLANT_CONSENT=yes "
        "or call stack tools/joy_loop_planter.py --i-consent directly.",
        file=sys.stderr,
    )
    raise SystemExit(2)
cmd = [sys.executable, str(ROOT / "tools" / "joy_loop_planter.py"), "--i-consent"]
raise SystemExit(subprocess.call(cmd, cwd=ROOT))