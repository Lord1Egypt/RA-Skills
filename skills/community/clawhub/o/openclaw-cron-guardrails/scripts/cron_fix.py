#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys

DEFAULT_TIMEOUT_SECONDS = 300


def run(cmd: list[str]):
    proc = subprocess.run(cmd, text=True, capture_output=True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def load_lint_results():
    proc = subprocess.run(
        [sys.executable, __file__.replace("cron_fix.py", "lint_existing_crons.py")],
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "lint_existing_crons failed")
    return json.loads(proc.stdout)


def choose_patch(job: dict, default_tz: str):
    findings = {f.get("code") for f in job.get("findings", []) if isinstance(f, dict)}
    patch = []
    rationale = []

    if "announce-last-route" in findings or "delivery-route-failed" in findings:
        patch.extend(["--no-deliver"])
        rationale.append("switch fragile announce/last-route delivery to internal-only")

    if "timeout-short" in findings or "recent-timeout" in findings:
        patch.extend(["--timeout-seconds", str(DEFAULT_TIMEOUT_SECONDS)])
        rationale.append(f"raise timeoutSeconds to {DEFAULT_TIMEOUT_SECONDS}")

    schedule = job.get("schedule") or {}
    if "missing-timezone" in findings and isinstance(schedule, dict) and schedule.get("kind") == "cron":
        patch.extend(["--tz", default_tz])
        rationale.append(f"set explicit timezone to {default_tz}")

    return patch, rationale


def main():
    parser = argparse.ArgumentParser(description="Conservative fixer for known OpenClaw cron issues")
    parser.add_argument("job_id", help="Cron job id to fix")
    parser.add_argument("--apply", action="store_true", help="Apply the edit instead of reporting the patch")
    parser.add_argument("--tz", default="America/New_York", help="Default timezone to use when adding missing tz")
    args = parser.parse_args()

    data = load_lint_results()
    target = None
    for r in data.get("results", []):
        if r.get("id") == args.job_id:
            target = r
            break
    if not target:
        print(json.dumps({"ok": False, "error": f"job not found in lint results: {args.job_id}"}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    patch, rationale = choose_patch(target, args.tz)
    if not patch:
        print(json.dumps({"ok": True, "jobId": args.job_id, "message": "no automatic fix needed", "target": target}, ensure_ascii=False, indent=2))
        raise SystemExit(0)

    command = ["openclaw", "cron", "edit", args.job_id, *patch]
    result = {
        "ok": True,
        "jobId": args.job_id,
        "mode": "apply" if args.apply else "dry-run",
        "name": target.get("name"),
        "findings": target.get("findings", []),
        "rationale": rationale,
        "command": command,
    }

    if args.apply:
        result["execution"] = run(command)
        result["ok"] = result["execution"]["returncode"] == 0
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(0 if result["ok"] else 1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
