"""静态 HTML 报告生成（spec §3.3, §6）。

自包含：单文件，无外部依赖，可离线分享。
默认脱敏：高敏感度对象的绝对路径只显示相对路径，敏感内容片段截断。
零依赖：纯字符串拼接，不用模板引擎。
"""

from __future__ import annotations

import html
from pathlib import Path

from .schema import Report, AGR, Finding, Sensitivity


def render_html_report(report: Report) -> str:
    """把 Report 渲染为自包含 HTML 字符串。"""
    parts: list[str] = []
    parts.append("<!DOCTYPE html>")
    parts.append("<html lang='zh-CN'>")
    parts.append(_render_head(report))
    parts.append("<body>")
    parts.append(_render_header(report))
    parts.append(_render_summary(report))
    parts.append(_render_invisible(report))
    parts.append(_render_objects(report))
    parts.append(_render_findings(report))
    parts.append("</body></html>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# 片段
# ---------------------------------------------------------------------------


def _render_head(report: Report) -> str:
    return (
        "<head>"
        "<meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>MemoryGuard Report - {html.escape(report.workspace)}</title>"
        "<style>" + _CSS + "</style>"
        "</head>"
    )


def _render_header(report: Report) -> str:
    return (
        "<header class='hero'>"
        "<h1>MemoryGuard 治理报告</h1>"
        f"<div class='meta'>工作区: <code>{html.escape(report.workspace)}</code></div>"
        f"<div class='meta'>生成时间: {html.escape(report.generated_at)}</div>"
        f"<div class='meta'>耗时: {report.duration_ms} ms</div>"
        "</header>"
    )


def _render_summary(report: Report) -> str:
    s = report.summary()
    by_sev = s.get("finding_count_by_severity", {})
    sev_cells = "".join(
        f"<span class='chip sev-{html.escape(k)}'>{html.escape(k)}: {v}</span>"
        for k, v in sorted(by_sev.items())
    )
    return (
        "<section class='card'>"
        "<h2>概览</h2>"
        f"<div class='metrics'>"
        f"<div class='metric'><span class='num'>{s['object_count']}</span><span>对象</span></div>"
        f"<div class='metric'><span class='num'>{len(report.findings)}</span><span>问题</span></div>"
        f"<div class='metric'><span class='num'>{s['invisible_count']}</span><span>不可见</span></div>"
        f"<div class='metric'><span class='num'>{report.health_score:.1f}</span><span>健康分</span></div>"
        "</div>"
        f"<div class='chips'>{sev_cells}</div>"
        "</section>"
    )


def _render_invisible(report: Report) -> str:
    if not report.invisible:
        return ""
    rows = "".join(
        f"<tr><td>{html.escape(str(item.get('type','')))}</td>"
        f"<td><code>{html.escape(str(item.get('path','')))}</code></td>"
        f"<td>{html.escape(str(item.get('reason','')))}</td></tr>"
        for item in report.invisible
    )
    return (
        "<section class='card'>"
        "<h2>不可见范围</h2>"
        "<p class='note'>以下对象无法读取或导出，必须显式显示，不能静默当作不存在。</p>"
        "<table><thead><tr><th>类型</th><th>路径</th><th>原因</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        "</section>"
    )


def _render_objects(report: Report) -> str:
    rows = "".join(_render_object_row(o) for o in report.objects)
    return (
        "<section class='card'>"
        f"<h2>对象清单（{len(report.objects)}）</h2>"
        "<table><thead><tr><th>类型</th><th>路径</th><th>来源</th><th>敏感度</th><th>大小</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        "</section>"
    )


def _render_object_row(o: AGR) -> str:
    # 默认脱敏：只显示相对路径
    rel = o.metadata.get("rel_path", o.path)
    size = o.metadata.get("size", 0)
    sev_class = f"sev-{o.sensitivity.value}" if o.sensitivity != Sensitivity.NONE else ""
    return (
        f"<tr class='{sev_class}'>"
        f"<td><span class='chip type-{o.type.value}'>{o.type.value}</span></td>"
        f"<td><code>{html.escape(str(rel))}</code></td>"
        f"<td>{html.escape(o.source)}</td>"
        f"<td>{html.escape(o.sensitivity.value)}</td>"
        f"<td>{size}</td>"
        "</tr>"
    )


def _render_findings(report: Report) -> str:
    if not report.findings:
        return (
            "<section class='card'>"
            "<h2>问题（0）</h2>"
            "<p class='note'>本次扫描未发现问题。当前为首期骨架，规则引擎将在阶段 B 实现。</p>"
            "</section>"
        )
    # 首期骨架阶段无规则引擎，这里留好渲染逻辑
    rows = "".join(_render_finding_row(f) for f in report.findings)
    return (
        "<section class='card'>"
        f"<h2>问题（{len(report.findings)}）</h2>"
        "<table><thead><tr><th>严重度</th><th>维度</th><th>表面</th><th>证据</th><th>建议</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        "</section>"
    )


def _render_finding_row(f: Finding) -> str:
    return (
        f"<tr class='sev-{f.severity.value}'>"
        f"<td><span class='chip sev-{f.severity.value}'>{f.severity.value}</span></td>"
        f"<td>{html.escape(f.dimension.value)}</td>"
        f"<td>{html.escape(f.surface.value)}</td>"
        f"<td><code>{html.escape(f.evidence[:200])}</code></td>"
        f"<td>{html.escape(f.suggestion[:200])}</td>"
        "</tr>"
    )


# ---------------------------------------------------------------------------
# CSS（内联，保证自包含）
# ---------------------------------------------------------------------------

_CSS = """
:root {
  color-scheme: dark;
  --bg: #040b09; --fg: #e4f5ef; --muted: #78988d;
  --card: rgba(10, 25, 21, 0.88); --border: rgba(110, 231, 196, 0.16);
  --accent: #6ee7c4; --red: #ff7d88; --orange: #e9bb64;
  --green: #6ee7c4; --blue: #9fc4b8; --purple: #9be8d4;
}
* { box-sizing: border-box; }
body {
  max-width: 1440px; margin: 0 auto; padding: 2.5rem;
  background:
    radial-gradient(circle at 12% 8%, rgba(48,170,133,.10), transparent 30rem),
    radial-gradient(circle at 86% 80%, rgba(78,150,125,.07), transparent 34rem),
    var(--bg);
  color: var(--fg);
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI",
    "PingFang SC", "Microsoft YaHei", sans-serif; line-height: 1.6;
}
body::before {
  content: ""; position: fixed; inset: 0; z-index: -1; opacity: .28;
  background-image: linear-gradient(var(--border) 1px, transparent 1px),
    linear-gradient(90deg, var(--border) 1px, transparent 1px);
  background-size: 56px 56px;
  mask-image: radial-gradient(circle at center, black, transparent 80%);
}
code {
  padding: .15em .4em; border: 1px solid var(--border); border-radius: 5px;
  background: rgba(110,231,196,.06); color: #b9d8ce; font-size: .88em;
  overflow-wrap: anywhere;
}
.hero {
  position: relative; overflow: hidden; margin-bottom: 1.5rem; padding: 2rem;
  border: 1px solid var(--border); border-radius: 18px;
  background: radial-gradient(circle at 90% 10%, rgba(110,231,196,.12), transparent 24rem), var(--card);
}
.hero::after {
  content: ""; position: absolute; right: 2.5rem; top: 50%; width: 86px; height: 86px;
  transform: translateY(-50%); border: 1px solid rgba(110,231,196,.28); border-radius: 50%;
  box-shadow: 0 0 44px rgba(110,231,196,.10), inset 0 0 30px rgba(110,231,196,.05);
}
.hero h1 { display: flex; align-items: center; gap: .7rem; margin: 0 0 .75rem; color: var(--fg); letter-spacing: -.03em; }
.hero h1::before {
  content: ""; width: 18px; height: 18px; border: 1px solid var(--accent); border-radius: 50%;
  background: radial-gradient(circle, var(--accent), rgba(110,231,196,.12) 48%, transparent 50%);
  box-shadow: 0 0 18px rgba(110,231,196,.36);
}
.meta { color: var(--muted); font-size: .82rem; margin: .22rem 0; }
.card {
  position: relative; overflow: hidden; padding: 1.5rem; margin-bottom: 1rem;
  border: 1px solid var(--border); border-radius: 14px;
  background: linear-gradient(145deg, rgba(15,35,29,.86), rgba(7,18,15,.80));
}
.card::before { content: ""; position: absolute; top: -2px; left: 22px; width: 5px; height: 5px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 12px var(--accent); }
.card h2 { margin: 0 0 1rem; color: var(--fg); font-size: .92rem; letter-spacing: .04em; }
.metrics { display: grid; grid-template-columns: repeat(4, minmax(120px,1fr)); gap: .75rem; margin: 1rem 0; }
.metric { min-height: 100px; display: flex; flex-direction: column; align-items: flex-start; justify-content: center; padding: 1rem; border: 1px solid var(--border); border-radius: 10px; background: rgba(110,231,196,.035); }
.metric .num { color: var(--accent); font-size: 2rem; font-weight: 550; line-height: 1.1; }
.metric span:last-child { margin-top: .45rem; color: var(--muted); font-size: .75rem; }
.chips { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: .6rem; }
.chip {
  display: inline-flex; align-items: center; padding: .16rem .5rem; margin: .1rem;
  border: 1px solid var(--border); border-radius: 999px; background: rgba(255,255,255,.018);
  color: var(--muted); font-size: .72rem;
}
.sev-info { color: var(--blue); }
.sev-low { color: var(--green); }
.sev-medium { color: var(--orange); border-color: rgba(233,187,100,.28); }
.sev-high, .sev-critical { color: var(--red); border-color: rgba(255,125,136,.28); }
.sev-none { color: var(--muted); }
table { width: 100%; border-collapse: collapse; margin-top: .5rem; font-size: .8rem; }
th, td { padding: .65rem .75rem; text-align: left; vertical-align: top; border-bottom: 1px solid var(--border); }
th { color: var(--muted); font-size: .68rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; }
tbody tr:hover { background: rgba(110,231,196,.035); }
tr.sev-high, tr.sev-critical { background: rgba(255,125,136,.045); }
tr.sev-medium { background: rgba(233,187,100,.04); }
.note { color: var(--muted); font-size: .82rem; }
.type-instruction, .type-skill, .type-memory { color: var(--accent); }
.type-rag_source { color: var(--orange); }
@media (max-width: 760px) {
  body { padding: 1rem; }
  .hero::after { display: none; }
  .metrics { grid-template-columns: repeat(2, minmax(110px,1fr)); }
  .card { overflow-x: auto; }
}
"""
