#!/usr/bin/env python3
"""
Tech News CLI - 国际科技新闻命令行工具
从多个国际科技新闻网站获取最新RSS资讯
"""

import argparse
import json
import os
import sys
import webbrowser
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlparse

import feedparser
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import print as rprint

# 初始化 Rich Console
console = Console()

# RSS 源配置
RSS_FEEDS = {
    "techcrunch": {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "description": "创业与科技新闻",
        "category": "startup"
    },
    "theverge": {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "description": "科技、科学、艺术与文化",
        "category": "general"
    },
    "wired": {
        "name": "Wired",
        "url": "https://www.wired.com/feed/rss",
        "description": "科技与文化深度报道",
        "category": "general"
    },
    "arstechnica": {
        "name": "Ars Technica",
        "url": "https://feeds.arstechnica.com/arstechnica/index",
        "description": "深度科技分析与评论",
        "category": "tech"
    },
    "engadget": {
        "name": "Engadget",
        "url": "https://www.engadget.com/rss.xml",
        "description": "消费电子产品评测",
        "category": "gadgets"
    },
    "hackernews": {
        "name": "Hacker News",
        "url": "https://hnrss.org/frontpage",
        "description": "程序员社区热门",
        "category": "developer"
    },
    "mittech": {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "description": "麻省理工科技评论",
        "category": "science"
    },
    "gizmodo": {
        "name": "Gizmodo",
        "url": "https://gizmodo.com/rss",
        "description": "科技与生活方式",
        "category": "lifestyle"
    }
}

# 缓存目录
CACHE_DIR = os.path.expanduser("~/.tech_news_cli/cache")
CACHE_EXPIRE_MINUTES = 30


@dataclass
class NewsItem:
    """新闻条目数据类"""
    title: str
    link: str
    source: str
    published: Optional[str] = None
    summary: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "link": self.link,
            "source": self.source,
            "published": self.published,
            "summary": self.summary
        }


class NewsCache:
    """新闻缓存管理"""
    
    def __init__(self):
        self.cache_dir = CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_path(self, source_key: str) -> str:
        # 安全检查：防止路径遍历攻击
        # 只允许字母、数字、下划线和连字符
        import re
        safe_key = re.sub(r'[^a-zA-Z0-9_-]', '_', source_key)
        path = os.path.join(self.cache_dir, f"{safe_key}.json")
        # 确保最终路径在缓存目录内
        real_path = os.path.realpath(path)
        real_cache_dir = os.path.realpath(self.cache_dir)
        if not real_path.startswith(real_cache_dir):
            raise ValueError(f"Invalid cache key: {source_key}")
        return path
    
    def get(self, source_key: str) -> Optional[list]:
        """获取缓存的新闻"""
        cache_path = self._get_cache_path(source_key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查缓存是否过期
            cache_time = datetime.fromisoformat(data.get("cached_at", "2000-01-01"))
            if datetime.now() - cache_time > timedelta(minutes=CACHE_EXPIRE_MINUTES):
                return None
            
            return data.get("news", [])
        except (json.JSONDecodeError, ValueError, KeyError):
            return None
    
    def set(self, source_key: str, news_list: list):
        """设置缓存"""
        cache_path = self._get_cache_path(source_key)
        
        data = {
            "cached_at": datetime.now().isoformat(),
            "news": news_list
        }
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class RSSFetcher:
    """RSS 获取器"""
    
    def __init__(self, use_cache: bool = True):
        self.cache = NewsCache() if use_cache else None
        self.use_cache = use_cache
    
    def fetch(self, source_key: str, limit: int = 10) -> list[NewsItem]:
        """获取指定源的新闻"""
        if source_key not in RSS_FEEDS:
            console.print(f"[red]错误: 未知的新闻源 '{source_key}'[/red]")
            return []
        
        # 尝试从缓存获取
        if self.use_cache and self.cache:
            cached = self.cache.get(source_key)
            if cached:
                console.print(f"[dim]从缓存加载 {RSS_FEEDS[source_key]['name']}...[/dim]")
                return [NewsItem(**item) for item in cached[:limit]]
        
        feed_config = RSS_FEEDS[source_key]
        
        try:
            console.print(f"[cyan]正在获取 {feed_config['name']}...[/cyan]")
            
            # 设置请求头和超时
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(
                feed_config['url'], 
                headers=headers, 
                timeout=15
            )
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            news_list = []
            for entry in feed.entries[:limit]:
                # 解析发布时间
                published = None
                if hasattr(entry, 'published'):
                    published = entry.published
                elif hasattr(entry, 'pubDate'):
                    published = entry.pubDate
                
                # 解析摘要
                summary = None
                if hasattr(entry, 'summary'):
                    summary = entry.summary[:200] + "..." if len(entry.summary) > 200 else entry.summary
                
                news_item = NewsItem(
                    title=entry.title,
                    link=entry.link,
                    source=feed_config['name'],
                    published=published,
                    summary=summary
                )
                news_list.append(news_item)
            
            # 缓存结果
            if self.use_cache and self.cache:
                self.cache.set(source_key, [item.to_dict() for item in news_list])
            
            return news_list
            
        except requests.RequestException as e:
            console.print(f"[red]网络错误: {e}[/red]")
            return []
        except Exception as e:
            console.print(f"[red]解析错误: {e}[/red]")
            return []
    
    def fetch_all(self, limit_per_source: int = 5) -> list[NewsItem]:
        """获取所有源的新闻"""
        all_news = []
        
        for source_key in RSS_FEEDS:
            news = self.fetch(source_key, limit_per_source)
            all_news.extend(news)
        
        return all_news


def display_news_list(news_list: list[NewsItem], show_summary: bool = False):
    """显示新闻列表"""
    if not news_list:
        console.print("[yellow]没有获取到新闻[/yellow]")
        return
    
    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("标题", style="green", ratio=3)
    table.add_column("来源", style="blue", width=15)
    table.add_column("发布时间", style="yellow", width=20)
    
    if show_summary:
        table.add_column("摘要", style="dim", ratio=2)
    
    for idx, news in enumerate(news_list, 1):
        row = [str(idx), news.title, news.source, news.published or "N/A"]
        
        if show_summary:
            # 清理HTML标签
            summary = news.summary.replace("<br/>", " ").replace("<br>", " ") if news.summary else ""
            row.append(summary[:100] + "..." if len(summary) > 100 else summary)
        
        table.add_row(*row)
    
    console.print(table)


def display_news_detail(news: NewsItem, index: int):
    """显示新闻详情"""
    panel = Panel(
        f"[bold green]{news.title}[/bold green]\n\n"
        f"[dim]来源:[/dim] [blue]{news.source}[/blue]\n"
        f"[dim]时间:[/dim] [yellow]{news.published or 'N/A'}[/yellow]\n"
        f"[dim]链接:[/dim] [link={news.link}]{news.link}[/link]\n",
        title=f"[bold]新闻 #{index}[/bold]",
        border_style="cyan"
    )
    console.print(panel)


def display_sources():
    """显示所有可用的新闻源"""
    table = Table(title="📰 可用的新闻源", show_header=True, header_style="bold magenta")
    table.add_column("序号", style="dim", width=6)
    table.add_column("Key", style="cyan", width=15)
    table.add_column("名称", style="green", width=20)
    table.add_column("描述", style="white")
    table.add_column("分类", style="yellow", width=12)
    
    for idx, (key, config) in enumerate(RSS_FEEDS.items(), 1):
        table.add_row(
            str(idx),
            key,
            config['name'],
            config['description'],
            config['category']
        )
    
    console.print(table)


def open_in_browser(news_list: list[NewsItem], index: int):
    """在浏览器中打开新闻"""
    if 1 <= index <= len(news_list):
        news = news_list[index - 1]
        console.print(f"[cyan]正在打开: {news.title}[/cyan]")
        webbrowser.open(news.link)
    else:
        console.print(f"[red]无效的序号: {index}[/red]")


def interactive_mode(fetcher: RSSFetcher, news_list: list[NewsItem]):
    """交互模式"""
    console.print("\n[bold cyan]交互模式[/bold cyan]")
    console.print("[dim]输入 'h' 查看帮助, 'q' 退出[/dim]\n")
    
    while True:
        try:
            user_input = console.input("[bold green]>>> [/bold green]").strip().lower()
            
            if not user_input:
                continue
            
            if user_input == 'q' or user_input == 'quit' or user_input == 'exit':
                console.print("[yellow]再见！[/yellow]")
                break
            
            elif user_input == 'h' or user_input == 'help':
                help_text = """
[bold]命令帮助:[/bold]
  [cyan]h, help[/cyan]     - 显示帮助信息
  [cyan]q, quit[/cyan]     - 退出程序
  [cyan]l, list[/cyan]     - 重新显示新闻列表
  [cyan]s, sources[/cyan]  - 显示所有新闻源
  [cyan]r, refresh[/cyan]  - 刷新当前源
  [cyan]<数字>[/cyan]       - 查看指定新闻详情
  [cyan]o <数字>[/cyan]     - 在浏览器中打开指定新闻
  [cyan]all[/cyan]          - 获取所有源的新闻
"""
                console.print(Panel(help_text, title="帮助", border_style="blue"))
            
            elif user_input == 'l' or user_input == 'list':
                display_news_list(news_list)
            
            elif user_input == 's' or user_input == 'sources':
                display_sources()
            
            elif user_input == 'r' or user_input == 'refresh':
                console.print("[cyan]刷新中...[/cyan]")
                news_list = fetcher.fetch_all()
                display_news_list(news_list)
            
            elif user_input == 'all':
                news_list = fetcher.fetch_all()
                display_news_list(news_list)
            
            elif user_input.startswith('o '):
                try:
                    index = int(user_input[2:])
                    open_in_browser(news_list, index)
                except ValueError:
                    console.print("[red]请输入有效的数字[/red]")
            
            elif user_input.isdigit():
                index = int(user_input)
                if 1 <= index <= len(news_list):
                    display_news_detail(news_list[index - 1], index)
                else:
                    console.print(f"[red]无效的序号: {index}[/red]")
            
            else:
                console.print(f"[red]未知命令: {user_input}[/red]")
                console.print("[dim]输入 'h' 查看帮助[/dim]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]再见！[/yellow]")
            break


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Tech News CLI - 国际科技新闻命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 获取所有新闻源的头条
  %(prog)s -s techcrunch      # 获取 TechCrunch 新闻
  %(prog)s -l 20              # 每个源获取20条新闻
  %(prog)s --sources          # 显示所有新闻源
  %(prog)s -i                 # 进入交互模式
  %(prog)s --no-cache         # 不使用缓存
        """
    )
    
    parser.add_argument(
        '-s', '--source',
        type=str,
        default=None,
        help='指定新闻源 (如: techcrunch, theverge)'
    )
    
    parser.add_argument(
        '-l', '--limit',
        type=int,
        default=10,
        help='每个源获取的新闻数量 (默认: 10)'
    )
    
    parser.add_argument(
        '--sources',
        action='store_true',
        help='显示所有可用的新闻源'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='进入交互模式'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='不使用缓存'
    )
    
    parser.add_argument(
        '--summary',
        action='store_true',
        help='显示新闻摘要'
    )
    
    parser.add_argument(
        '-o', '--open',
        type=int,
        default=None,
        help='在浏览器中打开指定序号的新闻'
    )
    
    args = parser.parse_args()
    
    # 显示新闻源
    if args.sources:
        display_sources()
        return
    
    # 创建获取器
    fetcher = RSSFetcher(use_cache=not args.no_cache)
    
    # 获取新闻
    if args.source:
        if args.source not in RSS_FEEDS:
            console.print(f"[red]错误: 未知的新闻源 '{args.source}'[/red]")
            console.print("[dim]使用 --sources 查看所有可用的新闻源[/dim]")
            sys.exit(1)
        news_list = fetcher.fetch(args.source, args.limit)
    else:
        news_list = fetcher.fetch_all(args.limit)
    
    # 打开指定新闻
    if args.open is not None:
        open_in_browser(news_list, args.open)
        return
    
    # 显示新闻
    md = display_news_list_markdown(news_list, show_summary=args.summary)
    print(md)

def display_news_list_markdown(news_list: list[NewsItem], show_summary: bool = False) -> str:
    """返回 Markdown 格式的新闻列表（source 带链接）"""
    if not news_list:
        return "⚠️ 没有获取到新闻"

    headers = ["#", "标题", "来源", "发布时间"]
    if show_summary:
        headers.append("摘要")

    md = []
    md.append("| " + " | ".join(headers) + " |")
    md.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for idx, news in enumerate(news_list, 1):
        # 👉 source 加链接（假设 news.link 存在）
        source_md = news.source
        if getattr(news, "link", None):
            source_md = f"[{news.source}]({news.link})"

        row = [
            str(idx),
            news.title,
            source_md,
            news.published or "N/A",
        ]

        if show_summary:
            summary = (
                news.summary.replace("<br/>", " ").replace("<br>", " ")
                if news.summary else ""
            )
            summary = summary[:100] + "..." if len(summary) > 100 else summary
            row.append(summary)

        # 转义 Markdown 特殊字符（避免破坏表格）
        row = [str(cell).replace("|", "\\|") for cell in row]

        md.append("| " + " | ".join(row) + " |")

    return "\n".join(md)

if __name__ == "__main__":
    # Fix Windows console encoding
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    main()
