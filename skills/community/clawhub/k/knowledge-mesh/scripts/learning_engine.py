#!/usr/bin/env python3
"""
knowledge-mesh 自学习搜索引擎模块

基于用户反馈和搜索行为自动调整搜索排序权重，
提供主动建议和搜索分析统计。

用法:
    python3 learning_engine.py --action record-feedback --data '{"result_id":"SR...","source":"github","rating":"helpful"}'
    python3 learning_engine.py --action record-click --data '{"result_id":"SR...","source":"github"}'
    python3 learning_engine.py --action record-query --data '{"query":"python async","sources":["github","stackoverflow"],"result_counts":{"github":5,"stackoverflow":8}}'
    python3 learning_engine.py --action boost-weights
    python3 learning_engine.py --action suggest
    python3 learning_engine.py --action stats
"""

import json
import math
import os
import sys
from collections import Counter
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from utils import (
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    write_json_file,
)


# ============================================================
# 常量
# ============================================================

# 学习数据文件
LEARNING_DATA_FILE = "learning.json"

# 反馈评级定义
VALID_RATINGS = {"relevant", "irrelevant", "helpful"}

# 评级到分数的映射（用于权重计算）
RATING_SCORES = {
    "helpful": 1.0,
    "relevant": 0.5,
    "irrelevant": -0.5,
}

# 默认知识源权重
DEFAULT_SOURCE_WEIGHTS = {
    "github": 1.0,
    "stackoverflow": 1.0,
    "discord": 1.0,
    "confluence": 1.0,
    "notion": 1.0,
    "slack": 1.0,
    "baidu": 1.0,
    "obsidian": 1.0,
}

# 权重调整范围
MIN_WEIGHT = 0.1
MAX_WEIGHT = 3.0

# 权重调整学习率
LEARNING_RATE = 0.1

# 建议生成所需的最小查询记录数
MIN_QUERIES_FOR_SUGGEST = 3

# 建议生成所需的最小反馈记录数
MIN_FEEDBACK_FOR_SUGGEST = 2

# 主题提取时的最小出现次数
MIN_TOPIC_COUNT = 2


# ============================================================
# 学习数据持久化
# ============================================================

def _get_learning_file() -> str:
    """获取学习数据文件路径。

    Returns:
        学习数据文件的绝对路径。
    """
    return get_data_file(LEARNING_DATA_FILE)


def _load_learning_data() -> Dict[str, Any]:
    """加载学习数据。

    Returns:
        学习数据字典，包含 query_log, feedback, click_log, source_weights。
    """
    data = read_json_file(_get_learning_file())
    if not isinstance(data, dict):
        data = {}

    # 确保必要字段存在
    if "query_log" not in data:
        data["query_log"] = []
    if "feedback" not in data:
        data["feedback"] = []
    if "click_log" not in data:
        data["click_log"] = []
    if "source_weights" not in data:
        data["source_weights"] = dict(DEFAULT_SOURCE_WEIGHTS)

    return data


def _save_learning_data(data: Dict[str, Any]) -> None:
    """保存学习数据。

    Args:
        data: 学习数据字典。
    """
    write_json_file(_get_learning_file(), data)


# ============================================================
# 查询日志分析辅助函数
# ============================================================

def _extract_topics(query_log: List[Dict[str, Any]], top_n: int = 10) -> List[Tuple[str, int]]:
    """从查询日志中提取热门主题词。

    对所有查询进行简单分词，统计出现频率最高的词。

    Args:
        query_log: 查询记录列表。
        top_n: 返回前 N 个主题。

    Returns:
        (主题词, 出现次数) 元组列表，按次数降序排列。
    """
    word_counter = Counter()
    # 常见停用词
    stop_words = {
        "the", "a", "an", "is", "are", "in", "on", "for", "to", "of",
        "and", "or", "not", "with", "how", "what", "why", "when", "where",
        "的", "了", "在", "是", "我", "有", "和", "不", "怎么", "如何",
    }

    for entry in query_log:
        query = entry.get("query", "")
        if not query:
            continue
        # 简单分词：按空格和常见分隔符分割
        import re
        tokens = re.findall(r"[a-zA-Z0-9_]+|[\u4e00-\u9fff]+", query.lower())
        for token in tokens:
            if token not in stop_words and len(token) >= 2:
                word_counter[token] += 1

    # 过滤出至少出现 MIN_TOPIC_COUNT 次的词
    filtered = [(word, count) for word, count in word_counter.most_common(top_n * 2)
                if count >= MIN_TOPIC_COUNT]

    return filtered[:top_n]


def _calculate_source_adoption_rate(feedback: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """计算各知识源的结果采纳率。

    采纳率 = helpful 评价数 / 总评价数。

    Args:
        feedback: 反馈记录列表。

    Returns:
        {source: {total, helpful, relevant, irrelevant, adoption_rate}} 映射。
    """
    source_stats = {}

    for entry in feedback:
        source = entry.get("source", "unknown")
        rating = entry.get("rating", "")

        if source not in source_stats:
            source_stats[source] = {
                "total": 0,
                "helpful": 0,
                "relevant": 0,
                "irrelevant": 0,
            }

        source_stats[source]["total"] += 1
        if rating in source_stats[source]:
            source_stats[source][rating] += 1

    # 计算采纳率
    for source, stats in source_stats.items():
        total = stats["total"]
        if total > 0:
            stats["adoption_rate"] = round(stats["helpful"] / total, 4)
        else:
            stats["adoption_rate"] = 0.0

    return source_stats


def _get_recent_queries(query_log: List[Dict[str, Any]], days: int = 30) -> List[Dict[str, Any]]:
    """获取最近 N 天的查询记录。

    Args:
        query_log: 查询记录列表。
        days: 天数范围。

    Returns:
        最近 N 天内的查询记录列表。
    """
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S")
    recent = []
    for entry in query_log:
        ts = entry.get("timestamp", "")
        if ts >= cutoff:
            recent.append(entry)
    return recent


def _compute_optimal_weights(feedback: List[Dict[str, Any]], current_weights: Dict[str, float]) -> Dict[str, float]:
    """根据反馈历史计算最优权重。

    评分高的知识源权重提升，评分低的权重降低。

    Args:
        feedback: 反馈记录列表。
        current_weights: 当前权重。

    Returns:
        更新后的权重字典。
    """
    new_weights = dict(current_weights)

    # 统计各源的反馈分数
    source_scores = {}
    source_counts = {}

    for entry in feedback:
        source = entry.get("source", "")
        rating = entry.get("rating", "")
        if not source or rating not in RATING_SCORES:
            continue

        if source not in source_scores:
            source_scores[source] = 0.0
            source_counts[source] = 0

        source_scores[source] += RATING_SCORES[rating]
        source_counts[source] += 1

    # 计算平均分并调整权重
    for source, total_score in source_scores.items():
        count = source_counts.get(source, 1)
        avg_score = total_score / max(count, 1)

        # 使用学习率渐进式调整
        base_weight = current_weights.get(source, 1.0)
        adjustment = LEARNING_RATE * avg_score
        new_weight = base_weight + adjustment

        # 限制在合理范围内
        new_weight = max(MIN_WEIGHT, min(MAX_WEIGHT, new_weight))
        new_weights[source] = round(new_weight, 4)

    return new_weights


# ============================================================
# 操作实现
# ============================================================

def action_record_feedback(data: Dict[str, Any]) -> None:
    """记录用户对搜索结果的反馈。

    反馈类型包括：relevant（相关）、irrelevant（不相关）、helpful（有帮助）。

    Args:
        data: 包含 result_id、source、rating 的字典。
    """
    result_id = data.get("result_id", "").strip()
    source = data.get("source", "").strip()
    rating = data.get("rating", "").strip().lower()

    if not result_id:
        output_error("请提供搜索结果ID（result_id）", code="VALIDATION_ERROR")
        return
    if not source:
        output_error("请提供知识源名称（source）", code="VALIDATION_ERROR")
        return
    if rating not in VALID_RATINGS:
        valid = "、".join(VALID_RATINGS)
        output_error(f"无效的评级: {rating}，支持: {valid}", code="VALIDATION_ERROR")
        return

    learning_data = _load_learning_data()

    feedback_entry = {
        "id": generate_id("FB"),
        "result_id": result_id,
        "source": source,
        "rating": rating,
        "timestamp": now_iso(),
    }

    learning_data["feedback"].append(feedback_entry)
    _save_learning_data(learning_data)

    output_success({
        "message": f"已记录反馈: {source} 结果 {result_id} 评级为 {rating}",
        "feedback_id": feedback_entry["id"],
        "total_feedback": len(learning_data["feedback"]),
    })


def action_record_click(data: Dict[str, Any]) -> None:
    """记录用户点击/使用搜索结果的行为（隐式相关性信号）。

    Args:
        data: 包含 result_id、source 的字典，可选 query。
    """
    result_id = data.get("result_id", "").strip()
    source = data.get("source", "").strip()
    query = data.get("query", "").strip()

    if not result_id:
        output_error("请提供搜索结果ID（result_id）", code="VALIDATION_ERROR")
        return
    if not source:
        output_error("请提供知识源名称（source）", code="VALIDATION_ERROR")
        return

    learning_data = _load_learning_data()

    click_entry = {
        "id": generate_id("CK"),
        "result_id": result_id,
        "source": source,
        "query": query,
        "timestamp": now_iso(),
    }

    learning_data["click_log"].append(click_entry)
    _save_learning_data(learning_data)

    output_success({
        "message": f"已记录点击: {source} 结果 {result_id}",
        "click_id": click_entry["id"],
        "total_clicks": len(learning_data["click_log"]),
    })


def action_record_query(data: Dict[str, Any]) -> None:
    """记录搜索查询及各知识源的结果数量。

    用于分析搜索行为和知识源覆盖率。

    Args:
        data: 包含 query、sources、result_counts 的字典。
    """
    query = data.get("query", "").strip()
    sources = data.get("sources", [])
    result_counts = data.get("result_counts", {})

    if not query:
        output_error("请提供搜索查询（query）", code="VALIDATION_ERROR")
        return

    learning_data = _load_learning_data()

    query_entry = {
        "id": generate_id("QR"),
        "query": query,
        "sources": sources,
        "result_counts": result_counts,
        "total_results": sum(result_counts.values()) if result_counts else 0,
        "timestamp": now_iso(),
    }

    learning_data["query_log"].append(query_entry)
    _save_learning_data(learning_data)

    output_success({
        "message": f"已记录查询: '{query}'，共 {query_entry['total_results']} 条结果",
        "query_id": query_entry["id"],
        "total_queries": len(learning_data["query_log"]),
    })


def action_boost_weights(data: Optional[Dict[str, Any]] = None) -> None:
    """根据累积反馈调整知识源可靠性权重。

    helpful 评价多的知识源权重提升，irrelevant 评价多的权重降低。
    """
    learning_data = _load_learning_data()
    feedback = learning_data.get("feedback", [])

    if len(feedback) < MIN_FEEDBACK_FOR_SUGGEST:
        output_error(
            f"反馈数据不足（当前 {len(feedback)} 条，需要至少 {MIN_FEEDBACK_FOR_SUGGEST} 条），无法调整权重",
            code="INSUFFICIENT_DATA",
        )
        return

    old_weights = dict(learning_data.get("source_weights", DEFAULT_SOURCE_WEIGHTS))

    # 计算新权重
    new_weights = _compute_optimal_weights(feedback, old_weights)
    learning_data["source_weights"] = new_weights

    # 记录权重变更历史
    changes = []
    for source in set(list(old_weights.keys()) + list(new_weights.keys())):
        old_w = old_weights.get(source, 1.0)
        new_w = new_weights.get(source, 1.0)
        if abs(old_w - new_w) > 0.001:
            direction = "提升" if new_w > old_w else "降低"
            changes.append({
                "source": source,
                "old_weight": old_w,
                "new_weight": new_w,
                "direction": direction,
            })

    _save_learning_data(learning_data)

    output_success({
        "message": f"权重调整完成，基于 {len(feedback)} 条反馈",
        "weights": new_weights,
        "changes": changes,
        "feedback_count": len(feedback),
    })


def action_suggest(data: Optional[Dict[str, Any]] = None) -> None:
    """基于搜索历史和反馈生成主动建议。

    建议类型包括：
    - 高频主题推荐关注
    - 高采纳率知识源推荐
    - 搜索习惯优化建议
    """
    learning_data = _load_learning_data()
    query_log = learning_data.get("query_log", [])
    feedback = learning_data.get("feedback", [])
    click_log = learning_data.get("click_log", [])
    source_weights = learning_data.get("source_weights", DEFAULT_SOURCE_WEIGHTS)

    suggestions = []

    # 建议1: 高频主题推荐
    if len(query_log) >= MIN_QUERIES_FOR_SUGGEST:
        topics = _extract_topics(query_log, top_n=5)
        if topics:
            top_topic = topics[0]
            topic_name = top_topic[0]
            topic_count = top_topic[1]

            # 根据主题内容给出不同建议
            suggestion_text = f"您经常搜索 {topic_name} 相关内容（共 {topic_count} 次），"

            # 检查是否为技术框架/工具
            tech_suggestions = {
                "react": "建议关注 React GitHub Discussions 和官方博客",
                "vue": "建议关注 Vue.js RFC 和 GitHub Discussions",
                "python": "建议关注 Python PEP 提案和 PyPI 新包发布",
                "fastapi": "建议关注 FastAPI GitHub Releases 和文档更新",
                "kubernetes": "建议关注 Kubernetes Enhancement Proposals (KEPs)",
                "docker": "建议关注 Docker 官方博客和 GitHub Releases",
                "typescript": "建议关注 TypeScript GitHub Discussions",
                "golang": "建议关注 Go 官方博客和 Release Notes",
                "rust": "建议关注 Rust RFC 和 This Week in Rust",
                "java": "建议关注 OpenJDK 和 Spring 官方博客",
            }

            topic_lower = topic_name.lower()
            if topic_lower in tech_suggestions:
                suggestion_text += tech_suggestions[topic_lower]
            else:
                suggestion_text += f"建议在搜索时尝试添加更具体的子主题以获得更精确的结果"

            suggestions.append({
                "type": "topic_recommendation",
                "text": suggestion_text,
                "topic": topic_name,
                "frequency": topic_count,
            })

    # 建议2: 高采纳率知识源推荐
    if len(feedback) >= MIN_FEEDBACK_FOR_SUGGEST:
        adoption_stats = _calculate_source_adoption_rate(feedback)

        # 找到采纳率最高的知识源
        best_source = None
        best_rate = 0.0
        for source, stats in adoption_stats.items():
            if stats["total"] >= 2 and stats["adoption_rate"] > best_rate:
                best_rate = stats["adoption_rate"]
                best_source = source

        if best_source and best_rate > 0.3:
            rate_pct = int(best_rate * 100)
            source_display = {
                "github": "GitHub",
                "stackoverflow": "Stack Overflow",
                "discord": "Discord",
                "confluence": "Confluence",
                "notion": "Notion",
                "slack": "Slack",
                "baidu": "百度搜索",
                "obsidian": "Obsidian",
            }.get(best_source, best_source)

            suggestions.append({
                "type": "source_recommendation",
                "text": f"{source_display} 的结果采纳率最高({rate_pct}%)，建议优先查看",
                "source": best_source,
                "adoption_rate": best_rate,
            })

    # 建议3: 搜索习惯优化
    if len(query_log) >= MIN_QUERIES_FOR_SUGGEST:
        recent_queries = _get_recent_queries(query_log, days=7)
        if recent_queries:
            # 检查是否有重复查询
            query_texts = [q.get("query", "") for q in recent_queries]
            query_counts = Counter(query_texts)
            repeated = [(q, c) for q, c in query_counts.items() if c >= 2]

            if repeated:
                most_repeated = max(repeated, key=lambda x: x[1])
                suggestions.append({
                    "type": "search_optimization",
                    "text": f"您最近 7 天内重复搜索了 '{most_repeated[0]}' {most_repeated[1]} 次，建议使用主题监控功能自动跟踪更新",
                    "repeated_query": most_repeated[0],
                    "repeat_count": most_repeated[1],
                })

        # 检查平均结果数
        result_totals = [q.get("total_results", 0) for q in recent_queries]
        if result_totals:
            avg_results = sum(result_totals) / len(result_totals)
            if avg_results < 3:
                suggestions.append({
                    "type": "search_optimization",
                    "text": "您最近的搜索平均结果较少，建议尝试使用更通用的关键词或启用更多知识源",
                    "avg_results": round(avg_results, 1),
                })

    # 建议4: 点击行为分析
    if len(click_log) >= 3:
        # 统计各源的点击分布
        click_sources = Counter()
        for click in click_log:
            click_sources[click.get("source", "")] += 1

        total_clicks = sum(click_sources.values())
        if total_clicks > 0:
            # 找到最常点击的知识源
            top_click_source, top_click_count = click_sources.most_common(1)[0]
            click_pct = int((top_click_count / total_clicks) * 100)
            if click_pct >= 60:
                source_display = {
                    "github": "GitHub",
                    "stackoverflow": "Stack Overflow",
                    "discord": "Discord",
                    "confluence": "Confluence",
                    "notion": "Notion",
                    "slack": "Slack",
                    "baidu": "百度搜索",
                    "obsidian": "Obsidian",
                }.get(top_click_source, top_click_source)

                suggestions.append({
                    "type": "usage_pattern",
                    "text": f"您 {click_pct}% 的点击来自 {source_display}，该知识源的排序权重已自动提升",
                    "source": top_click_source,
                    "click_percentage": click_pct,
                })

    if not suggestions:
        suggestions.append({
            "type": "info",
            "text": "当前搜索数据不足，继续使用后将为您生成个性化建议",
        })

    output_success({
        "suggestions": suggestions,
        "total_suggestions": len(suggestions),
        "data_summary": {
            "total_queries": len(query_log),
            "total_feedback": len(feedback),
            "total_clicks": len(click_log),
        },
    })


def action_stats(data: Optional[Dict[str, Any]] = None) -> None:
    """搜索分析统计：最常搜索的主题、最佳表现知识源、平均结果质量。"""
    learning_data = _load_learning_data()
    query_log = learning_data.get("query_log", [])
    feedback = learning_data.get("feedback", [])
    click_log = learning_data.get("click_log", [])
    source_weights = learning_data.get("source_weights", DEFAULT_SOURCE_WEIGHTS)

    # 基本统计
    total_queries = len(query_log)
    total_feedback = len(feedback)
    total_clicks = len(click_log)

    # 热门主题
    topics = _extract_topics(query_log, top_n=10)
    top_topics = [{"topic": t, "count": c} for t, c in topics]

    # 知识源结果统计
    source_result_stats = {}
    for entry in query_log:
        result_counts = entry.get("result_counts", {})
        for source, count in result_counts.items():
            if source not in source_result_stats:
                source_result_stats[source] = {"total_results": 0, "query_count": 0}
            source_result_stats[source]["total_results"] += count
            source_result_stats[source]["query_count"] += 1

    # 计算各源平均结果数
    for source, stats in source_result_stats.items():
        qc = stats["query_count"]
        stats["avg_results"] = round(stats["total_results"] / max(qc, 1), 1)

    # 知识源采纳率
    adoption_stats = _calculate_source_adoption_rate(feedback)

    # 最佳表现知识源
    best_source = None
    best_score = -1.0
    for source, stats in adoption_stats.items():
        score = stats["adoption_rate"] * stats["total"]  # 综合采纳率和样本量
        if score > best_score:
            best_score = score
            best_source = source

    # 平均结果质量（基于反馈）
    quality_scores = []
    for entry in feedback:
        rating = entry.get("rating", "")
        if rating in RATING_SCORES:
            quality_scores.append(RATING_SCORES[rating])

    avg_quality = round(sum(quality_scores) / max(len(quality_scores), 1), 3)

    # 时间分布统计
    daily_queries = Counter()
    for entry in query_log:
        ts = entry.get("timestamp", "")
        if ts:
            day = ts[:10]  # 截取日期部分 YYYY-MM-DD
            daily_queries[day] += 1

    # 最近7天统计
    recent_daily = []
    today = datetime.utcnow().date()
    for i in range(7):
        day = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        recent_daily.append({
            "date": day,
            "queries": daily_queries.get(day, 0),
        })

    output_success({
        "overview": {
            "total_queries": total_queries,
            "total_feedback": total_feedback,
            "total_clicks": total_clicks,
            "avg_result_quality": avg_quality,
        },
        "top_topics": top_topics,
        "source_performance": {
            "result_stats": source_result_stats,
            "adoption_stats": adoption_stats,
            "best_source": best_source,
        },
        "current_weights": source_weights,
        "recent_activity": recent_daily,
    })


# ============================================================
# 公开 API（供其他模块调用）
# ============================================================

def get_source_weights() -> Dict[str, float]:
    """获取当前知识源权重。

    供 result_ranker 等模块调用，用于排序调整。

    Returns:
        知识源权重字典。
    """
    learning_data = _load_learning_data()
    return learning_data.get("source_weights", dict(DEFAULT_SOURCE_WEIGHTS))


def record_query_data(query: str, sources: List[str], result_counts: Dict[str, int]) -> None:
    """记录查询数据（供 source_searcher 调用）。

    Args:
        query: 搜索查询。
        sources: 搜索的知识源列表。
        result_counts: 各知识源的结果数量。
    """
    learning_data = _load_learning_data()

    query_entry = {
        "id": generate_id("QR"),
        "query": query,
        "sources": sources,
        "result_counts": result_counts,
        "total_results": sum(result_counts.values()) if result_counts else 0,
        "timestamp": now_iso(),
    }

    learning_data["query_log"].append(query_entry)
    _save_learning_data(learning_data)


def record_feedback_data(result_id: str, source: str, rating: str) -> None:
    """记录反馈数据（供 result_ranker 调用）。

    Args:
        result_id: 搜索结果 ID。
        source: 知识源名称。
        rating: 评级（relevant/irrelevant/helpful）。
    """
    if rating not in VALID_RATINGS:
        return

    learning_data = _load_learning_data()

    feedback_entry = {
        "id": generate_id("FB"),
        "result_id": result_id,
        "source": source,
        "rating": rating,
        "timestamp": now_iso(),
    }

    learning_data["feedback"].append(feedback_entry)
    _save_learning_data(learning_data)


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("knowledge-mesh 自学习搜索引擎")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "record-feedback": lambda: action_record_feedback(data or {}),
        "record-click": lambda: action_record_click(data or {}),
        "record-query": lambda: action_record_query(data or {}),
        "boost-weights": lambda: action_boost_weights(data),
        "suggest": lambda: action_suggest(data),
        "stats": lambda: action_stats(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
