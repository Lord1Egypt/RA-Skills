#!/usr/bin/env python3
"""Render a Markdown document to PDF using Playwright."""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


CSS = """
@page { size: A4; margin: 18mm 15mm; }
* { box-sizing: border-box; }
body {
  color: #1f2933;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "Noto Sans CJK SC", "Arial Unicode MS", sans-serif;
  font-size: 12px;
  line-height: 1.68;
}
h1 { font-size: 24px; margin: 0 0 18px; padding-bottom: 10px; border-bottom: 2px solid #111827; }
h2 { font-size: 17px; margin: 24px 0 10px; padding-bottom: 5px; border-bottom: 1px solid #d8dee6; }
h3 { font-size: 14px; margin: 18px 0 8px; }
p { margin: 7px 0; }
ul, ol { margin: 7px 0 7px 20px; padding: 0; }
li { margin: 3px 0; }
table { width: 100%; border-collapse: collapse; margin: 10px 0 16px; table-layout: fixed; }
th, td { border: 1px solid #d8dee6; padding: 7px 8px; vertical-align: top; word-break: break-word; }
th { background: #f3f6f8; font-weight: 700; }
blockquote { margin: 10px 0; padding: 8px 12px; border-left: 4px solid #9aa7b3; background: #f7f9fb; }
code { font-family: "SFMono-Regular", Consolas, monospace; background: #f3f4f6; padding: 1px 4px; border-radius: 4px; }
pre { white-space: pre-wrap; word-break: break-word; background: #f3f4f6; padding: 10px; border-radius: 6px; }
hr { border: 0; border-top: 1px solid #d8dee6; margin: 18px 0; }
"""


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def render_table(lines: list[str], start: int) -> tuple[str, int]:
    header = split_table_row(lines[start])
    rows: list[list[str]] = []
    i = start + 2
    while i < len(lines) and "|" in lines[i].strip() and lines[i].strip().startswith("|"):
        rows.append(split_table_row(lines[i]))
        i += 1
    html_rows = ["<table><thead><tr>"]
    html_rows.extend(f"<th>{inline_markdown(cell)}</th>" for cell in header)
    html_rows.append("</tr></thead><tbody>")
    for row in rows:
        padded = row + [""] * max(0, len(header) - len(row))
        html_rows.append("<tr>")
        html_rows.extend(f"<td>{inline_markdown(cell)}</td>" for cell in padded[: len(header)])
        html_rows.append("</tr>")
    html_rows.append("</tbody></table>")
    return "".join(html_rows), i


def markdown_to_html(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append(f"<p>{inline_markdown(' '.join(paragraph).strip())}</p>")
            paragraph.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                out.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code = False
            else:
                flush_paragraph()
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not stripped:
            flush_paragraph()
            i += 1
            continue

        if i + 1 < len(lines) and "|" in stripped and is_table_separator(lines[i + 1].strip()):
            flush_paragraph()
            table_html, i = render_table(lines, i)
            out.append(table_html)
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = min(len(heading.group(1)), 3)
            out.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            i += 1
            continue

        if re.fullmatch(r"[-*_]{3,}", stripped):
            flush_paragraph()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            quote = stripped.lstrip(">").strip()
            out.append(f"<blockquote>{inline_markdown(quote)}</blockquote>")
            i += 1
            continue

        if re.match(r"^[-*]\s+", stripped):
            flush_paragraph()
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip()))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            flush_paragraph()
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in items) + "</ol>")
            continue

        paragraph.append(stripped)
        i += 1

    flush_paragraph()
    return "\n".join(out)


def find_node(cli_node: str | None) -> str:
    candidates = [
        cli_node,
        os.environ.get("CODEX_NODE"),
        str(Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node"),
        shutil.which("node"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise SystemExit("未找到 Node.js。请通过 --node 指定 Node.js 路径。")


def find_node_modules(cli_node_modules: str | None) -> str | None:
    candidates = [
        cli_node_modules,
        os.environ.get("CODEX_NODE_MODULES"),
        os.environ.get("NODE_REPL_NODE_MODULE_DIRS", "").split(os.pathsep)[0],
        str(Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def render_pdf(html_path: Path, pdf_path: Path, node: str, node_modules: str | None) -> None:
    script = f"""
const path = require('node:path');
const {{ pathToFileURL }} = require('node:url');
const Module = require('node:module');
Module._initPaths();
const {{ chromium }} = require('playwright');

(async () => {{
  const browser = await chromium.launch({{ headless: true }});
  const page = await browser.newPage({{ viewport: {{ width: 1120, height: 1600 }} }});
  await page.goto(pathToFileURL({str(html_path)!r}).href, {{ waitUntil: 'networkidle' }});
  await page.pdf({{
    path: {str(pdf_path)!r},
    format: 'A4',
    printBackground: true,
    margin: {{ top: '18mm', right: '15mm', bottom: '18mm', left: '15mm' }}
  }});
  await browser.close();
}})().catch((error) => {{
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}});
"""
    env = os.environ.copy()
    if node_modules:
        existing = env.get("NODE_PATH", "")
        env["NODE_PATH"] = node_modules if not existing else node_modules + os.pathsep + existing
    with tempfile.NamedTemporaryFile("w", suffix=".cjs", delete=False, encoding="utf-8") as handle:
        handle.write(script)
        script_path = handle.name
    try:
        subprocess.run([node, script_path], check=True, env=env)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(
            "PDF 渲染失败。请确认 Node.js 环境中可用 playwright，或通过 --node-modules 指定包含 playwright 的 node_modules。"
        ) from exc
    finally:
        Path(script_path).unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="将 Markdown 渲染为适合评审的 A4 PDF。")
    parser.add_argument("input", type=Path, help="输入 Markdown 文件")
    parser.add_argument("output", type=Path, help="输出 PDF 文件")
    parser.add_argument("--title", default=None, help="HTML/PDF 标题")
    parser.add_argument("--keep-html", action="store_true", help="保留中间 HTML 文件")
    parser.add_argument("--node", default=None, help="Node.js 可执行文件路径")
    parser.add_argument("--node-modules", default=None, help="包含 playwright 的 node_modules 路径")
    args = parser.parse_args()

    markdown_path = args.input.resolve()
    pdf_path = args.output.resolve()
    if not markdown_path.exists():
        raise SystemExit(f"输入文件不存在：{markdown_path}")

    title = args.title or markdown_path.stem
    body = markdown_to_html(markdown_path.read_text(encoding="utf-8"))
    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""
    html_path = pdf_path.with_suffix(".html") if args.keep_html else Path(tempfile.mkstemp(suffix=".html")[1])
    html_path.write_text(html_doc, encoding="utf-8")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        render_pdf(html_path, pdf_path, find_node(args.node), find_node_modules(args.node_modules))
    finally:
        if not args.keep_html:
            html_path.unlink(missing_ok=True)

    print(str(pdf_path))


if __name__ == "__main__":
    main()
