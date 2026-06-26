"""Approval polling module — polls channels for approval responses."""

from __future__ import annotations

import logging
import time
from typing import Callable, Optional

from ..models import AuditEntryType, Decision, PermissionRequest
from ..vault import Vault

logger = logging.getLogger(__name__)


class ApprovalPoller:
    """
    Poll an approval source until a decision is received or timeout expires.

    Usage::

        poller = ApprovalPoller(vault, config_path="config.yaml")

        def on_approve(request: PermissionRequest) -> None:
            vault.create_grant(...)

        grant = poller.wait_for_decision(
            request=req,
            timeout_seconds=300,
            poll_interval=5,
            on_approve=on_approve,
        )
    """

    def __init__(self, vault: Vault, config_path: str = "./config.yaml"):
        self.vault = vault
        self.config_path = config_path
        self._approvers: dict[str, Callable] = {}

    def register_approver(self, channel: str, callback: Callable) -> None:
        """Register a callback for a specific channel's approval responses."""
        self._approvers[channel] = callback

    def wait_for_decision(
        self,
        request: PermissionRequest,
        timeout_seconds: int = 300,
        poll_interval: int = 5,
        on_approve: Optional[Callable[[PermissionRequest], None]] = None,
        on_deny: Optional[Callable[[PermissionRequest], None]] = None,
    ) -> Optional[PermissionRequest]:
        """
        Poll until the request is approved or denied.

        Returns the updated PermissionRequest, or None on timeout.
        """
        deadline = time.time() + timeout_seconds
        logger.info(
            "Waiting for decision on request %s (token=%s, timeout=%ds)",
            request.request_id,
            request.approval_token,
            timeout_seconds,
        )

        while time.time() < deadline:
            # Check if a callback updated the request status
            updated = self._check_status(request)
            if updated:
                return updated

            # Also check vault for a matching grant (approve path)
            grants = self.vault.get_active_grants(agent_id=request.agent_id)
            for grant in grants:
                if grant.scope == request.scope:
                    request.status = "approved"
                    if on_approve:
                        on_approve(request)
                    self.vault.log_audit(
                        entry_type=AuditEntryType.APPROVAL,
                        agent_id=request.agent_id,
                        scope=request.scope,
                        decision=Decision.GRANTED,
                        details=f"Approved via polling for {request.request_id}",
                    )
                    return request

            time.sleep(poll_interval)

        logger.warning("Request %s timed out", request.request_id)
        request.status = "expired"
        if on_deny:
            on_deny(request)
        return None

    def _check_status(self, request: PermissionRequest) -> Optional[PermissionRequest]:
        """
        Check if status was updated by an external callback.
        Override or extend in subclasses for specific channels.
        """
        return None
