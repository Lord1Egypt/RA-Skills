"""Deterministic lexical retrieval shared by detection, search, and local indexes.

Scores describe query evidence, not whether a stored claim is true. Callers must
resolve provenance and superseded facts before presenting a current user fact.
No dictionary, network, model, or conversation-specific topic list is required.
"""
from __future__ import annotations

import re
import unicodedata

# Preserve the public field names and weights used by signal_detect callers.
FIELD_WEIGHTS = {
    "title": 2.2, "summary": 1.5, "semantic_context": 1.8,
    "tags": 1.0, "triggers": 1.2, "scenarios": 1.1, "aliases": 2.2,
}
STRONG_FIELDS = frozenset({"title", "summary", "tags", "triggers", "aliases"})
_FIELD_QUALITY = {
    "title": 1.0, "summary": 0.9, "semantic_context": 0.85,
    "tags": 0.95, "triggers": 0.9, "scenarios": 0.8, "aliases": 1.0,
}
_HAN = r"[\u3400-\u4dbf\u4e00-\u9fff\U00020000-\U0002fa1f]"
_HAN_RUN = re.compile(_HAN + "+")
_WORD = re.compile(r"[^\W_]+(?:[_.+-][^\W_]+)*", re.UNICODE)
_EN_FILLER = frozenset("""
    a an and are as at be been being but by can could did do does for from
    had has have how i if in is it its me my of on or our please remember
    recall so that the their them then there these they this those to us
    was we were what when where which who why will with would you your
    about again before earlier previously last time tell help some any
    information context thing things issue issues problem problems details
    note notes memory memories solution solutions situation
""".split())
# These are grammatical/common recall words, not topic names. Replace with a
# separator so removing boilerplate never creates an invented adjacent bigram.
_ZH_FILLER = tuple(sorted({
    "你还记得", "还记得", "回忆一下", "回忆下", "请帮我", "帮我", "请问",
    "告诉我", "能不能", "可不可以", "有没有", "为什么", "是什么",
    "什么时候", "上一次", "怎么回事", "之前", "以前", "上次", "曾经",
    "当时", "最近", "目前", "现在", "回忆", "记得", "记忆", "一下",
    "怎样", "怎么", "如何", "哪里", "哪些", "什么", "是否", "还是",
    "已经", "仍然", "就是", "那个", "这个", "这些", "那些", "关于",
    "有关", "相关", "我们", "你们", "他们", "我的", "你的", "用户",
    "麻烦", "以及", "然后", "的话", "时候", "可以", "需要", "希望",
    "问题", "解决", "处理", "方法", "记录", "笔记", "内容", "信息",
    "东西", "事情", "经验", "情况", "步骤", "帮助", "告诉",
}, key=lambda value: (-len(value), value)))
_ZH_SPLIT = re.compile("|".join(map(re.escape, _ZH_FILLER)))
_ZH_PARTICLES = frozenset("的了呢吗啊吧呀着是和与及把被对从到这那有我你他")
_ZH_TRAILING = re.compile(r"[的了呢吗啊吧呀]+$")


def normalize(text: str | None) -> str:
    return unicodedata.normalize("NFKC", text or "").casefold()


def tokenize(text: str | None) -> list[str]:
    """Return unique informative words/CJK bigrams in stable order.

    Adjacent Chinese words need no spaces; overlapping bigrams contribute only
    to a bounded coverage ratio. Repeating input cannot multiply match evidence.
    Latin identifiers retain underscores, dots, and hyphens and match whole.
    """
    text = normalize(text)
    tokens: list[str] = []
    for run in _HAN_RUN.finditer(text):
        for phrase in _ZH_SPLIT.split(run.group()):
            # Do not split single characters inside names/topics (和田, 有道,
            # 前端, 后端). Only trailing sentence particles are discarded.
            phrase = _ZH_TRAILING.sub("", phrase)
            tokens.extend(gram for index in range(len(phrase) - 1)
                          if not set(gram := phrase[index:index + 2]).issubset(_ZH_PARTICLES))
    # Splitting the scripts first keeps OpenClaw更新 from becoming one word.
    non_han = _HAN_RUN.sub(" ", text)
    # Preserve short programming-language identifiers without accepting every
    # single Latin letter as independent evidence.
    symbols = re.findall(r"(?<!\w)[a-z](?:\+\+|#)(?!\w)", non_han)
    tokens.extend(symbols)
    for word in _WORD.findall(non_han):
        if word not in _EN_FILLER and len(word) >= 2:
            tokens.append(word)
    return list(dict.fromkeys(tokens))


def field_text(note: dict, field: str) -> str:
    value = note.get(field, "")
    if isinstance(value, list):
        return " \n ".join(str(item) for item in value if item is not None)
    return "" if value is None else str(value)


def note_is_retrievable(note: dict) -> bool:
    """Honor explicit lifecycle/test metadata; never guess from a note title."""
    if note.get("active") is False or note.get("superseded_by"):
        return False
    if str(note.get("status", "")).casefold() in {"superseded", "retracted", "deleted", "inactive"}:
        return False
    if note.get("is_fixture") is True or note.get("fixture") is True:
        return False
    return str(note.get("memory_type", note.get("type", ""))).casefold() not in {"fixture", "test_fixture"}


def _contains_alias(query: str, alias: str) -> bool:
    # No substring match inside a Latin identifier (art != partial).
    alias = normalize(alias).strip()
    if not alias or not tokenize(alias):
        return False
    def identifier_char(char: str) -> bool:
        return char in "_.+-" or (char.isalnum() and not _HAN_RUN.fullmatch(char))

    for hit in re.finditer(re.escape(alias), query):
        if identifier_char(alias[0]) and hit.start() and identifier_char(query[hit.start() - 1]):
            continue
        if identifier_char(alias[-1]) and hit.end() < len(query) and identifier_char(query[hit.end()]):
            continue
        return True
    return False


def match_note(note: dict, query: str) -> tuple[float, dict]:
    """Match meaningful query coverage, independently of note frequency.

    An alias contributes only when that declared alias occurs exactly, so a long
    alias does not invent a shorter synonym. Other fields use whole word/gram
    evidence. A generic or unrelated query has zero score, regardless of dates,
    importance, prior hits, or a note's own factual-confidence label.
    """
    empty = {"matched_fields": [], "overlap_terms": [], "raw_score": 0.0,
             "confidence": "none", "query_coverage": 0.0, "match_eligible": False}
    query_terms = set(tokenize(query))
    if not query_terms or not note_is_retrievable(note):
        return 0.0, empty
    matched_fields: list[str] = []
    overlap_terms: set[str] = set()
    field_quality = 0.0
    raw_score = 0.0
    normalized_query = normalize(query)
    for field, weight in FIELD_WEIGHTS.items():
        value = field_text(note, field)
        if field == "aliases":
            aliases = note.get("aliases", [])
            if isinstance(aliases, str):
                aliases = [aliases]
            value = " \n ".join(str(alias) for alias in aliases if _contains_alias(normalized_query, str(alias))) if isinstance(aliases, list) else ""
        hits = query_terms.intersection(tokenize(value))
        if hits:
            matched_fields.append(field)
            overlap_terms.update(hits)
            raw_score += weight * len(hits) / len(query_terms)
            field_quality = max(field_quality, _FIELD_QUALITY[field])
    coverage = len(overlap_terms) / len(query_terms)
    confirmation = min(max(len(matched_fields) - 1, 0), 2) / 2
    relevance = min(1.0, coverage * (0.70 + 0.20 * field_quality + 0.10 * confirmation))
    if relevance >= 0.60 and STRONG_FIELDS.intersection(matched_fields):
        confidence = "high"
    elif relevance >= 0.30:
        confidence = "medium"
    elif relevance >= 0.15:
        confidence = "low"
    else:
        confidence = "none"
    return relevance, {
        "matched_fields": sorted(matched_fields), "overlap_terms": sorted(overlap_terms),
        "raw_score": raw_score, "confidence": confidence, "query_coverage": coverage,
        "match_eligible": confidence in {"medium", "high"},
    }
