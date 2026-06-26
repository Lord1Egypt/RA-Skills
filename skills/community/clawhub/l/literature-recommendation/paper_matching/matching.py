"""Rule-based matching and ranking."""

from __future__ import annotations

from datetime import datetime, timezone

from .models import MemberProfile, Paper, Recommendation


def _lower_tokens(value: str) -> list[str]:
    value = (value or "").lower().replace("/", " ").replace("-", " ")
    return [token for token in value.split() if token]


def _contains_any(text: str, keywords: list[str]) -> list[str]:
    haystack = (text or "").lower()
    matched = []
    for keyword in keywords:
        needle = keyword.lower().strip()
        if needle and needle in haystack:
            matched.append(keyword)
    return matched


def score_paper(profile: MemberProfile, paper: Paper) -> tuple[float, str, list[str]]:
    title = paper.title.lower()
    abstract = paper.abstract.lower()
    tags = [tag.lower() for tag in paper.tags]
    keywords = profile.keywords or []
    directions = [profile.primary_direction, *profile.secondary_directions]
    excluded = profile.excluded_topics or []

    excluded_hits = _contains_any(title + " " + abstract, excluded)
    if excluded_hits:
        return 0.0, f"filtered by excluded topics: {', '.join(excluded_hits[:3])}", excluded_hits

    matched_keywords = _contains_any(title, keywords) + _contains_any(abstract, keywords)
    matched_directions = _contains_any(title, directions) + _contains_any(abstract, directions)
    matched_tags = [tag for tag in tags if any(keyword.lower() in tag for keyword in keywords)]

    score = 0.0
    reasons: list[str] = []

    if matched_directions:
        score += 6.0 + min(3.0, len(set(matched_directions)) * 1.5)
        reasons.append(f"matches direction: {', '.join(sorted(set(matched_directions))[:3])}")
    if matched_keywords:
        score += 4.0 + min(2.0, len(set(matched_keywords)) * 0.8)
        reasons.append(f"matches keywords: {', '.join(sorted(set(matched_keywords))[:4])}")
    if matched_tags:
        score += 1.5 + min(1.5, len(set(matched_tags)) * 0.5)
        reasons.append(f"matches tags: {', '.join(sorted(set(matched_tags))[:4])}")

    if not reasons:
        title_tokens = _lower_tokens(profile.primary_direction)
        overlap = [token for token in title_tokens if token in title or token in abstract]
        if overlap:
            score += 2.5
            reasons.append(f"direction token overlap: {', '.join(overlap[:3])}")

    try:
        published = datetime.fromisoformat(paper.published_at.replace("Z", "+00:00")).astimezone(timezone.utc)
        age_days = max(0.0, (datetime.now(timezone.utc) - published).total_seconds() / 86400.0)
    except Exception:
        age_days = 14.0

    novelty_bonus = max(0.0, 3.5 - age_days * 0.25)
    score += novelty_bonus
    if novelty_bonus > 0:
        reasons.append(f"novelty bonus: {novelty_bonus:.1f}")

    if profile.confidence:
        score *= max(0.7, min(1.3, profile.confidence))

    if not reasons:
        reasons.append("light lexical similarity")

    return round(score, 3), "; ".join(reasons), []


def rank_for_member(profile: MemberProfile, papers: list[Paper], top_k: int = 5) -> list[Recommendation]:
    scored = []
    seen = set()
    for paper in papers:
        if paper.paper_id in seen:
            continue
        seen.add(paper.paper_id)
        score, reason, _ = score_paper(profile, paper)
        if score <= 0:
            continue
        scored.append((score, paper, reason))

    scored.sort(key=lambda item: (-item[0], item[1].published_at, item[1].paper_id))
    recommendations: list[Recommendation] = []
    for index, (score, paper, reason) in enumerate(scored[:top_k], start=1):
        recommendations.append(
            Recommendation(
                record_id=profile.record_id,
                paper_id=paper.paper_id,
                score=score,
                rank=index,
                reason=reason,
                channel="personal_dm",
            )
        )
    return recommendations
