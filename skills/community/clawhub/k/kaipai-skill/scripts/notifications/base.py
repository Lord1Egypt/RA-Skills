"""Base notification interface for Kaipai AI skill."""

from abc import ABC, abstractmethod
from typing import Dict, Any


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
    ) -> Dict[str, Any]:
        """
        Send video notification.

        :param video_path: Video file path
        :param recipient: Recipient ID
        :param video_url: Optional video URL for download link
        :param cover_url: Optional cover image URL
        :param duration: Video duration in milliseconds
        :param caption: Optional caption
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
            raise ValueError(f"Unknown notifier: {name}")
        return notifier
