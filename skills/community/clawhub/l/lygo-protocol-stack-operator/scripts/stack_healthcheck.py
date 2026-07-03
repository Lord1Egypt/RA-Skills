#!/usr/bin/env python3
"""Local health check for LYGO stack checkout (no network)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def find_stack_root() -> Path | None:
    env = os.environ.get("LYGO_STACK_ROOT")
    if env:
        p = Path(env)
        if (p / "stack" / "lygo_stack.py").is_file():
            return p
    candidates = [
        SKILL_ROOT.parent.parent / "lygo-protocol-stack",
        Path.home() / "lygo-protocol-stack",
        Path.cwd() / "lygo-protocol-stack",
    ]
    for c in candidates:
        if (c / "stack" / "lygo_stack.py").is_file():
            return c
    return None


def main() -> int:
    root = find_stack_root()
    print("LYGO Protocol Stack — local healthcheck")
    print("=" * 50)
    if not root:
        print("STACK: not found (set LYGO_STACK_ROOT or clone GitHub repo)")
        print("  https://github.com/DeepSeekOracle/lygo-protocol-stack")
        return 1
    print(f"STACK: {root}")
    checks = [
        ("P0 demo", [sys.executable, str(root / "tools" / "run_p0_demo.py"), "--quiet", "--id", "json_minimal"]),
        ("Stack demo", [sys.executable, str(root / "tools" / "run_full_stack_demo.py")]),
    ]
    ok = 0
    for name, cmd in checks:
        if not cmd[1] or not Path(cmd[1]).is_file():
            print(f"  SKIP {name} (script missing)")
            continue
        r = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=120)
        status = "OK" if r.returncode == 0 else f"FAIL({r.returncode})"
        print(f"  {name}: {status}")
        if r.returncode == 0:
            ok += 1
    gate = SKILL_ROOT / "scripts" / "lygo_p0_gate.py"
    if gate.is_file():
        r = subprocess.run([sys.executable, str(gate), str(SKILL_ROOT / "SKILL.md")], capture_output=True)
        print(f"  P0 gate SKILL.md: {'OK' if r.returncode == 0 else 'SOFTEN/QUARANTINE'}")
    print(f"Done ({ok} stack checks). HF dataset: https://huggingface.co/datasets/DeepSeekOracle/lygo-protocol-stack")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())