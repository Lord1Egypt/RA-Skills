#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可信答案 RAG-lite（V2.1.0 新增）

功能：多源正文抓取 → 本地分块 → TF-IDF 相关块选择 → 带 citation 答案。
答案结构固定三段：结论 / 依据 / 反证。

设计原则（死规则）：
- 死规则 9：全本地实现（TF-IDF），不依赖外部 API；LLM（GLM-4-Flash）仅可选增强，
  不可用时自动降级为抽取式。零 Key 也能产出三段答案。
- 死规则 10：控制计算量——只选 Top-K 相关块，不做全篇两两比对。
- 死规则 13：不生成 __pycache__。

反证策略（本地规则实现，非 LLM 黑盒）：
    反证 = 与「结论关键词」同主题、但与已选支撑块语义重叠低的相关块。
    即"提到了同一主题、但说法与结论不同"的段落，作为供用户判断的对立面。
    该策略无法保证找出严格逻辑反例，但可在无 LLM 时提供诚实的"另一面"。

输出结构：
    结论：一到两句核心回答（来自最高相关块）
    依据：支撑结论的原文块（带 [来源N] citation，可回链原文）
    反证：与结论同主题但表述不同的原文块（带 citation）
"""

import re
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.dont_write_bytecode = True

try:
    from ranking import extract_features
except ImportError:
    from .ranking import extract_features

try:
    from fact_checker import _split_sentences, _cosine_similarity
except ImportError:
    from .fact_checker import _split_sentences, _cosine_similarity

# 默认配置
_DEFAULT_CONFIG = {
    "top_k_evidence": 3,        # 依据块数量上限
    "top_k_counter": 2,         # 反证块数量上限
    "counter_overlap_max": 0.45,  # 反证与依据相似度低于此值才算"另一面"
    "chunk_size": 1200,         # 单块字符数
    "max_answer_chars": 1500,   # 答案总长度上限
}

# 引用标记
_CITATION_RE = re.compile(r"\[\d+\]")


# ============================================================
# 分块（保留来源归属）
# ============================================================

def chunk_sources(
    sources: List[Tuple[int, str, str]],
    chunk_size: int = 1200,
) -> List[Dict[str, Any]]:
    """
    把多源正文切成带来源归属的块

    Args:
        sources: [(source_id, url, content), ...]
        chunk_size: 单块最大字符数

    Returns:
        [{"source_id": int, "url": str, "text": str, "vec": {...}}, ...]
    """
    from fact_checker import _extract_tfidf_vector

    chunks: List[Dict[str, Any]] = []
    for source_id, url, content in sources:
        if not content:
            continue
        # 先按句分，再按 chunk_size 组块（保留语义完整）
        sents = _split_sentences(content)
        buf = ""
        for sent in sents:
            if len(buf) + len(sent) > chunk_size and buf:
                chunks.append({
                    "source_id": source_id,
                    "url": url,
                    "text": buf.strip(),
                    "vec": _extract_tfidf_vector(buf),
                })
                buf = sent
            else:
                buf += (" " if buf else "") + sent
        if buf.strip():
            chunks.append({
                "source_id": source_id,
                "url": url,
                "text": buf.strip(),
                "vec": _extract_tfidf_vector(buf),
            })
    return chunks


# ============================================================
# TF-IDF 相关块选择
# ============================================================

def select_relevant_chunks(
    query: str,
    chunks: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Tuple[Dict[str, Any], float]]:
    """按与查询的 TF-IDF 余弦相似度选出 Top-K 块"""
    from fact_checker import _extract_tfidf_vector

    q_vec = _extract_tfidf_vector(query)
    if not q_vec or not chunks:
        return []

    scored: List[Tuple[Dict[str, Any], float]] = []
    for ch in chunks:
        vec = ch.get("vec") or _extract_tfidf_vector(ch["text"])
        sim = _cosine_similarity(q_vec, vec)
        scored.append((ch, sim))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def select_counter_chunks(
    supporting: List[Tuple[Dict[str, Any], float]],
    all_chunks: List[Dict[str, Any]],
    config: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    选择反证块：与查询相关、但与支撑块语义重叠低。

    实现：用支撑块文本的向量均值作为"结论向量"，
    从剩余高相关块中选与结论向量相似度 < counter_overlap_max 的块。
    """
    overlap_max = float(config.get("counter_overlap_max", 0.45))
    top_k_counter = int(config.get("top_k_counter", 2))

    if not supporting:
        return []

    # 支撑块向量（取最高分的几个）
    support_vecs = [ch.get("vec") or {} for ch, _ in supporting[:3]]
    support_text_vec: Dict[str, float] = {}
    for vec in support_vecs:
        for k, v in vec.items():
            support_text_vec[k] = support_text_vec.get(k, 0.0) + v

    support_texts = {id(ch) for ch, _ in supporting}
    counter: List[Dict[str, Any]] = []
    for ch in all_chunks:
        if id(ch) in support_texts:
            continue
        vec = ch.get("vec") or {}
        sim_to_support = _cosine_similarity(support_text_vec, vec)
        # 语义重叠低 = 说法不同；查询相关度高 = 同主题
        if sim_to_support < overlap_max:
            counter.append(ch)
        if len(counter) >= top_k_counter:
            break
    return counter


# ============================================================
# 三段答案生成
# ============================================================

def _source_citation(chunk: Dict[str, Any], sources: List[Tuple[int, str, str]]) -> str:
    """生成 citation 标记，返回 [来源N]"""
    sid = chunk.get("source_id", 0)
    return f"[来源{sid}]"


def _build_conclusion(
    query: str,
    supporting: List[Tuple[Dict[str, Any], float]],
    max_chars: int = 300,
) -> str:
    """从最高相关块提炼结论句（取该块前 1-2 句）"""
    if not supporting:
        return "根据现有搜索结果无法确定明确结论。"
    top_chunk = supporting[0][0]
    sentences = _split_sentences(top_chunk["text"])
    if not sentences:
        return top_chunk["text"][:max_chars]
    conclusion = sentences[0]
    if len(sentences) > 1 and len(conclusion) + len(sentences[1]) <= max_chars:
        conclusion += sentences[1]
    return conclusion[:max_chars]


def synthesize_rag_lite(
    query: str,
    sources: List[Tuple[int, str, str]],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    RAG-lite 主入口：无 Key 抽取式，产出三段答案。

    Args:
        query: 用户问题
        sources: [(source_id, url, content), ...]
        config: 配置字典（rag_lite 段）

    Returns:
        {
            "answer": str,              # 三段答案文本
            "conclusion": str,          # 结论段
            "evidence": [...],          # 依据块（含 citation）
            "counter": [...],           # 反证块（含 citation）
            "sources": [...],           # 来源清单
            "chunks_count": int,        # 分块总数
            "method": str,              # 方法说明
        }
    """
    cfg = dict(_DEFAULT_CONFIG)
    if config:
        rc = config.get("rag_lite", {}) or {}
        cfg.update(rc)

    empty = {
        "answer": "没有找到足够的相关内容来生成答案。",
        "conclusion": "",
        "evidence": [],
        "counter": [],
        "sources": [{"id": sid, "url": url} for sid, url, _ in (sources or [])],
        "chunks_count": 0,
        "method": "RAG-lite 本地抽取式（无可用正文）",
    }
    if not sources or not query:
        return empty

    chunk_size = int(cfg["chunk_size"])
    chunks = chunk_sources(sources, chunk_size=chunk_size)
    if not chunks:
        return empty

    top_k = int(cfg["top_k_evidence"]) + int(cfg["top_k_counter"]) + 2
    relevant = select_relevant_chunks(query, chunks, top_k=max(top_k, 5))
    supporting = relevant[:int(cfg["top_k_evidence"])]
    counter = select_counter_chunks(supporting, [c for c, _ in relevant], cfg)

    conclusion = _build_conclusion(query, supporting)

    # 依据段：结论句带最高分块的 citation
    evidence_lines: List[str] = []
    evidence_data: List[Dict[str, Any]] = []
    for ch, sim in supporting:
        cite = _source_citation(ch, sources)
        text = ch["text"][:400]
        evidence_lines.append(f"  • {text} {cite}")
        evidence_data.append({
            "text": text,
            "citation": cite,
            "source_id": ch["source_id"],
            "url": ch["url"],
            "similarity": round(sim, 3),
        })

    # 反证段
    counter_lines: List[str] = []
    counter_data: List[Dict[str, Any]] = []
    for ch in counter:
        cite = _source_citation(ch, sources)
        text = ch["text"][:400]
        counter_lines.append(f"  • {text} {cite}")
        counter_data.append({
            "text": text,
            "citation": cite,
            "source_id": ch["source_id"],
            "url": ch["url"],
        })

    # 结论 citation
    if supporting:
        top_cite = _source_citation(supporting[0][0], sources)
        conclusion = f"{conclusion} {top_cite}"

    # 来源清单
    source_list = [f"[{sid}] {url}" for sid, url, _ in sources]

    parts = [
        "【结论】",
        conclusion,
        "",
        "【依据】",
        "\n".join(evidence_lines) if evidence_lines else "  （未找到明确支撑段落）",
        "",
        "【反证】",
        "\n".join(counter_lines) if counter_lines else "  （未找到明显对立表述，建议自行核对来源）",
        "",
        "--- 来源 ---",
        "\n".join(source_list),
    ]
    answer = "\n".join(parts)

    # 长度封顶（死规则 10）
    if len(answer) > int(cfg["max_answer_chars"]):
        answer = answer[:int(cfg["max_answer_chars"])] + "\n…（已截断，建议查看来源原文）"

    return {
        "answer": answer,
        "conclusion": conclusion,
        "evidence": evidence_data,
        "counter": counter_data,
        "sources": [{"id": sid, "url": url} for sid, url, _ in sources],
        "chunks_count": len(chunks),
        "method": (
            f"RAG-lite 本地抽取式：{len(sources)} 个来源切分为 {len(chunks)} 块，"
            f"TF-IDF 选出 {len(supporting)} 个依据块、{len(counter)} 个反证块。"
            f"反证为同主题低重叠段落，供用户判断，非严格逻辑反例。"
        ),
    }


if __name__ == "__main__":
    test_sources = [
        (1, "https://a.com", "量子计算利用量子比特的叠加态进行并行计算，在特定问题上具有指数级加速潜力。科学家认为量子计算将改变密码学格局。"),
        (2, "https://b.com", "量子计算机面临的主要挑战是量子退相干问题。研究人员正在研发纠错码来延长量子比特的相干时间。"),
        (3, "https://c.com", "有学者指出，量子计算的实际应用仍受限于硬件成本，短期内难以大规模商用，部分承诺被夸大。"),
    ]
    result = synthesize_rag_lite("量子计算的优势和挑战是什么", test_sources, {})
    print(result["answer"])
    print("\n---")
    print(result["method"])
