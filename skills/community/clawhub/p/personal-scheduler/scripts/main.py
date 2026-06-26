#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人日程管理 Skill - 主入口（集成自动提醒）
支持自然语言交互，自动创建定时提醒任务
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 添加脚本路径
sys.path.insert(0, str(Path(__file__).parent))

from scheduler import PersonalScheduler
from natural_language import NaturalLanguageParser

def main():
    scheduler = PersonalScheduler()
    parser = NaturalLanguageParser()
    
    if len(sys.argv) < 2:
        print("="*60)
        print("个人日程管理 Skill")
        print("="*60)
        print("\n用法:")
        print('  python main.py "明天下午3点开会"')
        print('  python main.py "后天晚上7点吃饭"')
        print('  python main.py list')
        print('  python main.py web')
        print("="*60)
        return
    
    command = sys.argv[1]
    
    if command == "list":
        # 列出今日日程
        events = scheduler.list_events()
        if events:
            print(f"\n今日日程 ({len(events)} 个):")
            print("-" * 50)
            for event in events[:5]:
                print(f"  {event[1]}")
                print(f"     {event[2]} - {event[3]}")
                if event[4]:
                    print(f"     地点: {event[4]}")
                print()
        else:
            print("\n今日暂无日程")
    
    elif command == "web":
        # 启动 Web 服务
        import web_server
    
    elif command == "check":
        # 检查并执行待发送的提醒
        pending = scheduler.get_pending_reminders()
        if pending:
            print(f"发现 {len(pending)} 个待发送提醒:")
            for job in pending:
                print(f"  - {job['event_title']}: {job['reminder_time']}")
                # 执行发送
                import subprocess
                subprocess.run(['python', 'send_reminder.py', job['event_id']])
        else:
            print("没有待发送的提醒")
    
    else:
        # 自然语言解析
        text = command
        result = parser.parse(text)
        
        print(f"\n输入: {text}")
        
        # 转换 datetime 为字符串以便打印
        result_display = result.copy()
        if result_display.get('start_time'):
            result_display['start_time'] = result_display['start_time'].strftime('%Y-%m-%d %H:%M')
        if result_display.get('end_time'):
            result_display['end_time'] = result_display['end_time'].strftime('%Y-%m-%d %H:%M')
        print(f"解析: {json.dumps(result_display, ensure_ascii=False, indent=2)}")
        
        if result['action'] == 'create':
            # 创建日程 - 自动创建提醒任务
            event_result = scheduler.add_event(
                title=result['title'],
                start_time=result['start_time'],
                end_time=result['end_time'],
                location=result.get('location'),
                reminder_minutes=result.get('reminder_minutes', 15),
                repeat_rule=result.get('repeat_rule')
            )
            
            print(f"\n已创建日程: {event_result['title']}")
            print(f"   时间: {event_result['start_time']}")
            if result.get('location'):
                print(f"   地点: {result['location']}")
            if result.get('repeat_rule'):
                print(f"   重复: {result['repeat_rule']}")
            
            # 显示提醒任务信息
            reminder = event_result['reminder_job']
            if reminder['created']:
                print(f"\n已设置提醒:")
                print(f"   提醒时间: {reminder['reminder_time']}")
                print(f"   提前: {event_result['reminder_minutes']} 分钟")
            else:
                print(f"\n提醒未创建: {reminder['reason']}")
        
        elif result['action'] == 'delete':
            # 删除日程
            query = result.get('query', '')
            # 先搜索匹配的日程
            events = scheduler.list_events()
            matched = []
            for event in events:
                if query in event[1] or query in str(event[2]):  # 匹配标题或时间
                    matched.append(event)
            
            if matched:
                if len(matched) == 1:
                    event = matched[0]
                    scheduler.delete_event(event[0])
                    print(f"\n已删除日程: {event[1]}")
                else:
                    print(f"\n找到 {len(matched)} 个匹配日程:")
                    for i, event in enumerate(matched, 1):
                        print(f"  {i}. {event[1]} ({event[2]})")
                    print("请指定更精确的时间或标题")
            else:
                print(f"\n未找到匹配的日程: {query}")
        
        elif result['action'] == 'update':
            # 修改日程
            query = result.get('query', '')
            changes = result.get('changes', {})
            
            if not query:
                print("\n请指定要修改的日程，例如：把明天3点的会议改到4点")
                return
            
            # 搜索匹配的日程
            events = scheduler.list_events()
            matched = []
            for event in events:
                if query in event[1] or query in str(event[2]):
                    matched.append(event)
            
            if not matched:
                print(f"\n未找到匹配的日程: {query}")
                return
            
            if len(matched) > 1:
                print(f"\n找到 {len(matched)} 个匹配日程:")
                for i, event in enumerate(matched, 1):
                    print(f"  {i}. {event[1]} ({event[2]})")
                print("请指定更精确的时间或标题")
                return
            
            # 修改日程
            event = matched[0]
            event_id = event[0]
            
            # 获取修改后的时间
            if 'start_time' in changes:
                new_start = changes['start_time']
                new_end = changes['end_time']
                # 删除旧日程，创建新日程
                scheduler.delete_event(event_id)
                new_result = scheduler.add_event(
                    title=event[1],
                    start_time=new_start,
                    end_time=new_end,
                    location=event[4],
                    reminder_minutes=event[6]
                )
                print(f"\n已修改日程: {event[1]}")
                print(f"   新时间: {new_start}")
            
            elif 'postpone_minutes' in changes:
                # 推迟
                from datetime import timedelta
                old_start = datetime.fromisoformat(event[2])
                old_end = datetime.fromisoformat(event[3])
                new_start = old_start + timedelta(minutes=changes['postpone_minutes'])
                new_end = old_end + timedelta(minutes=changes['postpone_minutes'])
                
                scheduler.delete_event(event_id)
                new_result = scheduler.add_event(
                    title=event[1],
                    start_time=new_start,
                    end_time=new_end,
                    location=event[4],
                    reminder_minutes=event[6]
                )
                print(f"\n已推迟日程: {event[1]}")
                print(f"   新时间: {new_start}")
            
            elif 'advance_minutes' in changes:
                # 提前
                from datetime import timedelta
                old_start = datetime.fromisoformat(event[2])
                old_end = datetime.fromisoformat(event[3])
                new_start = old_start - timedelta(minutes=changes['advance_minutes'])
                new_end = old_end - timedelta(minutes=changes['advance_minutes'])
                
                scheduler.delete_event(event_id)
                new_result = scheduler.add_event(
                    title=event[1],
                    start_time=new_start,
                    end_time=new_end,
                    location=event[4],
                    reminder_minutes=event[6]
                )
                print(f"\n已提前日程: {event[1]}")
                print(f"   新时间: {new_start}")
            
            else:
                print("\n未能解析修改内容")

if __name__ == "__main__":
    main()
