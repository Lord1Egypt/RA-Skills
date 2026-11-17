#!/usr/bin/env python3
import sys
from pathlib import Path

STACK = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(STACK))

from lygo_openclaw.gatekeeper import P0Gatekeeper
from lygo_openclaw.harmony import P5HarmonyNode
from lygo_openclaw.limbs import dispatch


def main() -> int:
    g = P0Gatekeeper()
    v = g.validate("help")
    assert v["verdict"] in ("AMPLIFY", "SOFTEN", "QUARANTINE")
    ident = P5HarmonyNode().create_node("self_check", [])
    assert ident["light_code"].startswith("LF-")
    out = dispatch("help")
    assert "limbs" in out
    print("OK lygo-openclaw self_check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
