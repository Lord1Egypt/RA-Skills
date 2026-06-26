#!/usr/bin/env python3
"""Read-only nchat diagnostics with privacy-preserving output."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


SENSITIVE_KEY_RE = re.compile(r"(pass|password|secret|token|local_key|api.*hash|hash|key)$", re.I)
PHONE_RE = re.compile(r"\+\d[\d .()_-]{4,}\d")

CONFIG_FILES = (
    "app.conf",
    "ui.conf",
    "key.conf",
    "color.conf",
    "usercolor.conf",
)

PROFILE_CONFIGS = (
    "telegram.conf",
    "whatsappmd.conf",
    "signal.conf",
)


def mask_phone_text(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(0)
        digits = re.sub(r"\D", "", raw)
        if len(digits) <= 4:
            return "+***"
        return "+***" + digits[-2:]

    return PHONE_RE.sub(repl, text)


def redact_value(key: str, value: str) -> str:
    if SENSITIVE_KEY_RE.search(key):
        return "[redacted]"
    if key.lower() in {"proxy_user"} and value:
        return "[redacted-user]"
    return mask_phone_text(value)


def run_command(args: list[str], timeout: int = 5) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            args,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
        return {"ok": proc.returncode == 0, "code": proc.returncode, "output": proc.stdout.strip()}
    except FileNotFoundError:
        return {"ok": False, "code": None, "output": "not found"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "code": None, "output": "timeout"}


def permission_summary(path: Path) -> dict[str, Any]:
    try:
        st = path.lstat()
    except FileNotFoundError:
        return {"exists": False}

    mode = stat.S_IMODE(st.st_mode)
    warnings = []
    if mode & 0o077:
        warnings.append("group/other permissions are open")
    if path.is_symlink():
        warnings.append("path is a symlink")
    return {
        "exists": True,
        "mode": oct(mode),
        "is_dir": path.is_dir(),
        "is_file": path.is_file(),
        "is_symlink": path.is_symlink(),
        "warnings": warnings,
    }


def parse_config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file() or path.is_symlink():
        return values
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, value = stripped.split("=", 1)
                values[key] = redact_value(key, value)
    except OSError as exc:
        values["__error__"] = str(exc)
    return values


def collect_profiles(confdir: Path, include_config: bool) -> list[dict[str, Any]]:
    profiles_dir = confdir / "profiles"
    if not profiles_dir.is_dir():
        return []

    profiles: list[dict[str, Any]] = []
    for profile in sorted(p for p in profiles_dir.iterdir() if p.is_dir()):
        item: dict[str, Any] = {
            "name": mask_phone_text(profile.name),
            "path": mask_phone_text(str(profile)),
            "permissions": permission_summary(profile),
            "config_files": {},
        }
        for cfg in PROFILE_CONFIGS:
            cfg_path = profile / cfg
            if cfg_path.exists() or include_config:
                cfg_item: dict[str, Any] = {"permissions": permission_summary(cfg_path)}
                if include_config:
                    cfg_item["values"] = parse_config(cfg_path)
                item["config_files"][cfg] = cfg_item
        profiles.append(item)
    return profiles


def collect_config(confdir: Path, include_config: bool) -> dict[str, Any]:
    configs: dict[str, Any] = {}
    for cfg in CONFIG_FILES:
        path = confdir / cfg
        item: dict[str, Any] = {"permissions": permission_summary(path)}
        if include_config:
            item["values"] = parse_config(path)
        configs[cfg] = item
    return configs


def running_nchat() -> dict[str, Any]:
    pgrep = shutil.which("pgrep")
    if not pgrep:
        return {"checked": False, "reason": "pgrep not available"}
    result = run_command([pgrep, "-x", "nchat"])
    if result["ok"] and result["output"]:
        pids = [p for p in result["output"].splitlines() if p.strip()]
        return {"checked": True, "running": True, "count": len(pids), "pids": pids}
    return {"checked": True, "running": False, "count": 0, "pids": []}


def collect(args: argparse.Namespace) -> dict[str, Any]:
    confdir = Path(args.confdir).expanduser()
    nchat_path = shutil.which("nchat")
    version = run_command([nchat_path, "--version"]) if nchat_path else {"ok": False, "output": "not found"}

    return {
        "nchat": {
            "binary": nchat_path,
            "version": version["output"].splitlines()[0] if version["output"] else version["output"],
            "version_ok": version["ok"],
        },
        "confdir": {
            "path": mask_phone_text(str(confdir)),
            "permissions": permission_summary(confdir),
        },
        "running": running_nchat(),
        "configs": collect_config(confdir, args.include_config),
        "profiles": collect_profiles(confdir, args.include_config),
        "notes": [
            "This script does not read message cache, exports, attachments, logs, cookies, or browser data.",
            "Phone-like values and sensitive config keys are redacted.",
        ],
    }


def emit_text(report: dict[str, Any]) -> None:
    print("nchat doctor")
    print(f"binary: {report['nchat']['binary'] or 'not found'}")
    print(f"version: {report['nchat']['version'] or 'unknown'}")
    print(f"confdir: {report['confdir']['path']}")
    print(f"confdir permissions: {report['confdir']['permissions']}")
    print(f"running: {report['running']}")

    print("\nconfig files:")
    for name, item in report["configs"].items():
        print(f"- {name}: {item['permissions']}")
        values = item.get("values")
        if values:
            for key, value in values.items():
                print(f"    {key}={value}")

    print("\nprofiles:")
    if not report["profiles"]:
        print("- none found")
    for profile in report["profiles"]:
        print(f"- {profile['name']}: {profile['permissions']}")
        for cfg_name, cfg_item in profile["config_files"].items():
            print(f"    {cfg_name}: {cfg_item['permissions']}")
            values = cfg_item.get("values")
            if values:
                for key, value in values.items():
                    print(f"        {key}={value}")

    print("\nnotes:")
    for note in report["notes"]:
        print(f"- {note}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Read-only nchat diagnostic report.")
    parser.add_argument("--confdir", default="~/.config/nchat", help="nchat config directory")
    parser.add_argument(
        "--include-config",
        action="store_true",
        help="include redacted key=value config contents; never reads cache/history/log files",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = parser.parse_args(argv)

    report = collect(args)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        emit_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
