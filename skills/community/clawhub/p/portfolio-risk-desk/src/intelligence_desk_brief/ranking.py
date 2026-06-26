"""Evidence ranking for portfolio-aware prioritization."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.memory import MemoryContext, fingerprint_evidence


def _recency_score(published_at: str | None, lookback_hours: int) -> int:
    if not published_at:
        return 0
    try:
        parsed = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    except ValueError:
        return 0
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    age = datetime.now(timezone.utc) - parsed
    if age <= timedelta(hours=max(lookback_hours // 4, 1)):
        return 15
    if age <= timedelta(hours=lookback_hours):
        return 8
    return 2


def rank_evidence(
    request: CreateBriefRequest,
    normalized_items: list[dict[str, Any]],
    *,
    memory_context: MemoryContext | None = None,
) -> list[dict[str, Any]]:
    corroboration_counts: dict[str, int] = {}
    for item in normalized_items:
        key = item["factor"]
        corroboration_counts[key] = corroboration_counts.get(key, 0) + 1

    ranked: list[dict[str, Any]] = []
    for item in normalized_items:
        reasons: list[str] = []
        score = 0

        if item["direct_relevance"]:
            points = 30 * item["direct_relevance"]
            score += points
            reasons.append(f"direct holdings relevance +{points}")
        if item["watchlist_relevance"]:
            points = 20 * item["watchlist_relevance"]
            score += points
            reasons.append(f"watchlist relevance +{points}")
        if item["adjacent_relevance"]:
            points = 12 * item["adjacent_relevance"]
            score += points
            reasons.append(f"theme match +{points}")

        if item["cross_name_impact"] > 1:
            points = 5 * item["cross_name_impact"]
            score += points
            reasons.append(f"cross-name impact +{points}")

        confidence_points = item["confidence_value"] * 6
        score += confidence_points
        reasons.append(f"confidence +{confidence_points}")

        signal_points = item["signal_value"] * 5
        score += signal_points
        reasons.append(f"signal strength +{signal_points}")

        recency_points = _recency_score(item["published_at"], request.lookback_hours)
        score += recency_points
        if recency_points:
            reasons.append(f"recency +{recency_points}")

        corroboration = corroboration_counts.get(item["factor"], 0)
        if corroboration > 1:
            points = (corroboration - 1) * 4
            score += points
            reasons.append(f"corroboration +{points}")

        if item["is_x_signal"]:
            score -= 8
            reasons.append("supplementary X penalty -8")
        if item["low_quality"]:
            score -= 25
            reasons.append("low-quality or degraded source penalty -25")
        if memory_context and fingerprint_evidence(item) in memory_context.repeated_evidence_fingerprints:
            if item["is_x_signal"] or item["signal_strength"] == "low":
                score -= 14
                reasons.append("repeated low-signal memory penalty -14")
            else:
                score -= 4
                reasons.append("repeated evidence novelty penalty -4")

        ranked_item = dict(item)
        ranked_item["ranking"] = {"score": score, "reasons": reasons}
        ranked.append(ranked_item)

    ranked.sort(key=lambda item: item["ranking"]["score"], reverse=True)
    return ranked
