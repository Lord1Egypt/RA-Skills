#!/usr/bin/env python3
"""
AI Report Intelligence — CLI Helper

A thin CLI wrapper for the RealMarket AI Report Service. Designed for use by
OpenClaw agents and human developers alike.

Usage:
    python3 aireport.py generate --ticker TSLA --user-id user@test.com [--user-tier PRO]
    python3 aireport.py status --job-id <job_id>
    python3 aireport.py report --user-id user@test.com --ticker TSLA --trading-day 2026-03-25 --report-id rpt-456
    python3 aireport.py report --job-id <job_id> --format markdown
    python3 aireport.py history --ticker TSLA --trading-day 2026-03-25 [--user-id user@test.com]
    python3 aireport.py summary --user-id user@test.com --trading-day 2026-03-25
    python3 aireport.py quota --user-id user@test.com [--tier PRO]
    python3 aireport.py eligibility --ticker TSLA --user-id user@test.com [--user-tier PRO]
    python3 aireport.py health

Reads AI_API_TOKEN from the environment.
Outputs JSON to stdout for piping through jq or agent parsing.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date

API_BASE = "https://ai-service-production-b44b.up.railway.app"


def get_api_token() -> str:
    """Read API token from environment."""
    token = os.environ.get("AI_API_TOKEN", "")
    if not token:
        print(
            json.dumps({"error": "AI_API_TOKEN environment variable not set"}),
            file=sys.stderr,
        )
        sys.exit(1)
    return token


def api_request(method: str, path: str, token: str, body: dict = None) -> dict:
    """Make an authenticated request to the AI service."""
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode() if e.fp else ""
        try:
            err = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            err = {"detail": raw or e.reason}
        print(
            json.dumps({"error": f"HTTP {e.code}", "detail": err}, indent=2),
            file=sys.stderr,
        )
        sys.exit(1)
    except urllib.error.URLError as e:
        print(
            json.dumps({"error": "Connection failed", "detail": str(e.reason)}),
            file=sys.stderr,
        )
        sys.exit(1)


def api_request_raw(method: str, path: str, token: str) -> str:
    """Make an authenticated request and return raw text (for markdown)."""
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read().decode()
    except urllib.error.HTTPError as e:
        raw = e.read().decode() if e.fp else ""
        try:
            err = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            err = {"detail": raw or e.reason}
        print(
            json.dumps({"error": f"HTTP {e.code}", "detail": err}, indent=2),
            file=sys.stderr,
        )
        sys.exit(1)
    except urllib.error.URLError as e:
        print(
            json.dumps({"error": "Connection failed", "detail": str(e.reason)}),
            file=sys.stderr,
        )
        sys.exit(1)


# ─── Subcommands ───────────────────────────────────────────────────────────


def cmd_generate(args, token: str):
    """Enqueue a report generation job."""
    orders = []
    if args.orders_file:
        with open(args.orders_file, "r") as f:
            orders = json.load(f)

    body = {
        "user_id": args.user_id,
        "user_tier": args.user_tier,
        "ticker": args.ticker.upper(),
        "session_date": args.session_date or date.today().isoformat(),
        "session_type": args.session_type,
        "large_orders": orders,
    }
    data = api_request("POST", "/reports", token, body)
    print(json.dumps(data, indent=2))


def cmd_status(args, token: str):
    """Poll job status."""
    data = api_request("GET", f"/reports/{args.job_id}", token)
    print(json.dumps(data, indent=2))


def cmd_report(args, token: str):
    """Fetch a completed report."""
    fmt = (args.format or "json").lower()

    if args.job_id:
        # Mode B: by job_id + artifact type
        if fmt == "markdown":
            text = api_request_raw("GET", f"/reports/{args.job_id}/artifact/md", token)
            print(text)
        else:
            data = api_request("GET", f"/reports/{args.job_id}/artifact/json", token)
            print(json.dumps(data, indent=2))
    else:
        # Mode A: by report metadata
        if not all([args.user_id, args.ticker, args.trading_day, args.report_id]):
            print(
                json.dumps(
                    {
                        "error": "Either --job-id or all of --user-id, --ticker, --trading-day, --report-id are required"
                    }
                ),
                file=sys.stderr,
            )
            sys.exit(1)
        params = urllib.request.quote(
            f"user_id={args.user_id}&ticker={args.ticker.upper()}"
            f"&trading_day={args.trading_day}&report_id={args.report_id}",
            safe="=&",
        )
        data = api_request("GET", f"/reports/by-id?{params}", token)
        print(json.dumps(data, indent=2))


def cmd_history(args, token: str):
    """List reports for a ticker+day."""
    params = f"ticker={args.ticker.upper()}&trading_day={args.trading_day}"
    if args.user_id:
        params += f"&user_id={args.user_id}"
    data = api_request("GET", f"/reports/history?{params}", token)
    print(json.dumps(data, indent=2))


def cmd_summary(args, token: str):
    """Per-ticker summary for a user+day."""
    params = f"user_id={args.user_id}&trading_day={args.trading_day}"
    data = api_request("GET", f"/reports/history/summary?{params}", token)
    print(json.dumps(data, indent=2))


def cmd_quota(args, token: str):
    """Check credit usage."""
    tier = args.tier or "FREE"
    params = f"user_id={args.user_id}&tier={tier}"
    data = api_request("GET", f"/quotas?{params}", token)
    print(json.dumps(data, indent=2))


def cmd_eligibility(args, token: str):
    """Pre-check if report generation is allowed."""
    orders = []
    if args.orders_file:
        with open(args.orders_file, "r") as f:
            orders = json.load(f)

    body = {
        "user_id": args.user_id,
        "user_tier": args.user_tier or "FREE",
        "ticker": args.ticker.upper(),
        "session_date": args.session_date or date.today().isoformat(),
        "session_type": args.session_type or "live",
        "large_orders": orders,
    }
    data = api_request("POST", "/eligibility", token, body)
    print(json.dumps(data, indent=2))


def cmd_health(args, token: str):
    """Service health check."""
    data = api_request("GET", "/health", token)
    print(json.dumps(data, indent=2))


# ─── Argument Parser ───────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aireport",
        description="Query the RealMarket AI Report Service",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # generate
    p_gen = sub.add_parser("generate", help="Enqueue report generation")
    p_gen.add_argument("--ticker", "-t", required=True, help="Ticker symbol")
    p_gen.add_argument("--user-id", "-u", required=True, help="User email/ID")
    p_gen.add_argument("--user-tier", default="FREE", help="User tier (FREE/TRIAL/PRO/ADMIN)")
    p_gen.add_argument("--session-date", help="Session date YYYY-MM-DD (default: today)")
    p_gen.add_argument("--session-type", default="live", help="live or historical")
    p_gen.add_argument("--orders-file", help="JSON file with large_orders array")

    # status
    p_status = sub.add_parser("status", help="Poll job status")
    p_status.add_argument("--job-id", "-j", required=True, help="Job ID from generate")

    # report
    p_report = sub.add_parser("report", help="Fetch a completed report")
    p_report.add_argument("--job-id", "-j", help="Job ID (for artifact mode)")
    p_report.add_argument("--user-id", "-u", help="User email/ID")
    p_report.add_argument("--ticker", "-t", help="Ticker symbol")
    p_report.add_argument("--trading-day", help="Trading day YYYY-MM-DD")
    p_report.add_argument("--report-id", help="Report ID")
    p_report.add_argument("--format", "-f", default="json", help="json or markdown")

    # history
    p_hist = sub.add_parser("history", help="List reports for ticker+day")
    p_hist.add_argument("--ticker", "-t", required=True, help="Ticker symbol")
    p_hist.add_argument("--trading-day", required=True, help="Trading day YYYY-MM-DD")
    p_hist.add_argument("--user-id", "-u", help="User email/ID")

    # summary
    p_sum = sub.add_parser("summary", help="Per-ticker summary for user+day")
    p_sum.add_argument("--user-id", "-u", required=True, help="User email/ID")
    p_sum.add_argument("--trading-day", required=True, help="Trading day YYYY-MM-DD")

    # quota
    p_quota = sub.add_parser("quota", help="Check credit usage")
    p_quota.add_argument("--user-id", "-u", required=True, help="User email/ID")
    p_quota.add_argument("--tier", default="FREE", help="User tier")

    # eligibility
    p_elig = sub.add_parser("eligibility", help="Pre-check generation eligibility")
    p_elig.add_argument("--ticker", "-t", required=True, help="Ticker symbol")
    p_elig.add_argument("--user-id", "-u", required=True, help="User email/ID")
    p_elig.add_argument("--user-tier", default="FREE", help="User tier")
    p_elig.add_argument("--session-date", help="Session date YYYY-MM-DD")
    p_elig.add_argument("--session-type", default="live", help="live or historical")
    p_elig.add_argument("--orders-file", help="JSON file with large_orders array")

    # health
    sub.add_parser("health", help="Service health check")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    token = get_api_token()

    dispatch = {
        "generate": cmd_generate,
        "status": cmd_status,
        "report": cmd_report,
        "history": cmd_history,
        "summary": cmd_summary,
        "quota": cmd_quota,
        "eligibility": cmd_eligibility,
        "health": cmd_health,
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(args, token)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
