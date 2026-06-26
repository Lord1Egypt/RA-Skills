"""Approval callback handler — process incoming approval/denial webhooks."""

from __future__ import annotations

import hashlib
import hmac
import logging
from typing import Callable, Dict, Optional

from ..models import AuditEntryType, Decision, PermissionRequest
from ..vault import Vault

logger = logging.getLogger(__name__)


class CallbackHandler:
    """
    Handle incoming webhook callbacks for approval/denial.

    Usage::

        handler = CallbackHandler(vault)

        # Flask/FastAPI route:
        @app.route("/approve", methods=["POST"])
        def approve():
            ok = handler.handle_approval(request.json())
            return "OK" if ok else "FAIL", 200 if ok else 400
    """

    def __init__(self, vault: Vault):
        self.vault = vault
        self._callbacks: Dict[str, Callable] = {}

    def handle_approval(
        self,
        payload: dict,
        *,
        agent_id: Optional[str] = None,
        approved_by: Optional[str] = None,
    ) -> bool:
        """
        Process an approval callback payload.

        Expected payload shape::

            {
                "approval_token": "tok_abc123",
                "agent_id": "coder",
                "scope": "/tmp/build",
                "scope_type": "path",
                "reason": "cleanup",
                "ttl_minutes": 10,
            }

        Creates a grant in the vault and logs the decision.
        Returns True on success.
        """
        token = payload.get("approval_token")
        if not token:
            logger.warning("Approval callback missing approval_token")
            return False

        try:
            grant = self.vault.create_grant(
                agent_id=payload.get("agent_id", agent_id or "unknown"),
                scope=payload.get("scope", ""),
                scope_type=payload.get("scope_type", "path"),
                reason=payload.get("reason", "approved via callback"),
                ttl_minutes=payload.get("ttl_minutes", 30),
                approved_by=approved_by,
            )
            logger.info(
                "Grant %s created via approval callback (token=%s)",
                grant.grant_id,
                token,
            )
            return True
        except Exception:
            logger.exception("Failed to process approval callback")
            return False

    def handle_denial(
        self,
        payload: dict,
        *,
        denied_by: Optional[str] = None,
    ) -> bool:
        """
        Process a denial callback payload.

        Logs the denial in the audit trail but does not create a grant.
        Returns True on success.
        """
        token = payload.get("approval_token")
        if not token:
            logger.warning("Denial callback missing approval_token")
            return False

        self.vault.log_audit(
            entry_type=AuditEntryType.DENIAL,
            agent_id=payload.get("agent_id"),
            scope=payload.get("scope"),
            decision=Decision.DENIED,
            details=f"Request denied via callback (token={token})",
            grant_id=None,
        )
        logger.info("Denial recorded for token=%s", token)
        return True

    def verify_discord_interaction(
        self,
        payload: bytes,
        signature: str,
        timestamp: str,
        client_secret: str,
    ) -> bool:
        """Verify Discord interaction signature (interactions endpoint URL)."""
        if not signature or not timestamp:
            return False
        msg = timestamp.encode() + payload
        expected = hmac.new(
            client_secret.encode(),
            msg,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(f"sha256={expected}", signature)

    def register_callback(self, token: str, cb: Callable) -> None:
        """Register a one-shot callback for a specific approval token."""
        self._callbacks[token] = cb

    def trigger_callback(self, token: str) -> None:
        """Trigger and remove a registered callback."""
        cb = self._callbacks.pop(token, None)
        if cb:
            cb()
