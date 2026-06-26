#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 定时任务管理器
自动为日程创建提醒任务
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

class CronManager:
    """管理 OpenClaw 定时任务"""
    
    def __init__(self):
        self.skill_dir = Path(__file__).parent.parent
        self.cron_script = self.skill_dir / "scripts" / "send_reminder.py"
    
    def create_reminder_cron(self, event_id: str, event_title: str, 
                             reminder_time: datetime, feishu_user_id: str = None):
        """
        为特定日程创建提醒定时任务
        
        Args:
            event_id: 日程ID
            event_title: 日程标题
            reminder_time: 提醒时间
            feishu_user_id: 飞书用户ID
        """
        # 生成 cron 表达式（精确到分钟）
        cron_expr = self._datetime_to_cron(reminder_time)
        
        # 任务名称
        job_name = f"scheduler_reminder_{event_id}"
        
        # 构建命令
        cmd = f"python {self.cron_script} {event_id}"
        if feishu_user_id:
            cmd += f" --user {feishu_user_id}"
        
        # 使用 openclaw 命令创建定时任务
        cron_job = {
            "name": job_name,
            "schedule": cron_expr,
            "command": cmd,
            "description": f"日程提醒: {event_title}"
        }
        
        # 保存到本地 cron 配置文件
        self._save_cron_job(cron_job)
        
        return {
            "success": True,
            "job_name": job_name,
            "schedule": cron_expr,
            "reminder_time": reminder_time.strftime("%Y-%m-%d %H:%M")
        }
    
    def _datetime_to_cron(self, dt: datetime) -> str:
        """将 datetime 转换为 cron 表达式"""
        # cron 格式: 分 时 日 月 周
        return f"{dt.minute} {dt.hour} {dt.day} {dt.month} *"
    
    def _save_cron_job(self, job: dict):
        """保存定时任务到配置文件"""
        cron_file = self.skill_dir / "data" / "cron_jobs.json"
        
        jobs = []
        if cron_file.exists():
            with open(cron_file, 'r', encoding='utf-8') as f:
                jobs = json.load(f)
        
        # 检查是否已存在同名任务，存在则更新
        existing = [j for j in jobs if j["name"] == job["name"]]
        if existing:
            existing[0].update(job)
        else:
            jobs.append(job)
        
        with open(cron_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
    
    def delete_reminder_cron(self, event_id: str):
        """删除日程对应的提醒定时任务"""
        job_name = f"scheduler_reminder_{event_id}"
        cron_file = self.skill_dir / "data" / "cron_jobs.json"
        
        if not cron_file.exists():
            return
        
        with open(cron_file, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        
        # 过滤掉要删除的任务
        jobs = [j for j in jobs if j["name"] != job_name]
        
        with open(cron_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
    
    def list_cron_jobs(self) -> list:
        """列出所有定时任务"""
        cron_file = self.skill_dir / "data" / "cron_jobs.json"
        
        if not cron_file.exists():
            return []
        
        with open(cron_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def sync_to_openclaw(self):
        """
        将本地定时任务同步到 OpenClaw
        这个函数应该在 skill 初始化时调用
        """
        jobs = self.list_cron_jobs()
        
        # 检查哪些任务需要创建/更新
        # 实际调用 openclaw cron 命令
        # 这里只是示例，实际实现需要调用 OpenClaw API
        
        for job in jobs:
            # 检查任务是否过期
            schedule = job["schedule"]
            # 解析 cron 表达式检查是否已过期
            # 如果过期则删除
            pass

if __name__ == "__main__":
    # 测试
    manager = CronManager()
    
    # 创建一个测试任务
    test_time = datetime.now() + timedelta(minutes=5)
    result = manager.create_reminder_cron(
        event_id="test123",
        event_title="测试会议",
        reminder_time=test_time,
        feishu_user_id="ou_669575f70b8b81dd5c431c4ed1ad41c4"
    )
    
    print(f"创建结果: {result}")
    
    # 列出所有任务
    jobs = manager.list_cron_jobs()
    print(f"\n当前任务数: {len(jobs)}")
    for job in jobs:
        print(f"  - {job['name']}: {job['schedule']}")
