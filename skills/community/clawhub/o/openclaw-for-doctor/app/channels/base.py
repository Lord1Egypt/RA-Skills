from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Any

from app.channels.formatter import format_task_result_message
from app.config import get_settings
from app.core.models import ChannelType, DeliveryReceipt, TaskResult


class ChannelAdapter(ABC):
    channel: ChannelType

    @abstractmethod
    def send_result(self, result: TaskResult) -> DeliveryReceipt:
        raise NotImplementedError

    def build_payload(self, result: TaskResult) -> dict[str, Any]:
        return {
            "channel": self.channel.value,
            "task_id": result.task_id,
            "message": format_task_result_message(result),
            "summary": result.summary,
        }


class WebhookChannelAdapter(ChannelAdapter):
    """Baseline adapter.

    If webhook env is missing, delivery is marked pending instead of failing hard.
    """

    webhook_env_key: str

    def send_result(self, result: TaskResult) -> DeliveryReceipt:
        settings = get_settings()
        webhook = os.getenv(self.webhook_env_key, "").strip()
        if not webhook:
            return DeliveryReceipt(
                channel=self.channel,
                delivered=False,
                detail=(
                    f"{self.channel.value} adapter initialized but {self.webhook_env_key} "
                    "is not configured."
                ),
            )

        payload = self.build_payload(result)
        if not settings.enable_outbound_send:
            return DeliveryReceipt(
                channel=self.channel,
                delivered=True,
                detail=(
                    f"Prepared payload for {self.channel.value} "
                    "(outbound send disabled by OPENCLAW_DOCTOR_ENABLE_OUTBOUND_SEND)."
                ),
            )

        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            webhook,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=settings.webhook_timeout_seconds) as resp:
                status_code = resp.getcode()
            if 200 <= status_code < 300:
                return DeliveryReceipt(
                    channel=self.channel,
                    delivered=True,
                    detail=f"Webhook delivered with HTTP {status_code}.",
                )
            return DeliveryReceipt(
                channel=self.channel,
                delivered=False,
                detail=f"Webhook failed with HTTP {status_code}.",
            )
        except urllib.error.URLError as exc:
            return DeliveryReceipt(
                channel=self.channel,
                delivered=False,
                detail=f"Webhook delivery error: {exc.reason}",
            )
        except Exception as exc:
            return DeliveryReceipt(
                channel=self.channel,
                delivered=False,
                detail=f"Webhook delivery exception: {exc}",
            )


class StaticChannelAdapter(ChannelAdapter):
    """Adapter for local/dev channels that return data directly in API response."""

    def send_result(self, result: TaskResult) -> DeliveryReceipt:
        return DeliveryReceipt(
            channel=self.channel,
            delivered=True,
            detail="Result returned directly to caller.",
        )
