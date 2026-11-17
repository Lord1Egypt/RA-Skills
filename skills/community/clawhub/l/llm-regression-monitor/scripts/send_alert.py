"""send_alert.py — Send an alert if monitor_report.json contains failures.

Reads monitor_report.json and sends a formatted message via:
  - WhatsApp (wacli) if ALERT_WHATSAPP_TO is set
  - Slack webhook if ALERT_SLACK_WEBHOOK is set
  - Discord webhook if ALERT_DISCORD_WEBHOOK is set
  - Email (SMTP) if ALERT_EMAIL_TO and ALERT_EMAIL_FROM are set
  - Always: stdout + appended to monitor_alerts.log

Exits silently with code 0 if all tests passed (no noise on green runs).
"""

from __future__ import annotations

import json
import os
import smtplib
import subprocess
import sys
from datetime import datetime, timezone
from email.mime.text import MIMEText
from pathlib import Path

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def load_report(path: Path) -> dict:
    if not path.exists():
        print(f"ERROR: Report not found at {path}")
        print("Run run_monitor.py first to generate it.")
        sys.exit(1)

    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Could not parse {path}: {e}")
        sys.exit(1)


def format_alert(report: dict) -> str:
    ts = report.get("timestamp", "")
    try:
        dt = datetime.fromisoformat(ts).astimezone()
        ts_display = dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        ts_display = ts[:16] if ts else "unknown time"

    total = report["total"]
    passed = report["passed"]
    failed = report["failed"]

    lines = [
        f"LLM Regression Detected - {ts_display}",
        "",
        f"Tests run: {total} | Passed: {passed} | FAILED: {failed}",
        "",
    ]

    for r in report["results"]:
        name = r["name"]
        provider = r["provider"]
        model = r["model"]

        if r["passed"]:
            lines.append(f"PASS  {name} ({provider} / {model})")
            continue

        if r["status"] == "error":
            lines.append(f"ERROR {name} ({provider} / {model})")
            lines.append(f"      {r['error']}")
            continue

        lines.append(f"FAIL  {name} ({provider} / {model})")

        drift = r.get("drift")
        if drift and drift["enabled"] and not drift["passed"]:
            score = drift["score"]
            threshold = drift["threshold"]
            score_str = f"{score:.2f}" if score is not None else "N/A"
            lines.append(f"      Drift score: {score_str} < threshold {threshold}")

            # Show output preview for context
            preview = r.get("output_preview", "")
            if preview:
                lines.append(f"      Current:  \"{preview[:100]}\"")

        for a in r.get("assertion_results", []):
            if not a["passed"]:
                score_str = f" [score: {a['score']}]" if a["score"] is not None else ""
                lines.append(f"      Assertion({a['type']}) FAILED{score_str}: {a['message']}")

    return "\n".join(lines)


def send_whatsapp(message: str, to: str) -> bool:
    """Send via wacli. Returns True on success."""
    try:
        result = subprocess.run(
            ["wacli", "send", "--to", to, "--message", message],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            print(f"WhatsApp alert sent to {to}")
            return True
        else:
            print(f"WhatsApp send failed (exit {result.returncode}): {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("WhatsApp alert skipped: wacli not found. Install wacli to enable WhatsApp alerts.")
        return False
    except subprocess.TimeoutExpired:
        print("WhatsApp alert timed out after 30s.")
        return False
    except Exception as e:
        print(f"WhatsApp alert failed: {e}")
        return False


def send_slack(message: str, webhook_url: str) -> bool:
    """Send via Slack incoming webhook. Returns True on success."""
    try:
        import requests
    except ImportError:
        print("Slack alert skipped: requests not installed. Install with: pip install requests")
        return False

    try:
        payload = {"text": f"```{message}```"}
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Slack alert sent.")
            return True
        else:
            print(f"Slack send failed (HTTP {response.status_code}): {response.text[:200]}")
            return False
    except Exception as e:
        print(f"Slack alert failed: {e}")
        return False


def send_discord(message: str, webhook_url: str) -> bool:
    """Send via Discord incoming webhook. Returns True on success."""
    try:
        import requests
    except ImportError:
        print("Discord alert skipped: requests not installed. Install with: pip install requests")
        return False

    try:
        payload = {"content": f"```{message}```"}
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code in (200, 204):
            print("Discord alert sent.")
            return True
        else:
            print(f"Discord send failed (HTTP {response.status_code}): {response.text[:200]}")
            return False
    except Exception as e:
        print(f"Discord alert failed: {e}")
        return False


def send_email(message: str, to: str, from_addr: str, subject: str = "LLM Regression Detected") -> bool:
    """Send via SMTP. Returns True on success.

    Required env vars:
      ALERT_EMAIL_TO       — recipient address
      ALERT_EMAIL_FROM     — sender address
      ALERT_EMAIL_PASSWORD — sender password (app password for Gmail)

    Optional env vars:
      ALERT_EMAIL_SMTP     — SMTP host (default: smtp.gmail.com)
      ALERT_EMAIL_PORT     — SMTP port (default: 587, uses STARTTLS)
    """
    password = os.environ.get("ALERT_EMAIL_PASSWORD")
    if not password:
        print("Email alert skipped: ALERT_EMAIL_PASSWORD is not set.")
        return False

    smtp_host = os.environ.get("ALERT_EMAIL_SMTP", "smtp.gmail.com")
    smtp_port = int(os.environ.get("ALERT_EMAIL_PORT", "587"))

    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to

        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.starttls()
            server.login(from_addr, password)
            server.sendmail(from_addr, [to], msg.as_string())

        print(f"Email alert sent to {to}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("Email alert failed: authentication error. Check ALERT_EMAIL_FROM and ALERT_EMAIL_PASSWORD.")
        return False
    except Exception as e:
        print(f"Email alert failed: {e}")
        return False


def log_to_file(message: str, log_path: Path) -> None:
    with open(log_path, "a") as f:
        f.write(message)
        f.write("\n\n" + "=" * 60 + "\n\n")
    print(f"Alert logged to {log_path}")


def load_trend_warnings(warnings_path: Path) -> list[str]:
    """Load trend warnings written by trend_tracker.py. Returns empty list if none."""
    if not warnings_path.exists():
        return []
    try:
        with open(warnings_path) as f:
            data = json.load(f)
        return data.get("warnings", [])
    except Exception:
        return []


def format_trend_alert(warnings: list[str]) -> str:
    lines = ["LLM Drift Trend Warning", "", "Tests are passing today but scores are declining:"]
    lines.extend(warnings)
    return "\n".join(lines)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Send LLM regression alert from monitor_report.json.")
    parser.add_argument(
        "--report",
        default="monitor_report.json",
        metavar="PATH",
        help="Path to monitor_report.json (default: monitor_report.json)",
    )
    parser.add_argument(
        "--trend-warnings",
        default="trend_warnings.json",
        metavar="PATH",
        help="Path to trend warnings file from trend_tracker.py (default: trend_warnings.json)",
    )
    parser.add_argument(
        "--log",
        default="monitor_alerts.log",
        metavar="PATH",
        help="Path to append alerts log (default: monitor_alerts.log)",
    )
    args = parser.parse_args()

    report_path = Path(args.report)
    log_path = Path(args.log)
    trend_warnings_path = Path(args.trend_warnings)

    report = load_report(report_path)
    trend_warnings = load_trend_warnings(trend_warnings_path)

    # Nothing to alert on — exit silently
    if report["failed"] == 0 and not trend_warnings:
        sys.exit(0)

    # Build message — monitor failures take priority; trend warnings appended or standalone
    if report["failed"] > 0:
        message = format_alert(report)
        if trend_warnings:
            message += "\n\nAdditional trend warnings:\n" + "\n".join(trend_warnings)
    else:
        message = format_trend_alert(trend_warnings)

    # Always print and log
    print("\n" + message + "\n")
    log_to_file(message, log_path)

    # WhatsApp
    whatsapp_to = os.environ.get("ALERT_WHATSAPP_TO")
    if whatsapp_to:
        send_whatsapp(message, whatsapp_to)
    else:
        print("WhatsApp alert skipped: ALERT_WHATSAPP_TO not set.")

    # Slack
    slack_webhook = os.environ.get("ALERT_SLACK_WEBHOOK")
    if slack_webhook:
        send_slack(message, slack_webhook)
    else:
        print("Slack alert skipped: ALERT_SLACK_WEBHOOK not set.")

    # Discord
    discord_webhook = os.environ.get("ALERT_DISCORD_WEBHOOK")
    if discord_webhook:
        send_discord(message, discord_webhook)
    else:
        print("Discord alert skipped: ALERT_DISCORD_WEBHOOK not set.")

    # Email
    email_to = os.environ.get("ALERT_EMAIL_TO")
    email_from = os.environ.get("ALERT_EMAIL_FROM")
    email_subject = "LLM Regression Detected" if report["failed"] > 0 else "LLM Drift Trend Warning"
    if email_to and email_from:
        send_email(message, email_to, email_from, subject=email_subject)
    else:
        print("Email alert skipped: ALERT_EMAIL_TO and ALERT_EMAIL_FROM not set.")


if __name__ == "__main__":
    main()
