#!/usr/bin/env python3
import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Optional


SKILL_NAME = "openclaw-feishu-quota-guard"


def script_root() -> Path:
    return Path(__file__).resolve().parent


def detect_workspace(explicit: Optional[str]) -> Optional[Path]:
    if explicit:
        path = Path(explicit).expanduser()
        return path if path.is_dir() else None

    cwd = Path.cwd()
    if (cwd / "AGENTS.md").is_file() and (cwd / "skills").is_dir():
        return cwd

    default_workspace = Path.home() / ".openclaw" / "workspace"
    if default_workspace.is_dir():
        return default_workspace

    for candidate in limited_workspace_search(Path.home(), max_depth=4):
        if candidate.is_dir() and (candidate / "AGENTS.md").is_file():
            return candidate
    return None


def limited_workspace_search(root: Path, max_depth: int):
    base_depth = len(root.parts)
    for current_root, dirnames, _ in os.walk(root):
        current = Path(current_root)
        depth = len(current.parts) - base_depth
        if depth > max_depth:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "__pycache__"}]
        if current.name == "workspace":
            yield current


def copy_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)

    for name in ["SKILL.md", "_meta.json", "README.md"]:
        shutil.copy2(src / name, dest / name)

    shutil.copytree(src / "scripts", dest / "scripts")
    shutil.copytree(src / "references", dest / "references")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the OpenClaw Feishu Quota Guard skill into an OpenClaw workspace or shared skill directory."
    )
    parser.add_argument(
        "workspace",
        nargs="?",
        help="Install into <workspace>/skills/<skill-name>",
    )
    parser.add_argument(
        "--workspace",
        dest="workspace_flag",
        help="Install into <workspace>/skills/<skill-name>",
    )
    parser.add_argument(
        "--shared",
        action="store_true",
        help="Install into ~/.openclaw/skills/<skill-name> for all local agents",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    src = script_root()

    if args.shared:
        target_dir = Path.home() / ".openclaw" / "skills" / SKILL_NAME
    else:
        workspace_input = args.workspace_flag or args.workspace
        workspace = detect_workspace(workspace_input)
        if not workspace:
            print("Could not detect an OpenClaw workspace.", file=sys.stderr)
            print("Pass one explicitly, for example:", file=sys.stderr)
            print(
                "  python install_openclaw_skill.py --workspace /path/to/openclaw/workspace",
                file=sys.stderr,
            )
            return 1
        target_dir = workspace / "skills" / SKILL_NAME

    target_dir.parent.mkdir(parents=True, exist_ok=True)
    copy_tree(src, target_dir)

    print("Installed skill to:")
    print("  {}".format(target_dir))
    print()
    print("Run once now:")
    print("  python \"{}\"".format(target_dir / "scripts" / "apply_feishu_quota_fix.py"))
    print()
    print("Dry run first:")
    print(
        "  python \"{}\" --dry-run".format(
            target_dir / "scripts" / "apply_feishu_quota_fix.py"
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
