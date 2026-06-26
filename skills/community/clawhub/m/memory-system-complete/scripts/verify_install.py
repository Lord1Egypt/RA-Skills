#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory System Installation Verification Script
验证安装是否成功
"""

import os
import sys
import sqlite3
from datetime import datetime

def check_python_version():
    """检查Python版本"""
    print("[PYTHON] Checking Python version...")

    version = sys.version_info
    print(f"  Current: {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 7:
        print("  [OK] Python version OK (>= 3.7)")
        return True
    else:
        print("  [ERROR] Python version too old (need >= 3.7)")
        return False

def check_directory_structure():
    """检查目录结构"""
    print("\n[DIR] Checking directory structure...")

    required_dirs = [
        'memory',
        'memory/database',
        'memory/database/backups',
        'scripts',
        'examples'
    ]

    all_ok = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  [OK] {directory}")
        else:
            print(f"  [ERROR] {directory} (missing)")
            all_ok = False

    return all_ok

def check_database_file():
    """检查数据库文件"""
    print("\n[DB] Checking database file...")

    db_path = os.path.join('memory', 'database', 'xiaozhi_memory.db')

    if not os.path.exists(db_path):
        print(f"  [ERROR] Database file not found: {db_path}")
        print(f"  [INFO] Run: python scripts/init_database.py")
        return False

    print(f"  [OK] Database file exists: {db_path}")

    # 检查文件大小
    size = os.path.getsize(db_path)
    print(f"  [INFO] File size: {size} bytes")

    if size < 1000:
        print(f"  [WARN] Database seems empty or corrupted")
        return False

    return True

def check_database_structure():
    """检查数据库结构"""
    print("\n[CHECK] Checking database structure...")

    db_path = os.path.join('memory', 'database', 'xiaozhi_memory.db')

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        required_tables = ['memories', 'memory_links', 'config']
        all_ok = True

        for table in required_tables:
            if table in tables:
                print(f"  [OK] Table: {table}")
            else:
                print(f"  [ERROR] Table: {table} (missing)")
                all_ok = False

        # 检查索引
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]

        print(f"  [INFO] Indexes: {len(indexes)}")

        # 检查配置
        cursor.execute("SELECT COUNT(*) FROM config")
        config_count = cursor.fetchone()[0]
        print(f"  [INFO] Config entries: {config_count}")

        # 检查记忆数量
        cursor.execute("SELECT COUNT(*) FROM memories")
        memory_count = cursor.fetchone()[0]
        print(f"  [INFO] Memories: {memory_count}")

        conn.close()

        return all_ok

    except Exception as e:
        print(f"  [ERROR] Error checking database: {e}")
        return False

def check_lancedb():
    """检查LanceDB（可选）"""
    print("\n[CHECK] Checking LanceDB (optional)...")

    try:
        import lancedb
        print("  [OK] LanceDB package installed")

        lancedb_path = os.path.join('memory', 'database', 'lancedb')
        if os.path.exists(lancedb_path):
            print(f"  [OK] LanceDB directory exists")

            try:
                db = lancedb.connect(lancedb_path)
                print(f"  [OK] LanceDB connection successful")
                return True
            except Exception as e:
                print(f"  [WARN] LanceDB connection failed: {e}")
                return False
        else:
            print(f"  [WARN] LanceDB directory not found")
            return False

    except ImportError:
        print("  [WARN] LanceDB not installed (optional)")
        print("  [INFO] Install with: pip install lancedb")
        return False

def check_memory_system_module():
    """检查memory_system模块"""
    print("\n[MODULE] Checking memory_system module...")

    try:
        # 添加scripts目录到路径
        scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)

        from memory_system import MemorySystem

        print("  [OK] memory_system module imported")

        # 尝试初始化
        memory = MemorySystem()
        success = memory.initialize()

        if success:
            print("  [OK] MemorySystem initialized")

            # 测试基本操作
            stats = memory.stats()
            print(f"  [INFO] Total memories: {stats['total']}")

            memory.close()
            return True
        else:
            print("  [ERROR] MemorySystem initialization failed")
            return False

    except ImportError as e:
        print(f"  [ERROR] Cannot import memory_system: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] Error testing memory_system: {e}")
        return False

def check_required_files():
    """检查必需文件"""
    print("\n[FILES] Checking required files...")

    required_files = [
        'SKILL.md',
        'README.md',
        'package.json',
        'scripts/memory_system.py',
        'examples/usage_demo.py'
    ]

    all_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  [OK] {file_path} ({size} bytes)")
        else:
            print(f"  [ERROR] {file_path} (missing)")
            all_ok = False

    return all_ok

def run_test_operations():
    """运行测试操作"""
    print("\n[TEST] Running test operations...")

    try:
        # 添加scripts目录到路径
        scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)

        from memory_system import MemorySystem

        memory = MemorySystem()
        memory.initialize()

        # 测试保存
        test_id = memory.save(
            type='test',
            title='Verification Test',
            content='Testing memory system installation',
            importance=5
        )
        print(f"  [OK] Save test: ID {test_id}")

        # 测试查询
        result = memory.get(test_id)
        if result:
            print(f"  [OK] Query test: Found memory")
        else:
            print(f"  [ERROR] Query test: Failed to find memory")
            memory.close()
            return False

        # 测试更新
        memory.update(test_id, importance=7)
        print(f"  [OK] Update test: Updated importance")

        # 测试删除
        memory.delete(test_id)
        print(f"  [OK] Delete test: Deleted test memory")

        memory.close()
        return True

    except Exception as e:
        print(f"  [ERROR] Test operations failed: {e}")
        return False

def main():
    """主函数"""
    print("="*70)
    print("Memory System Installation Verification")
    print("="*70)
    print()

    # 运行所有检查
    checks = [
        ("Python Version", check_python_version),
        ("Directory Structure", check_directory_structure),
        ("Required Files", check_required_files),
        ("Database File", check_database_file),
        ("Database Structure", check_database_structure),
        ("LanceDB (Optional)", check_lancedb),
        ("Memory System Module", check_memory_system_module),
        ("Test Operations", run_test_operations)
    ]

    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            results[name] = False

    # 总结
    print("\n" + "="*70)
    print("Verification Summary")
    print("="*70)
    print()

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {name}")

    print()
    print(f"[RESULT] Result: {passed}/{total} checks passed")
    print()

    if passed == total:
        print("[SUCCESS] All checks passed! Installation is successful.")
        print()
        print("[READY] You can now use the memory system:")
        print("  from memory_system import MemorySystem")
        print("  memory = MemorySystem()")
        print("  memory.initialize()")
        print()
        return 0
    else:
        print("[WARNING] Some checks failed. Please review the errors above.")
        print()
        print("[FIX] Common fixes:")
        print("  - Run: python scripts/init_database.py")
        print("  - Install: pip install lancedb (optional)")
        print("  - Check: Python version >= 3.7")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
