"""
Nex Life Logger - Keyword Extractor
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import re
import json
import logging
from urllib.parse import urlparse, parse_qs
import user_filters

log = logging.getLogger("life-logger.keywords")


def _get_all_patterns():
    return user_filters.get_compiled_tool_patterns() + user_filters.get_compiled_topic_patterns()


def extract_keywords_from_text(text):
    if not text:
        return []
    found = []
    seen = set()
    for pattern, keyword, category in _get_all_patterns():
        if pattern.search(text) and keyword not in seen:
            found.append((keyword, category))
            seen.add(keyword)
    return found


def extract_from_activity(activity):
    keywords = []
    date = activity.get("timestamp", "")[:10]
    if not date:
        return []
    title = activity.get("title", "") or ""
    url = activity.get("url", "") or ""
    kind = activity.get("kind", "")
    extra = {}
    try:
        extra = json.loads(activity.get("extra", "{}") or "{}")
    except Exception:
        pass
    try:
        host = urlparse(url).hostname or ""
        if host.startswith("www."):
            host = host[4:]
        if host and "." in host:
            domain_map = user_filters.get("domain_keyword_map")
            if host in domain_map:
                keywords.append({
                    "keyword": domain_map[host], "category": "domain",
                    "source_type": "activity", "source_date": date,
                })
    except Exception:
        pass
    if kind == "search":
        query = extra.get("search_query", "")
        if query and len(query) > 2:
            keywords.append({
                "keyword": query[:100], "category": "search",
                "source_type": "activity", "source_date": date,
            })
    combined = "%s %s" % (title, url)
    for kw, cat in extract_keywords_from_text(combined):
        keywords.append({
            "keyword": kw, "category": cat,
            "source_type": "activity", "source_date": date,
        })
    if kind == "app_focus":
        process = extra.get("process", "")
        process_map = user_filters.get("process_keyword_map")
        if process in process_map:
            keywords.append({
                "keyword": process_map[process], "category": "tool",
                "source_type": "activity", "source_date": date,
            })
    return keywords


def extract_from_activities(activities):
    all_kw = []
    for a in activities:
        all_kw.extend(extract_from_activity(a))
    return all_kw


def extract_from_summary(summary_text, date):
    keywords = []
    for kw, cat in extract_keywords_from_text(summary_text):
        keywords.append({
            "keyword": kw, "category": cat,
            "source_type": "summary", "source_date": date,
        })
    return keywords


def extract_from_transcript(transcript, date):
    keywords = []
    for kw, cat in extract_keywords_from_text(transcript[:2000]):
        keywords.append({
            "keyword": kw, "category": cat,
            "source_type": "transcript", "source_date": date,
        })
    return keywords
