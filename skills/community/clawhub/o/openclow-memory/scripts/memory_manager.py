#!/usr/bin/env python3
"""
记忆管理脚本
- 本地文件保留7天
- 超过7天的移动到 PostgreSQL 数据库
"""

import os
import sqlite3
import subprocess
from datetime import datetime, timedelta

MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,  # Postgres.app 默认端口
    "user": "damien",
    "database": "postgres"
}

def get_files_older_than(days=7):
    """获取指定天数之前的文件"""
    cutoff = datetime.now() - timedelta(days=days)
    old_files = []
    
    for root, dirs, files in os.walk(MEMORY_DIR):
        # 跳过子目录
        if "project-context" in root or "preferences" in root or "reference" in root:
            continue
            
        for f in files:
            if f.endswith(".md"):
                filepath = os.path.join(root, f)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if mtime < cutoff:
                    old_files.append(filepath)
    
    return old_files

def import_to_database(filepath):
    """将文件内容导入到数据库"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    
    # 使用 psql 导入
    cmd = [
        "psql", "-h", DB_CONFIG["host"], "-p", str(DB_CONFIG["port"]),
        "-U", DB_CONFIG["user"], "-d", DB_CONFIG["database"],
        "-c", f"INSERT INTO memory_structured (category, title, content) VALUES ('archived', '{filename}', {repr(content)});"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    print(f"检查 {MEMORY_DIR} 中的旧文件...")
    
    # 查找7天前的文件
    old_files = get_files_older_than(7)
    
    if not old_files:
        print("没有需要归档的文件")
        return
    
    print(f"找到 {len(old_files)} 个文件需要归档:")
    for f in old_files:
        print(f"  - {f}")
    
    # 导入到数据库
    for f in old_files:
        if import_to_database(f):
            print(f"✓ 已导入: {f}")
            # 可选：删除本地文件
            # os.remove(f)
        else:
            print(f"✗ 导入失败: {f}")

if __name__ == "__main__":
    main()
