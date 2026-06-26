"""
Nex Life Logger - AI Summarizer
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Generates hierarchical summaries:
  daily  -> from raw activities
  weekly -> from daily summaries
  monthly -> from weekly summaries
  yearly -> from monthly summaries
"""
import json
import datetime as dt
import logging
import time
from openai import OpenAI
from pathlib import Path
from config import (
    AI_API_KEY, AI_API_BASE, AI_MODEL, DATA_DIR,
    API_MIN_INTERVAL, API_MAX_RETRIES, API_BACKOFF_BASE,
)
from storage import (
    get_activities,
    save_summary,
    get_summary,
    get_summaries_in_range,
    get_transcripts_for_period,
    save_keywords,
)
from keyword_extractor import extract_from_summary, extract_from_transcript

log = logging.getLogger("life-logger.summarizer")

_last_api_call = 0.0


def _get_llm_settings():
    """Read LLM settings from llm_settings.json. Falls back to env vars.
    Returns (api_key, api_base, model). All empty strings if not configured.
    No default endpoints are ever used - the user must explicitly configure."""
    api_key = ""
    api_base = ""
    model = ""
    settings_path = DATA_DIR / "llm_settings.json"
    try:
        if settings_path.exists():
            s = json.loads(settings_path.read_text("utf-8"))
            api_key = s.get("api_key", "")
            api_base = s.get("api_base", "")
            model = s.get("model", "")
    except Exception:
        pass
    # Only fall back to env vars, never to hardcoded defaults
    if not api_key:
        api_key = AI_API_KEY
    if not api_base:
        api_base = AI_API_BASE
    if not model:
        model = AI_MODEL
    return api_key, api_base, model


def is_llm_configured():
    """Check if the user has explicitly configured an LLM provider."""
    api_key, api_base, model = _get_llm_settings()
    # Require both an API key and a base URL to be set
    return bool(api_key) and bool(api_base) and bool(model)


def _client():
    api_key, api_base, _ = _get_llm_settings()
    if not api_key or not api_base:
        raise RuntimeError(
            "No LLM configured. Run 'nex-life-logger config set-api-key' "
            "and 'nex-life-logger config set-provider <name>' first. "
            "No external API calls are made until you explicitly configure a provider."
        )
    return OpenAI(api_key=api_key, base_url=api_base)


def _call_ai(system_prompt, user_content, max_tokens=2048):
    global _last_api_call
    _, _, model = _get_llm_settings()
    elapsed = time.time() - _last_api_call
    if elapsed < API_MIN_INTERVAL:
        time.sleep(API_MIN_INTERVAL - elapsed)
    client = _client()
    for attempt in range(API_MAX_RETRIES):
        try:
            _last_api_call = time.time()
            resp = client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
            )
            content = resp.choices[0].message.content
            if content is None:
                raise ValueError("API returned empty response")
            return content
        except Exception as e:
            wait = API_BACKOFF_BASE ** (attempt + 1)
            log.warning("API call failed (attempt %d/%d): %s", attempt + 1, API_MAX_RETRIES, e)
            if attempt < API_MAX_RETRIES - 1:
                log.info("Retrying in %ds...", wait)
                time.sleep(wait)
            else:
                raise


def _format_activities(activities):
    if not activities:
        return "(no activity recorded)"
    lines = []
    for a in activities:
        ts = a["timestamp"][:19]
        kind = a["kind"]
        title = a.get("title", "")
        url = a.get("url", "")
        extra = {}
        try:
            extra = json.loads(a.get("extra", "{}") or "{}")
        except Exception:
            pass
        if kind == "search":
            query = extra.get("search_query", "")
            lines.append('[%s] SEARCH: "%s"' % (ts, query))
        elif kind == "youtube":
            vid = extra.get("video_id", "")
            lines.append('[%s] YOUTUBE: "%s" (video: %s)' % (ts, title, vid))
        elif kind == "app_focus":
            proc = extra.get("process", "")
            lines.append("[%s] APP: %s - %s" % (ts, proc, title))
        else:
            domain = ""
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).hostname or ""
            except Exception:
                pass
            lines.append("[%s] WEB: %s - %s" % (ts, domain, title))
    return "\n".join(lines)


DAILY_SYSTEM = """You are a personal life-logger assistant. You will receive a log of
someone's computer activities for one day (websites visited, searches made,
YouTube videos watched, applications used). Private chats have already been
filtered out.

Write a concise but informative summary of their day. Group related activities
together (e.g., "research session on X", "watched Y videos about Z",
"worked on project A in VS Code"). Note patterns, topics of interest, and
how they spent their time. Be specific about topics, not just "browsed the web".

When YouTube transcripts are provided, use them to give detailed insight into
what was actually learned from each video.

Note: only productive content is tracked (AI, programming, design, building).
Politics, news, and entertainment have already been filtered out.

Format: 2-4 short paragraphs. Use a warm, observational tone.
End with a brief "highlights" or "main themes" sentence."""

WEEKLY_SYSTEM = """You are a personal life-logger assistant. You will receive daily summaries
for one week. Write a weekly summary that:
1. Identifies recurring themes and interests across the week
2. Notes any new topics or projects that emerged
3. Highlights how time was distributed
4. Notes any trends or shifts in focus

Format: 3-5 short paragraphs. Keep it insightful and personal."""

MONTHLY_SYSTEM = """You are a personal life-logger assistant. You will receive weekly summaries
for one month. Write a monthly summary that:
1. Identifies the major themes and projects of the month
2. Shows how interests evolved over the 4-5 weeks
3. Highlights accomplishments or milestones
4. Notes any new directions or abandoned interests

Format: 4-6 paragraphs. Reflective and slightly more analytical."""

YEARLY_SYSTEM = """You are a personal life-logger assistant. You will receive monthly summaries
for one year. Write a comprehensive yearly summary that:
1. Maps the arc of the year
2. Identifies the biggest themes and interests
3. Notes personal growth or evolving expertise areas
4. Highlights the most significant activities or discoveries

Format: A thoughtful 5-8 paragraph review of the year."""


def generate_daily_summary(date):
    existing = get_summary("daily", date.isoformat())
    if existing:
        log.info("Daily summary for %s already exists, skipping", date)
        return existing
    start = dt.datetime.combine(date, dt.time.min, tzinfo=dt.timezone.utc).isoformat()
    end = dt.datetime.combine(date + dt.timedelta(days=1), dt.time.min, tzinfo=dt.timezone.utc).isoformat()
    activities = get_activities(start, end)
    if not activities:
        log.info("No activities for %s, skipping summary", date)
        return None
    formatted = _format_activities(activities)
    transcripts = get_transcripts_for_period(start, end)
    transcript_section = ""
    if transcripts:
        parts = []
        for t in transcripts:
            snippet = t["transcript"][:1000]
            parts.append('--- Video: "%s" (%s) ---\n%s...' % (t.get("title", "Unknown"), t["video_id"], snippet))
        transcript_section = (
            "\n\n== YOUTUBE TRANSCRIPTS (key content from videos watched) ==\n"
            + "\n\n".join(parts)
        )
    user_msg = "Here is the activity log for %s:\n\n%s%s" % (
        date.strftime("%A, %B %d, %Y"), formatted, transcript_section
    )
    log.info("Generating daily summary for %s (%d activities, %d transcripts)", date, len(activities), len(transcripts))
    summary = _call_ai(DAILY_SYSTEM, user_msg, max_tokens=3000)
    save_summary("daily", date.isoformat(), date.isoformat(), summary)
    try:
        keywords = extract_from_summary(summary, date.isoformat())
        for t in transcripts:
            keywords.extend(extract_from_transcript(t["transcript"], date.isoformat()))
        if keywords:
            save_keywords(keywords)
            log.info("Extracted %d keywords from daily summary + transcripts", len(keywords))
    except Exception as e:
        log.warning("Keyword extraction from summary failed: %s", e)
    return summary


def generate_weekly_summary(week_start):
    existing = get_summary("weekly", week_start.isoformat())
    if existing:
        return existing
    week_end = week_start + dt.timedelta(days=7)
    dailies = get_summaries_in_range("daily", week_start.isoformat(), week_end.isoformat())
    if not dailies:
        log.info("No daily summaries for week of %s, skipping", week_start)
        return None
    parts = []
    for d in dailies:
        parts.append("=== %s ===\n%s\n" % (d["start_date"], d["content"]))
    user_msg = "Here are the daily summaries for the week of %s - %s:\n\n%s" % (
        week_start.strftime("%B %d"),
        (week_end - dt.timedelta(days=1)).strftime("%B %d, %Y"),
        "\n".join(parts),
    )
    log.info("Generating weekly summary for week of %s", week_start)
    summary = _call_ai(WEEKLY_SYSTEM, user_msg, max_tokens=3000)
    save_summary("weekly", week_start.isoformat(), (week_end - dt.timedelta(days=1)).isoformat(), summary)
    try:
        keywords = extract_from_summary(summary, week_start.isoformat())
        if keywords:
            save_keywords(keywords)
    except Exception as e:
        log.warning("Keyword extraction from weekly summary failed: %s", e)
    return summary


def generate_monthly_summary(year, month):
    start = dt.date(year, month, 1)
    start_str = start.isoformat()
    existing = get_summary("monthly", start_str)
    if existing:
        return existing
    if month == 12:
        end = dt.date(year + 1, 1, 1)
    else:
        end = dt.date(year, month + 1, 1)
    weeklies = get_summaries_in_range("weekly", start_str, end.isoformat())
    if not weeklies:
        log.info("No weekly summaries for %d-%02d, skipping", year, month)
        return None
    parts = []
    for w in weeklies:
        parts.append("=== Week of %s ===\n%s\n" % (w["start_date"], w["content"]))
    user_msg = "Here are the weekly summaries for %s:\n\n%s" % (
        start.strftime("%B %Y"), "\n".join(parts)
    )
    log.info("Generating monthly summary for %s", start.strftime("%B %Y"))
    summary = _call_ai(MONTHLY_SYSTEM, user_msg, max_tokens=4000)
    save_summary("monthly", start_str, (end - dt.timedelta(days=1)).isoformat(), summary)
    try:
        keywords = extract_from_summary(summary, start_str)
        if keywords:
            save_keywords(keywords)
    except Exception as e:
        log.warning("Keyword extraction from monthly summary failed: %s", e)
    return summary


def generate_yearly_summary(year):
    start = dt.date(year, 1, 1)
    start_str = start.isoformat()
    existing = get_summary("yearly", start_str)
    if existing:
        return existing
    end = dt.date(year + 1, 1, 1)
    monthlies = get_summaries_in_range("monthly", start_str, end.isoformat())
    if not monthlies:
        log.info("No monthly summaries for %d, skipping", year)
        return None
    parts = []
    for m in monthlies:
        parts.append("=== %s ===\n%s\n" % (m["start_date"][:7], m["content"]))
    user_msg = "Here are the monthly summaries for %d:\n\n%s" % (year, "\n".join(parts))
    log.info("Generating yearly summary for %d", year)
    summary = _call_ai(YEARLY_SYSTEM, user_msg, max_tokens=5000)
    save_summary("yearly", start_str, (end - dt.timedelta(days=1)).isoformat(), summary)
    try:
        keywords = extract_from_summary(summary, start_str)
        if keywords:
            save_keywords(keywords)
    except Exception as e:
        log.warning("Keyword extraction from yearly summary failed: %s", e)
    return summary
