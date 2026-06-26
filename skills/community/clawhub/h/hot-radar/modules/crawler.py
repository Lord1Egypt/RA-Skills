#!/usr/bin/env python3
# modules/crawler.py - 多平台热搜爬虫
"""
支持平台：
- zhihu      : 知乎热榜 API
- weibo      : 微博实时热搜
- douyin     : 抖音热点
- youtube    : YouTube 热门视频（需 API Key，config里配置）
- x_twitter : X/Twitter 趋势（RSS / 第三方代理）
- instagram : Instagram 趋势（需 Cookie，见说明）
- rebang    : 今日热榜/热榜聚合
"""
import requests, time, json, sys, os, re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOKEN_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts', '.feishu_token.json')

# 翻墙代理（Clash HTTP 代理）
PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or \
        os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy') or None

PROXIES = {'http': PROXY, 'https': PROXY} if PROXY else None

def _get(url, headers=None, timeout=15, json_resp=True, use_proxy=False):
    headers = headers or {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
    }
    proxies = PROXIES if use_proxy else None
    r = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
    r.raise_for_status()
    if json_resp:
        return r.json()
    return r.text


# ============================================================
# 已有平台
# ============================================================

def crawl_zhihu(limit=10):
    """知乎热榜"""
    try:
        data = _get(
            'https://api.zhihu.com/topstory/hot-lists/total?limit=50&desktop=true',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.zhihu.com/',
                'x-app-za': 'OS=Web',
            }
        )
        items = []
        for item in (data.get('data') or [])[:limit]:
            target = item.get('target') or {}
            items.append({
                'platform': '知乎热榜',
                'title': target.get('title', ''),
                'link': f'https://www.zhihu.com/question/{target.get("id", "")}',
                'hot': item.get('detail_text') or target.get('follower_count', 0),
                'excerpt': target.get('excerpt', ''),
            })
        return items
    except Exception as e:
        print(f'  ⚠️ 知乎失败: {e}')
        return []


def crawl_weibo(limit=10):
    """微博实时热搜"""
    try:
        data = _get(
            'https://weibo.com/ajax/side/hotSearch',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Referer': 'https://weibo.com/',
            }
        )
        items = []
        for item in (data.get('data', {}).get('realtime') or [])[:limit]:
            word = item.get('word', '') or item.get('topic_name', '')
            items.append({
                'platform': '微博热搜',
                'title': word,
                'link': item.get('url') or f'https://s.weibo.com/weibo?q={word}',
                'hot': item.get('raw_hot') or item.get('num', 0),
                'label': item.get('label_name', ''),
            })
        return items
    except Exception as e:
        print(f'  ⚠️ 微博失败: {e}')
        return []


def crawl_douyin(limit=10):
    """抖音热点"""
    try:
        data = _get(
            'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1',
            headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)',
                'Referer': 'https://www.douyin.com/',
            }
        )
        items = []
        for item in (data.get('data', {}).get('word_list') or [])[:limit]:
            word = item.get('word') or item.get('word_info', {}).get('word', '')
            items.append({
                'platform': '抖音热点',
                'title': word,
                'link': f'https://www.douyin.com/search/{word}',
                'hot': item.get('hot_value') or item.get('total_hot_value', 0),
                'hot_level': item.get('hot_level', ''),
            })
        return items
    except Exception as e:
        print(f'  ⚠️ 抖音失败: {e}')
        return []


# ============================================================
# 新增平台
# ============================================================

def crawl_youtube(limit=10):
    """YouTube 热门视频
    方式1: YouTube Data API v3 (需要 API Key，写入 config/platforms.json)
    方式2: Google Feeds (无需 Key，但数据有限)
    """
    import os as _os
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'platforms.json')
    api_key = None
    if os.path.exists(config_path):
        cfg = json.load(open(config_path, encoding='utf-8'))
        api_key = cfg.get('platforms', {}).get('youtube', {}).get('api_key')

    if api_key:
        try:
            # YouTube Data API v3 - Most Popular Videos
            data = _get(
                'https://www.googleapis.com/youtube/v3/videos',
                params={
                    'part': 'snippet,statistics',
                    'chart': 'mostPopular',
                    'regionCode': 'CN',
                    'maxResults': limit,
                    'key': api_key,
                },
                use_proxy=True,
            )
            items = []
            for item in (data.get('items') or [])[:limit]:
                snip = item.get('snippet', {})
                stats = item.get('statistics', {})
                items.append({
                    'platform': 'YouTube热门',
                    'title': snip.get('title', ''),
                    'link': f'https://youtu.be/{item.get("id", "")}',
                    'hot': int(stats.get('viewCount', 0)),
                    'channel': snip.get('channelTitle', ''),
                })
            return items
        except Exception as e:
            print(f'  ⚠️ YouTube API 失败: {e}')

    # Fallback: Google News YouTube 趋势
    try:
        data = _get(
            'https://news.google.com/rss/search?q=youtube+trending&hl=zh-CN&gl=CN&ceid=CN:zh-Hans',
            json_resp=False,
            use_proxy=True,
        )
        titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', data)
        items = []
        links = re.findall(r'<link/>(https?://.*?)<', data)
        for i, (title, link) in enumerate(zip(titles[1:limit+1], links[:limit])):
            items.append({
                'platform': 'YouTube热门',
                'title': title.strip(),
                'link': link.strip() if link else f'https://news.google.com/search?q=youtube+trending',
                'hot': 0,
            })
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ YouTube Google Feeds 失败: {e}')

    return []


def crawl_x_twitter(limit=10):
    """X / Twitter 趋势
    方式: Nitter 实例 RSS 或 syndication API
    注意: Twitter/X 官方 API 需要 OAuth，第三方实例可能不稳定
    """
    # 尝试多个 Nitter 实例
    nitter_instances = [
        'https://nitter.net',
        'https://nitter.privacydev.net',
        'https://nitter.poast.org',
    ]

    for base in nitter_instances:
        try:
            # 获取 Twitter Trending 的 RSS（通过 Nitter）
            url = f'{base}/i/trends'
            html = _get(url, json_resp=False, timeout=10, use_proxy=True)
            # 解析趋势标题
            titles = re.findall(r'class="trend-item[^"]*">(?:<[^>]*>)*\s*([\u4e00-\u9fa5a-zA-Z0-9].*?)(?:\s*<|"|\')', html)
            if not titles:
                titles = re.findall(r'<a[^>]+href="/([^"]+)"[^>]*class="[^"]*trend[^"]*"[^>]*>([^<]+)<', html)
            if titles:
                items = []
                for i, t in enumerate(titles[:limit]):
                    if isinstance(t, tuple):
                        title = t[1].strip()
                        link = f"https://twitter.com/{t[0]}"
                    else:
                        title = t.strip()
                        link = f'https://twitter.com/search?q={title}'
                    items.append({
                        'platform': 'X/Twitter趋势',
                        'title': title,
                        'link': link,
                        'hot': 0,
                    })
                return items
        except Exception:
            continue

    # Fallback: 使用 Google News 搜索 Twitter Trending
    try:
        data = _get(
            'https://news.google.com/rss/search?q=twitter+trending&hl=zh-CN&gl=CN&ceid=CN:zh-Hans',
            json_resp=False,
            use_proxy=True,
        )
        titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', data)
        items = []
        for title in titles[1:limit+1]:
            items.append({
                'platform': 'X/Twitter趋势',
                'title': title.strip(),
                'link': f'https://twitter.com/search?q={title.strip()}',
                'hot': 0,
            })
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ Twitter RSS 失败: {e}')

    return []


def crawl_instagram(limit=10):
    """Instagram 趋势
    注意: Instagram 官方 API 需要 Facebook 账号授权，公开接口极少
    此处使用替代方案: Google News Instagram 趋势
    如需完整数据，需提供 Instagram Session Cookie (config/instagram.json)
    """
    cookie_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'instagram.json')

    # 如果有配置 cookie，使用非官方接口（需要用户自行承担风险）
    if os.path.exists(cookie_file):
        cfg = json.load(open(cookie_file, encoding='utf-8'))
        cookie = cfg.get('session_cookie')
        if cookie:
            try:
                data = _get(
                    'https://i.instagram.com/api/v1/clips/reels/home_timeline_clips/',
                    headers={
                        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
                        'Cookie': cookie,
                        'X-IG-App-ID': '936619743392459',
                    },
                    use_proxy=True,
                )
                items = []
                for item in (data.get('items', []) or [])[:limit]:
                    items.append({
                        'platform': 'Instagram热点',
                        'title': item.get('title', '') or item.get('code', ''),
                        'link': f'https://www.instagram.com/p/{item.get("code", "")}/',
                        'hot': item.get('like_count', 0),
                    })
                return items
            except Exception as e:
                print(f'  ⚠️ Instagram API 失败: {e}')
                return []
        return []

    # Fallback: Google News
    try:
        data = _get(
            'https://news.google.com/rss/search?q=instagram+trending&hl=zh-CN&gl=CN&ceid=CN:zh-Hans',
            json_resp=False,
            use_proxy=True,
        )
        titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', data)
        items = []
        for title in titles[1:limit+1]:
            items.append({
                'platform': 'Instagram热点',
                'title': title.strip(),
                'link': 'https://www.instagram.com/explore/',
                'hot': 0,
            })
        return items
    except Exception as e:
        print(f'  ⚠️ Instagram RSS 失败: {e}')
        return []


def _parse_rss_items(data, platform_name, limit=10):
    """通用 RSS 解析器，处理 CDATA 和非 CDATA 两种格式"""
    import xml.etree.ElementTree as ET

    def _strip_tags(html):
        return re.sub(r'<[^>]+>', '', html or '')[:120].strip()

    def _extract_text(tag_content):
        """提取标签内容，支持 CDATA 包裹"""
        m = re.search(r'<!\[CDATA\[(.*?)\]\]>', tag_content, re.DOTALL)
        if m:
            return m.group(1).strip()
        return re.sub(r'<[^>]+>', '', tag_content or '').strip()

    items = []
    # 方式1: 直接解析 item 标签（最可靠）
    item_blocks = re.findall(r'<item>(.*?)</item>', data, re.DOTALL)
    if not item_blocks:
        # 方式2: 解析 entry 标签（Atom 格式）
        item_blocks = re.findall(r'<entry>(.*?)</entry>', data, re.DOTALL)

    for block in item_blocks[:limit]:
        title_m = re.search(r'<title[^>]*>(.*?)</title>', block, re.DOTALL)
        link_m = re.search(r'<link[^>]*>(?:<!\[CDATA\[(.*?)\]\]>|(.*?))?</link>', block, re.DOTALL)
        desc_m = re.search(r'<description[^>]*>(.*?)</description>', block, re.DOTALL)
        content_m = re.search(r'<content[^>]*>(.*?)</content>', block, re.DOTALL)
        summary_m = re.search(r'<summary[^>]*>(.*?)</summary>', block, re.DOTALL)

        title = _extract_text(title_m.group(1)) if title_m else ''
        if not title:
            continue

        # 跳过 feed 本身标题（第一个 item 通常是 channel 标题重复）
        link = (link_m.group(1) or link_m.group(2) or '') if link_m else ''
        link = _extract_text(link) if link else ''
        desc_raw = (desc_m or content_m or summary_m)
        desc = _strip_tags(_extract_text(desc_raw.group(1))) if desc_raw else ''

        items.append({
            'platform': platform_name,
            'title': title,
            'link': link,
            'hot': 0,
            'excerpt': desc,
        })

    return items


def crawl_36kr(limit=10):
    """36氪 RSS 订阅源"""
    try:
        data = _get(
            'https://36kr.com/feed',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://36kr.com/',
            },
            json_resp=False,
            timeout=15,
        )
        items = _parse_rss_items(data, '36氪', limit)
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ 36氪失败: {e}')
    return []


def crawl_huxiu(limit=10):
    """虎嗅 - RSS被WAF拦截，改用主站列表页爬取"""
    try:
        data = _get(
            'https://www.huxiu.com/channel/107.html',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.huxiu.com/',
                'Accept': 'text/html,application/xhtml+xml',
            },
            json_resp=False,
            timeout=15,
        )
        titles = re.findall(r'class="article-item--main.*?<h3[^>]*>(.*?)</h3>', data, re.DOTALL)
        links = re.findall(r'href="(https?://www\.huxiu\.com/article/\d+\.html)"', data)
        descs = re.findall(r'class="article-item--main.*?<p[^>]*>(.*?)</p>', data, re.DOTALL)
        items = []
        for i in range(min(limit, len(titles))):
            title = re.sub(r'<[^>]+>', '', titles[i]).strip() if i < len(titles) else ''
            desc = re.sub(r'<[^>]+>', '', descs[i]).strip()[:120] if i < len(descs) else ''
            link = links[i] if i < len(links) else 'https://www.huxiu.com/'
            if title:
                items.append({
                    'platform': '虎嗅',
                    'title': title,
                    'link': link,
                    'hot': 0,
                    'excerpt': desc,
                })
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ 虎嗅失败: {e}')
    return []


def crawl_leiphone(limit=10):
    """雷锋网 RSS 订阅源"""
    try:
        data = _get(
            'https://www.leiphone.com/feed/',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.leiphone.com/',
            },
            json_resp=False,
            timeout=15,
        )
        items = _parse_rss_items(data, '雷锋网', limit)
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ 雷锋网失败: {e}')
    return []


def crawl_ithome(limit=10):
    """IT之家 RSS - 国内头部科技媒体"""
    try:
        data = _get(
            'https://www.ithome.com/rss/',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.ithome.com/',
            },
            json_resp=False,
            timeout=15,
        )
        items = _parse_rss_items(data, 'IT之家', limit)
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ IT之家失败: {e}')
    return []


def crawl_ifanr(limit=10):
    """爱范儿 RSS - 消费科技+商业"""
    try:
        data = _get(
            'https://www.ifanr.com/feed/',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.ifanr.com/',
            },
            json_resp=False,
            timeout=15,
        )
        items = _parse_rss_items(data, '爱范儿', limit)
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ 爱范儿失败: {e}')
    return []


def crawl_huxiu(limit=10):
    """虎嗅 - RSS被WAF拦截，改用主站列表页爬取"""
    try:
        # 尝试获取虎嗅科技栏目最新文章
        data = _get(
            'https://www.huxiu.com/channel/107.html',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.huxiu.com/',
                'Accept': 'text/html,application/xhtml+xml',
            },
            json_resp=False,
            timeout=15,
        )
        # 解析文章标题+链接
        titles = re.findall(r'class="article-item--main.*?<h3[^>]*>(.*?)</h3>', data, re.DOTALL)
        links = re.findall(r'href="(https?://www\.huxiu\.com/article/\d+\.html)"', data)
        descs = re.findall(r'class="article-item--main.*?<p[^>]*>(.*?)</p>', data, re.DOTALL)
        items = []
        for i in range(min(limit, len(titles))):
            title = re.sub(r'<[^>]+>', '', titles[i]).strip() if i < len(titles) else ''
            desc = re.sub(r'<[^>]+>', '', descs[i]).strip()[:120] if i < len(descs) else ''
            link = links[i] if i < len(links) else 'https://www.huxiu.com/'
            if title:
                items.append({
                    'platform': '虎嗅',
                    'title': title,
                    'link': link,
                    'hot': 0,
                    'excerpt': desc,
                })
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ 虎嗅失败: {e}')
    return []


def crawl_pengpai(limit=10):
    """界面新闻 RSS"""
    try:
        data = _get(
            'https://www.jiemian.com/rss.xml',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json_resp=False,
            timeout=15,
        )
        items = _parse_rss_items(data, '界面新闻', limit)
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ 界面新闻失败: {e}')
    return []


def crawl_rebang(limit=10):
    """今日热榜 / rebang.today 聚合
    来源: 多个热榜聚合站（toPhub今日热榜、zhanqi等）
    注意: 部分站点有 Cloudflare 保护，会返回验证码页面
    """
    # 方式1: 今日热榜 API (若有公开接口)
    sources = [
        ('今日热榜', 'https://tophub.today/'),
    ]

    # 方式2: 知乎/微博/抖音聚合（已有数据，通过分析聚合）
    # 此函数返回空列表，实际通过已有平台数据 + analyzer 做聚合分析
    try:
        # 尝试 tophub.today 今日汇总页
        data = _get(
            'https://tophub.today/',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            json_resp=False,
            timeout=10,
            use_proxy=True,
        )
        # 如果返回的是验证码页（包含 captcha），说明被拦截
        if 'captcha' in data.lower() or '安全验证' in data:
            print('  ⚠️ 今日热榜: 被 Cloudflare 拦截，切换到 Google News 聚合')
        else:
            # 尝试解析标题
            titles = re.findall(r'<a[^>]+class="[^"]*item[^"]*"[^>]+title="([^"]+)"', data)
            if not titles:
                titles = re.findall(r'<td[^>]*>[\s\S]*?<a[^>]+>([^<]{4,50})<', data)
            if titles:
                items = []
                for title in titles[:limit]:
                    items.append({
                        'platform': '今日热榜',
                        'title': title.strip(),
                        'link': 'https://tophub.today/',
                        'hot': 0,
                    })
                return items
    except Exception as e:
        print(f'  ⚠️ 今日热榜失败: {e}')

    # Fallback: Google News 科技+社会热点聚合（中文）
    try:
        # 用多个中文关键词组合，扩大覆盖面
        queries = [
            ('热搜', 'https://news.google.com/rss/search?q=%E7%83%AD%E6%90%9C&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
            ('热点', 'https://news.google.com/rss/search?q=%E7%83%AD%E7%82%B9&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
            ('AI', 'https://news.google.com/rss/search?q=AI&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
        ]
        all_titles = []
        for label, url in queries:
            try:
                data = _get(url, json_resp=False, use_proxy=True, timeout=10)
                # Use _parse_rss_items if available, else regex
                titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', data)
                if not titles:
                    titles = re.findall(r'<title>(.*?)</title>', data)
                # Skip first (feed title)
                for t in titles[1:limit+1]:
                    all_titles.append(t.strip())
            except Exception:
                continue
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for t in all_titles:
            if t not in seen and len(t) > 3:
                seen.add(t)
                unique.append(t)
        if unique:
            items = [{'platform': '今日热榜', 'title': t, 'link': 'https://news.google.com/search?q='+t[:20], 'hot': 0} for t in unique[:limit]]
            return items
    except Exception as e:
        print(f'  ⚠️ Google News 热榜失败: {e}')
    return []


# ============================================================
# 海外科技媒体 RSS
# ============================================================

def crawl_techcrunch(limit=10):
    """TechCrunch RSS - 全球头部科技媒体"""
    try:
        data = _get(
            'https://techcrunch.com/feed/',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://techcrunch.com/',
            },
            json_resp=False,
            timeout=15,
        )
        items = _parse_rss_items(data, 'TechCrunch', limit)
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ TechCrunch 失败: {e}')
    return []


def crawl_theverge(limit=10):
    """The Verge RSS - 科技+文化+设计"""
    try:
        data = _get(
            'https://www.theverge.com/rss/index.xml',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.theverge.com/',
            },
            json_resp=False,
            timeout=15,
        )
        items = _parse_rss_items(data, 'The Verge', limit)
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ The Verge 失败: {e}')
    return []


def crawl_wired(limit=10):
    """Wired RSS - 科技+商业+文化"""
    try:
        data = _get(
            'https://www.wired.com/feed/rss',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.wired.com/',
            },
            json_resp=False,
            timeout=15,
        )
        items = _parse_rss_items(data, 'Wired', limit)
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ Wired 失败: {e}')
    return []


def crawl_engadget(limit=10):
    """Engadget RSS - 消费科技新闻"""
    try:
        data = _get(
            'https://www.engadget.com/rss.xml',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.engadget.com/',
            },
            json_resp=False,
            timeout=15,
        )
        items = _parse_rss_items(data, 'Engadget', limit)
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ Engadget 失败: {e}')
    return []


def crawl_ars(limit=10):
    """Ars Technica RSS - 深度科技+科学"""
    try:
        data = _get(
            'https://feeds.arstechnica.com/arstechnica/index',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://arstechnica.com/',
            },
            json_resp=False,
            timeout=15,
        )
        items = _parse_rss_items(data, 'Ars Technica', limit)
        if items:
            return items
    except Exception as e:
        print(f'  ⚠️ Ars Technica 失败: {e}')
    return []


# ============================================================
# 调度器
# ============================================================

def crawl_platform(name):
    """爬取单个平台"""
    dispatch = {
        'zhihu': crawl_zhihu,
        'weibo': crawl_weibo,
        'douyin': crawl_douyin,
        '36kr': crawl_36kr,
        'huxiu': crawl_huxiu,
        'leiphone': crawl_leiphone,
        'jiemian': crawl_pengpai,
        'ithome': crawl_ithome,
        'ifanr': crawl_ifanr,
        'techcrunch': crawl_techcrunch,
        'theverge': crawl_theverge,
        'wired': crawl_wired,
        'engadget': crawl_engadget,
        'ars': crawl_ars,
        'youtube': crawl_youtube,
        'x_twitter': crawl_x_twitter,
        'instagram': crawl_instagram,
        'rebang': crawl_rebang,
    }
    fn = dispatch.get(name)
    if fn:
        return fn()
    print(f'  ⚠️ 未知平台: {name}')
    return []


def crawl_all(enabled_platforms=None):
    """并发爬取所有已启用平台"""
    import concurrent.futures

    if enabled_platforms is None:
        # 从 config 读取
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'platforms.json')
        if os.path.exists(config_path):
            cfg = json.load(open(config_path, encoding='utf-8'))
            enabled_platforms = {
                name: cfg_data.get('enabled', False)
                for name, cfg_data in cfg.get('platforms', {}).items()
            }
        else:
            enabled_platforms = {'zhihu': True, 'weibo': True, 'douyin': True}

    platforms = {
        '知乎': lambda: crawl_platform('zhihu'),
        '微博': lambda: crawl_platform('weibo'),
        '抖音': lambda: crawl_platform('douyin'),
        '36氪': lambda: crawl_platform('36kr'),
        '虎嗅': lambda: crawl_platform('huxiu'),
        '雷锋网': lambda: crawl_platform('leiphone'),
        'IT之家': lambda: crawl_platform('ithome'),
        '爱范儿': lambda: crawl_platform('ifanr'),
        '界面新闻': lambda: crawl_platform('jiemian'),
        'TechCrunch': lambda: crawl_platform('techcrunch'),
        'The Verge': lambda: crawl_platform('theverge'),
        'Wired': lambda: crawl_platform('wired'),
        'Engadget': lambda: crawl_platform('engadget'),
        'Ars Technica': lambda: crawl_platform('ars'),
        'YouTube': lambda: crawl_platform('youtube'),
        'X/Twitter': lambda: crawl_platform('x_twitter'),
        'Instagram': lambda: crawl_platform('instagram'),
        '今日热榜': lambda: crawl_platform('rebang'),
    }

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(fn): name for name, fn in platforms.items()}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
                print(f'  ✅ {name}: {len(results[name])} 条')
            except Exception as e:
                print(f'  ❌ {name}: {e}')
                results[name] = []

    return results


if __name__ == '__main__':
    r = crawl_all()
    print(json.dumps(r, ensure_ascii=False, indent=2))
