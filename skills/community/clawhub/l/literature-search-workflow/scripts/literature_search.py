#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Literature Search Workflow - 标准化文献搜索工作流
"""

import os
import sys
import io
import json
import requests
from datetime import datetime

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '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')

def tavily_search(query, max_results=10):
    """Tavily 搜索"""
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    data = {
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
        "max_results": max_results
    }
    response = requests.post(url, json=data, headers=headers, timeout=30)
    return response.json()

def analyze_query(query):
    """查询分析"""
    analysis = {
        'type': 'academic_paper',
        'keywords': [],
        'time_range': 'year',
        'field': 'psychology'
    }
    
    # 简单的类型判断
    if '量表' in query or 'scale' in query.lower():
        analysis['type'] = 'scale_search'
    elif '综述' in query or 'review' in query.lower():
        analysis['type'] = 'review'
        analysis['max_results'] = 50
    elif '方法' in query or 'method' in query.lower():
        analysis['type'] = 'methodology'
    
    # 提取关键词
    analysis['keywords'] = query.split()
    
    return analysis

def process_results(results):
    """结果处理：去重、排序"""
    unique_dois = set()
    unique_results = []
    for r in results.get('results', []):
        doi = r.get('doi', r.get('url', ''))
        if doi not in unique_dois:
            unique_dois.add(doi)
            unique_results.append(r)
    return unique_results[:10]

def generate_report(query, results, analysis):
    """生成文献搜索报告"""
    report = []
    report.append(f"# 文献搜索结果报告\n")
    report.append(f"**查询**: {query}")
    report.append(f"**搜索时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**搜索类型**: {analysis['type']}")
    report.append(f"**结果数量**: {len(results)}\n")
    
    if results and results[0].get('answer'):
        report.append(f"## 📝 搜索摘要\n")
        report.append(f"{results[0]['answer']}\n")
    
    report.append(f"## 🔍 关键文献\n")
    for i, r in enumerate(results, 1):
        report.append(f"### {i}. {r.get('title', '无标题')}")
        report.append(f"**URL**: {r.get('url', '')}")
        if r.get('published_date'):
            report.append(f"**日期**: {r.get('published_date')}")
        report.append(f"\n{r.get('content', '')[:200]}...\n")
        report.append("---\n")
    
    return "\n".join(report)

def literature_search_workflow(query, search_type="academic_paper"):
    """标准化文献搜索工作流"""
    print(f"🔍 开始文献搜索：{query}")
    print(f"搜索类型：{search_type}")
    
    # 阶段 1: 查询分析
    print("\n阶段 1: 查询分析...")
    analysis = analyze_query(query)
    
    # 阶段 2: 初步搜索
    print("阶段 2: 初步搜索 (Tavily)...")
    results = tavily_search(query, max_results=analysis.get('max_results', 10))
    
    # 阶段 3: 深度搜索（可选）
    if search_type in ["academic_paper", "review"]:
        print("阶段 3: 深度搜索 (PubMed/BGPT)...")
        # 可以调用 pubmed-database 或 bgpt-paper-search
    
    # 阶段 4: 结果整理
    print("阶段 4: 结果整理...")
    processed = process_results(results)
    
    # 阶段 5: 文献获取（可选）
    if search_type == "scale_search":
        print("阶段 5: 文献获取...")
        # 可以调用 web_fetch 获取全文
    
    # 阶段 6: 输出报告
    print("阶段 6: 输出报告...")
    report = generate_report(query, processed, analysis)
    
    # 保存结果
    filename = f"literature_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 文献搜索完成！")
    print(f"📁 结果已保存：{filename}")
    
    return report

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "主观幸福感量表 validation"
    search_type = sys.argv[2] if len(sys.argv) > 2 else "academic_paper"
    literature_search_workflow(query, search_type)
