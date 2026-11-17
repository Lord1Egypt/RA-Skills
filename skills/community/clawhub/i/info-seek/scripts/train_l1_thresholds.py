#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/train_l1_thresholds.py — HF-P1 L1 阈值重训骨架 (mod-v1.0.0)

固化 forensics_retrain.py 阶段 1 (坐标下降, FPR<=2% 约束) 为可独立运行的管道;
无真实样本时由 make_synthetic_accounts 自造合成账号数据驱动跑通 (对齐 data_adapter
Dataset 格式: meta_df[index=id] + likes/growth dict{id:array} + G/timing 可选)。

能力:
  1) --demo : 合成账号数据(默认 400 正常 / 120 水军 ×120 天) → 60/40 分层重训 → 出报告
  2) --data : 真实元表(CSV/JSON/parquet, 须含 group_label/label/is_fake/group 标注) → 重训
  3) --write: 原子写回 extensions/fake_detect/l1_thresholds.json (默认只读, 只出报告)

依赖: numpy / pandas / scipy / networkx / l1_engine / data_adapter (extensions/fake_detect)

权限: 只读文件(--data); 可选写文件(--write 原子回写带备份, 默认关闭); 无网络/无子进程/无敏感环境变量
安全: 默认不改动任何资产; --write 才写回(备份旧 l1_thresholds.json 到 .bak)
"""
import argparse
import json
import os
import sys
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parent.parent
_FD = _ROOT / "extensions" / "fake_detect"
for _p in (str(_FD), str(_ROOT / "scripts"), str(_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import data_adapter  # noqa: E402
import l1_engine  # noqa: E402

MOD_VERSION = "mod-v1.0.0"
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


# ═══════════════════════════════════════════════════════════════════════
# 合成账户样本生成器 (无真实样本由 Agent 自造, 对齐 data_adapter.Dataset)
# ═══════════════════════════════════════════════════════════════════════

def make_synthetic_accounts(n_normal=400, n_fake=120, T=120, seed=SEED):
    """合成 B3 标注账号数据, 返回 data_adapter.Dataset。

    - 正常(group_label=0): likes 幂律(首位近似 Benford 友好) + 平滑 growth + 中性 ER
    - 水军(group_label>=1): likes 首位集中(1/2 开头)破坏 Benford + 末段 growth 尖峰 + 极端 ER
    """
    rng = np.random.default_rng(seed)
    n = n_normal + n_fake
    ids = list(range(n))
    likes, growth, rows = {}, {}, []
    for i in ids:
        if i < n_normal:
            g = 0
            # 幂律点赞: 首位分布近似 Benford (chi2 p 较高, 多数不触发 L1a)
            ser = np.round(10 ** rng.uniform(1.0, 3.5, T)).astype(float)
            # 平滑增长曲线 (小波动随机游走, 无尖峰)
            gser = np.maximum(0.0, np.cumsum(rng.normal(0, 2, T)) + rng.uniform(-5, 15))
            er = float(rng.uniform(0.015, 0.045))  # 安全区(避开 er_high=0.05), 防正常误判
            followers = int(10 ** rng.uniform(3, 5))
            following = int(10 ** rng.uniform(2.5, 4))
        else:
            g = 1
            # 首位集中(1/2 开头)的小整数 -> Benford 偏离 (L1a 触发)
            ser = np.array([float(f"{rng.choice(['1','2'])}{rng.integers(0,9)}" + "0" * int(rng.integers(1, 3)))
                            for _ in range(T)])
            # 末段暴涨尖峰 (前段 0, 末 20-40 天暴涨) -> L1c 触发
            gser = np.zeros(T)
            k = int(rng.integers(80, 100))
            gser[k:] = rng.uniform(50, 200, size=T - k)
            # 极端 ER (极低或极高) -> L1b 触发
            er = float(rng.choice([rng.uniform(1e-6, 5e-5), rng.uniform(0.06, 0.09)]))
            followers = int(10 ** rng.uniform(2, 4))
            following = int(10 ** rng.uniform(3, 5))
        likes[i] = ser
        growth[i] = gser
        rows.append(dict(id=i, group_label=g, followers=followers, following=following,
                         posts=int(rng.integers(10, 500)), er=er))
    # 注意: 不 set_index('id') — data_adapter._clean_meta 需 'id' 在列中探测;
    # compute_l1_features 用 df.index 查 likes/growth, 本生成器 id==range(0..N-1) 与默认 index 一致
    meta_df = pd.DataFrame(rows)
    ds = data_adapter.from_raw(meta_df=meta_df, likes=likes, growth=growth)
    return ds


# ═══════════════════════════════════════════════════════════════════════
# 重训算法 (固化自 forensics_retrain.py 阶段 1)
# ═══════════════════════════════════════════════════════════════════════

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
        raise ValueError("元表缺少标注列 group_label/label/is_fake/group（HF-P1 需标注数据）")
    groups = pd.to_numeric(meta[ycol], errors='coerce').fillna(0).astype(int).values
    y = (groups > 0).astype(int)
    norm = (groups == 0)
    if y.sum() == 0 or norm.sum() == 0:
        raise ValueError(f"标注不平衡：水军={int(y.sum())} 正常={int(norm.sum())}（重训需双类）")
    feats = l1_engine.compute_l1_features(meta, ds.likes, ds.growth, ds.G, ds.timing)
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
        "metrics": {
            "train": tr_metric,
            "holdout_default": {"recall": round(float(rec_d), 4), "fpr": round(float(fpr_d), 4)},
            "holdout_trained": {"recall": round(float(rec_t), 4), "fpr": round(float(fpr_t), 4)},
        },
        "candidates": CANDIDATES,
        "fpr_cap": FPR_CAP,
        "mod_version": MOD_VERSION,
    }


# ═══════════════════════════════════════════════════════════════════════
# 资产写回 (原子, 带备份)
# ═══════════════════════════════════════════════════════════════════════

def write_thresholds(th_new: dict, out_path: Path):
    """原子写回 l1_thresholds.json (备份旧文件); 仅 --write 调用。"""
    out_path = Path(out_path)
    if out_path.exists():
        shutil.copyfile(out_path, out_path.with_suffix(out_path.suffix + ".bak"))
    payload = {"DEFAULT_THRESHOLDS": th_new, "retrained_by": "train_l1_thresholds",
               "mod_version": MOD_VERSION}
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(out_path)
    print(f"  [write] 已写回 {out_path} (旧文件备份 .bak)")


# ═══════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="HF-P1 L1 阈值重训骨架")
    ap.add_argument("--demo", action="store_true", help="合成账户数据 self-check")
    ap.add_argument("--data", help="真实元表路径 (CSV/JSON/parquet, 须含标注列)")
    ap.add_argument("--ts-dir", help="时序目录 (可选; 每账号一个 csv/npy)")
    ap.add_argument("--graph", help="关系图 edgelist/nx (可选)")
    ap.add_argument("--out-dir", default=str(_FD / "retrain_out"), help="输出目录")
    ap.add_argument("--write", action="store_true", help="写回 l1_thresholds.json (默认只读)")
    ap.add_argument("--json", action="store_true", help="报告以 JSON 输出")
    args = ap.parse_args()

    if args.demo:
        print("=" * 60)
        print(f"[HF-P1 demo] 合成账号数据 self-check ({MOD_VERSION})")
        print("=" * 60)
        ds = make_synthetic_accounts()
        print(f"  合成样本: n={len(ds.meta_df)} (正常={int((ds.meta_df['group_label']==0).sum())} "
              f"水军={int((ds.meta_df['group_label']>0).sum())}), T={120}")
        rep = retrain_l1(ds, verbose=not args.json)
    elif args.data:
        print(f"[HF-P1] 加载真实数据: {args.data}")
        ds = data_adapter.load_dataset(source=args.data, ts_path=args.ts_dir, graph_src=args.graph)
        rep = retrain_l1(ds, verbose=not args.json)
    else:
        ap.error("需 --demo 或 --data")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rep_path = out_dir / "l1_retrain_report.json"
    rep_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(f"\n[报告] 已写 {rep_path}")

    if args.write:
        th = rep["trained_thresholds"]
        write_thresholds(th, _FD / "l1_thresholds.json")
    else:
        print("[安全] 未 --write, 未改动任何资产 (仅出报告)")


if __name__ == "__main__":
    main()
