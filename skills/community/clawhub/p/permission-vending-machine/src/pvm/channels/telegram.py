"""Telegram bot notification channel."""

import logging
from typing import Optional

import requests

from .base import NotificationChannel, NotificationResult

logger = logging.getLogger(__name__)

TG_API = "https://api.telegram.org"


class TelegramChannel(NotificationChannel):
    name = "telegram"

    def __init__(self, bot_token: str, approver_chat_ids: list[str]):
        self.bot_token = bot_token
        self.approver_chat_ids = approver_chat_ids
        self._base = f"{TG_API}/bot{bot_token}"

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
        success = False

        for chat_id in self.approver_chat_ids:
            try:
                resp = requests.post(
                    f"{self._base}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": full_message,
                        "parse_mode": "Markdown",
                        "reply_markup": {
                            "inline_keyboard": [
                                [
                                    {"text": "✅ Approve", "callback_data": f"approve:{approval_token}"},
                                    {"text": "❌ Deny", "callback_data": f"deny:{approval_token}"},
                                ]
                            ]
                        },
                    },
                    timeout=15,
                )
                data = resp.json()
                if resp.status_code == 200 and data.get("ok"):
                    success = True
                else:
                    errors.append(f"{chat_id}: {data}")
            except Exception as exc:
                errors.append(f"{chat_id}: {exc}")

        if errors and not success:
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
