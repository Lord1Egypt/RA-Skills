#!/usr/bin/env python3
"""
合并 LinkFox Agent 输出的多份 HTML 报告为一个完整报告。
支持自动检测报告标题、排序、生成带侧边导航的单页报告。

用法:
  python3 merge_html.py <input_dir> [--output merged_report.html] [--keyword "Portable Blender"]
  python3 merge_html.py part01.html part02.html part03.html [--output merged.html]
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Part 编号映射（用于排序）
PART_ORDER = {
    "市场概况": 1, "搜索趋势": 1, "市场规模": 1,
    "关键词": 2,
    "BSR": 3, "销售分析": 3, "竞争格局": 3, "竞品": 3,
    "卖家分析": 4, "卖家": 4, "上架": 4,
    "消费者": 5, "评论": 5, "好评": 5, "痛点": 5,
    "可行性": 6,
    "风险": 7, "利润": 7,
    "专利": 8, "综合建议": 8,
}


def extract_title(html: str) -> str:
    """从 HTML 中提取 h1 标题"""
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    return m.group(1).strip() if m else "未知报告"


def extract_subtitle(html: str) -> str:
    """从 HTML 中提取 h2 副标题"""
    m = re.search(r'<h2[^>]*>([^<]+)</h2>', html)
    return m.group(1).strip() if m else ""


def extract_body(html: str) -> str:
    """提取 <body> 内容，去掉外层 html/head/body 标签"""
    # 找 body 内容
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL)
    if m:
        return m.group(1).strip()
    return html


def extract_styles(html: str) -> str:
    """提取 <style> 块"""
    styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    return "\n".join(styles)


def extract_scripts(html: str) -> str:
    """提取内联 <script> 块（不含外部引用）"""
    scripts = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', html, re.DOTALL)
    return "\n".join(s for s in scripts if s.strip())


def guess_part_order(title: str) -> int:
    """根据标题猜测排序"""
    for keyword, order in PART_ORDER.items():
        if keyword in title:
            return order
    return 99


def collect_reports(inputs: list) -> list:
    """收集所有 HTML 文件"""
    files = []
    for inp in inputs:
        p = Path(inp)
        if p.is_dir():
            files.extend(sorted(p.glob("*.html")))
        elif p.is_file() and p.suffix == ".html":
            files.append(p)
    return files


def merge(files: list, keyword: str = "") -> str:
    """合并多个 HTML 报告为一个带导航的单页报告"""
    reports = []
    all_styles = set()
    all_scripts = []
    external_css = set()
    external_js = set()

    for f in files:
        html = f.read_text(encoding="utf-8")
        title = extract_title(html)
        subtitle = extract_subtitle(html)
        body = extract_body(html)
        style = extract_styles(html)
        script = extract_scripts(html)
        order = guess_part_order(title)

        # 收集外部 CSS/JS 引用
        for m in re.finditer(r'<link[^>]+href="([^"]+)"[^>]*stylesheet', html):
            external_css.add(m.group(1))
        for m in re.finditer(r'<script[^>]+src="([^"]+)"', html):
            external_js.add(m.group(1))

        if style:
            all_styles.add(style)
        if script:
            all_scripts.append(f"// === {title} ===\n{script}")

        reports.append({
            "file": f.name,
            "title": title,
            "subtitle": subtitle,
            "body": body,
            "order": order,
        })

    # 排序
    reports.sort(key=lambda r: (r["order"], r["file"]))

    # 生成报告标题
    report_title = keyword if keyword else "市场调研综合报告"

    # 生成导航和内容
    nav_items = []
    content_sections = []
    for i, r in enumerate(reports):
        section_id = f"section-{i}"
        short_title = r["title"]
        if len(short_title) > 25:
            short_title = short_title[:22] + "..."
        nav_items.append(
            f'<a href="#{section_id}" class="nav-item" onclick="scrollToSection(\'{section_id}\')">'
            f'<span class="nav-num">{i+1}</span>{short_title}</a>'
        )
        content_sections.append(
            f'<section id="{section_id}" class="report-section">'
            f'<div class="section-divider"><span>Part {i+1:02d}</span></div>'
            f'{r["body"]}'
            f'</section>'
        )

    css_links = "\n".join(f'<link href="{url}" rel="stylesheet">' for url in sorted(external_css))
    js_links = "\n".join(f'<script src="{url}"></script>' for url in sorted(external_js))
    merged_styles = "\n".join(all_styles)
    merged_scripts = "\n".join(all_scripts)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title}</title>
    <link rel="icon" href="https://agent-files.linkfox.com/example/public/favicon.ico">
    {css_links}
    <style>
        {merged_styles}

        /* === 合并报告导航样式 === */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ display: flex; min-height: 100vh; font-family: 'Noto Sans SC', sans-serif; background: #f5f5f5; }}

        .sidebar {{
            width: 280px; min-width: 280px;
            background: #1a1a2e; color: #fff;
            padding: 20px 0; position: fixed;
            top: 0; left: 0; bottom: 0;
            overflow-y: auto; z-index: 100;
            transition: transform 0.3s;
        }}
        .sidebar-title {{
            padding: 16px 24px 24px;
            font-size: 18px; font-weight: 700;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 8px;
        }}
        .sidebar-subtitle {{ font-size: 12px; opacity: 0.6; margin-top: 4px; font-weight: 400; }}
        .nav-item {{
            display: flex; align-items: center; gap: 10px;
            padding: 10px 24px; color: rgba(255,255,255,0.7);
            text-decoration: none; font-size: 13px;
            transition: all 0.2s; border-left: 3px solid transparent;
        }}
        .nav-item:hover {{ background: rgba(255,255,255,0.08); color: #fff; }}
        .nav-item.active {{ background: rgba(255,255,255,0.12); color: #fff; border-left-color: #4ade80; }}
        .nav-num {{
            background: rgba(255,255,255,0.15); border-radius: 4px;
            width: 24px; height: 24px; display: flex;
            align-items: center; justify-content: center;
            font-size: 11px; font-weight: 600; flex-shrink: 0;
        }}

        .main-content {{ margin-left: 280px; flex: 1; padding: 0; }}
        .report-section {{ background: #fff; margin: 24px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }}
        .section-divider {{
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #fff; padding: 12px 24px; font-size: 14px; font-weight: 600;
        }}
        .section-divider span {{ background: rgba(74,222,128,0.2); padding: 4px 12px; border-radius: 4px; }}

        /* 移动端 */
        .menu-toggle {{
            display: none; position: fixed; top: 12px; left: 12px; z-index: 200;
            background: #1a1a2e; color: #fff; border: none; border-radius: 8px;
            padding: 8px 12px; font-size: 18px; cursor: pointer;
        }}
        @media (max-width: 768px) {{
            .sidebar {{ transform: translateX(-100%); }}
            .sidebar.open {{ transform: translateX(0); }}
            .main-content {{ margin-left: 0; }}
            .menu-toggle {{ display: block; }}
            .report-section {{ margin: 12px; }}
        }}

        /* 报告内部样式覆盖 */
        .report-section .report-title {{ padding: 20px 24px 0; }}
        .report-section > div {{ padding: 0 24px 24px; }}
    </style>
</head>
<body>
    <button class="menu-toggle" onclick="document.querySelector('.sidebar').classList.toggle('open')">☰</button>

    <nav class="sidebar">
        <div class="sidebar-title">
            📊 {report_title}
            <div class="sidebar-subtitle">{len(reports)} 份报告 · LinkFox Agent</div>
        </div>
        {"".join(nav_items)}
    </nav>

    <main class="main-content">
        {"".join(content_sections)}
    </main>

    {js_links}
    <script>
        {merged_scripts}

        // 导航高亮 + 滚动
        function scrollToSection(id) {{
            document.getElementById(id).scrollIntoView({{ behavior: 'smooth' }});
            document.querySelector('.sidebar').classList.remove('open');
        }}

        // 滚动监听高亮
        const sections = document.querySelectorAll('.report-section');
        const navItems = document.querySelectorAll('.nav-item');
        window.addEventListener('scroll', () => {{
            let current = 0;
            sections.forEach((s, i) => {{
                if (window.scrollY >= s.offsetTop - 200) current = i;
            }});
            navItems.forEach((n, i) => n.classList.toggle('active', i === current));
        }});
    </script>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description="合并 LinkFox Agent HTML 报告")
    parser.add_argument("inputs", nargs="+", help="HTML 文件或包含 HTML 的目录")
    parser.add_argument("--output", "-o", default="merged_report.html", help="输出文件名")
    parser.add_argument("--keyword", "-k", default="", help="产品关键词（用作报告标题）")
    args = parser.parse_args()

    files = collect_reports(args.inputs)
    if not files:
        print("❌ 未找到 HTML 文件", file=sys.stderr)
        sys.exit(1)

    print(f"📂 找到 {len(files)} 个 HTML 文件:")
    for f in files:
        print(f"   • {f.name}")

    result = merge(files, args.keyword)

    output_path = Path(args.output)
    output_path.write_text(result, encoding="utf-8")
    print(f"\n✅ 合并完成 → {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
