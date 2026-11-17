#!/usr/bin/env python3
"""
PDF批量翻译主程序 - 调用其他模块完成翻译
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Dict, List

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config, show_config, parse_direction, get_language_name
from extract_pdf import extract_pdf_text, get_pdf_info, check_pdf_valid
from translate_api import LocalTranslator


def translate_pdf_to_markdown(
    pdf_path: str,
    output_path: str,
    api_url: str = None,
    api_key: str = None,
    model: str = None,
    direction: str = "en2zh",
    depth: str = "standard",
    pages: str = None,
    max_chunk_size: int = 1500
) -> Dict:
    """
    翻译PDF文件并输出为Markdown
    """
    # 校验翻译方向
    try:
        src, tgt = parse_direction(direction)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return {"error": str(e)}
    
    src_name = get_language_name(src, "en")
    tgt_name = get_language_name(tgt, "en")
    
    print(f"\n{'='*60}")
    print(f"Translating: {os.path.basename(pdf_path)}")
    print(f"Direction: {direction} ({src_name} -> {tgt_name}), Depth: {depth}")
    print(f"{'='*60}\n")
    
    # 1. Extract PDF text
    print("[1/3] Extracting PDF text...")
    try:
        page_texts = extract_pdf_text(pdf_path, pages)
    except Exception as e:
        print(f"Error: PDF extraction failed - {e}", file=sys.stderr)
        return {"error": str(e)}
    
    if not page_texts:
        print("Error: No extractable text in PDF", file=sys.stderr)
        return {"error": "No text found"}
    
    print(f"  Extracted {len(page_texts)} pages")
    
    # 2. Initialize translator
    print("[2/3] Initializing translator...")
    translator = LocalTranslator(api_url, api_key, model)
    
    if not translator.check_connection():
        print("Error: API connection failed", file=sys.stderr)
        return {"error": "API connection failed"}
    
    print("  Connection OK")
    
    # 3. Translate page by page
    print("[3/3] Starting translation...")
    
    pdf_info = get_pdf_info(pdf_path)
    title = pdf_info.get("title") or Path(pdf_path).stem
    
    output_lines = [
        f"# {title} - {tgt_name} Translation\n",
        f"\n> Source: {os.path.basename(pdf_path)}",
        f"\n> Direction: {direction} ({src_name} -> {tgt_name})",
        f"\n> Depth: {depth}",
        f"\n> Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"\n\n---\n"
    ]
    
    stats = {
        "total_pages": len(page_texts),
        "translated_pages": 0,
        "total_chars": 0,
        "total_time": 0
    }
    
    context = ""
    
    for page_num, text in page_texts.items():
        if not text.strip():
            continue
        
        print(f"\n  Page {page_num} ({len(text)} chars)...")
        start_time = time.time()
        
        # Split long text
        if len(text) > max_chunk_size * 2:
            chunks = _split_text(text, max_chunk_size)
            translated_chunks = []
            for i, chunk in enumerate(chunks):
                print(f"    Chunk {i+1}/{len(chunks)}...")
                result = translator.translate_segment(chunk, direction, depth, context)
                translated_chunks.append(result["translated"])
                context = result["translated"][-200:]
            translated = "\n\n".join(translated_chunks)
        else:
            result = translator.translate_segment(text, direction, depth, context)
            translated = result["translated"]
            context = translated[-200:]
        
        elapsed = time.time() - start_time
        
        output_lines.append(f"\n## Page {page_num}\n")
        output_lines.append(f"\n{translated}\n")
        
        stats["translated_pages"] += 1
        stats["total_chars"] += len(text)
        stats["total_time"] += elapsed
        
        print(f"    Done ({elapsed:.1f}s)")
    
    # Write output
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\n{'='*60}")
    print(f"Complete!")
    print(f"  Output: {output_path}")
    print(f"  Pages: {stats['translated_pages']}/{stats['total_pages']}")
    print(f"  Chars: {stats['total_chars']}")
    print(f"  Time: {stats['total_time']:.1f}s")
    print(f"{'='*60}\n")
    
    return stats


def _split_text(text: str, chunk_size: int = 1500) -> List[str]:
    """按段落分割文本"""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            current_chunk += "\n\n" + para if current_chunk else para
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks if chunks else [text]


def batch_translate(
    input_dir: str,
    output_dir: str,
    api_url: str = None,
    api_key: str = None,
    model: str = None,
    direction: str = "en2zh",
    depth: str = "standard",
    pages: str = None
) -> Dict:
    """
    批量翻译目录下的所有PDF文件
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"Error: Input directory not found: {input_dir}", file=sys.stderr)
        return {"error": "Input directory not found"}
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(set(list(input_path.glob("*.pdf")) + list(input_path.glob("*.PDF"))))
    
    if not pdf_files:
        print(f"Error: No PDF files found in: {input_dir}", file=sys.stderr)
        return {"error": "No PDF files found"}
    
    print(f"\nFound {len(pdf_files)} PDF files")
    print(f"Output: {output_dir}\n")
    
    # 校验翻译方向
    try:
        src, tgt = parse_direction(direction)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return {"error": str(e)}
    
    batch_stats = {
        "total_files": len(pdf_files),
        "success_files": 0,
        "failed_files": [],
        "total_pages": 0,
        "total_time": 0
    }
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] {pdf_file.name}")
        
        out_file = output_path / f"{pdf_file.stem}.{tgt}.md"
        
        try:
            stats = translate_pdf_to_markdown(
                str(pdf_file), str(out_file),
                api_url, api_key, model,
                direction, depth, pages
            )
            
            if "error" not in stats:
                batch_stats["success_files"] += 1
                batch_stats["total_pages"] += stats.get("translated_pages", 0)
                batch_stats["total_time"] += stats.get("total_time", 0)
            else:
                batch_stats["failed_files"].append({"file": pdf_file.name, "error": stats["error"]})
                
        except Exception as e:
            print(f"  Error: {e}", file=sys.stderr)
            batch_stats["failed_files"].append({"file": pdf_file.name, "error": str(e)})
    
    print(f"\n{'='*60}")
    print(f"Batch complete!")
    print(f"  Success: {batch_stats['success_files']}/{batch_stats['total_files']}")
    print(f"  Pages: {batch_stats['total_pages']}")
    print(f"  Time: {batch_stats['total_time']:.1f}s")
    if batch_stats["failed_files"]:
        print(f"  Failed:")
        for f in batch_stats["failed_files"]:
            print(f"    - {f['file']}: {f['error']}")
    print(f"{'='*60}\n")
    
    return batch_stats


def main():
    parser = argparse.ArgumentParser(description='PDF Batch Translation')
    
    parser.add_argument('--input', '-i', help='Input PDF file or directory')
    parser.add_argument('--output', '-o', help='Output file or directory')
    parser.add_argument('--input-dir', help='Input directory (batch mode)')
    parser.add_argument('--output-dir', help='Output directory (batch mode)')
    
    parser.add_argument('--api-url', help='API URL (override config)')
    parser.add_argument('--api-key', help='API key (override config)')
    parser.add_argument('--model', help='Model name (override config)')
    
    parser.add_argument('--direction', help='Translation direction, e.g. en2zh/zh2ja/ja2en')
    parser.add_argument('--depth', choices=['quick', 'standard', 'full'], help='Translation depth')
    parser.add_argument('--pages', help='Page range, e.g. "1-5"')
    
    parser.add_argument('--check', action='store_true', help='Check connection')
    parser.add_argument('--config', action='store_true', help='Show config')
    
    args = parser.parse_args()
    
    # Load config
    config = load_config()
    
    # CLI args override config
    api_url = args.api_url or config.get("api_url")
    api_key = args.api_key or config.get("api_key")
    model = args.model or config.get("model")
    direction = args.direction or config.get("direction", "en2zh")
    depth = args.depth or config.get("depth", "standard")
    
    # Validate direction
    try:
        src, tgt = parse_direction(direction)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    if args.config:
        show_config()
        return
    
    if args.check:
        translator = LocalTranslator(api_url, api_key, model)
        if translator.check_connection():
            print("[OK] API connected")
            print(f"  URL: {api_url}")
            print(f"  Model: {os.path.basename(model) if model else 'default'}")
            sys.exit(0)
        else:
            print("[FAIL] API connection failed", file=sys.stderr)
            sys.exit(1)
    
    # Batch mode
    if args.input_dir or args.output_dir:
        input_dir = args.input_dir or args.input
        output_dir = args.output_dir or args.output
        
        if not input_dir:
            print("Error: Need --input-dir or --input", file=sys.stderr)
            sys.exit(1)
        
        output_dir = output_dir or f"{input_dir}_{tgt}"
        
        batch_translate(input_dir, output_dir, api_url, api_key, model, direction, depth, args.pages)
        
    elif args.input:
        output = args.output or f"{Path(args.input).stem}.{tgt}.md"
        translate_pdf_to_markdown(args.input, output, api_url, api_key, model, direction, depth, args.pages)
        
    else:
        print("Error: Need --input or --input-dir", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
