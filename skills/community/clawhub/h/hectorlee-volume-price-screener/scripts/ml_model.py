#!/usr/bin/env python3
"""
V2 ML 概率模型 - 预测"命中后20日上涨概率"
===========================================
训练数据来自 backtest.py 导出的 jsonl 样本（每条含量价特征 + 未来收益）。

模型: XGBoost 二分类（优先）→ sklearn GradientBoosting（降级）→ 逻辑回归（兜底）
标签: fwd20 > 0（命中后20日上涨）

用法:
  python ml_model.py --train data/ml_samples.jsonl --save models/ml_model.json
  python ml_model.py --predict --model models/ml_model.json   # 交互/管道模式
  python ml_model.py --eval --train data/ml_samples.jsonl    # 交叉验证评估

特征（全部来自形态识别结果，纯量价）:
  surge_pct, volume_ratio, shrink_days, shrink_depth, amplitude,
  range_position(0/1/2), pullback_ratio, low_point_rise(0/1),
  breakout_60d(0/1), ma_support(0/1), vol_ma_bull(0/1),
  conc_rise_3d(0/1), conc_fall_3d(0/1), score
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, List, Optional

FEATURES = [
    "surge_pct", "volume_ratio", "shrink_days", "shrink_depth", "amplitude",
    "range_position_num", "pullback_ratio", "low_point_rise",
    "breakout_60d", "ma_support", "vol_ma_bull",
    "conc_rise_3d", "conc_fall_3d", "score",
]

POS_MAP = {"lower": 0, "mid": 1, "upper": 2}


def load_samples(path: str) -> List[dict]:
    """加载回测导出的样本"""
    samples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            s = json.loads(line)
            if "fwd20" not in s:
                continue
            samples.append(s)
    return samples


def extract_feature_vector(sample: dict) -> List[float]:
    """从样本提取特征向量"""
    return [
        float(sample.get("surge_pct", 0)),
        float(sample.get("volume_ratio", 0)),
        float(sample.get("shrink_days", 0)),
        float(sample.get("shrink_depth", 0)),
        float(sample.get("amplitude", 0)),
        POS_MAP.get(sample.get("range_position", "mid"), 1),
        float(sample.get("pullback_ratio", 0)),
        1.0 if sample.get("low_point_rise") else 0.0,
        1.0 if sample.get("breakout_60d") else 0.0,
        1.0 if sample.get("ma_support") else 0.0,
        1.0 if sample.get("vol_ma_bull") else 0.0,
        1.0 if sample.get("conc_rise_3d") else 0.0,
        1.0 if sample.get("conc_fall_3d") else 0.0,
        float(sample.get("score", 0)),
    ]


def make_dataset(samples: List[dict], fwd_field: str = "fwd20"):
    """构造 X, y 数据集"""
    X, y = [], []
    for s in samples:
        if fwd_field not in s:
            continue
        X.append(extract_feature_vector(s))
        y.append(1.0 if s[fwd_field] > 0 else 0.0)
    return X, y


def _get_model(backend: str):
    """按优先级获取模型"""
    if backend == "xgboost":
        from xgboost import XGBClassifier
        return XGBClassifier(
            n_estimators=200, max_depth=4, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, eval_metric="logloss",
            use_label_encoder=False, verbosity=0, random_state=42)
    if backend == "sklearn":
        from sklearn.ensemble import GradientBoostingClassifier
        return GradientBoostingClassifier(n_estimators=200, max_depth=3,
                                          learning_rate=0.05, random_state=42)
    from sklearn.linear_model import LogisticRegression
    return LogisticRegression(max_iter=2000, random_state=42)


def resolve_backend() -> str:
    """选择可用后端（不仅 import，还实测 fit/predict 避免运行时缺库）"""
    for candidate in ("xgboost", "sklearn"):
        try:
            if candidate == "xgboost":
                from xgboost import XGBClassifier
                m = XGBClassifier(n_estimators=2, max_depth=1, verbosity=0,
                                  use_label_encoder=False)
            else:
                from sklearn.ensemble import GradientBoostingClassifier
                m = GradientBoostingClassifier(n_estimators=2, max_depth=1)
            # 实测 fit/predict（触发底层库加载）
            m.fit([[0.0, 1.0], [1.0, 0.0]], [0, 1])
            m.predict_proba([[0.5, 0.5]])
            return candidate
        except Exception:
            continue
    return "logistic"


def train(samples: List[dict], backend: str = "auto",
          fwd_field: str = "fwd20") -> tuple:
    """训练模型，返回 (model, metrics)"""
    X, y = make_dataset(samples, fwd_field)
    if len(X) < 50:
        raise ValueError(f"样本不足（{len(X)}），至少需要50条")
    if backend == "auto":
        backend = resolve_backend()

    model = _get_model(backend)
    # 简单时间序列划分：前70%训练，后30%验证（避免未来函数）
    split = int(len(X) * 0.7)
    X_tr, y_tr = X[:split], y[:split]
    X_va, y_va = X[split:], y[split:]
    model.fit(X_tr, y_tr)
    probs = model.predict_proba(X_va)[:, 1]
    preds = [1 if p >= 0.5 else 0 for p in probs]
    acc = sum(1 for a, b in zip(preds, y_va) if a == b) / len(y_va)
    base_rate = sum(y_va) / len(y_va)  # 基线（全部猜1的准确率）
    # 简单AUC（面积法）
    auc = _simple_auc(y_va, probs)
    metrics = {
        "backend": backend, "n_samples": len(X),
        "n_train": len(X_tr), "n_valid": len(y_va),
        "accuracy": round(acc, 4), "base_rate": round(base_rate, 4),
        "auc": round(auc, 4),
        "fwd_field": fwd_field,
    }
    return model, metrics


def _simple_auc(y_true: List[float], y_score: List[float]) -> float:
    """简化AUC（Mann-Whitney U，处理并列取平均秩）"""
    pairs = sorted(zip(y_score, y_true), key=lambda x: x[0])
    n = len(pairs)
    pos = sum(1 for _, t in pairs if t == 1)
    neg = n - pos
    if pos == 0 or neg == 0:
        return 0.5
    # 计算正样本的平均秩（并列取平均）
    sum_rank_pos = 0.0
    i = 0
    while i < n:
        j = i
        while j < n and pairs[j][0] == pairs[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0   # 该并列组的平均秩
        for k in range(i, j):
            if pairs[k][1] == 1:
                sum_rank_pos += avg_rank
        i = j
    auc = (sum_rank_pos - pos * (pos + 1) / 2) / (pos * neg)
    return max(0.0, min(1.0, auc))


def save_model(model, path: str, metrics: dict):
    """保存模型（含元数据）"""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    import pickle
    with open(path, "wb") as f:
        pickle.dump({"model": model, "metrics": metrics, "features": FEATURES}, f)
    print(f"[ML] 模型已保存: {path}（{metrics['backend']}，AUC={metrics['auc']}）")


def load_model(path: str) -> dict:
    import pickle
    with open(path, "rb") as f:
        return pickle.load(f)


def predict(model, sample: dict) -> float:
    """预测单样本上涨概率"""
    X = [extract_feature_vector(sample)]
    return float(model.predict_proba(X)[0][1])


def main():
    ap = argparse.ArgumentParser(description="V2 ML概率模型")
    ap.add_argument("--train", help="训练样本路径(.jsonl)")
    ap.add_argument("--save", default="models/ml_model.pkl", help="模型保存路径")
    ap.add_argument("--eval", action="store_true", help="训练后输出评估")
    ap.add_argument("--backend", default="auto", choices=["auto", "xgboost", "sklearn", "logistic"])
    ap.add_argument("--fwd", default="fwd20", help="预测目标（fwd5/10/20）")
    args = ap.parse_args()

    if not args.train:
        ap.print_help()
        sys.exit(1)

    print(f"[ML] 加载样本: {args.train}")
    samples = load_samples(args.train)
    print(f"[ML] 样本数: {len(samples)}（目标 {args.fwd}>0）")
    if not samples:
        print("[ML] 无样本，请先运行 backtest.py --export")
        sys.exit(1)

    t0 = time.time()
    model, metrics = train(samples, backend=args.backend, fwd_field=args.fwd)
    print(f"[ML] 训练完成 {time.time()-t0:.1f}s")
    print(f"[ML] {metrics}")
    save_model(model, args.save, metrics)


if __name__ == "__main__":
    main()
