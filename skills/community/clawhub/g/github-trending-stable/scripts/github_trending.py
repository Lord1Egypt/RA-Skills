import argparse
import http.client
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser

# 设置时区
BEIJING_TZ = timezone(timedelta(hours=8))

# 语言别名映射
LANGUAGE_SLUG_MAP = {
    "c++": "c++", "cpp": "c++", "c#": "c%23", "csharp": "c%23",
    "js": "javascript", "ts": "typescript", "py": "python",
    "rs": "rust", "rb": "ruby", "go": "go"
}

class GithubTrendingParser(HTMLParser):
    def __init__(self, limit=15):
        super().__init__()
        self.limit = limit
        self.repos = []
        self.current_repo = None
        
        # 状态机控制
        self.in_repo = False
        self.tag_stack = []
        self.capture_desc = False
        self.capture_lang = False
        self.capture_stars_gained = False
        self.capture_stars_total = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')
        
        # 1. 发现项目容器
        if tag == 'article' and 'Box-row' in cls:
            self.in_repo = True
            self.current_repo = {
                "rank": len(self.repos) + 1,
                "full_name": "", "url": "", "description": "",
                "language": "", "stars_total": "", "stars_gained": ""
            }

        if not self.in_repo: return
        self.tag_stack.append(tag)

        # 2. 提取名称和链接 (在 h2 下的 a)
        if tag == 'a' and len(self.tag_stack) >= 2 and self.tag_stack[-2] == 'h2':
            href = attrs_dict.get('href', '')
            self.current_repo["full_name"] = href.strip('/')
            self.current_repo["url"] = f"https://github.com{href}"

        # 3. 提取描述 (p 标签)
        if tag == 'p' and 'col-9' in cls:
            self.capture_desc = True

        # 4. 提取编程语言
        if tag == 'span' and attrs_dict.get('itemprop') == 'programmingLanguage':
            self.capture_lang = True

        # 5. 提取 Star 总数 (带有 stargazers 链接的 a)
        if tag == 'a' and '/stargazers' in attrs_dict.get('href', ''):
            self.capture_stars_total = True

        # 6. 提取新增 Star (包含 float-sm-right 的 span)
        if tag == 'span' and 'float-sm-right' in cls:
            self.capture_stars_gained = True

    def handle_data(self, data):
        if not self.current_repo: return
        val = data.strip()
        if not val: return

        if self.capture_desc:
            self.current_repo["description"] = val
        elif self.capture_lang:
            self.current_repo["language"] = val
        elif self.capture_stars_total:
            self.current_repo["stars_total"] = val.replace(',', '')
        elif self.capture_stars_gained:
            # 提取数字，例如 "1,234 stars today" -> "1234"
            num = "".join(filter(str.isdigit, val.replace(',', '')))
            if num: self.current_repo["stars_gained"] = int(num)

    def handle_endtag(self, tag):
        if self.tag_stack: self.tag_stack.pop()
        
        # 关闭捕获状态
        if tag == 'p': self.capture_desc = False
        if tag == 'span': 
            self.capture_lang = False
            self.capture_stars_gained = False
        if tag == 'a': self.capture_stars_total = False
            
        # 结束条目解析
        if tag == 'article' and self.current_repo:
            if len(self.repos) < self.limit:
                self.repos.append(self.current_repo)
            self.in_repo = False
            self.current_repo = None

def fetch_trending(period="weekly", language="", limit=15):
    lang_slug = LANGUAGE_SLUG_MAP.get(language.lower(), language.replace(" ", "-")) if language else ""
    base = "https://github.com/trending"
    url = f"{base}/{lang_slug}?since={period}" if lang_slug else f"{base}?since={period}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            try:
                html = response.read().decode('utf-8')
            except http.client.IncompleteRead as e:
                # 连接提前关闭时使用已读取的数据（通常前 400KB 已包含趋势列表）
                html = (e.partial or b"").decode('utf-8', errors='replace')
                if not e.partial:
                    print(f"[WARN] 未读取到数据", file=sys.stderr)
                    return []
            parser = GithubTrendingParser(limit=limit)
            parser.feed(html)
            return parser.repos
    except Exception as e:
        print(f"[ERROR] 抓取失败: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="GitHub Trending (Standard Library Version)")
    parser.add_argument("period", nargs="?", default="weekly", choices=["daily", "weekly", "monthly"], help="时间跨度")
    parser.add_argument("--limit", type=int, default=15, help="展示数量")
    parser.add_argument("--language", default="", help="编程语言")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    args = parser.parse_args()

    repos = fetch_trending(args.period, args.language, args.limit)

    if args.json:
        result = {
            "period": args.period,
            "updated_at": datetime.now(BEIJING_TZ).isoformat(),
            "data": repos
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n🚀 GitHub Trending ({args.period}) | {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M')}")
        print("=" * 60)
        for r in repos:
            print(f"{r['rank']}. {r['full_name']}")
            if r['description']:
                desc = r['description']
                print(f"   📝 {desc}")
            
            stats = []
            if r['language']: stats.append(f"🔧 {r['language']}")
            if r['stars_total']: stats.append(f"⭐ {r['stars_total']}")
            if r['stars_gained']: stats.append(f"📈 +{r['stars_gained']}")
            
            if stats: print(f"   {' | '.join(stats)}")
            print("-" * 40)

if __name__ == "__main__":
    main()
