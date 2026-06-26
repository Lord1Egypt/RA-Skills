"""IMAP email polling — detect approval/denial replies to PVM permission requests."""

from __future__ import annotations

import base64
import imaplib
import logging
import re
import time
from dataclasses import dataclass
from typing import Callable, Optional

logger = logging.getLogger(__name__)

# Pattern to extract approval token from email body
TOKEN_RE = re.compile(r"(?:approval\s+)?token:\s*([a-zA-Z0-9_-]+)", re.IGNORECASE)


@dataclass
class EmailApproval:
    approval_token: str
    decision: str  # "APPROVE" or "DENY"
    email_addr: str


class EmailPoller:
    """
    Poll an IMAP mailbox for approval replies to PVM permission emails.

    Looks for unread emails with subject containing "Agent Permission Request"
    and body containing APPROVE or DENY.

    Usage::

        def on_approval(token: str, decision: str, email_addr: str):
            if decision == "APPROVE":
                vault.create_grant(...)

        poller = EmailPoller(
            imap_host="imap.mail.me.com",
            imap_port=993,
            username="tyler.delano@icloud.com",
            password="app-password",
        )
        poller.poll(on_approval=on_approval, interval_seconds=30)
    """

    def __init__(
        self,
        imap_host: str,
        imap_port: int,
        username: str,
        password: str,
        folder: str = "INBOX",
    ):
        self.host = imap_host
        self.port = imap_port
        self.username = username
        self.password = password
        self.folder = folder
        self._processed: set[str] = set()  # email IDs already seen

    def poll(
        self,
        on_approval: Callable[[str, str, str], None],
        interval_seconds: int = 30,
    ) -> None:
        """
        Run the email polling loop indefinitely.

        `on_approval` is called with (approval_token, decision, email_addr).
        """
        while True:
            try:
                self._poll_once(on_approval)
            except Exception:
                logger.exception("Email poll error")
            time.sleep(interval_seconds)

    def _poll_once(
        self,
        on_approval: Callable[[str, str, str], None],
    ) -> list[EmailApproval]:
        """
        Check for new unread PVM emails. Returns list of approvals found.
        Marks processed emails as SEEN.
        """
        approvals = []
        try:
            conn = imaplib.IMAP4_SSL(self.host, self.port)
            conn.login(self.username, self.password)
            conn.select(self.folder)

            # Search for unread PVM permission request emails
            typ, data = conn.search(None, '(UNSEEN SUBJECT "Agent Permission Request")')
            if typ != "OK" or not data or not data[0]:
                return []

            email_ids = data[0].split()
            if not email_ids:
                return []

            logger.debug("Found %d unread PVM emails", len(email_ids))

            for eid in email_ids:
                eid_str = eid.decode()
                if eid_str in self._processed:
                    continue

                try:
                    approval = self._read_email(conn, eid_str)
                    if approval:
                        approvals.append(approval)
                        self._processed.add(eid_str)
                        # Mark as read so we don't re-process
                        conn.store(eid, "+FLAGS", "\\Seen")
                        logger.info(
                            "Email approval detected: token=%s decision=%s",
                            approval.approval_token,
                            approval.decision,
                        )
                        on_approval(approval.approval_token, approval.decision, approval.email_addr)
                except Exception:
                    logger.exception("Error reading email %s", eid_str)

            conn.logout()
        except Exception:
            logger.exception("IMAP connection error")
        return approvals

    def _read_email(self, conn, eid: str) -> Optional[EmailApproval]:
        """Parse a single email for approval decisions."""
        typ, msg_data = conn.fetch(eid, "(BODY[TEXT])")
        if typ != "OK":
            return None

        # msg_data is [(b'...', bytes), ...]
        raw = None
        for item in msg_data:
            if isinstance(item, tuple) and len(item) == 2:
                payload = item[1]
                if isinstance(payload, bytes):
                    raw = payload
                    break

        if not raw:
            return None

        # Decode the MIME message
        from email.message import Message
        msg = Message()
        # The raw bytes might need to be parsed differently
        # Try parsing as a full RFC822 message
        try:
            from email import message_from_bytes
            msg = message_from_bytes(raw)
        except Exception:
            return None

        # Extract body
        body = self._extract_body(msg).upper()

        # Check for APPROVE or DENY
        decision = None
        if "APPROVE" in body and "DENY" not in body:
            decision = "APPROVE"
        elif "DENY" in body:
            decision = "DENY"

        if not decision:
            return None

        # Extract sender
        from_addr = msg.get("From", "")
        addr_match = re.search(r"<(.+?)>|^(.+?)$", from_addr)
        email_addr = addr_match.group(1) or addr_match.group(2) if addr_match else from_addr

        # Extract token from body (optional — caller may resolve to most recent pending)
        token_match = TOKEN_RE.search(body)
        approval_token = token_match.group(1) if token_match else ""
        return EmailApproval(
            approval_token=approval_token,
            decision=decision,
            email_addr=email_addr,
        )

    def _extract_body(self, msg) -> str:
        """Get plaintext body from email message."""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == "text/plain":
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        charset = part.get_content_charset() or "utf-8"
                        return payload.decode(charset, errors="replace")
                    return str(payload)
        else:
            payload = msg.get_payload(decode=True)
            if isinstance(payload, bytes):
                charset = msg.get_content_charset() or "utf-8"
                return payload.decode(charset, errors="replace")
            return str(payload)
        return ""
