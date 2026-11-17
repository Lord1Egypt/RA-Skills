#!/usr/bin/env python3
"""
School Email Monitor
Monitors Gmail for important school updates and PDF flyers.
Filters out routine check-in/out and daily summary emails.
"""

import json
import os
import re
import sys
import base64
from datetime import datetime
from typing import Dict, List, Optional

from utils import (write_json_atomic, append_capped_id, locked_file,
                   read_id_list, AuthErrorFlag)


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
        # Why the last fetch could not happen. See the vocabulary note below.
        self.auth_status: Optional[str] = None
        self.auth_detail: Optional[str] = None
        self.auth_message: Optional[str] = None

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

    # The JSON files are the ordered record; `processed_ids` /
    # `calendar_synced_ids` are in-memory membership indexes over them. See
    # utils.append_capped_id for why the cap must not be applied to the set.
    # utils.read_id_list is the one implementation; kept as a method so the
    # existing call sites read the same.
    _read_id_list = staticmethod(read_id_list)

    def _load_processed_ids(self) -> set:
        self._processed_order = self._read_id_list(self.processed_ids_file)
        return set(self._processed_order)

    def _save_processed_ids(self):
        write_json_atomic(self.processed_ids_file, self._processed_order)

    def _mark_processed(self, msg_id: str):
        # Locked across read -> append -> write, and re-read INSIDE the lock.
        # write_json_atomic prevents a corrupt file; it does nothing about a
        # lost update, and the ordered list is loaded once in __init__. The
        # runner holds one monitor across ~20 sequential Gmail round trips
        # while chat can call mark_email_synced at any moment; last writer
        # wins, and a dropped id means the email is re-fetched and its events
        # re-proposed to the shared family calendar.
        with locked_file(self.processed_ids_file):
            self._processed_order = append_capped_id(
                self._read_id_list(self.processed_ids_file), msg_id)
            self.processed_ids = set(self._processed_order)
            self._save_processed_ids()

    def _load_calendar_synced_ids(self) -> set:
        self._synced_order = self._read_id_list(self.calendar_synced_ids_file)
        return set(self._synced_order)

    def mark_calendar_synced(self, msg_id: str):
        """Record that an email's events reached the calendar."""
        # Same lost-update race as _mark_processed; same remedy.
        with locked_file(self.calendar_synced_ids_file):
            self._synced_order = append_capped_id(
                self._read_id_list(self.calendar_synced_ids_file), msg_id)
            self.calendar_synced_ids = set(self._synced_order)
            self._save_calendar_synced_ids()

    def _save_calendar_synced_ids(self):
        write_json_atomic(self.calendar_synced_ids_file, self._synced_order)

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
            print(f"[school_email_monitor] Warning: could not save auth_error_state: {e}", file=sys.stderr)

    # ─── Gmail Auth ──────────────────────────────────────────────────────────

    # Set when a fetch cannot happen, so callers can tell WHY without parsing
    # stdout. One of:
    #   "no_query"    — school_email_query is empty or unreadable in config
    #   "auth_failed" — gog could not read mail
    #
    # The three-way credential vocabulary that used to live here — env_broken /
    # no_creds / auth_failed — described homebase's OWN credentials, which it
    # no longer has. It existed to stop telling the user to re-authenticate
    # when the real problem was an interpreter without `keyring`. gog owns the
    # token now and reports its own state via `gog auth status`, so the
    # distinction has moved to where it can actually be made.
    #
    # `auth_message` carries the family-facing text for the FIRST auth_failed
    # only; on repeat failures it is None so the caller stays silent. That
    # one-shot behaviour is unchanged and still matters: a revoked token
    # otherwise alerts on every run, four times a day.
    AUTH_HELP = (
        "⚠️ *Google auth error — school emails paused*\n\n"
        "The Google refresh token has expired or been revoked.\n"
        "School email monitoring is paused until re-authenticated.\n\n"
        "*To check:*\n"
        "  gog auth status\n\n"
        "*To fix:*\n"
        "  gog auth add <your-google-account> --services gmail,calendar\n\n"
        "_(This message will not repeat until the token is fixed and breaks again.)_"
    )

    # ─── Email Body Extraction ───────────────────────────────────────────────

    def _extract_body_and_attachments(self, payload: Dict) -> tuple:
        """
        Recursive multipart parser.
        Returns (body_text, has_pdf, has_image).
        """
        body = ""
        has_pdf = False
        has_image = False
        mime = payload.get("mimeType", "")

        if mime == "text/plain":
            data = payload.get("body", {}).get("data", "")
            if data:
                body += base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

        elif mime == "application/pdf":
            has_pdf = True

        elif mime.startswith("image/"):
            has_image = True

        elif mime.startswith("multipart/"):
            for part in payload.get("parts", []):
                sub_body, sub_pdf, sub_image = self._extract_body_and_attachments(part)
                body += sub_body
                if sub_pdf:
                    has_pdf = True
                if sub_image:
                    has_image = True

        # Fallback: non-multipart with body data but unknown mime
        elif "data" in payload.get("body", {}):
            try:
                body += base64.urlsafe_b64decode(
                    payload["body"]["data"]
                ).decode("utf-8", errors="replace")
            except Exception:
                pass

        return body, has_pdf, has_image

    # ─── Core Fetch ─────────────────────────────────────────────────────────

    def fetch_recent_school_emails(self, skip_processed: bool = True) -> List[Dict]:
        """
        Fetch recent school emails from Gmail.
        Skips already-processed message IDs by default.
        """
        from core import gmail

        # Build query from config — no hardcoded school domains
        try:
            from core.config_loader import config as _cfg
            query = _cfg.school_email_query or ""
        except Exception:
            query = ""
        if not query:
            # A missing query is "cannot read mail", not "no mail". Left
            # undifferentiated it returned [] forever and the runner logged a
            # quiet day every time — the same shape as the auth failure this
            # class went to trouble to separate out, and the same family as
            # the `none`-bucket and has:attachment silent drops.
            self.auth_status = "no_query"
            self.auth_detail = "school_email_query is empty or unreadable in config"
            return []

        try:
            message_ids = gmail.search(query, max_results=20)

            # A search that came back is proof the token works. Clearing the
            # notified flag here is what re-arms the one-shot alert, so a token
            # that breaks, gets fixed, and breaks again is reported the second
            # time too. Without it the first failure would be the only one this
            # household ever hears about.
            self._set_auth_error_notified(False)

            email_data = []
            for msg_id in message_ids:
                # FIX: Skip already-processed emails properly (was a comment placeholder)
                if skip_processed and msg_id in self.processed_ids:
                    continue

                txt = gmail.get_message(msg_id)

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
                body, has_pdf, has_image = self._extract_body_and_attachments(txt['payload'])

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
                    "has_inline_image": has_image,
                    "fetched_at": datetime.now().isoformat(),
                    # Raw Gmail payload kept for attachment download in calendar sync
                    "_payload": txt['payload'],
                })

                # Do NOT mark processed here — this email hasn't been acted on
                # yet, only fetched. Marking processed happens in
                # mark_email_synced(), once the agent has actually evaluated
                # it. Otherwise an agent that bails early (crash, hallucinated
                # tool call, silent no-op) permanently loses the email: it's
                # already "processed" even though nothing happened.

            return email_data

        except Exception as e:
            # A fetch that fails must not read as "no mail today". Returning []
            # with no status was how a broken token looked identical to a quiet
            # day — the same silent-drop family as the `none` bucket and the
            # has:attachment filter. The caller keys on auth_status.
            print(f"Error fetching Gmail: {e}", file=sys.stderr)
            self.auth_status = "auth_failed"
            self.auth_detail = str(e)[:300]
            # One shot only: a revoked token would otherwise alert the family
            # four times a day until someone noticed.
            if not self._is_auth_error_notified():
                self._set_auth_error_notified(True)
                self.auth_message = self.AUTH_HELP
            return []

    @staticmethod
    def _defang(text: str) -> str:
        """Neutralize WhatsApp markup in text an outsider wrote.

        Anyone can email the household, so `subject` and `body` are
        attacker-controlled. A `*` or `_` in either breaks the surrounding
        formatting of a message that reads as the assistant speaking.
        """
        return re.sub(r"[*_~`]", "", text or "")

    def format_for_whatsapp(self, emails: List[Dict]) -> Optional[str]:
        """
        Format fetched school emails into a WhatsApp-ready summary string.
        Returns None if there are no emails to report.
        """
        if not emails:
            return None

        lines = ["📚 *School Updates*\n"]
        for email in emails:
            lines.append(f"📧 *{self._defang(email['subject'])}*")
            lines.append(f"From: {self._defang(email['sender'])}")
            if email.get("has_pdf_attachment"):
                lines.append("📎 PDF attachment detected")
            # Show a brief snippet of the body
            snippet = self._defang(email.get("body", ""))[:300].strip()
            if snippet:
                # Quoted, so the family can see where the school's words end
                # and the assistant's begin.
                ellipsis = "..." if len(email.get("body", "")) > 300 else ""
                lines.append(f"> _{snippet}{ellipsis}_")
            lines.append("")  # blank line between emails

        return "\n".join(lines).strip()


if __name__ == "__main__":
    # Output school emails as JSON for the agent to process and deliver via OpenClaw.
    # Top-level guard so cron always sees a parseable status, even on crash.
    import json as _json
    import sys as _sys
    import traceback as _tb
    try:
        # The keyring-importability bail-out that stood here until 2026-09-07
        # is gone with the credentials it guarded. It emitted `env_broken` +
        # NO_REPLY when this interpreter could not read the Keychain, so a
        # cron python without `keyring` would not fire a misleading
        # credentials-missing DM. gog holds the token now and this interpreter
        # reads no secrets at all, so there is nothing to bail out of; a gog
        # failure surfaces as auth_failed from the fetch instead.
        from core.config_loader import SKILL_DIR
        monitor = SchoolEmailMonitor(SKILL_DIR)
        emails = monitor.fetch_recent_school_emails()
        if emails:
            summary = monitor.format_for_whatsapp(emails)
            print(_json.dumps({"status": "emails_found", "count": len(emails), "summary": summary}, indent=2))
        elif monitor.auth_status:
            # No service. The getter recorded why; this entry point decides what
            # reaches a human. Only the first auth failure carries a message —
            # after that auth_message is None and we stay silent (principle 6).
            payload = {"status": monitor.auth_status, "error": monitor.auth_detail}
            if monitor.auth_status == "env_broken":
                payload["interpreter"] = _sys.executable
            if monitor.auth_message:
                payload["summary"] = monitor.auth_message
            print(_json.dumps(payload, indent=2))
            if not monitor.auth_message:
                print("NO_REPLY")
        else:
            print(_json.dumps({"status": "no_new_emails"}))
    except Exception as _e:
        print(_json.dumps({
            "status": "crashed",
            "error": str(_e),
            "traceback": _tb.format_exc(),
        }, indent=2))
        _sys.exit(1)