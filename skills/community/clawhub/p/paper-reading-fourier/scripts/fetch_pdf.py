#!/usr/bin/env python3
"""Fetch a PDF from a local path, arXiv URL, or paper title.

Usage:
    python fetch_pdf.py <path_or_url_or_title> [--output <output_path>]

Input types (auto-detected):
  1. Local file path  -> validate existence
  2. arXiv URL        -> download PDF
  3. Paper title      -> search arXiv API, download the most relevant PDF

Prints the absolute path of the fetched PDF to stdout.
"""

import argparse
import os
import re
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Optional


ARXIV_API = "http://export.arxiv.org/api/query"


def is_local_pdf(path: str) -> bool:
    return os.path.isfile(path)


def is_arxiv_url(url: str) -> bool:
    return bool(re.search(r'arxiv\.org', url, re.IGNORECASE))


def normalize_arxiv_pdf_url(url: str) -> str:
    match = re.search(r'arxiv\.org/abs/([\d.]+)', url)
    if match:
        arxiv_id = match.group(1)
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    return url


def search_arxiv(title: str) -> Optional[str]:
    """Search arXiv by title and return the PDF URL of the most relevant result."""
    params = urllib.parse.urlencode({
        "search_query": f'ti:"{title}"',
        "max_results": "1",
        "sortBy": "relevance",
        "sortOrder": "descending",
    })
    url = f"{ARXIV_API}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "PaperReading/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8")
    except Exception as e:
        print(f"Error searching arXiv: {e}", file=sys.stderr)
        return None

    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(data)

    entries = root.findall("atom:entry", ns)
    if not entries:
        print(f"No results found on arXiv for title: {title}", file=sys.stderr)
        return None

    entry = entries[0]
    # Try to find PDF link
    links = entry.findall("atom:link", ns)
    for link in links:
        if link.get("title") == "pdf":
            return link.get("href")

    # Fallback: construct from arxiv id
    arxiv_id_elem = entry.find("arxiv:primary_id", ns)
    if arxiv_id_elem is not None and arxiv_id_elem.text:
        return f"https://arxiv.org/pdf/{arxiv_id_elem.text}.pdf"

    return None


def download_pdf(url: str, output: str) -> str:
    url = normalize_arxiv_pdf_url(url)
    print(f"Downloading from: {url}", file=sys.stderr)
    urllib.request.urlretrieve(url, output)
    return os.path.abspath(output)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch a PDF from local path, arXiv URL, or paper title"
    )
    parser.add_argument("source", help="Local PDF path, arXiv URL, or paper title")
    parser.add_argument("--output", "-o", default=None, help="Output PDF path (default: auto)")
    args = parser.parse_args()

    source = args.source

    # Case 1: local file
    if is_local_pdf(source):
        print(os.path.abspath(source))
        return

    # Case 2: URL
    if source.startswith("http://") or source.startswith("https://"):
        if not is_arxiv_url(source):
            print(f"Error: Only arXiv URLs are supported. Got: {source}", file=sys.stderr)
            sys.exit(1)
        output = args.output
        if not output:
            match = re.search(r'arxiv\.org/(?:abs|pdf)/([\d.]+)', source)
            if match:
                arxiv_id = match.group(1).replace(".", "_")
                output = f"arxiv_{arxiv_id}.pdf"
            else:
                output = "paper.pdf"
        pdf_path = download_pdf(source, output)
        print(pdf_path)
        return

    # Case 3: paper title -> search arXiv
    print(f"Searching arXiv for: {source}", file=sys.stderr)
    pdf_url = search_arxiv(source)
    if not pdf_url:
        print(f"Error: Could not find paper on arXiv: {source}", file=sys.stderr)
        sys.exit(1)

    print(f"Found: {pdf_url}", file=sys.stderr)
    output = args.output
    if not output:
        safe_title = re.sub(r'[^\w\s-]', '', source)[:50].strip().replace(" ", "_")
        output = f"{safe_title}.pdf"
    pdf_path = download_pdf(pdf_url, output)
    print(pdf_path)


if __name__ == "__main__":
    main()
