#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证安装 v2.0
Verify Installation v2.0
"""

import sqlite3
import os
import sys

def verify_database(db_path):
    """验证数据库"""
    if not os.path.exists(db_path):
        print(f"[X] Database file not found: {db_path}")
        return False

    print(f"[OK] Database file exists: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    expected_tables = [
        'memories',
        'causal_relations',
        'knowledge_relations',
        'memory_associations',
        'memory_communities',
        'graph_insights',
        'review_queue',
        'deep_research',
        'ingestion_cache',
        'retrieval_history',
        'evolution_log'
    ]

    print("\n[Tables]")
    all_ok = True
    for table in expected_tables:
        if table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  [OK] {table} ({count} records)")
        else:
            print(f"  [X] {table} (not found)")
            all_ok = False

    conn.close()
    return all_ok

def verify_scripts():
    """验证脚本"""
    print("\n[Scripts]")
    scripts = [
        'memory_system_v2.py',
        'init_database_v2.py',
        'causal_knowledge_graphs.py',
        'auto_relation_detector.py'
    ]

    all_ok = True
    for script in scripts:
        script_path = f"scripts/{script}"
        if os.path.exists(script_path):
            print(f"  [OK] {script}")
        else:
            print(f"  [X] {script} (not found)")
            all_ok = False

    return all_ok

def verify_python_version():
    """验证Python版本"""
    print("\n[Python Version]")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 7:
        print(f"  [OK] Python version >= 3.7")
        return True
    else:
        print(f"  [X] Python version < 3.7")
        return False

def verify_optional_dependencies():
    """验证可选依赖"""
    print("\n[Optional Dependencies]")

    dependencies = {
        'lancedb': 'LanceDB (vector search)',
        'sentence_transformers': 'Sentence Transformers (embeddings)',
        'networkx': 'NetworkX (graph analysis)'
    }

    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"  [OK] {description}")
        except ImportError:
            print(f"  [ ] {description} (optional)")

    return True

def run_test():
    """运行测试"""
    print("\n[Test]")
    try:
        from scripts.memory_system_v2 import MemorySystemV2

        memory = MemorySystemV2()
        success = memory.initialize()

        if success:
            print("  [OK] MemorySystemV2 initialized")

            # 保存测试记忆
            test_id = memory.save(
                type='test',
                title='Installation Test v2.0',
                content='Testing memory system v2.0 installation',
                importance=5
            )

            print(f"  [OK] Saved test memory (ID: {test_id})")

            # 获取记忆
            result = memory.get(test_id)
            if result:
                print(f"  [OK] Retrieved test memory")
            else:
                print(f"  [X] Failed to retrieve test memory")
                return False

            # 搜索记忆
            results = memory.search('test')
            if len(results) > 0:
                print(f"  [OK] Search working (found {len(results)} results)")
            else:
                print(f"  [X] Search failed")
                return False

            # 清理
            memory.delete(test_id)
            print(f"  [OK] Cleaned up test memory")

            return True
        else:
            print(f"  [X] MemorySystemV2 initialization failed")
            return False
    except Exception as e:
        print(f"  [X] Test failed: {e}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("Verify Memory System Installation v2.0")
    print("="*60)
    print("")

    db_path = "memory/database/xiaozhi_memory.db"

    # 1. 验证Python版本
    python_ok = verify_python_version()

    # 2. 验证脚本
    scripts_ok = verify_scripts()

    # 3. 验证数据库
    database_ok = verify_database(db_path)

    # 4. 验证可选依赖
    dependencies_ok = verify_optional_dependencies()

    # 5. 运行测试
    test_ok = run_test()

    # 总结
    print("\n" + "="*60)
    print("Verification Summary")
    print("="*60)
    print(f"Python Version: {'[OK]' if python_ok else '[X]'}")
    print(f"Scripts: {'[OK]' if scripts_ok else '[X]'}")
    print(f"Database: {'[OK]' if database_ok else '[X]'}")
    print(f"Optional Dependencies: {'[OK]' if dependencies_ok else '[ ]'}")
    print(f"Test: {'[OK]' if test_ok else '[X]'}")
    print("")

    all_ok = python_ok and scripts_ok and database_ok and test_ok

    if all_ok:
        print("✅ Installation verified successfully!")
        print("\nYou can now use Memory System v2.0:")
        print("  from scripts.memory_system_v2 import MemorySystemV2")
        print("  memory = MemorySystemV2()")
        print("  memory.initialize()")
    else:
        print("❌ Installation verification failed!")
        print("\nPlease check the errors above and try again.")

    print("="*60)

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
