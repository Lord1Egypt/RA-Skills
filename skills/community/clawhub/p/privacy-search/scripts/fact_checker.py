#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事实核查层（V1.8 新增）

功能：合成答案逐论断回链原文句做相似度比对，标注支撑度三级。
目标：答案可信度可验证——每个论断都能确认是否源于抓取的正文。

支撑度分级：
  sufficient（充分）  — 原文明确包含该论断的核心语义
  partial（部分）     — 原文有相关表述但不够精确
  unsupported（无源） — 原文找不到支撑，疑似幻觉

遵循死规则 9：纯本地计算（TF-IDF + 余弦相似度），不依赖外部 API。
遵循死规则 10：控制计算量（仅比对论断句与原文句，不做全篇两两比对）。
遵循死规则 13：不生成 __pycache__。

依赖：ranking 模块的 TF-IDF 与 jieba 分词（jieba 缺失时自动降级为字符级）。
"""

import re
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.dont_write_bytecode = True

# 相似度阈值（可调）
SUFFICIENT_THRESHOLD = 0.55
PARTIAL_THRESHOLD = 0.25

# 默认配置
_DEFAULT_CONFIG = {
    "sufficient_threshold": SUFFICIENT_THRESHOLD,
    "partial_threshold": PARTIAL_THRESHOLD,
    "remove_unsupported": True,       # 默认剔除无源论断
    "min_claim_length": 8,            # 短于此字符数的论断不核查（通常是衔接句）
}


# ============================================================
# 文本分句
# ============================================================

_SENT_SPLIT_RE = re.compile(r"[。！？.!?\n]+|(?:\n{2,})")


def _split_sentences(text: str) -> List[str]:
    """
    把文本切成句子列表

    优先按句末标点切分；中文语境下换行也作为切分信号。
    尾部无标点的剩余内容也保留为一个句子。
    """
    if not text:
        return []
    parts = _SENT_SPLIT_RE.split(text)
    return [p.strip() for p in parts if p and len(p.strip()) >= 3]


# ============================================================
# 文本特征提取（复用 ranking 模块）
# ============================================================

def _extract_tfidf_vector(text: str) -> Dict[str, float]:
    """
    构建 TF-IDF 向量（无外部语料，用单个文档内词频近似 TF）

    不需要全局语料库——我们只关心 claim 与 source_sentence 之间的
    词汇重叠程度，单文档级别的 tf 足够区分"完全无关"与"高度相关"。
    """
    try:
        from ranking import extract_features
    except ImportError:
        from .ranking import extract_features

    features = extract_features(text, max_len=512)
    if not features:
        return {}

    # 词频作为 tf
    tf: Dict[str, float] = {}
    for f in features:
        tf[f] = tf.get(f, 0.0) + 1.0

    # 归一化
    total = sum(tf.values())
    if total > 0:
        for k in tf:
            tf[k] /= total

    return tf


def _cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    """计算两个稀疏向量的余弦相似度"""
    if not vec_a or not vec_b:
        return 0.0

    # 取交集维度计算点积
    common = set(vec_a.keys()) & set(vec_b.keys())
    if not common:
        return 0.0

    dot = sum(vec_a[k] * vec_b[k] for k in common)
    norm_a = sum(v * v for v in vec_a.values()) ** 0.5
    norm_b = sum(v * v for v in vec_b.values()) ** 0.5

    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0
    return dot / (norm_a * norm_b)


# ============================================================
# 论断拆分
# ============================================================

# 匹配形如 [1]、[1][2]、[1,2] 的引用标记
_CITATION_RE = re.compile(r"\[\d+(?:[,\s]+\d+)*\]")


def _split_claims(answer: str) -> List[str]:
    """
    把答案拆成独立论断（句子粒度）

    以句末标点 + 引用标记为切分依据。
    如果整个答案都没引用标记，按句号分句后整体作为一个论断。
    """
    if not answer:
        return []

    # 先按行分（citation 通常跟在句末换行前）
    lines = answer.replace("\r\n", "\n").split("\n")
    claims: List[str] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 如果一个句号后面紧跟引用标记，优先按句号切
        if _CITATION_RE.search(line):
            # 把引用标记前移：把 "xx[1]" 切成 "xx [1]"
            line = re.sub(r"\s*(\[\d)", r" \1", line)
            # 按句号+引用标记切
            sub_parts = re.split(r"(?<=[。！？])", line)
            for part in sub_parts:
                part = part.strip()
                if part:
                    claims.append(part)
        else:
            # 无引用标记的行直接作为一个候选
            sents = _split_sentences(line)
            claims.extend(sents if sents else [line])

    return [c for c in claims if len(c.strip()) > 5]


# ============================================================
# 事实核查主逻辑
# ============================================================

def _check_single_claim(
    claim: str,
    source_sentences: List[str],
    config: Dict[str, Any],
) -> Tuple[str, float, str]:
    """
    核查单个论断

    Returns:
        (支撑度标签, 最大相似度, 最匹配原文句)
    """
    claim_vec = _extract_tfidf_vector(claim)
    if not claim_vec:
        return ("unsupported", 0.0, "")

    sufficient_th = float(config.get("sufficient_threshold", SUFFICIENT_THRESHOLD))
    partial_th = float(config.get("partial_threshold", PARTIAL_THRESHOLD))

    best_sim = 0.0
    best_sentence = ""

    for sent in source_sentences:
        sent_vec = _extract_tfidf_vector(sent)
        if not sent_vec:
            continue
        sim = _cosine_similarity(claim_vec, sent_vec)
        if sim > best_sim:
            best_sim = sim
            best_sentence = sent

    if best_sim >= sufficient_th:
        return ("sufficient", best_sim, best_sentence)
    elif best_sim >= partial_th:
        return ("partial", best_sim, best_sentence)
    else:
        return ("unsupported", best_sim, best_sentence)


def _extract_source_sentences(sources: List[Any]) -> List[str]:
    """
    从 sources 中提取全部原文句子

    sources 格式：List[Tuple[int, str, str]] — (source_id, url, content)
    """
    sentences: List[str] = []
    if not sources:
        return sentences

    for item in sources:
        if isinstance(item, (list, tuple)) and len(item) >= 3:
            content = item[2]
        elif isinstance(item, dict):
            content = item.get("content", "") or ""
        else:
            content = ""
        if content:
            sentences.extend(_split_sentences(content))

    return sentences


def _strip_citation_markers(text: str) -> str:
    """移除引用标记，便于展示"""
    return _CITATION_RE.sub("", text).strip()


def fact_check(
    answer: str,
    sources: List[Any],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    对合成答案执行事实核查

    Args:
        answer: 合成答案文本（带 citation 标记）
        sources: 来源列表，格式 [(source_id, url, content), ...]
        config: 配置字典，可覆盖 _DEFAULT_CONFIG

    Returns:
        {
            "cleaned_answer": str,          # 处理后的答案
            "claims": [                     # 每个论断的核查结果
                {
                    "text": str,            # 论断原文
                    "label": str,           # sufficient / partial / unsupported
                    "similarity": float,    # 最大相似度
                    "evidence": str,        # 最匹配的原文句
                    "kept": bool,           # 是否保留在答案中
                }
            ],
            "removed_claims": List[str],    # 被移除的论断（无源）
            "source_count": int,            # 来源数
            "check_method": str,            # 核查方法说明
        }
    """
    cfg = dict(_DEFAULT_CONFIG)
    if config:
        fc = config.get("fact_check", {}) or {}
        cfg.update(fc)

    min_claim_len = int(cfg.get("min_claim_length", 8))

    # 提取原文句
    source_sentences = _extract_source_sentences(sources)

    # 拆分论断
    raw_claims = _split_claims(answer)

    claims_result: List[Dict[str, Any]] = []
    removed: List[str] = []
    kept_parts: List[str] = []

    for claim in raw_claims:
        # 跳过太短的（衔接语、引用列表等）
        stripped = _strip_citation_markers(claim)
        if len(stripped) < min_claim_len:
            kept_parts.append(claim)
            continue

        label, sim, evidence = _check_single_claim(claim, source_sentences, cfg)

        kept = True
        if label == "unsupported" and cfg.get("remove_unsupported", True):
            kept = False
            removed.append(claim)

        claims_result.append({
            "text": claim,
            "label": label,
            "similarity": round(sim, 3),
            "evidence": evidence[:200] if evidence else "",
            "kept": kept,
        })

        if kept:
            kept_parts.append(claim)

    # 重新拼接保留的论断
    cleaned = "\n".join(kept_parts)

    # 统计
    sufficient_count = sum(1 for c in claims_result if c["label"] == "sufficient")
    partial_count = sum(1 for c in claims_result if c["label"] == "partial")
    unsupported_count = sum(1 for c in claims_result if c["label"] == "unsupported")

    method_note = (
        f"事实核查：使用 TF-IDF 余弦相似度逐论断比对原文句。"
        f"阈值：充分≥{cfg['sufficient_threshold']}，部分≥{cfg['partial_threshold']}。"
        f"本轮核查 {len(claims_result)} 条论断，"
        f"充分 {sufficient_count} / 部分 {partial_count} / 无源 {unsupported_count}。"
    )

    return {
        "cleaned_answer": cleaned,
        "claims": claims_result,
        "removed_claims": removed,
        "source_count": len(sources) if sources else 0,
        "check_method": method_note,
    }


# ============================================================
# 格式化输出
# ============================================================

def format_fact_check_report(result: Dict[str, Any]) -> str:
    """
    将 fact_check 结果格式化为可读报告（追加到答案末尾）
    """
    lines: List[str] = []
    lines.append("\n--- 事实核查报告 ---")

    # 支撑度分布
    sufficient = sum(1 for c in result["claims"] if c["label"] == "sufficient")
    partial = sum(1 for c in result["claims"] if c["label"] == "partial")
    unsupported = sum(1 for c in result["claims"] if c["label"] == "unsupported")
    total = len(result["claims"])

    lines.append(f"论断总数：{total}")
    lines.append(f"  充分支撑：{sufficient}")
    lines.append(f"  部分支撑：{partial}")
    lines.append(f"  无源：{unsupported}")

    if result["removed_claims"]:
        lines.append(f"\n已移除无源论断 {len(result['removed_claims'])} 条：")
        for rc in result["removed_claims"][:3]:
            lines.append(f"  · {_strip_citation_markers(rc)[:80]}")

    # 引用清单
    lines.append(f"\n引用清单（{result['source_count']} 个来源）：")
    # 引用清单由调用方在合成后追加
    lines.append(f"\n核查方法：{result['check_method']}")
    return "\n".join(lines)


if __name__ == "__main__":
    # 简单自测
    test_sources = [
        (1, "https://a.com", "量子计算利用量子比特的叠加态进行并行计算。与传统计算机相比，量子计算机在特定问题上具有指数级加速潜力。"),
        (2, "https://b.com", "目前量子计算机面临的主要挑战是量子退相干问题。科学家正在研发纠错码来解决这一难题。"),
    ]
    test_answer = (
        "量子计算利用量子比特进行并行计算 [1]。\n"
        "量子计算机已在所有问题上超越了传统计算机 [1][2]。\n"
        "量子退相干是当前的主要挑战之一 [2]。"
    )
    result = fact_check(test_answer, test_sources, {})
    print("原始答案:")
    print(test_answer)
    print("\n处理后答案:")
    print(result["cleaned_answer"])
    print("\n核查详情:")
    for c in result["claims"]:
        print(f"  [{c['label']}] sim={c['similarity']:.3f} | {c['text'][:40]}")
    print(format_fact_check_report(result))
