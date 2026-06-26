#!/usr/bin/env python3
"""
整理脚本 - 对提取的文章数据进行清洗、去重、分类和格式化
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from collections import defaultdict


DEFAULT_OUTPUT_DIR = "data/organized"


def clean_title(title: str) -> str:
    """清理标题，移除多余空白和特殊字符"""
    if not title:
        return ""
    
    # 移除多余空白
    title = re.sub(r'\s+', ' ', title).strip()
    
    # 移除常见的垃圾字符
    title = title.replace('\n', ' ').replace('\t', ' ')
    
    # 限制长度
    if len(title) > 200:
        title = title[:197] + "..."
    
    return title


def clean_url(url: str) -> str:
    """清理 URL，移除跟踪参数"""
    if not url:
        return ""
    
    # 移除常见的跟踪参数
    tracking_params = [
        'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
        'fbclid', 'gclid', 'ref', 'source', 'campaign'
    ]
    
    # 简单处理，实际应用中可能需要 urllib.parse
    for param in tracking_params:
        url = re.sub(rf'[?&]{param}=[^&]*', '', url)
    
    # 清理末尾的 ? 和 &
    url = url.rstrip('?&')
    
    return url


def normalize_category(category: str) -> str:
    """标准化分类名称"""
    category_map = {
        'ai': 'AI',
        'artificialintelligence': 'AI',
        'machinelearning': 'AI',
        'ml': 'AI',
        'deeplearning': 'AI',
        'programming': 'Programming',
        'coding': 'Programming',
        'development': 'Programming',
        'software': 'Programming',
        'startup': 'Startup',
        'business': 'Startup',
        'venture': 'Startup',
        'science': 'Science',
        'research': 'Science',
        'security': 'Security',
        'privacy': 'Security',
        'hardware': 'Hardware',
        'other': 'Other',
    }
    
    normalized = category_map.get(category.lower(), category)
    return normalized if normalized else "Other"


def deduplicate_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    对文章进行去重
    
    策略：
    1. 基于 URL 精确去重
    2. 基于标题相似度去重（可选）
    """
    seen_urls: Set[str] = set()
    seen_titles: Set[str] = set()
    unique_articles = []
    
    for article in articles:
        url = article.get('url', '').strip().lower()
        title = article.get('title', '').strip().lower()
        
        # URL 去重
        if url in seen_urls:
            continue
        
        # 标题去重（完全匹配）
        if title in seen_titles:
            continue
        
        seen_urls.add(url)
        seen_titles.add(title)
        unique_articles.append(article)
    
    return unique_articles


def filter_articles(articles: List[Dict[str, Any]], min_score: int = 0) -> List[Dict[str, Any]]:
    """
    过滤文章
    
    Args:
        articles: 文章列表
        min_score: 最小分数阈值
    """
    filtered = []
    
    for article in articles:
        # 必须有标题和 URL
        if not article.get('title') or not article.get('url'):
            continue
        
        # 标题不能太短
        if len(article['title']) < 5:
            continue
        
        # 分数过滤
        if article.get('score', 0) < min_score:
            continue
        
        filtered.append(article)
    
    return filtered


def sort_articles(articles: List[Dict[str, Any]], sort_by: str = "score") -> List[Dict[str, Any]]:
    """
    对文章进行排序
    
    Args:
        articles: 文章列表
        sort_by: 排序字段 (score, comments, time)
    """
    if sort_by == "score":
        return sorted(articles, key=lambda x: x.get('score', 0), reverse=True)
    elif sort_by == "comments":
        return sorted(articles, key=lambda x: x.get('comments_count', 0), reverse=True)
    elif sort_by == "time":
        # 按时间排序（这里简化处理，实际应该解析时间）
        return articles
    else:
        return articles


def categorize_articles(articles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """按分类对文章进行分组"""
    categories = defaultdict(list)
    
    for article in articles:
        category = article.get('category', 'Other')
        category = normalize_category(category)
        categories[category].append(article)
    
    return dict(categories)


def enrich_article(article: Dict[str, Any]) -> Dict[str, Any]]:
    """丰富文章信息"""
    enriched = article.copy()
    
    # 清理标题
    enriched['title'] = clean_title(article.get('title', ''))
    
    # 清理 URL
    enriched['url'] = clean_url(article.get('url', ''))
    
    # 标准化分类
    enriched['category'] = normalize_category(article.get('category', 'Other'))
    
    # 确保数值字段
    enriched['score'] = int(article.get('score', 0) or 0)
    enriched['comments_count'] = int(article.get('comments_count', 0) or 0)
    
    # 添加整理时间戳
    enriched['organized_at'] = datetime.now().isoformat()
    
    return enriched


def organize_articles(articles: List[Dict[str, Any]], min_score: int = 0) -> Dict[str, Any]]:
    """
    整理文章数据
    
    Args:
        articles: 原始文章列表
        min_score: 最小分数阈值
        
    Returns:
        整理后的数据结构
    """
    print(f"[Organize] 开始整理 {len(articles)} 篇文章...")
    
    # 1. 丰富和清理每篇文章
    enriched = [enrich_article(a) for a in articles]
    print(f"[Organize] 数据清理完成")
    
    # 2. 过滤
    filtered = filter_articles(enriched, min_score)
    print(f"[Organize] 过滤后剩余 {len(filtered)} 篇文章")
    
    # 3. 去重
    unique = deduplicate_articles(filtered)
    print(f"[Organize] 去重后剩余 {len(unique)} 篇文章")
    
    # 4. 排序
    sorted_articles = sort_articles(unique, "score")
    
    # 5. 分类
    categorized = categorize_articles(sorted_articles)
    print(f"[Organize] 分类统计: {dict((k, len(v)) for k, v in categorized.items())}")
    
    # 6. 生成统计信息
    stats = {
        "total_articles": len(sorted_articles),
        "categories": {cat: len(items) for cat, items in categorized.items()},
        "top_sources": get_top_sources(sorted_articles, 10),
        "score_distribution": get_score_distribution(sorted_articles),
        "organized_at": datetime.now().isoformat(),
    }
    
    result = {
        "articles": sorted_articles,
        "by_category": categorized,
        "statistics": stats,
        "metadata": {
            "original_count": len(articles),
            "filtered_count": len(filtered),
            "final_count": len(sorted_articles),
            "min_score": min_score,
        }
    }
    
    return result


def get_top_sources(articles: List[Dict[str, Any]], n: int = 10) -> List[Dict[str, Any]]:
    """获取主要来源网站统计"""
    source_counts = defaultdict(lambda: {"count": 0, "total_score": 0})
    
    for article in articles:
        source = article.get('source_site', 'Unknown')
        source_counts[source]["count"] += 1
        source_counts[source]["total_score"] += article.get('score', 0)
    
    # 转换为列表并排序
    sources = [
        {"name": name, **data}
        for name, data in source_counts.items()
    ]
    sources.sort(key=lambda x: x["count"], reverse=True)
    
    return sources[:n]


def get_score_distribution(articles: List[Dict[str, Any]]) -> Dict[str, int]:
    """获取分数分布"""
    distribution = {
        "high (100+)": 0,
        "medium (50-99)": 0,
        "low (10-49)": 0,
        "very low (<10)": 0,
    }
    
    for article in articles:
        score = article.get('score', 0)
        if score >= 100:
            distribution["high (100+)"] += 1
        elif score >= 50:
            distribution["medium (50-99)"] += 1
        elif score >= 10:
            distribution["low (10-49)"] += 1
        else:
            distribution["very low (<10)"] += 1
    
    return distribution


def save_organized_data(data: Dict[str, Any], output_dir: str, source_file: str = None) -> Path:
    """保存整理后的数据"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"articles_organized_{timestamp}.json"
    file_path = output_path / filename
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[Organize] 数据已保存到: {file_path}")
    
    return file_path


def main():
    parser = argparse.ArgumentParser(
        description="整理和清洗文章数据"
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="输入 JSON 文件路径（默认从 data/extracted/ 目录查找最新文件）"
    )
    parser.add_argument(
        "--output-dir",
        default=os.getenv("OUTPUT_DIR", DEFAULT_OUTPUT_DIR),
        help=f"输出目录 (默认: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=0,
        help="最小分数阈值 (默认: 0)"
    )
    
    args = parser.parse_args()
    
    try:
        # 确定输入文件
        if args.input_file:
            input_path = Path(args.input_file)
        else:
            # 查找最新的 JSON 文件
            extracted_dir = Path("data/extracted")
            if extracted_dir.exists():
                json_files = sorted(extracted_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
                if json_files:
                    input_path = json_files[0]
                    print(f"[Organize] 使用最新的 JSON 文件: {input_path}")
                else:
                    print("[Organize] 错误: 未找到 JSON 文件", file=sys.stderr)
                    return 1
            else:
                print("[Organize] 错误: data/extracted/ 目录不存在", file=sys.stderr)
                return 1
        
        # 读取数据
        print(f"[Organize] 正在读取: {input_path}")
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        articles = data.get("articles", [])
        
        if not articles:
            print("[Organize] 错误: 没有找到文章数据", file=sys.stderr)
            return 1
        
        # 整理数据
        organized = organize_articles(articles, args.min_score)
        
        # 保存结果
        output_path = save_organized_data(organized, args.output_dir, input_path)
        
        print(f"[Organize] 完成！")
        print(f"[Organize] - 原始文章数: {organized['metadata']['original_count']}")
        print(f"[Organize] - 最终文章数: {organized['metadata']['final_count']}")
        print(f"[Organize] - 分类数: {len(organized['by_category'])}")
        print(f"OUTPUT_FILE:{output_path}")
        
        return 0
        
    except Exception as e:
        print(f"[Organize] 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
