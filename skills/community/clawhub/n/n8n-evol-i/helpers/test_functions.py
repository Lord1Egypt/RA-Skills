#!/usr/bin/env python3
"""Run unit tests over JS used in n8n Code nodes and/or Python used in cloud functions."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_common


def _layout(workspace: Path) -> dict:
    common = load_common(workspace)
    return common.get("workspace_layout", {}) or {}


def _resolve(workspace: Path, key: str, default: str) -> Path:
    layout = _layout(workspace)
    rel = layout.get(key, default).rstrip("/")
    return workspace / rel


def _run_node_tests(tests_dir: Path, name_filter: str | None) -> tuple[int, str]:
    if not tests_dir.is_dir():
        return (0, "n8n: no tests dir")
    tests = sorted(tests_dir.glob("*.test.js"))
    if name_filter:
        tests = [t for t in tests if name_filter in t.stem]
    if not tests:
        return (0, "n8n: no tests")

    if shutil.which("node") is None:
        return (1, "n8n: node binary not found on PATH")

    pkg_json = tests_dir / "package.json"
    if pkg_json.exists():
        # Defer to project's npm test runner
        cmd = ["npm", "test", "--silent"]
        cwd = tests_dir
    else:
        cmd = ["node", "--test", *[str(t) for t in tests]]
        cwd = tests_dir

    r = subprocess.run(cmd, cwd=cwd)
    return (r.returncode, f"n8n: ran {len(tests)} test file(s) (exit={r.returncode})")


def _run_pytest_tests(tests_dir: Path, name_filter: str | None) -> tuple[int, str]:
    if not tests_dir.is_dir():
        return (0, "cloud: no tests dir")
    tests = sorted(tests_dir.glob("test_*.py"))
    if name_filter:
        tests = [t for t in tests if name_filter in t.stem]
    if not tests:
        return (0, "cloud: no tests")

    cmd = [sys.executable, "-m", "pytest", "-v", *[str(t) for t in tests]]
    r = subprocess.run(cmd, cwd=tests_dir)
    return (r.returncode, f"cloud: ran {len(tests)} test file(s) (exit={r.returncode})")


def _run_pytest_n8n_tests(tests_dir: Path, name_filter: str | None) -> tuple[int, str]:
    """Run pytest over test_*.py files in n8n-functions-tests/ (Python pure-function tests)."""
    if not tests_dir.is_dir():
        return (0, "n8n-py: no tests dir")
    tests = sorted(tests_dir.glob("test_*.py"))
    if name_filter:
        tests = [t for t in tests if name_filter in t.stem]
    if not tests:
        return (0, "n8n-py: no tests")

    cmd = [sys.executable, "-m", "pytest", "-v", *[str(t) for t in tests]]
    r = subprocess.run(cmd, cwd=tests_dir)
    return (r.returncode, f"n8n-py: ran {len(tests)} test file(s) (exit={r.returncode})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--target", choices=("n8n", "cloud", "all"), default="all")
    parser.add_argument("--filter", default=None, dest="name_filter")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    n8n_tests = _resolve(ws, "n8n_functions_tests_dir", "n8n-functions-tests")
    cloud_tests = _resolve(ws, "cloud_functions_tests_dir", "cloud-functions-tests")

    summaries: list[tuple[int, str]] = []
    if args.target in ("n8n", "all"):
        summaries.append(_run_node_tests(n8n_tests, args.name_filter))
        summaries.append(_run_pytest_n8n_tests(n8n_tests, args.name_filter))
    if args.target in ("cloud", "all"):
        summaries.append(_run_pytest_tests(cloud_tests, args.name_filter))

    print("\nTest summary:")
    for code, line in summaries:
        print(f"  [{'OK' if code == 0 else 'FAIL'}] {line}")

    sys.exit(0 if all(c == 0 for c, _ in summaries) else 1)


if __name__ == "__main__":
    main()
