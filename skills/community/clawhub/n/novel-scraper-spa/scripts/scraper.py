#!/usr/bin/env python3.11
"""
Main scraper script for novel-scraper-spa

CLI tool for scraping novels from websites, supporting both static and SPA sites.
"""

import argparse
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

from browser import get_html, cleanup

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

NOVELS_DIR = Path.home() / ".openclaw" / "workspace" / "novels"


def detect_spa(url: str, html: Optional[str] = None) -> bool:
    """
    Detect if a website is SPA by checking for common patterns.

    Args:
        url: Target URL
        html: Optional HTML content to analyze

    Returns:
        True if likely SPA, False otherwise
    """
    spa_indicators = [
        r'<div[^>]*id=["\']app["\']',
        r'<div[^>]*id=["\']root["\']',
        r"data-reactroot",
        r"<script[^>]*window\.__REACT__",
        r"<script[^>]*window\.__STATE__",
        r"window\.__INITIAL_STATE__",
        r"v-app=",
        r"data-v-",
    ]

    if html is None:
        try:
            response = requests.get(url, timeout=10)
            html = response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return False

    for pattern in spa_indicators:
        if re.search(pattern, html):
            logger.info(f"SPA indicator found: {pattern}")
            return True

    return False


def extract_content(html: str, url: str) -> Optional[str]:
    """
    Extract novel content from HTML using BeautifulSoup.

    Args:
        html: HTML content
        url: Source URL for context

    Returns:
        Extracted text content or None
    """
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("article") or soup.find("div", class_="content")

    if article:
        for selector in ["script", "style", "nav", "footer", "header", "aside"]:
            for tag in article.find_all(selector):
                tag.decompose()

        content = article.get_text("\n", strip=True)

        title = soup.find("title")
        if title:
            content = f"# {title.get_text(strip=True)}\n\n{content}"

        return content

    return None


def save_content(content: str, url: str, output_path: Optional[str] = None) -> str:
    """
    Save content to file.

    Args:
        content: Text content to save
        url: Source URL
        output_path: Optional custom output path

    Returns:
        Path to saved file
    """
    if output_path:
        output_file = Path(output_path)
    else:
        output_file = (
            NOVELS_DIR / f"scraped_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"Content saved to: {output_file}")
    return str(output_file)


def scrape_url(
    url: str, output_path: Optional[str] = None, force_spa: bool = False
) -> Optional[str]:
    """
    Scrape content from URL, auto-detecting SPA vs static.

    Args:
        url: Target URL
        output_path: Optional custom output path
        force_spa: Force SPA mode (use browser)

    Returns:
        Path to saved file or None if failed
    """
    logger.info(f"Processing: {url}")

    html = None
    use_browser = force_spa

    if not use_browser:
        use_browser = detect_spa(url)

    if use_browser:
        logger.info("Using browser (SPA detected)")
        html = get_html(url)
    else:
        logger.info("Using requests (static site)")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            html = response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            if detect_spa(url):
                logger.info("Retrying with browser...")
                html = get_html(url)

    if not html:
        logger.error("Failed to retrieve content")
        return None

    content = extract_content(html, url)

    if not content:
        logger.error("Failed to extract content")
        return None

    return save_content(content, url, output_path)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scrape novel content from websites (static or SPA)"
    )
    parser.add_argument("--url", help="Target URL to scrape")
    parser.add_argument("--book", help="Book name for output filename")
    parser.add_argument("--chapter", help="Chapter number/title")
    parser.add_argument(
        "-o", "--output", help="Output file path (default: ~/novels/scraped_*.txt)"
    )
    parser.add_argument(
        "--force-spa", action="store_true", help="Force using browser (SPA mode)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging"
    )

    args = parser.parse_args()

    if not args.url:
        parser.error("--url is required")

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Build output path from book and chapter if provided
        output_path = args.output
        if not output_path and args.book:
            chapter_str = args.chapter or "unknown"
            safe_book = re.sub(r'[^\w\u4e00-\u9fff-]', '_', args.book)
            safe_chapter = re.sub(r'[^\w\u4e00-\u9fff-]', '_', chapter_str)
            output_path = str(NOVELS_DIR / f"{safe_book}_{safe_chapter}.txt")

        result = scrape_url(args.url, output_path, args.force_spa)
        if result:
            print(f"Success: {result}")
            sys.exit(0)
        else:
            print("Failed to scrape content")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        cleanup()


if __name__ == "__main__":
    main()
