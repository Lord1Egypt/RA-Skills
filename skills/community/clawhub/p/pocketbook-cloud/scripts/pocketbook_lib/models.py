from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable

from .common import AmbiguousBook, NotFound, MAX_UNTRUSTED_TEXT, safe_untrusted_text

_CYR_PHONETIC = str.maketrans({
    'а':'a','б':'b','в':'w','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z',
    'и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
    'с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sh',
    'ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',
})

def normalize_text(value: Any) -> str:
    return unicodedata.normalize("NFKC", str(value or "")).strip().casefold()

def display_title(book: dict[str, Any]) -> str:
    meta = book.get("metadata") if isinstance(book.get("metadata"), dict) else {}
    return safe_untrusted_text(meta.get("title") or book.get("title") or Path(str(book.get("name") or "")).stem or "Untitled", 512)

def display_author(book: dict[str, Any]) -> str:
    meta = book.get("metadata") if isinstance(book.get("metadata"), dict) else {}
    return safe_untrusted_text(meta.get("authors") or book.get("author") or "", 512)

def display_isbn(book: dict[str, Any]) -> str:
    meta = book.get("metadata") if isinstance(book.get("metadata"), dict) else {}
    return safe_untrusted_text(meta.get("isbn") or book.get("isbn") or "", 128)

def progress_percent(book: dict[str, Any]) -> int:
    values: list[Any] = [book.get("read_percent"), book.get("percent")]
    for key in ("position", "read_position"):
        obj = book.get(key)
        if isinstance(obj, dict):
            values.append(obj.get("percent"))
    best = 0.0
    for v in values:
        if v is None or v == "":
            continue
        try:
            num = float(str(v).strip().rstrip("%"))
        except ValueError:
            continue
        if 0 < num <= 1:
            num *= 100
        best = max(best, num)
    return max(0, min(100, round(best)))

def reading_status(book: dict[str, Any]) -> str:
    raw = normalize_text(book.get("read_status"))
    p = progress_percent(book)
    if raw in {"read", "finished", "completed", "done"} or p >= 99:
        return "finished"
    if raw in {"reading", "in_progress", "in-progress"} or p > 0:
        return "reading"
    return "unread"

def book_summary(book: dict[str, Any]) -> dict[str, Any]:
    out = {
        "id": str(book.get("id") or "") or None,
        "fastHash": str(book.get("fast_hash") or "") or None,
        "title": display_title(book),
        "author": display_author(book) or None,
        "filename": safe_untrusted_text(book.get("name") or "", 512) or None,
        "format": safe_untrusted_text(book.get("format") or "", 64) or None,
        "isbn": display_isbn(book) or None,
        "bytes": book.get("bytes") if isinstance(book.get("bytes"), int) else None,
        "status": reading_status(book),
        "progressPercent": progress_percent(book),
        "drm": bool(book.get("isDrm") or book.get("is_drm")),
        "lcp": bool(book.get("isLcp") or book.get("is_lcp")),
        "updated": (book.get("read_position") or {}).get("updated") if isinstance(book.get("read_position"), dict) else None,
    }
    return {k: v for k, v in out.items() if v is not None}

def score_book(book: dict[str, Any], query: str) -> int:
    q = normalize_text(query)
    if not q:
        return 0
    ident = normalize_text(book.get("id"))
    fast = normalize_text(book.get("fast_hash"))
    title = normalize_text(display_title(book))
    author = normalize_text(display_author(book))
    name = normalize_text(book.get("name"))
    isbn = normalize_text(display_isbn(book))
    if q in {ident, fast} and q:
        return 120
    if q == title:
        return 110
    if q == name or q == isbn:
        return 108
    if q == f"{title} {author}".strip():
        return 107
    score = 0
    if q in title: score = max(score, 90)
    if q in name: score = max(score, 86)
    if q in author: score = max(score, 72)
    if q in isbn: score = max(score, 96)
    tokens = [t for t in re.split(r"\s+", q) if t]
    hay = " ".join([title, author, name, isbn])
    if tokens and all(t in hay for t in tokens):
        score = max(score, 80 + min(8, len(tokens)))
    return score

def search_books(books: Iterable[dict[str, Any]], query: str) -> list[tuple[int, dict[str, Any]]]:
    scored = [(score_book(b, query), b) for b in books]
    scored = [(s, b) for s, b in scored if s > 0]
    scored.sort(key=lambda x: (-x[0], display_title(x[1]).casefold(), display_author(x[1]).casefold()))
    return scored

def resolve_book(books: list[dict[str, Any]], query: str) -> dict[str, Any]:
    scored = search_books(books, query)
    if not scored:
        raise NotFound(f"Book not found: {query}")
    if len(scored) == 1:
        return scored[0][1]
    top_score = scored[0][0]
    second = scored[1][0]
    if top_score >= 108 and top_score - second >= 10:
        return scored[0][1]
    candidates = [book_summary(b) | {"matchScore": s} for s, b in scored[:8]]
    raise AmbiguousBook(query, candidates)

def phonetic_title_key(value: Any) -> str:
    """Conservative cross-script key for title/file-name fallback."""
    raw = normalize_text(value).translate(_CYR_PHONETIC).replace('v', 'w')
    raw = re.sub(r'[^a-z0-9]+', '', raw)
    return ''.join(ch for ch in raw if ch not in 'aeiouy')

def phonetic_title_candidates(books: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    qkey = phonetic_title_key(query)
    if len(qkey) < 4:
        return []
    matches: list[dict[str, Any]] = []
    for book in books:
        fields = [display_title(book), Path(str(book.get('name') or '')).stem]
        tokens: list[str] = []
        for field in fields:
            tokens.extend(t for t in re.split(r'(?:[^\w]+|_+)', normalize_text(field), flags=re.UNICODE) if t)
        if any(phonetic_title_key(t) == qkey for t in tokens):
            matches.append(book)
    return matches

def resolve_book_phonetic_unique(books: list[dict[str, Any]], query: str) -> dict[str, Any]:
    matches = phonetic_title_candidates(books, query)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise AmbiguousBook(query, [book_summary(b) | {'matchScore': 70} for b in matches[:8]])
    raise NotFound(f"Book not found: {query}")

def normalize_note(detail: dict[str, Any], info: dict[str, Any]) -> dict[str, Any]:
    def nested(name: str, field: str = "value") -> Any:
        obj = detail.get(name)
        return obj.get(field) if isinstance(obj, dict) else None
    quotation = detail.get("quotation") if isinstance(detail.get("quotation"), dict) else {}
    mark = detail.get("mark") if isinstance(detail.get("mark"), dict) else {}
    out = {
        "uuid": safe_untrusted_text(detail.get("uuid") or info.get("uuid"), 128),
        "type": safe_untrusted_text(nested("type") or info.get("type"), 64),
        "color": safe_untrusted_text(nested("color"), 64),
        "note": safe_untrusted_text(nested("note"), MAX_UNTRUSTED_TEXT),
        "quotation": safe_untrusted_text(quotation.get("text"), MAX_UNTRUSTED_TEXT),
        "anchor": safe_untrusted_text(mark.get("anchor"), 1024),
        "created": mark.get("created"),
        "updated": nested("note", "updated") or quotation.get("updated") or info.get("updated"),
    }
    return {k: v for k, v in out.items() if v not in (None, "")}

__all__ = ['normalize_text', 'display_title', 'display_author', 'display_isbn', 'progress_percent', 'reading_status', 'book_summary', 'score_book', 'search_books', 'resolve_book', 'phonetic_title_key', 'phonetic_title_candidates', 'resolve_book_phonetic_unique', 'normalize_note', '_CYR_PHONETIC']
