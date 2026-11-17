#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_subject_threading_v211.py — 阶段0 主体贯通守护测试（openfix，版本号不变）

背景（P3 阶段0，2026-09-18 审计实锤）：
    生产链路 conflict_v3._group_and_detect 构造 claim_a/claim_b 时只带
    {source, source_title, text}，**丢掉实体**；而 contradiction_scorer._subject_key
    只读 claim.entity / claim.subject，不读 claim.entity_name（NER 口径）
    → 生产链路主体键恒为空 → same_subject 恒 True
    → GA11 keyed 路「跨主体隔离」在生产路径实际从未启用。

本批修复（两处，零行为风险）：
    ① core/conflict_v3.py：claim_a/claim_b 补 'entity': entity_name
      （真源注入，一处修复使 core_v2 三个调用点全部受益）
    ② core/contradiction_scorer.py：_subject_key 读取字段扩为
      entity > subject > entity_name

断言四组（21 条）：
    A 主体键契约（优先级 / 归一化 / 兜底）
    B keyed 路主体隔离（隔离生效 / 无主体通配向后兼容）
    C 生产链路贯通（claim 携带主体 → 端到端隔离生效）
    D 零回归（同实体判定不变 / 返回 schema 不变 / 旧式调用不变）
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "scripts"), ROOT, os.path.join(ROOT, "core")):
    if p not in sys.path:
        sys.path.insert(0, p)

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  -> {detail}" if detail and not cond else ""))


import contradiction_scorer as cs

try:
    import conflict_v3 as cv3
    _CV3_OK = True
except Exception as _e:  # pragma: no cover
    cv3, _CV3_OK = None, False
    print(f"[WARN] conflict_v3 导入失败：{_e}")

# ═══════════════════════════════════════════════════════════
# A 主体键契约
# ═══════════════════════════════════════════════════════════
k = cs._subject_key
check("A1 entity 字段生效", k({"entity": "Alpha"}, "") == "alpha")
check("A2 subject 字段生效（兼容）", k({"subject": "Beta"}, "") == "beta")
check("A3 entity_name 字段生效（阶段0 新增）", k({"entity_name": "甲公司"}, "") == "甲公司")
check("A4 优先级 entity > entity_name", k({"entity": "A", "entity_name": "B"}, "") == "a")
check("A5 优先级 subject > entity_name", k({"subject": "S", "entity_name": "E"}, "") == "s")
check("A6 归一化：去空白 + 小写", k({"entity": "  甲 公司 "}, "") == "甲公司")
check("A7 空/None/非 dict 兜底全局空串",
      k({}, "") == "" and k({"entity": None, "entity_name": ""}, "") == "" and k(None, "") == "")

# ═══════════════════════════════════════════════════════════
# B keyed 路主体隔离
# ═══════════════════════════════════════════════════════════
TA, TB = "甲公司营收增长20%", "甲公司营收增长35%"

# B1 基线：同主体同指标不同值 → 冲突
r_same = cs.keyed_score({"text": TA, "entity_name": "甲公司"},
                        {"text": TB, "entity_name": "甲公司"}, TA, TB)
check("B1 同主体(entity_name) 营收差异判冲突",
      "revenue" in r_same["conflict_slots"] and r_same["score"] > 0)

# B2 跨主体（entity_name 字段）→ 隔离生效（阶段0 修复目标）
XA, XB = "甲公司营收增长20%", "乙公司营收增长35%"
r_diff = cs.keyed_score({"text": XA, "entity_name": "甲公司"},
                        {"text": XB, "entity_name": "乙公司"}, XA, XB)
check("B2 跨主体(entity_name) 隔离生效", r_diff["score"] == 0 and "revenue" not in r_diff["conflict_slots"])

# B3 跨主体（entity 字段，旧契约）→ 隔离保持
r_diff2 = cs.keyed_score({"text": XA, "entity": "A"},
                         {"text": XB, "entity": "B"}, XA, XB)
check("B3 跨主体(entity) 隔离生效（旧契约保持）", r_diff2["score"] == 0)

# B4 双方无主体 → 通配仍比对（向后兼容，不做主体猜测）
r_none = cs.keyed_score({"text": TA}, {"text": TB}, TA, TB)
check("B4 双方无主体通配仍判冲突（向后兼容）",
      r_none["score"] > 0 and "revenue" in r_none["conflict_slots"])

# B5 单侧有主体 → 仍通配（契约：任一为全局默认键即比对）
r_half = cs.keyed_score({"text": TA, "entity_name": "甲公司"}, {"text": TB}, TA, TB)
check("B5 单侧有主体仍通配比对（旧契约）", r_half["score"] > 0)

# ═══════════════════════════════════════════════════════════
# C 生产链路贯通（conflict_v3 → contradiction_scorer）
# ═══════════════════════════════════════════════════════════
claims = [
    {"entity_name": "甲公司", "source": "https://a.example/1", "source_title": "T1", "text": TA},
    {"entity_name": "甲公司", "source": "https://b.example/2", "source_title": "T2", "text": TB},
]
confs = cv3._group_and_detect(claims, {}) if _CV3_OK else []
check("C1 _group_and_detect 产出 1 条冲突", len(confs) == 1, str(len(confs)))
ca = confs[0]["claim_a"] if confs else {}
cb = confs[0]["claim_b"] if confs else {}
check("C2 claim_a 携带 entity 且等于 entity_name", ca.get("entity") == "甲公司")
check("C3 claim_b 携带 entity 且等于 entity_name", cb.get("entity") == "甲公司")
sc = cs.score_contradiction(ca, cb)
check("C4 端到端同实体判冲突（修复后仍生效）",
      sc["keyed_score"] > 0 and "revenue" in sc["conflict_slots"])
check("C5 端到端 score/verdict 正确", sc["score"] > 0 and sc["verdict"] == "conflict")

# C6 端到端跨主体（手工构造带 entity_name 的 claim 对）→ 隔离
sc_x = cs.score_contradiction({"text": XA, "entity_name": "甲公司"},
                              {"text": XB, "entity_name": "乙公司"})
check("C6 端到端跨主体 keyed 路隔离", sc_x["keyed_score"] == 0)

# ═══════════════════════════════════════════════════════════
# D 零回归
# ═══════════════════════════════════════════════════════════
# D1 同实体：带主体键 vs 不带主体键 → 判定必须完全一致（修复不改变既有行为）
r_we = cs.keyed_score({"text": TA, "entity": "甲公司"}, {"text": TB, "entity": "甲公司"}, TA, TB)
r_wo = cs.keyed_score({"text": TA}, {"text": TB}, TA, TB)
check("D1 同实体带/不带主体键判定一致（零回归）",
      r_we["score"] == r_wo["score"] and r_we["conflict_slots"] == r_wo["conflict_slots"])

# D2 返回 schema 完整（新增字段不挤占既有字段）
need = {"score", "severity", "reasons", "neg_hits", "shared_slots", "slot_score",
        "neg_score", "keyed_score", "conflict_slots", "scorer_mode", "time_score",
        "time_slots_a", "time_slots_b", "time_coverage", "assessable", "verdict"}
check("D2 score_contradiction 返回 schema 完整（16 字段）", need.issubset(set(sc.keys())))

# D3 旧式无主体直调：文本含不同公司名仍通配判冲突（不引入主体推断）
r_legacy = cs.keyed_score({"text": XA}, {"text": XB}, XA, XB)
check("D3 无主体旧式调用维持通配（不猜测主体）", r_legacy["score"] > 0)

# ── 汇总 ────────────────────────────────────────────────────
print(f"\n阶段0 主体贯通: {len(PASS)} PASS / {len(FAIL)} FAIL（目标 21 断言）")
sys.exit(1 if FAIL else 0)
