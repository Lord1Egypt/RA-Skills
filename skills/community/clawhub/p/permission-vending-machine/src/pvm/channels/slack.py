"""Slack webhook notification channel."""

import logging
from typing import Optional

import requests

from .base import NotificationChannel, NotificationResult

logger = logging.getLogger(__name__)


class SlackChannel(NotificationChannel):
    name = "slack"

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

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
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🤖 Agent Permission Request",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Agent:*\n{agent_id or 'unknown'}"},
                    {"type": "mrkdwn", "text": f"*Duration:*\n{ttl_minutes}min" if ttl_minutes else "*Duration:*\nN/A"},
                ],
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Scope:*\n```{scope or 'N/A'}```"},
                    {"type": "mrkdwn", "text": f"*Reason:*\n{reason or 'N/A'}"},
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": message or "_No additional message_"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Approval Token:*\n`{approval_token}`",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "✅ Approve"},
                        "action_id": f"approve_{approval_token}",
                        "style": "primary",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "❌ Deny"},
                        "action_id": f"deny_{approval_token}",
                        "style": "danger",
                    },
                ],
            },
        ]

        body = {"blocks": blocks}

        try:
            resp = requests.post(self.webhook_url, json=body, timeout=15)
            if resp.status_code == 200:
                return NotificationResult(
                    channel=self.name,
                    success=True,
                    message=message,
                )
            return NotificationResult(
                channel=self.name,
                success=False,
                message=message,
                error=f"HTTP {resp.status_code}: {resp.text[:200]}",
            )
        except Exception as exc:
            logger.exception("Slack send failed")
            return NotificationResult(
                channel=self.name,
                success=False,
                message=message,
                error=str(exc),
            )
