#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

URL_RE = re.compile(r'https?://[^\s)>"]+')


def load_config(path):
    if not path:
        return {}
    return json.loads(Path(path).read_text())


def issue_from_config(config):
    newspaper = config.get('newspaper', {})
    design = config.get('design', {})
    issue = config.get('issue', {})
    return {
        'title': newspaper.get('title') or 'The Non-Annoying News',
        'subtitle': newspaper.get('subtitle') or 'Personal newspaper',
        'language': newspaper.get('language') or 'en',
        'date': datetime.now(timezone.utc).date().isoformat(),
        'pageSize': design.get('pageSize') or 'A4',
        'maxPages': issue.get('maxPages') or 3,
        'onboardingComplete': bool(config.get('onboarding', {}).get('complete', False)),
    }


def clean_url(url):
    return url.rstrip('.,;:')


def collect(text, *, signal_type='manual_urls', signal_priority=100, config=None):
    config = config or {}
    sources = []
    for line in text.splitlines():
        raw = line.strip()
        if not raw:
            continue
        urls = [clean_url(u) for u in URL_RE.findall(raw)]
        if urls:
            for url in urls:
                title = raw.replace(url, '').strip(' -–—\t') or url
                sources.append({
                    'id': f's{len(sources)+1}',
                    'title': title[:180],
                    'url': url,
                    'type': 'url',
                    'signalType': signal_type,
                    'signalPriority': signal_priority,
                    'notes': '',
                    'tags': [],
                    'access': 'unknown',
                })
        else:
            sources.append({
                'id': f's{len(sources)+1}',
                'title': raw[:120],
                'url': '',
                'type': 'note',
                'signalType': signal_type,
                'signalPriority': signal_priority,
                'notes': raw,
                'tags': [],
                'access': 'pasted-note',
            })
    return {
        'issue': issue_from_config(config),
        'collectedAt': datetime.now(timezone.utc).isoformat(),
        'sources': sources,
    }


def main():
    parser = argparse.ArgumentParser(description='Normalize pasted URLs/notes into a Non-Annoying News source manifest.')
    parser.add_argument('input', nargs='?', help='Input text file. Reads stdin if omitted.')
    parser.add_argument('--config', help='Optional local config JSON for issue metadata.')
    parser.add_argument('--signal-type', default='manual_urls', help='Signal type to attach to collected items.')
    parser.add_argument('--priority', type=int, default=100, help='Signal priority to attach to collected items.')
    args = parser.parse_args()

    text = Path(args.input).read_text() if args.input else sys.stdin.read()
    config = load_config(args.config)
    print(json.dumps(collect(text, signal_type=args.signal_type, signal_priority=args.priority, config=config), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
