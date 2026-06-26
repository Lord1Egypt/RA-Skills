#!/usr/bin/env python3
"""
knowledge-mesh 搜索结果排序与合成模块

对跨平台搜索结果进行 TF-IDF 相关性评分、权威性评分、
去重合并和智能摘要生成。

用法:
    python3 result_ranker.py --action rank --data '{"query":"...", "results":[...]}'
    python3 result_ranker.py --action dedup --data '{"results":[...]}'
    python3 result_ranker.py --action synthesize --data '{"query":"...", "results":[...]}'
    python3 result_ranker.py --action summarize --data '{"results":[...]}'
"""

import math
import re
import sys
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from utils import (
    check_subscription,
    clean_html,
    days_ago,
    format_source_badge,
    highlight_match,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    require_paid_feature,
    truncate_text,
    SOURCE_DISPLAY_NAMES,
)


# ============================================================
# 常量
# ============================================================

# 各知识源的可信度系数
SOURCE_RELIABILITY = {
    "github": 0.9,
    "stackoverflow": 0.95,
    "discord": 0.5,
    "confluence": 0.85,
    "notion": 0.7,
    "slack": 0.4,
    "baidu": 0.6,
    "obsidian": 0.8,
}

# 时间衰减半衰期（天）
RECENCY_HALF_LIFE = 90

# Jaccard 相似度去重阈值
DEDUP_THRESHOLD = 0.7

# 停用词列表（常见中英文停用词）
STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "can", "shall",
    "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above",
    "below", "between", "and", "but", "or", "nor", "not", "so",
    "if", "then", "than", "too", "very", "just", "about", "up",
    "out", "no", "it", "its", "this", "that", "these", "those",
    "i", "me", "my", "we", "our", "you", "your", "he", "she",
    "him", "her", "they", "them", "their", "what", "which", "who",
    "how", "when", "where", "why", "all", "each", "every", "both",
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
    "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
    "你", "会", "着", "没有", "看", "好", "自己", "这", "他", "她",
    "吗", "什么", "怎么", "如何", "为什么", "哪个", "那个",
}


# ============================================================
# 文本处理
# ============================================================

def _tokenize(text: str) -> List[str]:
    """将文本分词为词语列表。

    使用简单的正则表达式分割，同时处理中英文。

    Args:
        text: 原始文本。

    Returns:
        小写词语列表。
    """
    if not text:
        return []
    # 英文按单词分割，中文按字符分割
    tokens = re.findall(r"[a-zA-Z0-9_]+|[\u4e00-\u9fff]", text.lower())
    return [t for t in tokens if t and t not in STOP_WORDS]


def _word_set(text: str) -> Set[str]:
    """提取文本的词语集合（去停用词）。

    Args:
        text: 原始文本。

    Returns:
        词语集合。
    """
    return set(_tokenize(text))


def _term_frequency(tokens: List[str]) -> Dict[str, float]:
    """计算词频（TF）。

    使用对数归一化 TF: 1 + log(count)。

    Args:
        tokens: 词语列表。

    Returns:
        词语到 TF 值的映射。
    """
    if not tokens:
        return {}
    counts = Counter(tokens)
    tf = {}
    for term, count in counts.items():
        tf[term] = 1 + math.log(count)
    return tf


def _inverse_document_frequency(
    term: str,
    doc_count: int,
    doc_freq: int,
) -> float:
    """计算逆文档频率（IDF）。

    IDF = log(N / (1 + df))

    Args:
        term: 词语。
        doc_count: 总文档数。
        doc_freq: 包含该词语的文档数。

    Returns:
        IDF 值。
    """
    if doc_count <= 0:
        return 0.0
    return math.log(doc_count / (1 + doc_freq))


def _build_corpus_idf(documents: List[List[str]]) -> Dict[str, float]:
    """构建语料库的 IDF 字典。

    Args:
        documents: 文档词语列表的列表。

    Returns:
        词语到 IDF 值的映射。
    """
    doc_count = len(documents)
    if doc_count == 0:
        return {}

    # 统计每个词出现在多少文档中
    df = Counter()
    for doc_tokens in documents:
        unique_terms = set(doc_tokens)
        for term in unique_terms:
            df[term] += 1

    idf = {}
    for term, freq in df.items():
        idf[term] = _inverse_document_frequency(term, doc_count, freq)

    return idf


# ============================================================
# 评分函数
# ============================================================

def _tfidf_relevance_score(
    query_tokens: List[str],
    doc_tokens: List[str],
    idf: Dict[str, float],
) -> float:
    """计算查询与文档的 TF-IDF 相关性分数。

    Args:
        query_tokens: 查询词语列表。
        doc_tokens: 文档词语列表。
        idf: IDF 字典。

    Returns:
        相关性分数（0.0 ~ 1.0）。
    """
    if not query_tokens or not doc_tokens:
        return 0.0

    doc_tf = _term_frequency(doc_tokens)
    score = 0.0

    for q_term in query_tokens:
        tf_val = doc_tf.get(q_term, 0.0)
        idf_val = idf.get(q_term, 0.0)
        score += tf_val * idf_val

    # 归一化
    max_possible = sum(idf.get(q, 0.0) for q in query_tokens)
    if max_possible > 0:
        score = score / max_possible

    return min(1.0, max(0.0, score))


def _get_learned_weight(source: str) -> float:
    """获取知识源的自学习权重。

    从 learning_engine 加载累积反馈计算出的权重，
    作为排序调整的乘数因子。

    Args:
        source: 知识源名称。

    Returns:
        权重乘数（默认 1.0）。
    """
    try:
        from learning_engine import get_source_weights
        weights = get_source_weights()
        return weights.get(source, 1.0)
    except (ImportError, Exception):
        return 1.0


def _authority_score(result: Dict[str, Any]) -> float:
    """计算结果的权威性分数。

    综合考虑：原始分数、来源可信度、时间衰减。

    Args:
        result: 搜索结果条目。

    Returns:
        权威性分数（0.0 ~ 1.0）。
    """
    # 原始分数（归一化到 0-1）
    raw_score = float(result.get("score", 0))
    if raw_score > 1.0:
        # Stack Overflow 等平台的分数可能很大
        raw_score = min(1.0, math.log(1 + raw_score) / 10)
    elif raw_score < 0:
        raw_score = 0.0

    # 来源可信度系数（结合自学习权重）
    source = result.get("source", "")
    reliability = SOURCE_RELIABILITY.get(source, 0.5)

    # 应用自学习权重调整
    learned_weight = _get_learned_weight(source)
    reliability = min(1.0, reliability * learned_weight)

    # 时间衰减：最近的内容权重更高
    created = result.get("created_at", "")
    age_days = days_ago(created) if created else 365
    recency_factor = math.pow(0.5, age_days / RECENCY_HALF_LIFE)

    # 综合评分
    authority = (raw_score * 0.4 + reliability * 0.3 + recency_factor * 0.3)
    return min(1.0, max(0.0, authority))


def _combined_score(
    result: Dict[str, Any],
    query_tokens: List[str],
    idf: Dict[str, float],
) -> float:
    """计算综合排序分数。

    综合 TF-IDF 相关性和权威性。

    Args:
        result: 搜索结果条目。
        query_tokens: 查询词语列表。
        idf: IDF 字典。

    Returns:
        综合分数（0.0 ~ 1.0）。
    """
    # 文档内容 = 标题 + 摘要
    text = f"{result.get('title', '')} {result.get('snippet', '')}"
    doc_tokens = _tokenize(text)

    relevance = _tfidf_relevance_score(query_tokens, doc_tokens, idf)
    authority = _authority_score(result)

    # 相关性权重 60%，权威性权重 40%
    return relevance * 0.6 + authority * 0.4


# ============================================================
# Jaccard 去重
# ============================================================

def _jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """计算两个集合的 Jaccard 相似度。

    J(A, B) = |A ∩ B| / |A ∪ B|

    Args:
        set_a: 集合 A。
        set_b: 集合 B。

    Returns:
        Jaccard 相似度（0.0 ~ 1.0）。
    """
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0

    intersection = len(set_a & set_b)
    union = len(set_a | set_b)

    if union == 0:
        return 0.0
    return intersection / union


def _deduplicate_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """对搜索结果进行去重。

    使用 Jaccard 相似度比较标题和摘要的词集，
    相似度超过阈值的结果保留分数较高的。

    Args:
        results: 搜索结果列表。

    Returns:
        去重后的结果列表。
    """
    if not results:
        return []

    # 为每个结果计算词集
    result_word_sets = []
    for r in results:
        text = f"{r.get('title', '')} {r.get('snippet', '')}"
        result_word_sets.append(_word_set(text))

    kept = []
    kept_indices = []

    for i, result in enumerate(results):
        is_duplicate = False
        for j in kept_indices:
            sim = _jaccard_similarity(result_word_sets[i], result_word_sets[j])
            if sim >= DEDUP_THRESHOLD:
                is_duplicate = True
                break
        if not is_duplicate:
            kept.append(result)
            kept_indices.append(i)

    return kept


# ============================================================
# 合成摘要（付费功能）
# ============================================================

def _synthesize_results(
    query: str,
    results: List[Dict[str, Any]],
    max_items: int = 10,
) -> str:
    """将搜索结果合成为结构化 Markdown 摘要。

    Args:
        query: 原始查询。
        results: 排序后的搜索结果。
        max_items: 纳入合成的最大结果数。

    Returns:
        Markdown 格式的合成摘要。
    """
    top = results[:max_items]
    parts = []
    parts.append(f"# 知识搜索合成报告\n")
    parts.append(f"**查询**: {query}")
    parts.append(f"**结果数**: {len(results)} 条（展示前 {len(top)} 条）")
    parts.append(f"**生成时间**: {now_iso()}\n")

    # 按来源分组
    by_source = {}
    for r in top:
        src = r.get("source", "unknown")
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(r)

    parts.append("## 来源分布\n")
    for src, items in by_source.items():
        badge = format_source_badge(src)
        parts.append(f"- {badge}: {len(items)} 条结果")
    parts.append("")

    # 关键发现
    parts.append("## 关键发现\n")
    for idx, r in enumerate(top, 1):
        badge = format_source_badge(r.get("source", ""))
        title = r.get("title", "无标题")
        url = r.get("url", "")
        snippet = truncate_text(r.get("snippet", ""), 150)
        score = r.get("_combined_score", r.get("score", 0))
        author = r.get("author", "")
        created = r.get("created_at", "")

        parts.append(f"### {idx}. {title}")
        parts.append(f"- **来源**: {badge}")
        if url:
            parts.append(f"- **链接**: {url}")
        if author:
            parts.append(f"- **作者**: {author}")
        if created:
            parts.append(f"- **日期**: {created}")
        parts.append(f"- **相关度**: {score:.2f}")
        parts.append(f"- **摘要**: {snippet}")
        parts.append("")

    # 标签汇总
    all_tags = []
    for r in top:
        all_tags.extend(r.get("tags", []))
    if all_tags:
        tag_counts = Counter(all_tags)
        top_tags = tag_counts.most_common(10)
        parts.append("## 热门标签\n")
        for tag, count in top_tags:
            parts.append(f"- `{tag}` ({count})")
        parts.append("")

    # Mermaid 来源分布图
    parts.append("## 来源分布图\n")
    parts.append("```mermaid")
    parts.append("pie title 搜索结果来源分布")
    for src, items in by_source.items():
        display = SOURCE_DISPLAY_NAMES.get(src, src)
        parts.append(f'    "{display}" : {len(items)}')
    parts.append("```\n")

    parts.append("---")
    parts.append("*由 knowledge-mesh 自动生成*")

    return "\n".join(parts)


# ============================================================
# 操作实现
# ============================================================

def action_rank(data: Dict[str, Any]) -> None:
    """对搜索结果进行综合排序。

    Args:
        data: 包含 query 和 results 的字典。
    """
    query = data.get("query", "")
    results = data.get("results", [])

    if not results:
        output_success({"query": query, "total": 0, "results": []})
        return

    query_tokens = _tokenize(query)

    # 构建语料库 IDF
    documents = []
    for r in results:
        text = f"{r.get('title', '')} {r.get('snippet', '')}"
        documents.append(_tokenize(text))
    idf = _build_corpus_idf(documents)

    # 计算综合分数
    for r in results:
        r["_combined_score"] = _combined_score(r, query_tokens, idf)

    # 排序
    results.sort(key=lambda r: r.get("_combined_score", 0), reverse=True)

    output_success({
        "query": query,
        "total": len(results),
        "results": results,
    })


def action_dedup(data: Dict[str, Any]) -> None:
    """对搜索结果进行去重。

    Args:
        data: 包含 results 的字典。
    """
    results = data.get("results", [])
    original_count = len(results)

    deduped = _deduplicate_results(results)

    output_success({
        "original_count": original_count,
        "deduped_count": len(deduped),
        "removed": original_count - len(deduped),
        "results": deduped,
    })


def action_synthesize(data: Dict[str, Any]) -> None:
    """合成搜索结果为结构化报告（付费功能）。

    Args:
        data: 包含 query 和 results 的字典。
    """
    if not require_paid_feature("synthesis", "知识合成"):
        return

    query = data.get("query", "")
    results = data.get("results", [])

    if not results:
        output_error("无搜索结果可合成", code="NO_DATA")
        return

    # 先排序
    query_tokens = _tokenize(query)
    documents = []
    for r in results:
        text = f"{r.get('title', '')} {r.get('snippet', '')}"
        documents.append(_tokenize(text))
    idf = _build_corpus_idf(documents)
    for r in results:
        r["_combined_score"] = _combined_score(r, query_tokens, idf)
    results.sort(key=lambda r: r.get("_combined_score", 0), reverse=True)

    # 去重
    results = _deduplicate_results(results)

    # 生成合成报告
    max_items = data.get("max_items", 10)
    report = _synthesize_results(query, results, max_items=max_items)

    output_success({
        "query": query,
        "total": len(results),
        "report": report,
    })


def action_summarize(data: Dict[str, Any]) -> None:
    """生成搜索结果的简要统计摘要。

    Args:
        data: 包含 results 的字典，可选 query。
    """
    results = data.get("results", [])
    query = data.get("query", "")

    total = len(results)

    # 来源统计
    source_counts = Counter()
    for r in results:
        source_counts[r.get("source", "unknown")] += 1

    # 时间分布
    recent_7d = 0
    recent_30d = 0
    older = 0
    for r in results:
        created = r.get("created_at", "")
        age = days_ago(created) if created else 999
        if age <= 7:
            recent_7d += 1
        elif age <= 30:
            recent_30d += 1
        else:
            older += 1

    # 热门标签
    all_tags = []
    for r in results:
        all_tags.extend(r.get("tags", []))
    top_tags = Counter(all_tags).most_common(10)

    # 平均分数
    scores = [r.get("score", 0) for r in results if r.get("score", 0) > 0]
    avg_score = sum(scores) / len(scores) if scores else 0.0

    summary = {
        "query": query,
        "total_results": total,
        "source_distribution": dict(source_counts),
        "time_distribution": {
            "last_7_days": recent_7d,
            "last_30_days": recent_30d,
            "older": older,
        },
        "top_tags": [{"tag": t, "count": c} for t, c in top_tags],
        "average_score": round(avg_score, 3),
    }

    output_success(summary)


def action_record_feedback(data: Dict[str, Any]) -> None:
    """记录用户对搜索结果的反馈，并更新自学习权重。

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
    if rating not in {"relevant", "irrelevant", "helpful"}:
        output_error(
            f"无效的评级: {rating}，支持: relevant、irrelevant、helpful",
            code="VALIDATION_ERROR",
        )
        return

    # 委托给 learning_engine 记录反馈
    try:
        from learning_engine import record_feedback_data
        record_feedback_data(result_id, source, rating)
        output_success({
            "message": f"已记录反馈: {source} 结果 {result_id} 评级为 {rating}",
            "result_id": result_id,
            "source": source,
            "rating": rating,
        })
    except ImportError:
        output_error("自学习模块不可用", code="MODULE_ERROR")
    except Exception as e:
        output_error(f"记录反馈失败: {e}", code="FEEDBACK_ERROR")


def action_calibrate(data: Optional[Dict[str, Any]] = None) -> None:
    """根据反馈历史重新校准最优知识源权重。

    从 learning_engine 触发权重重算并返回新权重。
    """
    try:
        from learning_engine import _load_learning_data, _compute_optimal_weights, _save_learning_data, DEFAULT_SOURCE_WEIGHTS

        learning_data = _load_learning_data()
        feedback = learning_data.get("feedback", [])

        if len(feedback) < 2:
            output_error(
                f"反馈数据不足（当前 {len(feedback)} 条，需要至少 2 条），无法校准",
                code="INSUFFICIENT_DATA",
            )
            return

        old_weights = dict(learning_data.get("source_weights", DEFAULT_SOURCE_WEIGHTS))
        new_weights = _compute_optimal_weights(feedback, old_weights)
        learning_data["source_weights"] = new_weights
        _save_learning_data(learning_data)

        changes = []
        for source in set(list(old_weights.keys()) + list(new_weights.keys())):
            old_w = old_weights.get(source, 1.0)
            new_w = new_weights.get(source, 1.0)
            if abs(old_w - new_w) > 0.001:
                changes.append({
                    "source": source,
                    "old_weight": old_w,
                    "new_weight": new_w,
                })

        output_success({
            "message": f"权重校准完成，基于 {len(feedback)} 条反馈",
            "weights": new_weights,
            "changes": changes,
        })
    except ImportError:
        output_error("自学习模块不可用", code="MODULE_ERROR")
    except Exception as e:
        output_error(f"校准失败: {e}", code="CALIBRATE_ERROR")


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("knowledge-mesh 搜索结果排序与合成")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "rank": lambda: action_rank(data or {}),
        "dedup": lambda: action_dedup(data or {}),
        "synthesize": lambda: action_synthesize(data or {}),
        "summarize": lambda: action_summarize(data or {}),
        "record-feedback": lambda: action_record_feedback(data or {}),
        "calibrate": lambda: action_calibrate(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
