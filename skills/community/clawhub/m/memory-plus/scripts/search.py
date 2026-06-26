"""
记忆搜索 - 文件 + FTS5 混合搜索

FTS5 全文搜索增强，零外部依赖
后续可升级为向量搜索 + rerank
"""
import re
import json
import os
import math
from pathlib import Path
from typing import Optional
from .config import MEMORY_DIR, RERANK_SERVICE_URL, get_memory_files
from .fts5 import search_fts, rerank_with_fts


def get_all_chunks(limit: int = 1000) -> list[dict]:
    """
    获取所有记忆片段（用于去重、合并等维护操作）
    """
    chunks = []
    for mf in get_memory_files():
        try:
            date = mf.stem  # YYYY-MM-DD
            content = mf.read_text(encoding="utf-8")

            for para in content.split("\n"):
                para = para.strip()
                if len(para) > 10:
                    para = re.sub(r"^[-*]\s+", "", para).strip()
                    if para:
                        chunks.append({
                            "chunk": para,
                            "date": date,
                            "file": str(mf),
                        })
        except Exception:
            continue

        if len(chunks) >= limit:
            break

    return chunks


def _ngram(text: str, n: int = 2) -> set:
    """
    字符级 N-gram 提取
    中文：'今天天气不错' → {'今天', '天好', '好不', '不错'}
    英文：'hello world' → {'he', 'el', 'll', 'lo', 'o ', ' w', 'wo', 'or', 'rl', 'ld'}
    """
    return {text[i:i+n] for i in range(len(text) - n + 1)}


def _jaccard_ngram(text1: str, text2: str, n: int = 2) -> float:
    """基于字符 N-gram 的 Jaccard 相似度（适合中英文混合）"""
    ng1 = _ngram(text1.lower(), n)
    ng2 = _ngram(text2.lower(), n)
    if not ng1 or not ng2:
        return 0.0
    intersection = len(ng1 & ng2)
    union = len(ng1 | ng2)
    return intersection / union if union > 0 else 0.0


def simple_search(query: str, limit: int = 3) -> list[dict]:
    """
    简单搜索：基于字符 N-gram Jaccard 相似度
    支持中英文混合，无需分词
    """
    results = []

    for mf in get_memory_files():
        try:
            date = mf.stem
            content = mf.read_text(encoding="utf-8")

            for para in content.split("\n"):
                para = para.strip()
                if len(para) < 5:
                    continue
                para = re.sub(r"^[-*]\s+", "", para).strip()
                if not para:
                    continue

                # 字符 N-gram Jaccard
                score = _jaccard_ngram(query, para, n=2)

                if score > 0:
                    results.append({
                        "chunk": para,
                        "date": date,
                        "score": score,
                        "file": str(mf)
                    })
        except Exception:
            continue

    # 按相似度排序
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def rerank_results(query: str, results: list[dict], top_n: int = 3) -> list[dict]:
    """
    简单的 rerank：优先返回近期、高分的结果
    后续可接入真正的 bge-reranker-v2-m3
    """
    # 简单加权：分数 * 时间衰减因子
    import time
    now = time.time()
    DAY = 86400

    reranked = []
    for r in results:
        try:
            file_date = r.get("date", "")
            if file_date:
                from datetime import datetime
                d = datetime.strptime(file_date, "%Y-%m-%d")
                age_days = (now - d.timestamp()) / DAY
                time_weight = math.exp(-0.05 * age_days)  # 指数衰减
            else:
                time_weight = 0.5

            r["rerank_score"] = r["score"] * (0.7 + 0.3 * time_weight)
            reranked.append(r)
        except Exception:
            r["rerank_score"] = r["score"]
            reranked.append(r)

    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    return reranked[:top_n]


def search_memories(
    query: str,
    limit: int = 3,
    use_rerank: bool = True,
    use_llm: bool = False,
) -> dict:
    """
    主搜索入口 — FTS5 + Jaccard 混合搜索

    流程：
    1. Jaccard 快速召回 top-k
    2. FTS5 BM25 重排（如果 FTS5 可用）
    3. 时间衰减 rerank

    Args:
        query: 搜索查询
        limit: 返回数量
        use_rerank: 是否使用 rerank（目前强制开启）
        use_llm: 是否用 LLM 生成总结（暂不支持）
    """
    if not query or not query.strip():
        return {"answer": "", "results": [], "count": 0}

    # 1. Jaccard 快速召回（不用外部服务）
    results = simple_search(query, limit=limit * 3)

    if not results:
        return {"answer": "", "results": [], "count": 0}

    # 2. FTS5 重排（零依赖，如果失败静默降级）
    # 注意：FTS5 默认不支持中文分词，中文查询会返回空，此时保留 Jaccard 结果
    if use_rerank:
        fts_results = rerank_with_fts(results, query, top_n=limit * 2)
        # 如果 FTS5 重排后有结果才用，否则保持 Jaccard 结果
        if fts_results:
            results = fts_results

    # 3. 时间衰减 rerank
    if use_rerank:
        results = rerank_results(query, results, top_n=limit)

    return {
        "answer": "",
        "results": results[:limit],
        "count": len(results[:limit])
    }


def rag_search(query: str, limit: int = 3) -> dict:
    """RAG 搜索（当前等价于简单搜索）"""
    return search_memories(query, limit=limit, use_rerank=True, use_llm=False)
