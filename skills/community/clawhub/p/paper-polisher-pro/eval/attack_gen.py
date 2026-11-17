#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
attack_gen — Phase 0 对抗攻击样本生成器。

用 skill 自带资源做规则级攻击（常见规则级改写扰动（评测语料生成））：
  paraphrase : synonyms_general.json 同义词替换（替换率~35%）+ 相邻句序打乱（30%句子）
  mixed      : 人类段落 + AI 段落 50/50 拼接（模拟人机混写）

自我红队原则：本 skill 的去AI化改写能力，就是检测器必须扛住的攻击。

用法：
  python attack_gen.py --corpus corpora_small/eval_zh.jsonl --out corpora_small/attacks.jsonl \
                       [--n-per-model 25]
"""
import os, json, random, re, argparse

random.seed(2026)
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "references")

_SENT_SPLIT = re.compile(r"(?<=[。！？!?；;])")


def load_synonyms():
    data = json.load(open(os.path.join(REF, "synonyms_general.json"), encoding="utf-8"))
    pairs = []
    for k, alts in (data.get("general") or {}).items():
        if len(k) >= 2 and alts:
            pairs.append((k, [a for a in alts if a and a != k]))
    return pairs


def paraphrase(text, syn_pairs):
    """同义词替换 + 相邻句交换。返回 (新文本, 替换次数)."""
    hits = 0
    for k, alts in syn_pairs:
        if k in text and random.random() < 0.5:
            text = text.replace(k, random.choice(alts))
            hits += 1
    sents = [s for s in _SENT_SPLIT.split(text) if s.strip()]
    for i in range(len(sents) - 1):
        if random.random() < 0.3:
            sents[i], sents[i + 1] = sents[i + 1], sents[i]
    return "".join(sents), hits


def mix_doc(ai_paras, hu_paras):
    """人机段落交错拼接。"""
    n = min(len(ai_paras), len(hu_paras))
    if n == 0:
        return None
    out = []
    for i in range(n):
        out.append(hu_paras[i] if i % 2 == 0 else ai_paras[i])
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=os.path.join(HERE, "corpora_small", "eval_zh.jsonl"))
    ap.add_argument("--out", default=os.path.join(HERE, "corpora_small", "attacks.jsonl"))
    ap.add_argument("--n-per-model", type=int, default=25)
    a = ap.parse_args()

    recs = [json.loads(l) for l in open(a.corpus, encoding="utf-8") if l.strip()]
    syn = load_synonyms()
    print("同义词组: %d" % len(syn))

    ai_by_model, humans = {}, []
    for r in recs:
        if r["attack"] != "none":
            continue
        if r["label"] == 1:
            ai_by_model.setdefault(r["model"], []).append(r)
        else:
            humans.append(r)

    out = []
    # paraphrase 攻击: 每模型 n 条
    for model, pool in sorted(ai_by_model.items()):
        random.shuffle(pool)
        for r in pool[:a.n_per_model]:
            new, hits = paraphrase(r["text"], syn)
            if abs(len(new) - len(r["text"])) > len(r["text"]) * 0.5 or hits == 0:
                continue  # 攻击强度过低的不算
            out.append({"id": r["id"] + "-para", "text": new, "label": 1,
                        "model": model, "domain": r["domain"], "source": r["source"],
                        "attack": "paraphrase", "is_medical": False,
                        "length": len(new), "base_id": r["id"], "syn_hits": hits})
    # mixed 攻击: 取AI池前n, 与人类段落交错
    made = 0
    random.shuffle(humans)
    for model, pool in sorted(ai_by_model.items()):
        for r in pool:
            if made >= a.n_per_model * 3:
                break
            hu = humans[made % len(humans)]
            paras_ai = [p for p in r["text"].split("\n") if p.strip()][:3]
            paras_hu = [p for p in hu["text"].split("\n") if p.strip()][:3]
            doc = mix_doc(paras_ai, paras_hu)
            if not doc or len(doc) < 150:
                continue
            out.append({"id": r["id"] + "-mix", "text": doc, "label": 1,
                        "model": model, "domain": r["domain"], "source": r["source"],
                        "attack": "mixed", "is_medical": False,
                        "length": len(doc), "base_id": r["id"]})
            made += 1

    with open(a.out, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    from collections import Counter
    print("输出: %s (%d 条)" % (a.out, len(out)))
    print("  攻击类型:", dict(Counter(r["attack"] for r in out)))
    print("  覆盖模型:", dict(Counter(r["model"] for r in out)))


if __name__ == "__main__":
    main()
