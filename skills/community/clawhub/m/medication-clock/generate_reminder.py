#!/usr/bin/env python3
"""
生成优甲乐智能提醒消息
这个脚本被 OpenClaw cron 任务调用，生成包含昨天状态的智能提醒
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def generate_reminder_message(reminder_count=1):
    """生成智能提醒消息"""
    try:
        from medication_reminder import MedicationReminder
        
        reminder = MedicationReminder()
        message = reminder.get_smart_reminder_message(reminder_count)
        
        # 返回纯文本消息
        return message
    
    except Exception as e:
        # 如果出错，返回默认消息
        default_messages = [
            "⏰ 优甲乐服药提醒\\n\\n现在是早上6:30，请服用优甲乐。\\n💊 服药后请回复：/medication taken",
            "⏰ 优甲乐服药提醒\\n\\n现在是早上6:45，请尽快服用优甲乐。\\n💊 服药后请回复：/medication taken",
            "⏰ 优甲乐服药提醒\\n\\n现在是早上7:00，请立即服用优甲乐。\\n💊 服药后请回复：/medication taken",
            "⏰ 优甲乐服药提醒\\n\\n现在是早上7:15，请立即服用优甲乐。\\n💊 服药后请回复：/medication taken"
        ]
        
        index = min(reminder_count - 1, len(default_messages) - 1)
        return default_messages[index]

def main():
    """主函数"""
    # 从命令行参数获取提醒次数
    reminder_count = 1
    if len(sys.argv) > 1:
        try:
            reminder_count = int(sys.argv[1])
        except ValueError:
            reminder_count = 1
    
    # 生成消息
    message = generate_reminder_message(reminder_count)
    
    # 输出消息
    print(message)
    
    # 同时输出为 JSON 格式，方便 OpenClaw 解析
    import json
    result = {
        "message": message,
        "reminder_count": reminder_count,
        "success": True
    }
    
    # 输出到 stderr，避免干扰主输出
    print(json.dumps(result, ensure_ascii=False), file=sys.stderr)

if __name__ == "__main__":
    main()