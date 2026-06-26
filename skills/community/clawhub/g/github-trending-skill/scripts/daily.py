from pathlib import Path
from typing import List

from scripts.utils import fetch_html, load_cache, parse_trending, save_cache, utc_now_iso

BASE_URL = "https://github.com/trending"
CACHE_PATH = Path(__file__).resolve().parent / "cache_daily.json"


def build_url(language: str) -> str:
    if language and language.lower() != "all":
        return f"{BASE_URL}/{language}?since=daily"
    return f"{BASE_URL}?since=daily"


def format_daily(items: List[dict], language: str, limit: int) -> str:
    header = f"## GitHub Trending 日榜（UTC {utc_now_iso()}）\n"
    header += f"语言：{language if language else 'All'}\n\n"
    if not items:
        return header + "暂无数据。"
    lines = [header]
    for idx, item in enumerate(items[:limit], start=1):
        name = item.get("name") or "(unknown)"
        description = item.get("description") or "暂无描述"
        language_text = item.get("language") or "未知"
        stars_total = item.get("stars_total") or 0
        stars_today = item.get("stars_period") or 0
        lines.append(
            f"{idx}. **{name}** - {description} "
            f"(语言: {language_text}, ⭐ {stars_total}, 今日+{stars_today})"
        )
    lines.append("\n趋势标签：今日热榜")
    return "\n".join(lines)


def run(language: str = "All", limit: int = 10) -> str:
    url = build_url(language)
    try:
        html = fetch_html(url)
        items = parse_trending(html)
        payload = {
            "last_fetched": utc_now_iso(),
            "language": language,
            "items": items,
        }
        save_cache(CACHE_PATH, payload)
        return format_daily(items, language, limit)
    except Exception:
        cached = load_cache(CACHE_PATH)
        if cached and "items" in cached:
            notice = "\n\n> 网络失败，返回上一次缓存结果。"
            return format_daily(cached["items"], cached.get("language", language), limit) + notice
        return "抓取失败，请稍后再试。"


if __name__ == "__main__":
    print(run())

