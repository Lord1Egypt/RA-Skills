#!/usr/bin/env python3
"""
Render a code-review JSON payload into a styled standalone HTML report.

Usage:
    python3 render_report.py <input.json> <output.html>

Input JSON schema (all fields required unless marked optional):
{
  "repo": "/abs/path/to/repo",
  "platform": "android" | "ios" | "general",
  "mode": "single" | "range",
  "range": "abc1234..HEAD" | "abc1234",
  "generated_at": "2026-04-22 12:34:56",
  "stats": {"files_changed": 15, "added": 272, "removed": 76},
  "summary": "string (markdown allowed in <p>)",
  "commits": [
    {
      "sha": "abc1234",
      "subject": "fix: ...",
      "author": "name",
      "date": "2026-04-21",
      "files_changed": 3,
      "findings": [
        {
          "severity": "P0" | "P1" | "P2" | "blocker" | "major" | "minor" | "nit",
          "title": "short title",
          "file": "path/to/File.kt",
          "line": "123" | "123-145",
          "dimension": "线程安全 / 内存管理 / ...",
          "rule_source": "general" | "android" | "ios",
          "problem": "markdown text",
          "code": "ORIGINAL code snippet (REQUIRED, non-empty)",
          "code_lang": "kotlin",
          "fix_suggestion": "markdown text (REQUIRED)",
          "fix_code": "suggested code snippet (REQUIRED, non-empty)",
          "fix_lang": "kotlin"
        }
      ],
      "passed": ["string", ...]
    }
  ],
  "overall": {
    "patterns": ["..."],
    "blockers": ["..."],
    "next_steps": ["..."],
    "matrix": [
      {"dim": "线程安全", "p0": 2, "p1": 1, "p2": 0}
    ],
    "verdict": "建议修复 P0 后再合入"
  }
}

The script ENFORCES that every finding has non-empty `code` and `fix_code`.
"""
import json
import sys
import html
from pathlib import Path
from datetime import datetime

SEVERITY_META = {
    "P0":      {"label": "P0 · Blocker",  "color": "#ef4444", "bg": "#fef2f2", "border": "#fecaca"},
    "blocker": {"label": "Blocker",       "color": "#ef4444", "bg": "#fef2f2", "border": "#fecaca"},
    "P1":      {"label": "P1 · Major",    "color": "#f59e0b", "bg": "#fffbeb", "border": "#fde68a"},
    "major":   {"label": "Major",         "color": "#f59e0b", "bg": "#fffbeb", "border": "#fde68a"},
    "P2":      {"label": "P2 · Minor",    "color": "#3b82f6", "bg": "#eff6ff", "border": "#bfdbfe"},
    "minor":   {"label": "Minor",         "color": "#3b82f6", "bg": "#eff6ff", "border": "#bfdbfe"},
    "nit":     {"label": "Nit",           "color": "#64748b", "bg": "#f8fafc", "border": "#e2e8f0"},
}
SEVERITY_ORDER = ["P0", "blocker", "P1", "major", "P2", "minor", "nit"]


def esc(x):
    return html.escape(str(x) if x is not None else "")


def md_inline(text: str) -> str:
    """Very small markdown-ish: escape, then convert `code` and **bold**."""
    if text is None:
        return ""
    s = esc(text)
    # inline code
    import re
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    # paragraphs by double newlines, line breaks by single newline
    paras = [p.strip() for p in s.split("\n\n") if p.strip()]
    return "".join(f"<p>{p.replace(chr(10), '<br/>')}</p>" for p in paras)


def render_finding(idx: int, f: dict) -> str:
    sev = f.get("severity", "P2")
    meta = SEVERITY_META.get(sev, SEVERITY_META["P2"])
    title = esc(f.get("title", "(no title)"))
    file_ = esc(f.get("file", ""))
    line = esc(f.get("line", ""))
    dim = esc(f.get("dimension", ""))
    rule_src = esc(f.get("rule_source", ""))
    problem_html = md_inline(f.get("problem", ""))
    fix_html = md_inline(f.get("fix_suggestion", ""))

    code = f.get("code", "")
    fix_code = f.get("fix_code", "")
    if not code or not str(code).strip():
        raise ValueError(f"Finding '{title}' is missing required `code` snippet")
    if not fix_code or not str(fix_code).strip():
        raise ValueError(f"Finding '{title}' is missing required `fix_code` snippet")

    code_lang = esc(f.get("code_lang", "text"))
    fix_lang = esc(f.get("fix_lang", code_lang))

    return f"""
    <article class="finding" data-sev="{esc(sev)}" style="--sev-color:{meta['color']}; --sev-bg:{meta['bg']}; --sev-border:{meta['border']};">
      <header class="f-head">
        <span class="badge">{esc(meta['label'])}</span>
        <span class="dim">{dim}</span>
        <span class="rule-src">rule: {rule_src}</span>
      </header>
      <h4 class="f-title">#{idx} {title}</h4>
      <div class="f-loc">
        <span class="file">📄 {file_}</span>
        <span class="line">:{line}</span>
      </div>
      <div class="f-section">
        <div class="f-label">问题描述</div>
        <div class="f-body">{problem_html}</div>
      </div>
      <div class="f-section">
        <div class="f-label">原代码片段（核心逻辑）</div>
        <pre class="code"><code class="lang-{code_lang}">{esc(code)}</code></pre>
      </div>
      <div class="f-section">
        <div class="f-label">修复建议</div>
        <div class="f-body">{fix_html}</div>
        <pre class="code fix"><code class="lang-{fix_lang}">{esc(fix_code)}</code></pre>
      </div>
    </article>
    """


def render_commit(i: int, total: int, c: dict) -> str:
    findings = c.get("findings", []) or []
    findings_sorted = sorted(
        findings,
        key=lambda x: SEVERITY_ORDER.index(x.get("severity", "P2"))
        if x.get("severity", "P2") in SEVERITY_ORDER else 99,
    )
    findings_html = "\n".join(render_finding(j + 1, f) for j, f in enumerate(findings_sorted))
    if not findings_html:
        findings_html = '<p class="empty">无问题 ✅</p>'

    passed = c.get("passed", []) or []
    passed_html = ""
    if passed:
        items = "".join(f"<li>{md_inline(p)}</li>" for p in passed)
        passed_html = f'<details class="passed"><summary>✅ Passed Checks ({len(passed)})</summary><ul>{items}</ul></details>'

    p0 = sum(1 for f in findings if f.get("severity") in ("P0", "blocker"))
    p1 = sum(1 for f in findings if f.get("severity") in ("P1", "major"))
    p2 = sum(1 for f in findings if f.get("severity") in ("P2", "minor", "nit"))

    return f"""
    <section class="commit-card" id="commit-{esc(c.get('sha',''))[:7]}">
      <header class="c-head">
        <div class="c-idx">Commit {i}/{total}</div>
        <code class="c-sha">{esc(c.get('sha','')[:10])}</code>
        <h3 class="c-subject">{esc(c.get('subject',''))}</h3>
      </header>
      <div class="c-meta">
        <span>👤 {esc(c.get('author',''))}</span>
        <span>🕒 {esc(c.get('date',''))}</span>
        <span>📁 {esc(c.get('files_changed',0))} files</span>
        <span class="pill p0">P0 · {p0}</span>
        <span class="pill p1">P1 · {p1}</span>
        <span class="pill p2">P2 · {p2}</span>
      </div>
      <div class="findings">{findings_html}</div>
      {passed_html}
    </section>
    """


def render_overall(o: dict) -> str:
    if not o:
        return ""
    patterns = "".join(f"<li>{md_inline(x)}</li>" for x in o.get("patterns", []))
    blockers = "".join(f"<li>{md_inline(x)}</li>" for x in o.get("blockers", []))
    next_steps = "".join(f"<li>{md_inline(x)}</li>" for x in o.get("next_steps", []))
    matrix_rows = "".join(
        f"<tr><td>{esc(r['dim'])}</td>"
        f"<td class='m p0'>{esc(r.get('p0',0))}</td>"
        f"<td class='m p1'>{esc(r.get('p1',0))}</td>"
        f"<td class='m p2'>{esc(r.get('p2',0))}</td></tr>"
        for r in o.get("matrix", [])
    )
    verdict = esc(o.get("verdict", ""))
    return f"""
    <section class="overall">
      <h2>📊 Overall Summary</h2>
      <div class="overall-grid">
        <div class="card">
          <h3>跨 Commit 重复模式</h3>
          <ul>{patterns or '<li class="empty">无</li>'}</ul>
        </div>
        <div class="card">
          <h3>关键 Blocker</h3>
          <ul>{blockers or '<li class="empty">无</li>'}</ul>
        </div>
        <div class="card">
          <h3>建议下一步</h3>
          <ul>{next_steps or '<li class="empty">无</li>'}</ul>
        </div>
      </div>
      <div class="matrix">
        <h3>问题维度统计</h3>
        <table>
          <thead><tr><th>维度</th><th>P0</th><th>P1</th><th>P2</th></tr></thead>
          <tbody>{matrix_rows}</tbody>
        </table>
      </div>
      <div class="verdict">🎯 {verdict}</div>
    </section>
    """


CSS = """
:root {
  --bg: #0f172a;
  --bg-2: #111827;
  --panel: #ffffff;
  --text: #1e293b;
  --muted: #64748b;
  --border: #e2e8f0;
  --accent: #6366f1;
  --accent-2: #8b5cf6;
  --code-bg: #0b1020;
  --code-fg: #e2e8f0;
  --p0: #ef4444;
  --p1: #f59e0b;
  --p2: #3b82f6;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
  color: var(--text);
  background: linear-gradient(135deg, #f5f7fb 0%, #eef2ff 100%);
  line-height: 1.6;
}
.hero {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
  color: white;
  padding: 48px 32px 36px;
  box-shadow: 0 10px 30px rgba(99,102,241,.25);
}
.hero h1 { margin: 0 0 8px; font-size: 28px; letter-spacing: 0.3px; }
.hero .meta { display: flex; flex-wrap: wrap; gap: 16px; opacity: .92; font-size: 14px; }
.hero .meta span { display: inline-flex; align-items: center; gap: 6px; }
.hero .stats {
  display: flex; gap: 12px; margin-top: 18px; flex-wrap: wrap;
}
.hero .stat {
  background: rgba(255,255,255,.18);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,.25);
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 13px;
}
.hero .stat b { font-size: 18px; display: block; margin-bottom: 2px; }

.container { max-width: 1100px; margin: -24px auto 60px; padding: 0 24px; }
.summary-card, .toc, .commit-card, .overall {
  background: var(--panel);
  border-radius: 14px;
  box-shadow: 0 4px 16px rgba(15,23,42,.06);
  padding: 22px 24px;
  margin-bottom: 20px;
  border: 1px solid var(--border);
}
.summary-card h2, .commit-card h3, .overall h2 { margin-top: 0; }

.toc h2 { margin: 0 0 12px; font-size: 16px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
.toc ol { margin: 0; padding-left: 20px; }
.toc li { margin: 6px 0; }
.toc a { color: var(--accent); text-decoration: none; }
.toc a:hover { text-decoration: underline; }

.commit-card .c-head {
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 8px;
}
.c-idx { font-size: 12px; color: var(--muted); background:#f1f5f9; padding: 2px 8px; border-radius: 6px; }
.c-sha { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; background:#eef2ff; color:#4338ca; padding:2px 8px; border-radius:6px; font-size:13px; }
.c-subject { margin: 0; font-size: 18px; }
.c-meta { display: flex; gap: 12px; flex-wrap: wrap; color: var(--muted); font-size: 13px; margin-bottom: 18px; padding-bottom: 14px; border-bottom: 1px dashed var(--border); }
.pill { padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; color: white; }
.pill.p0 { background: var(--p0); }
.pill.p1 { background: var(--p1); }
.pill.p2 { background: var(--p2); }

.finding {
  border-left: 4px solid var(--sev-color);
  background: var(--sev-bg);
  border: 1px solid var(--sev-border);
  border-left-width: 4px;
  border-radius: 10px;
  padding: 16px 18px;
  margin: 14px 0;
}
.finding .f-head { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 6px; }
.finding .badge { background: var(--sev-color); color: white; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; letter-spacing: .3px; }
.finding .dim { color: var(--muted); font-size: 12px; }
.finding .rule-src { color: var(--muted); font-size: 12px; font-family: ui-monospace, monospace; }
.f-title { margin: 4px 0 6px; font-size: 16px; }
.f-loc { font-size: 13px; color: var(--muted); margin-bottom: 12px; font-family: ui-monospace, monospace; }
.f-loc .file { color: #334155; }
.f-section { margin-top: 10px; }
.f-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px; color: var(--muted); font-weight: 700; margin-bottom: 6px; }
.f-body p { margin: 4px 0; }
.f-body code { background: rgba(15,23,42,.08); padding: 1px 5px; border-radius: 4px; font-size: 90%; }

pre.code {
  background: var(--code-bg);
  color: var(--code-fg);
  padding: 14px 16px;
  border-radius: 8px;
  overflow-x: auto;
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 13px;
  line-height: 1.55;
  margin: 6px 0 0;
}
pre.code.fix {
  background: #052e1a;
  border-left: 3px solid #10b981;
}

details.passed { margin-top: 14px; }
details.passed summary { cursor: pointer; color: #10b981; font-weight: 600; }
details.passed ul { margin: 8px 0 0 0; }

.overall .overall-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }
.overall .card { background: #f8fafc; border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; }
.overall .card h3 { margin: 0 0 8px; font-size: 14px; color: var(--muted); }
.overall ul { margin: 0; padding-left: 18px; }
.overall ul li { margin: 4px 0; }
.matrix { margin-top: 18px; }
.matrix table { width: 100%; border-collapse: collapse; font-size: 13px; }
.matrix th, .matrix td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border); }
.matrix td.m { text-align: center; font-weight: 700; }
.matrix td.m.p0 { color: var(--p0); }
.matrix td.m.p1 { color: var(--p1); }
.matrix td.m.p2 { color: var(--p2); }
.verdict {
  margin-top: 18px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 1px solid #fcd34d;
  border-radius: 10px;
  padding: 14px 18px;
  font-weight: 600;
  color: #78350f;
}

.filter-bar {
  display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px;
}
.filter-bar button {
  border: 1px solid var(--border);
  background: white;
  padding: 6px 14px;
  border-radius: 999px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text);
  transition: all .15s;
}
.filter-bar button.active { background: var(--accent); color: white; border-color: var(--accent); }
.filter-bar button:hover:not(.active) { background: #f1f5f9; }

footer { text-align: center; color: var(--muted); font-size: 12px; padding: 30px 0; }
.empty { color: var(--muted); font-style: italic; }
"""

JS = """
document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.filter-bar button');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const sev = btn.dataset.sev;
      document.querySelectorAll('.finding').forEach(f => {
        if (sev === 'all') {
          f.style.display = '';
        } else {
          const fsev = f.dataset.sev;
          const matches = (sev === 'P0' && (fsev === 'P0' || fsev === 'blocker')) ||
                          (sev === 'P1' && (fsev === 'P1' || fsev === 'major')) ||
                          (sev === 'P2' && (fsev === 'P2' || fsev === 'minor' || fsev === 'nit'));
          f.style.display = matches ? '' : 'none';
        }
      });
    });
  });
});
"""


def render(data: dict) -> str:
    repo = esc(data.get("repo", ""))
    platform = esc(data.get("platform", "general"))
    mode = esc(data.get("mode", "single"))
    rng = esc(data.get("range", ""))
    generated_at = esc(data.get("generated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    stats = data.get("stats", {}) or {}
    summary_html = md_inline(data.get("summary", ""))
    commits = data.get("commits", []) or []
    overall_html = render_overall(data.get("overall", {}) or {})

    toc = "".join(
        f'<li><a href="#commit-{esc(c.get("sha",""))[:7]}">'
        f'{esc(c.get("sha",""))[:10]} — {esc(c.get("subject",""))}</a></li>'
        for c in commits
    )

    commits_html = "\n".join(render_commit(i + 1, len(commits), c) for i, c in enumerate(commits))

    title = f"Code Review · {rng}"
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
<div class="hero">
  <h1>🔍 Code Review Report</h1>
  <div class="meta">
    <span>📦 {repo}</span>
    <span>🛠 {platform}</span>
    <span>🌿 {rng}</span>
    <span>⏱ {generated_at}</span>
  </div>
  <div class="stats">
    <div class="stat"><b>{esc(stats.get('files_changed', 0))}</b>files changed</div>
    <div class="stat"><b style="color:#bbf7d0">+{esc(stats.get('added', 0))}</b>insertions</div>
    <div class="stat"><b style="color:#fecaca">-{esc(stats.get('removed', 0))}</b>deletions</div>
    <div class="stat"><b>{len(commits)}</b>commits reviewed</div>
  </div>
</div>

<div class="container">
  <section class="summary-card">
    <h2>📝 Summary</h2>
    {summary_html}
  </section>

  <section class="toc">
    <h2>Commits</h2>
    <ol>{toc}</ol>
  </section>

  <div class="filter-bar">
    <button class="active" data-sev="all">全部</button>
    <button data-sev="P0">仅 P0</button>
    <button data-sev="P1">仅 P1</button>
    <button data-sev="P2">仅 P2</button>
  </div>

  {commits_html}

  {overall_html}

  <footer>Generated by code-reviewer skill · {generated_at}</footer>
</div>
<script>{JS}</script>
</body>
</html>
"""


def main():
    if len(sys.argv) != 3:
        print("usage: render_report.py <input.json> <output.html>", file=sys.stderr)
        sys.exit(2)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    data = json.loads(src.read_text(encoding="utf-8"))
    # Validate required code blocks per finding
    for c in data.get("commits", []):
        for f in c.get("findings", []):
            if not f.get("code", "").strip():
                raise SystemExit(f"[render_report] finding '{f.get('title','?')}' missing `code`")
            if not f.get("fix_code", "").strip():
                raise SystemExit(f"[render_report] finding '{f.get('title','?')}' missing `fix_code`")
    html_text = render(data)
    dst.write_text(html_text, encoding="utf-8")
    print(str(dst))


if __name__ == "__main__":
    main()
