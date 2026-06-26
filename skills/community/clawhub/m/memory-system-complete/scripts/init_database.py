#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory System Database Initialization Script
自动初始化数据库和目录结构
"""

import os
import sys
import sqlite3
from datetime import datetime

def create_directory_structure():
    """创建必要的目录结构"""
    print("[DIR] Creating directory structure...")
    
    directories = [
        'memory',
        'memory/database',
        'memory/database/backups',
        'memory/database/backups/daily',
        'memory/database/backups/weekly'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  [OK] Created: {directory}")
        else:
            print(f"  [OK] Exists: {directory}")
    
    return True

def initialize_sqlite_database(db_path):
    """初始化SQLite数据库"""
    print(f"\n[DB] Initializing SQLite database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 创建主记忆表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                category TEXT,
                tags TEXT,
                importance INTEGER DEFAULT 5,
                confidence REAL DEFAULT 0.8,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("  [OK] Created table: memories")
        
        # 创建索引
        indexes = [
            ('idx_type', 'type'),
            ('idx_category', 'category'),
            ('idx_importance', 'importance'),
            ('idx_created_at', 'created_at')
        ]
        
        for index_name, column in indexes:
            cursor.execute(f'CREATE INDEX IF NOT EXISTS {index_name} ON memories({column})')
            print(f"  [OK] Created index: {index_name}")
        
        # 创建记忆链接表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id_1 INTEGER,
                memory_id_2 INTEGER,
                link_type TEXT,
                strength REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (memory_id_1) REFERENCES memories(id),
                FOREIGN KEY (memory_id_2) REFERENCES memories(id)
            )
        ''')
        print("  [OK] Created table: memory_links")
        
        # 创建配置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("  [OK] Created table: config")
        
        # 插入默认配置
        default_config = {
            'version': '1.0.0',
            'initialized_at': datetime.now().isoformat(),
            'min_confidence': '0.3',
            'cleanup_interval_days': '90'
        }
        
        for key, value in default_config.items():
            cursor.execute('''
                INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)
            ''', (key, value))
        
        print("  [OK] Inserted default configuration")
        
        conn.commit()
        conn.close()
        
        print(f"\n[OK] SQLite database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error initializing SQLite database: {e}")
        return False

def check_lancedb():
    """检查LanceDB是否可用"""
    print(f"\n[CHECK] Checking LanceDB availability...")
    
    try:
        import lancedb
        print("  [OK] LanceDB is installed")
        
        # 尝试连接
        lancedb_path = 'memory/database/lancedb'
        if not os.path.exists(lancedb_path):
            os.makedirs(lancedb_path)
            print(f"  [OK] Created LanceDB directory: {lancedb_path}")
        
        db = lancedb.connect(lancedb_path)
        print("  [OK] LanceDB connection successful")
        
        return True
        
    except ImportError:
        print("  [WARN] LanceDB not installed (optional)")
        print("  [INFO] Install with: pip install lancedb")
        return False
    except Exception as e:
        print(f"  [WARN] LanceDB error: {e}")
        return False

def create_sample_data(db_path):
    """创建示例数据（可选）"""
    print(f"\n[DATA] Creating sample data...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查是否已有数据
        cursor.execute('SELECT COUNT(*) FROM memories')
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"  [INFO] Database already has {count} memories")
            print(f"  [SKIP] Skipping sample data creation")
            conn.close()
            return True
        
        # 创建示例记忆
        sample_memories = [
            {
                'type': 'learning',
                'title': 'Memory System Installation',
                'content': 'Successfully installed the memory system with SQLite and optional LanceDB support',
                'category': 'milestone',
                'tags': ['installation', 'memory', 'system'],
                'importance': 8
            },
            {
                'type': 'preference',
                'title': 'Default Configuration',
                'content': 'Using default configuration: min_confidence=0.3, cleanup_interval_days=90',
                'category': 'config',
                'tags': ['config', 'default'],
                'importance': 5
            }
        ]
        
        for mem in sample_memories:
            import json
            tags_json = json.dumps(mem['tags'])
            
            cursor.execute('''
                INSERT INTO memories (type, title, content, category, tags, importance)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (mem['type'], mem['title'], mem['content'], 
                  mem['category'], tags_json, mem['importance']))
        
        conn.commit()
        conn.close()
        
        print(f"  [OK] Created {len(sample_memories)} sample memories")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Error creating sample data: {e}")
        return False

def main():
    """主函数"""
    print("="*70)
    print("Memory System Database Initialization")
    print("="*70)
    print()
    
    # 获取数据库路径
    db_path = os.path.join('memory', 'database', 'xiaozhi_memory.db')
    
    # 1. 创建目录结构
    if not create_directory_structure():
        print("\n❌ Failed to create directory structure")
        sys.exit(1)
    
    # 2. 初始化SQLite数据库
    if not initialize_sqlite_database(db_path):
        print("\n❌ Failed to initialize SQLite database")
        sys.exit(1)
    
    # 3. 检查LanceDB（可选）
    lancedb_available = check_lancedb()
    
    # 4. 创建示例数据
    if not create_sample_data(db_path):
        print("\n⚠️  Warning: Failed to create sample data")
    
    # 5. 完成
    print("\n[OK] Initialization Complete!")
    print("="*70)
    print()
    print("[SUMMARY] Summary:")
    print(f"  - Database: {db_path}")
    print(f"  - SQLite: [OK] Ready")
    print(f"  - LanceDB: {'[OK] Ready' if lancedb_available else '[WARN] Not installed (optional)'}")
    print()
    print("[NEXT] Next steps:")
    print("  1. Run verification: python scripts/verify_install.py")
    print("  2. Start using: from memory_system import MemorySystem")
    print()
    print("[TIP] Tip: Install LanceDB for vector search:")
    print("  pip install lancedb sentence-transformers")
    print()

if __name__ == "__main__":
    main()
