#!/usr/bin/env python3
"""Copy a single primitive template from harness/primitives into the workspace.

Unlike `create_lock.py` (which bundles the lock pair + opt-ins and registers in
env YAMLs), this helper copies any primitive by name and does NOT register it.
Use `create_workflow.py --no-template --key <name>` afterwards to register the
copied primitive in env YAMLs if needed.
"""
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root, harness_root


def _list_available() -> list[str]:
    """List primitive keys available in <harness>/primitives/workflows/."""
    primitives_dir = harness_root() / "primitives" / "workflows"
    if not primitives_dir.is_dir():
        return []
    keys: list[str] = []
    for f in sorted(primitives_dir.glob("*.template.json")):
        # strip .template.json
        stem = f.name[: -len(".template.json")]
        if stem.startswith("_"):
            # `_minimal.template.json` is a scaffold seed, not a user-facing primitive
            continue
        keys.append(stem)
    return keys


def _copy(workspace: Path, key: str, force_overwrite: bool) -> Path:
    src = harness_root() / "primitives" / "workflows" / f"{key}.template.json"
    if not src.exists():
        available = _list_available()
        raise SystemExit(
            f"Primitive not found: {src}\n"
            f"Available: {', '.join(available) if available else '(none)'}"
        )
    dst_dir = workspace / "n8n-workflows-template"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / f"{key}.template.json"
    if dst.exists() and not force_overwrite:
        print(
            f"  WARNING: {key}.template.json already exists — re-run with "
            f"--force-overwrite to update to the real Redis implementation."
        )
        return dst
    existed = dst.exists()
    shutil.copyfile(src, dst)
    action = "Overwrote" if existed else "Copied"
    print(f"  {action} {src.name} → {dst}")
    return dst


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument(
        "--name",
        default=None,
        help="Primitive key (file name minus `.template.json`). Use --list to see options.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_primitives",
        help="Print available primitive keys and exit.",
    )
    parser.add_argument(
        "--force-overwrite",
        action="store_true",
        dest="force_overwrite",
        help="Overwrite an existing copy in the workspace instead of skipping.",
    )
    args = parser.parse_args()

    if args.list_primitives or not args.name:
        available = _list_available()
        if not available:
            print("No primitives available under <harness>/primitives/workflows/.", file=sys.stderr)
            sys.exit(1)
        print("Available primitives:")
        for k in available:
            print(f"  - {k}")
        if not args.name:
            sys.exit(0 if args.list_primitives else 2)
        sys.exit(0)

    ws = workspace_root(args.workspace)
    _copy(ws, args.name, force_overwrite=args.force_overwrite)

    if args.name in ("lock_acquisition", "lock_release", "error_handler_lock_cleanup"):
        print(
            "  NOTE: lock primitives also need env-YAML registration. Run "
            "`python3 <harness>/helpers/create_lock.py` (or "
            "`create_workflow.py --no-template --key <name>` for ad-hoc registration)."
        )

    print("copy-primitive complete.")


if __name__ == "__main__":
    main()
