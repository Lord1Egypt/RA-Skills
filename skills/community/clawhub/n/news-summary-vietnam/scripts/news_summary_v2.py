#!/usr/bin/env python3
# news_summary_v2.py — Tổng hợp tin tức v2, mỗi tin có link bài viết
# Đọc config từ config.json (cùng thư mục)

import json, os, sys, time, re
import subprocess
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

TMP_DIR = f'/tmp/news_summary_{os.getpid()}'
BOT_TOKEN = ''
CHAT_ID = ''
SOURCES = {}

# Tìm config.json ở nhiều vị trí
CONFIG_PATHS = [
    os.path.join(PARENT_DIR, 'config.json'),
    os.path.join(SCRIPT_DIR, 'config.json'),
    os.path.join(PARENT_DIR, '..', 'config.json'),
    '/home/pc999/.openclaw/workspace/config.json',
    os.path.expanduser('~/.openclaw/workspace/config.json'),
]

CONFIG_FILE = None
for p in CONFIG_PATHS:
    if os.path.exists(p):
        CONFIG_FILE = p
        break

if CONFIG_FILE:
    try:
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        BOT_TOKEN = cfg.get('botToken', '')
        CHAT_ID = cfg.get('chatId', '')
        SOURCES = cfg.get('sources', {})
    except Exception as e:
        print(f"⚠️ Config read error: {e}")

if not BOT_TOKEN or not CHAT_ID:
    print("❌ Lỗi: Cần tạo config.json với botToken và chatId. Xem SKILL.md")
    print("   Đặt config.json cùng thư mục với news_summary_v2.py")
    sys.exit(1)

# ── Helpers ────────────────────────────────────────────────────────────────────
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def fetch_url(url, timeout=15):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return ''

def escape_html(text):
    return text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def send_telegram(text):
    import urllib.parse
    data = urllib.parse.urlencode({
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': 'true',
    }).encode()
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
        data=data,
        headers={'User-Agent': UA}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = json.loads(r.read().decode())
            if not resp.get('ok'):
                print(f"Telegram error: {resp.get('description','')}")
            return resp.get('ok', False)
    except Exception as e:
        print(f"Telegram error: {e}")
    return False

# ── Fetch RSS with links ──────────────────────────────────────────────────────
def fetch_rss(url, limit=5):
    results = []
    xml = fetch_url(url)
    if not xml:
        return results

    try:
        # Parse RSS
        root = ET.fromstring(xml)
        channel = root if root.tag == 'rss' else root.find('.//channel')
        if channel is None:
            return results

        ns = {'rss': 'http://www.w3.org/2005/RSS'}
        items = channel.findall('.//item') if not ns['rss'] else root.findall('.//item')

        # Try without namespace first
        if not items:
            items = [c for c in channel if c.tag == 'item']

        for item in items[:limit]:
            title = ''
            link = ''

            for child in item:
                if child.tag in ('title', '{http://purl.org/dc/elements/1.1/}title'):
                    t = child.text or ''
                    # Handle CDATA
                    if '<![CDATA[' in ET.tostring(child, encoding='unicode'):
                        t = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', ET.tostring(child, encoding='unicode'))
                        t = re.sub(r'<[^>]+>', '', t)
                    title = t.strip()
                elif child.tag in ('link', '{http://purl.org/dc/elements/1.1/}link'):
                    link = (child.text or '').strip()
                elif child.tag == 'enclosure':
                    link = child.attrib.get('url', '')
                elif child.tag == 'guid':
                    g = child.text or ''
                    if g.startswith('http'):
                        link = g.strip()

            # Handle CDATA in text
            if title and not link:
                # Try description for link
                for child in item:
                    if child.tag in ('description', 'link'):
                        pass

            if title:
                results.append({'text': title, 'url': link or url})

            if len(results) >= limit:
                break

    except ET.ParseError:
        # Fallback: regex
        items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
        for item in items[:limit]:
            tm = re.search(r'<title>(?:<!\[CDATA\[(.*?)\]\]>|(.*?))</title>', item, re.DOTALL)
            title = ''
            if tm:
                title = (tm.group(1) or tm.group(2) or '').strip()

            lm = re.search(r'<link>(?:<!\[CDATA\[(.*?)\]\]>|(.*?))</link>', item, re.DOTALL)
            link = ''
            if lm:
                link = (lm.group(1) or lm.group(2) or '').strip()
            if not link:
                enc = re.search(r'<enclosure[^>]+url=["\']([^"\']+)["\']', item)
                if enc: link = enc.group(1)

            if title:
                results.append({'text': title, 'url': link or url})
            if len(results) >= limit:
                break

    return results

# ── Fetch Báo Mới via Playwright ────────────────────────────────────────────
def fetch_baomoi(limit=5):
    results = []
    node_bin = os.environ.get('NODE_BIN') or 'node'

    # Tìm node_modules
    node_paths = [
        '/home/pc999/.openclaw/workspace/node_modules',
        os.path.join(PARENT_DIR, 'node_modules'),
        os.path.join(SCRIPT_DIR, 'node_modules'),
        os.environ.get('NODE_PATH', ''),
    ]

    for node_path in node_paths:
        if node_path and os.path.exists(os.path.join(node_path, 'playwright')):
            break
    else:
        node_path = ''

    scraper = os.path.join(SCRIPT_DIR, 'scrape_baomoi_v2.js')
    if not os.path.exists(scraper):
        scraper = '/home/pc999/.openclaw/workspace/scrape_baomoi_v2.js'

    if not os.path.exists(scraper):
        return results

    env = os.environ.copy()
    if node_path:
        env['NODE_PATH'] = node_path

    try:
        proc = subprocess.run(
            [node_bin, scraper],
            capture_output=True, text=True, timeout=30,
            env=env
        )
        for line in proc.stdout.strip().split('\n'):
            line = line.strip()
            if line.startswith('{') and '"text"' in line and '"url"' in line:
                try:
                    item = json.loads(line)
                    results.append(item)
                except:
                    pass
            if len(results) >= limit:
                break
    except Exception as e:
        print(f"Báo Mới error: {e}")

    return results

# ── Build message ─────────────────────────────────────────────────────────────
def build_section(label, items):
    out = f"📰 <b>{label}</b>\n"
    if not items:
        out += "  ⚠️ Không lấy được tin\n"
    else:
        for item in items:
            text = escape_html(item.get('text', ''))
            url = item.get('url', '')
            if text:
                out += f'• <a href="{url}">{text}</a>\n'
    return out

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(TMP_DIR, exist_ok=True)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching news...")

    # Fetch all sources (sequential for simplicity)
    baomoi_results = fetch_baomoi(5)
    vne_results = fetch_rss('https://vnexpress.net/rss/tin-moi-nhat.rss', 5)
    tt_results = fetch_rss('https://tuoitre.vn/rss/homepage.rss', 5)
    dt_results = fetch_rss('https://dantri.com.vn/rss/home.rss', 5)

    now = datetime.now()
    date_str = now.strftime('%H:%M %d/%m/%Y')

    sections = []
    sections.append(build_section('Báo Mới', baomoi_results))
    sections.append(build_section('VnExpress', vne_results))
    sections.append(build_section('Tuổi Trẻ', tt_results))
    sections.append(build_section('Dân Trí', dt_results))

    message = f"""📊 <b>TỔNG HỢP TIN TỨC v2</b> — {date_str}

{sections[0]}
{sections[1]}
{sections[2]}
{sections[3]}
━━━━━━━━━━━━━━━━━━━━━━
✅ Cập nhật lúc {date_str}
🔗 Nhấn vào tin để đọc bài gốc"""

    ok = send_telegram(message)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent to Telegram: {ok}")

    # Cleanup
    import shutil
    shutil.rmtree(TMP_DIR, ignore_errors=True)

if __name__ == '__main__':
    main()
