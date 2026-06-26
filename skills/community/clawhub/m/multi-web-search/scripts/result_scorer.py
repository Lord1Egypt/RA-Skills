#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
result_scorer.py - 结果评分与排序工具

根据来源可信度、新鲜度、相关性对搜索结果进行评分和排序。

Usage:
    from result_scorer import score_and_rank_results

    scored = score_and_rank_results(results, query="python tutorial")
"""
import re
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# 来源可信度权重（0-100）
SOURCE_CREDIBILITY = {
    # 学术/官方来源 - 高权重
    "arxiv": 95,
    "wikipedia": 90,
    "github": 88,
    "stackoverflow": 85,
    "medium": 75,
    "dev.to": 72,
    "reddit": 70,
    "hackernews": 73,

    # 主流搜索引擎
    "google": 82,
    "bing": 78,
    "duckduckgo": 80,
    "brave": 79,

    # 国内来源
    "baidu": 65,
    "sogou": 60,
    "zhihu": 68,

    # 其他
    "default": 60
}

# 年龄衰减因子（每增加一天降低的分数）
DAILY_DECAY = 0.5


def get_domain_credibility(url: str) -> int:
    """根据 URL 域名获取可信度分数"""
    if not url:
        return SOURCE_CREDIBILITY["default"]

    # 提取域名
    domain_match = re.search(r'https?://([^/]+)', url)
    if not domain_match:
        return SOURCE_CREDIBILITY["default"]

    domain = domain_match.group(1).lower()

    # 检查已知高权重域名
    for source, score in SOURCE_CREDIBILITY.items():
        if source != "default" and source in domain:
            return score

    # 检查顶级域
    tld = domain.split('.')[-1]
    if tld in ("edu", "gov", "org"):
        return 75
    elif tld == "com":
        return 60

    return SOURCE_CREDIBILITY["default"]


def calculate_recency_score(published_date: Optional[str]) -> float:
    """
    计算新鲜度分数。

    Args:
        published_date: ISO 格式日期字符串或 YYYY-MM-DD

    Returns:
        0-100 的分数，越新的日期分数越高
    """
    if not published_date:
        return 50  # 无日期信息给中等分数

    try:
        # 尝试解析日期
        if isinstance(published_date, str):
            # 处理 ISO 格式
            if 'T' in published_date:
                pub_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
            else:
                pub_date = datetime.strptime(published_date[:10], "%Y-%m-%d")

        days_old = (datetime.now() - pub_date.replace(tzinfo=None)).days

        # 评分：7天内 100分，之后每天衰减
        if days_old <= 7:
            return 100
        elif days_old <= 30:
            return 90 - (days_old - 7) * 0.5
        elif days_old <= 90:
            return 80 - (days_old - 30) * 0.3
        elif days_old <= 365:
            return 70 - (days_old - 90) * 0.1
        else:
            return max(30, 60 - (days_old - 365) * 0.02)

    except (ValueError, TypeError):
        return 50  # 解析失败给中等分数


def calculate_relevance_score(title: str, snippet: str, query: str) -> float:
    """
    计算相关性分数。

    基于查询词在标题和摘要中出现的次数和位置。

    Args:
        title: 结果标题
        snippet: 结果摘要
        query: 搜索查询

    Returns:
        0-100 的分数
    """
    if not query:
        return 70  # 无查询给中等分数

    query_terms = query.lower().split()
    title_lower = title.lower()
    snippet_lower = snippet.lower()

    score = 50  # 基础分数

    for term in query_terms:
        # 标题中匹配（更高权重）
        title_matches = len(re.findall(r'\b' + re.escape(term) + r'\b', title_lower))
        score += title_matches * 15

        # 摘要中匹配
        snippet_matches = len(re.findall(r'\b' + re.escape(term) + r'\b', snippet_lower))
        score += snippet_matches * 5

        # 精确短语匹配
        if query.lower() in title_lower:
            score += 10
        if query.lower() in snippet_lower:
            score += 5

    return min(100, score)


def score_result(result: Dict, query: str = "", weight_crecibility: float = 0.3,
                 weight_recency: float = 0.3, weight_relevance: float = 0.4) -> float:
    """
    对单个结果进行综合评分。

    Args:
        result: 结果字典
        query: 搜索查询
        weight_crecibility: 可信度权重
        weight_recency: 新鲜度权重
        weight_relevance: 相关性权重

    Returns:
        0-100 的综合分数
    """
    # 获取来源可信度
    source = result.get("source", "").lower()
    if source in SOURCE_CREDIBILITY:
        cred_score = SOURCE_CREDIBILITY[source]
    else:
        # 根据 URL 域名判断
        cred_score = get_domain_credibility(result.get("url", ""))

    # 新鲜度分数
    recency_score = calculate_recency_score(result.get("published_date"))

    # 相关性分数
    relevance_score = calculate_relevance_score(
        result.get("title", ""),
        result.get("snippet", ""),
        query
    )

    # 加权求和
    total_score = (
        cred_score * weight_crecibility +
        recency_score * weight_recency +
        relevance_score * weight_relevance
    )

    return round(total_score, 2)


def score_and_rank_results(
    results: List[Dict],
    query: str = "",
    weight_crecibility: float = 0.3,
    weight_recency: float = 0.3,
    weight_relevance: float = 0.4,
    top_n: Optional[int] = None
) -> List[Dict]:
    """
    对结果进行评分和排序。

    Args:
        results: 结果列表
        query: 搜索查询
        weight_crecibility: 可信度权重
        weight_recency: 新鲜度权重
        weight_relevance: 相关性权重
        top_n: 返回前 N 个结果（None = 返回全部）

    Returns:
        按分数排序的结果列表，每项包含 _score 字段
    """
    # 为每个结果计算分数
    scored_results = []
    for r in results:
        score = score_result(
            r, query,
            weight_crecibility, weight_recency, weight_relevance
        )
        r_copy = r.copy()
        r_copy["_score"] = score
        scored_results.append(r_copy)

    # 按分数降序排序
    scored_results.sort(key=lambda x: x["_score"], reverse=True)

    # 返回前 N 个
    if top_n is not None:
        return scored_results[:top_n]

    return scored_results


def get_score_breakdown(result: Dict, query: str = "") -> Dict[str, float]:
    """
    获取结果分数的详细分解。

    Returns:
        包含各维度分数的字典
    """
    source = result.get("source", "").lower()
    if source in SOURCE_CREDIBILITY:
        cred_score = SOURCE_CREDIBILITY[source]
    else:
        cred_score = get_domain_credibility(result.get("url", ""))

    recency_score = calculate_recency_score(result.get("published_date"))
    relevance_score = calculate_relevance_score(
        result.get("title", ""),
        result.get("snippet", ""),
        query
    )

    return {
        "credibility": cred_score,
        "recency": recency_score,
        "relevance": relevance_score,
        "total": score_result(result, query)
    }


if __name__ == "__main__":
    # 测试
    print("=== 结果评分测试 ===\n")

    test_results = [
        {
            "title": "Python Tutorial for Beginners",
            "url": "https://github.com/python/tutorial",
            "snippet": "Complete Python guide...",
            "published_date": "2026-04-20",
            "source": "github"
        },
        {
            "title": "Python Basics",
            "url": "https://stackoverflow.com/python-basics",
            "snippet": "Python programming basics...",
            "published_date": "2025-01-15",
            "source": "stackoverflow"
        },
        {
            "title": "Learn Python",
            "url": "https://medium.com/learn-python",
            "snippet": "How to learn Python...",
            "published_date": None,
            "source": "medium"
        }
    ]

    query = "python tutorial"

    print(f"查询: {query}\n")
    print("评分详情:")
    for r in test_results:
        breakdown = get_score_breakdown(r, query)
        print(f"\n  {r['title']}")
        print(f"    可信度: {breakdown['credibility']}")
        print(f"    新鲜度: {breakdown['recency']}")
        print(f"    相关性: {breakdown['relevance']}")
        print(f"    总分: {breakdown['total']}")

    print("\n\n排序后的结果:")
    ranked = score_and_rank_results(test_results, query)
    for i, r in enumerate(ranked, 1):
        print(f"{i}. [{r['_score']}] {r['title']} ({r['source']})")