#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LINTER = SCRIPT_DIR / "lint_existing_crons.py"
FIXER = SCRIPT_DIR / "cron_fix.py"


def run_json(cmd: list[str]):
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        return proc.returncode, {"ok": False, "stdout": proc.stdout, "stderr": proc.stderr}
    try:
        return proc.returncode, json.loads(proc.stdout)
    except Exception:
        return 1, {"ok": False, "stdout": proc.stdout, "stderr": proc.stderr, "error": "invalid json"}


def main():
    parser = argparse.ArgumentParser(description="Scan cron jobs, warn on risks, and optionally auto-fix errors")
    parser.add_argument("--apply-errors", action="store_true", help="Apply fixes for jobs that have error-severity findings")
    parser.add_argument("--tz", default="America/New_York", help="Default timezone to use when fixing missing tz")
    args = parser.parse_args()

    rc, lint = run_json([sys.executable, str(LINTER)])
    if rc != 0 or not lint.get("ok"):
        print(json.dumps({"ok": False, "stage": "lint", "result": lint}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    warnings = []
    errors = []
    fixes = []
    for r in lint.get("results", []):
        findings = r.get("findings", [])
        if not findings:
            continue
        severities = {f.get("severity") for f in findings if isinstance(f, dict)}
        if "error" in severities:
            errors.append({"id": r.get("id"), "name": r.get("name"), "findings": findings})
        else:
            warnings.append({"id": r.get("id"), "name": r.get("name"), "findings": findings})

    if args.apply_errors:
        for item in errors:
            frc, fixed = run_json([sys.executable, str(FIXER), item["id"], "--apply", "--tz", args.tz])
            fixes.append({"id": item["id"], "name": item["name"], "ok": frc == 0 and fixed.get("ok"), "result": fixed})

    result = {
        "ok": True,
        "summary": lint.get("summary", {}),
        "warnings": warnings,
        "errors": errors,
        "fixes": fixes,
        "mode": "apply-errors" if args.apply_errors else "scan-only",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
