"""Approval polling — poll for approval responses from a backing store."""

from __future__ import annotations

import logging
import time
from typing import Callable, Optional

from ..models import AuditEntryType, Decision, PermissionRequest
from ..vault import Vault

logger = logging.getLogger(__name__)


class ApprovalPoller:
    """
    Poll for approval decisions within a timeout window.

    Usage::

        vault = Vault()
        poller = ApprovalPoller(vault)

        def on_approve(req: PermissionRequest):
            vault.create_grant(
                agent_id=req.agent_id,
                scope=req.scope,
                scope_type=req.scope_type,
                reason=req.reason,
                ttl_minutes=req.ttl_minutes,
            )

        result = poller.wait_for_decision(
            request=req,
            timeout_seconds=300,
            poll_interval=5,
            on_approve=on_approve,
        )
    """

    def __init__(self, vault: Vault):
        self.vault = vault

    def wait_for_decision(
        self,
        request: PermissionRequest,
        timeout_seconds: int = 300,
        poll_interval: int = 5,
        on_approve: Optional[Callable[[PermissionRequest], None]] = None,
        on_deny: Optional[Callable[[PermissionRequest], None]] = None,
        on_expire: Optional[Callable[[PermissionRequest], None]] = None,
    ) -> Optional[PermissionRequest]:
        """
        Poll vault until request is approved, denied, or timeout reached.

        Returns the updated request, or None on timeout.
        """
        deadline = time.time() + timeout_seconds
        logger.info(
            "Polling for decision on request %s (token=%s, timeout=%ds)",
            request.request_id,
            request.approval_token,
            timeout_seconds,
        )

        while time.time() < deadline:
            status = self._poll_once(request)
            if status == "approved":
                request.status = "approved"
                if on_approve:
                    on_approve(request)
                return request
            elif status == "denied":
                request.status = "denied"
                if on_deny:
                    on_deny(request)
                self.vault.log_audit(
                    entry_type=AuditEntryType.DENIAL,
                    agent_id=request.agent_id,
                    scope=request.scope,
                    decision=Decision.DENIED,
                    details=f"Request {request.request_id} denied",
                )
                return request
            # still pending
            time.sleep(poll_interval)

        # timeout
        request.status = "expired"
        logger.warning("Request %s timed out after %ds", request.request_id, timeout_seconds)
        if on_expire:
            on_expire(request)
        self.vault.log_audit(
            entry_type=AuditEntryType.REVOCATION,
            agent_id=request.agent_id,
            scope=request.scope,
            decision=Decision.EXPIRED,
            details=f"Request {request.request_id} expired without decision",
        )
        return None

    def _poll_once(self, request: PermissionRequest) -> str:
        """
        Single poll iteration. Override to check custom backing store.
        Default implementation checks vault for a matching active grant.
        """
        grants = self.vault.get_active_grants(agent_id=request.agent_id)
        for grant in grants:
            if grant.scope == request.scope:
                return "approved"
        return "pending"
