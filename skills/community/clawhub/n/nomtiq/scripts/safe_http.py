#!/usr/bin/env python3
from __future__ import annotations

"""Small shared HTTP safety helpers for Nomtiq's fixed provider clients."""

import re
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


class _NoRedirectHandler(HTTPRedirectHandler):
    """Return redirect responses to the caller instead of forwarding secrets."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: N802
        return None


_NO_REDIRECT_OPENER = build_opener(_NoRedirectHandler())


def open_no_redirect(request: Request, timeout: int = 20):
    """Open one request without following HTTP redirects."""
    return _NO_REDIRECT_OPENER.open(request, timeout=timeout)


def is_allowed_https_url(url: str, allowed_domains: tuple[str, ...]) -> bool:
    """Require HTTPS and an exact domain or subdomain match."""
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower().rstrip(".")
    except (TypeError, ValueError):
        return False
    if parsed.scheme.lower() != "https" or not host:
        return False
    return any(host == domain or host.endswith(f".{domain}") for domain in allowed_domains)


def quoted_search_term(value: str, max_length: int = 200) -> str:
    """Keep user/listing text inside one conservative search phrase."""
    cleaned = re.sub(r"[\x00-\x1f\x7f\\\"]+", " ", str(value))
    cleaned = re.sub(r"\s+", " ", cleaned).strip()[:max_length]
    return f'"{cleaned}"' if cleaned else '""'
