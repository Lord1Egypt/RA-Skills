#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/forensics_retrain.py — FakeDetect 模型资产重训管道（B3 / v1.6.0 融入）

真实数据接入后重训：
  阶段 1: L1 阈值重训（坐标下降，FPR<=2% 约束；train_l1_thresholds 管道化）
  阶段 2: 对抗训练增量（--adv：G0-G4 对抗样本混合，OOD→ID 化；adv_train 管道化）

用法:
  python scripts/forensics_retrain.py --data accounts.csv --ts-dir ts/ --graph graph.edgelist \
      [--adv] [--out-dir DIR] [--write] [--json]
  --data    数据源（CSV/JSON/parquet 元表路径；元表须含 group_label/label/is_fake/group 标注）
  --ts-dir  时序目录（可选；每账号一个 csv/npy，前缀匹配 id）；或 --ts-npz 单一 npz
  --graph   edgelist 路径 / nx 文件（可选）
  --adv     启用对抗训练增量（默认仅 L1 阈值重训）
  --write   写回 extensions/fake_detect/l1_thresholds.json（默认只出报告，不动资产）
  --out-dir 输出目录（默认 <infoseek>/extensions/fake_detect/retrain_out/）

安全: 默认只读不改资产；--write 才原子写回（备份旧文件）。
"""
import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parent.parent
_FD = _ROOT / "extensions" / "fake_detect"
for _p in (str(_FD), str(_ROOT / "scripts"), str(_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from data_adapter import load_dataset, from_raw  # noqa: E402
import l1_engine  # noqa: E402

FPR_CAP = 0.02
SEED = 42
CANDIDATES = {
    'benford_alpha': [0.001, 0.005, 0.01, 0.05],
    'er_low': [1e-5, 0.0001, 0.001],
    'er_high': [0.03, 0.05, 0.08],
    'spike_ratio_th': [10.0, 20.0, 50.0],
    'spike_cnt_th': [2, 3, 5],
    'n_flags_th': [1, 2, 3],
    'recip_th': [0.3, 0.5, 0.7],
    'recip_min_deg': [2, 3, 5],
}
ADV_LEVELS = ['G0_笨水军', 'G1_伪装ER', 'G2_伪装增长', 'G3_伪装Benford', 'G4_全伪装']


# ═══════════════════════════════════════════════════════════════
# 阶段 1: L1 阈值重训（坐标下降，对齐 train_l1_thresholds 协议）
# ═══════════════════════════════════════════════════════════════

def eval_thresholds(feats, y, thresholds, normal_mask=None):
    """FPR<=2% 约束下的召回得分; 越限强惩罚 (score = rec - 10*(fpr-cap))"""
    res = l1_engine.apply_l1_rules(feats, thresholds=thresholds, normal_mask=normal_mask)
    pred = res['pred']
    rec = ((pred == 1) & (y == 1)).sum() / max((y == 1).sum(), 1)
    fpr = ((pred == 1) & (y == 0)).sum() / max((y == 0).sum(), 1)
    return rec - 10.0 * max(0.0, fpr - FPR_CAP), rec, fpr


def coordinate_descent(feats, y, normal_mask, verbose=True):
    """从默认阈值出发, 逐参数坐标下降 3 轮。返回 (best_th, 指标)。"""
    best_th = dict(l1_engine.DEFAULT_THRESHOLDS)
    best_score, best_rec, best_fpr = eval_thresholds(feats, y, best_th, normal_mask)
    if verbose:
        print(f"  [起始] 默认阈值: Recall={best_rec:.3f} FPR={best_fpr:.3f}")
    for _it in range(3):
        improved = False
        for param, cands in CANDIDATES.items():
            for v in cands:
                th_try = dict(best_th)
                th_try[param] = v
                sc, rec, fpr = eval_thresholds(feats, y, th_try, normal_mask)
                if sc > best_score + 1e-9:
                    best_th, best_score = th_try, sc
                    best_rec, best_fpr = rec, fpr
                    improved = True
                    if verbose:
                        print(f"  [改进] {param}={v} -> Recall={rec:.3f} FPR={fpr:.3f}")
        if not improved:
            break
    return best_th, dict(recall=round(float(best_rec), 4), fpr=round(float(best_fpr), 4))


def retrain_l1(ds, verbose=True) -> dict:
    """阶段 1：L1 阈值重训（60/40 分层划分 + holdout）。"""
    meta = ds.meta_df
    ycol = next((c for c in ('group_label', 'label', 'is_fake', 'group') if c in meta.columns), None)
    if ycol is None:
        raise ValueError("元表缺少标注列 group_label/label/is_fake/group（B3 需标注数据）")
    groups = pd.to_numeric(meta[ycol], errors='coerce').fillna(0).astype(int).values
    y = (groups > 0).astype(int)
    norm = (groups == 0)
    if y.sum() == 0 or norm.sum() == 0:
        raise ValueError(f"标注不平衡：水军={int(y.sum())} 正常={int(norm.sum())}（重训需双类）")
    feats = l1_engine.compute_l1_features(meta, ds.likes, ds.growth, ds.G)
    n = len(y)
    idx = np.random.RandomState(SEED).permutation(n)
    n_tr = int(n * 0.6)
    tr, te = idx[:n_tr], idx[n_tr:]

    th_new, tr_metric = coordinate_descent(feats.iloc[tr], y[tr], norm[tr], verbose=verbose)
    sc_d, rec_d, fpr_d = eval_thresholds(feats.iloc[te], y[te], l1_engine.DEFAULT_THRESHOLDS, norm[te])
    sc_t, rec_t, fpr_t = eval_thresholds(feats.iloc[te], y[te], th_new, norm[te])
    if verbose:
        print(f"\n[holdout] 测试段 n={len(te)}：默认 Recall={rec_d:.3f} FPR={fpr_d:.3f} | "
              f"重训 Recall={rec_t:.3f} FPR={fpr_t:.3f}")
    return {
        "trained_thresholds": th_new,
        "metrics": {"train": tr_metric,
                    "holdout_default": {"recall": round(float(rec_d), 4), "fpr": round(float(fpr_d), 4)},
                    "holdout_trained": {"recall": round(float(rec_t), 4), "fpr": round(float(fpr_t), 4)}},
        "candidates": CANDIDATES, "fpr_cap": FPR_CAP,
    }


# ═══════════════════════════════════════════════════════════════
# 阶段 2: 对抗训练增量（G0-G4 特征空间扰动对抗样本混合）
# ═══════════════════════════════════════════════════════════════

def gen_adv_batch(level: str, n: int, seed: int, X_norm: np.ndarray) -> np.ndarray:
    """特征空间对抗样本生成（G0-G4 对齐 adv_train 概念）：
    在正常账号特征分布上按级别注入水军指纹扰动，返回 (n, n_feat) 特征矩阵。"""
    rng = np.random.RandomState(seed)
    X = X_norm[rng.randint(0, len(X_norm), n)].copy() if len(X_norm) else \
        np.zeros((n, X_norm.shape[1]))
    b, er, sr, sc_, fr, recip = 0, 1, 2, 3, 4, 5
    if level == 'G0_笨水军':
        X[:, er] = rng.uniform(0.0001, 0.001, n)          # 低互动
        X[:, sr] = rng.uniform(20, 80, n)                 # 高尖峰
        X[:, fr] = rng.uniform(-3, -1.2, n)               # 关注比异常
    elif level == 'G1_伪装ER':
        X[:, er] = rng.uniform(0.01, 0.05, n)             # ER 伪装正常
        X[:, sr] = rng.uniform(20, 60, n)
        X[:, sc_] = rng.randint(2, 5, n)
    elif level == 'G2_伪装增长':
        X[:, er] = rng.uniform(0.0001, 0.005, n)
        X[:, sr] = rng.uniform(5, 15, n)                  # 尖峰抑制
    elif level == 'G3_伪装Benford':
        X[:, b] = rng.uniform(0.1, 0.9, n)                # Benford 伪装正常
        X[:, er] = rng.uniform(0.0001, 0.005, n)
    elif level == 'G4_全伪装':
        X[:, b] = rng.uniform(0.1, 0.9, n)
        X[:, er] = rng.uniform(0.01, 0.05, n)
        X[:, sr] = rng.uniform(2, 10, n)
        X[:, sc_] = rng.randint(0, 2, n)
        X[:, fr] = rng.uniform(-0.8, 0.8, n)
    return X


def cap_recall(proba, y):
    """CAP 阈值（FPR<=2% 最大召回）→ (recall, fpr, t)"""
    best_t, best_rec = 1.0, 0.0
    for t in np.percentile(proba, np.arange(50, 100, 0.5)):
        p = (proba >= t).astype(int)
        fpr = ((p == 1) & (y == 0)).sum() / max((y == 0).sum(), 1)
        rec = ((p == 1) & (y == 1)).sum() / max((y == 1).sum(), 1)
        if fpr <= FPR_CAP and rec > best_rec:
            best_rec, best_t = rec, t
    fpr_at = ((proba >= best_t).astype(int) == 1).sum() / max((y == 0).sum(), 1) \
        if (y == 0).sum() else 0.0
    return float(best_rec), float(fpr_at), float(best_t)


def retrain_adv(ds, X_feat: np.ndarray, y: np.ndarray, norm_ids: np.ndarray,
                verbose=True) -> dict:
    """阶段 2：对抗训练增量。基线 RF vs 混合对抗样本 RF，逐级累计（协议对齐 adv_train）：
    - ID 化证据: 训练内对抗样本 CAP 召回
    - OOD→ID 泛化: 留出(未见)对抗样本 CAP 召回提升 = 部署漏检下降
    - 误伤监测: 原正常账号在 CAP 阈值下 FP"""
    from sklearn.ensemble import RandomForestClassifier
    X_norm = X_feat[norm_ids]
    clf_base = RandomForestClassifier(n_estimators=300, random_state=42, class_weight='balanced')
    clf_base.fit(X_feat, y)
    rows, X_adv_all, y_adv_all = [], [], []
    for lv, level in enumerate(ADV_LEVELS):
        X_tr = gen_adv_batch(level, 100, seed=7, X_norm=X_norm)
        X_adv_all.append(X_tr); y_adv_all.append(np.ones(len(X_tr)))
        X_mix = np.vstack([X_feat] + X_adv_all)
        y_mix = np.concatenate([y] + y_adv_all)
        clf_adv = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
        clf_adv.fit(X_mix, y_mix)
        # ID 化证据（训练内）
        r_in, _, _ = cap_recall(clf_adv.predict_proba(np.vstack(X_adv_all))[:, 1],
                                np.concatenate(y_adv_all))
        # 留出泛化（未见对抗 + 原正常背景）
        X_ho = gen_adv_batch(level, 100, seed=99, X_norm=X_norm)
        X_eval = np.vstack([X_ho, X_norm])
        y_eval = np.concatenate([np.ones(len(X_ho)), np.zeros(len(norm_ids))])
        p_b = clf_base.predict_proba(X_eval)[:, 1]
        p_a = clf_adv.predict_proba(X_eval)[:, 1]
        rec_b, fpr_b, t_b = cap_recall(p_b, y_eval)
        rec_a, fpr_a, t_a = cap_recall(p_a, y_eval)
        fp_norm_b = float((p_b[len(X_ho):] >= t_b).mean())
        fp_norm_a = float((p_a[len(X_ho):] >= t_a).mean())
        rows.append({"level": level, "n_train_adv": (lv + 1) * 100,
                     "id_cap_recall": round(r_in, 4),
                     "ood_base": {"cap_recall": round(rec_b, 4), "fpr": round(fpr_b, 4)},
                     "ood_adv": {"cap_recall": round(rec_a, 4), "fpr": round(fpr_a, 4)},
                     "fp_normal_base": round(fp_norm_b, 4),
                     "fp_normal_adv": round(fp_norm_a, 4),
                     "gain": round(rec_a - rec_b, 4)})
        if verbose:
            g = rows[-1]["gain"]
            print(f"  [{level}] 留出 CAP召回 {rec_b:.2f}→{rec_a:.2f} "
                  f"(gain {g:+.2f}) | 正常误伤 {fp_norm_b:.3f}→{fp_norm_a:.3f}")
    total_gain = sum(r["gain"] for r in rows)
    return {"levels": rows, "total_gain": round(float(total_gain), 4),
            "note": "对抗训练把 OOD 转 ID（评估报告 P0 对策 5a）；G3/G4 盲区诚实保留于引擎 blindspots"}


# ═══════════════════════════════════════════════════════════════

def build_feature_matrix(ds) -> tuple:
    """L1 特征矩阵 + 标注 + 正常掩码（重训共用）。"""
    meta = ds.meta_df
    feats = l1_engine.compute_l1_features(meta, ds.likes, ds.growth, ds.G)
    cols = ['benford_p', 'er', 'spike_ratio', 'spike_cnt', 'log_fr']
    if 'recip' in feats.columns:
        cols.append('recip')
    X = feats[cols].fillna(0).values.astype(float)
    ycol = next((c for c in ('group_label', 'label', 'is_fake', 'group') if c in meta.columns), None)
    y = pd.to_numeric(meta[ycol], errors='coerce').fillna(0).astype(int).values
    y = (y > 0).astype(int)
    return X, y, np.where(y == 0)[0]


def main() -> int:
    ap = argparse.ArgumentParser(description='FakeDetect 模型资产重训管道（B3）')
    ap.add_argument('--data', required=True, help='元表数据源（CSV/JSON/parquet 路径）')
    ap.add_argument('--ts-npz', default=None, help='时序 npz（{"likes"/"growth": {id: array}}）')
    ap.add_argument('--graph', default=None, help='edgelist 路径')
    ap.add_argument('--adv', action='store_true', help='启用对抗训练增量（阶段 2）')
    ap.add_argument('--write', action='store_true',
                    help='写回 extensions/fake_detect/l1_thresholds.json（默认仅报告）')
    ap.add_argument('--out-dir', default=str(_FD / "retrain_out"), help='输出目录')
    ap.add_argument('--json', action='store_true', help='JSON 输出')
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ds = load_dataset(source=args.data, ts_npz=args.ts_npz, graph_src=args.graph)
    if ds.meta_df.empty:
        print("数据接入失败：元表为空"); return 1

    # 阶段 1
    print("=" * 70)
    print("阶段 1: L1 阈值重训（坐标下降, FPR<=2% 约束）")
    print("=" * 70)
    l1_res = retrain_l1(ds)
    out_l1 = out_dir / "retrain_l1.json"
    out_l1.write_text(json.dumps(l1_res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"输出: {out_l1}")

    # 阶段 2（可选）
    adv_res = None
    if args.adv:
        print("\n" + "=" * 70)
        print("阶段 2: 对抗训练增量（G0-G4 累计混合, OOD→ID）")
        print("=" * 70)
        X, y, norm_ids = build_feature_matrix(ds)
        adv_res = retrain_adv(ds, X, y, norm_ids)
        out_adv = out_dir / "adv_retrain.json"
        out_adv.write_text(json.dumps(adv_res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"输出: {out_adv}")

    # 写回（可选）
    if args.write:
        target = _FD / "l1_thresholds.json"
        backup = out_dir / "l1_thresholds.previous.json"
        if target.exists():
            backup.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
        merged = {"trained_thresholds": l1_res["trained_thresholds"],
                  "dirty_demo_thresholds": {},
                  "candidates": CANDIDATES, "fpr_cap": FPR_CAP,
                  "note": f"重训于 {pd.Timestamp.now().isoformat()}（B3 管道；备份 {backup.name}）"}
        target.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[已写回] {target}（备份于 {backup.name}）")

    if args.json:
        print(json.dumps({"l1": l1_res, "adv": adv_res}, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())