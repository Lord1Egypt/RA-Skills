import os
import sqlite3
import re
import datetime
from pathlib import Path

# 文件路径
MEMORY_MD = '/home/awu/.openclaw/workspace-work/MEMORY.md'
MEMORY_DB = '/home/awu/.openclaw/workspace-work/memory.db'

# 检查 MEMORY.md 是否有更新
last_modified_db = Path(MEMORY_DB).stat().st_mtime if Path(MEMORY_DB).exists() else 0
last_modified_md = Path(MEMORY_MD).stat().st_mtime if Path(MEMORY_MD).exists() else 0

if last_modified_md > last_modified_db:
    print('🔄 MEMORY.md 已更新，正在同步到 memory.db...')
    
    # 读取 MEMORY.md
    with open(MEMORY_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按 '### ' 分割主题块
    blocks = re.split(r'\n### ', content)
    
    # 创建或连接数据库
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        created_at TEXT
    )
    ''')
    
    # 清空旧数据（或可选：只更新变化）
    cursor.execute('DELETE FROM memories')
    
    # 插入新数据
    for block in blocks[1:]:
        lines = block.split('\n', 1)
        if len(lines) < 2:
            continue
        title = lines[0].strip()
        content = '\n'.join([line.strip() for line in lines[1].split('\n') if line.strip()])
        
        cursor.execute('''
        INSERT INTO memories (title, content, created_at)
        VALUES (?, ?, ?)
        ''', (title, content, datetime.datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print('✅ memory.db 已更新。')
else:
    print('✅ memory.db 已是最新的，无需同步。')