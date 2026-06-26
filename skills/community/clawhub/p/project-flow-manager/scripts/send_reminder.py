#!/usr/bin/env python3
"""
发送任务提醒邮件
用法: python3 send_reminder.py <project-id> --recipient EMAIL [--type TYPE]
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

def send_reminder(project_id, recipient, reminder_type="progress"):
    """生成提醒邮件内容"""
    
    project_file = Path("projects") / f"{project_id}.json"
    
    if not project_file.exists():
        print(f"❌ 项目不存在: {project_id}")
        return None
    
    with open(project_file, 'r', encoding='utf-8') as f:
        project = json.load(f)
    
    tasks = project.get("tasks", [])
    now = datetime.now()
    
    # 生成邮件内容
    subject = f"【项目提醒】{project['name']} - {now.strftime('%m月%d日')}"
    
    lines = [
        f"您好，",
        f"",
        f"这是「{project['name']}」的自动进度提醒。",
        f"",
        f"📊 项目概况",
        f"- 项目状态: {project.get('status', 'N/A')}",
    ]
    
    if tasks:
        overall = sum(t.get("progress", 0) for t in tasks) / len(tasks)
        completed = len([t for t in tasks if t.get("status") == "已完成"])
        blocked = len([t for t in tasks if t.get("status") == "已阻塞"])
        
        lines.extend([
            f"- 整体进度: {overall:.1f}%",
            f"- 任务完成: {completed}/{len(tasks)}",
            f""
        ])
        
        if blocked > 0:
            lines.append(f"⚠️ 有 {blocked} 个任务遇到阻塞，需要关注。")
            lines.append("")
        
        # 即将到期的任务
        upcoming = []
        for t in tasks:
            if t.get("status") not in ["已完成", "已取消"] and t.get("endDate"):
                try:
                    due = datetime.strptime(t["endDate"], "%Y-%m-%d")
                    days_left = (due - now).days
                    if 0 <= days_left <= 7:
                        upcoming.append((t, days_left))
                except:
                    pass
        
        if upcoming:
            lines.extend([
                f"📅 即将到期任务 (7天内):",
                f""
            ])
            for t, days in sorted(upcoming, key=lambda x: x[1]):
                urgency = "🔴" if days <= 1 else "🟡" if days <= 3 else "🟢"
                lines.append(f"{urgency} {t['name']} - 还剩{days}天 ({t.get('endDate')})")
            lines.append("")
        
        # 阻塞的任务
        blocked_tasks = [t for t in tasks if t.get("status") == "已阻塞"]
        if blocked_tasks:
            lines.extend([
                f"🚫 阻塞中的任务:",
                f""
            ])
            for t in blocked_tasks:
                lines.append(f"- {t['name']}: {', '.join(t.get('blockers', ['未说明原因']))}")
            lines.append("")
    
    lines.extend([
        f"---",
        f"",
        f"如需查看详细信息，请访问项目看板。",
        f"",
        f"此邮件由项目管理系统自动发送",
        f"发送时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    ])
    
    email_content = "\n".join(lines)
    
    # 保存邮件草稿
    emails_dir = Path("emails")
    emails_dir.mkdir(exist_ok=True)
    
    email_file = emails_dir / f"{project_id}-reminder-{now.strftime('%Y%m%d')}.txt"
    
    with open(email_file, 'w', encoding='utf-8') as f:
        f.write(f"收件人: {recipient}\n")
        f.write(f"主题: {subject}\n")
        f.write(f"\n{'='*50}\n\n")
        f.write(email_content)
    
    print(f"✅ 提醒邮件已生成!")
    print(f"   收件人: {recipient}")
    print(f"   主题: {subject}")
    print(f"   文件: {email_file}")
    print(f"")
    print(f"💡 提示: 请使用邮件客户端发送此邮件，或配置SMTP自动发送")
    print(f"   配置方法见 references/email-config.md")
    
    return email_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="发送任务提醒")
    parser.add_argument("project_id", help="项目ID")
    parser.add_argument("--recipient", "-r", required=True, help="收件人邮箱")
    parser.add_argument("--type", "-t", default="progress",
                        choices=["progress", "deadline", "blocker"],
                        help="提醒类型")
    
    args = parser.parse_args()
    
    send_reminder(args.project_id, args.recipient, args.type)
