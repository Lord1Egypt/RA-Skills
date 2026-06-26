#!/usr/bin/env python3
"""
总结脚本 - 生成摘要报告，包括热点话题统计、趋势分析等
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import defaultdict


DEFAULT_OUTPUT_DIR = "data/summary"


def generate_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成数据总结
    
    Args:
        data: 整理后的数据
        
    Returns:
        总结报告
    """
    articles = data.get("articles", [])
    by_category = data.get("by_category", {})
    stats = data.get("statistics", {})
    
    summary = {
        "report_title": "HN AI Maker 资讯日报",
        "generated_at": datetime.now().isoformat(),
        "source_url": "https://hn.aimaker.dev/",
        "overview": generate_overview(articles, stats),
        "highlights": generate_highlights(articles),
        "by_category": generate_category_summary(by_category),
        "trending_topics": extract_trending_topics(articles),
        "top_discussions": get_top_discussions(articles),
        "source_analysis": analyze_sources(stats.get("top_sources", [])),
        "recommendations": generate_recommendations(articles, by_category),
    }
    
    return summary


def generate_overview(articles: List[Dict[str, Any]], stats: Dict[str, Any]) -> Dict[str, Any]:
    """生成概览信息"""
    if not articles:
        return {"error": "没有文章数据"}
    
    total_score = sum(a.get("score", 0) for a in articles)
    total_comments = sum(a.get("comments_count", 0) for a in articles)
    avg_score = total_score / len(articles) if articles else 0
    
    # 找出最高分的文章
    top_article = max(articles, key=lambda x: x.get("score", 0))
    
    # 找出最热门的讨论
    most_discussed = max(articles, key=lambda x: x.get("comments_count", 0))
    
    return {
        "total_articles": len(articles),
        "total_score": total_score,
        "total_comments": total_comments,
        "average_score": round(avg_score, 2),
        "top_article": {
            "title": top_article.get("title", ""),
            "url": top_article.get("url", ""),
            "score": top_article.get("score", 0),
        },
        "most_discussed": {
            "title": most_discussed.get("title", ""),
            "url": most_discussed.get("url", ""),
            "comments_count": most_discussed.get("comments_count", 0),
        },
        "categories": stats.get("categories", {}),
        "score_distribution": stats.get("score_distribution", {}),
    }


def generate_highlights(articles: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
    """生成热门文章列表"""
    sorted_articles = sorted(articles, key=lambda x: x.get("score", 0), reverse=True)
    
    highlights = []
    for i, article in enumerate(sorted_articles[:top_n], 1):
        highlights.append({
            "rank": i,
            "title": article.get("title", ""),
            "url": article.get("url", ""),
            "source_site": article.get("source_site", ""),
            "score": article.get("score", 0),
            "comments_count": article.get("comments_count", 0),
            "category": article.get("category", "Other"),
        })
    
    return highlights


def generate_category_summary(by_category: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """生成分类摘要"""
    summary = {}
    
    for category, articles in by_category.items():
        if not articles:
            continue
        
        total_score = sum(a.get("score", 0) for a in articles)
        avg_score = total_score / len(articles)
        
        # 获取该分类的热门文章
        top_article = max(articles, key=lambda x: x.get("score", 0))
        
        summary[category] = {
            "count": len(articles),
            "total_score": total_score,
            "average_score": round(avg_score, 2),
            "top_article": {
                "title": top_article.get("title", ""),
                "url": top_article.get("url", ""),
                "score": top_article.get("score", 0),
            },
            "articles": [
                {
                    "title": a.get("title", ""),
                    "url": a.get("url", ""),
                    "score": a.get("score", 0),
                }
                for a in sorted(articles, key=lambda x: x.get("score", 0), reverse=True)[:5]
            ],
        }
    
    return summary


def extract_trending_topics(articles: List[Dict[str, Any]], top_n: int = 15) -> List[Dict[str, Any]]:
    """提取热门话题/关键词"""
    # 定义技术关键词
    tech_keywords = {
        "AI": ["ai", "artificial intelligence", "machine learning", "deep learning", "neural network", "llm", "gpt", "chatgpt", "claude", "gemini", "openai", "anthropic"],
        "Programming": ["python", "javascript", "typescript", "rust", "go", "programming", "coding", "developer", "software", "github", "open source"],
        "Web": ["web", "frontend", "backend", "api", "react", "vue", "angular", "node.js", "cloud", "serverless"],
        "Data": ["data", "database", "sql", "nosql", "analytics", "big data", "data science"],
        "Security": ["security", "privacy", "encryption", "vulnerability", "hack", "cybersecurity"],
        "Mobile": ["mobile", "ios", "android", "app", "flutter", "react native"],
        "DevOps": ["devops", "docker", "kubernetes", "k8s", "ci/cd", "deployment", "infrastructure"],
        "Hardware": ["hardware", "gpu", "cpu", "chip", "semiconductor", "nvidia", "intel", "amd"],
    }
    
    topic_scores = defaultdict(lambda: {"count": 0, "total_score": 0, "articles": []})
    
    for article in articles:
        title_lower = article.get("title", "").lower()
        score = article.get("score", 0)
        
        for topic, keywords in tech_keywords.items():
            for keyword in keywords:
                if keyword in title_lower:
                    topic_scores[topic]["count"] += 1
                    topic_scores[topic]["total_score"] += score
                    if len(topic_scores[topic]["articles"]) < 3:
                        topic_scores[topic]["articles"].append({
                            "title": article.get("title", ""),
                            "url": article.get("url", ""),
                            "score": score,
                        })
                    break
    
    # 转换为列表并排序
    topics = [
        {
            "topic": topic,
            "count": data["count"],
            "total_score": data["total_score"],
            "average_score": round(data["total_score"] / data["count"], 2) if data["count"] > 0 else 0,
            "sample_articles": data["articles"],
        }
        for topic, data in topic_scores.items()
    ]
    
    topics.sort(key=lambda x: x["total_score"], reverse=True)
    
    return topics[:top_n]


def get_top_discussions(articles: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    """获取讨论最多的文章"""
    sorted_by_comments = sorted(articles, key=lambda x: x.get("comments_count", 0), reverse=True)
    
    discussions = []
    for article in sorted_by_comments[:top_n]:
        if article.get("comments_count", 0) > 0:
            discussions.append({
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "comments_count": article.get("comments_count", 0),
                "score": article.get("score", 0),
                "category": article.get("category", "Other"),
            })
    
    return discussions


def analyze_sources(top_sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    """分析来源网站"""
    if not top_sources:
        return {}
    
    total_count = sum(s.get("count", 0) for s in top_sources)
    
    sources_with_percentage = []
    for source in top_sources:
        count = source.get("count", 0)
        percentage = (count / total_count * 100) if total_count > 0 else 0
        sources_with_percentage.append({
            **source,
            "percentage": round(percentage, 2),
        })
    
    return {
        "total_sources": len(top_sources),
        "top_sources": sources_with_percentage[:10],
        "diversity_index": round(len(top_sources) / total_count, 4) if total_count > 0 else 0,
    }


def generate_recommendations(articles: List[Dict[str, Any]], by_category: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    """生成阅读建议"""
    recommendations = []
    
    # 基于分类分布的建议
    ai_count = len(by_category.get("AI", []))
    if ai_count > len(articles) * 0.3:
        recommendations.append(f"今日 AI 相关内容较多（{ai_count} 篇），建议重点关注最新模型和技术进展。")
    
    # 基于热门程度的建议
    high_score_articles = [a for a in articles if a.get("score", 0) >= 100]
    if len(high_score_articles) >= 5:
        recommendations.append(f"今日有 {len(high_score_articles)} 篇高分文章，质量较高，值得深入阅读。")
    
    # 基于讨论热度的建议
    hot_discussions = [a for a in articles if a.get("comments_count", 0) >= 50]
    if hot_discussions:
        recommendations.append(f"有 {len(hot_discussions)} 篇文章讨论热烈，可以在评论区获取更多观点。")
    
    # 通用建议
    if not recommendations:
        recommendations.append("建议浏览各分类的热门文章，了解最新的技术动态。")
    
    return recommendations


def generate_markdown_report(summary: Dict[str, Any]) -> str:
    """生成 Markdown 格式的报告"""
    lines = []
    
    # 标题
    lines.append(f"# {summary['report_title']}")
    lines.append("")
    lines.append(f"**生成时间**: {summary['generated_at'][:19]}")
    lines.append("")
    lines.append(f"**数据来源**: [{summary['source_url']}]({summary['source_url']})")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 概览
    overview = summary.get("overview", {})
    lines.append("## 📊 数据概览")
    lines.append("")
    lines.append(f"- **文章总数**: {overview.get('total_articles', 0)}")
    lines.append(f"- **总热度**: {overview.get('total_score', 0)}")
    lines.append(f"- **总评论数**: {overview.get('total_comments', 0)}")
    lines.append(f"- **平均热度**: {overview.get('average_score', 0)}")
    lines.append("")
    
    # 分类统计
    categories = overview.get("categories", {})
    if categories:
        lines.append("### 分类分布")
        lines.append("")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- **{cat}**: {count} 篇")
        lines.append("")
    
    # 最高分文章
    top_article = overview.get("top_article", {})
    if top_article:
        lines.append("### 🏆 今日最热")
        lines.append("")
        lines.append(f"**[{top_article.get('title', '')}]({top_article.get('url', '')})**")
        lines.append(f"- 热度: {top_article.get('score', 0)}")
        lines.append("")
    
    # 热门话题
    lines.append("---")
    lines.append("")
    lines.append("## 🔥 热门话题")
    lines.append("")
    
    trending = summary.get("trending_topics", [])
    for topic in trending[:10]:
        lines.append(f"### {topic['topic']}")
        lines.append(f"- 文章数: {topic['count']} | 总热度: {topic['total_score']}")
        if topic.get("sample_articles"):
            lines.append("- 相关文章:")
            for article in topic["sample_articles"][:2]:
                lines.append(f"  - [{article['title'][:60]}...]({article['url']})")
        lines.append("")
    
    # 热门文章
    lines.append("---")
    lines.append("")
    lines.append("## 📰 热门文章 Top 10")
    lines.append("")
    
    highlights = summary.get("highlights", [])
    for item in highlights:
        lines.append(f"{item['rank']}. **[{item['title']}]({item['url']})**")
        lines.append(f"   - 热度: {item['score']} | 评论: {item['comments_count']} | 来源: {item['source_site']} | 分类: {item['category']}")
        lines.append("")
    
    # 分类详情
    lines.append("---")
    lines.append("")
    lines.append("## 📂 分类详情")
    lines.append("")
    
    by_category_summary = summary.get("by_category", {})
    for category, data in sorted(by_category_summary.items(), key=lambda x: x[1].get("count", 0), reverse=True):
        lines.append(f"### {category}")
        lines.append(f"- 文章数: {data.get('count', 0)} | 平均热度: {data.get('average_score', 0)}")
        if data.get("articles"):
            lines.append("- 热门文章:")
            for article in data["articles"][:3]:
                lines.append(f"  - [{article['title'][:50]}...]({article['url']}) (热度: {article['score']})")
        lines.append("")
    
    # 热门讨论
    discussions = summary.get("top_discussions", [])
    if discussions:
        lines.append("---")
        lines.append("")
        lines.append("## 💬 热门讨论")
        lines.append("")
        for item in discussions:
            lines.append(f"- **[{item['title']}]({item['url']})** - {item['comments_count']} 条评论")
        lines.append("")
    
    # 阅读建议
    recommendations = summary.get("recommendations", [])
    if recommendations:
        lines.append("---")
        lines.append("")
        lines.append("## 💡 阅读建议")
        lines.append("")
        for rec in recommendations:
            lines.append(f"- {rec}")
        lines.append("")
    
    # 页脚
    lines.append("---")
    lines.append("")
    lines.append("*本报告由 HN Crawler Skill 自动生成*")
    
    return "\n".join(lines)


def save_summary(summary: Dict[str, Any], output_dir: str, source_file: str = None) -> Path:
    """保存总结报告"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存 JSON 格式
    json_filename = f"summary_{timestamp}.json"
    json_path = output_path / json_filename
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"[Summarize] JSON 报告已保存到: {json_path}")
    
    # 保存 Markdown 格式
    md_filename = f"summary_{timestamp}.md"
    md_path = output_path / md_filename
    
    markdown_content = generate_markdown_report(summary)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"[Summarize] Markdown 报告已保存到: {md_path}")
    
    return md_path


def main():
    parser = argparse.ArgumentParser(
        description="生成资讯总结报告"
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="输入 JSON 文件路径（默认从 data/organized/ 目录查找最新文件）"
    )
    parser.add_argument(
        "--output-dir",
        default=os.getenv("OUTPUT_DIR", DEFAULT_OUTPUT_DIR),
        help=f"输出目录 (默认: {DEFAULT_OUTPUT_DIR})"
    )
    
    args = parser.parse_args()
    
    try:
        # 确定输入文件
        if args.input_file:
            input_path = Path(args.input_file)
        else:
            # 查找最新的整理后 JSON 文件
            organized_dir = Path("data/organized")
            if organized_dir.exists():
                json_files = sorted(organized_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
                if json_files:
                    input_path = json_files[0]
                    print(f"[Summarize] 使用最新的整理数据: {input_path}")
                else:
                    print("[Summarize] 错误: 未找到整理后的数据文件", file=sys.stderr)
                    return 1
            else:
                print("[Summarize] 错误: data/organized/ 目录不存在", file=sys.stderr)
                return 1
        
        # 读取数据
        print(f"[Summarize] 正在读取: {input_path}")
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        articles = data.get("articles", [])
        
        if not articles:
            print("[Summarize] 错误: 没有找到文章数据", file=sys.stderr)
            return 1
        
        print(f"[Summarize] 正在生成总结报告...")
        
        # 生成总结
        summary = generate_summary(data)
        
        # 保存报告
        output_path = save_summary(summary, args.output_dir, input_path)
        
        print(f"[Summarize] 完成！")
        print(f"[Summarize] - 报告文件: {output_path}")
        print(f"OUTPUT_FILE:{output_path}")
        
        return 0
        
    except Exception as e:
        print(f"[Summarize] 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
