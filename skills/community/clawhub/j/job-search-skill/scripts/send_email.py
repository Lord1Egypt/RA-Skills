#!/usr/bin/env python3
"""
send_email.py
Reads data/scored_jobs.json (written by the agent after scoring) and sends
a formatted HTML digest email via SMTP.

Only runs if config.json → email.enabled is true.
Called by the agent AFTER it has already output results in chat.

Usage:
  python scripts/send_email.py --jobs '[{"title":...}, ...]'   # JSON string from agent
  python scripts/send_email.py                                  # reads data/scored_jobs.json
"""

import json
import smtplib
import sys
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

BASE_DIR    = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "workspace" / "config.json"
JOBS_PATH   = BASE_DIR / "data" / "scored_jobs.json"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def score_color(score):
    if score >= 8: return "#16a34a"
    if score >= 6: return "#d97706"
    return "#dc2626"

def score_label(score):
    if score >= 8: return "Strong fit"
    if score >= 6: return "Good fit"
    return "Moderate fit"


def build_html(jobs, run_date):
    strong   = sum(1 for j in jobs if j.get("score", 0) >= 8)
    good     = sum(1 for j in jobs if 6 <= j.get("score", 0) < 8)
    moderate = sum(1 for j in jobs if j.get("score", 0) < 6)

    def render_job(job):
        score = job.get("score", 0)
        col   = score_color(score)
        label = score_label(score)
        tags  = job.get("tags", [])
        tag_html = ""
        if tags:
            tag_html = "<div style='margin-top:6px;'>" + "".join(
                f"<span style='background:#f3f4f6;border:1px solid #e5e7eb;border-radius:3px;"
                f"padding:2px 7px;font-size:11px;color:#374151;margin-right:4px;'>{t}</span>"
                for t in tags[:8]
            ) + "</div>"

        return f"""
        <div style="border:1px solid #e5e7eb;border-left:4px solid {col};border-radius:6px;
                    padding:16px 18px;margin-bottom:12px;background:#fff;">
          <div style="display:flex;justify-content:space-between;gap:12px;">
            <div style="flex:1;">
              <a href="{job.get('url','')}" style="font-size:15px;font-weight:600;
                 color:#111827;text-decoration:none;">{job.get('title','')}</a>
              <div style="color:#6b7280;font-size:13px;margin-top:2px;">
                {job.get('company','')} &nbsp;·&nbsp; {job.get('location','')}
              </div>
              {tag_html}
            </div>
            <div style="text-align:center;flex-shrink:0;">
              <div style="background:{col};color:#fff;border-radius:50%;width:42px;height:42px;
                          display:flex;align-items:center;justify-content:center;
                          font-size:17px;font-weight:700;margin:0 auto;">{score}</div>
              <div style="font-size:10px;color:{col};font-weight:600;margin-top:3px;">{label}</div>
            </div>
          </div>
          <div style="margin-top:10px;font-size:13px;color:#374151;line-height:1.5;
                      padding:9px 12px;background:#f9fafb;border-radius:4px;">
            <strong>Why:</strong> {job.get('justification', 'See listing for details.')}
          </div>
          <div style="margin-top:10px;">
            <a href="{job.get('url','')}" style="display:inline-block;padding:6px 14px;
               background:#1d4ed8;color:#fff;border-radius:4px;font-size:13px;
               font-weight:600;text-decoration:none;">View &amp; Apply →</a>
          </div>
        </div>"""

    # Group by source
    by_source = {}
    for job in jobs:
        src = job.get("source", "Other")
        by_source.setdefault(src, []).append(job)

    sections = ""
    source_icons = {"LinkedIn": "🔵", "Infostud": "🇷🇸", "HelloWorld": "🌍"}
    for src, src_jobs in by_source.items():
        icon = source_icons.get(src, "📋")
        cards = "\n".join(render_job(j) for j in src_jobs)
        sections += f"""
        <div style="margin-bottom:28px;">
          <h2 style="font-size:13px;font-weight:700;color:#6b7280;text-transform:uppercase;
                     letter-spacing:.07em;margin:0 0 12px;padding-bottom:6px;
                     border-bottom:1px solid #e5e7eb;">{icon} {src} ({len(src_jobs)})</h2>
          {cards}
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f3f4f6;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
<div style="max-width:660px;margin:28px auto;">
  <div style="background:#111827;border-radius:8px 8px 0 0;padding:24px 28px;">
    <div style="font-size:20px;font-weight:700;color:#fff;">Job Digest</div>
    <div style="font-size:12px;color:#9ca3af;margin-top:3px;">{run_date}</div>
  </div>
  <div style="background:#1f2937;padding:14px 28px;display:flex;gap:20px;">
    <div style="color:#fff;"><span style="font-size:22px;font-weight:700;">{len(jobs)}</span>
      <span style="font-size:12px;color:#9ca3af;margin-left:4px;">listings</span></div>
    <div style="color:#16a34a;"><span style="font-size:18px;font-weight:700;">{strong}</span>
      <span style="font-size:12px;margin-left:3px;">strong</span></div>
    <div style="color:#d97706;"><span style="font-size:18px;font-weight:700;">{good}</span>
      <span style="font-size:12px;margin-left:3px;">good</span></div>
    <div style="color:#ef4444;"><span style="font-size:18px;font-weight:700;">{moderate}</span>
      <span style="font-size:12px;margin-left:3px;">moderate</span></div>
  </div>
  <div style="background:#fff;padding:24px 28px;border-radius:0 0 8px 8px;">
    {sections}
    <div style="margin-top:24px;padding-top:14px;border-top:1px solid #e5e7eb;
                font-size:11px;color:#9ca3af;text-align:center;">
      Generated by job-search-belgrade skill · Apply manually · Never auto-submitted.
    </div>
  </div>
</div></body></html>"""


def send(config, subject, html):
    ec = config["email"]
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{ec['sender_name']} <{ec['smtp_user']}>"
    msg["To"]      = ec["recipient"]
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(ec["smtp_host"], ec["smtp_port"]) as srv:
        srv.ehlo()
        srv.starttls()
        srv.login(ec["smtp_user"], ec["smtp_pass"])
        srv.sendmail(ec["smtp_user"], ec["recipient"], msg.as_string())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", default="", help="JSON array of scored jobs from agent")
    args = parser.parse_args()

    config = load_config()
    email_cfg = config.get("email", {})

    if not email_cfg.get("enabled", False):
        print("Email is disabled in config.json (email.enabled = false). Skipping.")
        return

    # Load jobs — from agent argument or from file
    if args.jobs:
        try:
            jobs = json.loads(args.jobs)
        except json.JSONDecodeError as e:
            print(f"ERROR: Could not parse --jobs JSON: {e}")
            sys.exit(1)
    elif JOBS_PATH.exists():
        with open(JOBS_PATH, encoding="utf-8") as f:
            jobs = json.load(f)
    else:
        print("No jobs to send. Pass --jobs or ensure data/scored_jobs.json exists.")
        return

    if not jobs:
        print("Job list is empty. Nothing to email.")
        return

    run_date = datetime.now().strftime("%A, %d %B %Y — %H:%M")
    subject  = f"Job Digest — {len(jobs)} listings · {datetime.now().strftime('%d %b %Y')}"
    html     = build_html(jobs, run_date)

    print(f"Sending to {email_cfg['recipient']}...")
    try:
        send(config, subject, html)
        print(f"✓ Email sent ({len(jobs)} jobs)")
    except Exception as e:
        print(f"✗ Email failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
