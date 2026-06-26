#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Omni 控制台 (omni-ctl)
全能技能管理工具：支持技能注册 (register)、注销 (deregister) 以及 30 秒回滚 (rollback)。
本地使用 SQLite 作为注册表存储。
"""

import argparse
import sqlite3
import json
import time
import os
import sys
from typing import Dict, Any

# 导入统一配置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.settings as settings

def update_skill_md_registry(conn: sqlite3.Connection):
    """
    动态更新 SKILL.md，将已注册的子技能列表写入其中，
    以便大模型 (LLM) 能够知道当前有哪些可用的子技能进行调度。
    """
    if not os.path.exists(settings.SKILL_MD_PATH):
        print(f"[警告] 未找到 {settings.SKILL_MD_PATH}，跳过更新。")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT name, metadata, runtime_type FROM skills")
    skills = cursor.fetchall()

    registry_content = "## 当前可用子技能列表 (Available Sub-Skills)\n\n"
    if not skills:
        registry_content += "*当前暂无已注册的子技能。*\n"
    else:
        for name, meta_str, runtime in skills:
            try:
                meta = json.loads(meta_str)
                desc = meta.get("description", "无描述")
            except:
                desc = "无描述"
            registry_content += f"- **{name}** (`{runtime}`): {desc}\n"
    
    registry_content += "\n*(此列表由 `omni_ctl` 自动维护，请勿手动修改)*\n"

    try:
        with open(settings.SKILL_MD_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        # 查找替换标记，如果没有则在末尾追加
        start_marker = "<!-- OMNI_REGISTRY_START -->"
        end_marker = "<!-- OMNI_REGISTRY_END -->"
        
        if start_marker in content and end_marker in content:
            before = content.split(start_marker)[0]
            after = content.split(end_marker)[1]
            new_content = before + start_marker + "\n" + registry_content + end_marker + after
        else:
            new_content = content + "\n\n" + start_marker + "\n" + registry_content + end_marker + "\n"

        with open(settings.SKILL_MD_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"[通知] SKILL.md 的可用子技能列表已更新。")
    except Exception as e:
        print(f"[错误] 更新 SKILL.md 失败: {e}")

def init_db():
    """初始化数据库表结构"""
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    # 创建技能主表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            name TEXT PRIMARY KEY,
            metadata TEXT,
            runtime_type TEXT,
            sandbox_score REAL,
            status TEXT,
            updated_at REAL
        )
    ''')
    # 创建历史记录表，用于支持回滚
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skill_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT,
            action TEXT,
            previous_state TEXT,
            timestamp REAL
        )
    ''')
    conn.commit()
    conn.close()

def get_current_state(cursor, name):
    """获取技能当前状态的 JSON 字符串"""
    cursor.execute('SELECT * FROM skills WHERE name = ?', (name,))
    row = cursor.fetchone()
    if row:
        return json.dumps({
            'name': row[0],
            'metadata': row[1],
            'runtime_type': row[2],
            'sandbox_score': row[3],
            'status': row[4],
            'updated_at': row[5]
        })
    return None

def save_history(cursor, name, action, previous_state):
    """保存操作历史记录，以便回滚"""
    timestamp = time.time()
    cursor.execute('''
        INSERT INTO skill_history (skill_name, action, previous_state, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (name, action, previous_state, timestamp))

def register(args):
    """注册技能"""
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    
    name = args.name
    metadata_str = args.metadata
    runtime_type = args.runtime_type
    sandbox_score = args.sandbox_score
    status = args.status
    current_time = time.time()
    
    # 如果 metadata 只有默认的 "{}"，尝试从已打包好的 core package 中提取 manifest.json
    if metadata_str == "{}" or metadata_str == "":
        manifest_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugins", name, "manifest.json")
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                    if "metadata" in manifest:
                        metadata_str = json.dumps(manifest["metadata"], ensure_ascii=False)
            except Exception as e:
                print(f"[警告] 无法读取 {manifest_path} 中的元数据: {e}")
                
    # 获取之前状态
    previous_state = get_current_state(cursor, name)
    
    # 记录历史
    save_history(cursor, name, 'register', previous_state)
    
    # 插入或更新
    cursor.execute('''
        INSERT INTO skills (name, metadata, runtime_type, sandbox_score, status, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            metadata=excluded.metadata,
            runtime_type=excluded.runtime_type,
            sandbox_score=excluded.sandbox_score,
            status=excluded.status,
            updated_at=excluded.updated_at
    ''', (name, metadata_str, runtime_type, sandbox_score, status, current_time))
    
    conn.commit()
    update_skill_md_registry(conn)
    conn.close()
    print(f"✅ 技能 '{name}' 注册成功。")

def deregister(args):
    """注销技能"""
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    
    name = args.name
    
    # 获取之前状态
    previous_state = get_current_state(cursor, name)
    if not previous_state:
        print(f"❌ 技能 '{name}' 不存在，无法注销。")
        conn.close()
        sys.exit(1)
        
    # 记录历史
    save_history(cursor, name, 'deregister', previous_state)
    
    cursor.execute('DELETE FROM skills WHERE name = ?', (name,))
    
    conn.commit()
    update_skill_md_registry(conn)
    conn.close()
    print(f"✅ 技能 '{name}' 已成功注销。")

def rollback(args):
    """回滚 30 秒内的最近一次操作"""
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    
    name = args.name
    current_time = time.time()
    time_limit = current_time - 30.0  # 30秒内
    
    # 查找最近的一次历史记录
    cursor.execute('''
        SELECT id, action, previous_state, timestamp 
        FROM skill_history 
        WHERE skill_name = ? AND timestamp >= ? 
        ORDER BY timestamp DESC LIMIT 1
    ''', (name, time_limit))
    
    record = cursor.fetchone()
    
    if not record:
        print(f"❌ 未找到技能 '{name}' 在过去 30 秒内的可回滚记录。")
        conn.close()
        sys.exit(1)
        
    history_id, action, previous_state_json, timestamp = record
    
    # 执行回滚逻辑
    if previous_state_json is None:
        # 之前的状态为空，说明是新注册的，回滚即删除
        cursor.execute('DELETE FROM skills WHERE name = ?', (name,))
    else:
        # 恢复到之前的状态
        state = json.loads(previous_state_json)
        cursor.execute('''
            INSERT INTO skills (name, metadata, runtime_type, sandbox_score, status, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                metadata=excluded.metadata,
                runtime_type=excluded.runtime_type,
                sandbox_score=excluded.sandbox_score,
                status=excluded.status,
                updated_at=excluded.updated_at
        ''', (state['name'], state['metadata'], state['runtime_type'], state['sandbox_score'], state['status'], state['updated_at']))
        
    # 删除该条历史记录以防重复回滚
    cursor.execute('DELETE FROM skill_history WHERE id = ?', (history_id,))
    
    conn.commit()
    update_skill_md_registry(conn)
    conn.close()
    
    # 卸载后的额外还原逻辑：如果注册时生成了打包文件，可以考虑删除它
    # （这里的还原仅针对数据库注册状态和 SKILL.md，实际打包生成的代码目录需要根据您的具体设计清理）
    print(f"✅ 技能 '{name}' 已成功回滚到 '{action}' 操作前的状态。")

def main():
    init_db()
    
    parser = argparse.ArgumentParser(description="全能技能控制台 (omni-ctl)")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    subparsers.required = True
    
    # 注册子命令
    parser_register = subparsers.add_parser("register", help="注册新的技能")
    parser_register.add_argument("--name", required=True, help="技能名称")
    parser_register.add_argument("--metadata", default="{}", help="技能元数据 (JSON格式)")
    parser_register.add_argument("--runtime-type", required=True, help="运行环境类型 (如 python, nodejs)")
    parser_register.add_argument("--sandbox-score", type=float, default=0.0, help="沙盒评分")
    parser_register.add_argument("--status", default="active", help="技能状态 (如 active, inactive)")
    parser_register.set_defaults(func=register)
    
    # 注销子命令
    parser_deregister = subparsers.add_parser("deregister", help="注销技能")
    parser_deregister.add_argument("--name", required=True, help="要注销的技能名称")
    parser_deregister.set_defaults(func=deregister)
    
    # 回滚子命令
    parser_rollback = subparsers.add_parser("rollback", help="回滚过去 30 秒内的技能修改")
    parser_rollback.add_argument("--name", required=True, help="要回滚的技能名称")
    parser_rollback.set_defaults(func=rollback)
    
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
