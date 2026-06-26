#!/usr/bin/env python3
"""
gen_report.py — 生成深色仪表盘风格资讯 HTML 报告
用法：python3 gen_report.py --data /tmp/report_data.json --output /path/to/report.html
data JSON 结构（由 LLM 填充）：
{
  "title": "报告标题",
  "subtitle": "副标题",
  "date": "2026-03-09",
  "keyword": "搜索关键词",
  "kpis": [{"num":"190K+","label":"xxx","sub":"yyy","color":"blue"},...],
  "summary": "执行摘要文本",
  "timeline": [{"date":"2026-02","title":"xxx","desc":"yyy","color":"blue"},...],
  "news": [{"num":1,"date":"2026-02-16","source":"InfoWorld","title":"xxx",
             "body":"yyy","tag":"战略收购","tag_color":"blue"},...],
  "analysis": {
    "tech":    {"title":"技术亮点","icon":"⚡","color":"blue",  "items":["..."]},
    "risk":    {"title":"安全风险","icon":"⚠️","color":"red",   "items":["..."]},
    "trend":   {"title":"未来趋势","icon":"🚀","color":"green", "items":["..."]}
  },
  "comparison": {
    "headers": ["产品","定位","平台","扩展","隐私","状态"],
    "rows": [["🦞 OpenClaw","自托管网关","★★★★★","★★★★★","★★★★★","被OpenAI收购"],...]
  },
  "conclusion": {
    "pros":  ["优势1","优势2",...],
    "risks": ["风险1","风险2",...],
    "refs":  [{"title":"参考价值1","body":"说明"},...]
  },
  "source_note": "数据来源说明"
}
"""
import argparse, json, os

COLORS = {
    "blue":   ("#58a6ff", "rgba(88,166,255,0.15)",  "rgba(88,166,255,0.3)"),
    "orange": ("#f0883e", "rgba(240,136,62,0.15)",  "rgba(240,136,62,0.3)"),
    "green":  ("#3fb950", "rgba(63,185,80,0.15)",   "rgba(63,185,80,0.3)"),
    "red":    ("#f85149", "rgba(248,81,73,0.15)",   "rgba(248,81,73,0.2)"),
    "purple": ("#a371f7", "rgba(163,113,247,0.15)", "rgba(163,113,247,0.3)"),
    "gold":   ("#d29922", "rgba(210,153,34,0.15)",  "rgba(210,153,34,0.3)"),
}

def c(name, idx=0): return COLORS.get(name, COLORS["blue"])[idx]

def kpi_cards(kpis):
    cols = len(kpis)
    out = f'<div class="kpi-grid" style="grid-template-columns:repeat({cols},1fr)">'
    for k in kpis:
        col = k.get("color","blue")
        out += f'''<div class="kpi-card" style="border-top:2px solid {c(col)}">
  <div class="kpi-num" style="color:{c(col)}">{k["num"]}</div>
  <div class="kpi-label">{k["label"]}</div>
  <div class="kpi-sub">{k.get("sub","")}</div>
</div>'''
    out += "</div>"
    return out

def timeline_html(items):
    out = '<div class="timeline">'
    for it in items:
        col = it.get("color","blue")
        out += f'''<div class="tl-item">
  <div class="tl-dot" style="background:{c(col)};box-shadow:0 0 8px {c(col)}88"></div>
  <div class="tl-date">{it.get("date","")}</div>
  <div class="tl-title">{it.get("title","")}</div>
  <div class="tl-desc">{it.get("desc","")}</div>
</div>'''
    out += "</div>"
    return out

def news_cards(news_list):
    out = '<div class="news-grid">'
    for n in news_list:
        col = n.get("tag_color","blue")
        out += f'''<div class="news-card">
  <div class="news-meta">
    <div class="news-num">{str(n.get("num","")).zfill(2)}</div>
    <span class="news-date">{n.get("date","")}</span>
    <span class="news-source">{n.get("source","")}</span>
  </div>
  <div class="news-title">{n.get("title","")}</div>
  <div class="news-body">{n.get("body","")}</div>
  <span class="news-tag" style="background:{c(col,1)};color:{c(col)};border:1px solid {c(col,2)}">{n.get("tag","")}</span>
</div>'''
    out += "</div>"
    return out

def analysis_html(analysis):
    out = '<div class="analysis-grid">'
    for key in ["tech","risk","trend"]:
        a = analysis.get(key, {})
        col = a.get("color","blue")
        items_html = "".join(f"<li>{i}</li>" for i in a.get("items",[]))
        out += f'''<div class="analysis-card" style="border-top:2px solid {c(col)}">
  <div class="analysis-icon">{a.get("icon","")}</div>
  <div class="analysis-title" style="color:{c(col)}">{a.get("title","")}</div>
  <ul class="analysis-list">{items_html}</ul>
</div>'''
    out += "</div>"
    return out

def comparison_html(cmp):
    hdrs = cmp.get("headers",[])
    rows = cmp.get("rows",[])
    th = "".join(f"<th>{h}</th>" for h in hdrs)
    trs = ""
    for row in rows:
        trs += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    return f'''<div style="background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden">
<table class="cmp-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>
</div>'''

def conclusion_html(con):
    pros  = con.get("pros",[])
    risks = con.get("risks",[])
    refs  = con.get("refs",[])
    pros_html  = "".join(f'<div class="summary-point"><div class="dot" style="background:var(--green)"></div>{p}</div>' for p in pros)
    risks_html = "".join(f'<div class="summary-point"><div class="dot" style="background:var(--red)"></div>{r}</div>' for r in risks)
    refs_cols  = "".join(f'<div class="summary-point" style="flex-direction:column;gap:4px"><div style="color:var(--accent);font-weight:600;margin-bottom:4px">{r["title"]}</div><div>{r["body"]}</div></div>' for r in refs)
    grid_cols  = len(refs) if refs else 1
    return f'''<div class="summary-grid">
  <div class="summary-card" style="border-top:2px solid var(--green)">
    <h3 style="color:var(--green)">✅ 优势与机遇</h3>{pros_html}
  </div>
  <div class="summary-card" style="border-top:2px solid var(--red)">
    <h3 style="color:var(--red)">⚠️ 风险与挑战</h3>{risks_html}
  </div>
  <div class="summary-card" style="border-top:2px solid var(--accent);grid-column:1/-1">
    <h3 style="color:var(--accent)">💡 参考价值</h3>
    <div style="display:grid;grid-template-columns:repeat({grid_cols},1fr);gap:16px;margin-top:8px">{refs_cols}</div>
  </div>
</div>'''

CSS = """
:root{--bg:#0d1117;--card:#161b22;--card2:#1c2128;--border:#30363d;
  --accent:#58a6ff;--accent2:#f0883e;--green:#3fb950;--red:#f85149;
  --purple:#a371f7;--text:#e6edf3;--dim:#8b949e;--gold:#d29922}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;line-height:1.6}
.header{background:linear-gradient(135deg,#0d1117,#161b22,#0d1117);border-bottom:1px solid var(--border);padding:48px 0 36px;text-align:center;position:relative;overflow:hidden}
.header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(88,166,255,0.06),transparent)}
.header-badge{display:inline-block;background:rgba(88,166,255,0.1);border:1px solid rgba(88,166,255,0.3);color:var(--accent);font-size:12px;padding:4px 14px;border-radius:20px;letter-spacing:2px;margin-bottom:16px}
.header h1{font-size:40px;font-weight:800;letter-spacing:2px;background:linear-gradient(135deg,#e6edf3,#58a6ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.header .sub{color:var(--dim);font-size:15px;margin-top:10px;letter-spacing:1px}
.header-meta{display:flex;justify-content:center;gap:32px;margin-top:24px;flex-wrap:wrap}
.header-meta span{font-size:13px;color:var(--dim)}
.header-meta strong{color:var(--accent)}
.container{max-width:1100px;margin:0 auto;padding:0 24px 60px}
.kpi-grid{display:grid;gap:16px;margin:40px 0}
.kpi-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px 20px;text-align:center;transition:border-color .2s}
.kpi-card:hover{border-color:var(--accent)}
.kpi-num{font-size:36px;font-weight:800;line-height:1.2}
.kpi-label{font-size:13px;color:var(--dim);margin-top:6px}
.kpi-sub{font-size:11px;color:var(--dim);margin-top:4px;opacity:.7}
.section{margin:48px 0}
.section-header{display:flex;align-items:center;gap:12px;margin-bottom:24px;padding-bottom:12px;border-bottom:1px solid var(--border)}
.section-title{font-size:20px;font-weight:700;color:var(--text)}
.section-badge{font-size:11px;padding:2px 10px;border-radius:10px;font-weight:600;letter-spacing:1px}
.badge-blue{background:rgba(88,166,255,0.15);color:var(--accent);border:1px solid rgba(88,166,255,0.3)}
.badge-orange{background:rgba(240,136,62,0.15);color:var(--accent2);border:1px solid rgba(240,136,62,0.3)}
.badge-green{background:rgba(63,185,80,0.15);color:var(--green);border:1px solid rgba(63,185,80,0.3)}
.timeline{position:relative;padding-left:28px}
.timeline::before{content:'';position:absolute;left:6px;top:8px;bottom:8px;width:2px;background:linear-gradient(180deg,var(--accent),var(--purple),var(--accent2));border-radius:2px}
.tl-item{position:relative;margin-bottom:24px}
.tl-dot{position:absolute;left:-25px;top:6px;width:14px;height:14px;border-radius:50%;border:2px solid var(--bg)}
.tl-date{font-size:12px;color:var(--dim);margin-bottom:4px;letter-spacing:1px}
.tl-title{font-size:15px;font-weight:600;color:var(--text)}
.tl-desc{font-size:13px;color:var(--dim);margin-top:4px;line-height:1.7}
.news-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.news-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;transition:all .2s}
.news-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.news-meta{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.news-num{width:28px;height:28px;border-radius:50%;background:rgba(88,166,255,0.15);color:var(--accent);font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.news-date{font-size:12px;color:var(--dim)}
.news-source{font-size:11px;padding:2px 8px;border-radius:8px;background:var(--card2);color:var(--dim);border:1px solid var(--border)}
.news-title{font-size:15px;font-weight:600;color:var(--text);margin-bottom:8px;line-height:1.5}
.news-body{font-size:13px;color:var(--dim);line-height:1.7}
.news-tag{display:inline-block;font-size:11px;padding:2px 8px;border-radius:8px;margin-top:10px;font-weight:600}
.analysis-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.analysis-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px}
.analysis-icon{font-size:28px;margin-bottom:12px}
.analysis-title{font-size:15px;font-weight:700;color:var(--text);margin-bottom:12px}
.analysis-list{list-style:none}
.analysis-list li{font-size:13px;color:var(--dim);padding:5px 0;border-bottom:1px solid rgba(48,54,61,0.5);display:flex;align-items:flex-start;gap:8px}
.analysis-list li::before{content:'›';color:var(--accent);flex-shrink:0}
.cmp-table{width:100%;border-collapse:collapse}
.cmp-table th{background:var(--card2);color:var(--dim);font-size:13px;padding:12px 16px;text-align:left;border-bottom:1px solid var(--border);font-weight:600;letter-spacing:1px}
.cmp-table td{padding:12px 16px;border-bottom:1px solid var(--border);font-size:13px;color:var(--dim);vertical-align:top}
.cmp-table tr:hover td{background:rgba(22,27,34,0.5)}
.cmp-table td:first-child{color:var(--text);font-weight:600}
.summary-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.summary-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px}
.summary-card h3{font-size:15px;font-weight:700;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.summary-point{display:flex;gap:10px;margin-bottom:10px;font-size:13px;color:var(--dim);line-height:1.6}
.summary-point .dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;margin-top:7px}
.exec-summary{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px;font-size:14px;color:var(--dim);line-height:1.9}
footer{border-top:1px solid var(--border);padding:24px;text-align:center;color:var(--dim);font-size:12px}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",   required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    d = json.load(open(args.data, encoding="utf-8"))
    title    = d.get("title",    "行业资讯分析报告")
    subtitle = d.get("subtitle", "")
    date     = d.get("date",     "")
    keyword  = d.get("keyword",  "")
    summary  = d.get("summary",  "")
    source   = d.get("source_note","")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | {date}</title>
<style>{CSS}</style></head>
<body>
<div class="header">
  <div class="header-badge">INTELLIGENCE REPORT · {date[:7].replace("-",".")}</div>
  <h1>{title}</h1>
  <div class="sub">{subtitle}</div>
  <div class="header-meta">
    <span>报告日期：<strong>{date}</strong></span>
    <span>关键词：<strong>{keyword}</strong></span>
  </div>
</div>
<div class="container">
  {kpi_cards(d.get("kpis",[]))}

  <div class="section">
    <div class="section-header"><div class="section-title">执行摘要</div>
    <span class="section-badge badge-blue">EXECUTIVE SUMMARY</span></div>
    <div class="exec-summary">{summary}</div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-title">核心事件时间线</div>
    <span class="section-badge badge-orange">TIMELINE</span></div>
    {timeline_html(d.get("timeline",[]))}
  </div>

  <div class="section">
    <div class="section-header"><div class="section-title">十大关键资讯</div>
    <span class="section-badge badge-blue">TOP 10 INSIGHTS</span></div>
    {news_cards(d.get("news",[]))}
  </div>

  <div class="section">
    <div class="section-header"><div class="section-title">深度分析</div>
    <span class="section-badge badge-green">DEEP ANALYSIS</span></div>
    {analysis_html(d.get("analysis",{}))}
  </div>

  {"<div class='section'><div class='section-header'><div class='section-title'>竞品对比</div><span class='section-badge badge-orange'>COMPARISON</span></div>" + comparison_html(d["comparison"]) + "</div>" if d.get("comparison") else ""}

  <div class="section">
    <div class="section-header"><div class="section-title">总结与建议</div>
    <span class="section-badge badge-blue">CONCLUSION</span></div>
    {conclusion_html(d.get("conclusion",{}))}
  </div>
</div>
<footer>{source or title + " · " + date + " · 由 astronClaw AI 生成"}</footer>
</body></html>"""

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)
    size = os.path.getsize(args.output) // 1024
    print(f"✅ 报告生成: {args.output} ({size}KB)")

if __name__ == "__main__":
    main()
