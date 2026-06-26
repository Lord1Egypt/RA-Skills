"""LinkedIn URL constants and builder functions."""

from urllib.parse import urlencode

HOME_URL = "https://www.linkedin.com/feed/"
MESSAGING_URL = "https://www.linkedin.com/messaging/"
LOGOUT_URL = "https://www.linkedin.com/m/logout/"


def make_profile_url(username: str) -> str:
    """Build LinkedIn profile URL from a username/slug or return as-is if already a URL."""
    if username.startswith("http"):
        return username
    return f"https://www.linkedin.com/in/{username}/"


def make_company_url(slug: str) -> str:
    """Build company page URL from slug or return as-is if already a URL."""
    if slug.startswith("http"):
        return slug
    return f"https://www.linkedin.com/company/{slug}/"


def make_search_url(
    query: str,
    search_type: str = "content",
    *,
    title: str = "",
    location_urn: str = "",
    company: str = "",
    network: str = "",
) -> str:
    """Build search URL with optional filters.

    Args:
        query: Search keywords.
        search_type: 'content' (posts), 'people', 'companies', 'jobs'.
        title: Job title filter (people only), e.g. "CTO".
        location_urn: LinkedIn geo URN, e.g. "103644278" for India.
        company: Company name filter (people only).
        network: Degree filter: "F"=1st, "S"=2nd, "O"=3rd+.
    """
    params: dict[str, str] = {"keywords": query}
    if title:
        params["titleFreeText"] = title
    if location_urn:
        params["geoUrn"] = f'["{location_urn}"]'
    if company:
        params["company"] = company
    if network:
        params["network"] = f'["{network}"]'
    qs = urlencode(params)
    return f"https://www.linkedin.com/search/results/{search_type}/?{qs}"


def make_post_url(post_url: str) -> str:
    """Normalize a post URL. Accepts full URL or URN."""
    if post_url.startswith("http"):
        return post_url
    # Handle urn:li:activity:... format
    return f"https://www.linkedin.com/feed/update/{post_url}/"
