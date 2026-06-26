#!/usr/bin/env python3
"""
End-to-end Mailgo email verification: submit a list of emails, then poll
until all results are ready.

Usage:
    python3 verify_emails.py alice@example.com bob@gmail.com
    python3 verify_emails.py --file leads.txt
    python3 verify_emails.py --file leads.csv --email-column "Email Address"

Requires:
    MAILGO_API_KEY environment variable

Output:
    JSON summary with categorized results on stdout.
    Progress updates on stderr.
"""

import argparse
import csv
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

_ssl_ctx = ssl.create_default_context()
# Do NOT disable certificate verification — MITM attacks would allow token theft

BASE = "https://api.leadsnavi.com"
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

_EMAIL_COL_NAMES = {
    "email", "e-mail", "mail", "emailaddress", "email_address",
    "contact_email", "contactemail", "recipient", "to",
}


def _headers(api_key):
    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "mailgo-mcp-server/1.0 (https://github.com/netease-im/leadsnavi-mcp-server)",
    }


# ── helpers to read emails from files ──────────────────────────────────


def _looks_like_email(val):
    return isinstance(val, str) and _EMAIL_RE.match(val.strip()) is not None


def _detect_email_col(headers_row, rows):
    lower_map = {h: h.strip().lower().replace(" ", "_") for h in headers_row}
    for h in headers_row:
        if lower_map[h] in _EMAIL_COL_NAMES:
            return h
    best_col, best_count = None, 0
    for h in headers_row:
        count = sum(1 for row in rows if _looks_like_email(row.get(h, "")))
        if count > best_count:
            best_col, best_count = h, count
    return best_col


def read_emails_from_file(path, email_col_override=None):
    """Read emails from a TXT, CSV, XLSX, or JSON file. Returns a deduplicated list."""
    ext = os.path.splitext(path)[1].lower()
    print(f"Reading emails from: {path} ({ext})", file=sys.stderr)

    if ext == ".txt":
        with open(path, "r", encoding="utf-8-sig") as f:
            emails = [
                line.strip() for line in f if _looks_like_email(line.strip())
            ]
    elif ext == ".csv":
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            hdrs = reader.fieldnames or []
            rows = list(reader)
        col = email_col_override or _detect_email_col(hdrs, rows)
        if not col:
            print(
                f"Error: cannot detect email column. Headers: {hdrs}\n"
                f"Use --email-column to specify.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"  Using column: '{col}'", file=sys.stderr)
        emails = [
            str(row.get(col, "")).strip()
            for row in rows
            if _looks_like_email(str(row.get(col, "")).strip())
        ]
    elif ext in (".xlsx", ".xls"):
        try:
            import openpyxl
        except ImportError:
            print(
                "Error: openpyxl is required to read .xlsx files. "
                "Install with: pip install openpyxl",
                file=sys.stderr,
            )
            sys.exit(1)
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.active
        all_rows = list(ws.iter_rows(values_only=True))
        wb.close()

        if not all_rows:
            emails = []
        else:
            # Detect whether the first row is a header or data
            first_row = [str(c) if c is not None else "" for c in all_rows[0]]
            first_row_has_email = any(_looks_like_email(v) for v in first_row)

            if first_row_has_email and not email_col_override:
                # No header row — all rows are data, collect emails from all cells
                emails = []
                for raw_row in all_rows:
                    for cell in raw_row:
                        val = str(cell).strip() if cell is not None else ""
                        if _looks_like_email(val):
                            emails.append(val)
            else:
                # First row is a header
                hdrs = first_row
                rows = []
                for raw_row in all_rows[1:]:
                    rows.append({hdrs[i]: (str(raw_row[i]) if i < len(raw_row) and raw_row[i] is not None else "")
                                 for i in range(len(hdrs))})
                col = email_col_override or _detect_email_col(hdrs, rows)
                if not col:
                    print(
                        f"Error: cannot detect email column. Headers: {hdrs}\n"
                        f"Use --email-column to specify.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                print(f"  Using column: '{col}'", file=sys.stderr)
                emails = [
                    str(row.get(col, "")).strip()
                    for row in rows
                    if _looks_like_email(str(row.get(col, "")).strip())
                ]
    elif ext == ".json":
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        if isinstance(data, list) and data and isinstance(data[0], str):
            emails = [e.strip() for e in data if _looks_like_email(e.strip())]
        elif isinstance(data, list) and data and isinstance(data[0], dict):
            hdrs = list(data[0].keys())
            col = email_col_override or _detect_email_col(hdrs, data)
            if not col:
                print(
                    f"Error: cannot detect email column. Keys: {hdrs}",
                    file=sys.stderr,
                )
                sys.exit(1)
            emails = [
                str(row.get(col, "")).strip()
                for row in data
                if _looks_like_email(str(row.get(col, "")).strip())
            ]
        else:
            print(
                "Error: JSON must be an array of emails or objects",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        # fallback: try as plain-text one-per-line
        with open(path, "r", encoding="utf-8-sig") as f:
            emails = [
                line.strip() for line in f if _looks_like_email(line.strip())
            ]

    # deduplicate while preserving order
    seen = set()
    unique = []
    for e in emails:
        lower = e.lower()
        if lower not in seen:
            seen.add(lower)
            unique.append(e)
    return unique


# ── API calls ──────────────────────────────────────────────────────────


def submit(emails, api_key):
    """POST email list → returns taskId string."""
    url = f"{BASE}/mcp/mailgo-auth/api/biz/email/verification"
    data = json.dumps({"emails": emails}).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers=_headers(api_key), method="POST"
    )
    print(f"Submitting {len(emails)} email(s) for verification...", file=sys.stderr)
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {err[:500]}", file=sys.stderr)
        sys.exit(1)

    if body.get("code") != 0:
        msg = body.get("message", "unknown error")
        print(f"API error: {msg}", file=sys.stderr)
        if "credit" in msg.lower():
            print(
                "Verification credits exhausted. "
                "Please top up at https://app.leadsnavi.com/billing",
                file=sys.stderr,
            )
        sys.exit(1)

    task_id = body.get("data")
    if not task_id:
        print("Error: no taskId in response", file=sys.stderr)
        sys.exit(1)
    print(f"  taskId: {task_id}", file=sys.stderr)
    return task_id


def poll(task_id, api_key, timeout=180, interval=5):
    """Poll until all results are ready. Returns categorized dict."""
    url = f"{BASE}/mcp/mailgo-auth/api/biz/email/verification/task/{task_id}"
    hdrs = _headers(api_key)
    # GET request doesn't need Content-Type
    hdrs.pop("Content-Type", None)

    elapsed = 0
    entries = []
    while elapsed < timeout:
        time.sleep(interval)
        elapsed += interval

        req = urllib.request.Request(url, headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
            sys.exit(1)

        if body.get("code") != 0:
            print(f"API error: {body.get('message')}", file=sys.stderr)
            sys.exit(1)

        entries = body.get("data", {}).get("data", [])
        unchecked = [e for e in entries if e.get("status") == "UNCHECKED"]

        if len(unchecked) == 0:
            return _categorize(entries)

        completed = len(entries) - len(unchecked)
        print(f"Verifying... {completed}/{len(entries)} done", file=sys.stderr)

    # timeout — not necessarily a failure
    completed = len(entries) - len(
        [e for e in entries if e.get("status") == "UNCHECKED"]
    )
    print(
        f"Timeout after {timeout}s: {completed}/{len(entries)} done. "
        "Server continues processing for up to 3 hours.",
        file=sys.stderr,
    )
    return _categorize(entries)


def _categorize(entries):
    result = {"total": len(entries), "valid": [], "invalid": [], "domain_error": [], "unknown": [], "unchecked": []}
    for e in entries:
        status = e.get("status", "UNKNOWN")
        bucket = status.lower()
        if bucket in result:
            result[bucket].append(e)
        else:
            result["unknown"].append(e)
    return result


# ── main ───────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Submit emails for Mailgo verification and poll for results"
    )
    parser.add_argument(
        "emails", nargs="*", help="Email addresses to verify"
    )
    parser.add_argument(
        "--file", "-f", default="", help="Read emails from file (TXT/CSV/JSON)"
    )
    parser.add_argument(
        "--email-column", default="", help="Override email column name in CSV/JSON"
    )
    parser.add_argument(
        "--timeout", type=int, default=180, help="Poll timeout in seconds (default 180)"
    )
    parser.add_argument(
        "--interval", type=int, default=5, help="Poll interval in seconds (default 5)"
    )
    args = parser.parse_args()

    # Collect emails
    emails = []
    if args.file:
        emails = read_emails_from_file(args.file, args.email_column or None)
    if args.emails:
        emails.extend(
            e.strip() for e in args.emails if _looks_like_email(e.strip())
        )
    if not emails:
        print(
            "Error: provide emails as arguments or via --file", file=sys.stderr
        )
        sys.exit(1)

    # Deduplicate
    seen = set()
    unique = []
    for e in emails:
        lower = e.lower()
        if lower not in seen:
            seen.add(lower)
            unique.append(e)
    emails = unique

    if len(emails) > 10000:
        print(
            f"Warning: {len(emails)} emails exceeds 10,000 limit per task. "
            "Splitting into batches.",
            file=sys.stderr,
        )

    # API key
    api_key = os.environ.get("MAILGO_API_KEY")
    if not api_key:
        print(
            "Error: MAILGO_API_KEY environment variable not set",
            file=sys.stderr,
        )
        sys.exit(1)

    # Process in batches of 10,000
    all_results = {"total": 0, "valid": [], "invalid": [], "domain_error": [], "unknown": [], "unchecked": []}
    batch_size = 10000
    for i in range(0, len(emails), batch_size):
        batch = emails[i : i + batch_size]
        if len(emails) > batch_size:
            print(
                f"\nBatch {i // batch_size + 1}: "
                f"emails {i + 1}-{i + len(batch)} of {len(emails)}",
                file=sys.stderr,
            )

        task_id = submit(batch, api_key)
        result = poll(task_id, api_key, timeout=args.timeout, interval=args.interval)

        all_results["total"] += result["total"]
        for key in ("valid", "invalid", "domain_error", "unknown", "unchecked"):
            all_results[key].extend(result.get(key, []))

    # Summary
    print(
        f"\nVerification complete: "
        f"{len(all_results['valid'])} valid, "
        f"{len(all_results['invalid'])} invalid, "
        f"{len(all_results['domain_error'])} domain_error, "
        f"{len(all_results['unknown'])} unknown"
        + (f", {len(all_results['unchecked'])} still processing" if all_results["unchecked"] else ""),
        file=sys.stderr,
    )

    print(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    main()
