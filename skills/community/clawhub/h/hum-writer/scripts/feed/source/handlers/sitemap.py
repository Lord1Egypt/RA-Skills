"""Sitemap handler -- walks an XML sitemap and extracts each linked article."""

import time
import requests
import xml.etree.ElementTree as ET

from .common import (
    DELAY,
    HEADERS,
    existing_urls,
    source_dir,
    make_filename,
    extract_article_with_meta,
    build_frontmatter,
)


def fetch_sitemap_urls(sitemap_url: str) -> list:
    """Fetch and parse a sitemap XML, return flat list of article URLs.

    Handles both regular sitemaps and sitemap indexes (recurses).
    """
    try:
        r = requests.get(sitemap_url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            print(f"    ! sitemap returned HTTP {r.status_code}: {sitemap_url}")
            return []
        root = ET.fromstring(r.content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = []
        for url_el in root.findall("sm:url", ns):
            loc = url_el.find("sm:loc", ns)
            if loc is not None and loc.text:
                urls.append(loc.text.strip())
        for sitemap_el in root.findall("sm:sitemap", ns):
            loc = sitemap_el.find("sm:loc", ns)
            if loc is not None and loc.text:
                urls.extend(fetch_sitemap_urls(loc.text.strip()))
        return urls
    except Exception as e:
        print(f"    ! sitemap parse error: {e}")
        return []


def crawl(source: dict, max_articles: int = 0, recrawl: bool = False) -> int:
    key = source["key"]
    name = source["name"]
    author = source["author"]
    sitemap_url = source["url"]

    out_dir = source_dir(key)
    out_dir.mkdir(parents=True, exist_ok=True)

    already = set() if recrawl else existing_urls(key)
    if already:
        print(f"   {len(already)} articles already saved -- skipping those")

    print(f"   fetching sitemap: {sitemap_url}")
    urls = fetch_sitemap_urls(sitemap_url)
    if not urls:
        print(f"   ! no URLs found in sitemap")
        return 0

    print(f"   {len(urls)} URLs in sitemap")

    saved = 0
    for url in urls:
        if max_articles and saved >= max_articles:
            break
        if url in already:
            continue

        result = extract_article_with_meta(url, key)
        if not result:
            print(f"   -> skipped: {url.split('/')[-1][:50]}")
            time.sleep(DELAY)
            continue

        title, date, content = result
        filename = make_filename(date, url)
        dest = out_dir / filename

        if not recrawl and dest.exists():
            continue

        print(f"   -> {title[:60]}")
        fm = build_frontmatter(title, date, url, key, name, author)
        dest.write_text(fm + content, encoding="utf-8")
        saved += 1
        time.sleep(DELAY)

    print(f"   done: {saved} new articles saved")
    return saved
