#!/usr/bin/env python3
"""
索引生成脚本
功能：为已处理的PDF生成JSON索引
"""

import json
from pathlib import Path
from datetime import datetime
import re

def parse_summary_file(summary_path):
    """解析概述文件，提取关键信息"""
    if not summary_path.exists():
        return None

    content = summary_path.read_text(encoding='utf-8')

    # 提取标题
    title_en = None
    title_zh = None

    title_en_match = re.search(r'\*\*英文\*\*:\s*(.+?)(?:\n|$)', content)
    title_zh_match = re.search(r'\*\*中文\*\*:\s*(.+?)(?:\n|$)', content)

    if title_en_match:
        title_en = title_en_match.group(1).strip()
    if title_zh_match:
        title_zh = title_zh_match.group(1).strip()

    # 提取概述
    summary_match = re.search(r'## 📝 论文概述\s*\n\s*(.+)', content, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else ""

    # 提取源文件名
    source_match = re.search(r'\*\*源文件\*\*:\s*(.+?)\.pdf', content)
    filename = source_match.group(1).strip() + ".pdf" if source_match else summary_path.stem.replace("_概述", ".pdf")

    # 提取处理时间
    time_match = re.search(r'\*\*处理时间\*\*:\s*(.+)', content)
    processed_at = time_match.group(1).strip() if time_match else None

    return {
        "filename": filename,
        "title_en": title_en,
        "title_zh": title_zh,
        "summary": summary,
        "processed_at": processed_at,
        "path": str(summary_path.parent.parent / "原文" / filename)
    }

def parse_summary_folder(summary_dir):
    """解析所有概述文件"""
    papers = []
    summary_files = list(summary_dir.glob("*_概述.txt"))

    for summary_file in sorted(summary_files):
        paper_info = parse_summary_file(summary_file)
        if paper_info:
            papers.append(paper_info)

    return papers

def generate_index(summary_dir, output_path):
    """生成索引文件"""
    print(f"🔍 扫描目录: {summary_dir}")

    # 解析所有论文
    papers = parse_summary_folder(summary_dir)

    if not papers:
        print("⚠️ 未找到任何已处理的论文")
        return

    # 创建索引
    index = {
        "version": "2.0",
        "last_updated": datetime.now().isoformat(),
        "total_papers": len(papers),
        "papers": papers
    }

    # 保存索引
    output_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"✅ 索引生成完成！")
    print(f"📊 总论文数: {len(papers)}")
    print(f"💾 索引文件: {output_path}")

    # 显示摘要统计
    en_count = sum(1 for p in papers if p['title_en'] and p['title_en'])
    zh_count = sum(1 for p in papers if not p['title_en'] or not p['title_en'])
    print(f"📋 英文论文: {en_count} | 中文论文: {zh_count}")

def update_index(base_dir):
    """更新现有索引（增量模式）"""
    summary_dir = base_dir / "已完成" / "概述"
    output_path = base_dir / "索引" / "papers_index.json"

    # 确保目录存在
    summary_dir.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 生成索引
    generate_index(summary_dir, output_path)

def search_index(base_dir, keyword):
    """搜索索引"""
    output_path = base_dir / "索引" / "papers_index.json"

    if not output_path.exists():
        print("❌ 索引文件不存在，请先生成索引")
        return

    index = json.loads(output_path.read_text(encoding='utf-8'))
    keyword = keyword.lower()

    results = []
    for paper in index['papers']:
        title_en = (paper.get('title_en') or '').lower()
        title_zh = (paper.get('title_zh') or '').lower()
        summary = (paper.get('summary') or '').lower()

        if (keyword in title_en or
            keyword in title_zh or
            keyword in summary):
            results.append(paper)

    print(f"\n🔍 搜索关键词: {keyword}")
    print(f"📊 找到 {len(results)} 篇论文:\n")

    for i, paper in enumerate(results, 1):
        print(f"{i}. {paper.get('title_zh', paper.get('filename', 'N/A'))}")
        if paper.get('summary'):
            print(f"   {paper['summary'][:100]}...")
        print()

def main():
    """主函数"""
    import sys

    base_dir = Path.home() / "Documents" / "论文处理"

    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python3 generate_index.py generate  - 生成索引")
        print("  python3 generate_index.py search <关键词>  - 搜索索引")
        return

    command = sys.argv[1]

    if command == "generate":
        update_index(base_dir)
    elif command == "search" and len(sys.argv) > 2:
        keyword = sys.argv[2]
        search_index(base_dir, keyword)
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main()
