#!/usr/bin/env python3
"""
手机端优甲乐智能提醒消息生成器
专为 Feishu 和 WebChat 优化显示
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def generate_mobile_reminder(reminder_count=1, channel="feishu"):
    """生成手机端优化的提醒消息"""
    try:
        from medication_reminder import MedicationReminder
        
        reminder = MedicationReminder()
        
        # 获取数据
        yesterday_status = reminder.get_yesterday_status()
        yesterday_feedback = reminder.get_yesterday_feedback()
        stats = reminder._load_stats()
        today_status = reminder.get_today_status()
        
        # 根据渠道优化消息格式
        if channel == "feishu":
            # 飞书优化格式（支持富文本）
            return generate_feishu_message(
                reminder_count, yesterday_status, yesterday_feedback, 
                stats, today_status
            )
        else:
            # WebChat/通用格式
            return generate_webchat_message(
                reminder_count, yesterday_status, yesterday_feedback, 
                stats, today_status
            )
            
    except Exception as e:
        # 出错时返回默认消息
        return f"⏰ 优甲乐服药提醒\n\n请服用优甲乐。服药后回复确认。"

def generate_feishu_message(reminder_count, yesterday_status, yesterday_feedback, stats, today_status):
    """生成飞书优化消息"""
    # 时间描述
    time_descriptions = [
        "早上6:30，请服用优甲乐",
        "早上6:45，请尽快服用优甲乐", 
        "早上7:00，请立即服用优甲乐",
        "早上7:15，请立即服用优甲乐"
    ]
    
    time_desc = time_descriptions[min(reminder_count-1, 3)]
    
    # 构建飞书富文本消息
    message = f"💊 **优甲乐服药提醒**\n\n"
    message += f"🕐 **时间**：{time_desc}\n\n"
    
    message += f"📊 **昨天状态**\n"
    message += f"{yesterday_status['message']}\n\n"
    
    message += f"💡 **智能反馈**\n"
    message += f"{yesterday_feedback}\n\n"
    
    if stats['current_streak'] > 0:
        message += f"🔥 **连续服药**：{stats['current_streak']}天\n\n"
    
    message += f"📱 **操作指引**\n"
    message += "1. 立即服药\n"
    message += "2. 回复「服药了」或「/medication taken」\n"
    message += "3. 系统自动记录并更新统计\n"
    
    # 添加今日状态（如果已服药）
    if today_status['taken']:
        message += f"\n✅ **今日已服药**：{today_status['time']}"
        if not today_status['is_on_time']:
            message += "（延迟）"
    
    return message

def generate_webchat_message(reminder_count, yesterday_status, yesterday_feedback, stats, today_status):
    """生成WebChat优化消息"""
    # 时间表情和描述
    time_emojis = ["⏰", "🕐", "🕑", "🕒"]
    time_descriptions = [
        "现在是早上6:30，请服用优甲乐",
        "现在是早上6:45，请尽快服用优甲乐",
        "现在是早上7:00，请立即服用优甲乐",
        "现在是早上7:15，请立即服用优甲乐"
    ]
    
    emoji = time_emojis[min(reminder_count-1, 3)]
    time_desc = time_descriptions[min(reminder_count-1, 3)]
    
    # 构建WebChat消息
    message = f"{emoji} **优甲乐智能服药提醒**\n\n"
    message += f"**{time_desc}**\n\n"
    
    message += f"📅 昨天状态：{yesterday_status['message']}\n"
    message += f"💡 智能反馈：{yesterday_feedback}\n\n"
    
    if stats['current_streak'] > 0:
        message += f"🔥 连续服药：{stats['current_streak']}天（继续保持！）\n\n"
    
    message += f"💊 **服药后请回复**：\n"
    message += "• 在飞书中：回复「服药了」\n"
    message += "• 在WebChat：回复「/medication taken」\n"
    message += "• 或直接点击确认链接（如果支持）\n"
    
    # 添加快速操作提示
    message += f"\n⚡ **快速操作**：\n"
    message += "📱 飞书App → 找到此消息 → 回复确认\n"
    message += "💻 WebChat → 直接在此回复\n"
    
    return message

def generate_reminder_for_cron(reminder_count=1):
    """为cron任务生成消息（通用格式）"""
    try:
        from medication_reminder import MedicationReminder
        
        reminder = MedicationReminder()
        yesterday_feedback = reminder.get_yesterday_feedback()
        stats = reminder._load_stats()
        
        # 时间描述
        time_descriptions = [
            "现在是早上6:30，请服用优甲乐",
            "现在是早上6:45，请尽快服用优甲乐",
            "现在是早上7:00，请立即服用优甲乐", 
            "现在是早上7:15，请立即服用优甲乐"
        ]
        
        time_desc = time_descriptions[min(reminder_count-1, 3)]
        
        # 通用消息格式
        message = f"⏰ 优甲乐服药提醒\n\n"
        message += f"{time_desc}\n\n"
        message += f"{yesterday_feedback}\n\n"
        
        if stats['current_streak'] > 0:
            message += f"🔥 你已经连续服药 {stats['current_streak']} 天，继续保持！\n\n"
        
        message += f"💊 服药后请回复确认。"
        
        return message
        
    except Exception as e:
        return "⏰ 请服用优甲乐。服药后回复确认。"

def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="手机端优甲乐提醒生成器")
    parser.add_argument("--count", type=int, default=1, help="提醒次数（1-4）")
    parser.add_argument("--channel", choices=["feishu", "webchat", "auto"], default="auto", help="目标渠道")
    parser.add_argument("--test", action="store_true", help="测试所有渠道")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 测试所有渠道的消息生成：")
        print("\n" + "="*50)
        
        for channel in ["feishu", "webchat"]:
            print(f"\n📱 {channel.upper()} 渠道消息：")
            print("-"*30)
            message = generate_mobile_reminder(args.count, channel)
            print(message)
            print("\n" + "="*50)
        
        print("\n📅 通用cron消息：")
        print("-"*30)
        message = generate_reminder_for_cron(args.count)
        print(message)
        
    else:
        if args.channel == "auto":
            # 自动检测：如果从cron调用，使用通用格式
            message = generate_reminder_for_cron(args.count)
        else:
            message = generate_mobile_reminder(args.count, args.channel)
        
        print(message)
        
        # 同时输出JSON信息（供cron使用）
        import json
        info = {
            "message": message,
            "reminder_count": args.count,
            "channel": args.channel,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
        print(json.dumps(info, ensure_ascii=False), file=sys.stderr)

if __name__ == "__main__":
    main()