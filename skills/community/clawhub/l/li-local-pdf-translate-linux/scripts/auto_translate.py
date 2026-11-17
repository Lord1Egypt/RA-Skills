#!/usr/bin/env python3
"""
单Agent自动翻译程序 - 顺序处理文档
连接本地大模型，逐个读取文档，逐个翻译
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config, show_config, parse_direction, get_language_name
from extract_pdf import extract_pdf_text, get_pdf_info, check_pdf_valid
from translate_api import LocalTranslator


class SingleAgentTranslator:
    """单Agent翻译器 - 顺序处理"""
    
    def __init__(self, config: Dict = None):
        self.config = config or load_config()
        self.translator = LocalTranslator(
            self.config["api_url"],
            self.config["api_key"],
            self.config["model"]
        )
        self.stats = {
            "total_files": 0,
            "success_files": 0,
            "failed_files": [],
            "total_pages": 0,
            "total_chars": 0,
            "total_time": 0
        }
    
    def run(self, input_dir: str, output_dir: str, 
            direction: str = None, depth: str = None,
            pages: str = None, file_filter: str = None):
        """
        运行翻译
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            direction: 翻译方向
            depth: 翻译深度
            pages: 页码范围
            file_filter: 文件过滤（如 "*.pdf"）
        """
        direction = direction or self.config["direction"]
        depth = depth or self.config["depth"]
        
        # 校验翻译方向
        try:
            src, tgt = parse_direction(direction)
        except ValueError as e:
            print(f"Error: {e}")
            return
        src_name = get_language_name(src, "en")
        tgt_name = get_language_name(tgt, "en")
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        if not input_path.exists():
            print(f"Error: Input directory not found: {input_dir}")
            return
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 查找文件
        if file_filter:
            files = list(input_path.glob(file_filter))
        else:
            files = list(set(
                list(input_path.glob("*.pdf")) + 
                list(input_path.glob("*.PDF")) +
                list(input_path.glob("*.md")) +
                list(input_path.glob("*.MD")) +
                list(input_path.glob("*.txt")) +
                list(input_path.glob("*.TXT"))
            ))
        
        files.sort()
        
        if not files:
            print(f"No files found in: {input_dir}")
            return
        
        self.stats["total_files"] = len(files)
        
        print(f"\n{'='*60}")
        print(f"Single Agent Translation")
        print(f"Input:  {input_dir}")
        print(f"Output: {output_dir}")
        print(f"Files:  {len(files)}")
        print(f"Model:  {os.path.basename(self.config['model'])}")
        print(f"Direction: {direction} ({src_name} -> {tgt_name}), Depth: {depth}")
        print(f"{'='*60}\n")
        
        # 检查连接
        if not self.translator.check_connection():
            print("Error: API connection failed")
            return
        
        # 逐个处理
        for i, file_path in enumerate(files, 1):
            self._process_file(file_path, output_path, direction, tgt, depth, pages, i, len(files))
        
        # 打印统计
        self._print_stats()
    
    def _process_file(self, file_path: Path, output_path: Path,
                     direction: str, tgt: str, depth: str, pages: str,
                     current: int, total: int):
        """处理单个文件"""
        print(f"\n[{current}/{total}] {file_path.name}")
        
        start_time = time.time()
        
        try:
            # 检查文件类型
            suffix = file_path.suffix.lower()
            
            if suffix == '.pdf':
                # PDF文件 - 提取后翻译
                is_valid, msg = check_pdf_valid(str(file_path))
                if not is_valid:
                    print(f"  Skip: {msg}")
                    self.stats["failed_files"].append({"file": file_path.name, "error": msg})
                    return
                
                page_texts = extract_pdf_text(str(file_path), pages)
                
                if not page_texts:
                    print(f"  Skip: No text found")
                    self.stats["failed_files"].append({"file": file_path.name, "error": "No text"})
                    return
                
                # 翻译
                translated_content = self._translate_pages(page_texts, direction, depth)
                
                # 输出
                out_file = output_path / f"{file_path.stem}.{tgt}.md"
                self._write_output(out_file, file_path.name, page_texts, translated_content, direction, depth)
                
                elapsed = time.time() - start_time
                pages_count = len(page_texts)
                chars_count = sum(len(t) for t in page_texts.values())
                
                self.stats["success_files"] += 1
                self.stats["total_pages"] += pages_count
                self.stats["total_chars"] += chars_count
                self.stats["total_time"] += elapsed
                
                print(f"  Done: {pages_count} pages, {chars_count} chars, {elapsed:.1f}s")
                
            elif suffix in ['.md', '.txt']:
                # 文本文件 - 直接翻译
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.strip():
                    print(f"  Skip: Empty file")
                    return
                
                # 翻译
                result = self.translator.translate_segment(content, direction, depth)
                
                # 输出
                out_file = output_path / f"{file_path.stem}.{tgt}.md"
                tgt_name = get_language_name(tgt, "en")
                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {file_path.stem} - {tgt_name} Translation\n\n")
                    f.write(f"> Source: {file_path.name}\n")
                    f.write(f"> Direction: {direction}\n")
                    f.write(f"> Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")
                    f.write(result["translated"])
                
                elapsed = time.time() - start_time
                
                self.stats["success_files"] += 1
                self.stats["total_chars"] += len(content)
                self.stats["total_time"] += elapsed
                
                print(f"  Done: {len(content)} chars, {elapsed:.1f}s")
            
            else:
                print(f"  Skip: Unsupported file type ({suffix})")
                
        except Exception as e:
            print(f"  Error: {e}")
            self.stats["failed_files"].append({"file": file_path.name, "error": str(e)})
    
    def _translate_pages(self, page_texts: Dict, direction: str, depth: str) -> Dict:
        """翻译多页内容"""
        context = ""
        results = {}
        
        max_chunk = self.config.get("max_chunk_size", 1500)
        
        for page_num, text in page_texts.items():
            if len(text) > max_chunk * 2:
                # 分块翻译
                chunks = self._split_text(text, max_chunk)
                translated_chunks = []
                for chunk in chunks:
                    result = self.translator.translate_segment(chunk, direction, depth, context)
                    translated_chunks.append(result["translated"])
                    context = result["translated"][-200:]
                results[page_num] = "\n\n".join(translated_chunks)
            else:
                result = self.translator.translate_segment(text, direction, depth, context)
                results[page_num] = result["translated"]
                context = result["translated"][-200:]
        
        return results
    
    def _split_text(self, text: str, chunk_size: int) -> List[str]:
        """分割文本"""
        paragraphs = text.split('\n\n')
        chunks = []
        current = ""
        
        for para in paragraphs:
            if len(current) + len(para) > chunk_size and current:
                chunks.append(current.strip())
                current = para
            else:
                current += "\n\n" + para if current else para
        
        if current.strip():
            chunks.append(current.strip())
        
        return chunks if chunks else [text]
    
    def _write_output(self, out_file: Path, source_name: str,
                     page_texts: Dict, translated: Dict,
                     direction: str, depth: str):
        """写入输出文件"""
        try:
            src, tgt = parse_direction(direction)
        except ValueError:
            src, tgt = "en", "zh"
        src_name = get_language_name(src, "en")
        tgt_name = get_language_name(tgt, "en")
        
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(f"# {source_name} - {tgt_name} Translation\n\n")
            f.write(f"> Source: {source_name}\n")
            f.write(f"> Direction: {direction} ({src_name} -> {tgt_name})\n")
            f.write(f"> Depth: {depth}\n")
            f.write(f"> Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n")
            
            for page_num in sorted(translated.keys()):
                f.write(f"\n## Page {page_num}\n\n")
                f.write(translated[page_num])
                f.write("\n")
    
    def _print_stats(self):
        """打印统计"""
        print(f"\n{'='*60}")
        print(f"Translation Complete!")
        print(f"  Success: {self.stats['success_files']}/{self.stats['total_files']}")
        print(f"  Pages:   {self.stats['total_pages']}")
        print(f"  Chars:   {self.stats['total_chars']}")
        print(f"  Time:    {self.stats['total_time']:.1f}s")
        if self.stats['total_time'] > 0:
            speed = self.stats['total_chars'] / self.stats['total_time']
            print(f"  Speed:   {speed:.0f} chars/s")
        if self.stats["failed_files"]:
            print(f"  Failed:")
            for f in self.stats["failed_files"]:
                print(f"    - {f['file']}: {f['error']}")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='Single Agent Auto Translation')
    
    parser.add_argument('--input', '-i', required=True, help='Input directory')
    parser.add_argument('--output', '-o', help='Output directory (default: input_<target_lang>)')
    parser.add_argument('--direction', help='Direction, e.g. en2zh/zh2ja/ja2en')
    parser.add_argument('--depth', choices=['quick', 'standard', 'full'], help='Depth')
    parser.add_argument('--pages', help='Page range')
    parser.add_argument('--filter', help='File filter (e.g. "*.pdf")')
    
    args = parser.parse_args()
    
    config = load_config()
    
    direction = args.direction or config.get("direction", "en2zh")
    try:
        src, tgt = parse_direction(direction)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    agent = SingleAgentTranslator(config)
    agent.run(
        input_dir=args.input,
        output_dir=args.output or f"{args.input}_{tgt}",
        direction=args.direction,
        depth=args.depth,
        pages=args.pages,
        file_filter=args.filter
    )


if __name__ == "__main__":
    main()
