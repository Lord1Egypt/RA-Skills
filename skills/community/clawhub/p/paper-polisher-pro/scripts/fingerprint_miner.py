#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fingerprint_miner — 模型指纹自动挖掘管线（Phase 3 核心）。

对一个模型的语料 vs 人类语料:
  1. 候选生成: 字符 n-gram(3-6字) + 连接短语, 按模型内覆盖率初筛
  2. 对比排序: lift = 模型覆盖率 / (人类覆盖率+ε), 过滤 fpr_human>8%
  3. 入库: top-K 写入 references/model_fingerprints.json (registry, 带元数据)
          并注入 ai_patterns_zh.json 的 fingerprint_<model> 类别 (引擎直接受益)

⚠️ 只在 calib 半挖掘, test 半留给最终评测（防泄漏）。
用法:
  python fingerprint_miner.py --corpus <jsonl> --model deepseek-r1 [--k 12] [--apply]
  python fingerprint_miner.py --corpus glm53_samples.jsonl --model glm-5.3 \
      --humans <local_corpus> --sampled-via "self:GLM-5.3(agent)" [--apply]
"""
import os, re, sys, json, argparse, time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pp_split import filter_split

REG_PATH = os.path.join(HERE, "..", "references", "model_fingerprints.json")
PAT_PATH = os.path.join(HERE, "..", "references", "ai_patterns_zh.json")


def ngrams(text, n_list=(3, 4, 5, 6)):
    out = set()
    for run in re.findall(r"[\u4e00-\u9fff]+", text):
        for n in n_list:
            if len(run) >= n:
                out.update(run[i:i + n] for i in range(len(run) - n + 1))
    return out


def mine(model_docs, human_docs, k=12, min_cov=0.15, max_fpr=0.08):
    m_cnt, h_cnt = Counter(), Counter()
    m_n, h_n = len(model_docs), len(human_docs)
    for t in model_docs:
        m_cnt.update(ngrams(t))
    for t in human_docs:
        h_cnt.update(ngrams(t))
    cands = []
    for g, c in m_cnt.items():
        cov = c / m_n
        if cov < min_cov:
            continue
        fpr = h_cnt.get(g, 0) / h_n
        if fpr > max_fpr:
            continue
        lift = cov / (fpr + 0.01)
        if lift >= 2.0:
            cands.append((g, round(cov, 3), round(fpr, 3), round(lift, 2)))
    cands.sort(key=lambda x: (-x[3], -x[1]))
    # 去重叠: 已选模式是新模式的子串则跳过
    picked = []
    for c in cands:
        if any(c[0] in p[0] or p[0] in c[0] for p in picked):
            continue
        picked.append(c)
        if len(picked) >= k:
            break
    return picked


def weight_of(lift):
    return 4 if lift >= 3 else (3 if lift >= 2.5 else 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True, help="该模型的AI语料jsonl(或含多模型,配--model过滤)")
    ap.add_argument("--model", required=True)
    ap.add_argument("--humans", default=None, help="人类对照语料(默认取corpus内label=0)")
    ap.add_argument("--k", type=int, default=12)
    ap.add_argument("--sampled-via", default="", help="采样通道(如 glm-5.2-route / self:GLM-5.3)")
    ap.add_argument("--versions", default="", help="逗号分隔版本标签")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    def load(path):
        recs = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
        return [r for r in recs if r.get("attack", "none") == "none"]

    corpus = load(a.corpus)
    ai_docs = [r["text"] for r in filter_split(corpus, "calib")
               if r["label"] == 1 and (r.get("model") == a.model or a.model in r.get("model", ""))]
    if a.humans:
        hrecs = filter_split(load(a.humans), "calib")
        human_docs = [r["text"] for r in hrecs if r["label"] == 0]
    else:
        human_docs = [r["text"] for r in filter_split(corpus, "calib") if r["label"] == 0]
    print("模型=%s  ai_docs=%d  human_docs=%d" % (a.model, len(ai_docs), len(human_docs)))
    if len(ai_docs) < 5:
        print("  [skip] 样本不足(最小5)")
        return

    picked = mine(ai_docs, human_docs, k=a.k)
    if not picked:
        print("  [skip] 无满足条件的模式")
        return
    for g, cov, fpr, lift in picked:
        print("  cov=%.0f%% fpr_h=%.1f%% lift=%.1f w=%d  %s" %
              (cov * 100, fpr * 100, lift, weight_of(lift), g))

    if a.apply:
        reg = {"version": "4.0", "families": {}}
        if os.path.exists(REG_PATH):
            reg = json.load(open(REG_PATH, encoding="utf-8"))
        fam = reg["families"].setdefault(a.model, {"versions": [], "sampled_via": "",
                                                   "patterns": [], "sampled_docs": 0})
        if a.versions:
            for v in a.versions.split(","):
                if v and v not in fam["versions"]:
                    fam["versions"].append(v)
        if a.sampled_via:
            fam["sampled_via"] = a.sampled_via
        fam["sampled_docs"] = fam.get("sampled_docs", 0) + len(ai_docs)
        fam["mined_at"] = time.strftime("%Y-%m-%d")
        fam["patterns"] = [{"p": g, "w": weight_of(lift), "cov_model": cov,
                            "fpr_human": fpr, "lift": lift} for g, cov, fpr, lift in picked]
        json.dump(reg, open(REG_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

        pats = json.load(open(PAT_PATH, encoding="utf-8"))
        cat = "fingerprint_" + re.sub(r"[^a-z0-9]+", "_", a.model.lower()).strip("_")
        pats["categories"][cat] = {
            "weight": 3,
            "description": "v4挖掘: %s (mined %s via %s)" % (a.model, fam["mined_at"], a.sampled_via or "corpus"),
            "patterns": [p["p"] for p in fam["patterns"]]}
        json.dump(pats, open(PAT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("  ✅ registry + ai_patterns 已更新 (cat=%s)" % cat)


if __name__ == "__main__":
    main()
