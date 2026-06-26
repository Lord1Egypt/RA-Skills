#!/usr/bin/env python3
"""
Query Mailgo campaign statistics: overview, per-round breakdown, daily progress, send records, replies.

Usage:
    python3 campaign_report.py overview <campaignId> [--start DATE] [--end DATE] [--dimension USER|COUNT]
    python3 campaign_report.py rounds <campaignId> [--start DATE] [--end DATE]
    python3 campaign_report.py daily <campaignId> --start DATE --end DATE
    python3 campaign_report.py send-records <campaignId> [--start DATE] [--end DATE]
                                            [--email QUERY] [--status 1|2|3|4] [--page N] [--size N]
    python3 campaign_report.py replies <campaignId> --sender SENDER_EMAIL [--read-content]

Requires:
    MAILGO_API_KEY environment variable

Output:
    Formatted report on stdout. Raw JSON available with --json flag.
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser

_ssl_ctx = ssl.create_default_context()
# Do NOT disable certificate verification — MITM attacks would allow token theft

BASE = "https://api.leadsnavi.com"
PREFIX = "/mcp/mailgo-logical"


def headers(api_key):
    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "mailgo-mcp-server/1.0 (https://github.com/netease-im/leadsnavi-mcp-server)",
    }


def post(api_key, path, body):
    url = f"{BASE}{PREFIX}{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers(api_key), method="POST")
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


def pct(num, denom):
    if not denom:
        return "  -  "
    return f"{num / denom * 100:5.1f}%"


def cmd_overview(api_key, campaign_id, start, end, dimension, as_json):
    body = {"campaignId": int(campaign_id)}
    if start:
        body["start"] = start
    if end:
        body["end"] = end
    if dimension:
        body["dimension"] = dimension

    result = post(api_key, "/api/biz/mailgo/stat/overview", body)
    d = result.get("data", {})

    if as_json:
        print(json.dumps(d, indent=2))
        return

    sent = d.get("sent", 0)
    delivered = d.get("delivered", 0)
    opened = d.get("opened", 0)
    replied = d.get("replied", 0)
    clicked = d.get("click", 0)
    tracking = d.get("openClick", 0)

    print(f"Campaign Overview (ID: {campaign_id})")
    print("=" * 50)
    print(f"  Leads:       {d.get('leads', 0):>6}")
    print(f"    Completed: {d.get('completed', 0):>6}")
    print(f"    In progress:{d.get('inProgress', 0):>5}")
    print(f"    Not yet:   {d.get('notYet', 0):>6}")
    print(f"    Failed:    {d.get('failed', 0):>6}")
    print()
    print("  Sending Performance:")
    print(f"    Sent:      {sent:>6}")
    print(f"    Delivered: {delivered:>6}  ({pct(delivered, sent)})")
    if tracking:
        print(f"    Opened:    {opened:>6}  ({pct(opened, delivered)})")
        print(f"    Replied:   {replied:>6}  ({pct(replied, delivered)})")
        print(f"    Clicked:   {clicked:>6}  ({pct(clicked, delivered)})")
    else:
        print(f"    Replied:   {replied:>6}  ({pct(replied, delivered)})")
        print("    (Open/click tracking disabled)")
    bounced = sent - delivered
    if sent > 0:
        print(f"    Bounced:   {bounced:>6}  ({pct(bounced, sent)})")


def cmd_rounds(api_key, campaign_id, start, end, as_json):
    body = {"campaignId": int(campaign_id)}
    if start:
        body["start"] = start
    if end:
        body["end"] = end

    result = post(api_key, "/api/biz/mailgo/stat/sequence-info", body)
    infos = result.get("data", {}).get("infos", [])

    if as_json:
        print(json.dumps(infos, indent=2))
        return

    if not infos:
        print("No round data available.")
        return

    print(f"Per-Round Breakdown (Campaign: {campaign_id})")
    print("=" * 75)
    print(f"  {'Round':>5}  {'Sent':>7}  {'Delivered':>9}  {'Opened':>8}  {'Replied':>8}  {'Clicked':>8}")
    print(f"  {'-----':>5}  {'-------':>7}  {'---------':>9}  {'--------':>8}  {'--------':>8}  {'--------':>8}")

    for info in infos:
        r = info.get("round", 0)
        s = info.get("sent", 0)
        d = info.get("delivered", 0)
        o = info.get("opened", 0)
        rp = info.get("replied", 0)
        c = info.get("click", 0)
        print(f"  {r:>5}  {s:>7}  {d:>9}  {o:>6} {pct(o, d)}  {rp:>4} {pct(rp, d)}  {c:>4} {pct(c, d)}")


def cmd_daily(api_key, campaign_id, start, end, as_json):
    if not start or not end:
        print("Error: --start and --end are required for daily report", file=sys.stderr)
        sys.exit(1)

    body = {
        "campaignId": int(campaign_id),
        "startDate": start,
        "endDate": end,
    }

    result = post(api_key, "/api/biz/mailgo/stat/daily-step", body)
    steps = result.get("data", {}).get("stepList", [])

    if as_json:
        print(json.dumps(steps, indent=2))
        return

    if not steps:
        print("No daily data available for this range.")
        return

    print(f"Daily Progress (Campaign: {campaign_id}, {start} to {end})")
    print("=" * 80)
    print(f"  {'Date':>10}  {'Step':>4}  {'Sent':>7}  {'Success':>7}  {'Failed':>7}  {'Pending':>7}  {'Remain':>7}")
    print(f"  {'----------':>10}  {'----':>4}  {'-------':>7}  {'-------':>7}  {'-------':>7}  {'-------':>7}  {'-------':>7}")

    for step in steps:
        date_int = step.get("date", 0)
        date_str = f"{date_int // 10000}-{(date_int % 10000) // 100:02d}-{date_int % 100:02d}"
        print(f"  {date_str:>10}  {step.get('step', 0):>4}  "
              f"{step.get('sendCount', 0):>7}  {step.get('successCount', 0):>7}  "
              f"{step.get('failedCount', 0):>7}  {step.get('willSendCount', 0):>7}  "
              f"{step.get('limitRemainCount', 0):>7}")


# ---------------------------------------------------------------------------
# HTML → plain text helpers
# ---------------------------------------------------------------------------

class _HTMLTextExtractor(HTMLParser):
    """Minimal HTML-to-text: strip tags, decode entities, collapse whitespace.

    blockquote (quoted original email) is rendered with a '> ' prefix per line,
    so the user can distinguish the reply from the original message.
    Table rows emit a single newline on close to avoid double-spacing.
    """
    _SKIP_TAGS = {"script", "style", "head", "meta", "link"}
    _QUOTE_TAGS = {"blockquote"}
    # Block tags that emit newline on open
    _OPEN_NL_TAGS = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6"}
    # Block tags that emit newline on close only
    _CLOSE_NL_TAGS = {"tr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._parts = []
        self._skip_depth = 0
        self._quote_depth = 0

    def _skipped(self):
        return self._skip_depth > 0

    def handle_starttag(self, tag, attrs):
        tl = tag.lower()
        if tl in self._SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skipped():
            return
        if tl in self._QUOTE_TAGS:
            self._quote_depth += 1
            self._parts.append("\n")   # blank line before quote block
        elif tl in self._OPEN_NL_TAGS:
            self._parts.append("\n")
        elif tl in self._CLOSE_NL_TAGS:
            pass  # handled on endtag

    def handle_endtag(self, tag):
        tl = tag.lower()
        if tl in self._SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
            return
        if self._skipped():
            return
        if tl in self._QUOTE_TAGS and self._quote_depth > 0:
            self._quote_depth -= 1
            self._parts.append("\n")   # blank line after quote block
        elif tl in self._CLOSE_NL_TAGS:
            self._parts.append("\n")

    def handle_data(self, data):
        if self._skipped():
            return
        if self._quote_depth > 0:
            # Prefix every non-empty line inside blockquote with "> "
            for line in data.splitlines(keepends=True):
                stripped = line.rstrip("\n\r")
                if stripped.strip():
                    self._parts.append(f"> {stripped}")
                self._parts.append("\n")
        else:
            self._parts.append(data)

    def get_text(self):
        raw = "".join(self._parts)
        # Collapse 3+ consecutive newlines → 2
        cleaned = re.sub(r"\n{3,}", "\n\n", raw)
        lines = [ln.rstrip() for ln in cleaned.splitlines()]
        # Remove consecutive blank lines
        result = []
        prev_blank = False
        for ln in lines:
            is_blank = not ln.strip()
            if is_blank and prev_blank:
                continue
            result.append(ln)
            prev_blank = is_blank
        while result and not result[0].strip():
            result.pop(0)
        while result and not result[-1].strip():
            result.pop()
        return "\n".join(result)


def _html_to_text(html_content):
    """Extract readable plain text from an HTML email body."""
    extractor = _HTMLTextExtractor()
    try:
        extractor.feed(html_content)
        return extractor.get_text()
    except Exception:
        text = re.sub(r"<[^>]+>", " ", html_content)
        return re.sub(r"\s{2,}", " ", text).strip()


# ---------------------------------------------------------------------------
# Mailgo hmail proxy (for reading reply content)
# All calls go to https://api.leadsnavi.com — same host as all other API
# calls in this script. The /mcp/mailgo-tp prefix routes to Mailgo's
# internal hmail wrapper service; no external endpoint is involved.
# ---------------------------------------------------------------------------

def post_tp(api_key, path, body):
    """POST to the /mcp/mailgo-tp prefix (Mailgo's internal hmail wrapper, still on api.leadsnavi.com)."""
    url = f"{BASE}/mcp/mailgo-tp{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers(api_key), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {err[:500]}", file=sys.stderr)
        return None


def _read_message_text(api_key, sender_account, mid):
    """
    Fetch a single email via hmail proxy and return extracted plain text.
    Returns (subject, from_addr, sent_ts, body_text).
    """
    result = post_tp(api_key, "/api/hmail/proxy", {
        "_account": sender_account,
        "func": "mbox:readMessage",
        "mid": mid,
    })
    if not result or result.get("code") != "S_OK":
        code = result.get("code", "unknown") if result else "no response"
        return None, None, None, f"[Failed to read message: {code}]"

    msg = result.get("var", {})
    subject = msg.get("subject", "")
    from_list = msg.get("from") or []
    from_addr = from_list[0] if from_list else ""
    sent_ts = msg.get("sentDate")

    html_part = msg.get("html") or {}
    text_part = msg.get("text") or {}
    html_content = html_part.get("content", "")
    text_content = text_part.get("content", "")

    if html_content:
        body_text = _html_to_text(html_content)
    elif text_content:
        body_text = text_content.strip()
    else:
        body_text = "[No readable content]"

    return subject, from_addr, sent_ts, body_text


def _get_campaign_sender(api_key, campaign_id):
    """
    Look up the sender email for a campaign via campaign/info.
    Returns the first sender email string, or None if not found.
    The API may return senderEmails as:
      - a list of strings:  ["alice@example.com"]
      - a list of objects:  [{"email": "alice@example.com"}]
    Both forms are handled.
    """
    url = f"{BASE}{PREFIX}/api/biz/mailgo/campaign/info?campaignId={campaign_id}"
    req = urllib.request.Request(url, headers=headers(api_key), method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} fetching campaign info: {err[:300]}", file=sys.stderr)
        return None

    if not result.get("success", False):
        print(f"campaign/info error: {result.get('message', 'unknown')}", file=sys.stderr)
        return None

    data = result.get("data", {})

    # Try top-level senderEmails first (observed in practice)
    raw = data.get("senderEmails") or []
    # Fall back to basicInfo.senderEmails
    if not raw:
        raw = (data.get("basicInfo") or {}).get("senderEmails") or []

    for entry in raw:
        if isinstance(entry, str) and entry:
            return entry
        if isinstance(entry, dict) and entry.get("email"):
            return entry["email"]

    return None


def cmd_replies(api_key, campaign_id, sender_account, read_content, as_json):
    """List all replies for a campaign, concurrently reading message bodies when requested."""
    # If the user wants to read content but didn't provide --sender, auto-detect from campaign info
    if read_content and not sender_account:
        print("No --sender provided, looking up from campaign info...", file=sys.stderr)
        sender_account = _get_campaign_sender(api_key, campaign_id)
        if sender_account:
            print(f"  Auto-detected sender: {sender_account}", file=sys.stderr)
        else:
            print("  Warning: could not determine sender, body fetch skipped", file=sys.stderr)

    body = {
        "campaignId": int(campaign_id),
        "round": 1,
        "pageNum": 1,
        "pageSize": 100,
    }
    result = post(api_key, "/api/biz/mailgo/stat/sequence-detail-reply", body)
    records = result.get("data", {}).get("records", [])

    if as_json and not read_content:
        print(json.dumps(records, indent=2))
        return

    if not records:
        print(f"No replies found for campaign {campaign_id}.")
        return

    # Flatten all reply entries across contacts, preserving order
    all_replies = []
    for contact in records:
        for item in contact.get("recordList", []):
            all_replies.append(item)

    # Concurrently fetch message bodies if requested
    body_map = {}   # mid -> body_text
    if read_content and sender_account and all_replies:
        mids = [item.get("mid", "") for item in all_replies if item.get("mid")]
        max_workers = min(len(mids), 8)   # cap at 8 concurrent connections
        print(f"Fetching {len(mids)} message(s) concurrently "
              f"(workers={max_workers})...", file=sys.stderr)

        def fetch(mid):
            _, _, _, text = _read_message_text(api_key, sender_account, mid)
            return mid, text

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(fetch, mid): mid for mid in mids}
            for future in as_completed(futures):
                mid, text = future.result()
                body_map[mid] = text

    print(f"Replies — Campaign {campaign_id}  ({len(all_replies)} total)")
    print("=" * 60)

    for idx, item in enumerate(all_replies, 1):
        from_email = item.get("email", "")
        mid = item.get("mid", "")
        time_str = item.get("time", "")
        subject = item.get("subject", "")

        print(f"\n[{idx}] From:    {from_email}")
        print(f"     Time:    {time_str}")
        print(f"     Subject: {subject}")
        print(f"     mid:     {mid}")

        if read_content:
            if not sender_account:
                print("     [Tip: pass --sender to read message body]")
            elif mid in body_map:
                print()
                for line in body_map[mid].splitlines():
                    print(f"     {line}")

    print()


STATUS_LABELS = {
    2: "PROGRESS (paused/waiting)",
    3: "SUCCESS  (sent)",
    4: "FAILED",
}


def cmd_send_records(api_key, campaign_id, start, end, email_query, status_filter, page, size, as_json):
    body = {"campaignId": int(campaign_id), "page": page, "size": size}
    if start:
        body["start"] = start.replace("-", "")
    if end:
        body["end"] = end.replace("-", "")
    if email_query:
        body["emailQuery"] = email_query
    if status_filter:
        body["statusList"] = [int(s) for s in status_filter]

    result = post(api_key, "/api/biz/mailgo/stat/send-records", body)
    d = result.get("data", {})

    if as_json:
        print(json.dumps(d, indent=2))
        return

    records = d.get("records", [])
    total = d.get("total", 0)
    has_next = d.get("hasNext", 0)
    campaign_name = d.get("campaignName", "")

    print(f"Send Records — {campaign_name} (ID: {campaign_id})")
    print("=" * 80)
    print(f"  Total returned: {total}{'  (more pages available)' if has_next else ''}")
    print()

    if not records:
        print("  No records found.")
        return

    col_email  = max(len(r.get("contactEmail", "")) for r in records)
    col_email  = max(col_email, len("Recipient"))

    header = (f"  {'Recipient':<{col_email}}  {'Planned Send Time':<17}  "
              f"{'Actual Send Time':<17}  {'Round':>5}  Status")
    print(header)
    print("  " + "-" * (len(header) - 2))

    for r in records:
        contact    = r.get("contactEmail", "")
        plan_date  = r.get("planSendDate") or "—"
        send_date  = r.get("sendDate")
        # sendTimestamp == -1 means not yet sent
        if r.get("sendTimestamp", -1) == -1 or not send_date:
            send_date = "—"
        round_num  = r.get("round", 0)
        status_val = r.get("status", 0)
        status_str = STATUS_LABELS.get(status_val, str(status_val))
        print(f"  {contact:<{col_email}}  {plan_date:<17}  {send_date:<17}  {round_num:>5}  {status_str}")


def main():
    parser = argparse.ArgumentParser(description="Mailgo campaign statistics report")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    for cmd_name in ("overview", "rounds", "daily", "send-records"):
        p = sub.add_parser(cmd_name, help=f"Campaign {cmd_name}")
        p.add_argument("campaign_id", help="Campaign ID")
        p.add_argument("--start", default="", help="Start date (yyyy-MM-dd or yyyyMMdd)")
        p.add_argument("--end", default="", help="End date (yyyy-MM-dd or yyyyMMdd)")
        if cmd_name == "overview":
            p.add_argument("--dimension", default="USER", choices=["USER", "COUNT"],
                           help="USER=unique contacts, COUNT=total events")
        if cmd_name == "send-records":
            p.add_argument("--email", default="", dest="email_query",
                           help="Filter by recipient email keyword")
            p.add_argument("--status", nargs="+", dest="status_filter",
                           choices=["1", "2", "3", "4"],
                           help="Filter by status: 1=pending 2=waiting 3=success 4=failed")
            p.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
            p.add_argument("--size", type=int, default=50, help="Page size (default: 50)")

    # replies subcommand
    p_replies = sub.add_parser("replies", help="List replies and optionally read message bodies")
    p_replies.add_argument("campaign_id", help="Campaign ID")
    p_replies.add_argument("--sender", default="", dest="sender_account",
                           help="Sender mailbox email (required to read message body)")
    p_replies.add_argument("--read-content", action="store_true",
                           help="Fetch and display the plain-text body of each reply")

    args = parser.parse_args()

    api_key = os.environ.get("MAILGO_API_KEY")
    if not api_key:
        print("Error: MAILGO_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if args.command == "overview":
        cmd_overview(api_key, args.campaign_id, args.start, args.end, args.dimension, args.json)
    elif args.command == "rounds":
        cmd_rounds(api_key, args.campaign_id, args.start, args.end, args.json)
    elif args.command == "daily":
        cmd_daily(api_key, args.campaign_id, args.start, args.end, args.json)
    elif args.command == "send-records":
        cmd_send_records(api_key, args.campaign_id, args.start, args.end,
                         args.email_query, args.status_filter, args.page, args.size, args.json)
    elif args.command == "replies":
        cmd_replies(api_key, args.campaign_id, args.sender_account,
                    args.read_content, args.json)


if __name__ == "__main__":
    main()
