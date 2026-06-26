"""Shared helpers for knowledge-base crawl handlers."""

import os
import re
import hashlib
import sys
import requests
import trafilatura
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from slugify import slugify

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config

_CFG = load_config()
KNOWLEDGE_DIR = _CFG["knowledge_dir"]
INDEX_FILE = KNOWLEDGE_DIR / "index.md"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

DELAY = 1.0  # seconds between requests


# -- Paths -------------------------------------------------------------------

def source_dir(source_key: str) -> Path:
    return KNOWLEDGE_DIR / source_key

def images_dir(source_key: str) -> Path:
    d = source_dir(source_key) / "images"
    d.mkdir(parents=True, exist_ok=True)
    return d


# -- De-dup ------------------------------------------------------------------

def existing_urls(source_key: str) -> set:
    """Return set of URLs already saved for this source (parsed from frontmatter)."""
    urls = set()
    d = source_dir(source_key)
    if not d.exists():
        return urls
    for f in d.glob("*.md"):
        try:
            content = f.read_text(errors="ignore")
        except Exception:
            continue
        m = re.search(r"^url:\s*(.+)$", content, re.MULTILINE)
        if m:
            urls.add(m.group(1).strip())
    return urls


# -- Filenames / frontmatter -------------------------------------------------

def parse_date(entry) -> str:
    """Extract ISO date from a feedparser entry."""
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            return datetime(*t[:3]).strftime("%Y-%m-%d")
    return datetime.today().strftime("%Y-%m-%d")

def make_filename(date: str, url_or_slug: str) -> str:
    """Build a YYYY-MM-DD-slug.md filename."""
    if "://" in url_or_slug:
        basis = urlparse(url_or_slug).path.strip("/").split("/")[-1] or url_or_slug
    else:
        basis = url_or_slug
    slug_part = slugify(basis, max_length=80)
    return f"{date}-{slug_part}.md"

def build_frontmatter(
    title: str,
    date: str,
    url: str,
    source_key: str,
    source_name: str,
    author: str,
    extra: Optional[dict] = None,
) -> str:
    """Build a YAML frontmatter block for a crawled article."""
    slug = slugify(urlparse(url).path.strip("/").split("/")[-1] or title, max_length=80)
    lines = [
        "---",
        f'title: "{title.replace(chr(34), chr(39))}"',
        f"date: {date}",
        f"slug: {slug}",
        f"url: {url}",
        f"source: {source_key}",
        f'source_name: "{source_name}"',
        f'author: "{author}"',
    ]
    if extra:
        for k, v in extra.items():
            if v is None:
                continue
            if isinstance(v, str):
                lines.append(f'{k}: "{v.replace(chr(34), chr(39))}"')
            else:
                lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append("")
    return "\n".join(lines)


# -- Images ------------------------------------------------------------------

def download_image(url: str, source_key: str) -> Optional[str]:
    """Download image, return relative path or None on failure."""
    try:
        ext = os.path.splitext(urlparse(url).path)[-1].split("?")[0] or ".jpg"
        if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"):
            ext = ".jpg"
        name = hashlib.md5(url.encode()).hexdigest()[:12] + ext
        dest = images_dir(source_key) / name
        if dest.exists():
            return f"images/{name}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200 and len(r.content) > 500:
            dest.write_bytes(r.content)
            return f"images/{name}"
    except Exception:
        pass
    return None

def localise_images(markdown: str, source_key: str) -> str:
    """Download all images in markdown and replace URLs with local paths."""
    def replace(m):
        alt, url = m.group(1), m.group(2)
        if url.startswith("data:"):
            return m.group(0)
        local = download_image(url, source_key)
        if local:
            return f"![{alt}]({local})"
        return m.group(0)
    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace, markdown)


# -- Extraction --------------------------------------------------------------

def extract_article(url: str, source_key: str, download_images: bool = True) -> Optional[str]:
    """Fetch URL, extract clean markdown, optionally download images."""
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None
        text = trafilatura.extract(
            downloaded,
            include_images=download_images,
            include_links=False,
            output_format="markdown",
            favor_recall=True,
        )
        if not text or len(text) < 200:
            return None
        if download_images:
            text = localise_images(text, source_key)
        return text
    except Exception as e:
        print(f"    ! extraction error: {e}")
        return None

def extract_article_with_meta(url: str, source_key: str) -> Optional[tuple]:
    """Fetch URL, return (title, date, content) tuple or None."""
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None
        meta = trafilatura.extract_metadata(downloaded)
        content = trafilatura.extract(
            downloaded,
            include_images=True,
            include_links=False,
            output_format="markdown",
            favor_recall=True,
        )
        if not content or len(content) < 200:
            return None
        content = localise_images(content, source_key)
        title = (meta.title if meta and meta.title else None) or urlparse(url).path.strip("/").split("/")[-1]
        date = (meta.date if meta and meta.date else None) or datetime.today().strftime("%Y-%m-%d")
        if date and len(date) > 10:
            date = date[:10]
        return title, date, content
    except Exception as e:
        print(f"    ! extraction error: {e}")
        return None
