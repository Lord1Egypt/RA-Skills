#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把一个客户 Excel 文件分类到三个标准模板之一。

用法:
    python classify_form.py <文件1> [<文件2> ...] [--json]

输出每个文件的：各模板得分、判定结果、置信度、判定依据（命中的关键词/结构信号）。
脚本只“建议”，最终由 OpenClaw agent 复核——置信度低或得分接近时务必让 agent 看实际内容再定。
"""
from __future__ import annotations
import sys, os, json, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_forms import load_schema, read_any, norm_text, parse_date_header, is_probably_non_date


def gather_text(rows, top=6):
    """收集前 top 行的所有单元格文本（表头通常在这里）。"""
    blob = []
    for r in rows[:top]:
        for c in r:
            if c is not None:
                blob.append(norm_text(c))
    return blob


def count_date_cols(rows, top=6):
    """估算横向日期列数量（取前 top 行里日期表头最多的一行）。"""
    best = 0
    for r in rows[:top]:
        n = 0
        for c in r:
            if is_probably_non_date(c):
                continue
            d = parse_date_header(c, allow_serial=True)
            if d and d.get("kind") in ("day", "month"):
                n += 1
        best = max(best, n)
    return best


def score_template(blob, date_cols, tpl):
    kw = tpl["classify_keywords"]
    hits_strong = sorted({k for k in kw["strong"] if any(norm_text(k) in b for b in blob)})
    hits_weak = sorted({k for k in kw["weak"] if any(norm_text(k) in b for b in blob)})
    hits_neg = sorted({k for k in kw["negative"] if any(norm_text(k) in b for b in blob)})
    score = 3.0 * len(hits_strong) + 1.0 * len(hits_weak) - 3.0 * len(hits_neg)
    # 结构信号：横向日期列多 -> demand / dip 加分；tracking 不靠大量日期列
    if tpl["id"] in ("demand_schedule", "dip_schedule") and date_cols >= 3:
        score += min(date_cols, 8) * 0.4
    return {
        "id": tpl["id"], "display_name": tpl["display_name"], "score": round(score, 2),
        "hits_strong": hits_strong, "hits_weak": hits_weak, "hits_negative": hits_neg,
    }


def classify_file(path, schema):
    info = read_any(path, sheet=0, max_rows=8)
    # 多 sheet：合并所有 sheet 前几行的文本一起判（客户文件常把主表放在某个非首 sheet）
    blob, date_cols = [], 0
    for sn in info["sheets"][:6]:
        try:
            si = read_any(path, sheet=sn, max_rows=6)
        except Exception:
            continue
        blob += gather_text(si["rows"])
        date_cols = max(date_cols, count_date_cols(si["rows"]))
    scored = [score_template(blob, date_cols, t) for t in schema["templates"]]
    scored.sort(key=lambda x: x["score"], reverse=True)
    top, second = scored[0], scored[1]
    margin = top["score"] - second["score"]
    if top["score"] <= 0:
        conf = "low"
    elif margin >= 3 and top["score"] >= 4:
        conf = "high"
    elif margin >= 1.5:
        conf = "medium"
    else:
        conf = "low"
    return {
        "file": os.path.basename(path), "path": path,
        "sheets": info["sheets"], "date_columns_detected": date_cols,
        "chosen": top["id"], "chosen_name": top["display_name"],
        "confidence": conf, "margin": round(margin, 2), "ranking": scored,
        "note": ("判定明确" if conf == "high"
                 else "得分接近或偏低，请 agent 打开文件复核后再定模板"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true", help="只输出 JSON")
    args = ap.parse_args()
    schema = load_schema()
    results = []
    for f in args.files:
        try:
            results.append(classify_file(f, schema))
        except Exception as e:
            results.append({"file": os.path.basename(f), "error": str(e)})

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    for r in results:
        print("=" * 72)
        if "error" in r:
            print(f"❌ {r['file']}: {r['error']}")
            continue
        print(f"📄 {r['file']}")
        print(f"   sheets={r['sheets']}  日期列≈{r['date_columns_detected']}")
        print(f"   ➜ 判定: 【{r['chosen_name']}】 ({r['chosen']})  置信度={r['confidence']}  领先={r['margin']}")
        for s in r["ranking"]:
            mark = "✓" if s["id"] == r["chosen"] else " "
            print(f"   {mark} {s['display_name']:8} 得分={s['score']:>5}  "
                  f"强={s['hits_strong']} 弱={s['hits_weak']} 负={s['hits_negative']}")
        print(f"   {r['note']}")


if __name__ == "__main__":
    main()
