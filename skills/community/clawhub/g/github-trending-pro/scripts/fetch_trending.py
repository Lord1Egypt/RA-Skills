#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import date
from datetime import datetime
from datetime import timezone
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


BASE_URL = "https://github.com/trending"
VALID_SINCE = {"daily", "weekly", "monthly"}
LANGUAGE_COLORS = {
    "C": "#555555",
    "C#": "#178600",
    "C++": "#f34b7d",
    "Clojure": "#db5855",
    "CSS": "#563d7c",
    "Dart": "#00B4AB",
    "Go": "#00ADD8",
    "HTML": "#e34c26",
    "Java": "#b07219",
    "JavaScript": "#f1e05a",
    "Kotlin": "#A97BFF",
    "PHP": "#4F5D95",
    "Python": "#3572A5",
    "Ruby": "#701516",
    "Rust": "#dea584",
    "Shell": "#89e051",
    "Swift": "#F05138",
    "TypeScript": "#3178c6",
}


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def parse_int(value: str) -> int | None:
    match = re.search(r"[\d,]+", value)
    if not match:
        return None
    return int(match.group(0).replace(",", ""))


def is_english_text(value: str | None) -> bool:
    if not value:
        return False
    letters = sum(1 for char in value if char.isalpha())
    ascii_letters = sum(1 for char in value if char.isascii() and char.isalpha())
    return bool(letters) and ascii_letters / letters > 0.9


def truncate(value: str | None, limit: int = 220) -> str | None:
    if value is None or len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def title_from_description(description: str | None) -> str | None:
    if not description:
        return None
    sentence = re.split(r"(?<=[.!?。！？])\s+", description, maxsplit=1)[0]
    return truncate(sentence, 120)


def generated_at_from_report_date(report_date: str | None) -> str:
    if report_date:
        return f"{report_date}T00:00:00Z"
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_url(language: str | None, since: str, spoken_language: str | None) -> str:
    if since not in VALID_SINCE:
        raise ValueError(f"since must be one of: {', '.join(sorted(VALID_SINCE))}")

    url = BASE_URL
    if language:
        url += "/" + quote(language.strip().lower(), safe="")

    params = {"since": since}
    if spoken_language:
        params["spoken_language_code"] = spoken_language.strip()
    return f"{url}?{urlencode(params)}"


class TrendingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.repos: list[dict[str, Any]] = []
        self.current: dict[str, Any] | None = None
        self.capture: str | None = None
        self.buffer: list[str] = []
        self.link_kinds: list[str | None] = []
        self.in_repo_heading = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        classes = attr.get("class", "")

        if tag == "article" and "Box-row" in classes:
            self.current = {
                "repo": None,
                "url": None,
                "description": None,
                "language": None,
                "total_stars": None,
                "forks": None,
                "current_period_stars": None,
            }
            return

        if self.current is None:
            return

        if tag == "h2":
            self.in_repo_heading = True
            return

        if tag == "a":
            href = attr.get("href") or ""
            if (
                self.in_repo_heading
                and self.current.get("repo") is None
                and re.match(r"^/[^/\s]+/[^/\s]+/?$", href)
            ):
                self._begin_capture("repo")
                self.current["url"] = "https://github.com" + href.rstrip("/")
                self.link_kinds.append("repo")
            elif href.endswith("/stargazers"):
                self._begin_capture("stars")
                self.link_kinds.append("stars")
            elif href.endswith("/forks"):
                self._begin_capture("forks")
                self.link_kinds.append("forks")
            else:
                self.link_kinds.append(None)
            return

        if tag == "p" and self.current.get("description") is None:
            self._begin_capture("description")
            return

        if tag == "span" and attr.get("itemprop") == "programmingLanguage":
            self._begin_capture("language")
            return

        if tag == "span" and "float-sm-right" in classes:
            self._begin_capture("current_period_stars")

    def handle_data(self, data: str) -> None:
        if self.capture:
            self.buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return

        if tag == "a" and self.link_kinds:
            self._finish_capture(self.link_kinds.pop())
            return

        if tag == "h2":
            self.in_repo_heading = False
            return

        if tag == "p":
            self._finish_capture("description")
            return

        if tag == "span" and self.capture in {"language", "current_period_stars"}:
            self._finish_capture(self.capture)
            return

        if tag == "article":
            repo = self.current.get("repo")
            if repo:
                self.repos.append(self.current)
            self.current = None
            self.capture = None
            self.buffer = []
            self.in_repo_heading = False

    def _begin_capture(self, kind: str) -> None:
        self.capture = kind
        self.buffer = []

    def _finish_capture(self, kind: str | None) -> None:
        if not kind or not self.capture:
            return

        value = normalize_space("".join(self.buffer))
        if not value:
            self.capture = None
            self.buffer = []
            return

        if kind == "repo":
            self.current["repo"] = value.replace(" / ", "/").replace(" ", "")
        elif kind == "description":
            self.current["description"] = value
        elif kind == "language":
            self.current["language"] = value
        elif kind == "stars":
            self.current["total_stars"] = parse_int(value)
        elif kind == "forks":
            self.current["forks"] = parse_int(value)
        elif kind == "current_period_stars":
            self.current["current_period_stars"] = parse_int(value)

        self.capture = None
        self.buffer = []


def parse_trending_html(html: str, limit: int) -> list[dict[str, Any]]:
    parser = TrendingParser()
    parser.feed(html)

    repositories = parser.repos[:limit]
    for index, repo in enumerate(repositories, start=1):
        repo["rank"] = index
        repo.setdefault("description", None)
        repo.setdefault("language", None)
        repo.setdefault("total_stars", None)
        repo.setdefault("forks", None)
        repo.setdefault("current_period_stars", None)
        enrich_repository(repo)
    return repositories


def enrich_repository(repo: dict[str, Any], updated_at: str | None = None) -> dict[str, Any]:
    full_name = repo.get("repo")
    author = None
    name = None
    if isinstance(full_name, str) and "/" in full_name:
        author, name = full_name.split("/", 1)

    description = repo.get("description")
    language = repo.get("language")
    title = title_from_description(description)
    english_description = description if is_english_text(description) else None

    repo["full_name"] = full_name
    repo["author"] = author
    repo["name"] = name
    repo["author_avatar"] = f"https://github.com/{author}.png" if author else None
    repo["title"] = title
    repo["title_en"] = title if is_english_text(title) else None
    repo["summary"] = truncate(description)
    repo["summary_en"] = truncate(english_description)
    repo["primary_lang"] = language
    repo["lang_color"] = LANGUAGE_COLORS.get(language)
    if updated_at is not None:
        repo["updated_at"] = updated_at
    return repo


def fetch_html(url: str) -> str:
    request = Request(
        url,
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "codex-github-trending-skill/1.0",
        },
    )
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    url = build_url(args.language, args.since, args.spoken_language)
    html = fetch_html(url)
    updated_at = generated_at_from_report_date(args.date)
    repositories = parse_trending_html(html, args.limit)
    for repo in repositories:
        enrich_repository(repo, updated_at)
    return {
        "date": args.date or date.today().isoformat(),
        "since": args.since,
        "language": args.language,
        "spoken_language": args.spoken_language,
        "url": url,
        "updated_at": updated_at,
        "repositories": repositories,
    }


def format_number(value: int | None) -> str:
    if value is None:
        return "-"
    return f"{value:,}"


def format_delta(value: int | None) -> str:
    if value is None:
        return "-"
    return f"+{value:,}"


def escape_markdown_cell(value: Any) -> str:
    if value is None:
        return "-"
    return str(value).replace("|", "\\|").replace("\n", " ")


def period_label(since: str) -> str:
    return {"daily": "Today", "weekly": "This Week", "monthly": "This Month"}[since]


def render_markdown(report: dict[str, Any]) -> str:
    since = report["since"]
    label = period_label(since)
    title = f"# GitHub Trending {since.title()} Report"
    lines = [
        title,
        "",
        f"Date: {report['date']}",
        f"Range: {label} / {since.title()}",
        f"Programming Language: {report['language'] or 'All'}",
        f"Spoken Language: {report['spoken_language'] or 'All'}",
        f"Source: {report['url']}",
        "",
        "## Overview",
        "",
        f"| # | Repo | Total Stars | {label} | Lang | Description |",
        "|---|------|-------------|-------|------|-------------|",
    ]

    for repo in report["repositories"]:
        lines.append(
            "| {rank} | {repo} | {stars} | {period} | {lang} | {description} |".format(
                rank=repo["rank"],
                repo=escape_markdown_cell(repo["full_name"]),
                stars=format_number(repo["total_stars"]),
                period=format_delta(repo["current_period_stars"]),
                lang=escape_markdown_cell(repo["primary_lang"]),
                description=escape_markdown_cell(truncate(repo["summary"], 140)),
            )
        )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch GitHub Trending repositories as JSON.")
    parser.add_argument("--language", help="Programming language filter, for example python, rust, c++.")
    parser.add_argument("--since", choices=sorted(VALID_SINCE), default="daily", help="Trending date range.")
    parser.add_argument("--spoken-language", help="Spoken language code, for example zh or en.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum repositories to return.")
    parser.add_argument("--date", help="Report date to include in output; defaults to today.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = build_report(args)
    except (HTTPError, URLError, TimeoutError, ValueError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1

    if args.format == "markdown":
        print(render_markdown(report), end="")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
