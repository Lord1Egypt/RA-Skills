#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大文件处理器 - 命令行接口

使用方法:
    python handle_file.py "文件路径" --user-id "用户 ID" --channel "渠道"

示例:
    python handle_file.py "C:/Users/test/document.pdf" --user-id "ou_xxx" --channel "feishu"
"""

import sys
import os
import argparse
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# 工作目录
WORKSPACE = Path("E:/ai/openclaw/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "large-file-handler"
TMP_DIR = WORKSPACE / "tmp" / "files"

# 配置
LARGE_FILE_THRESHOLD = 10 * 1024 * 1024  # 10MB
MAX_FILE_SIZE = 500 * 1024 * 1024        # 500MB

# 文件类型映射
FILE_HANDLERS = {
    '.pdf': 'pdf-processor.py',
    '.mp4': 'video-processor.py',
    '.mov': 'video-processor.py',
    '.avi': 'video-processor.py',
    '.jpg': 'image-processor.py',
    '.jpeg': 'image-processor.py',
    '.png': 'image-processor.py',
    '.webp': 'image-processor.py',
    '.log': 'log-processor.py',
    '.txt': 'text-processor.py',
    '.docx': 'office-processor.py',
    '.pptx': 'office-processor.py',
    '.xlsx': 'office-processor.py',
    '.zip': 'archive-processor.py',
    '.rar': 'archive-processor.py',
    '.7z': 'archive-processor.py',
}


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_handler(file_path: Path) -> str:
    """获取处理器脚本名称"""
    ext = file_path.suffix.lower()
    return FILE_HANDLERS.get(ext, 'generic_processor.py')


def ensure_dirs():
    """确保目录存在"""
    for subdir in ['pending', 'processing', 'completed']:
        (TMP_DIR / subdir).mkdir(parents=True, exist_ok=True)


def process_file(file_path: str, user_id: str, channel: str):
    """处理文件"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"错误：文件不存在 - {file_path}")
        sys.exit(1)
    
    # 检查文件大小
    file_size = file_path.stat().st_size
    
    if file_size > MAX_FILE_SIZE:
        print(f"错误：文件过大 ({format_size(file_size)})，最大支持 {format_size(MAX_FILE_SIZE)}")
        sys.exit(1)
    
    # 确保目录存在
    ensure_dirs()
    
    # 生成目标路径
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_name = f"{timestamp}_{file_path.name}"
    pending_path = TMP_DIR / "pending" / dest_name
    
    # 复制文件到 pending 目录
    print(f"保存文件到：{pending_path}")
    shutil.copy2(str(file_path), str(pending_path))
    
    # 获取处理器
    handler_name = get_handler(file_path)
    handler_path = SKILL_DIR / handler_name
    
    is_async = file_size > LARGE_FILE_THRESHOLD
    
    if is_async:
        # 异步处理
        print(f"\n[ASYNC] 大文件模式：{format_size(file_size)}")
        print(f"处理器：{handler_name}")
        print(f"状态：后台处理中...")
        print(f"\n提示：处理完成后会推送结果到 {channel}")
        
        # 启动后台进程
        if handler_path.exists():
            subprocess.Popen([
                sys.executable, str(handler_path),
                '--file', str(pending_path),
                '--user-id', user_id,
                '--channel', channel
            ], cwd=str(SKILL_DIR))
        else:
            # 使用通用处理器
            subprocess.Popen([
                sys.executable, str(SKILL_DIR / 'generic_processor.py'),
                '--file', str(pending_path),
                '--handler', handler_name.replace('.py', ''),
                '--user-id', user_id,
                '--channel', channel
            ], cwd=str(SKILL_DIR))
        
        # 立即返回确认消息
        print(f"\n[OK] 收到文件「{file_path.name}」（{format_size(file_size)}）")
        print(f"正在后台处理，完成后发你结果")
        
    else:
        # 同步处理
        print(f"\n[SYNC] 小文件模式：{format_size(file_size)}")
        print(f"处理器：{handler_name}")
        
        # 直接处理（简化示例）
        print(f"\n[OK] 文件「{file_path.name}」处理完成")
        print(f"大小：{format_size(file_size)}")
        print(f"类型：{file_path.suffix}")


def main():
    parser = argparse.ArgumentParser(description='大文件处理器')
    parser.add_argument('file', help='文件路径')
    parser.add_argument('--user-id', required=True, help='用户 ID')
    parser.add_argument('--channel', default='feishu', help='通信渠道')
    
    args = parser.parse_args()
    
    process_file(args.file, args.user_id, args.channel)


if __name__ == '__main__':
    main()
