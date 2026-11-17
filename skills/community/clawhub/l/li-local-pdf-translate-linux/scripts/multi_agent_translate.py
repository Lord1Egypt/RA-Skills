#!/usr/bin/env python3
"""
多Agent并行翻译程序 - 同时处理多个文档
使用concurrent.futures实现并行翻译
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config, show_config, parse_direction, get_language_name
from extract_pdf import extract_pdf_text, get_pdf_info, check_pdf_valid
from translate_api import LocalTranslator


class MultiAgentTranslator:
    """多Agent翻译器 - 并行处理"""
    
    def __init__(self, config: Dict = None, max_agents: int = 2):
        """
        初始化多Agent翻译器
        
        Args:
            config: 配置字典
            max_agents: 最大并行Agent数（建议2-3，避免GPU过载）
        """
        self.config = config or load_config()
        self.max_agents = max_agents
        self.lock = threading.Lock()
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
        """运行多Agent翻译"""
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
        print(f"Multi-Agent Translation")
        print(f"Input:     {input_dir}")
        print(f"Output:    {output_dir}")
        print(f"Files:     {len(files)}")
        print(f"Agents:    {self.max_agents}")
        print(f"Model:     {os.path.basename(self.config['model'])}")
        print(f"Direction: {direction} ({src_name} -> {tgt_name}), Depth: {depth}")
        print(f"{'='*60}\n")
        
        # 测试连接
        test_translator = LocalTranslator(
            self.config["api_url"],
            self.config["api_key"],
            self.config["model"]
        )
        if not test_translator.check_connection():
            print("Error: API connection failed")
            return
        
        # 并行处理
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_agents) as executor:
            future_to_file = {}
            
            for file_path in files:
                future = executor.submit(
                    self._process_file,
                    file_path, output_path, direction, tgt, depth, pages
                )
                future_to_file[future] = file_path
            
            # 收集结果
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"  Fatal error in {file_path.name}: {e}")
                    with self.lock:
                        self.stats["failed_files"].append({
                            "file": file_path.name,
                            "error": str(e)
                        })
        
        self.stats["total_time"] = time.time() - start_time
        
        # 打印统计
        self._print_stats()
    
    def _process_file(self, file_path: Path, output_path: Path,
                     direction: str, tgt: str, depth: str, pages: str):
        """处理单个文件（线程安全）"""
        # 每个线程创建自己的翻译器实例
        translator = LocalTranslator(
            self.config["api_url"],
            self.config["api_key"],
            self.config["model"]
        )
        
        thread_name = threading.current_thread().name
        print(f"\n[{thread_name}] {file_path.name}")
        
        start_time = time.time()
        
        try:
            suffix = file_path.suffix.lower()
            
            if suffix == '.pdf':
                # PDF处理
                is_valid, msg = check_pdf_valid(str(file_path))
                if not is_valid:
                    print(f"  [{thread_name}] Skip: {msg}")
                    with self.lock:
                        self.stats["failed_files"].append({"file": file_path.name, "error": msg})
                    return
                
                page_texts = extract_pdf_text(str(file_path), pages)
                
                if not page_texts:
                    print(f"  [{thread_name}] Skip: No text")
                    with self.lock:
                        self.stats["failed_files"].append({"file": file_path.name, "error": "No text"})
                    return
                
                # 翻译
                max_chunk = self.config.get("max_chunk_size", 1500)
                context = ""
                translated = {}
                
                for page_num, text in page_texts.items():
                    if len(text) > max_chunk * 2:
                        chunks = self._split_text(text, max_chunk)
                        translated_chunks = []
                        for chunk in chunks:
                            result = translator.translate_segment(chunk, direction, depth, context)
                            translated_chunks.append(result["translated"])
                            context = result["translated"][-200:]
                        translated[page_num] = "\n\n".join(translated_chunks)
                    else:
                        result = translator.translate_segment(text, direction, depth, context)
                        translated[page_num] = result["translated"]
                        context = result["translated"][-200:]
                
                # 写入
                out_file = output_path / f"{file_path.stem}.{tgt}.md"
                self._write_output(out_file, file_path.name, translated, direction, depth)
                
                elapsed = time.time() - start_time
                pages_count = len(page_texts)
                chars_count = sum(len(t) for t in page_texts.values())
                
                with self.lock:
                    self.stats["success_files"] += 1
                    self.stats["total_pages"] += pages_count
                    self.stats["total_chars"] += chars_count
                
                print(f"  [{thread_name}] Done: {pages_count} pages, {elapsed:.1f}s")
                
            elif suffix in ['.md', '.txt']:
                # 文本文件处理
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.strip():
                    print(f"  [{thread_name}] Skip: Empty")
                    return
                
                result = translator.translate_segment(content, direction, depth)
                
                out_file = output_path / f"{file_path.stem}.{tgt}.md"
                tgt_name = get_language_name(tgt, "en")
                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {file_path.stem} - {tgt_name} Translation\n\n")
                    f.write(f"> Source: {file_path.name}\n")
                    f.write(f"> Direction: {direction}\n")
                    f.write(f"> Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")
                    f.write(result["translated"])
                
                elapsed = time.time() - start_time
                
                with self.lock:
                    self.stats["success_files"] += 1
                    self.stats["total_chars"] += len(content)
                
                print(f"  [{thread_name}] Done: {len(content)} chars, {elapsed:.1f}s")
            
            else:
                print(f"  [{thread_name}] Skip: {suffix}")
                
        except Exception as e:
            print(f"  [{thread_name}] Error: {e}")
            with self.lock:
                self.stats["failed_files"].append({"file": file_path.name, "error": str(e)})
    
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
                     translated: Dict, direction: str, depth: str):
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
        print(f"Multi-Agent Translation Complete!")
        print(f"  Agents:   {self.max_agents}")
        print(f"  Success:  {self.stats['success_files']}/{self.stats['total_files']}")
        print(f"  Pages:    {self.stats['total_pages']}")
        print(f"  Chars:    {self.stats['total_chars']}")
        print(f"  Time:     {self.stats['total_time']:.1f}s")
        if self.stats['total_time'] > 0:
            speed = self.stats['total_chars'] / self.stats['total_time']
            print(f"  Speed:    {speed:.0f} chars/s")
        if self.stats["failed_files"]:
            print(f"  Failed:")
            for f in self.stats["failed_files"]:
                print(f"    - {f['file']}: {f['error']}")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='Multi-Agent Parallel Translation')
    
    parser.add_argument('--input', '-i', required=True, help='Input directory')
    parser.add_argument('--output', '-o', help='Output directory')
    parser.add_argument('--agents', '-a', type=int, default=2, 
                       help='Number of parallel agents (default: 2, max: 4)')
    parser.add_argument('--direction', help='Direction, e.g. en2zh/zh2ja/ja2en')
    parser.add_argument('--depth', choices=['quick', 'standard', 'full'], help='Depth')
    parser.add_argument('--pages', help='Page range')
    parser.add_argument('--filter', help='File filter')
    
    args = parser.parse_args()
    
    # 限制最大agent数
    max_agents = min(args.agents, 4)
    
    config = load_config()
    
    direction = args.direction or config.get("direction", "en2zh")
    try:
        src, tgt = parse_direction(direction)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    agent = MultiAgentTranslator(config, max_agents)
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
