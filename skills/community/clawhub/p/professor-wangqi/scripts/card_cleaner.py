"""
Knowledge-card cleaning helpers.

These helpers are intentionally conservative:
- prefer removing obvious noise over fabricating new content
- use source_file as fallback when title/author extraction is clearly broken
- turn generic template knowledge points into more specific, source-backed ones
"""

from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


TITLE_LABEL_BLACKLIST = {
    "review article",
    "original article",
    "research article",
    "short communication",
    "case report",
    "editorial",
    "letter to editor",
    "commentary",
    "perspective",
    "brief communication",
    "research paper",
    "full paper",
    "extended abstract",
    "position paper",
    "white paper",
    "technical report",
    "access this article online",
    "quick response code",
    "from cas & cae members",
    "cas & cae members",
}

JOURNAL_SUFFIXES_ZH = ("杂志", "学报", "期刊")
JOURNAL_HINTS_EN = ("journal", "medicine", "med", "review")

AUTHOR_NOISE_TOKENS = {
    "cnki",
    "unknown",
    "administrator",
    "admin",
    "author",
    "guest",
    "system",
    "test",
    "website",
    "correspondence",
    "email",
    "e-mail",
    "doi",
    "quick",
    "response",
    "code",
}

AUTHOR_INSTITUTION_HINTS = {
    "university",
    "college",
    "institute",
    "hospital",
    "school",
    "department",
    "center",
    "centre",
    "laboratory",
    "faculty",
    "academy",
    "beijing",
    "china",
    "medical",
    "medicine",
    "research",
    "national",
    "provincial",
    "municipal",
}

CHINESE_INSTITUTION_HINTS = (
    "大学",
    "医院",
    "研究院",
    "研究所",
    "学院",
    "朝阳区",
    "海淀区",
    "北京市",
    "邮编",
    "电话",
    "邮箱",
    "通讯",
    "地址",
)

GENERIC_KP_PREFIXES = (
    "本文涉及",
    "本文研究",
    "本文讨论",
    "本文分析",
    "本文探讨",
    "研究主题涉及",
)

NOISE_TEXT_PATTERNS = [
    r"grant\s*no",
    r"supported\s*by",
    r"funded\s*by",
    r"author contributions?",
    r"acknowledg",
    r"conflicts? of interest",
    r"availability of data",
    r"supplementary material",
    r"\babbreviations?\b",
    r"the online version contains",
    r"correspondence",
    r"received:\s*\d",
    r"https?://",
    r"www\.",
    r"\bdoi\b",
    r"电子邮箱|邮箱|邮编|电话",
]

TRAILING_SECTION_MARKERS = [
    "abbreviations",
    "keywords",
    "references",
    "acknowledgements",
    "acknowledgments",
    "author contributions",
    "funding",
    "availability of data",
    "competing interests",
    "declarations",
    "supplementary material",
    "the online version contains",
    "publisher’s note",
    "publisher's note",
    "参考文献",
    "致谢",
    "附录",
]


def normalize_spaces(text: str) -> str:
    """Normalize mixed unicode spaces and broken line wraps."""
    if not text:
        return ""
    text = (
        text.replace("\u00a0", " ")
        .replace("\u200b", "")
        .replace("\ufeff", "")
        .replace("\t", " ")
    )
    text = re.sub(r"[ \xa0]+", " ", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_text_block(text: str) -> str:
    """Normalize a free-text block and trim obvious reference tails."""
    if not text:
        return ""
    cleaned = normalize_spaces(text)
    lower = cleaned.lower()

    cutoff = len(cleaned)
    for marker in TRAILING_SECTION_MARKERS:
        idx = lower.find(marker.lower())
        if idx != -1 and idx > 80:
            cutoff = min(cutoff, idx)

    cleaned = cleaned[:cutoff].strip()
    return cleaned


def filename_title_fallback(source_file: str) -> str:
    """Derive a cleaner title from source file name."""
    if not source_file:
        return ""

    title = Path(source_file).stem
    title = re.sub(r"^[\d\s._-]+", "", title)
    title = re.sub(r"_[\u4e00-\u9fff]{2,4}$", "", title)
    title = title.replace("_", " ").replace("-", " ")
    title = normalize_spaces(title)
    return title


def filename_author_fallback(source_file: str) -> str:
    """Try to read a Chinese trailing author name from the source file."""
    stem = Path(source_file).stem
    match = re.search(r"_([\u4e00-\u9fff]{2,4})$", stem)
    return match.group(1) if match else ""


def title_is_placeholder(title: str) -> bool:
    """Detect obviously broken titles."""
    if not title:
        return True

    candidate = normalize_spaces(title)
    lower = candidate.lower()

    if lower in TITLE_LABEL_BLACKLIST:
        return True

    if re.fullmatch(r"[•·●▪▫◦○\s\d\-–—_()（）]+", candidate):
        return True

    if "•" in candidate and sum(ch.isalpha() or "\u4e00" <= ch <= "\u9fff" for ch in candidate) < 3:
        return True

    if re.search(r"\bet\s+al\.", lower) and re.search(r"\(\d{4}\)", candidate):
        return True

    if re.search(r"\b(page|vol\.?|no\.?|pp\.)\b", lower):
        return True

    if len(candidate) <= 12 and candidate.endswith(JOURNAL_SUFFIXES_ZH):
        return True

    if len(candidate) <= 40 and any(hint in lower for hint in JOURNAL_HINTS_EN) and "et al." not in lower:
        words = re.findall(r"[A-Za-z]+", candidate)
        if len(words) <= 4:
            return True

    alnum_count = sum(ch.isalnum() or ("\u4e00" <= ch <= "\u9fff") for ch in candidate)
    special_count = sum(not ch.isalnum() and not ch.isspace() and not ("\u4e00" <= ch <= "\u9fff") for ch in candidate)
    if len(candidate) > 0 and alnum_count / len(candidate) < 0.45:
        return True
    if len(candidate) > 0 and special_count / len(candidate) > 0.4:
        return True

    return False


def clean_title(title: str, source_file: str = "") -> str:
    """Normalize title and fallback to source_file when needed."""
    candidate = normalize_spaces(title)
    candidate = re.sub(r"^[•·●▪▫◦○\s\-–—_]+", "", candidate)
    candidate = re.sub(r"[•·●▪▫◦○\s\-–—_]+$", "", candidate)
    candidate = re.sub(r"^page\s+\d+\s+of\s+\d+\s*", "", candidate, flags=re.IGNORECASE)
    candidate = candidate.strip("：:;；,.，。()（）[]【】")

    if title_is_placeholder(candidate):
        fallback = filename_title_fallback(source_file)
        return fallback or candidate

    return candidate


def _looks_like_chinese_name(token: str) -> bool:
    token = token.strip()
    if not token:
        return False
    if any(hint in token for hint in CHINESE_INSTITUTION_HINTS):
        return False
    return bool(re.fullmatch(r"[\u4e00-\u9fff·]{2,8}", token))


def _looks_like_english_name(token: str, title_words: Iterable[str]) -> bool:
    token = token.strip()
    if not token:
        return False

    if any(char.isdigit() for char in token):
        return False

    if any(hint in token.lower() for hint in AUTHOR_INSTITUTION_HINTS):
        return False

    parts = [part for part in re.split(r"\s+", token) if part]
    if not parts or len(parts) > 4:
        return False

    if any(part.lower() in AUTHOR_NOISE_TOKENS for part in parts):
        return False

    if all(part.lower() in set(title_words) for part in parts):
        return False

    for part in parts:
        if not re.fullmatch(r"[A-Za-z][A-Za-z'.-]{0,30}", part):
            return False

    return any(part[0].isupper() for part in parts)


def clean_authors(authors: object, source_file: str = "", title: str = "") -> List[str]:
    """Filter institution/address noise from authors."""
    raw_items: List[str] = []

    if isinstance(authors, str):
        raw_items = [authors]
    elif isinstance(authors, list):
        raw_items = [item for item in authors if isinstance(item, str)]

    split_items: List[str] = []
    for item in raw_items:
        normalized = normalize_spaces(item)
        normalized = re.sub(r"^(作者|Authors?|通讯作者)[：:]\s*", "", normalized, flags=re.IGNORECASE)
        if not normalized:
            continue
        split_items.extend(re.split(r"[;,，、；]+", normalized))

    title_words = {word.lower() for word in re.findall(r"[A-Za-z]+", title)}
    cleaned: List[str] = []
    removed_noise_count = 0

    for item in split_items:
        candidate = normalize_spaces(item)
        candidate = re.sub(r"[\d\*＊†‡§¶]+", "", candidate).strip("：:;；,.，。[]【】()（） ")

        if not candidate:
            continue

        lower = candidate.lower()
        if (
            "@" in candidate
            or re.search(r"e-?mail", lower)
            or re.search(r"https?://|www\.", lower)
            or re.search(r"电话|邮编|地址", candidate)
            or any(hint in lower for hint in AUTHOR_INSTITUTION_HINTS)
            or any(hint in candidate for hint in CHINESE_INSTITUTION_HINTS)
            or lower in AUTHOR_NOISE_TOKENS
        ):
            removed_noise_count += 1
            continue

        if _looks_like_chinese_name(candidate) or _looks_like_english_name(candidate, title_words):
            cleaned.append(candidate)
        else:
            removed_noise_count += 1

    deduped: List[str] = []
    seen = set()
    for author in cleaned:
        key = author.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(author)

    fallback_author = filename_author_fallback(source_file)
    if fallback_author:
        if not deduped:
            deduped = [fallback_author]
        elif removed_noise_count > 0 and fallback_author not in deduped and len(deduped) <= 1:
            deduped = [fallback_author]

    return deduped


def is_generic_knowledge_point(content: str) -> bool:
    """Check whether a knowledge point is a low-information template."""
    candidate = normalize_spaces(content)
    if not candidate:
        return True

    if any(candidate.startswith(prefix) for prefix in GENERIC_KP_PREFIXES):
        return True

    if len(candidate) < 8:
        return True

    if len(candidate) < 12 and not any(
        token in candidate for token in ("方", "汤", "散", "丸", "治疗", "治法", "辨证", "体质", "问卷", "量表")
    ):
        return True

    return False


def _is_noise_sentence(sentence: str) -> bool:
    sentence = normalize_spaces(sentence)
    if not sentence:
        return True

    if len(sentence) < 8 or len(sentence) > 260:
        return True

    lower = sentence.lower()
    if any(re.search(pattern, lower, flags=re.IGNORECASE) for pattern in NOISE_TEXT_PATTERNS):
        return True

    if re.search(r"^\d+[\.\)]", sentence):
        return True

    digit_ratio = sum(ch.isdigit() for ch in sentence) / max(1, len(sentence))
    if digit_ratio > 0.35:
        return True

    acronym_tokens = re.findall(r"\b[A-Z]{2,}\b", sentence)
    if len(acronym_tokens) >= 4 and sum(ch.islower() for ch in sentence) < 10:
        return True

    return False


def split_sentences(text: str) -> List[str]:
    """Split a text block into candidate sentences."""
    normalized = clean_text_block(text)
    if not normalized:
        return []

    parts = re.split(r"(?<=[。！？；!?])\s*|(?<=[.])\s+(?=[A-Z])", normalized)
    sentences = []
    for part in parts:
        candidate = normalize_spaces(part).strip("；;,.，。 ")
        if candidate:
            sentences.append(candidate)
    return sentences


def _infer_category(sentence: str, source_type: str, default: str) -> str:
    lower = sentence.lower()
    if any(token in sentence for token in ("辨证", "辨体", "证候", "诊疗模式")):
        return "diagnosis"
    if any(token in sentence for token in ("方", "汤", "散", "丸", "治法", "治疗原则")):
        return "treatment"
    if any(token in lower for token in ("machine learning", "automated", "questionnaire", "问卷", "量表", "sample", "纳入", "调查")):
        return "method"
    if source_type == "clinical_experience":
        return "insight" if default == "finding" else default
    return default


def _infer_evidence_level(category: str, source_type: str) -> str:
    if source_type == "clinical_experience":
        return "C"
    if category in {"finding", "method"}:
        return "B"
    return "C"


def _add_point(points: List[Dict], seen: set, category: str, content: str, source_type: str, importance: str = "high") -> None:
    candidate = normalize_spaces(content)
    if _is_noise_sentence(candidate) or is_generic_knowledge_point(candidate):
        return

    key = re.sub(r"\W+", "", candidate).lower()
    if key in seen:
        return

    seen.add(key)
    points.append(
        {
            "category": _infer_category(candidate, source_type, category),
            "content": candidate,
            "importance": importance,
            "evidence_level": _infer_evidence_level(category, source_type),
        }
    )


def build_knowledge_points(card: Dict) -> List[Dict]:
    """Build cleaner, more specific knowledge points from existing fields."""
    source_type = card.get("source_type", "paper")
    points: List[Dict] = []
    seen = set()

    for kp in card.get("knowledge_points", []):
        if not isinstance(kp, dict):
            continue
        content = kp.get("content", "")
        if is_generic_knowledge_point(content):
            continue
        _add_point(
            points,
            seen,
            kp.get("category", "finding"),
            content,
            source_type,
            kp.get("importance", "high"),
        )

    for item in card.get("evidence_sentences", []):
        if isinstance(item, dict):
            _add_point(points, seen, "finding", item.get("sentence", ""), source_type, "high")

    structured_sources: List[Tuple[str, str]] = []
    if source_type == "clinical_experience":
        diagnostic = card.get("diagnostic_approach", {}) or {}
        treatment = card.get("treatment_approach", {}) or {}
        if diagnostic.get("key_points"):
            structured_sources.append(("diagnosis", f"辨证要点：{diagnostic['key_points']}"))
        if treatment.get("principle"):
            structured_sources.append(("treatment", f"治疗原则为{treatment['principle']}。"))
        if treatment.get("main_formula"):
            structured_sources.append(("treatment", f"核心方药为{treatment['main_formula']}。"))
        herbs = treatment.get("herbs", [])
        if herbs:
            structured_sources.append(("treatment", f"常用药物包括{'、'.join(herbs[:8])}。"))

    for category, content in structured_sources:
        _add_point(points, seen, category, content, source_type, "high")

    text_sources = [
        ("finding", card.get("conclusions", "")),
        ("finding", card.get("abstract", "")),
        ("insight", card.get("clinical_insights", "")),
    ]

    for category, text in text_sources:
        for sentence in split_sentences(text):
            _add_point(points, seen, category, sentence, source_type, "high")
            if len(points) >= 8:
                return points[:8]

    if not points:
        related_constitutions = card.get("related_constitutions", [])
        related_diseases = card.get("related_diseases", [])
        if related_constitutions:
            _add_point(
                points,
                seen,
                "theory",
                f"研究重点涉及{ '、'.join(related_constitutions[:4]) }等体质类型。",
                source_type,
                "medium",
            )
        if related_diseases:
            _add_point(
                points,
                seen,
                "finding",
                f"文章围绕{ '、'.join(related_diseases[:4]) }等疾病与体质关系展开。",
                source_type,
                "medium",
            )

    return points[:8]


def clean_evidence_sentences(evidence_sentences: object) -> List[Dict]:
    """Deduplicate and remove low-value evidence sentences."""
    if not isinstance(evidence_sentences, list):
        return []

    cleaned: List[Dict] = []
    seen = set()

    for item in evidence_sentences:
        if not isinstance(item, dict):
            continue

        sentence = normalize_spaces(item.get("sentence", ""))
        if _is_noise_sentence(sentence):
            continue

        key = re.sub(r"\W+", "", sentence).lower()
        if key in seen:
            continue
        seen.add(key)

        cleaned.append(
            {
                "sentence": sentence,
                "section": item.get("section", "main_text"),
                "claim_type": item.get("claim_type", "statement"),
                "page_num": item.get("page_num"),
            }
        )

    return cleaned


def _dedupe_str_list(values: object) -> List[str]:
    if not isinstance(values, list):
        return []
    result: List[str] = []
    seen = set()
    for value in values:
        if not isinstance(value, str):
            continue
        cleaned = normalize_spaces(value)
        if not cleaned:
            continue
        if cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result


def clean_card(card: Dict) -> Tuple[Dict, Dict]:
    """Clean a knowledge card and return a simple change summary."""
    cleaned = copy.deepcopy(card)
    changes: Dict[str, Dict[str, object]] = {}

    def update_field(field: str, new_value: object) -> None:
        old_value = cleaned.get(field)
        if old_value != new_value:
            changes[field] = {"before": old_value, "after": new_value}
            cleaned[field] = new_value

    source_file = cleaned.get("source_file", "")

    update_field("title", clean_title(cleaned.get("title", ""), source_file))
    update_field(
        "authors",
        clean_authors(
            cleaned.get("authors", []),
            source_file=source_file,
            title=cleaned.get("title", ""),
        ),
    )

    for field in ("abstract", "conclusions", "clinical_insights", "journal"):
        if field in cleaned:
            text = cleaned.get(field, "")
            if field == "journal":
                text = normalize_spaces(text)
                text = re.sub(r",?\s*https?://\S+", "", text, flags=re.IGNORECASE).strip(" ,")
            else:
                text = clean_text_block(text)
            update_field(field, text)

    update_field("related_constitutions", _dedupe_str_list(cleaned.get("related_constitutions", [])))
    update_field("related_diseases", _dedupe_str_list(cleaned.get("related_diseases", [])))
    update_field("evidence_sentences", clean_evidence_sentences(cleaned.get("evidence_sentences", [])))
    update_field("knowledge_points", build_knowledge_points(cleaned))

    return cleaned, {
        "changed_fields": list(changes.keys()),
        "changes": changes,
    }
