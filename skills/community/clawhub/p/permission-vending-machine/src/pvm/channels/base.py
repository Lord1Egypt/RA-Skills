"""Abstract base class for PVM notification channels."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class NotificationResult:
    """Result of a notification send attempt."""

    channel: str
    success: bool
    message: str
    response_data: Optional[dict] = None
    error: Optional[str] = None


class NotificationChannel(ABC):
    """Abstract notification channel."""

    name: str = "abstract"

    @abstractmethod
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
        """
        Send an approval request notification.

        Should return a NotificationResult regardless of success/failure.
        """

    def _format_message(
        self,
        message: str,
        *,
        agent_id: Optional[str] = None,
        scope: Optional[str] = None,
        reason: Optional[str] = None,
        ttl_minutes: Optional[int] = None,
        approval_token: Optional[str] = None,
    ) -> str:
        """Format the approval request message."""
        lines = [
            f"🤖 Agent Permission Request",
            f"",
            f"Agent: {agent_id or 'unknown'}",
            f"Scope: {scope or 'N/A'}",
            f"Reason: {reason or 'N/A'}",
            f"Duration: {ttl_minutes}min" if ttl_minutes else "",
            f"",
            f"{message}",
            f"",
            f"Approval token: {approval_token or 'N/A'}",
            f"",
            f"Reply APPROVE or DENY to this message.",
        ]
        return "\n".join(line for line in lines if line)
