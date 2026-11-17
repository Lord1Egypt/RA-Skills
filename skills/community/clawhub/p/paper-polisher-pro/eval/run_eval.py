#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_eval — Paper Polisher 检测引擎评测框架（Phase 0 基线 → 后续各阶段回归）。

指标（对齐学界口径）：
  AUROC            排序判别力（C-ReD/DetectRL 论文同款）
  TPR@FPR=1%/5%    人类误报率控制在1%/5%时的AI检出率（学术期刊实际口径）
  分模型检出        每个生成器的独立表现（模型指纹有效性的直接证据）
  人类误报率        总体 + 医学子集（论文/CSL摘要，领域误报防护）
  攻击衰减          paraphrase/mixed/adversarial 下 AUROC 相对降幅

用法：
  python run_eval.py --tag baseline_v2.0          # 全量
  python run_eval.py --tag xxx --sample 800       # 抽样加速
输出：eval/results/<tag>.json + 控制台摘要表
"""
import os, sys, json, random, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import ai_detector  # noqa: E402

RESULTS = os.path.join(HERE, "results")


# ── 引擎适配层（未来 v3 引擎在此注册）──
def score_current(text):
    r = ai_detector.detect(text, lang="zh")
    # detect() 返回 DetectionReport 对象（非 dict）
    for k in ("overall_ai_score", "ai_score", "score"):
        v = getattr(r, k, None) if not isinstance(r, dict) else r.get(k)
        if v is not None:
            return float(v)
    return 0.0


ENGINES = {"current": score_current}

# 部署模型指纹: 缓存键必须绑定具体权重——换模型而键不变会让评测静默复用旧分
# (2026-10-02 事故: v36 换模后 score_cache 全命中, "位级 0.9022" 实为 v35 陈旧分)。
MODEL_FP = "unset"

# v5.6.0: 打分器内容哈希入缓存键——模型指纹绑定（v4.8.0）之外补上代码维度。
# 教训（10-14 L14 层实测复现）：改打分逻辑不改键 → 评测静默复放旧分（10-02 事故同族）。
def _scorer_ver():
    import hashlib
    h = hashlib.md5()
    here = os.path.dirname(os.path.abspath(__file__))
    for rel in ("../scripts/ai_detector.py",
                "../references/ai_patterns_zh.json",
                "../references/ai_patterns_en.json"):
        fp = os.path.join(here, rel)
        if os.path.isfile(fp):
            with open(fp, "rb") as f:
                h.update(f.read())
    return h.hexdigest()[:8]


SCORER_VER = "unset"


def _model_fp():
    """部署监督模型 md5 前 12 位; 无模型(纯规则)返回 'rules'。"""
    import hashlib
    from layers_lm import DET_DIR
    mp = os.path.join(DET_DIR, "model.int8.onnx")
    if not os.path.isfile(mp):
        return "rules"
    h = hashlib.md5()
    with open(mp, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


# ── 指标 ──
def auroc(pairs):
    """pairs: [(score, label)] label 1=AI。秩法AUROC（含并列处理）。"""
    if not pairs:
        return None
    pos = [s for s, l in pairs if l == 1]
    neg = [s for s, l in pairs if l == 0]
    if not pos or not neg:
        return None
    ranked = sorted(pairs, key=lambda x: x[0])
    # 并列取平均秩
    ranks = {}
    i = 0
    while i < len(ranked):
        j = i
        while j < len(ranked) and ranked[j][0] == ranked[i][0]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[id(ranked[k])] = avg
        i = j
    sum_pos = sum(ranks[id(p)] for p in ranked if p[1] == 1)
    n1, n0 = len(pos), len(neg)
    return round((sum_pos - n1 * (n1 + 1) / 2) / (n1 * n0), 4)


def tpr_at_fpr(pos_scores, neg_scores, fpr):
    """在人类FPR≤fpr 的最高阈值下的AI检出率。"""
    if not pos_scores or not neg_scores:
        return None
    thr = sorted(neg_scores)[min(len(neg_scores) - 1, int((1 - fpr) * len(neg_scores)))]
    # 找满足 FPR≤fpr 的最高阈值
    import bisect
    srt = sorted(neg_scores)
    k = int((1 - fpr) * len(srt))
    if k >= len(srt):
        thr = srt[-1] + 1e-9
    else:
        thr = srt[k]
    det = sum(1 for s in pos_scores if s >= thr)
    return round(det / len(pos_scores), 4), round(thr, 2)


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def evaluate(recs, engine, cache, tag):
    """打分（带缓存）并计算全部指标。"""
    for r in recs:
        cid = "%s:%s:%s:%s" % (tag, MODEL_FP, SCORER_VER, r["id"])
        if cache.get(cid) is None:
            try:
                v = engine(r["text"])
                if v is not None:
                    cache[cid] = v
            except Exception as e:
                if not hasattr(evaluate, "_warned"):
                    print("  [warn] 打分异常: %s" % e)
                    evaluate._warned = True
        r["_score"] = cache.get(cid)
    scored = [r for r in recs if r.get("_score") is not None]

    base = [r for r in scored if r["attack"] == "none"]
    pos = [r["_score"] for r in base if r["label"] == 1]
    neg = [r["_score"] for r in base if r["label"] == 0]

    res = {"n": len(scored), "n_base": len(base),
           "model_fp": MODEL_FP,
           "auroc": auroc([(r["_score"], r["label"]) for r in base])}
    for fpr in (0.01, 0.05):
        t = tpr_at_fpr(pos, neg, fpr)
        res["tpr@fpr%d%%" % (fpr * 100)] = t[0] if t else None
        res["thr@fpr%d%%" % (fpr * 100)] = t[1] if t else None

    # 人类误报（v3: 优先用引擎校准阈值 fusion_config.thresholds; 找不到回退35/60）
    fc_path = os.path.join(HERE, "..", "references", "fusion_config.json")
    thr_m, thr_h = 35.0, 60.0
    try:
        fc = json.load(open(fc_path, encoding="utf-8"))
        thr_m = float(fc["thresholds"]["medium"]) * 100
        thr_h = float(fc["thresholds"]["high"]) * 100
    except Exception:
        pass
    hu = [r for r in base if r["label"] == 0]
    res["thresholds"] = {"medium": round(thr_m, 1), "high": round(thr_h, 1)}
    res["human_fpr@med"] = round(sum(1 for r in hu if r["_score"] >= thr_m) / max(len(hu), 1), 4)
    res["human_fpr@high"] = round(sum(1 for r in hu if r["_score"] >= thr_h) / max(len(hu), 1), 4)
    hu_med = [r for r in hu if r.get("is_medical")]
    if hu_med:
        res["human_med_fpr@med"] = round(sum(1 for r in hu_med if r["_score"] >= thr_m) / len(hu_med), 4)

    # 分模型
    per_model = {}
    models = sorted(set(r["model"] for r in base if r["label"] == 1))
    for m in models:
        mp = [r["_score"] for r in base if r["label"] == 1 and r["model"] == m]
        thr = res.get("thr@fpr5%")
        per_model[m] = {"n": len(mp), "mean": round(sum(mp) / len(mp), 1),
                        "tpr@thr5%": round(sum(1 for s in mp if s >= thr) / len(mp), 4) if thr else None}
    res["per_model"] = per_model

    # 攻击衰减（与全体human对照）
    if neg:
        for atk in ("paraphrase", "mixed", "adversarial"):
            ap_ = [r for r in scored if r.get("attack") == atk]
            if ap_:
                pairs = [(r["_score"], r["label"]) for r in ap_] + [(s, 0) for s in neg]
                a = auroc(pairs)
                res["auroc_%s" % atk] = a
                if res["auroc"] and a is not None:
                    res["decay_%s" % atk] = round(1 - a / max(res["auroc"], 1e-9), 4)
    # 长度分段（Phase 2 路由依据）
    bands = {"short<300": (0, 300), "mid300-800": (300, 800), "long>800": (800, 10 ** 9)}
    res["auroc_by_len"] = {}
    for name, (lo, hi) in bands.items():
        seg = [(r["_score"], r["label"]) for r in base if lo <= r["length"] < hi]
        a = auroc(seg)
        if a is not None:
            res["auroc_by_len"][name] = a
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=os.path.join(HERE, "corpora_small", "eval_zh.jsonl"))
    ap.add_argument("--attacks", default=os.path.join(HERE, "corpora_small", "attacks.jsonl"))
    ap.add_argument("--tag", default="run")
    ap.add_argument("--engine", default="current", choices=list(ENGINES.keys()))
    ap.add_argument("--sample", type=int, default=0, help="每格子抽样加速(0=全量)")
    ap.add_argument("--layer", default=None,
                    help="报告层独立评测(如 surprisal): 对该层 0-10 分做 AUROC 统计, 不走主融合")
    ap.add_argument("--split", default="all", choices=["all", "calib", "test"],
                    help="test=只评留出半(诚实数字,频谱/权重未见过)")
    a = ap.parse_args()

    global MODEL_FP
    MODEL_FP = _model_fp()
    global SCORER_VER
    SCORER_VER = _scorer_ver()
    # v4.8.0: 规则档评测独立命名空间（外部测试发现#1——PP_NO_SUP 不入键会导致
    # 规则档评测重放监督层缓存分, 基础引擎指标不可复现）
    if os.environ.get("PP_NO_SUP") == "1":
        MODEL_FP += ":nosup"

    recs = load(a.corpus)
    if os.path.exists(a.attacks):
        recs += load(a.attacks)
    if a.split != "all":
        sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
        from pp_split import filter_split
        recs = filter_split(recs, a.split)
    if a.sample:
        random.seed(7)
        by_cell = {}
        for r in recs:
            by_cell.setdefault((r["source"], r["model"], r.get("attack", "none")), []).append(r)
        recs = []
        for pool in by_cell.values():
            random.shuffle(pool)
            recs += pool[:a.sample]

    os.makedirs(RESULTS, exist_ok=True)
    if a.layer:
        import importlib.util
        from pp_split import filter_split
        spec = importlib.util.spec_from_file_location(
            "layers_surface", os.path.join(os.path.dirname(HERE), "scripts", "layers_surface.py"))
        LS = importlib.util.module_from_spec(spec); spec.loader.exec_module(LS)
        _LAYER_FN = {"surprisal": lambda txt: (LS.surprisal_variation_layer(txt) or {}).get("score", 0.0)}
        if a.layer not in _LAYER_FN:
            print(f"未知报告层: {a.layer}（可用: {list(_LAYER_FN)}）")
            return 2
        fn = _LAYER_FN[a.layer]
        recs = [json.loads(l) for l in open(a.corpus, encoding="utf-8") if l.strip()]
        recs = [r for r in recs if r.get("attack") == "none"]
        data = filter_split(recs, a.split)
        pairs = []
        for r in data:
            if len(r["text"]) <= 800:  # L13 仅对长文有效
                continue
            pairs.append((fn(r["text"]), r["label"]))
        au = auroc(pairs)
        n_ai = sum(1 for _, y in pairs if y == 1)
        n_hu = len(pairs) - n_ai
        det6 = sum(1 for s, y in pairs if y == 1 and s >= 6)
        fp6 = sum(1 for s, y in pairs if y == 0 and s >= 6)
        print("─" * 50)
        print(f"报告层评测 [{a.layer}] split={a.split} 长文(>800字)")
        print(f"  样本: {len(pairs)} (AI {n_ai} / 人类 {n_hu})")
        print(f"  AUROC          : {au:.4f}")
        print(f"  检出率@≥6      : {det6}/{n_ai}")
        print(f"  人类误报@≥6    : {fp6}/{n_hu}")
        print(f"  [汇总] layer={a.layer} auroc={au:.4f} det={det6}/{n_ai} fpr={fp6}/{n_hu} -> "
              f"{'PASS' if au >= 0.6 else 'REVIEW'}")
        out = {"layer": a.layer, "split": a.split, "n": len(pairs), "auroc": au,
               "det_at6": det6, "n_ai": n_ai, "fpr_at6": fp6, "n_hu": n_hu}
        rp = os.path.join(RESULTS, f"layer_{a.layer}_{a.tag}.json")
        json.dump(out, open(rp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"  结果: {rp}")
        return 0

    cache_path = os.path.join(RESULTS, "score_cache.json")
    cache = json.load(open(cache_path, encoding="utf-8")) if os.path.exists(cache_path) else {}

    print("评测: engine=%s tag=%s model_fp=%s 样本=%d ..." % (a.engine, a.tag, MODEL_FP, len(recs)))
    res = evaluate(recs, ENGINES[a.engine], cache, a.engine)

    json.dump(cache, open(cache_path, "w", encoding="utf-8"), ensure_ascii=False)
    res["engine"], res["tag"] = a.engine, a.tag
    outp = os.path.join(RESULTS, a.tag + ".json")
    json.dump(res, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # 摘要输出
    print("\n┌─ 摘要 [%s/%s] ─────────────────────────────" % (a.engine, a.tag))
    print("│ 样本 %d (基线集 %d)" % (res["n"], res["n_base"]))
    print("│ AUROC            : %s" % res["auroc"])
    print("│ TPR@FPR1%% / 5%%  : %s / %s" % (res.get("tpr@fpr1%"), res.get("tpr@fpr5%")))
    print("│ 人类误报@med/@high: %.1f%% / %.1f%%  (阈值 %.0f/%.0f)" % (100 * res["human_fpr@med"], 100 * res["human_fpr@high"], res["thresholds"]["medium"], res["thresholds"]["high"]))
    if "human_med_fpr@med" in res:
        print("│ 人类医学误报@med : %.1f%%" % (100 * res["human_med_fpr@med"]))
    print("│ 攻击AUROC(para/mixed/adv): %s / %s / %s" %
          (res.get("auroc_paraphrase"), res.get("auroc_mixed"), res.get("auroc_adversarial")))
    print("│ 长度分段AUROC    : %s" % res.get("auroc_by_len"))
    print("└─ 分模型 (n | 均分 | TPR@thr5%%):")
    for m, v in sorted(res["per_model"].items(), key=lambda x: -x[1]["mean"]):
        print("   %-22s %4d | %5.1f | %s" % (m, v["n"], v["mean"], v["tpr@thr5%"]))
    print("\n结果: %s" % outp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
