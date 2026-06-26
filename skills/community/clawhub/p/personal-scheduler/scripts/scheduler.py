#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人日程管理 - 核心模块（集成自动提醒）
"""

import sqlite3
import json
import uuid
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 添加脚本路径
sys.path.insert(0, str(Path(__file__).parent))

class PersonalScheduler:
    """个人日程管理器 - 自动创建提醒任务"""
    
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.data_dir / "scheduler.db"
        self.config_path = self.data_dir / "config.json"
        
        self._init_database()
        self._load_config()
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建表（如果不存在）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                location TEXT,
                description TEXT,
                reminder_minutes INTEGER DEFAULT 15,
                is_all_day BOOLEAN DEFAULT 0,
                feishu_user_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 检查是否需要添加新列（兼容旧表）
        cursor.execute("PRAGMA table_info(events)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'feishu_user_id' not in columns:
            cursor.execute('ALTER TABLE events ADD COLUMN feishu_user_id TEXT')
        if 'created_at' not in columns:
            cursor.execute('ALTER TABLE events ADD COLUMN created_at DATETIME')
        
        conn.commit()
        conn.close()
    
    def _load_config(self):
        """加载配置"""
        default_config = {
            "default_reminder_minutes": 15,
            "feishu_user_id": "ou_669575f70b8b81dd5c431c4ed1ad41c4",
            "timezone": "Asia/Shanghai"
        }
        
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = {**default_config, **json.load(f)}
        else:
            self.config = default_config
            self._save_config()
    
    def _save_config(self):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def add_event(self, title, start_time, end_time, location=None, 
                  description=None, reminder_minutes=None, 
                  feishu_user_id=None, is_all_day=False, repeat_rule=None):
        """
        添加日程 - 自动创建提醒任务
        
        Args:
            repeat_rule: RRULE 格式，如 'FREQ=WEEKLY;BYDAY=MO'
        
        Returns:
            dict: 包含 event_id 和 reminder_job 信息
        """
        if reminder_minutes is None:
            reminder_minutes = self.config.get('default_reminder_minutes', 15)
        
        if feishu_user_id is None:
            feishu_user_id = self.config.get('feishu_user_id')
        
        event_id = str(uuid.uuid4())[:8]
        
        # 保存到数据库
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (id, title, start_time, end_time, location, 
                              description, reminder_minutes, is_all_day, feishu_user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (event_id, title, start_time, end_time, location, 
              description, reminder_minutes, is_all_day, feishu_user_id))
        conn.commit()
        conn.close()
        
        # 自动创建提醒任务
        reminder_job = self._create_reminder_job(
            event_id, title, start_time, reminder_minutes, feishu_user_id
        )
        
        return {
            'event_id': event_id,
            'title': title,
            'start_time': start_time,
            'end_time': end_time,
            'reminder_minutes': reminder_minutes,
            'reminder_job': reminder_job
        }
    
    def _create_reminder_job(self, event_id, title, start_time, 
                             reminder_minutes, feishu_user_id):
        """创建提醒定时任务"""
        # 计算提醒时间
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        
        reminder_time = start_time - timedelta(minutes=reminder_minutes)
        
        # 如果提醒时间已经过去，不创建任务
        if reminder_time < datetime.now():
            return {
                'created': False,
                'reason': '提醒时间已过去'
            }
        
        # 生成 cron 表达式
        cron_expr = f"{reminder_time.minute} {reminder_time.hour} {reminder_time.day} {reminder_time.month} *"
        
        # 任务名称
        job_name = f"reminder_{event_id}"
        
        # 构建命令
        skill_dir = Path(__file__).parent.parent
        send_script = skill_dir / "scripts" / "send_reminder.py"
        cmd = f"python {send_script} {event_id}"
        
        # 保存定时任务配置
        job = {
            'name': job_name,
            'schedule': cron_expr,
            'command': cmd,
            'event_id': event_id,
            'event_title': title,
            'reminder_time': reminder_time.isoformat(),
            'feishu_user_id': feishu_user_id
        }
        
        self._save_reminder_job(job)
        
        return {
            'created': True,
            'job_name': job_name,
            'schedule': cron_expr,
            'reminder_time': reminder_time.strftime('%Y-%m-%d %H:%M')
        }
    
    def _save_reminder_job(self, job):
        """保存提醒任务到配置文件"""
        jobs_file = self.data_dir / "reminder_jobs.json"
        
        jobs = []
        if jobs_file.exists():
            with open(jobs_file, 'r', encoding='utf-8') as f:
                jobs = json.load(f)
        
        # 检查是否已存在
        existing = [j for j in jobs if j['name'] == job['name']]
        if existing:
            existing[0].update(job)
        else:
            jobs.append(job)
        
        with open(jobs_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
    
    def list_events(self, date_str=None):
        """查询日程"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if date_str:
            start = datetime.strptime(date_str, '%Y-%m-%d')
            end = start + timedelta(days=1)
            cursor.execute('''
                SELECT id, title, start_time, end_time, location, 
                       description, reminder_minutes, is_all_day
                FROM events 
                WHERE start_time >= ? AND start_time < ? 
                ORDER BY start_time
            ''', (start, end))
        else:
            cursor.execute('''
                SELECT id, title, start_time, end_time, location,
                       description, reminder_minutes, is_all_day
                FROM events 
                WHERE end_time >= ? 
                ORDER BY start_time
            ''', (datetime.now(),))
        
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def delete_event(self, event_id):
        """删除日程 - 同时删除提醒任务"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        
        if deleted:
            self._delete_reminder_job(event_id)
        
        return deleted
    
    def _delete_reminder_job(self, event_id):
        """删除提醒任务"""
        jobs_file = self.data_dir / "reminder_jobs.json"
        
        if not jobs_file.exists():
            return
        
        with open(jobs_file, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        
        job_name = f"reminder_{event_id}"
        jobs = [j for j in jobs if j['name'] != job_name]
        
        with open(jobs_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
    
    def get_pending_reminders(self):
        """获取待执行的提醒任务"""
        jobs_file = self.data_dir / "reminder_jobs.json"
        
        if not jobs_file.exists():
            return []
        
        with open(jobs_file, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        
        now = datetime.now()
        pending = []
        
        for job in jobs:
            reminder_time = datetime.fromisoformat(job['reminder_time'])
            if reminder_time <= now:
                pending.append(job)
        
        return pending

if __name__ == "__main__":
    scheduler = PersonalScheduler()
    print("Scheduler initialized with auto-reminder")
