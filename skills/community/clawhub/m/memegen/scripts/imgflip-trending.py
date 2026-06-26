#!/usr/bin/env python3
"""
Scrape trending meme templates from Imgflip's "Top New" page.
No API key required — just plain HTTP scraping.

Usage:
    python3 imgflip-trending.py [--limit 20] [--json]

Output:
    JSON array of {id, name, url} for each trending template.
"""

import re
import json
import sys
import urllib.request

def fetch_trending(limit=30):
    """Scrape Imgflip's top-new meme templates page."""
    url = "https://imgflip.com/memetemplates?sort=top-new"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; MemeSkill/1.0)"
    })

    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching Imgflip: {e}", file=sys.stderr)
        return []

    # Extract template IDs and slugs from links like /meme/123456/Template-Name
    template_links = re.findall(r'/meme/(\d+)/([^"\'<>\s]+)', html)

    # Extract image URLs like src="//i.imgflip.com/abc123.jpg"
    image_urls = re.findall(r'src="(//i\.imgflip\.com/[^"]+)"', html)

    # Deduplicate templates by ID (same template may appear multiple times)
    seen = set()
    templates = []
    img_idx = 0

    for template_id, slug in template_links:
        if template_id in seen:
            continue
        seen.add(template_id)

        name = slug.replace("-", " ").title()

        # Try to match with an image URL
        img_url = None
        if img_idx < len(image_urls):
            img_url = "https:" + image_urls[img_idx]
            img_idx += 1

        templates.append({
            "id": template_id,
            "name": name,
            "url": img_url or f"https://imgflip.com/meme/{template_id}/{slug}"
        })

        if len(templates) >= limit:
            break

    return templates


def main():
    limit = 20

    # Simple arg parsing
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
        elif arg == "--help" or arg == "-h":
            print(__doc__.strip())
            sys.exit(0)

    templates = fetch_trending(limit=limit)

    if not templates:
        print("No templates found.", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(templates, indent=2))
    print(f"\n# Found {len(templates)} trending templates", file=sys.stderr)


if __name__ == "__main__":
    main()
