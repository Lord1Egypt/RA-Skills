#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


def load_jobs(path_arg: str | None):
    if path_arg:
        return json.loads(Path(path_arg).read_text())
    proc = subprocess.run(
        ["openclaw", "cron", "list", "--all", "--json"],
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "failed to run openclaw cron list --all --json")
    return json.loads(proc.stdout)


def classify_job(job: dict):
    findings: list[dict] = []
    delivery = job.get("delivery") if isinstance(job.get("delivery"), dict) else None
    payload = job.get("payload") if isinstance(job.get("payload"), dict) else {}
    schedule = job.get("schedule") if isinstance(job.get("schedule"), dict) else {}

    session_target = job.get("sessionTarget")
    payload_kind = payload.get("kind")
    delivery_mode = delivery.get("mode") if delivery else None
    delivery_channel = delivery.get("channel") if delivery else None
    delivery_to = delivery.get("to") if delivery else None
    timeout_seconds = payload.get("timeoutSeconds")
    message = payload.get("message") if isinstance(payload.get("message"), str) else ""

    def add(severity: str, code: str, message_text: str):
        findings.append({"severity": severity, "code": code, "message": message_text})

    if session_target == "main" and payload_kind != "systemEvent":
        add("error", "invalid-main-payload", "main job should use payload.kind=systemEvent")
    if session_target == "isolated" and payload_kind != "agentTurn":
        add("error", "invalid-isolated-payload", "isolated job should use payload.kind=agentTurn")

    if session_target == "isolated" and delivery is None:
        add("warn", "implicit-default-announce", "isolated job has no delivery config and will default to announce")

    if delivery_mode == "announce" and delivery_channel == "last":
        add("warn", "announce-last-route", "announce delivery uses channel=last, which is fragile in multi-channel setups")

    if delivery_mode == "announce" and not delivery_channel:
        add("warn", "missing-delivery-channel", "announce delivery has no explicit channel")

    if delivery_mode == "announce" and delivery_channel not in {None, "last"} and not delivery_to:
        add("warn", "missing-delivery-target", "announce delivery has explicit channel but no explicit target")

    if delivery_mode == "webhook" and not delivery_to:
        add("error", "missing-webhook-target", "webhook delivery requires delivery.to")

    if schedule.get("kind") == "cron" and not schedule.get("tz"):
        add("warn", "missing-timezone", "recurring cron job is missing explicit timezone")

    if isinstance(timeout_seconds, int):
        if timeout_seconds < 120 and len(message) > 120:
            add("warn", "timeout-short", "timeoutSeconds looks short for a non-trivial prompt")
    elif payload_kind == "agentTurn":
        add("info", "timeout-implicit", "agentTurn job uses implicit timeout")

    last_error = ((job.get("state") or {}).get("lastError") or "") if isinstance(job.get("state"), dict) else ""
    if isinstance(last_error, str) and "Channel is required when multiple channels are configured" in last_error:
        add("error", "delivery-route-failed", "recent runs show multi-channel delivery route resolution failure")
    if isinstance(last_error, str) and "timed out" in last_error.lower():
        add("error", "recent-timeout", "recent runs timed out")

    return findings


def main():
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        data = load_jobs(path_arg)
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    jobs = data.get("jobs") if isinstance(data, dict) else None
    if not isinstance(jobs, list):
        print(json.dumps({"ok": False, "error": "expected { jobs: [...] } input"}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    results = []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        findings = classify_job(job)
        results.append(
            {
                "id": job.get("id"),
                "name": job.get("name"),
                "enabled": job.get("enabled"),
                "sessionTarget": job.get("sessionTarget"),
                "delivery": job.get("delivery"),
                "findings": findings,
            }
        )

    summary = {
        "jobs": len(results),
        "jobsWithFindings": sum(1 for r in results if r["findings"]),
        "errors": sum(1 for r in results for f in r["findings"] if f["severity"] == "error"),
        "warnings": sum(1 for r in results for f in r["findings"] if f["severity"] == "warn"),
        "infos": sum(1 for r in results for f in r["findings"] if f["severity"] == "info"),
    }

    print(json.dumps({"ok": True, "summary": summary, "results": results}, ensure_ascii=False, indent=2))
    raise SystemExit(0)


if __name__ == "__main__":
    main()
