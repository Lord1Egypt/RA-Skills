"""Discord webhook notification channel."""

import logging
from typing import Optional

import requests

from .base import NotificationChannel, NotificationResult

logger = logging.getLogger(__name__)

DISCORD_MAX_LENGTH = 4096


class DiscordChannel(NotificationChannel):
    name = "discord"

    def __init__(self, webhook_url: str, http_approval_base: str = "http://localhost:8080"):
        self.webhook_url = webhook_url
        self.http_approval_base = http_approval_base

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
        approve_url = f"{self.http_approval_base}/approve/{approval_token}"
        deny_url = f"{self.http_approval_base}/deny/{approval_token}"

        embed = {
            "title": "🤖 Agent Permission Request",
            "color": 0xFF6B00,  # Tyler orange
            "fields": [
                {"name": "Agent", "value": agent_id or "unknown", "inline": True},
                {"name": "Scope", "value": scope or "N/A", "inline": False},
                {"name": "Reason", "value": reason or "N/A", "inline": False},
                {
                    "name": "Duration",
                    "value": f"{ttl_minutes} min" if ttl_minutes else "N/A",
                    "inline": True,
                },
                {
                    "name": "Approval Token",
                    "value": f"```\n{approval_token}\n```",
                    "inline": False,
                },
                {
                    "name": "Approve",
                    "value": f"[Click to approve]({approve_url})",
                    "inline": False,
                },
                {
                    "name": "Deny",
                    "value": f"[Click to deny]({deny_url})",
                    "inline": False,
                },
            ],
            "description": message or "(no additional message)",
            "footer": {
                "text": "Or reply via iMessage/SMS with: APPROVE token\nOr reply to approval email"
            },
        }

        body = {
            "username": "PVM",
            "avatar_url": "https://i.imgur.com/axios.png",
            "embeds": [embed],
        }

        try:
            resp = requests.post(self.webhook_url, json=body, timeout=15)
            if resp.status_code in (200, 204):
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
            logger.exception("Discord send failed")
            return NotificationResult(
                channel=self.name,
                success=False,
                message=message,
                error=str(exc),
            )
