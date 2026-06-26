#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提醒检查脚本 - 由 OpenClaw 定时任务调用
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

def check_reminders():
    """检查需要发送的提醒"""
    data_dir = Path(__file__).parent.parent / "data"
    db_path = data_dir / "scheduler.db"
    
    if not db_path.exists():
        print("[INFO] 数据库不存在，跳过")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    now = datetime.now()
    # 检查未来5分钟内需要提醒的事件
    check_window = now + timedelta(minutes=5)
    
    cursor.execute('''
        SELECT r.id, r.event_id, e.title, e.start_time, e.location, e.reminder_minutes
        FROM reminders r
        JOIN events e ON r.event_id = e.id
        WHERE r.reminder_time <= ? AND r.reminder_time >= ? AND r.is_sent = 0
    ''', (check_window, now))
    
    reminders = cursor.fetchall()
    
    for reminder in reminders:
        reminder_id, event_id, title, start_time, location, reminder_minutes = reminder
        
        # 构建提醒消息
        start_dt = datetime.fromisoformat(start_time)
        time_str = start_dt.strftime('%H:%M')
        date_str = start_dt.strftime('%m月%d日')
        
        message = f"""⏰ 日程提醒

📌 {title}
🕐 {date_str} {time_str}"""
        
        if location:
            message += f"\n📍 {location}"
        
        message += f"\n⏳ 还有 {reminder_minutes} 分钟"
        
        # 输出消息（OpenClaw 会捕获并发送）
        print(message)
        print("---")
        
        # 标记为已发送
        cursor.execute('UPDATE reminders SET is_sent = 1 WHERE id = ?', (reminder_id,))
    
    conn.commit()
    conn.close()
    
    if reminders:
        print(f"[OK] 已处理 {len(reminders)} 个提醒")
    else:
        print("[OK] 没有待发送的提醒")

if __name__ == "__main__":
    check_reminders()
