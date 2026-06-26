#!/usr/bin/env python3
"""
记忆唤醒器
当被标记为 stale 的记忆被访问时，自动唤醒（复活）它
"""
import os
import sys
import json
from datetime import datetime

def get_memory_path(relative_path):
    """获取记忆文件的完整路径"""
    workspace = os.path.expanduser('~/.openclaw/workspace')
    return os.path.join(workspace, relative_path)

def is_stale(memory_file):
    """检查记忆是否被标记为 stale"""
    if not os.path.exists(memory_file):
        return False
    
    with open(memory_file, 'r') as f:
        content = f.read()
    
    return 'status: stale' in content or 'status:old' in content

def revive_memory(relative_path):
    """
    唤醒记忆：移除 stale 标记，更新访问时间
    """
    full_path = get_memory_path(relative_path)
    
    if not os.path.exists(full_path):
        return None
    
    # 读取内容
    with open(full_path, 'r') as f:
        content = f.read()
    
    # 检查是否是 stale
    if 'status: stale' not in content and 'status:old' not in content:
        return None  # 不是 stale，不需要唤醒
    
    # 移除 stale 标记
    lines = content.split('\n')
    new_lines = []
    stale_removed = False
    
    for line in lines:
        if line.strip() == 'status: stale' or line.strip() == 'status:old':
            stale_removed = True
            continue  # 跳过这一行
        new_lines.append(line)
    
    # 更新 updated 时间
    today = datetime.now().strftime('%Y-%m-%d')
    for i, line in enumerate(new_lines):
        if line.strip().startswith('updated:'):
            new_lines[i] = f'updated: {today}'
            break
    
    # 写回文件
    with open(full_path, 'w') as f:
        f.write('\n'.join(new_lines))
    
    return {
        'path': relative_path,
        'revived': True,
        'date': today
    }

def check_and_revive(relative_path):
    """
    检查并唤醒（如果需要）
    返回唤醒结果
    """
    full_path = get_memory_path(relative_path)
    
    # 检查是否是 stale
    if not is_stale(full_path):
        return None
    
    # 唤醒
    return revive_memory(relative_path)

def revive_all_stale():
    """
    检查所有记忆文件，唤醒所有 stale 的记忆
    """
    workspace = os.path.expanduser('~/.openclaw/workspace/memory')
    revived = []
    
    for root, dirs, files in os.walk(workspace):
        for filename in files:
            if filename.endswith('.md') and filename != 'index.json':
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, workspace)
                
                if is_stale(full_path):
                    result = revive_memory(relative_path)
                    if result:
                        revived.append(result)
    
    return revived

def main():
    if len(sys.argv) < 2:
        # 无参数：检查并唤醒所有 stale 记忆
        print("🔍 检查所有 stale 记忆...")
        revived = revive_all_stale()
        
        if revived:
            print(f"\n✅ 唤醒了 {len(revived)} 个记忆:")
            for r in revived:
                print(f"   - {r['path']}")
        else:
            print("没有需要唤醒的记忆")
        return
    
    command = sys.argv[1]
    
    if command == 'check' and len(sys.argv) >= 3:
        # 检查单个记忆
        path = sys.argv[2]
        full_path = get_memory_path(path)
        
        if is_stale(full_path):
            print(f"🔴 {path} 是 stale 状态")
        else:
            print(f"🟢 {path} 是活跃状态")
    
    elif command == 'revive' and len(sys.argv) >= 3:
        # 唤醒单个记忆
        path = sys.argv[2]
        result = check_and_revive(path)
        
        if result:
            print(f"✅ 已唤醒: {path}")
        else:
            print(f"⚠️  {path} 不需要唤醒")
    
    elif command == 'list':
        # 列出所有 stale 记忆
        print("📋 所有 stale 记忆:")
        workspace = os.path.expanduser('~/.openclaw/workspace/memory')
        stale_count = 0
        
        for root, dirs, files in os.walk(workspace):
            for filename in files:
                if filename.endswith('.md'):
                    full_path = os.path.join(root, filename)
                    if is_stale(full_path):
                        relative_path = os.path.relpath(full_path, workspace)
                        print(f"   🔴 {relative_path}")
                        stale_count += 1
        
        if stale_count == 0:
            print("   没有 stale 记忆")
        else:
            print(f"\n共 {stale_count} 个 stale 记忆")
    
    else:
        print("用法:")
        print("  python memory-revive.py              # 检查并唤醒所有 stale 记忆")
        print("  python memory-revive.py list          # 列出所有 stale 记忆")
        print("  python memory-revive.py check <path> # 检查单个记忆")
        print("  python memory-revive.py revive <path> # 唤醒单个记忆")

if __name__ == '__main__':
    main()
