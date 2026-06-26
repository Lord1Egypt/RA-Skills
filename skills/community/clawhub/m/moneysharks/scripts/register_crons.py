#!/usr/bin/env python3
"""
Generate ready-to-register OpenClaw cron job definitions for MoneySharks.
Substitutes the /ABSOLUTE/PATH/TO/moneysharks placeholder with the real skill root path.
Writes a register_crons.json output file the OpenClaw agent uses to register cron jobs.

usage: register_crons.py <config.json> [--skill-root <path>] [--mode autonomous_live|paper] [--output <file>]

If --skill-root is not provided, defaults to the parent directory of this script.
Output file defaults to <skill-root>/register_crons.json.
"""
import json
import sys
from pathlib import Path


PLACEHOLDER = "/ABSOLUTE/PATH/TO/moneysharks"


def main() -> int:
    base = Path(__file__).resolve().parent
    skill_root = base.parent  # default: parent of scripts/

    # Config path: first non-flag argument (if any)
    config_path = None
    if len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        config_path = Path(sys.argv[1])

    output_path = skill_root / "register_crons.json"
    mode = "autonomous_live"

    for i, arg in enumerate(sys.argv):
        if arg == "--skill-root" and i + 1 < len(sys.argv):
            skill_root = Path(sys.argv[i + 1]).resolve()
        elif arg == "--mode" and i + 1 < len(sys.argv):
            mode = sys.argv[i + 1]
        elif arg == "--output" and i + 1 < len(sys.argv):
            output_path = Path(sys.argv[i + 1])

    # Default config path now that skill_root is resolved
    if config_path is None:
        config_path = skill_root / "config.json"

    # Load config for path to config.json and scan interval
    config = {}
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
        except Exception:
            pass

    scan_interval = int(config.get("cron", {}).get("scan_interval_minutes", 2))
    config_file = str(config_path.resolve())
    skill_path = str(skill_root.resolve())

    # Load templates
    templates_path = skill_root / "openclaw-cron-templates.json"
    if not templates_path.exists():
        print(f"ERROR: openclaw-cron-templates.json not found at {templates_path}", file=sys.stderr)
        return 1

    raw = templates_path.read_text()
    # Substitute skill path placeholder
    substituted = raw.replace(PLACEHOLDER, skill_path)
    # Also substitute config path references
    substituted = substituted.replace(
        f"{skill_path}/config.json", config_file
    )
    templates = json.loads(substituted)

    # Select which jobs to enable based on mode
    if mode == "autonomous_live":
        active_jobs = ["autonomous_live_scan", "autonomous_review", "autonomous_daily_summary", "halt_check"]
        disabled_jobs = ["paper_market_scan", "paper_review_cycle", "autonomous_live_scan_systemEvent"]
    else:
        active_jobs = ["paper_market_scan", "paper_review_cycle"]
        disabled_jobs = ["autonomous_live_scan", "autonomous_review", "autonomous_daily_summary",
                         "halt_check", "autonomous_live_scan_systemEvent"]

    result = {}
    for job_id, job in templates.items():
        if job_id.startswith("_"):
            continue
        job_copy = dict(job)
        job_copy["enabled"] = job_id in active_jobs

        # Update scan interval for autonomous scan
        if job_id == "autonomous_live_scan" and scan_interval != 2:
            job_copy["schedule"] = {
                "kind": "cron",
                "expr": f"*/{scan_interval} * * * *",
                "tz": "UTC",
            }

        # Update agentTurn messages with real config path
        if job_copy.get("payload", {}).get("kind") == "agentTurn":
            msg = job_copy["payload"]["message"]
            msg = msg.replace(PLACEHOLDER, skill_path)
            job_copy["payload"]["message"] = msg
        elif job_copy.get("payload", {}).get("kind") == "systemEvent":
            text = job_copy["payload"].get("text", "")
            text = text.replace(PLACEHOLDER, skill_path)
            job_copy["payload"]["text"] = text

        result[job_id] = job_copy

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2))

    print(json.dumps({
        "ok": True,
        "output": str(output_path),
        "skill_root": skill_path,
        "config_path": config_file,
        "mode": mode,
        "active_jobs": active_jobs,
        "cron_jobs": result,
    }, indent=2))

    print(f"\n✓ Cron job definitions written to: {output_path}", file=sys.stderr)
    print(f"  Active jobs ({mode}): {', '.join(active_jobs)}", file=sys.stderr)
    print(f"\n  If you're using the OpenClaw agent, it will register these automatically.", file=sys.stderr)
    print(f"  Otherwise, register manually via the OpenClaw cron tool using the JSON above.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
