#!/usr/bin/env python3
"""
IELTS Reading Passage Extractor
从剑桥雅思 PDF 提取阅读文章
"""

import pdfplumber
import json
import sys

def find_reading_passage_pages(pdf, test_num, passage_num):
    """查找指定 Test 和 Passage 的起始页码"""
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text and f"Test {test_num}" in text and f"READING PASSAGE {passage_num}" in text:
            return i
    return None

def extract_article(pdf, start_page, num_pages):
    """从指定页码范围提取文章"""
    article = ""
    for i in range(start_page, min(start_page + num_pages, len(pdf.pages))):
        article += pdf.pages[i].extract_text()
    return article

def extract_twocolumn_page(page):
    """从两栏页面提取文本（按阅读顺序）"""
    chars = page.chars
    mid = page.width / 2
    
    left = sorted([c for c in chars if c['x0'] < mid], key=lambda x: (x['top'], x['x0']))
    right = sorted([c for c in chars if c['x0'] >= mid], key=lambda x: (x['top'], x['x0']))
    
    left_text = ''.join([c['text'] for c in left])
    right_text = ''.join([c['text'] for c in right])
    
    return left_text + right_text

def main(pdf_path, test_num, passage_num, num_pages=3):
    """主函数"""
    with pdfplumber.open(pdf_path) as pdf:
        # 查找起始页
        start_page = find_reading_passage_pages(pdf, test_num, passage_num)
        
        if start_page is None:
            print(f"找不到 Test {test_num} Reading Passage {passage_num}")
            return
        
        print(f"找到: Test {test_num} Passage {passage_num}, 起始页 {start_page + 1}")
        
        # 提取文章
        article = extract_article(pdf, start_page, num_pages)
        
        print("\n=== 提取的文章 ===")
        print(article[:2000])
        print("..." if len(article) > 2000 else "")
        
        return article

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python extract_article.py <pdf_path> <test_num> <passage_num> [pages]")
        print("示例: python extract_article.py '剑桥雅思4.pdf' 2 1 3")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    test_num = int(sys.argv[2])
    passage_num = int(sys.argv[3])
    num_pages = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    
    main(pdf_path, test_num, passage_num, num_pages)
