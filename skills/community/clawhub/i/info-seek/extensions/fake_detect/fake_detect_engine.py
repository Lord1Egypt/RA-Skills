# -*- coding: utf-8 -*-
"""
extensions/fake_detect/fake_detect_engine.py — FakeDetect 深度取证引擎（v1.0.0 · 函数化）

run_detect.py 从「文件输入脚本」函数化为 detect(dataset) -> Report：
  输入 : data_adapter.Dataset（标准化: meta_df + likes + growth + G）或 dict
  输出 : Report（对齐 AccountTrustScorer 输出契约 trust_score/verdict/verdict_cn/trust_confidence）

四层检测（与评估报告 P0/P1/P1.5 一致）：
  L1 统计规则   l1_engine（阈值参数化 + 互惠率前移，无图自动降级）
  L2 图结构     Louvain 密度社区判定 + PPR 种子富集（种子=L1 红旗）
  时序同步      sync_detect（纯时序小集群共享事件，growth 可用时）
  L3 ML         RandomForest 5 折 CV + CAP 阈值（FPR<=2% 最大 recall；需标注 label）

命门：数据充分性门控（缺数据 ≠ 水军）
  - assess_sufficiency: 时序/ER/图谱 信号覆盖评估
  - 不足 -> Report{sufficiency.sufficient=false, degradation="insufficient_signals"} 不硬跑
  - 深度取证由 B 模式工具（account_forensics MCP）显式投喂数据；pipeline 自动路径降级
    AccountTrustScorer（A2 信号门控在 infoseek_pipeline._verify_accounts 消费本评估）

盲区边界（评估报告 P0 诚实刻画）：
  G0-G2 攻击面全灭；G3 伪装 Benford 漏检 ~75%；G4 全伪装漏检 ~67%（单层指纹全失效）；
  本引擎输出 blindspots 字段如实声明，不夸大覆盖。

CLI:
  python fake_detect_engine.py --demo          # 内置合成数据全链自检（自包含）
  python fake_detect_engine.py --json '{"meta": ...}'  # 任意 JSON 数据（经 data_adapter）
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_PKG_DIR = Path(__file__).resolve().parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

import l1_engine                      # noqa: E402  同包 L1 参数化规则
from data_adapter import QualityReport, from_raw, load_dataset  # noqa: E402  数据接入
from sync_detect import detect_sync   # noqa: E402  时序同步

ENGINE_VERSION = "1.0.0"
ROUTED_INFOSEEK = "1.6.0"             # 对外版本保持 infoseek 1.6.0（V1.5.x 策略，不 bump）

# 盲区边界（评估报告_P0P1P2 结论：G0-G2 全灭 / G3 漏检 75% / G4 67%，诚实声明）
BLINDSPOTS = [
    "G3 伪装Benford: 漏检 ~75%（统计指纹被对手规避，仅剩行为/图谱弱信号）",
    "G4 全伪装: 漏检 ~67%（单层指纹全部失效，需行为时序跨期或外部证据）",
]
G3_G4_NOTE = "对抗级对手（G3/G4）存在系统性盲区，本引擎不承诺覆盖；命中以 L1+L2+时序 弱信号聚合为准。"

# 充分性门控默认阈值（A2 数据充分性判定）
SUFFICIENCY_DEFAULTS = {
    "min_ts_ratio": 0.30,     # 时序（likes/growth）覆盖账号比例
    "min_er_cover": 0.30,     # ER 信号可用比例
    "min_graph_edges": 50,    # 图边数下限（关系数据可用性）
    "deep_score_th": 0.50,    # 综合深度分阈值（ts*0.5 + er*0.25 + graph*0.25）
}

# verdict 语义对齐 AccountTrustScorer（trust_score 0-100，越低越可疑）
VERDICT_TIERS = [
    (80, "real", "高置信真人"),
    (60, "likely_real", "大概率真人"),
    (40, "suspicious", "可疑（需人工核实）"),
    (0, "bot", "高概率机器人/水军"),
]


def load_trained_thresholds() -> dict:
    """l1_thresholds.json 重训阈值（缺失回退 l1_engine.DEFAULT_THRESHOLDS）"""
    p = _PKG_DIR / "l1_thresholds.json"
    try:
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            return dict(data.get("trained_thresholds", {}))
    except Exception:
        pass
    return {}


def _verdict_from_risk(risk: float) -> dict:
    """risk(0-100) -> AccountTrustScorer 契约 {trust_score, verdict, verdict_cn}"""
    trust = max(0.0, min(100.0, 100.0 - risk))
    for th, v, cn in VERDICT_TIERS:
        if trust >= th:
            return {"trust_score": round(trust, 1), "verdict": v, "verdict_cn": cn}
    return {"trust_score": round(trust, 1), "verdict": "bot", "verdict_cn": "高概率机器人/水军"}


def assess_sufficiency(ds, thresholds: dict | None = None) -> dict:
    """信号充分性评估（A2 门控核心）：
    ts_ratio(时序覆盖) / er_cover(互动率覆盖) / graph_score(关系图可用)。
    deep_score = ts*0.5 + er*0.25 + graph*0.25 >= th -> sufficient。
    返回 {sufficient, deep_score, signals{...}, missing[]}
    """
    th = dict(SUFFICIENCY_DEFAULTS)
    if thresholds:
        th.update({k: v for k, v in thresholds.items() if k in SUFFICIENCY_DEFAULTS})
    meta = ds.meta_df
    n = len(meta)
    if n == 0:
        return {"sufficient": False, "deep_score": 0.0,
                "signals": {}, "missing": ["无账号元数据"]}
    meta_ids = set(meta.index)
    ts_ids = set(ds.likes) | set(ds.growth)
    ts_ratio = len(ts_ids & meta_ids) / n
    er_cover = float((meta.get("er", pd.Series(0.0, index=meta.index)).fillna(0) > 0).mean())
    if ds.G is not None and ds.G.number_of_edges() > 0:
        graph_ratio = min(1.0, ds.G.number_of_edges() / max(th["min_graph_edges"], 1))
        graph_score = graph_ratio
    else:
        graph_score = 0.0
    deep = ts_ratio * 0.5 + er_cover * 0.25 + graph_score * 0.25
    missing = []
    if ts_ratio < th["min_ts_ratio"]:
        missing.append(f"时序覆盖不足({ts_ratio:.0%}<{th['min_ts_ratio']:.0%})")
    if er_cover < th["min_er_cover"]:
        missing.append(f"ER 覆盖不足({er_cover:.0%}<{th['min_er_cover']:.0%})")
    if graph_score == 0.0:
        missing.append("无关系图")
    return {"sufficient": deep >= th["deep_score_th"] and len(missing) <= 1,
            "deep_score": round(deep, 3),
            "signals": {"ts_ratio": round(ts_ratio, 3), "er_cover": round(er_cover, 3),
                        "graph_edges": ds.G.number_of_edges() if ds.G else 0,
                        "meta_n": n},
            "missing": missing}


# ═══════════════════════════════════════════════════════════════
# 四层检测
# ═══════════════════════════════════════════════════════════════

def _run_l1(ds, thresholds: dict) -> dict:
    """L1 统计规则：红旗数/单规则命中/聚合判定（互惠率前移开，图缺失自动降级）"""
    feats = l1_engine.compute_l1_features(ds.meta_df, ds.likes, ds.growth, ds.G,
                                          timing=getattr(ds, "timing", None))
    res = l1_engine.apply_l1_rules(feats, thresholds=thresholds or None)
    n_flags = res["n_flags"]
    flags = {
        "benford": res["benford"], "er": res["er"], "growth": res["growth"],
        "fr": res["fr"], "recip": res["recip"],
        # HF-R1 新增规则（默认关闭；命中永远为 False，仅结构完整）
        "hour_entropy": res["hour_entropy"], "rhythm": res["rhythm"],
        "tpl": res["tpl"], "follower_quality": res["follower_quality"],
    }
    return {"feats": feats, "n_flags": n_flags, "pred": res["pred"], "flags": flags}


def _run_l2(ds, l1_pred: np.ndarray) -> dict:
    """L2 图结构：Louvain 社区 + density>0.25 可疑社区 + PPR 种子富集（无图降级）"""
    if ds.G is None or ds.G.number_of_edges() == 0:
        return {"available": False, "susp_member": np.zeros(len(ds.meta_df), dtype=bool),
                "density": pd.Series(0.0, index=ds.meta_df.index),
                "behav_entropy": pd.Series(0.0, index=ds.meta_df.index),
                "ppr": pd.Series(0.0, index=ds.meta_df.index),
                "coord_clusters": [], "nmi": None}
    G = ds.G
    GU = G.to_undirected()
    import networkx as nx
    comm_list = sorted(nx.community.louvain_communities(GU, seed=42), key=len, reverse=True)
    node_comm = {}
    for ci, c in enumerate(comm_list):
        for n in c:
            node_comm[n] = ci
    density = pd.Series(0.0, index=ds.meta_df.index)
    behav_entropy = pd.Series(0.0, index=ds.meta_df.index)
    for ci, c in enumerate(comm_list):
        sub = GU.subgraph(c)
        m = sub.number_of_edges()
        dens = m / max(len(c) * (len(c) - 1) / 2, 1)
        ers = ds.meta_df.loc[list(c), "er"].values if not ds.meta_df.empty else []
        ent = 0.0
        if len(ers) >= 8:
            h, _ = np.histogram(ers, bins=8, range=(0, 0.08))
            p = h / h.sum()
            p = p[p > 0]
            ent = float(-(p * np.log(p)).sum() / np.log(8))
        for n in c:
            if n in density.index:
                density.at[n] = dens
                behav_entropy.at[n] = ent
    coord_clusters = []
    for ci, c in enumerate(comm_list):
        if len(c) >= 3:
            dens = density.loc[list(c)].iloc[0] if len(c) else 0.0
            if dens > 0.25:
                coord_clusters.append({"cluster_id": int(ci), "members": sorted(c),
                                       "size": len(c), "density": round(float(dens), 3),
                                       "behav_entropy": round(float(behav_entropy.loc[list(c)].iloc[0]), 3)})
    susp_comm = {cc["cluster_id"] for cc in coord_clusters}
    idx_arr = np.array([node_comm.get(n, -1) for n in ds.meta_df.index])
    susp_member = np.array([1 if node_comm.get(n, -1) in susp_comm else 0 for n in ds.meta_df.index],
                           dtype=bool)
    # PPR 富集（种子 = L1 红旗）
    ppr_vals = np.zeros(len(ds.meta_df))
    seeds = ds.meta_df.index[l1_pred == 1].tolist()
    if seeds:
        pers = {s: 1.0 for s in seeds}
        try:
            ppr = nx.pagerank(G, alpha=0.85, personalization=pers)
            ppr_vals = np.array([ppr.get(n, 0.0) for n in ds.meta_df.index])
        except Exception:
            ppr_vals = np.zeros(len(ds.meta_df))
    return {"available": True, "susp_member": susp_member,
            "density": density, "behav_entropy": behav_entropy,
            "ppr": pd.Series(ppr_vals, index=ds.meta_df.index),
            "coord_clusters": coord_clusters, "nmi_comm_n": len(comm_list),
            "idx_arr": idx_arr}


def _run_sync(ds) -> dict:
    """时序同步：growth 可用时 detect_sync；返回 member/groupsz + 组件"""
    if not ds.growth or len(ds.growth) == 0:
        return {"available": False, "member": np.zeros(len(ds.meta_df), dtype=bool),
                "groupsz": np.zeros(len(ds.meta_df), dtype=int), "groups": []}
    ids_order = sorted(ds.growth.keys())
    susp, comps = detect_sync(ds.growth, ids_order)
    member = np.zeros(len(ds.meta_df), dtype=bool)
    groupsz = np.zeros(len(ds.meta_df), dtype=int)
    groups = []
    for gi, c in enumerate(comps):
        m = sorted(c)
        groups.append({"group_id": int(gi), "members": m, "size": len(m)})
        for k in m:
            if k in ds.meta_df.index:
                pos = ds.meta_df.index.get_loc(k)
                member[pos] = True
                groupsz[pos] = len(m)
    return {"available": True, "member": member, "groupsz": groupsz, "groups": groups,
            "n_marked": int(member.sum())}


def _run_l3(ds, feats_df: pd.DataFrame) -> dict:
    """L3 ML：需要标注（group_label 双类）；无标注/单类跳过。CAP 阈值 FPR<=2% 最大 recall。"""
    ycol = None
    for c in ("group_label", "label", "is_fake", "group"):
        if c in feats_df.columns:
            ycol = c
            break
    if ycol is None:
        return {"available": False, "reason": "no_labels"}
    y = pd.to_numeric(feats_df[ycol], errors="coerce").fillna(0).astype(int)
    y01 = (y > 0).astype(int)
    if y01.nunique() < 2:
        return {"available": False, "reason": "single_class"}
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import StratifiedKFold, cross_val_predict
        from sklearn.metrics import roc_auc_score, average_precision_score
    except Exception:
        return {"available": False, "reason": "sklearn_missing"}
    feat_cols = [c for c in ["benford_p", "er", "spike_ratio", "spike_cnt", "log_fr",
                             "density", "behav_entropy", "recip", "ppr",
                             "sync_member", "sync_groupsz"] if c in feats_df.columns]
    X = feats_df[feat_cols].fillna(0).values
    clf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    try:
        proba = cross_val_predict(clf, X, y01, cv=skf, method="predict_proba")[:, 1]
    except Exception:
        return {"available": False, "reason": "cv_failed"}
    auc = float(roc_auc_score(y01, proba))
    ap = float(average_precision_score(y01, proba))
    order = np.argsort(-proba)
    best_t, best_rec = 1.0, 0.0
    for t in np.percentile(proba, np.arange(50, 100, 0.5)):
        p = (proba >= t).astype(int)
        fpr = ((p == 1) & (y01 == 0)).sum() / max((y01 == 0).sum(), 1)
        rec = ((p == 1) & (y01 == 1)).sum() / max((y01 == 1).sum(), 1)
        if fpr <= 0.02 and rec > best_rec:
            best_rec, best_t = rec, t
    score = pd.Series(proba, index=feats_df.index)
    return {"available": True, "auc": round(auc, 3), "ap": round(ap, 3),
            "cap_t": round(float(best_t), 3), "cap_recall": round(best_rec, 3),
            "score": score}


# ═══════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════

def detect(dataset, thresholds: dict | None = None, require_sufficient: bool = True,
           run_l3: bool = True, verbose: bool = False) -> dict:
    """FakeDetect 深度取证主入口：dataset(Dataset|dict) -> Report。

    返回 Report 结构：
      status / sufficiency / degradation / verdicts / coord_clusters / sync_groups
      / summary(四层命中) / blindspots / meta
    契约对齐 AccountTrustScorer：verdicts[id] = {trust_score, verdict, verdict_cn, flags}
    """
    # 1) 数据接入（dict -> Dataset）
    ds = dataset
    if not hasattr(ds, "meta_df"):
        try:
            if isinstance(ds, dict) and ds.get("meta") is not None:
                ds = from_raw(meta_df=pd.DataFrame(ds.get("meta", [])),
                              likes=ds.get("likes"), growth=ds.get("growth"),
                              edges=ds.get("edges"), groups=ds.get("groups"),
                              profile=ds.get("profile"), timing=ds.get("timing"))
            else:
                ds = load_dataset(source=ds if isinstance(ds, str) else None)
        except Exception as e:
            return {"status": "failed", "reason": f"数据接入失败: {e}",
                    "degradation": "invalid_input", "meta": _meta()}
    report = {"status": "ok", "sufficiency": None, "degradation": "none",
              "verdicts": {}, "coord_clusters": [], "sync_groups": [],
              "summary": {}, "blindspots": list(BLINDSPOTS),
              "blindspots_note": G3_G4_NOTE, "meta": _meta()}
    report["quality"] = str(ds.report) if hasattr(ds.report, "issues") else ""

    # 2) 充分性门控（A2 命门：缺数据 ≠ 水军）
    suf = assess_sufficiency(ds, thresholds)
    report["sufficiency"] = suf
    if require_sufficient and not suf["sufficient"]:
        report["status"] = "degraded"
        report["degradation"] = "insufficient_signals"
        report["summary"]["gate"] = {"route": "AccountTrustScorer",
                                     "reason": suf["missing"]}
        return report

    # 3) 阈值装配：l1_thresholds.json 重训阈值 <- 调用方覆盖
    th = load_trained_thresholds()
    if thresholds:
        th.update({k: v for k, v in thresholds.items() if k not in SUFFICIENCY_DEFAULTS})
    if th.get("n_flags_th") is None:
        th = {}  # 全默认回退 l1_engine.DEFAULT_THRESHOLDS

    # 4) L1
    import l1_engine as _l1
    r1 = _run_l1(ds, th or None)
    n_flags = np.asarray(r1["n_flags"])
    l1_pred = np.asarray(r1["pred"])

    # 5) L2（无图自动降级）
    r2 = _run_l2(ds, l1_pred)
    l2_member = r2["susp_member"] if r2["available"] else np.zeros(len(ds.meta_df), dtype=bool)

    # 6) 时序同步
    r4 = _run_sync(ds)
    sync_member = r4["member"] if r4["available"] else np.zeros(len(ds.meta_df), dtype=bool)

    # 7) L3 ML（需标注；集成 L1/L2/时序特征）
    l3 = {"available": False, "reason": "no_labels"}
    if run_l3:
        feats_l3 = r1["feats"].copy()
        feats_l3["density"] = r2["density"]
        feats_l3["behav_entropy"] = r2["behav_entropy"]
        feats_l3["ppr"] = r2["ppr"]
        feats_l3["sync_member"] = pd.Series(sync_member.astype(int), index=ds.meta_df.index)
        feats_l3["sync_groupsz"] = pd.Series(r4["groupsz"], index=ds.meta_df.index)
        l3 = _run_l3(ds, feats_l3)

    # 8) 账号级 verdict 聚合（risk 融合：L1 红旗*20 + L2 可疑 + 时序同步 + L3 proba）
    risk = np.zeros(len(ds.meta_df))
    risk += (n_flags >= 1).astype(float) * 25.0
    risk += (n_flags >= 2).astype(float) * 25.0
    risk += l2_member.astype(float) * 30.0
    risk += sync_member.astype(float) * 25.0
    if l3.get("available"):
        risk = 0.6 * risk + 0.4 * (l3["score"].values * 100.0)
    verdicts = {}
    for pos, aid in enumerate(ds.meta_df.index):
        flags = []
        if l1_pred[pos]:
            flags.append(f"L1红旗x{int(n_flags[pos])}")
        if l2_member[pos]:
            flags.append("L2可疑社区")
        if sync_member[pos]:
            flags.append(f"时序同步组({int(r4['groupsz'][pos])}人)")
        if l3.get("available"):
            flags.append(f"L3分={risk[pos] / 100:.2f}")
        v = _verdict_from_risk(float(risk[pos]))
        d = {"trust_score": v["trust_score"], "verdict": v["verdict"],
             "verdict_cn": v["verdict_cn"], "flags": flags,
             "layers": {"l1_flags": int(n_flags[pos]),
                        "l2_susp": bool(l2_member[pos]),
                        "sync_member": bool(sync_member[pos]),
                        "risk": round(float(risk[pos]), 1)}}
        report["verdicts"][str(aid)] = d

    # 9) 汇总（四层命中）
    report["coord_clusters"] = r2.get("coord_clusters", [])
    report["sync_groups"] = r4.get("groups", [])
    report["summary"] = {
        "l1": {"n_flags_th": th.get("n_flags_th", _l1.DEFAULT_THRESHOLDS["n_flags_th"]),
               "flagged": int(l1_pred.sum()),
               "flagged_rate": round(float(l1_pred.mean()), 3),
               "rule_hits": {k: int(v.sum()) for k, v in r1["flags"].items()}},
        "l2": {"available": r2["available"],
               "susp_member": int(l2_member.sum()),
               "coord_clusters": len(report["coord_clusters"]),
               "nmi_comm_n": r2.get("nmi_comm_n")},
        "sync": {"available": r4["available"], "n_marked": int(sync_member.sum()),
                 "groups": len(report["sync_groups"])},
        "l3": {"available": l3.get("available", False), **({k: v for k, v in l3.items()
                                                           if k not in ("available", "score")})},
        "verdict_dist": {"bot": sum(1 for v in report["verdicts"].values() if v["verdict"] == "bot"),
                         "suspicious": sum(1 for v in report["verdicts"].values() if v["verdict"] == "suspicious"),
                         "likely_real": sum(1 for v in report["verdicts"].values() if v["verdict"] == "likely_real"),
                         "real": sum(1 for v in report["verdicts"].values() if v["verdict"] == "real")},
        "gate": {"route": "FakeDetect", "reason": "充分性达标"},
    }
    degradations = []
    if not r2["available"]:
        degradations.append("no_graph")
    if not r4["available"]:
        degradations.append("no_timeseries_sync")
    if not l3.get("available"):
        degradations.append("no_labels")
    if degradations:
        report["status"] = "degraded" if l1_pred.sum() == 0 else "ok"
        report["degradation"] = "+".join(degradations[:1]) if len(degradations) == 1 else "partial"
        report["degradation_detail"] = degradations
    if verbose:
        print(f"[FakeDetect] N={len(ds.meta_df)} 充分性={suf['sufficient']} "
              f"L1红旗={int(l1_pred.sum())} L2可疑={int(l2_member.sum())} "
              f"时序={int(sync_member.sum())} L3={'on' if l3.get('available') else 'off'}")
    return report


def _meta() -> dict:
    return {"engine": "fake_detect", "version": ENGINE_VERSION,
            "routed_infoseek": ROUTED_INFOSEEK,
            "changelog": "v1.0.0 函数化（run_detect.py -> detect(dataset)->Report）；P1.5 时序同步内置；"
                         "HF-R1 增列 hour_entropy / rhythm_cv / tpl_ngram / follower_quality（L1 规则默认关闭）"}


# ═══════════════════════════════════════════════════════════════
# CLI 自检
# ═══════════════════════════════════════════════════════════════

def gen_demo_dataset(n_norm: int = 40, n_bot: int = 10, seed: int = 7, days: int = 90):
    """内置合成演示数据（自包含 self-check，不经外部文件）：
    正常账号：低频缓增涨粉 + 温和 ER；水军账号：高尖峰涨粉 + 低 ER + 互相关注团。
    返回 Dataset（from_raw 标准化结构）。
    """
    rng = np.random.RandomState(seed)
    N = n_norm + n_bot
    ids = list(range(N))
    followers, following, posts, er = [], [], [], []
    likes, growth = {}, {}
    edges = []
    bot_ids = set(ids[n_norm:])
    for i in ids:
        is_bot = i in bot_ids
        followers.append(int(rng.randint(2000, 200000) if not is_bot else rng.randint(50, 5000)))
        following.append(int(rng.randint(50, 2000) if not is_bot else rng.randint(2000, 9000)))
        posts.append(int(rng.randint(200, 5000)))
        er.append(round(float(rng.uniform(0.01, 0.06) if not is_bot else rng.uniform(0.0001, 0.001)), 5))
        base = float(rng.uniform(1.0, 6.0))
        g = np.abs(rng.normal(base, base * 0.8, days))
        if is_bot:
            for d in (15, 45, 75):
                g[d:d + 3] += rng.uniform(25, 60)
        growth[i] = np.round(g, 1)
        likes[i] = np.abs(rng.normal(50, 40, days))
    # 水军之间互相关注团（协调特征）
    for a in range(n_norm, N):
        for b in range(a + 1, N):
            if rng.rand() < 0.6:
                edges.append((a, b))
    meta = pd.DataFrame({"id": ids, "followers": followers, "following": following,
                         "posts": posts, "er": er})
    meta["group_label"] = [1 if i in bot_ids else 0 for i in ids]
    return from_raw(meta_df=meta, likes=likes, growth=growth, edges=edges)


def _cli_demo():
    """全链自检：充分性 -> L1/L2/时序 -> L3 -> 契约对齐 -> 盲区声明"""
    ds = gen_demo_dataset()
    rep = detect(ds, verbose=True)
    print(json.dumps({
        "status": rep["status"],
        "sufficiency": rep["sufficiency"],
        "degradation": rep["degradation"],
        "summary": rep["summary"],
        "coord_clusters_n": len(rep["coord_clusters"]),
        "sync_groups_n": len(rep["sync_groups"]),
        "verdict_sample": {k: rep["verdicts"][k] for k in list(rep["verdicts"])[:3]},
        "blindspots": rep["blindspots"],
    }, ensure_ascii=False, indent=1))


def _cli_json(raw: str):
    data = json.loads(raw)
    ds = load_dataset(source=data) if isinstance(data, str) and os.path.exists(data) \
        else from_raw(meta_df=pd.DataFrame(data.get("meta", [])),
                      likes=data.get("likes"), growth=data.get("growth"),
                      edges=data.get("edges"))
    print(json.dumps(detect(ds), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:] if len(sys.argv) > 1 else []
    if a and a[0] == "--json":
        _cli_json(a[1] if len(a) > 1 else "{}")
    else:
        _cli_demo()