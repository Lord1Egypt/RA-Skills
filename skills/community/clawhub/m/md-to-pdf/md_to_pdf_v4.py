#!/usr/bin/env python3
"""Markdown → PDF converter v4.0 - COMPLETE CSS OVERRIDE STRATEGY

Key insight: Pandoc's --standalone generates its own <style> blocks which override custom CSS.
Solution: Delete ALL Pandoc styles, inject ONLY our BUILTIN_CSS.
"""

import sys, os, subprocess, tempfile, pathlib, argparse, re, shutil
import http.server, socketserver, threading, time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from datetime import datetime

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PANDOC = r"D:\mycode\pandoc\pandoc.exe"


BUILTIN_CSS = """
@page {
  size: A4;
  margin: 2.2cm 2cm 2.2cm 2cm;
  @bottom-center {
    content: counter(page) " / " counter(pages);
    font-family: "Microsoft YaHei", sans-serif;
    font-size: 9pt;
    color: #9ca3af;
  }
}
* {
  box-sizing: border-box;
  max-width: none !important;
}
body {
  font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "Noto Sans SC", sans-serif;
  font-size: 11pt;
  line-height: 1.7;
  color: #1a1a1a;
  padding: 0;
  margin: 0;
  overflow-x: hidden;
}

h1 {
  font-size: 20pt;
  font-weight: 700;
  border-bottom: 2.5px solid #2563eb;
  padding-bottom: 8px;
  margin-top: 30px;
  margin-bottom: 16px;
  page-break-before: always;
  color: #111827;
}
h1:first-of-type { page-break-before: auto; }
h2 {
  font-size: 15pt;
  font-weight: 600;
  color: #1e40af;
  margin-top: 24px;
  margin-bottom: 10px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 5px;
}
h3 { font-size: 13pt; font-weight: 600; color: #374151; margin-top: 18px; margin-bottom: 8px; }
h4 { font-size: 11.5pt; font-weight: 600; color: #4b5563; margin-top: 14px; margin-bottom: 6px; }
h5, h6 { font-size: 11pt; font-weight: 600; color: #6b7280; margin-top: 12px; margin-bottom: 4px; }

/* TABLES - V4.0: Override ALL default styles */
table {
  border-collapse: collapse !important;
  width: 100% !important;
  margin: 12px 0 16px 0 !important;
  font-size: 9.5pt;
  line-height: 1.5;
  page-break-inside: auto;
}
thead { display: table-header-group !important; }
tbody { display: table-row-group !important; }
tr { 
  page-break-inside: avoid;
  page-break-after: auto;
  break-inside: avoid;
}
th {
  background-color: #1e40af !important;
  color: white !important;
  font-weight: 600 !important;
  padding: 8px 10px !important;
  text-align: left !important;
  border: 1px solid #1e3a8a !important;
}
td {
  padding: 6px 10px !important;
  border: 1px solid #d1d5db !important;
  vertical-align: top !important;
  word-break: normal;
  overflow-wrap: break-word;
}
tr:nth-child(even) { background-color: #f8fafc !important; }

/* LISTS - V4.0: Force proper rendering */
ul, ol {
  margin: 6px 0 !important;
  padding-left: 28px !important;
  list-style-position: outside !important;
}
ul { list-style-type: disc !important; }
ol { list-style-type: decimal !important; }
li {
  margin-bottom: 4px !important;
  line-height: 1.6 !important;
  padding-left: 4px !important;
  page-break-inside: avoid !important;
  break-inside: avoid !important;
}
li::marker { color: #374151 !important; }
li > p {
  margin: 0.2em 0 !important;
}
li > ul, li > ol {
  margin-top: 3px !important;
  margin-bottom: 3px !important;
  padding-left: 20px !important;
}
li > ul li > ul, li > ol li > ol { padding-left: 16px !important; }
li > ul li > ul li > ul, li > ol li > ol li > ol { padding-left: 12px !important; }

/* Task lists (checkboxes) */
.task-list {
  list-style: none !important;
  padding-left: 0 !important;
}
.task-list li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px !important;
}
.task-list li input[type="checkbox"] {
  margin-top: 3px;
  width: 14px;
  height: 14px;
  cursor: pointer;
  flex-shrink: 0;
}
.task-list li label {
  flex-grow: 1;
  line-height: 1.5;
}

/* Code blocks */
pre {
  background-color: #f3f4f6 !important;
  border: 1px solid #d1d5db !important;
  border-radius: 6px !important;
  padding: 12px 16px !important;
  font-family: "Cascadia Code", "JetBrains Mono", "Consolas", "Microsoft YaHei", monospace !important;
  font-size: 9pt !important;
  line-height: 1.5 !important;
  overflow-x: auto !important;
  white-space: pre-wrap !important;
  word-wrap: break-word !important;
  margin: 10px 0 !important;
  page-break-inside: avoid !important;
}
.diagram-block {
  font-size: 8.2pt !important;
  line-height: 1.35 !important;
  white-space: pre !important;
  word-wrap: normal !important;
  overflow-wrap: normal !important;
  word-break: keep-all !important;
}
code {
  font-family: "Cascadia Code", "JetBrains Mono", "Consolas", "Microsoft YaHei", monospace !important;
  font-size: 0.9em !important;
  background-color: #f0f0f0 !important;
  padding: 1px 4px !important;
  border-radius: 3px !important;
  color: #c7254e !important;
}
pre code {
  background: none !important;
  padding: 0 !important;
  border-radius: 0 !important;
  color: inherit !important;
  font-size: inherit !important;
}

/* Syntax highlighting */
.sourceCode .kw { color: #008000 !important; font-weight: bold !important; }
.sourceCode .dt { color: #902000 !important; }
.sourceCode .dv { color: #40a070 !important; }
.sourceCode .st { color: #a31515 !important; }
.sourceCode .co { color: #008000 !important; font-style: italic !important; }

/* Math rendering */
math {
  font-family: "Cambria Math", "Latin Modern Math", "Times New Roman", serif !important;
}
.math {
  font-family: "Cambria Math", "Latin Modern Math", "Times New Roman", serif !important;
}
.display.math,
div.math {
  display: block !important;
  text-align: center !important;
  margin: 0.6em 0 !important;
  overflow-x: auto !important;
}
.math.inline {
  white-space: nowrap;
}

/* Mermaid diagram rendering */
.mermaid {
  margin: 12px 0 !important;
  text-align: center !important;
  page-break-inside: avoid !important;
  break-inside: avoid !important;
}
.mermaid svg {
  max-width: 100% !important;
  width: auto !important;
  height: auto !important;
  max-height: 58vh !important;
}
.mermaid pre,
pre.mermaid {
  text-align: left;
}

/* Blockquote */
blockquote {
  border-left: 4px solid #3b82f6 !important;
  margin: 10px 0 !important;
  padding: 8px 16px !important;
  background-color: #eff6ff !important;
  color: #1e40af !important;
}

/* HR */
hr { 
  border: none !important;
  border-top: 1px solid #d1d5db !important;
  margin: 20px 0 !important;
}

/* Strong/Emphasis */
strong { font-weight: 700 !important; color: #111827 !important; }
em { font-style: italic !important; color: #374151 !important; }

/* Links */
a { color: #2563eb !important; text-decoration: none !important; }

/* TOC */
#TOC {
  background-color: #f8fafc !important;
  border: 1px solid #e5e7eb !important;
  border-radius: 8px !important;
  padding: 16px 24px !important;
  margin: 16px 0 24px 0 !important;
  page-break-after: always !important;
}
#TOC ul { list-style: none !important; padding-left: 0 !important; }
#TOC > ul { padding-left: 8px !important; }
#TOC li { margin-bottom: 4px !important; }
#TOC a { color: #374151 !important; text-decoration: none !important; font-size: 10.5pt !important; }

/* Images */
img { max-width: 100% !important; height: auto !important; }

/* Print optimization */
@media print {
  body { font-size: 10.5pt !important; }
}
"""


COVER_HTML = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>
@page { size: A4; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #111827;
  background: #ffffff;
  margin: 0;
  padding: 0;
}
.cover-title {
  font-size: 28pt;
  font-weight: 700;
  margin-bottom: 80px;
  line-height: 1.4;
}
.cover-date {
  font-size: 14pt;
  color: #6b7280;
  border-top: 2px solid #e5e7eb;
  padding-top: 20px;
  width: 200px;
  line-height: 1.5;
}
</style></head>
<body>
  <div class="cover-title">{title}</div>
  <div class="cover-date">{date}</div>
</body>
</html>"""


def sanitize_title(text: str) -> str:
    return re.sub(
        r'[\U0001f300-\U0001f9ff\U00002600-\U000027bf\U0000fe00-\U0000fe0f\U0000200d\U0001f1e6-\U0001f1ff]',
        '', text
    ).strip()


def extract_title(md_path: str) -> str:
    with open(md_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# "):
                return sanitize_title(line[2:].strip())
    return pathlib.Path(md_path).stem


def _is_table_row(line: str) -> bool:
    s = line.strip()
    if not s or s.startswith("```"):
        return False
    # Allow optional indentation for markdown tables.
    return s.startswith("|") and s.count("|") >= 2


def _is_table_alignment(line: str) -> bool:
    s = line.strip()
    # Typical alignment row: | --- | :---: | ---: |
    return bool(re.match(r'^\|[\s:\-\|]+\|$', s))


def preprocess_markdown(md_path: str, tmpdir: str):
    """Normalize common markdown issues before Pandoc parsing."""
    raw_text = pathlib.Path(md_path).read_text(encoding="utf-8", errors="replace")
    lines = raw_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    issues = []
    fixed_backtick_lines = 0
    fixed_lang_backtick_lines = 0
    fixed_equation_marker_escape_count = 0
    fixed_table_gap_count = 0
    fixed_list_wrap_count = 0
    fixed_list_leading_blank_count = 0
    suspicious_table_rows = 0

    # Pass 1: Normalize pseudo code fences:
    # - `lang  -> ```lang
    # - `      -> ```
    normalized = []
    in_real_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_real_fence = not in_real_fence
            normalized.append(line)
            continue

        if not in_real_fence:
            # Prevent Pandoc fancy-list misparse for equation steps like:
            # "(1) + (3):" / "(4) - (2):" / "(1) + (2) + (3):"
            # Without this, Pandoc may parse it as ordered list + nested bullet.
            if re.match(r'^\s*\(\d+\)\s*[+\-*/=＋－×÷].*\(\d+\)', line):
                line = re.sub(r'^(\s*)\(', r'\1\\(', line, count=1)
                fixed_equation_marker_escape_count += 1
            elif re.match(r'^\s*[-+*]\s+\(\d+\)\s*[+\-*/=＋－×÷].*\(\d+\)', line):
                # Same issue inside unordered list item content, e.g.:
                # "- (4) - (1): ..."
                line = re.sub(r'^(\s*[-+*]\s+)\(', r'\1\\(', line, count=1)
                fixed_equation_marker_escape_count += 1

            lang_match = re.match(r'^`([A-Za-z0-9_+\-]+)\s*$', stripped)
            if lang_match:
                normalized.append(f"```{lang_match.group(1)}")
                fixed_lang_backtick_lines += 1
                continue
            if stripped == "`":
                normalized.append("```")
                fixed_backtick_lines += 1
                continue

        normalized.append(line)

    # Pass 2: Ensure blank line before/after markdown table blocks.
    with_table_gaps = []
    in_fence = False
    i = 0
    n = len(normalized)
    while i < n:
        line = normalized[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            with_table_gaps.append(line)
            i += 1
            continue

        if not in_fence:
            start_table = False
            if _is_table_row(line):
                prev_line = normalized[i - 1] if i > 0 else ""
                next_line = normalized[i + 1] if i + 1 < n else ""
                start_table = _is_table_alignment(next_line) or _is_table_alignment(prev_line) or _is_table_row(next_line)

            if start_table:
                if with_table_gaps and with_table_gaps[-1].strip() != "":
                    with_table_gaps.append("")
                    fixed_table_gap_count += 1

                while i < n and _is_table_row(normalized[i]):
                    with_table_gaps.append(normalized[i])
                    i += 1

                if i < n and normalized[i].strip() != "":
                    with_table_gaps.append("")
                    fixed_table_gap_count += 1
                continue

        with_table_gaps.append(line)
        i += 1

    # Pass 3: Repair common broken "-" list continuation lines.
    # Example:
    # - item line 1
    #   (generator accidentally starts a new line without indentation)
    #   line 2
    # becomes:
    # - item line 1 line 2
    list_normalized = []
    in_fence = False
    i = 0
    n = len(with_table_gaps)

    bullet_re = re.compile(r'^(\s*)([-+*])\s+(.*\S)\s*$')
    marker_re = re.compile(r'^\s*([-+*]|\d+[.)])\s+')
    heading_re = re.compile(r'^\s{0,3}#{1,6}\s+')
    hr_re = re.compile(r'^\s{0,3}([-*_])(?:\s*\1){2,}\s*$')
    blockquote_re = re.compile(r'^\s*>')

    while i < n:
        line = with_table_gaps[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            list_normalized.append(line)
            i += 1
            continue

        if in_fence:
            list_normalized.append(line)
            i += 1
            continue

        m = bullet_re.match(line)
        if not m or hr_re.match(stripped):
            list_normalized.append(line)
            i += 1
            continue

        base_indent = len(m.group(1))
        merged = line.rstrip()
        j = i + 1
        while j < n:
            nxt = with_table_gaps[j]
            nxt_strip = nxt.strip()

            if not nxt_strip:
                break
            if nxt_strip.startswith("```"):
                break
            if heading_re.match(nxt) or blockquote_re.match(nxt):
                break
            if _is_table_row(nxt):
                break
            if hr_re.match(nxt_strip):
                break

            nxt_indent = len(nxt) - len(nxt.lstrip(" "))
            # New list item at same or less indentation => stop.
            if marker_re.match(nxt) and nxt_indent <= base_indent:
                break
            # Nested list / code block / explicit indentation => keep structure.
            if nxt_indent > base_indent:
                break

            merged += " " + nxt_strip
            fixed_list_wrap_count += 1
            j += 1

        list_normalized.append(merged)
        i = j

    # Pass 4: Ensure blank line before top-level "-" list after paragraph text.
    # Pandoc may parse:
    #   段落文本：
    #   - item
    # as one paragraph instead of a list if there is no blank line.
    list_spaced = []
    in_fence = False
    bullet_re = re.compile(r'^\s*[-+*]\s+')
    for line in list_normalized:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            list_spaced.append(line)
            continue

        if not in_fence and bullet_re.match(line):
            curr_indent = len(line) - len(line.lstrip(" "))
            if curr_indent == 0 and list_spaced and list_spaced[-1].strip() != "":
                prev = list_spaced[-1].strip()
                if (
                    not marker_re.match(prev)
                    and not _is_table_row(prev)
                    and not heading_re.match(prev)
                    and not blockquote_re.match(prev)
                    and not hr_re.match(prev)
                ):
                    list_spaced.append("")
                    fixed_list_leading_blank_count += 1

        list_spaced.append(line)

    # Validation checks.
    fence_count = 0
    in_fence_validation = False
    for line in list_spaced:
        if line.strip().startswith("```"):
            fence_count += 1
            in_fence_validation = not in_fence_validation
            continue
        if in_fence_validation:
            continue
        s = line.strip()
        if s.startswith("|") and not _is_table_row(s) and not s.startswith(">"):
            # A line containing | but not recognized as a table row
            # can indicate malformed table syntax from generated markdown.
            suspicious_table_rows += 1
    if fence_count % 2 != 0:
        issues.append("检测到未闭合代码块（``` 数量为奇数），Pandoc 可能仍会误判部分结构。")

    if fixed_lang_backtick_lines:
        issues.append(f"已修复 {fixed_lang_backtick_lines} 处 `lang 伪代码块起始标记。")
    if fixed_backtick_lines:
        issues.append(f"已修复 {fixed_backtick_lines} 处单反引号代码块边界。")
    if fixed_equation_marker_escape_count:
        issues.append(
            f"已修复 {fixed_equation_marker_escape_count} 处 '(n) +|-|*|/|=' 算式行误判为列表的问题。"
        )
    if fixed_table_gap_count:
        issues.append(f"已自动补齐 {fixed_table_gap_count} 处表格前后空行。")
    if fixed_list_wrap_count:
        issues.append(f"已修复 {fixed_list_wrap_count} 处 '-' 列表续行断裂。")
    if fixed_list_leading_blank_count:
        issues.append(f"已自动补齐 {fixed_list_leading_blank_count} 处列表前置空行（避免被识别为普通段落）。")
    if suspicious_table_rows:
        issues.append(
            f"检测到 {suspicious_table_rows} 行疑似表格但语法不完整（包含“|”但不满足标准表格行），可能影响渲染。"
        )

    normalized_md = os.path.join(tmpdir, "normalized_input.md")
    pathlib.Path(normalized_md).write_text("\n".join(list_spaced), encoding="utf-8")
    return normalized_md, issues


def mark_diagram_code_blocks(html_content: str) -> str:
    """Mark box-drawing / flow-diagram code blocks for special CSS rendering."""

    diagram_chars = set("┌┐└┘├┤┬┴┼│─→←↑↓")

    def _replace(match):
        pre_attrs = match.group(1) or ""
        code_attrs = match.group(2) or ""
        inner = match.group(3) or ""
        if any(ch in inner for ch in diagram_chars):
            if 'class="' in pre_attrs:
                pre_attrs = re.sub(
                    r'class="([^"]*)"',
                    lambda m: f'class="{m.group(1)} diagram-block"',
                    pre_attrs,
                    count=1,
                )
            else:
                pre_attrs = (pre_attrs + ' class="diagram-block"').strip()
        pre_tag = "<pre>" if not pre_attrs else f"<pre {pre_attrs}>"
        code_tag = "<code>" if not code_attrs else f"<code {code_attrs}>"
        return f"{pre_tag}{code_tag}{inner}</code></pre>"

    pattern = re.compile(r"<pre(?:\s+([^>]*))?><code(?:\s+([^>]*))?>(.*?)</code></pre>", re.DOTALL)
    return pattern.sub(_replace, html_content)


def md_to_html(md_path: str, tmpdir: str, toc: bool, css_path: str) -> str:
    """Generate HTML with Pandoc, then REMOVE all Pandoc styles and inject ours."""
    html_path = os.path.join(tmpdir, "output.html")

    cmd = [
        PANDOC, md_path, "-o", html_path,
        "--standalone",
        "--from", "markdown-fancy_lists",
        "--mathml",
        "--highlight-style", "pygments",
        "--metadata", "lang=zh-CN",
    ]
    if toc:
        cmd.extend(["--toc", "--toc-depth=3"])

    if css_path:
        css_content = pathlib.Path(css_path).read_text(encoding="utf-8")
        css_file = os.path.join(tmpdir, "style.css")
        pathlib.Path(css_file).write_text(css_content, encoding="utf-8")
        cmd.extend(["--css", "style.css"])
    else:
        css_file = os.path.join(tmpdir, "style.css")
        pathlib.Path(css_file).write_text(BUILTIN_CSS, encoding="utf-8")
        cmd.extend(["--css", "style.css"])

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"Pandoc error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    html_content = pathlib.Path(html_path).read_text(encoding="utf-8")

    # CRITICAL FIX: Remove ALL of Pandoc's built-in <style> blocks!
    # This is the key difference from v4.0 (replaces v2.2/v2.1 CSS override strategy)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Inject our BUILTIN_CSS as the ONLY stylesheet
    html_content = re.sub(
        r'</head>',
        f'<style>{BUILTIN_CSS}</style></head>',
        html_content,
        count=1
    )

    # Mark ASCII/box-drawing diagrams for non-wrapping rendering.
    html_content = mark_diagram_code_blocks(html_content)

    # Remove Pandoc-generated colgroup width hints so table columns can size by content.
    # This improves readability for "label + long text" tables.
    html_content = re.sub(r'<colgroup>.*?</colgroup>\s*', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # Move TOC after cover-page div (if present)
    if toc:
        toc_match = re.search(r'(<nav id="TOC".*?</nav>)', html_content, re.DOTALL)
        cover_match = re.search(r'(<div class="cover-page".*?</div>)', html_content, re.DOTALL)
        if toc_match and cover_match:
            toc_html = toc_match.group(1)
            html_content = html_content[:toc_match.start()] + html_content[toc_match.end():]
            new_cover_match = re.search(r'(<div class="cover-page".*?</div>)', html_content, re.DOTALL)
            if new_cover_match:
                html_content = html_content[:new_cover_match.end()] + toc_html + html_content[new_cover_match.end():]
            html_content = re.sub(r'\s*<hr\s*/?>\s*\n?', '', html_content, count=1)

    pathlib.Path(html_path).write_text(html_content, encoding="utf-8")
    return html_path


def render_mermaid_if_needed(page):
    """Render Mermaid blocks (if any) before printing PDF."""
    candidate_count = page.evaluate("""
() => {
  const sels = [
    'pre code.language-mermaid',
    'pre code.mermaid',
    'pre.mermaid',
    'div.mermaid'
  ];
  const all = new Set();
  for (const s of sels) {
    document.querySelectorAll(s).forEach((el) => all.add(el));
  }
  return all.size;
}
""")
    if not candidate_count:
        return

    try:
        page.add_script_tag(url="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js")
    except Exception as e:
        print(f"  Mermaid render warning: script load failed, fallback to code block ({e})")
        return

    result = page.evaluate("""
async () => {
  if (!window.mermaid) {
    return { rendered: 0, failed: 0, total: 0, reason: 'mermaid_not_loaded' };
  }

  window.mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',
    theme: 'default'
  });

  const getCandidates = () => {
    const found = [];
    document.querySelectorAll('pre code.language-mermaid, pre code.mermaid').forEach((code) => {
      found.push({ host: code.closest('pre') || code, source: code.textContent || '' });
    });
    document.querySelectorAll('pre.mermaid').forEach((pre) => {
      if (!found.some((x) => x.host === pre)) {
        found.push({ host: pre, source: pre.textContent || '' });
      }
    });
    document.querySelectorAll('div.mermaid').forEach((div) => {
      if (div.querySelector('svg')) return;
      found.push({ host: div, source: div.textContent || '' });
    });
    return found;
  };

  const candidates = getCandidates().filter((x) => (x.source || '').trim().length > 0);
  let rendered = 0;
  let failed = 0;
  let idx = 0;

  for (const item of candidates) {
    const source = item.source.trim();
    const host = item.host;
    let target = host;

    if (!(host.tagName === 'DIV' && host.classList.contains('mermaid'))) {
      const div = document.createElement('div');
      div.className = 'mermaid';
      host.replaceWith(div);
      target = div;
    }

    try {
      const id = `md2pdf-mermaid-${Date.now()}-${idx++}`;
      const out = await window.mermaid.render(id, source);
      target.innerHTML = out.svg;
      rendered += 1;
    } catch (err) {
      target.innerHTML = `<pre>${source.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>`;
      failed += 1;
    }
  }

  return { rendered, failed, total: candidates.length, reason: 'ok' };
}
""")
    page.wait_for_timeout(350)
    print(
        f"  Mermaid render: total={result.get('total', 0)}, "
        f"rendered={result.get('rendered', 0)}, failed={result.get('failed', 0)}"
    )


def chrome_print_cdp(html_url: str, pdf_path: str, enable_mermaid: bool = True):
    """Use Playwright CDP for stable HTML-to-PDF rendering."""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        # Navigate and wait for complete load
        page.goto(html_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)  # Extra wait for complex layouts
        if enable_mermaid:
            render_mermaid_if_needed(page)
        
        # Print to PDF
        page.pdf(path=os.path.abspath(pdf_path), format="A4", print_background=True)
        
        page.close()
        browser.close()


def merge_pdfs(cover_path: str, content_path: str, output_path: str):
    from PyPDF2 import PdfMerger
    merger = PdfMerger()
    merger.append(cover_path)
    merger.append(content_path)
    merger.write(output_path)
    merger.close()
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  Merged cover + content → {output_path} ({size_mb:.1f} MB)")


def generate_cover_pdf(title: str, today: str, cover_path: str):
    """Generate cover page using local HTTP server + CDP."""
    import http.server, socketserver, threading, time
    
    cover_html_content = f'''<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 0; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #111827;
  background: #ffffff;
  margin: 0;
  padding: 0;
}}
.cover-title {{
  font-size: 28pt;
  font-weight: 700;
  margin-bottom: 80px;
  line-height: 1.4;
}}
.cover-date {{
  font-size: 14pt;
  color: #6b7280;
  border-top: 2px solid #e5e7eb;
  padding-top: 20px;
  width: 200px;
  line-height: 1.5;
}}
</style></head>
<body>
  <div class="cover-title">{title}</div>
  <div class="cover-date">{today}</div>
</body>
</html>'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(cover_html_content)
        html_path = f.name
    
    tmpdir = os.path.dirname(html_path)
    
    try:
        PORT = 0
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=tmpdir, **kwargs)
        server = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
        assigned_port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        time.sleep(0.5)
        
        url = f"http://127.0.0.1:{assigned_port}/{os.path.basename(html_path)}"
        chrome_print_cdp(url, cover_path)
        server.shutdown()
    finally:
        os.unlink(html_path)


def main():
    parser = argparse.ArgumentParser(description="Markdown to PDF v4.0 - Complete CSS Override")
    parser.add_argument("input", help="Input .md file")
    parser.add_argument("output", help="Output .pdf file")
    parser.add_argument("--toc", action="store_true", help="Include table of contents")
    parser.add_argument("--no-cover", action="store_true", help="Skip cover page generation")
    parser.add_argument("--css", help="Custom CSS file path")
    parser.add_argument("--no-fix-markdown", action="store_true", help="Disable markdown normalization and validation")
    parser.add_argument("--no-mermaid", action="store_true", help="Disable Mermaid rendering before PDF export")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory(prefix="md2pdf_") as tmpdir:
        title = extract_title(args.input)
        # Language-neutral global date format for cover page.
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"Converting: {args.input} → {args.output}")
        print(f"  Title: {title}")
        print(f"  Date: {today}")
        print(f"  Cover: {'disabled' if args.no_cover else 'enabled'}")
        print(f"  Strategy: DELETE Pandoc styles → inject BUILTIN_CSS only")

        # Step 1: Generate cover
        if not args.no_cover:
            cover_pdf = os.path.join(tmpdir, "cover.pdf")
            print(f"[1/3] Generating cover page...")
            generate_cover_pdf(title, today, cover_pdf)

        # Step 2: Normalize markdown (default enabled)
        input_for_pandoc = args.input
        if not args.no_fix_markdown:
            input_for_pandoc, issues = preprocess_markdown(args.input, tmpdir)
            if issues:
                print("  Markdown normalize/validate:")
                for item in issues:
                    print(f"    - {item}")
            else:
                print("  Markdown normalize/validate: no issues detected")
        else:
            print("  Markdown normalize/validate: disabled (--no-fix-markdown)")

        # Step 3: Generate content
        print(f"[2/3] Generating content (Pandoc + CSS override)...")
        html_path = md_to_html(input_for_pandoc, tmpdir, args.toc, args.css)
        
        abs_path = os.path.abspath(html_path).replace(os.sep, '/')
        html_url = f"file:///{abs_path}"
        
        # Serve via HTTP (better for CDP)
        PORT = 0
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=tmpdir, **kwargs)
        server = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
        assigned_port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        time.sleep(0.5)
        filename = os.path.basename(html_path)
        served_url = f"http://127.0.0.1:{assigned_port}/{filename}"
        print(f"  Serving: {served_url}")
        
        content_pdf = os.path.join(tmpdir, "content.pdf")
        chrome_print_cdp(served_url, content_pdf, enable_mermaid=(not args.no_mermaid))
        server.shutdown()

        # Step 4: Merge
        print(f"[3/3] Finalizing...")
        if not args.no_cover:
            merge_pdfs(cover_pdf, content_pdf, args.output)
        else:
            shutil.copy2(content_pdf, args.output)
            size_mb = os.path.getsize(args.output) / (1024 * 1024)
            print(f"  → {args.output} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
