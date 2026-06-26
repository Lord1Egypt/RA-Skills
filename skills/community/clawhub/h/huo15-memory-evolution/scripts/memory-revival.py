#!/usr/bin/env python3
"""
记忆读取器
读取记忆时自动检查并唤醒 stale 记忆
"""
import os
import sys

# 导入唤醒模块
sys.path.insert(0, os.path.dirname(__file__))
from memory_revival import check_and_revive, is_stale

def read_memory(relative_path):
    """
    读取记忆文件
    如果是 stale 状态，自动唤醒
    """
    workspace = os.path.expanduser('~/.openclaw/workspace')
    full_path = os.path.join(workspace, relative_path)
    
    if not os.path.exists(full_path):
        print(f"文件不存在: {relative_path}")
        return None
    
    # 检查是否是 stale
    was_stale = is_stale(full_path)
    
    # 如果是 stale，自动唤醒
    if was_stale:
        result = check_and_revive(relative_path)
        if result:
            print(f"🔄 已唤醒: {relative_path}")
    
    # 读取内容
    with open(full_path, 'r') as f:
        content = f.read()
    
    return content

def main():
    if len(sys.argv) < 2:
        print("用法: memory-read.py <memory-path>")
        print("示例: memory-read.py memory/user/test.md")
        return
    
    path = sys.argv[1]
    content = read_memory(path)
    
    if content:
        print(content)
    else:
        print(f"❌ 无法读取: {path}")

if __name__ == '__main__':
    main()
