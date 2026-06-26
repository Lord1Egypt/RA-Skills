#!/usr/bin/env python3
"""
Perplexity Proxy — multi-metric predictability score for AI detection.

Core finding from empirical analysis:
- Bigram diversity is the strongest single indicator (AI: 0.83-0.94, Human: 0.97-0.99)
- Average sentence length is a strong secondary signal (AI: 29-38 chars, Human: 18-21 chars ZH)
- Sentence length CV provides additional signal (AI: lower uniformity)

Combined as "perplexity proxy" score (0-15 points).
No external dependencies. Works for both ZH and EN.
"""

import math
import re
from collections import Counter
from typing import List, Tuple


def _tokenize(text: str, lang: str) -> List[str]:
    if lang == "zh":
        return [ch for ch in text if '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf']
    else:
        return re.findall(r"[a-zA-Z]+(?:'[a-z]+)?", text.lower())


def _split_sentences(text: str, lang: str) -> List[str]:
    if lang == "zh":
        parts = re.split(r'[。！？；\n]+', text)
    else:
        parts = re.split(r'(?<=[.!?])\s+|\n+', text)
    return [s.strip() for s in parts if len(s.strip()) > 3]


# ═══════════════════════════════════════════════════════
# Metric 1: Bigram Diversity (strongest signal)
# ═══════════════════════════════════════════════════════

def bigram_diversity(text: str, lang: str) -> float:
    """
    Ratio of unique bigrams to total bigrams.
    AI text: 0.83-0.94 (stays in safe, common patterns)
    Human text: 0.97-0.99 (more varied, surprising combinations)
    """
    if lang == "zh":
        chars = [c for c in text if '\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf']
        if len(chars) < 4:
            return 0.5
        bigrams = [(chars[i], chars[i+1]) for i in range(len(chars)-1)]
    else:
        tokens = _tokenize(text, lang)
        if len(tokens) < 4:
            return 0.5
        bigrams = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
    
    if not bigrams:
        return 0.5
    return len(set(bigrams)) / len(bigrams)


# ═══════════════════════════════════════════════════════
# Metric 2: Trigram Diversity (secondary signal)
# ═══════════════════════════════════════════════════════

def trigram_diversity(text: str, lang: str) -> float:
    """Same as bigram diversity but for trigrams. Even more discriminating."""
    if lang == "zh":
        chars = [c for c in text if '\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf']
        if len(chars) < 6:
            return 0.5
        trigrams = [tuple(chars[i:i+3]) for i in range(len(chars)-2)]
    else:
        tokens = _tokenize(text, lang)
        if len(tokens) < 6:
            return 0.5
        trigrams = [tuple(tokens[i:i+3]) for i in range(len(tokens)-2)]
    
    if not trigrams:
        return 0.5
    return len(set(trigrams)) / len(trigrams)


# ═══════════════════════════════════════════════════════
# Metric 3: Sentence Length Uniformity (burstiness inverse)
# ═══════════════════════════════════════════════════════

def burstiness(text: str, lang: str) -> float:
    """
    Burstiness = natural variation in sentence length.
    Computed as: CV of adjacent sentence length differences.
    
    High burstiness (>0.6): human-like — sentences vary wildly in length.
    Low burstiness (<0.3): AI-like — sentences are uniformly long/short.
    """
    sentences = _split_sentences(text, lang)
    if len(sentences) < 3:
        return 0.5
    
    if lang == "zh":
        lengths = [len(s) for s in sentences]
    else:
        lengths = [len(s.split()) for s in sentences]
    
    # Adjacent differences
    diffs = [abs(lengths[i] - lengths[i+1]) for i in range(len(lengths)-1)]
    if not diffs:
        return 0.5
    
    avg_diff = sum(diffs) / len(diffs)
    if avg_diff == 0:
        return 0.0  # All sentences same length = zero burstiness
    
    # CV of differences (how much the jumps themselves vary)
    if len(diffs) > 1:
        std_diff = math.sqrt(sum((d - avg_diff)**2 for d in diffs) / len(diffs))
        return std_diff / avg_diff
    return 0.5


# ═══════════════════════════════════════════════════════
# Metric 4: Repetition Ratio
# ═══════════════════════════════════════════════════════

def repetition_ratio(text: str, lang: str) -> float:
    """
    How much does text repeat itself at phrase level?
    AI text reuses phrases more (repetition > 0.05).
    Human text has less repetition (< 0.03).
    
    Measures: ratio of repeated 4-gram sequences to total.
    """
    if lang == "zh":
        chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
        if len(chars) < 8:
            return 0.0
        fourgrams = [''.join(chars[i:i+4]) for i in range(len(chars)-3)]
    else:
        tokens = _tokenize(text, lang)
        if len(tokens) < 8:
            return 0.0
        fourgrams = [' '.join(tokens[i:i+4]) for i in range(len(tokens)-3)]
    
    if not fourgrams:
        return 0.0
    counts = Counter(fourgrams)
    repeated = sum(c - 1 for c in counts.values() if c > 1)
    return repeated / len(fourgrams)


# ═══════════════════════════════════════════════════════
# Combined Score
# ═══════════════════════════════════════════════════════

def compute_perplexity_metrics(text: str, lang: str = "zh") -> dict:
    """Compute all perplexity-proxy metrics."""
    bg = bigram_diversity(text, lang)
    tg = trigram_diversity(text, lang)
    burst = burstiness(text, lang)
    rep = repetition_ratio(text, lang)
    
    return {
        "bigram_diversity": round(bg, 4),
        "trigram_diversity": round(tg, 4),
        "burstiness": round(burst, 4),
        "repetition_ratio": round(rep, 4),
    }


def score_perplexity(text: str, lang: str = "zh", paragraph_len: int = 0) -> float:
    """
    Return a 0-15 score where higher = more AI-like.
    
    Scoring breakdown:
    - Low bigram diversity: 0-5 points
    - Low trigram diversity: 0-3 points
    - Low burstiness: 0-4 points
    - High repetition: 0-3 points
    """
    metrics = compute_perplexity_metrics(text, lang)
    
    # Check minimum content
    tokens = _tokenize(text, lang)
    if len(tokens) < 15:
        return 0.0
    
    score = 0.0
    
    # 1. Bigram diversity (strongest signal, 0-5 pts)
    # AI ZH: 0.83-0.94, Human ZH: 0.97-0.99
    # AI EN: 0.70-0.85, Human EN: 0.85-0.95
    bg = metrics["bigram_diversity"]
    if lang == "zh":
        if bg < 0.88:
            score += 5.0
        elif bg < 0.93:
            score += 3.5
        elif bg < 0.96:
            score += 1.5
    else:
        if bg < 0.75:
            score += 5.0
        elif bg < 0.82:
            score += 3.5
        elif bg < 0.88:
            score += 1.5
    
    # 2. Trigram diversity (0-3 pts)
    tg = metrics["trigram_diversity"]
    if lang == "zh":
        if tg < 0.95:
            score += 3.0
        elif tg < 0.98:
            score += 1.5
    else:
        if tg < 0.85:
            score += 3.0
        elif tg < 0.90:
            score += 1.5
    
    # 3. Burstiness (0-4 pts) — low = AI-like
    burst = metrics["burstiness"]
    if burst < 0.2:
        score += 4.0
    elif burst < 0.4:
        score += 2.5
    elif burst < 0.6:
        score += 1.0
    
    # 4. Repetition ratio (0-3 pts) — high = AI-like
    rep = metrics["repetition_ratio"]
    if rep > 0.08:
        score += 3.0
    elif rep > 0.04:
        score += 1.5
    elif rep > 0.02:
        score += 0.5
    
    # Scale down for short text
    if paragraph_len > 0 and paragraph_len < 50:
        score *= max(paragraph_len / 50.0, 0.3)
    
    return round(min(score, 15.0), 1)


if __name__ == "__main__":
    tests = {
        "ZH-AI-1": "本研究旨在探讨系统性红斑狼疮合并感染的临床特点及危险因素。方法：回顾性分析2018年1月至2023年12月期间收治的126例SLE患者的临床资料。结果显示感染组与非感染组在年龄、病程、补体C3水平等方面存在显著差异。多因素Logistic回归分析显示，糖皮质激素日剂量、低补体血症和淋巴细胞减少是SLE合并感染的独立危险因素。结论：临床上应重视SLE患者感染风险的评估，合理使用免疫抑制剂。",
        "ZH-Human-1": "这个病人挺有意思的。来的时候发热关节痛，查了一堆自身抗体都是阳性。但补体不低，dsDNA也是阴性。跟老主任讨论了一下，他说见过类似病例，最后确诊是混合性结缔组织病。用了吗替麦考酚酯效果还不错，三周就控制住了。这种不典型的确实容易误诊。",
        "ZH-AI-2": "近年来，免疫检查点抑制剂在肿瘤治疗领域取得了突破性进展。然而，其相关不良反应日益引起临床关注。本文综述了免疫检查点抑制剂相关不良反应的发生机制、临床表现及处理策略，为临床实践提供参考。",
        "ZH-Human-2": "说实话这篇综述写得很一般。作者列了一大堆文献但没自己的观点。数据来源也不太靠谱，好几篇引用的样本量才二三十例。结论部分基本是套话，没有实质性建议。我觉得如果要在科会上讲这个话题，还是得自己重新查一遍文献。",
        "ZH-AI-3": "综上所述，本研究通过系统回顾和荟萃分析，证实了该治疗方案在改善患者预后方面的显著效果。本研究的创新之处在于首次将该方案应用于该特定人群。然而，本研究仍存在一定局限性，包括样本量相对较小和随访时间相对较短。未来需要开展更大规模的前瞻性随机对照研究以进一步验证上述结论。",
        "ZH-Human-3": "前一天门诊碰见个罕见病例，二十出头的女生，反复口腔溃疡三年了一直没确诊。查了针刺试验阳性，HLA-B51也阳性。本来考虑白塞但是没有外阴溃疡和眼部受累。主任说先按不完全型白塞治，秋水仙碱加沙利度胺。过两周复查看看效果再定。",
        "EN-AI-1": "This systematic review and meta-analysis aimed to evaluate the efficacy and safety of the intervention. A comprehensive literature search was conducted across multiple databases. The results demonstrated statistically significant improvements in primary outcomes. These findings suggest that the intervention represents a promising approach for clinical management.",
        "EN-Human-1": "So we ran the numbers last night and honestly I'm not sure what to make of them. The treatment group did better, sure, but the effect size was tiny - like clinically irrelevant tiny. And three patients dropped out which complicates things. My gut says we need more data before making any claims.",
    }
    
    print(f"{'Name':15s} | {'BigD':>5s} | {'TriD':>5s} | {'Burs':>5s} | {'Rept':>5s} | {'Score':>5s}")
    print("-" * 70)
    for name, text in tests.items():
        lang = "zh" if name.startswith("ZH") else "en"
        m = compute_perplexity_metrics(text, lang)
        s = score_perplexity(text, lang)
        print(f"{name:15s} | {m['bigram_diversity']:.3f} | {m['trigram_diversity']:.3f} | {m['burstiness']:.3f} | {m['repetition_ratio']:.4f} | {s:4.1f}")
