#!/usr/bin/env python3
"""Copy lock primitive templates from harness/primitives into the workspace and register them."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root, harness_root


_PRIMITIVES = {
    "lock_acquisition": "Lock Acquisition",
    "lock_release": "Lock Release",
}
_ERROR_HANDLER = ("error_handler_lock_cleanup", "Error Handler Lock Cleanup")
_RATE_LIMIT = ("rate_limit_check", "Rate Limit Check")


def _copy_primitive(workspace: Path, key: str, force_overwrite: bool = False) -> Path:
    src = harness_root() / "primitives" / "workflows" / f"{key}.template.json"
    if not src.exists():
        raise FileNotFoundError(f"Primitive missing: {src}")
    dst_dir = workspace / "n8n-workflows-template"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / f"{key}.template.json"
    if dst.exists() and not force_overwrite:
        print(
            f"  WARNING: {key}.template.json already exists — re-run with "
            f"--force-overwrite to update to the real Redis implementation."
        )
    else:
        existed = dst.exists()
        shutil.copyfile(src, dst)
        action = "Overwrote" if existed else "Copied"
        print(f"  {action} {src.name} → {dst}")
    return dst


def _register_via_create_workflow(workspace: Path, key: str, name: str, tier: str) -> None:
    """Register the workflow in env YAMLs (and mint placeholder IDs) without re-writing the template."""
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "create_workflow.py"),
        "--workspace", str(workspace),
        "--key", key,
        "--name", name,
        "--no-template",
        "--tier", tier,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, file=sys.stderr)
        print(r.stderr, file=sys.stderr)
        raise SystemExit(r.returncode)
    print(r.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--include-error-handler", action="store_true", dest="include_error_handler")
    parser.add_argument("--include-rate-limit", action="store_true", dest="include_rate_limit")
    parser.add_argument("--force-overwrite", action="store_true", dest="force_overwrite")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)

    primitives = dict(_PRIMITIVES)
    if args.include_error_handler:
        key, name = _ERROR_HANDLER
        primitives[key] = name
    if args.include_rate_limit:
        key, name = _RATE_LIMIT
        primitives[key] = name

    # Two-pass: copy all primitives first, then attempt registrations. If a
    # registration fails (e.g. transient n8n API hiccup or expired API key),
    # the workspace is at least left with all template files on disk so a
    # later re-run can resume by registering only the un-registered keys.
    for key, _ in primitives.items():
        _copy_primitive(ws, key, force_overwrite=args.force_overwrite)

    failures: list[tuple[str, Exception]] = []
    for key, name in primitives.items():
        try:
            _register_via_create_workflow(ws, key, name, "Tier 0a: leaves")
        except SystemExit as e:
            failures.append((key, e))
            print(f"  WARNING: registration failed for '{key}'; continuing.", file=sys.stderr)

    if failures:
        print(
            f"create-lock partial: {len(primitives) - len(failures)}/{len(primitives)} registered. "
            f"Re-run after fixing the underlying issue (commonly: invalid N8N_API_KEY).",
            file=sys.stderr,
        )
        sys.exit(1)
    print("create-lock complete.")


if __name__ == "__main__":
    main()
