#!/usr/bin/env python3
"""
提醒发送器：从任务列表中获取待提醒的任务。
建议通过 cron 每小时运行一次。
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

TASK_MANAGER = Path(__file__).parent / "task_manager.py"

def send_wechat_message(text: str):
    """
    发送消息到微信。
    请根据你的微信接入方式修改此函数。
    """
    # 默认实现：写入日志文件
    log_path = Path.home() / "openclaw_reminders.log"
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()}: {text}\n")
    print(f"提醒已写入日志: {log_path}")
    
    # TODO: 如果你有企业微信或 itchat，请替换为实际发送代码

def get_reminders():
    result = subprocess.run(
        [sys.executable, str(TASK_MANAGER), "remind"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("获取提醒失败:", result.stderr)
        return []
    data = json.loads(result.stdout)
    return data.get("reminders", [])

def format_reminder(task):
    deadline = task["deadline"].replace("T", " ")[:16]
    title = task["title"]
    extra = task.get("extra", {})
    extra_str = ""
    if extra:
        parts = []
        if "cinema" in extra:
            parts.append(f"影院: {extra['cinema']}")
        if "seat" in extra:
            parts.append(f"座位: {extra['seat']}")
        if parts:
            extra_str = " (" + ", ".join(parts) + ")"
    return f"🔔 提醒：{title}\n时间：{deadline}{extra_str}"

def main():
    reminders = get_reminders()
    if not reminders:
        print("没有需要提醒的任务")
        return
    for task in reminders:
        msg = format_reminder(task)
        send_wechat_message(msg)
        print(f"已记录提醒：{task['title']}")

if __name__ == "__main__":
    main()
