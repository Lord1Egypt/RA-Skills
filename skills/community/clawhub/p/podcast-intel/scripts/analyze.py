#!/usr/bin/env python3
"""Analyze and score podcast episodes for relevance, novelty, and overlap."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from utils import Analysis, OverlapFlag, SegmentScore, load_diary, load_interests_config

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "with",
}


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Analyze episodes for relevance and novelty")
    parser.add_argument(
        "--episodes",
        type=str,
        help="Path to segmented episodes JSON file or JSON string",
    )
    parser.add_argument("--interests", type=Path, help="Path to interests configuration YAML")
    parser.add_argument("--diary", type=Path, help="Path to consumption diary JSONL")
    parser.add_argument("--output", type=Path, help="Output path for analysis JSON")
    return parser.parse_args()


def tokenize(text: str) -> Set[str]:
    """Tokenize text into lowercase content words."""
    raw_tokens = set(re.findall(r"[a-zA-Z0-9]+", text.lower()))
    normalized: Set[str] = set()
    for token in raw_tokens:
        if token in STOP_WORDS or len(token) <= 1:
            continue
        if token.endswith("s") and len(token) > 3:
            token = token[:-1]
        normalized.add(token)
    return normalized


def text_overlap_score(left: str, right: str) -> float:
    """Compute Jaccard overlap between two short texts."""
    left_tokens = tokenize(left)
    right_tokens = tokenize(right)
    if not left_tokens or not right_tokens:
        return 0.0
    intersection = len(left_tokens & right_tokens)
    union = len(left_tokens | right_tokens)
    return intersection / union if union else 0.0


def score_interest_group(text: str, phrases: List[str], weight: float) -> float:
    """Score a segment against one group of user interest phrases."""
    if not phrases:
        return 0.0

    scores = []
    lowered = text.lower()
    for phrase in phrases:
        phrase_lower = phrase.lower().strip()
        if not phrase_lower:
            continue
        exact = 1.0 if phrase_lower in lowered else 0.0
        overlap = text_overlap_score(lowered, phrase_lower)
        scores.append(max(exact, overlap))

    if not scores:
        return 0.0
    return weight * max(scores)


def compute_relevance_score(segment_label: str, segment_summary: str, interests: Dict[str, Any]) -> float:
    """Compute relevance score (0-1) from user interest profile."""
    text = f"{segment_label} {segment_summary}".strip()
    if not text:
        return 0.1

    profile = interests or {}
    interest_groups = profile.get("interests", {})

    relevance = 0.2  # neutral baseline
    relevance += score_interest_group(text, interest_groups.get("primary", []), 0.6)
    relevance += score_interest_group(text, interest_groups.get("secondary", []), 0.35)
    relevance += score_interest_group(text, interest_groups.get("casual", []), 0.2)

    anti_score = score_interest_group(text, profile.get("anti_interests", []), 0.7)
    boost_score = score_interest_group(text, profile.get("boost_keywords", []), 0.5)

    relevance += boost_score
    relevance -= anti_score
    return max(0.0, min(1.0, relevance))


def compute_novelty_score(segment_label: str, segment_summary: str, diary_entries: List[Dict[str, Any]]) -> float:
    """Compute novelty score (0-1) vs prior diary topics."""
    if not diary_entries:
        return 0.9

    segment_text = f"{segment_label} {segment_summary}".strip()
    if not segment_text:
        return 0.1

    max_overlap = 0.0
    for entry in diary_entries:
        for prior_topic in entry.get("topics_exposed", []):
            overlap = text_overlap_score(segment_text, str(prior_topic))
            if overlap > max_overlap:
                max_overlap = overlap

    novelty = 1.0 - max_overlap
    return max(0.05, min(1.0, novelty))


def build_segment_scores(
    topics: List[Dict[str, Any]],
    interests: Dict[str, Any],
    diary: List[Dict[str, Any]],
) -> List[SegmentScore]:
    """Compute per-segment score payloads."""
    segment_scores: List[SegmentScore] = []

    for topic in topics:
        relevance = compute_relevance_score(topic.get("label", ""), topic.get("summary", ""), interests)
        novelty = compute_novelty_score(topic.get("label", ""), topic.get("summary", ""), diary)

        try:
            density = float(topic.get("information_density", 0.5))
        except (TypeError, ValueError):
            density = 0.5
        density = max(0.0, min(1.0, density))

        composite = 0.35 * relevance + 0.35 * novelty + 0.30 * density

        if composite >= 0.72:
            recommendation = f"LISTEN — high signal ({composite:.0%} composite)"
        elif composite >= 0.45:
            recommendation = f"MAYBE — mixed signal ({composite:.0%} composite)"
        else:
            recommendation = f"SKIP — low signal ({composite:.0%} composite)"

        segment_scores.append(
            SegmentScore(
                topic_id=int(topic.get("topic_id", 0)),
                label=str(topic.get("label", "Unknown topic")),
                relevance=relevance,
                novelty=novelty,
                density=density,
                composite_score=composite,
                listen_recommendation=recommendation,
            )
        )

    return segment_scores


def analyze_single_episode(
    episode: Dict[str, Any],
    interests: Dict[str, Any],
    diary: List[Dict[str, Any]],
) -> Optional[Analysis]:
    """Analyze a single segmented episode."""
    episode_id = episode.get("episode_id") or episode.get("id", "unknown")
    show = str(episode.get("show", "Unknown"))
    title = str(episode.get("title", "Untitled"))
    topics = episode.get("topics", [])

    if not topics:
        return None

    segment_scores = build_segment_scores(topics, interests, diary)
    if not segment_scores:
        return None

    novelty_by_topic_id = {segment.topic_id: segment.novelty for segment in segment_scores}
    total_minutes = 0.0
    novel_minutes = 0.0
    for topic in topics:
        try:
            duration_minutes = max(0.0, float(topic.get("duration_seconds", 0.0)) / 60.0)
        except (TypeError, ValueError):
            duration_minutes = 0.0
        total_minutes += duration_minutes
        topic_id = int(topic.get("topic_id", 0))
        if novelty_by_topic_id.get(topic_id, 0.0) >= 0.6:
            novel_minutes += duration_minutes

    if total_minutes <= 0:
        total_minutes = max(1.0, len(segment_scores) * 5.0)

    segment_scores.sort(key=lambda item: item.composite_score, reverse=True)
    novel_ratio = max(0.0, min(1.0, novel_minutes / total_minutes))
    average_segment_score = sum(s.composite_score for s in segment_scores) / len(segment_scores)
    wyt_score = max(0.0, min(1.0, average_segment_score * novel_ratio))

    novel_percent = int(round(novel_ratio * 100))
    if wyt_score >= 0.70:
        recommendation = (
            f"HIGH — {novel_percent}% novel content ({novel_minutes:.0f} of {total_minutes:.0f} min), "
            "start with top-ranked segments."
        )
    elif wyt_score >= 0.40:
        recommendation = (
            f"MEDIUM — {novel_percent}% novel content, selective listening recommended."
        )
    else:
        recommendation = (
            "LOW — heavy overlap with prior topics or weak relevance for your profile."
        )

    return Analysis(
        episode_id=str(episode_id),
        show=show,
        title=title,
        worth_your_time_score=round(wyt_score, 4),
        novel_minutes=round(novel_minutes, 2),
        total_minutes=round(total_minutes, 2),
        recommendation=recommendation,
        segments_ranked=segment_scores,
        overlaps=[],
    )


def analyze_episodes(
    episodes: List[Dict[str, Any]],
    interests: Dict[str, Any],
    diary: List[Dict[str, Any]],
) -> List[Analysis]:
    """Analyze all episodes in the batch."""
    analyses: List[Analysis] = []
    for episode in episodes:
        analysis = analyze_single_episode(episode, interests, diary)
        if analysis:
            analyses.append(analysis)
    return analyses


def detect_cross_episode_overlaps(analyses: List[Analysis], threshold: float = 0.55) -> None:
    """Populate overlap flags when segments across shows are highly similar."""
    for i, first in enumerate(analyses):
        for j in range(i + 1, len(analyses)):
            second = analyses[j]
            if first.show == second.show:
                continue

            for first_seg in first.segments_ranked:
                for second_seg in second.segments_ranked:
                    overlap = text_overlap_score(first_seg.label, second_seg.label)
                    if overlap < threshold:
                        continue

                    winner = first if first_seg.composite_score >= second_seg.composite_score else second
                    first_verdict = (
                        f"{winner.show} has the stronger treatment for this topic"
                    )
                    second_verdict = first_verdict

                    first.overlaps.append(
                        OverlapFlag(
                            topic=first_seg.label,
                            this_episode_segment=first_seg.topic_id,
                            overlaps_with_show=second.show,
                            overlaps_with_episode=second.title,
                            overlaps_with_segment=second_seg.topic_id,
                            overlap_score=round(overlap, 4),
                            verdict=first_verdict,
                        )
                    )
                    second.overlaps.append(
                        OverlapFlag(
                            topic=second_seg.label,
                            this_episode_segment=second_seg.topic_id,
                            overlaps_with_show=first.show,
                            overlaps_with_episode=first.title,
                            overlaps_with_segment=first_seg.topic_id,
                            overlap_score=round(overlap, 4),
                            verdict=second_verdict,
                        )
                    )


def load_episodes_payload(path_or_json: Optional[str]) -> List[Dict[str, Any]]:
    """Load segmented episodes from JSON string, file, or stdin."""
    if path_or_json:
        try:
            payload = json.loads(path_or_json)
        except json.JSONDecodeError:
            with open(path_or_json, "r") as handle:
                payload = json.load(handle)
    else:
        payload = json.load(sys.stdin)

    if isinstance(payload, list):
        return payload
    return [payload]


def load_diary_entries(path: Optional[Path]) -> List[Dict[str, Any]]:
    """Load diary JSONL entries from explicit path or default location."""
    if path and path.exists():
        entries: List[Dict[str, Any]] = []
        with open(path, "r") as handle:
            for line in handle:
                if line.strip():
                    entries.append(json.loads(line))
        return entries
    return load_diary()


def analysis_to_dict(analysis: Analysis) -> Dict[str, Any]:
    """Serialize Analysis dataclass for output JSON."""
    return {
        "episode_id": analysis.episode_id,
        "show": analysis.show,
        "title": analysis.title,
        "worth_your_time_score": analysis.worth_your_time_score,
        "novel_minutes": analysis.novel_minutes,
        "total_minutes": analysis.total_minutes,
        "recommendation": analysis.recommendation,
        "segments_ranked": [
            {
                "topic_id": segment.topic_id,
                "label": segment.label,
                "relevance": segment.relevance,
                "novelty": segment.novelty,
                "density": segment.density,
                "composite_score": segment.composite_score,
                "listen_recommendation": segment.listen_recommendation,
            }
            for segment in analysis.segments_ranked
        ],
        "overlaps": [
            {
                "topic": overlap.topic,
                "this_episode_segment": overlap.this_episode_segment,
                "overlaps_with_show": overlap.overlaps_with_show,
                "overlaps_with_episode": overlap.overlaps_with_episode,
                "overlaps_with_segment": overlap.overlaps_with_segment,
                "overlap_score": overlap.overlap_score,
                "verdict": overlap.verdict,
            }
            for overlap in analysis.overlaps
        ],
    }


def main() -> None:
    """Main analysis entry point."""
    args = parse_args()

    try:
        episodes = load_episodes_payload(args.episodes)
    except Exception as exc:
        print(f"Error loading episodes data: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        interests = load_interests_config(args.interests)
    except Exception as exc:
        print(f"Warning: could not load interests config: {exc}", file=sys.stderr)
        interests = {}

    try:
        diary = load_diary_entries(args.diary)
    except Exception as exc:
        print(f"Warning: could not load diary: {exc}", file=sys.stderr)
        diary = []

    analyses = analyze_episodes(episodes, interests, diary)
    if not analyses:
        print("No analyses generated", file=sys.stderr)
        sys.exit(1)

    detect_cross_episode_overlaps(analyses)
    analyses.sort(key=lambda item: item.worth_your_time_score, reverse=True)

    output = [analysis_to_dict(analysis) for analysis in analyses]
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as handle:
            json.dump(output, handle, indent=2)
    else:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
