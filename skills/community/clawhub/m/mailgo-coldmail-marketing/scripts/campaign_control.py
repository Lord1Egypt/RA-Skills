#!/usr/bin/env python3
"""
Control Mailgo campaign status: activate, pause, delete, list, or get info.

Usage:
    python3 campaign_control.py activate <campaignId>
    python3 campaign_control.py pause <campaignId>
    python3 campaign_control.py delete <campaignId>
    python3 campaign_control.py list [--status 1,0] [--name "search"] [--page 1] [--size 20]
    python3 campaign_control.py info <campaignId>

Requires:
    MAILGO_API_KEY environment variable

Output:
    JSON result on stdout. Progress/errors on stderr.
"""

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

_ssl_ctx = ssl.create_default_context()
# Do NOT disable certificate verification — MITM attacks would allow token theft

BASE = "https://api.leadsnavi.com"
PREFIX = "/mcp/mailgo-logical"

STATUS_NAMES = {-1: "DRAFT", 0: "PAUSE", 1: "ACTIVE", 2: "COMPLETE", 3: "ERROR"}
OPERATE_MAP = {"activate": 1, "pause": 0, "delete": 2}


def headers(api_key):
    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "mailgo-mcp-server/1.0 (https://github.com/netease-im/leadsnavi-mcp-server)",
    }


def request(api_key, method, path, body=None):
    url = f"{BASE}{PREFIX}{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers(api_key), method=method)
    print(f"{method} {url}", file=sys.stderr)
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if not result.get("success", False):
                print(f"API error: {result.get('message', 'unknown')}", file=sys.stderr)
                sys.exit(1)
            return result
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {err[:500]}", file=sys.stderr)
        sys.exit(1)


def cmd_operate(api_key, action, campaign_id):
    status_code = OPERATE_MAP[action]
    result = request(api_key, "POST", "/api/biz/mailgo/campaign/operate", {
        "campaignId": int(campaign_id),
        "status": status_code,
    })
    action_past = {"activate": "activated", "pause": "paused", "delete": "deleted"}[action]
    summary = {
        "campaignId": campaign_id,
        "action": action,
        "result": result.get("data"),
        "message": f"Campaign {campaign_id} {action_past} successfully",
    }
    print(json.dumps(summary, indent=2))


def cmd_list(api_key, status_list, name, page, size):
    body = {"page": page, "size": size}
    if status_list:
        body["statusList"] = status_list
    if name:
        body["name"] = name
    result = request(api_key, "POST", "/api/biz/mailgo/campaign/list", body)
    data = result.get("data", {})
    campaigns = data.get("campaigns", [])

    output = {"total": data.get("total", 0), "campaigns": []}
    for c in campaigns:
        status_code = c.get("status", -1)
        output["campaigns"].append({
            "campaignId": c.get("campaignId"),
            "campaignName": c.get("campaignName"),
            "status": STATUS_NAMES.get(status_code, f"UNKNOWN({status_code})"),
            "statusCode": status_code,
            "createTime": c.get("createTime"),
            "leads": c.get("leads", 0),
            "delivered": c.get("delivered", 0),
            "opened": c.get("opened", 0),
            "replied": c.get("replied", 0),
            "clicked": c.get("clicked", 0),
            "progress": c.get("progress", 0),
        })

    print(json.dumps(output, indent=2))
    print(f"\nShowing {len(campaigns)} of {data.get('total', 0)} campaigns", file=sys.stderr)


def cmd_info(api_key, campaign_id):
    result = request(api_key, "GET", f"/api/biz/mailgo/campaign/info?campaignId={campaign_id}")
    data = result.get("data", {})
    status_code = data.get("status", -1)

    summary = {
        "campaignId": data.get("campaignId"),
        "campaignName": data.get("campaignName"),
        "status": STATUS_NAMES.get(status_code, f"UNKNOWN({status_code})"),
        "statusCode": status_code,
        "senderEmails": [e.get("email") for e in (data.get("basicInfo") or {}).get("senderEmails", [])],
        "scheduleRule": data.get("scheduleRule"),
        "limitRule": data.get("limitRule"),
        "rounds": len((data.get("sequenceInfo") or {}).get("mailInfos", [])),
    }
    print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Mailgo campaign control")
    sub = parser.add_subparsers(dest="command", required=True)

    for action in ("activate", "pause", "delete"):
        p = sub.add_parser(action, help=f"{action.capitalize()} a campaign")
        p.add_argument("campaign_id", help="Campaign ID")

    p_list = sub.add_parser("list", help="List campaigns")
    p_list.add_argument("--status", default="", help="Comma-separated status codes")
    p_list.add_argument("--name", default="", help="Search by name")
    p_list.add_argument("--page", type=int, default=1, help="Page number")
    p_list.add_argument("--size", type=int, default=20, help="Page size")

    p_info = sub.add_parser("info", help="Get campaign detail")
    p_info.add_argument("campaign_id", help="Campaign ID")

    args = parser.parse_args()

    api_key = os.environ.get("MAILGO_API_KEY")
    if not api_key:
        print("Error: MAILGO_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if args.command in ("activate", "pause", "delete"):
        cmd_operate(api_key, args.command, args.campaign_id)
    elif args.command == "list":
        status_list = [int(s.strip()) for s in args.status.split(",") if s.strip()] if args.status else None
        cmd_list(api_key, status_list, args.name, args.page, args.size)
    elif args.command == "info":
        cmd_info(api_key, args.campaign_id)


if __name__ == "__main__":
    main()
