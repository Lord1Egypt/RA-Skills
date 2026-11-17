#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import lygo_lora as t  # noqa: E402


def main() -> int:
    src = (HERE / "lygo_lora.py").read_text(encoding="utf-8")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    no_sub = not re.search(r"(?m)^\s*import\s+subprocess\b", src)
    no_net = "urllib" not in src and "requests" not in src and "http.client" not in src
    no_serial = not re.search(r"(?m)^\s*(import|from)\s+serial\b", src) and "pyserial" not in src
    pulse = t.encode_pulse(t.DEMO_NODE, t.DEMO_DIGEST, "A", 0)
    back = t.decode_pulse(pulse)
    demo_badge = json.loads((ROOT / "examples" / "demo_badge.json").read_text(encoding="utf-8"))
    from_badge = t.pulse_from_badge(demo_badge)
    shadow = t.probe(None)
    fork = t.compare(t.DEMO_DIGEST, t.decode_pulse(t.encode_pulse("PEER", "0" * 64, "A", 1)))
    m = t.map_payload()
    ok = (
        no_sub
        and no_net
        and no_serial
        and t.VERSION == "1.0.0"
        and t.SIG == "Delta9Phi963-LYGO-LORA-MESH-v1.0.0"
        and "version: 1.0.0" in skill
        and back.get("ok") is True
        and back.get("roots_digest") == t.DEMO_DIGEST
        and len(pulse.encode("ascii")) <= t.MAX_PAYLOAD
        and t.MAX_PAYLOAD <= 237
        and from_badge.startswith("LY1/")
        and shadow.get("yield") == "NAMED_SHADOW"
        and fork.get("verdict") == "FORK_VISIBLE"
        and m["live_star_chart_ingest"] is False
        and m["class"] == "RESOURCE"
        and "egg payloads on RF" in m["forbidden"]
        and t.plain().startswith("LYGO LoRa mesh")
    )
    print(
        json.dumps(
            {
                "ok": ok,
                "signature": t.SIG,
                "version": t.VERSION,
                "no_subprocess": no_sub,
                "no_network_imports": no_net,
                "no_serial_driver": no_serial,
                "pulse": pulse,
                "bytes": len(pulse.encode("ascii")),
                "roundtrip": back.get("ok"),
                "no_board": shadow.get("yield"),
                "fork_demo": fork.get("verdict"),
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
