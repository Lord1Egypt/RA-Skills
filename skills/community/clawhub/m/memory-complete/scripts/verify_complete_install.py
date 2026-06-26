#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Memory System - Installation Verification
完整记忆系统 - 安装验证脚本
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
    print("完整记忆系统 v4.0 - 安装验证")
    print("="*60)
    print(f"数据库路径: {db_path}")
    print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")

    # 1. 检查数据库文件
    print("[1/5] 检查数据库文件...")
    if not os.path.exists(db_path):
        result['success'] = False
        result['errors'].append(f"数据库文件不存在: {db_path}")
        print("  [ERROR] 数据库文件不存在")
        return result
    print(f"  [OK] 数据库文件存在 ({os.path.getsize(db_path) / 1024:.2f} KB)")

    # 2. 检查所有20个表
    print("\n[2/5] 检查数据库表...")
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
                print(f"  [OK] {table} ({count} 条记录)")
            else:
                result['success'] = False
                result['errors'].append(f"表不存在: {table}")
                print(f"  [ERROR] {table} (不存在)")

        conn.close()

    except Exception as e:
        result['success'] = False
        result['errors'].append(f"数据库检查失败: {e}")
        print(f"  [ERROR] 数据库检查失败: {e}")
        return result

    # 3. 检查Python模块
    print("\n[3/5] 检查Python模块...")
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
            result['warnings'].append(f"模块导入失败: {module} - {e}")
            result['modules'][module] = False
            print(f"  [WARNING] {module} (导入失败)")

    # 4. 检查核心功能
    print("\n[4/5] 检查核心功能...")
    try:
        from complete_memory_system import CompleteMemorySystem

        system = CompleteMemorySystem(db_path)
        if system.initialize():
            print("  [OK] 系统初始化成功")

            # 测试添加记忆
            try:
                mem_id = system.add_memory(
                    memory_type="test",
                    title="验证测试",
                    content="安装验证测试记忆",
                    importance=5
                )
                print(f"  [OK] 添加记忆成功 (ID: {mem_id})")
            except Exception as e:
                result['warnings'].append(f"添加记忆失败: {e}")
                print(f"  [WARNING] 添加记忆失败: {e}")

            # 测试搜索
            try:
                results = system.search("验证", limit=5)
                print(f"  [OK] 搜索成功 ({len(results)} 条结果)")
            except Exception as e:
                result['warnings'].append(f"搜索失败: {e}")
                print(f"  [WARNING] 搜索失败: {e}")

            # 测试情感分析
            try:
                emotion = system.analyze_emotion("I am happy!")
                print(f"  [OK] 情感分析成功 ({emotion['primary_emotion']})")
            except Exception as e:
                result['warnings'].append(f"情感分析失败: {e}")
                print(f"  [WARNING] 情感分析失败: {e}")

            system.close()
        else:
            result['success'] = False
            result['errors'].append("系统初始化失败")
            print("  [ERROR] 系统初始化失败")

    except Exception as e:
        result['success'] = False
        result['errors'].append(f"功能检查失败: {e}")
        print(f"  [ERROR] 功能检查失败: {e}")

    # 5. 检查Ollama（可选）
    print("\n[5/5] 检查Ollama（可选）...")
    try:
        from ollama_embedding import OllamaEmbedding

        ollama = OllamaEmbedding()
        if ollama.check_connection():
            print("  [OK] Ollama服务可用")
        else:
            result['warnings'].append("Ollama服务不可用（可选）")
            print("  [WARNING] Ollama服务不可用（可选）")
    except Exception as e:
        result['warnings'].append(f"Ollama检查失败: {e}（可选）")
        print(f"  [WARNING] Ollama检查失败: {e}（可选）")

    # 总结
    print("\n" + "="*60)
    print("验证结果")
    print("="*60)

    if result['success']:
        print("[OK] 安装验证成功！")
        print(f"  - 数据库表: {len(result['tables'])}/20")
        print(f"  - Python模块: {sum(result['modules'].values())}/{len(result['modules'])}")
        print(f"  - 错误: {len(result['errors'])}")
        print(f"  - 警告: {len(result['warnings'])}")
    else:
        print("[ERROR] 安装验证失败！")
        print(f"  错误:")
        for error in result['errors']:
            print(f"    - {error}")

    if result['warnings']:
        print(f"\n  警告:")
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
