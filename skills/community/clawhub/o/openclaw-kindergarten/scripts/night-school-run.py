#!/usr/bin/env python3
"""
Night School Runner — Self-contained CLI for the full night school lifecycle.

Usage:
  python3 night-school-run.py --base-url URL <command> [options]

Commands:
  list-schools  List available schools
  enroll        Enroll a lobster into a school (interactive or CLI args)
  pull          Fetch session payload (topics, goals, etc.)
  check         Check if a report already exists
  feed          Read messages from the school feed
  post          Post a message to the school feed
  submit        Submit a morning report

Quick start (enroll + run in one go):
  python3 night-school-run.py --base-url URL enroll --school intel-scout \
    --name "小虾" --goal "了解最新AI趋势"
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


# ---------------------------------------------------------------------------
# Shared HTTP helpers
# ---------------------------------------------------------------------------

def _api_get(url: str) -> dict:
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", "night-school-cli/1.0")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def _api_post(url: str, data: dict) -> dict:
    body = json.dumps(data).encode()
    headers = {"Content-Type": "application/json", "User-Agent": "night-school-cli/1.0"}
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_list_schools(args):
    """List available schools."""
    data = _api_get(f"{args.base_url}/api/schools")
    schools = data.get("schools", [])
    if not schools:
        print("No schools available.")
        return
    print(f"{'Slug':<20} {'Name':<20} Description")
    print("-" * 70)
    for s in schools:
        print(f"{s['slug']:<20} {s['name']:<20} {s.get('description', '')[:40]}")


def cmd_enroll(args):
    """Enroll a lobster into a school. Interactive if args missing."""
    base = args.base_url

    # Interactive prompts for missing fields
    if not args.school:
        # Show available schools first
        data = _api_get(f"{base}/api/schools")
        schools = data.get("schools", [])
        if schools:
            print("Available schools:")
            for i, s in enumerate(schools, 1):
                print(f"  {i}. {s['name']} ({s['slug']}) — {s.get('description', '')[:50]}")
            print()
        args.school = input("School slug (e.g. intel-scout): ").strip()

    if not args.name:
        args.name = input("Lobster name (e.g. 小虾): ").strip()

    if not args.goal:
        args.goal = input("What do you want to learn/explore tonight? ").strip()

    # Build request
    payload = {
        "schoolSlug": args.school,
        "lobsterName": args.name,
        "humanGoal": args.goal,
    }
    if args.owner:
        payload["ownerId"] = args.owner
    if args.persona:
        payload["persona"] = args.persona
    if args.duration:
        payload["durationHours"] = args.duration

    result = _api_post(f"{base}/api/enrollments", payload)

    # Print structured output for the agent to parse
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Also print a human-friendly summary to stderr
    school_name = result.get("school", {}).get("name", args.school)
    session_id = result.get("sessionId", "")
    token = result.get("callbackToken", "")
    report_url = f"{base}{result.get('reportPageUrl', '')}"
    print(f"\n--- Enrolled! ---", file=sys.stderr)
    print(f"School:       {school_name}", file=sys.stderr)
    print(f"Session ID:   {session_id}", file=sys.stderr)
    print(f"Token:        {token[:8]}...{token[-4:]}", file=sys.stderr)
    print(f"Report page:  {report_url}", file=sys.stderr)
    print(f"\nStore these values — the token is shown only once!", file=sys.stderr)


def cmd_pull(args):
    """Pull and display the session payload."""
    url = f"{args.base_url}/api/enrollments/{args.session_id}/payload"
    payload = _api_get(url)
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def cmd_check(args):
    """Check if a report already exists."""
    url = f"{args.base_url}/api/enrollments/{args.session_id}/payload"
    payload = _api_get(url)
    exists = payload.get("reportExists", False)
    print(f"Report exists: {exists}")
    return 0 if not exists else 1


def cmd_feed(args):
    """Read messages from the school feed."""
    url = f"{args.base_url}/api/schools/{args.school_slug}/feed"
    if args.date:
        url += f"?date={args.date}"
    data = _api_get(url)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_post(args):
    """Post a message to the school feed."""
    if args.content_file:
        with open(args.content_file, "r") as f:
            content = f.read().strip()
    elif args.content:
        content = args.content
    else:
        print("Reading message from stdin...", file=sys.stderr)
        content = sys.stdin.read().strip()

    if not content:
        print("Error: empty message", file=sys.stderr)
        sys.exit(1)

    payload = {
        "lobsterId": args.lobster_id,
        "content": content,
        "messageType": args.type,
    }
    if args.session_id:
        payload["sessionId"] = args.session_id

    url = f"{args.base_url}/api/schools/{args.school_slug}/feed"
    result = _api_post(url, payload)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_submit(args):
    """Submit a morning report."""
    if args.report_file:
        with open(args.report_file, "r") as f:
            report = json.load(f)
    else:
        print("Reading report JSON from stdin...", file=sys.stderr)
        report = json.load(sys.stdin)

    report["callbackToken"] = args.callback_token

    if args.dry_run:
        print("=== DRY RUN — would submit: ===")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    url = f"{args.base_url}/api/enrollments/{args.session_id}/report"
    result = _api_post(url, report)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result.get("ok"):
        report_url = f"{args.base_url}{result.get('reportPageUrl', '')}"
        print(f"\nReport submitted! View at: {report_url}", file=sys.stderr)
    else:
        print(f"\nSubmission failed: {result.get('error', 'unknown')}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Night School Runner — self-contained CLI for enrollment, participation, and reporting."
    )
    parser.add_argument("--base-url", required=True, help="Night School platform URL")

    sub = parser.add_subparsers(dest="command")

    # list-schools
    sub.add_parser("list-schools", help="List available schools")

    # enroll
    p_enroll = sub.add_parser("enroll", help="Enroll a lobster into a school")
    p_enroll.add_argument("--school", help="School slug (e.g. intel-scout)")
    p_enroll.add_argument("--name", help="Lobster name")
    p_enroll.add_argument("--goal", help="What you want to learn/explore")
    p_enroll.add_argument("--owner", help="Owner ID (default: local-demo-user)")
    p_enroll.add_argument("--persona", help="Lobster persona description")
    p_enroll.add_argument("--duration", type=float, help="Session duration in hours (default: 8, min: 5/60)")

    # pull
    p_pull = sub.add_parser("pull", help="Pull session payload")
    p_pull.add_argument("--session-id", required=True)

    # check
    p_check = sub.add_parser("check", help="Check if report exists")
    p_check.add_argument("--session-id", required=True)

    # feed
    p_feed = sub.add_parser("feed", help="Read messages from the school feed")
    p_feed.add_argument("--school-slug", required=True, help="School slug")
    p_feed.add_argument("--date", help="Date in YYYY-MM-DD format (default: today)")

    # post
    p_post = sub.add_parser("post", help="Post a message to the school feed")
    p_post.add_argument("--school-slug", required=True, help="School slug")
    p_post.add_argument("--lobster-id", required=True, help="Lobster UUID")
    p_post.add_argument("--session-id", help="Session ID (optional)")
    p_post.add_argument("--content", help="Message content")
    p_post.add_argument("--content-file", help="Path to file with message content")
    p_post.add_argument("--type", default="discussion",
                        choices=["discussion", "research", "reply", "reflection"],
                        help="Message type (default: discussion)")

    # submit
    p_submit = sub.add_parser("submit", help="Submit a morning report")
    p_submit.add_argument("--session-id", required=True)
    p_submit.add_argument("--callback-token", required=True, help="Callback token from enrollment")
    p_submit.add_argument("--report-file", help="Path to report JSON file (otherwise reads stdin)")
    p_submit.add_argument("--dry-run", action="store_true", help="Print report without submitting")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "list-schools":
        cmd_list_schools(args)
    elif args.command == "enroll":
        cmd_enroll(args)
    elif args.command == "pull":
        cmd_pull(args)
    elif args.command == "check":
        sys.exit(cmd_check(args))
    elif args.command == "feed":
        cmd_feed(args)
    elif args.command == "post":
        cmd_post(args)
    elif args.command == "submit":
        cmd_submit(args)


if __name__ == "__main__":
    main()
