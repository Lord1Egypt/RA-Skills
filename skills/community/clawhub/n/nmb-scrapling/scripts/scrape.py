#!/usr/bin/env python3
"""
Scrapling quick scrape script
Usage:
    python3 scrape.py <url> [--css ".selector"] [--output output.json]
    python3 scrape.py <url> --stealthy  # 使用隐身模式过反爬
    python3 scrape.py <url> --dynamic   # 使用浏览器模式渲染JS
"""

import sys
import json
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Quick scrape with Scrapling')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--css', '-c', default='body', help='CSS selector (default: body)')
    parser.add_argument('--output', '-o', help='Output file (json/txt/md)')
    parser.add_argument('--stealthy', '-s', action='store_true', help='Use StealthyFetcher (bypass anti-bot)')
    parser.add_argument('--dynamic', '-d', action='store_true', help='Use DynamicFetcher (JS rendering)')
    parser.add_argument('--text-only', '-t', action='store_true', help='Extract text only')
    parser.add_argument('--headless', action='store_true', default=True, help='Headless mode (default: True)')

    args = parser.parse_args()

    # Import appropriate fetcher
    if args.stealthy:
        from scrapling.fetchers import StealthyFetcher
        page = StealthyFetcher.fetch(args.url, headless=args.headless)
    elif args.dynamic:
        from scrapling.fetchers import DynamicFetcher
        page = DynamicFetcher.fetch(args.url, headless=args.headless, network_idle=True)
    else:
        from scrapling.fetchers import Fetcher
        page = Fetcher.get(args.url)

    # Extract data
    elements = page.css(args.css)

    if args.text_only:
        data = [el.get_text(strip=True) for el in elements]
    else:
        data = []
        for el in elements:
            item = {
                'text': el.get_text(strip=True),
                'html': el.get(),
                'attributes': el.attrib,
            }
            data.append(item)

    # Output
    result = {
        'url': args.url,
        'selector': args.css,
        'count': len(data),
        'data': data,
    }

    if args.output:
        output_path = Path(args.output)
        if output_path.suffix == '.json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                for item in data:
                    if isinstance(item, dict):
                        f.write(item.get('text', '') + '\n\n')
                    else:
                        f.write(str(item) + '\n\n')
        print(f"Saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
