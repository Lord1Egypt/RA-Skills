#!/usr/bin/env python3
"""
Run a complete Mailgo campaign: upload content, create campaign, add leads, activate.

Usage:
    python3 run_campaign.py \\
        --sender "user@outlook.com" \\
        --subject "Your subject" \\
        --body "<html><body><p>Hello</p></body></html>" \\
        --recipients "alice@example.com,bob@test.com" \\
        --campaign-name "My Campaign"

    Or read recipients from a file (CSV, XLSX, TXT, JSON):
    python3 run_campaign.py \\
        --sender "user@outlook.com" \\
        --subject "Your subject" \\
        --body "<html><body><p>Hello</p></body></html>" \\
        --recipients-file leads.xlsx \\
        --campaign-name "My Campaign"

Optional flags:
    --recipient-names "Alice,Bob"       Comma-separated display names (same order as recipients)
                                        If omitted, names are auto-derived from email prefixes
                                        e.g. alice.smith@co.com -> "Alice Smith"
    --recipient-companies "Acme,Globex" Comma-separated company names
    --recipient-titles "CEO,CTO"        Comma-separated job titles
    --recipient-domains "acme.com,..."  Comma-separated company websites
    --recipients-file "leads.xlsx"      Read recipients from file (CSV/XLSX/TXT/JSON)
                                        Auto-detects email, name, company, title, domain columns
    --email-column "email"              Override auto-detected email column name
    --name-column "name"                Override auto-detected name column name
    --company-column "company"          Override auto-detected company column name
    --title-column "title"              Override auto-detected title column name
    --domain-column "domain"            Override auto-detected domain column name
    --body-file "email.html"            Read HTML body from file instead of --body
     --timezone-id "Asia/Singapore"      Timezone ID (default: Asia/Singapore)
     --timezone-offset "+08:00"          UTC offset (default: +08:00)
    --send-days "1,2,3,4,5"            Days of week: 1=Mon..7=Sun (default: Mon-Fri)
    --send-hours "9,18"                 Start,end hour 0-23 (default: 9,18)
    --daily-limit 50                    Daily sending limit (default: 50)
    --no-tracking                       Disable open/click tracking
    --dry-run                           Stop after creating campaign (do not activate)

Requires:
    MAILGO_API_KEY environment variable
    openpyxl (only if reading .xlsx files: pip install openpyxl)

Output:
    JSON summary on stdout with campaignId, emailContentId, and lead counts.
    Progress messages on stderr.
"""

import argparse
import csv
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request

_ssl_ctx = ssl.create_default_context()
# Do NOT disable certificate verification — MITM attacks would allow token theft

BASE = "https://api.leadsnavi.com"


def make_headers(api_key):
    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "mailgo-mcp-server/1.0 (https://github.com/netease-im/leadsnavi-mcp-server)",
    }


def post(api_key, prefix, path, body):
    url = f"{BASE}{prefix}{path}"
    data = json.dumps(body).encode("utf-8")
    headers = make_headers(api_key)
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    print(f"POST {url}", file=sys.stderr)
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if not result.get("success", False):
                print(f"API error: {result.get('message', 'unknown')}", file=sys.stderr)
                sys.exit(1)
            return result
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {err_body[:500]}", file=sys.stderr)
        sys.exit(1)


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

_EMAIL_COL_NAMES = {"email", "e-mail", "mail", "emailaddress", "email_address",
                    "contact_email", "contactemail", "recipient", "to"}
_NAME_COL_NAMES = {"name", "contactname", "contact_name", "fullname", "full_name",
                   "first_name", "firstname", "display_name", "displayname",
                   "recipient_name"}
_COMPANY_COL_NAMES = {"company", "companyname", "company_name", "organization",
                      "org", "organisation", "employer", "firm", "business",
                      "contact_company", "contactcompany"}
_TITLE_COL_NAMES = {"title", "jobtitle", "job_title", "position", "role",
                    "job", "designation", "contact_title", "contacttitle"}
_DOMAIN_COL_NAMES = {"domain", "website", "web", "url", "site", "homepage",
                     "company_domain", "companydomain", "company_website",
                     "companywebsite"}


def _looks_like_email(val):
    return isinstance(val, str) and _EMAIL_RE.match(val.strip()) is not None


def _detect_email_col(headers, rows):
    """Return the header name of the column most likely to contain emails."""
    lower_map = {h: h.strip().lower().replace(" ", "_") for h in headers}
    for h in headers:
        if lower_map[h] in _EMAIL_COL_NAMES:
            return h
    best_col, best_count = None, 0
    for h in headers:
        count = sum(1 for row in rows if _looks_like_email(row.get(h, "")))
        if count > best_count:
            best_col, best_count = h, count
    return best_col


def _detect_name_col(headers, email_col):
    """Return the header name of the column most likely to contain names."""
    return _detect_col_by_names(headers, _NAME_COL_NAMES, exclude={email_col})


def _detect_col_by_names(headers, known_names, exclude=None):
    """Return the header matching known_names, excluding specified columns."""
    exclude = exclude or set()
    lower_map = {h: h.strip().lower().replace(" ", "_") for h in headers}
    for h in headers:
        if h in exclude:
            continue
        if lower_map[h] in known_names:
            return h
    return None


def _detect_company_col(headers, email_col):
    """Return the header name of the column most likely to contain company names."""
    return _detect_col_by_names(headers, _COMPANY_COL_NAMES, exclude={email_col})


def _detect_title_col(headers, email_col):
    """Return the header name of the column most likely to contain job titles."""
    return _detect_col_by_names(headers, _TITLE_COL_NAMES, exclude={email_col})


def _detect_domain_col(headers, email_col):
    """Return the header name of the column most likely to contain domains."""
    return _detect_col_by_names(headers, _DOMAIN_COL_NAMES, exclude={email_col})


def _read_txt(path):
    """One email per line, no name/company/title/domain columns."""
    recipients = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            val = line.strip()
            if val and _looks_like_email(val):
                recipients.append(val)
    return recipients, [], [], [], []


def _read_csv(path, email_col_override=None, name_col_override=None,
              company_col_override=None, title_col_override=None,
              domain_col_override=None):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)
    return _extract_from_rows(headers, rows, email_col_override, name_col_override,
                              company_col_override, title_col_override, domain_col_override)


def _read_xlsx(path, email_col_override=None, name_col_override=None,
               company_col_override=None, title_col_override=None,
               domain_col_override=None):
    try:
        import openpyxl
    except ImportError:
        print("Error: openpyxl is required to read .xlsx files. "
              "Install with: pip install openpyxl", file=sys.stderr)
        sys.exit(1)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    all_rows = list(ws.iter_rows(values_only=True))
    wb.close()

    if not all_rows:
        return [], [], [], [], []

    # Detect whether the first row is a header or data
    first_row = [str(c) if c is not None else "" for c in all_rows[0]]
    first_row_has_email = any(_looks_like_email(v) for v in first_row)

    if first_row_has_email and not email_col_override:
        # First row looks like data (no header) — treat all rows as data
        # Build synthetic headers: col_0, col_1, ...
        num_cols = max(len(r) for r in all_rows)
        headers = [f"col_{i}" for i in range(num_cols)]
        rows = []
        for raw_row in all_rows:
            rows.append({headers[i]: (str(raw_row[i]) if i < len(raw_row) and raw_row[i] is not None else "")
                         for i in range(num_cols)})
    else:
        # First row is a header
        headers = first_row
        rows = []
        for raw_row in all_rows[1:]:
            rows.append({headers[i]: (str(raw_row[i]) if i < len(raw_row) and raw_row[i] is not None else "")
                         for i in range(len(headers))})

    return _extract_from_rows(headers, rows, email_col_override, name_col_override,
                              company_col_override, title_col_override, domain_col_override)


def _read_json(path, email_col_override=None, name_col_override=None,
               company_col_override=None, title_col_override=None,
               domain_col_override=None):
    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], str):
            return [e.strip() for e in data if _looks_like_email(e.strip())], [], [], [], []
        if isinstance(data[0], dict):
            headers = list(data[0].keys())
            return _extract_from_rows(headers, data, email_col_override, name_col_override,
                                      company_col_override, title_col_override, domain_col_override)
    print("Error: JSON must be an array of emails or an array of objects", file=sys.stderr)
    sys.exit(1)


def _extract_from_rows(headers, rows, email_col_override, name_col_override,
                       company_col_override=None, title_col_override=None,
                       domain_col_override=None):
    email_col = email_col_override or _detect_email_col(headers, rows)
    if not email_col:
        print(f"Error: could not detect email column. Headers: {headers}\n"
              f"Use --email-column to specify.", file=sys.stderr)
        sys.exit(1)
    name_col = name_col_override or _detect_name_col(headers, email_col)
    company_col = company_col_override or _detect_company_col(headers, email_col)
    title_col = title_col_override or _detect_title_col(headers, email_col)
    domain_col = domain_col_override or _detect_domain_col(headers, email_col)

    detected = [f"email: '{email_col}'"]
    if name_col:
        detected.append(f"name: '{name_col}'")
    if company_col:
        detected.append(f"company: '{company_col}'")
    if title_col:
        detected.append(f"title: '{title_col}'")
    if domain_col:
        detected.append(f"domain: '{domain_col}'")
    print(f"  Detected columns: {', '.join(detected)}", file=sys.stderr)

    recipients, names, companies, titles, domains = [], [], [], [], []
    for row in rows:
        email_val = str(row.get(email_col, "")).strip()
        if not email_val or not _looks_like_email(email_val):
            continue
        recipients.append(email_val)
        if name_col:
            names.append(str(row.get(name_col, "")).strip())
        if company_col:
            companies.append(str(row.get(company_col, "")).strip())
        if title_col:
            titles.append(str(row.get(title_col, "")).strip())
        if domain_col:
            domains.append(str(row.get(domain_col, "")).strip())
    return recipients, names, companies, titles, domains


def read_recipients_file(path, email_col=None, name_col=None,
                         company_col=None, title_col=None, domain_col=None):
    """Read recipients from a file. Returns (recipients, names, companies, titles, domains) lists."""
    ext = os.path.splitext(path)[1].lower()
    print(f"  Reading recipients from: {path} ({ext})", file=sys.stderr)
    if ext == ".txt":
        return _read_txt(path)
    elif ext == ".csv":
        return _read_csv(path, email_col, name_col, company_col, title_col, domain_col)
    elif ext in (".xlsx", ".xls"):
        return _read_xlsx(path, email_col, name_col, company_col, title_col, domain_col)
    elif ext == ".json":
        return _read_json(path, email_col, name_col, company_col, title_col, domain_col)
    else:
        # Try CSV as fallback
        print(f"  Unknown extension '{ext}', trying CSV format...", file=sys.stderr)
        return _read_csv(path, email_col, name_col, company_col, title_col, domain_col)


def main():
    parser = argparse.ArgumentParser(description="Create and activate a Mailgo campaign")
    parser.add_argument("--sender", required=True, help="Sender email address")
    parser.add_argument("--subject", required=True, help="Email subject line")
    parser.add_argument("--body", default="", help="HTML email body content")
    parser.add_argument("--body-file", default="", help="Read HTML body from file instead of --body")
    parser.add_argument("--recipients", default="", help="Comma-separated recipient emails")
    parser.add_argument("--recipients-file", default="", help="Read recipients from file (CSV/XLSX/TXT/JSON)")
    parser.add_argument("--email-column", default="", help="Override auto-detected email column name")
    parser.add_argument("--name-column", default="", help="Override auto-detected name column name")
    parser.add_argument("--company-column", default="", help="Override auto-detected company column name")
    parser.add_argument("--title-column", default="", help="Override auto-detected title/job column name")
    parser.add_argument("--domain-column", default="", help="Override auto-detected domain/website column name")
    parser.add_argument("--campaign-name", default="Campaign", help="Campaign name")
    parser.add_argument("--recipient-names", default="", help="Comma-separated display names (auto-derived from email prefix if omitted)")
    parser.add_argument("--recipient-companies", default="", help="Comma-separated company names")
    parser.add_argument("--recipient-titles", default="", help="Comma-separated job titles")
    parser.add_argument("--recipient-domains", default="", help="Comma-separated company websites/domains")
    parser.add_argument("--timezone-id", default="Asia/Singapore", help="Timezone ID")
    parser.add_argument("--timezone-offset", default="+08:00", help="UTC offset")
    parser.add_argument("--send-days", default="1,2,3,4,5", help="Days of week (1=Mon..7=Sun)")
    parser.add_argument("--send-hours", default="9,18", help="Start,end hour")
    parser.add_argument("--daily-limit", type=int, default=50, help="Daily sending limit")
    parser.add_argument("--no-tracking", action="store_true", help="Disable open/click tracking")
    parser.add_argument("--dry-run", action="store_true", help="Create but do not activate")
    args = parser.parse_args()

    if not args.recipients and not args.recipients_file:
        print("Error: provide either --recipients or --recipients-file", file=sys.stderr)
        sys.exit(1)

    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8-sig") as f:
            body = f.read().strip()
        print(f"  Read email body from: {args.body_file} ({len(body)} chars)", file=sys.stderr)
    elif args.body:
        body = args.body
    else:
        print("Error: provide either --body or --body-file", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("MAILGO_API_KEY")
    if not api_key:
        print("Error: MAILGO_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    if args.recipients_file:
        recipients, file_names, file_companies, file_titles, file_domains = read_recipients_file(
            args.recipients_file,
            args.email_column or None,
            args.name_column or None,
            args.company_column or None,
            args.title_column or None,
            args.domain_column or None,
        )
        names = [n.strip() for n in args.recipient_names.split(",") if n.strip()] if args.recipient_names else file_names
        companies = [c.strip() for c in args.recipient_companies.split(",") if c.strip()] if args.recipient_companies else file_companies
        titles = [t.strip() for t in args.recipient_titles.split(",") if t.strip()] if args.recipient_titles else file_titles
        domains = [d.strip() for d in args.recipient_domains.split(",") if d.strip()] if args.recipient_domains else file_domains
    else:
        recipients = [e.strip() for e in args.recipients.split(",") if e.strip()]
        names = [n.strip() for n in args.recipient_names.split(",") if n.strip()] if args.recipient_names else []
        companies = [c.strip() for c in args.recipient_companies.split(",") if c.strip()] if args.recipient_companies else []
        titles = [t.strip() for t in args.recipient_titles.split(",") if t.strip()] if args.recipient_titles else []
        domains = [d.strip() for d in args.recipient_domains.split(",") if d.strip()] if args.recipient_domains else []

    def name_from_email(email):
        prefix = email.split("@")[0]
        return " ".join(part.capitalize() for part in prefix.replace("_", ".").replace("-", ".").split("."))

    if not names:
        names = [name_from_email(e) for e in recipients]
        print(f"  Auto-derived recipient names from email prefixes: {names}", file=sys.stderr)

    # Report available recipient fields
    field_report = ["name"]
    if companies:
        field_report.append("company")
    if titles:
        field_report.append("title")
    if domains:
        field_report.append("domain")
    print(f"  Recipient fields available: {', '.join(field_report)}", file=sys.stderr)

    send_days = [int(d.strip()) for d in args.send_days.split(",")]
    hours = [int(h.strip()) for h in args.send_hours.split(",")]
    tracking = 0 if args.no_tracking else 1

    # Step 1: Upload content
    print("Step 1/4: Uploading email content...", file=sys.stderr)
    r = post(api_key, "/mcp/mailgo-logical", "/api/biz/mailgo/email/content/upload", {
        "emailContent": body
    })
    content_id = r["data"]["emailContentId"]
    print(f"  emailContentId: {content_id}", file=sys.stderr)

    # Step 2: Create campaign
    print("Step 2/4: Creating campaign...", file=sys.stderr)
    r = post(api_key, "/mcp/mailgo-logical", "/api/biz/mailgo/campaign/save", {
        "campaignName": args.campaign_name,
        "basicInfo": {
            "senderEmails": [{"email": args.sender}]
        },
        "scheduleRule": {
            "timeZoneInfo": {
                "id": args.timezone_id,
                "timeZone": args.timezone_offset,
                "timeZoneDesc": args.timezone_id
            },
            "sendingDate": send_days,
            "timeDuration": {"from": hours[0], "to": hours[1]}
        },
        "limitRule": {
            "sendLimit": args.daily_limit,
            "readTracking": tracking,
            "domainLimit": 100000,
            "clickTracking": tracking
        },
        "execRule": {
            "terminateType": 1,
            "providerMatching": 0
        },
        "sequenceInfo": {
            "intervalRule": {
                "timeInterval": [],
                "timeUnit": 1,
                "maxRound": 1
            },
            "mailInfos": [{
                "round": 1,
                "mailType": 0,
                "contentEditInfo": {
                    "emailSubjects": [{"subject": args.subject}],
                    "originalEmailContentId": content_id
                }
            }]
        }
    })
    campaign_id = r["data"]["campaignId"]
    print(f"  campaignId: {campaign_id}", file=sys.stderr)

    # Step 3: Add leads
    print("Step 3/4: Adding leads...", file=sys.stderr)
    leads = []
    for i, email in enumerate(recipients):
        lead = {"contactEmail": email}
        if i < len(names) and names[i]:
            lead["contactName"] = names[i]
        if i < len(companies) and companies[i]:
            lead["companyName"] = companies[i]
        if i < len(titles) and titles[i]:
            lead["title"] = titles[i]
        if i < len(domains) and domains[i]:
            lead["domain"] = domains[i]
        leads.append(lead)

    r = post(api_key, "/mcp/mailgo-logical", "/api/biz/mailgo/leads/add", {
        "campaignId": int(campaign_id),
        "addType": 0,
        "leadsInfos": leads
    })
    leads_data = r.get("data", {})
    success_count = leads_data.get("successCount", 0)
    failed_count = leads_data.get("failedCount", 0)
    print(f"  Added {success_count} leads ({failed_count} failed)", file=sys.stderr)

    # Step 4: Activate
    activated = False
    if not args.dry_run:
        print("Step 4/4: Activating campaign...", file=sys.stderr)
        post(api_key, "/mcp/mailgo-logical", "/api/biz/mailgo/campaign/operate", {
            "campaignId": int(campaign_id),
            "status": 1
        })
        activated = True
        print("  Campaign activated!", file=sys.stderr)
    else:
        print("Step 4/4: Skipped (dry-run mode)", file=sys.stderr)

    # Output summary
    summary = {
        "campaignId": campaign_id,
        "campaignName": args.campaign_name,
        "emailContentId": content_id,
        "sender": args.sender,
        "subject": args.subject,
        "recipientCount": len(recipients),
        "successCount": success_count,
        "failedCount": failed_count,
        "activated": activated
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
