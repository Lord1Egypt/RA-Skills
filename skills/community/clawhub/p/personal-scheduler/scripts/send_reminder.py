#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送提醒消息 - 由定时任务调用
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

def send_reminder(event_id: str, feishu_user_id: str = None):
    """发送日程提醒"""
    
    # 连接数据库
    data_dir = Path(__file__).parent.parent / "data"
    db_path = data_dir / "scheduler.db"
    
    if not db_path.exists():
        print(f"[ERROR] 数据库不存在: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询日程信息
    cursor.execute('''
        SELECT title, start_time, end_time, location, reminder_minutes
        FROM events WHERE id = ?
    ''', (event_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        print(f"[ERROR] 找不到日程: {event_id}")
        return
    
    title, start_time, end_time, location, reminder_minutes = row
    
    # 解析时间
    start_dt = datetime.fromisoformat(start_time)
    time_str = start_dt.strftime('%H:%M')
    date_str = start_dt.strftime('%m月%d日')
    
    # 构建提醒消息
    message_lines = [
        "⏰ 日程提醒",
        "",
        f"📌 {title}",
        f"🕐 {date_str} {time_str}",
    ]
    
    if location:
        message_lines.append(f"📍 {location}")
    
    message_lines.append(f"⏳ 还有 {reminder_minutes} 分钟")
    
    message = "\n".join(message_lines)
    
    # 输出消息（OpenClaw 会捕获并发送到飞书）
    print(message)
    
    # 如果有飞书用户ID，可以通过 OpenClaw 发送
    if feishu_user_id:
        # 实际发送逻辑由 OpenClaw 处理
        # 这里只是标记需要发送
        print(f"\n[TO: {feishu_user_id}]")
    
    return message

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python send_reminder.py <event_id> [--user <feishu_user_id>]")
        sys.exit(1)
    
    event_id = sys.argv[1]
    user_id = None
    
    # 解析参数
    if "--user" in sys.argv:
        idx = sys.argv.index("--user")
        if idx + 1 < len(sys.argv):
            user_id = sys.argv[idx + 1]
    
    # 从配置文件读取默认用户
    if not user_id:
        config_path = Path(__file__).parent.parent / "data" / "config.json"
        if config_path.exists():
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                user_id = config.get('feishu_user_id')
    
    send_reminder(event_id, user_id)
