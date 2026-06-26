"""
Approval daemon — polls all channels and activates grants when Tyler approves.

Run with: pvm approve-daemon [--config config.yaml] [--port 8080]

This is the approval-side counterpart to `pvm request --block`.
While `pvm request` sends notifications and waits, this daemon watches
email, Sendblue, and HTTP callbacks so Tyler can approve from anywhere.

It should run as a persistent service (background process, systemd, launchd).
On Mac: `python -m pvm.approval.daemon` via launchd or directly.
"""

from __future__ import annotations

import argparse
import logging
import os
import signal
import sys
import threading
from pathlib import Path
from typing import Optional

import yaml

from ..vault import Vault

logger = logging.getLogger(__name__)


class ApprovalDaemon:
    """
    Unified approval detector for PVM.

    Starts:
    - Flask HTTP server for Discord/web approvals
    - Email IMAP poller (thread)
    - Sendblue inbound poller (thread)

    When any channel detects an approval, creates the grant in the vault.
    The agent's `pvm request --block` will then unblock.
    """

    def __init__(
        self,
        vault: Vault,
        config_path: str,
        http_port: int = 7823,
        approver_name: str = "Tyler",
    ):
        self.vault = vault
        self.config_path = config_path
        self.http_port = http_port
        self.approver_name = approver_name
        self._shutdown = threading.Event()
        self._threads: list[threading.Thread] = []
        self._sendblue_channel = None  # set after _load_config
        self._approver_numbers: list[str] = []  # set after _load_config

    def start(self) -> None:
        """Start all poller threads and the HTTP server."""
        self._load_config()

        # Email poller
        if self._email_enabled:
            t = threading.Thread(target=self._run_email_poller, daemon=True)
            t.start()
            self._threads.append(t)
            logger.info("Email poller started (interval=%ds)", self._email_interval)

        # Sendblue poller
        if self._sendblue_enabled:
            t = threading.Thread(target=self._run_sendblue_poller, daemon=True)
            t.start()
            self._threads.append(t)
            logger.info("Sendblue poller started (interval=%ds)", self._sendblue_interval)

        # HTTP server (Flask) — blocks the main thread
        self._run_http_server()

    def _load_config(self) -> None:
        """Load channel config to determine which pollers to start."""
        path = Path(self.config_path)
        if not path.exists():
            logger.warning("Config not found at %s — no pollers will start", self.config_path)
            self._email_enabled = False
            self._sendblue_enabled = False
            self._email_cfg = {}
            self._sendblue_cfg = {}
            return

        cfg = yaml.safe_load(path.read_text())
        channels = cfg.get("channels", {})

        ec = channels.get("email", {})
        self._email_enabled = ec.get("enabled", False)
        self._email_cfg = ec
        self._email_interval = ec.get("poll_interval_seconds", 30)

        sc = channels.get("sendblue", {})
        self._sendblue_enabled = sc.get("enabled", False)
        self._sendblue_cfg = sc
        self._sendblue_interval = sc.get("poll_interval_seconds", 15)
        self._approver_numbers = sc.get("approver_numbers", [])

        # Initialize Sendblue sender for outbound confirmation replies
        if sc.get("enabled"):
            from ..channels.sendblue import SendblueChannel
            self._sendblue_channel = SendblueChannel(
                api_key=sc.get("api_key", ""),
                from_number=sc.get("from_number", ""),
                approver_numbers=[],
            )

        self._http_approver_name = cfg.get("approver", {}).get("name", "Tyler")

    def _run_email_poller(self) -> None:
        from .email_poller import EmailPoller
        # Use dedicated imap_host if set, otherwise derive from smtp_host
        imap_host = self._email_cfg.get("imap_host", "imap.mail.me.com")
        if "imap" not in imap_host:
            imap_host = imap_host.replace("smtp", "imap")
        poller = EmailPoller(
            imap_host=imap_host,
            imap_port=int(self._email_cfg.get("imap_port", 993)),
            username=self._email_cfg["username"],
            password=self._email_cfg["password"],
        )
        poller.poll(
            on_approval=self._handle_approval,
            interval_seconds=self._email_interval,
        )

    def _run_sendblue_poller(self) -> None:
        from .sendblue_poller import SendbluePoller
        poller = SendbluePoller()
        poller.poll(
            on_approval=self._handle_approval,
            interval_seconds=self._sendblue_interval,
        )

    def _run_http_server(self) -> None:
        from .server import run_server
        logger.info("Starting HTTP approval server on :%d", self.http_port)
        run_server(
            on_approve=self._handle_http_approve,
            on_deny=self._handle_http_deny,
            host="0.0.0.0",
            port=self.http_port,
            approver_name=self._http_approver_name,
        )

    def _handle_approval(
        self,
        approval_token: str,
        decision: str,
        from_number: str,
    ) -> None:
        """Called by any channel when an approval or denial is detected."""
        logger.info(
            "Approval decision: token=%s decision=%s from=%s",
            approval_token,
            decision,
            from_number,
        )
        # from_number may be a name like "Tyler" (from HTTP) or a phone number (from Sendblue)
        # Try to normalize: if it looks like a phone number, use it for SMS reply
        is_phone = from_number.startswith("+") or from_number.startswith("(") or from_number[0].isdigit()
        reply_to = from_number if is_phone else ""

        if decision.upper() == "APPROVE":
            self._handle_http_approve(approval_token, from_number, reply_to)
        else:
            self._handle_http_deny(approval_token, from_number, reply_to)

    def _handle_http_approve(self, token: str, approver: str, reply_to: str = "") -> None:
        """Create a grant from an approved request."""
        # Look up the request — by token if provided, otherwise most recent pending
        req = None
        if token:
            req = self.vault.get_request_by_token(token)
            if req:
                logger.info("Found pending request by token=%s: agent=%s scope=%s",
                            token, req["agent_id"], req["scope"])

        if not req:
            # No token provided or not found — find most recent pending request
            req = self.vault.get_most_recent_pending_request()
            if req:
                logger.info(
                    "No token / not found — approving most recent pending: agent=%s scope=%s token=%s",
                    req["agent_id"], req["scope"], req["approval_token"],
                )

        if not req:
            logger.warning("No pending request found to approve")
            return

        try:
            grant = self.vault.create_grant(
                agent_id=req["agent_id"],
                scope=req["scope"],
                scope_type=req["scope_type"],
                reason=f"Approved via PVM by {approver}",
                ttl_minutes=req["ttl_minutes"],
                approved_by=approver,
                approval_token=req["approval_token"],
            )
            logger.info(
                "Grant %s created: agent=%s scope=%s (approved by %s)",
                grant.grant_id, req["agent_id"], req["scope"], approver,
            )
            # Send confirmation SMS back to approver via Sendblue CLI
            if reply_to:
                import subprocess
                msg = f"✅ Approved! Scope: {req['scope']} | Duration: {req['ttl_minutes']}min | Agent: {req['agent_id']}"
                try:
                    result = subprocess.run(
                        ["sendblue", "send", reply_to, msg],
                        capture_output=True, text=True, timeout=30,
                    )
                    if result.returncode == 0:
                        logger.info("Confirmation SMS sent to %s", reply_to)
                    else:
                        logger.warning("Failed to send confirmation SMS: %s", result.stderr.strip())
                except Exception as exc:
                    logger.warning("Could not send confirmation SMS: %s", exc)
        except Exception as exc:
            logger.exception("Failed to create grant")


    def _handle_http_deny(self, token: str, approver: str, reply_to: str = "") -> None:
        """Log a denial."""
        from ..models import AuditEntryType, Decision
        entries = self.vault.get_audit_log(limit=1000)
        matching = [e for e in entries if token in (e.details or "")]
        latest = matching[0] if matching else None
        scope = latest.scope if latest else "(unknown)"

        self.vault.log_audit(
            entry_type=AuditEntryType.DENIAL,
            agent_id=latest.agent_id if latest else None,
            scope=scope,
            decision=Decision.DENIED,
            details=f"Request denied by {approver} (token={token})",
        )
        logger.info("Request denied: token=%s by=%s", token, approver)

        # Send confirmation SMS back to approver
        if reply_to:
            import subprocess
            msg = f"❌ Denied. Scope: {scope}"
            try:
                result = subprocess.run(
                    ["sendblue", "send", reply_to, msg],
                    capture_output=True, text=True, timeout=30,
                )
                if result.returncode == 0:
                    logger.info("Denial confirmation SMS sent to %s", reply_to)
                else:
                    logger.warning("Failed to send denial SMS: %s", result.stderr.strip())
            except Exception as exc:
                logger.warning("Could not send denial SMS: %s", exc)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(prog="pvm approve-daemon")
    parser.add_argument("--config", default=os.environ.get("PVM_CONFIG", "./config.yaml"))
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--approver", default="Tyler")
    args = parser.parse_args()

    vault = Vault("./grants.db")
    daemon = ApprovalDaemon(
        vault=vault,
        config_path=args.config,
        http_port=args.port,
        approver_name=args.approver,
    )

    def shutdown(signum, frame):
        logger.info("Shutting down approval daemon...")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info("PVM Approval Daemon starting...")
    logger.info("Approve via: HTTP (:%d), email replies, Sendblue iMessage", args.port)
    daemon.start()
    return 0
