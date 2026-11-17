#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_leak.py — 训练集/评测集污染审计（v4.4.0 数据卫生闸）

背景（2026-10-03 v36 事故）：v36 再训练把 285 篇「当打代新鲜样本」直接取自评测集
eval_gen2026.jsonl 本身，导致 gen2026 评测集 64.6%（286/443）、oldgen 语料 41.6%
（953/2290）的文档进入训练集——0.9994 的 AUROC 是背书不是泛化，全部数字作废。
本工具把这类污染变成发布前必过的机器闸：训练集与评测集的交集必须为零。

判据：归一化（去全部空白字符）后前 400/200 字符 md5 精确匹配（双窗口防截断差异）。
阈值：任一评测文档命中训练集即 FAIL（exit 1）——训练绝不允许吞评测文档。

用法：
  python eval/check_leak.py --train ~/.pp_train/train_v36.jsonl                # 单训练集
  python eval/check_leak.py --train a.jsonl --train b.jsonl --json out.json    # 多训练集+落档
  python eval/check_leak.py --train t.jsonl --corpora my_eval.jsonl            # 自定评测集
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CORPORA = [
    os.path.join(HERE, "corpora_small", "eval_zh.jsonl"),
    os.path.join(HERE, "corpora_small", "eval_gen2026.jsonl"),
    os.path.join(HERE, "corpora_small", "attacks.jsonl"),
]


def norm_hash(text, n):
    return hashlib.md5("".join(text.split())[:n].encode("utf-8")).hexdigest()


def load_jsonl(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", action="append", required=True,
                    help="训练集 jsonl（可重复传多个）")
    ap.add_argument("--corpora", action="append", default=None,
                    help="评测集 jsonl（默认 corpora_small 三件）")
    ap.add_argument("--json", dest="json_out", default=None,
                    help="审计结果落档路径")
    a = ap.parse_args()

    corpora = a.corpora or DEFAULT_CORPORA
    train_sets = {}
    for tp in a.train:
        rows = load_jsonl(tp)
        train_sets[os.path.basename(tp)] = {
            "rows": len(rows),
            "h400": set(norm_hash(r["t"], 400) for r in rows),
            "h200": set(norm_hash(r["t"], 200) for r in rows),
        }

    leaked = 0
    report = {"train": {k: {"rows": v["rows"]} for k, v in train_sets.items()},
              "corpora": []}
    print("═" * 62)
    print("训练/评测污染审计（判据：归一化前 400/200 字符 md5 精确匹配）")
    for tp in train_sets:
        print("  训练集 %-22s %d 行" % (tp, train_sets[tp]["rows"]))
    print("─" * 62)
    for cp in corpora:
        recs = load_jsonl(cp)
        per_train = {}
        for tname, ts in train_sets.items():
            hits = [r for r in recs
                    if norm_hash(r["text"], 400) in ts["h400"]
                    or norm_hash(r["text"], 200) in ts["h200"]]
            per_train[tname] = {
                "hits": len(hits),
                "rate": round(len(hits) / max(len(recs), 1), 4),
                "by_label": {str(lb): sum(1 for h in hits if h.get("label") == lb)
                             for lb in {h.get("label") for h in hits}},
                "by_split": {},
            }
            try:
                sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
                from pp_split import filter_split
                for half in ("calib", "test"):
                    hs = [r for r in hits if r in filter_split(recs, half)]
                    per_train[tname]["by_split"][half] = len(hs)
            except Exception:
                pass
            leaked += len(hits)
        worst = max(v["rate"] for v in per_train.values())
        report["corpora"].append({"corpus": os.path.basename(cp), "n": len(recs),
                                  "per_train": per_train})
        for tname, v in per_train.items():
            mark = "LEAK" if v["hits"] else "clean"
            print("  %-22s vs %-22s 命中 %4d/%4d (%.1f%%) %s %s" % (
                os.path.basename(cp), tname, v["hits"], len(recs),
                100 * v["rate"], mark,
                ("split=" + str(v["by_split"])) if v["by_split"] else ""))
    print("─" * 62)
    verdict = "FAIL（%d 篇评测文档泄漏进训练集——数字不可信）" % leaked if leaked \
        else "PASS（训练集与评测集零交集）"
    print("审计结论:", verdict)
    if a.json_out:
        report["leaked_total"] = leaked
        report["verdict"] = verdict
        json.dump(report, open(a.json_out, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("审计档: %s" % a.json_out)
    sys.exit(1 if leaked else 0)


if __name__ == "__main__":
    main()
