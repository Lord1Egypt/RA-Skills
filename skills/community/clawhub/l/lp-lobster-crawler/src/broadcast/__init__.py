"""播报模块。"""

from .dingtalk import send_markdown, send_text
from .templates import (
    get_broadcast_strategy,
    render_daily_digest,
    render_immediate,
    render_weekly_digest,
)

__all__ = [
    "get_broadcast_strategy",
    "render_daily_digest",
    "render_immediate",
    "render_weekly_digest",
    "send_markdown",
    "send_text",
]
