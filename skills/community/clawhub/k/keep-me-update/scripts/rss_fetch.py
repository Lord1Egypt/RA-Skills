#!/usr/bin/env python3
"""
RSS Feed Fetcher — stdlib only, no pip deps.
Usage:
  python3 rss_fetch.py                          # fetch all feeds, output JSON
  python3 rss_fetch.py --import-opml <file>     # import OPML into feed DB
  python3 rss_fetch.py --check                  # check feed availability
  python3 rss_fetch.py --list                   # list all feeds
"""

import json
import os
import re
import sys
import time
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ── Config ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FEED_DB = os.path.join(SCRIPT_DIR, 'rss_feeds.json')
CACHE_DIR = os.path.join(SCRIPT_DIR, 'rss_cache')
SEEN_GUIDS_PATH = os.path.join(SCRIPT_DIR, 'seen_guids.json')
os.makedirs(CACHE_DIR, exist_ok=True)

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0',
    'Accept': 'application/rss+xml, application/xml, text/xml, */*',
}
FETCH_TIMEOUT = 20
MAX_ARTICLES_PER_FEED = 10


# ── HTML Stripper ─────────────────────────────────────────────────────────
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def handle_entityref(self, name):
        self.text.append(f'&{name};')

    def handle_charref(self, name):
        self.text.append(f'&#{name};')

    def get_data(self):
        return ''.join(self.text)


def strip_html(html):
    if not html:
        return ''
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def clean_text(text):
    """Clean whitespace, strip HTML, truncate."""
    if not text:
        return ''
    text = strip_html(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:800]


# ── Feed Database ─────────────────────────────────────────────────────────
def load_feeds():
    if not os.path.exists(FEED_DB):
        return []
    with open(FEED_DB, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def save_feeds(feeds):
    with open(FEED_DB, 'w', encoding='utf-8') as f:
        json.dump(feeds, f, ensure_ascii=False, indent=2)
    print(f'💾 Saved {len(feeds)} feeds to {FEED_DB}', file=sys.stderr)


def import_opml(opml_path):
    """Import OPML file into feed database."""
    feeds = load_feeds()
    existing_urls = {f['url'] for f in feeds}

    tree = ET.parse(opml_path)
    root = tree.getroot()
    body = root.find('body')

    imported = 0
    skipped = 0

    def walk_outline(element, category=None):
        nonlocal imported, skipped
        for child in element.findall('outline'):
            # Support nested categories
            if child.get('type') != 'rss' and not child.get('xmlUrl'):
                # This is a category folder, recurse
                cat = child.get('text') or child.get('title') or category
                walk_outline(child, cat)
                continue

            url = child.get('xmlUrl') or child.get('url')
            if not url:
                continue

            if url in existing_urls:
                skipped += 1
                continue

            entry = {
                'id': str(uuid.uuid4())[:8],
                'title': child.get('title') or child.get('text') or url,
                'url': url,
                'category': category or child.get('text') or 'Uncategorized',
                'added': datetime.now(timezone.utc).isoformat(),
                'last_ok': None,
                'last_error': None,
                'enabled': True,
            }
            feeds.append(entry)
            existing_urls.add(url)
            imported += 1

    walk_outline(body)
    save_feeds(feeds)
    print(f'✅ Imported {imported} feeds, skipped {skipped} duplicates.',
          file=sys.stderr)
    return imported


# ── Feed Fetching ─────────────────────────────────────────────────────────
def fetch_url(url):
    """Fetch a URL and return (content_bytes, charset)."""
    req = Request(url, headers=REQUEST_HEADERS)
    resp = urlopen(req, timeout=FETCH_TIMEOUT)
    content_type = resp.headers.get('Content-Type', '')
    # Detect charset
    charset = 'utf-8'
    m = re.search(r'charset=([\w-]+)', content_type, re.I)
    if m:
        charset = m.group(1)
    raw = resp.read()
    # Try declared charset, fallback to utf-8
    for enc in [charset, 'utf-8', 'latin-1']:
        try:
            return raw.decode(enc, errors='surrogateescape')
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode('utf-8', errors='surrogateescape')


def parse_date(date_str):
    """Parse various date formats to ISO string."""
    if not date_str:
        return None
    date_str = date_str.strip()
    # RFC 2822 (most common in RSS)
    patterns = [
        '%a, %d %b %Y %H:%M:%S %z',      # RFC 2822
        '%a, %d %b %Y %H:%M:%S %Z',       # RFC 2822 with named tz
        '%Y-%m-%dT%H:%M:%S%z',            # ISO 8601
        '%Y-%m-%dT%H:%M:%S',              # ISO 8601 no tz
        '%Y-%m-%d %H:%M:%S',              # SQL style
        '%Y-%m-%d',                       # Date only
        '%d %b %Y %H:%M:%S %z',
        '%d %b %Y %H:%M:%S',
    ]
    for fmt in patterns:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.replace(tzinfo=None).isoformat() + 'Z'
        except ValueError:
            continue
    return None


def preclean_xml(text):
    """Fix common XML issues before parsing: unescaped &, invalid chars, etc."""
    # 1. Strip surrogates produced by surrogateescape decode
    text = re.sub(r'[\ud800-\udfff\ufffe\uffff]', '', text)
    # 2. Strip ASCII control chars (except TAB, LF, CR which are valid)
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)
    # 3. Fix unescaped ampersands: & that is not part of &amp; &lt; &gt; &quot; &apos; &#...
    # Only fix & that appear inside tag attributes (between quotes)
    def fix_amp_in_attr(m):
        prefix = m.group(1)
        attr_content = m.group(2)
        # Escape any bare &
        fixed = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)', '&amp;', attr_content)
        return prefix + '"' + fixed + '"'
    # Match attributes with double-quoted values
    text = re.sub(r'(<\w[^>]*?\s+[\w:-]+=)"([^"]*?)"', fix_amp_in_attr, text)
    # Also fix bare & in text content (between tags)
    text = re.sub(r'>([^<]*?)&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)([^<]*?)<', 
                  lambda m: '>' + m.group(1) + '&amp;' + m.group(2) + '<', text)
    return text


def parse_rss(xml_text, feed_url):
    """Parse RSS 2.0, RSS 1.0 (RDF), or Atom XML, return list of articles."""
    articles = []

    xml_text = preclean_xml(xml_text)

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        return articles, f'XML parse error: {e}'

    ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}

    # RSS 2.0
    channel = root.find('channel')
    if channel is not None:
        for item in channel.findall('item'):
            title = clean_text(item.findtext('title', ''))
            link = (item.findtext('link', '') or '').strip()
            desc = clean_text(item.findtext('description', ''))
            # content:encoded for full content
            content_enc = item.find('content:encoded', ns)
            if content_enc is not None and content_enc.text:
                desc = clean_text(content_enc.text)
            pub_date = parse_date(item.findtext('pubDate', ''))
            creator_el = item.find('{http://purl.org/dc/elements/1.1/}creator')
            author = creator_el.text if creator_el is not None else ''
            guid = item.findtext('guid', link)
            categories = []
            for cat in item.findall('category'):
                if cat.text:
                    categories.append(cat.text)

            if title or link:
                articles.append({
                    'title': title or '(无标题)',
                    'url': link or feed_url,
                    'summary': desc[:500] if desc else '',
                    'date': pub_date or datetime.now(timezone.utc).isoformat(),
                    'author': author,
                    'guid': guid or link,
                    'categories': categories,
                })
        return articles, None

    # Atom
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')
    if entries:
        for entry in entries:
            title = clean_text(
                entry.findtext('{http://www.w3.org/2005/Atom}title', ''))
            link_el = entry.find('{http://www.w3.org/2005/Atom}link')
            link = ''
            if link_el is not None:
                link = link_el.get('href', '') or ''
            summary_el = entry.find('{http://www.w3.org/2005/Atom}summary')
            content_el = entry.find('{http://www.w3.org/2005/Atom}content')
            desc = ''
            if content_el is not None:
                desc = clean_text(content_el.text or '')
            elif summary_el is not None:
                desc = clean_text(summary_el.text or '')
            published = parse_date(
                entry.findtext('{http://www.w3.org/2005/Atom}published', ''))
            updated = parse_date(
                entry.findtext('{http://www.w3.org/2005/Atom}updated', ''))
            author_el = entry.find('{http://www.w3.org/2005/Atom}author')
            author = author_el.findtext(
                '{http://www.w3.org/2005/Atom}name', ''
            ) if author_el is not None else ''
            entry_id = entry.findtext(
                '{http://www.w3.org/2005/Atom}id', link)

            if title or link:
                articles.append({
                    'title': title or '(无标题)',
                    'url': link or '',
                    'summary': desc[:500] if desc else '',
                    'date': (published or updated
                             or datetime.now(timezone.utc).isoformat()),
                    'author': author,
                    'guid': entry_id or link,
                    'categories': [],
                })
        return articles, None

    # RSS 1.0 / RDF
    rdf_ns = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    rss1_ns = 'http://purl.org/rss/1.0/'
    dc_ns = 'http://purl.org/dc/elements/1.1/'
    rdf_tag = f'{{{rdf_ns}}}RDF'
    if root.tag == rdf_tag:
        for item in root.findall(f'{{{rss1_ns}}}item'):
            title = clean_text(item.findtext(f'{{{rss1_ns}}}title', ''))
            link = (item.findtext(f'{{{rss1_ns}}}link', '') or '').strip()
            desc = clean_text(
                item.findtext(f'{{{rss1_ns}}}description', ''))
            pub_date = parse_date(item.findtext(f'{{{dc_ns}}}date', ''))
            author = item.findtext(f'{{{dc_ns}}}creator', '')
            # Try content:encoded
            content_enc = item.find('content:encoded', ns)
            if content_enc is not None and content_enc.text:
                desc = clean_text(content_enc.text)
            categories = []
            for cat in item.findall(f'{{{dc_ns}}}subject'):
                if cat.text:
                    categories.append(cat.text)

            if title or link:
                articles.append({
                    'title': title or '(无标题)',
                    'url': link or feed_url,
                    'summary': desc[:500] if desc else '',
                    'date': pub_date or datetime.now(timezone.utc).isoformat(),
                    'author': author,
                    'guid': link or '',
                    'categories': categories,
                })
        if articles:
            return articles, None

    return articles, 'Unknown feed format (not RSS 2.0, RSS 1.0, or Atom)'


def fetch_feed(feed):
    """Fetch a single feed and return (articles, error)."""
    url = feed['url']
    try:
        xml_text = fetch_url(url)
        articles, error = parse_rss(xml_text, url)
        if error:
            return [], error
        # Sort by date descending, limit
        articles.sort(key=lambda a: a.get('date', ''), reverse=True)
        articles = articles[:MAX_ARTICLES_PER_FEED]
        return articles, None
    except HTTPError as e:
        return [], f'HTTP {e.code}: {e.reason}'
    except URLError as e:
        return [], f'Network error: {e.reason}'
    except Exception as e:
        return [], f'Error: {type(e).__name__}: {e}'


# ── Check Feeds ───────────────────────────────────────────────────────────
def check_feeds():
    """Check all feeds for availability."""
    feeds = load_feeds()
    results = []
    for feed in feeds:
        if not feed['enabled']:
            continue
        url = feed['url']
        try:
            req = Request(url, headers=REQUEST_HEADERS)
            resp = urlopen(req, timeout=15)
            feed['last_ok'] = datetime.now(timezone.utc).isoformat()
            feed['last_error'] = None
            results.append({
                'id': feed['id'],
                'title': feed['title'],
                'url': url,
                'status': 'ok',
                'http': resp.status,
            })
        except HTTPError as e:
            feed['last_error'] = f'HTTP {e.code}'
            results.append({
                'id': feed['id'],
                'title': feed['title'],
                'url': url,
                'status': 'error',
                'error': f'HTTP {e.code}',
            })
        except Exception as e:
            feed['last_error'] = str(e)[:100]
            results.append({
                'id': feed['id'],
                'title': feed['title'],
                'url': url,
                'status': 'error',
                'error': str(e)[:100],
            })
    save_feeds(feeds)
    return results


# ── Seen GUIDs (read/unread tracking) ────────────────────────────────────
SEEN_GUIDS = None  # lazy load


def load_seen_guids():
    global SEEN_GUIDS
    if SEEN_GUIDS is not None:
        return SEEN_GUIDS
    if not os.path.exists(SEEN_GUIDS_PATH):
        SEEN_GUIDS = set()
        return SEEN_GUIDS
    with open(SEEN_GUIDS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    SEEN_GUIDS = set(data.get('guids', []))
    return SEEN_GUIDS


def save_seen_guids():
    guids = load_seen_guids()
    with open(SEEN_GUIDS_PATH, 'w', encoding='utf-8') as f:
        json.dump({'guids': sorted(list(guids))}, f, ensure_ascii=False)


def mark_read(article_guids):
    """Add article GUIDs to the seen set and save."""
    guids = load_seen_guids()
    before = len(guids)
    guids.update(article_guids)
    save_seen_guids()
    return len(guids) - before


# ── Main Fetch (output for agent consumption) ─────────────────────────────
def fetch_all(skip_read=False):
    """Fetch all enabled feeds, save full data to cache, output summary to stdout."""
    feeds = load_feeds()
    enabled = [f for f in feeds if f.get('enabled', True)]

    seen_guids = load_seen_guids() if skip_read else set()

    all_articles = []
    feed_stats = []

    for i, feed in enumerate(enabled):
        title = feed['title']
        print(f'  [{i + 1}/{len(enabled)}] {title}...', file=sys.stderr)
        articles, error = fetch_feed(feed)
        if error:
            print(f'    ✗ {error}', file=sys.stderr)
            feed['last_error'] = error
            feed_stats.append({'title': title, 'status': 'error', 'error': error})
        else:
            print(f'    ✓ {len(articles)} articles', file=sys.stderr)
            feed['last_ok'] = datetime.now(timezone.utc).isoformat()
            feed['last_error'] = None
            feed_stats.append({'title': title, 'status': 'ok', 'count': len(articles)})
            for a in articles:
                a['feed_title'] = title
                a['feed_category'] = feed.get('category', 'Uncategorized')
                all_articles.append(a)

        # Polite delay between requests
        if i < len(enabled) - 1:
            time.sleep(1.5)

    save_feeds(feeds)

    # Deduplicate by guid
    seen = set()
    unique_articles = []
    skipped_read = 0
    for a in all_articles:
        g = a.get('guid', '') or a.get('url', '')
        if g in seen:
            continue
        seen.add(g)
        if skip_read and g in seen_guids:
            skipped_read += 1
            continue
        unique_articles.append(a)

    unique_articles.sort(key=lambda a: a.get('date', ''), reverse=True)

    now = datetime.now(timezone.utc)
    today_str = now.strftime('%Y-%m-%d')

    # Save full data to cache file
    cache_file = os.path.join(CACHE_DIR, f'articles_{today_str}.json')
    full_output = {
        'fetched_at': now.isoformat(),
        'total_feeds': len(enabled),
        'feeds_ok': sum(1 for s in feed_stats if s['status'] == 'ok'),
        'feeds_error': sum(1 for s in feed_stats if s['status'] == 'error'),
        'feed_stats': feed_stats,
        'total_articles': len(unique_articles),
        'skipped_read': skipped_read,
        'articles': unique_articles,
    }
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(full_output, f, ensure_ascii=False, indent=2)

    # Output summary to stdout (agent context)
    summary = {
        'fetched_at': now.isoformat(),
        'total_feeds': len(enabled),
        'feeds_ok': sum(1 for s in feed_stats if s['status'] == 'ok'),
        'feeds_error': sum(1 for s in feed_stats if s['status'] == 'error'),
        'feed_stats': feed_stats,
        'total_articles': len(unique_articles),
        'skipped_read': skipped_read,
        'cache_file': cache_file,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=None), file=sys.stdout)


# ── CLI ───────────────────────────────────────────────────────────────────
def cmd_list():
    feeds = load_feeds()
    if not feeds:
        print('No feeds in database.')

    # Group by category
    from collections import defaultdict
    groups = defaultdict(list)
    for f in feeds:
        groups[f.get('category', 'Uncategorized')].append(f)

    for cat, items in groups.items():
        print(f'\n## {cat} ({len(items)})')
        for f in items:
            status = '✓' if f.get('last_ok') else ('✗' if f.get('last_error') else '·')
            enabled = 'ON' if f.get('enabled', True) else 'OFF'
            print(f'  [{enabled}] {status} {f["title"]}')
            print(f'         {f["url"]}')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--import-opml' and len(sys.argv) > 2:
            import_opml(sys.argv[2])
        elif sys.argv[1] == '--check':
            results = check_feeds()
            ok = [r for r in results if r['status'] == 'ok']
            err = [r for r in results if r['status'] == 'error']
            print(f'Checked {len(results)} feeds: {len(ok)} ok, {len(err)} errors')
            for r in err:
                print(f'  ✗ {r["title"]}: {r["error"]}')
        elif sys.argv[1] == '--list':
            cmd_list()
        elif sys.argv[1] == '--skip-read':
            fetch_all(skip_read=True)
        elif sys.argv[1] == '--mark-read':
            # Find latest cache file, mark all articles as read
            cache_files = sorted(
                [f for f in os.listdir(CACHE_DIR) if f.startswith('articles_')],
                reverse=True)
            if not cache_files:
                print('No cache files found.', file=sys.stderr)
                sys.exit(1)
            latest = os.path.join(CACHE_DIR, cache_files[0])
            with open(latest, 'r', encoding='utf-8') as f:
                data = json.load(f)
            guids = []
            for a in data.get('articles', []):
                g = a.get('guid', '') or a.get('url', '')
                if g:
                    guids.append(g)
            added = mark_read(guids)
            print(f'Marked {len(guids)} articles as read ({added} new).')
        elif sys.argv[1] == '--help':
            print(__doc__)
        else:
            print(f'Unknown option: {sys.argv[1]}', file=sys.stderr)
            sys.exit(1)
    else:
        fetch_all(skip_read=False)
