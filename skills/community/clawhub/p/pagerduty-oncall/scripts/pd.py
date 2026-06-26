#!/usr/bin/env python3
"""
PagerDuty CLI for OpenClaw agents.
Usage: pd.py <command> [options]
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

API_BASE = "https://api.pagerduty.com"
EVENTS_V2 = "https://events.pagerduty.com/v2/enqueue"


def get_headers(require_from=False):
    key = os.environ.get("PAGERDUTY_API_KEY")
    if not key:
        print("ERROR: PAGERDUTY_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    headers = {
        "Authorization": f"Token token={key}",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Content-Type": "application/json",
    }
    if require_from:
        from_email = os.environ.get("PAGERDUTY_FROM_EMAIL", "")
        if from_email:
            headers["From"] = from_email
    return headers


def api_request(method, path, body=None, headers=None):
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers or get_headers(), method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def cmd_incidents(args):
    statuses = getattr(args, 'status', 'triggered,acknowledged')
    params = f"?statuses[]={'&statuses[]='.join(statuses.split(','))}&limit={args.limit}"
    if hasattr(args, 'service_id') and args.service_id:
        params += f"&service_ids[]={args.service_id}"
    result = api_request("GET", f"/incidents{params}")
    incidents = result.get("incidents", [])
    if not incidents:
        print("No incidents found.")
        return
    for inc in incidents:
        svc = inc.get("service", {}).get("summary", "unknown")
        print(f"[{inc['status'].upper()}] {inc['id']} — {inc['title']}")
        print(f"  Service: {svc} | Urgency: {inc.get('urgency','?')} | Created: {inc.get('created_at','?')[:19]}")
        if inc.get("assignments"):
            assignee = inc["assignments"][0].get("assignee", {}).get("summary", "?")
            print(f"  Assigned to: {assignee}")
        print()
    print(f"Total: {len(incidents)} incident(s)")


def cmd_get(args):
    result = api_request("GET", f"/incidents/{args.id}")
    inc = result.get("incident", {})
    print(json.dumps(inc, indent=2))


def cmd_acknowledge(args):
    headers = get_headers(require_from=True)
    body = {"incidents": [{"id": args.id, "type": "incident_reference", "status": "acknowledged"}]}
    result = api_request("PUT", "/incidents", body=body, headers=headers)
    incs = result.get("incidents", [])
    if incs:
        print(f"✓ Acknowledged: {incs[0]['id']} — {incs[0].get('status','?')}")
    else:
        print("Done.")


def cmd_resolve(args):
    headers = get_headers(require_from=True)
    body = {"incidents": [{"id": args.id, "type": "incident_reference", "status": "resolved"}]}
    result = api_request("PUT", "/incidents", body=body, headers=headers)
    incs = result.get("incidents", [])
    if incs:
        print(f"✓ Resolved: {incs[0]['id']} — {incs[0].get('status','?')}")
    else:
        print("Done.")


def cmd_trigger(args):
    """Trigger via Events API v2."""
    integration_key = os.environ.get("PAGERDUTY_INTEGRATION_KEY", getattr(args, "service_key", ""))
    if not integration_key:
        print("ERROR: Provide --service-key or set PAGERDUTY_INTEGRATION_KEY", file=sys.stderr)
        sys.exit(1)
    payload = {
        "routing_key": integration_key,
        "event_action": "trigger",
        "payload": {
            "summary": args.description,
            "severity": getattr(args, "severity", "critical"),
            "source": "pagerduty-oncall-skill",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        EVENTS_V2,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            print(f"✓ Triggered: dedup_key={result.get('dedup_key','?')}")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def cmd_oncall(args):
    params = "?include[]=users&limit=25"
    if hasattr(args, 'schedule_id') and args.schedule_id:
        params += f"&schedule_ids[]={args.schedule_id}"
    result = api_request("GET", f"/oncalls{params}")
    oncalls = result.get("oncalls", [])
    if not oncalls:
        print("No on-call entries found.")
        return
    seen = set()
    for oc in oncalls:
        user = oc.get("user", {}).get("summary", "?")
        policy = oc.get("escalation_policy", {}).get("summary", "?")
        sched = oc.get("schedule", {})
        sched_name = sched.get("summary", "N/A") if sched else "N/A"
        key = f"{user}|{policy}"
        if key not in seen:
            seen.add(key)
            print(f"👤 {user}")
            print(f"   Policy: {policy} | Schedule: {sched_name}")
            start = oc.get("start", "")
            end = oc.get("end", "")
            if start:
                print(f"   On-call: {start[:16]} → {end[:16] if end else 'ongoing'}")
            print()


def cmd_services(args):
    result = api_request("GET", f"/services?limit={args.limit}")
    for svc in result.get("services", []):
        print(f"{svc['id']} — {svc['name']} [{svc.get('status','?')}]")
        if svc.get("description"):
            print(f"  {svc['description'][:80]}")


def cmd_escalations(args):
    result = api_request("GET", "/escalation_policies?limit=25")
    for ep in result.get("escalation_policies", []):
        print(f"{ep['id']} — {ep['name']}")
        for i, rule in enumerate(ep.get("escalation_rules", []), 1):
            delay = rule.get("escalation_delay_in_minutes", 0)
            targets = [t.get("summary","?") for t in rule.get("targets", [])]
            print(f"  Level {i} ({delay}min): {', '.join(targets)}")


def cmd_note(args):
    headers = get_headers(require_from=True)
    body = {"note": {"content": args.message}}
    result = api_request("POST", f"/incidents/{args.id}/notes", body=body, headers=headers)
    note = result.get("note", {})
    print(f"✓ Note added: {note.get('id','?')} at {note.get('created_at','?')[:19]}")


def cmd_snooze(args):
    headers = get_headers(require_from=True)
    body = {"duration": args.duration}
    result = api_request("POST", f"/incidents/{args.id}/snooze", body=body, headers=headers)
    inc = result.get("incident", {})
    print(f"✓ Snoozed: {inc.get('id','?')} until snooze expires ({args.duration}s)")


def cmd_reassign(args):
    headers = get_headers(require_from=True)
    body = {
        "incidents": [{
            "id": args.id,
            "type": "incident_reference",
            "assignments": [{"assignee": {"id": args.user_id, "type": "user_reference"}}]
        }]
    }
    result = api_request("PUT", "/incidents", body=body, headers=headers)
    incs = result.get("incidents", [])
    if incs:
        print(f"✓ Reassigned: {incs[0]['id']}")


def main():
    parser = argparse.ArgumentParser(description="PagerDuty CLI for OpenClaw agents")
    sub = parser.add_subparsers(dest="command")

    p_incidents = sub.add_parser("incidents", help="List incidents")
    p_incidents.add_argument("--status", default="triggered,acknowledged")
    p_incidents.add_argument("--service-id")
    p_incidents.add_argument("--limit", type=int, default=25)

    p_get = sub.add_parser("get", help="Get incident details")
    p_get.add_argument("--id", required=True)

    p_ack = sub.add_parser("acknowledge", help="Acknowledge incident")
    p_ack.add_argument("--id", required=True)

    p_resolve = sub.add_parser("resolve", help="Resolve incident")
    p_resolve.add_argument("--id", required=True)

    p_trigger = sub.add_parser("trigger", help="Trigger new incident")
    p_trigger.add_argument("--service-key", required=True)
    p_trigger.add_argument("--description", required=True)
    p_trigger.add_argument("--severity", default="critical",
                           choices=["critical", "error", "warning", "info"])

    p_oncall = sub.add_parser("oncall", help="Who is on-call")
    p_oncall.add_argument("--schedule-id")

    p_svc = sub.add_parser("services", help="List services")
    p_svc.add_argument("--limit", type=int, default=25)

    sub.add_parser("escalations", help="List escalation policies")

    p_note = sub.add_parser("note", help="Add note to incident")
    p_note.add_argument("--id", required=True)
    p_note.add_argument("--message", required=True)

    p_snooze = sub.add_parser("snooze", help="Snooze incident")
    p_snooze.add_argument("--id", required=True)
    p_snooze.add_argument("--duration", type=int, default=3600, help="Seconds to snooze")

    p_reassign = sub.add_parser("reassign", help="Reassign incident")
    p_reassign.add_argument("--id", required=True)
    p_reassign.add_argument("--user-id", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "incidents": cmd_incidents,
        "get": cmd_get,
        "acknowledge": cmd_acknowledge,
        "resolve": cmd_resolve,
        "trigger": cmd_trigger,
        "oncall": cmd_oncall,
        "services": cmd_services,
        "escalations": cmd_escalations,
        "note": cmd_note,
        "snooze": cmd_snooze,
        "reassign": cmd_reassign,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
