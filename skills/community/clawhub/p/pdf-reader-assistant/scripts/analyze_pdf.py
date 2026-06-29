#!/usr/bin/env python3
"""
PDF 结构化分析脚本 v2.0
支持：目录生成、智能摘要、关键词提取、表格汇总、图片注记、多文档对比
"""

import sys
import json
import re
import os


def analyze_pdf(extract_result: dict) -> dict:
    """Analyze extracted PDF text and generate structured output."""
    if not extract_result.get("success"):
        return {"success": False, "error": extract_result.get("error", "Unknown error")}

    text = extract_result.get("full_text", "")
    pages = extract_result.get("pages", [])
    metadata = extract_result.get("metadata", {})
    tables = extract_result.get("tables", [])
    images = extract_result.get("images", [])
    is_scanned = extract_result.get("is_scanned", False)

    # 1. 目录提取
    toc = []
    heading_patterns = [
        r'^(?:第[一二三四五六七八九十百\d]+章|Chapter\s+\d+)[\s\.：:。](.{2,40})$',
        r'^(?:\d+[\.\d]*)\s+(.{2,40})$',
        r'^(?:\d+\s+)([A-Z][A-Za-z\s]{4,40})$',
        r'^[一二三四五六七八九十]+[、.．]\s*(.{2,30})$',
    ]
    seen_titles = set()
    for p in pages:
        lines = p["text"].split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 80 or len(line) < 3:
                continue
            for pat in heading_patterns:
                m = re.match(pat, line)
                if m and line not in seen_titles:
                    toc.append({"page": p["page"], "title": line})
                    seen_titles.add(line)
                    break
        if len(toc) >= 40:
            break

    # 2. 智能摘要（取前800字 + 中间采样 + 后200字）
    total_len = len(text)
    if total_len <= 1200:
        summary = text
    else:
        head = text[:800]
        mid_start = total_len // 2 - 100
        mid = text[mid_start:mid_start+200]
        tail = text[-200:]
        summary = head + "\n\n[...中间内容...]\n\n" + mid + "\n\n[...]\n\n" + tail

    # 3. 关键词词频（中文 + 英文专词）
    stopwords = set("的 了 和 是 在 有 我 他 她 它 们 这 那 为 之 与 及 或 但 而 因为 所以 如果 就 也 都 要 会 能 可以 一个 一种 通过 进行 使用 需要 实现 方法 系统 本文 研究 分析 基于 提出 设计 开发 应用 技术 数据 结果 实验 表明 显示 发现 总结 结论 其 对 等 将 该 此 由 以 来 已 中 上 下 内 外 前 后 从 到 被 于 个 人 年 月 日 时".split())
    cn_words = re.findall(r'[\u4e00-\u9fff]{2,6}', text)
    en_terms = re.findall(r'[A-Z][a-zA-Z]{3,}(?:\s+[A-Z][a-zA-Z]{2,})*', text)  # 专有名词

    freq = {}
    for w in cn_words:
        if w not in stopwords:
            freq[w] = freq.get(w, 0) + 1
    for w in en_terms:
        if len(w) > 3:
            freq[w] = freq.get(w, 0) + 1

    keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:15]

    # 4. 统计信息
    total_chars = len(text)
    cn_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    en_words_count = len(re.findall(r'\b[a-zA-Z]+\b', text))
    numbers_count = len(re.findall(r'\d+\.?\d*', text))

    # 5. 表格摘要
    table_summary = []
    for t in tables:
        table_summary.append({
            "page": t["page"],
            "table_index": t["table_index"],
            "size": f"{t['rows']}行×{t['cols']}列",
            "markdown": t["markdown"]
        })

    return {
        "success": True,
        "filename": extract_result.get("filename", ""),
        "total_pages": extract_result.get("total_pages", 0),
        "is_scanned": is_scanned,
        "ocr_engine": extract_result.get("ocr_engine", None),
        "metadata": metadata,
        "summary": summary,
        "keywords": [{"word": w, "count": c} for w, c in keywords],
        "toc": toc,
        "tables": table_summary,
        "images": images,
        "stats": {
            "total_chars": total_chars,
            "chinese_chars": cn_chars,
            "english_words": en_words_count,
            "numbers": numbers_count,
            "table_count": len(tables),
            "image_pages": len(images),
        },
    }


def compare_pdfs(results: list) -> dict:
    """对比多个PDF的关键词和主题"""
    if len(results) < 2:
        return {"success": False, "error": "至少需要2个PDF才能对比"}

    comparison = []
    all_keywords = {}

    for r in results:
        if not r.get("success"):
            continue
        kws = {item["word"]: item["count"] for item in r.get("keywords", [])}
        all_keywords[r["filename"]] = kws
        comparison.append({
            "filename": r["filename"],
            "pages": r.get("total_pages", 0),
            "chars": r.get("stats", {}).get("total_chars", 0),
            "top_keywords": list(kws.keys())[:5],
            "table_count": r.get("stats", {}).get("table_count", 0),
        })

    # 找共同关键词
    if len(all_keywords) >= 2:
        files = list(all_keywords.keys())
        common = set(all_keywords[files[0]].keys())
        for f in files[1:]:
            common &= set(all_keywords[f].keys())
        shared_keywords = list(common)[:10]
    else:
        shared_keywords = []

    return {
        "success": True,
        "doc_count": len(results),
        "documents": comparison,
        "shared_keywords": shared_keywords,
        "note": "共同关键词代表各文档的共同主题"
    }


def batch_analyze(pdf_paths: list, max_pages: int = 10) -> dict:
    """批量分析多个PDF"""
    sys.path.insert(0, os.path.dirname(__file__))
    from extract_pdf import extract_pdf

    results = []
    for path in pdf_paths:
        ext = extract_pdf(path, max_pages)
        analyzed = analyze_pdf(ext)
        analyzed["path"] = path
        results.append(analyzed)

    return {
        "success": True,
        "total": len(pdf_paths),
        "results": results,
        "comparison": compare_pdfs(results)
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Usage: analyze_pdf.py <extract_result.json>"}, ensure_ascii=False))
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = analyze_pdf(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
