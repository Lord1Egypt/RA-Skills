"""Optional delivery providers; importing this package does not load either one."""

from .base import NotificationChannel, NotifierFactory
from delivery import bundled_channels

__all__ = [
    "NotificationChannel",
    "NotifierFactory",
    "get_notifier",
]
_PROVIDERS = {"FeishuNotifier": "feishu", "TelegramNotifier": "telegram"}
__all__ += [name for name, channel in _PROVIDERS.items() if channel in bundled_channels()]


def get_notifier(channel: str) -> NotificationChannel:
    """Instantiate a bundled provider without importing unrelated integrations."""
    from delivery import resolve_channel
    channel = resolve_channel(channel)
    if channel == "feishu":
        from .feishu import FeishuNotifier
        return FeishuNotifier()
    elif channel == "telegram":
        from .telegram import TelegramNotifier
        return TelegramNotifier()
    else:
        raise ValueError(f"Unknown notification channel: {channel}")


def __getattr__(name):
    """Keep existing notifier imports lazy so another provider can be omitted."""
    if name not in _PROVIDERS or _PROVIDERS[name] not in bundled_channels():
        raise AttributeError(name)
    from delivery import resolve_channel
    from importlib import import_module
    channel = resolve_channel(_PROVIDERS[name])
    return getattr(import_module("." + channel, __name__), name)
