#!/usr/bin/env python3
"""
Fetch and parse a client's sitemap.xml, returning a list of page URLs.
Filters to service/area pages (skips assets, tags, author, media files).
"""
import argparse
import re
import sys
import urllib.request

SKIP_PATTERNS = [
    r"\.(jpg|jpeg|png|gif|webp|svg|css|js|pdf|zip|xml)$",
    r"/tag/", r"/category/", r"/author/", r"/feed", r"/wp-json",
    r"/page/\d+", r"/amp/?$", r"#", r"\?",
    r"/blog/page", r"/assets/", r"/uploads/",
    # Junk / non-content pages: these are not worth posting about or linking back to
    r"/about", r"/about-us", r"/aboutus", r"/our-story", r"/team", r"/meet-the-team",
    r"/sitemap", r"/sitemap.xml", r"/sitemap_index",
    r"/terms", r"/t&c", r"/t-and-c", r"/conditions", r"/legal", r"/disclaimer",
    r"/privacy", r"/privacy-policy", r"/cookie", r"/cookies", r"/gdpr",
    r"/contact", r"/contact-us", r"/contactus", r"/get-in-touch",
    r"/faq", r"/faqs", r"/help", r"/support",
    r"/login", r"/signin", r"/sign-up", r"/signup", r"/register", r"/account",
    r"/cart", r"/checkout", r"/wishlist", r"/my-account", r"/dashboard",
    r"/search", r"/404", r"/error", r"/under-construction", r"/coming-soon",
    r"/blog/?$", r"/news/?$", r"/press", r"/media-kit",
    # Blog POSTS are intentionally kept: individual blog posts (e.g. /blog/title)
    # are valid content and link-back targets. Only the blog index (/blog/?$)
    # and pagination (/blog/page) are dropped.
]


def fetch_sitemap(url: str, timeout: int = 25) -> list[str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/126.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", errors="replace")

    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", body, re.S)

    # Handle sitemap index (nested sitemaps) - one level deep
    if len(locs) > 0 and all(l.endswith((".xml", ".xml.gz")) for l in locs):
        nested = []
        for sub in locs[:20]:
            try:
                req2 = urllib.request.Request(sub, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req2, timeout=timeout) as r2:
                    body2 = r2.read().decode("utf-8", errors="replace")
                nested.extend(re.findall(r"<loc>\s*(.*?)\s*</loc>", body2, re.S))
            except Exception:
                continue
        locs = nested

    # Filter
    cleaned = []
    for l in locs:
        l = l.strip()
        if any(re.search(p, l, re.I) for p in SKIP_PATTERNS):
            continue
        if l not in cleaned:
            cleaned.append(l)
    return cleaned


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", help="sitemap URL, e.g. https://example.com/sitemap.xml")
    ap.add_argument("--out", default="", help="write URLs to file (one per line)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    urls = fetch_sitemap(args.url)
    if args.json:
        import json
        print(json.dumps(urls))
    else:
        for u in urls:
            print(u)
    if args.out:
        with open(args.out, "w") as f:
            f.write("\n".join(urls))
    print(f"# {len(urls)} URLs", file=sys.stderr)


if __name__ == "__main__":
    main()
