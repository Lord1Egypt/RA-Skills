#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Memory System - Installation Verification (ASCII Safe)
完整记忆系统 - 安装验证脚本（ASCII安全版本）
"""

import sqlite3
import os
import sys
from datetime import datetime
from typing import Dict

def verify_installation(db_path: str = "memory/database/xiaozhi_memory.db") -> Dict:
    """
    验证完整记忆系统安装

    Args:
        db_path: 数据库路径

    Returns:
        验证结果字典
    """
    result = {
        'success': True,
        'errors': [],
        'warnings': [],
        'tables': {},
        'modules': {}
    }

    print("="*60)
    print("Complete Memory System v4.0 - Installation Verification")
    print("="*60)
    print(f"Database path: {db_path}")
    print(f"Verification time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")

    # 1. 检查数据库文件
    print("[1/5] Checking database file...")
    if not os.path.exists(db_path):
        result['success'] = False
        result['errors'].append(f"Database file not found: {db_path}")
        print("  [X] Database file not found")
        return result
    print(f"  [OK] Database file exists ({os.path.getsize(db_path) / 1024:.2f} KB)")

    # 2. 检查所有20个表
    print("\n[2/5] Checking database tables...")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        expected_tables = [
            'memories', 'episodic_memories', 'semantic_memories', 'procedural_memories',
            'working_memory', 'agent_diary', 'retrieval_cache', 'originals',
            'entities', 'entity_timelines', 'layered_context', 'evolution_log',
            'registered_tools', 'platform_messages', 'session_summaries',
            'security_scans', 'vulnerability_findings', 'osint_intel',
            'attack_chains', 'system_config'
        ]

        for table in expected_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                result['tables'][table] = count
                print(f"  [OK] {table} ({count} records)")
            else:
                result['success'] = False
                result['errors'].append(f"Table not found: {table}")
                print(f"  [X] {table} (not found)")

        conn.close()

    except Exception as e:
        result['success'] = False
        result['errors'].append(f"Database check failed: {e}")
        print(f"  [X] Database check failed: {e}")
        return result

    # 3. 检查Python模块
    print("\n[3/5] Checking Python modules...")
    modules = [
        'complete_memory_system',
        'retrieval_strategies',
        'memory_palace',
        'tom_engine',
        'emotional_analyzer',
        'enhanced_retrieval',
        'ollama_embedding'
    ]

    for module in modules:
        try:
            __import__(module)
            result['modules'][module] = True
            print(f"  [OK] {module}")
        except ImportError as e:
            result['warnings'].append(f"Module import failed: {module} - {e}")
            result['modules'][module] = False
            print(f"  [!] {module} (import failed)")

    # 4. 检查核心功能
    print("\n[4/5] Checking core functions...")
    try:
        from complete_memory_system import CompleteMemorySystem

        system = CompleteMemorySystem(db_path)
        if system.initialize():
            print("  [OK] System initialization successful")

            # 测试添加记忆
            try:
                mem_id = system.add_memory(
                    memory_type="test",
                    title="Verification Test",
                    content="Installation verification test memory",
                    importance=5
                )
                print(f"  [OK] Add memory successful (ID: {mem_id})")
            except Exception as e:
                result['warnings'].append(f"Add memory failed: {e}")
                print(f"  [!] Add memory failed: {e}")

            # 测试搜索
            try:
                results = system.search("Verification", limit=5)
                print(f"  [OK] Search successful ({len(results)} results)")
            except Exception as e:
                result['warnings'].append(f"Search failed: {e}")
                print(f"  [!] Search failed: {e}")

            # 测试情感分析
            try:
                emotion = system.analyze_emotion("I am happy!")
                print(f"  [OK] Emotion analysis successful ({emotion['primary_emotion']})")
            except Exception as e:
                result['warnings'].append(f"Emotion analysis failed: {e}")
                print(f"  [!] Emotion analysis failed: {e}")

            system.close()
        else:
            result['success'] = False
            result['errors'].append("System initialization failed")
            print("  [X] System initialization failed")

    except Exception as e:
        result['success'] = False
        result['errors'].append(f"Function check failed: {e}")
        print(f"  [X] Function check failed: {e}")

    # 5. 检查Ollama（可选）
    print("\n[5/5] Checking Ollama (optional)...")
    try:
        from ollama_embedding import OllamaEmbedding

        ollama = OllamaEmbedding()
        if ollama.check_connection():
            print("  [OK] Ollama service available")
        else:
            result['warnings'].append("Ollama service not available (optional)")
            print("  [!] Ollama service not available (optional)")
    except Exception as e:
        result['warnings'].append(f"Ollama check failed: {e} (optional)")
        print(f"  [!] Ollama check failed: {e} (optional)")

    # 总结
    print("\n" + "="*60)
    print("Verification Results")
    print("="*60)

    if result['success']:
        print("[OK] Installation verification successful!")
        print(f"  - Database tables: {len(result['tables'])}/20")
        print(f"  - Python modules: {sum(result['modules'].values())}/{len(result['modules'])}")
        print(f"  - Errors: {len(result['errors'])}")
        print(f"  - Warnings: {len(result['warnings'])}")
    else:
        print("[X] Installation verification failed!")
        print(f"  Errors:")
        for error in result['errors']:
            print(f"    - {error}")

    if result['warnings']:
        print(f"\n  Warnings:")
        for warning in result['warnings']:
            print(f"    - {warning}")

    print("="*60)

    return result


if __name__ == "__main__":
    import sys

    # 获取数据库路径
    db_path = sys.argv[1] if len(sys.argv) > 1 else "memory/database/xiaozhi_memory.db"

    # 验证
    result = verify_installation(db_path)

    # 退出码
    sys.exit(0 if result['success'] else 1)
