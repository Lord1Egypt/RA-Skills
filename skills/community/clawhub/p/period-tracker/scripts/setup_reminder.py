#!/usr/bin/env python3
"""
setup_reminder.py - 经期提醒设置脚本
通过 cron 在预测经期前 N 天发送系统通知
"""

import argparse
import subprocess
import json
import sys
from datetime import date, timedelta
from pathlib import Path

DATA_PATH = Path.home() / ".openclaw" / "workspace" / "period_tracker" / "data.json"
TRACKER_SCRIPT = Path(__file__).parent / "period_tracker.py"
CRON_TAG = "# period-tracker-reminder"


def get_next_period_date() -> str:
    """调用 period_tracker 获取下次经期日期"""
    try:
        result = subprocess.run(
            [sys.executable, str(TRACKER_SCRIPT), "predict"],
            capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if "下次预测经期" in line:
                # 提取 YYYY-MM-DD
                import re
                dates = re.findall(r"\d{4}-\d{2}-\d{2}", line)
                if dates:
                    return dates[0]
    except Exception as e:
        print(f"⚠️  无法获取预测日期：{e}")
    return None


def list_reminders():
    """列出当前经期提醒 cron 任务"""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        lines = [l for l in result.stdout.splitlines() if CRON_TAG in l]
        if lines:
            print("📋 当前经期提醒：")
            for l in lines:
                print(f"  {l}")
        else:
            print("暂无经期提醒设置")
    except Exception as e:
        print(f"读取 cron 失败：{e}")


def add_reminder(days_before: int, hour: int = 9, minute: int = 0, reminder_type: str = "period"):
    """设置提前 N 天的经期提醒"""
    next_date = get_next_period_date()
    if not next_date:
        print("❌ 无法获取预测日期，请先添加至少一条经期记录")
        return

    from datetime import datetime
    remind_date = datetime.strptime(next_date, "%Y-%m-%d").date() - timedelta(days=days_before)
    today = date.today()

    if remind_date <= today:
        print(f"⚠️  提醒日期 {remind_date} 已过（预测经期 {next_date}，提前 {days_before} 天）")
        print("   建议减少提前天数，或等待下次经期记录后重新设置")
        return

    # cron 格式：minute hour day month *
    cron_line = (
        f"{minute} {hour} {remind_date.day} {remind_date.month} * "
        f'python3 {TRACKER_SCRIPT} today {CRON_TAG} type={reminder_type} days_before={days_before}'
    )

    # 读取现有 crontab
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    existing = result.stdout if result.returncode == 0 else ""

    # 移除同类旧提醒
    lines = [l for l in existing.splitlines() if CRON_TAG not in l or f"type={reminder_type}" not in l]
    lines.append(cron_line)
    new_crontab = "\n".join(lines) + "\n"

    proc = subprocess.run(["crontab", "-"], input=new_crontab, text=True, capture_output=True)
    if proc.returncode == 0:
        print(f"✅ 已设置经期提醒")
        print(f"   下次预测经期：{next_date}")
        print(f"   提醒时间：{remind_date} {hour:02d}:{minute:02d}（提前 {days_before} 天）")
    else:
        print(f"❌ 设置 cron 失败：{proc.stderr}")


def add_daily_report(hour: int = 9, minute: int = 0):
    """设置每日经期数据报告"""
    # cron 格式：每天固定时间执行
    cron_line = (
        f"{minute} {hour} * * * "
        f'python3 {TRACKER_SCRIPT} today {CRON_TAG} type=daily_report'
    )

    # 读取现有 crontab
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    existing = result.stdout if result.returncode == 0 else ""

    # 移除同类旧提醒
    lines = [l for l in existing.splitlines() if CRON_TAG not in l or "type=daily_report" not in l]
    lines.append(cron_line)
    new_crontab = "\n".join(lines) + "\n"

    proc = subprocess.run(["crontab", "-"], input=new_crontab, text=True, capture_output=True)
    if proc.returncode == 0:
        print(f"✅ 已设置每日经期报告")
        print(f"   报告时间：每天 {hour:02d}:{minute:02d}")
        print(f"   报告内容：经期状态、排卵信息、受孕指数")
    else:
        print(f"❌ 设置 cron 失败：{proc.stderr}")


def add_ovulation_reminder(days_before: int = 2, hour: int = 9, minute: int = 0):
    """设置排卵日提醒"""
    # 这里简化处理，实际应该计算排卵日
    print("⚠️  排卵日提醒功能需要配合周期计算，建议先记录至少2次经期")
    print("   当前可使用每日报告功能，会自动包含排卵信息")


def remove_reminders(reminder_type: str = None):
    """清除经期提醒"""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if result.returncode != 0:
        print("暂无 crontab")
        return
    
    if reminder_type:
        # 只清除特定类型的提醒
        lines = [l for l in result.stdout.splitlines() if CRON_TAG not in l or f"type={reminder_type}" not in l]
    else:
        # 清除所有经期提醒
        lines = [l for l in result.stdout.splitlines() if CRON_TAG not in l]
    
    new_crontab = "\n".join(lines) + "\n"
    subprocess.run(["crontab", "-"], input=new_crontab, text=True)
    
    if reminder_type:
        print(f"✅ 已清除 {reminder_type} 提醒")
    else:
        print("✅ 已清除所有经期提醒")


def parse_natural_language(text: str) -> dict:
    """解析自然语言设置提醒"""
    text = text.lower().strip()
    result = {"type": None, "days": 3, "hour": 9, "minute": 0}
    
    # 判断提醒类型
    if "每天" in text or "每日" in text or "日报" in text:
        result["type"] = "daily"
    elif "经期" in text or "月经" in text or "大姨妈" in text:
        result["type"] = "period"
    elif "排卵" in text:
        result["type"] = "ovulation"
    else:
        result["type"] = "period"  # 默认经期提醒
    
    # 解析提前天数
    import re
    days_match = re.search(r'(\d+)\s*天', text)
    if days_match:
        result["days"] = int(days_match.group(1))
    
    # 解析时间
    time_match = re.search(r'(\d{1,2})\s*[:点]\s*(\d{0,2})', text)
    if time_match:
        result["hour"] = int(time_match.group(1))
        minute_str = time_match.group(2)
        result["minute"] = int(minute_str) if minute_str else 0
    
    # 处理上午/下午
    if "下午" in text or "晚上" in text or "傍晚" in text:
        if result["hour"] < 12:
            result["hour"] += 12
    elif "上午" in text or "早上" in text or "早晨" in text:
        if result["hour"] > 12:
            result["hour"] -= 12
    
    return result


def setup_from_natural_language(text: str):
    """从自然语言设置提醒"""
    config = parse_natural_language(text)
    
    print(f"📝 解析设置：{text}")
    print(f"   提醒类型：{config['type']}")
    print(f"   提醒时间：{config['hour']:02d}:{config['minute']:02d}")
    
    if config["type"] == "daily":
        add_daily_report(config["hour"], config["minute"])
    elif config["type"] == "period":
        add_reminder(config["days"], config["hour"], config["minute"], "period")
        print(f"   提前天数：{config['days']}天")
    elif config["type"] == "ovulation":
        add_ovulation_reminder(config["days"], config["hour"], config["minute"])
    
    print(f"\n✅ 设置完成！")
    print(f"💡 如需取消，说\"取消经期提醒\"")


def main():
    parser = argparse.ArgumentParser(description="经期提醒设置")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="添加经期提醒")
    p_add.add_argument("--days", type=int, default=3, help="提前天数（默认3天）")
    p_add.add_argument("--hour", type=int, default=9, help="提醒小时（24h，默认9）")
    p_add.add_argument("--minute", type=int, default=0, help="提醒分钟（默认0）")

    p_daily = sub.add_parser("daily", help="设置每日经期报告")
    p_daily.add_argument("--hour", type=int, default=9, help="报告时间小时（默认9）")
    p_daily.add_argument("--minute", type=int, default=0, help="报告时间分钟（默认0）")

    sub.add_parser("list", help="列出所有提醒")
    
    p_remove = sub.add_parser("remove", help="清除提醒")
    p_remove.add_argument("--type", choices=["period", "daily_report"], help="清除特定类型的提醒")
    
    p_natural = sub.add_parser("自然语言", help="使用自然语言设置提醒")
    p_natural.add_argument("text", nargs="+", help="自然语言描述，如：每天早上9点发经期报告")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return

    if args.cmd == "add":
        add_reminder(args.days, args.hour, args.minute, "period")
    elif args.cmd == "daily":
        add_daily_report(args.hour, args.minute)
    elif args.cmd == "list":
        list_reminders()
    elif args.cmd == "remove":
        remove_reminders(getattr(args, 'type', None))
    elif args.cmd == "自然语言":
        text = " ".join(args.text)
        setup_from_natural_language(text)
        remove_reminders(args.type)


if __name__ == "__main__":
    main()
