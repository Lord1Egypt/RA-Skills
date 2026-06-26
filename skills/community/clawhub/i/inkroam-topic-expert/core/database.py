#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题库管理系统
功能：存储、去重、检索、统计选题
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
import hashlib


class TopicDatabase:
    """选题库管理"""
    
    def __init__(self, db_path="~/.openclaw/workspace-bijian/data/topics.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        cursor = self.conn.cursor()
        
        # 选题表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_hash TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            source_url TEXT,
            fetch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            hot_score INTEGER DEFAULT 0,
            relevance_score INTEGER DEFAULT 0,
            total_score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            excerpt TEXT,
            raw_data TEXT
        )
        """)
        
        # 生成记录表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            article_id TEXT,
            theme TEXT,
            viewpoints TEXT,
            generate_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'draft',
            FOREIGN KEY (topic_id) REFERENCES topics(id)
        )
        """)
        
        # 跳过记录表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS skipped_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            skip_reason TEXT,
            skip_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (topic_id) REFERENCES topics(id)
        )
        """)
        
        # 数据源统计表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS source_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            fetch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_count INTEGER DEFAULT 0,
            qualified_count INTEGER DEFAULT 0
        )
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_hash ON topics(topic_hash)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_source ON topics(source)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON topics(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fetch_time ON topics(fetch_time)")
        
        self.conn.commit()
    
    def generate_topic_hash(self, title, source):
        """生成选题唯一标识（用于去重）"""
        # 标题归一化：去除空格、标点、转小写
        normalized = title.lower().replace(" ", "").replace("#", "")
        hash_str = f"{normalized}_{source}"
        return hashlib.md5(hash_str.encode()).hexdigest()
    
    def add_topic(self, title, source, source_url="", hot_score=0, 
                  relevance_score=0, total_score=0, excerpt="", raw_data=None):
        """添加选题（自动去重）"""
        topic_hash = self.generate_topic_hash(title, source)
        
        cursor = self.conn.cursor()
        
        # 检查是否已存在
        cursor.execute("SELECT id, status FROM topics WHERE topic_hash = ?", (topic_hash,))
        existing = cursor.fetchone()
        
        if existing:
            # 已存在，更新分数和时间
            cursor.execute("""
            UPDATE topics 
            SET hot_score = ?, total_score = ?, fetch_time = CURRENT_TIMESTAMP
            WHERE topic_hash = ?
            """, (hot_score, total_score, topic_hash))
            self.conn.commit()
            return {"status": "updated", "topic_id": existing[0], "existing_status": existing[1]}
        
        # 新增选题
        cursor.execute("""
        INSERT INTO topics 
        (topic_hash, title, source, source_url, hot_score, relevance_score, 
         total_score, excerpt, raw_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (topic_hash, title, source, source_url, hot_score, relevance_score,
              total_score, excerpt, json.dumps(raw_data) if raw_data else None))
        
        self.conn.commit()
        return {"status": "added", "topic_id": cursor.lastrowid}
    
    def get_pending_topics(self, min_score=70, limit=10):
        """获取待处理的高分选题"""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT id, title, source, source_url, total_score, excerpt, fetch_time
        FROM topics
        WHERE status = 'pending' AND total_score >= ?
        ORDER BY total_score DESC, fetch_time DESC
        LIMIT ?
        """, (min_score, limit))
        
        columns = ['id', 'title', 'source', 'source_url', 'total_score', 'excerpt', 'fetch_time']
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def mark_as_generated(self, topic_id, article_id, theme, viewpoints):
        """标记选题已生成文章"""
        cursor = self.conn.cursor()
        
        # 更新选题状态
        cursor.execute("UPDATE topics SET status = 'generated' WHERE id = ?", (topic_id,))
        
        # 记录生成信息
        cursor.execute("""
        INSERT INTO generated_articles (topic_id, article_id, theme, viewpoints)
        VALUES (?, ?, ?, ?)
        """, (topic_id, article_id, theme, json.dumps(viewpoints)))
        
        self.conn.commit()
    
    def mark_as_skipped(self, topic_id, reason=""):
        """标记选题已跳过"""
        cursor = self.conn.cursor()
        
        cursor.execute("UPDATE topics SET status = 'skipped' WHERE id = ?", (topic_id,))
        cursor.execute("""
        INSERT INTO skipped_topics (topic_id, skip_reason)
        VALUES (?, ?)
        """, (topic_id, reason))
        
        self.conn.commit()
    
    def get_stats(self, days=7):
        """获取统计数据"""
        cursor = self.conn.cursor()
        
        # 总选题数
        cursor.execute("SELECT COUNT(*) FROM topics WHERE fetch_time >= datetime('now', '-{} days')".format(days))
        total = cursor.fetchone()[0]
        
        # 各状态数量
        cursor.execute("""
        SELECT status, COUNT(*) 
        FROM topics 
        WHERE fetch_time >= datetime('now', '-{} days')
        GROUP BY status
        """.format(days))
        status_counts = dict(cursor.fetchall())
        
        # 各来源数量
        cursor.execute("""
        SELECT source, COUNT(*), AVG(total_score)
        FROM topics
        WHERE fetch_time >= datetime('now', '-{} days')
        GROUP BY source
        ORDER BY COUNT(*) DESC
        """.format(days))
        source_stats = [
            {"source": row[0], "count": row[1], "avg_score": round(row[2], 1)}
            for row in cursor.fetchall()
        ]
        
        return {
            "total": total,
            "status": status_counts,
            "sources": source_stats,
            "days": days
        }
    
    def search_topics(self, keyword, limit=20):
        """搜索选题"""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT id, title, source, total_score, status, fetch_time
        FROM topics
        WHERE title LIKE ?
        ORDER BY fetch_time DESC
        LIMIT ?
        """, (f"%{keyword}%", limit))
        
        columns = ['id', 'title', 'source', 'total_score', 'status', 'fetch_time']
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()


def main():
    """测试"""
    db = TopicDatabase()
    
    # 添加测试选题
    result = db.add_topic(
        title="OpenAI多位负责人抗议辞职",
        source="weibo",
        source_url="https://weibo.com/...",
        hot_score=25,
        relevance_score=25,
        total_score=75
    )
    print(f"添加选题：{result}")
    
    # 获取待处理选题
    pending = db.get_pending_topics(min_score=70, limit=5)
    print(f"\n待处理选题（≥70分）：{len(pending)} 个")
    for topic in pending:
        print(f"  - {topic['title']} ({topic['source']}, {topic['total_score']}分)")
    
    # 统计
    stats = db.get_stats(days=7)
    print(f"\n近7天统计：")
    print(f"  总选题：{stats['total']} 个")
    print(f"  状态分布：{stats['status']}")
    print(f"  来源分布：{stats['sources']}")
    
    db.close()


if __name__ == '__main__':
    main()
