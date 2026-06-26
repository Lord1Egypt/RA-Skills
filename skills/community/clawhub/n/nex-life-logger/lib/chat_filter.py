"""
Nex Life Logger - Chat / messaging filter
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
from urllib.parse import urlparse
import user_filters


def is_chat_url(url):
    if not url:
        return False
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    host = (parsed.hostname or "").lower()
    path = (parsed.path or "").lower()
    blocked_domains = user_filters.get("chat_blocked_domains")
    url_patterns = user_filters.get("chat_url_patterns")
    for blocked in blocked_domains:
        if host == blocked or host.endswith("." + blocked):
            return True
        if "/" in blocked:
            domain_part, path_part = blocked.split("/", 1)
            if (host == domain_part or host.endswith("." + domain_part)) and path.startswith("/" + path_part):
                return True
    for pattern in url_patterns:
        if pattern in path:
            return True
    return False


def is_chat_window(title):
    if not title:
        return False
    lower = title.lower()
    window_keywords = user_filters.get("chat_window_keywords")
    return any(kw in lower for kw in window_keywords)
