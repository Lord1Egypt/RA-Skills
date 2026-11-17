#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_hf_r1_v220.py — HF-R1 守护：人因指纹增强 P0 四子项（33 断言）

HF-P0（既有资产补齐 · 零合规风险）四子项：
  ① AccountTrustScorer 新增「内容伪造特征」子维 → 四维升五维（scripts/account_trust_scorer.py）
  ② FakeDetect L1 增列 活跃时段熵 / 节奏规律 / 内容模板化 n-gram（extensions/fake_detect/l1_engine.py）
  ③ FakeDetect 粉丝质量回灌（data_adapter 别名 + 归一化 + L1 派生）
  ④ account_forensics dataset 增 profile / timing 字段（向后兼容）

判据（报告 §五）：仅扩展字段 + 规则，不新增能力项、不改 network_boundary、不动默认开关。

分组：
  A1-A9  五维升级     —— DIM_WEIGHTS / 权和 / forge 中性 / dimensions 5 键 / confidence 自适应 /
                         输出契约向后兼容 / forge 低分 + 强 flag
  B1-B8  L1 扩展与零回归 —— 四规则默认关 / l1_rule_names / 新特征列 / hour_entropy·rhythm_cv 边界 /
                         n_flags == 旧五项和（零回归）/ 开启后才计入 / pred 默认不变
  C1-C5  粉丝质量回灌  —— 别名 / 归一化(0-100→0-1) / 缺列不报错 / 三路派生 / 中文别名映射
  D1-D7  profile·timing —— _norm_profile(dict·list) / _merge_profile(meta 优先·空透传) /
                         from_raw 签名默认 None / Dataset.profile·timing 默认 None / profile 透传
  E1-E4  合规判据      —— l1_engine 零网络 / forensics 零网络 / FakeDetect 默认 OFF / 无新增能力项

设计原则：本套件**不自我 SKIP**；断言基于真源实时取值。头部显式隔离 INFOSEEK_ENABLE_*
（㉖铁律：能力默认 OFF 语义依赖环境的用例必须显式 pop per-capability env）。
"""
import ast
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
for _p in (str(ROOT / "scripts"), str(ROOT / "core"), str(ROOT),
           str(ROOT / "extensions" / "fake_detect")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# 环境隔离（㉖）：锁定纯注册表默认态，避免 env 旁路绕过默认 OFF 语义
for _e in ("INFOSEEK_ENABLE_FAKE_DETECT", "INFOSEEK_ENABLE_ACCOUNTTRUSTSCORER",
           "INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION", "INFOSEEK_ENABLE_MAIGRET",
           "INFOSEEK_ENABLE_SHERLOCK"):
    os.environ.pop(_e, None)

import numpy as np
import pandas as pd

PASS, FAIL = [], []
TARGET = 33


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def _imports(rel):
    src = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(src)
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods.update(a.name.split(".")[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module:
            mods.add(n.module.split(".")[0])
    return mods


# ═══════════════════════════════════════════════════════════════
# A 组：AccountTrustScorer 四维 → 五维
# ═══════════════════════════════════════════════════════════════
print("=== ① A 组：五维升级 ===")
import account_trust_scorer as ats

ok("A1 DIM_WEIGHTS 含 5 维（maturity/audience/behavior/content/forge）",
   set(ats.DIM_WEIGHTS) == {"maturity", "audience", "behavior", "content", "forge"},
   f"keys={sorted(ats.DIM_WEIGHTS)}")
ok("A2 五维权重和 == 1.0", abs(sum(ats.DIM_WEIGHTS.values()) - 1.0) < 1e-9,
   f"sum={sum(ats.DIM_WEIGHTS.values())}")

_sf, _sff = ats._score_forge({})
ok("A3 _score_forge 缺省中性 50 且带缺信号 flag",
   _sf == 50.0 and any("缺内容伪造信号" in f for f in _sff), f"score={_sf} flags={_sff}")

_r = ats.score_account({"username": "x", "account_age_days": 100, "post_count": 50,
                        "followers": 100, "following": 100, "engagement_rate": 0.02,
                        "post_interval_std": 2.0, "active_hours": 10,
                        "topic_diversity": 0.5, "template_similarity": 0.2})
ok("A4 输出 dimensions 含 5 键", len(_r["dimensions"]) == 5,
   f"keys={sorted(_r['dimensions'])}")
ok("A5 输出契约向后兼容（7 键齐备）",
   all(k in _r for k in ("username", "trust_score", "verdict", "verdict_cn",
                         "confidence", "dimensions", "flags", "missing")))

_c0 = ats.score_account({"username": "ghost"})
ok("A6 confidence 分母自适应：全缺 → 0.0", _c0["confidence"] == 0.0, f"conf={_c0['confidence']}")
_c1 = ats.score_account({"username": "x", "account_age_days": 100})
ok("A7 confidence 一维有信号 → 1-4/5 == 0.2", _c1["confidence"] == 0.2, f"conf={_c1['confidence']}")

_fk = ats.score_account({"username": "bot", "template_similarity": 0.95,
                         "ai_generated_ratio": 0.9, "duplicate_ratio": 0.8})
ok("A8 内容伪造特征强 → forge 低分且触发 flag",
   _fk["dimensions"]["forge"]["score"] < 40 and
   any("疑似伪造" in f or "疑似搬运" in f for f in _fk["flags"]),
   f"forge={_fk['dimensions']['forge']['score']}")

ok("A9 强机器人 flag 集合含新增 forge 项",
   any("高度模板化内容(疑似伪造)" in f for f in _fk["flags"]), f"flags={_fk['flags']}")


# ═══════════════════════════════════════════════════════════════
# B 组：FakeDetect L1 扩展与零回归
# ═══════════════════════════════════════════════════════════════
print("\n=== ② B 组：L1 扩展与零回归 ===")
import l1_engine
from fake_detect_engine import gen_demo_dataset

ok("B1 四条 HF-R1 规则默认关闭（*_enabled is False）",
   all(l1_engine.DEFAULT_THRESHOLDS[k] is False for k in
       ("hour_entropy_enabled", "rhythm_enabled", "tpl_enabled", "fq_enabled")),
   f"keys={[k for k in l1_engine.DEFAULT_THRESHOLDS if k.endswith('_enabled')]}")

_rule_names = l1_engine.l1_rule_names()
ok("B2 l1_rule_names 扩展至 9 项且含 4 新规则",
   len(_rule_names) == 9 and
   {"hour_entropy", "rhythm", "tpl", "follower_quality"} <= set(_rule_names),
   f"names={_rule_names}")

_ds = gen_demo_dataset()
_feats = l1_engine.compute_l1_features(_ds.meta_df, _ds.likes, _ds.growth, _ds.G)
ok("B3 compute_l1_features 输出含 4 新特征列",
   {"hour_entropy", "rhythm_cv", "tpl_ngram", "follower_quality"} <= set(_feats.columns),
   f"new={[c for c in ('hour_entropy','rhythm_cv','tpl_ngram','follower_quality') if c in _feats.columns]}")

ok("B4 hour_entropy 边界：均匀→1.0 / 集中→低 / 空→1.0",
   abs(l1_engine.hour_entropy([1] * 24) - 1.0) < 1e-9
   and l1_engine.hour_entropy([10] + [0] * 22 + [0.1]) < 0.35
   and l1_engine.hour_entropy(None) == 1.0 and l1_engine.hour_entropy([]) == 1.0)

ok("B5 rhythm_cv 边界：恒定→0 / 波动→大 / 样本不足→1.0",
   l1_engine.rhythm_cv([5] * 12) == 0.0
   and l1_engine.rhythm_cv([1, 1, 1, 50, 1, 1, 1, 90]) > 0.5
   and l1_engine.rhythm_cv([1]) == 1.0)

_res = l1_engine.apply_l1_rules(_feats)          # 默认阈值（新规则关闭）
_base = (  # 旧五项基线
    _res["benford"].astype(int) + _res["er"].astype(int) + _res["growth"].astype(int)
    + _res["fr"].astype(int) + _res["recip"].astype(int))
ok("B6 零回归：默认阈值下 4 新规则全 False 且不进入 n_flags",
   all(not _res[k].any() for k in ("hour_entropy", "rhythm", "tpl", "follower_quality"))
   and bool((_res["n_flags"] == _base).all()),
   f"n_flags==旧五项和: {bool((_res['n_flags'] == _base).all())}")
ok("B7 零回归：默认 pred 仍等价 n_flags>=2",
   bool((_res["pred"] == (_res["n_flags"] >= 2).astype(int)).all()))

# 构造单行 feats 验证「开启后才计入」
_one = pd.DataFrame({
    "benford_p": [0.5], "er": [0.02], "spike_ratio": [1.0], "spike_cnt": [0],
    "log_fr": [0.5], "recip": [0.0], "recip_deg": [0],
    "hour_entropy": [0.1], "rhythm_cv": [0.05], "tpl_ngram": [0.9], "follower_quality": [0.1]})
_th = dict(l1_engine.DEFAULT_THRESHOLDS)
_th.update({"hour_entropy_enabled": True, "rhythm_enabled": True,
            "tpl_enabled": True, "fq_enabled": True})
_r_on = l1_engine.apply_l1_rules(_one, thresholds=_th)
_r_off = l1_engine.apply_l1_rules(_one)
ok("B8 开启 4 规则后才命中（off=0 / on=4）",
   int(_r_off["n_flags"][0]) == 0 and int(_r_on["n_flags"][0]) == 4
   and all(_r_on[k][0] for k in ("hour_entropy", "rhythm", "tpl", "follower_quality")),
   f"off={int(_r_off['n_flags'][0])} on={int(_r_on['n_flags'][0])}")


# ═══════════════════════════════════════════════════════════════
# C 组：粉丝质量回灌
# ═══════════════════════════════════════════════════════════════
print("\n=== ③ C 组：粉丝质量回灌 ===")
import data_adapter as da

ok("C1 META_ALIASES 含 follower_quality / template_similarity",
   "follower_quality" in da.META_ALIASES and "template_similarity" in da.META_ALIASES)

_rep = da.QualityReport()
_m, _ = da._clean_meta(pd.DataFrame({
    "id": [1, 2, 3], "followers": [1, 1, 1], "following": [1, 1, 1], "posts": [1, 1, 1],
    "er": [0.0, 0.0, 0.0], "follower_quality": [80, 50, 20]}), _rep)
ok("C2 _clean_meta 归一化 0-100 分制 → 0-1",
   float(_m["follower_quality"].max()) <= 1.0
   and abs(float(_m["follower_quality"].iloc[0]) - 0.8) < 1e-9,
   f"vals={list(_m['follower_quality'])}")
_rep2 = da.QualityReport()
_m2, _ = da._clean_meta(pd.DataFrame({
    "id": [1], "followers": [1], "following": [1], "posts": [1], "er": [0.0]}), _rep2)
ok("C3 缺列时不新增列、不报错（向后兼容）",
   "follower_quality" not in _m2.columns and len(_rep2.issues) == 0,
   f"issues={_rep2.issues}")
_gm = {0: [1.0, 2.0, 3.0, 4.0], 1: [1.0, 2.0, 3.0, 4.0]}
_fq_col = l1_engine.compute_l1_features(
    pd.DataFrame({"id": [1, 2], "followers": [1, 1], "following": [1, 1], "posts": [1, 1],
                  "er": [0.0, 0.0], "follower_quality": [0.9, 0.1]}), {}, _gm)
_fq_zom = l1_engine.compute_l1_features(
    pd.DataFrame({"id": [1, 2], "followers": [1, 1], "following": [1, 1], "posts": [1, 1],
                  "er": [0.0, 0.0], "zombie_follower_ratio": [0.8, 0.2]}), {}, _gm)
_fq_none = l1_engine.compute_l1_features(
    pd.DataFrame({"id": [1, 2], "followers": [1, 1], "following": [1, 1], "posts": [1, 1],
                  "er": [0.0, 0.0]}), {}, _gm)
ok("C4 follower_quality 三路派生（列直取 / zombie 取反 / 缺省 0.5）",
   abs(float(_fq_col["follower_quality"].iloc[0]) - 0.9) < 1e-9
   and abs(float(_fq_zom["follower_quality"].iloc[0]) - 0.2) < 1e-9
   and bool((_fq_none["follower_quality"] == 0.5).all()))

_found = da.map_schema(["id", "粉丝质量", "模板相似度"], da.META_ALIASES)
ok("C5 中文别名映射（粉丝质量→follower_quality / 模板相似度→template_similarity）",
   _found.get("follower_quality") == "粉丝质量"
   and _found.get("template_similarity") == "模板相似度", f"found={_found}")


# ═══════════════════════════════════════════════════════════════
# D 组：account_forensics profile / timing（向后兼容）
# ═══════════════════════════════════════════════════════════════
print("\n=== ④ D 组：profile / timing 向后兼容 ===")
import mcp_tools_forensics as mtf
from data_adapter import from_raw

ok("D1 _norm_profile dict 形式",
   mtf._norm_profile({"1": {"account_age_days": 100}}) == {"1": {"account_age_days": 100}})
ok("D2 _norm_profile list 形式（id 剥离）",
   mtf._norm_profile([{"id": 1, "account_age_days": 100}]) == {"1": {"account_age_days": 100}})
_mg = mtf._merge_profile([{"id": 1, "followers": 100}],
                         {"1": {"followers": 999, "account_age_days": 10}})
ok("D3 _merge_profile：meta 既有键优先于 profile",
   len(_mg) == 1 and _mg[0]["followers"] == 100 and _mg[0]["account_age_days"] == 10,
   f"row={_mg[0]}")
ok("D4 _merge_profile：profile 空 → 原样返回",
   mtf._merge_profile([{"id": 1}], None) == [{"id": 1}]
   and mtf._merge_profile([{"id": 1}], {}) == [{"id": 1}])

import inspect
_sig = inspect.signature(from_raw)
ok("D5 from_raw 签名含 profile/timing 且默认 None（向后兼容）",
   _sig.parameters.get("profile") is not None and _sig.parameters.get("timing") is not None
   and _sig.parameters["profile"].default is None and _sig.parameters["timing"].default is None,
   f"params={list(_sig.parameters)}")
_ds_default = from_raw(pd.DataFrame({
    "id": [1], "followers": [1], "following": [1], "posts": [1], "er": [0.0]}))
ok("D6 默认调用 → Dataset.profile / timing 为 None",
   _ds_default.profile is None and _ds_default.timing is None)
_prof_ds = from_raw(
    pd.DataFrame({"id": [1, 2], "followers": [1, 1], "following": [1, 1], "posts": [1, 1],
                  "er": [0.0, 0.0]}),
    profile={"1": {"template_similarity": 0.9}})
ok("D7 传入 profile → Dataset.profile 经 id 归一化透传",
   isinstance(_prof_ds.profile, dict) and 1 in _prof_ds.profile,
   f"profile={_prof_ds.profile}")


# ═══════════════════════════════════════════════════════════════
# E 组：合规判据（零网络 / 默认开关不动 / 不新增能力项）
# ═══════════════════════════════════════════════════════════════
print("\n=== ⑤ E 组：合规判据 ===")
_NET = {"urllib", "requests", "socket", "httpx", "aiohttp", "http", "ftplib"}
_e1 = _imports("extensions/fake_detect/l1_engine.py") & _NET
_e2 = _imports("scripts/mcp_tools_forensics.py") & _NET
ok("E1 l1_engine 零网络导入", not _e1, f"涉网={sorted(_e1) or '无'}")
ok("E2 mcp_tools_forensics 零网络导入", not _e2, f"涉网={sorted(_e2) or '无'}")

from core import capability_registry as cr
cr.reload()
cr._consent_state.clear()
ok("E3 FakeDetect 默认 OFF（默认开关不动）", cr.is_effective_enabled("FakeDetect") is False)
_names = {c["name"] for c in cr.list_capabilities()}
ok("E4 无新增能力项（无 HF/Forge/Fingerprint 命名）",
   not any(("HF" in n or "Forge" in n or "Fingerprint" in n) for n in _names),
   f"疑似新增={[n for n in _names if 'HF' in n or 'Forge' in n or 'Fingerprint' in n] or '无'}")


print(f"\n=== HF-R1 守护测试: {len(PASS)} PASS / {len(FAIL)} FAIL / TARGET {TARGET} ===")
if FAIL:
    print("FAIL 明细: " + ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
