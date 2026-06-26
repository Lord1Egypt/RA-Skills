#!/usr/bin/env python3
"""PDF 处理工具 - 合并/拆分/提取/加水印"""
import sys
import argparse
from PyPDF2 import PdfReader, PdfWriter, PdfFileMerger
from PyPDF2.generic import AnnotationBuilder
import os


def merge_pdfs(input_files, output_path):
    merger = PdfFileMerger()
    for f in input_files:
        merger.append(f)
    merger.write(output_path)
    merger.close()
    print(f"[OK] PDF 合并完成: {output_path}")


def split_pdf(input_path, output_dir, page_range=None):
    reader = PdfReader(input_path)
    os.makedirs(output_dir, exist_ok=True)
    if page_range:
        writer = PdfWriter()
        for pg in page_range:
            writer.add_page(reader.pages[pg - 1])
        out = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_path))[0]}_pages_{page_range}.pdf")
        with open(out, 'wb') as f:
            writer.write(f)
        print(f"[OK] 页面 {page_range} 已导出: {out}")
    else:
        for i, page in enumerate(reader.pages, 1):
            writer = PdfWriter()
            writer.add_page(page)
            out = os.path.join(output_dir, f"page_{i:03d}.pdf")
            with open(out, 'wb') as f:
                writer.write(f)
        print(f"[OK] PDF 已拆分为 {len(reader.pages)} 个页面: {output_dir}")


def extract_text(input_path, output_path=None):
    reader = PdfReader(input_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n--- Page Break ---\n"
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"[OK] 文本已提取: {output_path}")
    else:
        print(text)


def add_watermark(input_path, output_path, text, opacity=0.3):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        # 简单文本水印：添加文本 annotation
        annotation = AnnotationBuilder.string_annotation(
            contents=text,
            rect=(50, 50, 200, 100)
        )
        page.add_annotation(annotation)
        writer.add_page(page)
    with open(output_path, 'wb') as f:
        writer.write(f)
    print(f"[OK] 水印已添加: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PDF 处理工具')
    sub = parser.add_subparsers(dest='cmd')
    sub.add_parser('merge', help='合并 PDF').add_argument('inputs', nargs='+', help='输入文件')
    merge_p = sub.add_parser('split', help='拆分 PDF')
    merge_p.add_argument('input')
    merge_p.add_argument('--output', '-o', default='.')
    merge_p.add_argument('--pages', '-p', help='如 1-3 或 1,3,5')
    ext_p = sub.add_parser('extract', help='提取文本')
    ext_p.add_argument('input')
    ext_p.add_argument('--output', '-o', default=None)
    water_p = sub.add_parser('watermark')
    water_p.add_argument('input')
    water_p.add_argument('--text', '-t', default='CONFIDENTIAL')
    water_p.add_argument('--output', '-o', default='watermarked.pdf')
    args = parser.parse_args()
    if args.cmd == 'merge':
        merge_pdfs(args.inputs, 'merged.pdf')
    elif args.cmd == 'split':
        pr = None
        if args.pages:
            parts = args.pages.split('-')
            if len(parts) == 2:
                pr = range(int(parts[0]) - 1, int(parts[1]))
            else:
                pr = [int(x) - 1 for x in args.pages.split(',')]
        split_pdf(args.input, args.output, pr)
    elif args.cmd == 'extract':
        extract_text(args.input, args.output)
    elif args.cmd == 'watermark':
        add_watermark(args.input, args.output, args.text)
