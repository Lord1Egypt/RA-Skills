#!/usr/bin/env python3
"""
大文件智能处理模块
支持 50MB-200MB 文件的自动拆分、并行解析、结果合并
"""

import os
import time
import threading
from typing import List, Dict, Callable, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json


@dataclass
class ProcessingProgress:
    """处理进度"""
    total_chunks: int = 0
    completed_chunks: int = 0
    failed_chunks: int = 0
    current_chunk: int = 0
    status: str = "idle"  # idle/running/paused/completed/failed
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    
    @property
    def percentage(self) -> float:
        """完成百分比"""
        if self.total_chunks == 0:
            return 0.0
        return (self.completed_chunks / self.total_chunks) * 100
    
    @property
    def elapsed_time(self) -> float:
        """已用时间（秒）"""
        end = self.end_time or time.time()
        return end - self.start_time
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "total_chunks": self.total_chunks,
            "completed_chunks": self.completed_chunks,
            "failed_chunks": self.failed_chunks,
            "current_chunk": self.current_chunk,
            "percentage": round(self.percentage, 2),
            "status": self.status,
            "elapsed_time": round(self.elapsed_time, 2)
        }


class LargeFileHandler:
    """
    大文件处理器
    自动拆分、并行解析、断点续传、崩溃恢复
    """
    
    def __init__(self, chunk_size_mb: int = 50, 
                 max_workers: int = 4,
                 progress_callback: Callable = None):
        """
        初始化处理器
        
        Args:
            chunk_size_mb: 分片大小（MB）
            max_workers: 并行工作线程数
            progress_callback: 进度回调函数
        """
        self.chunk_size = chunk_size_mb * 1024 * 1024  # 转换为字节
        self.max_workers = max_workers
        self.progress_callback = progress_callback
        
        self.progress = ProcessingProgress()
        self.checkpoint_file = None
        self.is_running = False
        self._lock = threading.Lock()
    
    def process_large_file(self, file_path: str, 
                          parser_func: Callable,
                          output_dir: str = None) -> Dict[str, Any]:
        """
        处理大文件
        
        Args:
            file_path: 文件路径
            parser_func: 解析函数
            output_dir: 输出目录（可选）
            
        Returns:
            处理结果
        """
        file_size = os.path.getsize(file_path)
        
        # 检查是否需要拆分
        if file_size <= self.chunk_size:
            # 小文件直接处理
            return self._process_small_file(file_path, parser_func)
        
        # 大文件拆分处理
        return self._process_large_file(file_path, parser_func, output_dir)
    
    def _process_small_file(self, file_path: str, 
                           parser_func: Callable) -> Dict[str, Any]:
        """处理小文件"""
        self.progress.status = "running"
        self.progress.total_chunks = 1
        
        try:
            result = parser_func(file_path)
            
            self.progress.completed_chunks = 1
            self.progress.status = "completed"
            self.progress.end_time = time.time()
            
            return {
                "success": True,
                "result": result,
                "chunks": 1,
                "progress": self.progress.to_dict()
            }
            
        except Exception as e:
            self.progress.status = "failed"
            self.progress.end_time = time.time()
            
            return {
                "success": False,
                "error": str(e),
                "progress": self.progress.to_dict()
            }
    
    def _process_large_file(self, file_path: str,
                           parser_func: Callable,
                           output_dir: str = None) -> Dict[str, Any]:
        """处理大文件（拆分+并行）"""
        file_size = os.path.getsize(file_path)
        
        # 检查断点
        checkpoint = self._load_checkpoint(file_path)
        if checkpoint:
            print(f"[LargeFileHandler] 发现断点，从第 {checkpoint['last_chunk']} 个分片继续")
            start_chunk = checkpoint['last_chunk']
        else:
            start_chunk = 0
        
        # 智能拆分
        chunks = self._split_file_smart(file_path)
        total_chunks = len(chunks)
        
        self.progress.total_chunks = total_chunks
        self.progress.status = "running"
        self.is_running = True
        
        # 初始化 checkpoint
        self.checkpoint_file = self._get_checkpoint_path(file_path, output_dir)
        
        results = []
        failed_chunks = []
        
        # 并行处理分片
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交任务
            future_to_chunk = {}
            for i, chunk_info in enumerate(chunks):
                if i < start_chunk:
                    continue  # 跳过已处理的分片
                
                future = executor.submit(
                    self._process_chunk,
                    chunk_info,
                    parser_func
                )
                future_to_chunk[future] = i
            
            # 收集结果
            for future in as_completed(future_to_chunk):
                chunk_idx = future_to_chunk[future]
                
                try:
                    result = future.result()
                    results.append((chunk_idx, result))
                    
                    with self._lock:
                        self.progress.completed_chunks += 1
                        self.progress.current_chunk = chunk_idx
                    
                    # 保存断点
                    self._save_checkpoint(file_path, chunk_idx + 1)
                    
                except Exception as e:
                    failed_chunks.append((chunk_idx, str(e)))
                    
                    with self._lock:
                        self.progress.failed_chunks += 1
                    
                    print(f"[LargeFileHandler] 分片 {chunk_idx} 处理失败: {e}")
                
                # 进度回调
                if self.progress_callback:
                    self.progress_callback(self.progress.to_dict())
                
                if not self.is_running:
                    break
        
        self.is_running = False
        
        # 合并结果
        if self.progress.failed_chunks == 0:
            merged_result = self._merge_results(results)
            self.progress.status = "completed"
            
            # 清理 checkpoint
            self._cleanup_checkpoint(file_path)
            
            return {
                "success": True,
                "result": merged_result,
                "chunks": total_chunks,
                "progress": self.progress.to_dict()
            }
        else:
            self.progress.status = "failed"
            
            return {
                "success": False,
                "error": f"{len(failed_chunks)} 个分片处理失败",
                "failed_chunks": failed_chunks,
                "progress": self.progress.to_dict()
            }
    
    def _split_file_smart(self, file_path: str) -> List[Dict]:
        """
        智能拆分文件
        
        根据文件类型选择最佳拆分策略
        """
        file_ext = Path(file_path).suffix.lower()
        file_size = os.path.getsize(file_path)
        
        # 根据文件类型选择拆分策略
        if file_ext == '.pdf':
            return self._split_pdf(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            return self._split_excel(file_path)
        elif file_ext in ['.docx', '.doc']:
            return self._split_word(file_path)
        else:
            # 通用二进制拆分
            return self._split_binary(file_path)
    
    def _split_pdf(self, file_path: str) -> List[Dict]:
        """按页拆分 PDF"""
        try:
            import fitz
            
            doc = fitz.open(file_path)
            total_pages = len(doc)
            doc.close()
            
            # 计算每份的页数
            pages_per_chunk = max(1, total_pages // (os.path.getsize(file_path) // self.chunk_size + 1))
            
            chunks = []
            for start_page in range(0, total_pages, pages_per_chunk):
                end_page = min(start_page + pages_per_chunk, total_pages)
                chunks.append({
                    "file_path": file_path,
                    "type": "pdf_pages",
                    "start_page": start_page,
                    "end_page": end_page
                })
            
            return chunks
            
        except Exception as e:
            print(f"[LargeFileHandler] PDF 拆分失败，使用二进制拆分: {e}")
            return self._split_binary(file_path)
    
    def _split_excel(self, file_path: str) -> List[Dict]:
        """按工作表拆分 Excel"""
        try:
            import pandas as pd
            
            xl = pd.ExcelFile(file_path)
            sheet_names = xl.sheet_names
            
            chunks = []
            for sheet_name in sheet_names:
                chunks.append({
                    "file_path": file_path,
                    "type": "excel_sheet",
                    "sheet_name": sheet_name
                })
            
            return chunks
            
        except Exception as e:
            print(f"[LargeFileHandler] Excel 拆分失败，使用二进制拆分: {e}")
            return self._split_binary(file_path)
    
    def _split_word(self, file_path: str) -> List[Dict]:
        """按段落拆分 Word"""
        # Word 文档通常不大，直接作为一个分片
        return [{
            "file_path": file_path,
            "type": "word_full"
        }]
    
    def _split_binary(self, file_path: str) -> List[Dict]:
        """二进制拆分"""
        file_size = os.path.getsize(file_path)
        chunks = []
        
        for start in range(0, file_size, self.chunk_size):
            end = min(start + self.chunk_size, file_size)
            chunks.append({
                "file_path": file_path,
                "type": "binary",
                "start_byte": start,
                "end_byte": end
            })
        
        return chunks
    
    def _process_chunk(self, chunk_info: Dict, 
                      parser_func: Callable) -> Any:
        """处理单个分片"""
        chunk_type = chunk_info.get("type")
        file_path = chunk_info.get("file_path")
        
        if chunk_type == "pdf_pages":
            # PDF 按页处理
            return self._process_pdf_pages(
                file_path,
                chunk_info["start_page"],
                chunk_info["end_page"],
                parser_func
            )
        elif chunk_type == "excel_sheet":
            # Excel 按工作表处理
            return self._process_excel_sheet(
                file_path,
                chunk_info["sheet_name"],
                parser_func
            )
        else:
            # 通用处理
            return parser_func(file_path)
    
    def _process_pdf_pages(self, file_path: str, start_page: int,
                          end_page: int, parser_func: Callable) -> Any:
        """处理 PDF 页范围"""
        import fitz
        
        # 创建临时 PDF
        src_doc = fitz.open(file_path)
        new_doc = fitz.open()
        
        for page_num in range(start_page, end_page):
            new_doc.insert_pdf(src_doc, from_page=page_num, to_page=page_num)
        
        # 保存临时文件
        temp_path = f"{file_path}.temp_{start_page}_{end_page}.pdf"
        new_doc.save(temp_path)
        new_doc.close()
        src_doc.close()
        
        try:
            result = parser_func(temp_path)
        finally:
            os.remove(temp_path)
        
        return result
    
    def _process_excel_sheet(self, file_path: str, sheet_name: str,
                            parser_func: Callable) -> Any:
        """处理 Excel 工作表"""
        import pandas as pd
        
        # 读取单个工作表
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # 保存为临时文件
        temp_path = f"{file_path}.temp_{sheet_name}.xlsx"
        df.to_excel(temp_path, index=False)
        
        try:
            result = parser_func(temp_path)
        finally:
            os.remove(temp_path)
        
        return result
    
    def _merge_results(self, results: List[tuple]) -> Any:
        """合并分片结果"""
        # 按分片索引排序
        results.sort(key=lambda x: x[0])
        
        # 简单拼接（实际应根据结果类型智能合并）
        merged = []
        for idx, result in results:
            if hasattr(result, 'content'):
                merged.append(result.content)
            elif isinstance(result, str):
                merged.append(result)
            elif isinstance(result, dict):
                merged.append(str(result))
        
        return "\n".join(merged)
    
    def _get_checkpoint_path(self, file_path: str, 
                            output_dir: str = None) -> str:
        """获取 checkpoint 文件路径"""
        import hashlib
        
        file_hash = hashlib.md5(file_path.encode()).hexdigest()[:16]
        
        if output_dir:
            checkpoint_dir = Path(output_dir) / "checkpoints"
        else:
            checkpoint_dir = Path(tempfile.gettempdir()) / "local_data_ai_checkpoints"
        
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        return str(checkpoint_dir / f"{file_hash}.json")
    
    def _load_checkpoint(self, file_path: str) -> Optional[Dict]:
        """加载断点"""
        if not self.checkpoint_file:
            return None
        
        try:
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
            
            # 验证文件是否变化
            import hashlib
            current_hash = hashlib.md5(open(file_path, 'rb').read(8192)).hexdigest()
            
            if checkpoint.get('file_hash') == current_hash:
                return checkpoint
            else:
                print("[LargeFileHandler] 文件已变化，重新开始处理")
                return None
                
        except:
            return None
    
    def _save_checkpoint(self, file_path: str, last_chunk: int):
        """保存断点"""
        if not self.checkpoint_file:
            return
        
        import hashlib
        file_hash = hashlib.md5(open(file_path, 'rb').read(8192)).hexdigest()
        
        checkpoint = {
            "file_path": file_path,
            "file_hash": file_hash,
            "last_chunk": last_chunk,
            "timestamp": time.time()
        }
        
        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f)
    
    def _cleanup_checkpoint(self, file_path: str):
        """清理 checkpoint"""
        if self.checkpoint_file and os.path.exists(self.checkpoint_file):
            os.remove(self.checkpoint_file)
    
    def pause(self):
        """暂停处理"""
        self.is_running = False
        self.progress.status = "paused"
    
    def resume(self, file_path: str, parser_func: Callable):
        """恢复处理"""
        return self.process_large_file(file_path, parser_func)
    
    def get_progress(self) -> Dict:
        """获取当前进度"""
        return self.progress.to_dict()
