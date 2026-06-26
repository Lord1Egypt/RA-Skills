"""Multicast notifier — sends approval requests to all configured channels."""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .channels import (
    DiscordChannel,
    EmailChannel,
    NotificationChannel,
    SendblueChannel,
    SlackChannel,
    TelegramChannel,
)
from .channels.base import NotificationResult

logger = logging.getLogger(__name__)

# Pattern for ${VAR} env var substitution
_ENV_PATTERN = re.compile(r"\$\{([^}]+)\}")


def _subenv(value: Any) -> Any:
    """Recursively substitute ${VAR} in strings with os.environ."""
    if isinstance(value, str):
        return _ENV_PATTERN.sub(lambda m: os.environ.get(m.group(1), ""), value)
    if isinstance(value, dict):
        return {k: _subenv(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_subenv(item) for item in value]
    return value


class Notifier:
    """
    Loads channel config and multicasts notifications to all enabled channels.

    Usage::

        notifier = Notifier("config.yaml")
        results = notifier.notify_approvers(
            message="Please approve deletion of /tmp/build",
            approval_token="tok_abc123",
            agent_id="coder",
            scope="/tmp/build",
            reason="removing stale temp files",
            ttl_minutes=5,
        )
        for ch, result in results.items():
            print(f"{ch}: {result.success}")
    """

    def __init__(self, config_path: str = "./config.yaml"):
        self.config = self._load_config(config_path)
        self.channels: Dict[str, NotificationChannel] = {}
        self._register_channels()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        raw = yaml.safe_load(path.read_text())
        return _subenv(raw)

    def _register_channels(self) -> None:
        cfg = self.config.get("channels", {})
        vault_cfg = self.config.get("vault", {})

        # Sendblue
        sc = cfg.get("sendblue", {})
        if sc.get("enabled"):
            self.channels["sendblue"] = SendblueChannel(
                api_key=sc["api_key"],
                from_number=sc["from_number"],
                approver_numbers=sc.get("approver_numbers", []),
            )
            logger.info("Registered Sendblue channel")

        # Email
        ec = cfg.get("email", {})
        if ec.get("enabled"):
            self.channels["email"] = EmailChannel(
                smtp_host=ec["smtp_host"],
                smtp_port=ec["smtp_port"],
                username=ec["username"],
                password=ec["password"],
                from_addr=ec["from_addr"],
                approver_emails=ec.get("approver_emails", []),
            )
            logger.info("Registered Email channel")

        # Discord
        dc = cfg.get("discord", {})
        if dc.get("enabled"):
            self.channels["discord"] = DiscordChannel(
                webhook_url=dc["webhook_url"],
                http_approval_base=dc.get("http_approval_base", "http://localhost:8080"),
            )
            logger.info("Registered Discord channel")

        # Telegram
        tc = cfg.get("telegram", {})
        if tc.get("enabled"):
            self.channels["telegram"] = TelegramChannel(
                bot_token=tc["bot_token"],
                approver_chat_ids=tc.get("approver_chat_ids", []),
            )
            logger.info("Registered Telegram channel")

        # Slack
        sl = cfg.get("slack", {})
        if sl.get("enabled"):
            self.channels["slack"] = SlackChannel(
                webhook_url=sl["webhook_url"],
            )
            logger.info("Registered Slack channel")

    def notify_approvers(
        self,
        message: str,
        approval_token: str,
        *,
        agent_id: Optional[str] = None,
        scope: Optional[str] = None,
        reason: Optional[str] = None,
        ttl_minutes: Optional[int] = None,
        approver_name: Optional[str] = None,
    ) -> Dict[str, NotificationResult]:
        """
        Send approval request to all enabled channels.

        Returns a dict of channel_name -> NotificationResult.
        Failures on individual channels do NOT prevent others from being tried.
        """
        results: Dict[str, NotificationResult] = {}
        if not self.channels:
            logger.warning("No notification channels enabled")

        for name, channel in self.channels.items():
            try:
                result = channel.send(
                    message=message,
                    approval_token=approval_token,
                    agent_id=agent_id,
                    scope=scope,
                    reason=reason,
                    ttl_minutes=ttl_minutes,
                    approver_name=approver_name,
                )
                results[name] = result
                if result.success:
                    logger.info("Notification sent via %s", name)
                else:
                    logger.warning("Notification failed via %s: %s", name, result.error)
            except Exception as exc:
                logger.exception("Unexpected error on channel %s", name)
                results[name] = NotificationResult(
                    channel=name,
                    success=False,
                    message=message,
                    error=str(exc),
                )

        return results

    @property
    def enabled_channels(self) -> List[str]:
        return list(self.channels.keys())

    def default_ttl_minutes(self) -> int:
        return self.config.get("vault", {}).get("default_ttl_minutes", 30)

    def max_ttl_minutes(self) -> int:
        return self.config.get("vault", {}).get("max_ttl_minutes", 480)
