#!/usr/bin/env python3
"""Personal Knowledge Hub handler."""

from __future__ import annotations

import re
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional

from models import KnowledgeGraph, KnowledgeItem, QueryIntent, SearchResult


SAMPLE_KNOWLEDGE = [
    KnowledgeItem(
        id="k1",
        title="Machine Learning Basics / 机器学习基础",
        content="Machine learning, also called 机器学习, is a branch of AI covering supervised learning, unsupervised learning, and reinforcement learning.",
        source_type="note",
        tags=["AI", "machine-learning", "机器学习", "basics"],
        entities=["AI", "machine learning", "机器学习", "supervised learning"],
    ),
    KnowledgeItem(
        id="k2",
        title="深度学习应用总结",
        content="深度学习在图像识别、自然语言处理、语音识别和推荐系统中常见。",
        source_type="note",
        tags=["AI", "深度学习", "应用"],
        entities=["深度学习", "图像识别", "NLP", "推荐系统"],
    ),
    KnowledgeItem(
        id="k3",
        title="Python Engineering Notes",
        content="Python engineering practice includes type hints, tests, clear modules, and simple CLI entry points.",
        source_type="doc",
        tags=["Python", "engineering", "testing"],
        entities=["Python", "type hints", "tests"],
    ),
    KnowledgeItem(
        id="k4",
        title="产品设计思考",
        content="产品设计需要平衡用户需求、技术可行性、商业价值和长期维护成本。",
        source_type="note",
        tags=["产品", "设计", "方法论"],
        entities=["产品设计", "用户需求", "商业价值"],
    ),
    KnowledgeItem(
        id="k5",
        title="知识管理复盘",
        content="个人知识库应当把收集、整理、复习和输出连接起来，避免只收藏不使用。",
        source_type="note",
        tags=["知识管理", "复习", "输出"],
        entities=["个人知识库", "复习", "输出"],
    ),
]


INTENT_PREFIXES = {
    "search": ["搜索", "查找", "查询", "找", "检索", "复习", "search", "find", "lookup", "review"],
    "ingest": ["添加", "存入", "收藏", "记录", "保存", "记下", "capture", "save", "ingest", "add"],
    "analyze": ["分析", "总结", "概括", "提炼", "抽取", "analyze", "summarize", "extract"],
    "explore": ["关联", "图谱", "关系", "探索", "连接", "explore", "graph", "connect", "map"],
}

REJECT_PATTERN = re.compile(r"(外挂|破解|盗取|入侵|窃取|exfiltrate|steal|hack)", re.IGNORECASE)
WORD_PATTERN = re.compile(r"[A-Za-z0-9_+-]+|[\u4e00-\u9fff]{2,12}")
STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "about",
    "please",
    "搜索",
    "查找",
    "查询",
    "记录",
    "保存",
    "分析",
    "总结",
    "探索",
    "关于",
    "一下",
    "我的",
    "一个",
    "这个",
    "什么",
}


def normalize(text: str) -> str:
    return " ".join(WORD_PATTERN.findall(text.lower()))


def strip_intent_words(text: str) -> str:
    cleaned = text.strip()
    for words in INTENT_PREFIXES.values():
        for word in words:
            cleaned = re.sub(rf"\b{re.escape(word)}\b", " ", cleaned, flags=re.IGNORECASE)
            cleaned = cleaned.replace(word, " ")
    cleaned = cleaned.replace("关于", " ").replace("一下", " ")
    return re.sub(r"\s+", " ", cleaned).strip()


def keywords(text: str) -> List[str]:
    cleaned = strip_intent_words(text)
    terms: List[str] = []
    for source in [cleaned, text]:
        for term in WORD_PATTERN.findall(source.lower()):
            if term and term not in STOPWORDS and term not in terms:
                terms.append(term)
    if cleaned and cleaned.lower() not in terms:
        terms.insert(0, cleaned.lower())
    return terms[:12]


def parse_intent(text: str) -> QueryIntent:
    lowered = text.lower()
    for intent_type, markers in INTENT_PREFIXES.items():
        if any(marker.lower() in lowered for marker in markers):
            return QueryIntent(intent_type=intent_type, query_text=text, topic=strip_intent_words(text) or text)
    return QueryIntent(intent_type="search", query_text=text, topic=strip_intent_words(text) or text)


def item_from_dict(raw: Dict) -> KnowledgeItem:
    return KnowledgeItem(
        id=str(raw.get("id") or raw.get("slug") or raw.get("title") or "item"),
        title=str(raw.get("title") or raw.get("name") or "Untitled"),
        content=str(raw.get("content") or raw.get("body") or raw.get("text") or raw.get("summary") or ""),
        source_type=str(raw.get("source_type") or raw.get("source") or "note"),
        source_uri=str(raw.get("source_uri") or raw.get("url") or ""),
        tags=list(raw.get("tags") or []),
        entities=list(raw.get("entities") or []),
        created_at=str(raw.get("created_at") or raw.get("created") or ""),
    )


def coerce_items(knowledge_base: Optional[List[Dict]]) -> List[KnowledgeItem]:
    if not knowledge_base:
        return SAMPLE_KNOWLEDGE
    items = []
    for raw in knowledge_base:
        if isinstance(raw, KnowledgeItem):
            items.append(raw)
        elif isinstance(raw, dict):
            items.append(item_from_dict(raw))
    return items or SAMPLE_KNOWLEDGE


def search_knowledge(query: str, items: Optional[List[KnowledgeItem]] = None) -> List[SearchResult]:
    items = items or SAMPLE_KNOWLEDGE
    query_terms = keywords(query)
    results: List[SearchResult] = []

    for item in items:
        haystack = normalize(" ".join([item.title, item.content, " ".join(item.tags), " ".join(item.entities)]))
        matched = []
        score = 0.0
        for term in query_terms:
            term_l = term.lower()
            if term_l in haystack:
                matched.append(term)
                score += 1.0
                if term_l in item.title.lower():
                    score += 2.0
                if any(term_l in tag.lower() for tag in item.tags):
                    score += 1.5
                if any(term_l in entity.lower() for entity in item.entities):
                    score += 1.5
        if matched:
            snippet = make_snippet(item.content, matched[0])
            related_tags = [tag for tag in item.tags if any(term.lower() in tag.lower() for term in matched)]
            results.append(
                SearchResult(
                    item=item,
                    snippet=snippet,
                    relevance_score=min(score / max(len(query_terms), 1), 1.0),
                    matched_terms=matched,
                    related_tags=related_tags,
                )
            )

    results.sort(key=lambda result: result.relevance_score, reverse=True)
    return results[:10]


def make_snippet(content: str, term: str) -> str:
    idx = content.lower().find(term.lower())
    if idx < 0:
        return content[:120]
    start = max(0, idx - 32)
    end = min(len(content), idx + 96)
    prefix = "..." if start else ""
    suffix = "..." if end < len(content) else ""
    return f"{prefix}{content[start:end]}{suffix}"


def extract_metadata(text: str) -> Dict:
    terms = keywords(text)
    word_count = len(WORD_PATTERN.findall(text))
    suggested_title = strip_intent_words(text) or text
    suggested_title = suggested_title[:60]
    entities = [term for term in terms if len(term) >= 2][:8]
    return {
        "suggested_title": suggested_title,
        "suggested_tags": terms[:8],
        "entities": entities,
        "word_count": word_count,
        "captured_at": datetime.now(timezone.utc).isoformat(),
    }


def build_graph(topic: str, items: Optional[List[KnowledgeItem]] = None) -> KnowledgeGraph:
    items = items or SAMPLE_KNOWLEDGE
    topic_terms = keywords(topic)
    entities: List[Dict] = []
    connections: List[Dict] = []
    seen_entities = set()

    related_items = []
    for item in items:
        haystack = normalize(" ".join([item.title, item.content, " ".join(item.tags), " ".join(item.entities)]))
        if any(term.lower() in haystack for term in topic_terms):
            related_items.append(item)
            for entity in item.entities:
                if entity not in seen_entities:
                    seen_entities.add(entity)
                    entities.append({"name": entity, "type": "entity", "source": item.title})

    for item in related_items:
        for entity in item.entities:
            connections.append({"from": topic, "to": entity, "type": "mentions", "source": item.title})

    return KnowledgeGraph(central_topic=topic, entities=entities[:20], connections=connections[:30], depth=1)


def check_rejection(text: str) -> Optional[str]:
    if REJECT_PATTERN.search(text):
        return "This skill only handles user-owned knowledge and does not support unauthorized access or data theft."
    return None


def handle(text: str, knowledge_base: Optional[List[Dict]] = None) -> Dict:
    rejection = check_rejection(text)
    if rejection:
        return {"status": "rejected", "reason": rejection}

    items = coerce_items(knowledge_base)
    intent = parse_intent(text)

    if intent.intent_type == "search":
        results = search_knowledge(intent.topic or text, items)
        return {
            "status": "ok",
            "requestType": "search",
            "query": intent.topic or text,
            "total_results": len(results),
            "results": [
                {
                    "id": result.item.id,
                    "title": result.item.title,
                    "snippet": result.snippet,
                    "score": round(result.relevance_score, 2),
                    "tags": result.item.tags,
                    "source": result.item.source_type,
                    "matched_terms": result.matched_terms,
                }
                for result in results[:5]
            ],
            "message": "Found matching knowledge items." if results else "No matching knowledge items found.",
            "using_sample_data": knowledge_base is None,
        }

    if intent.intent_type == "ingest":
        metadata = extract_metadata(intent.topic or text)
        return {
            "status": "ok",
            "requestType": "ingest",
            "message": "Knowledge item captured as a draft.",
            "note": {
                "title": metadata["suggested_title"],
                "tags": metadata["suggested_tags"],
                "entities": metadata["entities"],
                "template": [
                    "Core idea",
                    "Evidence or examples",
                    "My interpretation",
                    "Next action or review date",
                ],
            },
            "metadata": metadata,
        }

    if intent.intent_type == "analyze":
        metadata = extract_metadata(intent.topic or text)
        results = search_knowledge(intent.topic or text, items)
        return {
            "status": "ok",
            "requestType": "analyze",
            "topic": intent.topic or text,
            "summary": results[0].item.content[:240] if results else "No existing note matched; extracted metadata from the supplied text.",
            "suggested_tags": metadata["suggested_tags"],
            "entities": metadata["entities"],
            "related_items": [result.item.title for result in results[:5]],
            "using_sample_data": knowledge_base is None,
        }

    if intent.intent_type == "explore":
        graph = build_graph(intent.topic or text, items)
        return {
            "status": "ok",
            "requestType": "explore",
            "central_topic": graph.central_topic,
            "entities_found": len(graph.entities),
            "connections_found": len(graph.connections),
            "top_entities": [entity["name"] for entity in graph.entities[:10]],
            "connections": graph.connections[:10],
            "using_sample_data": knowledge_base is None,
        }

    return {"status": "ok", "requestType": "help", "message": "Personal Knowledge Hub is ready."}


if __name__ == "__main__":
    examples = [
        "搜索机器学习",
        "存入今天读到的产品设计方法：先识别用户痛点，再设计低摩擦路径",
        "分析深度学习应用",
        "探索AI知识图谱",
    ]
    for example in examples:
        print(handle(example))
