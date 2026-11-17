"""User-intent routing for the Perplexity CLI and direct-browser workflow."""

import re
from typing import List, TypedDict


class RouteDecision(TypedDict):
    route: str
    matched_terms: List[str]
    reason: str


# Keep this list deliberately narrow. A query about web development is still a
# normal research request; only explicit instructions to use a browser route
# should select direct WebBridge execution.
_DIRECT_BROWSER_MARKERS = (
    ("网页方式", re.compile(r"网页方式")),
    ("网页版", re.compile(r"网页版")),
    ("用网页", re.compile(r"(?:用|拿|走|通过)\s*网页")),
    ("web page", re.compile(r"\bweb\s+page\b", re.IGNORECASE)),
    ("browser", re.compile(r"\bbrowser\b|浏览器")),
    ("Chrome", re.compile(r"\bchrome\b", re.IGNORECASE)),
    ("WebBridge", re.compile(r"\bwebbridge\b", re.IGNORECASE)),
    ("Kimi WebBridge", re.compile(r"kimi\s+webbridge", re.IGNORECASE)),
    ("open Perplexity", re.compile(
        r"(?:\bopen\b|打开)\s*(?:perplexity(?:\.ai)?|perplexity\s+页面)",
        re.IGNORECASE,
    )),
    ("current browser thread", re.compile(
        r"(?:continue|use)\s+(?:the\s+)?current\s+browser\s+thread",
        re.IGNORECASE,
    )),
    ("当前浏览器线程", re.compile(r"当前(?:浏览器|网页).{0,12}(?:线程|对话|tab|标签页)")),
)


def select_route(request: str) -> RouteDecision:
    """Select the user-facing route without probing either execution backend."""
    text = request or ""
    matched_terms = [label for label, pattern in _DIRECT_BROWSER_MARKERS
                     if pattern.search(text)]
    if matched_terms:
        return {
            "route": "browser",
            "matched_terms": matched_terms,
            "reason": "explicit browser/WebBridge wording",
        }
    return {
        "route": "cli",
        "matched_terms": [],
        "reason": "no explicit browser route wording",
    }
