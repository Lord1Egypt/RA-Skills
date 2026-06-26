#!/usr/bin/env python3
"""
Session Backup & Compact Script
用于 heartbeat 定期执行：
1. 备份会话内容到 memory-indexer
2. 精简原会话文件到 ~10KB

用法：
    python3 session_backup.py [--agents-dir PATH] [--indexer-dir PATH] [--backup-dir PATH] [--max-size KB]

选项：
    --agents-dir PATH   Agent sessions 目录 (默认: ~/.openclaw/agents/main/sessions)
    --indexer-dir PATH  memory-indexer 目录 (默认: ~/.openclaw/workspace/skills/memory-indexer)
    --backup-dir PATH   备份目录 (默认: ~/.openclaw/workspace/memory-index/session-backups)
    --max-size KB      精简后最大 KB 数 (默认: 10)
"""

import json
import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime

# 默认配置
DEFAULT_AGENTS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
DEFAULT_INDEXER_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "memory-indexer"
DEFAULT_BACKUP_DIR = Path.home() / ".openclaw" / "workspace" / "memory-index" / "session-backups"
DEFAULT_MAX_SIZE_KB = 10


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="Session Backup & Compact - 备份并精简会话文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 session_backup.py                           # 使用默认配置
    python3 session_backup.py --max-size 20            # 精简后最大 20KB
    python3 session_backup.py --agents-dir /path/to/sessions
    python3 session_backup.py --indexer-dir /path/to/indexer --backup-dir /path/to/backup
        """
    )
    parser.add_argument(
        "--agents-dir", "-a",
        type=Path,
        default=DEFAULT_AGENTS_DIR,
        help=f"Agent sessions 目录 (默认: {DEFAULT_AGENTS_DIR})"
    )
    parser.add_argument(
        "--indexer-dir", "-i",
        type=Path,
        default=DEFAULT_INDEXER_DIR,
        help=f"memory-indexer 目录 (默认: {DEFAULT_INDEXER_DIR})"
    )
    parser.add_argument(
        "--backup-dir", "-b",
        type=Path,
        default=DEFAULT_BACKUP_DIR,
        help=f"备份目录 (默认: {DEFAULT_BACKUP_DIR})"
    )
    parser.add_argument(
        "--max-size", "-s",
        type=int,
        default=DEFAULT_MAX_SIZE_KB,
        help=f"精简后最大 KB 数 (默认: {DEFAULT_MAX_SIZE_KB})"
    )
    return parser.parse_args()


# 解析命令行参数获取配置
args = parse_args()
AGENTS_DIR = args.agents_dir
MEMORY_INDEXER_DIR = args.indexer_dir
BACKUP_DIR = args.backup_dir
MAX_SIZE_KB = args.max_size


def extract_messages(jsonl_path):
    """从 JSONL 文件提取用户消息内容"""
    messages = []
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        if data.get('type') == 'message' and data.get('message', {}).get('role') == 'user':
                            content = data.get('message', {}).get('content', [])
                            for c in content:
                                if c.get('type') == 'text':
                                    text = c.get('text', '')
                                    # 去掉 System: 开头的元数据，保留真正的用户消息
                                    if text:
                                        # 找到第一个非元数据行（通常是用户的实际消息）
                                        lines = text.split('\n')
                                        real_lines = []
                                        in_metadata = True
                                        
                                        for line in lines:
                                            # 跳过 System: 开头的行
                                            if line.startswith('System:'):
                                                continue
                                            # 跳过 JSON 元数据块
                                            if line.strip().startswith('```json'):
                                                in_metadata = True
                                                continue
                                            if line.strip() == '```':
                                                in_metadata = False
                                                continue
                                            # 跳过 JSON 对象行
                                            if in_metadata and (line.strip().startswith('{') or line.strip().startswith('}') or line.strip().startswith('"')):
                                                continue
                                            # 跳过空行
                                            if not line.strip():
                                                continue
                                            
                                            real_lines.append(line)
                                        
                                        if real_lines:
                                            real_content = '\n'.join(real_lines).strip()
                                            if len(real_content) > 2:
                                                messages.append(real_content)
                    except:
                        pass
    except Exception as e:
        print(f"Error reading {jsonl_path}: {e}")
    return messages


def compact_session(jsonl_path, max_size_kb=MAX_SIZE_KB):
    """精简会话文件到指定大小"""
    file_size = jsonl_path.stat().st_size
    max_bytes = max_size_kb * 1024
    
    if file_size <= max_bytes:
        print(f"  {jsonl_path.name} already small enough ({file_size / 1024:.1f}KB)")
        return False
    
    # 读取所有内容
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 保留头部（session 元数据）和最近的对话
    # 头部通常在前几行
    header_lines = []
    message_lines = []
    
    for line in lines:
        data = json.loads(line)
        if data.get('type') == 'session':
            header_lines.append(line)
        else:
            message_lines.append(line)
    
    # 保留最近的 message_lines（从后往前）
    kept_lines = header_lines.copy()
    current_size = sum(len(l) for l in kept_lines)
    
    for line in reversed(message_lines):
        if current_size + len(line) <= max_bytes:
            kept_lines.append(line)
            current_size += len(line)
    
    # 写回
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        f.writelines(kept_lines)
    
    print(f"  Compacted {jsonl_path.name}: {file_size / 1024:.1f}KB -> {current_size / 1024:.1f}KB")
    return True


def backup_to_indexer(messages, session_name):
    """将消息添加到 memory-indexer"""
    if not messages:
        return
    
    # 合并消息内容（保留更多内容以提取更多关键词）
    content = "\n".join(messages[:100])  # 最多 100 条
    
    # 调用 memory-indexer add，使用更多关键词
    import subprocess
    cmd = [
        sys.executable,
        str(MEMORY_INDEXER_DIR / "memory-indexer.py"),
        "add",
        content,
        "session-backup",
        session_name,
        "--keywords", "20"  # 提取更多关键词
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"  ✓ Added to indexer: {len(messages)} messages, {len(content)} chars")
        else:
            print(f"  ✗ Indexer error: {result.stderr}")
    except Exception as e:
        print(f"  ✗ Failed to add to indexer: {e}")


def main():
    print("🔄 Session Backup & Compact")
    print("=" * 40)
    
    # 确保备份目录存在
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    # 获取所有会话文件
    sessions = sorted(AGENTS_DIR.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"Found {len(sessions)} session files")
    
    # 只处理最近的 3 个会话（避免处理太多）
    for session in sessions[:3]:
        print(f"\n📄 Processing: {session.name}")
        
        # 提取消息
        messages = extract_messages(session)
        print(f"  Found {len(messages)} user messages")
        
        if messages:
            # 备份到 indexer
            session_name = session.stem[:8]  # 取前 8 位作为名称
            backup_to_indexer(messages, session_name)
        
        # 精简文件
        compact_session(session)
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
