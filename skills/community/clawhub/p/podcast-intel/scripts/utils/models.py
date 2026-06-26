"""Data models for podcast-intel skill."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Episode:
    """Podcast episode metadata."""
    id: str
    show: str
    title: str
    published: datetime
    audio_url: str
    duration_seconds: int
    description: str
    feed_url: str


@dataclass
class TranscriptSegment:
    """A time-bounded transcript segment."""
    start: float
    end: float
    text: str


@dataclass
class Transcript:
    """Full episode transcript with segments."""
    episode_id: str
    segments: List[TranscriptSegment]
    full_text: str
    word_count: int
    language: str


@dataclass
class TopicSegment:
    """A topical segment identified from transcript."""
    topic_id: int
    label: str
    start_time: float
    end_time: float
    duration_seconds: float
    key_entities: List[str]
    summary: str
    information_density: float


@dataclass
class Segmentation:
    """Segmentation result for an episode."""
    episode_id: str
    topics: List[TopicSegment]
    total_topics: int
    avg_topic_duration_seconds: float


@dataclass
class SegmentScore:
    """Relevance, novelty, and density scores for a segment."""
    topic_id: int
    label: str
    relevance: float  # 0-1: how well matches user interests
    novelty: float    # 0-1: how much new info vs. diary
    density: float    # 0-1: information density
    composite_score: float  # weighted combination
    listen_recommendation: str  # "LISTEN" or "SKIP" with reasoning


@dataclass
class OverlapFlag:
    """Cross-episode deduplication flag."""
    topic: str
    this_episode_segment: int
    overlaps_with_show: str
    overlaps_with_episode: str
    overlaps_with_segment: int
    overlap_score: float
    verdict: str


@dataclass
class Analysis:
    """Complete analysis of an episode."""
    episode_id: str
    show: str
    title: str
    worth_your_time_score: float  # 0-1
    novel_minutes: float
    total_minutes: float
    recommendation: str
    segments_ranked: List[SegmentScore]
    overlaps: List[OverlapFlag] = field(default_factory=list)


@dataclass
class DiaryEntry:
    """An entry in the consumption diary (JSONL format)."""
    briefed_at: datetime
    episode_id: str
    show: str
    title: str
    topics_exposed: List[str]
    topic_embeddings_hash: str
    wyt_score: float
    novel_minutes: float
    total_minutes: float
    segments_recommended: List[int]
    segments_skipped: List[int]
    overlap_flags: List[str]


# Type aliases for clarity
EpisodeList = List[Episode]
TranscriptList = List[Transcript]
SegmentationList = List[Segmentation]
AnalysisList = List[Analysis]
