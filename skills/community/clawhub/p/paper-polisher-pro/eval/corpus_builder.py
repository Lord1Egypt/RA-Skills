#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corpus_builder — Phase 0 评测语料构建器。

把公开评测集归一化为统一格式，供 run_eval.py 使用：
  C-ReD       (ACL 2026 Findings, 5域×9生成器+human, CSV)
  DetectRL-ZH (NLPCC 2025 Task1, 3域×3生成器+human, train常规/test对抗)

统一记录 schema（label: 1=AI生成, 0=人类）：
  {"id","text","label","model","domain","source","attack","is_medical","length"}

⚠️ 关键事实：C-ReD 原始标签 1=human / 0=AI（与其他集相反），本脚本统一翻转。

用法：
  python corpus_builder.py --cred-dir <C-ReD目录> --detectrl-dir <DetectRL目录> \
                           --out ../eval/corpora_small [--per-cell 30] [--adv-n 400]
"""
import os, csv, json, hashlib, argparse, random

random.seed(42)
MIN_LEN, MAX_LEN, STORE_CAP = 100, 4000, 2000


def text_id(t):
    return hashlib.md5(t.encode("utf-8")).hexdigest()[:12]


def norm(rec):
    """过滤+截断+规范化一条记录。"""
    t = (rec.get("text") or "").strip()
    if not (MIN_LEN <= len(t) <= MAX_LEN):
        return None
    stored = t if len(t) <= STORE_CAP else t[:STORE_CAP]
    return {"id": text_id(t), "text": stored, "label": int(rec["label"]),
            "model": rec.get("model", ""), "domain": rec.get("domain", ""),
            "source": rec.get("source", ""), "attack": rec.get("attack", "none"),
            "is_medical": bool(rec.get("is_medical", False)), "length": len(t)}


def load_cred(d):
    """C-ReD CSV → 记录。注意翻转标签(原1=human→0, 原0=ai→1)。"""
    out = []
    bd = os.path.join(d, "benchmark data")
    for domain in sorted(os.listdir(bd)):
        dp = os.path.join(bd, domain)
        if not os.path.isdir(dp):
            continue
        for fn in sorted(os.listdir(dp)):
            if not fn.endswith(".csv"):
                continue
            model = fn.replace(".csv", "").split("_")[-1]
            try:
                with open(os.path.join(dp, fn), encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        raw = (row.get("label") or "").strip()
                        if raw not in ("0", "1"):
                            continue
                        label = 1 - int(raw)  # 翻转: C-ReD 0=AI → 我们 1=AI
                        out.append(norm({"text": row.get("text", ""), "label": label,
                                         "model": model, "domain": domain,
                                         "source": "C-ReD",
                                         "is_medical": (model == "human" and domain == "paper")}))
            except Exception as e:
                print("  [warn] %s/%s: %s" % (domain, fn, e))
    return [r for r in out if r]


def load_detectrl(d):
    out = []
    # train/dev: 常规(含model字段)
    for fn, attack in (("train.json", "none"), ("dev.json", "none")):
        p = os.path.join(d, "data", fn)
        if not os.path.exists(p):
            continue
        data = json.load(open(p, encoding="utf-8"))
        for x in data:
            model = x.get("model", "unknown")
            out.append(norm({"text": x.get("text", ""), "label": x.get("label", -1),
                             "model": model, "domain": x.get("source", fn.replace(".json", "")),
                             "source": "DetectRL",
                             "is_medical": (model == "human" and x.get("source") == "csl")}))
    # test_with_label: 对抗集(无model信息, 均衡)
    p = os.path.join(d, "data", "test_with_label.json")
    if os.path.exists(p):
        for x in json.load(open(p, encoding="utf-8")):
            out.append(norm({"text": x.get("text", ""), "label": x.get("label", -1),
                             "model": "unknown-adversarial", "domain": "mixed",
                             "source": "DetectRL-adv", "attack": "adversarial",
                             "is_medical": False}))
    return [r for r in out if r]


def stratified(records, per_cell, adv_n):
    """分层抽样: 每 (source,model,domain,attack) 格子取 per_cell 条; 对抗集单独 adv_n 条均衡。"""
    cells = {}
    adv_pool = {0: [], 1: []}
    for r in records:
        key = (r["source"], r["model"], r["domain"], r["attack"])
        cells.setdefault(key, []).append(r)
        if r["attack"] == "adversarial":
            adv_pool[r["label"]].append(r)
    picked, seen = [], set()
    for key in sorted(cells):
        pool = [r for r in cells[key] if r["id"] not in seen]
        random.shuffle(pool)
        take = adv_n if key[3] == "adversarial" else per_cell
        for r in pool[:take]:
            picked.append(r)
            seen.add(r["id"])
    return picked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cred-dir", required=True)
    ap.add_argument("--detectrl-dir", required=True)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "corpora_small"))
    ap.add_argument("--per-cell", type=int, default=30)
    ap.add_argument("--adv-n", type=int, default=400)
    a = ap.parse_args()

    print("[1/3] 加载 C-ReD ...")
    cred = load_cred(a.cred_dir)
    print("      有效记录:", len(cred))
    print("[2/3] 加载 DetectRL-ZH ...")
    drl = load_detectrl(a.detectrl_dir)
    print("      有效记录:", len(drl))
    print("[3/3] 分层抽样 per_cell=%d adv_n=%d ..." % (a.per_cell, a.adv_n))
    final = stratified(cred + drl, a.per_cell, a.adv_n)

    os.makedirs(a.out, exist_ok=True)
    outp = os.path.join(a.out, "eval_zh.jsonl")
    with open(outp, "w", encoding="utf-8") as f:
        for r in final:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # 统计
    from collections import Counter
    by_src = Counter((r["source"], r["model"]) for r in final)
    n_ai = sum(1 for r in final if r["label"] == 1)
    n_hu = len(final) - n_ai
    n_med_hu = sum(1 for r in final if r["label"] == 0 and r["is_medical"])
    n_adv = sum(1 for r in final if r["attack"] == "adversarial")
    print("\n输出: %s  (%d 条, %.1f MB)" % (outp, len(final),
          os.path.getsize(outp) / 1048576))
    print("  AI=%d  human=%d  (human医学子集=%d, 对抗集=%d)" % (n_ai, n_hu, n_med_hu, n_adv))
    print("  来源×模型:")
    for k, v in sorted(by_src.items()):
        print("    %-28s %d" % ("/".join(k), v))


if __name__ == "__main__":
    main()
