#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
large-file-handler - 大文件异步处理核心模块

功能：
1. 流式保存文件到磁盘
2. 根据文件大小决定同步/异步处理
3. 启动后台任务处理大文件
4. 推送处理结果给用户
"""

import os
import sys
import json
import shutil
import subprocess
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple

# 配置
WORKSPACE = Path(r"E:\ai\openclaw\.openclaw\workspace")
TMP_DIR = WORKSPACE / "tmp" / "files"
PENDING_DIR = TMP_DIR / "pending"
PROCESSING_DIR = TMP_DIR / "processing"
COMPLETED_DIR = TMP_DIR / "completed"

# 阈值配置（字节）
LARGE_FILE_THRESHOLD = 10 * 1024 * 1024  # 10MB
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
CHUNK_SIZE = 5 * 1024 * 1024  # 5MB 分块
RETENTION_HOURS = 24  # 完成文件保留时间

# 文件类型映射
FILE_HANDLERS = {
    '.pdf': 'pdf-processor',
    '.mp4': 'video-processor',
    '.mov': 'video-processor',
    '.avi': 'video-processor',
    '.jpg': 'image-processor',
    '.jpeg': 'image-processor',
    '.png': 'image-processor',
    '.webp': 'image-processor',
    '.log': 'log-processor',
    '.txt': 'text-processor',
    '.docx': 'office-processor',
    '.pptx': 'office-processor',
    '.xlsx': 'office-processor',
    '.zip': 'archive-processor',
    '.rar': 'archive-processor',
    '.7z': 'archive-processor',
}


def ensure_dirs():
    """确保所有目录存在"""
    for dir_path in [PENDING_DIR, PROCESSING_DIR, COMPLETED_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)


def get_file_hash(file_path: Path) -> str:
    """计算文件 MD5 哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def format_size(size_bytes: int) -> str:
    """格式化文件大小显示"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_handler_type(file_path: Path) -> Optional[str]:
    """根据文件扩展名获取处理器类型"""
    ext = file_path.suffix.lower()
    return FILE_HANDLERS.get(ext)


def save_file_stream(file_stream, file_name: str) -> Tuple[Path, int]:
    """
    流式保存文件到 pending 目录
    
    Args:
        file_stream: 文件流对象
        file_name: 文件名
    
    Returns:
        (文件路径，文件大小)
    """
    ensure_dirs()
    
    # 生成唯一文件名（避免冲突）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{timestamp}_{file_name}"
    dest_path = PENDING_DIR / safe_name
    
    # 流式写入
    total_size = 0
    with open(dest_path, 'wb') as f:
        while True:
            chunk = file_stream.read(CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)
            total_size += len(chunk)
    
    return dest_path, total_size


def acquire_lock(file_path: Path) -> bool:
    """
    获取文件处理锁
    
    Returns:
        True 如果成功获取锁，False 如果已被其他进程处理
    """
    lock_file = file_path.with_suffix(file_path.suffix + '.lock')
    try:
        with open(lock_file, 'x') as f:
            f.write(str(os.getpid()))
        return True
    except FileExistsError:
        return False


def release_lock(file_path: Path):
    """释放文件处理锁"""
    lock_file = file_path.with_suffix(file_path.suffix + '.lock')
    if lock_file.exists():
        lock_file.unlink()


def start_async_task(file_path: Path, handler_type: str, user_id: str, channel: str):
    """
    启动异步处理任务
    
    Args:
        file_path: 文件路径
        handler_type: 处理器类型
        user_id: 用户 ID
        channel: 通信渠道
    """
    # 移动文件到 processing 目录
    processing_path = PROCESSING_DIR / file_path.name
    shutil.move(str(file_path), str(processing_path))
    
    # 创建锁文件
    acquire_lock(processing_path)
    
    # 启动独立子进程
    script_path = Path(__file__).parent / "processors" / f"{handler_type}.py"
    
    if script_path.exists():
        subprocess.Popen([
            sys.executable, str(script_path),
            '--file', str(processing_path),
            '--user-id', user_id,
            '--channel', channel
        ], cwd=str(WORKSPACE), 
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0)
    else:
        # 如果处理器脚本不存在，使用通用处理器
        subprocess.Popen([
            sys.executable, str(Path(__file__).parent / "generic_processor.py"),
            '--file', str(processing_path),
            '--handler', handler_type,
            '--user-id', user_id,
            '--channel', channel
        ], cwd=str(WORKSPACE),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0)


def handle_file(file_stream, file_name: str, user_id: str, channel: str = 'feishu') -> Dict:
    """
    主处理函数
    
    Args:
        file_stream: 文件流
        file_name: 文件名
        user_id: 用户 ID
        channel: 通信渠道
    
    Returns:
        处理结果字典
    """
    # 保存文件
    file_path, file_size = save_file_stream(file_stream, file_name)
    
    # 检查文件大小
    if file_size > MAX_FILE_SIZE:
        file_path.unlink()  # 删除文件
        return {
            'success': False,
            'error': f'文件过大（{format_size(file_size)}），最大支持 {format_size(MAX_FILE_SIZE)}'
        }
    
    # 获取处理器类型
    handler_type = get_handler_type(file_path)
    if not handler_type:
        handler_type = 'generic-processor'
    
    # 决定同步还是异步
    is_async = file_size > LARGE_FILE_THRESHOLD
    
    if is_async:
        # 异步模式
        start_async_task(file_path, handler_type, user_id, channel)
        return {
            'success': True,
            'async': True,
            'file_name': file_name,
            'file_size': format_size(file_size),
            'message': f'收到文件「{file_name}」（{format_size(file_size)}），正在后台处理，完成后发你结果 🦁'
        }
    else:
        # 同步模式 - 直接处理
        # 这里简化处理，实际应该调用处理器
        return {
            'success': True,
            'async': False,
            'file_name': file_name,
            'file_size': format_size(file_size),
            'handler': handler_type,
            'message': f'正在处理文件「{file_name}」（{format_size(file_size)}）...'
        }


def cleanup_old_files():
    """清理超过保留时间的已完成文件"""
    if not COMPLETED_DIR.exists():
        return
    
    cutoff = datetime.now() - timedelta(hours=RETENTION_HOURS)
    
    for file_path in COMPLETED_DIR.iterdir():
        if file_path.is_file():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime < cutoff:
                file_path.unlink()
                print(f"清理过期文件：{file_path.name}")


if __name__ == '__main__':
    # 测试代码
    print("大文件处理器已就绪")
    print(f"工作目录：{WORKSPACE}")
    print(f"临时目录：{TMP_DIR}")
    print(f"大文件阈值：{format_size(LARGE_FILE_THRESHOLD)}")
    print(f"最大文件大小：{format_size(MAX_FILE_SIZE)}")
