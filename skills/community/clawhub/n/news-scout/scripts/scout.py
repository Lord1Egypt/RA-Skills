#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻斥候 (News Scout) - 自动化新闻抓取工具
===========================================
功能：从 RSS 源和 Bing 新闻搜索抓取 AI 和投资领域的最新新闻
输出：JSON 格式的新闻列表

使用方法:
    python3 scout.py --category ai,investing
    python3 scout.py --category ai
    python3 scout.py --category investing

依赖安装:
    pip3 install feedparser requests
"""

import json
import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
import warnings

# 忽略警告信息，保持输出干净
warnings.filterwarnings("ignore")

# 尝试导入依赖库
try:
    import feedparser
    import requests
except ImportError as e:
    print(json.dumps({
        "error": f"缺少必要的依赖库：{e}",
        "solution": "请运行：pip3 install feedparser requests"
    }, ensure_ascii=False))
    sys.exit(1)

# 配置常量
CONFIG = {
    "timeout_seconds": 30,          # 请求超时时间（秒）
    "max_rss_entries": 5,           # 每个 RSS 源最多获取的条目数
    "max_search_results": 3,        # 每个搜索词最多获取的结果数
    "max_search_queries": 4,        # 每个分类最多使用的搜索词数量
    "time_window_hours": 48,        # 新闻时间窗口（小时）
    "max_workers": 10,              # 并发线程数
}


def fetch_rss(feed_info, hours=48):
    """
    从 RSS 源抓取新闻
    
    参数:
        feed_info: 包含 name, url, priority 的字典
        hours: 时间窗口（小时），默认 48 小时
    
    返回:
        新闻列表，每条新闻包含 title, url, source, priority, snippet, date
    """
    results = []
    try:
        # 计算时间阈值
        parsed_date = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        # 解析 RSS 源（带超时）
        d = feedparser.parse(feed_info["url"])
        
        for entry in d.entries[:CONFIG["max_rss_entries"]]:
            # 尝试解析发布日期
            entry_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                from time import mktime
                try:
                    entry_date = datetime.fromtimestamp(
                        mktime(entry.published_parsed), 
                        timezone.utc
                    )
                except (ValueError, OSError):
                    pass
            
            # 过滤时间：如果无法解析日期则保留，否则检查是否在时间窗口内
            if not entry_date or entry_date >= parsed_date:
                results.append({
                    "title": entry.title if hasattr(entry, 'title') else "",
                    "url": entry.link if hasattr(entry, 'link') else "",
                    "source": feed_info["name"],
                    "priority": feed_info.get("priority", "P2"),
                    "snippet": entry.summary if hasattr(entry, 'summary') else "",
                    "date": entry_date.isoformat() if entry_date else "Unknown",
                    "category": feed_info.get("category", "unknown")
                })
    except Exception as e:
        # 静默失败，避免单个 RSS 源影响整体
        pass
    
    return results


def fetch_search(query, debug=False):
    """
    通过 Bing News RSS 搜索新闻（国内可直接访问，无需 API Key）

    参数:
        query: 搜索关键词
        debug: 是否输出调试信息

    返回:
        新闻列表
    """
    results = []
    try:
        # 构建 Bing News RSS 搜索 URL
        encoded_query = requests.utils.quote(query)
        rss_url = f"https://www.bing.com/news/search?q={encoded_query}&format=rss"

        if debug:
            print(f"[DEBUG] Bing News RSS 搜索: {rss_url}", file=sys.stderr)

        # 使用 feedparser 解析 Bing RSS（国内可正常访问）
        d = feedparser.parse(rss_url)

        if d.bozo and debug:
            print(f"[DEBUG] Bing RSS 解析警告: {d.bozo_exception}", file=sys.stderr)

        for entry in d.entries[:CONFIG["max_search_results"]]:
            # 尝试解析日期
            entry_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                from time import mktime
                try:
                    entry_date = datetime.fromtimestamp(
                        mktime(entry.published_parsed),
                        timezone.utc
                    ).isoformat()
                except (ValueError, OSError):
                    pass

            results.append({
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "source": entry.get("source", {}).get("value", "Bing News") if hasattr(entry, "source") else "Bing News",
                "priority": "P2",
                "snippet": entry.get("summary", ""),
                "date": entry_date or "Unknown",
                "category": "search"
            })

    except Exception as e:
        if debug:
            print(f"[DEBUG] Bing News RSS 搜索失败 '{query}': {e}", file=sys.stderr)
        pass

    return results


def deduplicate_news(news_list):
    """
    对新闻列表进行去重处理
    
    策略:
        1. 基于标题相似度识别重复新闻
        2. 保留优先级更高的来源（P0 > P1 > P2）
        3. 标记被合并的新闻为"多家媒体报道"
    
    参数:
        news_list: 原始新闻列表
    
    返回:
        去重后的新闻列表
    """
    if not news_list:
        return []
    
    # 优先级映射（数字越小优先级越高）
    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    
    # 按标题分组
    grouped = {}
    for news in news_list:
        # 简化标题用于分组（去除标点、转小写）
        title_key = news["title"].lower().replace(":", "").replace(",", "")
        
        if title_key not in grouped:
            grouped[title_key] = []
        grouped[title_key].append(news)
    
    # 每组保留优先级最高的来源
    deduplicated = []
    for title_key, group in grouped.items():
        # 按优先级排序
        group.sort(key=lambda x: priority_order.get(x.get("priority", "P2"), 2))
        best = group[0]
        
        # 如果有多个来源，标记为"多家媒体报道"
        if len(group) > 1:
            best["multi_source"] = True
            best["other_sources"] = [g["source"] for g in group[1:]]
        
        deduplicated.append(best)
    
    return deduplicated


def main():
    """主函数：解析参数、加载配置、抓取新闻、输出结果"""
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="新闻斥候 (News Scout) - 自动化新闻抓取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 scout.py --category ai
    python3 scout.py --category investing
    python3 scout.py --category ai,investing
        """
    )
    parser.add_argument(
        "--category", 
        type=str, 
        default="ai,investing", 
        help="需要抓取的分类，用逗号分隔 (例如：ai,investing)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试模式，输出详细信息"
    )
    args = parser.parse_args()
    
    # 解析分类列表
    categories = [cat.strip() for cat in args.category.split(",")]
    
    # 确定工作目录和配置文件路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "resources", "news_sources.json")
    
    # 加载新闻源配置
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            sources = json.load(f)
        if args.debug:
            print(f"[DEBUG] 已加载配置文件：{json_path}", file=sys.stderr)
    except FileNotFoundError:
        print(json.dumps({
            "error": f"配置文件不存在：{json_path}",
            "solution": "请确保 news_sources.json 文件位于 resources/ 目录下"
        }, ensure_ascii=False))
        return
    except json.JSONDecodeError as e:
        print(json.dumps({
            "error": f"配置文件格式错误：{e}",
            "solution": "请检查 news_sources.json 是否为有效的 JSON 格式"
        }, ensure_ascii=False))
        return
    
    all_news = {}
    
    # 按分类抓取新闻
    for cat in categories:
        cat = cat.strip()
        all_news[cat] = []
        
        # 获取该分类的 RSS 源和搜索词
        rss_list = sources.get("rss_feeds", {}).get(cat, [])
        search_list = sources.get("search_queries", {}).get(cat, [])
        
        if args.debug:
            print(f"[DEBUG] 分类 '{cat}': {len(rss_list)} 个 RSS 源，{len(search_list)} 个搜索词", file=sys.stderr)
        
        # 为每个 RSS 源添加分类标记
        for feed in rss_list:
            feed["category"] = cat
        
        # 并发抓取（使用 ThreadPoolExecutor）
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG["max_workers"]) as executor:
            # 提交 RSS 抓取任务
            rss_futures = [
                executor.submit(fetch_rss, feed) 
                for feed in rss_list
            ]
            
            # 提交搜索任务（限制数量避免触发反爬）
            search_futures = [
                executor.submit(fetch_search, query, args.debug) 
                for query in search_list[:CONFIG["max_search_queries"]]
            ]
            
            # 收集结果
            for future in concurrent.futures.as_completed(rss_futures + search_futures):
                try:
                    res = future.result(timeout=CONFIG["timeout_seconds"])
                    if res:
                        all_news[cat].extend(res)
                except Exception as e:
                    if args.debug:
                        print(f"[DEBUG] 任务失败：{e}", file=sys.stderr)
        
        # 去重处理
        if all_news[cat]:
            all_news[cat] = deduplicate_news(all_news[cat])
            
            if args.debug:
                print(f"[DEBUG] 分类 '{cat}' 去重后剩余 {len(all_news[cat])} 条新闻", file=sys.stderr)
    
    # 输出 JSON 结果（确保中文正常显示）
    print(json.dumps(all_news, indent=2, ensure_ascii=False))
    
    # 输出统计信息到 stderr（不干扰 JSON 输出）
    if args.debug:
        total = sum(len(news) for news in all_news.values())
        print(f"[DEBUG] 总计抓取 {total} 条新闻", file=sys.stderr)


if __name__ == "__main__":
    main()
