#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_rewrite_check.py — 改写效果回归验证（v5.1.0 新增）

定位：fix_suggest 回答「哪几句怎么改」，本脚本回答改完后的下一个问题——
「这样改，到底变了多少」。对同一篇文稿的原稿与改稿做引擎同源对比：

  1. 文档级：AI 率分数与风险带迁移（原 → 改）
  2. 段落级：difflib 模糊对齐（相似度 ≥0.5 配对），逐段分数 delta
  3. 特征级：fix_suggest 七类特征计数对比（清除 / 残留 / 新增）
  4. 幅度：字数变化比 + 段落替换率

诚实框架：分数变化是本引擎口径下的相对参考，用于作者自查改写效果；
不构成也不预示任何机构检测器的结论。改写与否、如何披露，由作者按所在
机构政策决定（学术诚信声明随输出）。

用法:
  python3 pp_rewrite_check.py <原稿> <改稿> [--json] [--lang auto]
  python3 pp_rewrite_check.py --demo
"""
import argparse
import difflib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

_INTEGRITY = ("学术诚信：本对比仅供作者自查改写效果（句式、术语、文风的相对变化），"
              "不构成也不预示任何机构检测器的结论；请按所在机构政策规范披露 AI 使用。")

_SIM_THRESHOLD = 0.5  # 段落配对的 difflib 相似度阈值


def _read(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"文件不存在: {p}")
    from docx_text import read_text_any
    return read_text_any(p)


def _risk_band(score):
    return "high" if score >= 60 else ("medium" if score >= 35 else "low")


def _feature_counts(text, lang):
    """复用 fix_suggest 引擎口径，返回 {type: count} 与 flagged 句数。"""
    import pp_fix_suggest
    results, stats, _ = pp_fix_suggest.analyze(text, lang=lang)
    return dict(stats.get("type_counts") or {}), stats


def _paragraph_scores(text, lang):
    import ai_detector
    rep = ai_detector.detect(text, lang=lang)
    paras = ai_detector.split_paragraphs(text)
    items = []
    for i, p in enumerate(paras):
        s = None
        for ps in rep.paragraph_scores:
            if ps.get("index") == i:
                s = ps.get("ai_score")
                break
        items.append({"index": i, "text": p.strip(), "score": float(s) if s is not None else None})
    return rep, items


def _align_pairs(orig_items, rev_items):
    """difflib 顺序对齐：相似度 ≥0.5 配对；返回 [(orig_item|None, rev_item|None, ratio)]。"""
    pairs = []
    used_rev = set()
    for o in orig_items:
        best, best_r = None, 0.0
        for r in rev_items:
            if r["index"] in used_rev:
                continue
            ratio = difflib.SequenceMatcher(None, o["text"], r["text"]).ratio()
            if ratio > best_r:
                best, best_r = r, ratio
        if best is not None and best_r >= _SIM_THRESHOLD:
            used_rev.add(best["index"])
            pairs.append((o, best, best_r))
        else:
            pairs.append((o, None, 0.0))
    for r in rev_items:
        if r["index"] not in used_rev:
            pairs.append((None, r, 0.0))
    return pairs


def rewrite_check(original: str, revised: str, lang: str = "auto") -> dict:
    """引擎同源对比原稿与改稿，返回 JSON 兼容 dict。

    异常语义与 pp_api 一致：非字符串/空白输入 ValueError。
    """
    if not isinstance(original, str) or not original.strip():
        raise ValueError("original 必须是非空字符串")
    if not isinstance(revised, str) or not revised.strip():
        raise ValueError("revised 必须是非空字符串")

    import ai_detector
    import pp_api

    if lang == "auto":
        lang = ai_detector.detect_lang(original)

    rep_o, paras_o = _paragraph_scores(original, lang)
    rep_r, paras_r = _paragraph_scores(revised, lang)
    s_o = float(rep_o.overall_ai_score)
    s_r = float(rep_r.overall_ai_score)

    feat_o, stats_o = _feature_counts(original, lang)
    feat_r, stats_r = _feature_counts(revised, lang)
    types = sorted(set(feat_o) | set(feat_r))
    feat_delta = [{"type": t,
                   "original": feat_o.get(t, 0),
                   "revised": feat_r.get(t, 0),
                   "change": feat_r.get(t, 0) - feat_o.get(t, 0)} for t in types]

    para_pairs = _align_pairs(paras_o, paras_r) if lang == "zh" else []
    para_rows, replaced, n_pairs = [], 0, 0
    for o, r, ratio in para_pairs:
        def _ex(item):
            return (item.get("text", "")[:100] if item else "")
        if o is not None and r is not None:
            n_pairs += 1
            d = (r["score"] or 0) - (o["score"] or 0)
            para_rows.append({"pair": f"O{o['index'] + 1}→R{r['index'] + 1}",
                              "similarity": round(ratio, 3),
                              "original_score": o["score"], "revised_score": r["score"],
                              "delta": round(d, 1),
                              "original_excerpt": _ex(o), "revised_excerpt": _ex(r)})
        elif o is not None:
            replaced += 1
            para_rows.append({"pair": f"O{o['index'] + 1}→(新增/重写)", "similarity": 0.0,
                              "original_score": o["score"], "revised_score": None, "delta": None,
                              "original_excerpt": _ex(o), "revised_excerpt": ""})
        else:
            para_rows.append({"pair": f"(原稿无)→R{r['index'] + 1}", "similarity": 0.0,
                              "original_score": None, "revised_score": r["score"], "delta": None,
                              "original_excerpt": "", "revised_excerpt": _ex(r)})
    replaced += sum(1 for o, r, _ in para_pairs if o is None)

    return {
        "engine_version": pp_api.engine_version(),
        "language": lang,
        "document": {
            "original_score": round(s_o, 1), "revised_score": round(s_r, 1),
            "delta": round(s_r - s_o, 1),
            "original_risk": rep_o.overall_risk, "revised_risk": rep_r.overall_risk,
            "risk_moved": rep_o.overall_risk != rep_r.overall_risk,
            "degraded_mode": bool(getattr(rep_r, "degraded_mode", False)),
        },
        "edit_extent": {
            "original_chars": len(original), "revised_chars": len(revised),
            "char_change_ratio": round((len(revised) - len(original)) / max(len(original), 1), 3),
            "paragraphs_original": len(paras_o), "paragraphs_revised": len(paras_r),
            "paired_paragraphs": n_pairs, "replaced_or_new_paragraphs": replaced,
        },
        "features": {"original_total": stats_o.get("flagged_sentences", 0),
                     "revised_total": stats_r.get("flagged_sentences", 0),
                     "delta_by_type": feat_delta},
        "paragraphs": para_rows,
        "integrity_notice": _INTEGRITY,
        "notice": ("分数变化是本引擎口径下的相对参考：用于比较同一篇文稿改写前后的"
                   "引擎读数变化，不与任何机构检测器互换（能力边界矩阵适用）。"),
    }



# ── v6.2.0: 双栏对照 HTML（自包含，零外部资源，全部文本 html.escape） ──
import html as _html

_HTML_CSS = """
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;margin:24px;color:#222;max-width:1180px}
h1{font-size:20px}h2{font-size:16px;margin-top:24px}
table{border-collapse:collapse;width:100%;font-size:13px;margin-top:10px}
th,td{border:1px solid #ddd;padding:5px 8px;text-align:left;vertical-align:top}
th{background:#f5f5f5}
.cards{display:flex;gap:12px;margin:14px 0;flex-wrap:wrap}
.card{border:1px solid #e3e3e3;border-radius:6px;padding:10px 16px;min-width:130px}
.card b{font-size:22px;display:block}
.badge{color:#fff;border-radius:3px;padding:1px 7px;font-size:12px}
.down{color:#27ae60;font-weight:bold}.up{color:#c0392b;font-weight:bold}
.note{color:#777;font-size:12px;margin-top:16px}.muted{color:#888;font-size:12px}
td.ex{max-width:430px}
"""


def _esc(text, limit=100):
    s = str(text or "").replace("\n", " ").strip()
    return _html.escape(s[:limit] + ("…" if len(s) > limit else ""))


def _badge(risk):
    color = {"high": "#c0392b", "medium": "#e67e22", "low": "#27ae60",
             "unknown": "#7f8c8d"}.get(str(risk or ""), "#7f8c8d")
    return f'<span class="badge" style="background:{color}">{_html.escape(str(risk or "?"))}</span>'


def render_html(r, title):
    """对比结果 dict → 自包含双栏对照 HTML。"""
    d = r["document"]
    delta = d["delta"]
    net = f"{delta:+.1f}"
    cls = "down" if delta < -0.05 else ("up" if delta > 0.05 else "")
    moved = "风险带迁移 ✓" if d["risk_moved"] else "风险带未变"
    parts = [f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>{_html.escape(title)}</title><style>{_HTML_CSS}</style></head><body>
<h1>{_html.escape(title)}</h1>
<div class="cards">
<div class="card"><b>{_html.escape(str(d["original_score"]))}</b>原稿 {_badge(d["original_risk"])}</div>
<div class="card"><b>{_html.escape(str(d["revised_score"]))}</b>改稿 {_badge(d["revised_risk"])}</div>
<div class="card"><b class="{cls}">{net}</b>分数变化（{moved}）</div>
<div class="card"><b>{r["features"]["original_total"]} → {r["features"]["revised_total"]}</b>标记句数</div>
</div>"""]
    if d.get("degraded_mode"):
        parts.append('<p class="muted">⚠️ 降级档对比（无监督模型）：医学文本只采信 @high 档；'
                     '两轮同档位时对比才有意义。</p>')
    parts.append("<h2>逐段对照（difflib 对齐，相似度 ≥0.5 配对）</h2>")
    head = ("<tr><th>对齐</th><th>相似度</th>"
            "<th>原稿摘录（分数）</th><th>改稿摘录（分数）</th><th>变化</th></tr>")
    body = []
    for row in r["paragraphs"]:
        dl = row.get("delta")
        if dl is None:
            dcell, dcls = "—", ""
        else:
            dcell = f"{dl:+.1f}"
            dcls = "down" if dl < -0.05 else ("up" if dl > 0.05 else "")
        body.append(f"<tr><td>{_html.escape(row['pair'])}</td>"
                    f"<td>{row['similarity']}</td>"
                    f"<td class='ex'>{_esc(row.get('original_excerpt'))} "
                    f"({row.get('original_score') if row.get('original_score') is not None else '—'})</td>"
                    f"<td class='ex'>{_esc(row.get('revised_excerpt'))} "
                    f"({row.get('revised_score') if row.get('revised_score') is not None else '—'})</td>"
                    f"<td class='{dcls}'>{dcell}</td></tr>")
    parts.append(f"<table>{head}{''.join(body)}</table>")
    if r["features"]["delta_by_type"]:
        frows = "".join(
            f"<tr><td>{_html.escape(x['type'])}</td><td>{x['original']}</td>"
            f"<td>{x['revised']}</td><td class='{'down' if x['change'] < 0 else ('up' if x['change'] > 0 else '')}'>"
            f"{x['change']:+d}</td></tr>"
            for x in r["features"]["delta_by_type"])
        parts.append("<h2>特征类型增减</h2>"
                     "<table><tr><th>类型</th><th>原稿</th><th>改稿</th><th>变化</th></tr>"
                     + frows + "</table>")
    parts.append(f'<p class="note">{_html.escape(r.get("integrity_notice", ""))}<br>'
                 f'{_html.escape(r.get("notice", ""))} ｜ 引擎 {_html.escape(r.get("engine_version", "?"))} ｜ '
                 f'单文件渲染，零外部资源、零网络</p>')
    parts.append("</body></html>")
    return "\n".join(parts)

def to_text(r: dict) -> str:
    d = r["document"]
    e = r["edit_extent"]
    f = r["features"]
    lines = [
        "── 改写效果对比 ──",
        f"文档级：{d['original_score']} ({d['original_risk']}) → {d['revised_score']} "
        f"({d['revised_risk']})｜变化 {d['delta']:+.1f}"
        + ("｜风险带迁移 ✓" if d["risk_moved"] else "｜风险带未变"),
        f"幅度：{e['original_chars']} → {e['revised_chars']} 字"
        f"（{e['char_change_ratio']:+.1%}）｜段落 {e['paragraphs_original']} → "
        f"{e['paragraphs_revised']}（配对 {e['paired_paragraphs']}，重写/新增 "
        f"{e['replaced_or_new_paragraphs']}）",
        f"特征句：{f['original_total']} → {f['revised_total']}",
        "",
    ]
    rows = [x for x in f["delta_by_type"] if x["change"] or x["original"] or x["revised"]]
    if rows:
        lines.append("特征类型变化（清除为负 / 残留为正 / 新增为正）：")
        for x in rows:
            mark = "清除" if x["change"] < 0 else ("新增" if x["change"] > 0 else "不变")
            lines.append(f"  · {x['type']}: {x['original']} → {x['revised']}（{mark}）")
        lines.append("")
    moved = [x for x in r["paragraphs"] if x.get("delta") is not None]
    moved.sort(key=lambda x: x["delta"])
    if moved:
        lines.append("段落级变化（降最多前 5 / 升最多前 3）：")
        for x in moved[:5]:
            lines.append(f"  ↓ {x['pair']} 相似 {x['similarity']:.0%}: "
                         f"{x['original_score']} → {x['revised_score']}（{x['delta']:+.1f}）")
        for x in moved[-3:]:
            if x["delta"] > 0 and x not in moved[:5]:
                lines.append(f"  ↑ {x['pair']} 相似 {x['similarity']:.0%}: "
                             f"{x['original_score']} → {x['revised_score']}（{x['delta']:+.1f}）")
        lines.append("")
    lines.append(r["notice"])
    lines.append(r["integrity_notice"])
    return "\n".join(lines)


_DEMO_ORIG = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。"
              "具体而言，AI 不仅能够提高诊断效率，而且可以优化治疗方案的制定。"
              "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。"
              "在一定程度上，数据安全问题的存在对行业发展产生了一定的制约。"
              "综上所述，本研究为该领域的进一步探索提供了一定的参考价值。")
_DEMO_REV = ("过去两年，我们科室把 AI 辅助读片接进了 312 例急诊 CT 的初筛。"
             "读片时间从平均 11 分钟降到 4 分钟，漏诊率没有升高。"
             "代价是新的问题：系统把 6 例伪影误报成出血，医生复核时顶住了压力。"
             "数据共享协议至今没谈拢，三家医院各留了一手。"
             "这套流程值不值得推广，取决于你所在科室有没有复核的第二双眼睛。")


def run_demo():
    print("=" * 20, "样例：原稿（AI 感）→ 改稿（具体化重写）", "=" * 20)
    r = rewrite_check(_DEMO_ORIG, _DEMO_REV)
    print(to_text(r))


def main():
    ap = argparse.ArgumentParser(description="改写效果回归验证（原稿 vs 改稿，引擎同源）")
    ap.add_argument("original", nargs="?", help="原稿文件")
    ap.add_argument("revised", nargs="?", help="改稿文件")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--html", metavar="PATH", default=None,
                    help="输出双栏对照 HTML 报告（v6.2.0：原文/改稿并排+逐段分数迁移）")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo:
        run_demo()
        return 0
    if not args.original or not args.revised:
        ap.print_help()
        return 2
    try:
        orig, rev = _read(args.original), _read(args.revised)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    for name, t in (("原稿", orig), ("改稿", rev)):
        if len(t.strip()) < 100:
            print(f"ERROR: {name}不足 100 字（铁律 2：短文本不出判定），无法做有效对比。", file=sys.stderr)
            return 2
    r = rewrite_check(orig, rev, lang=args.lang)
    if getattr(args, "html", None):
        out_html = Path(args.html)
        out_html.write_text(render_html(r, f"改写对照 · {Path(args.original).stem} → {Path(args.revised).stem}"),
                            encoding="utf-8")
        print(f"对照 HTML 已生成: {out_html}")
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print(to_text(r))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
