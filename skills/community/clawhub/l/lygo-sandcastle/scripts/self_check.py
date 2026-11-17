#!/usr/bin/env python3
"""Self-check LYGO sandcastle (no Ollama/sandcastle required)."""

from __future__ import annotations

import sys
from pathlib import Path

STACK = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(STACK))

from lygo_sandcastle.gatekeeper import P0Gatekeeper  # noqa: E402
from lygo_sandcastle.harmony import P5HarmonyNode  # noqa: E402


def main() -> int:
    wf = STACK / "lygo_sandcastle" / "workflows" / "example_sovereign.yaml"
    if not wf.is_file():
        print("FAIL missing example workflow")
        return 1
    text = wf.read_text(encoding="utf-8")
    g = P0Gatekeeper()
    v = g.validate(text)
    assert v["verdict"] in ("AMPLIFY", "SOFTEN", "QUARANTINE")
    ident = P5HarmonyNode().create_node({"name": "self_check"})
    assert ident["light_code"].startswith("LF-Δ9-")
    print("OK lygo-sandcastle self_check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())