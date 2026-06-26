#!/usr/bin/env python3
"""
Generate a self-contained HTML audit report from upload audit results.
"""
import datetime
import json
import sys
from pathlib import Path


def escape(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate_html_report(sheet_url, uploaded_rows, output_path="audit_report.html", summary_data=None):
    """
    Generate HTML report.
    
    Args:
        sheet_url: URL of the working spreadsheet
        uploaded_rows: list of dicts with url, file_name, file_type
        output_path: local output file path
        summary_data: optional dict with high/med/low counts and overall result
    """
    items = []
    for row in uploaded_rows:
        url = row.get("url", "")
        fname = row.get("file_name", url.split("/")[-1].split("?")[0] if url else "unknown")
        ftype = row.get("file_type", "image")
        risk = row.get("risk", "high")
        ai = row.get("ai_analysis", {})
        
        thumb_url = ""
        if url and url != "#":
            thumb_url = url.split("?")[0] + "/thumbnail/300x300%3E/quality/80"
        
        items.append({
            "url": url,
            "file_name": fname,
            "file_type": ftype,
            "risk": risk,
            "thumb_url": thumb_url,
            "third_party": ai.get("third_party", "—"),
            "internal": ai.get("internal", "—"),
            "industry": ai.get("industry", "—"),
            "font_result": ai.get("font", "—"),
            "risk_hits": ai.get("risk_hits", []),
            "block_reason": ai.get("block_reason", "暂无明确原因"),
            "suggestions": ai.get("suggestions", []),
            "rewrite_direction": ai.get("rewrite_direction", ""),
        })

    if not items:
        items.append({
            "url": "#", "file_name": "No files", "file_type": "image",
            "risk": "low", "thumb_url": "", "third_party": "—",
            "internal": "—", "industry": "—", "font_result": "—",
            "risk_hits": [], "block_reason": "无数据", "suggestions": [], "rewrite_direction": ""
        })

    high_items = [i for i in items if i["risk"] == "high"]
    med_items = [i for i in items if i["risk"] == "med"]
    low_items = [i for i in items if i["risk"] == "low"]

    if high_items:
        overall_badge = "🔴 高风险批次"
        overall_class = "danger"
        overall_result = "不通过"
        overall_desc = "该批次中存在高风险内容，请查看具体风险点并按建议修改。"
    elif med_items:
        overall_badge = "🟠 中风险批次"
        overall_class = "warn"
        overall_result = "需修改"
        overall_desc = "该批次中存在中等风险内容，建议按建议优化后重新提交。"
    else:
        overall_badge = "🟢 低风险批次"
        overall_class = "ok"
        overall_result = "通过"
        overall_desc = "该批次内容风险较低，审核通过。"

    badge_color = {"danger": "#ff4757", "warn": "#ffa502", "ok": "#2ed573"}.get(overall_class, "#747d8c")

    cards_html = ""
    for item in items:
        risk = item["risk"]
        risk_label = {"high": "🔴 高风险", "med": "🟠 中风险", "low": "🟢 低风险"}.get(risk, risk)
        risk_cls = {"high": "risk-high", "med": "risk-med", "low": "risk-low"}.get(risk, "")

        hits = item["risk_hits"]
        hits_html = "".join(f"<li>• <span class='hit'>{escape(h)}</span></li>" for h in hits) if hits else "<li>暂无明确风险点</li>"
        
        suggestions = item["suggestions"]
        suggestions_html = "".join(f"<li>{i+1}. <span class='suggest'>{escape(s)}</span></li>" for i, s in enumerate(suggestions)) if suggestions else "<li>无具体建议</li>"

        def color_result(val):
            return "#ff6b7a" if "不通过" in str(val) else "#2ed573"

        tp_color = color_result(item["third_party"])
        int_color = color_result(item["internal"])
        ind_color = color_result(item["industry"])

        cards_html += f"""
        <div class="card" data-risk="{risk}">
          <div class="card-header">
            <img class="thumb" src="{escape(item['thumb_url'])}" alt="preview" onerror="this.style.display='none'">
            <div>
              <div class="card-title">{escape(item['file_name'])}</div>
              <span class="risk-badge {risk_cls}">{risk_label}</span>
              <div class="card-subtitle">{escape(item['file_type'])} | {escape(item['url'])}</div>
              <a href="{escape(item['url'])}" target="_blank" style="font-size:12px;color:#747d8c;">🔗 查看原图</a>
            </div>
          </div>
          <div class="section">
            <h4>⚠️ 风险点</h4>
            <ul>{hits_html}</ul>
          </div>
          <div class="section">
            <h4>🚫 BLOCK 原因</h4>
            <div class="block-reason">{escape(item['block_reason'])}</div>
          </div>
          <div class="section">
            <h4>📝 建议修改点</h4>
            <ul>{suggestions_html}</ul>
          </div>
          <div class="section">
            <h4>🔍 审核子项明细</h4>
            <ul>
              <li>第三方审核：<span style="color:{tp_color};">{escape(item['third_party'])}</span></li>
              <li>内部规则审核：<span style="color:{int_color};">{escape(item['internal'])}</span></li>
              <li>行业规则审核：<span style="color:{ind_color};">{escape(item['industry'])}</span></li>
              <li>字体审核：<span style="color:#888;">{escape(item['font_result'])}</span></li>
            </ul>
          </div>
          <div class="section">
            <h4>🏷️ 修改方向</h4>
            <p style="color:#2ed573;">{escape(item['rewrite_direction']) or '无特定方向建议'}</p>
          </div>
        </div>
        """

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>审核报告</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f0f14; color: #e0e0e6; min-height: 100vh; padding: 24px; }}
  .container {{ max-width: 900px; margin: 0 auto; }}
  .header {{ text-align: center; margin-bottom: 32px; }}
  .header h1 {{ font-size: 24px; color: #fff; margin-bottom: 8px; }}
  .header p {{ color: #888; font-size: 14px; }}
  .metrics {{ display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }}
  .metric {{ background: #1a1a24; border-radius: 12px; padding: 20px 24px; flex: 1; min-width: 140px; text-align: center; }}
  .metric .num {{ font-size: 36px; font-weight: 700; }}
  .metric .label {{ font-size: 12px; color: #888; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .metric.danger .num {{ color: #ff4757; }}
  .metric.warn .num {{ color: #ffa502; }}
  .metric.ok .num {{ color: #2ed573; }}
  .metric.total .num {{ color: #747d8c; }}
  .overall {{ background: #1a1a24; border-radius: 16px; padding: 24px; margin-bottom: 24px; border-left: 4px solid {badge_color}; }}
  .overall h2 {{ font-size: 18px; color: #fff; margin-bottom: 8px; }}
  .overall p {{ color: #aaa; font-size: 14px; line-height: 1.6; }}
  .overall .badge {{ display: inline-block; background: {badge_color}; color: #fff; font-size: 12px; padding: 4px 12px; border-radius: 20px; margin-bottom: 12px; font-weight: 600; }}
  .tabs {{ display: flex; gap: 4px; margin-bottom: 24px; }}
  .tab {{ padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; color: #888; background: #1a1a24; border: none; }}
  .tab.active {{ background: {badge_color}; color: #fff; }}
  .card {{ background: #1a1a24; border-radius: 16px; padding: 24px; margin-bottom: 16px; border: 1px solid #2a2a3a; }}
  .card.hidden {{ display: none; }}
  .card .card-header {{ display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }}
  .card .thumb {{ width: 80px; height: 80px; border-radius: 8px; object-fit: cover; background: #2a2a3a; flex-shrink: 0; }}
  .card .card-title {{ font-size: 16px; color: #fff; font-weight: 600; }}
  .card .card-subtitle {{ font-size: 12px; color: #888; margin-top: 4px; word-break: break-all; }}
  .card .risk-badge {{ display: inline-block; font-size: 11px; padding: 3px 10px; border-radius: 12px; font-weight: 600; margin-top: 4px; }}
  .risk-high {{ background: #ff475730; color: #ff4757; border: 1px solid #ff4757; }}
  .risk-med {{ background: #ffa50230; color: #ffa502; border: 1px solid #ffa502; }}
  .risk-low {{ background: #2ed57330; color: #2ed573; border: 1px solid #2ed573; }}
  .section {{ margin-top: 16px; }}
  .section h4 {{ font-size: 13px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }}
  .section p, .section li {{ font-size: 14px; color: #ccc; line-height: 1.7; }}
  .section ul {{ list-style: none; padding-left: 0; }}
  .section li {{ padding: 4px 0; border-bottom: 1px solid #2a2a3a; }}
  .section li:last-child {{ border-bottom: none; }}
  .section .hit {{ color: #ff6b7a; font-weight: 500; }}
  .section .suggest {{ color: #2ed573; }}
  .section .block-reason {{ background: #ff475720; border-left: 3px solid #ff4757; padding: 12px; border-radius: 0 8px 8px 0; color: #ff6b7a; font-size: 13px; }}
  .footer {{ text-align: center; color: #555; font-size: 12px; margin-top: 40px; padding: 20px; }}
  a {{ color: #747d8c; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🛡️ MaybeAI 审核报告</h1>
    <p>审核时间：{now} &nbsp;|&nbsp; 工作表：<a href="{escape(sheet_url)}" target="_blank">{escape(sheet_url)}</a></p>
  </div>

  <div class="metrics">
    <div class="metric total"><div class="num">{len(items)}</div><div class="label">总文件数</div></div>
    <div class="metric danger"><div class="num">{len(high_items)}</div><div class="label">高风险</div></div>
    <div class="metric warn"><div class="num">{len(med_items)}</div><div class="label">中风险</div></div>
    <div class="metric ok"><div class="num">{len(low_items)}</div><div class="label">低风险</div></div>
  </div>

  <div class="overall">
    <span class="badge">{overall_badge}</span>
    <h2>整体审核结果：{overall_result}</h2>
    <p>{overall_desc}</p>
  </div>

  <div class="tabs">
    <button class="tab active" onclick="showTab('all')">全部 ({len(items)})</button>
    <button class="tab" onclick="showTab('high')">🔴 高风险 ({len(high_items)})</button>
    <button class="tab" onclick="showTab('med')">🟠 中风险 ({len(med_items)})</button>
    <button class="tab" onclick="showTab('low')">🟢 低风险 ({len(low_items)})</button>
  </div>

  {cards_html}

  <div class="footer">
    MaybeAI 合规审核报告 · 由 OpenClaw 自动生成 · {now}<br>
    <a href="{escape(sheet_url)}" target="_blank">📄 查看 MaybeAI 工作表</a>
  </div>
</div>
<script>
function showTab(tab) {{
  document.querySelectorAll('.card').forEach(c => {{
    if (tab === 'all') {{ c.style.display = 'block'; }}
    else {{ c.style.display = c.dataset.risk === tab ? 'block' : 'none'; }}
  }});
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  event.target.classList.add('active');
}}
</script>
</body>
</html>"""

    Path(output_path).write_text(html, encoding="utf-8")
    print(f"HTML report generated: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: html_report.py <sheet_url> <uploaded_json> [output_path]")
        sys.exit(1)
    sheet_url = sys.argv[1]
    uploaded_rows = json.loads(sys.argv[2])
    output_path = sys.argv[3] if len(sys.argv) > 3 else "audit_report.html"
    generate_html_report(sheet_url, uploaded_rows, output_path)
