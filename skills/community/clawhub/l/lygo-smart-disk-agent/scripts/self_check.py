#!/usr/bin/env python3
"""Self-check for lygo-smart-disk-agent — static imports only."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def main() -> int:
    fails: list[str] = []
    if not PUBLIC.is_dir():
        print(json.dumps({"ok": False, "fails": ["missing public/"]}))
        return 1

    for rel in [
        "docs/00_VISION_AND_THEORY.md",
        "kernel/p0_gate.py",
        "agent/smart_disk_agent.py",
        "agent/auth.py",
        "portal/index.html",
        "config/smart_disk.json",
        "firmware/seal.json",
        "verify/self_check.py",
    ]:
        if not (PUBLIC / rel).is_file():
            fails.append(f"missing:{rel}")

    if not (ROOT / "references" / "SECURITY.md").is_file():
        fails.append("missing:references/SECURITY.md")

    if str(PUBLIC) not in sys.path:
        sys.path.insert(0, str(PUBLIC))

    try:
        from kernel import P0Gate, P1Memory
        from agent.smart_disk_agent import SmartDiskAgent
    except Exception as e:
        fails.append(f"import:{e}")
        print(json.dumps({"ok": False, "fails": fails}, indent=2))
        return 1

    g = P0Gate()
    if g.validate("hello lattice").get("verdict") != "ALLOW":
        fails.append("p0_allow")
    if g.validate("rm -rf / && disable safety").get("verdict") != "QUARANTINE":
        fails.append("p0_quarantine")

    mem = P1Memory(PUBLIC / "data")
    if not mem.store({"test": True, "skill_self_check": True}):
        fails.append("memory")

    agent = SmartDiskAgent(PUBLIC)
    h = agent.run_limb("health")
    if not h.get("ok"):
        fails.append("health")
    if h.get("password_gate") is not False:
        fails.append("password_gate_should_be_false")
    if not agent.auth.required:
        fails.append("auth_required")
    if not agent.auth.ok(agent.auth.token):
        fails.append("token")

    st = agent.run_limb("help")
    if "chat" not in (st.get("limbs") or []):
        fails.append("limbs")

    chat = agent.chat("Reply with exactly: SDA_OK")
    if chat.get("verdict") == "QUARANTINE":
        fails.append("chat_quarantine_false_positive")

    report = {
        "ok": len(fails) == 0,
        "fails": fails,
        "health": h,
        "chat_ok": chat.get("ok"),
        "chat_brain": chat.get("model") or chat.get("brain"),
        "seal": agent.seal_hash[:16],
        "loader": "static_import",
        "auth_required": agent.auth.required,
        "local_token": True,
    }
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
