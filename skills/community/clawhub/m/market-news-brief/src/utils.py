import re
from datetime import datetime

from constants import COUNTRY_SCOPES, REGION_SCOPES


def format_number(num, decimals=2):
    """Format a number with commas and specified decimals."""
    if num is None:
        return "N/A"
    try:
        return f"{float(num):,.{decimals}f}"
    except (TypeError, ValueError):
        return "N/A"


def format_change(change, change_percent):
    """Format absolute and percentage change with direction markers."""
    if change is None or change_percent is None:
        return "-"
    if change > 0:
        return f"▲${format_number(change)} ({format_number(change_percent)}%)"
    if change < 0:
        return f"▼${format_number(abs(change))} ({format_number(change_percent)}%)"
    return f"${format_number(change)} ({format_number(change_percent)}%)"


def format_event_date(value) -> str:
    """Format a publish date into a GMT timestamp string."""
    if value is None:
        return "Unknown"
    if isinstance(value, (int, float)):
        return datetime.utcfromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S GMT")
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S GMT")

    text = str(value)
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S GMT")
    except ValueError:
        return text


def build_alias_map() -> dict:
    """Build a lookup map for canonical scope resolution."""
    alias_map = {}

    for scope_name, config in COUNTRY_SCOPES.items():
        alias_map[scope_name] = scope_name
        for alias in config["aliases"]:
            alias_map[alias.upper()] = scope_name

    for scope_name, config in REGION_SCOPES.items():
        alias_map[scope_name] = scope_name
        for alias in config["aliases"]:
            alias_map[alias.upper()] = scope_name

    return alias_map


def looks_like_bare_ticker(value: str) -> bool:
    """Detect a bare ticker that should not be auto-resolved to a market scope."""
    candidate = value.strip().upper()
    return "." not in candidate and bool(re.fullmatch(r"[A-Z0-9-]{1,10}", candidate))


def dedupe_symbol_entries(entries: list[dict]) -> list[dict]:
    """Deduplicate symbol entries while preserving order."""
    deduped = []
    seen_symbols = set()

    for entry in entries:
        symbol = entry["symbol"]
        if symbol in seen_symbols:
            continue
        seen_symbols.add(symbol)
        deduped.append(entry)

    return deduped


def dedupe_articles(articles: list[dict], limit: int) -> list[dict]:
    """Deduplicate articles by URL or title while preserving order."""
    deduped = []
    seen_titles = set()
    seen_urls = set()

    for article in articles:
        title_key = article.get("title", "").strip().lower()
        url_key = article.get("url", "").strip().lower()

        if title_key and title_key in seen_titles:
            continue
        if url_key and url_key in seen_urls:
            continue

        if title_key:
            seen_titles.add(title_key)
        if url_key:
            seen_urls.add(url_key)

        deduped.append(article)
        if len(deduped) >= limit:
            break

    return deduped


def merge_ranked_articles(
    primary_articles: list[dict], secondary_articles: list[dict], limit: int
) -> list[dict]:
    """Fill a ranked article list without introducing duplicates."""
    ranked = dedupe_articles(primary_articles, limit)
    if len(ranked) >= limit:
        return ranked[:limit]

    existing_titles = {article.get("title", "").strip().lower() for article in ranked}
    existing_urls = {
        article.get("url", "").strip().lower()
        for article in ranked
        if article.get("url")
    }

    for article in secondary_articles:
        title_key = article.get("title", "").strip().lower()
        url_key = article.get("url", "").strip().lower()

        if title_key and title_key in existing_titles:
            continue
        if url_key and url_key in existing_urls:
            continue

        ranked.append(article)
        if title_key:
            existing_titles.add(title_key)
        if url_key:
            existing_urls.add(url_key)

        if len(ranked) >= limit:
            break

    return ranked[:limit]
