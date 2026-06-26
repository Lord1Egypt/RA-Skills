#!/usr/bin/env python3
"""
GitHub Trending Scraper
Scrapes https://github.com/trending and returns structured JSON.

Usage:
  python3 github_trending.py                    # All languages, today
  python3 github_trending.py --language python   # Python repos only
  python3 github_trending.py --since weekly      # This week
  python3 github_trending.py --output /tmp/trending.json
  python3 github_trending.py --top 25            # Top 25 repos
"""

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone


GITHUB_TRENDING_URL = "https://github.com/trending"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def fetch_trending(language: str = "", since: str = "daily") -> list[dict]:
    """Fetch trending repos from GitHub.

    Args:
        language: Filter by programming language (e.g. 'python', 'rust'). Empty for all.
        since: Time range - 'daily', 'weekly', or 'monthly'.

    Returns:
        List of dicts with keys: rank, owner, name, full_name, url, description,
        language, stars, forks, stars_today
    """
    url = GITHUB_TRENDING_URL
    if language:
        url += f"/{language}"
    url += f"?since={since}"

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return []

    articles = re.findall(r"<article.*?</article>", html, re.DOTALL)
    repos = []

    for i, art in enumerate(articles, 1):
        # Repo full name from href (skip login/other links)
        hrefs = re.findall(r'href="(/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)"', art)
        if not hrefs:
            continue
        repo_path = hrefs[0]
        parts = repo_path.strip("/").split("/")
        if len(parts) != 2:
            continue
        owner, name = parts

        # Description
        desc_match = re.search(
            r'<p\s+class="[^"]*col-9[^"]*"[^>]*>\s*(.*?)\s*</p>', art, re.DOTALL
        )
        description = ""
        if desc_match:
            description = re.sub(r"<[^>]+>", "", desc_match.group(1)).strip()

        # Language
        lang_match = re.search(r'itemprop="programmingLanguage">(.*?)<', art)
        language_name = lang_match.group(1).strip() if lang_match else ""

        # Total stars (number appears after SVG icon inside stargazers link)
        stars_match = re.search(
            r'href="/' + re.escape(owner + "/" + name) + r'/stargazers".*?(\d[\d,]+)\s*</a>',
            art,
            re.DOTALL,
        )
        total_stars = 0
        if stars_match:
            total_stars = int(stars_match.group(1).replace(",", ""))

        # Forks (number appears after SVG icon inside forks link)
        forks_match = re.search(
            r'href="/' + re.escape(owner + "/" + name) + r'/forks".*?(\d[\d,]+)\s*</a>',
            art,
            re.DOTALL,
        )
        forks = 0
        if forks_match:
            forks = int(forks_match.group(1).replace(",", ""))

        # Stars today/this week/this month
        stars_period_match = re.search(r"([\d,]+)\s*stars?\s*(today|this week|this month)", art)
        stars_period = 0
        stars_period_label = ""
        if stars_period_match:
            stars_period = int(stars_period_match.group(1).replace(",", ""))
            stars_period_label = stars_period_match.group(2)

        repos.append(
            {
                "rank": i,
                "owner": owner,
                "name": name,
                "full_name": f"{owner}/{name}",
                "url": f"https://github.com{repo_path}",
                "description": description,
                "language": language_name,
                "stars": total_stars,
                "forks": forks,
                "stars_period": stars_period,
                "stars_period_label": stars_period_label,
            }
        )

    return repos


def main():
    parser = argparse.ArgumentParser(description="Scrape GitHub Trending repos")
    parser.add_argument(
        "--language", "-l", default="", help="Filter by language (e.g. python, rust, go)"
    )
    parser.add_argument(
        "--since",
        "-s",
        default="daily",
        choices=["daily", "weekly", "monthly"],
        help="Time range (default: daily)",
    )
    parser.add_argument("--top", "-n", type=int, default=25, help="Number of repos (default: 25)")
    parser.add_argument("--output", "-o", help="Output JSON file path (default: stdout)")
    parser.add_argument(
        "--compact", action="store_true", help="Output compact JSON (no indentation)"
    )
    args = parser.parse_args()

    repos = fetch_trending(language=args.language, since=args.since)
    repos = repos[: args.top]

    result = {
        "source": "github-trending",
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "language": args.language or "all",
        "since": args.since,
        "count": len(repos),
        "repos": repos,
    }

    indent = None if args.compact else 2
    output = json.dumps(result, ensure_ascii=False, indent=indent)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Saved {len(repos)} repos to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
