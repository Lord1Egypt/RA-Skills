#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    script_dir = Path(__file__).resolve().parent
    result = {
        "python_ok": sys.version_info >= (3, 9),
        "swift_ok": shutil.which("swift") is not None,
        "calendar_access_ok": False,
        "writable_calendars": 0,
        "errors": [],
    }

    if not result["python_ok"]:
        result["errors"].append("Python 3.9+ required")
    if not result["swift_ok"]:
        result["errors"].append("Swift not found (install Xcode Command Line Tools)")

    if result["swift_ok"]:
        p = run(["swift", str(script_dir / "list_calendars.swift")])
        if p.returncode != 0:
            result["errors"].append("Failed to list calendars (check Calendar permission)")
        else:
            try:
                data = json.loads(p.stdout)
                cals = data.get("calendars", [])
                writable = [c for c in cals if c.get("writable")]
                result["writable_calendars"] = len(writable)
                result["calendar_access_ok"] = len(cals) > 0
                if len(writable) == 0:
                    result["errors"].append("No writable calendars found")
            except Exception:
                result["errors"].append("Invalid JSON from list_calendars.swift")

    result["ok"] = result["python_ok"] and result["swift_ok"] and result["calendar_access_ok"] and result["writable_calendars"] > 0
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
