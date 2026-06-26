#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run(cmd: list[str], *, cwd: Path) -> int:
    printable = " ".join(cmd)
    print(f"+ {printable}")
    completed = subprocess.run(cmd, cwd=str(cwd))
    return completed.returncode


def execute_patch_workflow(
    *,
    source_root: Path,
    patch: str | None = None,
    apply: bool = False,
    rebuild: bool = False,
) -> int:
    skill_root = Path(__file__).resolve().parents[1]
    source_root = source_root.expanduser().resolve()
    patch_path = Path(patch).expanduser().resolve() if patch else skill_root / "assets" / "patch" / "thread-continuity.patch"

    if not source_root.exists():
        print(f"ERROR: source root not found: {source_root}")
        return 2
    if not patch_path.exists():
        print(f"ERROR: patch not found: {patch_path}")
        return 2

    check_cmd = ["git", "apply", "--check", str(patch_path)]
    check_rc = run(check_cmd, cwd=source_root)
    if check_rc != 0:
        print("\nPATCH_CHECK_FAILED")
        print("The target tree may be on a different OpenClaw revision, already patched, or otherwise divergent.")
        print("Compare the tree against references/files-to-replace.md and references/deploy-notes.md.")
        return check_rc

    print("\nPATCH_CHECK_OK")
    if not apply:
        print("Use --apply to write the patch.")
        return 0

    apply_cmd = ["git", "apply", str(patch_path)]
    apply_rc = run(apply_cmd, cwd=source_root)
    if apply_rc != 0:
        print("\nPATCH_APPLY_FAILED")
        return apply_rc

    print("\nPATCH_APPLIED")
    if not rebuild:
        print("Patch applied. Next run: pnpm build && pnpm ui:build")
        return 0

    build_rc = run(["pnpm", "build"], cwd=source_root)
    if build_rc != 0:
        print("\nBUILD_FAILED")
        return build_rc

    ui_build_rc = run(["pnpm", "ui:build"], cwd=source_root)
    if ui_build_rc != 0:
        print("\nUI_BUILD_FAILED")
        return ui_build_rc

    print("\nREBUILD_COMPLETE")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or apply the OpenClaw thread continuity runtime patch."
    )
    parser.add_argument("--source-root", required=True, help="Target OpenClaw source root")
    parser.add_argument(
        "--patch",
        help="Override the bundled patch path",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the patch after a successful check",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Run pnpm build and pnpm ui:build after applying the patch",
    )
    args = parser.parse_args()
    return execute_patch_workflow(
        source_root=Path(args.source_root),
        patch=args.patch,
        apply=args.apply,
        rebuild=args.rebuild,
    )


if __name__ == "__main__":
    raise SystemExit(main())
