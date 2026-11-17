#!/usr/bin/env python3
"""
exporter.py — Infoseek 多平台导出器（v1.8.0）

将调研报告导出为多种格式：
  - md (Markdown)
  - json (JSON)
  - csv (CSV, 锚点列表)
  - claude (Claude SKILL.md 格式)
  - openai (OpenAI Plugin manifest 格式)
  - lobehub (LobeHub Skill 格式)

CLI 用法:
  python exporter.py md < report.json > out.md
  python exporter.py lobehub --name "tech-research" < report.json > skill.yaml
"""

import sys
import json
import re
import yaml
from pathlib import Path
from typing import Optional


def to_markdown(report: dict) -> str:
    """导出为 Markdown 报告"""
    lines = [f"# {report.get('subject', '调研报告')}\n"]

    lines.append(f"\n> 调研模式：**{report.get('domain', '通用')}**\n")
    lines.append(f"> 生成时间：{report.get('generated_at', '')}\n\n")

    # 摘要
    if report.get('summary'):
        lines.append("## 摘要\n")
        lines.append(report['summary'] + "\n\n")

    # 锚点列表
    lines.append("## 锚点列表\n")
    anchors = report.get('anchors', [])
    for i, a in enumerate(anchors, 1):
        score = a.get('score', 0)
        marker = "🥇" if score >= 70 else "🥈" if score >= 40 else "🥉"
        lines.append(f"### {marker} [{i}] {a.get('title', 'Untitled')} — {score}\n")
        lines.append(f"- **来源**：{a.get('platform', '')}")
        lines.append(f"- **链接**：{a.get('url', '')}")
        if a.get('credibility'):
            lines.append(f"- **可信度**：{a['credibility']}/100")
        if a.get('snippet'):
            lines.append(f"\n> {a['snippet'][:300]}{'...' if len(a.get('snippet', '')) > 300 else ''}\n")

    # 来源溯源
    if report.get('citation_graph'):
        lines.append("\n## 来源溯源图\n")
        lines.append("```dot")
        lines.append(report['citation_graph'])
        lines.append("```\n")

    return "\n".join(lines)


def to_json(report: dict, indent: int = 2) -> str:
    """导出为 JSON"""
    return json.dumps(report, ensure_ascii=False, indent=indent)


def _csv_safe(value):
    """DEF-14（v2.1.1 P2）：CSV 公式注入防护。

    电子表格把 =、+、-、@、Tab、CR 开头的单元格当公式执行（=HYPERLINK/=cmd|...），
    即使 QUOTE_ALL 包裹也会触发。首字符命中时前置单引号强制文本；数值型不处理。
    """
    if value is None:
        return ''
    if isinstance(value, (int, float)):
        return value
    text = str(value)
    if text and text[0] in ('=', '+', '-', '@', '\t', '\r'):
        return "'" + text
    return text


def to_csv(report: dict) -> str:
    """导出为 CSV（锚点列表）"""
    import csv
    import io

    buffer = io.StringIO()
    fieldnames = ['idx', 'title', 'url', 'platform', 'score', 'credibility', 'domain']
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    anchors = report.get('anchors', [])
    for i, a in enumerate(anchors, 1):
        writer.writerow({
            'idx': i,
            'title': _csv_safe((a.get('title', '') or '')[:80]),
            'url': _csv_safe(a.get('url', '')),
            'platform': _csv_safe(a.get('platform', '')),
            'score': a.get('score', 0),
            'credibility': a.get('credibility', 0),
            'domain': _csv_safe(report.get('domain', '')),
        })

    return buffer.getvalue()


def to_claude_skill(report: dict) -> str:
    """导出为 Claude SKILL.md 格式"""
    subject = report.get('subject', 'Untitled')
    description = report.get('summary', '')[:300]

    lines = [
        "---",
        f"name: {_slugify(subject)}",
        "version: 1.0.0",
        f"description: {description}。调研模式：{report.get('domain', '通用')}。",
        "",
        "license: MIT",
        "---",
        "",
        f"# {subject} (Claude Skill)",
        "",
        "> 自动生成自 Infoseek v1.8.0 多平台导出器。",
        "",
    ]

    # 来源索引
    lines.append("## 来源索引\n")
    for i, a in enumerate(report.get('anchors', []), 1):
        lines.append(f"- [{a.get('title', 'Untitled')[:60]}]({a.get('url', '')}) — {a.get('platform', '')} / 评分 {a.get('score', 0)}")

    return "\n".join(lines)


def to_openai_plugin(report: dict) -> str:
    """导出为 OpenAI Plugin manifest 格式"""
    subject = report.get('subject', 'Untitled')
    description = (report.get('summary', '')[:100] + '...') if report.get('summary') else "Infoseek generated research report"

    manifest = {
        "schema_version": "v1",
        "name_for_model": _slugify(subject),
        "name_for_human": subject,
        "description_for_model": description,
        "description_for_human": description,
        "auth": {"type": "none"},
        "api": {
            "type": "infoseek",
            "url": "https://infoseek.example.com/api",
            "has_user_authentication": False,
        },
        "logo_url": "",
        "contact_email": "",
        "legal_info_url": "",
    }
    return json.dumps(manifest, ensure_ascii=False, indent=2)


def to_traced_markdown(report: dict) -> str:
    """导出为带引用图的 Markdown 报告（v1.9.0 新增）

    与 to_markdown 区别：
      1. 顶部加引用图（DOT 代码块）
      2. 锚点列表每项加 via_refs 标记
      3. 末尾加"引用图谱"章节
    """
    md = to_markdown(report)

    # 1. 顶部插入引用图
    citation_graph = report.get('citation_graph', '')
    if citation_graph:
        graph_section = (
            "\n## 引用溯源图\n\n"
            "```dot\n"
            f"{citation_graph}\n"
            "```\n"
            "\n---\n"
        )
        # 插入到第一个 ## 章节之前
        if '## ' in md:
            first_h2 = md.find('## ')
            md = md[:first_h2] + graph_section + md[first_h2:]
        else:
            md = graph_section + md

    # 2. 锚点列表加 via 标签
    anchors = report.get('anchors', [])
    for i, anchor in enumerate(anchors, 1):
        ref_id = anchor.get('ref_id', i)
        via_refs = anchor.get('via_refs', [])
        marker = f"[{i}]"
        if marker in md and via_refs:
            replacement = f"[{i}] (via ref:{ref_id} | {', '.join(str(r) for r in via_refs[:3])})"
            md = md.replace(marker, replacement, 1)

    return md


def to_traced_csv(report: dict) -> str:
    """导出为带引用追溯的 CSV（v1.9.0 新增）

    比 to_csv 多 ref_id 和 via_refs 字段
    """
    import csv
    import io

    buffer = io.StringIO()
    fieldnames = ['idx', 'ref_id', 'title', 'url', 'platform', 'score', 'credibility', 'via_refs', 'domain']
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    anchors = report.get('anchors', [])
    for i, a in enumerate(anchors, 1):
        writer.writerow({
            'idx': i,
            'ref_id': a.get('ref_id', i),
            'title': _csv_safe((a.get('title', '') or '')[:80]),
            'url': _csv_safe(a.get('url', '')),
            'platform': _csv_safe(a.get('platform', '')),
            'score': a.get('score', 0),
            'credibility': a.get('credibility', 0),
            'via_refs': _csv_safe('|'.join(str(r) for r in a.get('via_refs', []))),
            'domain': _csv_safe(report.get('domain', '')),
        })

    return buffer.getvalue()


def to_lobehub_skill(report: dict) -> str:
    """导出为 LobeHub Skill manifest 格式"""
    subject = report.get('subject', 'Untitled')
    domain = report.get('domain', 'general')
    description = (report.get('summary', '')[:200] + '...') if report.get('summary') else "Infoseek 调研报告"

    return yaml.dump({
        'name': _slugify(subject),
        'displayName': subject,
        'description': description,
        'tags': [domain, 'research', 'infoseek'],
        'version': '1.0.0',
        'author': 'Infoseek Team',
        'homepage': 'https://github.com/infoseek/infoseek',
        'config': {
            'domain': domain,
            'anchors_count': len(report.get('anchors', [])),
            'sources': [{
                'title': a.get('title', '')[:60],
                'url': a.get('url', ''),
                'platform': a.get('platform', ''),
                'score': a.get('score', 0),
            } for a in report.get('anchors', [])[:10]],
        },
    }, allow_unicode=True, sort_keys=False, default_flow_style=False)


def _slugify(s: str) -> str:
    """字符串转 slug（用于文件名/SKILL 名）"""
    s = re.sub(r'[^\w\s-]', '', s.lower())
    s = re.sub(r'[\s_-]+', '-', s).strip('-')
    return s or 'untitled'


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════

FORMATTERS = {
    'md': to_markdown,
    'json': to_json,
    'csv': to_csv,
    'claude': to_claude_skill,
    'openai': to_openai_plugin,
    'lobehub': to_lobehub_skill,
    # v1.9.0 新增：traced 系列（带引用图）
    'traced_md': to_traced_markdown,
    'traced_csv': to_traced_csv,
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python exporter.py <format> [--in path] [--out path]")
        print(f"  Formats: {', '.join(FORMATTERS.keys())}")
        sys.exit(1)

    fmt = sys.argv[1]

    # 解析参数
    args = sys.argv[2:]
    in_path = None
    out_path = None
    i = 0
    while i < len(args):
        if args[i] == '--in' and i + 1 < len(args):
            in_path = args[i + 1]
            i += 2
        elif args[i] == '--out' and i + 1 < len(args):
            out_path = args[i + 1]
            i += 2
        else:
            i += 1

    if fmt not in FORMATTERS:
        print(f"❌ Unknown format: {fmt}")
        print(f"Available: {', '.join(FORMATTERS.keys())}")
        sys.exit(1)

    # 读取输入
    if in_path:
        with open(in_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
    else:
        report = json.load(sys.stdin)

    # 转换
    output = FORMATTERS[fmt](report)

    # 输出
    if out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ Exported to {out_path} ({len(output)} chars)")
    else:
        print(output)


if __name__ == '__main__':
    main()
