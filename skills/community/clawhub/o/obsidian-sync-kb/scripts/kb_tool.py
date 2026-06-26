#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import dataclasses
import datetime as dt
import hashlib
import html
import json
import math
import os
import pathlib
import re
import sqlite3
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import yaml


BASE_DIR = pathlib.Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = BASE_DIR / "config.yaml"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
)


BAD_CAPTURE_PATTERNS = [
    "异常流量",
    "关于此网页",
    "确认这些请求是由您而不是自动程序发出的",
    "unusual traffic",
    "automated queries",
    "robot check",
    "captcha",
]

BLOCKED_SOURCE_PATTERNS = [
    "需要登录",
    "登录后查看",
    "无权限",
    "权限不足",
    "请先登录",
    "访问受限",
    "内部文档",
    "受限访问",
    "you need permission",
    "permission required",
    "access denied",
    "sign in",
    "log in",
    "private document",
    "forbidden",
]

LOW_SIGNAL_PATTERNS = [
    "view all features",
    "view all solutions",
    "view all topics",
    "github advanced security",
    "customer stories",
    "events & webinars",
    "premium support",
    "plans and pricing",
    "sign in to github",
    "view all industries",
    "view all use cases",
]

BOILERPLATE_PREFIXES = [
    "公众号名称：",
    "作者名称：",
    "发布时间：",
    "关注公众号回复",
    "扫码",
    "文章来源：",
    "来源：",
]

BOILERPLATE_SUBSTRINGS = [
    "免费拉你进",
    "关注下",
    "一起学习 原创",
    "ai code creation",
    "developer workflows",
    "github copilotwrite better code with ai",
    "mcp registrynewintegrate external tools",
]

TOPIC_DISPLAY_NAMES = {
    "openclaw": "OpenClaw",
    "agent-harness": "Agent 与 Harness",
    "retrieval-rag": "检索与 RAG",
    "skills-tools": "Skills 与工具",
    "ai-org-management": "AI 组织与管理",
    "case-study": "案例与实践",
    "misc": "其他",
}

OPEN_QUESTIONS = {
    "openclaw": [
        "OpenClaw 应该优先把哪些检索能力内置成稳定工作流？",
        "哪些同步内容值得提升为 OpenClaw 的长期知识资产？",
    ],
    "agent-harness": [
        "哪些 harness 机制是当前 OpenClaw 最缺的关键环节？",
        "多 agent、上下文压缩和任务回退之间的边界应该如何划分？",
    ],
    "retrieval-rag": [
        "中文技术文章的 chunk 粒度和重排策略应该如何继续优化？",
        "哪些查询场景需要专题卡片，哪些只需要返回原文证据？",
    ],
    "skills-tools": [
        "哪些工具和 skill 应该直接固化成 OpenClaw 的默认工作流？",
        "插件类内容应该如何和正式研究结论分层沉淀？",
    ],
    "ai-org-management": [
        "这些团队协作理念里哪些适合你现在的组织阶段？",
        "哪些流程变化会真实影响产出，而不仅是概念层面的升级？",
    ],
    "case-study": [
        "哪些实战案例最值得拆成可复用的方法论？",
        "案例里的前提条件哪些适用于你当前团队，哪些不适用？",
    ],
    "misc": [
        "这类内容是否值得继续沉淀，还是应该保持为原始收件箱材料？",
        "它和你现有的 OpenClaw/检索主题之间是否存在隐藏关联？",
    ],
}

TOPIC_RULES: List[Tuple[str, List[str]]] = [
    (
        "openclaw",
        [
            "openclaw",
            "claw0",
            "橙皮书",
            "open claw",
        ],
    ),
    (
        "agent-harness",
        [
            "harness",
            "orchestration",
            "编排",
            "子 agent",
            "子代理",
            "multi-agent",
            "多agent",
            "多 agent",
            "context",
            "上下文",
            "claude code",
            "codex",
            "agent loop",
        ],
    ),
    (
        "retrieval-rag",
        [
            "检索",
            "rag",
            "retrieval",
            "embedding",
            "vector",
            "向量",
            "召回",
            "重排",
            "知识库",
            "chunk",
            "search",
        ],
    ),
    (
        "skills-tools",
        [
            "skill",
            "skills",
            "tool",
            "tools",
            "插件",
            "web access",
            "notehelper",
            "浏览器能力",
            "工具",
        ],
    ),
    (
        "ai-org-management",
        [
            "manager",
            "management",
            "组织",
            "团队",
            "管理",
            "流程",
            "看板",
            "symphony",
            "paperclip",
            "supermanager",
        ],
    ),
    (
        "case-study",
        [
            "实战",
            "案例",
            "复盘",
            "最佳实践",
            "best practice",
            "教材",
            "教程",
            "经验",
            "得物",
        ],
    ),
]


@dataclasses.dataclass
class Config:
    vault_root: pathlib.Path
    inbox_root: pathlib.Path
    research_root: pathlib.Path
    topic_updates_root: pathlib.Path
    daily_digest_root: pathlib.Path
    artifacts_root: pathlib.Path
    state_root: pathlib.Path
    exclude_bad_capture: bool
    target_min_chars: int
    target_max_chars: int
    overlap_chars: int
    promotion_min_quality: float
    promotion_min_docs: int
    research_min_chars: int
    max_external_sources: int
    network_timeout: int
    enable_network: bool
    full_rescan_days: int


@dataclasses.dataclass
class Fragment:
    heading_path: str
    text: str
    start_offset: int
    end_offset: int


@dataclasses.dataclass
class NormalizedNote:
    doc_id: str
    source_file: str
    source_type: str
    title: str
    author: str
    source_domain: str
    original_url: str
    saved_at: str
    doc_shape: str
    capture_status: str
    content_kind: str
    source_resolution_status: str
    research_status: str
    theme_status: str
    clean_text: str
    image_refs: List[str]
    source_links: List[str]
    auto_topics: List[str]
    summary: str
    quality_score: float
    theme_candidate: str
    change_summary: str
    content_hash: str
    last_seen_at: str
    last_enriched_at: str
    retry_after: str
    obsidian_path: str
    raw_text_length: int

    def to_record(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> "NormalizedNote":
        return cls(**record)


@dataclasses.dataclass
class ChunkRecord:
    chunk_id: str
    doc_id: str
    heading_path: str
    chunk_text: str
    start_offset: int
    end_offset: int
    rank_features: Dict[str, Any]

    def to_record(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class EnrichedNote:
    doc_id: str
    theme_candidate: str
    research_summary: str
    key_findings: List[str]
    source_evidence: List[Dict[str, Any]]
    confidence: float
    gaps: List[str]
    research_status: str
    updated_at: str

    def to_record(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> "EnrichedNote":
        return cls(**record)


@dataclasses.dataclass
class ThemeUpdateLog:
    topic: str
    topic_title: str
    theme_kind: str
    updated_at: str
    trigger_docs: List[str]
    what_changed: str
    why_changed: str
    next_questions: List[str]
    file_path: str
    obsidian_path: str

    def to_record(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


def load_config(path: pathlib.Path) -> Config:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    vault_root_raw = str(raw.get("vault_root") or "").strip()
    if not vault_root_raw or vault_root_raw.startswith("__SET_"):
        vault_root_raw = os.environ.get("OBSIDIAN_SYNC_KB_VAULT", "").strip()
    if not vault_root_raw:
        raise FileNotFoundError(
            "config not initialized; run scripts/setup_config.py --vault-root /path/to/ClawVault "
            "or set OBSIDIAN_SYNC_KB_VAULT"
        )
    vault_root = pathlib.Path(vault_root_raw).expanduser().resolve()
    inbox_root = vault_root / raw.get("inbox_dir", "笔记同步助手")
    research_root = vault_root / raw.get("research_dir", "Research/同步助手主题卡片")
    topic_updates_root = vault_root / raw.get("topic_updates_dir", "Research/同步助手主题更新日志")
    daily_digest_root = vault_root / raw.get("daily_digest_dir", "Research/同步助手今日变更摘要")
    artifacts_root = BASE_DIR / raw.get("artifacts_dir", "artifacts")
    state_root = BASE_DIR / raw.get("state_dir", "state")
    chunking = raw.get("chunking", {})
    promotion = raw.get("promotion", {})
    research = raw.get("research", {})
    scan = raw.get("scan", {})
    return Config(
        vault_root=vault_root,
        inbox_root=inbox_root,
        research_root=research_root,
        topic_updates_root=topic_updates_root,
        daily_digest_root=daily_digest_root,
        artifacts_root=artifacts_root,
        state_root=state_root,
        exclude_bad_capture=bool(raw.get("exclude_bad_capture", True)),
        target_min_chars=int(chunking.get("target_min_chars", 400)),
        target_max_chars=int(chunking.get("target_max_chars", 800)),
        overlap_chars=int(chunking.get("overlap_chars", 100)),
        promotion_min_quality=float(promotion.get("min_quality", 0.55)),
        promotion_min_docs=int(promotion.get("min_docs", 3)),
        research_min_chars=int(research.get("min_chars", 220)),
        max_external_sources=int(research.get("max_external_sources", 3)),
        network_timeout=int(research.get("network_timeout", 10)),
        enable_network=bool(research.get("enable_network", True)),
        full_rescan_days=int(scan.get("full_rescan_days", 7)),
    )


def ensure_layout(config: Config) -> None:
    config.artifacts_root.mkdir(parents=True, exist_ok=True)
    config.state_root.mkdir(parents=True, exist_ok=True)
    config.research_root.mkdir(parents=True, exist_ok=True)
    config.topic_updates_root.mkdir(parents=True, exist_ok=True)
    config.daily_digest_root.mkdir(parents=True, exist_ok=True)


def now_string() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha1_text(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()


def normalize_whitespace(value: str) -> str:
    value = value.replace("\u200b", "")
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def slugify_topic(value: str) -> str:
    slug = re.sub(r"[^a-z0-9\-]+", "-", value.lower()).strip("-")
    return slug or f"topic-{sha1_text(value)[:10]}"


def path_in_vault(path: pathlib.Path, vault_root: pathlib.Path) -> str:
    return path.resolve().relative_to(vault_root.resolve()).as_posix()


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not match:
        return {}, text
    try:
        frontmatter = yaml.safe_load(match.group(1)) or {}
    except Exception:
        frontmatter = {}
    body = text[match.end():]
    return frontmatter, body


def dedupe_keep_order(items: Iterable[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for item in items:
        item = str(item).strip()
        if not item or item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def extract_image_refs(text: str) -> List[str]:
    refs: List[str] = []
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        refs.append(match.group(1).strip())
    for match in re.finditer(r"!\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text):
        refs.append(match.group(1).strip())
    return dedupe_keep_order(refs)


def normalize_source_link(link: str) -> str:
    link = link.strip().strip("<>").strip()
    while link and link[-1] in ".,);]，。；、":
        link = link[:-1]
    return link


def sanitize_frontmatter_url(value: str) -> str:
    value = normalize_source_link(value)
    if not value:
        return ""
    match = re.search(r"https?://[^\s，。；、]+", value)
    return normalize_source_link(match.group(0)) if match else value


def extract_source_links(text: str) -> List[str]:
    links: List[str] = []
    for match in re.finditer(r"\((obsidian://[^)\s]+|https?://[^)\s，。；、]+)\)", text):
        links.append(normalize_source_link(match.group(1)))
    for match in re.finditer(r"(?<!\()(?P<url>obsidian://[^\s<>\]]+|https?://[^\s<>\]，。；、]+)", text):
        links.append(normalize_source_link(match.group("url")))
    return dedupe_keep_order(links)


def strip_markdown_links(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\(([^)]+)\)", "", text)
    text = re.sub(r"!\[\[([^\]]+)\]\]", "", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"`{1,3}", "", text)
    return text


def looks_like_bad_capture(text: str) -> bool:
    lowered = text.lower()
    return any(pattern.lower() in lowered for pattern in BAD_CAPTURE_PATTERNS)


def looks_like_blocked_source(text: str) -> bool:
    lowered = text.lower()
    return any(pattern.lower() in lowered for pattern in BLOCKED_SOURCE_PATTERNS)


def looks_like_low_signal_page(text: str, source_domain: str = "") -> bool:
    lowered = text.lower()
    hit_count = sum(1 for pattern in LOW_SIGNAL_PATTERNS if pattern in lowered)
    if source_domain == "github.com" and hit_count >= 2:
        return True
    if "sign in" in lowered and "pricing" in lowered and "support" in lowered:
        return True
    return hit_count >= 4


def parse_datetime_safe(value: str) -> Optional[dt.datetime]:
    if not value:
        return None
    value = value.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def normalize_saved_at(value: str) -> str:
    parsed = parse_datetime_safe(value)
    if not parsed:
        return value.strip()
    if parsed.time() == dt.time(0, 0, 0):
        return parsed.strftime("%Y-%m-%d")
    return parsed.strftime("%Y-%m-%d %H:%M:%S")


def get_domain(url: str, fallback: str = "") -> str:
    if url:
        parsed = urllib.parse.urlparse(url)
        if parsed.netloc:
            return parsed.netloc.lower()
    if fallback and "." in fallback:
        return fallback.lower()
    return ""


def strip_boilerplate_lines(lines: Sequence[str]) -> List[str]:
    cleaned: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            cleaned.append("")
            continue
        if line == "---":
            continue
        if line.startswith("Original "):
            continue
        if any(line.startswith(prefix) for prefix in BOILERPLATE_PREFIXES):
            continue
        if any(fragment in line.lower() for fragment in BOILERPLATE_SUBSTRINGS):
            continue
        if line.startswith("![cover_image]"):
            continue
        if line.startswith("![](") or line.startswith("![缩略图]("):
            continue
        if line.startswith(">"):
            line = line.lstrip("> ").strip()
            if any(fragment in line.lower() for fragment in BOILERPLATE_SUBSTRINGS):
                continue
        if re.fullmatch(r"https?://\S+", line):
            cleaned.append(line)
            continue
        line = re.sub(r"^\*\*描述\*\*:\s*", "", line)
        line = re.sub(r"^地址：\s*", "", line)
        cleaned.append(line)
    text = "\n".join(cleaned)
    text = strip_markdown_links(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.splitlines()


def clean_text_block(text: str) -> str:
    text = strip_markdown_links(text)
    lines = strip_boilerplate_lines(text.splitlines())
    return normalize_whitespace("\n".join(lines))


def detect_doc_shape(title: str, url: str, clean_text: str, bad_capture: bool, preferred: str) -> str:
    if bad_capture:
        return "bad_capture"
    haystack = f"{title} {url}".lower()
    if any(marker in haystack for marker in (".pdf", ".ppt", ".pptx", ".doc", ".docx", ".xls", ".xlsx")):
        return "attachment"
    if preferred == "daily_item":
        return "daily_item"
    return "article"


def detect_capture_status(doc_shape: str, clean_text: str, bad_capture: bool, image_refs: Sequence[str]) -> str:
    if bad_capture:
        return "failed"
    length = len(clean_text)
    if doc_shape == "attachment" and length < 120:
        return "partial"
    if length < 140 and image_refs:
        return "partial"
    if length < 100:
        return "partial"
    return "ok"


def detect_content_kind(
    clean_text: str,
    image_refs: Sequence[str],
    source_links: Sequence[str],
    bad_capture: bool,
) -> str:
    if bad_capture:
        return "bad_capture"
    has_text = len(clean_text) >= 40
    has_images = bool(image_refs)
    has_links = bool(source_links)
    if has_images and not has_text:
        return "image_only"
    if has_links and not has_text:
        return "link_only"
    if has_images or (has_links and len(clean_text) < 220):
        return "mixed"
    return "article"


def initial_source_resolution_status(
    clean_text: str,
    source_links: Sequence[str],
    image_refs: Sequence[str],
    bad_capture: bool,
    min_chars: int,
) -> str:
    if bad_capture:
        return "failed"
    if len(clean_text) >= min_chars:
        return "resolved"
    if clean_text or source_links or image_refs:
        return "partial"
    return "failed"


def extract_sentences(text: str) -> List[str]:
    normalized = normalize_whitespace(text.replace("\n", " "))
    if not normalized:
        return []
    pieces = re.split(r"(?<=[。！？!?；;])\s+|(?<=[。！？!?；;])", normalized)
    sentences = [piece.strip() for piece in pieces if piece.strip()]
    return sentences or [normalized]


def build_summary(text: str, max_chars: int = 220) -> str:
    sentences = extract_sentences(text)
    if not sentences:
        return ""
    buffer: List[str] = []
    total = 0
    for sentence in sentences:
        next_total = total + len(sentence)
        if buffer and next_total > max_chars:
            break
        buffer.append(sentence)
        total = next_total
        if total >= max_chars:
            break
    return normalize_whitespace(" ".join(buffer))[:max_chars]


def compute_quality_score(
    clean_text: str,
    author: str,
    original_url: str,
    capture_status: str,
    doc_shape: str,
    content_kind: str,
    low_signal: bool,
    bad_capture: bool,
) -> float:
    if bad_capture:
        return 0.08
    text_score = min(len(clean_text) / 1200.0, 1.0)
    metadata_score = 0.0
    if author and author.lower() not in {"unknown", "unk", "none"}:
        metadata_score += 0.35
    if original_url:
        metadata_score += 0.35
    status_score = {"ok": 1.0, "partial": 0.55, "failed": 0.1}[capture_status]
    shape_penalty = 0.82 if doc_shape == "attachment" else 1.0
    kind_penalty = {
        "article": 1.0,
        "mixed": 0.93,
        "link_only": 0.78,
        "image_only": 0.7,
        "bad_capture": 0.1,
    }[content_kind]
    low_signal_penalty = 0.28 if low_signal else 1.0
    score = (0.45 * text_score) + (0.25 * metadata_score) + (0.30 * status_score)
    return round(max(0.0, min(score * shape_penalty * kind_penalty * low_signal_penalty, 1.0)), 4)


def auto_topics_for_note(title: str, summary: str, clean_text: str, doc_shape: str) -> List[str]:
    haystack = f"{title}\n{summary}\n{clean_text}".lower()
    scores: Dict[str, int] = collections.defaultdict(int)
    for topic, patterns in TOPIC_RULES:
        for pattern in patterns:
            matches = haystack.count(pattern.lower())
            if matches:
                scores[topic] += matches
    if doc_shape == "attachment":
        scores["skills-tools"] += 1
    ordered = [topic for topic, _score in sorted(scores.items(), key=lambda item: (-item[1], item[0]))]
    if not ordered:
        return ["misc"]
    return ordered[:3]


def stable_section_doc_id(path: pathlib.Path, title: str, url: str, saved_at: str, index: int) -> str:
    return sha1_text(f"{path.resolve()}::{saved_at}::{url}::{title}::{index}")


def parse_single_article_file(path: pathlib.Path, config: Config) -> NormalizedNote:
    raw_text = path.read_text(encoding="utf-8", errors="ignore")
    frontmatter, body = parse_frontmatter(raw_text)
    image_refs = extract_image_refs(raw_text)
    original_url = sanitize_frontmatter_url(str(frontmatter.get("url") or ""))
    author = str(frontmatter.get("author") or "").strip()
    source_hint = str(frontmatter.get("source") or "").strip()
    saved_at = normalize_saved_at(str(frontmatter.get("saved") or ""))
    source_links = dedupe_keep_order(([original_url] if original_url else []) + extract_source_links(raw_text))
    clean_text = clean_text_block(body)
    bad_capture = looks_like_bad_capture(body) or looks_like_bad_capture(clean_text)
    title = path.stem.strip()
    if title.startswith("https---") and original_url:
        title = original_url
    title = normalize_whitespace(title)
    source_domain = get_domain(original_url, fallback=source_hint)
    doc_shape = detect_doc_shape(title, original_url, clean_text, bad_capture, preferred="article")
    capture_status = detect_capture_status(doc_shape, clean_text, bad_capture, image_refs)
    low_signal = looks_like_low_signal_page(clean_text, source_domain)
    if low_signal and capture_status == "ok":
        capture_status = "partial"
    content_kind = detect_content_kind(clean_text, image_refs, source_links, bad_capture)
    summary = build_summary(clean_text or title)
    topics = ["misc"] if low_signal else auto_topics_for_note(title, summary, clean_text, doc_shape)
    quality_score = compute_quality_score(
        clean_text,
        author,
        original_url,
        capture_status,
        doc_shape,
        content_kind,
        low_signal,
        bad_capture,
    )
    obsidian_path = path_in_vault(path, config.vault_root)
    doc_id = sha1_text(f"{path.resolve()}::root::{frontmatter.get('id', '')}")
    initial_status = initial_source_resolution_status(
        clean_text,
        source_links,
        image_refs,
        bad_capture,
        config.research_min_chars,
    )
    return NormalizedNote(
        doc_id=doc_id,
        source_file=str(path.resolve()),
        source_type="article_file",
        title=title,
        author=author or "unknown",
        source_domain=source_domain,
        original_url=original_url,
        saved_at=saved_at,
        doc_shape=doc_shape,
        capture_status=capture_status,
        content_kind=content_kind,
        source_resolution_status=initial_status,
        research_status="queued" if should_trigger_research_stub(content_kind, capture_status, len(clean_text), config.research_min_chars) else "not_needed",
        theme_status="unassigned",
        clean_text=clean_text,
        image_refs=image_refs,
        source_links=source_links,
        auto_topics=topics,
        summary=summary,
        quality_score=quality_score,
        theme_candidate="",
        change_summary="检测到低信息页面，等待进一步富化或重试" if low_signal else "等待富化处理",
        content_hash=sha1_text(raw_text),
        last_seen_at=now_string(),
        last_enriched_at="",
        retry_after="",
        obsidian_path=obsidian_path,
        raw_text_length=len(raw_text),
    )


def split_daily_sections(body: str) -> List[str]:
    sections: List[str] = []
    current: List[str] = []
    for line in body.splitlines():
        if line.strip() == "---":
            chunk = "\n".join(current).strip()
            if chunk:
                sections.append(chunk)
            current = []
            continue
        current.append(line)
    tail = "\n".join(current).strip()
    if tail:
        sections.append(tail)
    return [section for section in sections if "## 📅" in section]


def pick_primary_link(section: str) -> Tuple[str, str]:
    for line in section.splitlines():
        if line.strip().startswith("!"):
            continue
        match = re.search(r"\[([^\]]+)\]\((https?://[^)]+|obsidian://[^)]+)\)", line)
        if match:
            return normalize_whitespace(match.group(1)), normalize_source_link(match.group(2))
    for line in section.splitlines():
        if line.strip().startswith("!"):
            continue
        match = re.search(r"(https?://\S+|obsidian://\S+)", line)
        if match:
            return "", normalize_source_link(match.group(1))
    return "", ""


def parse_daily_item_sections(path: pathlib.Path, config: Config) -> List[NormalizedNote]:
    raw_text = path.read_text(encoding="utf-8", errors="ignore")
    _frontmatter, body = parse_frontmatter(raw_text)
    sections = split_daily_sections(body)
    notes: List[NormalizedNote] = []
    for index, section in enumerate(sections):
        title, primary_link = pick_primary_link(section)
        saved_match = re.search(r"^## 📅 (.+)$", section, re.M)
        saved_at = normalize_saved_at(saved_match.group(1) if saved_match else "")
        title_match = re.search(r"^####\s+(.+)$", section, re.M)
        if not title and title_match:
            title = normalize_whitespace(strip_markdown_links(title_match.group(1)))
        title = title or f"{path.stem} section {index + 1}"
        lines = section.splitlines()
        body_lines: List[str] = []
        seen_timestamp = False
        skipped_primary_link = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("## 📅 "):
                seen_timestamp = True
                continue
            if not seen_timestamp:
                continue
            if not skipped_primary_link and re.search(r"\[([^\]]+)\]\((https?://[^)]+|obsidian://[^)]+)\)", stripped):
                skipped_primary_link = True
                continue
            body_lines.append(line)
        image_refs = extract_image_refs(section)
        source_links = dedupe_keep_order(([primary_link] if primary_link else []) + extract_source_links(section))
        clean_text = clean_text_block("\n".join(body_lines))
        bad_capture = looks_like_bad_capture(section) or looks_like_bad_capture(clean_text)
        doc_shape = detect_doc_shape(title, primary_link, clean_text, bad_capture, preferred="daily_item")
        capture_status = detect_capture_status(doc_shape, clean_text, bad_capture, image_refs)
        low_signal = looks_like_low_signal_page(clean_text, get_domain(primary_link))
        if low_signal and capture_status == "ok":
            capture_status = "partial"
        content_kind = detect_content_kind(clean_text, image_refs, source_links, bad_capture)
        summary = build_summary(clean_text or title)
        topics = ["misc"] if low_signal else auto_topics_for_note(title, summary, clean_text, doc_shape)
        quality_score = compute_quality_score(
            clean_text,
            "",
            primary_link if primary_link.startswith("http") else "",
            capture_status,
            doc_shape,
            content_kind,
            low_signal,
            bad_capture,
        )
        doc_id = stable_section_doc_id(path, title, primary_link, saved_at, index)
        notes.append(
            NormalizedNote(
                doc_id=doc_id,
                source_file=str(path.resolve()),
                source_type="daily_bundle_item",
                title=title,
                author="unknown",
                source_domain=get_domain(primary_link),
                original_url=primary_link if primary_link.startswith("http") else "",
                saved_at=saved_at,
                doc_shape=doc_shape,
                capture_status=capture_status,
                content_kind=content_kind,
                source_resolution_status=initial_source_resolution_status(
                    clean_text,
                    source_links,
                    image_refs,
                    bad_capture,
                    config.research_min_chars,
                ),
                research_status="queued" if should_trigger_research_stub(content_kind, capture_status, len(clean_text), config.research_min_chars) else "not_needed",
                theme_status="unassigned",
                clean_text=clean_text,
                image_refs=image_refs,
                source_links=source_links,
                auto_topics=topics,
                summary=summary,
                quality_score=quality_score,
                theme_candidate="",
                change_summary="检测到低信息页面，等待进一步富化或重试" if low_signal else "等待富化处理",
                content_hash=sha1_text(section),
                last_seen_at=now_string(),
                last_enriched_at="",
                retry_after="",
                obsidian_path=path_in_vault(path, config.vault_root),
                raw_text_length=len(section),
            )
        )
    return notes


def build_notes(config: Config) -> List[NormalizedNote]:
    notes: List[NormalizedNote] = []
    for path in sorted(config.inbox_root.rglob("*.md")):
        if not path.is_file():
            continue
        raw_text = path.read_text(encoding="utf-8", errors="ignore")
        if path.name.startswith("同步助手_") and re.search(r"^## 📅 ", raw_text, re.M):
            notes.extend(parse_daily_item_sections(path, config))
        else:
            notes.append(parse_single_article_file(path, config))
    return notes


def split_paragraph(text: str, heading_path: str, start_offset: int, max_chars: int) -> List[Fragment]:
    if len(text) <= max_chars:
        return [Fragment(heading_path, text, start_offset, start_offset + len(text))]
    sentences = extract_sentences(text)
    if len(sentences) == 1:
        fragments: List[Fragment] = []
        for offset in range(0, len(text), max_chars):
            piece = text[offset: offset + max_chars]
            fragments.append(Fragment(heading_path, piece, start_offset + offset, start_offset + offset + len(piece)))
        return fragments
    fragments = []
    cursor = start_offset
    bucket: List[str] = []
    bucket_start = start_offset
    for sentence in sentences:
        candidate = "".join(bucket) + sentence
        if bucket and len(candidate) > max_chars:
            text_value = "".join(bucket)
            fragments.append(Fragment(heading_path, text_value, bucket_start, bucket_start + len(text_value)))
            cursor = bucket_start + len(text_value)
            bucket = [sentence]
            bucket_start = cursor
        else:
            if not bucket:
                bucket_start = cursor
            bucket.append(sentence)
        cursor += len(sentence)
    if bucket:
        text_value = "".join(bucket)
        fragments.append(Fragment(heading_path, text_value, bucket_start, bucket_start + len(text_value)))
    return fragments


def extract_fragments(note: NormalizedNote, max_chars: int) -> List[Fragment]:
    text = note.clean_text
    if not text:
        return []
    fragments: List[Fragment] = []
    headings: List[str] = [note.title]
    cursor = 0
    for line in text.splitlines(True):
        stripped = line.strip()
        if not stripped:
            cursor += len(line)
            continue
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            headings = headings[: level - 1] + [title]
            cursor += len(line)
            continue
        heading_path = " / ".join([part for part in headings if part])
        line_start = cursor + (len(line) - len(line.lstrip()))
        fragments.extend(split_paragraph(stripped, heading_path, line_start, max_chars))
        cursor += len(line)
    if not fragments:
        fragments.append(Fragment(note.title, text, 0, len(text)))
    return fragments


def build_chunks_for_note(note: NormalizedNote, config: Config) -> List[ChunkRecord]:
    fragments = extract_fragments(note, config.target_max_chars)
    if not fragments:
        return []
    chunks: List[ChunkRecord] = []
    current: List[Fragment] = []
    current_len = 0
    carry_text = ""
    carry_start = 0
    carry_heading = note.title
    for fragment in fragments:
        fragment_len = len(fragment.text)
        if current and current_len + fragment_len > config.target_max_chars and current_len >= config.target_min_chars:
            chunk_text = normalize_whitespace("\n".join(part.text for part in current))
            start_offset = current[0].start_offset
            end_offset = current[-1].end_offset
            chunk_id = sha1_text(f"{note.doc_id}::{len(chunks)}::{start_offset}::{end_offset}")
            chunks.append(
                ChunkRecord(
                    chunk_id=chunk_id,
                    doc_id=note.doc_id,
                    heading_path=current[-1].heading_path,
                    chunk_text=chunk_text,
                    start_offset=start_offset,
                    end_offset=end_offset,
                    rank_features={},
                )
            )
            carry_text = chunk_text[-config.overlap_chars:] if config.overlap_chars else ""
            carry_start = max(start_offset, end_offset - len(carry_text))
            carry_heading = current[-1].heading_path
            current = []
            current_len = 0
            if carry_text:
                current.append(Fragment(carry_heading, carry_text, carry_start, end_offset))
                current_len = len(carry_text)
        current.append(fragment)
        current_len += fragment_len
    if current:
        chunk_text = normalize_whitespace("\n".join(part.text for part in current))
        start_offset = current[0].start_offset
        end_offset = current[-1].end_offset
        chunk_id = sha1_text(f"{note.doc_id}::{len(chunks)}::{start_offset}::{end_offset}")
        chunks.append(
            ChunkRecord(
                chunk_id=chunk_id,
                doc_id=note.doc_id,
                heading_path=current[-1].heading_path,
                chunk_text=chunk_text,
                start_offset=start_offset,
                end_offset=end_offset,
                rank_features={},
            )
        )
    for chunk in chunks:
        chunk.rank_features = {
            "quality_score": note.quality_score,
            "doc_shape": note.doc_shape,
            "capture_status": note.capture_status,
            "content_kind": note.content_kind,
            "source_resolution_status": note.source_resolution_status,
            "research_status": note.research_status,
            "theme_status": note.theme_status,
            "theme_candidate": note.theme_candidate,
            "topics": note.auto_topics,
            "source_domain": note.source_domain,
            "saved_at": note.saved_at,
            "text_length": len(chunk.chunk_text),
        }
    return chunks


def build_chunks(notes: Sequence[NormalizedNote], config: Config) -> List[ChunkRecord]:
    chunks: List[ChunkRecord] = []
    for note in notes:
        if note.research_status == "needs_manual_access" and not note.clean_text:
            continue
        chunks.extend(build_chunks_for_note(note, config))
    return chunks


def tokenize_for_vector(text: str) -> List[str]:
    lowered = text.lower()
    terms: List[str] = []
    for token in re.findall(r"[a-z0-9][a-z0-9\-\._/]{1,}", lowered):
        terms.append(token)
    for block in re.findall(r"[\u4e00-\u9fff]{2,}", lowered):
        if len(block) <= 3:
            terms.append(block)
        else:
            for index in range(len(block) - 1):
                terms.append(block[index:index + 2])
            for index in range(len(block) - 2):
                terms.append(block[index:index + 3])
    return terms


def build_vector_index(chunks: Sequence[ChunkRecord]) -> Dict[str, Any]:
    chunk_terms: Dict[str, collections.Counter] = {}
    df_counter: collections.Counter = collections.Counter()
    for chunk in chunks:
        tokens = tokenize_for_vector(chunk.chunk_text)
        counter = collections.Counter(tokens)
        chunk_terms[chunk.chunk_id] = counter
        for token in counter:
            df_counter[token] += 1
    total_docs = max(len(chunks), 1)
    chunk_vectors: Dict[str, Dict[str, Any]] = {}
    for chunk in chunks:
        counter = chunk_terms[chunk.chunk_id]
        weights: Dict[str, float] = {}
        norm_sq = 0.0
        for token, count in counter.items():
            idf = math.log((1 + total_docs) / (1 + df_counter[token])) + 1.0
            weight = (1.0 + math.log(count)) * idf
            weights[token] = round(weight, 6)
            norm_sq += weight * weight
        chunk_vectors[chunk.chunk_id] = {
            "norm": round(math.sqrt(norm_sq), 6),
            "weights": weights,
        }
    return {
        "total_chunks": total_docs,
        "doc_freq": dict(df_counter),
        "chunks": chunk_vectors,
    }


def vector_query_scores(query: str, vector_index: Dict[str, Any]) -> Dict[str, float]:
    tokens = tokenize_for_vector(query)
    if not tokens:
        return {}
    counter = collections.Counter(tokens)
    total_chunks = max(int(vector_index.get("total_chunks", 1)), 1)
    doc_freq = vector_index.get("doc_freq", {})
    query_weights: Dict[str, float] = {}
    norm_sq = 0.0
    for token, count in counter.items():
        idf = math.log((1 + total_chunks) / (1 + int(doc_freq.get(token, 0)))) + 1.0
        weight = (1.0 + math.log(count)) * idf
        query_weights[token] = weight
        norm_sq += weight * weight
    if norm_sq == 0.0:
        return {}
    query_norm = math.sqrt(norm_sq)
    scores: Dict[str, float] = {}
    for chunk_id, payload in vector_index.get("chunks", {}).items():
        chunk_norm = float(payload.get("norm", 0.0))
        if chunk_norm <= 0:
            continue
        weights = payload.get("weights", {})
        dot = 0.0
        for token, q_weight in query_weights.items():
            chunk_weight = weights.get(token)
            if chunk_weight is not None:
                dot += q_weight * float(chunk_weight)
        if dot > 0:
            scores[chunk_id] = dot / (query_norm * chunk_norm)
    return scores


def write_jsonl(path: pathlib.Path, records: Sequence[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_jsonl(path: pathlib.Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def load_vector_index(path: pathlib.Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_vector_index(path: pathlib.Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def build_sqlite_index(notes: Sequence[NormalizedNote], chunks: Sequence[ChunkRecord], db_path: pathlib.Path) -> None:
    if db_path.exists():
        db_path.unlink()
    connection = sqlite3.connect(str(db_path))
    try:
        connection.execute(
            """
            create table docs (
                doc_id text primary key,
                source_file text not null,
                source_type text not null,
                title text not null,
                author text not null,
                source_domain text not null,
                original_url text not null,
                saved_at text not null,
                doc_shape text not null,
                capture_status text not null,
                content_kind text not null,
                source_resolution_status text not null,
                research_status text not null,
                theme_status text not null,
                clean_text text not null,
                image_refs_json text not null,
                source_links_json text not null,
                auto_topics_json text not null,
                summary text not null,
                quality_score real not null,
                theme_candidate text not null,
                change_summary text not null,
                content_hash text not null,
                last_seen_at text not null,
                last_enriched_at text not null,
                retry_after text not null,
                obsidian_path text not null,
                raw_text_length integer not null
            )
            """
        )
        connection.execute(
            """
            create table chunks (
                chunk_id text primary key,
                doc_id text not null,
                heading_path text not null,
                chunk_text text not null,
                start_offset integer not null,
                end_offset integer not null,
                rank_features_json text not null
            )
            """
        )
        connection.execute(
            """
            create virtual table chunk_fts using fts5(
                chunk_id unindexed,
                doc_id unindexed,
                title,
                summary,
                chunk_text,
                tokenize='trigram'
            )
            """
        )
        connection.executemany(
            """
            insert into docs (
                doc_id, source_file, source_type, title, author, source_domain, original_url, saved_at,
                doc_shape, capture_status, content_kind, source_resolution_status, research_status, theme_status,
                clean_text, image_refs_json, source_links_json, auto_topics_json, summary, quality_score,
                theme_candidate, change_summary, content_hash, last_seen_at, last_enriched_at, retry_after,
                obsidian_path, raw_text_length
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    note.doc_id,
                    note.source_file,
                    note.source_type,
                    note.title,
                    note.author,
                    note.source_domain,
                    note.original_url,
                    note.saved_at,
                    note.doc_shape,
                    note.capture_status,
                    note.content_kind,
                    note.source_resolution_status,
                    note.research_status,
                    note.theme_status,
                    note.clean_text,
                    json.dumps(note.image_refs, ensure_ascii=False),
                    json.dumps(note.source_links, ensure_ascii=False),
                    json.dumps(note.auto_topics, ensure_ascii=False),
                    note.summary,
                    note.quality_score,
                    note.theme_candidate,
                    note.change_summary,
                    note.content_hash,
                    note.last_seen_at,
                    note.last_enriched_at,
                    note.retry_after,
                    note.obsidian_path,
                    note.raw_text_length,
                )
                for note in notes
            ],
        )
        note_map = {note.doc_id: note for note in notes}
        connection.executemany(
            """
            insert into chunks (
                chunk_id, doc_id, heading_path, chunk_text, start_offset, end_offset, rank_features_json
            ) values (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    chunk.chunk_id,
                    chunk.doc_id,
                    chunk.heading_path,
                    chunk.chunk_text,
                    chunk.start_offset,
                    chunk.end_offset,
                    json.dumps(chunk.rank_features, ensure_ascii=False),
                )
                for chunk in chunks
            ],
        )
        connection.executemany(
            """
            insert into chunk_fts (chunk_id, doc_id, title, summary, chunk_text)
            values (?, ?, ?, ?, ?)
            """,
            [
                (
                    chunk.chunk_id,
                    chunk.doc_id,
                    note_map[chunk.doc_id].title,
                    note_map[chunk.doc_id].summary,
                    chunk.chunk_text,
                )
                for chunk in chunks
            ],
        )
        connection.commit()
    finally:
        connection.close()


def read_manual_stars(config: Config) -> Dict[str, Dict[str, str]]:
    path = config.state_root / "manual_stars.json"
    if not path.exists():
        return {"docs": {}, "topics": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def write_manual_stars(config: Config, payload: Dict[str, Dict[str, str]]) -> None:
    path = config.state_root / "manual_stars.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_scan_state(config: Config) -> Dict[str, Any]:
    path = config.state_root / "scan_state.json"
    if not path.exists():
        return {"docs": {}, "last_full_scan_at": ""}
    return json.loads(path.read_text(encoding="utf-8"))


def write_scan_state(config: Config, payload: Dict[str, Any]) -> None:
    path = config.state_root / "scan_state.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_query_history(config: Config, query: str, result: Dict[str, Any]) -> None:
    path = config.state_root / "query_history.jsonl"
    record = {
        "timestamp": now_string(),
        "query": query,
        "confidence": result.get("confidence", 0.0),
        "top_docs": [note["doc_id"] for note in result.get("related_notes", []) if note.get("doc_id")],
        "topics": dedupe_keep_order(
            topic
            for note in result.get("related_notes", [])
            for topic in note.get("topics", [])
        ),
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_query_history(config: Config) -> List[Dict[str, Any]]:
    return load_jsonl(config.state_root / "query_history.jsonl")


def build_fts_query(query: str) -> str:
    query = normalize_whitespace(query.replace('"', " "))
    if len(query) >= 3:
        return f'"{query}"'
    tokens = dedupe_keep_order(token for token in tokenize_for_vector(query) if len(token) >= 2)
    return " OR ".join(f'"{token}"' for token in tokens[:8])


def load_notes_and_chunks(config: Config) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    notes = load_jsonl(config.artifacts_root / "normalized_docs.jsonl")
    chunks = load_jsonl(config.artifacts_root / "chunks.jsonl")
    vector_index = load_vector_index(config.artifacts_root / "vector_index.json")
    if not notes or not chunks:
        raise FileNotFoundError("index artifacts missing; run build-index first")
    return notes, chunks, vector_index


def load_topic_cards(config: Config) -> List[Dict[str, Any]]:
    return load_jsonl(config.artifacts_root / "topic_cards.jsonl")


def load_enriched_notes(config: Config) -> List[Dict[str, Any]]:
    return load_jsonl(config.artifacts_root / "enriched_notes.jsonl")


def load_topic_update_logs(config: Config) -> List[Dict[str, Any]]:
    return load_jsonl(config.artifacts_root / "topic_update_logs.jsonl")


def load_daily_digests(config: Config) -> List[Dict[str, Any]]:
    return load_jsonl(config.artifacts_root / "daily_change_digests.jsonl")


def should_trigger_research_stub(content_kind: str, capture_status: str, text_len: int, min_chars: int) -> bool:
    return content_kind in {"link_only", "image_only", "mixed", "bad_capture"} or capture_status != "ok" or text_len < min_chars


def should_trigger_research(note: NormalizedNote, config: Config) -> bool:
    return should_trigger_research_stub(
        note.content_kind,
        note.capture_status,
        len(note.clean_text),
        config.research_min_chars,
    )


def is_retry_due(retry_after: str) -> bool:
    retry_dt = parse_datetime_safe(retry_after)
    if not retry_dt:
        return True
    return retry_dt <= dt.datetime.now()


def is_full_rescan_due(last_full_scan_at: str, full_rescan_days: int) -> bool:
    last = parse_datetime_safe(last_full_scan_at)
    if not last:
        return True
    return (dt.datetime.now() - last) >= dt.timedelta(days=full_rescan_days)


def html_to_text(raw_html: str) -> str:
    raw_html = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", raw_html)
    raw_html = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", raw_html)
    raw_html = re.sub(r"(?is)<noscript[^>]*>.*?</noscript>", " ", raw_html)
    raw_html = re.sub(r"(?i)<br\s*/?>", "\n", raw_html)
    raw_html = re.sub(r"(?i)</(p|div|section|article|h1|h2|h3|h4|h5|h6|li|tr|ul|ol)>", "\n", raw_html)
    raw_html = re.sub(r"(?is)<[^>]+>", " ", raw_html)
    return normalize_whitespace(html.unescape(raw_html))


def decode_response_bytes(raw: bytes, charset: str = "") -> str:
    tried = [charset, "utf-8", "utf-8-sig", "gb18030", "latin-1"]
    for encoding in tried:
        if not encoding:
            continue
        try:
            return raw.decode(encoding, errors="ignore")
        except LookupError:
            continue
    return raw.decode("utf-8", errors="ignore")


def fetch_web_document(url: str, config: Config) -> Dict[str, Any]:
    if not config.enable_network:
        return {"status": "failed", "url": url, "text": "", "error": "network disabled"}
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,text/plain,application/json;q=0.8,*/*;q=0.5",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=config.network_timeout) as response:
            raw = response.read(250000)
            content_type = response.headers.get("Content-Type", "")
            charset = response.headers.get_content_charset() or ""
            final_url = response.geturl()
    except urllib.error.HTTPError as exc:
        raw = exc.read(120000)
        content_type = exc.headers.get("Content-Type", "") if exc.headers else ""
        charset = exc.headers.get_content_charset() if exc.headers else ""
        text = decode_response_bytes(raw, charset or "")
        clean = clean_text_block(html_to_text(text) if "html" in content_type.lower() else text)
        blocked = looks_like_blocked_source(clean)
        low_signal = looks_like_low_signal_page(clean, get_domain(url))
        return {
            "status": "blocked" if blocked else ("partial" if low_signal and clean else "failed"),
            "url": url,
            "final_url": url,
            "text": clean,
            "title": "",
            "content_type": content_type,
            "error": f"http {exc.code}",
            "low_signal": low_signal,
        }
    except Exception as exc:
        return {"status": "failed", "url": url, "final_url": url, "text": "", "title": "", "content_type": "", "error": str(exc), "low_signal": False}
    text = decode_response_bytes(raw, charset or "")
    is_html = "html" in content_type.lower() or "<html" in text.lower()
    clean = clean_text_block(html_to_text(text) if is_html else text)
    blocked = looks_like_blocked_source(clean)
    low_signal = looks_like_low_signal_page(clean, get_domain(final_url))
    status = "blocked" if blocked else ("partial" if low_signal and clean else ("ok" if clean else "failed"))
    title_match = re.search(r"(?is)<title>(.*?)</title>", text)
    return {
        "status": status,
        "url": url,
        "final_url": final_url,
        "text": clean,
        "title": normalize_whitespace(html.unescape(title_match.group(1))) if title_match else "",
        "content_type": content_type,
        "error": "",
        "low_signal": low_signal,
    }


def resolve_obsidian_uri_to_path(uri: str, vault_root: pathlib.Path) -> Optional[pathlib.Path]:
    parsed = urllib.parse.urlparse(uri)
    if parsed.scheme != "obsidian":
        return None
    query = urllib.parse.parse_qs(parsed.query)
    raw_file = (query.get("file") or [""])[0]
    if not raw_file:
        return None
    relative = pathlib.Path(urllib.parse.unquote(raw_file))
    if relative.suffix == "":
        relative = relative.with_suffix(".md")
    path = (vault_root / relative).resolve()
    try:
        path.relative_to(vault_root.resolve())
    except ValueError:
        return None
    return path if path.exists() else None


def load_local_source(path: pathlib.Path, vault_root: pathlib.Path) -> Dict[str, Any]:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    frontmatter, body = parse_frontmatter(raw)
    clean = clean_text_block(body or raw)
    low_signal = looks_like_low_signal_page(clean, get_domain(str(frontmatter.get("url") or "")))
    return {
        "status": "partial" if low_signal and clean else ("ok" if clean else "failed"),
        "file_path": str(path.resolve()),
        "obsidian_path": path_in_vault(path, vault_root),
        "url": sanitize_frontmatter_url(str(frontmatter.get("url") or "")),
        "text": clean,
        "title": normalize_whitespace(path.stem),
        "low_signal": low_signal,
    }


def search_public_sources(query: str, preferred_domain: str, config: Config) -> List[str]:
    if not config.enable_network or not query.strip():
        return []
    final_query = normalize_whitespace(query)
    if preferred_domain:
        final_query = f"{final_query} site:{preferred_domain}"
    url = "https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": final_query})
    result = fetch_web_document(url, config)
    if result.get("status") != "ok" or not result.get("text"):
        return []
    raw_html = result.get("text", "")
    urls: List[str] = []
    # `fetch_web_document` strips HTML tags, so query search separately using raw download.
    request = urllib.request.Request(url, headers={"User-Agent": DEFAULT_USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=config.network_timeout) as response:
            html_text = decode_response_bytes(response.read(250000), response.headers.get_content_charset() or "")
    except Exception:
        return []
    for match in re.finditer(r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"', html_text):
        link = html.unescape(match.group(1))
        parsed = urllib.parse.urlparse(link)
        if parsed.netloc.endswith("duckduckgo.com"):
            target = urllib.parse.parse_qs(parsed.query).get("uddg", [""])[0]
            link = urllib.parse.unquote(target) if target else link
        link = normalize_source_link(link)
        if link.startswith("http"):
            urls.append(link)
    return dedupe_keep_order(urls)[: config.max_external_sources]


def build_search_query(note: NormalizedNote) -> str:
    title = normalize_whitespace(strip_markdown_links(note.title))
    normalized_title = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "", title).lower()
    generic = {"docs", "docs2", "消息", "内容创作", "message", "opencla", "claudecod"}
    if normalized_title and normalized_title not in generic and len(normalized_title) >= 5:
        return title
    if len(note.summary) >= 10:
        return note.summary[:80]
    if len(note.clean_text) >= 20:
        return build_summary(note.clean_text, max_chars=80)
    return ""


def source_candidates_for_note(note: NormalizedNote, vault_root: pathlib.Path) -> List[Dict[str, str]]:
    candidates: List[Dict[str, str]] = []
    seen = set()
    for link in dedupe_keep_order(([note.original_url] if note.original_url else []) + note.source_links):
        if not link or link in seen:
            continue
        seen.add(link)
        if link.startswith("obsidian://"):
            resolved = resolve_obsidian_uri_to_path(link, vault_root)
            if resolved:
                candidates.append({"kind": "obsidian_note", "value": str(resolved.resolve()), "raw": link})
            else:
                candidates.append({"kind": "obsidian_note", "value": "", "raw": link})
        elif link.startswith("http"):
            kind = "source_url" if link == note.original_url else "embedded_url"
            candidates.append({"kind": kind, "value": link, "raw": link})
    return candidates


def evidence_excerpt(text: str, max_chars: int = 260) -> str:
    return build_summary(text, max_chars=max_chars) or normalize_whitespace(text)[:max_chars]


def candidate_label_from_note(note: NormalizedNote, enriched_text: str = "") -> str:
    if any(topic != "misc" for topic in note.auto_topics):
        return next(topic for topic in note.auto_topics if topic != "misc")
    candidate = note.title.strip()
    if candidate.lower().startswith("https://") or candidate.lower().startswith("http://"):
        candidate = note.summary or note.clean_text[:30]
    candidate = re.sub(r"\s+", " ", strip_markdown_links(candidate))
    candidate = re.sub(r"[|｜:：\-—_]+$", "", candidate).strip()
    if candidate.lower() in {"docs", "docs 2", "message", "消息", "内容创作"} or len(candidate) < 4:
        candidate = note.summary or build_summary(enriched_text or note.clean_text, max_chars=18)
    candidate = normalize_whitespace(candidate)
    return candidate[:24] or "候选主题"


def combine_texts_for_summary(note: NormalizedNote, evidence: Sequence[Dict[str, Any]]) -> str:
    parts = [note.clean_text]
    parts.extend(item.get("full_text", "") for item in evidence if item.get("status") == "ok")
    return normalize_whitespace("\n\n".join(part for part in parts if part))


def build_key_findings(note: NormalizedNote, evidence: Sequence[Dict[str, Any]], limit: int = 4) -> List[str]:
    candidates = [{"excerpt": note.summary or note.clean_text[:220], "score": note.quality_score}]
    candidates.extend(
        {
            "excerpt": item.get("excerpt", ""),
            "score": 0.7 if item.get("type") != "public_search" else 0.55,
        }
        for item in evidence
        if item.get("excerpt")
    )
    return choose_summary_sentences(candidates, note.title, limit=limit)


def build_gaps(note: NormalizedNote, blocked_count: int, usable_count: int, need_research: bool) -> List[str]:
    gaps: List[str] = []
    if note.content_kind == "image_only":
        gaps.append("原始材料只有图片，没有执行 OCR 或视觉推断。")
    if note.doc_shape == "bad_capture":
        gaps.append("原始抓取内容是反爬或校验页。")
    if blocked_count:
        gaps.append("源链接受权限或登录限制，当前无法完整读取。")
    if need_research and usable_count == 0 and len(note.clean_text) < 80:
        gaps.append("缺少足够的一手正文，结论只能等待补读或补权限。")
    return dedupe_keep_order(gaps)


def update_change_summary(
    note: NormalizedNote,
    previous_note: Optional[Dict[str, Any]],
    previous_enriched: Optional[Dict[str, Any]],
    new_enriched: EnrichedNote,
) -> str:
    if not previous_note or not previous_enriched:
        return "首次进入知识库并完成富化处理"
    if previous_note.get("content_hash") != note.content_hash:
        return "原始内容有变更，已重新整理并更新研究结果"
    if previous_enriched.get("research_status") != new_enriched.research_status:
        return f"研究状态从 {previous_enriched.get('research_status', 'unknown')} 更新为 {new_enriched.research_status}"
    if previous_enriched.get("theme_candidate") != new_enriched.theme_candidate:
        return "主题归并结果已更新"
    if previous_enriched.get("research_summary") != new_enriched.research_summary:
        return "补充了新证据并更新研究摘要"
    return "复用已有富化结果"


def enrich_note(
    note: NormalizedNote,
    config: Config,
    previous_note: Optional[Dict[str, Any]] = None,
    previous_enriched: Optional[Dict[str, Any]] = None,
) -> Tuple[NormalizedNote, EnrichedNote]:
    note = dataclasses.replace(note)
    now = now_string()
    need_research = should_trigger_research(note, config)
    evidence: List[Dict[str, Any]] = []
    used_values = set()
    blocked_count = 0
    usable_count = 0

    note_low_signal = looks_like_low_signal_page(note.clean_text, note.source_domain)
    if note.clean_text:
        evidence.append(
            {
                "type": "local_note",
                "title": note.title,
                "file_path": note.source_file,
                "obsidian_path": note.obsidian_path,
                "url": note.original_url,
                "excerpt": evidence_excerpt(note.clean_text),
                "full_text": note.clean_text,
                "status": "partial" if note_low_signal else "ok",
                "source_domain": note.source_domain,
            }
        )
        if not note_low_signal:
            usable_count += 1

    if need_research:
        for candidate in source_candidates_for_note(note, config.vault_root):
            candidate_key = f"{candidate['kind']}::{candidate['value']}::{candidate.get('raw', '')}"
            if candidate_key in used_values:
                continue
            used_values.add(candidate_key)
            if candidate["kind"] == "obsidian_note":
                if not candidate["value"]:
                    evidence.append(
                        {
                            "type": "obsidian_note",
                            "title": note.title,
                            "file_path": "",
                            "obsidian_path": "",
                            "url": candidate.get("raw", ""),
                            "excerpt": "Obsidian 链接无法解析到本地文件",
                            "full_text": "",
                            "status": "failed",
                            "source_domain": "",
                        }
                    )
                    continue
                local_path = pathlib.Path(candidate["value"])
                if str(local_path.resolve()) == note.source_file:
                    continue
                local_source = load_local_source(local_path, config.vault_root)
                evidence.append(
                    {
                        "type": "obsidian_note",
                        "title": local_source["title"],
                        "file_path": local_source["file_path"],
                        "obsidian_path": local_source["obsidian_path"],
                        "url": local_source["url"],
                        "excerpt": evidence_excerpt(local_source["text"]),
                        "full_text": local_source["text"],
                        "status": local_source["status"],
                        "source_domain": get_domain(local_source["url"]),
                    }
                )
                if local_source["status"] == "ok" and local_source["text"]:
                    usable_count += 1
            else:
                fetched = fetch_web_document(candidate["value"], config)
                evidence.append(
                    {
                        "type": candidate["kind"],
                        "title": fetched.get("title", "") or note.title,
                        "file_path": "",
                        "obsidian_path": "",
                        "url": fetched.get("final_url", "") or candidate["value"],
                        "excerpt": evidence_excerpt(fetched.get("text", "")),
                        "full_text": fetched.get("text", ""),
                        "status": fetched.get("status", "failed"),
                        "source_domain": get_domain(fetched.get("final_url", "") or candidate["value"]),
                        "error": fetched.get("error", ""),
                    }
                )
                if fetched.get("status") == "blocked":
                    blocked_count += 1
                if fetched.get("status") == "ok" and fetched.get("text"):
                    usable_count += 1
            if usable_count >= max(2, config.max_external_sources):
                break

        combined_text = combine_texts_for_summary(note, evidence)
        if config.enable_network and len(combined_text) < config.research_min_chars:
            search_query = build_search_query(note)
            if search_query:
                for url in search_public_sources(search_query, note.source_domain, config):
                    if url in used_values or url == note.original_url:
                        continue
                    fetched = fetch_web_document(url, config)
                    evidence.append(
                        {
                            "type": "public_search",
                            "title": fetched.get("title", "") or search_query,
                            "file_path": "",
                            "obsidian_path": "",
                            "url": fetched.get("final_url", "") or url,
                            "excerpt": evidence_excerpt(fetched.get("text", "")),
                            "full_text": fetched.get("text", ""),
                            "status": fetched.get("status", "failed"),
                            "source_domain": get_domain(fetched.get("final_url", "") or url),
                            "error": fetched.get("error", ""),
                        }
                    )
                    used_values.add(url)
                    if fetched.get("status") == "blocked":
                        blocked_count += 1
                    if fetched.get("status") == "ok" and fetched.get("text"):
                        usable_count += 1
                    if usable_count >= max(2, config.max_external_sources):
                        break

    combined_text = combine_texts_for_summary(note, evidence)
    stable_text = normalize_whitespace("\n\n".join(item.get("full_text", "") for item in evidence if item.get("status") == "ok"))
    theme_candidate = candidate_label_from_note(note, combined_text)
    key_findings = build_key_findings(note, evidence)
    research_summary = build_summary(combined_text or note.summary or note.title, max_chars=320)
    if not research_summary:
        research_summary = note.summary or note.title

    if not need_research and len(note.clean_text) >= config.research_min_chars:
        source_resolution_status = "resolved"
        research_status = "not_needed"
    elif blocked_count and usable_count <= 1 and len(note.clean_text) < config.research_min_chars:
        source_resolution_status = "blocked"
        research_status = "needs_manual_access"
    elif usable_count >= 2 or len(stable_text) >= config.research_min_chars:
        source_resolution_status = "resolved"
        research_status = "enriched"
    elif note.clean_text or note.source_links or note.image_refs:
        source_resolution_status = "partial"
        research_status = "needs_retry"
    else:
        source_resolution_status = "failed"
        research_status = "needs_retry"

    note.source_resolution_status = source_resolution_status
    note.research_status = research_status
    note.theme_candidate = theme_candidate
    note.theme_status = "candidate_topic" if theme_candidate not in TOPIC_DISPLAY_NAMES else "existing_topic"
    note.last_enriched_at = now
    note.retry_after = (
        (dt.datetime.now() + dt.timedelta(days=config.full_rescan_days)).strftime("%Y-%m-%d %H:%M:%S")
        if research_status == "needs_retry"
        else ""
    )
    note.change_summary = update_change_summary(
        note,
        previous_note,
        previous_enriched,
        EnrichedNote(
            doc_id=note.doc_id,
            theme_candidate=theme_candidate,
            research_summary=research_summary,
            key_findings=key_findings,
            source_evidence=[],
            confidence=0.0,
            gaps=[],
            research_status=research_status,
            updated_at=now,
        ),
    )
    gaps = build_gaps(note, blocked_count, usable_count, need_research)
    confidence_base = 0.28 + (0.12 * min(usable_count, 3)) + (0.18 * min(note.quality_score, 1.0))
    if research_status == "needs_manual_access":
        confidence = 0.22
    elif research_status == "needs_retry":
        confidence = min(0.48, confidence_base)
    elif research_status == "not_needed":
        confidence = min(0.88, 0.5 + (0.25 * note.quality_score))
    else:
        confidence = min(0.94, confidence_base + 0.16)
    enriched = EnrichedNote(
        doc_id=note.doc_id,
        theme_candidate=theme_candidate,
        research_summary=research_summary,
        key_findings=key_findings,
        source_evidence=[
            {
                "type": item.get("type", ""),
                "title": item.get("title", ""),
                "file_path": item.get("file_path", ""),
                "obsidian_path": item.get("obsidian_path", ""),
                "url": item.get("url", ""),
                "excerpt": item.get("excerpt", ""),
                "status": item.get("status", ""),
                "source_domain": item.get("source_domain", ""),
                "error": item.get("error", ""),
            }
            for item in evidence
        ],
        confidence=round(confidence, 4),
        gaps=gaps,
        research_status=research_status,
        updated_at=now,
    )
    note.change_summary = update_change_summary(note, previous_note, previous_enriched, enriched)
    return note, enriched


def enrich_notes(
    notes: Sequence[NormalizedNote],
    config: Config,
    force_full_rescan: bool = False,
) -> Tuple[List[NormalizedNote], List[EnrichedNote], Dict[str, Any]]:
    previous_state = load_scan_state(config)
    previous_enriched_map = {
        item["doc_id"]: item
        for item in load_enriched_notes(config)
    }
    now = now_string()
    full_rescan_due = force_full_rescan or is_full_rescan_due(
        previous_state.get("last_full_scan_at", ""),
        config.full_rescan_days,
    )
    updated_notes: List[NormalizedNote] = []
    enriched_notes: List[EnrichedNote] = []
    next_state = {"docs": {}, "last_full_scan_at": now if full_rescan_due else previous_state.get("last_full_scan_at", "")}
    counts = collections.Counter()

    for note in notes:
        previous_note = previous_state.get("docs", {}).get(note.doc_id)
        previous_enriched = previous_enriched_map.get(note.doc_id)
        changed = previous_note is None or previous_note.get("content_hash") != note.content_hash
        retry_due = bool(previous_note and previous_note.get("research_status") == "needs_retry" and is_retry_due(previous_note.get("retry_after", "")))
        manual_review_due = bool(previous_note and previous_note.get("research_status") == "needs_manual_access" and full_rescan_due)
        needs_processing = changed or retry_due or full_rescan_due or manual_review_due or previous_enriched is None

        if previous_note and not changed and not needs_processing:
            note.source_resolution_status = previous_note.get("source_resolution_status", note.source_resolution_status)
            note.research_status = previous_note.get("research_status", note.research_status)
            note.theme_status = previous_note.get("theme_status", note.theme_status)
            note.theme_candidate = previous_note.get("theme_candidate", "")
            note.last_enriched_at = previous_note.get("last_enriched_at", "")
            note.retry_after = previous_note.get("retry_after", "")
            note.change_summary = "复用上次富化结果"
            if previous_enriched:
                enriched_notes.append(EnrichedNote.from_record(previous_enriched))
            counts["unchanged_doc_count"] += 1
        else:
            note, enriched = enrich_note(note, config, previous_note=previous_note, previous_enriched=previous_enriched)
            enriched_notes.append(enriched)
            if previous_note is None:
                counts["new_doc_count"] += 1
            elif changed:
                counts["updated_doc_count"] += 1
            else:
                counts["retried_doc_count"] += 1
            if note.research_status == "needs_manual_access":
                counts["needs_manual_access_count"] += 1
            if note.research_status == "needs_retry":
                counts["needs_retry_count"] += 1
            if note.capture_status == "failed" or note.source_resolution_status == "failed":
                counts["failed_doc_count"] += 1
        updated_notes.append(note)
        next_state["docs"][note.doc_id] = {
            "doc_id": note.doc_id,
            "source_file": note.source_file,
            "content_hash": note.content_hash,
            "source_resolution_status": note.source_resolution_status,
            "research_status": note.research_status,
            "theme_status": note.theme_status,
            "theme_candidate": note.theme_candidate,
            "last_enriched_at": note.last_enriched_at,
            "retry_after": note.retry_after,
            "obsidian_path": note.obsidian_path,
        }

    write_scan_state(config, next_state)
    counts.setdefault("new_doc_count", 0)
    counts.setdefault("updated_doc_count", 0)
    counts.setdefault("retried_doc_count", 0)
    counts.setdefault("unchanged_doc_count", 0)
    counts.setdefault("failed_doc_count", 0)
    counts.setdefault("needs_manual_access_count", 0)
    counts.setdefault("needs_retry_count", 0)
    counts["full_rescan_due"] = full_rescan_due
    counts["processed_doc_count"] = (
        counts["new_doc_count"] + counts["updated_doc_count"] + counts["retried_doc_count"]
    )
    return updated_notes, enriched_notes, dict(counts)


def query_hits_by_topic(history: Sequence[Dict[str, Any]]) -> Dict[str, int]:
    counter: Dict[str, int] = collections.Counter()
    for item in history:
        for topic in item.get("topics", []):
            counter[topic] += 1
    return dict(counter)


def normalize_topic_title(topic: str) -> str:
    return TOPIC_DISPLAY_NAMES.get(topic, topic)


def key_points_from_related_docs(
    related_docs: Sequence[Dict[str, Any]],
    enriched_map: Dict[str, Dict[str, Any]],
    topic_title: str,
) -> List[str]:
    items: List[Dict[str, Any]] = []
    for doc in related_docs[:8]:
        enriched = enriched_map.get(doc["doc_id"])
        if enriched and enriched.get("research_summary"):
            items.append({"excerpt": enriched["research_summary"], "score": enriched.get("confidence", 0.6)})
            for finding in enriched.get("key_findings", [])[:3]:
                items.append({"excerpt": finding, "score": enriched.get("confidence", 0.6)})
        else:
            items.append({"excerpt": doc.get("summary") or doc.get("clean_text", "")[:220], "score": doc.get("quality_score", 0.5)})
    return choose_summary_sentences(items, topic_title, limit=4)


def topic_card_payload(
    topic: str,
    topic_title: str,
    summary: str,
    related_docs: Sequence[Dict[str, Any]],
    theme_kind: str,
    change_count: int,
    last_updated_at: str,
    absolute_file_path: pathlib.Path,
    obsidian_path: str,
    key_points: Sequence[str],
) -> Dict[str, Any]:
    return {
        "topic": topic,
        "display_title": topic_title,
        "title": f"{topic_title} 主题卡片",
        "theme_kind": theme_kind,
        "one_paragraph_summary": summary,
        "key_points": list(key_points),
        "related_docs": [doc["doc_id"] for doc in related_docs],
        "related_doc_paths": [doc["obsidian_path"] for doc in related_docs],
        "open_questions": OPEN_QUESTIONS.get(topic, OPEN_QUESTIONS["misc"]),
        "source_file": str(absolute_file_path.resolve()),
        "obsidian_path": obsidian_path,
        "summary": summary,
        "original_url": "",
        "saved_at": last_updated_at,
        "last_updated_at": last_updated_at,
        "change_count": change_count,
        "auto_topics": [topic] if topic in TOPIC_DISPLAY_NAMES else [],
        "source_scope": "笔记同步助手",
    }


def render_topic_card(card: Dict[str, Any], related_docs: Sequence[Dict[str, Any]]) -> str:
    related_block = "\n".join(
        f"- [[{doc['obsidian_path'].replace('.md', '')}]] | {doc['original_url'] or 'no-url'}"
        for doc in related_docs[:10]
    ) or "- 暂无"
    key_block = "\n".join(f"- {point}" for point in card.get("key_points", [])[:5]) or "- 暂无"
    questions = card.get("open_questions", OPEN_QUESTIONS["misc"])
    question_block = "\n".join(f"- {question}" for question in questions)
    frontmatter = {
        "主题": card["display_title"],
        "主题键": card["topic"],
        "主题状态": "正式主题" if card["theme_kind"] == "formal" else "候选主题",
        "一句话总结": card["one_paragraph_summary"],
        "关联文档": card["related_doc_paths"][:10],
        "最近更新": card["last_updated_at"],
        "变更次数": card["change_count"],
        "来源范围": "笔记同步助手",
    }
    return (
        "---\n"
        f"{yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()}\n"
        "---\n\n"
        f"# {card['display_title']}\n\n"
        "## 当前结论\n"
        f"{card['one_paragraph_summary']}\n\n"
        "## 关键要点\n"
        f"{key_block}\n\n"
        "## 关联文档\n"
        f"{related_block}\n\n"
        "## 待解问题\n"
        f"{question_block}\n"
    )


def render_theme_update_log(topic: str, topic_title: str, records: Sequence[Dict[str, Any]]) -> str:
    frontmatter = {
        "主题": topic_title,
        "主题键": topic,
        "日志条数": len(records),
        "最近更新": records[0]["updated_at"] if records else "",
        "来源范围": "笔记同步助手",
    }
    sections: List[str] = []
    for record in records:
        trigger_docs = "\n".join(f"- {doc}" for doc in record.get("trigger_docs", [])) or "- 暂无"
        next_questions = "\n".join(f"- {item}" for item in record.get("next_questions", [])) or "- 暂无"
        sections.append(
            f"## {record['updated_at']}\n"
            f"- 主题状态：{'正式主题' if record['theme_kind'] == 'formal' else '候选主题'}\n"
            f"- 变更内容：{record['what_changed']}\n"
            f"- 变更原因：{record['why_changed']}\n"
            "### 触发文档\n"
            f"{trigger_docs}\n\n"
            "### 后续问题\n"
            f"{next_questions}"
        )
    return (
        "---\n"
        f"{yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()}\n"
        "---\n\n"
        f"# {topic_title} 更新日志\n\n"
        + "\n\n".join(sections)
        + "\n"
    )


def render_daily_digest(payload: Dict[str, Any]) -> str:
    frontmatter = {
        "摘要日期": payload["digest_date"],
        "生成时间": payload["generated_at"],
        "来源范围": "笔记同步助手",
        "新增主题数": len(payload.get("new_topics", [])),
        "更新主题数": len(payload.get("updated_topics", [])),
        "待人工处理数": len(payload.get("manual_access_notes", [])),
    }

    def topic_lines(items: Sequence[Dict[str, Any]]) -> str:
        lines = []
        for item in items:
            lines.append(f"- [[{item['obsidian_path'].replace('.md', '')}]] | {item['display_title']} | {item['what_changed']}")
        return "\n".join(lines) or "- 暂无"

    manual_lines = "\n".join(
        f"- [[{note['obsidian_path'].replace('.md', '')}]] | {note['title']} | {note['research_status']}"
        for note in payload.get("manual_access_notes", [])
    ) or "- 暂无"
    priority_lines = topic_lines(payload.get("priority_topics", []))
    return (
        "---\n"
        f"{yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()}\n"
        "---\n\n"
        f"# 今日变更摘要 {payload['digest_date']}\n\n"
        "## 新增主题\n"
        f"{topic_lines(payload.get('new_topics', []))}\n\n"
        "## 已有主题更新\n"
        f"{topic_lines(payload.get('updated_topics', []))}\n\n"
        "## 待人工处理\n"
        f"{manual_lines}\n\n"
        "## 建议优先阅读\n"
        f"{priority_lines}\n"
    )


def build_topic_summary(related_docs: Sequence[Dict[str, Any]], enriched_map: Dict[str, Dict[str, Any]], topic: str) -> str:
    summary_candidates: List[Dict[str, Any]] = []
    for doc in related_docs[:8]:
        enriched = enriched_map.get(doc["doc_id"])
        if enriched and enriched.get("research_summary"):
            summary_candidates.append({"excerpt": enriched["research_summary"], "score": enriched.get("confidence", 0.6)})
        else:
            summary_candidates.append({"excerpt": doc.get("summary") or doc.get("clean_text", "")[:220], "score": doc.get("quality_score", 0.5)})
    summary_sentences = choose_summary_sentences(summary_candidates, topic, limit=4)
    summary = normalize_whitespace(" ".join(summary_sentences[:3]))
    if summary:
        return summary
    fallback_parts = [
        enriched_map[doc["doc_id"]]["research_summary"]
        for doc in related_docs[:4]
        if doc["doc_id"] in enriched_map and enriched_map[doc["doc_id"]].get("research_summary")
    ]
    if fallback_parts:
        return normalize_whitespace(" ".join(fallback_parts))[:320]
    return normalize_whitespace(" ".join(doc.get("summary", "") for doc in related_docs[:3] if doc.get("summary")))[:320]


def card_change_summary(previous_card: Optional[Dict[str, Any]], new_card: Dict[str, Any], related_docs: Sequence[Dict[str, Any]]) -> Tuple[str, str]:
    if previous_card is None:
        return "首次创建主题主卡", "主题达到沉淀条件，开始作为独立主题持续跟踪"
    changes: List[str] = []
    previous_docs = set(previous_card.get("related_docs", []))
    new_docs = set(new_card.get("related_docs", []))
    added_count = len(new_docs - previous_docs)
    if added_count:
        changes.append(f"新增 {added_count} 条关联文档")
    if previous_card.get("one_paragraph_summary") != new_card.get("one_paragraph_summary"):
        changes.append("更新了一句话总结")
    if previous_card.get("theme_kind") != new_card.get("theme_kind"):
        changes.append("调整了主题状态")
    if not changes:
        changes.append("刷新了主题状态")
    why = "；".join(
        part
        for part in [
            "有新材料进入主题" if added_count else "",
            "已有结论被更高质量证据修正" if previous_card.get("one_paragraph_summary") != new_card.get("one_paragraph_summary") else "",
            "主题积累达到新的沉淀阈值" if previous_card.get("theme_kind") != new_card.get("theme_kind") else "",
        ]
        if part
    ) or "重新整理了主题内容"
    return "；".join(changes), why


def choose_theme_groups(
    notes: Sequence[Dict[str, Any]],
    enriched_map: Dict[str, Dict[str, Any]],
    config: Config,
    args: argparse.Namespace,
    stars: Dict[str, Dict[str, str]],
    history: Sequence[Dict[str, Any]],
) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, Dict[str, str]]]:
    topic_hits = query_hits_by_topic(history)
    groups: Dict[str, List[Dict[str, Any]]] = collections.defaultdict(list)
    assignments: Dict[str, Dict[str, str]] = {}

    for note in notes:
        if note["doc_shape"] == "bad_capture":
            continue
        if note["research_status"] == "needs_manual_access" and not note.get("clean_text"):
            continue
        enriched = enriched_map.get(note["doc_id"], {})
        primary_topic = next((topic for topic in note.get("auto_topics", []) if topic != "misc"), "")
        topic = primary_topic or enriched.get("theme_candidate") or note.get("theme_candidate") or candidate_label_from_note(NormalizedNote.from_record(note))
        if not topic:
            continue
        topic_hit_count = topic_hits.get(topic, 0)
        is_starred = stars.get("topics", {}).get(topic) == "starred" or stars.get("docs", {}).get(note["doc_id"]) == "starred"
        if not primary_topic and not is_starred and topic_hit_count < 1 and float(note.get("quality_score", 0.0)) < args.min_quality:
            continue
        groups[topic].append(note)

    for topic, related_docs in groups.items():
        unique_sources = {
            (doc.get("original_url") or doc.get("source_domain") or doc["doc_id"])
            for doc in related_docs
            if doc.get("original_url") or doc.get("source_domain")
        }
        topic_hits = query_hits_by_topic(history).get(topic, 0)
        topic_starred = stars.get("topics", {}).get(topic) == "starred"
        high_quality_docs = [doc for doc in related_docs if float(doc.get("quality_score", 0.0)) >= args.min_quality]
        formal = (
            len(high_quality_docs) >= args.min_docs
            or topic_starred
            or (len(unique_sources) >= 2 and len(related_docs) >= 2)
            or topic_hits >= 3
        )
        theme_kind = "formal" if formal else "candidate"
        for doc in related_docs:
            assignments[doc["doc_id"]] = {"topic": topic, "theme_status": theme_kind}
    return groups, assignments


def promote_topics_from_records(
    notes: Sequence[Dict[str, Any]],
    enriched_notes: Sequence[Dict[str, Any]],
    config: Config,
    args: argparse.Namespace,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], Dict[str, Dict[str, str]]]:
    ensure_layout(config)
    stars = read_manual_stars(config)
    history = load_query_history(config)
    previous_cards = {item["topic"]: item for item in load_topic_cards(config)}
    previous_logs = load_topic_update_logs(config)
    enriched_map = {item["doc_id"]: item for item in enriched_notes}
    groups, assignments = choose_theme_groups(notes, enriched_map, config, args, stars, history)

    cards: List[Dict[str, Any]] = []
    new_logs: List[Dict[str, Any]] = []
    digest_new_topics: List[Dict[str, Any]] = []
    digest_updated_topics: List[Dict[str, Any]] = []
    manual_access_notes = [
        note for note in notes
        if note.get("research_status") == "needs_manual_access"
    ]

    for topic, related_docs in sorted(groups.items()):
        related_docs.sort(
            key=lambda item: (
                -float(item.get("quality_score", 0.0)),
                item.get("saved_at", ""),
                item.get("title", ""),
            )
        )
        assignment = assignments.get(related_docs[0]["doc_id"], {"theme_status": "candidate"})
        theme_kind = assignment["theme_status"]
        topic_title = normalize_topic_title(topic)
        summary = build_topic_summary(related_docs, enriched_map, topic_title)
        key_points = key_points_from_related_docs(related_docs, enriched_map, topic_title)
        previous_card = previous_cards.get(topic)
        change_count = int(previous_card.get("change_count", 0)) + 1 if previous_card else 1
        last_updated_at = now_string()
        card_path = config.research_root / f"{slugify_topic(topic)}.md"
        card = topic_card_payload(
            topic=topic,
            topic_title=topic_title,
            summary=summary,
            related_docs=related_docs,
            theme_kind=theme_kind,
            change_count=change_count,
            last_updated_at=last_updated_at,
            absolute_file_path=card_path,
            obsidian_path=path_in_vault(card_path, config.vault_root),
            key_points=key_points,
        )
        card_path.write_text(render_topic_card(card, related_docs), encoding="utf-8")
        cards.append(card)

        what_changed, why_changed = card_change_summary(previous_card, card, related_docs)
        changed = previous_card is None or what_changed != "刷新了主题状态"
        if changed:
            log_path = config.topic_updates_root / f"{slugify_topic(topic)}.md"
            log_record = ThemeUpdateLog(
                topic=topic,
                topic_title=topic_title,
                theme_kind=theme_kind,
                updated_at=last_updated_at,
                trigger_docs=[doc["obsidian_path"] for doc in related_docs[:5]],
                what_changed=what_changed,
                why_changed=why_changed,
                next_questions=OPEN_QUESTIONS.get(topic, OPEN_QUESTIONS["misc"]),
                file_path=str(log_path.resolve()),
                obsidian_path=path_in_vault(log_path, config.vault_root),
            ).to_record()
            new_logs.append(log_record)
            digest_item = {
                "topic": topic,
                "display_title": topic_title,
                "obsidian_path": card["obsidian_path"],
                "what_changed": what_changed,
            }
            if previous_card is None:
                digest_new_topics.append(digest_item)
            else:
                digest_updated_topics.append(digest_item)

    current_card_paths = {str(pathlib.Path(card["source_file"]).resolve()) for card in cards}
    for path in config.research_root.glob("*.md"):
        if str(path.resolve()) not in current_card_paths:
            path.unlink()

    all_logs = previous_logs + new_logs
    write_jsonl(config.artifacts_root / "topic_update_logs.jsonl", all_logs)
    grouped_logs: Dict[str, List[Dict[str, Any]]] = collections.defaultdict(list)
    for record in all_logs:
        grouped_logs[record["topic"]].append(record)
    for topic, records in grouped_logs.items():
        records.sort(key=lambda item: item["updated_at"], reverse=True)
        log_path = config.topic_updates_root / f"{slugify_topic(topic)}.md"
        topic_title = records[0]["topic_title"]
        log_path.write_text(render_theme_update_log(topic, topic_title, records), encoding="utf-8")

    write_jsonl(config.artifacts_root / "topic_cards.jsonl", cards)

    digest_date = dt.datetime.now().strftime("%Y-%m-%d")
    priority_topics = (digest_new_topics + digest_updated_topics)[:8]
    digest_payload = {
        "digest_date": digest_date,
        "generated_at": now_string(),
        "new_topics": digest_new_topics,
        "updated_topics": digest_updated_topics,
        "manual_access_notes": manual_access_notes[:12],
        "priority_topics": priority_topics,
        "file_path": str((config.daily_digest_root / f"{digest_date}.md").resolve()),
        "obsidian_path": path_in_vault(config.daily_digest_root / f"{digest_date}.md", config.vault_root),
    }
    digest_path = config.daily_digest_root / f"{digest_date}.md"
    digest_path.write_text(render_daily_digest(digest_payload), encoding="utf-8")
    digest_record = dict(digest_payload)
    all_digests = load_daily_digests(config) + [digest_record]
    write_jsonl(config.artifacts_root / "daily_change_digests.jsonl", all_digests)
    return cards, new_logs, digest_payload, assignments


def apply_theme_assignments(notes: Sequence[NormalizedNote], assignments: Dict[str, Dict[str, str]]) -> List[NormalizedNote]:
    updated: List[NormalizedNote] = []
    for note in notes:
        assignment = assignments.get(note.doc_id)
        if assignment:
            note = dataclasses.replace(
                note,
                theme_candidate=assignment["topic"],
                theme_status=assignment["theme_status"],
            )
        updated.append(note)
    return updated


def apply_filters(
    note: Dict[str, Any],
    topic: str,
    source_domain: str,
    date_range: str,
    include_bad_capture: bool,
) -> bool:
    if not include_bad_capture and note.get("doc_shape") == "bad_capture":
        return False
    if note.get("capture_status") == "failed" and note.get("doc_shape") == "bad_capture":
        return include_bad_capture
    if note.get("research_status") == "needs_manual_access":
        return False
    if topic and topic not in (note.get("auto_topics") or []) and topic != note.get("theme_candidate"):
        return False
    if source_domain and source_domain.lower() != str(note.get("source_domain") or "").lower():
        return False
    if date_range:
        start_raw, end_raw = (date_range.split(":", 1) + [""])[:2]
        saved = parse_datetime_safe(str(note.get("saved_at") or ""))
        if not saved:
            return False
        start = parse_datetime_safe(start_raw) if start_raw else None
        end = parse_datetime_safe(end_raw) if end_raw else None
        if start and saved < start:
            return False
        if end and saved > end + dt.timedelta(days=1):
            return False
    return True


def build_excerpt(text: str, query: str, max_chars: int = 220) -> str:
    normalized = normalize_whitespace(text.replace("\n", " "))
    if len(normalized) <= max_chars:
        return normalized
    query_terms = tokenize_for_vector(query)
    lowered = normalized.lower()
    start = 0
    for term in query_terms:
        idx = lowered.find(term.lower())
        if idx >= 0:
            start = max(0, idx - 40)
            break
    excerpt = normalized[start:start + max_chars]
    if start > 0:
        excerpt = "..." + excerpt
    if start + max_chars < len(normalized):
        excerpt += "..."
    return excerpt


def exact_match_boost(note: Dict[str, Any], query: str) -> float:
    query_lower = query.lower()
    title = str(note.get("title") or "").lower()
    url = str(note.get("original_url") or "").lower()
    obsidian_path = str(note.get("obsidian_path") or "").lower()
    boost = 0.0
    if query_lower and query_lower in title:
        boost += 0.35
    if query_lower and query_lower in url:
        boost += 0.45
    if query_lower and query_lower in obsidian_path:
        boost += 0.25
    return boost


def citation_payload(note: Dict[str, Any], chunk: Dict[str, Any], score: float, query: str) -> Dict[str, Any]:
    return {
        "doc_id": note["doc_id"],
        "title": note["title"],
        "file_path": note["source_file"],
        "obsidian_path": note["obsidian_path"],
        "url": note["original_url"],
        "excerpt": build_excerpt(chunk["chunk_text"], query),
        "score": round(score, 4),
        "heading_path": chunk["heading_path"],
        "evidence_type": "raw_chunk",
    }


def sentence_score(sentence: str, query_terms: Sequence[str], base_score: float) -> float:
    lowered = sentence.lower()
    overlap = sum(1 for term in query_terms if term.lower() in lowered)
    return base_score + (0.12 * overlap) + min(len(sentence) / 300.0, 0.08)


def choose_summary_sentences(citations: Sequence[Dict[str, Any]], query: str, limit: int = 4) -> List[str]:
    query_terms = tokenize_for_vector(query)
    candidates: List[Tuple[float, str]] = []
    seen = set()
    for citation in citations[:8]:
        for sentence in extract_sentences(str(citation["excerpt"])):
            normalized = normalize_whitespace(sentence)
            if len(normalized) < 20 or normalized in seen:
                continue
            seen.add(normalized)
            candidates.append((sentence_score(normalized, query_terms, float(citation.get("score", 0.4))), normalized))
    chosen = [sentence for _score, sentence in sorted(candidates, key=lambda item: item[0], reverse=True)[:limit]]
    return chosen


def related_note_payload(note: Dict[str, Any], score: float, note_type: str = "raw_note") -> Dict[str, Any]:
    title = note.get("display_title") or note.get("title", "")
    topics = note.get("auto_topics") or ([note.get("topic")] if note.get("topic") else [])
    return {
        "doc_id": note.get("doc_id", ""),
        "title": title,
        "summary": note.get("summary", "") or note.get("one_paragraph_summary", ""),
        "file_path": note.get("source_file", ""),
        "obsidian_path": note.get("obsidian_path", ""),
        "url": note.get("original_url", ""),
        "topics": topics,
        "saved_at": note.get("saved_at", ""),
        "score": round(score, 4),
        "note_type": note_type,
    }


def enriched_note_payload(enriched: Dict[str, Any], note: Dict[str, Any], score: float) -> Dict[str, Any]:
    return {
        "doc_id": note["doc_id"],
        "title": f"{note['title']} 研究笔记",
        "summary": enriched.get("research_summary", ""),
        "file_path": note.get("source_file", ""),
        "obsidian_path": note.get("obsidian_path", ""),
        "url": note.get("original_url", ""),
        "topics": dedupe_keep_order(([enriched.get("theme_candidate", "")] if enriched.get("theme_candidate") else []) + note.get("auto_topics", [])),
        "saved_at": enriched.get("updated_at", note.get("saved_at", "")),
        "score": round(score, 4),
        "note_type": "enriched_note",
    }


def build_empty_result(message: str) -> Dict[str, Any]:
    return {
        "answer": answer_markdown("", message, [], []),
        "citations": [],
        "related_notes": [],
        "confidence": 0.12,
    }


def answer_markdown(
    query: str,
    brief_summary: str,
    related_notes: Sequence[Dict[str, Any]],
    citations: Sequence[Dict[str, Any]],
) -> str:
    lines = [
        "## 简要结论",
        brief_summary or "没有找到足够高质量的证据来稳定回答这个问题。",
        "",
        "## 相关文章",
    ]
    if related_notes:
        for note in related_notes[:6]:
            note_kind = {
                "topic_card": "主题卡",
                "enriched_note": "研究笔记",
                "raw_note": "原始笔记",
            }.get(note.get("note_type", "raw_note"), "笔记")
            topic_text = ", ".join(note.get("topics", []))
            lines.append(f"- [{note_kind}] {note['title']} | {topic_text} | {note.get('file_path', '')}")
    else:
        lines.append("- 暂无匹配结果")
    lines.extend(["", "## 关键摘录"])
    if citations:
        for citation in citations[:4]:
            lines.append(f"- {citation['excerpt']}")
    else:
        lines.append("- 暂无摘录")
    lines.extend(["", "## 引用来源"])
    if citations:
        for citation in citations[:4]:
            lines.append(f"- {citation['file_path']} | {citation['url'] or 'no-url'}")
    else:
        lines.append("- 暂无来源")
    return "\n".join(lines).strip()


def query_index(args: argparse.Namespace, config: Config) -> Dict[str, Any]:
    notes, chunks, vector_index = load_notes_and_chunks(config)
    enriched_notes = {item["doc_id"]: item for item in load_enriched_notes(config)}
    note_map = {note["doc_id"]: note for note in notes}
    chunk_map = {chunk["chunk_id"]: chunk for chunk in chunks}
    query_topics = auto_topics_for_note(args.query, args.query, args.query, "article")
    exact_good_match_notes = [
        note
        for note in notes
        if note.get("doc_shape") != "bad_capture" and exact_match_boost(note, args.query) >= 0.45
    ]
    fts_scores: Dict[str, float] = {}
    db_path = config.artifacts_root / "index.sqlite"
    if db_path.exists():
        connection = sqlite3.connect(str(db_path))
        try:
            fts_query = build_fts_query(args.query)
            if fts_query:
                rows = connection.execute(
                    """
                    select chunk_id, bm25(chunk_fts) as score
                    from chunk_fts
                    where chunk_fts match ?
                    limit 60
                    """,
                    (fts_query,),
                ).fetchall()
                for chunk_id, bm25_score in rows:
                    lexical_score = 1.0 / (1.0 + abs(float(bm25_score)))
                    fts_scores[str(chunk_id)] = lexical_score
        except sqlite3.Error:
            pass
        finally:
            connection.close()
    vector_scores = vector_query_scores(args.query, vector_index)
    candidate_ids = set(fts_scores) | set(vector_scores)
    exact_bad_capture_notes = [
        note
        for note in notes
        if note.get("doc_shape") == "bad_capture" and exact_match_boost(note, args.query) >= 0.45
    ]
    if exact_bad_capture_notes and not exact_good_match_notes and not args.include_bad_capture:
        note = exact_bad_capture_notes[0]
        result = {
            "answer": answer_markdown(
                args.query,
                "匹配到的记录是一次抓取失败页面，已按默认规则排除出正常答案。你可以改用原始 URL 重新抓取，或在排查模式下显式包含 bad_capture。",
                [related_note_payload(note, 0.6)],
                [],
            ),
            "citations": [],
            "related_notes": [related_note_payload(note, 0.6)],
            "confidence": 0.26,
        }
        append_query_history(config, args.query, result)
        return result
    if not candidate_ids:
        result = build_empty_result("没有检索到足够相关的同步内容。先同步更多原文，或换更具体的标题/URL 再试。")
        append_query_history(config, args.query, result)
        return result
    ranked_chunks: List[Tuple[float, Dict[str, Any], Dict[str, Any]]] = []
    for chunk_id in candidate_ids:
        chunk = chunk_map.get(chunk_id)
        if not chunk:
            continue
        note = note_map.get(chunk["doc_id"])
        if not note:
            continue
        if not apply_filters(note, args.topic, args.source_domain, args.date_range, args.include_bad_capture):
            continue
        lexical = fts_scores.get(chunk_id, 0.0)
        vector = vector_scores.get(chunk_id, 0.0)
        boost = exact_match_boost(note, args.query)
        quality = float(note.get("quality_score", 0.0))
        note_topics = note.get("auto_topics") or []
        topic_overlap = len(set(query_topics) & set(note_topics))
        theme_match = 0.12 if note.get("theme_candidate") and note.get("theme_candidate") in query_topics else 0.0
        topic_boost = 0.08 if args.topic and args.topic in note_topics else 0.0
        if topic_overlap and "misc" not in query_topics:
            topic_boost += 0.22 * topic_overlap
        score = (0.52 * lexical) + (0.25 * vector) + boost + topic_boost + theme_match + (0.15 * quality)
        if note.get("doc_shape") == "bad_capture":
            score *= 0.2
        if note.get("research_status") == "needs_manual_access":
            score *= 0.4
        if score <= 0:
            continue
        ranked_chunks.append((score, chunk, note))
    ranked_chunks.sort(key=lambda item: item[0], reverse=True)
    if not ranked_chunks:
        result = build_empty_result("没有检索到足够高质量的相关内容。可以尝试更精确的标题、URL 或 topic 过滤。")
        append_query_history(config, args.query, result)
        return result
    citations: List[Dict[str, Any]] = []
    related_notes_raw: List[Tuple[float, Dict[str, Any]]] = []
    best_doc_scores: Dict[str, float] = {}
    for score, chunk, note in ranked_chunks[:30]:
        citations.append(citation_payload(note, chunk, score, args.query))
        best_doc_scores[note["doc_id"]] = max(best_doc_scores.get(note["doc_id"], 0.0), score)
    for doc_id, score in sorted(best_doc_scores.items(), key=lambda item: item[1], reverse=True):
        related_notes_raw.append((score, note_map[doc_id]))

    topic_cards = load_topic_cards(config)
    topic_card_map = {card["topic"]: card for card in topic_cards}
    related_notes: List[Dict[str, Any]] = []
    top_topics = dedupe_keep_order(
        topic
        for _score, note in related_notes_raw[:5]
        for topic in note.get("auto_topics", [])
        if topic != "misc"
    )
    preferred_cards: List[Dict[str, Any]] = []
    preferred_topic_order = dedupe_keep_order(([args.topic] if args.topic else []) + [topic for topic in query_topics if topic != "misc"] + top_topics)
    for topic in preferred_topic_order:
        card = topic_card_map.get(topic)
        if card:
            preferred_cards.append(card)

    strong_exact_match = any(score >= 0.9 for score, _note in related_notes_raw[:2])
    ordered_raw_notes = related_notes_raw[:5] if strong_exact_match else related_notes_raw[:6]
    for card in dedupe_keep_order(card["topic"] for card in preferred_cards):
        payload = topic_card_map[card]
        related_notes.append(related_note_payload(payload, 0.99, note_type="topic_card"))
    for score, note in ordered_raw_notes:
        enriched = enriched_notes.get(note["doc_id"])
        if enriched and enriched.get("research_status") == "enriched":
            related_notes.append(enriched_note_payload(enriched, note, max(score, enriched.get("confidence", 0.0))))
        related_notes.append(related_note_payload(note, score))

    summary_sentences = choose_summary_sentences(citations, args.query)
    brief_parts: List[str] = []
    for card in preferred_cards[:2]:
        summary = card.get("one_paragraph_summary", "").strip()
        if summary:
            brief_parts.append(summary)
    for score, note in ordered_raw_notes[:3]:
        enriched = enriched_notes.get(note["doc_id"])
        if enriched and enriched.get("research_summary"):
            brief_parts.append(enriched["research_summary"])
        elif note.get("summary"):
            brief_parts.append(note["summary"])
    if summary_sentences:
        brief_parts.append(" ".join(summary_sentences[:3]))
    brief_summary = normalize_whitespace(" ".join(dedupe_keep_order(part for part in brief_parts if part)))
    top_score = ranked_chunks[0][0] if ranked_chunks else 0.0
    confidence = round(min(0.96, 0.25 + top_score + (0.05 * min(len(best_doc_scores), 4))), 4)
    answer = answer_markdown(args.query, brief_summary, related_notes, citations)
    result = {
        "answer": answer,
        "citations": citations[:4],
        "related_notes": related_notes[:8],
        "confidence": confidence,
    }
    append_query_history(config, args.query, result)
    return result


def print_json(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_index_command(args: argparse.Namespace, config: Config) -> None:
    ensure_layout(config)
    effective_config = dataclasses.replace(config, enable_network=(config.enable_network and not getattr(args, "disable_network", False)))
    notes = build_notes(effective_config)
    notes, enriched_notes, scan_report = enrich_notes(notes, effective_config, force_full_rescan=args.force_full_rescan)
    cards, new_logs, digest_payload, assignments = promote_topics_from_records(
        [note.to_record() for note in notes],
        [item.to_record() for item in enriched_notes],
        effective_config,
        argparse.Namespace(min_quality=effective_config.promotion_min_quality, min_docs=effective_config.promotion_min_docs),
    )
    notes = apply_theme_assignments(notes, assignments)
    chunks = build_chunks(notes, effective_config)
    vector_index = build_vector_index(chunks)
    write_jsonl(effective_config.artifacts_root / "normalized_docs.jsonl", [note.to_record() for note in notes])
    write_jsonl(effective_config.artifacts_root / "enriched_notes.jsonl", [item.to_record() for item in enriched_notes])
    write_jsonl(effective_config.artifacts_root / "chunks.jsonl", [chunk.to_record() for chunk in chunks])
    write_vector_index(effective_config.artifacts_root / "vector_index.json", vector_index)
    build_sqlite_index(notes, chunks, effective_config.artifacts_root / "index.sqlite")
    report = {
        "built_at": now_string(),
        "note_count": len(notes),
        "chunk_count": len(chunks),
        "enriched_note_count": len(enriched_notes),
        "topic_card_count": len(cards),
        "new_topic_count": len(digest_payload.get("new_topics", [])),
        "updated_topic_count": len(digest_payload.get("updated_topics", [])),
        "new_doc_count": scan_report["new_doc_count"],
        "updated_doc_count": scan_report["updated_doc_count"],
        "retried_doc_count": scan_report["retried_doc_count"],
        "unchanged_doc_count": scan_report["unchanged_doc_count"],
        "failed_doc_count": scan_report["failed_doc_count"],
        "needs_manual_access_count": scan_report["needs_manual_access_count"],
        "needs_retry_count": scan_report["needs_retry_count"],
        "full_rescan_due": scan_report["full_rescan_due"],
        "topic_counts": dict(collections.Counter(topic for note in notes for topic in note.auto_topics)),
        "doc_shape_counts": dict(collections.Counter(note.doc_shape for note in notes)),
        "capture_status_counts": dict(collections.Counter(note.capture_status for note in notes)),
        "research_status_counts": dict(collections.Counter(note.research_status for note in notes)),
        "content_kind_counts": dict(collections.Counter(note.content_kind for note in notes)),
        "daily_digest_path": digest_payload["file_path"],
        "new_topic_log_count": len(new_logs),
    }
    (effective_config.artifacts_root / "build_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print_json(report)


def query_command(args: argparse.Namespace, config: Config) -> None:
    result = query_index(args, config)
    if args.format == "json":
        print_json(result)
        return
    print(result["answer"])
    print("")
    print(f"confidence: {result['confidence']}")


def promote_command(args: argparse.Namespace, config: Config) -> None:
    ensure_layout(config)
    notes = load_jsonl(config.artifacts_root / "normalized_docs.jsonl")
    enriched_notes = load_enriched_notes(config)
    if not notes:
        raise FileNotFoundError("index artifacts missing; run build-index first")
    cards, new_logs, digest_payload, assignments = promote_topics_from_records(notes, enriched_notes, config, args)
    updated_notes = []
    for note in notes:
        assignment = assignments.get(note["doc_id"])
        if assignment:
            note["theme_candidate"] = assignment["topic"]
            note["theme_status"] = assignment["theme_status"]
        updated_notes.append(note)
    write_jsonl(config.artifacts_root / "normalized_docs.jsonl", updated_notes)
    print_json(
        {
            "generated_cards": len(cards),
            "new_topic_log_count": len(new_logs),
            "daily_digest_path": digest_payload["file_path"],
            "topics": [card["topic"] for card in cards],
        }
    )


def star_command(args: argparse.Namespace, config: Config) -> None:
    ensure_layout(config)
    payload = read_manual_stars(config)
    state = "starred" if args.value == "starred" else "cleared"
    key = "topics" if args.type == "topic" else "docs"
    if state == "starred":
        payload.setdefault(key, {})[args.target] = "starred"
    else:
        payload.setdefault(key, {}).pop(args.target, None)
    write_manual_stars(config, payload)
    print_json(payload)


def stats_command(config: Config) -> None:
    build_report_path = config.artifacts_root / "build_report.json"
    if not build_report_path.exists():
        raise FileNotFoundError("build report missing; run build-index first")
    print(build_report_path.read_text(encoding="utf-8"))


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian 同步助手本地知识库工具")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="配置文件路径")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build-index", help="重建 inbox 索引")
    build_parser.add_argument("--skip-promote", action="store_true", help="兼容旧参数；V2 始终会生成主题产物")
    build_parser.add_argument("--force-full-rescan", action="store_true", help="强制触发一次全量回扫")
    build_parser.add_argument("--disable-network", action="store_true", help="构建时禁用网络读取")

    query_parser = subparsers.add_parser("query", help="查询 inbox 知识库")
    query_parser.add_argument("query", help="查询文本")
    query_parser.add_argument("--topic", default="", help="按 topic 过滤")
    query_parser.add_argument("--source-domain", default="", help="按来源域名过滤")
    query_parser.add_argument("--date-range", default="", help="日期范围，格式 2026-03-01:2026-03-31")
    query_parser.add_argument("--include-bad-capture", action="store_true", help="包含 bad_capture 文档")
    query_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    promote_parser = subparsers.add_parser("promote", help="生成主题卡片")
    promote_parser.add_argument("--min-quality", type=float, default=None, help="升格最小质量分")
    promote_parser.add_argument("--min-docs", type=int, default=None, help="升格最小文档数")

    star_parser = subparsers.add_parser("star", help="手动标星 doc 或 topic")
    star_parser.add_argument("target", help="doc_id 或 topic")
    star_parser.add_argument("--type", choices=["doc", "topic"], default="doc")
    star_parser.add_argument("--value", choices=["starred", "clear"], default="starred")

    subparsers.add_parser("stats", help="查看最近一次 build 报告")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    config = load_config(pathlib.Path(args.config).expanduser().resolve())
    if getattr(args, "min_quality", None) is None:
        args.min_quality = config.promotion_min_quality
    if getattr(args, "min_docs", None) is None:
        args.min_docs = config.promotion_min_docs
    try:
        if args.command == "build-index":
            build_index_command(args, config)
        elif args.command == "query":
            query_command(args, config)
        elif args.command == "promote":
            promote_command(args, config)
        elif args.command == "star":
            star_command(args, config)
        elif args.command == "stats":
            stats_command(config)
        else:
            parser.error(f"unknown command: {args.command}")
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
