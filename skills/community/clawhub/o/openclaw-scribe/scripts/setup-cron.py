#!/usr/bin/env python3
"""
Scribe setup — registers a nightly OpenClaw cron job to run scribe automatically.

Usage:
    python3 scripts/setup-cron.py

This script calls the OpenClaw Gateway API to register a cron job that runs
scribe every night at 23:30 (local timezone). The job runs in an isolated
session and writes memory/YYYY-MM-DD.md to your workspace.
"""

import json
import os
import sys
import subprocess
from pathlib import Path

GATEWAY_DEFAULT = "http://127.0.0.1:19000"
CONFIG_PATH = Path.home() / ".openclaw/openclaw.json"

CRON_JOB = {
    "name": "scribe-nightly",
    "schedule": {
        "kind": "cron",
        "expr": "30 23 * * *",
        "tz": "Asia/Shanghai",    # change to your timezone
    },
    "payload": {
        "kind": "agentTurn",
        "message": (
            "Run the scribe skill now. "
            "Execute: python3 skills/public/scribe/scripts/scribe.py — "
            "scan today's session logs from ~/.openclaw/agents/main/sessions/ "
            "and write structured memory to memory/YYYY-MM-DD.md in the workspace. "
            "Report how many messages were processed and where the file was written."
        ),
    },
    "sessionTarget": "isolated",
    "enabled": True,
}


def get_gateway_url() -> str:
    url = os.environ.get("OPENCLAW_GATEWAY_URL", "")
    if url:
        return url.rstrip("/")
    try:
        cfg = json.loads(CONFIG_PATH.read_text())
        gw = cfg.get("gateway", {})
        port = gw.get("port") or gw.get("httpPort") or 19000
        return f"http://127.0.0.1:{port}"
    except Exception:
        return GATEWAY_DEFAULT


def get_gateway_token() -> str:
    token = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")
    if token:
        return token
    try:
        cfg = json.loads(CONFIG_PATH.read_text())
        gw = cfg.get("gateway", {})
        # token may be at gateway.token or gateway.auth.token
        return gw.get("token") or gw.get("auth", {}).get("token", "")
    except Exception:
        return ""


def curl_json(method: str, url: str, token: str, data=None) -> dict:
    cmd = ["curl", "-s", "-X", method, url,
           "-H", "Content-Type: application/json",
           "-H", f"Authorization: Bearer {token}"]
    if data:
        cmd += ["-d", json.dumps(data)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr}")
    return json.loads(result.stdout)


def main():
    gateway = get_gateway_url()
    token = get_gateway_token()

    print(f"[setup] Gateway: {gateway}")

    if not token:
        print("[setup] ❌ No gateway token found.")
        print("        Set OPENCLAW_GATEWAY_TOKEN or check ~/.openclaw/openclaw.json")
        sys.exit(1)

    # Check if job already exists
    try:
        jobs = curl_json("GET", f"{gateway}/api/cron/jobs", token)
        existing = [j for j in jobs.get("jobs", []) if j.get("name") == "scribe-nightly"]
        if existing:
            print(f"[setup] ⚠️  A cron job named 'scribe-nightly' already exists (id: {existing[0].get('id')}).")
            answer = input("         Replace it? [y/N] ").strip().lower()
            if answer != "y":
                print("[setup] Aborted.")
                sys.exit(0)
            # Delete existing
            job_id = existing[0].get("id") or existing[0].get("jobId")
            curl_json("DELETE", f"{gateway}/api/cron/jobs/{job_id}", token)
            print(f"[setup] Deleted existing job {job_id}")
    except Exception as e:
        print(f"[setup] ⚠️  Could not list existing jobs: {e}")

    # Register new job
    try:
        resp = curl_json("POST", f"{gateway}/api/cron/jobs", token, CRON_JOB)
        job_id = resp.get("id") or resp.get("jobId") or resp.get("job", {}).get("id")
        print(f"[setup] ✅ Cron job registered! id={job_id}")
        print(f"         Schedule: every night at 23:30 (Asia/Shanghai)")
        print(f"         Scribe will write to: memory/YYYY-MM-DD.md")
        print()
        print("To run immediately:  python3 skills/public/scribe/scripts/scribe.py")
        print("To change timezone:  edit CRON_JOB['schedule']['tz'] in this script")
    except Exception as e:
        print(f"[setup] ❌ Failed to register cron job: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
