#!/usr/bin/env python3
"""
n8n API Client for OpenClaw
Author: berzaf (Berzaf AI Automation)
Version: 1.0.0

Triggers and manages n8n workflows via the n8n REST API.
All credentials are read from environment variables only.
No secrets are stored in this file.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime


def get_config():
    """Read config from environment variables only."""
    api_key = os.environ.get("N8N_API_KEY")
    base_url = os.environ.get("N8N_WEBHOOK_BASE_URL", "").rstrip("/")

    if not api_key:
        print("ERROR: N8N_API_KEY environment variable not set.")
        print("Run: export N8N_API_KEY=your-api-key")
        sys.exit(1)

    if not base_url:
        print("ERROR: N8N_WEBHOOK_BASE_URL environment variable not set.")
        print("Run: export N8N_WEBHOOK_BASE_URL=https://your-n8n.com/webhook")
        sys.exit(1)

    return api_key, base_url


def make_request(url, method="GET", data=None, api_key=None):
    """Make an HTTP request to n8n."""
    headers = {
        "Content-Type": "application/json",
        "X-N8N-API-KEY": api_key or "",
    }

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Details: {error_body}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        print("Check that your n8n instance is running and N8N_WEBHOOK_BASE_URL is correct.")
        sys.exit(1)


def trigger_workflow(webhook_path, payload, pretty=False):
    """Trigger a workflow via webhook."""
    api_key, base_url = get_config()

    # Build full webhook URL
    url = f"{base_url}/{webhook_path.lstrip('/')}"

    # Add metadata
    payload["triggered_by"] = "openclaw"
    payload["triggered_at"] = datetime.utcnow().isoformat() + "Z"

    result = make_request(url, method="POST", data=payload, api_key=api_key)

    if pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))

    return result


def health_check(pretty=False):
    """Check if n8n instance is reachable."""
    api_key, base_url = get_config()
    url = f"{base_url}/health"

    try:
        result = make_request(url, method="GET", api_key=api_key)
        status = {
            "status": "ok",
            "instance_url": base_url,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "response": result,
        }
    except SystemExit:
        status = {
            "status": "error",
            "instance_url": base_url,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    if pretty:
        print(json.dumps(status, indent=2))
    else:
        print(json.dumps(status))

    return status


def trigger_lead_nurture(first_name, email, source="", pretty=False):
    """Trigger lead nurture email sequence."""
    payload = {
        "first_name": first_name,
        "email": email,
        "source": source,
    }
    return trigger_workflow("lead-nurture", payload, pretty)


def trigger_social_post(content, platforms=None, schedule_time=None, pretty=False):
    """Trigger social media post."""
    payload = {
        "content": content,
        "platforms": platforms or ["linkedin", "x"],
        "schedule_time": schedule_time,
    }
    return trigger_workflow("social-post", payload, pretty)


def trigger_meeting_followup(contact_name, contact_email, meeting_topic,
                              action_items=None, next_step=None, pretty=False):
    """Trigger meeting follow-up email."""
    payload = {
        "contact_name": contact_name,
        "contact_email": contact_email,
        "meeting_topic": meeting_topic,
        "action_items": action_items or [],
        "next_step": next_step,
        "meeting_date": datetime.utcnow().strftime("%Y-%m-%d"),
    }
    return trigger_workflow("meeting-followup", payload, pretty)


def trigger_crm_update(contact_name, notes, status="lead",
                        contact_email=None, follow_up_date=None, pretty=False):
    """Trigger CRM contact update."""
    payload = {
        "contact_name": contact_name,
        "contact_email": contact_email,
        "notes": notes,
        "status": status,
        "follow_up_date": follow_up_date,
        "logged_at": datetime.utcnow().isoformat() + "Z",
    }
    return trigger_workflow("crm-update", payload, pretty)


def trigger_competitor_monitor(report_type="summary", add_url=None, pretty=False):
    """Trigger competitor monitoring report."""
    payload = {
        "report_type": report_type,
        "add_competitor_url": add_url,
    }
    return trigger_workflow("competitor-monitor", payload, pretty)


def trigger_invoice_reminder(client_name, client_email, invoice_number,
                               amount, due_date, reminder_type="first", pretty=False):
    """Trigger invoice reminder email."""
    valid_types = ["first", "second", "final"]
    if reminder_type not in valid_types:
        print(f"ERROR: reminder_type must be one of {valid_types}")
        sys.exit(1)

    payload = {
        "client_name": client_name,
        "client_email": client_email,
        "invoice_number": invoice_number,
        "amount": float(amount),
        "due_date": due_date,
        "reminder_type": reminder_type,
    }
    return trigger_workflow("invoice-reminder", payload, pretty)


def trigger_content_repurpose(url, formats=None, brand_voice="", pretty=False):
    """Trigger content repurposing workflow."""
    payload = {
        "url": url,
        "formats": formats or ["thread", "linkedin", "email", "hook"],
        "brand_voice": brand_voice,
    }
    return trigger_workflow("content-repurpose", payload, pretty)


def trigger_daily_briefing(sections=None, pretty=False):
    """Trigger daily business briefing."""
    payload = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "sections": sections or ["leads", "deals", "social", "email", "priorities"],
    }
    return trigger_workflow("daily-briefing", payload, pretty)


def main():
    parser = argparse.ArgumentParser(
        description="n8n Automation Client for OpenClaw — Berzaf AI Automation"
    )
    subparsers = parser.add_subparsers(dest="command")

    # health
    subparsers.add_parser("health", help="Check n8n instance connection")

    # lead-nurture
    p_nurture = subparsers.add_parser("lead-nurture", help="Trigger lead nurture sequence")
    p_nurture.add_argument("--name", required=True, help="Contact first name")
    p_nurture.add_argument("--email", required=True, help="Contact email")
    p_nurture.add_argument("--source", default="", help="Lead source")
    p_nurture.add_argument("--pretty", action="store_true")

    # social-post
    p_social = subparsers.add_parser("social-post", help="Post to social media")
    p_social.add_argument("--content", required=True, help="Post content")
    p_social.add_argument("--platforms", nargs="+", default=["linkedin", "x"])
    p_social.add_argument("--schedule", default=None, help="Schedule time ISO format")
    p_social.add_argument("--pretty", action="store_true")

    # meeting-followup
    p_followup = subparsers.add_parser("meeting-followup", help="Send meeting follow-up")
    p_followup.add_argument("--name", required=True)
    p_followup.add_argument("--email", required=True)
    p_followup.add_argument("--topic", required=True)
    p_followup.add_argument("--actions", nargs="+", default=[])
    p_followup.add_argument("--next-step", default=None)
    p_followup.add_argument("--pretty", action="store_true")

    # crm-update
    p_crm = subparsers.add_parser("crm-update", help="Update CRM contact")
    p_crm.add_argument("--name", required=True)
    p_crm.add_argument("--notes", required=True)
    p_crm.add_argument("--status", default="lead",
                        choices=["lead", "warm", "hot", "closed-won", "closed-lost"])
    p_crm.add_argument("--email", default=None)
    p_crm.add_argument("--follow-up", default=None)
    p_crm.add_argument("--pretty", action="store_true")

    # competitor-monitor
    p_comp = subparsers.add_parser("competitor-monitor", help="Run competitor report")
    p_comp.add_argument("--type", default="summary", choices=["summary", "full"])
    p_comp.add_argument("--add-url", default=None)
    p_comp.add_argument("--pretty", action="store_true")

    # invoice-reminder
    p_inv = subparsers.add_parser("invoice-reminder", help="Send invoice reminder")
    p_inv.add_argument("--client-name", required=True)
    p_inv.add_argument("--client-email", required=True)
    p_inv.add_argument("--invoice-number", required=True)
    p_inv.add_argument("--amount", required=True, type=float)
    p_inv.add_argument("--due-date", required=True)
    p_inv.add_argument("--type", default="first", choices=["first", "second", "final"])
    p_inv.add_argument("--pretty", action="store_true")

    # content-repurpose
    p_repurpose = subparsers.add_parser("content-repurpose", help="Repurpose content")
    p_repurpose.add_argument("--url", required=True)
    p_repurpose.add_argument("--formats", nargs="+",
                              default=["thread", "linkedin", "email", "hook"])
    p_repurpose.add_argument("--voice", default="")
    p_repurpose.add_argument("--pretty", action="store_true")

    # daily-briefing
    p_brief = subparsers.add_parser("daily-briefing", help="Get daily briefing")
    p_brief.add_argument("--sections", nargs="+",
                          default=["leads", "deals", "social", "email", "priorities"])
    p_brief.add_argument("--pretty", action="store_true")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "health":
        health_check(pretty=True)

    elif args.command == "lead-nurture":
        trigger_lead_nurture(args.name, args.email, args.source, args.pretty)

    elif args.command == "social-post":
        trigger_social_post(args.content, args.platforms, args.schedule, args.pretty)

    elif args.command == "meeting-followup":
        trigger_meeting_followup(args.name, args.email, args.topic,
                                  args.actions, args.next_step, args.pretty)

    elif args.command == "crm-update":
        trigger_crm_update(args.name, args.notes, args.status,
                            args.email, args.follow_up, args.pretty)

    elif args.command == "competitor-monitor":
        trigger_competitor_monitor(args.type, args.add_url, args.pretty)

    elif args.command == "invoice-reminder":
        trigger_invoice_reminder(args.client_name, args.client_email,
                                  args.invoice_number, args.amount,
                                  args.due_date, args.type, args.pretty)

    elif args.command == "content-repurpose":
        trigger_content_repurpose(args.url, args.formats, args.voice, args.pretty)

    elif args.command == "daily-briefing":
        trigger_daily_briefing(args.sections, args.pretty)


if __name__ == "__main__":
    main()
