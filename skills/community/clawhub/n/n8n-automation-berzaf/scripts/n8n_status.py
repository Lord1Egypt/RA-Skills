#!/usr/bin/env python3
"""
n8n Status Checker for OpenClaw
Author: berzaf (Berzaf AI Automation)
Version: 1.0.0

Quick status check — shows all 8 workflow statuses
in a clean dashboard format. Called by OpenClaw when
user types "n8n status" or "/n8n-status".
Reads credentials from environment variables only.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime


def get_config():
    api_key = os.environ.get("N8N_API_KEY")
    base_url = os.environ.get("N8N_WEBHOOK_BASE_URL", "").rstrip("/")
    return api_key, base_url


def ping(url, api_key, timeout=8):
    """Ping a URL and return (ok, response_ms)."""
    headers = {
        "Content-Type": "application/json",
        "X-N8N-API-KEY": api_key or "",
    }
    payload = json.dumps({"ping": True}).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, headers=headers, method="POST"
    )

    import time
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout):
            ms = int((time.time() - start) * 1000)
            return True, ms
    except urllib.error.HTTPError as e:
        ms = int((time.time() - start) * 1000)
        # Non-404 = endpoint exists
        return (e.code != 404), ms
    except Exception:
        ms = int((time.time() - start) * 1000)
        return False, ms


def main():
    api_key, base_url = get_config()

    if not api_key or not base_url:
        print(json.dumps({
            "status": "error",
            "message": "N8N_API_KEY or N8N_WEBHOOK_BASE_URL not set",
            "fix": "export N8N_API_KEY=... && export N8N_WEBHOOK_BASE_URL=..."
        }, indent=2))
        sys.exit(1)

    workflows = [
        ("lead-nurture",       "Lead Nurture Email Sequence"),
        ("social-post",        "Social Media Auto-Post"),
        ("meeting-followup",   "Meeting Follow-Up"),
        ("crm-update",         "CRM Contact Update"),
        ("competitor-monitor", "Competitor Monitor Report"),
        ("invoice-reminder",   "Invoice Reminder"),
        ("content-repurpose",  "Content Repurpose"),
        ("daily-briefing",     "Daily Business Briefing"),
    ]

    # Check health endpoint first
    health_ok, health_ms = ping(f"{base_url}/health", api_key)

    report = {
        "instance": base_url,
        "checked_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "instance_status": "online" if health_ok else "offline",
        "response_ms": health_ms,
        "workflows": []
    }

    all_ok = health_ok

    for path, name in workflows:
        url = f"{base_url}/{path}"
        ok, ms = ping(url, api_key)
        report["workflows"].append({
            "name": name,
            "path": f"/{path}",
            "status": "active" if ok else "not found",
            "response_ms": ms
        })
        if not ok:
            all_ok = False

    report["all_workflows_active"] = all_ok

    # Pretty print for OpenClaw
    print("\n⚡ n8n + OpenClaw Status Report")
    print("─" * 40)
    status_icon = "✅" if health_ok else "❌"
    print(f"{status_icon} Instance: {base_url}")
    print(f"   Response: {health_ms}ms")
    print(f"   Checked:  {report['checked_at']}")
    print()

    for wf in report["workflows"]:
        icon = "✅" if wf["status"] == "active" else "❌"
        print(f"{icon} {wf['name']}")
        print(f"   {wf['path']}  ({wf['response_ms']}ms)")

    print()
    if all_ok:
        print("✅ All 8 workflows active. Ready to use!")
    else:
        print("⚠️  Some workflows inactive. Run:")
        print("   python3 scripts/n8n_validator.py")

    print()

    # Also output JSON for programmatic use
    return report


if __name__ == "__main__":
    report = main()
    # Optionally output raw JSON with --json flag
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
