# pyright: reportMissingImports=false

import yfinance as yf

from constants import (
    BROAD_MARKET_KEYWORDS,
    COUNTRY_SCOPES,
    MAX_HEADLINES,
    RAW_NEWS_FETCH_LIMIT,
    REGION_SCOPES,
    SUFFIX_SCOPE_MAP,
    THEME_KEYWORDS,
    VALID_SCOPES,
)
from utils import (
    build_alias_map,
    dedupe_symbol_entries,
    format_change,
    format_event_date,
    format_number,
    looks_like_bare_ticker,
    merge_ranked_articles,
)


ALIAS_MAP = build_alias_map()


def infer_scope_from_ticker_suffix(value: str) -> tuple[str | None, str | None]:
    """Infer a market scope from an obvious exchange suffix."""
    candidate = value.strip().upper()

    for suffix in sorted(SUFFIX_SCOPE_MAP, key=len, reverse=True):
        if candidate.endswith(suffix):
            inferred_scope = SUFFIX_SCOPE_MAP[suffix]
            return (
                inferred_scope,
                f"Inferred market scope '{inferred_scope}' from ticker suffix '{suffix}'.",
            )

    return None, None


def resolve_scope(
    requested_scope: str | None,
) -> tuple[str | None, str | None, str | None]:
    """Resolve the requested market scope or infer it from a ticker suffix."""
    if not requested_scope:
        return "GLOBAL", None, None

    normalized = requested_scope.strip().upper()
    if normalized in ALIAS_MAP:
        return ALIAS_MAP[normalized], None, None

    inferred_scope, note = infer_scope_from_ticker_suffix(normalized)
    if inferred_scope:
        return inferred_scope, note, None

    valid_scope_str = ", ".join(VALID_SCOPES)
    if looks_like_bare_ticker(normalized):
        return (
            None,
            None,
            f"Unsupported market scope '{requested_scope}'. Bare tickers are not inferred in this skill. Use a market scope such as {valid_scope_str}, or pass a ticker with an obvious exchange suffix like NOV.DE.",
        )

    return (
        None,
        None,
        f"Unsupported market scope '{requested_scope}'. Supported scopes: {valid_scope_str}. This skill also accepts exchange-suffixed tickers like NOV.DE to infer a market.",
    )


def get_scope_members(scope: str) -> list[str]:
    """Expand a canonical scope to its underlying country members."""
    if scope in COUNTRY_SCOPES:
        return [scope]
    return REGION_SCOPES[scope]["members"]


def get_scope_symbols(scope: str) -> tuple[list[dict], list[dict]]:
    """Collect snapshot and news symbols for a canonical scope."""
    members = get_scope_members(scope)
    snapshot_symbols = []
    news_symbols = []

    for member in members:
        for entry in COUNTRY_SCOPES[member]["snapshot_symbols"]:
            snapshot_symbols.append({**entry, "market": member})
        for entry in COUNTRY_SCOPES[member]["news_symbols"]:
            news_symbols.append({**entry, "market": member})

    return dedupe_symbol_entries(snapshot_symbols), dedupe_symbol_entries(news_symbols)


def parse_article(article: dict, source_entry: dict) -> dict | None:
    """Parse a Yahoo Finance news article into a stable internal shape."""
    if not isinstance(article, dict):
        return None

    content = article.get("content", {})
    if not isinstance(content, dict):
        content = {}

    title = content.get("title") or article.get("title")
    if not title:
        return None

    summary = content.get("summary") or article.get("summary") or ""
    provider = "Unknown"
    provider_info = content.get("provider")
    if isinstance(provider_info, dict):
        provider = provider_info.get("displayName") or provider
    elif article.get("publisher"):
        provider = article.get("publisher")

    click_url = content.get("clickThroughUrl")
    canonical_url = content.get("canonicalUrl")
    url = ""
    if isinstance(click_url, dict):
        url = click_url.get("url", "")
    if not url and isinstance(canonical_url, dict):
        url = canonical_url.get("url", "")
    if not url:
        url = article.get("link", "")

    published_at = content.get("pubDate") or article.get("providerPublishTime")

    return {
        "title": title,
        "summary": summary,
        "source": provider,
        "published_at": format_event_date(published_at),
        "url": url,
        "proxy_label": source_entry["label"],
        "proxy_symbol": source_entry["symbol"],
        "proxy_kind": source_entry["kind"],
        "proxy_market": source_entry["market"],
    }


def is_broad_market_article(article: dict) -> bool:
    """Prefer headlines that are clearly about overall markets or macro drivers."""
    haystack = f"{article.get('title', '')} {article.get('summary', '')}".lower()
    return any(keyword in haystack for keyword in BROAD_MARKET_KEYWORDS)


def get_market_snapshot(symbol_entries: list[dict]) -> list[dict]:
    """Fetch quote snapshots for market proxies."""
    snapshot = []

    for entry in symbol_entries:
        try:
            ticker = yf.Ticker(entry["symbol"])
            info = ticker.info or {}
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            previous_close = info.get("previousClose")
            change = (
                price - previous_close
                if price is not None and previous_close is not None
                else None
            )
            change_percent = (
                (change / previous_close) * 100
                if change is not None and previous_close not in (None, 0)
                else None
            )

            snapshot.append(
                {
                    "label": entry["label"],
                    "symbol": entry["symbol"],
                    "kind": entry["kind"],
                    "market": entry["market"],
                    "price": price,
                    "change": change,
                    "change_percent": change_percent,
                }
            )
        except Exception:
            snapshot.append(
                {
                    "label": entry["label"],
                    "symbol": entry["symbol"],
                    "kind": entry["kind"],
                    "market": entry["market"],
                    "price": None,
                    "change": None,
                    "change_percent": None,
                }
            )

    return snapshot


def collect_market_news(symbol_entries: list[dict]) -> list[dict]:
    """Collect and rank recent broad-market news from proxy symbols."""
    broad_articles = []
    fallback_articles = []

    for entry in symbol_entries:
        if entry["kind"] == "volatility":
            continue

        try:
            ticker = yf.Ticker(entry["symbol"])
            raw_news = ticker.news[:RAW_NEWS_FETCH_LIMIT] if ticker.news else []
        except Exception:
            raw_news = []

        for raw_article in raw_news:
            article = parse_article(raw_article, entry)
            if not article:
                continue
            if is_broad_market_article(article):
                broad_articles.append(article)
            else:
                fallback_articles.append(article)

    return merge_ranked_articles(broad_articles, fallback_articles, MAX_HEADLINES)


def classify_themes(articles: list[dict]) -> list[tuple[str, int]]:
    """Classify dominant news themes with simple keyword counts."""
    theme_counts = {theme: 0 for theme in THEME_KEYWORDS}

    for article in articles:
        haystack = f"{article.get('title', '')} {article.get('summary', '')}".lower()
        for theme, keywords in THEME_KEYWORDS.items():
            if any(keyword in haystack for keyword in keywords):
                theme_counts[theme] += 1

    ranked = [(theme, count) for theme, count in theme_counts.items() if count > 0]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:3]


def determine_market_tone(snapshot: list[dict]) -> str:
    """Infer a simple market tone from proxy moves and volatility context."""
    equity_changes = [
        item["change_percent"]
        for item in snapshot
        if item["kind"] != "volatility" and item["change_percent"] is not None
    ]
    avg_change = sum(equity_changes) / len(equity_changes) if equity_changes else 0

    volatility_changes = [
        item["change_percent"]
        for item in snapshot
        if item["kind"] == "volatility" and item["change_percent"] is not None
    ]
    avg_volatility_change = (
        sum(volatility_changes) / len(volatility_changes)
        if volatility_changes
        else None
    )

    if avg_change >= 0.35 and (
        avg_volatility_change is None or avg_volatility_change <= 0
    ):
        return "Risk-on"
    if avg_change <= -0.35 and (
        avg_volatility_change is None or avg_volatility_change >= 0
    ):
        return "Risk-off"
    return "Mixed"


def build_coverage_note(headlines: list[dict], news_symbols: list[dict]) -> str | None:
    """Describe sparse or proxy-heavy headline coverage."""
    if not headlines:
        return (
            "Limited recent Yahoo Finance headlines were available for this scope. "
            "Snapshot data is shown, but no broad-market headlines were found."
        )

    headline_count = len(headlines)
    source_symbol_count = len({article["proxy_symbol"] for article in headlines})
    etf_count = sum(1 for article in headlines if article["proxy_kind"] == "etf")
    index_count = sum(1 for article in headlines if article["proxy_kind"] == "index")
    expected_symbol_floor = 2 if len(news_symbols) >= 4 else 1

    if headline_count < 3 or source_symbol_count < expected_symbol_floor:
        return (
            "Limited recent Yahoo Finance headlines were available for this scope. "
            "Results may reflect a small set of market proxies."
        )

    if index_count == 0 and etf_count > 0:
        return (
            "Headline coverage for this scope is currently being supplemented by ETF proxies, "
            "so some stories may skew toward fund flows or positioning."
        )

    return None


def get_market_news_brief(requested_scope: str | None) -> dict:
    """Get a market snapshot, broad headlines, and dominant themes."""
    try:
        scope, scope_note, error = resolve_scope(requested_scope)
        if error:
            return {"error": error}
        if scope is None:
            return {
                "error": "Could not resolve a market scope from the provided input."
            }

        snapshot_symbols, news_symbols = get_scope_symbols(scope)
        snapshot = get_market_snapshot(snapshot_symbols)
        headlines = collect_market_news(news_symbols)
        themes = classify_themes(headlines)

        return {
            "scope": scope,
            "scope_note": scope_note,
            "coverage_note": build_coverage_note(headlines, news_symbols),
            "tone": determine_market_tone(snapshot),
            "snapshot": snapshot,
            "headlines": headlines,
            "themes": themes,
        }
    except Exception as exc:
        return {"error": f"Could not get market news brief: {str(exc)}"}


def format_output(data: dict) -> str:
    """Format all market news data into the final human-readable output."""
    if "error" in data:
        return f"Error: {data['error']}"

    lines = [
        f"Market News Brief: {data['scope']}",
        f"Market Tone: {data['tone']}",
    ]

    if data.get("scope_note"):
        lines.append(f"Scope Note: {data['scope_note']}")
    if data.get("coverage_note"):
        lines.append(f"Coverage Note: {data['coverage_note']}")

    lines.extend(["", "Market Snapshot:"])
    for item in data["snapshot"]:
        price = (
            f"${format_number(item['price'])}" if item["price"] is not None else "N/A"
        )
        lines.append(
            f"{item['label']} ({item['symbol']}): {price} {format_change(item['change'], item['change_percent'])}"
        )

    lines.extend(["", "Dominant Themes:"])
    if data["themes"]:
        for theme, count in data["themes"]:
            suffix = "s" if count != 1 else ""
            lines.append(f"- {theme} ({count} headline{suffix})")
    else:
        lines.append(
            "- No clear dominant themes stood out from the available headlines."
        )

    lines.extend(["", "Top Headlines:"])
    if data["headlines"]:
        for index, article in enumerate(data["headlines"], 1):
            lines.append(f"{index}. {article['title']}")
            lines.append(
                f"   Source: {article['source']} | Published: {article['published_at']} | Proxy: {article['proxy_label']}"
            )
            if article.get("url"):
                lines.append(f"   Link: {article['url']}")
    else:
        lines.append("No recent broad-market headlines found.")

    return "\n".join(lines)
