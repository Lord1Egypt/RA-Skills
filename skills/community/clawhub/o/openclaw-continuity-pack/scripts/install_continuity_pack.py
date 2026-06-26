#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from apply_runtime_patch import execute_patch_workflow
from bootstrap_workspace import bootstrap_workspace


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install OpenClaw Continuity Pack into a workspace, or run the full workspace + runtime continuity flow."
    )
    parser.add_argument(
        "--route",
        choices=("workspace", "continuity", "full"),
        default="workspace",
        help="workspace=full workspace layer, continuity=workflow-only, full=workspace layer + runtime patch flow",
    )
    parser.add_argument(
        "--workspace",
        default="auto",
        help="Target OpenClaw workspace path. Default: auto-detect from env/current workspace, else ~/.openclaw/workspace",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing workspace files")
    parser.add_argument("--source-root", help="Matching OpenClaw source tree for --route full")
    parser.add_argument("--patch", help="Override the bundled patch path for --route full")
    parser.add_argument(
        "--apply-runtime-patch",
        action="store_true",
        help="Actually write the runtime patch when using --route full",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Run pnpm build and pnpm ui:build after applying the runtime patch",
    )
    args = parser.parse_args()

    print(f"Route: {args.route}")

    profile = "continuity" if args.route == "continuity" else "full"
    bootstrap_rc = bootstrap_workspace(
        workspace_spec=args.workspace,
        profile=profile,
        force=args.force,
    )
    if bootstrap_rc != 0:
        return bootstrap_rc

    if args.route != "full":
        print("\nINSTALL_COMPLETE")
        return 0

    if not args.source_root:
        print("ERROR: --route full requires --source-root <OPENCLAW_SOURCE_ROOT>")
        return 2
    if not args.apply_runtime_patch:
        print("ERROR: --route full also requires --apply-runtime-patch because it modifies the target source tree.")
        print("If you only want workspace templates, use --route workspace or --route continuity.")
        return 2

    patch_rc = execute_patch_workflow(
        source_root=Path(args.source_root),
        patch=args.patch,
        apply=True,
        rebuild=args.rebuild,
    )
    if patch_rc != 0:
        return patch_rc

    print("\nFULL_INSTALL_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
