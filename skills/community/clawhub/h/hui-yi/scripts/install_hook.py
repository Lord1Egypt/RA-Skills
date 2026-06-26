#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import json

from core.common import WORKSPACE_ROOT
DEFAULT_HOOK_DIR = WORKSPACE_ROOT / "hooks" / "hui-yi-signal-hook"
DEFAULT_TEMPLATE_DIR = SKILL_ROOT / "templates" / "hook"
DEFAULT_CONFIG_PATH = WORKSPACE_ROOT.parent / "openclaw.json"
HOOK_NAME = "hui-yi-signal-hook"

IGNORED_NAMES = {
    ".DS_Store",
    "Thumbs.db",
}

IGNORED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".tmp",
    ".bak",
}

IGNORED_PARTS = {
    "__pycache__",
}


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def print_enable_disclosure(config_path: Path) -> None:
    print("DISCLOSURE: --enable will modify the OpenClaw runtime configuration:")
    print(f"  file: {config_path}")
    print("  SET hooks.internal.enabled = true (if not already true)")
    print(f"  SET hooks.internal.entries.{HOOK_NAME}.enabled = true (if not already true)")
    print("  The enabled hook listens on message:preprocessed events and writes")
    print("  Session signals to memory/cold/ notes and memory/cold/tags.json.")
    print("  Default hook logs persist no message content and only hashed scope ids;")
    print("  set HUI_YI_HOOK_DEBUG=1 to opt into verbose diagnostics.")


def ensure_hook_enabled(config: dict) -> tuple[dict, list[str]]:
    notes: list[str] = []
    hooks = config.setdefault("hooks", {})
    internal = hooks.setdefault("internal", {})
    if internal.get("enabled") is not True:
        internal["enabled"] = True
        notes.append("SET hooks.internal.enabled = true")
    entries = internal.setdefault("entries", {})
    entry = entries.setdefault(HOOK_NAME, {})
    if entry.get("enabled") is not True:
        entry["enabled"] = True
        notes.append(f"SET hooks.internal.entries.{HOOK_NAME}.enabled = true")
    return config, notes


def write_config(path: Path, config: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def should_ignore(path: Path) -> bool:
    if any(part in IGNORED_PARTS for part in path.parts):
        return True
    if path.name in IGNORED_NAMES:
        return True
    if path.suffix.lower() in IGNORED_SUFFIXES:
        return True
    if path.name.endswith("~"):
        return True
    return False


def iter_template_files(template_dir: Path):
    for path in sorted(template_dir.rglob("*")):
        if not path.is_file():
            continue
        if should_ignore(path):
            continue
        yield path


def build_plan(template_dir: Path, target_dir: Path) -> list[tuple[Path, Path]]:
    files = list(iter_template_files(template_dir))
    if not files:
        raise FileNotFoundError(f"No template files found in: {template_dir}")
    return [
        (target_dir / src.relative_to(template_dir), src)
        for src in files
    ]


def write_file(destination: Path, source: Path, force: bool) -> str:
    if destination.exists() and not force:
        return f"SKIP {destination} (already exists, use --force to overwrite)"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return f"WROTE {destination}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Hui-Yi hook files into workspace hooks/ from skill-bundled templates")
    parser.add_argument("--force", action="store_true", help="overwrite existing hook files")
    parser.add_argument("--dry-run", action="store_true", help="show planned writes without changing files")
    parser.add_argument("--enable", action="store_true", help="also enable the hook in openclaw.json")
    parser.add_argument("--target-dir", default=str(DEFAULT_HOOK_DIR), help="target hook directory")
    parser.add_argument("--template-dir", default=str(DEFAULT_TEMPLATE_DIR), help="template source directory")
    parser.add_argument("--config-path", default=str(DEFAULT_CONFIG_PATH), help="path to openclaw.json")
    args = parser.parse_args()

    target_dir = Path(args.target_dir)
    template_dir = Path(args.template_dir)
    config_path = Path(args.config_path)

    if not template_dir.exists():
        raise FileNotFoundError(f"Template directory not found: {template_dir}")
    if not template_dir.is_dir():
        raise NotADirectoryError(f"Template path is not a directory: {template_dir}")

    planned = build_plan(template_dir, target_dir)

    if args.dry_run:
        for destination, source in planned:
            if destination.exists() and not args.force:
                print(f"SKIP {destination} (already exists, use --force to overwrite)")
            else:
                print(f"WOULD WRITE {destination} <- {source}")
        if args.enable:
            print_enable_disclosure(config_path)
            if not config_path.exists():
                print(f"WOULD ABORT: config file not found: {config_path} (pass --config-path to the real openclaw.json)")
                return 0
            config = load_config(config_path)
            _, notes = ensure_hook_enabled(config)
            if notes:
                for note in notes:
                    print(f"WOULD {note}")
            else:
                print(f"HOOK ALREADY ENABLED in {config_path}")
        return 0

    for destination, source in planned:
        print(write_file(destination, source, force=args.force))

    if args.enable:
        print_enable_disclosure(config_path)
        if not config_path.exists():
            print(f"ERROR: config file not found: {config_path}", file=sys.stderr)
            print("Refusing to create a new openclaw.json; pass --config-path to the real config file.", file=sys.stderr)
            return 1
        config = load_config(config_path)
        config, notes = ensure_hook_enabled(config)
        write_config(config_path, config)
        if notes:
            for note in notes:
                print(note)
        else:
            print(f"HOOK ALREADY ENABLED in {config_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
