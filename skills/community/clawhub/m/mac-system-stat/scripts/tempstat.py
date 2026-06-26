#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from _common import json_dump, machine_meta
from _swift_helper import emit_failure, run_helper


PMSET = "/usr/bin/pmset"


THERM_PATTERNS = [
    (re.compile(r"No thermal warning level has been recorded", re.I), {"thermal_warning_recorded": False}),
    (re.compile(r"No performance warning level has been recorded", re.I), {"performance_warning_recorded": False}),
    (re.compile(r"No CPU power status has been recorded", re.I), {"cpu_power_status_recorded": False}),
]


def read_thermal_status() -> Dict[str, Any]:
    try:
        proc = subprocess.run([PMSET, "-g", "therm"], capture_output=True, text=True, timeout=10)
    except Exception as e:
        return {"available": False, "notes": [f"pmset therm failed: {e}"]}

    text = (proc.stdout or proc.stderr or "").strip()
    if proc.returncode != 0:
        return {"available": False, "notes": [text or f"pmset therm exited {proc.returncode}"]}

    status: Dict[str, Any] = {"available": bool(text), "raw": text, "notes": []}
    for pattern, patch in THERM_PATTERNS:
        if pattern.search(text):
            status.update(patch)

    if status.get("available") and status.get("thermal_warning_recorded") is False and status.get("performance_warning_recorded") is False:
        status["overall"] = "nominal"
    return status


def main() -> int:
    root = Path(__file__).resolve().parent
    try:
        data = run_helper(root, "tempstat", timeout=30)
        payload: Dict[str, Any] = {**machine_meta(), **data, "thermal_status": read_thermal_status()}
        json_dump(payload)
        return 0
    except Exception as e:
        return emit_failure(
            "tempstat",
            f"Swift AppleSMC temperature helper failed to build or run: {e}",
            [
                "Verify Command Line Tools / swiftc availability.",
                "If AppleSMC opens but temperature keys change on future SoCs, re-probe and refresh the candidate key list.",
            ],
        )


if __name__ == "__main__":
    raise SystemExit(main())
