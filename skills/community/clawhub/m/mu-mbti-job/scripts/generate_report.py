#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the bilingual MBTI personality & career PDF report.

Usage:
    python3 generate_report.py <result.json> [-o report.pdf]
    python3 generate_report.py <team_results.json> --team [-o team_report.pdf]
    (--team: input is a JSON array of result dicts; a team report PDF is
    produced via the weasyprint / Chromium headless HTML path)

Three-tier PDF engine fallback (each probed in order; the tier actually used
is printed to stdout; only failure of ALL tiers is fatal):
  1. weasyprint      - HTML template rendered to PDF (best typography)
  2. Chromium headless - Chrome / Chromium / Edge --headless --print-to-pdf
  3. reportlab       - pure-Python fallback layout
"""

import argparse
import html as html_mod
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")

EXIT_INPUT_ERROR = 2
EXIT_ENGINE_ERROR = 4

DIMENSIONS = ["E/I", "S/N", "T/F", "J/P"]
DIMENSION_POLES = {
    "E/I": ("E", "I"),
    "S/N": ("S", "N"),
    "T/F": ("T", "F"),
    "J/P": ("J", "P"),
}
POLE_LABELS = {
    "E": ("外向", "Extraversion"),
    "I": ("内向", "Introversion"),
    "S": ("实感", "Sensing"),
    "N": ("直觉", "Intuition"),
    "T": ("思考", "Thinking"),
    "F": ("情感", "Feeling"),
    "J": ("判断", "Judging"),
    "P": ("知觉", "Perceiving"),
}
DIMENSION_TITLES = {
    "E/I": ("能量方向", "Energy Orientation"),
    "S/N": ("信息获取", "Information Gathering"),
    "T/F": ("决策方式", "Decision Making"),
    "J/P": ("生活方式", "Lifestyle Orientation"),
}
CLARITY_BANDS = [
    (25, "轻微", "Slight"),
    (50, "中等", "Moderate"),
    (75, "清晰", "Clear"),
    (float("inf"), "非常清晰", "Very Clear"),
]
# Display names/counts are mapped from the result.json "version" field.
# Footer badges (brand colors follow the official landing-page template)
FOOTER_BADGES = [
    # (label, background, text color, url)
    ("微信 木先生iPPT", "#07C160", "#ffffff",
     "https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA"),
    ("小红书 木先生iPPT", "#FF2442", "#ffffff",
     "https://xhslink.com/m/ESxtgUNMdl"),
    ("著作《图解团队管理》", "#BBDDE5", "#1f3a4d",
     "https://item.m.jd.com/product/14547345.html"),
    ("mu-skill集合", "#9E95B7", "#ffffff",
     "https://muippt.github.io/mu-skill-hub/"),
    ("GitHub muippt", "#181717", "#ffffff",
     "https://github.com/muippt"),
]

VERSION_INFO = {
    "quick": ("快速版", "Quick", 70),
    "standard": ("标准版", "Standard", 93),
    "pro": ("专业版", "Pro", 144),
}
DISCLAIMER_ZH = ("本报告基于 MBTI 人格类型理论的自我认知参考工具，不作为招聘、晋升、"
                 "绩效评估等决策依据")
DISCLAIMER_EN = ("This report is a self-awareness reference tool based on MBTI personality "
                 "typology and must not be used for hiring, promotion, or performance "
                 "decisions.")
# Generic bilingual collaboration tips shown on the team report (zh, en).
TEAM_COLLABORATION_TIPS = [
    ("明确分工，各展所长：直觉型（N）成员适合牵头创意与方案探索，实感型（S）成员适合"
     "把控细节与落地执行，让合适的人做合适的事。",
     "Play to individual strengths: N-dominant members lead ideation and "
     "exploration while S-dominant members own details and execution."),
    ("统一沟通节奏：外向型（E）成员偏好即时讨论，内向型（I）成员需要独立思考的时间；"
     "会议前提前发出议题，会后留出消化时间。",
     "Align the communication rhythm: E members prefer live discussion while I "
     "members need thinking time - share agendas in advance and allow reflection "
     "afterwards."),
    ("建立决策机制：思考型（T）成员关注逻辑与标准，情感型（F）成员关注人与共识；"
     "重大决策先用数据框架收敛，再照顾各方感受。",
     "Set an explicit decision process: T members weigh logic and criteria while "
     "F members weigh people and consensus - converge on data first, then address "
     "feelings."),
    ("用差异对冲盲区：主动邀请倾向不同的成员挑战方案假设，把分歧当作团队免费的"
     "「风险检查」。",
     "Use differences to hedge blind spots: invite members with opposite "
     "preferences to challenge assumptions and treat disagreement as a free risk "
     "review."),
]
# Chinese font fallback chain (mandated order first, then extra system fonts).
CSS_FONT_STACK = ("'PingFang SC','Microsoft YaHei','Noto Sans CJK SC',"
                  "'Hiragino Sans GB','Heiti SC',sans-serif")
REPORTLAB_FONT_CANDIDATES = [
    # name, path, subfontIndex
    ("PingFangSC", "/System/Library/Fonts/PingFang.ttc", 0),
    ("PingFangSC", "/System/Library/Fonts/PingFangSC.ttf", None),
    ("MicrosoftYaHei", "/System/Library/Fonts/Microsoft YaHei.ttc", 0),
    ("MicrosoftYaHei", "C:/Windows/Fonts/msyh.ttc", 0),
    ("NotoSansCJKsc", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 2),
    ("NotoSansCJKsc", "/System/Library/Fonts/NotoSansCJKsc-Regular.otf", None),
    # Extra last-resort system CJK fonts.
    ("STHeiti", "/System/Library/Fonts/STHeiti Medium.ttc", 0),
    ("HiraginoSansGB", "/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
    ("ArialUnicode", "/Library/Fonts/Arial Unicode.ttf", None),
    ("ArialUnicode", "C:/Windows/Fonts/arialuni.ttf", None),
]


def fail(msg, code=EXIT_INPUT_ERROR):
    sys.stderr.write("ERROR: %s\n" % msg)
    sys.exit(code)


def load_json(path, what):
    if not os.path.isfile(path):
        fail("%s not found: %s" % (what, path))
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        fail("cannot read %s (%s): %s" % (what, path, exc))


def clarity_band(clarity):
    for upper, zh, en in CLARITY_BANDS:
        if clarity <= upper:
            return zh, en
    return CLARITY_BANDS[-1][1], CLARITY_BANDS[-1][2]


def esc(text):
    return html_mod.escape(str(text), quote=True)


# ---------------------------------------------------------------------------
# View model: everything the report shows, derived from result.json + data files
# ---------------------------------------------------------------------------

def build_view(result, profiles, careers):
    mbti_type = result["type"]
    if mbti_type not in profiles:
        fail("type %r missing from type_profiles.json" % mbti_type)
    if mbti_type not in careers:
        fail("type %r missing from career_mapping.json" % mbti_type)
    profile = profiles[mbti_type]
    career = careers[mbti_type]
    version = result.get("version", "")
    if version not in VERSION_INFO:
        fail("result.json has unknown version %r" % version)
    v_zh, v_en, v_count = VERSION_INFO[version]

    dims = []
    for dim in DIMENSIONS:
        info = result["dimensions"][dim]
        pole_a, pole_b = DIMENSION_POLES[dim]
        total = info["counts"][pole_a] + info["counts"][pole_b]
        pct_a = info["counts"][pole_a] / total * 100.0 if total else 50.0
        pct_b = 100.0 - pct_a
        dims.append({
            "dim": dim,
            "title_zh": DIMENSION_TITLES[dim][0],
            "title_en": DIMENSION_TITLES[dim][1],
            "pole_a": pole_a, "pole_b": pole_b,
            "label_a_zh": POLE_LABELS[pole_a][0], "label_a_en": POLE_LABELS[pole_a][1],
            "label_b_zh": POLE_LABELS[pole_b][0], "label_b_en": POLE_LABELS[pole_b][1],
            "pct_a": pct_a, "pct_b": pct_b,
            "winner": info.get("winner") or (pole_a if pct_a >= pct_b else pole_b),
            "pct": info["pct"],
            "clarity": info["clarity"],
            "band_zh": info["band_zh"], "band_en": info["band_en"],
            "borderline": info["clarity"] <= 25,
        })

    overall_clarity = result["overall_clarity"]
    ob_zh, ob_en = clarity_band(overall_clarity)

    def match_entry(code):
        p = profiles.get(code, {})
        return {"type": code,
                "name_cn": p.get("name_cn", ""), "name_en": p.get("name_en", "")}

    return {
        "nickname": result.get("nickname") or "",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "version_zh": v_zh, "version_en": v_en, "version_count": v_count,
        "version_label": "%s %s · %d题 / %d items" % (v_zh, v_en, v_count, v_count),
        "type": mbti_type,
        "name_cn": profile["name_cn"], "name_en": profile["name_en"],
        "overall_clarity": overall_clarity,
        "overall_band_zh": ob_zh, "overall_band_en": ob_en,
        "dims": dims,
        "traits_zh": profile["traits_zh"], "traits_en": profile["traits_en"],
        "strengths_zh": profile["strengths_zh"], "strengths_en": profile["strengths_en"],
        "weaknesses_zh": profile["weaknesses_zh"], "weaknesses_en": profile["weaknesses_en"],
        "work_style_zh": profile["work_style_zh"], "work_style_en": profile["work_style_en"],
        "decision_zh": profile["decision_zh"], "decision_en": profile["decision_en"],
        "stress_zh": profile["stress_zh"], "stress_en": profile["stress_en"],
        "communication_zh": profile["communication_zh"],
        "communication_en": profile["communication_en"],
        "careers": career["careers"],
        "growth_zh": career["growth_zh"], "growth_en": career["growth_en"],
        "top3_similar": result.get("top3_similar", []),
        "best_matches": [match_entry(c) for c in profile["best_matches"]],
        "challenging": [match_entry(c) for c in profile["challenging"]],
        "collaboration_zh": profile["collaboration_zh"],
        "collaboration_en": profile["collaboration_en"],
        "disclaimer_zh": DISCLAIMER_ZH, "disclaimer_en": DISCLAIMER_EN,
    }


# ---------------------------------------------------------------------------
# HTML rendering (shared by weasyprint tier and Chromium headless tier)
# ---------------------------------------------------------------------------

def _base_css():
    return """
@page { size: A4 portrait; margin: 16mm 15mm 18mm; }
* { box-sizing: border-box; }
body { font-family: %s; color: #22262e; font-size: 10.5pt; line-height: 1.55;
       margin: 0; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 17pt; margin: 0 0 4pt; }
h2 { font-size: 13.5pt; margin: 0 0 8pt; color: #8A315F;
     border-bottom: 1.5pt solid #AF4283; padding-bottom: 3pt; }
h3 { font-size: 11pt; margin: 16pt 0 6pt; color: #8A315F; }
.compact h3 { margin: 8pt 0 3pt; font-size: 10.5pt; }
.compact .sec { margin-bottom: 6pt; }
.compact .bilingual .zh { margin-bottom: 1pt; font-size: 10pt; }
.compact .bilingual .en { font-size: 9pt; }
.compact table.grid td, .compact table.grid th { padding: 2pt 4pt; font-size: 9pt; }
.compact ul.tight { margin: 2pt 0 4pt; }
.muted { color: #6b7280; }
.sec { margin-bottom: 14pt; }
.bilingual .zh { display: block; margin-bottom: 2pt; }
.bilingual .en { display: block; color: #55606e; font-size: 9.5pt; }
/* Cover */
.cover { text-align: center; padding-top: 55mm; }
.cover .sup { font-size: 12pt; letter-spacing: 2pt; color: #AF4283; }
.cover h1 { font-size: 21pt; margin: 6pt 0 2pt; }
.cover .type-code { font-size: 52pt; font-weight: 700; letter-spacing: 6pt;
                    color: #8A315F; margin: 16mm 0 4pt; }
.cover .type-name { font-size: 15pt; }
.cover .meta { margin-top: 12mm; font-size: 11pt; }
.cover .clarity-box { margin: 10mm auto 0; width: 70mm; border: 1pt solid #E8C6D6;
                      border-radius: 4pt; padding: 5pt; background: #FAEDF3; }
/* Dimension bars */
.dim-block { margin: 14pt 0 20pt; }
.dim-head { display: flex; justify-content: space-between; font-weight: 600;
            font-size: 10.5pt; }
.dim-title { color: #8A315F; }
.axis { display: flex; justify-content: space-between; font-size: 9pt;
        color: #55606e; margin-top: 2pt; }
.axis .win { font-weight: 700; color: #8A315F; }
  .bar { display: flex; height: 9mm; border-radius: 3pt; overflow: hidden;
       margin-top: 2pt; border: 0.5pt solid #E8C6D6; }
  .bar .seg-a { background: #D9A5C0; }
  .bar .seg-b { background: #AF4283; }
  .bar .seg-a.win { background: #AF4283; }
  .bar .seg-b.win { background: #AF4283; }
  .team-bar .team-seg { display: flex; align-items: center; justify-content: center; }
  .team-bar .team-seg.win { background: #AF4283; }
  .team-bar .team-seg.lose { background: #D9A5C0; }
.seg-label { display: flex; align-items: center; justify-content: center;
             color: #fff; font-size: 9.5pt; font-weight: 600; min-width: 12%%; }
.dim-foot { font-size: 9.5pt; margin-top: 2pt; color: #374151; }
.badge { display: inline-block; background: #FAEDF3; border: 0.5pt solid #AF4283;
         color: #8A315F; border-radius: 3pt; padding: 0 4pt; font-size: 8.5pt;
         font-weight: 600; }
.clarity-note { color: #6b7280; font-size: 9pt; }
ul.tight { margin: 4pt 0 10pt; padding-left: 16pt; }
table.grid { width: 100%%; border-collapse: collapse; margin-top: 6pt; }
table.grid td, table.grid th { border: 0.5pt solid #E8C6D6; padding: 4pt 6pt;
                               vertical-align: top; font-size: 9.5pt; }
table.grid th { background: #FAEDF3; color: #8A315F; text-align: left; }
.career-reason { color: #55606e; font-size: 9pt; }
.top3 td { text-align: center; }
.disclaimer { margin-top: 10pt; border: 0.5pt solid #AF4283; background: #FAEDF3;
              border-radius: 4pt; padding: 6pt 8pt; font-size: 9pt; color: #8A315F; }
.footer-note { margin-top: 8pt; color: #9aa3af; font-size: 8pt; text-align: center; }
/* Fixed footer badge row — repeats on every printed page */
.badge-footer { position: fixed; bottom: 2mm; left: 15mm; right: 15mm;
                display: flex; justify-content: center; gap: 5pt;
                flex-wrap: nowrap; }
.badge-footer a { display: inline-block; font-size: 7pt; font-weight: 600;
                  border-radius: 8pt; padding: 1.5pt 7pt; text-decoration: none;
                  white-space: nowrap; line-height: 1.6; }
""" % CSS_FONT_STACK


def build_html(view):
    css = _base_css()

    parts = []
    badge_html = "".join(
        "<a href='%s' style='background:%s;color:%s'>%s</a>" %
        (esc(url), bg, fg, esc(label))
        for label, bg, fg, url in FOOTER_BADGES)

    parts.append("<!DOCTYPE html><html><head><meta charset='utf-8'>")
    parts.append("<title>MBTI Report %s</title><style>%s</style></head><body>" %
                  (esc(view["type"]), css))
    parts.append("<div class='badge-footer'>" + badge_html + "</div>")
    # ---- Page 1: cover ----
    nickname = esc(view["nickname"]) if view["nickname"] else "&mdash;"
    parts.append("""
<div class="page cover">
  <div class="sup">PERSONALITY &amp; CAREER ASSESSMENT</div>
  <h1>MBTI Personality &amp; Career Report</h1>
  <div class="zh">MBTI 人格与职业报告</div>
  <div class="type-code">%s</div>
  <div class="type-name">%s <span class="muted">|</span> %s</div>
  <div class="meta">
    %s
    <div>日期 / Date: %s</div>
    <div>测试版本 / Version: %s</div>
  </div>
  <div class="clarity-box">
    <div>综合清晰度 / Overall Clarity</div>
    <div style="font-size:16pt;font-weight:700;color:#8A315F;">%.1f
      <span style="font-size:10pt;">%s / %s</span></div>
  </div>
</div>""" % (esc(view["type"]), esc(view["name_cn"]), esc(view["name_en"]),
             ("<div>测评者 / Test taker: <b>%s</b></div>" % nickname
              if view["nickname"] else ""),
             esc(view["date"]),
             esc(view["version_label"]), view["overall_clarity"],
             esc(view["overall_band_zh"]), esc(view["overall_band_en"])))
    # ---- Page 2: four dimensions ----
    parts.append("<div class='page'><h2>四维度分析 / Four Dimensions Analysis</h2>")
    for d in view["dims"]:
        a_cls = "seg-a win" if d["winner"] == d["pole_a"] else "seg-a"
        b_cls = "seg-b win" if d["winner"] == d["pole_b"] else "seg-b"
        badge = ("<span class='badge'>边界倾向 Borderline</span>"
                 if d["borderline"] else "")
        parts.append("""
<div class="dim-block">
  <div class="dim-head">
    <span class="dim-title">%s %s / %s</span>
    <span>清晰度 / Clarity: %.1f &nbsp;%s / %s</span>
  </div>
  <div class="axis">
    <span class="%s">%s %s / %s (%d%%)</span>
    <span class="%s">%s %s / %s (%d%%)</span>
  </div>
  <div class="bar">
    <div class="%s" style="width:%.1f%%;"><span class="seg-label">%d%%</span></div>
    <div class="%s" style="width:%.1f%%;"><span class="seg-label">%d%%</span></div>
  </div>
  <div class="dim-foot">倾向 / Preference: <b>%s %s / %s — %.1f%%</b> %s</div>
</div>""" % (esc(d["dim"]), esc(d["title_zh"]), esc(d["title_en"]),
             d["clarity"], esc(d["band_zh"]), esc(d["band_en"]),
             "win" if d["winner"] == d["pole_a"] else "",
             esc(d["pole_a"]), esc(d["label_a_zh"]), esc(d["label_a_en"]),
             round(d["pct_a"]),
             "win" if d["winner"] == d["pole_b"] else "",
             esc(d["pole_b"]), esc(d["label_b_zh"]), esc(d["label_b_en"]),
             round(d["pct_b"]),
             a_cls, d["pct_a"], round(d["pct_a"]),
             b_cls, d["pct_b"], round(d["pct_b"]),
             esc(d["winner"]),
             esc(POLE_LABELS[d["winner"]][0]), esc(POLE_LABELS[d["winner"]][1]),
             d["pct"], badge))
    parts.append("<div class='clarity-note'>注：清晰度 ≤25 的维度标记为「边界倾向」，"
                 "表示该维度两极倾向接近，结果易随情境变化。 / Dimensions with clarity "
                 "≤25 are marked Borderline: both poles are close and the preference "
                 "may vary by context.</div>")
    parts.append("</div>")

    # ---- Page 3: personality profile ----
    parts.append("""
<div class="page compact"><h2>人格特征 / Personality Profile</h2>
  <h3>核心特征 / Core Traits</h3>
  <div class="bilingual sec"><span class="zh">%s</span><span class="en">%s</span></div>
  <h3>优势 &amp; 盲区 / Strengths &amp; Blind Spots</h3>
  <table class="grid"><tr><th style="width:50%%">优势 Strengths</th>
    <th>盲区 Blind Spots</th></tr>
  """ % (esc(view["traits_zh"]), esc(view["traits_en"])))
    strengths_rows = ""
    for i in range(max(len(view["strengths_zh"]), len(view["weaknesses_zh"]))):
        s_zh = esc(view["strengths_zh"][i]) if i < len(view["strengths_zh"]) else ""
        s_en = esc(view["strengths_en"][i]) if i < len(view["strengths_en"]) else ""
        w_zh = esc(view["weaknesses_zh"][i]) if i < len(view["weaknesses_zh"]) else ""
        w_en = esc(view["weaknesses_en"][i]) if i < len(view["weaknesses_en"]) else ""
        strengths_rows += ("<tr><td>%s<div class='career-reason'>%s</div></td>"
                           "<td>%s<div class='career-reason'>%s</div></td></tr>"
                           % (s_zh, s_en, w_zh, w_en))
    parts.append(strengths_rows)
    parts.append("</table>")
    for title_zh, title_en, zh_key, en_key in (
            ("工作风格", "Work Style", "work_style_zh", "work_style_en"),
            ("决策方式", "Decision Making", "decision_zh", "decision_en"),
            ("压力反应", "Stress Response", "stress_zh", "stress_en"),
            ("沟通偏好", "Communication Preference", "communication_zh",
             "communication_en")):
        parts.append("<h3>%s / %s</h3><div class='bilingual sec'>"
                     "<span class='zh'>%s</span><span class='en'>%s</span></div>"
                     % (title_zh, title_en, esc(view[zh_key]), esc(view[en_key])))
    parts.append("</div>")

    # ---- Page 4: careers ----
    parts.append("<div class='page'><h2>职业岗位推荐 / Career Recommendations</h2>")
    parts.append("<table class='grid'><tr><th style='width:34%%'>岗位 / Position</th>"
                 "<th>推荐理由 / Why it fits</th></tr>")
    for c in view["careers"]:
        parts.append("<tr><td><b>%s</b><div class='career-reason'>%s</div></td>"
                     "<td>%s<div class='career-reason'>%s</div></td></tr>"
                     % (esc(c["name_zh"]), esc(c["name_en"]),
                        esc(c["reason_zh"]), esc(c["reason_en"])))
    parts.append("</table>")
    parts.append("<h3>发展建议 / Growth Advice</h3><div class='bilingual sec'>"
                 "<span class='zh'>%s</span><span class='en'>%s</span></div>"
                 % (esc(view["growth_zh"]), esc(view["growth_en"])))
    parts.append("<h3>Top 3 相似类型 / Most Similar Types</h3>")
    parts.append("<table class='grid top3'><tr><th>类型 / Type</th>"
                 "<th>类型名 / Name</th><th>相似度 / Similarity</th></tr>")
    for s in view["top3_similar"]:
        p = PROFILES_CACHE.get(s["type"], {})
        parts.append("<tr><td><b>%s</b></td><td>%s / %s</td><td>%.1f%%</td></tr>"
                     % (esc(s["type"]), esc(p.get("name_cn", "")),
                        esc(p.get("name_en", "")), s["similarity_pct"]))
    parts.append("</table></div>")

    # ---- Page 5: interpersonal matches + disclaimer ----
    parts.append("<div class='page'><h2>人际匹配 / Interpersonal Matches</h2>")
    parts.append("<h3>最佳搭档 / Best Matches</h3><ul class='tight'>")
    for m in view["best_matches"]:
        parts.append("<li><b>%s</b> — %s / %s</li>"
                     % (esc(m["type"]), esc(m["name_cn"]), esc(m["name_en"])))
    parts.append("</ul><h3>磨合挑战 / Challenging Matches</h3><ul class='tight'>")
    for m in view["challenging"]:
        parts.append("<li><b>%s</b> — %s / %s</li>"
                     % (esc(m["type"]), esc(m["name_cn"]), esc(m["name_en"])))
    parts.append("</ul>")
    parts.append("<h3>协作建议 / Collaboration Tips</h3><div class='bilingual sec'>"
                 "<span class='zh'>%s</span><span class='en'>%s</span></div>"
                 % (esc(view["collaboration_zh"]), esc(view["collaboration_en"])))
    parts.append("<div class='disclaimer'><b>免责声明 / Disclaimer：</b>"
                 "%s<br/>%s</div>"
                 % (esc(view["disclaimer_zh"]), esc(view["disclaimer_en"])))
    parts.append("<div class='footer-note'>MBTI Personality &amp; Career Report · "
                 "%s · %s</div></div>" % (esc(view["type"]), esc(view["date"])))
    parts.append("</body></html>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Team report: view model + HTML (weasyprint / Chromium headless path only)
# ---------------------------------------------------------------------------

def build_team_view(results, profiles, careers):
    """Aggregate a list of result dicts into the team report view model."""
    members = []
    vectors = []  # (display name, type, [pct_a per dimension])
    type_counter = Counter()
    dim_counts = {}
    for dim in DIMENSIONS:
        pole_a, pole_b = DIMENSION_POLES[dim]
        dim_counts[dim] = {pole_a: 0, pole_b: 0}
    strengths = []      # unique (zh, en) pairs across all member profiles
    blindspots = []
    seen_strengths = set()
    seen_blindspots = set()

    for result in results:
        for field in ("version", "type", "dimensions", "overall_clarity"):
            if field not in result:
                fail("team result entry missing required field %r" % field)
        mbti_type = result["type"]
        if mbti_type not in profiles:
            fail("type %r missing from type_profiles.json" % mbti_type)
        profile = profiles[mbti_type]
        overall = result["overall_clarity"]
        ob_zh, ob_en = clarity_band(overall)

        winners = []
        vector = []
        for dim in DIMENSIONS:
            info = result["dimensions"][dim]
            pole_a, pole_b = DIMENSION_POLES[dim]
            total = info["counts"][pole_a] + info["counts"][pole_b]
            pct_a = info["counts"][pole_a] / total * 100.0 if total else 50.0
            winner = info.get("winner") or (pole_a if pct_a >= 50.0 else pole_b)
            winners.append(winner)
            vector.append(pct_a)
            dim_counts[dim][winner] += 1

        nickname = result.get("nickname") or ""
        members.append({
            "nickname": nickname,
            "type": mbti_type,
            "name_cn": profile.get("name_cn", ""),
            "name_en": profile.get("name_en", ""),
            "overall_clarity": overall,
            "overall_band_zh": ob_zh, "overall_band_en": ob_en,
            "dims_summary": "-".join(winners),
        })
        type_counter[mbti_type] += 1
        vectors.append((nickname or mbti_type, mbti_type, vector))

        for zh, en in zip(profile["strengths_zh"], profile["strengths_en"]):
            if zh not in seen_strengths:
                seen_strengths.add(zh)
                strengths.append((zh, en))
        for zh, en in zip(profile["weaknesses_zh"], profile["weaknesses_en"]):
            if zh not in seen_blindspots:
                seen_blindspots.add(zh)
                blindspots.append((zh, en))

    total_members = len(results)

    type_distribution = []
    for mbti_type, count in type_counter.most_common():
        p = profiles.get(mbti_type, {})
        type_distribution.append({
            "type": mbti_type,
            "name_cn": p.get("name_cn", ""), "name_en": p.get("name_en", ""),
            "traits_zh": p.get("traits_zh", ""), "traits_en": p.get("traits_en", ""),
            "count": count,
            "pct": count / total_members * 100.0,
        })

    dims = []
    for dim in DIMENSIONS:
        pole_a, pole_b = DIMENSION_POLES[dim]
        count_a = dim_counts[dim][pole_a]
        count_b = dim_counts[dim][pole_b]
        pct_a = count_a / total_members * 100.0 if total_members else 50.0
        pct_b = 100.0 - pct_a
        dims.append({
            "dim": dim,
            "title_zh": DIMENSION_TITLES[dim][0],
            "title_en": DIMENSION_TITLES[dim][1],
            "pole_a": pole_a, "pole_b": pole_b,
            "label_a_zh": POLE_LABELS[pole_a][0],
            "label_a_en": POLE_LABELS[pole_a][1],
            "label_b_zh": POLE_LABELS[pole_b][0],
            "label_b_en": POLE_LABELS[pole_b][1],
            "count_a": count_a, "count_b": count_b,
            "pct_a": pct_a, "pct_b": pct_b,
            "winner": pole_a if count_a >= count_b else pole_b,
        })

    # Complementary pair: members with the largest Manhattan distance between
    # their four-dimension percentage vectors.
    complementary_pairs = []
    best = None
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            dist = sum(abs(a - b) for a, b in zip(vectors[i][2], vectors[j][2]))
            if best is None or dist > best[0]:
                best = (dist, vectors[i], vectors[j])
    if best is not None:
        dist, (name_a, type_a, _va), (name_b, type_b, _vb) = best
        complementary_pairs.append({
            "name_a": name_a, "type_a": type_a,
            "name_b": name_b, "type_b": type_b,
            "distance": dist,
            "reason_zh": ("%s（%s）与 %s（%s）在四个维度上的倾向差异最大"
                          "（差异度 %.0f / 400）。二人组合覆盖了团队中最广的认知"
                          "视角，适合在创意构思与落地执行上互为补充、互相校验。"
                          % (name_a, type_a, name_b, type_b, dist)),
            "reason_en": ("%s (%s) and %s (%s) show the largest divergence "
                          "across the four dimensions (difference %.0f / 400). "
                          "Together they cover the widest range of perspectives "
                          "in the team and complement each other between ideation "
                          "and execution."
                          % (name_a, type_a, name_b, type_b, dist)),
        })

    avg_clarity = (sum(m["overall_clarity"] for m in members) / total_members
                   if total_members else 0.0)
    avg_zh, avg_en = clarity_band(avg_clarity)

    return {
        "is_team": True,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "member_count": total_members,
        "avg_clarity": avg_clarity,
        "avg_band_zh": avg_zh, "avg_band_en": avg_en,
        "members": members,
        "type_distribution": type_distribution,
        "dims": dims,
        "team_strengths_zh": [zh for zh, _ in strengths[:5]],
        "team_strengths_en": [en for _, en in strengths[:5]],
        "team_blindspots_zh": [zh for zh, _ in blindspots[:5]],
        "team_blindspots_en": [en for _, en in blindspots[:5]],
        "complementary_pairs": complementary_pairs,
        "collaboration_zh": [zh for zh, _ in TEAM_COLLABORATION_TIPS],
        "collaboration_en": [en for _, en in TEAM_COLLABORATION_TIPS],
        "disclaimer_zh": DISCLAIMER_ZH, "disclaimer_en": DISCLAIMER_EN,
    }


def build_team_html(team_view):
    css = _base_css()

    parts = []
    badge_html = "".join(
        "<a href='%s' style='background:%s;color:%s'>%s</a>" %
        (esc(url), bg, fg, esc(label))
        for label, bg, fg, url in FOOTER_BADGES)

    parts.append("<!DOCTYPE html><html><head><meta charset='utf-8'>")
    parts.append("<title>MBTI Team Report</title><style>%s</style></head><body>" % css)
    parts.append("<div class='badge-footer'>" + badge_html + "</div>")

    # ---- P1: cover ----
    parts.append("""
<div class="page cover">
  <div class="sup">TEAM PERSONALITY ASSESSMENT</div>
  <h1>团队 MBTI 报告</h1>
  <div>Team MBTI Report</div>
  <div class="type-code">%d</div>
  <div class="type-name">位成员 / Members</div>
  <div class="meta">
    <div>成员数 / Members: %d</div>
    <div>日期 / Date: %s</div>
  </div>
  <div class="clarity-box">
    <div>团队综合清晰度均值 / Average Overall Clarity</div>
    <div style="font-size:16pt;font-weight:700;color:#8A315F;">%.1f
      <span style="font-size:10pt;">%s / %s</span></div>
  </div>
</div>""" % (team_view["member_count"], team_view["member_count"],
             esc(team_view["date"]), team_view["avg_clarity"],
             esc(team_view["avg_band_zh"]), esc(team_view["avg_band_en"])))

    # ---- P2: team members overview ----
    parts.append("<div class='page'><h2>团队成员概览 / Team Members Overview</h2>")
    parts.append("<table class='grid'><tr>"
                 "<th>昵称 / Nickname</th><th>类型 / Type</th>"
                 "<th>类型名 / Name</th><th>四维度 / Dimensions</th>"
                 "<th>清晰度 / Clarity</th><th>等级 / Band</th></tr>")
    for m in team_view["members"]:
        nickname = esc(m["nickname"]) if m["nickname"] else "&mdash;"
        parts.append("<tr><td>%s</td><td><b>%s</b></td>"
                     "<td>%s<div class='career-reason'>%s</div></td>"
                     "<td>%s</td><td>%.1f</td><td>%s / %s</td></tr>"
                     % (nickname, esc(m["type"]), esc(m["name_cn"]),
                        esc(m["name_en"]), esc(m["dims_summary"]),
                        m["overall_clarity"], esc(m["overall_band_zh"]),
                        esc(m["overall_band_en"])))
    parts.append("</table></div>")

    # ---- P3: 16-type distribution ----
    parts.append("<div class='page'><h2>16型分布 / 16-Type Distribution</h2>")
    parts.append("<table class='grid'><tr><th>类型 / Type</th>"
                 "<th>类型名 / Name</th><th>人数 / Count</th>"
                 "<th>占比 / Share</th></tr>")
    for t in team_view["type_distribution"]:
        parts.append("<tr><td><b>%s</b></td>"
                     "<td>%s<div class='career-reason'>%s</div></td>"
                     "<td>%d</td><td>%.1f%%</td></tr>"
                     % (esc(t["type"]), esc(t["name_cn"]), esc(t["name_en"]),
                        t["count"], t["pct"]))
    parts.append("</table>")
    parts.append("<h3>类型特征速览 / Type Traits Snapshot</h3>")
    for t in team_view["type_distribution"]:
        parts.append("<div class='bilingual sec'><span class='zh'><b>%s · %s</b> — %s</span>"
                     "<span class='en'><b>%s · %s</b> — %s</span></div>"
                     % (esc(t["type"]), esc(t["name_cn"]), esc(t["traits_zh"]),
                        esc(t["type"]), esc(t["name_en"]), esc(t["traits_en"])))
    parts.append("</div>")

    # ---- P4: team dimension heatmap ----
    parts.append("<div class='page'><h2>四维度团队热力 / Team Dimension Heatmap</h2>")
    n = team_view["member_count"]
    for d in team_view["dims"]:
        a_win = d["winner"] == d["pole_a"]
        b_win = d["winner"] == d["pole_b"]
        win_count = d["count_a"] if a_win else d["count_b"]
        win_pct = d["pct_a"] if a_win else d["pct_b"]
        parts.append("""
<div class="dim-block">
  <div class="dim-head">
    <span class="dim-title">%s %s / %s</span>
    <span>团队倾向 / Team preference: <b>%s</b></span>
  </div>
  <div class="axis">
    <span class="%s">%s %s / %s（%d人 · %d%%）</span>
    <span class="%s">%s %s / %s（%d人 · %d%%）</span>
  </div>
  <div class="bar team-bar">
    <div class="team-seg %s" style="width:%.1f%%;"><span class="seg-label">%d%%</span></div>
    <div class="team-seg %s" style="width:%.1f%%;"><span class="seg-label">%d%%</span></div>
  </div>
  <div class="dim-foot">团队整体倾向 / Team preference:
    <b>%s %s / %s — %d%%（%d/%d 人 / %d of %d members）</b></div>
</div>""" % (esc(d["dim"]), esc(d["title_zh"]), esc(d["title_en"]),
                 esc(d["winner"]),
                 "win" if a_win else "",
                 esc(d["pole_a"]), esc(d["label_a_zh"]), esc(d["label_a_en"]),
                 d["count_a"], round(d["pct_a"]),
                 "win" if b_win else "",
                 esc(d["pole_b"]), esc(d["label_b_zh"]), esc(d["label_b_en"]),
                 d["count_b"], round(d["pct_b"]),
                 "win" if a_win else "lose", d["pct_a"], round(d["pct_a"]),
                 "win" if b_win else "lose", d["pct_b"], round(d["pct_b"]),
                 esc(d["winner"]),
                 esc(POLE_LABELS[d["winner"]][0]), esc(POLE_LABELS[d["winner"]][1]),
                 round(win_pct), win_count, n, win_count, n))
    parts.append("<div class='clarity-note'>注：柱状图展示团队内偏好各极的人数占比，"
                 "并非个人百分比。 / Bars show the share of members preferring each "
                 "pole, not individual percentages.</div>")
    parts.append("</div>")

    # ---- P5: team strengths & blind spots ----
    parts.append("<div class='page compact'>"
                 "<h2>团队优势与盲区 / Team Strengths &amp; Blind Spots</h2>")
    parts.append("<div class='bilingual sec'><span class='zh'>以下条目来自各成员"
                 "类型画像，去重后取前 5 条。</span><span class='en'>The top 5 unique "
                 "strengths and blind spots aggregated from all members' type "
                 "profiles.</span></div>")
    parts.append("<table class='grid'><tr><th style='width:50%%'>"
                 "优势 Strengths</th><th>盲区 Blind Spots</th></tr>")
    s_zh_list = team_view["team_strengths_zh"]
    s_en_list = team_view["team_strengths_en"]
    w_zh_list = team_view["team_blindspots_zh"]
    w_en_list = team_view["team_blindspots_en"]
    for i in range(max(len(s_zh_list), len(w_zh_list))):
        s_zh = esc(s_zh_list[i]) if i < len(s_zh_list) else ""
        s_en = esc(s_en_list[i]) if i < len(s_en_list) else ""
        w_zh = esc(w_zh_list[i]) if i < len(w_zh_list) else ""
        w_en = esc(w_en_list[i]) if i < len(w_en_list) else ""
        parts.append("<tr><td>%s<div class='career-reason'>%s</div></td>"
                     "<td>%s<div class='career-reason'>%s</div></td></tr>"
                     % (s_zh, s_en, w_zh, w_en))
    parts.append("</table></div>")

    # ---- P6: collaboration tips + complementary pairs + disclaimer ----
    parts.append("<div class='page'>"
                 "<h2>协作建议与互补配对 / Collaboration &amp; Complementary Pairs"
                 "</h2>")
    parts.append("<h3>协作建议 / Collaboration Tips</h3>")
    for zh, en in zip(team_view["collaboration_zh"],
                      team_view["collaboration_en"]):
        parts.append("<div class='bilingual sec'><span class='zh'>%s</span>"
                     "<span class='en'>%s</span></div>" % (esc(zh), esc(en)))
    parts.append("<h3>互补配对 / Complementary Pairs</h3>")
    if team_view["complementary_pairs"]:
        parts.append("<table class='grid'><tr><th>成员 A / Member A</th>"
                     "<th>成员 B / Member B</th>"
                     "<th>差异度 / Difference</th></tr>")
        for p in team_view["complementary_pairs"]:
            parts.append("<tr><td><b>%s</b>（%s）</td><td><b>%s</b>（%s）</td>"
                         "<td>%.0f / 400</td></tr>"
                         % (esc(p["name_a"]), esc(p["type_a"]),
                            esc(p["name_b"]), esc(p["type_b"]), p["distance"]))
        parts.append("</table>")
        pair = team_view["complementary_pairs"][0]
        parts.append("<div class='bilingual sec'><span class='zh'>%s</span>"
                     "<span class='en'>%s</span></div>"
                     % (esc(pair["reason_zh"]), esc(pair["reason_en"])))
    else:
        parts.append("<div class='bilingual sec'><span class='zh'>团队人数不足 "
                     "2 人，无法生成互补配对。</span><span class='en'>Fewer than "
                     "2 members; no complementary pair available.</span></div>")
    parts.append("<div class='disclaimer'><b>免责声明 / Disclaimer：</b>"
                 "%s<br/>%s</div>"
                 % (esc(team_view["disclaimer_zh"]),
                    esc(team_view["disclaimer_en"])))
    parts.append("<div class='footer-note'>MBTI Team Report · %s · %s</div>"
                 % (esc(team_view["member_count"]), esc(team_view["date"])))
    parts.append("</div>")
    parts.append("</body></html>")
    return "".join(parts)


PROFILES_CACHE = {}


# ---------------------------------------------------------------------------
# Tier 1: weasyprint
# ---------------------------------------------------------------------------

def render_with_weasyprint(html_text, out_path):
    import weasyprint  # noqa: import here so the probe is cheap
    weasyprint.HTML(string=html_text, base_url=SCRIPT_DIR).write_pdf(out_path)
    return os.path.isfile(out_path) and os.path.getsize(out_path) > 0


# ---------------------------------------------------------------------------
# Tier 2: Chromium-family headless (Chrome / Chromium / Edge)
# ---------------------------------------------------------------------------

def _browser_candidates():
    paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    ]
    found = [p for p in paths if os.path.isfile(p)]
    for name in ("google-chrome", "chromium", "chromium-browser", "msedge"):
        which = shutil.which(name)
        if which:
            found.append(which)
    return found


def render_with_headless(html_text, out_path):
    candidates = _browser_candidates()
    if not candidates:
        return False, "no Chromium-family browser found"
    tmp_dir = tempfile.mkdtemp(prefix="mbti_report_")
    html_path = os.path.join(tmp_dir, "report.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html_text)
    last_err = ""
    try:
        for exe in candidates:
            cmd = [exe, "--headless", "--disable-gpu", "--no-sandbox",
                   "--disable-crashpad", "--no-pdf-header-footer",
                   "--print-to-pdf=%s" % out_path,
                   "file://%s" % html_path]
            try:
                proc = subprocess.run(cmd, capture_output=True, timeout=120)
                if proc.returncode == 0 and os.path.isfile(out_path) \
                        and os.path.getsize(out_path) > 0:
                    return True, exe
                last_err = "%s exit=%d %s" % (
                    exe, proc.returncode,
                    (proc.stderr or b"").decode("utf-8", "replace")[:200])
            except (OSError, subprocess.TimeoutExpired) as exc:
                last_err = "%s: %s" % (exe, exc)
        return False, last_err or "all browsers failed"
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Tier 3: reportlab
# ---------------------------------------------------------------------------

def _register_cjk_font():
    """Try the mandated font chain, then extra system CJK fonts, then builtin."""
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        return None, "reportlab not installed"
    for name, path, subfont in REPORTLAB_FONT_CANDIDATES:
        if not os.path.isfile(path):
            continue
        try:
            if subfont is not None:
                pdfmetrics.registerFont(TTFont(name, path, subfontIndex=subfont))
            else:
                pdfmetrics.registerFont(TTFont(name, path))
            return name, None
        except Exception:  # noqa: BLE001 - font registration is best effort
            continue
    return None, "no usable CJK font file found"


def render_with_reportlab(view, out_path):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate,
                                        Spacer, Table, TableStyle)
    except ImportError:
        return False, "reportlab not installed"

    font, font_err = _register_cjk_font()
    if font is None:
        print("[generate_report] WARNING: CJK font registration failed (%s); "
              "falling back to built-in fonts, Chinese text may not render."
              % font_err)
        font = "Helvetica"

    navy = colors.HexColor("#8A315F")
    blue = colors.HexColor("#AF4283")
    light = colors.HexColor("#FAEDF3")
    border = colors.HexColor("#E8C6D6")
    gold_bg = colors.HexColor("#FAEDF3")

    st_title = ParagraphStyle("title", fontName=font, fontSize=17, leading=22,
                              textColor=navy, alignment=1, spaceAfter=4)
    st_h2 = ParagraphStyle("h2", fontName=font, fontSize=13, leading=17,
                           textColor=navy, spaceBefore=6, spaceAfter=4)
    st_h3 = ParagraphStyle("h3", fontName=font, fontSize=11, leading=15,
                           textColor=navy, spaceBefore=16, spaceAfter=6)
    st_h3_compact = ParagraphStyle("h3c", parent=st_h3, spaceBefore=8, spaceAfter=3,
                                   fontSize=10.5, leading=13)
    st_body_compact = ParagraphStyle("bodyc", parent=st_body, fontSize=10, leading=13)
    st_muted_compact = ParagraphStyle("mutedc", parent=st_muted, fontSize=9, leading=12)
    st_body = ParagraphStyle("body", fontName=font, fontSize=9.5, leading=14)
    st_muted = ParagraphStyle("muted", parent=st_body, textColor=colors.HexColor(
        "#55606e"), fontSize=8.5, leading=12)
    st_center = ParagraphStyle("center", parent=st_body, alignment=1)
    st_small = ParagraphStyle("small", parent=st_body, fontSize=8.5, leading=12)

    def _draw_badge_footer(canvas, doc_):
        """Draw the 5-brand badge row at the bottom of every page."""
        canvas.saveState()
        from reportlab.lib.colors import HexColor
        try:
            from reportlab.pdfbase.pdfmetrics import stringWidth
        except ImportError:
            canvas.restoreState()
            return
        # --- footer badges ---
        pad_h, pill_h, gap, fs = 4, 7, 3, 5.5
        widths = [stringWidth(lbl, font, fs) + 2 * pad_h
                  for lbl, _, _, _ in FOOTER_BADGES]
        total_w = sum(widths) + gap * (len(FOOTER_BADGES) - 1)
        x = (A4[0] - total_w) / 2.0
        y = 4 * mm
        for (lbl, bg, fg, _url), w in zip(FOOTER_BADGES, widths):
            canvas.setFillColor(HexColor(bg))
            canvas.roundRect(x, y, w, pill_h, pill_h / 2.0, stroke=0, fill=1)
            canvas.setFillColor(HexColor(fg))
            canvas.setFont(font, fs)
            canvas.drawCentredString(x + w / 2.0, y + 1.6, lbl)
            x += w + gap
        canvas.restoreState()

    doc = SimpleDocTemplate(out_path, pagesize=A4,
                            topMargin=16 * mm, bottomMargin=22 * mm,
                            leftMargin=15 * mm, rightMargin=15 * mm,
                            title="MBTI Report %s" % view["type"],
                            onPage=_draw_badge_footer)
    story = []
    W = doc.width

    def bi(zh, en, style_zh=None, style_en=None):
        return [Paragraph(zh, style_zh or st_body),
                Paragraph(en, style_en or st_muted)]

    # ---- P1 cover ----
    story.append(Spacer(1, 55 * mm))
    story.append(Paragraph("PERSONALITY &amp; CAREER ASSESSMENT", st_muted))
    story.append(Paragraph("MBTI Personality &amp; Career Report", st_title))
    story.append(Paragraph("MBTI 人格与职业报告", st_title))
    story.append(Spacer(1, 14 * mm))
    story.append(Paragraph(view["type"], ParagraphStyle(
        "code", fontName=font, fontSize=52, leading=58, textColor=navy,
        alignment=1)))
    story.append(Paragraph("%s | %s" % (view["name_cn"], view["name_en"]), st_title))
    story.append(Spacer(1, 10 * mm))
    if view["nickname"]:
        story.append(Paragraph("测评者 / Test taker: <b>%s</b>"
                               % view["nickname"], st_center))
    story.append(Paragraph("日期 / Date: %s" % view["date"], st_center))
    story.append(Paragraph("测试版本 / Version: %s" % view["version_label"], st_center))
    story.append(Spacer(1, 8 * mm))
    clarity_tbl = Table([[Paragraph("综合清晰度 / Overall Clarity", st_center)],
                         [Paragraph("%.1f &nbsp; %s / %s"
                                    % (view["overall_clarity"],
                                       view["overall_band_zh"],
                                       view["overall_band_en"]), st_title)]],
                        colWidths=[70 * mm])
    clarity_tbl.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, blue),
        ("BACKGROUND", (0, 0), (-1, -1), light),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(clarity_tbl)
    story.append(PageBreak())

    # ---- P2 dimensions ----
    story.append(Paragraph("四维度分析 / Four Dimensions Analysis", st_h2))
    for d in view["dims"]:
        story.append(Paragraph("%s &nbsp;%s / %s — 清晰度 / Clarity: %.1f "
                               "%s / %s" % (d["dim"], d["title_zh"], d["title_en"],
                                            d["clarity"],
                                            d["band_zh"], d["band_en"]), st_h3))
        win_a = d["winner"] == d["pole_a"]
        bar = Table([["", ""]], colWidths=[W * d["pct_a"] / 100.0,
                                           W * d["pct_b"] / 100.0],
                    rowHeights=[9 * mm])
        bar.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor(
                "#AF4283" if win_a else "#D9A5C0")),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor(
                "#AF4283" if not win_a else "#C9759F")),
            ("BOX", (0, 0), (-1, -1), 0.5, border),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(bar)
        axis = Table([[Paragraph("<b>%s %s / %s</b> (%d%%)"
                                 % (d["pole_a"], d["label_a_zh"], d["label_a_en"],
                                    round(d["pct_a"])), st_small),
                       Paragraph("<b>%s %s / %s</b> (%d%%)"
                                 % (d["pole_b"], d["label_b_zh"], d["label_b_en"],
                                    round(d["pct_b"])), ParagraphStyle(
                                     "r", parent=st_small, alignment=2))]],
                      colWidths=[W / 2.0, W / 2.0])
        axis.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
        story.append(axis)
        note = (" <b>[边界倾向 Borderline]</b>" if d["borderline"] else "")
        story.append(Paragraph("倾向 / Preference: <b>%s %s / %s — %.1f%%</b>%s"
                               % (d["winner"], POLE_LABELS[d["winner"]][0],
                                  POLE_LABELS[d["winner"]][1], d["pct"], note),
                               st_body))
        story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "注：清晰度 ≤25 的维度标记为「边界倾向」。 / Dimensions with clarity ≤25 are "
        "marked Borderline: both poles are close and the preference may vary by "
        "context.", st_muted))
    story.append(PageBreak())

    # ---- P3 personality (compact layout to fit on one page) ----
    story.append(Paragraph("人格特征 / Personality Profile", st_h2))
    story.append(Paragraph("核心特征 / Core Traits", st_h3_compact))
    story.extend([Paragraph(view["traits_zh"], st_body_compact),
                  Paragraph(view["traits_en"], st_muted_compact)])
    story.append(Paragraph("优势 &amp; 盲区 / Strengths &amp; Blind Spots", st_h3_compact))
    rows = [[Paragraph("<b>优势 Strengths</b>", st_small),
             Paragraph("<b>盲区 Blind Spots</b>", st_small)]]
    for i in range(max(len(view["strengths_zh"]), len(view["weaknesses_zh"]))):
        rows.append([
            Paragraph("%s<br/><font size=7.5 color='#55606e'>%s</font>" % (
                view["strengths_zh"][i] if i < len(view["strengths_zh"]) else "",
                view["strengths_en"][i] if i < len(view["strengths_en"]) else ""),
                st_small),
            Paragraph("%s<br/><font size=7.5 color='#55606e'>%s</font>" % (
                view["weaknesses_zh"][i] if i < len(view["weaknesses_zh"]) else "",
                view["weaknesses_en"][i] if i < len(view["weaknesses_en"]) else ""),
                st_small)])
    tbl = Table(rows, colWidths=[W / 2.0, W / 2.0], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, border),
        ("BACKGROUND", (0, 0), (-1, 0), light),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story.append(tbl)
    for title_zh, title_en, zh_key, en_key in (
            ("工作风格", "Work Style", "work_style_zh", "work_style_en"),
            ("决策方式", "Decision Making", "decision_zh", "decision_en"),
            ("压力反应", "Stress Response", "stress_zh", "stress_en"),
            ("沟通偏好", "Communication Preference", "communication_zh",
             "communication_en")):
        story.append(Paragraph("%s / %s" % (title_zh, title_en), st_h3_compact))
        story.extend([Paragraph(view[zh_key], st_body_compact),
                      Paragraph(view[en_key], st_muted_compact)])
    story.append(PageBreak())

    # ---- P4 careers ----
    story.append(Paragraph("职业岗位推荐 / Career Recommendations", st_h2))
    rows = [[Paragraph("<b>岗位 / Position</b>", st_small),
             Paragraph("<b>推荐理由 / Why it fits</b>", st_small)]]
    for c in view["careers"]:
        rows.append([
            Paragraph("<b>%s</b><br/><font size=7.5 color='#55606e'>%s</font>"
                      % (c["name_zh"], c["name_en"]), st_small),
            Paragraph("%s<br/><font size=7.5 color='#55606e'>%s</font>"
                      % (c["reason_zh"], c["reason_en"]), st_small)])
    tbl = Table(rows, colWidths=[W * 0.34, W * 0.66], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, border),
        ("BACKGROUND", (0, 0), (-1, 0), light),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story.append(tbl)
    story.append(Paragraph("发展建议 / Growth Advice", st_h3))
    story.extend(bi(view["growth_zh"], view["growth_en"]))
    story.append(Paragraph("Top 3 相似类型 / Most Similar Types", st_h3))
    rows = [[Paragraph("<b>类型 / Type</b>", st_small),
             Paragraph("<b>类型名 / Name</b>", st_small),
             Paragraph("<b>相似度 / Similarity</b>", st_small)]]
    for s in view["top3_similar"]:
        p = PROFILES_CACHE.get(s["type"], {})
        rows.append([Paragraph("<b>%s</b>" % s["type"], st_small),
                     Paragraph("%s / %s" % (p.get("name_cn", ""),
                                            p.get("name_en", "")), st_small),
                     Paragraph("%.1f%%" % s["similarity_pct"], st_small)])
    tbl = Table(rows, colWidths=[W * 0.2, W * 0.55, W * 0.25], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, border),
        ("BACKGROUND", (0, 0), (-1, 0), light),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story.append(tbl)
    story.append(PageBreak())

    # ---- P5 matches + disclaimer ----
    story.append(Paragraph("人际匹配 / Interpersonal Matches", st_h2))
    story.append(Paragraph("最佳搭档 / Best Matches", st_h3))
    for m in view["best_matches"]:
        story.append(Paragraph("• <b>%s</b> — %s / %s"
                               % (m["type"], m["name_cn"], m["name_en"]), st_body))
    story.append(Paragraph("磨合挑战 / Challenging Matches", st_h3))
    for m in view["challenging"]:
        story.append(Paragraph("• <b>%s</b> — %s / %s"
                               % (m["type"], m["name_cn"], m["name_en"]), st_body))
    story.append(Paragraph("协作建议 / Collaboration Tips", st_h3))
    story.extend(bi(view["collaboration_zh"], view["collaboration_en"]))
    story.append(Spacer(1, 10 * mm))
    story.append(Table([[Paragraph(
        "<b>免责声明 / Disclaimer：</b>%s<br/>%s"
        % (view["disclaimer_zh"], view["disclaimer_en"]), st_small)]],
        colWidths=[W]))
    story[-1].setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#AF4283")),
        ("BACKGROUND", (0, 0), (-1, -1), gold_bg),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    doc.build(story)
    return os.path.isfile(out_path) and os.path.getsize(out_path) > 0, None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate MBTI PDF report.")
    parser.add_argument("result", help="path to result.json produced by score.py, "
                        "or (with --team) a JSON array of result dicts")
    parser.add_argument("--team", action="store_true",
                        help="treat input as a JSON array of result dicts and "
                        "generate a team report PDF")
    parser.add_argument("-o", "--output", help="output PDF path (default: "
                        "MBTI_Report_<TYPE>_<timestamp>.pdf next to result.json; "
                        "team mode: MBTI_Team_Report_<timestamp>.pdf)")
    args = parser.parse_args()

    global PROFILES_CACHE
    PROFILES_CACHE = load_json(os.path.join(DATA_DIR, "type_profiles.json"),
                               "type profiles")
    careers = load_json(os.path.join(DATA_DIR, "career_mapping.json"),
                        "career mapping")

    if args.team:
        results = load_json(args.result, "team results file")
        if not isinstance(results, list) or not results:
            fail("--team input must be a non-empty JSON array of result dicts")
        team_view = build_team_view(results, PROFILES_CACHE, careers)
        view = None
        html_text = build_team_html(team_view)
        if args.output:
            out_path = args.output
        else:
            stem = "MBTI_Team_Report_%s" % datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = os.path.join(
                os.path.dirname(os.path.abspath(args.result)), stem + ".pdf")
    else:
        result = load_json(args.result, "result file")
        for field in ("version", "type", "dimensions", "overall_clarity"):
            if field not in result:
                fail("result file missing required field %r" % field)

        view = build_view(result, PROFILES_CACHE, careers)
        html_text = build_html(view)

        if args.output:
            out_path = args.output
        else:
            stem = "MBTI_Report_%s_%s" % (view["type"],
                                          datetime.now().strftime("%Y%m%d_%H%M%S"))
            out_path = os.path.join(
                os.path.dirname(os.path.abspath(args.result)), stem + ".pdf")

    # Tier 1: weasyprint
    try:
        import weasyprint  # noqa: F401
        has_weasyprint = True
    except ImportError:
        has_weasyprint = False

    if has_weasyprint:
        try:
            if render_with_weasyprint(html_text, out_path):
                print("[generate_report] PDF engine: tier 1 (weasyprint)")
                print("[generate_report] PDF written: %s (%d bytes)"
                      % (os.path.abspath(out_path), os.path.getsize(out_path)))
                return
            print("[generate_report] tier 1 weasyprint produced no output; "
                  "falling back")
        except Exception as exc:  # noqa: BLE001 - engine errors must fall back
            print("[generate_report] tier 1 weasyprint failed (%s); falling back"
                  % exc)
    else:
        print("[generate_report] tier 1 weasyprint not available; falling back")

    # Tier 2: Chromium-family headless
    ok, info = render_with_headless(html_text, out_path)
    if ok:
        print("[generate_report] PDF engine: tier 2 (Chromium headless: %s)" % info)
        print("[generate_report] PDF written: %s (%d bytes)"
              % (os.path.abspath(out_path), os.path.getsize(out_path)))
        return
    print("[generate_report] tier 2 headless failed (%s); falling back" % info)

    # Tier 3: reportlab (personal reports only)
    if args.team:
        print("[generate_report] team mode does not support the tier 3 reportlab "
              "fallback yet")
        fail("all PDF engines failed for team report", EXIT_ENGINE_ERROR)
    ok, err = render_with_reportlab(view, out_path)
    if ok:
        print("[generate_report] PDF engine: tier 3 (reportlab)")
        print("[generate_report] PDF written: %s (%d bytes)"
              % (os.path.abspath(out_path), os.path.getsize(out_path)))
        return
    fail("all PDF engines failed; last error (reportlab): %s" % err,
         EXIT_ENGINE_ERROR)


if __name__ == "__main__":
    main()
