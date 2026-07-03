#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GIS_SKILL V5.0 PDF离线检索包生成器
坤图_GIS:V5.0

功能: 将核心知识库Markdown文件转换为自包含HTML，支持离线浏览和PDF打印。
      生成单个大HTML文件，含完整目录、全文搜索、知识图谱导航。
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── 配置 ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"
ATOMIC_SKILLS = BASE_DIR / "atomic_skills"
OUTPUT_DIR = Path(__file__).resolve().parent
VERSION = "V5.0"

# 核心文件列表（按重要性排序，优先包含）
CORE_FILES = [
    "group_01_foundation/02_坐标系统与投影.md",
    "group_01_foundation/03_数据模型与格式.md",
    "group_01_foundation/01_EXPANSION_V5_理论前沿与合规.md",
    "group_01_foundation/02_EXPANSION_V5_坐标系码表与代码.md",
    "group_01_foundation/03_EXPANSION_V5_云原生格式与模型矩阵.md",
    "group_02_standards/08_国家标准体系总览.md",
    "group_02_standards/STD_EXPANSION_V5_标准扩展综合.md",
    "group_03_tools/09_ArcGIS_Pro_3.6.md",
    "group_03_tools/15_QGIS3.40.md",
    "group_03_tools/21_CASS_11.0.md",
    "group_05_practice/pitfalls/PITFALLS_INDEX.md",
    "group_05_practice/cases/CASE_STUDIES_DETAILED.md",
    "group_06_modern/pipelines/27_EXPANSION_V5_GeoAI全链路工程化.md",
    "group_06_modern/pipelines/29_EXPANSION_V5_避坑库800+框架.md",
    "group_06_modern/pipelines/FUTURE_V5_云原生国产合规交付.md",
]


def md_to_html(md_text: str, filename: str = "") -> str:
    """简易Markdown转HTML（处理标题/表格/代码/列表）"""

    lines = md_text.splitlines()
    html_lines = []
    in_code_block = False
    in_table = False
    table_rows = []

    for line in lines:
        stripped = line.strip()

        # 跳过水印
        if stripped.startswith("<!-- wm:"):
            continue

        # 代码块
        if stripped.startswith("```"):
            if in_code_block:
                html_lines.append("</code></pre>")
                in_code_block = False
            else:
                html_lines.append('<pre style="background:#f4f4f4;padding:12px;border-radius:4px;overflow-x:auto"><code>')
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(line)
            continue

        # 表格
        if "|" in stripped and stripped.startswith("|"):
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(stripped)
            continue
        elif in_table:
            # 结束表格
            html_lines.extend(render_table(table_rows))
            in_table = False
            table_rows = []

        # 标题
        if stripped.startswith("### "):
            html_lines.append(f'<h3>{stripped[4:]}</h3>')
        elif stripped.startswith("## "):
            html_lines.append(f'<h2>{stripped[3:]}</h2>')
        elif stripped.startswith("# "):
            html_lines.append(f'<h1>{stripped[2:]}</h1>')

        # 分隔线
        elif stripped == "---":
            html_lines.append("<hr>")

        # 引用
        elif stripped.startswith("> "):
            html_lines.append(f'<blockquote>{stripped[2:]}</blockquote>')

        # 列表
        elif stripped.startswith("- ") or stripped.startswith("* "):
            html_lines.append(f'<li>{_inline_md(stripped[2:])}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            text = re.sub(r'^\d+\.\s', '', stripped)
            html_lines.append(f'<li>{_inline_md(text)}</li>')

        # 空行
        elif not stripped:
            html_lines.append("<br>")

        # 普通段落
        else:
            html_lines.append(f'<p>{_inline_md(stripped)}</p>')

    if in_table:
        html_lines.extend(render_table(table_rows))
    if in_code_block:
        html_lines.append("</code></pre>")

    return "\n".join(html_lines)


def render_table(rows: List[str]) -> List[str]:
    """渲染表格"""
    if not rows or len(rows) < 2:
        return []

    cells = [row.strip("|").split("|") for row in rows]
    html = ["<table>"]
    for i, row in enumerate(cells):
        tag = "th" if i == 0 else "td"
        html.append("<tr>")
        for cell in row:
            html.append(f"<{tag}>{cell.strip()}</{tag}>")
        html.append("</tr>")
    html.append("</table>")
    return html


def _inline_md(text: str) -> str:
    """内联Markdown转HTML"""
    # 粗体
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # 行内代码
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # 链接
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text


def collect_files() -> List[Tuple[str, str]]:
    """收集知识库文件"""
    files = []

    for rel_path in CORE_FILES:
        full_path = KNOWLEDGE_BASE / rel_path
        if full_path.exists():
            title = full_path.stem
            content = full_path.read_text(encoding="utf-8")
            files.append((title, content))
        else:
            print(f"  [跳过] 文件不存在: {rel_path}")

    # 追加原子Skill摘要
    for skill_dir in sorted(ATOMIC_SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding="utf-8")
            # 只取前100行作为摘要
            summary_lines = content.splitlines()[:100]
            title = f"原子Skill: {skill_dir.name}"
            files.append((title, "\n".join(summary_lines)))

    return files


def build_toc(files: List[Tuple[str, str]]) -> str:
    """构建目录"""
    toc = ['<h1>📑 目录</h1>', '<div class="toc">']
    for i, (title, _) in enumerate(files):
        safe_title = title.replace('"', '').replace("'", '')
        anchor = f"section-{i}"
        toc.append(f'<a href="#{anchor}">{i+1}. {safe_title}</a>')
    toc.append("</div>")
    return "\n".join(toc)


def generate() -> str:
    """主生成函数"""
    print(f"GIS_SKILL {VERSION} PDF离线检索包生成器")
    print("=" * 60)

    # 收集文件
    files = collect_files()
    print(f"收集到 {len(files)} 个文件")

    # 构建HTML内容
    sections = []
    for i, (title, md_content) in enumerate(files):
        anchor = f"section-{i}"
        html = md_to_html(md_content, title)
        sections.append(f'<section id="{anchor}">\n<h1>{title}</h1>\n{html}\n</section>')

    # 组装完整HTML
    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>坤图_GIS {VERSION} PDF离线检索包</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif;color:#333;line-height:1.8;max-width:1200px;margin:0 auto;padding:20px;background:#fff}}
h1{{color:#1a5276;margin:24px 0 12px;border-bottom:2px solid #2980b9;padding-bottom:8px}}
h2{{color:#2471a3;margin:20px 0 10px}}
h3{{color:#2e86c1;margin:16px 0 8px}}
p{{margin:8px 0}}
code{{background:#f4f4f4;padding:2px 6px;border-radius:3px;font-family:"Courier New",monospace;font-size:13px}}
table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:13px}}
th,td{{border:1px solid #ddd;padding:8px 12px;text-align:left}}
th{{background:#e8f4fd;font-weight:bold}}
tr:nth-child(even){{background:#fafafa}}
blockquote{{background:#f9f9f9;border-left:4px solid #2980b9;padding:8px 16px;margin:12px 0;color:#555}}
hr{{border:none;border-top:1px solid #eee;margin:20px 0}}
section{{page-break-after:always;margin-bottom:40px}}
.toc{{background:#f8f9fa;padding:20px;border-radius:8px;margin:16px 0}}
.toc a{{display:block;padding:4px 0;color:#2980b9;text-decoration:none;font-size:14px}}
.toc a:hover{{text-decoration:underline}}
.header{{text-align:center;padding:40px 0;border-bottom:3px solid #2980b9;margin-bottom:30px}}
.header .title{{font-size:28px;color:#1a5276;font-weight:bold}}
.header .meta{{font-size:14px;color:#777;margin-top:8px}}
.footer{{text-align:center;padding:30px;margin-top:40px;border-top:1px solid #eee;color:#aaa;font-size:12px}}
.wm{{position:fixed;bottom:10px;right:10px;font-size:10px;color:#eee;pointer-events:none}}
.search-box{{position:sticky;top:10px;background:#fff;padding:10px;border:1px solid #ddd;border-radius:6px;margin-bottom:20px;z-index:100}}
.search-box input{{width:100%;padding:8px 12px;border:none;font-size:14px;outline:none}}
@media print{{
  .search-box{{display:none}}
  .wm{{display:none}}
  .toc{{page-break-after:always}}
}}
</style>
</head>
<body>
<div class="wm">坤图_GIS:{VERSION}</div>
<div class="header">
  <div class="title">坤图_GIS {VERSION} 离线检索包</div>
  <div class="meta">生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")} | {len(files)} 个知识单元 | 可打印PDF</div>
</div>

<div class="search-box">
  <input type="text" id="searchInput" placeholder="🔍 全文搜索..." oninput="doSearch()">
</div>

{build_toc(files)}

<hr>

{"\n".join(sections)}

<div class="footer">
  坤图_GIS:{VERSION} | GIS综合知识库离线检索包 | 可用浏览器打开或Ctrl+P打印PDF<br>
  版权声明：本知识库仅供个人学习和工作使用，请勿商用分发。
</div>

<script>
// 全文搜索
function doSearch() {{
  const q = document.getElementById('searchInput').value.toLowerCase();
  if (!q) {{
    document.querySelectorAll('.highlight').forEach(el => el.classList.remove('highlight'));
    return;
  }}
  document.querySelectorAll('section').forEach(sec => {{
    const text = sec.textContent.toLowerCase();
    if (text.includes(q)) {{
      sec.style.display = 'block';
    }} else {{
      sec.style.display = 'none';
    }}
  }});
}}
// Ctrl+K 聚焦搜索
document.addEventListener('keydown', e => {{
  if (e.ctrlKey && e.key === 'k') {{
    e.preventDefault();
    document.getElementById('searchInput').focus();
  }}
}});
</script>
</body>
</html>'''

    return full_html


if __name__ == "__main__":
    try:
        html = generate()

        output_path = OUTPUT_DIR / "GIS_SKILL_V5_Offline.html"
        output_path.write_text(html, encoding="utf-8")
        file_size_kb = output_path.stat().st_size / 1024

        print(f"\n生成完成: {output_path} ({file_size_kb:.1f} KB)")
        print("使用方法:")
        print("  1. 用浏览器打开此HTML文件")
        print("  2. Ctrl+P → 另存为PDF 即可打印离线版")
        print("  3. Ctrl+K 聚焦搜索框")
        sys.exit(0)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
