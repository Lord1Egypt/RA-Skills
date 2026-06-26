"""Storage layer — daily archive with URL-based dedup."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


DATA_DIR = Path("data")


class JsonStore:
    """Stores daily feed snapshots as JSON files under data/."""

    def __init__(self, base_dir: str | Path = DATA_DIR):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path_for_date(self, date: str) -> Path:
        """Return path like data/2026-03-01.json"""
        return self.base_dir / f"{date}.json"

    def save(self, items: list[dict[str, Any]], date: str | None = None) -> Path:
        """Save items for a given date, deduping by URL against existing data."""
        date = date or datetime.now().strftime("%Y-%m-%d")
        path = self._path_for_date(date)

        # Load existing items for today (if pipeline runs multiple times)
        existing = self._load_raw(path)
        seen_urls: set[str] = {item["url"] for item in existing if item.get("url")}

        new_items = []
        for item in items:
            url = item.get("url", "")
            if url and url in seen_urls:
                continue
            seen_urls.add(url)
            new_items.append(item)

        merged = existing + new_items

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "date": date,
                    "saved_at": datetime.now().isoformat(),
                    "count": len(merged),
                    "items": merged,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(f"   💾 Stored {len(merged)} items ({len(new_items)} new) → {path}")
        return path

    def load(self, date: str) -> list[dict[str, Any]]:
        """Load items for a specific date."""
        path = self._path_for_date(date)
        return self._load_raw(path)

    def load_range(self, start: str, end: str) -> list[dict[str, Any]]:
        """Load items across a date range (inclusive)."""
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        all_items: list[dict[str, Any]] = []

        current = start_dt
        while current <= end_dt:
            date_str = current.strftime("%Y-%m-%d")
            all_items.extend(self.load(date_str))
            current += timedelta(days=1)

        return all_items

    def _load_raw(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("items", [])
