#!/usr/bin/env python3
"""
标书协作引擎 - 章节任务拆分脚本
功能：根据招标文件结构自动拆解章节任务表，支持人员能力匹配和手动调整
版本：v5.2.0
"""

import json
import os
import sqlite3
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

# 运行时数据库路径（符合死规则 #12 运行时例外）
OUTPUT_DIR = Path.home() / ".workbuddy" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
GOV_COLLAB_DB = OUTPUT_DIR / "gov_collab.db"

# 标准标书章节模板（政府采购通用结构）
STANDARD_CHAPTERS = [
    {"name": "投标函及法定代表人证明", "category": "商务", "weight": 5},
    {"name": "法定代表人授权委托书", "category": "商务", "weight": 5},
    {"name": "企业基本情况简介", "category": "商务", "weight": 8},
    {"name": "资质符合性说明", "category": "资质", "weight": 10},
    {"name": "技术方案（含技术路线）", "category": "技术", "weight": 25},
    {"name": "实施方案（含进度计划）", "category": "技术", "weight": 15},
    {"name": "人员配置与项目团队", "category": "技术", "weight": 10},
    {"name": "设备清单与技术参数", "category": "技术", "weight": 8},
    {"name": "质量保证措施", "category": "技术", "weight": 7},
    {"name": "售后服务承诺", "category": "商务", "weight": 5},
    {"name": "投标报价文件", "category": "报价", "weight": 10},
    {"name": "类似项目经验与业绩", "category": "商务", "weight": 8},
    {"name": "财务状况与纳税证明", "category": "商务", "weight": 5},
    {"name": "信用查询与无违法声明", "category": "商务", "weight": 5},
    {"name": "其他补充材料", "category": "其他", "weight": 3},
]

# 人员能力标签映射
CAPABILITY_MAP = {
    "商务": ["商务", "资质", "其他"],
    "技术": ["技术"],
    "报价": ["报价"],
    "资质": ["资质", "商务"],
}


def init_db():
    """初始化协作数据库"""
    conn = sqlite3.connect(str(GOV_COLLAB_DB))
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            project_name TEXT NOT NULL,
            deadline TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            status TEXT DEFAULT 'active'
        );
        
        CREATE TABLE IF NOT EXISTS chapter_tasks (
            id INTEGER PRIMARY KEY,
            project_id INTEGER,
            chapter_name TEXT NOT NULL,
            category TEXT,
            assignee TEXT,
            status TEXT DEFAULT 'pending',
            deadline TEXT,
            weight INTEGER DEFAULT 5,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        );
        
        CREATE TABLE IF NOT EXISTS chapter_locks (
            id INTEGER PRIMARY KEY,
            project_id TEXT NOT NULL,
            chapter_name TEXT NOT NULL,
            member_name TEXT NOT NULL,
            lock_time TEXT NOT NULL,
            lock_status TEXT DEFAULT 'locked',
            file_hash TEXT,
            UNIQUE(project_id, chapter_name)
        );
        
        CREATE TABLE IF NOT EXISTS chapter_versions (
            id INTEGER PRIMARY KEY,
            project_id TEXT NOT NULL,
            chapter_name TEXT NOT NULL,
            version_num INTEGER NOT NULL,
            member_name TEXT NOT NULL,
            save_time TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            change_summary TEXT
        );
    """)
    conn.commit()
    return conn


def create_project(project_name: str, deadline: str, members: list) -> dict:
    """
    创建标书项目并自动拆分章节任务
    
    Args:
        project_name: 项目名称
        deadline: 投标截止日 (YYYY-MM-DD)
        members: 团队成员列表 [{"name": "张三", "capability": "商务"}, ...]
    
    Returns:
        章节任务表
    """
    conn = init_db()
    cursor = conn.cursor()
    
    # 创建项目
    cursor.execute(
        "INSERT INTO projects (project_name, deadline) VALUES (?, ?)",
        (project_name, deadline)
    )
    project_id = cursor.lastrowid
    
    # 解析截止时间
    deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
    
    # 自动分配章节
    tasks = []
    for chapter in STANDARD_CHAPTERS:
        # 匹配最佳负责人
        assignee = _match_assignee(chapter["category"], members)
        
        # 计算章节截止时间（按权重倒排，权重高的先完成）
        days_before = max(1, int(chapter["weight"] / 5))
        chapter_deadline = (deadline_dt - timedelta(days=days_before)).strftime("%Y-%m-%d")
        
        cursor.execute("""
            INSERT INTO chapter_tasks 
            (project_id, chapter_name, category, assignee, status, deadline, weight)
            VALUES (?, ?, ?, ?, 'pending', ?, ?)
        """, (project_id, chapter["name"], chapter["category"], 
              assignee, chapter_deadline, chapter["weight"]))
        
        tasks.append({
            "chapter": chapter["name"],
            "category": chapter["category"],
            "assignee": assignee,
            "status": "pending",
            "deadline": chapter_deadline,
            "weight": chapter["weight"],
        })
    
    conn.commit()
    conn.close()
    
    return {
        "project_id": project_id,
        "project_name": project_name,
        "deadline": deadline,
        "tasks": tasks,
        "total_chapters": len(tasks),
    }


def _match_assignee(category: str, members: list) -> str:
    """根据章节类别匹配最佳负责人"""
    # 优先匹配精确能力
    for member in members:
        if category in CAPABILITY_MAP.get(member.get("capability", ""), []):
            return member["name"]
    # 次选匹配"商务"（通用能力）
    for member in members:
        if member.get("capability") == "商务":
            return member["name"]
    # 默认分配给第一个成员
    return members[0]["name"] if members else "未分配"


def acquire_lock(project_id: str, chapter_name: str, member_name: str) -> dict:
    """获取章节编辑锁"""
    conn = init_db()
    cursor = conn.cursor()
    
    # 检查是否已被锁定
    cursor.execute("""
        SELECT member_name, lock_time FROM chapter_locks 
        WHERE project_id = ? AND chapter_name = ? AND lock_status = 'locked'
    """, (project_id, chapter_name))
    existing = cursor.fetchone()
    
    if existing:
        lock_time = datetime.strptime(existing[1], "%Y-%m-%d %H:%M:%S")
        # 检查是否超时（30分钟）
        if datetime.now() - lock_time > timedelta(minutes=30):
            # 超时自动释放
            cursor.execute("""
                UPDATE chapter_locks SET lock_status = 'timeout_released'
                WHERE project_id = ? AND chapter_name = ?
            """, (project_id, chapter_name))
        else:
            conn.close()
            return {
                "success": False,
                "message": f"章节「{chapter_name}」已被 {existing[0]} 锁定（锁定时间：{existing[1]}）",
                "locked_by": existing[0],
            }
    
    # 获取锁
    cursor.execute("""
        INSERT OR REPLACE INTO chapter_locks 
        (project_id, chapter_name, member_name, lock_time, lock_status)
        VALUES (?, ?, ?, datetime('now'), 'locked')
    """, (project_id, chapter_name, member_name))
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"章节「{chapter_name}」已锁定，负责人：{member_name}",
        "locked_by": member_name,
    }


def release_lock(project_id: str, chapter_name: str, member_name: str, 
                 file_content: str = None, change_summary: str = "") -> dict:
    """释放章节编辑锁并保存版本"""
    conn = init_db()
    cursor = conn.cursor()
    
    # 计算文件哈希
    file_hash = hashlib.sha256(file_content.encode()).hexdigest() if file_content else None
    
    # 获取当前版本号
    cursor.execute("""
        SELECT MAX(version_num) FROM chapter_versions 
        WHERE project_id = ? AND chapter_name = ?
    """, (project_id, chapter_name))
    current_version = cursor.fetchone()[0] or 0
    
    # 保存版本
    cursor.execute("""
        INSERT INTO chapter_versions 
        (project_id, chapter_name, version_num, member_name, save_time, file_hash, change_summary)
        VALUES (?, ?, ?, ?, datetime('now'), ?, ?)
    """, (project_id, chapter_name, current_version + 1, member_name, file_hash, change_summary))
    
    # 释放锁
    cursor.execute("""
        UPDATE chapter_locks 
        SET lock_status = 'released', file_hash = ?
        WHERE project_id = ? AND chapter_name = ? AND member_name = ?
    """, (file_hash, project_id, chapter_name, member_name))
    
    # 更新任务状态
    cursor.execute("""
        UPDATE chapter_tasks SET status = 'completed'
        WHERE project_id = ? AND chapter_name = ? AND assignee = ?
    """, (project_id, chapter_name, member_name))
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"章节「{chapter_name}」已保存（版本 {current_version + 1}）",
        "version": current_version + 1,
        "file_hash": file_hash,
    }


def get_project_status(project_id: int) -> dict:
    """获取项目进度状态"""
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT chapter_name, assignee, status, deadline, weight
        FROM chapter_tasks WHERE project_id = ?
        ORDER BY weight DESC
    """, (project_id,))
    
    tasks = []
    for row in cursor.fetchall():
        tasks.append({
            "chapter": row[0],
            "assignee": row[1],
            "status": row[2],
            "deadline": row[3],
            "weight": row[4],
        })
    
    # 统计
    total = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "completed")
    in_progress = sum(1 for t in tasks if t["status"] == "in_progress")
    locked = sum(1 for t in tasks if t["status"] == "locked")
    
    conn.close()
    
    return {
        "project_id": project_id,
        "tasks": tasks,
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "locked": locked,
        "pending": total - completed - in_progress - locked,
        "progress": f"{completed}/{total}",
        "progress_pct": round(completed / total * 100, 1) if total > 0 else 0,
    }


if __name__ == "__main__":
    # 示例用法
    members = [
        {"name": "张三", "capability": "商务"},
        {"name": "李四", "capability": "技术"},
        {"name": "王五", "capability": "资质"},
        {"name": "赵六", "capability": "报价"},
    ]
    
    result = create_project("XX市IT运维采购项目", "2026-09-20", members)
    print(json.dumps(result, ensure_ascii=False, indent=2))
