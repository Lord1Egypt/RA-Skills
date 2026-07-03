from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from typing import Any


class MatchClass(StrEnum):
    HIGH = "高度匹配"
    POSSIBLE = "可能匹配"
    NO_MATCH = "不匹配"
    INSUFFICIENT = "信息不足"


class CandidateStatus(StrEnum):
    INVESTIGATE = "待调查"
    HUMAN_REVIEW = "待人工核验"
    NOT_QUALIFIED = "不符合"
    AWAITING_APPROVAL = "待候选确认"
    APPROVED = "已批准"
    DRAFT_REVIEW = "草稿待审"
    CONTACTED = "已联系"
    REPLIED = "已回复"
    ADVANCING = "推进中"
    FOLLOW_UP_LATER = "稍后跟进"
    NOT_INTERESTED = "无意向"
    UNSUBSCRIBED = "退订"
    CLOSED = "关闭"


class ReplyClass(StrEnum):
    ADVANCE = "积极推进"
    MORE_INFO = "需要更多信息"
    LATER = "稍后联系"
    NOT_INTERESTED = "无意向"
    UNSUBSCRIBE = "退订"
    UNCLEAR = "无法判断"


@dataclass(frozen=True)
class PaperRecord:
    source_key: str
    source_type: str
    source_record_id: str
    title: str
    normalized_title: str
    publication_date: date
    publication_date_precision: str = "day"
    abstract: str | None = None
    doi: str | None = None
    original_keywords: tuple[str, ...] = ()
    official_url: str | None = None
    acceptance_evidence_url: str | None = None
    is_retracted: bool = False
    authors: tuple[dict, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PaperMatchResult:
    classification: MatchClass
    evidence: tuple[str, ...]
    matched_requirements: tuple[str, ...]
    missing_requirements: tuple[str, ...]
    uncertainties: tuple[str, ...]
    summary: str
    model: str
    usage: dict[str, Any]


@dataclass(frozen=True)
class KeywordGenerationResult:
    keywords: tuple[str, ...]
    model: str
    usage: dict[str, Any]


@dataclass(frozen=True)
class ReplyClassificationResult:
    classification: ReplyClass
    evidence_summary: str
    confidence: float
    suggested_action: str
    needs_reply: bool
    reply_body: str | None
    followup_date: str | None
    model: str
    usage: dict[str, Any]
