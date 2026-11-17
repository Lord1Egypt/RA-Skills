"""Bundled delivery capabilities, independent of quota and algorithm execution."""

import importlib
import json
from pathlib import Path


def bundled_features():
    """Read the build-time feature manifest without loading optional providers."""
    return json.loads(Path(__file__).with_name("features.json").read_text(encoding="utf-8"))


def bundled_channels():
    """Return only provider channels included by the release packager."""
    return tuple(bundled_features()["delivery_channels"])


def resolve_channel(channel=None):
    """Preserve the legacy Feishu default when bundled; otherwise return links only."""
    available = bundled_channels()
    selected = (channel or "").strip().lower()
    if not selected:
        selected = "feishu" if "feishu" in available else "none"
    if selected in ("feishu", "telegram") and selected not in available:
        raise ValueError('当前安装包未包含此投递渠道：' + selected)
    # Other channel names remain host-managed, as in the existing worker API.
    return selected


def delivery_instructions(channel, base_dir, recipient, *, is_video):
    """Load provider-specific worker instructions only for a bundled channel."""
    channel = resolve_channel(channel)
    if channel in ("feishu", "telegram"):
        provider = importlib.import_module("notifications." + channel)
        return provider.delivery_instructions(base_dir, recipient, is_video=is_video)
    if channel == "none":
        return "  2. Return primary_result_url or output_urls to the parent session; no notification is requested."
    if channel == "discord":
        extension = "mp4" if is_video else "jpg"
        return (
            "  2. Download the result and send it with the host message tool on Discord "
            "(about 25 MB limit; send the URL instead for larger files).\n"
            "     Replace <result_url> below with primary_result_url or output_urls[0].\n"
            f"     curl -fL -o /tmp/vmake_result.{extension} '<result_url>'\n"
            "     Then call the host tool:\n"
            f"     message(action=\"send\", channel=\"discord\", target={json.dumps(recipient)}, "
            f"filePath=\"/tmp/vmake_result.{extension}\")\n"
            "     For larger files, send the result URL as text to the same channel and target."
        )
    return (
        f"  2. Use the host message tool with action=send, channel={json.dumps(channel)}, "
        f"target={json.dumps(recipient)} to deliver the result as media or a link "
        "using primary_result_url or output_urls[0]."
    )
