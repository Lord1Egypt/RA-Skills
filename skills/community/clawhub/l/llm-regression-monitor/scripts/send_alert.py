"""send_alert.py — Send an alert if monitor_report.json contains failures.

Reads monitor_report.json and sends a formatted message via:
  - WhatsApp (wacli) if ALERT_WHATSAPP_TO is set
  - Slack webhook if ALERT_SLACK_WEBHOOK is set
  - Always: stdout + appended to monitor_alerts.log

Exits silently with code 0 if all tests passed (no noise on green runs).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
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


def log_to_file(message: str, log_path: Path) -> None:
    with open(log_path, "a") as f:
        f.write(message)
        f.write("\n\n" + "=" * 60 + "\n\n")
    print(f"Alert logged to {log_path}")


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
        "--log",
        default="monitor_alerts.log",
        metavar="PATH",
        help="Path to append alerts log (default: monitor_alerts.log)",
    )
    args = parser.parse_args()

    report_path = Path(args.report)
    log_path = Path(args.log)

    report = load_report(report_path)

    # No failures — exit silently (no noise on green runs)
    if report["failed"] == 0:
        sys.exit(0)

    message = format_alert(report)

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


if __name__ == "__main__":
    main()
