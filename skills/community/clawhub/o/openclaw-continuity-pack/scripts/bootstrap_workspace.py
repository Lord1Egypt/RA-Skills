#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

WORKSPACE_HINT_FILES = (
    "AGENTS.md",
    "SOUL.md",
    "USER.md",
    "TOOLS.md",
    "HEARTBEAT.md",
    "SESSION_CONTINUITY.md",
)
WORKSPACE_HINT_DIRS = (
    "memory",
    "plans",
    "status",
    "handoff",
    "skills",
)
DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace"


def copy_file(src: Path, dst: Path, *, force: bool) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not force:
        return f"SKIP {dst} (exists)"
    shutil.copy2(src, dst)
    return f"COPY {src.name} -> {dst}"


def looks_like_workspace(path: Path) -> bool:
    if not path.exists() or not path.is_dir():
        return False
    return any((path / name).exists() for name in (*WORKSPACE_HINT_FILES, *WORKSPACE_HINT_DIRS))


def resolve_workspace(workspace_spec: str) -> tuple[Path, str]:
    if workspace_spec and workspace_spec != "auto":
        workspace = Path(workspace_spec).expanduser().resolve()
        if workspace.exists() and not workspace.is_dir():
            raise RuntimeError(f"workspace path is not a directory: {workspace}")
        return workspace, "explicit --workspace"

    env_candidates = (
        "OPENCLAW_CONTINUITY_WORKSPACE",
        "OPENCLAW_WORKSPACE_DIR",
        "OPENCLAW_WORKSPACE",
    )
    for env_name in env_candidates:
        raw = os.environ.get(env_name)
        if not raw:
            continue
        workspace = Path(raw).expanduser().resolve()
        if workspace.exists() and not workspace.is_dir():
            raise RuntimeError(f"{env_name} points to a file, not a directory: {workspace}")
        return workspace, f"env:{env_name}"

    cwd = Path.cwd().resolve()
    if looks_like_workspace(cwd):
        return cwd, "current working directory"

    return DEFAULT_WORKSPACE.expanduser().resolve(), "default ~/.openclaw/workspace"


def build_file_map(*, assets_root: Path, workspace: Path, profile: str) -> dict[Path, Path]:
    full_file_map = {
        assets_root / "SOUL.md": workspace / "SOUL.md",
        assets_root / "HEARTBEAT.md": workspace / "HEARTBEAT.md",
        assets_root / "AGENTS.md": workspace / "AGENTS.md",
        assets_root / "SESSION_CONTINUITY.md": workspace / "SESSION_CONTINUITY.md",
        assets_root / "plans" / "TEMPLATE.md": workspace / "plans" / "TEMPLATE.md",
        assets_root / "status" / "TEMPLATE.md": workspace / "status" / "TEMPLATE.md",
        assets_root / "handoff" / "TEMPLATE.md": workspace / "handoff" / "TEMPLATE.md",
        assets_root / "memory" / "README.md": workspace / "memory" / "README.md",
        assets_root / "temp" / "README.md": workspace / "temp" / "README.md",
        assets_root / "USER.template.md": workspace / "USER.md",
        assets_root / "TOOLS.template.md": workspace / "TOOLS.md",
    }
    continuity_file_map = {
        assets_root / "AGENTS.md": workspace / "AGENTS.md",
        assets_root / "SESSION_CONTINUITY.md": workspace / "SESSION_CONTINUITY.md",
        assets_root / "plans" / "TEMPLATE.md": workspace / "plans" / "TEMPLATE.md",
        assets_root / "status" / "TEMPLATE.md": workspace / "status" / "TEMPLATE.md",
        assets_root / "handoff" / "TEMPLATE.md": workspace / "handoff" / "TEMPLATE.md",
        assets_root / "memory" / "README.md": workspace / "memory" / "README.md",
        assets_root / "temp" / "README.md": workspace / "temp" / "README.md",
    }
    return full_file_map if profile == "full" else continuity_file_map


def bootstrap_workspace(*, workspace_spec: str, profile: str, force: bool) -> int:
    skill_root = Path(__file__).resolve().parents[1]
    assets_root = skill_root / "assets" / "workspace"
    workspace, resolved_from = resolve_workspace(workspace_spec)
    workspace.mkdir(parents=True, exist_ok=True)
    file_map = build_file_map(assets_root=assets_root, workspace=workspace, profile=profile)

    print(f"Workspace: {workspace}")
    print(f"Resolved from: {resolved_from}")
    print(f"Profile: {profile}")
    print("\nScaffolding reproducible workspace layer...\n")
    for src, dst in file_map.items():
        print(copy_file(src, dst, force=force))

    print("\nDone.")
    print("\nNotes:")
    print("- This script copies only reproducible templates and prompts.")
    print("- It does NOT copy real memory, secrets, user-specific notes, tokens, or live channel config.")
    print("- To enable runtime/UI continuity, you still need to apply assets/patch/thread-continuity.patch against a matching OpenClaw source tree and rebuild.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap the reproducible workspace layer from OpenClaw Continuity Pack."
    )
    parser.add_argument(
        "--workspace",
        default="auto",
        help="Target OpenClaw workspace path. Default: auto-detect from env/current workspace, else ~/.openclaw/workspace",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument(
        "--profile",
        choices=("full", "continuity"),
        default="full",
        help="Install the full operating layer or only the continuity workflow files",
    )
    args = parser.parse_args()

    try:
        return bootstrap_workspace(workspace_spec=args.workspace, profile=args.profile, force=args.force)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
