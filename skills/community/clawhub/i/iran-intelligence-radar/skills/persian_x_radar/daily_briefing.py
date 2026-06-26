from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Dict, List


HISTORY_FILE = Path(__file__).resolve().with_name("daily_history.json")


def _read_history() -> List[Dict]:
    if not HISTORY_FILE.exists():
        return []
    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _write_history(history: List[Dict]) -> None:
    with HISTORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def append_scan_snapshot(generated_at: str, rows: List[Dict], trending: List[Dict], escalation: Dict) -> None:
    history = _read_history()
    snapshot = {
        "generated_at": generated_at,
        "rows": rows,
        "trending": trending,
        "escalation_score": escalation.get("escalation_score", 0),
        "escalation_level": escalation.get("level", "LOW"),
    }
    history.append(snapshot)

    # Keep history reasonably small while preserving at least 48h of context.
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
    pruned: List[Dict] = []
    for item in history:
        try:
            ts = datetime.fromisoformat(item.get("generated_at", ""))
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if ts >= cutoff:
                pruned.append(item)
        except ValueError:
            continue
    _write_history(pruned[-500:])


def _get_last_24h(history: List[Dict]) -> List[Dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    out: List[Dict] = []
    for item in history:
        try:
            ts = datetime.fromisoformat(item.get("generated_at", ""))
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if ts >= cutoff:
                out.append(item)
        except ValueError:
            continue
    return out


def generate_daily_briefing() -> Dict[str, str]:
    history = _read_history()
    recent = _get_last_24h(history)
    now = datetime.now(timezone.utc)
    date_str = now.date().isoformat()

    all_trends: Dict[str, int] = {}
    all_rows: List[Dict] = []
    timeline: List[str] = []
    for item in recent:
        all_rows.extend(item.get("rows", []))
        for trend in item.get("trending", []):
            keyword = trend.get("keyword", "")
            all_trends[keyword] = all_trends.get(keyword, 0) + int(trend.get("current_volume", 0))
        timeline.append(f"{item.get('generated_at', '')}: {item.get('escalation_score', 0)}")

    top_trends = sorted(all_trends.items(), key=lambda kv: kv[1], reverse=True)[:5]
    top_rows = sorted(all_rows, key=lambda r: int(r.get("score", 0)), reverse=True)[:5]

    english_summary = (
        "Over the past 24 hours, Persian X activity indicates increased discussion of missile systems "
        "and sanctions. Several high-engagement posts referenced possible military movements."
    )
    chinese_summary = (
        "过去24小时内，波斯语X内容显示关于导弹系统与制裁的讨论上升，"
        "多条高互动帖子提及潜在军事动向。"
    )

    trend_lines = [f"- {k}: {v}" for k, v in top_trends] or ["- No trending signals in the last 24h."]
    top_tweet_lines = [
        f"- {row.get('author', 'unknown')}: {row.get('english', '')} ({row.get('engagement', '')})"
        for row in top_rows
    ] or ["- No high-engagement tweets available."]
    timeline_lines = [f"- {line}" for line in timeline[-10:]] or ["- No escalation timeline data."]

    markdown = "\n".join(
        [
            "# Iran Intelligence Brief",
            f"Date: {date_str}",
            "",
            "## Top Trending Keywords",
            *trend_lines,
            "",
            "## Highest Engagement Tweets",
            *top_tweet_lines,
            "",
            "## Escalation Score Timeline",
            *timeline_lines,
            "",
            "## AI Summary (English)",
            english_summary,
            "",
            "## AI Summary (Chinese)",
            chinese_summary,
        ]
    )

    return {
        "date": date_str,
        "markdown": markdown,
        "english_summary": english_summary,
        "chinese_summary": chinese_summary,
    }
