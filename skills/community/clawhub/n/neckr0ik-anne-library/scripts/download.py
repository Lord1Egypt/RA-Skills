#!/usr/bin/env python3
"""
Anne's Library Downloader - Download academic books and articles
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, quote
import subprocess
import tempfile

# Platform-specific downloaders
PLATFORMS = {
    "vitalsource": {
        "name": "VitalSource Bookshelf",
        "url_patterns": ["vitalsource.com", "bookshelf.vitalsource"],
        "requires_auth": True
    },
    "proquest": {
        "name": "ProQuest",
        "url_patterns": ["proquest.com"],
        "requires_auth": True
    },
    "ebsco": {
        "name": "EBSCOhost",
        "url_patterns": ["ebscohost.com", "search.ebsco"],
        "requires_auth": True
    },
    "jstor": {
        "name": "JSTOR",
        "url_patterns": ["jstor.org", "jstor.com"],
        "requires_auth": True
    },
    "springer": {
        "name": "Springer Link",
        "url_patterns": ["springer.com", "link.springer"],
        "requires_auth": False
    },
    "taylor_francis": {
        "name": "Taylor & Francis Online",
        "url_patterns": ["taylorfrancis.com", "tandfonline.com"],
        "requires_auth": True
    },
    "capella": {
        "name": "Capella University Library",
        "url_patterns": ["capella.alma.exlibrisgroup.com", "capella.edu"],
        "requires_auth": True
    }
}

def detect_platform(url: str) -> str:
    """Detect which platform the URL belongs to."""
    for platform, config in PLATFORMS.items():
        for pattern in config["url_patterns"]:
            if pattern in url.lower():
                return platform
    return "unknown"

def extract_doi(text: str) -> str:
    """Extract DOI from text or URL."""
    doi_pattern = r'10\.\d{4,}/[^\s]+'
    match = re.search(doi_pattern, text)
    return match.group(0) if match else None

def get_doi_from_book(title: str, author: str) -> str:
    """Search for DOI using book title and author."""
    import requests
    
    # Try Crossref API
    query = f"{title} {author}".strip()
    url = f"https://api.crossref.org/works?query={quote(query)}&rows=1"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data["message"]["total-results"] > 0:
            return data["message"]["items"][0]["DOI"]
    except Exception as e:
        print(f"Error searching Crossref: {e}")
    
    return None

def download_with_playwright(url: str, output_path: str, platform: str):
    """Download using Playwright for platforms that require JavaScript/auth."""
    script = f'''
const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const context = await browser.newContext();
    const page = await context.newPage();
    
    // Navigate to URL
    await page.goto('{url}', {{ waitUntil: 'networkidle' }});
    
    // Wait for content
    await page.waitForTimeout(2000);
    
    // Handle authentication if needed
    // (Would need credentials for institutional access)
    
    // Get PDF link or download directly
    const pdfLink = await page.$('a[href$=".pdf"]');
    if (pdfLink) {{
        const href = await pdfLink.getAttribute('href');
        console.log(href);
    }}
    
    await browser.close();
}})();
'''
    
    # Save and run script
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(script)
        temp_path = f.name
    
    try:
        result = subprocess.run(['node', temp_path], capture_output=True, text=True)
        return result.stdout.strip()
    finally:
        os.unlink(temp_path)

def download_book(title: str, author: str, output_dir: str = None):
    """Download a book by title and author."""
    output_dir = Path(output_dir or Path.home() / "Downloads" / "anne_library")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Searching for: {title} by {author}")
    
    # Get DOI
    doi = get_doi_from_book(title, author)
    if doi:
        print(f"Found DOI: {doi}")
    
    # Try to find direct download link
    # This is a placeholder - real implementation would need:
    # - Institution authentication
    # - Platform-specific download logic
    # - VitalSource SDK integration
    
    print(f"\nManual download required for: {title}")
    print(f"DOI: {doi or 'Not found'}")
    print(f"Suggested sources:")
    print(f"  - VitalSource: https://www.vitalsource.com")
    print(f"  - Taylor & Francis: https://www.taylorfrancis.com")
    print(f"  - Capella Library: https://capella.alma.exlibrisgroup.com")
    
    return {
        "title": title,
        "author": author,
        "doi": doi,
        "output_dir": str(output_dir),
        "status": "requires_manual_download"
    }

def main():
    parser = argparse.ArgumentParser(description="Download books and articles from academic libraries")
    parser.add_argument("--book", "-b", help="Book title to download")
    parser.add_argument("--author", "-a", help="Author name")
    parser.add_argument("--doi", "-d", help="DOI to download")
    parser.add_argument("--url", "-u", help="URL to download from")
    parser.add_argument("--list", "-l", help="File containing list of items to download")
    parser.add_argument("--output", "-o", help="Output directory", default=str(Path.home() / "Downloads" / "anne_library"))
    
    args = parser.parse_args()
    
    if args.book and args.author:
        result = download_book(args.book, args.author, args.output)
        print(json.dumps(result, indent=2))
    elif args.doi:
        print(f"DOI: {args.doi}")
        # Would need platform-specific download logic
    elif args.url:
        platform = detect_platform(args.url)
        print(f"Platform: {PLATFORMS.get(platform, {}).get('name', 'Unknown')}")
        print(f"URL: {args.url}")
    elif args.list:
        with open(args.list) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 2:
                        download_book(parts[0].strip(), parts[1].strip(), args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()