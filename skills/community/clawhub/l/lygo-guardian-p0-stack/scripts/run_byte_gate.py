#!/usr/bin/env python3
"""Portable P0 gate: bundled Guardian text API, or canonical stack byte gate if LYGO_STACK_ROOT set."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from guardian.integration_api import validate_decision  # noqa: E402


def stack_gate(path: Path) -> int:
    stack = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if not stack:
        return -1
    gate = Path(stack) / ".grok" / "skills" / "lygo-protocol-stack-operator" / "scripts" / "lygo_p0_gate.py"
    if not gate.is_file():
        gate = Path(stack) / "clawhub" / "mirrors" / "lygo-protocol-stack-operator" / "scripts" / "lygo_p0_gate.py"
    if not gate.is_file():
        return -1
    return subprocess.call([sys.executable, str(gate), str(path)])


def text_gate(content: str) -> dict:
    return validate_decision(
        {"channel": "cli", "task": "validate", "risk_tolerance": "low"},
        {"content": content},
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: run_byte_gate.py <file> | --text '...'", file=sys.stderr)
        return 1
    if sys.argv[1] == "--text":
        v = text_gate(" ".join(sys.argv[2:]))
        print(v)
        return 0 if v.get("action") == "allow" else 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print("not a file", file=sys.stderr)
        return 1
    rc = stack_gate(path)
    if rc >= 0:
        return rc
    data = path.read_bytes()[:8192]
    try:
        text = data.decode("utf-8", errors="replace")
    except Exception:
        text = repr(data[:200])
    v = text_gate(text)
    print(v)
    return 0 if v.get("action") == "allow" else 2


if __name__ == "__main__":
    raise SystemExit(main())