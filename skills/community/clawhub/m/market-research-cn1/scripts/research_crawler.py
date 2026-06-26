#!/usr/bin/env python3
"""
市场调研爬虫脚本
用于在RSS和web_fetch失效时，自动爬取网站内容供AI分析

使用方法:
    python research_crawler.py <搜索关键词> [搜索数量]
    
示例:
    python research_crawler.py "AI人工智能行业"       # 默认5条
    python research_crawler.py "新能源汽车市场" 10    # 指定10条
"""

import argparse
import json
import sys
import time
from urllib.parse import quote, urljoin
import re

try:
    import requests
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    # 如果没有beautifuls4，使用内置html.parser
    from html.parser import HTMLParser
    BS4_AVAILABLE = False
    print("⚠️ beautifulsoup4未安装，使用内置解析器", file=sys.stderr)

# 默认搜索源配置
SEARCH_SOURCES = [
    {
        "name": "百度搜索",
        "url": "https://www.baidu.com/s",
        "params": lambda q: {"wd": q, "rn": 10},
        "parse": "baidu"
    },
    {
        "name": "搜狗搜索",
        "url": "https://www.sogou.com/web",
        "params": lambda q: {"query": q, "num": 10},
        "parse": "sogou"
    },
    {
        "name": "必应搜索",
        "url": "https://www.bing.com/search",
        "params": lambda q: {"q": q, "count": 10},
        "parse": "bing"
    }
]

# 新闻源配置（可直接抓取）
NEWS_SOURCES = [
    {"name": "36氪", "url": "https://www.36kr.com/information/"},
    {"name": "虎嗅", "url": "https://www.huxiu.com/"},
    {"name": "钛媒体", "url": "https://www.tmtpost.com/"},
    {"name": "爱范儿", "url": "https://www.ifanr.com/"},
    {"name": "创业邦", "url": "https://www.cyzone.cn/"},
    {"name": "极客公园", "url": "https://www.geekpark.net/"},
    {"name": "网易科技", "url": "https://tech.163.com/"},
    {"name": "腾讯科技", "url": "https://new.qq.com/ch/tech/"},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

TIMEOUT = 15


def search_baidu(query, num=10):
    """百度搜索"""
    if not BS4_AVAILABLE:
        return []
    try:
        url = "https://www.baidu.com/s"
        params = {"wd": query, "rn": min(num, 50), "pn": 0}
        
        response = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for item in soup.select('.result, .result-op')[:num]:
            try:
                title_elem = item.select_one('h3 a') or item.select_one('.c-title')
                title = title_elem.get_text(strip=True) if title_elem else ""
                
                link = item.select_one('a')
                href = link.get('href', '') if link else ''
                
                # 百度搜索结果需要解析真实URL
                if 'baidu.com' in href and 'http' not in href:
                    try:
                        resp = requests.get(href, headers=HEADERS, timeout=5, allow_redirects=True)
                        href = resp.url
                    except:
                        pass
                
                # 摘要
                abstract = item.select_one('.c-abstract, .c-snippet, .result-op')
                summary = abstract.get_text(strip=True)[:200] if abstract else ""
                
                if title and href:
                    results.append({
                        "title": title,
                        "url": href,
                        "summary": summary
                    })
            except:
                continue
        
        return results
    except Exception as e:
        print(f"百度搜索失败: {e}", file=sys.stderr)
        return []


def search_bing(query, num=10):
    """必应搜索"""
    if not BS4_AVAILABLE:
        return []
    try:
        url = "https://www.bing.com/search"
        params = {"q": query, "count": min(num, 50), "first": 0}
        
        response = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for item in soup.select('.b_algo, .b_ansr')[:num]:
            try:
                title_elem = item.select_one('h2 a') or item.select_one('h3 a')
                title = title_elem.get_text(strip=True) if title_elem else ""
                
                href = title_elem.get('href', '') if title_elem else ''
                summary = item.select_one('.b_caption p, p')
                desc = summary.get_text(strip=True)[:200] if summary else ""
                
                if title and href:
                    results.append({
                        "title": title,
                        "url": href,
                        "summary": desc
                    })
            except:
                continue
        
        return results
    except Exception as e:
        print(f"必应搜索失败: {e}", file=sys.stderr)
        return []


def crawl_page(url, max_chars=5000):
    """爬取单个页面内容"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.encoding = response.apparent_encoding or 'utf-8'
        
        html = response.text
        
        if BS4_AVAILABLE:
            soup = BeautifulSoup(html, 'html.parser')
            # 移除脚本和样式
            for script in soup(["script", "style"]):
                script.decompose()
            # 获取标题
            title = soup.title.string if soup.title else ""
            if not title:
                title = soup.h1.get_text(strip=True) if soup.h1 else ""
            # 获取主要内容
            content = ""
            for selector in ['article', 'main', '.article-content', '.post-content', '.content', '#content']:
                elem = soup.select_one(selector)
                if elem:
                    content = elem.get_text(separator='\n', strip=True)
                    break
            if not content:
                body = soup.body
                if body:
                    content = body.get_text(separator='\n', strip=True)
        else:
            # 使用简单解析
            from html.parser import HTMLParser
            class SimpleParser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.title = ""
                    self.content = []
                    self.in_body = False
                    self.in_script = False
                    self.in_style = False
                    self.skip = False
                def handle_starttag(self, tag, attrs):
                    if tag == "title":
                        self.skip = True
                    elif tag in ("script", "style"):
                        self.in_script = True
                    elif tag == "body":
                        self.in_body = True
                    elif tag in ("h1", "p", "div", "span", "article") and self.in_body:
                        self.skip = True
                def handle_endtag(self, tag):
                    if tag == "title":
                        self.skip = False
                    elif tag in ("script", "style"):
                        self.in_script = False
                    elif tag in ("h1", "p", "div", "span", "article"):
                        self.skip = False
                def handle_data(self, data):
                    if not self.in_script:
                        if self.skip or self.in_body:
                            self.content.append(data)
            
            parser = SimpleParser()
            parser.feed(html)
            title = parser.title
            content = '\n'.join(parser.content)
        
        # 清理内容
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r' {2,}', ' ', content)
        
        # 限制长度
        if len(content) > max_chars:
            content = content[:max_chars] + "..."
        
        return {
            "title": title[:200] if title else url,
            "url": url,
            "content": content,
            "length": len(content)
        }
    except Exception as e:
        return {"error": str(e), "url": url}


def search_ddg(query, num=5):
    """DuckDuckGo搜索（不依赖bs4）"""
    try:
        url = "https://html.duckduckgo.com/html/"
        data = {"q": query, "b": ""}
        response = requests.post(url, data=data, headers=HEADERS, timeout=TIMEOUT)
        response.encoding = 'utf-8'
        
        results = []
        # 简单解析
        import re
        pattern = r'<a class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>'
        for match in re.findall(pattern, response.text)[:num]:
            href, title = match
            results.append({
                "title": title.strip(),
                "url": href.strip(),
                "summary": ""
            })
        return results
    except Exception as e:
        print(f"DuckDuckGo搜索失败: {e}", file=sys.stderr)
        return []


def search_industry(query, num=10):
    """行业搜索主函数"""
    print(f"🔍 正在搜索: {query}", file=sys.stderr)
    
    all_results = []
    
    # 如果有bs4，尝试百度/必应
    if BS4_AVAILABLE:
        print("  - 尝试百度搜索...", file=sys.stderr)
        results = search_baidu(query, num)
        if results:
            all_results.extend(results)
            print(f"    百度找到 {len(results)} 条结果", file=sys.stderr)
        
        if len(all_results) < 3:
            print("  - 尝试必应搜索...", file=sys.stderr)
            results = search_bing(query, num)
            if results:
                all_results.extend(results)
                print(f"    必应找到 {len(results)} 条结果", file=sys.stderr)
    
    # 如果没有结果，尝试DuckDuckGo
    if not all_results:
        print("  - 尝试DuckDuckGo搜索...", file=sys.stderr)
        results = search_ddg(query, num)
        if results:
            all_results.extend(results)
            print(f"    DuckDuckGo找到 {len(results)} 条结果", file=sys.stderr)
    
    # 如果还没结果，直接抓取新闻源
    if not all_results:
        print("⚠️ 搜索引擎均失败，尝试直接抓取新闻源...", file=sys.stderr)
        for source in NEWS_SOURCES[:3]:
            print(f"    尝试 {source['name']}...", file=sys.stderr)
            result = crawl_page(source['url'])
            if 'error' not in result:
                all_results.append({
                    "title": f"{source['name']} 首页",
                    "url": source['url'],
                    "summary": result['content'][:500]
                })
                break
    
    return all_results[:num]


def fetch_page_details(urls, max_pages=5):
    """获取多个页面的详细内容"""
    detailed = []
    
    for i, url in enumerate(urls[:max_pages]):
        print(f"  抓取页面 {i+1}/{min(len(urls), max_pages)}: {url[:50]}...", file=sys.stderr)
        result = crawl_page(url)
        
        if 'error' not in result:
            detailed.append(result)
        
        time.sleep(1)  # 避免请求过快
    
    return detailed


def main():
    parser = argparse.ArgumentParser(
        description="市场调研爬虫 - 自动爬取网站内容供AI分析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python research_crawler.py "AI人工智能行业"
    python research_crawler.py "新能源汽车市场" 10
    python research_crawler.py "咖啡市场分析" --pages 3
        """
    )
    parser.add_argument("query", help="搜索关键词/主题")
    parser.add_argument("-n", "--num", type=int, default=5, help="搜索结果数量 (默认: 5)")
    parser.add_argument("-p", "--pages", type=int, default=3, help="详细抓取页面数 (默认: 3)")
    parser.add_argument("-o", "--output", help="输出文件路径 (JSON格式)")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"🔍 搜索: {args.query}", file=sys.stderr)
        print(f"📊 搜索结果数: {args.num}", file=sys.stderr)
        print(f"📄 详细页面数: {args.pages}", file=sys.stderr)
        print("-" * 40, file=sys.stderr)
    
    # 步骤1: 搜索
    search_results = search_industry(args.query, args.num)
    
    if not search_results:
        print("❌ 未找到任何结果", file=sys.stderr)
        sys.exit(1)
    
    # 步骤2: 抓取详细页面
    urls = [r['url'] for r in search_results if 'url' in r]
    detailed_results = fetch_page_details(urls, args.pages)
    
    # 整合结果
    output = {
        "query": args.query,
        "search_results": search_results,
        "detailed_pages": detailed_results,
        "summary": f"共找到 {len(search_results)} 条搜索结果，详细抓取了 {len(detailed_results)} 个页面"
    }
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"✅ 结果已保存到: {args.output}", file=sys.stderr)
    else:
        # 输出JSON给AI解析
        print(json.dumps(output, ensure_ascii=False, indent=2))
    
    print(f"\n✅ 完成! 搜索:{len(search_results)}条, 抓取:{len(detailed_results)}页", file=sys.stderr)


if __name__ == "__main__":
    main()
