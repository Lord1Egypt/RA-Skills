#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_report_html.py — 单文档自查可视化仪表盘（v5.8.0 新增）

workflow / detect / fix_suggest / style_norm 的 JSON 产物各自是机器可读片段——
论文自查最后缺一步「打开一个文件看到全部」。本脚本把一个或多个 JSON
渲染成单文件 HTML 仪表盘：内联 CSS + 内联 SVG，零外部资源、零网络、零依赖
（标准库）；不重跑引擎，只渲染既有结果；所有正文文本经 html.escape。

自动识别输入类型（按特征键，可任意组合、顺序不限）：
  - workflow 报告（含 detect/paragraphs/fix_suggest/style_norm 等全部小节）
  - ai_detector detect 输出（overall_ai_score）
  - pp_fix_suggest 输出（suggestions）
  - pp_style_norm 输出（checks_run + findings）

用法:
  python3 pp_report_html.py draft.workflow.json -o report.html
  python3 pp_report_html.py detect.json fix.json norm.json -o report.html
  python3 pp_report_html.py draft.workflow.json            # 默认 <stem>.report.html

渲染板块（有数据才渲染）：顶栏卡片（综合分/风险带/段落/档位）· 半环仪表 ·
段落分数直方图 · 段落热表（Top-N）· 改写建议表 · 规范 findings 表 ·
workflow 附加块（混写评估/门禁/术语/翻译腔/文体/质量/AIGC/台账）· 诚信页脚。
"""
import argparse
import html
import json
import sys
from datetime import datetime
from pathlib import Path

_INTEGRITY = ("学术诚信：本报告由 Paper Polisher Pro 生成，供作者自查与改进写作质量，"
              "不用于规避机构 AIGC 检测；分数为引擎口径的相对参考，不与任何机构检测器互换。")

_CSS = """
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;margin:24px;color:#222;max-width:1080px}
h1{font-size:20px} h2{font-size:16px;margin-top:26px} h3{font-size:14px}
table{border-collapse:collapse;width:100%;font-size:13px;margin-top:10px}
th,td{border:1px solid #ddd;padding:5px 8px;text-align:left;vertical-align:top}
th{background:#f5f5f5} .cards{display:flex;gap:12px;margin:14px 0;flex-wrap:wrap}
.card{border:1px solid #e3e3e3;border-radius:6px;padding:10px 16px;min-width:110px}
.card b{font-size:22px;display:block}
.hrow{display:flex;align-items:center;gap:8px;margin:3px 0}
.hlab{width:52px;font-size:12px;color:#555}.hbar{height:14px;border-radius:2px}.hnum{font-size:12px;color:#555}
.badge{color:#fff;border-radius:3px;padding:1px 7px;font-size:12px}
.note{color:#777;font-size:12px;margin-top:16px}
.muted{color:#888;font-size:12px}.ledger li{margin:3px 0}
"""


# ---------- 输入识别与装配 ----------

def classify(obj):
    """按特征键识别 JSON 类型：workflow / detect / fix / norm；未知返回 None。"""
    if not isinstance(obj, dict):
        return None
    if "detect" in obj and ("paragraphs" in obj or "style_norm" in obj or "findings_ledger" in obj):
        return "workflow"
    if "overall_ai_score" in obj:
        return "detect"
    if "suggestions" in obj or (isinstance(obj.get("stats"), dict) and "top_issues" in obj):
        return "fix"
    if "checks_run" in obj and "findings" in obj:
        return "norm"
    return None


def load_sections(paths):
    """读入全部 JSON，装配为 sections；返回 (sections, sources, skipped)。"""
    sections = {"workflow": None, "detect": None, "fix": None, "norm": None}
    sources, skipped = [], []
    for p in paths:
        try:
            obj = json.loads(Path(p).read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            skipped.append((str(p), "读取/解析失败: %s" % e))
            continue
        kind = classify(obj)
        if kind is None:
            skipped.append((str(p), "未识别的 JSON 类型"))
            continue
        sources.append("%s（%s）" % (p, kind))
        if kind == "workflow":
            sections["workflow"] = obj
        elif kind == "detect":
            sections["detect"] = obj
        elif kind == "fix":
            sections["fix"] = obj
        elif kind == "norm":
            sections["norm"] = obj
    # workflow 内含同构小节，优先级高于散件（散件仅在缺位时补）
    wf = sections["workflow"]
    if wf:
        if wf.get("detect"):
            sections["detect"] = sections["detect"] or wf["detect"]
        _fx = wf.get("fix_suggest") or {}
        if _fx.get("stats"):
            sections["fix"] = sections["fix"] or {"stats": _fx["stats"],
                                                  "suggestions": _fx.get("top_issues", [])}
        _sn = wf.get("style_norm") or {}
        if _sn.get("findings"):
            sections["norm"] = sections["norm"] or _sn
    return sections, sources, skipped


# ---------- 渲染元件（全部文本经 html.escape） ----------

def _risk_badge(risk):
    color = {"high": "#c0392b", "medium": "#e67e22", "low": "#27ae60",
             "unknown": "#7f8c8d", "ERROR": "#8e44ad"}.get(str(risk or ""), "#7f8c8d")
    return '<span class="badge" style="background:%s">%s</span>' % (
        color, html.escape(str(risk or "?")))


def _gauge(score):
    """半环仪表（内联 SVG；无外部资源）。"""
    try:
        s = max(0.0, min(100.0, float(score)))
    except (TypeError, ValueError):
        return ""
    color = "#c0392b" if s >= 60 else ("#e67e22" if s >= 35 else "#27ae60")
    # 半环半径 90，圆心 (110,110)；周长半弧 ≈ 282.7
    frac = s / 100.0
    arc = 282.7
    return f"""<svg width="220" height="130" role="img" aria-label="AI score gauge">
<path d="M 20 110 A 90 90 0 0 1 200 110" fill="none" stroke="#e8e8e8" stroke-width="18" stroke-linecap="round"/>
<path d="M 20 110 A 90 90 0 0 1 200 110" fill="none" stroke="{color}" stroke-width="18" stroke-linecap="round"
 stroke-dasharray="{arc * frac:.1f} {arc:.1f}"/>
<text x="110" y="100" text-anchor="middle" font-size="34" font-weight="bold" fill="{color}">{s:.0f}</text>
<text x="110" y="122" text-anchor="middle" font-size="12" fill="#888">AI score / 100</text>
</svg>"""


def _histogram(scores):
    """10 分一桶频次柱条（复用批量报告的内联柱条风格）。"""
    if not scores:
        return "<p class='muted'>无段落分数据</p>"
    buckets = {}
    for s in scores:
        try:
            buckets[int(float(s) // 10) * 10] = buckets.get(int(float(s) // 10) * 10, 0) + 1
        except (TypeError, ValueError):
            continue
    peak = max(buckets.values()) or 1
    out = []
    for lo in range(0, 100, 10):
        c = buckets.get(lo, 0)
        pct = round(c / peak * 100)
        color = "#c0392b" if lo >= 60 else ("#e67e22" if lo >= 35 else "#27ae60")
        out.append(f'<div class="hrow"><span class="hlab">{lo:02d}-{lo + 9:02d}</span>'
                   f'<div class="hbar" style="width:{max(pct, 1 if c else 0)}%;background:{color}"></div>'
                   f'<span class="hnum">{c}</span></div>')
    return "\n".join(out)


def _esc_cell(text, limit=120):
    t = str(text or "").replace("\n", " ").strip()
    return html.escape(t[:limit] + ("…" if len(t) > limit else ""))


def _para_table(detect, paragraphs):
    """段落热表：优先 workflow 的 paragraphs.items（带 hi/med/lo 分级）。"""
    rows = []
    thr = ""
    if isinstance(paragraphs, dict) and paragraphs.get("items"):
        p = paragraphs
        thr = ("分级阈值：medium ≥%s / high ≥%s（融合口径）"
               % (p.get("thresholds", {}).get("medium", "?"), p.get("thresholds", {}).get("high", "?")))
        cls_color = {"hi": "#c0392b", "med": "#e67e22", "lo": "#27ae60"}
        rows = sorted(p["items"], key=lambda r: -(float(r.get("score", 0) or 0)))
        body = []
        for r in rows[:12]:
            c = cls_color.get(r.get("class", ""), "#7f8c8d")
            body.append(f"<tr><td>{html.escape(str(r.get('index', '?')))}</td>"
                        f"<td><span class='badge' style='background:{c}'>{html.escape(str(r.get('class', '?')))}</span></td>"
                        f"<td>{html.escape(str(r.get('score', '')))}</td>"
                        f"<td>{_esc_cell(r.get('excerpt', ''))}</td></tr>")
        head = "<tr><th>#</th><th>分级</th><th>分</th><th>段落摘录</th></tr>"
    elif detect.get("paragraph_scores"):
        ps = sorted(detect["paragraph_scores"], key=lambda r: -(float(r.get("ai_score", 0) or 0)))
        body = []
        for r in ps[:12]:
            body.append(f"<tr><td>{html.escape(str(r.get('index', '?')))}</td>"
                        f"<td>{html.escape(str(r.get('ai_score', '')))}</td>"
                        f"<td>{_esc_cell(r.get('text', ''))}</td></tr>")
        head = "<tr><th>#</th><th>AI 分</th><th>段落摘录</th></tr>"
    else:
        return ""
    return f"<h2>段落热表（分数降序 Top 12）{('<span class=muted>　' + thr + '</span>') if thr else ''}</h2>" \
           f"<table>{head}{''.join(body)}</table>"


def _fix_table(fix):
    if not fix:
        return ""
    stats = fix.get("stats") or {}
    sug = fix.get("suggestions") or fix.get("top_issues") or []
    if not sug:
        return ""
    head = (f"<p class='muted'>共 {stats.get('total_sentences', '?')} 句，"
            f"标记 {stats.get('flagged_sentences', '?')} 句"
            f"（flag_ratio {stats.get('flag_ratio', '?')}）——建议是排序辅助，"
            f"只指位与策略，改写决定权在作者。</p>")
    body = []
    for s in sug[:10]:
        issues = "；".join(
            _esc_cell("%s：%s" % (i.get("type", "?"), i.get("advice") or i.get("evidence", "")), 70)
            for i in (s.get("issues") or [])[:4])
        body.append(f"<tr><td>{s.get('index', '?')}</td>"
                    f"<td>{_esc_cell(s.get('sentence', ''), 100)}</td>"
                    f"<td>{issues}</td></tr>")
    return (f"<h2>句子级改写建议（Top 10）</h2>{head}"
            f"<table><tr><th>#</th><th>句子</th><th>特征与建议</th></tr>{''.join(body)}</table>")


def _norm_table(norm):
    if not norm:
        return ""
    finds = norm.get("findings") or []
    if not finds:
        return ""
    body = []
    for f in finds:
        ex = "、".join(_esc_cell(x, 24) for x in (f.get("examples") or [])[:3])
        advice = _esc_cell(f.get("advice", ""), 160)
        sent = ""
        if f.get("sentences"):
            sent = "<br><span class='muted'>命中句：" + _esc_cell(
                " ｜ ".join(f["sentences"][:2]), 120) + "</span>"
        body.append(f"<tr><td>{html.escape(f.get('check', '?'))}</td>"
                    f"<td>{html.escape(str(f.get('severity', '')))}</td>"
                    f"<td>{f.get('count', '')}</td><td>{ex}</td>"
                    f"<td>{advice}{sent}</td></tr>")
    return (f"<h2>学术写作规范自查（{len(finds)} 条 findings，不评分）</h2>"
            f"<table><tr><th>检查</th><th>级别</th><th>计数</th><th>示例</th><th>建议</th></tr>"
            f"{''.join(body)}</table>")


_WF_LABELS = {
    "composite": "门禁复合分", "composite_ai_risk": "门禁复合分", "verdict": "门禁判定",
    "standardization_rate": "术语标准率", "smell_count": "翻译腔命中", "style_score": "文体分",
    "aigc_label": "合规标识", "evidence": "显式标识证据", "note": "说明", "error": "错误",
    "ai_score": "AI 分", "ai_risk": "风险带", "structure_score": "结构完整性",
    "readability_score": "可读性", "overall_quality": "综合评分",
}


def _kv_table(title, pairs):
    rows = "".join(f"<tr><td>{html.escape(_WF_LABELS.get(k, k))}</td>"
                   f"<td>{_esc_cell(v, 200)}</td></tr>" for k, v in pairs)
    return f"<h2>{html.escape(title)}</h2><table>{rows}</table>" if rows else ""


def _wf_blocks(wf):
    """workflow 附加块：混写评估 / 门禁 / 术语/腔/文体 / AIGC / 台账。"""
    out = []
    md = wf.get("mixed_document") or {}
    if md.get("detected"):
        out.append(_kv_table("人机混写评估（判定仅排序辅助，需逐段人工复核）", [
            ("hi", "%s 段" % md.get("hi", "?")), ("medium", "%s 段" % md.get("medium", "?")),
            ("low", "%s 段" % md.get("low", "?")),
            ("note", md.get("guidance") or md.get("measured", {}).get("document_level_auroc", ""))]))
    gate = wf.get("gate") or {}
    if isinstance(gate, dict) and gate:
        pairs = [(k, v) for k, v in gate.items()
                 if isinstance(v, (str, int, float)) and k != "integrity_notice"]
        out.append(_kv_table("四层门禁", pairs[:8]))
    tr = []
    terms = wf.get("terms") or {}
    for k in ("standardization_rate", "total", "fixed"):
        if isinstance(terms.get(k), (str, int, float)):
            tr.append((k, terms[k]))
    out.append(_kv_table("术语标准化", tr))
    smell = wf.get("smell") or {}
    if isinstance(smell, dict):
        sc = smell.get("count", smell.get("hits", ""))
        if sc != "":
            out.append(_kv_table("翻译腔筛查", [("smell_count", sc)]))
    sty = wf.get("style") or {}
    if isinstance(sty, dict) and isinstance(sty.get("style_score"), (str, int, float)):
        out.append(_kv_table("文体特征", [("style_score", sty["style_score"])]))
    q = wf.get("quality") or {}
    if isinstance(q, dict) and q.get("overall_quality") is not None:
        out.append(_kv_table("综合质量（quality_report 口径）", [
            ("ai_score", q.get("ai_score", "?")), ("ai_risk", q.get("ai_risk", "?")),
            ("structure_score", q.get("structure_score", "?")),
            ("readability_score", q.get("readability_score", "?")),
            ("overall_quality", q.get("overall_quality", "?")),
            ("total_paragraphs", q.get("total_paragraphs", "?")),
            ("note", "结构/可读性等维度，非 AI 率判定；完整口径见 quality_report.py")]))
    aigc = wf.get("aigc_label") or {}
    if aigc:
        out.append(_kv_table("AIGC 合规标识（显式声明自查）", [
            ("evidence", "%d 条" % len(aigc.get("evidence") or [])),
            ("note", aigc.get("note", ""))]))
    # 信号细节（v6.2.0）：语域提示/混写预警/篇章特征/LLM 腔命中——全部只在报告有值时呈现
    sig = []
    if wf.get("detect", {}).get("register_hint"):
        sig.append(("语域提示", wf["detect"]["register_hint"]))
    if wf.get("detect", {}).get("mixed_notice"):
        sig.append(("混写预警", wf["detect"]["mixed_notice"]))
    dh = (wf.get("detect") or {}).get("discourse_hits") or []
    if dh:
        sig.append(("篇章结构特征", "%d 处（%s）" % (len(dh), "、".join(
            str(x.get("kind", x) if isinstance(x, dict) else x) for x in dh[:3]))))
    jh = (wf.get("detect") or {}).get("jargon_hits") or []
    if jh:
        sig.append(("LLM 腔命中（只提示不计分）", "%d 处" % len(jh)))
    if sig:
        out.append(_kv_table("信号细节", sig))
    fl = wf.get("findings_ledger") or {}
    if fl.get("items"):
        lis = "".join("<li><b>%s</b>：%s（%s）</li>" % (
            html.escape(i.get("check", "?")), html.escape(i.get("status", "?")),
            _esc_cell(i.get("detail", ""), 80)) for i in fl["items"])
        out.append(f"<h2>Findings Ledger（结论状态一览）</h2><ul class='ledger'>{lis}</ul>"
                   f"<p class='muted'>{_esc_cell(fl.get('note', ''), 200)}</p>")
    return "\n".join(x for x in out if x)


# ---------- 主渲染 ----------

def render(sections, sources, title):
    detect = sections.get("detect") or {}
    score = detect.get("overall_ai_score", "?")
    risk = detect.get("overall_risk", "unknown")
    parts = [f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>{html.escape(title)}</title><style>{_CSS}</style></head><body>
<h1>{html.escape(title)}</h1>"""]

    degraded = detect.get("degraded_mode")
    mode_note = ""
    if degraded is True:
        mode_note = "<div class='card'><b style='color:#e67e22'>降级档</b>纯规则+词频谱</div>"
    elif degraded is False:
        mode_note = "<div class='card'><b style='color:#27ae60'>融合档</b>监督层在位</div>"
    parts.append("<div class='cards'>"
                 f"<div class='card' style='min-width:150px'>{_gauge(score)}</div>"
                 f"<div class='card'><b>{_risk_badge(risk)}</b>风险带</div>"
                 f"<div class='card'><b>{html.escape(str(detect.get('total_paragraphs', '?')))}</b>段落总数</div>"
                 + mode_note + "</div>")
    notice = detect.get("degraded_notice") or detect.get("integrity_notice")
    if notice:
        parts.append(f"<p class='muted'>{_esc_cell(notice, 300)}</p>")

    paras = sections["workflow"].get("paragraphs") if sections.get("workflow") else None
    scores = []
    if isinstance(paras, dict) and paras.get("items"):
        scores = [r.get("score") for r in paras["items"]]
    elif detect.get("paragraph_scores"):
        scores = [r.get("ai_score") for r in detect["paragraph_scores"]]
    parts.append("<h2>段落分数分布</h2>" + _histogram(scores))
    parts.append(_para_table(detect, paras))
    parts.append(_fix_table(sections.get("fix")))
    parts.append(_norm_table(sections.get("norm")))
    if sections.get("workflow"):
        parts.append(_wf_blocks(sections["workflow"]))

    gen_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parts.append(f'<p class="note">{_INTEGRITY}<br>数据源：{html.escape("；".join(sources) or "—")} ｜ '
                 f'生成时间 {gen_at} ｜ 单文件渲染，零外部资源、零网络</p>')
    parts.append("</body></html>")
    return "\n".join(p for p in parts if p)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("inputs", nargs="+", help="JSON 输入（workflow/detect/fix/norm，可多个混给）")
    ap.add_argument("-o", "--output", default=None, help="输出 HTML 路径（默认 <首个输入名>.report.html）")
    ap.add_argument("--title", default=None, help="报告标题（默认「自查仪表盘 · <首个输入名>」）")
    a = ap.parse_args()

    sections, sources, skipped = load_sections(a.inputs)
    for p, why in skipped:
        print("WARN: 跳过 %s（%s）" % (p, why), file=sys.stderr)
    if not sources:
        print("ERROR: 没有可识别的输入（支持 workflow/detect/fix_suggest/style_norm 的 JSON 输出）",
              file=sys.stderr)
        return 2
    first = Path(a.inputs[0]).stem
    title = a.title or ("自查仪表盘 · %s" % first)
    out = Path(a.output) if a.output else Path(first + ".report.html")
    out.write_text(render(sections, sources, title), encoding="utf-8")
    print("HTML 报告已生成: %s（数据源 %d 个；单文件、零外部资源）" % (out, len(sources)))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
