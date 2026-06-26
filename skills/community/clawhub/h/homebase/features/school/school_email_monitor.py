#!/usr/bin/env python3
"""
School Email Monitor
Monitors Gmail for important school updates and PDF flyers.
Filters out routine check-in/out and daily summary emails.
"""

import json
import os
import sys
import base64
from core.keychain_secrets import load_google_secrets, keyring_module_available, last_keyring_error
load_google_secrets()
from datetime import datetime
from typing import Dict, List, Optional

from utils import write_json_atomic


class SchoolEmailMonitor:
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.config_file = os.path.join(base_path, "config.json")
        # FIX: Track processed email IDs to avoid re-processing on every run
        self.processed_ids_file = os.path.join(base_path, "calendar_data", "processed_email_ids.json")
        # Separate tracking for calendar sync — independent from WhatsApp summary dedup
        self.calendar_synced_ids_file = os.path.join(base_path, "calendar_data", "calendar_synced_ids.json")
        # Dedup auth-error notifications — only WhatsApp-notify once until the token is fixed
        self.auth_error_state_file = os.path.join(base_path, "calendar_data", "auth_error_state.json")
        os.makedirs(os.path.dirname(self.processed_ids_file), exist_ok=True)
        self.load_config()
        self.processed_ids = self._load_processed_ids()
        self.calendar_synced_ids = self._load_calendar_synced_ids()

    # ─── Config & State ─────────────────────────────────────────────────────

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}

        # FIX: Resolve ${ENV_VAR} placeholders from environment, same as calendar_aggregator
        for cal in self.config.get("supported_calendars", []):
            for key in ("client_id", "client_secret", "refresh_token", "access_token"):
                val = cal.get(key, "")
                if isinstance(val, str) and val.startswith("${") and val.endswith("}"):
                    env_key = val[2:-1]
                    cal[key] = os.environ.get(env_key, "")

    def _load_processed_ids(self) -> set:
        if os.path.exists(self.processed_ids_file):
            with open(self.processed_ids_file, 'r') as f:
                return set(json.load(f))
        return set()

    def _save_processed_ids(self):
        # Keep only the last 500 IDs to avoid unbounded growth
        ids_list = list(self.processed_ids)[-500:]
        write_json_atomic(self.processed_ids_file, ids_list)

    def _mark_processed(self, msg_id: str):
        self.processed_ids.add(msg_id)
        self._save_processed_ids()

    def _load_calendar_synced_ids(self) -> set:
        if os.path.exists(self.calendar_synced_ids_file):
            with open(self.calendar_synced_ids_file, 'r') as f:
                return set(json.load(f))
        return set()

    def _save_calendar_synced_ids(self):
        # Keep only the last 500 IDs to avoid unbounded growth
        ids_list = list(self.calendar_synced_ids)[-500:]
        write_json_atomic(self.calendar_synced_ids_file, ids_list)

    # ─── Auth-error deduplication ────────────────────────────────────────────

    def _is_auth_error_notified(self) -> bool:
        """Return True if we have already sent a WhatsApp auth-error notification."""
        try:
            if os.path.exists(self.auth_error_state_file):
                with open(self.auth_error_state_file) as f:
                    return json.load(f).get("notified", False)
        except Exception:
            pass
        return False

    def _set_auth_error_notified(self, notified: bool):
        """Persist the auth-error notification flag."""
        try:
            state = {"notified": notified, "updated_at": datetime.now().isoformat()}
            write_json_atomic(self.auth_error_state_file, state)
        except Exception as e:
            print(f"[school_email_monitor] Warning: could not save auth_error_state: {e}")

    # ─── Gmail Auth ──────────────────────────────────────────────────────────

    def get_gmail_service(self):
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        client_id     = os.environ.get("GOOGLE_CLIENT_ID", "")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
        refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN", "")

        if not all([client_id, client_secret, refresh_token]):
            # Distinguish "environment is broken" (interpreter has no `keyring`
            # module → keychain_secrets silently returned empty) from "the user
            # actually needs to re-auth." Telling the user to run reauth_google
            # when keyring isn't even importable is worse than silence — they
            # run the script, it appears to work, the cron still fails, they
            # lose trust in every alert.
            if not keyring_module_available():
                print(json.dumps({
                    "status": "env_broken",
                    "error": "keyring module unavailable in current interpreter",
                    "interpreter": sys.executable,
                    "detail": last_keyring_error(),
                }))
                print("NO_REPLY")
                return None
            print("Error: No valid Google credentials found for Gmail.")
            return None

        creds = Credentials(
            token="",
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )

        try:
            creds.refresh(Request())
            # Successful auth — clear any previous error flag so future failures notify fresh
            self._set_auth_error_notified(False)
            return build('gmail', 'v1', credentials=creds)
        except Exception as e:
            err_str = str(e)
            if self._is_auth_error_notified():
                # Already notified — log silently, output NO_REPLY so agent sends nothing
                print(f"[auth-suppressed] Token still invalid ({err_str[:60]}). Run `python core/reauth_google.py` to fix.")
                print("NO_REPLY")
            else:
                # First failure — surface it to WhatsApp once, then set the flag
                print(
                    f"⚠️ *Google auth error — school emails paused*\n\n"
                    f"The Google refresh token has expired or been revoked.\n"
                    f"School email monitoring is paused until re-authenticated.\n\n"
                    f"*To fix:*\n"
                    f"  cd ~/.openclaw/workspace/skills/homebase\n"
                    f"  python core/reauth_google.py\n\n"
                    f"_(This message will not repeat until the token is fixed and breaks again.)_"
                )
                self._set_auth_error_notified(True)
            return None
    # ─── Email Body Extraction ───────────────────────────────────────────────

    def _extract_body_and_attachments(self, payload: Dict) -> tuple:
        """
        FIX: Recursive multipart parser — original only went 1 level deep,
        missing content in nested multipart/alternative or multipart/mixed structures.
        Returns (body_text, has_pdf).
        """
        body = ""
        has_pdf = False
        mime = payload.get("mimeType", "")

        if mime == "text/plain":
            data = payload.get("body", {}).get("data", "")
            if data:
                body += base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

        elif mime == "application/pdf":
            has_pdf = True

        elif mime.startswith("multipart/"):
            for part in payload.get("parts", []):
                sub_body, sub_pdf = self._extract_body_and_attachments(part)
                body += sub_body
                if sub_pdf:
                    has_pdf = True

        # Fallback: non-multipart with body data but unknown mime
        elif "data" in payload.get("body", {}):
            try:
                body += base64.urlsafe_b64decode(
                    payload["body"]["data"]
                ).decode("utf-8", errors="replace")
            except Exception:
                pass

        return body, has_pdf

    # ─── Core Fetch ─────────────────────────────────────────────────────────

    def fetch_recent_school_emails(self, skip_processed: bool = True) -> List[Dict]:
        """
        Fetch recent school emails from Gmail.
        Skips already-processed message IDs by default.
        """
        service = self.get_gmail_service()
        if not service:
            return []

        # Build query from config — no hardcoded school domains
        try:
            from core.config_loader import config as _cfg
            query = _cfg.school_email_query or ""
        except Exception:
            query = ""
        if not query:
            return []

        try:
            results = service.users().messages().list(
                userId='me', q=query, maxResults=20
            ).execute()
            messages = results.get('messages', [])

            email_data = []
            for msg in messages:
                msg_id = msg['id']

                # FIX: Skip already-processed emails properly (was a comment placeholder)
                if skip_processed and msg_id in self.processed_ids:
                    continue

                txt = service.users().messages().get(
                    userId='me', id=msg_id, format='full'
                ).execute()

                headers = txt['payload'].get('headers', [])
                subject = next(
                    (h['value'] for h in headers if h['name'].lower() == 'Subject'.lower()),
                    'No Subject'
                )
                sender = next(
                    (h['value'] for h in headers if h['name'].lower() == 'From'.lower()),
                    'Unknown Sender'
                )
                date_str = next(
                    (h['value'] for h in headers if h['name'].lower() == 'Date'.lower()),
                    ''
                )

                # FIX: Use recursive parser instead of shallow 1-level check
                body, has_pdf = self._extract_body_and_attachments(txt['payload'])

                # Filter out daily summaries and routine check-in/check-out emails
                combined = (subject + " " + body).lower()
                if any(kw in combined for kw in ["daily summary", "checked in", "checked out", "check-in", "check-out"]):
                    self._mark_processed(msg_id)
                    continue

                # FIX: Context limit is now configurable via config instead of hardcoded 1500
                ctx_limit = self.config.get("email_body_context_limit", 2000)

                email_data.append({
                    "id": msg_id,
                    "subject": subject,
                    "sender": sender,
                    "date": date_str,
                    "body": body[:ctx_limit],
                    "has_pdf_attachment": has_pdf,
                    "fetched_at": datetime.now().isoformat(),
                    # Raw Gmail payload kept for PDF attachment download in calendar sync
                    "_payload": txt['payload'],
                })

                self._mark_processed(msg_id)

            return email_data

        except Exception as e:
            print(f"Error fetching Gmail: {e}")
            return []

    def format_for_whatsapp(self, emails: List[Dict]) -> Optional[str]:
        """
        Format fetched school emails into a WhatsApp-ready summary string.
        Returns None if there are no emails to report.
        """
        if not emails:
            return None

        lines = ["📚 *School Updates*\n"]
        for email in emails:
            lines.append(f"📧 *{email['subject']}*")
            lines.append(f"From: {email['sender']}")
            if email.get("has_pdf_attachment"):
                lines.append("📎 PDF attachment detected")
            # Show a brief snippet of the body
            snippet = email.get("body", "")[:300].strip()
            if snippet:
                lines.append(f"_{snippet}..._" if len(email.get("body", "")) > 300 else f"_{snippet}_")
            lines.append("")  # blank line between emails

        return "\n".join(lines).strip()


if __name__ == "__main__":
    # Output school emails as JSON for the agent to process and deliver via OpenClaw.
    # Top-level guard so cron always sees a parseable status, even on crash.
    import json as _json
    import sys as _sys
    import traceback as _tb
    try:
        # Bail early if the interpreter can't read Keychain — emit a parseable
        # env_broken status + NO_REPLY so the agent suppresses delivery instead
        # of firing a misleading credentials-missing DM. The Daily Owner Health
        # Digest will roll up these env_broken events overnight.
        if not keyring_module_available():
            print(_json.dumps({
                "status": "env_broken",
                "error": "keyring module unavailable in cron interpreter",
                "interpreter": _sys.executable,
                "detail": last_keyring_error(),
            }))
            print("NO_REPLY")
            _sys.exit(0)
        from core.config_loader import SKILL_DIR
        monitor = SchoolEmailMonitor(SKILL_DIR)
        emails = monitor.fetch_recent_school_emails()
        if emails:
            summary = monitor.format_for_whatsapp(emails)
            print(_json.dumps({"status": "emails_found", "count": len(emails), "summary": summary}, indent=2))
        else:
            print(_json.dumps({"status": "no_new_emails"}))
    except Exception as _e:
        print(_json.dumps({
            "status": "crashed",
            "error": str(_e),
            "traceback": _tb.format_exc(),
        }, indent=2))
        _sys.exit(1)