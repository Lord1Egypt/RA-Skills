#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/shadow_compare_s4.py — S4 影子模式：基线词典 vs 基线∪learned 候选（mod-v1.0.0）

铁律
----
  * **不改任何主链源码**：通过运行时 monkeypatch 模块级 `_ZH_HIGH_FREQ` 注入
    learned 候选；估计器 D 与锚点掩码 `_mask_zh_anchors` 都读这个全局，故一次
    注入同时影响「词典命中」与「掩码断点」，真实模拟 S5 接线效果。
  * **强制 zerodep**：monkeypatch `_optional_jieba`/`_optional_summa` 返回 None，
    确保走估计器 A/B/C/D 共识链（否则外部 NLP 直接返回，learned 层永不生效，
    无法观测差异）。
  * **只写报告，绝不回写主链、不改任何门控结果**。

输入：一个 JSONL（每行至少 {"text": ...}）或 S3 采集产物目录（自动找正文）。
输出：JSON 差异报告 + Markdown 人工抽检清单。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List, Dict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import infoseek_zerodep_nlp as zdn  # noqa: E402
from core import learned_anchor_store as las  # noqa: E402

MAX_KW = 15


def _force_zerodep():
    """关掉 jieba/summa 外部主路径，强制走零依赖共识链。返回还原句柄。"""
    saved_jb = zdn._optional_jieba
    saved_sm = zdn._optional_summa
    saved_freq = zdn._ZH_HIGH_FREQ
    zdn._optional_jieba = lambda text, top: None
    zdn._optional_summa = lambda text, top: None
    return saved_jb, saved_sm, saved_freq


def _restore(handle):
    jb, sm, freq = handle
    zdn._optional_jieba = jb
    zdn._optional_summa = sm
    zdn._ZH_HIGH_FREQ = freq


def extract(text: str, learned_terms) -> Dict:
    """在给定 _ZH_HIGH_FREQ 集合下抽取关键词。"""
    zdn._ZH_HIGH_FREQ = frozenset(zdn._ZH_HIGH_FREQ) | frozenset(learned_terms)
    out, engine = zdn.extract_keywords_detailed(text, max_kw=MAX_KW)
    return {"terms": [w for w, _ in out], "scores": dict(out), "engine": engine}


def run(texts: List[dict], learned_terms: List[str]) -> dict:
    base_freq = frozenset(zdn._ZH_HIGH_FREQ)
    handle = _force_zerodep()
    docs = []
    agg_added, agg_removed, agg_replaced = {}, {}, {}
    try:
        for i, rec in enumerate(texts):
            text = rec.get("text", "")
            if not text or not text.strip():
                continue
            # 基线
            zdn._ZH_HIGH_FREQ = base_freq
            base = extract(text, [])
            # 影子：基线 ∪ learned
            zdn._ZH_HIGH_FREQ = base_freq
            shadow = extract(text, learned_terms)
            bt, st_ = set(base["terms"]), set(shadow["terms"])
            added = sorted(st_ - bt)
            removed = sorted(bt - st_)
            docs.append({
                "idx": rec.get("idx", i),
                "slug": rec.get("slug", ""),
                "title": rec.get("title", ""),
                "source": rec.get("source", ""),
                "url": rec.get("url", ""),
                "engine_base": base["engine"],
                "engine_shadow": shadow["engine"],
                "base": base["terms"],
                "shadow": shadow["terms"],
                "added": added,
                "removed": removed,
                "learned_hits": sorted(t for t in learned_terms if t in text),
            })
            for w in added:
                agg_added[w] = agg_added.get(w, 0) + 1
            for w in removed:
                agg_removed[w] = agg_removed.get(w, 0) + 1
    finally:
        _restore(handle)

    n_changed = sum(1 for d in docs if d["added"] or d["removed"])
    by_topic = {}
    for d in docs:
        s = d.get("slug") or "_"
        t = by_topic.setdefault(s, {"n": 0, "changed": 0, "added": {}, "removed": {}})
        t["n"] += 1
        if d["added"] or d["removed"]:
            t["changed"] += 1
        for w in d["added"]:
            t["added"][w] = t["added"].get(w, 0) + 1
        for w in d["removed"]:
            t["removed"][w] = t["removed"].get(w, 0) + 1
    topic_out = {}
    for s, t in by_topic.items():
        topic_out[s] = {
            "n": t["n"], "changed": t["changed"],
            "added_freq": dict(sorted(t["added"].items(), key=lambda x: -x[1])),
            "removed_freq": dict(sorted(t["removed"].items(), key=lambda x: -x[1])),
        }
    return {
        "meta": {
            "phase": "S4_shadow",
            "mod_version": "mod-v1.0.0",
            "version_basis": "v2.3.0 (openfix, no bump; behavior<10%)",
            "n_docs": len(docs),
            "n_changed": n_changed,
            "n_learned_injected": len(learned_terms),
            "forced_engine": "zerodep (jieba/summa monkeypatched off)",
            "rule": "shadow only; main chain never touched",
        },
        "by_topic": topic_out,
        "aggregate": {
            "added_freq": dict(sorted(agg_added.items(), key=lambda x: -x[1])),
            "removed_freq": dict(sorted(agg_removed.items(), key=lambda x: -x[1])),
        },
        "docs": docs,
    }


def load_texts(path: str) -> List[dict]:
    """支持 .jsonl（每行 {text}）；S3 corpus 目录读 *.txt + manifest_S3.json。"""
    if os.path.isdir(path):
        manifest = os.path.join(path, "manifest_S3.json")
        if os.path.exists(manifest):
            metas = json.load(open(manifest, encoding="utf-8"))
            out = []
            for i, m in enumerate(metas):
                fp = os.path.join(path, m.get("file", ""))
                if not os.path.exists(fp):
                    continue
                text = open(fp, encoding="utf-8", errors="ignore").read()
                out.append({
                    "idx": i,
                    "text": text,
                    "slug": m.get("slug", ""),
                    "title": m.get("title", ""),
                    "source": m.get("source", ""),
                    "url": m.get("url", ""),
                })
            return out
        cand = os.path.join(path, "docs_s3.jsonl")
        if os.path.exists(cand):
            path = cand
        else:
            raise FileNotFoundError(f"目录下无 manifest_S3.json / docs_s3.jsonl: {path}")
    out = []
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            text = r.get("text") or r.get("content") or r.get("body") or ""
            out.append({"idx": r.get("idx", i), "text": text,
                        "slug": r.get("slug", ""), "title": r.get("title", "")})
    return out


def write_markdown(report: dict, path_md: str, seeds_f: str) -> None:
    m = report["meta"]
    L = []
    L.append("# S4 影子模式差异报告（人工抽检清单）\n")
    L.append(f"- 语料：{m['n_docs']} 篇；发生差异：{m['n_changed']} 篇；"
             f"注入 learned 候选：{m['n_learned_injected']} 词")
    L.append(f"- 引擎：{m['forced_engine']}")
    L.append(f"- 版本：{m['version_basis']}；规则：{m['rule']}\n")
    L.append("## 一、新增词命中频次（learned 净贡献）\n")
    L.append("| 词 | 命中篇数 | 判定 |")
    L.append("|----|---------:|------|")
    seedset = {s["term"] for s in json.load(open(seeds_f))["seeds"]}
    for w, c in report["aggregate"]["added_freq"].items():
        tag = "候选词" if w in seedset else "连锁顶替/统计连带"
        L.append(f"| {w} | {c} | {tag} |")
    L.append("")
    rem = report["aggregate"]["removed_freq"]
    if rem:
        L.append("## 二、被挤掉的词（长词顶替 / 掩码断点效应）\n")
        L.append("| 词 | 被挤掉篇数 |")
        L.append("|----|---------:|")
        for w, c in rem.items():
            L.append(f"| {w} | {c} |")
        L.append("")
    L.append("## 三、按主题命中（抽检种子纯度）\n")
    L.append("| 主题 | 篇数 | 差异篇数 | 候选词命中（候选/连锁） |")
    L.append("|------|----:|--------:|------|")
    for s, t in report.get("by_topic", {}).items():
        hits = []
        for w, c in t["added_freq"].items():
            tag = "" if w in seedset else "†"
            hits.append(f"{w}{tag}×{c}")
        L.append(f"| {s} | {t['n']} | {t['changed']} | {'、'.join(hits[:12])} |")
    L.append("\n> † = 连锁顶替/统计连带（非候选词本身）\n")
    L.append("## 四、逐篇差异（changed only）\n")
    for d in report["docs"]:
        if not (d["added"] or d["removed"]):
            continue
        head = f"### doc {d['idx']}"
        if d.get("slug"):
            head += f" · {d['slug']}"
        if d.get("title"):
            head += f"｜{d['title']}"
        L.append(head)
        L.append(f"（base:{d['engine_base']} → shadow:{d['engine_shadow']}）")
        if d["added"]:
            L.append("- 新增：" + "、".join(d["added"]))
        if d["removed"]:
            L.append("- 移除：" + "、".join(d["removed"]))
        L.append("- 影子：" + "、".join(d["shadow"][:15]))
        L.append("")
    with open(path_md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="JSONL 或 S3 产物目录")
    ap.add_argument("--store", default=None, help="learned store（默认 state_dir）")
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--all-pending", action="store_true",
                    help="影子跑全部 pending（S4 观测语义；默认即此）")
    ap.add_argument("--seeds", default=None,
                    help="选种 JSON（learned_seeds_S4.json）；store 为空时兜底")
    a = ap.parse_args()

    texts = load_texts(a.input)
    # S4：影子比对用全部 pending（未裁决）候选；若 store 已有 accept 亦并入
    terms = las.pending_terms(a.store) + las.active_terms("accept", a.store)
    if not terms:
        # store 未灌/未裁决时，从显式 --seeds 或 out 同目录选种文件取
        seeds_f = a.seeds or os.path.join(
            os.path.dirname(a.out_json), "learned_seeds_S4.json")
        terms = [s["term"] for s in json.load(open(seeds_f))["seeds"]]
    report = run(texts, sorted(set(terms)))
    os.makedirs(os.path.dirname(os.path.abspath(a.out_json)), exist_ok=True)
    with open(a.out_json, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    seeds_f = a.seeds or os.path.join(
        os.path.dirname(a.out_json), "learned_seeds_S4.json")
    write_markdown(report, a.out_md, seeds_f)
    print(f"docs={report['meta']['n_docs']} changed={report['meta']['n_changed']} "
          f"injected={report['meta']['n_learned_injected']}")
    print(f"JSON {a.out_json}\nMD   {a.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
