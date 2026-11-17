#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/identity_confidence_fusion.py — 身份归因四因子置信度融合（v1.7.0 · P1/T4 · HF-P1）

在 infoseek 已有发现层（Maigret/Sherlock）与验证层（AccountTrustScorer）基础之上，
将 A+B+C（+D）因子做联合置信度计算（此前三因子独立字段简单透传，未融合）：

  A 多平台交叉命中  cross_platform_matches  发现层产出（同名账号在多个平台的命中数）
  B 账号信任分      trust_score            AccountTrustScorer 五维人因评分（0-100）
  C 站点权威        site_rank / tier       maigret rank 数值 + core/trust_sources 4 级白名单
  D 协同簇强度      coord_cluster_* / sync_group_size   FakeDetect 发现层产出（HF-P1 新增；
                    coord_clusters 密度/规模 + 时序同步组规模，复用 CROSS_SOURCE_BOOST 语义）

融合方法（weighted_sum）：
  confidence_final = Σ w_i · norm_i ，缺失因子动态重归一化剩余权重（保证 Σw=1）

HF-P1 向后兼容承诺（**零回归**）：
  - 默认权重 a:b:c 比例**保持 7:8:5**（= 旧 0.35:0.40:0.25），故「无 D 信号」时结果与旧版**逐点一致**；
    D 因子仅在调用方提供协同簇信号时参与（权重默认 0.20），缺失自然不出现。
  - 新增输出字段（confidence_final / fusion / verdict_final / confidence_label* / d_cluster）
  - 绝不覆盖原 confidence / trust_score / verdict / verdict_cn / trust_confidence
  - 任意因子缺失或模块异常 → 降级（fusion_degradation 标注），不抛异常中断链路
  - INFOSEEK_FUSION_WEIGHTS 兼容旧 3 值（映射 a/b/c，d=0）与新 4 值（a,b,c,d）

可配置：
  INFOSEEK_FUSION_ENABLED   0 关闭融合（输出无融合字段）；默认 1
  INFOSEEK_FUSION_WEIGHTS   逗号分隔 3 或 4 权重，如 '0.28,0.32,0.20,0.20'；非法/缺省回退默认

用法：
    from identity_confidence_fusion import fuse_anchor, fuse_confidence
    res = fuse_anchor({...发现账号字段...})          # 单账号：原字段透传+新增融合字段
    out = fuse_confidence(cross=3, trust_score=72,  # 三因子原始值
                          site_rank=180, url="https://github.com/alice")
"""
from __future__ import annotations

import json
import logging
import os
import sys
from typing import Dict, List, Optional, Tuple

log = logging.getLogger("infoseek.identity_fusion")

# ── 默认权重（HF-P1 四因子：A 平台交叉 : B 信任分 : C 站点权威 : D 协同簇强度）──
# 关键约束：a:b:c == 0.28:0.32:0.20 == 7:8:5 == 旧 0.35:0.40:0.25（**比例不变**），
# 故「无 D 信号」时三因子重归一化结果与旧版逐点一致 → 零回归。D 校准初值 0.20（待真实样本）。
DEFAULT_WEIGHTS: Dict[str, float] = {"a": 0.28, "b": 0.32, "c": 0.20, "d": 0.20}
# HF-P1 推荐四因子校准配置（= DEFAULT_WEIGHTS，显式命名供真实样本校准替换）
FUSION_SCHEMA = "a/b/c/d"
WEIGHT_KEYS = ("a", "b", "c", "d")

# ── 交叉命中归一化分段（n → 归一值；缺失/0 → 中性 0.4，不惩罚单体存在）──
CROSS_STEPS: List[Tuple[int, float]] = [
    (0, 0.40), (1, 0.50), (2, 0.70), (3, 0.85), (4, 0.95), (5, 1.00),
]
CROSS_MAX = 5.0

# ── 站点权威 tier → 归一值（core/trust_sources 4 级白名单语义）──
TIER_TO_NORM = {1: 1.0, 2: 0.75, 3: 0.5, 4: 0.25}

# ── rank 数值（maigret Alexa 类排名，越小越权威）→ 归一值 分段对数衰减 ──
RANK_STEPS: List[Tuple[int, float]] = [
    (10, 1.0), (100, 0.75), (1000, 0.5), (10000, 0.25), (float("inf"), 0.1),
]
NORM_NEUTRAL = 0.5     # 因子缺失时的中性分
A_NEUTRAL = 0.4

# ── D 因子 协同簇强度分段（HF-P1：复用 CROSS_SOURCE_BOOST 语义的群体证据）──
#  协同簇规模（FakeDetect coord_clusters.size，密度 > 0.25 的 Louvain 社区）
#  簇密度（coord_clusters.density，0-1）
#  时序同步组规模（sync_groups.size）
CLUSTER_SIZE_STEPS: List[Tuple[int, float]] = [
    (0, 0.0), (1, 0.30), (3, 0.60), (5, 0.80), (8, 1.00),
]
SYNC_SIZE_STEPS: List[Tuple[int, float]] = [
    (0, 0.0), (2, 0.40), (4, 0.70), (6, 1.00),
]
CLUSTER_DENSITY_MIN = 0.25     # 与 FakeDetect coord_clusters 判定阈值一致

# ── 融合置信度标签 ──
LABEL_STEPS: List[Tuple[float, str, str]] = [
    (0.75, "high", "高置信"),
    (0.50, "medium", "中等置信"),
    (0.25, "low", "低置信"),
    (0.0, "critical", "极低置信"),
]


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def _load_weights() -> Dict[str, float]:
    """读取融合权重（env INFOSEEK_FUSION_WEIGHTS），非法回退默认。

    兼容 3 值（旧契约 'a,b,c' → d=0，D 因子不参与，行为同旧版）与
    4 值（新契约 'a,b,c,d'，HF-P1 四因子）。
    """
    raw = os.environ.get("INFOSEEK_FUSION_WEIGHTS", "").strip()
    if not raw:
        return dict(DEFAULT_WEIGHTS)
    parts = [p.strip() for p in raw.split(",")]
    try:
        vals = [float(p) for p in parts if p]
    except ValueError:
        log.warning("[融合] INFOSEEK_FUSION_WEIGHTS 非法，使用默认权重")
        return dict(DEFAULT_WEIGHTS)
    if len(vals) not in (3, 4) or any(v < 0 or v > 1 for v in vals) or sum(vals) <= 0:
        log.warning("[融合] INFOSEEK_FUSION_WEIGHTS 值域/个数异常，使用默认权重")
        return dict(DEFAULT_WEIGHTS)
    return {"a": vals[0], "b": vals[1], "c": vals[2],
            "d": (vals[3] if len(vals) == 4 else 0.0)}


def fusion_enabled() -> bool:
    """融合开关（env INFOSEEK_FUSION_ENABLED，缺省 1=开）。"""
    v = os.environ.get("INFOSEEK_FUSION_ENABLED", "1").strip().lower()
    return v not in ("0", "false", "off", "no")


# ═══════════════════════════════════════════════════════════════
# 单因子归一化
# ═══════════════════════════════════════════════════════════════

def norm_cross(cross: Optional[int]) -> Tuple[float, str]:
    """A 因子：多平台交叉命中数 → 0-1。缺失/0 → 0.4 中性（不惩罚单体存在）。"""
    if cross is None:
        return A_NEUTRAL, "missing"
    try:
        n = max(0, int(cross))
    except (TypeError, ValueError):
        return A_NEUTRAL, "missing"
    if n >= CROSS_MAX:
        return 1.0, "ok"
    for thr, val in CROSS_STEPS:
        if n <= thr:
            return val, "ok"
    return _clamp(n / CROSS_MAX), "ok"


def _match_tier(url: str) -> Optional[int]:
    """命中 core/trust_sources 4 级白名单 → 返回 tier（1-4）；未命中 → None。"""
    if not url:
        return None
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from core.trust_sources import build_pattern_index
        idx = build_pattern_index("general")
    except Exception as e:  # trust_sources 不可用时回退 rank 归一化
        log.debug(f"[融合] trust_sources 不可用: {e}")
        return None
    url_l = url.lower()
    for pat, (tier, _w) in idx.items():
        if pat and pat in url_l:
            return tier
    return None


def norm_site(url: str, site_rank: Optional[int]) -> Tuple[float, str]:
    """C 因子：站点权威 → 0-1。白名单 tier 优先；否则 rank 数值分段；双缺失 → 中性。"""
    tier = _match_tier(url)
    if tier is not None:
        return TIER_TO_NORM.get(tier, NORM_NEUTRAL), f"tier{tier}"
    if site_rank is None:
        return NORM_NEUTRAL, "missing"
    try:
        r = max(0, int(site_rank))
    except (TypeError, ValueError):
        return NORM_NEUTRAL, "missing"
    if r == 0:  # 0 = 无排名数据
        return NORM_NEUTRAL, "missing"
    for thr, val in RANK_STEPS:
        if r <= thr:
            return val, "rank"
    return 0.1, "rank"


def norm_trust(trust_score: Optional[float]) -> Tuple[float, str]:
    """B 因子：trust_score（0-100）→ 0-1；缺失 → None（触发动态重归一化）。"""
    if trust_score is None:
        return None, "missing"  # type: ignore[return-value]
    try:
        return _clamp(float(trust_score) / 100.0), "ok"
    except (TypeError, ValueError):
        return None, "missing"  # type: ignore[return-value]


def _step_norm(n: int, steps: List[Tuple[int, float]]) -> float:
    """分段归一：取首个 n <= thr 的 val；n 超过最大 thr → 末段 val。"""
    for thr, val in steps:
        if n <= thr:
            return val
    return steps[-1][1]


def norm_cluster(cluster_size: Optional[int] = None,
                 cluster_density: Optional[float] = None,
                 sync_size: Optional[int] = None) -> Tuple[Optional[float], str]:
    """D 因子（HF-P1）：协同簇强度 → 0-1；**无任何信号 → None**（不参与，保持旧行为）。

    三路信号取最大（互补证据，复用 CROSS_SOURCE_BOOST 的群体证据语义）：
      - cluster_size    : 协同簇规模（FakeDetect coord_clusters 成员数）
      - cluster_density : 簇密度（0-1，>= CLUSTER_DENSITY_MIN 才计入）
      - sync_size       : 时序同步组规模（sync_groups 成员数）
    聚众协同（水军集群）证据越强 → 归一值越高。
    """
    vals: List[float] = []
    for raw, steps in ((cluster_size, CLUSTER_SIZE_STEPS), (sync_size, SYNC_SIZE_STEPS)):
        if raw is None:
            continue
        try:
            n = max(0, int(raw))
        except (TypeError, ValueError):
            continue
        vals.append(_step_norm(n, steps))
    if cluster_density is not None:
        try:
            d = float(cluster_density)
            if d >= CLUSTER_DENSITY_MIN:
                vals.append(_clamp(d))
        except (TypeError, ValueError):
            pass
    if not vals:
        return None, "missing"  # type: ignore[return-value]
    return round(max(vals), 4), "ok"


# ═══════════════════════════════════════════════════════════════
# 融合计算
# ═══════════════════════════════════════════════════════════════

def fuse_confidence(cross: Optional[int] = None,
                    trust_score: Optional[float] = None,
                    site_rank: Optional[int] = None,
                    url: str = "",
                    cluster_size: Optional[int] = None,
                    cluster_density: Optional[float] = None,
                    sync_size: Optional[int] = None,
                    weights: Optional[Dict[str, float]] = None) -> Dict:
    """A+B+C(+D) 四因子联合置信度计算（HF-P1）。

    缺失因子动态重归一化剩余权重（fusion_degradation 标注缺失因子）；
    D 因子无信号时不进入 factors/present（保持旧三因子逐点结果，零回归）；
    全部缺失 → 中性 + degradation（不抛异常）。
    """
    w = weights or _load_weights()
    factors: Dict[str, Dict] = {}
    a, a_st = norm_cross(cross)
    factors["a_cross"] = {"raw": cross, "norm": round(a, 4), "status": a_st}
    b, b_st = norm_trust(trust_score)
    factors["b_trust"] = {"raw": trust_score,
                          "norm": (None if b is None else round(b, 4)),
                          "status": b_st}
    c, c_st = norm_site(url, site_rank)
    factors["c_site"] = {"raw": {"url": url, "site_rank": site_rank},
                         "norm": round(c, 4), "status": c_st}
    # D 因子（协同簇强度）：仅在有信号时进入，缺失不列入 degradation（保持旧三因子语义）
    # 方向：协同簇越强 → 越可疑 → 以「非协同」互补证据 (1 - d) 参与加权（高 conf = 可信真人）
    d, d_st = norm_cluster(cluster_size, cluster_density, sync_size)
    if d is not None:
        factors["d_cluster"] = {
            "raw": {"cluster_size": cluster_size,
                    "cluster_density": cluster_density, "sync_size": sync_size},
            "norm": round(d, 4), "contribution": round(1.0 - d, 4), "status": d_st}

    present = {"a": a}
    if b is not None:
        present["b"] = b
    else:
        log.debug("[融合] B 因子缺失（验证层未启用），动态重归一化")
    present["c"] = c
    if d is not None:
        present["d"] = 1.0 - d      # 互补证据：协同簇越强 → 身份置信越下调

    w_sum = sum(w.get(k, 0.0) for k in present)
    conf = sum(w.get(k, 0.0) * v for k, v in present.items()) / max(w_sum, 1e-9)
    conf = round(_clamp(conf), 4)

    label_en, label_cn = _label(conf)
    degraded = [f for f, v in factors.items() if v["status"] == "missing"]
    return {
        "confidence_final": conf,
        "confidence_label": label_en,
        "confidence_label_cn": label_cn,
        "fusion": {
            "factors": factors,
            "weights": {k: round(w[k], 4) for k in w},
            "method": "weighted_sum",
        },
        "fusion_degradation": degraded if degraded else None,
    }


def _label(conf: float) -> Tuple[str, str]:
    for thr, en, cn in LABEL_STEPS:
        if conf >= thr:
            return en, cn
    return "critical", "极低置信"


def _pick(d: Dict, *keys):
    """按序取首个非 None 值（字段别名兼容）。"""
    for k in keys:
        v = d.get(k)
        if v is not None:
            return v
    return None


def fuse_anchor(acc: Dict, username: str = "") -> Dict:
    """单账号融合入口：原字段透传 + 附加融合字段（不覆盖任何原字段）。

    输入：发现层/验证层账号条目（可含 cross_platform_matches / trust_score /
          site_rank / url / verdict，以及 HF-P1 协同簇字段
          coord_cluster_size / coord_cluster_density / sync_group_size 等）。
    输出：dict 副本，新增 confidence_final / confidence_label / confidence_label_cn /
          fusion / fusion_degradation / verdict_final。
    开关关闭或异常 → 原样返回（降级，不中断）。
    """
    if not fusion_enabled():
        return dict(acc)
    try:
        res = fuse_confidence(
            cross=acc.get("cross_platform_matches"),
            trust_score=acc.get("trust_score"),
            site_rank=acc.get("site_rank"),
            url=acc.get("url") or "",
            cluster_size=_pick(acc, "coord_cluster_size", "cluster_size"),
            cluster_density=_pick(acc, "coord_cluster_density", "cluster_density"),
            sync_size=_pick(acc, "sync_group_size", "sync_size"),
        )
        out = dict(acc)
        out["confidence_final"] = res["confidence_final"]
        out["confidence_label"] = res["confidence_label"]
        out["confidence_label_cn"] = res["confidence_label_cn"]
        out["fusion"] = res["fusion"]
        out["fusion_degradation"] = res["fusion_degradation"]
        # verdict_final：融合置信度 × 原人因判定（unknown 保持 unknown 语义）
        v = acc.get("verdict")
        if v == "unknown":
            out["verdict_final"] = "unknown"
        else:
            map_v = {"real": "real", "likely_real": "likely_real",
                     "suspicious": "suspicious", "bot": "bot"}
            vf = map_v.get(v, res["confidence_label"])
            # B 因子强否决：信任分 < 40（suspicious 以下）且融合分虚高 → 降档提示
            ts = acc.get("trust_score")
            if ts is not None and float(ts) < 40 and vf not in ("unknown", "bot"):
                vf = "needs_review"
            out["verdict_final"] = vf
        return out
    except Exception as e:
        log.warning(f"[融合] fuse_anchor 异常，返回原条目: {e}")
        return dict(acc)


# ═══════════════════════════════════════════════════════════════
# CLI 自检
# ═══════════════════════════════════════════════════════════════

def _demo() -> int:
    cases = [
        ("真人高权威", {"cross": 4, "trust_score": 82,
                      "site_rank": 18, "url": "https://github.com/alice"}),
        ("水军低权威", {"cross": 0, "trust_score": 18,
                      "site_rank": 120000, "url": "https://weibo.com/bot1"}),
        ("B 缺失（验证层未启用）", {"cross": 2,
                                 "site_rank": None, "url": ""}),
        ("全部缺失", {}),
    ]
    for name, kw in cases:
        r = fuse_confidence(**kw)
        factors = {k: v.get("norm") for k, v in r["fusion"]["factors"].items()}
        print(f"[{name}] final={r['confidence_final']} label={r['confidence_label_cn']} "
              f"factors={factors} deg={r['fusion_degradation']}")
    return 0


if __name__ == "__main__":
    sys.exit(_demo())