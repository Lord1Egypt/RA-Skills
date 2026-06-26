"""Notification modules for Kaipai AI skill."""

from scripts.notifications.base import NotificationChannel, NotifierFactory
from scripts.notifications.feishu import FeishuNotifier
from scripts.notifications.telegram import TelegramNotifier

__all__ = [
    "NotificationChannel",
    "NotifierFactory",
    "FeishuNotifier",
    "TelegramNotifier",
    "get_notifier",
]


def get_notifier(channel: str) -> NotificationChannel:
    """Get notifier for specified channel."""
    channel = channel.lower()
    if channel == "feishu":
        return FeishuNotifier()
    elif channel == "telegram":
        return TelegramNotifier()
    else:
        raise ValueError(f"Unknown notification channel: {channel}")
