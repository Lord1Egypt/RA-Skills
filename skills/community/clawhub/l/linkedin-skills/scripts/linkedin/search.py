"""LinkedIn search (posts, people, companies)."""

from __future__ import annotations

import json
import logging
import time

from .bridge import BridgePage
from .human import sleep_random
from .selectors import SEARCH_RESULT
from .types import SearchResult
from .urls import make_search_url

logger = logging.getLogger(__name__)

_EXTRACT_PEOPLE_JS = """
(() => {
    const results = [];
    // Find the search results <ul> containing /in/ links
    const lists = Array.from(document.querySelectorAll('ul'));
    const resultList = lists.find(ul => ul.querySelectorAll('a[href*="/in/"]').length >= 2);
    if (!resultList) return JSON.stringify(results);

    const items = Array.from(resultList.children).filter(c => c.tagName === 'LI');
    for (const li of items) {
        // Primary profile link: the one with span[aria-hidden="true"] inside
        const profileLinks = Array.from(li.querySelectorAll('a[href*="/in/"]'));
        const primaryLink = profileLinks.find(a => a.querySelector('span[aria-hidden="true"]'));
        if (!primaryLink) continue;

        const nameEl = primaryLink.querySelector('span[aria-hidden="true"]');
        const name = nameEl?.innerText?.trim() || '';
        const url = primaryLink.href?.split('?')[0] || '';
        if (!name || name.length < 2 || name.startsWith('View ')) continue;

        // Degree: "· 1st", "· 2nd", "· 3rd" in the li text
        const degreeMatch = li.innerText.match(/[·•]\\s*(1st|2nd|3rd)/);
        const degree = degreeMatch ? degreeMatch[1] : '';

        // Extract headline and location from text lines
        const lines = li.innerText.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
        const noise = [
            'View ', 'Connect', 'Follow', 'Message', 'Pending',
            'degree connection', 'mutual connection', 'are mutual',
            'likes this'
        ];
        const cleaned = lines.filter(l =>
            l !== name &&
            !noise.some(n => l.includes(n)) &&
            !/^[·•]\\s*(1st|2nd|3rd)$/.test(l) &&
            l.length > 3
        );
        const subtitle = cleaned[0] || '';
        const location = cleaned[1] || '';

        results.push({ name, subtitle, url, result_type: 'person', degree, location });
    }
    return JSON.stringify(results);
})()
"""

_EXTRACT_COMPANIES_JS = """
(() => {
    const results = [];
    const seen = new Set();
    document.querySelectorAll('a[href*="/company/"]').forEach(link => {
        const url = link.href.split('?')[0];
        if (seen.has(url)) return;
        if (!url.match(/\/company\/[\\w%-]{2,}/)) return;
        seen.add(url);

        const nameEl = link.querySelector('span[aria-hidden="true"]');
        const name = nameEl
            ? nameEl.innerText.trim()
            : link.innerText.trim().split('\\n')[0].trim();
        if (!name || name.length < 2 || name.startsWith('View ')) return;

        let container = link;
        for (let i = 0; i < 6; i++) {
            container = container.parentElement;
            if (!container) break;
        }
        const lines = (container?.innerText || '')
            .split('\\n')
            .map(l => l.trim())
            .filter(l => l.length > 2 && l !== name && !l.startsWith('View ') && l !== 'Follow');
        const subtitle = lines[0] || '';

        results.push({ name, subtitle, url, result_type: 'company' });
    });
    return JSON.stringify(results.slice(0, 15));
})()
"""

_EXTRACT_POSTS_JS = """
(() => {
    const results = [];
    // Post search: each result has "Open control menu for post by X" button
    const menuBtns = document.querySelectorAll(
        'button[aria-label^="Open control menu for post by"]'
    );
    menuBtns.forEach(btn => {
        try {
            const authorName = btn.getAttribute('aria-label')
                .replace('Open control menu for post by ', '').trim();

            let root = btn;
            for (let i = 0; i < 12; i++) {
                root = root.parentElement;
                if (!root) break;
                if (root.offsetHeight > 100) break;
            }
            if (!root) return;

            const profileLink = root.querySelector('a[href*="/in/"], a[href*="/company/"]');
            const url = profileLink ? profileLink.href.split('?')[0] : '';
            const lines = (root.innerText || '').split('\\n').map(l => l.trim())
                .filter(l => l && l !== 'Feed post' && l !== authorName);
            const subtitle = lines.slice(0, 3).join(' | ');

            results.push({ name: authorName, subtitle, url, result_type: 'post' });
        } catch (e) {}
    });
    return JSON.stringify(results);
})()
"""

_JS_MAP: dict[str, str] = {
    "people": _EXTRACT_PEOPLE_JS,
    "companies": _EXTRACT_COMPANIES_JS,
    "content": _EXTRACT_POSTS_JS,
    "posts": _EXTRACT_POSTS_JS,
}


def search(
    page: BridgePage,
    query: str,
    search_type: str = "content",
    *,
    title: str = "",
    location_urn: str = "",
    company: str = "",
    network: str = "",
) -> list[SearchResult]:
    """Search LinkedIn for posts, people, or companies.

    Args:
        page: BridgePage instance.
        query: Search terms.
        search_type: 'content' (posts), 'people', or 'companies'.
        title: Job title filter (people search only).
        location_urn: LinkedIn geo URN e.g. "103644278" for India.
        company: Company name filter (people search only).
        network: Connection degree filter: "F"=1st, "S"=2nd, "O"=3rd+.

    Returns:
        List of SearchResult objects.
    """
    url = make_search_url(
        query, search_type,
        title=title, location_urn=location_urn,
        company=company, network=network,
    )
    page.navigate(url)
    page.wait_for_load()
    page.wait_dom_stable()
    sleep_random(500, 1000)

    _wait_for_results(page)

    extract_js = _JS_MAP.get(search_type, _EXTRACT_PEOPLE_JS)
    result = page.evaluate(extract_js)
    if not result:
        return []

    data = json.loads(result)
    return [SearchResult(**r) for r in data]


def _wait_for_results(page: BridgePage, timeout: float = 15.0) -> None:
    deadline = time.monotonic() + timeout
    # Wait for any /in/ or /company/ links (people/companies) or post menu buttons
    while time.monotonic() < deadline:
        count = page.get_elements_count('a[href*="/in/"], a[href*="/company/"]')
        if count > 2:
            return
        time.sleep(0.5)
    logger.warning("Timeout waiting for search results")
