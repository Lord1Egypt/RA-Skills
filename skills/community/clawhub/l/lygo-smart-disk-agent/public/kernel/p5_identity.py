"""P5 action identity — light code per action."""
from __future__ import annotations

import hashlib
import time
from typing import Any


class P5Identity:
    def create_node(self, command: str, args: list[str] | None = None) -> dict[str, Any]:
        args = args or []
        raw = f"{time.time():.6f}|{command}|{' '.join(args)}"
        light = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
        # ethical mass heuristic: shorter commands slightly higher mass
        mass = max(0.1, min(1.0, 1.0 - len(command) / 500.0))
        return {
            "light_code": light,
            "ethical_mass": round(mass, 3),
            "command": command,
            "signature": "Δ9Φ963-SDA-P5-v1",
        }
