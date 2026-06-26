#!/usr/bin/env python3
"""
Magnet Search v3.0 - 智能多源磁力搜索
版本: 3.0.0 | 作者: HomeClaw

自动优先级调度，智能扩展数据源
"""

import argparse
import json
import sys
import re
import html
import gzip
import random
from urllib.parse import quote_plus
import urllib.request
import ssl
import xml.etree.ElementTree as ET


class MagnetSearcher:
    VERSION = "3.0.0"
    SOURCE_PRIORITY = ['yts', 'tpb', 'torrentgalaxy', 'nyaa', 'bt4g', 'eztv']
    
    def __init__(self):
        self.timeout = 15
        self.max_results = 20
        self.min_seeders = 3
        self.quality_filter = None
        self.min_size_gb = 0
        self.max_size_gb = 1000
        self.min_results_target = 10
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36']
        self.quality_priority = {'4K': 6, '2160p': 6, 'UHD': 6, '1080p': 5, '1080': 5,
                                '720p': 4, '720': 4, '480p': 3, '480': 3,
                                'BluRay': 5, 'WEB-DL': 5, 'WEBRip': 4, 'HDTV': 3, 'DVDRip': 3, 'HDRip': 3, 'Unknown': 1}
        self.source_status = {}
        
    def get_headers(self):
        return {'User-Agent': random.choice(self.user_agents),
                'Accept': 'application/json, text/html, application/rss+xml',
                'Accept-Encoding': 'gzip, deflate'}
        
    def fetch(self, url, timeout=None):
        try:
            req = urllib.request.Request(url, headers=self.get_headers())
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=timeout or self.timeout) as r:
                data = r.read()
                if r.headers.get('Content-Encoding') == 'gzip':
                    data = gzip.decompress(data)
                return data.decode('utf-8', errors='ignore')
        except:
            return None
    
    def fetch_json(self, url, timeout=None):
        try:
            return json.loads(self.fetch(url, timeout) or '{}')
        except:
            return None
    
    def _extract_q(self, name):
        n = name.lower()
        for q, v in [('2160p', '2160p'), ('4k', '4K'), ('1080p', '1080p'), ('720p', '720p'), ('480p', '480p')]:
            if q in n:
                return v
        for p, v in [('bluray', 'BluRay'), ('web-dl', 'WEB-DL'), ('webrip', 'WEBRip'), ('hdtv', 'HDTV'), ('dvdrip', 'DVDRip')]:
            if p in n:
                return v
        return 'Unknown'
    
    def _fmt_size(self, b):
        if b == 0:
            return 'Unknown'
        for u in ['B', 'KB', 'MB', 'GB', 'TB']:
            if b < 1024.0:
                return f"{b:.2f} {u}"
            b /= 1024.0
        return f"{b:.2f} PB"
    
    def _parse_size(self, s):
        s = str(s).lower().replace(',', '')
        try:
            if 'tb' in s:
                return float(s.replace('tb', '').strip()) * 1024**4
            elif 'gb' in s:
                return float(s.replace('gb', '').strip()) * 1024**3
            elif 'mb' in s:
                return float(s.replace('mb', '').strip()) * 1024**2
            elif 'kb' in s:
                return float(s.replace('kb', '').strip()) * 1024
        except:
            pass
        return 0
    
    def _magnet(self, h, n):
        from urllib.parse import quote_plus
        trackers = ['udp://tracker.openbittorrent.com:80', 'udp://opentracker.i2p.rocks:6969',
                   'udp://tracker.internetwarriors.net:1337', 'udp://tracker.opentrackr.org:1337']
        return f"magnet:?xt=urn:btih:{h}&dn={quote_plus(n)}&{'&'.join(f'tr={t}' for t in trackers)}"
    
    # ========== YTS ==========
    def search_yts(self, q):
        r = []
        try:
            d = self.fetch_json(f"https://yts.mx/api/v2/list_movies.json?query_term={quote_plus(q)}&limit=20", 10)
            if not d or d.get('status') != 'ok':
                return r
            for m in d.get('data', {}).get('movies', []):
                t = m.get('title_long', m.get('title', ''))
                for tr in m.get('torrents', []):
                    s = int(tr.get('seeds', 0))
                    if s < self.min_seeders:
                        continue
                    h = tr.get('hash', '').lower()
                    if len(h) != 40:
                        continue
                    r.append({"name": f"{t} [{tr.get('quality')}]")
                "quality": tr.get('quality', 'Unknown'), "size": tr.get('size', 'Unknown'),
                              "size_bytes": self._parse_size(tr.get('size', '0')), "seeders": s,
                              "leechers": int(tr.get('peers', 0)), "info_hash": h, "source": "YTS",
                              "uploaded": str(tr.get('date_uploaded', ''))[:10], "magnet": self._magnet(h, t)})
        except:
            pass
        return r
    
    # ========== EZTV ==========
    def search_eztv(self, q):
        r = []
        try:
            content = self.fetch(f"https://eztvx.to/search/{quote_plus(q.replace(' ', '-'))}", 10)
            if content:
                for match in re.findall(r'magnet:\?xt=urn:btih:([a-f0-9]{40})[^"]*"[^>]*>.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*>(\d+)</td>', content, re.S)[:15]:
                    h, n, sz, s = match
                    s = int(s)
                    if s >= self.min_seeders:
                        r.append({"name": html.unescape(n.strip()), "quality": self._extract_q(n), "size": sz.strip(),
                                  "size_bytes": self._parse_size(sz), "seeders": s, "leechers": 0, "info_hash": h.lower(),
                                  "source": "EZTV", "uploaded": 'Unknown', "magnet": self._magnet(h, n)})
        except:
            pass
        return r
    
    # ========== TPB ==========
    def search_tpb(self, q):
        r = []
        try:
            for url in [f"https://apibay.org/q.php?q={quote_plus(q)}&cat=200",
                        f"https://apibay.github.io/q.php?q={quote_plus(q)}&cat=200"]:
                d = self.fetch_json(url, 10)
                if d:
                    break
            if not d:
                return r
            for i in d:
                if i.get('id') == '0':
                    continue
                h = i.get('info_hash', '').lower()
                if len(h) != 40:
                    continue
                s = int(i.get('seeders', 0))
                if s < self.min_seeders:
                    continue
                r.append({"name": html.unescape(i.get('name', '')), "quality": self._extract_q(i.get('name', '')),
                          "size": self._fmt_size(int(i.get('size', 0))), "size_bytes": int(i.get('size', 0)),
                          "seeders": s, "leechers": int(i.get('leechers', 0)), "info_hash": h, "source": "TPB",
                          "uploaded": i.get('added', 'Unknown'), "magnet": self._magnet(h, i.get('name', ''))})
        except:
            pass
        return r
    
    # ========== TorrentGalaxy ==========
    def search_tgx(self, q):
        r = []
        try:
            content = self.fetch(f"https://torrentgalaxy.to/rss?search={quote_plus(q)}&lang=0&sort=seeders", 10)
            if not content:
                return r
            root = ET.fromstring(content)
            ns = {'tgx': 'https://torrentgalaxy.to/rss'}
            for item in root.findall('.//item'):
                t = item.find('title')
                if t is None:
                    continue
                s