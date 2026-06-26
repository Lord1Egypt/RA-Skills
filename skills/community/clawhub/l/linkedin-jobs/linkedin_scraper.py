"""
LinkedIn Job Scraper for OpenClaw
Scrapes LinkedIn job listings using the public job search endpoint (no login required).
Outputs JSON to stdout for agent consumption.

Usage:
    python linkedin_scraper.py --keywords "AI Engineer" --location "Bengaluru, India" --max-pages 2
"""

import requests
import json
import sys
import time
import random
import argparse
from dataclasses import dataclass, asdict, field
from typing import Optional
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────
#  Configuration Loading
# ─────────────────────────────────────────────

SKILL_DIR = Path(__file__).parent
GEO_IDS_FILE = SKILL_DIR / "geo_ids.json"
CONFIG_FILE = SKILL_DIR / "config.json"
CONFIG_EXAMPLE_FILE = SKILL_DIR / "config.example.json"


def load_config() -> dict:
    """Load configuration from config.json or fall back to defaults."""
    config = {
        "defaults": {
            "experience": "2",
            "remote": "1,3",
            "date_posted": "r86400",
            "max_pages": 2,
            "job_type": "",
        },
        "scraper": {
            "delay_min": 1.5,
            "delay_max": 3.5,
            "fetch_details": True,
            "timeout": 15,
        },
        "notifications": {
            "notify_on_empty": False,
            "max_jobs_per_notification": 20,
            "include_tech_stack": True,
            "include_requirements": True,
            "include_role_summary": True,
            "description_preview_length": 300,
            "group_by_location": True,
        },
        "custom_geo_ids": {},
    }

    # Try to load user config
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                # Merge user config (shallow merge per section)
                for key in ["defaults", "scraper", "notifications", "custom_geo_ids"]:
                    if key in user_config and isinstance(user_config[key], dict):
                        if key == "custom_geo_ids":
                            config[key] = user_config[key]
                        else:
                            config[key].update(user_config[key])
        except Exception as e:
            print(f"[Warning] Failed to load config.json: {e}", file=sys.stderr)

    return config


def load_geo_ids() -> dict:
    """Load geo IDs from geo_ids.json file."""
    geo_ids = {}

    if GEO_IDS_FILE.exists():
        try:
            with open(GEO_IDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Flatten the nested structure
                for region, cities in data.items():
                    if isinstance(cities, dict) and not region.startswith("_"):
                        for city, geo_id in cities.items():
                            if not city.startswith("_"):
                                geo_ids[city.lower()] = geo_id
        except Exception as e:
            print(f"[Warning] Failed to load geo_ids.json: {e}", file=sys.stderr)

    # Load custom geo IDs from config
    config = load_config()
    custom_ids = config.get("custom_geo_ids", {})
    for city, geo_id in custom_ids.items():
        if not city.startswith("_"):
            geo_ids[city.lower()] = geo_id

    return geo_ids


# Load on module import
GEO_IDS = load_geo_ids()
CONFIG = load_config()


def lookup_geo_id(location: str) -> Optional[str]:
    """Look up geo ID for a location string. Returns None if not found."""
    if not location:
        return None

    # Try exact match first
    loc_lower = location.lower().strip()
    if loc_lower in GEO_IDS:
        return GEO_IDS[loc_lower]

    # Try city name only (before comma)
    city = location.split(",")[0].strip().lower()
    if city in GEO_IDS:
        return GEO_IDS[city]

    # Try without common suffixes
    for suffix in [" india", " usa", " uk", " city"]:
        cleaned = city.replace(suffix, "").strip()
        if cleaned in GEO_IDS:
            return GEO_IDS[cleaned]

    return None


# ─────────────────────────────────────────────
#  Data Model
# ─────────────────────────────────────────────


@dataclass
class JobListing:
    title: str
    company: str
    location: str
    job_id: str
    url: str
    posted_date: str = ""
    employment_type: str = ""
    experience_level: str = ""
    description: str = ""
    requirements: str = ""
    tech_stack: str = ""
    role_summary: str = ""
    scraped_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ─────────────────────────────────────────────
#  Scraper
# ─────────────────────────────────────────────


class LinkedInScraper:
    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    JOB_DETAIL_URL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.linkedin.com/",
    }

    def __init__(
        self,
        delay_min: float = None,
        delay_max: float = None,
        fetch_details: bool = None,
        timeout: int = None,
    ):
        scraper_config = CONFIG.get("scraper", {})
        self.delay_min = (
            delay_min if delay_min is not None else scraper_config.get("delay_min", 1.5)
        )
        self.delay_max = (
            delay_max if delay_max is not None else scraper_config.get("delay_max", 3.5)
        )
        self.fetch_details = (
            fetch_details
            if fetch_details is not None
            else scraper_config.get("fetch_details", True)
        )
        self.timeout = (
            timeout if timeout is not None else scraper_config.get("timeout", 15)
        )
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def _sleep(self):
        time.sleep(random.uniform(self.delay_min, self.delay_max))

    def _log(self, msg: str):
        """Log to stderr so it doesn't interfere with JSON output."""
        print(msg, file=sys.stderr)

    def search_jobs(
        self,
        keywords: str,
        location: str = "",
        geo_id: str = "",
        date_posted: str = "",
        experience: str = "",
        job_type: str = "",
        remote: str = "",
        max_pages: int = None,
    ) -> list[JobListing]:
        """Search LinkedIn job listings."""
        all_jobs: list[JobListing] = []
        page_size = 25

        # Use config defaults if not specified
        defaults = CONFIG.get("defaults", {})
        if max_pages is None:
            max_pages = defaults.get("max_pages", 2)
        if not date_posted:
            date_posted = defaults.get("date_posted", "r86400")

        # Hybrid location strategy: use geo_id if available, otherwise text location
        resolved_geo_id = geo_id or lookup_geo_id(location)

        params = {
            "keywords": keywords,
            "location": location if not resolved_geo_id else "",
            "geoId": resolved_geo_id or "",
            "f_TPR": date_posted,
            "f_E": experience,
            "f_JT": job_type,
            "f_WT": remote,
            "start": 0,
            "count": page_size,
        }
        # Remove empty params
        params = {k: v for k, v in params.items() if v}

        location_display = location or "Worldwide"
        if resolved_geo_id:
            self._log(
                f"[LinkedIn] Searching: '{keywords}' in '{location_display}' (geo_id: {resolved_geo_id})"
            )
        else:
            self._log(
                f"[LinkedIn] Searching: '{keywords}' in '{location_display}' (text search)"
            )

        for page in range(max_pages):
            params["start"] = page * page_size
            url = f"{self.BASE_URL}?{urlencode(params)}"
            self._log(f"  -> Page {page + 1} (start={params['start']})")

            try:
                resp = self.session.get(url, timeout=self.timeout)
                resp.raise_for_status()
            except requests.RequestException as e:
                self._log(f"  [!] Request failed: {e}")
                break

            soup = BeautifulSoup(resp.text, "html.parser")
            job_cards = soup.find_all("div", class_="base-card")

            if not job_cards:
                self._log("  -> No more results.")
                break

            for card in job_cards:
                job = self._parse_job_card(card)
                if job:
                    if self.fetch_details:
                        self._enrich_with_details(job)
                        self._sleep()
                    all_jobs.append(job)

            self._log(f"  -> Collected {len(all_jobs)} jobs so far")
            self._sleep()

        return all_jobs

    def _parse_job_card(self, card) -> Optional[JobListing]:
        try:
            title_tag = card.find("h3", class_="base-search-card__title")
            company_tag = card.find("h4", class_="base-search-card__subtitle")
            location_tag = card.find("span", class_="job-search-card__location")
            link_tag = card.find("a", class_="base-card__full-link")
            time_tag = card.find("time")

            url = link_tag["href"].split("?")[0] if link_tag else ""
            job_id = url.rstrip("/").split("-")[-1] if url else ""

            return JobListing(
                title=title_tag.get_text(strip=True) if title_tag else "N/A",
                company=company_tag.get_text(strip=True) if company_tag else "N/A",
                location=location_tag.get_text(strip=True) if location_tag else "N/A",
                job_id=job_id,
                url=url,
                posted_date=time_tag.get("datetime", "") if time_tag else "",
            )
        except Exception as e:
            self._log(f"  [!] Card parse error: {e}")
            return None

    def _enrich_with_details(self, job: JobListing):
        """Fetch and parse the job detail page for description + metadata."""
        if not job.job_id:
            return
        url = self.JOB_DETAIL_URL.format(job_id=job.job_id)
        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            # Description
            desc_div = soup.find("div", class_="show-more-less-html__markup")
            if desc_div:
                full_desc = desc_div.get_text(separator="\n", strip=True)
                job.description = full_desc[:3000]

                # Extract key information from description
                self._extract_job_details(job, full_desc)

            # Criteria (employment type, experience level)
            for item in soup.find_all("li", class_="description__job-criteria-item"):
                header = item.find("h3")
                value = item.find("span")
                if header and value:
                    h = header.get_text(strip=True).lower()
                    v = value.get_text(strip=True)
                    if "employment" in h:
                        job.employment_type = v
                    elif "seniority" in h or "experience" in h:
                        job.experience_level = v

        except requests.RequestException as e:
            self._log(f"  [!] Detail fetch failed for {job.job_id}: {e}")

    def _extract_job_details(self, job: JobListing, description: str):
        """Extract requirements, tech stack, and role summary from description."""
        desc_lower = description.lower()
        lines = description.split("\n")

        notifications_config = CONFIG.get("notifications", {})

        # Common tech keywords to look for
        tech_keywords = [
            "python",
            "java",
            "javascript",
            "typescript",
            "react",
            "angular",
            "vue",
            "node.js",
            "nodejs",
            "django",
            "flask",
            "fastapi",
            "spring",
            "kubernetes",
            "docker",
            "aws",
            "azure",
            "gcp",
            "tensorflow",
            "pytorch",
            "spark",
            "sql",
            "postgresql",
            "mongodb",
            "redis",
            "kafka",
            "elasticsearch",
            "git",
            "ci/cd",
            "jenkins",
            "terraform",
            "linux",
            "rest",
            "graphql",
            "machine learning",
            "ml",
            "ai",
            "deep learning",
            "nlp",
            "computer vision",
            "data science",
            "pandas",
            "numpy",
            "scikit-learn",
            "tableau",
            "power bi",
            "golang",
            "go",
            "rust",
            "c++",
            "c#",
            ".net",
            "ruby",
            "rails",
            "php",
            "laravel",
            "swift",
            "kotlin",
            "flutter",
            "react native",
            "next.js",
            "vue.js",
            "svelte",
            "tailwind",
            "sass",
            "webpack",
            "vite",
        ]

        # Find tech stack
        if notifications_config.get("include_tech_stack", True):
            found_tech = []
            for tech in tech_keywords:
                if tech in desc_lower:
                    # Capitalize properly
                    if tech in ["aws", "gcp", "sql", "ci/cd", "ml", "ai", "nlp", "api"]:
                        found_tech.append(tech.upper())
                    elif tech == "node.js":
                        found_tech.append("Node.js")
                    elif tech == "next.js":
                        found_tech.append("Next.js")
                    elif tech == "vue.js":
                        found_tech.append("Vue.js")
                    elif tech == "postgresql":
                        found_tech.append("PostgreSQL")
                    elif tech == "mongodb":
                        found_tech.append("MongoDB")
                    elif tech == "elasticsearch":
                        found_tech.append("Elasticsearch")
                    elif tech == "graphql":
                        found_tech.append("GraphQL")
                    elif tech == "c++":
                        found_tech.append("C++")
                    elif tech == "c#":
                        found_tech.append("C#")
                    elif tech == ".net":
                        found_tech.append(".NET")
                    else:
                        found_tech.append(tech.title())

            job.tech_stack = ", ".join(found_tech[:10]) if found_tech else ""

        # Extract experience requirements
        if notifications_config.get("include_requirements", True):
            import re

            exp_patterns = [
                r"(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)",
                r"(?:experience|exp)(?:\s+of)?\s*:?\s*(\d+)\+?\s*(?:years?|yrs?)",
                r"(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)",
            ]

            exp_matches = []
            for pattern in exp_patterns:
                matches = re.findall(pattern, desc_lower)
                if matches:
                    if isinstance(matches[0], tuple):
                        exp_matches.append(f"{matches[0][0]}-{matches[0][1]} years")
                    else:
                        exp_matches.append(f"{matches[0]}+ years")
                    break

            job.requirements = exp_matches[0] if exp_matches else ""

        # Extract role summary (first meaningful paragraph)
        if notifications_config.get("include_role_summary", True):
            preview_length = notifications_config.get("description_preview_length", 300)
            role_lines = []
            for line in lines[:10]:
                line = line.strip()
                if len(line) > 50 and not line.startswith(("•", "-", "*", "·")):
                    role_lines.append(line)
                    if len(" ".join(role_lines)) > preview_length:
                        break

            job.role_summary = (
                " ".join(role_lines)[:preview_length] if role_lines else ""
            )


# ─────────────────────────────────────────────
#  CLI Interface
# ─────────────────────────────────────────────


def main():
    defaults = CONFIG.get("defaults", {})
    scraper_config = CONFIG.get("scraper", {})

    parser = argparse.ArgumentParser(
        description="LinkedIn Job Scraper for OpenClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python linkedin_scraper.py --keywords "AI Engineer" --location "Bengaluru, India"
  python linkedin_scraper.py --keywords "Python Developer" --location "San Francisco" --experience "2" --remote "2,3"
  python linkedin_scraper.py --keywords "Data Scientist" --date-posted "r604800" --max-pages 3

Filter Codes:
  --date-posted: r86400 (24h), r604800 (1wk), r2592000 (1mo)
  --experience:  1=Intern, 2=Entry, 3=Associate, 4=Mid-Senior, 5=Director, 6=Executive
  --job-type:    F=Full-time, P=Part-time, C=Contract, T=Temporary, I=Internship
  --remote:      1=On-site, 2=Remote, 3=Hybrid

Supported Cities (100+ worldwide):
  India: Bengaluru, Noida, Hyderabad, Mumbai, Delhi, Pune, Chennai, Gurugram...
  USA: San Francisco, New York, Seattle, Austin, Boston, Los Angeles, Chicago...
  UK: London, Manchester, Edinburgh, Cambridge, Oxford, Bristol...
  Europe: Berlin, Amsterdam, Dublin, Paris, Munich, Zurich, Stockholm...
  And many more! See geo_ids.json for full list.
        """,
    )

    parser.add_argument("--keywords", "-k", required=True, help="Job search keywords")
    parser.add_argument("--location", "-l", default="", help="Location (city, country)")
    parser.add_argument(
        "--geo-id", "-g", default="", help="LinkedIn geo ID (overrides location lookup)"
    )
    parser.add_argument(
        "--date-posted",
        "-d",
        default="",
        help=f"Time filter (default: {defaults.get('date_posted', 'r86400')})",
    )
    parser.add_argument(
        "--experience", "-e", default="", help="Experience levels (comma-separated)"
    )
    parser.add_argument(
        "--job-type", "-j", default="", help="Job types (comma-separated)"
    )
    parser.add_argument(
        "--remote", "-r", default="", help="Remote options (comma-separated)"
    )
    parser.add_argument(
        "--max-pages",
        "-p",
        type=int,
        default=None,
        help=f"Max pages to scrape (default: {defaults.get('max_pages', 2)})",
    )
    parser.add_argument(
        "--no-details", action="store_true", help="Skip fetching job descriptions"
    )
    parser.add_argument(
        "--delay-min",
        type=float,
        default=None,
        help=f"Min delay between requests (default: {scraper_config.get('delay_min', 1.5)})",
    )
    parser.add_argument(
        "--delay-max",
        type=float,
        default=None,
        help=f"Max delay between requests (default: {scraper_config.get('delay_max', 3.5)})",
    )

    args = parser.parse_args()

    try:
        scraper = LinkedInScraper(
            delay_min=args.delay_min,
            delay_max=args.delay_max,
            fetch_details=not args.no_details,
        )

        jobs = scraper.search_jobs(
            keywords=args.keywords,
            location=args.location,
            geo_id=args.geo_id,
            date_posted=args.date_posted,
            experience=args.experience,
            job_type=args.job_type,
            remote=args.remote,
            max_pages=args.max_pages,
        )

        # Output JSON to stdout
        result = {
            "success": True,
            "query": {
                "keywords": args.keywords,
                "location": args.location,
                "experience": args.experience,
                "remote": args.remote,
                "date_posted": args.date_posted
                or defaults.get("date_posted", "r86400"),
            },
            "total_jobs": len(jobs),
            "jobs": [asdict(j) for j in jobs],
        }

        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "query": {
                "keywords": args.keywords,
                "location": args.location,
            },
            "total_jobs": 0,
            "jobs": [],
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
