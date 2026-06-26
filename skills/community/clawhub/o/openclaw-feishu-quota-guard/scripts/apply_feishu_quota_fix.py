#!/usr/bin/env python3
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


def run(cmd: Sequence[str]) -> str:
    try:
        out = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return out.stdout.strip()
    except Exception:
        return ""


def detect_config(explicit: Optional[str]) -> Optional[Path]:
    if explicit:
        path = Path(explicit).expanduser()
        return path if path.is_file() else None

    env_path = os.environ.get("OPENCLAW_CONFIG_PATH")
    if env_path:
        path = Path(env_path).expanduser()
        if path.is_file():
            return path

    cli_path = run(["openclaw", "config", "file"])
    if cli_path:
        cli_path = cli_path.replace("~", str(Path.home()), 1)
        path = Path(cli_path).expanduser()
        if path.is_file():
            return path

    candidates = [Path.home() / ".openclaw" / "openclaw.json"]
    state_dir = os.environ.get("OPENCLAW_STATE_DIR")
    if state_dir:
        candidates.append(Path(state_dir).expanduser() / "openclaw.json")

    candidates.extend(
        [
            Path.cwd() / "state" / "openclaw.json",
            Path.cwd().parent / "state" / "openclaw.json",
        ]
    )
    for path in candidates:
        if path.is_file():
            return path
    return None


def detect_workspace(config_path: Path, explicit: Optional[str]) -> Optional[Path]:
    if explicit:
        path = Path(explicit).expanduser()
        return path if path.is_dir() else None

    cwd = Path.cwd()
    if (cwd / "AGENTS.md").is_file():
        return cwd

    if config_path.parent.name == ".openclaw":
        candidate = config_path.parent / "workspace"
        if candidate.is_dir():
            return candidate

    if config_path.parent.name == "state":
        candidate = config_path.parent.parent / "workspace"
        if candidate.is_dir():
            return candidate

    for path in [cwd, cwd.parent, cwd.parent.parent]:
        if (path / "AGENTS.md").is_file():
            return path
    return None


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def backup_file(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = Path(f"{path}.bak.feishu-quota-guard.{ts}")
    shutil.copy2(path, backup)
    return backup


def nested_setdefault(obj: Dict[str, Any], keys: List[str], default: Dict[str, Any]) -> Dict[str, Any]:
    cur = obj
    for key in keys[:-1]:
        nxt = cur.get(key)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[key] = nxt
        cur = nxt
    if keys[-1] not in cur or not isinstance(cur[keys[-1]], type(default)):
        cur[keys[-1]] = default
    return cur[keys[-1]]


def effective_empty_heartbeat(workspace: Optional[Path]) -> bool:
    if not workspace:
        return False
    hb = workspace / "HEARTBEAT.md"
    if not hb.is_file():
        return False
    lines = hb.read_text(encoding="utf-8", errors="ignore").splitlines()
    meaningful = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        meaningful.append(stripped)
    return len(meaningful) == 0


def grep_hits(workspace: Optional[Path], pattern: str) -> List[str]:
    if not workspace or not workspace.is_dir():
        return []
    if shutil.which("rg"):
        out = subprocess.run(
            [
                "rg",
                "-n",
                "-S",
                "-i",
                pattern,
                str(workspace),
                "-g",
                "!**/node_modules/**",
                "-g",
                "!**/.git/**",
                "-g",
                "!**/dist/**",
                "-g",
                "!**/build/**",
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        ).stdout
        hits = [line for line in out.splitlines() if line.strip()]
        return hits[:20]

    import re

    compiled = re.compile(pattern, re.I)
    ignored = {".git", "node_modules", "dist", "build", ".next", "coverage", "__pycache__"}
    hits: List[str] = []
    for current_root, dirnames, filenames in os.walk(workspace):
        dirnames[:] = [d for d in dirnames if d not in ignored]
        for filename in filenames:
            path = Path(current_root) / filename
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                if compiled.search(line):
                    hits.append("{}:{}:{}".format(path, lineno, line.strip()))
                    if len(hits) >= 20:
                        return hits
    return hits


def patch_config(data: Dict[str, Any], mode: str) -> List[Tuple[str, Any, Any]]:
    heartbeat = nested_setdefault(data, ["agents", "defaults", "heartbeat"], {})
    changes = []

    def set_value(key, value, only_if_missing=False):
        old = heartbeat.get(key)
        if only_if_missing and key in heartbeat:
            return
        if old != value:
            heartbeat[key] = value
            changes.append((key, old, value))

    if mode == "disable":
        set_value("every", "0m")
    else:
        set_value("every", "1h")
        set_value("lightContext", True)
        set_value("isolatedSession", True)
        set_value("target", "none", only_if_missing=True)

    return changes


def validate_config() -> str:
    if shutil.which("openclaw"):
        return run(["openclaw", "config", "validate"])
    return ""


def main():
    parser = argparse.ArgumentParser(
        description="Apply a safe OpenClaw Feishu quota fix to the active config."
    )
    parser.add_argument("--config", help="Path to openclaw.json")
    parser.add_argument("--workspace", help="Path to OpenClaw workspace")
    parser.add_argument(
        "--mode",
        choices=["throttle", "disable"],
        default="throttle",
        help="throttle: 1h + lightContext + isolatedSession; disable: heartbeat every 0m",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config_path = detect_config(args.config)
    if not config_path:
        print("Could not find an OpenClaw config file.", file=sys.stderr)
        print("Pass one explicitly with --config /path/to/openclaw.json", file=sys.stderr)
        return 2

    workspace = detect_workspace(config_path, args.workspace)
    data = load_json(config_path)
    changes = patch_config(data, args.mode)

    print(f"Config: {config_path}")
    print(f"Workspace: {workspace if workspace else 'not found'}")
    print(f"Mode: {args.mode}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print()

    if changes:
        print("Planned config changes:")
        for key, old, new in changes:
            print(f"  - agents.defaults.heartbeat.{key}: {old!r} -> {new!r}")
    else:
        print("No config changes were needed.")

    hb_empty = effective_empty_heartbeat(workspace)
    if hb_empty:
        print()
        print("Note: HEARTBEAT.md is effectively empty, so OpenClaw may already skip heartbeat model calls.")

    official_hits = grep_hits(workspace, r"@openclaw/feishu|channels\.feishu|connectionMode")
    custom_hits = grep_hits(workspace, r"verificationToken|/health|healthCheck|webhook|gateway")

    if official_hits:
        print()
        print("Official/current Feishu clues:")
        for hit in official_hits[:8]:
            print(f"  - {hit}")

    if custom_hits:
        print()
        print("Custom webhook/gateway clues:")
        for hit in custom_hits[:8]:
            print(f"  - {hit}")
        print("  - Manual follow-up may still be needed for /health or webhook routes.")

    if args.dry_run:
        print()
        print("Dry run only. No files were changed.")
        return 0

    backup = backup_file(config_path)
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=True, indent=2)
        f.write("\n")

    print()
    print(f"Backup created: {backup}")
    print("Config updated.")

    if validate_config():
        print("Validation: openclaw config validate completed.")
    else:
        print("Validation: skipped or unavailable.")

    print("Next: restart the relevant OpenClaw gateway/agent process.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
