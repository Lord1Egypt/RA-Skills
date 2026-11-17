#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补测两个评测欠账: ①医学人类@high误报 ②段落级归因AUROC。"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import ai_detector
from pp_split import filter_split

CORPUS = ""  # 必填: 经 --corpus 传入本地语料路径
fc = json.load(open(os.path.join(HERE, "..", "references", "fusion_config.json"), encoding="utf-8"))
TM = float(fc["thresholds"]["medium"]) * 100
TH = float(fc["thresholds"]["high"]) * 100
print("阈值: medium=%.1f high=%.1f" % (TM, TH))

# ── ① 医学人类 @med/@high 单独测 (用文档级缓存分数) ──
if not CORPUS:
    raise SystemExit("缺少语料路径: 请在脚本顶部 CORPUS 常量填入本地语料 jsonl 路径")
recs = [json.loads(l) for l in open(CORPUS, encoding="utf-8") if l.strip()]
recs = [r for r in recs if r.get("attack") == "none"]
test = filter_split(recs, "test")
cache = json.load(open(os.path.join(HERE, "results", "score_cache.json"), encoding="utf-8"))
med = [cache.get("current:" + r["id"]) for r in test if r["label"] == 0 and r.get("is_medical")]
med = [s for s in med if s is not None]
gen = [cache.get("current:" + r["id"]) for r in test if r["label"] == 0 and not r.get("is_medical")]
gen = [s for s in gen if s is not None]
print("\n[1] 医学人类文本单独误报 (test半, n=%d):" % len(med))
print("    @medium: %.1f%%  (%d/%d)" % (100 * sum(1 for s in med if s >= TM) / max(len(med), 1),
                                        sum(1 for s in med if s >= TM), len(med)))
print("    @high  : %.1f%%  (%d/%d)" % (100 * sum(1 for s in med if s >= TH) / max(len(med), 1),
                                        sum(1 for s in med if s >= TH), len(med)))
print("    对照-一般人类 (n=%d): @high %.1f%%" % (len(gen),
      100 * sum(1 for s in gen if s >= TH) / max(len(gen), 1)))

# ── ② 段落级归因独立AUROC ──
print("\n[2] 段落级归因评测 (blended=0.5*模式+0.5*谱, test半每文档取前2段):")
import layers_surface as LS
import random
random.seed(11)
cats = ai_detector.load_patterns("zh")


def para_pairs(doc_list, cap):
    out = []
    random.shuffle(doc_list)
    for r in doc_list:
        if len(out) >= cap:
            break
        for p in ai_detector.split_paragraphs(r["text"])[:2]:
            if len(p) < 60:
                continue
            base = ai_detector.score_paragraph(p, "zh", cats).ai_score
            spec = LS.spectrum_layer(p)["score"] * 10.0
            out.append((0.5 * base + 0.5 * spec, r["label"], r["source"], r.get("model", "")))
    return out


hu_docs = [r for r in test if r["label"] == 0]
ai_docs = [r for r in test if r["label"] == 1]
hp = para_pairs(hu_docs, 450)
ap_ = para_pairs(ai_docs, 450)
pairs = [(s, l) for s, l, _, _ in hp + ap_]
per_src = {}
for s, l, src, m in hp + ap_:
    per_src.setdefault(src + ("/ai:" + m if l else "/hu"), []).append(s)


def auroc(pl):
    pos = [s for s, l in pl if l == 1]
    neg = [s for s, l in pl if l == 0]
    if not pos or not neg:
        return None
    ranked = sorted(pl, key=lambda x: x[0])
    ranks, i = {}, 0
    while i < len(ranked):
        j = i
        while j < len(ranked) and ranked[j][0] == ranked[i][0]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[id(ranked[k])] = avg
        i = j
    n1, n0 = len(pos), len(neg)
    sp = sum(ranks[id(p)] for p in ranked if p[1] == 1)
    return round((sp - n1 * (n1 + 1) / 2) / (n1 * n0), 4)


print("    段落样本: %d (AI %d / 人类 %d)" %
      (len(pairs), sum(1 for _, l in pairs if l == 1), sum(1 for _, l in pairs if l == 0)))
print("    段落级 AUROC: %s" % auroc(pairs))
hu_scores = [s for s, l, _, _ in hp]
print("    段落级人类误报: @med %.1f%% @high %.1f%%" %
      (100 * sum(1 for s in hu_scores if s >= TM) / max(len(hu_scores), 1),
       100 * sum(1 for s in hu_scores if s >= TH) / max(len(hu_scores), 1)))
for k in sorted(per_src)[:14]:
    print("      %s: n=%d 均分%.1f" % (k, len(per_src[k]), sum(per_src[k]) / len(per_src[k])))
# 混合文档段落级(构造: test半人类段+AI段交错, 真实标签已知)
print("\n    构造混合文档段落级(人类段/AI段交错, 标签已知):")
mixed_pairs = []
for i in range(min(len(hp), len(ap_), 100)):
    mixed_pairs += [hp[i][:2], ap_[i][:2]]
m_hu = [s for s, l in mixed_pairs if l == 0]
m_ai = [s for s, l in mixed_pairs if l == 1]
print("      段落数: %d (人%d/AI%d) | AI段≥high: %.0f%% | 人类段<high: %.0f%%" %
      (len(mixed_pairs), len(m_hu), len(m_ai),
       100 * sum(1 for s in m_ai if s >= TH) / max(len(m_ai), 1),
       100 * sum(1 for s in m_hu if s < TH) / max(len(m_hu), 1)))
print("      混合场景段落级 AUROC: %s" % auroc(mixed_pairs))
