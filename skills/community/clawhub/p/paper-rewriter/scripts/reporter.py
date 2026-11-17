# -*- coding: utf-8 -*-
"""reporter.py — v1.5.0 实质功能：HTML 可视化报告与逐句 diff。

单文件零依赖：内联 CSS、无外链、无 JS 依赖；HTML 实体全转义。
设计立场与工具本体一致：报告呈现诊断与建议，不代写、不含任何对
外部评审结果的承诺。
"""

import html
import re
import difflib


def esc(s):
    return html.escape(str(s), quote=True)


_LEVEL_COLOR = {"低": "#1a7f37", "中": "#9a6700", "高": "#cf222e", "极高": "#82071e"}
_VERDICT_COLOR = {"PASS": "#1a7f37", "FAIL": "#cf222e"}

_CSS = """
body{font-family:-apple-system,'Segoe UI','Noto Sans SC',sans-serif;margin:0;
background:#f6f8fa;color:#1f2328}
.wrap{max-width:960px;margin:0 auto;padding:24px}
.card{background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:20px;
margin-bottom:16px}
h1{font-size:20px;margin:0 0 4px}h2{font-size:15px;margin:0 0 12px;color:#57606a}
.score{font-size:44px;font-weight:700;line-height:1}
.badge{display:inline-block;padding:2px 10px;border-radius:12px;color:#fff;
font-size:13px;margin-left:8px;vertical-align:middle}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid #eaeef2}
th{color:#57606a;font-weight:600}
.meta{color:#57606a;font-size:12px;margin-top:8px}
.foot{color:#8c959f;font-size:11px;margin-top:16px;text-align:center}
.del{background:#ffebe9;text-decoration:line-through;color:#cf222e}
.ins{background:#dafbe1;color:#1a7f37}
.pill{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;
margin:2px 4px 2px 0;background:#eaeef2}
.warn{color:#9a6700}
.ok{color:#1a7f37;font-weight:600}
.bad{color:#cf222e;font-weight:600}

@media print {
  .wrap { max-width: none; margin: 0; padding: 0; }
  .card { break-inside: avoid; box-shadow: none; border: 1px solid #ccc; }
  h1, h2 { page-break-after: avoid; }
  .foot { font-size: 9px; }
}
"""

_FOOT = ("<div class='foot'>本地启发式风格诊断 · 非任何官方检测分数 · "
         "报告不代写原文</div>"
         "<footer style=\"margin-top:24px;padding-top:12px;border-top:1px solid #eee;"
         "color:#9aa0a6;font-size:12px;text-align:center;\">"
         "本文档由 paper-rewriter 生成 · "
         "<a href=\"https://github.com/docsor1212/paper-rewriter\" "
         "style=\"color:#9aa0a6;\">GitHub</a> · "
         "<a href=\"https://skillhub.cn/skills/indiv-sorsor/paper-rewriter\" "
         "style=\"color:#9aa0a6;\">SkillHub</a> · 觉得有用欢迎 Star / 收藏</footer>\n")


def _score_card(title, score, level, extra=""):
    color = _LEVEL_COLOR.get(level, "#57606a")
    return ("<div class='card'><h2>%s</h2>"
            "<span class='score' style='color:%s'>%d</span>"
            "<span class='badge' style='background:%s'>%s</span>%s</div>"
            % (esc(title), color, score, color, esc(level), extra))


def _category_table(categories):
    if not categories:
        return "<div class='card'><h2>分类明细</h2><p>未发现明显特征。</p></div>"
    rows = []
    for cid, c in sorted(categories.items(),
                         key=lambda kv: -kv[1]["count"] * kv[1]["weight"]):
        samples = "".join("<div class='pill'>%s</div>" % esc(s) for s in c["samples"][:5])
        rows.append("<tr><td>%s</td><td>%d</td><td>%s</td></tr>"
                    % (esc(c["label"]), c["count"], samples))
    return ("<div class='card'><h2>分类明细</h2><table>"
            "<tr><th>类别</th><th>命中</th><th>样本</th></tr>%s</table></div>" % "".join(rows))


def _integrity_card(verify_result):
    v = verify_result
    verdict = "PASS" if v.get("ok") else "FAIL"
    color = _VERDICT_COLOR[verdict]
    rows = []
    for x in v.get("violations", []):
        rows.append("<tr><td><span class='bad'>✗ 红线</span></td><td>%s</td><td>%s</td></tr>"
                    % (esc(x["check"]), esc(x["detail"])))
    for x in v.get("warnings", []):
        rows.append("<tr><td><span class='warn'>⚠ 告警</span></td><td>%s</td><td>%s</td></tr>"
                    % (esc(x["check"]), esc(x["detail"])))
    if not rows:
        rows.append("<tr><td class='ok'>全部保全</td><td colspan='2'>数字/引用/术语/长度均在容差内。</td></tr>")
    st = v.get("stats", {})
    meta = "长度 %d → %d（%+.1f%%）" % (st.get("orig_chars", 0), st.get("new_chars", 0),
                                       st.get("length_delta_pct", 0.0))
    return ("<div class='card'><h2>完整性守卫 <span class='badge' style='background:%s'>%s</span></h2>"
            "<p class='meta'>%s</p><table><tr><th>级别</th><th>类别</th><th>明细</th></tr>%s</table></div>"
            % (color, verdict, esc(meta), "".join(rows)))


def _page(title, body):
    return ("<!DOCTYPE html><html lang='zh'><head><meta charset='utf-8'>"
            "<title>%s</title><style>%s</style></head><body><div class='wrap'>%s</div></body></html>"
            % (esc(title), _CSS, body))


import datetime


def _now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


# ────────────────────────── 三种报告 ──────────────────────────

def render_detect(text, r, source=""):
    """detect 报告：评分卡+分类+节奏+建议。"""
    stats = r.get("stats") or {}
    extra = ""
    for k, lab in (("burstiness_cv", "句长变异系数"), ("connector_density", "连接词/句"),
                   ("em_dash_density", "破折号/千词")):
        if stats.get(k) is not None:
            extra += "<span class='pill'>%s %s</span>" % (esc(lab), esc(stats[k]))
    body = ("<div class='card'><h1>风格自查报告</h1><p class='meta'>%s%s</p></div>"
            % (esc(source), (" · " + esc(r["lang"]) + " · " + esc(r.get("profile", ""))
                             + " 模式") if source else ""))
    body += _score_card("风格特征分", r["score"], r["level"], extra)
    if r.get("critical_hit"):
        body += ("<div class='card'><span class='bad'>⚠ 含模型残留/客套句等硬特征</span>——"
                 "先跑 transform.py 清理。</div>")
    body += _category_table(r.get("categories"))
    if r.get("suggestions"):
        sug = "".join("<li>「%s」→ %s</li>" % (esc(x["from"]), esc(x["to"]))
                      for x in r["suggestions"][:10])
        body += "<div class='card'><h2>改写建议（前 10）</h2><ul>%s</ul></div>" % sug
    for note in (stats.get("notes") or []):
        body += "<div class='card'><span class='warn'>⚠ %s</span></div>" % esc(note)
    body += "<div class='card'>深改方法论见 style_guide；改后务必跑 verify.py 守卫完整性。</div>"
    body += _FOOT.format(ts=_now())
    return _page("风格自查报告", body)


def render_sections(rs, source=""):
    """章节感知报告：综合+分章节表+缺失章节提示。"""
    color = _LEVEL_COLOR.get(rs.get("overall_level", ""), "#57606a")
    body = ("<div class='card'><h1>章节感知扫描（论文结构模式）</h1>"
            "<p class='meta'>%s</p></div>" % esc(source))
    body += ("<div class='card'><h2>综合</h2>"
             "<span class='score' style='color:%s'>%d</span>"
             "<span class='badge' style='background:%s'>%s</span></div>"
             % (color, rs["overall_score"], color, esc(rs["overall_level"])))
    rows = []
    for x in rs.get("sections", []):
        sc = ("%d [%s]" % (x["score"], x["level"])) if x.get("score") is not None else "不扫描"
        rows.append("<tr><td>%s</td><td>%s</td><td>%d</td></tr>"
                    % (esc(x["label"]), esc(sc), x.get("chars", 0)))
    body += ("<div class='card'><h2>分章节</h2><table>"
             "<tr><th>章节</th><th>特征分</th><th>字符</th></tr>%s</table></div>"
             % "".join(rows))
    if rs.get("missing_sections"):
        body += ("<div class='card'><span class='warn'>⚠ 未识别到章节: %s"
                 "（非 IMRaD 结构可忽略）</span></div>" % esc("/".join(rs["missing_sections"])))
    body += ("<div class='card'>方法/结果段已自动降权（文体常态）；"
             "本地启发式，非官方分数。</div>")
    body += _FOOT.format(ts=_now())
    return _page("章节感知扫描", body)


def render_pipeline(orig, new, ro, rn, verify_result, brief, chunked=None):
    """pipeline 报告：前后对比+完整性+工作单。"""
    body = ("<div class='card'><h1>一键管线报告</h1>"
            "<p class='meta'>机械清理层产物；深度改写由 agent 按指南执行</p></div>")
    body += ("<div style='display:flex;gap:16px'>"
             + _score_card("改写前", ro["score"], ro["level"])
             + _score_card("改写后", rn["score"], rn["level"]) + "</div>")
    body += _integrity_card(verify_result)
    if brief.get("remaining_patterns"):
        pats = "".join("<span class='pill'>%s</span>" % esc(p) for p in brief["remaining_patterns"])
        body += "<div class='card'><h2>剩余特征</h2>%s</div>" % pats
    body += "<div class='card'><h2>下一步</h2><p>%s</p><p class='meta'>指南: %s</p></div>" % (
        esc(brief.get("next_action", "")), esc(brief.get("guide", "")))
    if chunked:
        body += "<div class='card'><span class='warn'>⚠ 超大文本分块模式（%d 块）——跨块结构信号可能少量漏检</span></div>" % chunked
    body += _FOOT.format(ts=_now())
    return _page("一键管线报告", body)


def render_style_profile(profile, source=""):
    """风格画像 HTML（v2.7.0）：总览档位表+重点段落+指南锚点。"""
    names = {"jargon_1k": "黑话密度（每千字）", "sent_cv": "句长变异系数",
             "opener_top": "最高频句首占比", "opener_streak": "最长连续同开场"}
    band_color = {"自然": "#1a7f37", "观察": "#9a6700", "偏机器": "#cf222e"}
    body = ("<div class='card'><h1>风格画像</h1><p class='meta'>%s · %d 段 / %d 句"
            "</p></div>" % (esc(source), profile["n_paras"], profile["n_sents"]))
    rows = ""
    for k in ("jargon_1k", "sent_cv", "opener_top", "opener_streak"):
        g = profile["global"][k]
        c = band_color.get(g["band"], "#57606a")
        rows += ("<tr><td>%s</td><td>%s</td><td><span class='badge' "
                 "style='background:%s'>%s</span></td></tr>"
                 % (esc(names[k]), g["value"], c, esc(g["band"])))
    body += ("<div class='card'><h2>指标档位</h2><table><tr><th>指标</th>"
             "<th>值</th><th>档位</th></tr>%s</table>"
             "<p class='meta'>档位出自本地语料校准，只做验收提示，不改变评分。</p></div>" % rows)
    if profile["worst_paras"]:
        items = "".join("<li>第 %d 段（%d 字/%d 句，命中 %d）：%s</li>" % (
            p["idx"], p["chars"], p["sents"], p["jargon_hits"],
            esc(p["worst_sample"]))
            for p in profile["paras"] if p["idx"] in profile["worst_paras"])
        body += ("<div class='card'><h2>重点段落（黑话命中降序）</h2><ul>%s</ul></div>" % items)
    tips = "".join("<li>%s</li>" % esc(a) for a in profile["advice"])
    body += "<div class='card'><h2>指南锚点</h2><ul>%s</ul></div>" % tips
    body += _FOOT.format(ts=_now())
    return _page("风格画像", body)


def render_style_compare(pa, pb, sa, sb):
    """风格画像对比 HTML（v2.7.0）：改前改后档位变化+黑话合计。"""
    names = {"jargon_1k": "黑话密度（每千字）", "sent_cv": "句长变异系数",
             "opener_top": "最高频句首占比", "opener_streak": "最长连续同开场"}
    order = {"自然": 0, "观察": 1, "偏机器": 2}
    rows = ""
    for k in ("jargon_1k", "sent_cv", "opener_top", "opener_streak"):
        a, b = pa["global"][k], pb["global"][k]
        if a["band"] != b["band"]:
            delta = "%s → %s" % (a["band"], b["band"])
        elif order.get(a["band"], 0) == 0:
            delta = "维持自然"
        else:
            delta = "持平"
        rows += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            esc(names[k]), a["value"], b["value"], esc(delta))
    hit_a = sum(p["jargon_hits"] for p in pa["paras"])
    hit_b = sum(p["jargon_hits"] for p in pb["paras"])
    body = ("<div class='card'><h1>风格画像对比</h1><p class='meta'>%s → %s</p></div>"
            % (esc(sa), esc(sb)))
    body += ("<div class='card'><table><tr><th>指标</th><th>改前</th><th>改后</th>"
             "<th>档位</th></tr>%s</table></div>" % rows)
    body += ("<div class='card'><p>黑话命中合计：%d → %d（%s%d）</p>"
             "<p class='meta'>档位只做验收提示；改稿完整性以 verify.py 为准。</p></div>"
             % (hit_a, hit_b, "+" if hit_b >= hit_a else "", hit_b - hit_a))
    sa_, sb_ = pa.get("stats") or {}, pb.get("stats") or {}
    if sa_ and sb_:
        srows = ""
        for k, label in (("ttr_zh", "TTR（中）"), ("ttr_en", "TTR（英）"),
                         ("func_ratio_zh", "虚词比例（中）"),
                         ("func_ratio_en", "虚词比例（英）")):
            va, vb = sa_.get(k), sb_.get(k)
            if va is not None or vb is not None:
                srows += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    esc(label), va, vb)
        qa, qb = sa_.get("sent_len_quantiles") or {}, sb_.get("sent_len_quantiles") or {}
        if qa and qb:
            srows += ("<tr><td>句长分位 P25/50/75/90</td><td>%s/%s/%s/%s</td>"
                      "<td>%s/%s/%s/%s</td></tr>"
                      % (qa.get("p25"), qa.get("p50"), qa.get("p75"), qa.get("p90"),
                         qb.get("p25"), qb.get("p50"), qb.get("p75"), qb.get("p90")))
        body += ("<div class='card'><h2>统计面板（信息性）</h2>"
                 "<table><tr><th>统计量</th><th>改前</th><th>改后</th></tr>%s"
                 "</table></div>" % srows)
    body += _FOOT.format(ts=_now())
    return _page("风格画像对比", body)


def sentence_diff(orig, new):
    """句级对齐（v5.5.0 行号版）：返回 [(tag, orig_sent, new_sent, orig_line, new_line)]，
    tag∈equal/replace/delete/insert；行号=该句在各自文本中的 1-based 行号
    （删/增句对应侧行号为 None）。供 render_compare 的 L 锚列使用。"""
    def split_with_lines(text):
        out = []
        line = 1
        buf = ""
        for ch in text:
            if ch == "\n":
                if buf.strip():
                    out.append((buf.strip(), line))
                buf = ""
                line += 1
                continue
            buf += ch
            if re.match(r"[。！？!?;.]", ch):
                if buf.strip():
                    out.append((buf.strip(), line))
                buf = ""
        if buf.strip():
            out.append((buf.strip(), line))
        return out
    a, b = split_with_lines(orig), split_with_lines(new)
    sm = difflib.SequenceMatcher(None, [x[0] for x in a], [x[0] for x in b], autojunk=False)
    rows = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        o = "".join(x[0] for x in a[i1:i2])
        n = "".join(x[0] for x in b[j1:j2])
        o_ln = a[i1][1] if i1 < i2 else None
        n_ln = b[j1][1] if j1 < j2 else None
        rows.append((tag, o, n, o_ln, n_ln))
    return rows


def render_compare(orig, new, ro, rn, verify_result):
    """compare 报告：逐句 diff 对照（删红增绿）+ 双评分卡 + 完整性。"""
    body = "<div class='card'><h1>改写前后对照</h1></div>"
    body += ("<div style='display:flex;gap:16px'>"
             + _score_card("原稿", ro["score"], ro["level"])
             + _score_card("改稿", rn["score"], rn["level"]) + "</div>")
    body += _integrity_card(verify_result)
    # 命中依据节（v5.5.0 口径统一：改稿命中带 L 行号与依据折叠）
    cats = rn.get("categories") or {}
    if cats:
        det = []
        for cid, c in sorted(cats.items(), key=lambda kv: -(kv[1].get("weight", 1) * kv[1].get("count", 0))):
            rat = ("<details><summary>依据</summary><p class='meta'>%s</p></details>"
                   % esc(c["rationale"])) if c.get("rationale") else ""
            smps = "".join("<li>%s</li>" % esc(s) for s in c.get("samples", [])[:6])
            det.append("<details><summary>%s ×%d</summary>%s<ul>%s</ul></details>"
                       % (esc(c.get("label", cid)), c.get("count", 0), rat, smps))
        body += ("<div class='card'><h2>改稿命中明细（L=改稿行号）</h2>%s</div>"
                 % "".join(det))
    rows = sentence_diff(orig, new)
    trs = []
    for tag, o, n, o_ln, n_ln in rows:
        loc = ("<span class='meta'>L%s→L%s</span>" % (o_ln or "–", n_ln or "–"))
        if tag == "equal":
            trs.append("<tr><td class='meta'>同 %s</td><td>%s</td></tr>" % (loc, esc(o)))
        else:
            cell = ""
            if o:
                cell += "<span class='del'>%s</span> " % esc(o)
            if n:
                cell += "<span class='ins'>%s</span>" % esc(n)
            act = {"replace": "改", "delete": "删", "insert": "增"}.get(tag, tag)
            trs.append("<tr><td>%s</td><td>%s</td></tr>" % (act, cell))
    body += ("<div class='card'><h2>逐句对照（%d 句，其中变更 %d）</h2><table>"
             "<tr><th>操作</th><th>内容（<span class='del'>删除</span>/<span class='ins'>新增</span>）</th></tr>%s"
             "</table></div>" % (len(rows), sum(1 for r in rows if r[0] != "equal"), "".join(trs)))
    body += _FOOT.format(ts=_now())
    return _page("改写前后对照", body)


# ---------------------------------------------------------------------------
# v1.8.0 审稿报告（markdown 交付文档）
# ---------------------------------------------------------------------------

def build_review_md(text, scan_result, verify_result=None, source=""):
    """审稿报告（markdown 交付文档）：模仿人类编辑审稿格式。

    总评 → 分层修改建议（确定性/建议性/风格优化）→ 逐句引用 →
    修订流程 → 合规提示。报告可直接交付给作者或导师。
    """
    import datetime as _dt
    r = scan_result
    score, level = r["score"], r["level"]
    cats = r.get("categories", {})
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = ["# 审稿报告：%s" % (source or "未命名文稿"), ""]
    lines.append("> 本报告由 paper-rewriter 自动生成（%s）。" % now)
    lines.append("> 本地启发式风格诊断，非任何官方 AI 检测分数；不代写原文。")
    lines.append("")

    # 总评（定性段落）
    lines.append("## 总评")
    lines.append("")
    if level == "极高":
        lines.append("文本存在大量模板化行文和/或模型残留痕迹（风格特征分 %d/100，"
                     "严重度：极高）。建议优先清理硬残留，再逐段深改。" % score)
    elif level == "高":
        lines.append("文本风格特征密度较高（%d/100，严重度：高），主要问题集中在"
                     "模板化句式和 AI 高频词。建议按修订建议逐段深改。" % score)
    elif level == "中":
        lines.append("文本风格特征密度中等（%d/100），有改进空间但非紧急。" % score)
    else:
        lines.append("文本未检出明显模板化行文（%d/100）。" % score)
    lines.append("")

    # 分层修改建议
    lines.append("## 修改建议（按优先级）")
    lines.append("")
    tier1, tier2, tier3 = [], [], []
    for cid, c in sorted(cats.items(), key=lambda kv: -kv[1]["count"] * kv[1]["weight"]):
        label, count = c["label"], c["count"]
        for smp in c.get("samples", [])[:3]:
            if c.get("auto_fixable"):
                tier1.append({"label": label, "sample": smp, "count": count,
                              "action": "transform.py 可自动修复"})
            else:
                tier2.append({"label": label, "sample": smp, "count": count,
                              "action": "按 style_guide 深改"})
    if tier1:
        lines.append("### 优先级 1：确定性修复（transform.py 自动处理）")
        lines.append("")
        for e in tier1:
            lines.append("- [%s] %s（×%d）" % (e["label"], e["sample"], e["count"]))
        lines.append("")
    if tier2:
        lines.append("### 优先级 2：建议性深改")
        lines.append("")
        for e in tier2:
            lines.append("- [%s] %s（×%d）→ 按 style_guide 对应条目处理" % (e["label"], e["sample"], e["count"]))
        lines.append("")

    # 完整性
    if verify_result:
        v = verify_result
        verdict = "PASS" if v.get("ok") else "FAIL"
        lines.append("## 完整性守卫：%s" % verdict)
        lines.append("")
        for x in v.get("violations", []):
            lines.append("- ✗ [%s] %s" % (x.get("code", x["check"]), x["detail"]))
        for x in v.get("warnings", []):
            lines.append("- ⚠ [%s] %s" % (x.get("code", x["check"]), x["detail"]))
        if not v.get("violations") and not v.get("warnings"):
            lines.append("数字/引用/术语完整性：全部保全。")
        lines.append("")

    # 合规
    lines.append("## 合规提醒")
    lines.append("")
    lines.append("- 本报告为本地启发式风格诊断，非任何官方 AI 检测分数。")
    lines.append("- 如目标期刊/学校要求披露 AI 使用，披露义务在作者本人。")
    lines.append("- 深度改写请配合 style_guide 执行，改后务必 verify.py 守卫完整性。")
    lines.append("")
    lines.append("---")
    lines.append("*审稿报告由 paper-rewriter 自动生成 · 仅供写作质量参考 · 不构成任何检测结论*")
    lines.append("")
    lines.append("> 本文档由 paper-rewriter 生成"
                 "（[GitHub](https://github.com/docsor1212/paper-rewriter) · "
                 "[SkillHub](https://skillhub.cn/skills/indiv-sorsor/paper-rewriter)）"
                 "· 觉得有用欢迎 Star / 收藏")
    return "\n".join(lines)


def render_dashboard(ro, rn, vr, prof, st_issues, t_issues, led, meta=""):
    """v5.0.0 旗舰：投稿自查包 2.0 单页交互体检报告。

    聚合各件数据：分数卡（前→后）/完整性判定/命中行号定位表（含依据折叠，
    details 原生折叠零 JS）/术语+统计一致性面板/问题台账/处置清单。"""
    now = _now()
    delta = rn.get("score", 0) - ro.get("score", 0)
    head_cards = (
        "<div class='cards'>"
        + _score_card("改前风格分", ro.get("score", 0), ro.get("level", ""), "")
        + _score_card("改后风格分", rn.get("score", 0), rn.get("level", ""),
                      "Δ%+d" % delta if delta else "持平")
        + _integrity_card(vr)
        + "</div>")
    # 命中定位表（改后口径；samples 带 L 行号与依据折叠）
    rows = []
    cats = rn.get("categories") or {}
    for cid, c in sorted(cats.items(), key=lambda kv: -(kv[1].get("weight", 1) * kv[1].get("count", 0))):
        rat = ("<details><summary>依据</summary><p class='meta'>%s</p></details>"
               % esc(c["rationale"])) if c.get("rationale") else ""
        smps = "".join("<li>%s</li>" % esc(s) for s in c.get("samples", [])[:6])
        rows.append("<details><summary>%s ×%d%s</summary>%s<ul>%s</ul></details>"
                    % (esc(c.get("label", cid)), c.get("count", 0),
                       " [可自动修]" if cid in __import__("hxt_core").AUTO_FIXABLE else "",
                       rat, smps))
    hit_html = ("<div class='card'><h2>命中明细（改稿口径，L=原文行号）</h2>"
                + ("".join(rows) if rows else "<p>未命中任何特征。</p>") + "</div>")
    # 术语/统计面板
    t_rows = "".join("<tr><td>%s</td><td>%s</td><td>「%s」</td></tr>" % (
        esc(x.get("pack", "")),
        " / ".join("%s(%d)" % (v, n) for v, n in sorted(
            x.get("variants", {}).items(), key=lambda kv: -kv[1])),
        esc(x.get("suggestion", ""))) for x in (t_issues or []))
    st_rows = "".join("<li>%s</li>" % esc(str(x)[:120]) for x in (st_issues or [])) or "<li>无</li>"
    panel = ("<div class='card'><h2>术语一致性（%d 组）</h2><table>"
             "<tr><th>域</th><th>变体（次数）</th><th>建议</th></tr>%s</table></div>"
             % (len(t_issues or []), t_rows or "<tr><td colspan='3'>一致</td></tr>"))
    panel += ("<div class='card'><h2>统计一致性（%d 项）</h2><ul>%s</ul></div>"
              % (len(st_issues or []), st_rows))
    # 台账
    led_rows = "".join("<tr><td>%s</td><td>%s</td><td>%d</td><td>%d</td><td>%s</td></tr>" % (
        esc(cid), esc(label), b, a, esc(st)) for cid, label, b, a, st in (led or []))
    led_html = ("<div class='card'><h2>问题台账</h2><table><tr><th>问题</th><th>说明</th>"
                "<th>改前</th><th>改后</th><th>状态</th></tr>%s</table></div>" % led_rows)
    # 行动清单（v5.2.0）：报告→行动闭环——按命中性质分三段给可执行命令
    act_auto, act_deep, act_guard = [], [], []
    for cid, c in sorted(cats.items(), key=lambda kv: -kv[1].get("count", 0)):
        label = c.get("label", cid)
        cnt = c.get("count", 0)
        if cid in __import__("hxt_core").AUTO_FIXABLE:
            act_auto.append("<li>%s ×%d → <code>python scripts/transform.py 原稿 -o 改稿.txt</code>（机械层自动处理）</li>"
                            % (esc(label), cnt))
        elif cid.startswith(("chatbot", "cutoff", "model_artifact")):
            act_auto.append("<li>%s ×%d → 同上，transform 一步清除（硬残留零保留）</li>"
                            % (esc(label), cnt))
        else:
            act_deep.append("<li>%s ×%d → 按 style_guide 深改（<code>plan.py 原稿 --handoff</code> 出逐句指令单）</li>"
                            % (esc(label), cnt))
    if vr and not vr.get("ok"):
        act_guard.append("<li>完整性守卫 FAIL → 按 06_完整性判定.json 的 remedies 逐条修复改稿（不修守卫）</li>")
    act_guard.append("<li>交付前：<code>python scripts/verify.py 原稿 改稿</code>（exit 0 才算过）</li>")
    act_html = ("<div class='card'><h2>下一步行动（按序执行）</h2>"
                + ("<h3>①机械清理（自动）</h3><ul>%s</ul>" % "".join(act_auto) if act_auto else "")
                + ("<h3>②质量深改（agent/人工）</h3><ul>%s</ul>" % "".join(act_deep) if act_deep else "")
                + ("<h3>③守卫复核</h3><ul>%s</ul>" % "".join(act_guard))
                + "</div>")
    body = ("<div class='card'><h1>稿件体检报告（投稿自查包 2.0）</h1>"
            "<p class='meta'>%s · 本地启发式，非任何官方检测分数</p></div>" % esc(meta or now))
    body += head_cards + act_html + hit_html + panel + led_html
    return _page("稿件体检报告", body) + _FOOT.format(ts=now)
