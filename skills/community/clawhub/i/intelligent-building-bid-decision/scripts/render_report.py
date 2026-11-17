#!/usr/bin/env python3
"""把投标决策分析结果 JSON 渲染成自包含 HTML 报告。

零第三方依赖，内联 CSS，可直接浏览器打开/打印/转发。
用法：
    python3 render_report.py --in report.json [-o 输出目录]
输出：<输出目录>/<项目名>_投标决策分析.html，默认目录 ~/zlbx-bid-decision-files/

输入 JSON 结构（所有字段可缺省，缺省则该板块不渲染）：
{
  "project_name": "项目名称",
  "generated_at": "2026-07-14 18:00",
  "conclusion": {
    "verdict": "不建议投 | 谨慎参与 | 建议投",
    "confidence": "高 | 中 | 低",
    "reason": "一句话理由",
    "evidence": ["支撑数据1", "支撑数据2"],
    "prerequisites": ["谨慎参与时的前提条件"]
  },
  "profile": [{"label": "采购方", "value": "...", "url": "可选链接"}],
  "buyer_analysis": ["段落或要点"],
  "competitors": [{"name": "...", "threat": "高|中|低", "coop": "与采购方合作",
                   "wins": "同类中标", "note": "...", "url": "可选"}],
  "expected_bidders": "预计参与家数说明",
  "pricing": {"anchors": ["历史成交锚点"], "range": "建议报价带", "strategy": "策略提示"},
  "risks": ["风险1"],
  "actions": ["行动建议1"],
  "data_notes": {"source": "数据来源说明", "gaps": ["数据缺口"], "cost_units": 9},
  "bid_url": "公告详情免登录链接（API 返回的 url，含 sk 参数）",
  "citations": {                       // 数据引用附录，整体可缺省，缺省则不渲染
    "source": "知了标讯全网招中标数据库",
    "query_note": "检索条件摘要（可缺省）",
    "total_hits": 156,                 // 本次分析纳入的标讯总数
    "cited": 20,                       // 明细展示条数（脚本以实际渲染条数为准）
    "data_as_of": "2026-07-17",
    "items": [{"title": "...", "type": "招标公告/中标结果/拟建项目/公司",
               "date": "2026-07-01", "use": "该条在报告中的用途，如'竞对履历依据'",
               "url": "带sk链接，可缺省", "login_required": false}],
    "more_note": "其余 136 条可在知了标讯主站检索查看（可缺省，缺省时按 total_hits-cited 自动生成）"
  }
}

citations.items 脚本内硬性截断至最多 20 条，超出部分并入 more_note 的数字；
login_required 为 true 的条目标题后加「需登录主站」小标（通用能力，链接一般均带 sk 免登录，用不到时不传即可）；
明细表默认收起（原生 details），打印/导出 PDF 时自动展开。

报告头部固定展示知了标讯品牌标识（所有 skill 版本统一，与页脚的平台声明一致，不做马甲差异化）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from xml.sax.saxutils import escape as _esc


def esc(s) -> str:
    return _esc(str(s if s is not None else ""))


VERDICT_STYLE = {
    "建议投": ("#0d9463", "#e6f7f0", "✅"),
    "谨慎参与": ("#b9770e", "#fdf3e3", "⚠️"),
    "不建议": ("#c0392b", "#fdeceb", "⛔"),
}
THREAT_COLOR = {"高": "#c0392b", "中": "#b9770e", "低": "#0d9463"}

# 知了标讯白色 logo（299x96 PNG base64 内嵌，保证报告离线/打印/转发时不裂图）
_LOGO_B64 = "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"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;
     background:#f2f5f4;color:#1f2d2a;line-height:1.7;padding:24px 12px}
.page{max-width:860px;margin:0 auto}
.hero{background:linear-gradient(135deg,#0e9f8a,#0b7a6a);border-radius:14px;color:#fff;
      padding:28px 30px;margin-bottom:18px}
.hero .brand{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.hero .brand-logo{height:30px;display:block}
.hero .brand-sub{font-size:11px;opacity:.7;letter-spacing:1.5px}
.hero .tag{font-size:13px;opacity:.85;letter-spacing:2px}
.hero h1{font-size:24px;margin-top:6px;font-weight:600}
.hero .meta{font-size:12px;opacity:.75;margin-top:10px}
.verdict{border-radius:14px;padding:22px 26px;margin-bottom:18px;border:1px solid rgba(0,0,0,.05)}
.verdict .v-line{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.verdict .badge{font-size:20px;font-weight:700;padding:6px 18px;border-radius:99px;color:#fff}
.verdict .conf{font-size:13px;color:#5c6b68}
.verdict .reason{margin-top:10px;font-size:15px;font-weight:500}
.verdict ul{margin:10px 0 0 20px;font-size:14px;color:#374a46}
.card{background:#fff;border-radius:14px;padding:22px 26px;margin-bottom:16px;
      border:1px solid rgba(0,0,0,.05);box-shadow:0 1px 3px rgba(14,60,50,.04)}
.card h2{font-size:16px;color:#0b7a6a;margin-bottom:14px;padding-left:10px;
         border-left:4px solid #0e9f8a}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{background:#f0f7f5;color:#3c534e;text-align:left;padding:8px 10px;font-weight:600}
td{padding:8px 10px;border-top:1px solid #edf2f0;vertical-align:top}
.kv td:first-child{color:#5c6b68;width:110px;white-space:nowrap}
.threat{font-weight:700}
ul.plain{margin-left:20px;font-size:14px}
ul.plain li{margin-bottom:6px}
.price-range{font-size:18px;font-weight:700;color:#0b7a6a;margin:8px 0}
.cite-stats{font-size:13px;color:#374a46;margin-bottom:8px}
.cite-detail summary{cursor:pointer;font-size:13.5px;font-weight:600;color:#0b7a6a;padding:4px 0}
.cite-detail th,.cite-detail td:nth-child(2),.cite-detail td:nth-child(3){white-space:nowrap}
.cite-detail[open] summary{margin-bottom:8px}
.cite-tag{font-size:11px;color:#7a8a86;white-space:nowrap}
.cite-more{font-size:12px;color:#7a8a86;margin-top:8px}
a{color:#0b7a6a}
.footer{font-size:12px;color:#7a8a86;background:#eef3f1;border-radius:14px;padding:18px 24px}
.footer .cta{margin-bottom:10px;font-size:13px}
.footer .disclaim{border-top:1px dashed #cfdad6;padding-top:10px;margin-top:6px}
.toolbar{position:fixed;right:18px;bottom:18px;z-index:9;display:flex;gap:10px}
.toolbar button{display:flex;align-items:center;gap:6px;border:none;cursor:pointer;
      background:#0b7a6a;color:#fff;font-size:13px;font-weight:600;
      padding:10px 18px;border-radius:99px;box-shadow:0 4px 14px rgba(11,122,106,.35)}
.toolbar button:hover{background:#0e9f8a}
.toolbar button:disabled{opacity:.6;cursor:wait}
@page{margin:10mm}
@media print{
*{-webkit-print-color-adjust:exact !important;print-color-adjust:exact !important}
body{background:#fff;padding:0}
.card,.verdict{box-shadow:none;break-inside:avoid;border:1px solid #e3ebe8}
.hero{box-shadow:none;break-inside:avoid;border-radius:10px}
table,tr{break-inside:avoid}
.cite-detail{display:block}
.cite-detail>*{display:block}
.cite-detail summary{list-style:none}
.toolbar{display:none}}
"""


def _section(title: str, inner: str) -> str:
    return f'<div class="card"><h2>{esc(title)}</h2>{inner}</div>' if inner else ""


def _link(text, url):
    return f'<a href="{esc(url)}" target="_blank">{esc(text)}</a>' if url else esc(text)


def _citations_block(d: dict) -> str:
    """数据引用附录：口径统计行默认可见，明细表用原生 details 默认收起（打印时自动展开）。"""
    c = d.get("citations") or {}
    if not c:
        return ""
    raw_items = c.get("items") or []
    items = raw_items[:20]  # 硬性截断，超出部分并入 more_note 的数字
    shown = len(items)
    total = c.get("total_hits")

    stats = [f'数据来源：{esc(c.get("source", "知了标讯全网招中标数据库"))}']
    if c.get("query_note"):
        stats.append(f'检索条件：{esc(c["query_note"])}')
    if total is not None:
        stats.append(f"纳入分析 {esc(total)} 条")
    if shown:
        stats.append(f"明细展示 {shown} 条")
    if c.get("data_as_of"):
        stats.append(f'数据截至 {esc(c["data_as_of"])}')
    inner = f'<div class="cite-stats">{" · ".join(stats)}</div>'

    if items:
        rows = "".join(
            f'<tr><td>{_link(x.get("title"), x.get("url"))}'
            + ('<span class="cite-tag">（需登录主站）</span>' if x.get("login_required") else "")
            + f'</td><td>{esc(x.get("type", ""))}</td>'
            f'<td>{esc(x.get("date", ""))}</td><td>{esc(x.get("use", ""))}</td></tr>'
            for x in items
        )
        head = "<tr><th>标题</th><th>类型</th><th>日期</th><th>用途</th></tr>"
        inner += (
            f'<details class="cite-detail"><summary>查看本次引用的 {shown} 条数据明细 ▸</summary>'
            f'<div style="overflow-x:auto"><table>{head}{rows}</table></div></details>'
        )

    more = c.get("more_note", "")
    if len(raw_items) > shown or not more:
        rest = None
        if isinstance(total, (int, float)) and not isinstance(total, bool):
            rest = int(total) - shown
        elif len(raw_items) > shown:
            rest = len(raw_items) - shown
        if rest and rest > 0:
            more = f"其余 {rest} 条可在知了标讯主站检索查看"
    if more:
        more_html = esc(more).replace(
            "知了标讯",
            '<a href="https://www.zhiliaobiaoxun.com" target="_blank">知了标讯</a>', 1)
        inner += f'<div class="cite-more">{more_html}</div>'
    return _section("附：数据引用", inner)


def render(d: dict) -> str:
    name = d.get("project_name", "未命名项目")
    parts = []

    # 头部：品牌标识固定展示（所有 skill 版本统一，与页脚平台声明一致）
    brand_html = (
        f'<div class="brand"><img class="brand-logo" alt="知了标讯" '
        f'src="data:image/png;base64,{_LOGO_B64}"/>'
        '<span class="brand-sub">全网招中标大数据 · zhiliaobiaoxun.com</span></div>'
    )
    bid_link = f'<div class="meta"><a style="color:#d8f3ec" href="{esc(d["bid_url"])}" target="_blank">查看公告原文 ↗</a></div>' if d.get("bid_url") else ""
    parts.append(
        f'<div class="hero">{brand_html}<div class="tag">投标决策分析报告</div><h1>{esc(name)}</h1>'
        f'<div class="meta">生成时间：{esc(d.get("generated_at", datetime.now().strftime("%Y-%m-%d %H:%M")))}'
        f' · 数据来源：知了标讯全网招中标数据</div>{bid_link}</div>'
    )

    # 结论
    c = d.get("conclusion") or {}
    verdict = c.get("verdict", "")
    color, bg, icon = VERDICT_STYLE.get(verdict, ("#5c6b68", "#eef3f1", "📋"))
    ev = "".join(f"<li>{esc(x)}</li>" for x in c.get("evidence", []))
    pre = c.get("prerequisites") or []
    pre_html = (
        '<div class="reason" style="margin-top:12px">参与前提：</div><ul>'
        + "".join(f"<li>{esc(x)}</li>" for x in pre) + "</ul>"
    ) if pre else ""
    parts.append(
        f'<div class="verdict" style="background:{bg}">'
        f'<div class="v-line"><span class="badge" style="background:{color}">{icon} {esc(verdict)}</span>'
        f'<span class="conf">置信度：{esc(c.get("confidence", "—"))}</span></div>'
        f'<div class="reason">{esc(c.get("reason", ""))}</div><ul>{ev}</ul>{pre_html}</div>'
    )

    # 项目画像
    rows = "".join(
        f'<tr><td>{esc(i.get("label"))}</td><td>{_link(i.get("value"), i.get("url"))}</td></tr>'
        for i in d.get("profile", [])
    )
    if rows:
        parts.append(_section("一、项目画像", f'<table class="kv">{rows}</table>'))

    # 采购方分析
    ba = "".join(f"<li>{esc(x)}</li>" for x in d.get("buyer_analysis", []))
    if ba:
        parts.append(_section("二、采购方分析", f'<ul class="plain">{ba}</ul>'))

    # 竞争格局
    comps = d.get("competitors", [])
    if comps:
        head = "<tr><th>潜在竞争者</th><th>威胁</th><th>与采购方合作</th><th>同类中标</th><th>备注</th></tr>"
        body = "".join(
            f'<tr><td>{_link(x.get("name"), x.get("url"))}</td>'
            f'<td class="threat" style="color:{THREAT_COLOR.get(x.get("threat"), "#5c6b68")}">{esc(x.get("threat", ""))}</td>'
            f'<td>{esc(x.get("coop", ""))}</td><td>{esc(x.get("wins", ""))}</td><td>{esc(x.get("note", ""))}</td></tr>'
            for x in comps
        )
        extra = f'<p style="margin-top:10px;font-size:14px">{esc(d["expected_bidders"])}</p>' if d.get("expected_bidders") else ""
        parts.append(_section("三、竞争格局", f"<table>{head}{body}</table>{extra}"))

    # 报价参考
    p = d.get("pricing") or {}
    if p:
        anchors = "".join(f"<li>{esc(x)}</li>" for x in p.get("anchors", []))
        inner = (f'<ul class="plain">{anchors}</ul>' if anchors else "")
        if p.get("range"):
            inner += f'<div class="price-range">建议报价带：{esc(p["range"])}</div>'
        if p.get("strategy"):
            inner += f'<p style="font-size:14px">{esc(p["strategy"])}</p>'
        parts.append(_section("四、报价参考", inner))

    # 风险 / 行动
    risks = "".join(f"<li>{esc(x)}</li>" for x in d.get("risks", []))
    if risks:
        parts.append(_section("五、风险清单", f'<ul class="plain">{risks}</ul>'))
    acts = "".join(f"<li>{esc(x)}</li>" for x in d.get("actions", []))
    if acts:
        parts.append(_section("六、行动建议", f'<ul class="plain">{acts}</ul>'))

    # 附：数据引用（citations 整体缺省时不渲染）
    cite = _citations_block(d)
    if cite:
        parts.append(cite)

    # 数据说明 + 页脚
    n = d.get("data_notes") or {}
    gaps = "；".join(n.get("gaps", [])) or "无"
    cost = f' · 本次分析消耗约 {n["cost_units"]} 积分' if n.get("cost_units") else ""
    parts.append(
        '<div class="footer">'
        f'<div class="cta">📊 报告涉及企业的完整档案与更多商机，见 <a href="https://agent.zhiliaobiaoxun.com" target="_blank">知了商机大师</a>'
        f' · 本报告由 <a href="https://ai.zhiliaobiaoxun.com" target="_blank">知了标讯 AI 开放平台</a> 投标决策分析 Skill 生成</div>'
        f'<div>数据说明：{esc(n.get("source", "知了标讯全网招中标数据"))} · 数据缺口：{esc(gaps)}{cost}</div>'
        '<div class="disclaim">免责声明：本报告基于公开招中标数据自动生成，仅供一般性参考，不构成投标或商业决策建议，'
        '亦不构成对任何单位或个人行为的认定。数据可能存在不完整或滞后，请结合实际情况独立判断并自行承担决策结果。</div></div>'
    )

    # 右下角悬浮工具条：保存长图（SVG foreignObject 原生截图，零依赖；页面无外链资源故 canvas 不受污染）
    # + 存为 PDF（浏览器原生打印）。打印输出中自动隐藏。
    toolbar = (
        '<div class="toolbar">'
        '<button type="button" onclick="zlbxSavePng(this)" '
        'title="导出整页长图（PNG），适合微信/朋友圈转发">🖼 保存长图</button>'
        '<button type="button" onclick="window.print()" '
        'title="在打印对话框中选择「存储为 PDF」">🖨 存为 PDF</button></div>'
    )
    save_png_js = """<script>
function zlbxSavePng(btn){
  var node=document.querySelector('.page');
  var w=node.scrollWidth,h=node.scrollHeight;
  var styles='';
  document.querySelectorAll('style').forEach(function(s){styles+=s.textContent;});
  var xml=new XMLSerializer().serializeToString(node);
  var svg='<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'">'
    +'<foreignObject width="100%" height="100%">'
    +'<div xmlns="http://www.w3.org/1999/xhtml"><style>'+styles+'</style>'+xml+'</div>'
    +'</foreignObject></svg>';
  var orig=btn.textContent;btn.textContent='生成中…';btn.disabled=true;
  function done(){btn.textContent=orig;btn.disabled=false;}
  function fail(){done();alert('当前浏览器不支持长图导出，请改用「存为 PDF」或截图');}
  var img=new Image();
  img.onload=function(){
    try{
      var scale=2;
      var canvas=document.createElement('canvas');
      canvas.width=w*scale;canvas.height=h*scale;
      var ctx=canvas.getContext('2d');
      ctx.scale(scale,scale);
      ctx.fillStyle='#f2f5f4';ctx.fillRect(0,0,w,h);
      ctx.drawImage(img,0,0);
      canvas.toBlob(function(b){
        if(!b){fail();return;}
        var a=document.createElement('a');
        a.href=URL.createObjectURL(b);
        a.download=document.title.replace(/[\\\\/:*?"<>|]/g,'_')+'.png';
        document.body.appendChild(a);a.click();a.remove();
        setTimeout(function(){URL.revokeObjectURL(a.href);},5000);
        done();
      },'image/png');
    }catch(e){fail();}
  };
  img.onerror=fail;
  img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);
}
// 打印/导出 PDF 时自动展开「数据引用」明细，打印结束恢复原收起状态
window.addEventListener('beforeprint',function(){
  document.querySelectorAll('details').forEach(function(d){
    if(!d.open){d.setAttribute('data-print-open','1');d.open=true;}});});
window.addEventListener('afterprint',function(){
  document.querySelectorAll('details').forEach(function(d){
    if(d.getAttribute('data-print-open')){d.removeAttribute('data-print-open');d.open=false;}});});
</script>"""

    return (
        "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{esc(name)} · 投标决策分析</title><style>{CSS}</style></head>"
        f"<body><div class='page'>{''.join(parts)}</div>{toolbar}{save_png_js}</body></html>"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True, help="决策结果 JSON 路径")
    ap.add_argument("-o", "--outdir", default=os.path.expanduser("~/zlbx-bid-decision-files"))
    args = ap.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(args.outdir, exist_ok=True)
    safe = re.sub(r'[\\/:*?"<>|\s]+', "_", data.get("project_name", "未命名项目"))[:60]
    out = os.path.join(args.outdir, f"{safe}_投标决策分析.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(data))
    print(out)


if __name__ == "__main__":
    main()
