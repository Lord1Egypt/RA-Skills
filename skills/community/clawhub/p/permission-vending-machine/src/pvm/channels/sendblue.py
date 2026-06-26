"""Sendblue (iMessage/SMS) notification channel via CLI.

Uses the sendblue CLI (installed at /opt/homebrew/bin/sendblue) rather than the
REST API, since CLI auth is already configured on the system.
"""

import logging
import subprocess
import tempfile
from typing import Optional

from .base import NotificationChannel, NotificationResult

logger = logging.getLogger(__name__)


class SendblueChannel(NotificationChannel):
    name = "sendblue"

    def __init__(
        self,
        api_key: str,  # kept for compatibility; CLI uses its own credentials
        from_number: str,
        approver_numbers: list[str],
    ):
        self.from_number = from_number
        self.approver_numbers = approver_numbers

    def send(
        self,
        message: str,
        approval_token: str,
        *,
        agent_id: Optional[str] = None,
        scope: Optional[str] = None,
        reason: Optional[str] = None,
        ttl_minutes: Optional[int] = None,
        approver_name: Optional[str] = None,
    ) -> NotificationResult:
        full_message = self._format_message(
            message,
            agent_id=agent_id,
            scope=scope,
            reason=reason,
            ttl_minutes=ttl_minutes,
            approval_token=approval_token,
        )

        errors = []
        for number in self.approver_numbers:
            try:
                result = subprocess.run(
                    ["sendblue", "send", number, full_message],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode != 0:
                    errors.append(f"{number}: {result.stderr.strip()}")
                else:
                    logger.info("Sendblue sent to %s: %s", number, result.stdout.strip())
            except Exception as exc:
                errors.append(f"{number}: {exc}")

        if errors:
            return NotificationResult(
                channel=self.name,
                success=False,
                message=full_message,
                error="; ".join(errors),
            )
        return NotificationResult(
            channel=self.name,
            success=True,
            message=full_message,
        )
