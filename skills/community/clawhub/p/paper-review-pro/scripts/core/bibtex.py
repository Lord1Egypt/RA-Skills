#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BibTeX 导出模块

功能：
- 将论文信息转换为 BibTeX 格式
- 支持批量导出到 .bib 文件
- 方便一键导入 Zotero 等文献管理工具
"""

import os
import re
from datetime import datetime


def _sanitize_bibtex_key(title: str, year: str, authors: list) -> str:
    """
    生成 BibTeX 引用键（citation key）
    
    格式：作者姓氏 + 年份 + 标题关键词
    例如：Zhang2025LLMReasoning
    """
    # 获取第一作者的姓氏
    if authors and len(authors) > 0:
        # 假设姓氏是名字的第一部分（适用于英文姓名）
        first_author = authors[0]
        # 取第一个单词作为姓氏
        surname = first_author.split()[0] if first_author else "Unknown"
        # 移除姓氏中的非字母字符
        surname = re.sub(r'[^a-zA-Z]', '', surname)
    else:
        surname = "Unknown"
    
    # 提取标题中的关键词（移除停用词）
    stop_words = {"the", "a", "an", "and", "or", "of", "in", "on", "for", "with", "based", "using"}
    title_words = re.findall(r'\b\w+\b', title.lower())
    key_words = [w.capitalize() for w in title_words if w.lower() not in stop_words][:3]
    
    # 组合引用键
    key = f"{surname}{year}{''.join(key_words)}"
    
    # 确保只包含安全字符
    key = re.sub(r'[^a-zA-Z0-9]', '', key)
    
    return key[:50]  # 限制长度


def _escape_bibtex_string(text: str) -> str:
    """
    转义 BibTeX 字符串中的特殊字符
    """
    if not text:
        return ""
    
    # BibTeX 中需要转义的字符
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = text.replace('_', '\\_')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    
    return text


def paper_to_bibtex(paper: dict) -> str:
    """
    将单篇论文转换为 BibTeX 格式
    
    参数:
        paper: dict，包含 title, authors, year, url, abstract 等字段
               可选字段：publication（发表 venue），ccf_rank（CCF 评级）
    
    返回:
        str: BibTeX 格式的字符串
    """
    title = paper.get("title", "Unknown Title")
    authors = paper.get("authors", [])
    year = str(paper.get("year", "unknown"))
    url = paper.get("url", "")
    abstract = paper.get("abstract", "")
    source = paper.get("source", "arxiv")
    publication = paper.get("publication", "")  # 发表 venue
    ccf_rank = paper.get("ccf_rank", "")  # CCF 评级
    is_preprint = paper.get("is_preprint", False)  # 是否为预印本
    
    # 生成引用键
    bibtex_key = _sanitize_bibtex_key(title, year, authors)
    
    # 格式化作者列表
    if authors:
        # BibTeX 格式：作者之间用 " and " 连接
        author_list = " and ".join(authors)
    else:
        author_list = "Unknown"
    
    # 确定条目类型
    if is_preprint or source == "arxiv":
        entry_type = "misc"
        # 对于 arXiv 预印本，添加 eprint 字段
        eprint_info = f"\n  eprint = {{{url}}},\n  archivePrefix = {{arXiv}},"
    elif publication:
        entry_type = "inproceedings" if "conference" in publication.lower() or "proceedings" in publication.lower() else "article"
        eprint_info = ""
    else:
        entry_type = "misc"
        eprint_info = f"\n  howpublished = {{\\url{{{url}}}}},"
    
    # 构建 BibTeX 条目
    bibtex = f"@{entry_type}{{{bibtex_key},\n"
    bibtex += f"  title = {{{_escape_bibtex_string(title)}}},\n"
    bibtex += f"  author = {{{_escape_bibtex_string(author_list)}}},\n"
    bibtex += f"  year = {{{year}}},\n"
    
    # 添加发表信息
    if publication:
        if entry_type == "inproceedings":
            bibtex += f"  booktitle = {{{_escape_bibtex_string(publication)}}},\n"
        else:
            bibtex += f"  journal = {{{_escape_bibtex_string(publication)}}},\n"
        
        # 添加 CCF 评级作为注释
        if ccf_rank:
            bibtex += f"  note = {{CCF-{ccf_rank}}},\n"
    
    # 添加摘要（可选，Zotero 可以读取）
    if abstract:
        # 截断过长的摘要
        abstract_short = abstract[:500] + "..." if len(abstract) > 500 else abstract
        bibtex += f"  abstract = {{{_escape_bibtex_string(abstract_short)}}},\n"
    
    # 添加 URL/eprint 信息
    if eprint_info:
        bibtex += eprint_info
    elif url and not publication:
        bibtex += f"  url = {{{url}}},\n"
    
    # 添加访问日期（对于在线资源）
    if url:
        today = datetime.now().strftime("%Y-%m-%d")
        bibtex += f"  urldate = {{{today}}},\n"
    
    bibtex += "}"
    
    return bibtex


def export_bibtex(papers: list, output_path: str) -> str:
    """
    批量导出论文为 BibTeX 文件
    
    参数:
        papers: list of dict，论文列表
        output_path: 输出文件路径（.bib 文件）
    
    返回:
        str: 输出文件的绝对路径
    """
    # 确保目录存在
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    
    # 生成 BibTeX 内容
    bibtex_entries = []
    
    # 添加文件头注释
    header = f"""% This file was created by paper-review-pro
% Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
% Total entries: {len(papers)}
% 
% Import to Zotero: File -> Import -> From File -> Select this .bib file
%
"""
    bibtex_entries.append(header)
    
    for i, paper in enumerate(papers, 1):
        try:
            bibtex_entry = paper_to_bibtex(paper)
            bibtex_entries.append(bibtex_entry)
            print(f"  [BibTeX] 导出 {i}/{len(papers)}: {paper.get('title', 'Unknown')[:50]}...")
        except Exception as e:
            print(f"  [BibTeX 警告] 跳过论文 {i}: {e}")
    
    # 写入文件
    content = "\n\n".join(bibtex_entries)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  [BibTeX] 文件已保存：{output_path}")
    
    return output_path


def generate_bibtex_path(query: str, config: dict) -> str:
    """
    根据查询生成 BibTeX 文件路径
    
    参数:
        query: 原始查询字符串
        config: 配置字典
    
    返回:
        str: BibTeX 文件路径
    """
    # 使用查询字符串生成文件名
    safe_query = re.sub(r'[^a-zA-Z0-9]', '_', query.lower())[:30]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    papers_dir = config["storage"]["papers_dir"]
    bibtex_path = os.path.join(papers_dir, f"bibtex_{safe_query}_{timestamp}.bib")
    
    return bibtex_path


def main():
    """
    命令行测试入口
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="BibTeX 导出测试")
    parser.add_argument("--title", type=str, required=True, help="论文标题")
    parser.add_argument("--authors", type=str, nargs="+", default=["Unknown Author"], help="作者列表")
    parser.add_argument("--year", type=int, default=2025, help="发表年份")
    parser.add_argument("--url", type=str, default="", help="论文 URL")
    parser.add_argument("--abstract", type=str, default="", help="论文摘要")
    parser.add_argument("--publication", type=str, default="", help="发表 venue")
    parser.add_argument("--ccf-rank", type=str, default="", dest="ccf_rank", help="CCF 评级 (A/B/C)")
    parser.add_argument("--output", type=str, default="test.bib", help="输出文件路径")
    
    args = parser.parse_args()
    
    paper = {
        "title": args.title,
        "authors": args.authors,
        "year": args.year,
        "url": args.url,
        "abstract": args.abstract,
        "publication": args.publication,
        "ccf_rank": args.ccf_rank,
        "is_preprint": not args.publication
    }
    
    # 生成单篇 BibTeX
    bibtex = paper_to_bibtex(paper)
    print("\n=== BibTeX 条目 ===\n")
    print(bibtex)
    
    # 导出到文件
    export_bibtex([paper], args.output)
    print(f"\n✓ 已导出到：{args.output}")


if __name__ == "__main__":
    main()
