"""
Nex Life Logger - Productivity Content Filter
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import re
import logging
from urllib.parse import urlparse
import user_filters

log = logging.getLogger("life-logger.content-filter")


def _get_productive_domains():
    return set(user_filters.get("productive_domains"))

def _get_non_productive_domains():
    return set(user_filters.get("non_productive_domains"))


def _keyword_score(text):
    prod_patterns = user_filters.get_compiled_productive_keywords()
    nonprod_patterns = user_filters.get_compiled_non_productive_keywords()
    prod = sum(1 for p in prod_patterns if p.search(text))
    nonprod = sum(1 for p in nonprod_patterns if p.search(text))
    return prod, nonprod


def is_productive(url, title, transcript=None):
    if not url and not title:
        return True
    productive_domains = _get_productive_domains()
    non_productive_domains = _get_non_productive_domains()
    try:
        host = (urlparse(url).hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
    except Exception:
        host = ""
    if host in productive_domains:
        return True
    if host in non_productive_domains:
        log.debug("Filtered (non-productive domain): %s", host)
        return False
    is_youtube = "youtube.com" in host or "youtu.be" in host
    combined = "%s " % title
    if transcript:
        combined += transcript[:500]
    prod_score, nonprod_score = _keyword_score(combined)
    if prod_score >= 2 and nonprod_score == 0:
        return True
    if nonprod_score >= 2 and prod_score == 0:
        log.debug("Filtered (non-productive keywords): %s", title[:80])
        return False
    if is_youtube:
        if prod_score > nonprod_score:
            return True
        if nonprod_score > 0:
            log.debug("Filtered YouTube (not productive enough): %s", title[:80])
            return False
        if prod_score == 0 and nonprod_score == 0:
            log.debug("Filtered YouTube (no productive signal): %s", title[:80])
            return False
    if nonprod_score > prod_score:
        log.debug("Filtered (more non-productive signals): %s", title[:80])
        return False
    return True
