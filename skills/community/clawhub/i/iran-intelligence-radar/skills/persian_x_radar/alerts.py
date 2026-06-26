from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional


SendAlertFn = Callable[..., None]


@dataclass
class AlertThresholds:
    high_engagement: int = 500
    medium_engagement: int = 150


def classify_alert_level(text_fa: str, engagement_score: int, thresholds: AlertThresholds) -> str:
    high_keywords = ["موشک", "حمله", "غنی", "هسته", "nuclear", "missile"]
    medium_keywords = ["اعتراض", "تحریم", "sanction", "protest"]

    text = text_fa.lower()

    if engagement_score >= thresholds.high_engagement or any(k in text for k in high_keywords):
        return "HIGH"
    if engagement_score >= thresholds.medium_engagement or any(k in text for k in medium_keywords):
        return "MEDIUM"
    return "LOW"


def trigger_alerts_if_needed(
    rows: Iterable[Dict],
    channels: List[str],
    send_alert_tool: Optional[SendAlertFn] = None,
) -> None:
    if send_alert_tool is None:
        return

    for row in rows:
        if row.get("alert") != "HIGH":
            continue
        msg = (
            "HIGH ALERT\n"
            "Possible missile/nuclear discussion trending on Persian X.\n"
            f"Author: {row.get('author')}\n"
            f"Link: {row.get('link')}"
        )
        for channel in channels:
            try:
                send_alert_tool(channel=channel, message=msg)
            except Exception:
                continue
