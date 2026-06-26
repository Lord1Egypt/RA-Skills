#!/usr/bin/env python3
"""
Check user activity and send warnings or deliver message if inactive.
This script should be run daily via cron.
Usage: python3 check_activity.py [--dry-run]
"""

import argparse
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))

from database import (
    get_last_chat, update_last_chat, log_check,
    get_message, get_config, get_last_delivery_status, init_db
)
from debug_mode import is_debug_mode


# Warning thresholds (days)
WARNING_1_DAYS = 10
WARNING_2_DAYS = 20
DELIVERY_DAYS = 30


def send_warning_email(config, message, days):
    """Send warning email to the user (not the recipient)."""
    try:
        # Import smtplib here to avoid issues if not configured
        import smtplib
        from email.mime.text import MIMEText

        subject = f"[Last Words] Inactivity Warning - {days} Days"
        body = f"""
This is an automated warning from your Last Words system.

You have been inactive for {days} days.
If you reach {DELIVERY_DAYS} days of inactivity, your final message will be delivered to:
  {config['contact']}

To reset the timer, simply chat with your OpenClaw agent.

---
Last Words System
        """

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = config.get('smtp_user', 'last-words@system.local')
        msg['To'] = config['contact']  # For now, send to the configured contact

        # Send via SMTP if configured
        if config.get('smtp_host'):
            port = config.get('smtp_port', 587)
            if port == 465:
                with smtplib.SMTP_SSL(config['smtp_host'], port) as server:
                    if config.get('smtp_user') and config.get('smtp_pass'):
                        server.login(config['smtp_user'], config['smtp_pass'])
                    server.send_message(msg)
            else:
                with smtplib.SMTP(config['smtp_host'], port) as server:
                    server.starttls()
                    if config.get('smtp_user') and config.get('smtp_pass'):
                        server.login(config['smtp_user'], config['smtp_pass'])
                    server.send_message(msg)
            print(f"  ✓ Warning email sent via {config['smtp_host']}")
        else:
            # Fall back to local mail command
            subprocess.run(['mail', '-s', subject, config['contact']],
                          input=body.encode(), check=False)
            print(f"  ✓ Warning email sent via local mail")

        return True
    except Exception as e:
        print(f"  ✗ Failed to send warning email: {e}", file=sys.stderr)
        return False


def deliver_final_message(config, message, dry_run=False):
    """Deliver the final message to the configured recipient."""
    if dry_run:
        print(f"  [DRY RUN] Would deliver message to {config['contact']}")
        print(f"  [DRY RUN] Message: {message['content'][:100]}...")
        return True

    try:
        if config['method'] == 'email':
            return deliver_via_email(config, message)
        elif config['method'] == 'wechat':
            print("  ⚠ WeChat delivery not yet implemented")
            return False
        elif config['method'] == 'phone':
            print("  ⚠ Phone/SMS delivery not yet implemented")
            return False
        else:
            print(f"  ✗ Unknown delivery method: {config['method']}")
            return False
    except Exception as e:
        print(f"  ✗ Failed to deliver message: {e}", file=sys.stderr)
        return False


def deliver_via_email(config, message):
    """Deliver message via email."""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    subject = "[Last Words] A Message From Your Loved One"

    body = f"""
Dear loved one,

You are receiving this message because it was set as a final message to be delivered
in the event that your loved one has been unreachable for an extended period.

---

{message['content']}

---

This message was prepared with care and love.
With deepest sincerity,
Last Words System
    """

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = config.get('smtp_user', 'last-words@system.local')
    msg['To'] = config['contact']

    msg.attach(MIMEText(body, 'plain'))

    # Attach audio if available
    if message.get('audio_path') and Path(message['audio_path']).exists():
        from email.mime.audio import MIMEAudio
        with open(message['audio_path'], 'rb') as f:
            audio = MIMEAudio(f.read())
            audio.add_header('Content-Disposition', 'attachment',
                           filename=Path(message['audio_path']).name)
            msg.attach(audio)
        print(f"  ✓ Audio attachment included")

    # Send via SMTP if configured
    if config.get('smtp_host'):
        port = config.get('smtp_port', 587)
        # Use SSL for port 465, STARTTLS for port 587
        if port == 465:
            import smtplib
            with smtplib.SMTP_SSL(config['smtp_host'], port) as server:
                if config.get('smtp_user') and config.get('smtp_pass'):
                    server.login(config['smtp_user'], config['smtp_pass'])
                server.send_message(msg)
        else:
            with smtplib.SMTP(config['smtp_host'], port) as server:
                server.starttls()
                if config.get('smtp_user') and config.get('smtp_pass'):
                    server.login(config['smtp_user'], config['smtp_pass'])
                server.send_message(msg)
        print(f"  ✓ Final message delivered via {config['smtp_host']}")
    else:
        # Fall back to local mail command
        subprocess.run(['mail', '-s', subject, config['contact']],
                      input=body.encode(), check=False)
        print(f"  ✓ Final message delivered via local mail")

    return True


def check_sessions():
    """Check OpenClaw sessions for recent activity."""
    try:
        sessions_dir = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
        if not sessions_dir.exists():
            return None

        # Find the most recently modified session file
        latest_time = None
        for session_file in sessions_dir.glob("*.jsonl"):
            mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
            if latest_time is None or mtime > latest_time:
                latest_time = mtime

        return latest_time
    except Exception as e:
        print(f"  ⚠ Could not check sessions: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Check activity and send warnings or deliver message")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="Show what would happen without taking action")
    parser.add_argument("--debug-send", "-d", action="store_true",
                        help="Force immediate send (debug mode)")

    args = parser.parse_args()

    try:
        init_db()

        # Check for debug mode
        debug_mode = is_debug_mode() or args.debug_send

        print(f"\n⏰ Last Words Activity Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)

        if debug_mode:
            print("\n🐛 DEBUG MODE ENABLED")
            print("  Messages can be sent immediately without 30-day wait")
            print("=" * 50)

        # Check for recent session activity
        last_session = check_sessions()
        if last_session:
            print(f"  Last session activity: {last_session.strftime('%Y-%m-%d %H:%M:%S')}")
            # Update last_chat if session is more recent
            last_chat = get_last_chat()
            if last_session > last_chat:
                if not args.dry_run:
                    update_last_chat()
                    print("  ✓ Updated last activity from session data")
                else:
                    print("  [DRY RUN] Would update last activity from session data")

        # Get current inactivity period
        last_chat = get_last_chat()
        days_inactive = (datetime.now() - last_chat).days

        print(f"  Days since last chat: {days_inactive}")

        # Get message and config
        message = get_message()
        config = get_config()
        last_status = get_last_delivery_status()

        if not message:
            print("\n  ⚠ No message configured. Skipping.")
            log_check(days_inactive, warning_sent=False, warning_level=0, delivered=False)
            return

        if not config:
            print("\n  ⚠ No delivery configuration. Skipping.")
            log_check(days_inactive, warning_sent=False, warning_level=0, delivered=False)
            return

        # Determine action based on inactivity OR debug mode
        action_taken = False
        warning_sent = False
        warning_level = 0
        delivered = False

        if debug_mode:
            # Debug mode: allow immediate send
            print(f"\n  🐛 DEBUG MODE: Bypassing 30-day wait")
            print(f"  Ready to deliver message to {config['contact']}...")

            if args.dry_run:
                print(f"  [DRY RUN] Would deliver message immediately in debug mode")
            else:
                if deliver_final_message(config, message, args.dry_run):
                    delivered = True
                    action_taken = True
                    print(f"\n  ✓ Message delivered via DEBUG MODE")

        elif days_inactive >= DELIVERY_DAYS:
            # Time to deliver
            print(f"\n  🚨 INACTIVITY THRESHOLD REACHED ({days_inactive} days)")
            print(f"  Delivering final message to {config['contact']}...")

            if deliver_final_message(config, message, args.dry_run):
                delivered = True
                action_taken = True

        elif days_inactive >= WARNING_2_DAYS:
            # Second warning
            if not last_status or last_status.get('warning_level', 0) < 2:
                print(f"\n  ⚠️ SECOND WARNING ({days_inactive} days inactive)")
                print(f"  Sending warning to {config['contact']}...")

                if not args.dry_run:
                    warning_sent = send_warning_email(config, message, days_inactive)
                else:
                    print(f"  [DRY RUN] Would send second warning")
                    warning_sent = True

                warning_level = 2
                action_taken = True
            else:
                print(f"  Second warning already sent")

        elif days_inactive >= WARNING_1_DAYS:
            # First warning
            if not last_status or last_status.get('warning_level', 0) < 1:
                print(f"\n  ⚠️ FIRST WARNING ({days_inactive} days inactive)")
                print(f"  Sending warning to {config['contact']}...")

                if not args.dry_run:
                    warning_sent = send_warning_email(config, message, days_inactive)
                else:
                    print(f"  [DRY RUN] Would send first warning")
                    warning_sent = True

                warning_level = 1
                action_taken = True
            else:
                print(f"  First warning already sent")

        else:
            print(f"\n  ✓ Activity normal ({days_inactive} days)")

        # Log the check
        if not args.dry_run:
            log_check(days_inactive, warning_sent, warning_level, delivered)

        print("\n" + "=" * 50)

        if delivered:
            print("  ✓ FINAL MESSAGE DELIVERED")
        elif action_taken:
            print(f"  ✓ Action taken (warning level: {warning_level})")
        else:
            print("  ✓ Check complete")

    except Exception as e:
        print(f"\n  ✗ Error during check: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
