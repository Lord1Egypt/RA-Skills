"""
news_engine.py — Fetches Google News RSS feeds and scores each item for
sentiment, event type, impact level, and time sensitivity.

Uses only stdlib + feedparser (lightweight). No API keys required.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

import feedparser
from loguru import logger

ROOT = Path(__file__).parent.parent
NEWS_LOG_PATH = ROOT / "memory" / "news_log.json"

# ── Data Model ─────────────────────────────────────────────────────────────────

@dataclass
class NewsItem:
    headline: str
    source: str
    url: str
    published: str                  # ISO8601
    summary: str
    query_topic: str
    # Scored fields (filled by analyze())
    sentiment: str = "neutral"      # bullish | bearish | neutral | risk_event
    event_type: str = "unknown"     # macroeconomic | geopolitical | corporate | commodity | currency | systemic
    impact_level: str = "low"       # low | medium | high | market_moving
    time_sensitivity: str = "long_term"  # immediate | short_term | long_term
    sentiment_score: float = 0.0    # -1.0 (very bearish) to +1.0 (very bullish)
    affected_assets: list[str] = field(default_factory=list)
    agent_reaction: str = ""        # filled after decision
    market_reaction: str = ""       # filled after observation
    trade_result: str = ""          # filled after trade closes


# ── RSS Topics ────────────────────────────────────────────────────────────────

NEWS_TOPICS = {
    "global_markets":   "stock market",
    "economy":          "economy GDP inflation",
    "federal_reserve":  "Federal Reserve interest rates",
    "inflation":        "inflation CPI",
    "geopolitics":      "geopolitics war conflict",
    "energy":           "oil gas energy prices",
    "technology":       "technology sector AI",
    "earnings":         "earnings revenue profit",
}

GOOGLE_RSS_BASE = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"


# ── Keyword Dictionaries ───────────────────────────────────────────────────────

BULLISH_KEYWORDS = [
    "surge", "rally", "gain", "record high", "beat expectations", "strong earnings",
    "growth", "upgrade", "outperform", "beat", "boom", "bullish", "recovery",
    "expansion", "positive", "profit", "revenue growth", "deal", "acquisition",
    "dividend increase", "buyback", "FDA approval",
]
BEARISH_KEYWORDS = [
    "crash", "plunge", "fall", "drop", "miss", "disappoint", "recession", "layoff",
    "bankruptcy", "downgrade", "underperform", "loss", "decline", "slump", "bear",
    "default", "crisis", "collapse", "warning", "cut", "rate hike", "inflation surge",
    "tariff", "sanction", "war", "conflict",
]
RISK_KEYWORDS = [
    "war", "conflict", "attack", "nuclear", "emergency", "collapse", "bank run",
    "systemic", "contagion", "flash crash", "circuit breaker", "halt",
]
MACRO_KEYWORDS = ["fed", "interest rate", "cpi", "gdp", "inflation", "employment", "jobs", "fomc"]
GEO_KEYWORDS = ["war", "sanctions", "geopolit", "conflict", "treaty", "election"]
CORP_KEYWORDS = ["earnings", "revenue", "ceo", "acquisition", "merger", "ipo", "layoff", "recall"]
COMMODITY_KEYWORDS = ["oil", "gold", "copper", "wheat", "gas", "commodity"]
CURRENCY_KEYWORDS = ["dollar", "yen", "euro", "forex", "exchange rate", "currency"]

ASSET_MAP = {
    "apple": "AAPL", "microsoft": "MSFT", "nvidia": "NVDA", "tesla": "TSLA",
    "amazon": "AMZN", "google": "GOOGL", "alphabet": "GOOGL", "meta": "META",
    "spy": "SPY", "s&p": "SPY", "nasdaq": "QQQ", "oil": "USO",
    "gold": "GLD", "treasury": "TLT", "bond": "TLT",
}


# ── NewsEngine ─────────────────────────────────────────────────────────────────

class NewsEngine:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.news_cfg = cfg.get("news", {})
        self.max_items_per_topic = self.news_cfg.get("max_items_per_topic", 5)
        self.fetch_timeout = self.news_cfg.get("fetch_timeout_sec", 10)
        self._cache: list[NewsItem] = []
        self._last_fetch: float = 0
        self._cache_ttl = self.news_cfg.get("cache_ttl_sec", 300)
        logger.info("NewsEngine initialized.")

    # ── Fetch ──────────────────────────────────────────────────────────────────

    def fetch_all(self) -> list[NewsItem]:
        """Fetch and analyze news from all configured topics. Cached for TTL seconds."""
        now = time.time()
        if self._cache and (now - self._last_fetch) < self._cache_ttl:
            logger.debug("Returning cached news.")
            return self._cache

        all_items: list[NewsItem] = []
        topics = self.news_cfg.get("topics", list(NEWS_TOPICS.keys()))

        for topic_key in topics:
            query = NEWS_TOPICS.get(topic_key, topic_key)
            items = self._fetch_topic(topic_key, query)
            all_items.extend(items)

        # Fetch symbol-specific news for watchlist
        for symbol in self.cfg.get("watchlist", []):
            items = self._fetch_topic(f"symbol_{symbol}", symbol)
            all_items.extend(items)

        # Analyze each item
        analyzed = [self.analyze(item) for item in all_items]

        self._cache = analyzed
        self._last_fetch = now
        logger.info(f"NewsEngine fetched {len(analyzed)} items across {len(topics)} topics.")
        return analyzed

    def _fetch_topic(self, topic_key: str, query: str) -> list[NewsItem]:
        url = GOOGLE_RSS_BASE.format(query=quote_plus(query))
        items = []
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[: self.max_items_per_topic]:
                published = entry.get("published", datetime.now(timezone.utc).isoformat())
                summary = entry.get("summary", "")
                # Strip HTML tags from summary
                summary = re.sub(r"<[^>]+>", "", summary).strip()
                items.append(NewsItem(
                    headline=entry.get("title", ""),
                    source=entry.get("source", {}).get("title", "Unknown"),
                    url=entry.get("link", ""),
                    published=published,
                    summary=summary,
                    query_topic=topic_key,
                ))
        except Exception as e:
            logger.warning(f"Failed to fetch news for '{query}': {e}")
        return items

    # ── Analysis ───────────────────────────────────────────────────────────────

    def analyze(self, item: NewsItem) -> NewsItem:
        """Score a news item for sentiment, type, impact, and time sensitivity."""
        text = (item.headline + " " + item.summary).lower()

        # Sentiment scoring
        bullish_hits = sum(1 for kw in BULLISH_KEYWORDS if kw in text)
        bearish_hits = sum(1 for kw in BEARISH_KEYWORDS if kw in text)
        risk_hits = sum(1 for kw in RISK_KEYWORDS if kw in text)

        raw_score = (bullish_hits - bearish_hits) / max(bullish_hits + bearish_hits, 1)
        item.sentiment_score = round(raw_score, 3)

        if risk_hits >= 2:
            item.sentiment = "risk_event"
            item.sentiment_score = -1.0
        elif raw_score > 0.3:
            item.sentiment = "bullish"
        elif raw_score < -0.3:
            item.sentiment = "bearish"
        else:
            item.sentiment = "neutral"

        # Event type
        if any(kw in text for kw in MACRO_KEYWORDS):
            item.event_type = "macroeconomic"
        elif any(kw in text for kw in GEO_KEYWORDS):
            item.event_type = "geopolitical"
        elif any(kw in text for kw in CORP_KEYWORDS):
            item.event_type = "corporate"
        elif any(kw in text for kw in COMMODITY_KEYWORDS):
            item.event_type = "commodity"
        elif any(kw in text for kw in CURRENCY_KEYWORDS):
            item.event_type = "currency"
        else:
            item.event_type = "general"

        # Impact level
        total_hits = bullish_hits + bearish_hits + risk_hits
        if risk_hits >= 2 or total_hits >= 6:
            item.impact_level = "market_moving"
        elif total_hits >= 4:
            item.impact_level = "high"
        elif total_hits >= 2:
            item.impact_level = "medium"
        else:
            item.impact_level = "low"

        # Time sensitivity
        immediate_words = ["breaking", "just in", "emergency", "flash", "halt", "crash", "today"]
        short_words = ["this week", "quarterly", "earnings", "report", "announced"]
        if any(w in text for w in immediate_words):
            item.time_sensitivity = "immediate"
        elif any(w in text for w in short_words):
            item.time_sensitivity = "short_term"
        else:
            item.time_sensitivity = "long_term"

        # Affected assets
        item.affected_assets = [
            ticker for name, ticker in ASSET_MAP.items() if name in text
        ]

        return item

    # ── Aggregation ────────────────────────────────────────────────────────────

    def get_market_sentiment(self, news_items: list[NewsItem]) -> dict:
        """
        Aggregate all news into a market-level sentiment snapshot.
        Returns a dict used by decision_engine.
        """
        if not news_items:
            return {"aggregate_score": 0.0, "risk_event": False, "impact": "low", "top_items": []}

        scores = [item.sentiment_score for item in news_items]
        aggregate = sum(scores) / len(scores)

        risk_event = any(item.sentiment == "risk_event" for item in news_items)
        high_impact = any(item.impact_level in ("high", "market_moving") for item in news_items)

        # Top 3 most impactful items
        ranked = sorted(news_items, key=lambda x: abs(x.sentiment_score), reverse=True)
        top = [
            {"headline": i.headline, "sentiment": i.sentiment, "score": i.sentiment_score}
            for i in ranked[:3]
        ]

        return {
            "aggregate_score": round(aggregate, 3),
            "risk_event": risk_event,
            "high_impact": high_impact,
            "impact": "market_moving" if risk_event else ("high" if high_impact else "low"),
            "top_items": top,
        }

    def get_symbol_sentiment(self, symbol: str, news_items: list[NewsItem]) -> float:
        """Return avg sentiment score for items mentioning a specific symbol."""
        relevant = [
            item for item in news_items
            if symbol in item.affected_assets or symbol.lower() in item.headline.lower()
        ]
        if not relevant:
            return 0.0
        return round(sum(i.sentiment_score for i in relevant) / len(relevant), 3)

    # ── Logging ────────────────────────────────────────────────────────────────

    def log_news(self, items: list[NewsItem]) -> None:
        """Append news items to memory/news_log.json."""
        try:
            with open(NEWS_LOG_PATH) as f:
                data = json.load(f)
        except Exception:
            data = {"news": []}

        for item in items:
            data["news"].append(asdict(item))

        # Keep last 1000 entries
        data["news"] = data["news"][-1000:]

        with open(NEWS_LOG_PATH, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def load_history(self) -> list[dict]:
        """Load historical news log for learning analysis."""
        try:
            with open(NEWS_LOG_PATH) as f:
                return json.load(f).get("news", [])
        except Exception:
            return []

    # ── Learning ───────────────────────────────────────────────────────────────

    def evaluate_news_utility(self) -> dict:
        """
        Analyze historical news vs trade results to determine which news types
        are signal vs noise. Returns utility scores by event_type.
        """
        history = self.load_history()
        closed = [h for h in history if h.get("trade_result")]

        if len(closed) < 10:
            return {}

        utility: dict[str, list[float]] = {}
        for item in closed:
            etype = item.get("event_type", "unknown")
            result = item.get("trade_result", "")
            # Parse result as +1 (profit) or -1 (loss)
            score = 1.0 if "profit" in result.lower() else -1.0 if "loss" in result.lower() else 0.0
            utility.setdefault(etype, []).append(score)

        return {
            etype: round(sum(scores) / len(scores), 3)
            for etype, scores in utility.items()
            if len(scores) >= 3
        }
