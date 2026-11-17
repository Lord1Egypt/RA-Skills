"""Shared contracts for optional notification providers."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class MissingCredentialsError(ValueError):
    """Carry the legacy sender JSON without making providers print or terminate."""

    def __init__(self, message: str, hint: str):
        super().__init__(message)
        self.payload = {"error": message, "hint": hint}


def validate_duration_ms(duration, duration_ms):
    """Validate only the new explicit unit; preserve legacy duration values unchanged."""
    if duration_ms is None:
        return
    if duration not in (None, 0):
        raise ValueError('duration 与 duration_ms 不能同时提供')
    if isinstance(duration_ms, bool) or not isinstance(duration_ms, int) or duration_ms < 0:
        raise ValueError('duration_ms 必须为非负整数')


class NotificationChannel(ABC):
    """Notification channel interface."""

    @abstractmethod
    def send_image(
        self, image_source: str, recipient: str, caption: str = ""
    ) -> Dict[str, Any]:
        """
        Send image notification.

        :param image_source: Image file path or URL
        :param recipient: Recipient ID (open_id, chat_id, etc.)
        :param caption: Optional caption
        :return: Send result
        """
        pass

    @abstractmethod
    def send_video(
        self,
        video_path: str,
        recipient: str,
        video_url: str = "",
        cover_url: str = "",
        duration: int = 0,
        caption: str = "",
        *,
        duration_ms: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Send video notification.

        :param video_path: Video file path
        :param recipient: Recipient ID
        :param video_url: Optional video URL for download link
        :param cover_url: Optional cover image URL
        :param duration: Legacy channel units: milliseconds for Feishu, seconds for Telegram
        :param caption: Optional caption
        :param duration_ms: Explicit milliseconds for either channel; conflicts with nonzero duration
        :return: Send result
        """
        pass


class NotifierFactory:
    """Factory for creating notifiers."""

    _notifiers: Dict[str, NotificationChannel] = {}

    @classmethod
    def register(cls, name: str, notifier: NotificationChannel) -> None:
        """Register a notifier."""
        cls._notifiers[name.lower()] = notifier

    @classmethod
    def get(cls, name: str) -> NotificationChannel:
        """Get a notifier by name."""
        notifier = cls._notifiers.get(name.lower())
        if not notifier:
            raise ValueError(f'未知通知渠道：{name}')
        return notifier
