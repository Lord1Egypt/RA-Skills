#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/hf_sample_kit.py — HF-P1 真实样本接入 / 打样 / 校准套件（v2.2.0）

背景：HF-P1（协同簇融合 A/B/C→A/B/C/D + 权重校准 + FPR ≤ 2% 基线）中，
「权重校准」与「误报率基线」依赖真实标注样本，而沙箱不具备真实环境。
本套件提供**真实样本接入契约**与**可复现校准管线**：真实样本紧缺时用半合成
打样（source=synthetic）演练全链，真实样本到位后**同一切入口复用**（source=real）。

三件事（对应 HF-P1 判据）：
  1. validate_sample —— 真实样本接入门控（schema/类型/范围/标签完整性）
  2. make_synthetic  —— 半合成打样（零网络、固定 seed 可复现，供校准演练）
  3. calibrate       —— 在 FPR ≤ 2% 约束下最大化 recall，输出**推荐 D 权重 + 判定阈值**

零依赖（纯标准库 + 同目录 identity_confidence_fusion），零网络，不采集任何真实账号。

CLI:
  python scripts/hf_sample_kit.py --demo                    # 打样 + 校准全链自检
  python scripts/hf_sample_kit.py --validate sample.json    # 仅校验真实样本
  python scripts/hf_sample_kit.py --calibrate sample.json   # 用真实样本校准
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from identity_confidence_fusion import (  # noqa: E402
    DEFAULT_WEIGHTS, norm_cluster, norm_cross, norm_site, norm_trust,
)

SAMPLE_SCHEMA = "infoseek-hf-sample/1"

# 校准约束与网格
MAX_FPR = 0.02                       # HF-P1 判据：FPR ≤ 2%
_ABC_RATIO = (7.0, 8.0, 5.0)         # a:b:c 固定比例（与默认权重一致）
_D_GRID = [round(0.0 + 0.05 * i, 2) for i in range(0, 11)]   # d ∈ [0.00, 0.50]

# 真实样本 schema 字段契约
REQUIRED_FIELDS = ("label", "cross_platform_matches", "trust_score", "site_rank")
OPTIONAL_FIELDS = ("username", "platform", "url",
                   "coord_cluster_size", "coord_cluster_density", "sync_group_size")
NUMERIC_FIELDS = ("cross_platform_matches", "trust_score", "site_rank",
                  "coord_cluster_size", "coord_cluster_density", "sync_group_size")


# ═══════════════════════════════════════════════════════════════
# 1) 样本 schema 校验（真实样本接入门控）
# ═══════════════════════════════════════════════════════════════

def validate_sample(sample: Dict) -> Tuple[bool, List[str]]:
    """校验样本契约：返回 (ok, issues)。空样本/坏标签/坏类型/越界均记录。"""
    issues: List[str] = []
    if not isinstance(sample, dict):
        return False, ["样本根节点非对象"]
    if sample.get("schema") not in (None, SAMPLE_SCHEMA):
        issues.append(f"schema 非 {SAMPLE_SCHEMA}")
    recs = sample.get("records")
    if not isinstance(recs, list) or not recs:
        return False, (issues + ["records 缺失或为空"])

    n_bad_label = n_bad_num = n_missing = 0
    n_pos = 0
    for i, r in enumerate(recs):
        if not isinstance(r, dict):
            n_missing += 1
            continue
        if any(r.get(f) is None for f in REQUIRED_FIELDS):
            n_missing += 1
            continue
        try:
            lab = int(r["label"])
        except (TypeError, ValueError):
            n_bad_label += 1
            continue
        if lab not in (0, 1):
            n_bad_label += 1
            continue
        n_pos += lab
        for f in NUMERIC_FIELDS:
            v = r.get(f)
            if v is None:
                continue
            try:
                float(v)
            except (TypeError, ValueError):
                n_bad_num += 1
                break
        if r.get("trust_score") is not None:
            try:
                ts = float(r["trust_score"])
                if ts < 0 or ts > 100:
                    n_bad_num += 1
            except (TypeError, ValueError):
                n_bad_num += 1

    if n_missing:
        issues.append(f"{n_missing} 条记录缺必填字段 {REQUIRED_FIELDS}")
    if n_bad_label:
        issues.append(f"{n_bad_label} 条 label 非法（须 0/1）")
    if n_bad_num:
        issues.append(f"{n_bad_num} 条数值字段类型/范围非法")
    if n_pos == 0 or n_pos == len(recs):
        issues.append(f"标签单类（pos={n_pos}/{len(recs)}），无法校准")
    return (not issues), issues


def load_sample(path: str) -> Dict:
    """读 JSON 或 CSV 样本 → 标准化 dict。CSV 首行为表头。"""
    if str(path).endswith(".json"):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    import csv
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    recs = []
    for r in rows:
        rec = {}
        for k, v in r.items():
            if v in (None, ""):
                continue
            if k == "label":
                rec[k] = int(float(v))
            elif k in NUMERIC_FIELDS:
                rec[k] = float(v) if "." in str(v) else int(float(v))
            else:
                rec[k] = v
        recs.append(rec)
    return {"schema": SAMPLE_SCHEMA, "source": "real", "records": recs}


# ═══════════════════════════════════════════════════════════════
# 2) 半合成打样（零网络 + 固定 seed 可复现）
# ═══════════════════════════════════════════════════════════════

def make_synthetic(n_normal: int = 160, n_mob: int = 60, seed: int = 11) -> Dict:
    """生成半合成 HF-P1 样本（供无真实样本时演练校准管线）。

    正常账号：中高交叉命中 / 高信任分 / 高权威站点 / 弱协同簇。
    关联水军：低交叉 / 低信任分 / 长尾站点 / 强协同簇（簇规模+密度+同步组）。
    """
    rng = random.Random(seed)
    recs: List[Dict] = []

    def _add(label: int, n: int, gen) -> None:
        for i in range(n):
            recs.append(gen(i, label))

    def _normal(i: int, label: int) -> Dict:
        return {
            "username": f"real_{i}", "platform": "web",
            "url": f"https://example{i % 7}.com/u{i}",
            "label": label,
            "cross_platform_matches": rng.choice([1, 2, 2, 3, 4, 5]),
            "trust_score": round(rng.uniform(72, 96), 1),
            "site_rank": int(10 ** rng.uniform(1.0, 3.7)),
            "coord_cluster_size": rng.choice([0, 0, 0, 1]),
            "coord_cluster_density": round(rng.uniform(0.0, 0.15), 2),
            "sync_group_size": rng.choice([0, 0, 0, 1]),
        }

    def _mob(i: int, label: int) -> Dict:
        """笨水军：三因子即暴露（低信任分 + 长尾站点 + 低交叉）。"""
        return {
            "username": f"mob_{i}", "platform": "web",
            "url": f"https://tail{i % 5}.example.org/u{i}",
            "label": label,
            "cross_platform_matches": rng.choice([0, 0, 1, 1, 2]),
            "trust_score": round(rng.uniform(8, 36), 1),
            "site_rank": int(10 ** rng.uniform(5.0, 6.2)),
            "coord_cluster_size": rng.choice([3, 4, 5, 6, 7, 9]),
            "coord_cluster_density": round(rng.uniform(0.3, 0.9), 2),
            "sync_group_size": rng.choice([2, 3, 4, 5, 6, 8]),
        }

    def _mob_stealth(i: int, label: int) -> Dict:
        """伪装水军（G3/G4 型）：三因子接近正常账号，**仅协同簇暴露** —— 检验 D 因子增益。"""
        return {
            "username": f"stl_{i}", "platform": "web",
            "url": f"https://mid{i % 4}.example.net/u{i}",
            "label": label,
            "cross_platform_matches": rng.choice([2, 3, 3, 4]),
            "trust_score": round(rng.uniform(66, 90), 1),
            "site_rank": int(10 ** rng.uniform(3.0, 4.5)),
            "coord_cluster_size": rng.choice([4, 5, 6, 7, 8]),
            "coord_cluster_density": round(rng.uniform(0.4, 0.9), 2),
            "sync_group_size": rng.choice([3, 4, 5, 6]),
        }

    n_naive = n_mob // 2
    _add(0, n_normal, _normal)
    _add(1, n_naive, _mob)
    _add(1, n_mob - n_naive, _mob_stealth)
    rng.shuffle(recs)
    return {"schema": SAMPLE_SCHEMA, "source": "synthetic",
            "created": "2026-09-21", "seed": seed, "records": recs}


# ═══════════════════════════════════════════════════════════════
# 3) 权重校准（FPR ≤ 2% 约束下最大化 recall）
# ═══════════════════════════════════════════════════════════════

def _weights_for_d(wd: float) -> Dict[str, float]:
    """按 a:b:c = 7:8:5 分配剩余 (1-wd) 权重给三因子。"""
    s = sum(_ABC_RATIO)
    rest = max(0.0, 1.0 - wd)
    a, b, c = (r / s * rest for r in _ABC_RATIO)
    return {"a": round(a, 4), "b": round(b, 4), "c": round(c, 4), "d": round(wd, 4)}


def _row_norms(rec: Dict) -> Optional[Tuple[float, float, float, float]]:
    """记录 → 四因子归一值；B 或 D 缺失 → None（校准只用四因子齐全记录）。"""
    a, _ = norm_cross(rec.get("cross_platform_matches"))
    b, _ = norm_trust(rec.get("trust_score"))
    c, _ = norm_site(rec.get("url") or "", rec.get("site_rank"))
    d, _ = norm_cluster(rec.get("coord_cluster_size"),
                        rec.get("coord_cluster_density"), rec.get("sync_group_size"))
    if b is None or d is None:
        return None
    return a, b, c, d


def _scan_threshold(confs: List[float], labels: List[int],
                    max_fpr: float = MAX_FPR) -> Tuple[float, float, float]:
    """在 FPR ≤ max_fpr 约束下扫描阈值，返回 (阈值, recall, fpr)。

    判定语义：**共识置信度 ≤ 阈值 → 判为可疑/水军（label=1 为检测目标）**，
    故置信度越低越可疑（与 fusion confidence_final 语义一致）。
    """
    pos = sum(labels)
    neg = len(labels) - pos
    best = (0.0, 0.0, 0.0)
    for i in range(101):
        t = i / 100.0
        tp = sum(1 for c, l in zip(confs, labels) if c <= t and l == 1)
        fp = sum(1 for c, l in zip(confs, labels) if c <= t and l == 0)
        fpr = fp / max(neg, 1)
        rec = tp / max(pos, 1)
        if fpr <= max_fpr and rec > best[1]:
            best = (t, rec, fpr)
    return best


def calibrate(sample: Dict, d_grid: Optional[List[float]] = None) -> Dict:
    """用样本校准四因子权重（a:b:c 比例固定，仅搜 D 权重）与判定阈值。

    返回 {ok, n, n_pos, best:{d,weights,threshold,recall,fpr}, curve:[...]}。
    真实样本到位后，把推荐权重写入 INFOSEEK_FUSION_WEIGHTS 即生效。
    """
    recs = (sample or {}).get("records") or []
    rows = []
    for r in recs:
        if not isinstance(r, dict) or r.get("label") not in (0, 1):
            continue
        nr = _row_norms(r)
        if nr is not None:
            rows.append((nr, int(r["label"])))
    if len(rows) < 20:
        return {"ok": False, "reason": f"四因子齐全记录不足（{len(rows)}<20）",
                "n": len(rows)}

    d_grid = d_grid or _D_GRID
    curve = []
    best = None
    for wd in d_grid:
        w = _weights_for_d(wd)
        confs = [a * w["a"] + b * w["b"] + c * w["c"] + (1.0 - d) * w["d"]
                 for (a, b, c, d), _ in rows]
        labels = [l for _, l in rows]
        t, rec, fpr = _scan_threshold(confs, labels)
        curve.append({"d": wd, "threshold": t, "recall": round(rec, 4),
                      "fpr": round(fpr, 4)})
        if best is None or rec > best["recall"]:
            best = {"d": wd, "weights": w, "threshold": t,
                    "recall": round(rec, 4), "fpr": round(fpr, 4)}
    return {"ok": True, "n": len(rows),
            "n_pos": sum(l for _, l in rows),
            "best": best, "curve": curve}


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def _demo() -> int:
    print("=" * 66)
    print("HF-P1 样本套件自检：半合成打样 → 校验 → 校准（FPR ≤ 2%）")
    print("=" * 66)
    print(f"默认权重（HF-P1 四因子）: {DEFAULT_WEIGHTS}")
    s = make_synthetic()
    ok, issues = validate_sample(s)
    print(f"\n[打样] records={len(s['records'])} source={s['source']} "
          f"校验={'通过' if ok else '失败'} {issues or ''}")
    cal = calibrate(s)
    print(f"\n[校准] n={cal.get('n')} n_pos={cal.get('n_pos')}")
    if cal.get("ok"):
        b = cal["best"]
        print(f"  推荐 D 权重={b['d']}  weights={b['weights']}")
        print(f"  判定阈值={b['threshold']}  recall={b['recall']}  FPR={b['fpr']}"
              f"（约束 ≤ {MAX_FPR}）")
        print("  D 权重扫描曲线（前 6）:")
        for row in cal["curve"][:6]:
            print(f"    d={row['d']:.2f}  thr={row['threshold']:.2f}  "
                  f"recall={row['recall']:.3f}  fpr={row['fpr']:.3f}")
    else:
        print(f"  校准未完成: {cal.get('reason')}")
    print("\n[判据] 缺因子降级不中断 / 权重非法回退默认 —— 由 tests/test_hf_p1_v220.py 守护")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="HF-P1 样本接入/打样/校准套件")
    ap.add_argument("--demo", action="store_true", help="打样+校准全链自检")
    ap.add_argument("--validate", metavar="PATH", help="校验真实样本 JSON/CSV")
    ap.add_argument("--calibrate", metavar="PATH", help="用真实样本校准权重")
    args = ap.parse_args()

    if args.validate:
        s = load_sample(args.validate)
        ok, issues = validate_sample(s)
        print(json.dumps({"ok": ok, "n": len(s.get("records", [])), "issues": issues},
                         ensure_ascii=False, indent=2))
        return 0 if ok else 1
    if args.calibrate:
        s = load_sample(args.calibrate)
        ok, issues = validate_sample(s)
        if not ok:
            print(json.dumps({"ok": False, "issues": issues}, ensure_ascii=False, indent=2))
            return 1
        print(json.dumps(calibrate(s), ensure_ascii=False, indent=2))
        return 0
    return _demo()


if __name__ == "__main__":
    sys.exit(main())
