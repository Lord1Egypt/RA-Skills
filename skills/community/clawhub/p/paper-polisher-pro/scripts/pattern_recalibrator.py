#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pattern_recalibrator — 模式库数据驱动重校准器（Phase 1/3 核心工具）。

用 eval 语料实测每条模式的【人类命中率】与【AI命中率】，按规则自动淘汰/降权误报源。
这是指纹库 v4 "每条模式带 fpr_human 实测值" 的生成器，也是新模型指纹挖掘管线的校准环节。

规则（针对 attack=none 的基线集）：
  DROP   human_hit ≥ 12%                     （人类常用语，误报机器：如裸序号"一、二、三、"）
  DROP   ai_hit < 0.5%                       （死模式，零价值）
  DEMOTE human_hit ≥ 3% 且 lift < 2.0        → weight=1（弱信号，仅组合计分）
  CAP    markdown_format 类别 weight → 2     （一条**加粗**不该值8分）

用法：
  python pattern_recalibrator.py [--corpus ../eval/corpora_small/eval_zh.jsonl] [--apply]
不带 --apply 时只打印报告不动文件。
"""
import os, re, json, argparse, shutil, time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "references")


def compile_pattern(pat):
    """与 ai_detector.match_patterns 相同的编译逻辑。返回 callable(text)->bool 或 None。"""
    try:
        if any(c in pat for c in ".[({"):
            rx = re.compile(pat, re.IGNORECASE)
            return lambda t: bool(rx.search(t))
        pl = pat.lower()
        return lambda t: pl in t.lower()
    except re.error:
        return None


def hit_rates(patterns, docs):
    """patterns: list[str]; docs: list[str]。返回 {pattern: hit_ratio}。"""
    fns = {}
    for p in patterns:
        f = compile_pattern(p)
        if f:
            fns[p] = f
    hits = defaultdict(int)
    for t in docs:
        for p, f in fns.items():
            if f(t):
                hits[p] += 1
    n = max(len(docs), 1)
    return {p: hits.get(p, 0) / n for p in fns}


def recalibrate(lang, humans, ais, apply_changes):
    path = os.path.join(REF, "ai_patterns_%s.json" % lang)
    data = json.load(open(path, encoding="utf-8"))
    cats = data.get("categories", {})
    report = {"dropped": [], "demoted": [], "kept": 0, "md_capped": 0}
    new_cats = {}

    for cname, cdata in cats.items():
        pats = cdata.get("patterns", [])
        weight = cdata.get("weight", 1)
        hr = hit_rates(pats, humans)
        ar = hit_rates(pats, ais)
        keep_pats = []
        for p in pats:
            h, a = hr.get(p, 0.0), ar.get(p, 0.0)
            if h >= 0.12:
                report["dropped"].append((cname, p, round(h, 3), round(a, 3)))
                continue
            if a < 0.005:
                report["dropped"].append((cname, p, round(h, 3), round(a, 3)))
                continue
            keep_pats.append({"p": p, "h": h, "a": a})
        # 类别级降权判定
        new_weight = weight
        if cname == "markdown_format":
            new_weight = 2
            report["md_capped"] += 1
        avg_h = sum(x["h"] for x in keep_pats) / max(len(keep_pats), 1)
        avg_lift = (sum(x["a"] for x in keep_pats) / max(sum(x["h"] for x in keep_pats), 1e-9))
        if len(keep_pats) != len(pats) or new_weight != weight or any(
                x["h"] >= 0.03 and (x["a"] / max(x["h"], 1e-9)) < 2.0 for x in keep_pats):
            pass  # 详情在条目级处理
        # 条目级降权：高人类命中且lift低的单条 → 移入 weak 伪类别或直接降类别权重太粗，
        # 精确做法：把此类条目挪到 "weak_signals" 类别(weight=1)
        weak = [x for x in keep_pats if x["h"] >= 0.03 and (x["a"] / max(x["h"], 1e-9)) < 2.0]
        if weak:
            report["demoted"].extend((cname, x["p"], round(x["h"], 3), round(x["a"], 3)) for x in weak)
            weak_set = {x["p"] for x in weak}
            keep_pats = [x for x in keep_pats if x["p"] not in weak_set]
            new_cats.setdefault("weak_signals", {
                "weight": 1,
                "description": "v3重校准: 人类语料命中3%+且lift<2的弱信号, 仅组合计分(单独命中不足以判AI)",
                "patterns": []})["patterns"].extend(weak_set)
        new_cats[cname] = {"weight": new_weight,
                           "description": cdata.get("description", ""),
                           "patterns": [x["p"] for x in keep_pats]}
        report["kept"] += len(keep_pats)

    print("\n[%s] 淘汰 %d 条 | 降权→weak_signals %d 条 | 保留 %d 条 | markdown限帽 %d" %
          (lang, len(report["dropped"]), len(report["demoted"]), report["kept"], report["md_capped"]))
    print("  淘汰Top(按人类命中率):")
    for c, p, h, a in sorted(report["dropped"], key=lambda x: -x[2])[:12]:
        print("    [%s] human=%.1f%% ai=%.1f%%  %s" % (c, h * 100, a * 100, p[:40]))
    print("  降权Top:")
    for c, p, h, a in sorted(report["demoted"], key=lambda x: -x[2])[:8]:
        print("    [%s] human=%.1f%% ai=%.1f%%  %s" % (c, h * 100, a * 100, p[:40]))

    if apply_changes:
        bak = path + ".bak." + time.strftime("%Y%m%d")
        if not os.path.exists(bak):
            shutil.copy(path, bak)
        total = sum(len(c["patterns"]) for c in new_cats.values())
        out = {"version": "4.0.0", "description": "v3数据驱动重校准版 (基线语料实测FPR过滤)",
               "recalibration": {"date": time.strftime("%Y-%m-%d"),
                                 "corpus": "eval/corpora_small/eval_zh.jsonl",
                                 "humans": len(humans), "ais": len(ais),
                                 "dropped": len(report["dropped"]),
                                 "demoted": len(report["demoted"])},
               "categories": new_cats}
        json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("  ✅ 已写入 %s (共 %d 条, 备份 %s)" % (os.path.basename(path), total, os.path.basename(bak)))
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=os.path.join(HERE, "..", "eval", "corpora_small", "eval_zh.jsonl"))
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    recs = [json.loads(l) for l in open(a.corpus, encoding="utf-8") if l.strip()]
    recs = [r for r in recs if r.get("attack") == "none"]
    humans = [r["text"] for r in recs if r["label"] == 0]
    ais = [r["text"] for r in recs if r["label"] == 1]
    print("校准语料: human=%d ai=%d (来源 %s)" % (len(humans), len(ais), a.corpus))
    recalibrate("zh", humans, ais, a.apply)


if __name__ == "__main__":
    main()
