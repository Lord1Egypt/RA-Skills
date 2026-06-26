"""Data models for Personal Knowledge Hub."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class KnowledgeItem:
    id: str
    title: str
    content: str
    source_type: str
    source_uri: str = ""
    tags: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    created_at: str = ""


@dataclass
class SearchResult:
    item: KnowledgeItem
    snippet: str
    relevance_score: float
    matched_terms: List[str]
    related_tags: List[str]


@dataclass
class KnowledgeGraph:
    central_topic: str
    entities: List[Dict]
    connections: List[Dict]
    depth: int = 1


@dataclass
class QueryIntent:
    intent_type: str = "search"
    query_text: str = ""
    topic: str = ""
    filters: Dict = field(default_factory=dict)

