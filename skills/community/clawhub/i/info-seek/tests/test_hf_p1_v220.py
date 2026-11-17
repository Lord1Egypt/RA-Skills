#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_hf_p1_v220.py — HF-P1 守护：融合因子 A/B/C→A/B/C/D + 样本准备（33 断言）

HF-P1（协同簇增强 + 融合校准）：
  ① `coord_clusters` / `sync_groups` 群体证据注入融合 → 因子由 A/B/C 扩为 A/B/C/D
     （D = 协同簇强度，复用 CROSS_SOURCE_BOOST 群体证据语义）
  ② 四因子动态重归一化（缺失因子不中断），权重 a:b:c 比例保持 7:8:5 → 无 D 时零回归
  ③ FPR ≤ 2% 基线：`scripts/hf_sample_kit.py` 打样/校验/校准 + 接入契约

分组：
  A1-A7  D 因子归一化  —— norm_cluster 分段 / 密度阈值 / 三路取最大 / 缺失 None
  B1-B7  四因子融合    —— D 参与 / 互补方向 / 重归一化 / 缺 D 不中断 / fuse_anchor 提取
  C1-C4  零回归        —— 无 D 逐点等价旧三因子 / a:b:c 比例 7:8:5 / 权重和 1 / D 初值
  D1-D5  权重契约      —— 3 值兼容(d=0) / 4 值 / 非法回退 / 值域异常回退 / 缺省默认
  E1-E6  样本套件      —— 打样可复现 / 校验通过 / 坏样本检出 / 校准 FPR≤2% / D 增益 / 样本不足
  F1-F4  合规与容错    —— 零网络 / 畸形输入不抛

设计原则：本套件**不自我 SKIP**；头部显式隔离 INFOSEEK_FUSION_*（㉖）。
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
for _p in (str(ROOT / "scripts"), str(ROOT / "core"), str(ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# 环境隔离：锁定默认配置态
for _e in ("INFOSEEK_FUSION_ENABLED", "INFOSEEK_FUSION_WEIGHTS"):
    os.environ.pop(_e, None)

import ast

import hf_sample_kit as kit
import identity_confidence_fusion as icf

PASS, FAIL = [], []
TARGET = 33


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def close(a, b, eps=1e-3):
    return abs(a - b) <= eps


def _imports(rel):
    tree = ast.parse((ROOT / rel).read_text(encoding="utf-8", errors="replace"))
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods.update(a.name.split(".")[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module:
            mods.add(n.module.split(".")[0])
    return mods


# ═══════════════════════════════════════════════════════════════
# A 组：D 因子归一化
# ═══════════════════════════════════════════════════════════════
print("=== ① A 组：D 因子归一化（norm_cluster）===")
_V, _S = icf.norm_cluster(None, None, None)
ok("A1 无任何信号 → (None, missing)", _V is None and _S == "missing")
ok("A2 cluster_size=0 → 0.0", close(icf.norm_cluster(cluster_size=0)[0], 0.0))
ok("A3 cluster_size=5 → 0.80（分段）", close(icf.norm_cluster(cluster_size=5)[0], 0.80),
   f"v={icf.norm_cluster(cluster_size=5)[0]}")
ok("A4 cluster_size=20 → 1.0（≥8 封顶）", close(icf.norm_cluster(cluster_size=20)[0], 1.0))
ok("A5 密度 >= 0.25 计入 / < 0.25 不计",
   close(icf.norm_cluster(cluster_density=0.6)[0], 0.6)
   and icf.norm_cluster(cluster_density=0.1)[0] is None)
ok("A6 sync_size=4 → 0.70（分段）", close(icf.norm_cluster(sync_size=4)[0], 0.70))
ok("A7 三路取最大 max(0.6, 0.5, 0.4) = 0.6",
   close(icf.norm_cluster(3, 0.5, 2)[0], 0.6),
   f"v={icf.norm_cluster(3, 0.5, 2)[0]}")


# ═══════════════════════════════════════════════════════════════
# B 组：四因子融合
# ═══════════════════════════════════════════════════════════════
print("\n=== ② B 组：四因子融合 ===")
_base_kw = dict(cross=4, trust_score=82, site_rank=18, url="https://github.com/alice")
_r3 = icf.fuse_confidence(**_base_kw)
_r4 = icf.fuse_confidence(**_base_kw, cluster_size=5, cluster_density=0.6, sync_size=4)
ok("B1 提供协同簇信号 → factors 含 d_cluster",
   "d_cluster" in _r4["fusion"]["factors"] and "d_cluster" not in _r3["fusion"]["factors"])
ok("B2 D 为互补证据：高协同簇 → confidence_final 更低",
   _r4["confidence_final"] < _r3["confidence_final"],
   f"{_r4['confidence_final']} < {_r3['confidence_final']}")
ok("B3 d_cluster 记录 norm（协同强度）与 contribution（互补）",
   close(_r4["fusion"]["factors"]["d_cluster"]["norm"], 0.8)
   and close(_r4["fusion"]["factors"]["d_cluster"]["contribution"], 0.2))
ok("B4 缺 D 不中断：无 cluster → degradation 仍标注 a/b/c（=3 情形）",
   len(icf.fuse_confidence()["fusion_degradation"]) == 3)
ok("B5 fuse_anchor 提取 coord_cluster_size（别名 cluster_size）",
   close(icf.fuse_anchor({"coord_cluster_size": 5})["fusion"]["factors"]
         ["d_cluster"]["norm"], 0.8))
ok("B6 fuse_anchor 提取 sync_group_size → 0.70",
   close(icf.fuse_anchor({"sync_group_size": 4})["fusion"]["factors"]
         ["d_cluster"]["norm"], 0.70))
ok("B7 fuse_anchor 不覆盖原字段", (lambda o: o["trust_score"] == 82 and o["verdict"] == "real")(
    icf.fuse_anchor({**_base_kw, "verdict": "real", "cluster_size": 5})))


# ═══════════════════════════════════════════════════════════════
# C 组：零回归（无 D 时逐点等价旧三因子）
# ═══════════════════════════════════════════════════════════════
print("\n=== ③ C 组：零回归 ===")
ok("C1 无 D 时结果 == 旧三因子（0.848 / 0.237 / 0.6167）",
   close(icf.fuse_confidence(cross=4, trust_score=82, site_rank=18,
                             url="https://github.com/alice")["confidence_final"], 0.848)
   and close(icf.fuse_confidence(cross=0, trust_score=18, site_rank=120000,
                                 url="https://weibo.com/bot1")["confidence_final"], 0.237)
   and close(icf.fuse_confidence(cross=2, trust_score=None, site_rank=None,
                                 url="")["confidence_final"], 0.6167))
_w = icf.DEFAULT_WEIGHTS
ok("C2 默认权重 a:b:c 比例 == 7:8:5（保零回归）",
   close(_w["a"] / _w["b"], 7 / 8) and close(_w["b"] / _w["c"], 8 / 5),
   f"a:b:c={_w['a']}:{_w['b']}:{_w['c']}")
ok("C3 默认权重和 == 1.0", close(sum(_w.values()), 1.0))
ok("C4 D 因子默认初值 == 0.20", close(_w.get("d", -1), 0.20), f"d={_w.get('d')}")


# ═══════════════════════════════════════════════════════════════
# D 组：权重契约（3/4 值兼容 + 非法回退）
# ═══════════════════════════════════════════════════════════════
print("\n=== ④ D 组：权重契约 ===")
os.environ["INFOSEEK_FUSION_WEIGHTS"] = "0.5,0.3,0.2"
_w3 = icf._load_weights()
ok("D1 旧 3 值兼容 → 映射 a/b/c，d=0",
   close(_w3["a"], 0.5) and close(_w3["d"], 0.0), f"w={_w3}")
os.environ["INFOSEEK_FUSION_WEIGHTS"] = "0.28,0.32,0.20,0.20"
_w4 = icf._load_weights()
ok("D2 新 4 值 → d 生效", close(_w4["d"], 0.20) and close(_w4["a"], 0.28), f"w={_w4}")
os.environ["INFOSEEK_FUSION_WEIGHTS"] = "0.1,0.2,0.3,0.4,0.1"   # 5 值（个数非法）
ok("D3 个数非法（5 值）→ 回退默认",
   close(icf._load_weights()["a"], icf.DEFAULT_WEIGHTS["a"]))
os.environ["INFOSEEK_FUSION_WEIGHTS"] = "1.5,0.2,0.1"           # 值域非法（>1）
ok("D4 值域非法（>1）→ 回退默认",
   close(icf._load_weights()["b"], icf.DEFAULT_WEIGHTS["b"]))
os.environ.pop("INFOSEEK_FUSION_WEIGHTS", None)
ok("D5 缺省 → 默认四因子权重", icf._load_weights() == dict(icf.DEFAULT_WEIGHTS))


# ═══════════════════════════════════════════════════════════════
# E 组：样本套件（打样 / 校验 / 校准）
# ═══════════════════════════════════════════════════════════════
print("\n=== ⑤ E 组：样本套件 ===")
_s1 = kit.make_synthetic(seed=7)
_s2 = kit.make_synthetic(seed=7)
ok("E1 半合成打样可复现（同 seed 完全相同）", _s1 == _s2)
_vok, _viss = kit.validate_sample(_s1)
ok("E2 打样样本通过契约校验", _vok and not _viss, f"issues={_viss}")
_bad = {"schema": kit.SAMPLE_SCHEMA, "records": [
    {"label": 2, "cross_platform_matches": 1, "trust_score": 50, "site_rank": 100},
    {"cross_platform_matches": 1, "trust_score": 50, "site_rank": 100},
]}
_bok, _biss = kit.validate_sample(_bad)
ok("E3 坏样本检出（坏 label + 缺字段）", (not _bok) and len(_biss) >= 1, f"issues={_biss}")
_cal = kit.calibrate(_s1)
ok("E4 校准返回 ok 且 FPR ≤ 2%",
   _cal.get("ok") and _cal["best"]["fpr"] <= kit.MAX_FPR,
   f"best={_cal.get('best', {}).get('fpr')}")
_d0 = next((r["recall"] for r in _cal["curve"] if close(r["d"], 0.0)), 0.0)
ok("E5 D 因子增益：best recall ≥ 无 D（d=0）recall",
   _cal["best"]["recall"] >= _d0,
   f"best={_cal['best']['recall']} vs d0={_d0}")
ok("E6 样本不足 → ok=False（不静默给结论）",
   kit.calibrate({"records": [{"label": 1, "cross_platform_matches": 1,
                               "trust_score": 20, "site_rank": 9e5}]})["ok"] is False)


# ═══════════════════════════════════════════════════════════════
# F 组：合规与容错
# ═══════════════════════════════════════════════════════════════
print("\n=== ⑥ F 组：合规与容错 ===")
_NET = {"urllib", "requests", "socket", "httpx", "aiohttp", "http", "ftplib"}
_f1 = _imports("scripts/identity_confidence_fusion.py") & _NET
_f2 = _imports("scripts/hf_sample_kit.py") & _NET
ok("F1 identity_confidence_fusion 零网络导入", not _f1, f"涉网={sorted(_f1) or '无'}")
ok("F2 hf_sample_kit 零网络导入", not _f2, f"涉网={sorted(_f2) or '无'}")
ok("F3 fuse_confidence 畸形 D 输入不抛异常",
   isinstance(icf.fuse_confidence(cluster_size="abc", cluster_density=None,
                                  sync_size="x"), dict))
ok("F4 fuse_anchor({}) 不抛异常", isinstance(icf.fuse_anchor({}), dict))


print(f"\n=== HF-P1 守护测试: {len(PASS)} PASS / {len(FAIL)} FAIL / TARGET {TARGET} ===")
if FAIL:
    print("FAIL 明细: " + ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
