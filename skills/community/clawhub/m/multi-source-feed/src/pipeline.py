"""Aggregation pipeline — loads sources from YAML, fetches all, deduplicates, outputs merged JSON."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path

import yaml

from src.models import FeedItem
from src.sources import get_source_class
from src.store import JsonStore
from src.config import MEMO_DIR, SHOWN_URL_LOOKBACK_DAYS

# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _title_similarity(a: str, b: str) -> float:
    """Quick title similarity using SequenceMatcher (0-1)."""
    a_clean = re.sub(r"[^\w\s]", "", a.lower().strip())
    b_clean = re.sub(r"[^\w\s]", "", b.lower().strip())
    if not a_clean or not b_clean:
        return 0.0
    return SequenceMatcher(None, a_clean, b_clean).ratio()


def dedup_items(items: list[dict], sim_threshold: float = 0.65) -> list[dict]:
    """Remove duplicates by URL and by title similarity.

    When two items have similar titles, keep the one with richer content
    (longer content or more metrics).
    """
    # Phase 1: URL dedup
    seen_urls: set[str] = set()
    url_deduped: list[dict] = []
    for item in items:
        url = item.get("url", "")
        if url and url in seen_urls:
            continue
        if url:
            seen_urls.add(url)
        url_deduped.append(item)

    # Phase 2: Title similarity dedup
    keep: list[dict] = []
    dropped = 0
    for item in url_deduped:
        title = item.get("title", "")
        is_dup = False
        for existing in keep:
            if _title_similarity(title, existing.get("title", "")) >= sim_threshold:
                # Keep the one with more info (longer content + more metrics)
                item_richness = len(item.get("content", "")) + len(item.get("metrics", {}))
                existing_richness = len(existing.get("content", "")) + len(existing.get("metrics", {}))
                if item_richness > existing_richness:
                    keep.remove(existing)
                    keep.append(item)
                is_dup = True
                dropped += 1
                break
        if not is_dup:
            keep.append(item)

    if dropped:
        print(f"   🔀 Dedup: {len(items)} → {len(keep)} ({dropped} duplicates removed)")

    return keep


def _extract_urls_from_memo(path: Path) -> set[str]:
    """Extract all markdown link URLs from a memo .md file."""
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r'\[.*?\]\((https?://[^\)]+)\)', text))


def _get_shown_urls(lookback_days: int = SHOWN_URL_LOOKBACK_DAYS) -> set[str]:
    """Collect URLs from the last N days of delivered memos."""
    shown: set[str] = set()
    today = datetime.now().date()
    for i in range(1, lookback_days + 1):
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        shown |= _extract_urls_from_memo(MEMO_DIR / f"{date_str}.md")
    if shown:
        print(f"   📖 Loaded {len(shown)} shown URLs from last {lookback_days} memo(s)")
    return shown


def load_sources(config_path: str | Path = "config/sources.yaml"):
    """Read sources.yaml and instantiate enabled source objects."""
    config_path = Path(config_path)
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    sources = []
    for entry in cfg.get("sources", []):
        if not entry.get("enabled", True):
            continue
        type_name = entry["type"]
        name = entry["name"]
        # Everything except 'type', 'name', 'enabled' becomes source config.
        config = {k: v for k, v in entry.items() if k not in ("type", "name", "enabled")}
        cls = get_source_class(type_name)
        sources.append(cls(name=name, config=config))

    return sources


CRITICAL_SOURCES = {"x-main"}  # Pipeline aborts if any of these return 0 items


def run(config_path: str | Path = "config/sources.yaml", output_path: str | Path = "feed_merged.json"):
    """Fetch from all enabled sources and write merged output."""
    output_path = Path(output_path)

    # Delete stale merged file so a killed pipeline can't leave old data behind
    if output_path.exists():
        output_path.unlink()
        print("🗑️ Removed stale feed_merged.json")

    sources = load_sources(config_path)
    print(f"📡 Loaded {len(sources)} sources: {[s.name for s in sources]}")

    all_items: list[FeedItem] = []
    stats: dict[str, int] = {}

    for source in sources:
        print(f"\n🔄 Fetching: {source.name} ({source.__class__.__name__})...")
        try:
            items = source.fetch()
            all_items.extend(items)
            stats[source.name] = len(items)
            print(f"   ✅ {source.name}: {len(items)} items")
        except Exception as e:
            stats[source.name] = 0
            print(f"   ❌ {source.name} failed: {e}")

    # Critical source check — abort if any required source returned 0 items
    for cs in CRITICAL_SOURCES:
        if stats.get(cs, 0) == 0:
            print(f"\n❌ CRITICAL SOURCE '{cs}' returned 0 items — aborting pipeline")
            sys.exit(1)

    # Dedup by URL + title similarity (within today's batch)
    item_dicts = [item.to_dict() for item in all_items]
    item_dicts = dedup_items(item_dicts)

    # Cross-day dedup: remove items the user has already seen in delivered memos
    shown_urls = _get_shown_urls()
    if shown_urls:
        before = len(item_dicts)
        item_dicts = [item for item in item_dicts if not item.get("url") or item["url"] not in shown_urls]
        removed = before - len(item_dicts)
        if removed:
            print(f"   🗓️ Cross-day dedup: removed {removed} items already shown in recent memos")

    today = datetime.now().strftime("%Y-%m-%d")
    output = {
        "generated_at": datetime.now().isoformat(),
        "date": today,
        "stats": stats,
        "total_items": len(item_dicts),
        "items": item_dicts,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Saved {len(item_dicts)} items to {output_path}")

    # Write slim version for LLM memo generation (strip content/extra/tags/timestamp)
    slim_items = [
        {k: v for k, v in item.items() if k in ("source", "title", "url", "author", "metrics")}
        for item in item_dicts
    ]
    slim_output = {
        "date": today,
        "total_items": len(slim_items),
        "items": slim_items,
    }
    slim_path = output_path.parent / "feed_slim.json"
    with open(slim_path, "w", encoding="utf-8") as f:
        json.dump(slim_output, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved slim version ({len(json.dumps(slim_output))//1024}KB) to {slim_path}")

    # Archive to daily store (dedup by URL)
    store = JsonStore()
    store.save(item_dicts, date=today)

    print(f"✅ Pipeline completed for {today}")
    return output


if __name__ == "__main__":
    config = sys.argv[1] if len(sys.argv) > 1 else "config/sources.yaml"
    run(config_path=config)
