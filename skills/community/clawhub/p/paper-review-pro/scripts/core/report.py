#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
论文检索报告生成模块

生成全面的论文检索总结报告，包括：
- 检索基本信息（时间、主题、数量）
- 核心论文列表（标题、作者、年份、摘要、链接）
- 扩展检索词列表
- 扩展检索结果列表
- 整体主题领域研究分析
- 扩展领域分析
- 高价值研究问题建议
- 后续研究建议
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any


def load_paper_summary(path: str) -> Dict[str, str]:
    """从 markdown 文件加载论文摘要"""
    if not os.path.exists(path):
        return {}
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    summary = {}
    current_key = None
    current_value = []
    
    for line in content.split('\n'):
        if line.startswith('### '):
            if current_key:
                summary[current_key] = '\n'.join(current_value).strip()
            current_key = line.replace('### ', '').strip()
            current_value = []
        elif current_key and line.strip():
            current_value.append(line.strip())
    
    if current_key:
        summary[current_key] = '\n'.join(current_value).strip()
    
    return summary


def generate_report(
    query: str,
    saved_topk: List[Dict[str, Any]],
    saved_expanded: List[Dict[str, Any]],
    expansions: List[Dict[str, Any]],
    config: Dict[str, Any],
    use_authority: bool = True
) -> str:
    """生成完整的论文检索报告"""
    
    now = datetime.now()
    report_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # 加载核心论文摘要
    core_papers = []
    for paper in saved_topk:
        summary = load_paper_summary(paper.get('path', ''))
        pub_info = ""
        if paper.get("ccf_rank"):
            pub_info = f" [CCF-{paper['ccf_rank']}]"
        elif paper.get("publication"):
            pub_info = f" [{paper['publication']}]"
        elif paper.get("is_preprint"):
            pub_info = " [preprint]"
        
        core_papers.append({
            'title': paper.get('title', ''),
            'authors': paper.get('authors', []),
            'year': paper.get('year', ''),
            'url': paper.get('url', ''),
            'publication': pub_info,
            'summary': summary,
            'similarity': paper.get('sim_combined', paper.get('sim', 0))
        })
    
    # 加载扩展论文摘要
    expanded_papers = []
    for paper in saved_expanded:
        summary = load_paper_summary(paper.get('path', ''))
        expanded_papers.append({
            'title': paper.get('title', ''),
            'authors': paper.get('authors', []),
            'year': paper.get('year', ''),
            'url': paper.get('url', ''),
            'expansion_term': paper.get('expansion_term', ''),
            'summary': summary
        })
    
    # 生成报告
    report = []
    report.append("=" * 80)
    report.append("论文检索总结报告")
    report.append("=" * 80)
    report.append("")
    report.append(f"检索时间：{report_time}")
    report.append(f"检索主题：{query}")
    report.append(f"检索数量：{len(saved_topk) + len(saved_expanded)} 篇")
    report.append(f"核心论文：{len(saved_topk)} 篇")
    report.append(f"扩展论文：{len(saved_expanded)} 篇")
    report.append("")
    
    # 核心论文列表
    report.append("-" * 80)
    report.append("核心论文列表")
    report.append("-" * 80)
    for i, paper in enumerate(core_papers, 1):
        report.append(f"\n{i}. {paper['title']}{paper['publication']}")
        report.append(f"   作者：{', '.join(paper['authors'])}")
        report.append(f"   年份：{paper['year']}")
        report.append(f"   链接：{paper['url']}")
        report.append(f"   相关度：{paper['similarity']:.3f}")
        if paper['summary']:
            report.append(f"   研究问题：{paper['summary'].get('研究问题', 'N/A')}")
            report.append(f"   方法：{paper['summary'].get('方法', 'N/A')}")
            report.append(f"   结论：{paper['summary'].get('结论', 'N/A')}")
            report.append(f"   创新点：{paper['summary'].get('创新点', 'N/A')}")
    
    report.append("")
    
    # 扩展检索词
    report.append("-" * 80)
    report.append("扩展检索词")
    report.append("-" * 80)
    for exp in expansions:
        report.append(f"- {exp['term']} (score={exp['score']:.2f})")
    report.append("")
    
    # 扩展检索结果
    report.append("-" * 80)
    report.append("扩展检索结果")
    report.append("-" * 80)
    for i, paper in enumerate(expanded_papers, 1):
        report.append(f"\n{i}. [{paper['expansion_term']}] {paper['title']}")
        report.append(f"   作者：{', '.join(paper['authors'])}")
        report.append(f"   年份：{paper['year']}")
        report.append(f"   链接：{paper['url']}")
        if paper['summary']:
            report.append(f"   研究问题：{paper['summary'].get('研究问题', 'N/A')}")
            report.append(f"   方法：{paper['summary'].get('方法', 'N/A')}")
    
    report.append("")
    
    # 整体主题领域分析
    report.append("-" * 80)
    report.append("整体主题领域研究分析")
    report.append("-" * 80)
    report.append("")
    report.append("基于核心论文的分析：")
    report.append("")
    
    # 提取研究问题、方法、结论、创新点的共性
    research_questions = [p['summary'].get('研究问题', '') for p in core_papers if p['summary'].get('研究问题')]
    methods = [p['summary'].get('方法', '') for p in core_papers if p['summary'].get('方法')]
    conclusions = [p['summary'].get('结论', '') for p in core_papers if p['summary'].get('结论')]
    innovations = [p['summary'].get('创新点', '') for p in core_papers if p['summary'].get('创新点')]
    
    report.append("主要研究方向：")
    if research_questions:
        report.append(f"  - 研究问题聚焦：{research_questions[0][:100]}...")
    if methods:
        report.append(f"  - 常用方法：{methods[0][:100]}...")
    if conclusions:
        report.append(f"  - 主要结论：{conclusions[0][:100]}...")
    if innovations:
        report.append(f"  - 创新方向：{innovations[0][:100]}...")
    
    report.append("")
    
    # 扩展领域分析
    report.append("-" * 80)
    report.append("扩展领域分析")
    report.append("-" * 80)
    report.append("")
    report.append("基于扩展检索结果的分析（侧重可扩展性）：")
    report.append("")
    
    exp_terms = set(p['expansion_term'] for p in expanded_papers)
    for term in exp_terms:
        term_papers = [p for p in expanded_papers if p['expansion_term'] == term]
        report.append(f"扩展方向 [{term}]:")
        if term_papers:
            report.append(f"  - 相关论文：{len(term_papers)} 篇")
            if term_papers[0]['summary']:
                report.append(f"  - 研究问题：{term_papers[0]['summary'].get('研究问题', 'N/A')[:100]}...")
    
    report.append("")
    
    # 高价值研究建议
    report.append("-" * 80)
    report.append("高价值研究问题与建议")
    report.append("-" * 80)
    report.append("")
    report.append("基于核心论文和扩展检索结果的分析，提出以下建议：")
    report.append("")
    report.append("潜在研究问题：")
    report.append("  1. 结合核心论文的研究方向，探索尚未充分研究的问题")
    report.append("  2. 将扩展领域的方法应用到核心领域")
    report.append("  3. 跨领域融合创新")
    report.append("")
    report.append("方法建议：")
    report.append("  - 采用核心论文中验证有效的方法论")
    report.append("  - 借鉴扩展领域的技术手段")
    report.append("")
    report.append("后续研究建议：")
    report.append("  1. 深入阅读核心论文的完整内容")
    report.append("  2. 关注相关领域的最新进展")
    report.append("  3. 设计实验验证创新想法")
    report.append("  4. 与领域专家讨论研究方向")
    report.append("")
    report.append("=" * 80)
    report.append("报告结束")
    report.append("=" * 80)
    
    return '\n'.join(report)


def save_report(report: str, query: str, config: Dict[str, Any]) -> str:
    """保存报告到文件"""
    reports_dir = os.path.expanduser("~/.openclaw/paper-review-pro/reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = query.replace(" ", "_").replace("/", "_")[:50]
    filename = f"report_{safe_query}_{timestamp}.md"
    path = os.path.join(reports_dir, filename)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return path