#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""interpretable-attribution: 可解释归因引擎（model-agnostic）。

给出"为什么模型/规则在这个样本上做出这个预测"，而不只是黑箱输出。
能力：
  1. 全局重要性(permutation importance)：打乱某特征，看整体评分下降。
  2. 局部重要性(local ablation)：把待测样本某特征置为基值，看预测变化。
  3. 反事实(counterfactual)：最少改动哪些特征即可翻转预测。
  4. 自然语言归因：top-k 特征 -> 可读决策理由。
纯标准库，零依赖；--selftest 内置样例实测。
"""
import os, sys, json, random, statistics, argparse

def _baseline(rows, feat, is_num):
    vals = [r[feat] for r in rows]
    if is_num:
        return statistics.median(vals)
    # 分类：众数
    from collections import Counter
    return Counter(vals).most_common(1)[0][0]

def _score(predict, rows, label_key):
    """对二分类/回归打分：正确率(分类)或 -MAE(回归，越高越好)。"""
    ok = 0; errs = []
    for r in rows:
        try:
            y = predict(r); t = r.get(label_key)
        except Exception:
            continue
        if isinstance(t, bool) or set(map(type, [t, y])) <= {int, float, bool} and isinstance(t, (int, float)):
            if isinstance(t, bool):
                ok += 1 if (y >= 0.5) == t else 0
            else:
                errs.append(abs(y - t))
        else:
            ok += 1 if y == t else 0
    if errs:
        return -statistics.mean(errs)
    return ok / len(rows) if rows else 0.0

def global_importance(predict, rows, label_key, feats, n_perm=20, seed=0):
    rnd = random.Random(seed)
    base = _score(predict, rows, label_key)
    out = {}
    for f in feats:
        drops = []
        is_num = all(isinstance(r.get(f), (int, float)) for r in rows)
        bl = _baseline(rows, f, is_num)
        for _ in range(n_perm):
            perm = list(rows)
            vals = [r[f] for r in perm]
            rnd.shuffle(vals)
            for i, r in enumerate(perm):
                r = dict(r); r[f] = bl if False else vals[i]
                perm[i] = r
            drops.append(base - _score(predict, perm, label_key))
        out[f] = round(statistics.mean(drops), 4)
    return dict(sorted(out.items(), key=lambda x: -x[1])), round(base, 4)

def local_importance(predict, inst, rows, label_key, feats):
    base = predict(inst)
    out = {}
    for f in feats:
        is_num = isinstance(inst.get(f), (int, float))
        bl = _baseline(rows, f, is_num)
        abl = dict(inst); abl[f] = bl
        out[f] = round(abs(predict(abl) - base), 4)
    return dict(sorted(out.items(), key=lambda x: -x[1])), base

def _candidates(rows, f, is_num):
    vals = [r[f] for r in rows]
    if is_num:
        return [min(vals), max(vals)]
    # 分类：尝试每个离散取值
    return list(dict.fromkeys(vals))

def counterfactual(predict, inst, feats, target_class, rows, max_flip=5):
    """贪心反事实：每次选「置为极值/离散候选后预测最接近 target」的特征翻转，直至命中或达上限。"""
    cur = predict(inst); steps = []; work = dict(inst)
    for _ in range(max_flip):
        if _same_class(cur, target_class):
            break
        best_f, best_score, best_val = None, None, None
        for f in feats:
            is_num = isinstance(inst.get(f), (int, float))
            for cand_val in _candidates(rows, f, is_num):
                if cand_val == work.get(f):
                    continue
                c = dict(work); c[f] = cand_val
                sc = predict(c)
                if best_score is None or abs(sc - target_class) < abs(best_score - target_class):
                    best_score, best_f, best_val = sc, f, cand_val
        if best_f is None:
            break
        steps.append(best_f); work[best_f] = best_val; cur = best_score
    return steps, cur

def _same_class(pred, target):
    if isinstance(target, bool):
        return (pred >= 0.5) == target
    return pred == target

def rationale(top_feats, kind="positive"):
    if not top_feats:
        return "无可归因特征。"
    nonzero = [(k, v) for k, v in top_feats if v and v > 0]
    if not nonzero:
        return "该样本远离决策边界，单特征置基值均不改变预测（预测稳健，局部重要性≈0）。"
    parts = [f"{k}(影响 {v})" for k, v in nonzero[:3]]
    return f"该决策主要由 {', '.join(parts)} 驱动（{kind}贡献）。"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="数据集 json 路径(list of dicts)")
    ap.add_argument("--label", default="label")
    ap.add_argument("--predict", help="预测函数 py 文件(定义 predict(r)->val)")
    ap.add_argument("--instance", help="待解释样本 json 路径")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.data and a.predict and a.instance):
        print("用法: attributor.py --data d.json --predict p.py --instance i.json [--label label]"); sys.exit(2)
    ns = {}; exec(compile(open(a.predict, encoding="utf-8").read(), a.predict, "exec"), ns)
    predict = ns["predict"]
    rows = json.load(open(a.data, encoding="utf-8"))
    inst = json.load(open(a.instance, encoding="utf-8"))
    feats = [k for k in rows[0] if k != a.label]
    g, base = global_importance(predict, rows, a.label, feats)
    l, lbase = local_importance(predict, inst, rows, a.label, feats)
    print(json.dumps({"global_importance": g, "base_score": base,
                     "local_importance": l, "local_pred": lbase,
                     "rationale": rationale(list(l.items()))}, ensure_ascii=False, indent=2))

def selftest():
    # 合成：y = 2*A - B + 噪声(无)，A 应主导
    rnd = random.Random(1)
    rows = []
    for _ in range(60):
        A = rnd.uniform(0, 10); B = rnd.uniform(0, 10); C = rnd.choice(["x", "y"])
        rows.append({"A": A, "B": B, "C": C, "label": 1 if (2 * A - B) > 5 else 0})
    def predict(r):
        return 1 if (2 * r["A"] - r["B"]) > 5 else 0
    feats = ["A", "B", "C"]
    g, base = global_importance(predict, rows, "label", feats, n_perm=10, seed=2)
    inst = {"A": 8.0, "B": 9.0, "C": "x"}
    l, lbase = local_importance(predict, inst, rows, "label", feats)
    steps, cur = counterfactual(predict, inst, feats, 0, rows)
    assert list(g.keys())[0] == "A", f"全局重要性 A 应居首，实际 {list(g.keys())}"
    assert list(l.keys())[0] == "A", f"局部重要性 A 应居首，实际 {list(l.keys())}"
    assert lbase == 1, f"样本局部预测应为1，实际 {lbase}"
    assert cur == 0, f"反事实应翻转为0，实际 cur={cur} steps={steps}"
    print("✅ selftest PASS：A 为全局/局部首要特征，反事实可翻转预测")
    print(json.dumps({"global_top": list(g.items())[:2], "local_top": list(l.items())[:2],
                     "cf_steps": steps, "cf_pred": cur, "rationale": rationale(list(l.items()))},
                    ensure_ascii=False, indent=2))
    return True

if __name__ == "__main__":
    main()
