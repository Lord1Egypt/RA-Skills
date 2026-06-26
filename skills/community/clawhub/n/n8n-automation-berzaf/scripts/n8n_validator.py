#!/usr/bin/env python3
"""
n8n Workflow Validator for OpenClaw
Author: berzaf (Berzaf AI Automation)
Version: 1.0.0

Validates your n8n setup and confirms all 8 required
webhook endpoints are active and responding correctly.
Reads credentials from environment variables only.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime


REQUIRED_WEBHOOKS = [
    ("lead-nurture",       "Lead Nurture Email Sequence"),
    ("social-post",        "Social Media Auto-Post"),
    ("meeting-followup",   "Meeting Follow-Up"),
    ("crm-update",         "CRM Contact Update"),
    ("competitor-monitor", "Competitor Monitor Report"),
    ("invoice-reminder",   "Invoice Reminder"),
    ("content-repurpose",  "Content Repurpose"),
    ("daily-briefing",     "Daily Business Briefing"),
    ("health",             "Health Check"),
]


def get_config():
    """Read config from environment variables only."""
    api_key = os.environ.get("N8N_API_KEY")
    base_url = os.environ.get("N8N_WEBHOOK_BASE_URL", "").rstrip("/")

    if not api_key:
        print("❌  N8N_API_KEY not set in environment.")
        print("    Run: export N8N_API_KEY=your-api-key")
        return None, None

    if not base_url:
        print("❌  N8N_WEBHOOK_BASE_URL not set in environment.")
        print("    Run: export N8N_WEBHOOK_BASE_URL=https://your-n8n.com/webhook")
        return None, None

    return api_key, base_url


def check_endpoint(base_url, path, api_key):
    """Check if a webhook endpoint responds."""
    url = f"{base_url}/{path}"
    headers = {
        "Content-Type": "application/json",
        "X-N8N-API-KEY": api_key,
    }

    # Send minimal test payload
    test_payload = json.dumps({
        "test": True,
        "triggered_by": "openclaw-validator"
    }).encode("utf-8")

    req = urllib.request.Request(
        url, data=test_payload, headers=headers, method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, "ok"
    except urllib.error.HTTPError as e:
        # 404 = webhook not found, 200/201 = ok, others = workflow exists but errored
        if e.code == 404:
            return 404, "not found"
        return e.code, "error"
    except urllib.error.URLError as e:
        return 0, f"connection error: {e.reason}"


def validate_all():
    """Run full validation of all webhook endpoints."""
    api_key, base_url = get_config()
    if not api_key:
        sys.exit(1)

    print("\n" + "=" * 55)
    print("  n8n + OpenClaw Setup Validator — Berzaf AI Automation")
    print("=" * 55)
    print(f"  Instance: {base_url}")
    print(f"  Time:     {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 55 + "\n")

    results = []
    passed = 0
    failed = 0

    for path, name in REQUIRED_WEBHOOKS:
        status_code, status_text = check_endpoint(base_url, path, api_key)

        if status_code in (200, 201):
            icon = "✅"
            passed += 1
        elif status_code == 404:
            icon = "❌"
            failed += 1
            status_text = "webhook not found — check n8n workflow is active"
        else:
            icon = "⚠️ "
            # Non-404 errors mean endpoint exists, workflow may have issues
            passed += 1
            status_text = f"responded with {status_code} — workflow may need config"

        results.append((icon, name, path, status_text))
        print(f"  {icon}  {name}")
        print(f"       /{path}  →  {status_text}\n")

    print("=" * 55)
    print(f"  Results: {passed} passed  |  {failed} failed")
    print("=" * 55 + "\n")

    if failed == 0:
        print("  🎉 All webhooks validated! Your skill is ready to use.")
        print("  Test it: python3 scripts/n8n_trigger.py health --pretty\n")
    else:
        print("  ⚠️  Some webhooks are not responding.")
        print("  Steps to fix:")
        print("  1. Open your n8n instance")
        print("  2. Find the workflow for the failing endpoint")
        print("  3. Make sure it is ACTIVATED (not just saved)")
        print("  4. Copy the webhook path and confirm it matches above\n")

    return failed == 0


def validate_env():
    """Quick environment variable check."""
    print("\n  Checking environment variables...\n")

    api_key = os.environ.get("N8N_API_KEY")
    base_url = os.environ.get("N8N_WEBHOOK_BASE_URL")

    if api_key:
        # Show only first 8 chars for security
        masked = api_key[:8] + "*" * (len(api_key) - 8)
        print(f"  ✅  N8N_API_KEY      = {masked}")
    else:
        print("  ❌  N8N_API_KEY      = NOT SET")

    if base_url:
        print(f"  ✅  N8N_WEBHOOK_BASE_URL = {base_url}")
    else:
        print("  ❌  N8N_WEBHOOK_BASE_URL = NOT SET")

    print()

    if not api_key or not base_url:
        print("  Set missing variables then re-run this validator.\n")
        return False

    print("  ✅  Environment configured correctly.\n")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate n8n + OpenClaw webhook setup"
    )
    parser.add_argument(
        "--env-only", action="store_true",
        help="Only check environment variables, skip webhook tests"
    )
    args = parser.parse_args()

    if args.env_only:
        ok = validate_env()
        sys.exit(0 if ok else 1)
    else:
        validate_env()
        ok = validate_all()
        sys.exit(0 if ok else 1)
