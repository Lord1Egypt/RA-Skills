#!/usr/bin/env python3
"""
Job Hunter - LinkedIn Job Search Skill for OpenClaw

A personal job search assistant that reads publicly available LinkedIn job
listings (the same pages any web browser can access) and optionally scores
them with Google Gemini AI. No authentication, login, or private data access
is involved — only public search result pages are fetched.

Usage:
    job_hunter.py search '<json_params>'
    job_hunter.py setkey <gemini_api_key>
    job_hunter.py save '<json_job>'
    job_hunter.py saved
    job_hunter.py unsave <url>
    job_hunter.py history
    job_hunter.py rerun <index>

License: MIT
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlencode

import httpx
from selectolax.parser import HTMLParser, Node

__all__ = [
    "cmd_history",
    "cmd_rerun",
    "cmd_save",
    "cmd_saved",
    "cmd_search",
    "cmd_setkey",
    "cmd_unsave",
    "load_config",
    "load_json",
    "main",
    "parse_job_listings",
    "save_json",
    "score_jobs",
    "scrape_jobs",
]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_DESCRIPTION_LENGTH = 2000
MAX_DESCRIPTION_FOR_PROMPT = 500
MAX_RESULTS_OUTPUT = 30
MAX_HISTORY_ENTRIES = 20
DEFAULT_MIN_SCORE = 0.6
DEFAULT_MAX_PAGES = 3
MAX_PAGES_CAP = 5
DEFAULT_MAX_CONCURRENT = 5

# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------
DATA_DIR = Path.home() / ".openclaw" / "job-hunter"
CONFIG_FILE = DATA_DIR / "config.json"
HISTORY_FILE = DATA_DIR / "history.json"
SAVED_FILE = DATA_DIR / "saved.json"


def ensure_dir() -> None:
    """Create the data directory if it does not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any = None) -> Any:
    """Load and return JSON data from *path*, or *default* if missing."""
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return default if default is not None else {}


def save_json(path: Path, data: Any) -> None:
    """Persist *data* as JSON to *path*, creating directories as needed."""
    ensure_dir()
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_config() -> dict[str, Any]:
    """Return the stored config or sensible defaults."""
    return load_json(CONFIG_FILE, {
        "gemini_api_key": "",
        "gemini_model": "gemini-2.5-flash",
        "min_ai_score": DEFAULT_MIN_SCORE,
        "max_pages": DEFAULT_MAX_PAGES,
    })


# ---------------------------------------------------------------------------
# LinkedIn scraping
# ---------------------------------------------------------------------------
LINKEDIN_JOBS_URL = "https://www.linkedin.com/jobs/search/"
JOBS_PER_PAGE = 25

EXPERIENCE_MAP: dict[str, str] = {
    "internship": "1", "entry": "2", "associate": "3",
    "mid": "4", "mid-senior": "4", "senior": "4",
    "director": "5", "executive": "6",
}

LOCATION_TO_COUNTRY: dict[str, str] = {
    ", ca": "united states", ", ny": "united states", ", tx": "united states",
    ", wa": "united states", ", il": "united states", ", ma": "united states",
    ", co": "united states", ", ga": "united states", ", va": "united states",
    ", pa": "united states", ", nc": "united states", ", or": "united states",
    ", fl": "united states", ", nj": "united states", ", ct": "united states",
    ", az": "united states", ", mn": "united states", ", oh": "united states",
    ", md": "united states", ", mi": "united states", ", ut": "united states",
    ", dc": "united states", ", tn": "united states", ", mo": "united states",
    "new york": "united states", "san francisco": "united states",
    "seattle": "united states", "austin": "united states", "boston": "united states",
    "chicago": "united states", "los angeles": "united states", "denver": "united states",
    "atlanta": "united states", "dallas": "united states", "portland": "united states",
    "miami": "united states", "san jose": "united states", "san diego": "united states",
    "washington": "united states", "houston": "united states", "philadelphia": "united states",
    "charlotte": "united states", "pittsburgh": "united states", "raleigh": "united states",
    "minneapolis": "united states", "detroit": "united states", "phoenix": "united states",
    "salt lake": "united states",
    "london": "united kingdom", "manchester": "united kingdom",
    "edinburgh": "united kingdom", "birmingham": "united kingdom",
    "bristol": "united kingdom", "cambridge": "united kingdom",
    "oxford": "united kingdom", "glasgow": "united kingdom", "leeds": "united kingdom",
    "england": "united kingdom", "scotland": "united kingdom", "wales": "united kingdom",
    "berlin": "germany", "munich": "germany", "münchen": "germany",
    "hamburg": "germany", "frankfurt": "germany", "cologne": "germany",
    "köln": "germany", "düsseldorf": "germany", "stuttgart": "germany",
    "zurich": "switzerland", "zürich": "switzerland", "geneva": "switzerland",
    "genève": "switzerland", "basel": "switzerland", "bern": "switzerland",
    "lausanne": "switzerland",
    "vienna": "austria", "wien": "austria", "graz": "austria",
    "salzburg": "austria", "linz": "austria",
    "amsterdam": "netherlands", "rotterdam": "netherlands",
    "the hague": "netherlands", "eindhoven": "netherlands", "utrecht": "netherlands",
    "dublin": "ireland", "cork": "ireland", "galway": "ireland",
    "sydney": "australia", "melbourne": "australia", "brisbane": "australia",
    "perth": "australia", "adelaide": "australia", "canberra": "australia",
    "toronto": "canada", "vancouver": "canada", "montreal": "canada",
    "ottawa": "canada", "calgary": "canada",
    "stockholm": "sweden", "gothenburg": "sweden", "malmö": "sweden",
    "copenhagen": "denmark", "oslo": "norway", "helsinki": "finland",
    "paris": "france", "lyon": "france", "toulouse": "france",
    "brussels": "belgium", "antwerp": "belgium",
    "luxembourg": "luxembourg",
    "madrid": "spain", "barcelona": "spain", "valencia": "spain",
    "sevilla": "spain", "malaga": "spain", "bilbao": "spain",
    "lisbon": "portugal", "porto": "portugal",
    "rome": "italy", "milan": "italy", "turin": "italy",
    "warsaw": "poland", "krakow": "poland", "wroclaw": "poland",
    "prague": "czech republic", "brno": "czech republic",
    "bucharest": "romania", "cluj": "romania",
    "budapest": "hungary",
    "athens": "greece", "thessaloniki": "greece",
    "tel aviv": "israel", "jerusalem": "israel",
    "singapore": "singapore",
    "tokyo": "japan", "osaka": "japan",
    "seoul": "south korea",
    "bangalore": "india", "mumbai": "india", "hyderabad": "india",
    "delhi": "india", "pune": "india", "chennai": "india",
    "são paulo": "brazil", "rio de janeiro": "brazil",
    "mexico city": "mexico", "guadalajara": "mexico", "monterrey": "mexico",
    "buenos aires": "argentina",
    "bogota": "colombia", "medellin": "colombia",
    "santiago": "chile", "lima": "peru",
}

logger = logging.getLogger("job_hunter")


def _extract_linkedin_id(url: str) -> str | None:
    """Extract the numeric LinkedIn job ID from a job URL."""
    match = re.search(r"/jobs/view/(?:.*?[-/])?(\d+)", url)
    return match.group(1) if match else None


def _parse_relative_date(text: str | None) -> str | None:
    """Convert a relative date string (e.g. '3 days ago') to ISO date."""
    if not text:
        return None
    text = text.lower().strip()
    now = datetime.now(timezone.utc)
    patterns: list[tuple[str, Any]] = [
        (r"(\d+)\s*second", lambda m: timedelta(seconds=int(m.group(1)))),
        (r"(\d+)\s*minute", lambda m: timedelta(minutes=int(m.group(1)))),
        (r"(\d+)\s*hour", lambda m: timedelta(hours=int(m.group(1)))),
        (r"(\d+)\s*day", lambda m: timedelta(days=int(m.group(1)))),
        (r"(\d+)\s*week", lambda m: timedelta(weeks=int(m.group(1)))),
        (r"(\d+)\s*month", lambda m: timedelta(days=int(m.group(1)) * 30)),
    ]
    for pattern, delta_fn in patterns:
        match = re.search(pattern, text)
        if match:
            return (now - delta_fn(match)).date().isoformat()
    return None


def _parse_single_card(card: Node) -> dict[str, Any] | None:
    """Parse a single LinkedIn job card HTML node into a job dict."""
    title_el = card.css_first("h3, h4, .base-search-card__title")
    title = title_el.text(strip=True) if title_el else None

    link_el = card.css_first("a[href*='/jobs/view/'], a.base-card__full-link")
    url = link_el.attributes.get("href", "").split("?")[0] if link_el else None
    linkedin_id = _extract_linkedin_id(url) if url else None

    if not title or not linkedin_id or not url:
        return None

    company_el = card.css_first("h4 a, .base-search-card__subtitle, .base-search-card__subtitle a")
    company = company_el.text(strip=True) if company_el else "Unknown"

    location_el = card.css_first(".job-search-card__location, .base-search-card__metadata span")
    location = location_el.text(strip=True) if location_el else None

    time_el = card.css_first("time")
    posted_at = None
    if time_el:
        dt = time_el.attributes.get("datetime")
        posted_at = dt if dt else _parse_relative_date(time_el.text(strip=True))

    salary_el = card.css_first(".job-search-card__salary-info, .base-search-card__metadata .salary")
    salary = salary_el.text(strip=True) if salary_el else None

    return {
        "linkedin_id": linkedin_id, "title": title, "company": company,
        "location": location, "url": url, "posted_at": posted_at,
        "salary": salary, "description": None,
    }


def parse_job_listings(html: str) -> list[dict[str, Any]]:
    """Parse LinkedIn search results HTML and return a list of job dicts."""
    parser = HTMLParser(html)
    jobs: list[dict[str, Any]] = []
    cards = parser.css("ul.jobs-search__results-list > li")
    if not cards:
        cards = parser.css("[data-entity-urn]")
    if not cards:
        cards = parser.css("div.base-search-card")

    for card in cards:
        try:
            job = _parse_single_card(card)
            if job:
                jobs.append(job)
        except (AttributeError, KeyError, TypeError) as exc:
            logger.warning("Failed to parse job card: %s", exc)
            continue
    return jobs


async def _fetch_description(client: httpx.AsyncClient, job: dict[str, Any]) -> str | None:
    """Fetch the full description for a single job listing."""
    try:
        resp = await client.get(job["url"])
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.warning("HTTP %s fetching description for %s", exc.response.status_code, job["url"])
        return None
    except httpx.RequestError as exc:
        logger.warning("Request error fetching description for %s: %s", job["url"], exc)
        return None
    parser = HTMLParser(resp.text)
    desc_el = (
        parser.css_first("div.description__text")
        or parser.css_first("div.show-more-less-html__markup")
        or parser.css_first("section.description")
    )
    return desc_el.text(strip=True)[:MAX_DESCRIPTION_LENGTH] if desc_el else None


async def _enrich_descriptions(
    client: httpx.AsyncClient,
    jobs: list[dict[str, Any]],
    max_concurrent: int = DEFAULT_MAX_CONCURRENT,
) -> None:
    """Fetch and attach descriptions for a list of jobs in batches."""
    for i in range(0, len(jobs), max_concurrent):
        batch = jobs[i:i + max_concurrent]
        descriptions = await asyncio.gather(*[_fetch_description(client, j) for j in batch])
        for job, desc in zip(batch, descriptions):
            job["description"] = desc
        if i + max_concurrent < len(jobs):
            await asyncio.sleep(2.0)  # polite delay between batches


def _job_matches_technologies(job: dict[str, Any], techs_lower: list[str]) -> bool:
    """Return True if any technology keyword appears in the job title or description."""
    searchable = job["title"].lower()
    if job.get("description"):
        searchable += " " + job["description"].lower()
    return any(tech in searchable for tech in techs_lower)


def _location_matches_countries(location: str | None, countries_lower: set[str]) -> bool:
    """Return True if *location* maps to one of the given countries."""
    if not location:
        return False
    loc = location.lower()
    if any(country in loc for country in countries_lower):
        return True
    for fragment, country in LOCATION_TO_COUNTRY.items():
        if fragment in loc and country in countries_lower:
            return True
    return False


async def _scrape_one_location(
    client: httpx.AsyncClient,
    params: dict[str, Any],
    location: str | None,
    max_pages: int,
) -> list[dict[str, Any]]:
    """Scrape job listings for a single location across multiple pages."""
    all_jobs: list[dict[str, Any]] = []
    for page in range(max_pages):
        url_params: dict[str, str] = {
            "keywords": params["keywords"],
            "start": str(page * JOBS_PER_PAGE),
            "sortBy": "DD",
        }
        if location:
            url_params["location"] = location
        if params.get("remote"):
            url_params["f_WT"] = "2"
        if params.get("experience") and params["experience"] in EXPERIENCE_MAP:
            url_params["f_E"] = EXPERIENCE_MAP[params["experience"]]
        if params.get("company_size"):
            url_params["f_CS"] = ",".join(params["company_size"])

        url = f"{LINKEDIN_JOBS_URL}?{urlencode(url_params, quote_via=quote_plus)}"
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.warning("HTTP %s fetching page %d for '%s'", exc.response.status_code, page, location)
            break
        except httpx.RequestError as exc:
            logger.warning("Request error on page %d for '%s': %s", page, location, exc)
            break

        jobs = parse_job_listings(response.text)
        if not jobs:
            break
        all_jobs.extend(jobs)

        if page < max_pages - 1:
            await asyncio.sleep(2.0)  # polite delay between pages
    return all_jobs


async def scrape_jobs(params: dict[str, Any]) -> list[dict[str, Any]]:
    """Scrape LinkedIn job listings based on search parameters."""
    headers = {
        "Accept": "text/html",
    }
    max_pages = min(params.get("max_pages", DEFAULT_MAX_PAGES), MAX_PAGES_CAP)
    all_jobs: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=30.0) as client:
        countries = params.get("countries", [])
        if countries:
            for country in countries:
                jobs = await _scrape_one_location(client, params, country, max_pages)
                for j in jobs:
                    if j["linkedin_id"] not in seen_ids:
                        seen_ids.add(j["linkedin_id"])
                        all_jobs.append(j)
                await asyncio.sleep(2.0)  # polite delay between batches
        else:
            all_jobs = await _scrape_one_location(client, params, params.get("location"), max_pages)

    # Filter excluded terms
    exclude = params.get("exclude", [])
    if exclude:
        exclude_lower = [e.lower() for e in exclude]
        all_jobs = [
            j for j in all_jobs
            if not any(term in j["title"].lower() or term in j["company"].lower() for term in exclude_lower)
        ]

    # Enrich with descriptions
    if all_jobs:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as desc_client:
            await _enrich_descriptions(desc_client, all_jobs)

    # Filter by technologies
    technologies = params.get("technologies", [])
    if technologies:
        techs_lower = [t.lower() for t in technologies]
        all_jobs = [j for j in all_jobs if _job_matches_technologies(j, techs_lower)]

    return all_jobs


# ---------------------------------------------------------------------------
# AI Scoring (Google Gemini)
# ---------------------------------------------------------------------------
SCORING_PROMPT = """You are a job matching assistant. Score each job from 0.0 to 1.0 based on how
well it matches the candidate's criteria. Be strict: only score above 0.7 if the job is a strong match.

Candidate criteria:
- Keywords: {keywords}
- Required technologies: {technologies}
- Location preference: {location}
- Remote: {remote}
- Minimum salary: {salary_min}
- Experience level: {experience}
- Exclude terms: {exclude}
- Additional requirements: {ai_prompt}

Jobs to evaluate:
{jobs_text}

Respond ONLY with a JSON array. Each element must have:
- "index": the job number (starting from 0)
- "score": float from 0.0 to 1.0
- "reason": one sentence explaining the score in Spanish

Example response:
[{{"index": 0, "score": 0.85, "reason": "Buen match por tecnologia y ubicacion remota"}}]
"""

BATCH_SIZE = 10


def _format_jobs_for_prompt(jobs: list[dict[str, Any]]) -> str:
    """Format a list of jobs into a text block for the AI scoring prompt."""
    lines: list[str] = []
    for i, job in enumerate(jobs):
        parts = [f"Job {i}:", f"  Title: {job['title']}", f"  Company: {job['company']}"]
        if job.get("location"):
            parts.append(f"  Location: {job['location']}")
        if job.get("salary"):
            parts.append(f"  Salary: {job['salary']}")
        if job.get("description"):
            parts.append(f"  Description: {job['description'][:MAX_DESCRIPTION_FOR_PROMPT]}")
        parts.append(f"  URL: {job['url']}")
        lines.append("\n".join(parts))
    return "\n\n".join(lines)


def _build_scoring_prompt(jobs: list[dict[str, Any]], params: dict[str, Any]) -> str:
    """Build the full Gemini scoring prompt for a batch of jobs."""
    return SCORING_PROMPT.format(
        keywords=params.get("keywords", ""),
        technologies=", ".join(params.get("technologies", [])) or "Not specified",
        location=", ".join(params.get("countries", [])) or params.get("location", "Any"),
        remote="Yes" if params.get("remote") else "No preference",
        salary_min=f"EUR {params['salary_min']}" if params.get("salary_min") else "Not specified",
        experience=params.get("experience", "Any"),
        exclude=", ".join(params.get("exclude", [])) or "None",
        ai_prompt=params.get("ai_prompt", "No additional requirements"),
        jobs_text=_format_jobs_for_prompt(jobs),
    )


def _parse_scores(response_text: str, count: int) -> list[dict[str, Any]]:
    """Parse AI response text into a list of score dicts, with fallback."""
    try:
        text = response_text.strip()
        if "```" in text:
            start = text.find("[")
            end = text.rfind("]") + 1
            if start >= 0 and end > start:
                text = text[start:end]
        scores = json.loads(text)
        if not isinstance(scores, list):
            raise ValueError("Expected JSON array")
        return scores
    except (json.JSONDecodeError, ValueError) as exc:
        logger.warning("Failed to parse AI scores: %s", exc)
        return [{"index": i, "score": 0.5, "reason": "Score unavailable"} for i in range(count)]


def score_jobs(
    jobs: list[dict[str, Any]],
    params: dict[str, Any],
    api_key: str,
    model: str = "gemini-2.5-flash",
) -> list[dict[str, Any]]:
    """Score jobs using Google Gemini AI, or assign neutral scores if no key."""
    if not jobs:
        return []
    if not api_key:
        for job in jobs:
            job["ai_score"] = 0.5
            job["ai_summary"] = "No Gemini API key configured"
        return jobs

    from google import genai
    client = genai.Client(api_key=api_key)

    for batch_start in range(0, len(jobs), BATCH_SIZE):
        batch = jobs[batch_start:batch_start + BATCH_SIZE]
        prompt = _build_scoring_prompt(batch, params)
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=genai.types.GenerateContentConfig(temperature=0.1, max_output_tokens=2048),
            )
            scores = _parse_scores(response.text, len(batch))
            score_map = {s["index"]: s for s in scores}
            for i, job in enumerate(batch):
                score_data = score_map.get(i, {"score": 0.5, "reason": "Not scored"})
                job["ai_score"] = float(score_data.get("score", 0.5))
                job["ai_summary"] = score_data.get("reason")
        except Exception as e:
            logger.error("AI scoring failed for batch starting at %d: %s", batch_start, e)
            for job in batch:
                job["ai_score"] = 0.5
                job["ai_summary"] = f"AI error: {e}"

    return jobs


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def cmd_search(params_json: str) -> None:
    """Search LinkedIn for jobs matching the given JSON parameters."""
    params = json.loads(params_json)

    if "keywords" not in params:
        print(json.dumps({
            "status": "error",
            "message": "Missing required 'keywords' key in search parameters",
        }, indent=2))
        return

    config = load_config()

    # Run scraping
    jobs = asyncio.run(scrape_jobs(params))

    # Save to history (always, even with no results)
    history = load_json(HISTORY_FILE, [])
    history.insert(0, {
        "params": params,
        "total_found": len(jobs),
        "above_threshold": 0,
        "timestamp": datetime.now().isoformat(),
    })
    history = history[:MAX_HISTORY_ENTRIES]
    save_json(HISTORY_FILE, history)

    if not jobs:
        print(json.dumps({"status": "no_results", "message": "No jobs found matching your criteria"}, indent=2))
        return

    # Score with AI
    api_key = config.get("gemini_api_key", "")
    model = config.get("gemini_model", "gemini-2.5-flash")
    jobs = score_jobs(jobs, params, api_key, model)

    # Filter by min score
    min_score = params.get("min_score", config.get("min_ai_score", DEFAULT_MIN_SCORE))
    scored_jobs = sorted(jobs, key=lambda j: j.get("ai_score", 0), reverse=True)
    filtered = [j for j in scored_jobs if j.get("ai_score", 0) >= min_score]

    # Clean output (remove description to keep output manageable)
    for j in scored_jobs:
        j.pop("description", None)
        j.pop("linkedin_id", None)

    # Update history with actual above_threshold count
    history = load_json(HISTORY_FILE, [])
    if history:
        history[0]["above_threshold"] = len(filtered)
        save_json(HISTORY_FILE, history)

    print(json.dumps({
        "status": "ok",
        "total_scraped": len(jobs),
        "above_threshold": len(filtered),
        "min_score": min_score,
        "jobs": filtered[:MAX_RESULTS_OUTPUT],
        "all_jobs": len(scored_jobs),
    }, indent=2, ensure_ascii=False))


def cmd_setkey(api_key: str) -> None:
    """Store the Gemini API key in the config file."""
    config = load_config()
    config["gemini_api_key"] = api_key
    save_json(CONFIG_FILE, config)
    print(json.dumps({"status": "ok", "message": "Gemini API key saved"}, indent=2))


def cmd_save(job_json: str) -> None:
    """Save a job to the bookmarks list (no duplicates by URL)."""
    job = json.loads(job_json)
    job["saved_at"] = datetime.now().isoformat()
    saved = load_json(SAVED_FILE, [])
    # Don't duplicate
    if not any(s.get("url") == job.get("url") for s in saved):
        saved.append(job)
        save_json(SAVED_FILE, saved)
    print(json.dumps({"status": "saved", "total_saved": len(saved)}, indent=2))


def cmd_saved() -> None:
    """List all saved/bookmarked jobs."""
    saved = load_json(SAVED_FILE, [])
    print(json.dumps({"saved_jobs": saved, "total": len(saved)}, indent=2, ensure_ascii=False))


def cmd_unsave(url: str) -> None:
    """Remove a saved job by its URL."""
    saved = load_json(SAVED_FILE, [])
    saved = [s for s in saved if s.get("url") != url]
    save_json(SAVED_FILE, saved)
    print(json.dumps({"status": "removed", "total_saved": len(saved)}, indent=2))


def cmd_history() -> None:
    """Show the search history with indexed entries."""
    history = load_json(HISTORY_FILE, [])
    for i, h in enumerate(history):
        h["index"] = i
    print(json.dumps({"searches": history}, indent=2, ensure_ascii=False))


def cmd_rerun(index_str: str) -> None:
    """Re-run a previous search by its history index."""
    history = load_json(HISTORY_FILE, [])
    index = int(index_str)
    if index < 0 or index >= len(history):
        print(json.dumps({"status": "error", "message": f"Invalid index. History has {len(history)} entries."}, indent=2))
        return
    params = history[index]["params"]
    cmd_search(json.dumps(params))


def main() -> None:
    """CLI entry point for the job_hunter skill."""
    if len(sys.argv) < 2:
        print("Usage: job_hunter.py <command> [args]", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    commands: dict[str, Any] = {
        "search": lambda: cmd_search(sys.argv[2]),
        "setkey": lambda: cmd_setkey(sys.argv[2]),
        "save": lambda: cmd_save(sys.argv[2]),
        "saved": lambda: cmd_saved(),
        "unsave": lambda: cmd_unsave(sys.argv[2]),
        "history": lambda: cmd_history(),
        "rerun": lambda: cmd_rerun(sys.argv[2]),
    }

    if command not in commands:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

    commands[command]()


if __name__ == "__main__":
    main()
