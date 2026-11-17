#!/usr/bin/env python3
"""
PDF文本提取模块 - 独立的PDF处理功能
"""

import json
import sys
import fitz  # pymupdf


def extract_pdf_text(pdf_path, pages=None):
    """
    提取PDF文本，按页返回
    
    Args:
        pdf_path: PDF文件路径
        pages: 页码范围，如 "1-5" 或 "1,3,5-7"，None表示全部
    
    Returns:
        dict: {page_num: text, ...}
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    # 解析页码范围
    if pages:
        page_set = set()
        for part in pages.split(','):
            if '-' in part:
                start, end = part.split('-')
                start = max(1, int(start))
                end = min(total_pages, int(end))
                page_set.update(range(start, end + 1))
            else:
                p = int(part)
                if 1 <= p <= total_pages:
                    page_set.add(p)
        page_list = sorted(page_set)
    else:
        page_list = list(range(1, total_pages + 1))
    
    result = {}
    for page_num in page_list:
        page = doc[page_num - 1]  # pymupdf使用0-based索引
        text = page.get_text("text")
        if text.strip():
            result[page_num] = text.strip()
    
    doc.close()
    return result


def get_pdf_info(pdf_path):
    """
    获取PDF基本信息
    
    Args:
        pdf_path: PDF文件路径
    
    Returns:
        dict: PDF元数据
    """
    doc = fitz.open(pdf_path)
    info = {
        "file": pdf_path,
        "title": doc.metadata.get("title", ""),
        "author": doc.metadata.get("author", ""),
        "pages": len(doc)
    }
    doc.close()
    return info


def check_pdf_valid(pdf_path):
    """
    检查PDF是否可提取文本
    
    Args:
        pdf_path: PDF文件路径
    
    Returns:
        tuple: (is_valid, message)
    """
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        # 检查前3页是否有文本
        sample_pages = min(3, total_pages)
        total_chars = 0
        
        for i in range(sample_pages):
            text = doc[i].get_text("text")
            total_chars += len(text.strip())
        
        doc.close()
        
        if total_chars < 100:
            return False, f"PDF may be scanned (only {total_chars} chars in first {sample_pages} pages)"
        
        return True, f"OK ({total_pages} pages, {total_chars} chars in sample)"
        
    except Exception as e:
        return False, f"Error: {e}"


def main():
    """CLI入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PDF Text Extraction')
    parser.add_argument('--input', '-i', required=True, help='PDF file path')
    parser.add_argument('--pages', '-p', help='Page range, e.g. "1-5" or "1,3,5-7"')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--info', action='store_true', help='Show PDF info only')
    parser.add_argument('--check', action='store_true', help='Check if PDF is valid')
    
    args = parser.parse_args()
    
    try:
        if args.info:
            info = get_pdf_info(args.input)
            print(json.dumps(info, ensure_ascii=False, indent=2))
            return
        
        if args.check:
            is_valid, msg = check_pdf_valid(args.input)
            print(f"{'[OK]' if is_valid else '[FAIL]'} {msg}")
            sys.exit(0 if is_valid else 1)
        
        pages = extract_pdf_text(args.input, args.pages)
        
        output = {
            "file": args.input,
            "total_pages_extracted": len(pages),
            "pages": {str(k): v for k, v in pages.items()}
        }
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"Saved to: {args.output}")
        else:
            print(json.dumps(output, ensure_ascii=False, indent=2))
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
