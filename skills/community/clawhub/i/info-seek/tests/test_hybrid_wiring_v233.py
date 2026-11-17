#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_hybrid_wiring_v233.py — hybrid 矛盾打分接入 detect_conflicts_v3 主链守护（v2.3.3）

背景（GA11 接线缺口）：
  此前 _group_and_detect 只做分组/配对/结构组装，severity 恒 'medium'，
  contradiction_scorer 的键控事实槽（A 层）从未接入 v3 生产主链，hybrid 是死代码。
  v2.3.3 在配对组装后调 score_contradiction_hybrid 并回写真实严重度与槽证据。

测试隔离：
  finalize 会经 _augment_cross_session 用 claim_store 历史声明把 severity 升级一档。
  为避免跨会话持久化污染断言，本测试所有调用经 _detect() 注入临时 claim_store 路径，
  锁定"本轮会话内"打分语义（跨会话升级另有既有行为，不在本守护范围）。

本测试锁定（17 断言）：
  A 组 接线真实生效：detect_conflicts_v3 / ConflictMonitor.finalize 输出带
        contradiction_score / conflict_slots / scorer_mode / llm_used，severity 由真实分决定
  B 组 永久契约：_score_pair_hybrid 用模块对象导入（mock.patch 在消费点实测生效）
  C 组 降级兜底：打分器抛异常时不击穿主链，severity 回退 'medium'
"""

import os
import sys
import tempfile
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "scripts"), ROOT, os.path.join(ROOT, "core")):
    if p not in sys.path:
        sys.path.insert(0, p)

# 锁定纯注册表默认态：旁路 env 不得干扰
for _k in list(os.environ):
    if _k.startswith("INFOSEEK_") and "CONTRADICTION" in _k:
        os.environ.pop(_k, None)

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  -> {detail}" if detail and not cond else ""))


import conflict_v3 as cv

# 独立临时 claim_store，避免跨会话历史升级污染
_STORE_DIR = tempfile.mkdtemp(prefix="hybrid_wiring_")
_STORE_SEQ = [0]


def _detect(sources, subject="x"):
    """走 ConflictMonitor 主链，每次用全新空 claim_store，
    锁定"本轮会话内"打分语义（跨会话 severity 升级另有既有行为，不在本守护范围）。"""
    _STORE_SEQ[0] += 1
    path = os.path.join(_STORE_DIR, f"claims_{_STORE_SEQ[0]}.json")
    return cv.ConflictMonitor(claim_store_path=path).ingest_all(sources).finalize(subject=subject)


def _mk_sources():
    """两源对同一实体给出趋势矛盾的声明（异源、实体相同）。"""
    return [
        {"source": "s1", "url": "http://a", "title": "甲报道",
         "text": "宁德时代2025年三季度营收同比增长，净利润稳步提升，业绩向好。"},
        {"source": "s2", "url": "http://b", "title": "乙报道",
         "text": "宁德时代2025年三季度营收同比下滑，净利润持续下降，业绩承压。"},
    ]


# ═══════════════════════════════════════════════════════════
# A 组 接线真实生效
# ═══════════════════════════════════════════════════════════
res = _detect(_mk_sources(), "宁德时代")
conflicts = res.get("conflicts", [])
check("A1 检出 1 条配对冲突", len(conflicts) == 1, str(len(conflicts)))
cf = conflicts[0] if conflicts else {}
check("A2 回写 contradiction_score", isinstance(cf.get("contradiction_score"), int))
check("A3 回写 conflict_slots 非空（含趋势/收入槽）",
      isinstance(cf.get("conflict_slots"), list) and len(cf.get("conflict_slots", [])) >= 1,
      str(cf.get("conflict_slots")))
check("A4 scorer_mode 存在", cf.get("scorer_mode") in ("keyed", "negation", "time", "llm"))
check("A5 默认 OFF → llm_used=False", cf.get("llm_used") is False)
check("A6 severity 落在合法档", cf.get("severity") in ("low", "medium", "high"))
import contradiction_scorer as _cs
_expected_sev = _cs._sev(cf.get("contradiction_score", 0))
check("A7 severity == _sev(contradiction_score)",
      cf.get("severity") == _expected_sev, f"{cf.get('severity')} vs {_expected_sev}")

# 同值归一：数值/同义措辞归一后 score=0、无矛盾槽（配对条目仍在，severity 落 low）
_norm = _detect([
    {"source": "s1", "url": "a", "title": "t", "text": "宁德时代营收增长20%"},
    {"source": "s2", "url": "b", "title": "t", "text": "宁德时代营收提升百分之二十"},
], "").get("conflicts", [])
check("A8 同值归一（20% vs 百分之二十）score=0 且无矛盾槽",
      len(_norm) == 1 and _norm[0].get("contradiction_score") == 0
      and not _norm[0].get("conflict_slots"),
      str([(c.get("contradiction_score"), c.get("conflict_slots")) for c in _norm]))

# ConflictMonitor.finalize 同构路径同样接线（隔离 store）
mon = cv.ConflictMonitor(claim_store_path=os.path.join(_STORE_DIR, "manual_a9.json"))
for s in _mk_sources():
    mon.ingest_source(s)
fres = mon.finalize(subject="宁德时代")
fconf = fres.get("conflicts", [])
check("A9 ConflictMonitor.finalize 同样回写打分",
      len(fconf) == 1 and isinstance(fconf[0].get("contradiction_score"), int),
      str([c.get("contradiction_score") for c in fconf]))

# ═══════════════════════════════════════════════════════════
# B 组 永久契约：模块对象导入，mock 在消费点生效
# ═══════════════════════════════════════════════════════════
import inspect
_src = inspect.getsource(cv._score_pair_hybrid)
check("B1 _score_pair_hybrid 用 import contradiction_scorer（禁 from-import）",
      "import contradiction_scorer as" in _src and "from contradiction_scorer import" not in _src)

_fake = {"score": 77, "severity": "high", "conflict_slots": ["trend_dir"],
         "scorer_mode": "keyed", "llm_used": False, "reasons": ["fake"]}
with mock.patch("contradiction_scorer.score_contradiction_hybrid", return_value=_fake) as m:
    r2 = _detect(_mk_sources(), "x")
check("B2 mock.patch 在消费点生效（score=77 被回写）",
      r2["conflicts"] and r2["conflicts"][0].get("contradiction_score") == 77,
      str([c.get("contradiction_score") for c in r2.get("conflicts", [])]))
check("B3 mock 真实被调用", m.called)
check("B4 high 严重度随 mock 回写",
      r2["conflicts"] and r2["conflicts"][0].get("severity") == "high")

# ═══════════════════════════════════════════════════════════
# C 组 降级兜底：打分器异常不击穿主链
# ═══════════════════════════════════════════════════════════
with mock.patch("contradiction_scorer.score_contradiction_hybrid",
                side_effect=RuntimeError("boom")):
    r3 = _detect(_mk_sources(), "x")
check("C1 打分器异常时主链不崩", isinstance(r3, dict) and "conflicts" in r3)
check("C2 异常降级 severity 回退 medium 兜底",
      r3["conflicts"] and r3["conflicts"][0].get("severity") == "medium",
      str(r3["conflicts"][0].get("severity") if r3.get("conflicts") else None))
check("C3 降级时不带 contradiction_score 字段",
      r3["conflicts"] and "contradiction_score" not in r3["conflicts"][0])

# hybrid 默认 OFF 行为：enable_llm 默认 None → 不调 LLM
check("C4 hybrid 默认 env OFF → llm_used False（接线生产安全）",
      cf.get("llm_used") is False
      and _detect(_mk_sources(), "x")["conflicts"][0].get("llm_used") is False)

print(f"\nhybrid 接线守护: {len(PASS)} PASS / {len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
