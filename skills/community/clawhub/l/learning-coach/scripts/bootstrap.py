#!/usr/bin/env python3
"""Check/install optional dependencies for learning-coach skill."""

from __future__ import annotations
import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass, asdict


@dataclass
class Check:
    name: str
    required: bool
    found: bool
    hint: str


def has_bin(name: str) -> bool:
    return shutil.which(name) is not None


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def maybe_install_clawhub() -> tuple[bool, str]:
    if has_bin("clawhub"):
        return True, "already installed"
    if not has_bin("npm"):
        return False, "npm not found"
    code, out = run(["npm", "i", "-g", "clawhub"])
    return code == 0, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--install", action="store_true", help="Attempt installation for missing optional deps")
    ap.add_argument("--json", action="store_true", help="Output JSON only")
    args = ap.parse_args()

    checks = [
        Check("python3", True, has_bin("python3"), "Install Python 3"),
        Check("crontab", True, has_bin("crontab"), "Install cron/cronie package"),
        Check("clawhub", False, has_bin("clawhub"), "npm i -g clawhub"),
        Check("jq", False, has_bin("jq"), "Install jq for easier JSON debugging"),
    ]

    install_results: dict[str, str] = {}
    if args.install:
        for c in checks:
            if c.name == "clawhub" and not c.found:
                ok, msg = maybe_install_clawhub()
                c.found = ok or has_bin("clawhub")
                install_results[c.name] = msg

    payload = {
        "checks": [asdict(c) for c in checks],
        "ok": all(c.found for c in checks if c.required),
        "install_results": install_results,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return 0 if payload["ok"] else 1

    print("Dependency check:")
    for c in checks:
        status = "OK" if c.found else "MISSING"
        req = "required" if c.required else "optional"
        print(f"- {c.name}: {status} ({req})")
        if not c.found:
            print(f"  hint: {c.hint}")
    if install_results:
        print("\nInstall attempts:")
        for k, v in install_results.items():
            print(f"- {k}: {v}")

    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
