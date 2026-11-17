#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/promote_s5.py — S5「晋级真锚」：把人工裁决为真锚增益的候选从
pending 晋级为 accept(active)，写入独立 learned 物理层（mod-v1.0.0）。

口径（不可漂移）
================
* 候选来源：S4 影子对拍（shadow_compare_s4）在 A+B 合并 11 主题 / 220 篇
  语料上产出的 37 个 pending 候选；经人工裁决，15 个为「真锚增益」。
* 本脚本**只晋级这 15 个 accept 词**；其余 22 个为通用/噪声词，由选种硬
  规则（generic/in_builtin/non_noun_pos/drop_gate）天然排除，不入 store。
* 主链默认仍不消费：开关 INFOSEEK_LEARNED_ANCHORS=1 才经
  infoseek_zerodep_nlp._active_zh_anchors() 与基线 frozenset 取并集。
* 运行时数据落 ~/.infoseek/learned_anchors.json（或 INFOSEEK_DATA_DIR），
  **不进仓库**。

幂等
====
bulk_upsert_pending 不覆盖既有裁决、只补全 provenance；随后对每个词
set_decision(accept)。重复运行结果一致（accept 仍 accept，证据刷新）。

用法
====
  python3 scripts/promote_s5.py            # 执行晋级
  python3 scripts/promote_s5.py --dry-run  # 只打印将晋级的词与证据，不写盘
"""
from __future__ import annotations

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, os.path.join(_ROOT, "scripts"), os.path.join(_ROOT, "core")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import learned_anchor_store as las  # noqa: E402

MOD_VERSION = "mod-v1.0.0"
PROMOTE_PHASE = "S5-promote-accept"
BASIS_VERSION = "v2.3.1"

# term: (topic_cross, coverage, doc_hits, consensus_doc_hits, freq, pos)
# 证据取自 S4 seeds provenance 与人工裁决（见摘要 15 accept 表）。
# pos 记录选种时词性；规划产能/具身智能/加征关税为 nv，但语料中作名词性
# 短语使用，经人工裁决 accept；pos 仅作证据，不作晋级门控。
ACCEPT_ANCHORS = {
    "低空经济": (4, 1.0, 26, 24, 375, "n"),
    "能量密度": (3, 1.0, 21, 20, 137, "n"),
    "动力电池": (3, 1.0, 21, 15, 59, "n"),
    "规划产能": (3, 1.0, 3, 2, 6, "nv"),
    "知识产权": (3, 1.0, 3, 0, 4, "n"),
    "固态电池": (3, 0.9677, 23, 22, 614, "n"),
    "数据中心": (3, 1.0, 19, 14, 107, "n"),
    "具身智能": (3, 1.0, 10, 9, 42, "nv"),
    "技术壁垒": (3, 1.0, 6, 4, 13, "n"),
    "地缘政治": (3, 1.0, 3, 0, 4, "n"),
    "加征关税": (3, 1.0, 3, 0, 4, "nv"),
    "供需缺口": (3, 1.0, 11, 8, 27, "n"),
    "价格中枢": (3, 1.0, 4, 4, 12, "n"),
    "能源转型": (3, 1.0, 7, 3, 12, "n"),
    "现货价格": (3, 0.9615, 6, 6, 19, "n"),
}


def _build_items():
    items = []
    for term, (topic, cover, doc, cons, freq, pos) in ACCEPT_ANCHORS.items():
        items.append({
            "term": term,
            "promote_phase": PROMOTE_PHASE,
            "basis_version": BASIS_VERSION,
            "topic_cross": topic,
            "coverage": cover,
            "doc_hits": doc,
            "consensus_doc_hits": cons,
            "freq": freq,
            "pos": pos,
            "decision_rule": "human-adjudicated true-anchor gain (S4 shadow)",
        })
    return items


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="S5 promote learned anchors to accept")
    ap.add_argument("--dry-run", action="store_true", help="只打印不写盘")
    ap.add_argument("--path", default=None, help="覆盖 store 路径（测试用）")
    args = ap.parse_args(argv)

    items = _build_items()
    terms = [it["term"] for it in items]

    # 自检：晋级名单内部不得有子串冲突（长词优先匹配下的顶替风险）。
    for i, long in enumerate(sorted(terms, key=len, reverse=True)):
        for short in terms:
            if short != long and short in long:
                print(f"[FAIL] accept 名单内部存在子串冲突: {short} ⊂ {long}")
                return 2

    path = args.path or str(las.store_path())
    print(f"store path : {path}")
    print(f"candidates : {len(terms)} accept anchors")
    if args.dry_run:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        print("[dry-run] 未写盘")
        return 0

    n = las.bulk_upsert_pending(items, path)
    print(f"upsert     : {n} entries")
    for t in terms:
        e = las.set_decision(t, "accept",
                             note="S5 human-adjudicated true anchor", path=path)
        if e is None:
            print(f"[FAIL] set_decision 未命中词条: {t}")
            return 2

    accepted = las.active_terms("accept", path)
    missing = [t for t in terms if t not in accepted]
    if missing:
        print(f"[FAIL] 晋级后缺失 accept 词: {missing}")
        return 2

    pending = las.pending_terms(path)
    print(f"accept now : {len(accepted)} 词")
    print(f"pending    : {len(pending)} 词")
    print("promoted   : " + " / ".join(accepted))
    print("[OK] S5 晋级真锚完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
