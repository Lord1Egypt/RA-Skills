"""LinkedIn profile and company page scraping."""

from __future__ import annotations

import json
import logging

from .bridge import BridgePage
from .human import sleep_random
from .types import CompanyProfile, Profile
from .urls import make_company_url, make_profile_url

logger = logging.getLogger(__name__)

_EXTRACT_PROFILE_JS = """
(() => {
    const main = document.querySelector('main') || document.body;
    const sections = Array.from(main.querySelectorAll('section'));
    const card = sections[0];
    const cardText = card?.innerText || '';
    const lines = cardText.split('\\n').map(l => l.trim()).filter(l => l.length > 0);

    // Name: first non-empty line (LinkedIn 2025 no longer uses h1 on profiles)
    const name = lines[0] || '';

    // Degree: look for "· 1st" or "· 2nd" etc in the card text
    const degreeMatch = cardText.match(/[·•]\\s*(1st|2nd|3rd)/);
    const degree = degreeMatch ? degreeMatch[1] : '';

    // Filter noise lines to find headline, location
    const noise = [
        'View ', 'Contact info', 'Connect', 'Message', 'More', 'Follow',
        'degree connection', 'mutual connection', 'connections', 'followers',
        'He/Him', 'She/Her', 'They/Them'
    ];
    const cleaned = lines.slice(1).filter(l =>
        !noise.some(n => l.startsWith(n) || l.includes(n)) &&
        !/^[·•]\\s*(1st|2nd|3rd)$/.test(l) &&
        l !== name
    );
    // Headline is first cleaned line; location is second (if it looks like a place)
    const headline = cleaned[0] || '';
    const location = cleaned[1] || '';

    // Connections count
    const connMatch = cardText.match(/(\\d[\\d,+]*\\+?)\\s*connections?/i);
    const connections = connMatch ? connMatch[1] + ' connections' : '';

    // About section
    let about = '';
    const aboutAnchor = document.querySelector('#about');
    if (aboutAnchor) {
        let sec = aboutAnchor;
        for (let i = 0; i < 6; i++) { sec = sec.parentElement; if (!sec || sec.tagName === 'SECTION') break; }
        if (sec?.tagName === 'SECTION') {
            const spans = Array.from(sec.querySelectorAll('span[aria-hidden="true"], span')).filter(s => {
                const t = s.innerText?.trim() || '';
                return t.length > 30 && t !== 'About';
            });
            about = spans[0]?.innerText?.trim() || sec.innerText.replace(/^About\\s*/, '').trim().substring(0, 2000);
        }
    }

    // Experience entries
    const experience = [];
    const expAnchor = document.querySelector('#experience');
    if (expAnchor) {
        let sec = expAnchor;
        for (let i = 0; i < 6; i++) { sec = sec.parentElement; if (!sec || sec.tagName === 'SECTION') break; }
        if (sec?.tagName === 'SECTION') {
            const items = Array.from(sec.querySelectorAll('li'));
            items.forEach(li => {
                const spans = Array.from(li.querySelectorAll('span[aria-hidden="true"]'))
                    .map(s => s.innerText?.trim()).filter(Boolean);
                if (spans.length >= 1) {
                    experience.push({ role: spans[0], company: spans[1] || '' });
                }
            });
        }
    }

    return JSON.stringify({ name, headline, location, connections, about, experience, degree });
})()
"""

_EXTRACT_COMPANY_JS = """
(() => {
    const main = document.querySelector('main') || document.body;

    // Company name from h1 or first section
    const h1 = main.querySelector('h1');
    const name = h1?.innerText?.trim() || '';

    // Tagline — text near the name, usually a <p> or subtitle div
    const sections = Array.from(main.querySelectorAll('section'));
    const card = sections[0];
    const cardLines = (card?.innerText || '').split('\\n').map(l => l.trim()).filter(l => l.length > 0);
    const tagline = cardLines.find(l => l !== name && l.length > 5 && !l.includes('follower') && !l.includes('employee')) || '';

    // Followers
    const followerMatch = (card?.innerText || '').match(/(\\d[\\d,]*\\+?)\\s*followers?/i);
    const followers = followerMatch ? followerMatch[0] : '';

    // About section
    let about = '';
    const aboutAnchor = document.querySelector('#about');
    if (aboutAnchor) {
        let sec = aboutAnchor;
        for (let i = 0; i < 6; i++) { sec = sec.parentElement; if (!sec || sec.tagName === 'SECTION') break; }
        if (sec?.tagName === 'SECTION') {
            const p = sec.querySelector('p');
            about = p?.innerText?.trim() || sec.innerText.replace(/^About\\s*/, '').trim().substring(0, 2000);
        }
    }

    // Website
    const websiteLink = main.querySelector('a[href*="http"][rel*="noopener"], a[data-field="website"]');
    const website = websiteLink ? (websiteLink.href || websiteLink.innerText?.trim()) : '';

    return JSON.stringify({ name, tagline, followers, about, website });
})()
"""


def get_user_profile(page: BridgePage, username: str) -> dict:
    """Get a LinkedIn user's profile information.

    Args:
        page: BridgePage instance.
        username: LinkedIn profile slug (e.g. 'satyanadella') or full profile URL.

    Returns:
        Dict with profile fields.
    """
    url = make_profile_url(username)
    page.navigate(url)
    page.wait_for_load()
    page.wait_dom_stable()
    sleep_random(500, 1000)

    result = page.evaluate(_EXTRACT_PROFILE_JS)
    data = json.loads(result or "{}")

    profile = Profile(
        name=data.get("name", ""),
        headline=data.get("headline", ""),
        location=data.get("location", ""),
        profile_url=url,
        connections=data.get("connections", ""),
        about=data.get("about", ""),
        experience=data.get("experience", []),
        degree=data.get("degree", ""),
    )
    return profile.to_dict()


def get_company_profile(page: BridgePage, company_slug: str) -> dict:
    """Get LinkedIn company page information.

    Args:
        page: BridgePage instance.
        company_slug: Company URL slug (e.g. 'microsoft') or full company URL.

    Returns:
        Dict with company fields.
    """
    url = make_company_url(company_slug)
    page.navigate(url)
    page.wait_for_load()
    page.wait_dom_stable()
    sleep_random(500, 1000)

    result = page.evaluate(_EXTRACT_COMPANY_JS)
    data = json.loads(result or "{}")

    company = CompanyProfile(
        name=data.get("name", ""),
        tagline=data.get("tagline", ""),
        followers=data.get("followers", ""),
        about=data.get("about", ""),
        website=data.get("website", ""),
        company_url=url,
    )
    return company.to_dict()
