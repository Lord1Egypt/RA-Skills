from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Tuple


# Adapted from upstream core.query_parser.py

_REQUEST_PHRASES = [
    "뉴스",
    "브리핑",
    "브리핑해줘",
    "브리핑 해줘",
    "요약",
    "요약해줘",
    "요약해 줘",
    "검색",
    "검색해줘",
    "검색해 줘",
    "찾아줘",
    "찾아 줘",
    "알려줘",
    "알려 줘",
    "정리해줘",
    "정리해 줘",
    "보여줘",
    "보여 줘",
    "뽑아줘",
    "뽑아 줘",
    "체크해줘",
    "체크해 줘",
    "모아줘",
    "모아 줘",
    "보고싶어",
    "보고 싶어",
    "궁금해",
    "궁금한",
    "관련해서",
    "관련 기사",
    "관련 뉴스",
    "관련",
    "대해서",
    "대해",
    "관한",
    "중심으로",
    "위주로",
    "위주",
    "핵심만",
    "핵심",
    "동향",
]

_RECENT_TOKEN_DEFAULTS = {
    "오늘": 1,
    "금일": 1,
    "어제": 2,
    "최근": 7,
    "최신": 7,
    "요즘": 7,
    "이번주": 7,
    "이번 주": 7,
    "지난주": 14,
    "지난 주": 14,
    "일주일": 7,
    "한주": 7,
    "한 주": 7,
    "보름": 15,
    "한달": 30,
    "한 달": 30,
    "한달간": 30,
    "한 달간": 30,
}

_TOKEN_STOPWORDS = {
    "관련",
    "관련해서",
    "관련된",
    "대해",
    "대해서",
    "대한",
    "기사",
    "뉴스",
    "브리핑",
    "검색",
    "요약",
    "정리",
    "핵심",
    "동향",
    "위주",
    "중심",
    "중심으로",
    "위주로",
    "알려줘",
    "찾아줘",
    "보여줘",
    "정리해줘",
    "요약해줘",
    "브리핑해줘",
    "검색해줘",
    "해줘",
    "만",
    "최근",
    "최신",
    "오늘",
    "금일",
    "어제",
    "이번주",
    "지난주",
    "일주일",
    "한주",
    "한달",
    "한달간",
    "보름",
}

_KOREAN_PARTICLES = [
    "에서는",
    "에선",
    "으로는",
    "로는",
    "에게는",
    "한테는",
    "과는",
    "와는",
    "으로",
    "에서",
    "에게",
    "한테",
    "까지",
    "부터",
    "처럼",
    "보다",
    "마저",
    "조차",
    "이라도",
    "라도",
    "이나",
    "나",
    "은",
    "는",
    "이",
    "가",
    "을",
    "를",
    "에",
    "의",
    "과",
    "와",
    "도",
    "만",
]


def _split_query_tokens(raw: str) -> Tuple[List[str], List[str]]:
    parts = str(raw or "").split()
    if not parts:
        return [], []

    positive_words: List[str] = []
    exclude_words: List[str] = []
    for token in parts:
        if token.startswith("-"):
            if len(token) > 1:
                exclude_words.append(token[1:])
            continue
        positive_words.append(token)
    return positive_words, exclude_words


def parse_tab_query(raw: str) -> Tuple[str, List[str]]:
    positive_words, exclude_words = _split_query_tokens(raw)
    db_keyword = positive_words[0] if positive_words else ""
    return db_keyword, exclude_words


def parse_search_query(raw: str) -> Tuple[str, List[str]]:
    positive_words, exclude_words = _split_query_tokens(raw)
    search_query = " ".join(positive_words)
    return search_query, exclude_words


def build_fetch_key(search_keyword: str, exclude_words: List[str]) -> str:
    normalized_keyword = (search_keyword or "").strip().lower()
    normalized_excludes = sorted(
        {
            word.strip().lower()
            for word in (exclude_words or [])
            if isinstance(word, str) and word.strip()
        }
    )
    return f"{normalized_keyword}|{'|'.join(normalized_excludes)}"


@dataclass(frozen=True)
class QueryIntent:
    raw_query: str
    search_query: str
    db_keyword: str
    exclude_words: List[str]
    fetch_key: str
    days: int | None
    limit: int


def detect_recent_days(raw: str) -> int | None:
    lowered = str(raw or "").lower()

    import re

    patterns = [
        r"최근\s*(\d+)\s*일",
        r"(\d+)\s*일\s*(내|이내)",
        r"최근\s*(\d+)\s*주",
        r"(\d+)\s*주\s*(내|이내)",
        r"최근\s*(\d+)\s*(?:개월|달)",
        r"(\d+)\s*(?:개월|달)\s*(내|이내)",
    ]
    for pattern in patterns:
        m = re.search(pattern, raw)
        if not m:
            continue
        value = int(m.group(1))
        if "주" in pattern:
            value *= 7
        elif "개월" in pattern or "달" in pattern:
            value *= 30
        return max(1, min(365, value))

    for token, days in _RECENT_TOKEN_DEFAULTS.items():
        if token in raw:
            return days
    if "today" in lowered:
        return 1
    if "this week" in lowered or "recent" in lowered or "latest" in lowered:
        return 7
    if "last week" in lowered:
        return 14
    return None


def _normalize_spacing(raw: str) -> str:
    import re

    text = str(raw or "").strip()
    text = re.sub(r"[\[\]\(\){}<>\"'“”‘’,:;!?/~`]+", " ", text)
    text = text.replace("·", " ").replace("…", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _apply_exclude_phrases(raw: str) -> str:
    import re

    text = _normalize_spacing(raw)
    patterns = [
        r"([가-힣A-Za-z0-9+#./_-]+(?:\s+[가-힣A-Za-z0-9+#./_-]+){0,2})\s*(?:말고|빼고|제외|제외하고|제외한|없이)",
        r"([가-힣A-Za-z0-9+#./_-]+(?:\s+[가-힣A-Za-z0-9+#./_-]+){0,2})\s*(?:은|는|을|를)?\s*빼면",
    ]

    def repl(match: re.Match[str]) -> str:
        words = [w for w in match.group(1).split() if w]
        if not words:
            return " "
        return " " + " ".join(f"-{word}" for word in words) + " "

    for pattern in patterns:
        text = re.sub(pattern, repl, text)
    return _normalize_spacing(text)


def _strip_particle(token: str) -> str:
    stripped = token.strip()
    if stripped.startswith("-"):
        head = "-"
        stripped = stripped[1:]
    else:
        head = ""

    if not stripped:
        return token

    for particle in _KOREAN_PARTICLES:
        if stripped.endswith(particle) and len(stripped) > len(particle) + 1:
            stripped = stripped[: -len(particle)]
            break
    return head + stripped


def _normalize_token(token: str) -> str:
    import re

    token = _strip_particle(token)
    token = token.strip("- ") if token == "-" else token.strip()
    token = re.sub(r"^[^\w가-힣+#]+|[^\w가-힣+#-]+$", "", token)
    token = token.strip()
    if token.startswith("-"):
        body = token[1:].strip()
        body = re.sub(r"^[^\w가-힣+#]+|[^\w가-힣+#-]+$", "", body)
        return f"-{body}" if body else ""
    return token


def clean_natural_query(raw: str) -> str:
    import re

    stripped = _apply_exclude_phrases(raw)

    for token in _REQUEST_PHRASES:
        stripped = stripped.replace(token, " ")

    stripped = re.sub(r"\b(today|latest|recent|this week|last week)\b", " ", stripped, flags=re.IGNORECASE)
    stripped = re.sub(r"최근\s*\d+\s*(?:일|주|개월|달)", " ", stripped)
    stripped = re.sub(r"\d+\s*(?:일|주|개월|달)\s*(?:내|이내)", " ", stripped)
    stripped = re.sub(r"(?:일주일|한\s*주|한\s*달|한달|보름|이번\s*주|지난\s*주)", " ", stripped)
    stripped = re.sub(r"\b\d+\b", " ", stripped)
    stripped = _normalize_spacing(stripped)

    normalized_tokens: List[str] = []
    for raw_token in stripped.split():
        negative = raw_token.startswith("-")
        body = raw_token[1:] if negative else raw_token
        body = re.sub(r"^[^\w가-힣+#]+|[^\w가-힣+#]+$", "", body)
        body = _strip_particle(body).strip()
        body = body.strip("- ")
        if not body or body in _TOKEN_STOPWORDS:
            continue
        token = f"-{body}" if negative else body
        normalized_tokens.append(token)

    deduped: List[str] = []
    seen = set()
    for token in normalized_tokens:
        key = token.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(token)
    return " ".join(deduped)


def build_intent(raw_query: str, *, limit: int = 10, days: int | None = None) -> QueryIntent:
    cleaned = clean_natural_query(raw_query)
    detected_days = days if days is not None else detect_recent_days(raw_query)
    search_query, exclude_words = parse_search_query(cleaned)
    db_keyword, _ = parse_tab_query(cleaned)
    if not search_query:
        raise ValueError("최소 1개 이상의 일반 키워드가 필요합니다.")
    return QueryIntent(
        raw_query=raw_query,
        search_query=search_query,
        db_keyword=db_keyword or search_query,
        exclude_words=exclude_words,
        fetch_key=build_fetch_key(search_query, exclude_words),
        days=detected_days,
        limit=max(1, min(100, int(limit))),
    )


def cutoff_iso(days: int | None, now: datetime | None = None) -> str | None:
    if not days:
        return None
    base = now or datetime.now()
    return (base - timedelta(days=days)).isoformat(timespec="seconds")
