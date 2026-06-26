#!/usr/bin/env python3
"""
Fetch real-time hot news using direct API calls (newsnow-style implementation)
Based on newsnow project's source fetching patterns
https://github.com/ourongxing/newsnow
"""
import json
import sys
import re
import urllib.parse
import random
import string
import time
from typing import List, Dict, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

def generate_random_weibo_cookie():
    """Generate a random-looking Weibo cookie to avoid hardcoding credentials"""
    # Generate random parts that resemble a Weibo cookie format
    # This is a placeholder that helps avoid anti-scraping detection
    # Real cookie validation is handled by Weibo's backend
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
    return f"SUB=_2AkM{random_part}"

def http_request(url, headers=None, follow_redirects=True, timeout=30):
    """Helper function to make HTTP requests using urllib"""
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')

        if headers:
            for key, value in headers.items():
                req.add_header(key, value)

        response = urlopen(req, timeout=timeout)
        content = response.read().decode('utf-8', errors='ignore')

        # Handle redirects manually if needed
        if follow_redirects and response.status in [301, 302, 303, 307, 308]:
            redirect_url = response.getheader('Location')
            if redirect_url:
                return http_request(redirect_url, headers, False, timeout)

        return content
    except (URLError, HTTPError) as e:
        print(f"HTTP request error: {e}", file=sys.stderr)
        return None

def fetch_weibo_hot(limit=20):
    """Fetch Weibo hot search directly from API (newsnow-style)"""
    try:
        url = "https://s.weibo.com/top/summary?cate=realtimehot"

        # Generate a random-looking cookie to avoid hardcoding credentials
        cookie = generate_random_weibo_cookie()

        headers = {
            'Cookie': cookie,
            'Referer': url
        }

        html = http_request(url, headers, timeout=30)

        if html is None:
            return None

        # Check if we got valid HTML
        if not html or len(html) < 100:
            print("Weibo request returned empty or invalid response", file=sys.stderr)
            return None

        # Parse HTML to extract hot items (similar to newsnow's cheerio parsing)
        items = []

        # Look for table rows with hot search items
        pattern = r'<td[^>]*class="td-02"[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'

        try:
            matches = re.findall(pattern, html, re.DOTALL)
        except Exception as e:
            print(f"Regex matching error: {e}", file=sys.stderr)
            return None

        for i, (href, title) in enumerate(matches[:limit]):
            # Clean up title
            title = title.strip()
            # Skip empty titles or javascript links
            if title and not 'javascript:void(0);' in href:
                # Extract flag info (新, 热, 爆) from the row
                # This is simplified - newsnow has more sophisticated parsing
                items.append({
                    "id": title,
                    "title": title,
                    "url": f"https://s.weibo.com{href}" if not href.startswith('http') else href,
                    "mobileUrl": f"https://s.weibo.com{href}" if not href.startswith('http') else href,
                    "extra": {
                        "info": "微博热搜"
                    }
                })

        return items[:limit]

    except Exception as e:
        print(f"Error fetching weibo: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None

def fetch_zhihu_hot(limit=20):
    """Fetch Zhihu hot list directly from API (newsnow-style)"""
    try:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-list-web?limit=20&desktop=true"

        content = http_request(url, timeout=30)

        if content is None:
            return None

        data = json.loads(content)

        if 'data' not in data:
            return None

        items = []
        for item in data['data'][:limit]:
            try:
                target = item.get('target', {})
                title_area = target.get('title_area', {})
                metrics_area = target.get('metrics_area', {})
                excerpt_area = target.get('excerpt_area', {})
                link = target.get('link', {})

                title = title_area.get('text', '')
                item_url = link.get('url', '')
                info = metrics_area.get('text', '')
                hover = excerpt_area.get('text', '')

                # Extract ID from URL
                id_match = re.search(r'(\d+)$', item_url)
                item_id = id_match.group(1) if id_match else item_url

                if title:
                    items.append({
                        "id": item_id,
                        "title": title,
                        "url": item_url,
                        "extra": {
                            "info": info,
                            "hover": hover
                        }
                    })
            except Exception as e:
                print(f"Error parsing zhihu item: {e}", file=sys.stderr)
                continue

        return items[:limit]

    except Exception as e:
        print(f"Error fetching zhihu: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None

def fetch_baidu_hot(limit=20):
    """Fetch Baidu hot search directly from API (newsnow-style)"""
    try:
        url = "https://top.baidu.com/board?tab=realtime"

        html = http_request(url, timeout=30)

        if html is None:
            return None

        # Extract JSON data from HTML comment (newsnow-style)
        pattern = r'<!--s-data:(.*?)-->'
        match = re.search(pattern, html, re.DOTALL)

        if not match:
            return None

        data = json.loads(match.group(1))

        if 'data' not in data or 'cards' not in data['data']:
            return None

        items = []
        content = data['data']['cards'][0]['content']

        for item in content[:limit]:
            try:
                # Skip top items
                if item.get('isTop'):
                    continue

                word = item.get('word', '')
                raw_url = item.get('rawUrl', '')
                desc = item.get('desc', '')

                if word and raw_url:
                    items.append({
                        "id": raw_url,
                        "title": word,
                        "url": raw_url,
                        "extra": {
                            "hover": desc
                        }
                    })
            except Exception as e:
                print(f"Error parsing baidu item: {e}", file=sys.stderr)
                continue

        return items[:limit]

    except Exception as e:
        print(f"Error fetching baidu: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None

def fetch_douyin_hot(limit=20):
    """Fetch Douyin hot search directly from API (newsnow-style)"""
    try:
        url = "https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1"

        # Get session cookie
        login_url = "https://login.douyin.com/"
        login_req = Request(login_url)
        login_req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')

        try:
            login_response = urlopen(login_req, timeout=30)
        except (URLError, HTTPError):
            return None

        # Extract Set-Cookie headers
        cookies = []
        for cookie in login_response.headers.get_all('Set-Cookie') or []:
            # Extract cookie name and value
            cookie_parts = cookie.split(';')[0]
            cookies.append(cookie_parts)

        cookie_str = '; '.join(cookies)

        # Fetch hot search data
        headers = {
            'Cookie': cookie_str
        }

        content = http_request(url, headers, timeout=30)

        if content is None:
            return None

        data = json.loads(content)

        if 'data' not in data or 'word_list' not in data['data']:
            return None

        items = []
        for item in data['data']['word_list'][:limit]:
            try:
                sentence_id = item.get('sentence_id', '')
                word = item.get('word', '')
                event_time = item.get('event_time', '')
                hot_value = item.get('hot_value', '')

                if word and sentence_id:
                    items.append({
                        "id": sentence_id,
                        "title": word,
                        "url": f"https://www.douyin.com/hot/{sentence_id}",
                        "extra": {
                            "info": f"热度: {hot_value}",
                            "hover": f"时间: {event_time}"
                        }
                    })
            except Exception as e:
                print(f"Error parsing douyin item: {e}", file=sys.stderr)
                continue

        return items[:limit]

    except Exception as e:
        print(f"Error fetching douyin: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None

def fetch_wallstreetcn_hot(limit=20):
    """Fetch Wallstreetcn hot news directly from API (newsnow-style)"""
    try:
        url = "https://api-one.wallstcn.com/apiv1/content/articles/hot?period=all"

        content = http_request(url, timeout=30)

        if content is None:
            return None

        data = json.loads(content)

        if 'data' not in data or 'day_items' not in data['data']:
            return None

        items = []
        for item in data['data']['day_items'][:limit]:
            try:
                item_id = item.get('id', '')
                title = item.get('title', '')
                uri = item.get('uri', '')

                if title and uri:
                    items.append({
                        "id": item_id,
                        "title": title,
                        "url": uri,
                        "extra": {
                            "info": "华尔街见闻热搜"
                        }
                    })
            except Exception as e:
                print(f"Error parsing wallstreetcn item: {e}", file=sys.stderr)
                continue

        return items[:limit]

    except Exception as e:
        print(f"Error fetching wallstreetcn: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None

def fetch_toutiao_hot(limit=20):
    """Fetch Toutiao hot news directly from API (newsnow-style)"""
    try:
        url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"

        content = http_request(url, timeout=30)

        if content is None:
            return None

        data = json.loads(content)

        if 'data' not in data:
            return None

        items = []
        for item in data['data'][:limit]:
            try:
                cluster_id = item.get('ClusterIdStr', '')
                title = item.get('Title', '')
                hot_value = item.get('HotValue', '')
                image = item.get('Image', {}).get('url', '')
                label_uri = item.get('LabelUri', {}).get('url', '')

                if title and cluster_id:
                    items.append({
                        "id": cluster_id,
                        "title": title,
                        "url": f"https://www.toutiao.com/trending/{cluster_id}/",
                        "extra": {
                            "info": f"热度: {hot_value}",
                            "hover": f"图标: {label_uri}" if label_uri else ""
                        }
                    })
            except Exception as e:
                print(f"Error parsing toutiao item: {e}", file=sys.stderr)
                continue

        return items[:limit]

    except Exception as e:
        print(f"Error fetching toutiao: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None

def fetch_jin10_news(limit=20):
    """Fetch Jin10 flash news directly from API (newsnow-style)"""
    try:
        timestamp = int(time.time() * 1000)
        url = f"https://www.jin10.com/flash_newest.js?t={timestamp}"

        raw_data = http_request(url, timeout=30)

        if raw_data is None:
            return None

        # Jin10 returns JavaScript variable: var newest = [...];
        # Remove variable declaration and trailing semicolon
        json_str = re.sub(r'^var\s+newest\s*=\s*', '', raw_data)
        json_str = re.sub(r';*$', '', json_str).strip()

        # Try to parse as JSON
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}", file=sys.stderr)
            print(f"First 500 chars of response: {json_str[:500]}", file=sys.stderr)
            return None

        items = []
        for item in data[:limit]:
            try:
                # Filter out channel 5 and ensure content exists
                data_obj = item.get('data', {})
                if not (data_obj.get('title') or data_obj.get('content')):
                    continue

                channels = item.get('channel', [])
                if isinstance(channels, list) and 5 in channels:
                    continue

                item_id = item.get('id', '')
                important = item.get('important', 0)

                title = data_obj.get('title', data_obj.get('content', ''))
                source = data_obj.get('source', '')

                # Parse title/desc format 【标题】描述
                match = re.match(r'^【([^】]*)】】', title)
                if match:
                    parsed_title = match.group(1)
                    desc = title.replace(match.group(0), "").strip()
                else:
                    parsed_title = title
                    desc = ""

                # Remove HTML tags from title
                parsed_title = re.sub(r'<[^>]+>', '', parsed_title)

                if parsed_title:
                    info_text = "✰ 重要" if important else ""
                    hover_text = f"{desc} - 来源: {source}" if (desc or source) else ""
                    items.append({
                        "id": item_id,
                        "title": parsed_title,
                        "url": f"https://flash.jin10.com/detail/{item_id}",
                        "extra": {
                            "info": info_text,
                            "hover": hover_text
                        }
                    })
            except Exception as e:
                print(f"Error parsing jin10 item: {e}", file=sys.stderr)
                continue

        return items[:limit]

    except Exception as e:
        print(f"Error fetching jin10: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None

def fetch_thepaper_hot(limit=20):
    """Fetch The Paper hot news directly from API (newsnow-style)"""
    try:
        url = "https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar"

        content = http_request(url, timeout=30)

        if content is None:
            return None

        data = json.loads(content)

        if 'data' not in data or 'hotNews' not in data['data']:
            return None

        items = []
        for item in data['data']['hotNews'][:limit]:
            try:
                cont_id = item.get('contId', '')
                name = item.get('name', '')
                pub_time = item.get('pubTimeLong', '')

                if name and cont_id:
                    items.append({
                        "id": cont_id,
                        "title": name,
                        "url": f"https://www.thepaper.cn/newsDetail_forward_{cont_id}",
                        "mobileUrl": f"https://m.thepaper.cn/newsDetail_forward_{cont_id}",
                        "extra": {
                            "info": "澎湃新闻热搜"
                        }
                    })
            except Exception as e:
                print(f"Error parsing thepaper item: {e}", file=sys.stderr)
                continue

        return items[:limit]

    except Exception as e:
        print(f"Error fetching thepaper: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None

def fetch_news(source="weibo", limit=20):
    """Fetch hot news from specified source using (newsnow-style) API calls"""
    fetchers = {
        "weibo": fetch_weibo_hot,
        "zhihu": fetch_zhihu_hot,
        "baidu": fetch_baidu_hot,
        "douyin": fetch_douyin_hot,
        "wallstreetcn": fetch_wallstreetcn_hot,
        "toutiao": fetch_toutiao_hot,
        "jin10": fetch_jin10_news,
        "thepaper": fetch_thepaper_hot,
    }

    fetcher = fetchers.get(source, fetch_weibo_hot)
    return fetcher(limit)

if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else "weibo"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    news = fetch_news(source, limit)
    if news:
        print(json.dumps(news, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": f"Failed to fetch news from {source}"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
