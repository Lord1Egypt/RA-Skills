#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_entry_contract_g8.py — G8 公共入口类型契约回归守卫（G8-apply 后）

G8-apply 已将原 11 处「类型违规 CRASH」接线受控（受控 TypeError / 优雅降级）。
本套件现为**强回归守卫**：
  - A 组（A1-A10）：十处已优雅入口锁定不回退（OK 或 CONTROLLED）；
  - B 组（B1-B11）：原 11 处 CRASH 入口现断言为非 CRASH（OK 或 CONTROLLED）；
  - 任意入口复现非受控异常（CRASH）→ 立即 FAIL（回归捕捉）。

设计依据：references/g8-entry-contract-design.md（G8 专项设计 · 方案 C）
判定：OK=正常返回（含降级）/ CONTROLLED=受控 ValueError·TypeError（带消息）/ CRASH=非受控异常
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "scripts"), ROOT, os.path.join(ROOT, "core")):
    if p not in sys.path:
        sys.path.insert(0, p)

import infoseek_core_v2 as c
import anchor_score_v2 as asv2
import contradiction_scorer as cs
import conflict_v3 as cv3
import identity_aggregator as ia

PASS, FAIL = [], []

# G8-apply 后已收敛的 11 处（原 known_boundary）；若任一复现 CRASH → 回归 FAIL
RESOLVED = {
    "extract_entities(text=123)": lambda: c.extract_entities(123),
    "get_entities_by_type(entity_type=None)": lambda: c.get_entities_by_type(None),
    "compute_trust_bonus(url=123)": lambda: c.compute_trust_bonus(123),
    "score_source(source=None)": lambda: c.score_source(None, "s"),
    "score_source(source=[])": lambda: c.score_source([], None),
    "score_source(source='x')": lambda: c.score_source("x", "s"),
    "detect_conflicts(sources={'a':1})": lambda: c.detect_conflicts({"a": 1}),
    "render_report(sources=[None])": lambda: c.render_report("s", [None]),
    "estimate_cost(prompt=None)": lambda: c.estimate_cost(None),
    "detect_conflicts_v3(sources=[None])": lambda: cv3.detect_conflicts_v3([None]),
    "identity_aggregator.aggregate(None)": lambda: ia.aggregate(None),
}

# 已优雅处理入口（须锁定不回退）
GRACEFUL = {
    "research(subject=None)": lambda: c.research(None),
    "research(subject=123)": lambda: c.research(123),
    "score_source(source={})": lambda: c.score_source({}, "s"),
    "compute_trust_bonus(url=None)": lambda: c.compute_trust_bonus(None),
    "get_tier_level(url=None)": lambda: c.get_tier_level(None),
    "extract_entities(text=None)": lambda: c.extract_entities(None),
    "aggregate_score_v2(base_score=None)": lambda: asv2.aggregate_score_v2(None),
    "aggregate_score_v2(base_score='abc')": lambda: asv2.aggregate_score_v2("abc"),
    "score_contradiction(a=None,b='x')": lambda: cs.score_contradiction(None, "x"),
    "llm_call(prompt=None)": lambda: c.llm_call(None),
}


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def run(fn):
    """返回 (kind, excname)。kind ∈ {OK, CONTROLLED, CRASH}。"""
    try:
        fn()
        return "OK", ""
    except (ValueError, TypeError) as e:
        return ("CONTROLLED" if str(e).strip() else "CRASH"), type(e).__name__
    except Exception as e:  # noqa
        return "CRASH", type(e).__name__


# ── A 组：优雅面锁定 ──
print("=== A 组：优雅处理面锁定（不回退）===")
for i, (name, fn) in enumerate(GRACEFUL.items(), 1):
    kind, exc = run(fn)
    ok(f"A{i} {name} 保持优雅", kind in ("OK", "CONTROLLED"),
       f"实测={kind}{('(' + exc + ')') if exc else ''}")

# ── B 组：G8-apply 收敛断言（原 11 CRASH 现非 CRASH）──
print("\n=== B 组：G8-apply 收敛断言（原 11 CRASH 现非 CRASH）===")
for i, (name, fn) in enumerate(RESOLVED.items(), 1):
    kind, exc = run(fn)
    ok(f"B{i} {name} 不再 CRASH", kind in ("OK", "CONTROLLED"),
       f"实测={kind}{('(' + exc + ')') if exc else ''}")

print(f"\nG8 入口契约回归: {len(PASS)} PASS / {len(FAIL)} FAIL")
if FAIL:
    print("未通过：" + ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
