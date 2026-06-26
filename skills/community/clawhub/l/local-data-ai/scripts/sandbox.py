#!/usr/bin/env python3
"""
安全沙箱模块
提供隔离的文件处理环境，防止数据泄露
"""

import os
import sys
import shutil
import tempfile
import hashlib
from typing import Dict, Optional, Any
from pathlib import Path
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SandboxConfig:
    """沙箱配置"""
    isolate_filesystem: bool = True
    restrict_network: bool = True
    max_memory_mb: int = 2048
    temp_data_ttl: int = 3600  # 临时数据存活时间（秒）
    auto_cleanup: bool = True


class SecureSandbox:
    """
    安全沙箱
    隔离文件处理环境，保障数据安全
    """
    
    def __init__(self, config: SandboxConfig = None, 
                 sandbox_id: str = None):
        """
        初始化沙箱
        
        Args:
            config: 沙箱配置
            sandbox_id: 沙箱标识（可选）
        """
        self.config = config or SandboxConfig()
        self.sandbox_id = sandbox_id or self._generate_sandbox_id()
        self.base_dir = Path(tempfile.gettempdir()) / "local_data_ai_sandbox" / self.sandbox_id
        self.work_dir = self.base_dir / "work"
        self.input_dir = self.base_dir / "input"
        self.output_dir = self.base_dir / "output"
        self.log_dir = self.base_dir / "logs"
        
        self.is_active = False
        self.created_at = None
        self.processed_files = []
    
    def _generate_sandbox_id(self) -> str:
        """生成沙箱 ID"""
        import uuid
        return f"sb_{uuid.uuid4().hex[:12]}_{int(datetime.now().timestamp())}"
    
    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        if self.config.auto_cleanup:
            self.stop()
        return False
    
    def start(self):
        """启动沙箱"""
        if self.is_active:
            return
        
        # 创建沙箱目录
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.is_active = True
        self.created_at = datetime.now()
        
        print(f"[SecureSandbox] 沙箱 {self.sandbox_id} 已启动")
        print(f"[SecureSandbox] 工作目录: {self.base_dir}")
    
    def stop(self):
        """停止沙箱并清理"""
        if not self.is_active:
            return
        
        # 清理临时数据
        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)
        
        self.is_active = False
        print(f"[SecureSandbox] 沙箱 {self.sandbox_id} 已停止并清理")
    
    def process_file(self, file_path: str, processor_func, 
                     *args, **kwargs) -> Any:
        """
        在沙箱中处理文件
        
        Args:
            file_path: 原始文件路径
            processor_func: 处理函数
            *args, **kwargs: 处理函数参数
            
        Returns:
            处理结果
        """
        if not self.is_active:
            raise RuntimeError("沙箱未启动，请先调用 start()")
        
        # 复制文件到沙箱输入目录
        src_path = Path(file_path)
        sandbox_input = self.input_dir / src_path.name
        shutil.copy2(file_path, sandbox_input)
        
        # 记录文件处理
        file_hash = self._calculate_file_hash(file_path)
        self.processed_files.append({
            "original_path": file_path,
            "sandbox_path": str(sandbox_input),
            "file_hash": file_hash,
            "processed_at": datetime.now().isoformat()
        })
        
        try:
            # 在沙箱中执行处理
            result = processor_func(str(sandbox_input), *args, **kwargs)
            
            # 记录成功
            self._log_operation("process_file", "success", {
                "file": file_path,
                "hash": file_hash
            })
            
            return result
            
        except Exception as e:
            # 记录失败
            self._log_operation("process_file", "failed", {
                "file": file_path,
                "error": str(e)
            })
            raise
    
    def read_output(self, output_filename: str) -> Optional[str]:
        """
        读取沙箱输出文件
        
        Args:
            output_filename: 输出文件名
            
        Returns:
            文件内容，不存在返回 None
        """
        output_path = self.output_dir / output_filename
        
        if not output_path.exists():
            return None
        
        with open(output_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def write_output(self, filename: str, content: str):
        """
        写入沙箱输出文件
        
        Args:
            filename: 输出文件名
            content: 文件内容
        """
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def get_work_dir(self) -> Path:
        """获取沙箱工作目录"""
        return self.work_dir
    
    def get_input_dir(self) -> Path:
        """获取沙箱输入目录"""
        return self.input_dir
    
    def get_output_dir(self) -> Path:
        """获取沙箱输出目录"""
        return self.output_dir
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """计算文件哈希"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _log_operation(self, operation: str, status: str, 
                       metadata: Dict = None):
        """记录操作日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "sandbox_id": self.sandbox_id,
            "operation": operation,
            "status": status,
            "metadata": metadata or {}
        }
        
        log_file = self.log_dir / "operations.log"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{log_entry}\n")
    
    def get_statistics(self) -> Dict:
        """获取沙箱统计信息"""
        return {
            "sandbox_id": self.sandbox_id,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "processed_files_count": len(self.processed_files),
            "processed_files": self.processed_files,
            "base_dir": str(self.base_dir),
            "config": {
                "isolate_filesystem": self.config.isolate_filesystem,
                "restrict_network": self.config.restrict_network,
                "max_memory_mb": self.config.max_memory_mb
            }
        }


@contextmanager
def temporary_sandbox(config: SandboxConfig = None):
    """
    临时沙箱上下文管理器
    
    Usage:
        with temporary_sandbox() as sandbox:
            result = sandbox.process_file("document.pdf", parse_func)
    """
    sandbox = SecureSandbox(config=config)
    try:
        sandbox.start()
        yield sandbox
    finally:
        sandbox.stop()
