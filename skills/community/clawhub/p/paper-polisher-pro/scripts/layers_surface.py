#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layers_surface — v3 新增零模型检测层（EnsemJudge 配方，纯Python统计）。

L9 surface_layer   表面统计：双换行率(LLM高)/逗号分句密度(人类高)/重复标点(人类特征)/句长分布
L10 spectrum_layer 词频谱对比：CommonToken——文本token频率与"AI-人类差谱"的相关性
L11 cot_layer      思维链特征：逻辑连接词密度/段落均匀度/解释-结论句式/思维链泄漏（R1/V4-Pro一代）

每层输出 0-10 分（10=强AI特征）。频谱文件由 build_spectrum.py 从评测语料生成。
依据：NLPCC2025 中文检测冠军 EnsemJudge（arXiv:2603.27949）规则层 + C-ReD（arXiv:2604.11796）。
"""
import os, re, json
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SPECTRUM_PATH = os.path.join(HERE, "..", "references", "token_spectrum_zh.json")

# ── L9 表面统计层 ──
_DUP_PUNCT = re.compile(r"([。，、；！？，])\1{1,}")


def surface_layer(text: str) -> dict:
    """文档级表面统计。返回 {score(0-10), features}。"""
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    lines = [p for p in text.split("\n") if p.strip()]
    # 双换行率: LLM 几乎总用空行分段；人类随手写常单换行/不分段
    dbl_rate = 0.0
    if len(paras) >= 2:
        dbl = len(re.findall(r"\n\s*\n", text))
        dbl_rate = min(dbl / max(len(paras) - 1, 1), 1.0)
    # 逗号分句密度: 人类逗号:句号 比更高（口语化长句）
    commas = text.count("，") + text.count(",")
    periods = text.count("。") + text.count("．") + text.count(".")
    comma_ratio = commas / max(commas + periods, 1)
    # 重复标点(。。,,!!): 人类打字特征, LLM 几乎不出现 → 出现=人类信号(负分)
    dup_punct = len(_DUP_PUNCT.findall(text))
    # 全角标点占比（中文文本里半角标点多是AI或机翻痕迹之一）
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    half = len(re.findall(r"[,;:!?()]", text))
    full = len(re.findall(r"[，；：！？（）]", text))
    half_ratio = half / max(half + full, 1)

    score = 0.0
    score += min(dbl_rate, 1.0) * 3.0                     # 双换行习惯
    score += max(0, (comma_ratio - 0.35)) * 10.0 * 0.0    # 逗号比人类高→负贡献,放防误报区
    score -= min(dup_punct, 3) * 1.5                      # 重复标点=人类
    if cjk > 50:
        score += min(half_ratio * 8.0, 3.0)               # 半角标点混用
    score = max(0.0, min(10.0, score))
    return {"score": round(score, 2),
            "features": {"dbl_para_rate": round(dbl_rate, 3),
                         "comma_ratio": round(comma_ratio, 3),
                         "dup_punct": dup_punct,
                         "half_punct_ratio": round(half_ratio, 3)}}


# ── L10 词频谱对比层 ──
_spectrum_cache = None


def _load_spectrum():
    global _spectrum_cache
    if _spectrum_cache is None:
        try:
            data = json.load(open(SPECTRUM_PATH, encoding="utf-8"))
            _spectrum_cache = data.get("tokens", {})
        except Exception:
            _spectrum_cache = {}
    return _spectrum_cache


def _zh_tokens(text):
    toks = []
    for run in re.findall(r"[\u4e00-\u9fff]+", text):
        if len(run) == 1:
            toks.append(run)
        else:
            toks.extend(run[i:i + 2] for i in range(len(run) - 1))
    toks.extend(w for w in re.findall(r"[a-zA-Z]{2,}", text.lower()))
    return toks


def spectrum_layer(text: str) -> dict:
    """与 AI-人类 token 频率差谱的相关性。返回 {score(0-10), top_tokens}。"""
    spec = _load_spectrum()
    if not spec:
        return {"score": 0.0, "top_tokens": []}
    toks = _zh_tokens(text)
    if not toks:
        return {"score": 0.0, "top_tokens": []}
    cnt = Counter(t for t in toks if t in spec)
    total = sum(cnt.values())
    if total == 0:
        return {"score": 0.0, "top_tokens": []}
    # 频率加权平均 lift（AI高频token占比越高分越高）
    weighted = sum(spec[t] * c for t, c in cnt.items()) / total
    # lift 谱典型范围 [-1,+1]，映射到 0-10
    score = max(0.0, min(10.0, (weighted + 0.5) * 10.0))
    top = sorted(cnt.items(), key=lambda x: -spec[x[0]])[:5]
    return {"score": round(score, 2),
            "top_tokens": [(t, round(spec[t], 2), c) for t, c in top]}


# ── L11 思维链特征层 ──
_COT_CONN = re.compile(r"因此|所以|由此|这意味着|这表明|总的来说|综上所述|换言之|简而言之|可以看出")
_COT_EXPLAIN = re.compile(r"这(表明|意味着|说明|提示|反映了)|可以(看出|发现)|值得(注意的是|关注的是)")
_THINK_LEAK = re.compile(r"首先[^。]{0,8}需要|让我们|我们来看|接下来我们|我们来分析|第一步[^。]{0,10}准备")


def cot_layer(text: str) -> dict:
    """R1/V4-Pro 一代思维链模型特征。返回 {score(0-10), features}。"""
    sents = re.split(r"[。！？!?]", text)
    n_sent = max(len([s for s in sents if s.strip()]), 1)
    conn_hits = len(_COT_CONN.findall(text))
    explain_hits = len(_COT_EXPLAIN.findall(text))
    leak_hits = len(_THINK_LEAK.findall(text))
    conn_density = conn_hits / n_sent
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    para_cv = 0.0
    if len(paras) >= 4:
        lens = [len(p) for p in paras]
        mean = sum(lens) / len(lens)
        para_cv = (sum((x - mean) ** 2 for x in lens) / len(lens)) ** 0.5 / max(mean, 1)

    score = 0.0
    score += min(conn_density * 12.0, 4.0)          # 逻辑连接词密度
    score += min(explain_hits * 1.2, 3.0)           # 解释-结论句式
    score += min(leak_hits * 2.5, 5.0)              # 思维链泄漏(强信号)
    if para_cv > 0:                                  # 段落异常均匀
        score += max(0.0, (0.25 - para_cv)) * 8.0
    score = max(0.0, min(10.0, score))
    return {"score": round(score, 2),
            "features": {"conn_density": round(conn_density, 3),
                         "explain_hits": explain_hits,
                         "think_leak": leak_hits,
                         "para_cv": round(para_cv, 3)}}


# ── L13 surprisal-variation 层（v3.9.0，DivEye 思路的本地化实现）──
# 原理：人类写作的"意外度"（surprisal≈token 频率 lift 的负向）在窗口间波动大；
# AI 生成倾向平滑。用滑动窗口的频谱 lift 变异系数(CV)刻画——纯标准库、可复现。
_WIN = 60  # 滑窗 token 数


def surprisal_variation_layer(text: str) -> dict:
    """滑窗频谱 lift 的变异系数。返回 {score(0-10), cv, n_windows, verdict}。
    score 高=变化性低=更像 AI 平滑生成（DivEye: diversity boosts detection）。"""
    spec = _load_spectrum()
    toks = _zh_tokens(text)
    if not spec or not toks:
        return {"score": 0.0, "cv": None, "n_windows": 0, "verdict": "insufficient"}
    known = [t for t in toks if t in spec]
    # v3.9.0 调优: 谱覆盖率过低(C<40%)的文本 lift 估计噪声大——
    # 实测 3 篇人类误伤样本 known 比率 27-36%, 均为文学/演讲体; 正常 AI/人类样本 ≥60%
    coverage = len(known) / max(len(toks), 1)
    if len(known) < _WIN * 2 or coverage < 0.35:
        return {"score": 0.0, "cv": None, "n_windows": 0, "verdict": "insufficient", "coverage": round(coverage, 2)}
    lifts = [spec[t] for t in known]
    wins = [sum(lifts[i:i + _WIN]) / _WIN for i in range(0, len(lifts) - _WIN + 1, _WIN // 2)]
    if len(wins) < 4:
        return {"score": 0.0, "cv": None, "n_windows": len(wins), "verdict": "insufficient"}
    mean = sum(wins) / len(wins)
    var = sum((w - mean) ** 2 for w in wins) / len(wins)
    cv = (var ** 0.5) / abs(mean) if mean else 0.0
    # CV 低=平滑=AI 特征强。学术人类 CV 实测分布与 AI 差异见 eval/results/v390_*.json
    # 映射（保守线性，CV<0.05 → 10 分；CV>0.25 → 0 分）
    score = max(0.0, min(10.0, (0.25 - cv) / 0.20 * 10.0))
    # 证据折扣: coverage<0.55 时线性降权(谱覆盖不足=区分力弱, 宁可少说)
    score *= min(1.0, coverage / 0.55)
    verdict = "smooth" if score >= 6 else ("human" if score <= 3 else "mixed")
    return {"score": round(score, 2), "cv": round(cv, 4),
            "n_windows": len(wins), "verdict": verdict, "coverage": round(coverage, 2)}


def all_surface_layers(text: str) -> dict:
    """一次算齐四层，供 detect() 融合。"""
    return {"surface": surface_layer(text),
            "spectrum": spectrum_layer(text),
            "cot": cot_layer(text),
            "surprisal": surprisal_variation_layer(text)}
