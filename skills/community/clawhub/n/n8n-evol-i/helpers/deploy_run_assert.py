#!/usr/bin/env python3
"""Composite verify: validate (built) → deploy → run --expect-status success."""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root


def _run(cmd: list[str], stage: str) -> None:
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FAIL: stage={stage} exit={r.returncode}", file=sys.stderr)
        sys.exit(r.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--payload", default="{}")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--no-activate", action="store_true")
    parser.add_argument(
        "--expect-status",
        default="success",
        dest="expect_status",
        choices=("success", "error"),
        help="Expected terminal status of the run (default: success).",
    )
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    helpers = Path(__file__).parent
    ws_args = ["--workspace", str(ws)]

    # 1. hydrate (so the built JSON exists for validation)
    _run(
        [sys.executable, str(helpers / "hydrate.py"), *ws_args, "--env", args.env, "--workflow-key", args.workflow_key],
        stage="hydrate",
    )

    # 2. validate built
    _run(
        [sys.executable, str(helpers / "validate.py"), *ws_args, "--env", args.env, "--workflow-key", args.workflow_key, "--source", "built"],
        stage="validate",
    )

    # 3. deploy
    deploy_cmd = [sys.executable, str(helpers / "deploy.py"), *ws_args, "--env", args.env, "--workflow-key", args.workflow_key]
    if args.no_activate:
        deploy_cmd.append("--no-activate")
    _run(deploy_cmd, stage="deploy")

    # 4. run with expectation
    run_cmd = [
        sys.executable, str(helpers / "run.py"), *ws_args,
        "--env", args.env, "--workflow-key", args.workflow_key,
        "--payload", args.payload,
        "--timeout", str(args.timeout),
        "--expect-status", args.expect_status,
    ]
    _run(run_cmd, stage="run")

    print("deploy-run-assert OK")


if __name__ == "__main__":
    main()
