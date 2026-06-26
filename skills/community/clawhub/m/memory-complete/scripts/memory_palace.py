#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MemPalace 混合记忆系统 - 整合 MemPalace 设计理念
四层架构：工作记忆、情景记忆、语义记忆、程序记忆
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

DB_PATH = "memory/database/xiaozhi_memory.db"

# AAAK 压缩方言实体编码
ENTITY_CODES = {}
EMOTION_MARKERS = {
    'joy': '*warm*',
    'determination': '*fierce*',
    'vulnerability': '*raw*',
    'curiosity': '*spark*',
    'concern': '*dim*',
    'satisfaction': '*bright*',
}

class MemPalace:
    """混合记忆系统"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    # ========== 情景记忆 ==========

    def add_episodic(self, event_type: str, content: str,
                     emotion: str = None, importance: int = 5,
                     aaak_content: str = None) -> int:
        """添加情景记忆"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO episodic_memories
            (event_type, content, emotion, importance, aaak_content)
            VALUES (?, ?, ?, ?, ?)
        ''', (event_type, content, emotion, importance, aaak_content))
        self.conn.commit()
        return cursor.lastrowid

    def get_recent_episodes(self, limit: int = 10,
                            event_type: str = None) -> List[Dict]:
        """获取最近的情景记忆"""
        cursor = self.conn.cursor()
        if event_type:
            cursor.execute('''
                SELECT * FROM episodic_memories
                WHERE event_type = ?
                ORDER BY created_at DESC LIMIT ?
            ''', (event_type, limit))
        else:
            cursor.execute('''
                SELECT * FROM episodic_memories
                ORDER BY created_at DESC LIMIT ?
            ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]

    # ========== 语义记忆（知识图谱） ==========

    def add_knowledge(self, subject: str, predicate: str, object: str,
                      source: str = None, confidence: float = 1.0) -> int:
        """添加知识三元组"""
        cursor = self.conn.cursor()
        # 先失效旧的相同三元组
        cursor.execute('''
            UPDATE semantic_memories
            SET valid_until = CURRENT_TIMESTAMP
            WHERE subject = ? AND predicate = ? AND object = ?
            AND valid_until IS NULL
        ''', (subject, predicate, object))
        # 添加新的
        cursor.execute('''
            INSERT INTO semantic_memories
            (subject, predicate, object, source, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (subject, predicate, object, source, confidence))
        self.conn.commit()
        return cursor.lastrowid

    def query_knowledge(self, subject: str = None,
                        predicate: str = None) -> List[Dict]:
        """查询知识图谱"""
        cursor = self.conn.cursor()
        conditions = []
        params = []
        if subject:
            conditions.append('subject = ?')
            params.append(subject)
        if predicate:
            conditions.append('predicate = ?')
            params.append(predicate)
        conditions.append('valid_until IS NULL')

        query = f'''
            SELECT * FROM semantic_memories
            WHERE {' AND '.join(conditions)}
            ORDER BY confidence DESC
        '''
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    # ========== 程序记忆 ==========

    def add_skill(self, skill_name: str, skill_type: str,
                  description: str, steps: List[str]) -> int:
        """添加技能"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO procedural_memories
            (skill_name, skill_type, description, steps)
            VALUES (?, ?, ?, ?)
        ''', (skill_name, skill_type, description, json.dumps(steps)))
        self.conn.commit()
        return cursor.lastrowid

    def record_skill_usage(self, skill_name: str, success: bool):
        """记录技能使用结果"""
        cursor = self.conn.cursor()
        if success:
            cursor.execute('''
                UPDATE procedural_memories
                SET success_count = success_count + 1,
                    last_used = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE skill_name = ?
            ''', (skill_name,))
        else:
            cursor.execute('''
                UPDATE procedural_memories
                SET fail_count = fail_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE skill_name = ?
            ''', (skill_name,))
        self.conn.commit()

    # ========== Agent 日记 ==========

    def write_diary(self, summary: str, learnings: List[str],
                    decisions: List[str], session_id: str = None):
        """写日记"""
        cursor = self.conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        aaak_entry = self._to_aaak(summary, learnings, decisions)
        cursor.execute('''
            INSERT INTO agent_diary
            (session_id, date, summary, aaak_entry, learnings, decisions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id, today, summary, aaak_entry,
              json.dumps(learnings), json.dumps(decisions)))
        self.conn.commit()

    def _to_aaak(self, summary: str, learnings: List[str],
                 decisions: List[str]) -> str:
        """转换为 AAAK 压缩格式"""
        lines = [f"[{datetime.now().strftime('%H:%M')}] {summary}"]
        if learnings:
            lines.append("  > " + " | ".join(learnings))
        if decisions:
            lines.append("  ! " + " | ".join(decisions))
        return "\n".join(lines)

    def get_diary(self, date: str = None, limit: int = 7) -> List[Dict]:
        """获取日记"""
        cursor = self.conn.cursor()
        if date:
            cursor.execute('''
                SELECT * FROM agent_diary WHERE date = ?
            ''', (date,))
        else:
            cursor.execute('''
                SELECT * FROM agent_diary
                ORDER BY date DESC LIMIT ?
            ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]

    # ========== 工作记忆 ==========

    def set_working(self, session_id: str, key: str,
                    value: Any, ttl_seconds: int = 3600):
        """设置工作记忆"""
        cursor = self.conn.cursor()
        expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        cursor.execute('''
            INSERT OR REPLACE INTO working_memory
            (session_id, key, value, ttl_seconds, expires_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (session_id, key, json.dumps(value), ttl_seconds, expires_at))
        self.conn.commit()

    def get_working(self, session_id: str, key: str) -> Optional[Any]:
        """获取工作记忆"""
        cursor = self.conn.cursor()
        # 清理过期的
        cursor.execute('''
            DELETE FROM working_memory
            WHERE expires_at IS NOT NULL AND expires_at < CURRENT_TIMESTAMP
        ''')
        cursor.execute('''
            SELECT value FROM working_memory
            WHERE session_id = ? AND key = ?
        ''', (session_id, key))
        row = cursor.fetchone()
        if row:
            return json.loads(row['value'])
        return None

# 单例实例
_palace = None

def get_palace() -> MemPalace:
    global _palace
    if _palace is None:
        _palace = MemPalace()
        _palace.connect()
    return _palace

if __name__ == '__main__':
    # 测试
    palace = get_palace()

    # 添加情景记忆
    palace.add_episodic('learning', '学习了 MemPalace 四层架构', 'curiosity', 7)

    # 添加知识
    palace.add_knowledge('MemPalace', 'has_layer', 'working_memory', 'github')
    palace.add_knowledge('MemPalace', 'has_layer', 'episodic_memory', 'github')
    palace.add_knowledge('MemPalace', 'has_layer', 'semantic_memory', 'github')
    palace.add_knowledge('MemPalace', 'has_layer', 'procedural_memory', 'github')

    # 写日记
    palace.write_diary(
        summary='完成 MemPalace 混合系统整合',
        learnings=['四层架构设计', 'AAAK压缩方言'],
        decisions=['保留现有SQLite+LanceDB', '引入四层表结构']
    )

    print('测试完成！')
    print('最近情景:', palace.get_recent_episodes(3))
    print('知识查询:', palace.query_knowledge('MemPalace'))
    print('今日日记:', palace.get_diary(limit=1))
