from pathlib import Path
from typing import Dict, List

from scripts.utils import (
    fetch_html,
    load_cache,
    parse_trending,
    save_cache,
    sleep_if_needed,
    utc_now_iso,
)

BASE_URL = "https://github.com/trending"
CACHE_PATH = Path(__file__).resolve().parent / "cache_monthly.json"
DEFAULT_LANGUAGES = [
    "Python",
    "JavaScript",
    "TypeScript",
    "Go",
    "Rust",
    "Java",
    "C++",
    "C#",
    "PHP",
    "Ruby",
]


def build_url(language: str) -> str:
    if language and language.lower() != "all":
        return f"{BASE_URL}/{language}?since=monthly"
    return f"{BASE_URL}?since=monthly"


def aggregate_items(items: List[dict], stats: Dict[str, dict]) -> None:
    for item in items:
        name = item.get("name") or ""
        if not name:
            continue
        entry = stats.setdefault(
            name,
            {
                "name": name,
                "description": item.get("description") or "暂无描述",
                "language": item.get("language") or "未知",
                "count": 0,
                "stars_total": 0,
                "stars_period": 0,
            },
        )
        entry["count"] += 1
        entry["stars_period"] += int(item.get("stars_period") or 0)
        entry["stars_total"] = max(entry["stars_total"], int(item.get("stars_total") or 0))


def format_monthly(items: List[dict], language: str, limit: int, note: str = "") -> str:
    header = f"## GitHub Trending 月度汇总（UTC {utc_now_iso()}）\n"
    header += f"语言：{language if language else 'All'}\n\n"
    if not items:
        return header + "暂无数据。"
    lines = [header]
    for idx, item in enumerate(items[:limit], start=1):
        name = item.get("name") or "(unknown)"
        description = item.get("description") or "暂无描述"
        language_text = item.get("language") or "未知"
        stars_total = item.get("stars_total") or 0
        stars_period = item.get("stars_period") or 0
        count = item.get("count") or 0
        lines.append(
            f"{idx}. **{name}** - {description} "
            f"(语言: {language_text}, ⭐ {stars_total}, 本月+{stars_period}, 出现{count}次)"
        )
    lines.append("\n趋势标签：月度汇总")
    if note:
        lines.append(note)
    return "\n".join(lines)


def run(language: str = "All", limit: int = 10) -> str:
    cache = load_cache(CACHE_PATH) or {"languages": {}, "last_fetched": None}
    languages = [language] if language and language.lower() != "all" else DEFAULT_LANGUAGES
    stats: Dict[str, dict] = {}
    failed_languages = []

    for idx, lang in enumerate(languages):
        url = build_url(lang)
        try:
            html = fetch_html(url)
            items = parse_trending(html)
            cache["languages"][lang] = {
                "last_fetched": utc_now_iso(),
                "items": items,
            }
            aggregate_items(items, stats)
        except Exception:
            cached_lang = cache.get("languages", {}).get(lang)
            if cached_lang and "items" in cached_lang:
                aggregate_items(cached_lang["items"], stats)
            else:
                failed_languages.append(lang)
        if idx < len(languages) - 1:
            sleep_if_needed(3)

    cache["last_fetched"] = utc_now_iso()
    save_cache(CACHE_PATH, cache)

    ranked = sorted(
        stats.values(),
        key=lambda item: (item.get("count", 0), item.get("stars_period", 0), item.get("stars_total", 0)),
        reverse=True,
    )
    note = ""
    if failed_languages:
        note = "\n\n> 部分语言抓取失败：" + ", ".join(failed_languages)
    return format_monthly(ranked, "All" if language.lower() == "all" else language, limit, note)


if __name__ == "__main__":
    print(run())

