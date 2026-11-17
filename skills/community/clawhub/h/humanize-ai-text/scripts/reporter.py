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
"""

_FOOT = ("<div class='foot'>本地启发式风格诊断 · 非任何官方检测分数 · "
         "报告不代写原文 · 生成于 {ts}</div>")


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


def sentence_diff(orig, new):
    """句级对齐：返回 [(tag, orig_sent, new_sent)]，tag∈equal/replace/delete/insert。"""
    def split(text):
        return [x for x in re.split(r"(?<=[。！？!?;.])\s*|\n+", text) if x and x.strip()]
    a, b = split(orig), split(new)
    rows = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        o = "".join(a[i1:i2])
        n = "".join(b[j1:j2])
        rows.append((tag, o, n))
    return rows


def render_compare(orig, new, ro, rn, verify_result):
    """compare 报告：逐句 diff 对照（删红增绿）+ 双评分卡 + 完整性。"""
    body = "<div class='card'><h1>改写前后对照</h1></div>"
    body += ("<div style='display:flex;gap:16px'>"
             + _score_card("原稿", ro["score"], ro["level"])
             + _score_card("改稿", rn["score"], rn["level"]) + "</div>")
    body += _integrity_card(verify_result)
    rows = sentence_diff(orig, new)
    trs = []
    for tag, o, n in rows:
        if tag == "equal":
            trs.append("<tr><td class='meta'>同</td><td>%s</td></tr>" % esc(o))
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
             "</table></div>" % (len(rows), sum(1 for t, _, _ in rows if t != "equal"), "".join(trs)))
    body += _FOOT.format(ts=_now())
    return _page("改写前后对照", body)
