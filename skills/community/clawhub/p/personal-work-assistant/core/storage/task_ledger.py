import sqlite3
import os
import json
import datetime

class TaskLedger:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_conn() as conn:
            cur = conn.cursor()
            # 任务追踪主表
            cur.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,               -- 唯一标识 (如 tb:taskId, dt:msgId, manual:uuid)
                    source_type TEXT,                  -- tb | dingtalk_group | dingtalk_dm | dingtalk_at_all
                    source_name TEXT,                  -- 群名 / 任务项目名 / 发起人
                    title TEXT NOT NULL,               -- 任务/问题简述
                    detail TEXT,                       -- 详细描述 / 上下文
                    status TEXT NOT NULL,              -- pending(待处理) | in_progress(推进中) | to_confirm(待确认) | done(已完成)
                    priority TEXT DEFAULT 'normal',    -- urgent | high | normal | low
                    due_date TEXT,                     -- 截止日期 (YYYY-MM-DD 或 ISO)
                    first_seen_at TEXT NOT NULL,       -- 首次发现时间
                    last_updated_at TEXT NOT NULL,     -- 最近更新时间
                    closed_at TEXT,                    -- 闭环完成时间
                    resolution_note TEXT,              -- 闭环说明 / 进展记录
                    raw_data TEXT                      -- 原始元数据 JSON
                )
            ''')
            # 每日快照/公告表
            cur.execute('''
                CREATE TABLE IF NOT EXISTS announcements (
                    id TEXT PRIMARY KEY,
                    source_name TEXT,
                    content TEXT NOT NULL,
                    received_at TEXT NOT NULL,
                    is_reported INTEGER DEFAULT 0
                )
            ''')
            conn.commit()

    def upsert_task(self, task_id, source_type, source_name, title, detail="", status="pending", priority="normal", due_date=None, raw_data=None):
        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        raw_json = json.dumps(raw_data, ensure_ascii=False) if raw_data else "{}"
        
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute('SELECT first_seen_at, status FROM tasks WHERE id = ?', (task_id,))
            row = cur.fetchone()
            if row:
                first_seen = row[0]
                # 如果已闭环，且没有被明确重开，则保持状态
                cur.execute('''
                    UPDATE tasks 
                    SET source_type = ?, source_name = ?, title = ?, detail = ?, status = ?, priority = ?, due_date = ?, last_updated_at = ?, raw_data = ?
                    WHERE id = ?
                ''', (source_type, source_name, title, detail, status, priority, due_date, now_str, raw_json, task_id))
            else:
                cur.execute('''
                    INSERT INTO tasks (id, source_type, source_name, title, detail, status, priority, due_date, first_seen_at, last_updated_at, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (task_id, source_type, source_name, title, detail, status, priority, due_date, now_str, now_str, raw_json))
            conn.commit()

    def update_task_progress(self, task_id, status=None, resolution_note=None):
        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self._get_conn() as conn:
            cur = conn.cursor()
            updates = ["last_updated_at = ?"]
            params = [now_str]
            if status:
                updates.append("status = ?")
                params.append(status)
                if status == 'done':
                    updates.append("closed_at = ?")
                    params.append(now_str)
            if resolution_note:
                updates.append("resolution_note = ?")
                params.append(resolution_note)
            params.append(task_id)
            cur.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", params)
            conn.commit()

    def add_announcement(self, ann_id, source_name, content):
        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT OR REPLACE INTO announcements (id, source_name, content, received_at, is_reported)
                VALUES (?, ?, ?, ?, 0)
            ''', (ann_id, source_name, content, now_str))
            conn.commit()

    def get_active_tasks(self):
        """获取所有未完成的任务（pending, in_progress, to_confirm）"""
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM tasks 
                WHERE status != 'done'
                ORDER BY CASE priority WHEN 'urgent' THEN 1 WHEN 'high' THEN 2 WHEN 'normal' THEN 3 ELSE 4 END, first_seen_at ASC
            ''')
            return [dict(r) for r in cur.fetchall()]

    def get_recently_closed_tasks(self, hours=24):
        """获取最近 hours 小时内闭环的任务"""
        since = (datetime.datetime.now() - datetime.timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM tasks 
                WHERE status = 'done' AND closed_at >= ?
                ORDER BY closed_at DESC
            ''', (since,))
            return [dict(r) for r in cur.fetchall()]

    def get_unreported_announcements(self):
        """获取未播报的 @所有人 知悉公告"""
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('SELECT * FROM announcements WHERE is_reported = 0 ORDER BY received_at ASC')
            return [dict(r) for r in cur.fetchall()]

    def mark_announcements_reported(self, ids):
        if not ids:
            return
        with self._get_conn() as conn:
            cur = conn.cursor()
            placeholders = ','.join('?' for _ in ids)
            cur.execute(f'UPDATE announcements SET is_reported = 1 WHERE id IN ({placeholders})', ids)
            conn.commit()
