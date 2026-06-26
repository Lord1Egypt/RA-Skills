#!/usr/bin/env python3
"""
OpenClaw 优甲乐服药提醒集成
提供与 OpenClaw 命令系统集成的接口
"""

import os
import sys
import json
import datetime
from pathlib import Path

# 添加父目录到路径，以便导入 medication_reminder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medication_reminder import MedicationReminder


def generate_smart_reminder_message(reminder_count=1):
    """生成智能提醒消息（供其他模块调用的统一函数）"""
    try:
        reminder = MedicationReminder()
        return reminder.get_smart_reminder_message(reminder_count)
    except Exception:
        # 出错时返回默认消息
        default_messages = [
            "⏰ 优甲乐服药提醒\n\n现在是早上6:30，请服用优甲乐。\n💊 服药后请回复：/medication taken",
            "⏰ 优甲乐服药提醒\n\n现在是早上6:45，请尽快服用优甲乐。\n💊 服药后请回复：/medication taken",
            "⏰ 优甲乐服药提醒\n\n现在是早上7:00，请立即服用优甲乐。\n💊 服药后请回复：/medication taken",
            "⏰ 优甲乐服药提醒\n\n现在是早上7:15，请立即服用优甲乐。\n💊 服药后请回复：/medication taken"
        ]
        index = min(reminder_count - 1, len(default_messages) - 1)
        return default_messages[index]


class OpenClawMedicationIntegration:
    """OpenClaw 集成类"""
    
    def __init__(self):
        self.reminder = MedicationReminder()
        self.setup_commands()
    
    def setup_commands(self):
        """设置命令处理器"""
        self.commands = {
            "start": self.start_daily_reminders,
            "stop": self.stop_daily_reminders,
            "taken": self.record_taken,
            "status": self.get_status,
            "report": self.generate_report,
            "records": self.get_records,
            "export": self.export_data,
            "help": self.show_help,
            "settings": self.show_settings,
            "test-reminder": self.test_reminder
        }
    
    def process_command(self, command, args=None):
        """处理命令"""
        if command in self.commands:
            return self.commands[command](args)
        else:
            return self.show_help()
    
    def start_daily_reminders(self, args=None):
        """启动每日提醒"""
        # 这里需要设置 OpenClaw cron 任务
        # 实际实现中，这里会调用 OpenClaw 的 cron API
        settings = self.reminder.get_settings()
        settings["reminder_enabled"] = True
        self.reminder.update_settings(reminder_enabled=True)
        
        # 生成智能提醒消息示例
        smart_message_630 = self.reminder.get_smart_reminder_message(reminder_count=1)
        smart_message_645 = self.reminder.get_smart_reminder_message(reminder_count=2)
        smart_message_700 = self.reminder.get_smart_reminder_message(reminder_count=3)
        
        return {
            "type": "text",
            "content": "✅ 已启动每日优甲乐服药提醒系统\n"
                      f"⏰ 首次提醒时间：{settings['first_reminder_time']}\n"
                      f"🔄 重复提醒：6:45, 7:00, 7:15\n"
                      f"📅 从明天开始生效\n\n"
                      f"💡 **智能提醒功能已启用**\n"
                      f"• 每次提醒都会关注昨天服药状态\n"
                      f"• 根据昨天状态提供个性化反馈\n"
                      f"• 显示连续服药天数鼓励\n\n"
                      f"📋 **提醒消息示例**\n"
                      f"6:30提醒：\n{smart_message_630[:100]}...\n\n"
                      f"6:45提醒：\n{smart_message_645[:100]}..."
        }
    
    def stop_daily_reminders(self, args=None):
        """停止每日提醒"""
        self.reminder.update_settings(reminder_enabled=False)
        return {
            "type": "text",
            "content": "⏸️ 已停止每日优甲乐服药提醒"
        }
    
    def record_taken(self, args=None):
        """记录服药"""
        # 解析可选的时间参数
        taken_time = None
        if args and len(args) > 0:
            # 时间格式检查和验证
            import re
            time_pattern = r'^(\d{1,2}):(\d{2})$'
            match = re.match(time_pattern, args[0])
            if match:
                hour, minute = int(match.group(1)), int(match.group(2))
                # 验证时间有效性
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    taken_time = args[0]

        result = self.reminder.record_medication(taken_time, manual=False)
        
        # 获取今日状态以提供完整反馈
        status = self.reminder.get_today_status()
        stats = self.reminder._load_stats()
        
        response = f"{result['message']}\n\n"
        response += f"📊 今日状态：{status['status']}\n"
        response += f"🔥 连续服药：{stats['current_streak']} 天\n"
        response += f"🏆 最佳记录：{stats['best_streak']} 天"
        
        return {
            "type": "text",
            "content": response
        }
    
    def get_status(self, args=None):
        """获取状态"""
        status = self.reminder.get_today_status()
        stats = self.reminder._load_stats()
        settings = self.reminder.get_settings()
        
        # 获取最近5条记录
        recent_records = self.reminder.get_records()[:5]
        
        response = f"📊 **优甲乐服药状态**\n\n"
        response += f"**今日状态**：{status['status']}\n"
        response += f"📝 {status['message']}\n\n"
        
        response += f"**统计数据**\n"
        response += f"📅 总服药天数：{stats['total_days']}\n"
        response += f"✅ 按时服药天数：{stats['on_time_days']}\n"
        response += f"🔥 当前连续服药：{stats['current_streak']} 天\n"
        response += f"🏆 最佳连续服药：{stats['best_streak']} 天\n\n"
        
        if recent_records:
            response += f"**最近服药记录**\n"
            for record in recent_records:
                emoji = "✅" if record["is_on_time"] else "⚠️"
                response += f"{emoji} {record['date']} {record['time']}\n"
        
        return {
            "type": "text",
            "content": response
        }
    
    def generate_report(self, args=None):
        """生成报告"""
        days = 7  # 默认7天
        if args and len(args) > 0:
            try:
                days = int(args[0])
                if days < 1 or days > 365:
                    days = 7
            except ValueError:
                pass
        
        report = self.reminder.generate_report(days)
        
        # 构建格式化的报告
        response = f"📈 **优甲乐服药统计报告**\n\n"
        response += f"**报告期间**：{report['period']}\n"
        response += f"📊 **服药依从率**：{report['compliance_rate']}%\n\n"
        
        response += f"**统计摘要**\n"
        response += f"📅 总天数：{report['total_days']}\n"
        response += f"✅ 服药天数：{report['taken_days']}\n"
        response += f"⏰ 按时天数：{report['on_time_days']}\n"
        response += f"🔥 当前连续服药：{report['current_streak']} 天\n"
        response += f"🏆 最佳连续服药：{report['best_streak']} 天\n\n"
        
        # 添加每日详情（最近7天）
        response += f"**每日详情（最近7天）**\n"
        recent_data = report["data"][:7] if len(report["data"]) > 7 else report["data"]
        for item in recent_data:
            # 将日期格式化为更友好的形式
            date_obj = datetime.date.fromisoformat(item["date"])
            weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]
            formatted_date = f"{date_obj.month}/{date_obj.day} {weekday}"
            
            response += f"{formatted_date} - {item['time']} ({item['status']})\n"
        
        return {
            "type": "text",
            "content": response
        }
    
    def get_records(self, args=None):
        """获取记录"""
        days = None
        if args and len(args) > 0:
            try:
                days = int(args[0])
            except ValueError:
                pass
        
        if days:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=days-1)
            records = self.reminder.get_records(start_date, end_date)
            title = f"最近{days}天服药记录"
        else:
            records = self.reminder.get_records()[:10]
            title = "最近服药记录"
        
        if not records:
            return {
                "type": "text",
                "content": f"📭 {title}：暂无记录"
            }
        
        response = f"📋 **{title}**（共 {len(records)} 条）\n\n"
        
        for record in records:
            date_obj = datetime.date.fromisoformat(record["date"])
            weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]
            formatted_date = f"{date_obj.month}/{date_obj.day} {weekday}"
            
            status = "⏰ 按时" if record["is_on_time"] else "⚠️ 延迟"
            manual = "（手动记录）" if record.get("manual", False) else ""
            
            response += f"**{formatted_date}**\n"
            response += f"🕐 时间：{record['time']} {status}{manual}\n\n"
        
        return {
            "type": "text",
            "content": response
        }
    
    def export_data(self, args=None):
        """导出数据"""
        try:
            export_path = self.reminder.export_to_csv()
            return {
                "type": "text",
                "content": f"✅ 数据已导出到：\n`{export_path}`\n\n"
                          f"📁 文件位置：{export_path}"
            }
        except Exception as e:
            return {
                "type": "text",
                "content": f"❌ 导出失败：{str(e)}"
            }

    def test_reminder(self, args=None):
        """测试智能提醒消息"""
        reminder_count = 1
        if args and len(args) > 0:
            try:
                reminder_count = int(args[0])
                if reminder_count < 1 or reminder_count > 4:
                    reminder_count = 1
            except ValueError:
                reminder_count = 1
        
        # 获取昨天状态
        yesterday_status = self.reminder.get_yesterday_status()
        yesterday_feedback = self.reminder.get_yesterday_feedback()
        
        # 生成智能提醒
        smart_message = self.reminder.get_smart_reminder_message(reminder_count)
        
        response = f"🔬 **智能提醒测试**（第{reminder_count}次提醒）\n\n"
        response += f"📊 **昨天服药状态**\n"
        response += f"{yesterday_status['message']}\n\n"
        
        response += f"💡 **智能反馈**\n"
        response += f"{yesterday_feedback}\n\n"
        
        response += f"📝 **生成的提醒消息**\n"
        response += f"{smart_message}\n\n"
        
        response += f"⏰ **提醒时间对应**\n"
        times = ["6:30", "6:45", "7:00", "7:15"]
        for i, time in enumerate(times, 1):
            indicator = "✅" if i == reminder_count else "  "
            response += f"{indicator} 第{i}次提醒：{time}\n"
        
        return {
            "type": "text",
            "content": response
        }
    
    def show_settings(self, args=None):
        """显示设置"""
        settings = self.reminder.get_settings()
        
        response = "⚙️ **优甲乐提醒设置**\n\n"
        response += f"🔔 提醒状态：{'✅ 已启用' if settings['reminder_enabled'] else '⏸️ 已停用'}\n"
        response += f"⏰ 首次提醒：{settings['first_reminder_time']}\n"
        response += f"🔄 重复提醒：6:45, 7:00, 7:15\n"
        response += f"✅ 按时窗口：{settings['on_time_window']}分钟（{settings['first_reminder_time']}之后）\n"
        response += f"📢 通知渠道：{settings['notification_channel']}\n"
        response += f"💡 智能提醒：✅ 已启用（关注昨天状态）\n\n"
        
        # 显示昨天状态示例
        yesterday_status = self.reminder.get_yesterday_status()
        response += f"📊 **昨天状态示例**\n"
        response += f"{yesterday_status['message']}\n\n"
        
        response += "💡 提示：要修改设置，请直接编辑配置文件"
        
        return {
            "type": "text",
            "content": response
        }
    
    def generate_smart_reminder(self, reminder_count=1):
        """生成智能提醒消息（用于 cron 任务）"""
        try:
            message = generate_smart_reminder_message(reminder_count)
            return {
                "type": "text",
                "content": message
            }
        except Exception as e:
            # 出错时返回默认消息
            default_messages = [
                "⏰ 优甲乐服药提醒\n\n现在是早上6:30，请服用优甲乐。\n💊 服药后请回复：/medication taken",
                "⏰ 优甲乐服药提醒\n\n现在是早上6:45，请尽快服用优甲乐。\n💊 服药后请回复：/medication taken",
                "⏰ 优甲乐服药提醒\n\n现在是早上7:00，请立即服用优甲乐。\n💊 服药后请回复：/medication taken",
                "⏰ 优甲乐服药提醒\n\n现在是早上7:15，请立即服用优甲乐。\n💊 服药后请回复：/medication taken"
            ]

            index = min(reminder_count - 1, len(default_messages) - 1)
            return {
                "type": "text",
                "content": default_messages[index]
            }

    def show_help(self, args=None):
        """显示帮助"""
        help_text = """💊 **优甲乐服药提醒系统 - 专业版** - 使用帮助

**基本命令**：
`/medication-clock start` - 启动每日提醒
`/medication-clock stop` - 停止每日提醒
`/medication-clock taken [时间]` - 记录服药（可指定时间，如：07:15）
`/medication-clock status` - 查看今日状态和统计
`/medication-clock report [天数]` - 生成服药报告（默认7天）
`/medication-clock records [天数]` - 查看服药记录
`/medication-clock export` - 导出数据为CSV
`/medication-clock settings` - 查看当前设置
`/medication-clock test-reminder [次数]` - 测试智能提醒消息（1-4）
`/medication-clock help` - 显示此帮助

**示例**：
- `/medication-clock taken` - 记录当前时间服药
- `/medication-clock taken 07:15` - 记录7:15服药
- `/medication-clock report 30` - 生成30天报告
- `/medication-clock records 14` - 查看最近14天记录

**功能说明**：
- 每日6:30首次提醒服用优甲乐
- 每15分钟重复提醒，直到确认
- 自动记录服药时间和状态
- 提供统计报表和依从性分析
- 双渠道支持（Feishu + WebChat）
- 智能反馈系统（关注昨天状态）
- 数据本地存储，安全私密

**数据存储**：
所有数据存储在 `~/.openclaw/medication_data/` 目录下
"""
        
        return {
            "type": "text",
            "content": help_text
        }

def handle_medication_command(command_text):
    """
    处理服药命令的外部接口
    
    Args:
        command_text: 命令文本，如 "taken" 或 "status 30"
    
    Returns:
        格式化的响应字典
    """
    integration = OpenClawMedicationIntegration()
    
    # 解析命令和参数
    parts = command_text.strip().split()
    if not parts:
        return integration.show_help()
    
    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else None
    
    return integration.process_command(command, args)

def test_integration():
    """测试集成功能"""
    print("🧪 测试优甲乐服药提醒系统...\n")
    
    integration = OpenClawMedicationIntegration()
    
    # 测试各种命令
    commands = [
        ("help", None),
        ("status", None),
        ("taken", None),
        ("status", None),
        ("report", ["7"]),
        ("records", ["5"]),
        ("settings", None)
    ]
    
    for cmd, args in commands:
        print(f"\n{'='*50}")
        print(f"测试命令: /medication {cmd} {' '.join(args) if args else ''}")
        print(f"{'='*50}")
        
        result = integration.process_command(cmd, args)
        print(result["content"])
        print()

if __name__ == "__main__":
    # 如果直接运行，进行测试
    if len(sys.argv) > 1:
        # 命令行模式
        command_text = " ".join(sys.argv[1:])
        result = handle_medication_command(command_text)
        print(result["content"])
    else:
        # 测试模式
        test_integration()