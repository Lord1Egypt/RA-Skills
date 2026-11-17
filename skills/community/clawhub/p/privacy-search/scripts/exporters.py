#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索结果导出

V1.5 新增。将搜索结果保存为 Markdown / HTML / PDF。

PDF 导出采用降级方案：
    1. weasyprint（HTML→PDF，纯 Python）
    2. 不装时提示用户先导出 HTML 再用浏览器打印

遵循死规则 9：基础功能自研，外部依赖按需接入，必须提供降级方案。
"""

import html
import os
import sys
from typing import Any, Dict, List, Optional

sys.dont_write_bytecode = True


def export_markdown(results: List[Any], path: str, query: str = "") -> bool:
    """
    导出为 Markdown

    纯标准库实现，不依赖第三方。
    """
    try:
        lines = []
        lines.append("# 搜索结果：%s" % query if query else "# 搜索结果")
        lines.append("")
        lines.append("> 导出时间：%s" % __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        lines.append("")

        for i, r in enumerate(results, 1):
            title = getattr(r, "title", "") or "无标题"
            url = getattr(r, "url", "") or ""
            snippet = getattr(r, "snippet", "") or ""
            engine = getattr(r, "engine", "") or getattr(r, "engines", "")
            rank = getattr(r, "rank", 0)

            lines.append("## %d. %s" % (i, title))
            lines.append("")
            if url:
                lines.append("- **链接**：[%s](%s)" % (url, url))
            if engine:
                if isinstance(engine, (list, tuple)):
                    engine = ", ".join(engine)
                lines.append("- **引擎**：%s" % engine)
            if rank:
                lines.append("- **排名**：%d" % rank)
            lines.append("")
            if snippet:
                lines.append(snippet)
                lines.append("")

        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return True
    except Exception:
        return False


def export_html(results: List[Any], path: str, query: str = "") -> bool:
    """
    导出为 HTML（带基本样式，浏览器直接打开）
    """
    try:
        rows = []
        for i, r in enumerate(results, 1):
            title = html.escape(getattr(r, "title", "") or "无标题")
            url = html.escape(getattr(r, "url", "") or "")
            snippet = html.escape(getattr(r, "snippet", "") or "")
            engine = getattr(r, "engine", "") or getattr(r, "engines", "")
            if isinstance(engine, (list, tuple)):
                engine = ", ".join(engine)
            engine = html.escape(engine)
            rank = getattr(r, "rank", 0)

            rows.append(
                '<tr><td>%d</td><td><a href="%s" target="_blank">%s</a></td>'
                '<td>%s</td><td>%s</td><td>%d</td></tr>'
                % (i, url, title, snippet, engine, rank)
            )

        content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>搜索结果：{query}</title>
<style>
body {{ font-family: sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
h1 {{ color: #333; }}
.meta {{ color: #666; margin-bottom: 20px; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
th {{ background: #f5f5f5; }}
tr:nth-child(even) {{ background: #fafafa; }}
a {{ color: #1a73e8; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<h1>搜索结果</h1>
<p class="meta">关键词：{query} | 共 {count} 条 | 导出时间：{time}</p>
<table>
<thead><tr><th>#</th><th>标题</th><th>摘要</th><th>引擎</th><th>排名</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</body>
</html>'''.format(
            query=html.escape(query),
            count=len(results),
            time=__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            rows="\n".join(rows),
        )

        parent = os.path.dirname(os.path.abspath(path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception:  # noqa: BLE001 - 导出为可选功能
        return False


def export_pdf(results: List[Any], path: str, query: str = "") -> bool:
    """
    导出为 PDF

    主方案：weasyprint（HTML→PDF，纯 Python）
    降级：提示用户先导出 HTML 再用浏览器打印
    """
    try:
        import weasyprint
    except ImportError:
        print("[提示] PDF 导出需要 weasyprint，未安装")
        print("  请先导出 HTML，再用浏览器打印为 PDF")
        print("  或运行：pip install weasyprint")
        return False

    try:
        # 先生成 HTML，再转 PDF
        html_content = _generate_html_string(results, query)
        weasyprint.HTML(string=html_content).write_pdf(path)
        return True
    except Exception:
        return False


def _generate_html_string(results: List[Any], query: str) -> str:
    """生成 HTML 字符串（内部用）"""
    rows = []
    for i, r in enumerate(results, 1):
        title = html.escape(getattr(r, "title", "") or "无标题")
        url = html.escape(getattr(r, "url", "") or "")
        snippet = html.escape(getattr(r, "snippet", "") or "")
        engine = getattr(r, "engine", "") or getattr(r, "engines", "")
        if isinstance(engine, (list, tuple)):
            engine = ", ".join(engine)
        engine = html.escape(engine)
        rank = getattr(r, "rank", 0)

        rows.append(
            '<tr><td>%d</td><td><a href="%s">%s</a></td><td>%s</td><td>%s</td><td>%d</td></tr>'
            % (i, url, title, snippet, engine, rank)
        )

    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>搜索结果</title>
<style>
body { font-family: sans-serif; padding: 20px; }
h1 { color: #333; }
.meta { color: #666; margin-bottom: 20px; }
table { width: 100%; border-collapse: collapse; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 12px; }
th { background: #f5f5f5; }
a { color: #1a73e8; text-decoration: none; }
</style>
</head>
<body>
<h1>搜索结果：{query}</h1>
<p class="meta">共 {count} 条 | 导出时间：{time}</p>
<table>
<thead><tr><th>#</th><th>标题</th><th>摘要</th><th>引擎</th><th>排名</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</body>
</html>'''.format(
        query=html.escape(query),
        count=len(results),
        time=__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        rows="\n".join(rows),
    )


def auto_export(results: List[Any], path: str, query: str = "") -> bool:
    """
    按文件扩展名自动选择导出格式

    支持 .md / .html / .pdf
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == ".md":
        return export_markdown(results, path, query)
    elif ext == ".html":
        return export_html(results, path, query)
    elif ext == ".pdf":
        return export_pdf(results, path, query)
    else:
        print("[错误] 不支持的格式：%s（支持 .md / .html / .pdf）" % ext)
        return False
