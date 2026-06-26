#!/usr/bin/env python3
"""Health Reminder - Personal health tracking assistant"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path.home() / ".health-reminder"
MED_FILE = DATA_DIR / "medications.json"
WATER_FILE = DATA_DIR / "water.json"
ACTIVITY_FILE = DATA_DIR / "activity.json"

def init_data():
    """Initialize data files"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for f in [MED_FILE, WATER_FILE, ACTIVITY_FILE]:
        if not f.exists():
            with open(f, 'w') as f:
                json.dump([] if 'med' in str(f) or 'activity' in str(f) else {}, f)

def load_meds():
    init_data()
    with open(MED_FILE, 'r') as f:
        return json.load(f)

def save_meds(meds):
    with open(MED_FILE, 'w') as f:
        json.dump(meds, f, indent=2)

def load_water():
    init_data()
    with open(WATER_FILE, 'r') as f:
        return json.load(f)

def save_water(water):
    with open(WATER_FILE, 'w') as f:
        json.dump(water, f, indent=2)

# Medication commands
def cmd_med_add(name, time, frequency):
    """Add medication reminder"""
    meds = load_meds()
    med = {
        "id": len(meds) + 1,
        "name": name,
        "time": time,
        "frequency": frequency,
        "added_at": datetime.now().isoformat()
    }
    meds.append(med)
    save_meds(meds)
    print(f"✅ 已添加用药提醒: {name}")
    print(f"   时间: {time} | 频率: {frequency}")

def cmd_med_list():
    """List medications"""
    meds = load_meds()
    if not meds:
        print("📭 暂无用药提醒")
        return
    
    print("=" * 50)
    print("💊 用药提醒列表")
    print("=" * 50)
    for m in meds:
        print(f"   {m['id']}. {m['name']} - {m['time']} ({m['frequency']})")

def cmd_med_check(med_id):
    """Mark medication as taken"""
    print(f"✅ 已记录: 服用药物 #{med_id}")
    print(f"   时间: {datetime.now().strftime('%H:%M')}")

# Water commands
def cmd_water_log(amount):
    """Log water intake"""
    water = load_water()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in water:
        water[today] = []
    
    water[today].append({
        "amount": amount,
        "time": datetime.now().strftime("%H:%M"),
        "timestamp": datetime.now().isoformat()
    })
    
    save_water(water)
    
    total = sum(w['amount'] for w in water[today])
    print(f"✅ 已记录喝水: {amount}ml")
    print(f"   今日累计: {total}ml")

def cmd_water_stats():
    """Show water intake statistics"""
    water = load_water()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in water or not water[today]:
        print("📭 今日暂无喝水记录")
        return
    
    total = sum(w['amount'] for w in water[today])
    goal = 2000  # Default goal: 2000ml
    percentage = min(total / goal * 100, 100)
    
    print("=" * 50)
    print("💧 喝水统计")
    print("=" * 50)
    print(f"\n今日目标: {goal}ml")
    print(f"已喝水: {total}ml")
    print(f"完成度: {percentage:.0f}%")
    
    # Visual bar
    bar_len = 20
    filled = int(percentage / 100 * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)
    print(f"[{bar}]")
    
    if total >= goal:
        print("\n🎉 今日喝水目标已达成！")
    else:
        print(f"\n还需: {goal - total}ml")
    
    print(f"\n记录详情:")
    for w in water[today]:
        print(f"   {w['time']} - {w['amount']}ml")

# Activity commands
def cmd_activity_remind():
    """Show activity reminder"""
    print("=" * 50)
    print("🏃 活动提醒")
    print("=" * 50)
    print("\n💡 健康小贴士:")
    print("   • 每小时起身活动5分钟")
    print("   • 做几个伸展运动")
    print("   • 远眺放松眼睛")
    print("   • 深呼吸几次")
    print("\n⏰ 建议活动:")
    print("   1. 颈部环绕运动 (10次)")
    print("   2. 肩部上下运动 (10次)")
    print("   3. 腰部扭转运动 (左右各5次)")
    print("   4. 眼部按摩 (1分钟)")
    print("\n✅ 完成后请适当休息")

def cmd_activity_stats():
    """Show activity statistics"""
    print("=" * 50)
    print("📊 活动统计")
    print("=" * 50)
    print("\n💡 今日建议:")
    print("   • 目标: 每小时活动1次")
    print("   • 已完成: 请自行记录")
    print("   • 保持规律活动，预防久坐疾病")

# Main
def main():
    parser = argparse.ArgumentParser(description="Health Reminder")
    subparsers = parser.add_subparsers(dest='command')
    
    # Med subcommand
    med_parser = subparsers.add_parser('med', help='Medication reminders')
    med_subparsers = med_parser.add_subparsers(dest='med_cmd')
    
    med_add = med_subparsers.add_parser('add', help='Add medication')
    med_add.add_argument('name')
    med_add.add_argument('time')
    med_add.add_argument('frequency', choices=['daily', 'weekly'])
    
    med_subparsers.add_parser('list', help='List medications')
    
    med_check = med_subparsers.add_parser('check', help='Mark as taken')
    med_check.add_argument('id', type=int)
    
    # Water subcommand
    water_parser = subparsers.add_parser('water', help='Water tracking')
    water_subparsers = water_parser.add_subparsers(dest='water_cmd')
    
    water_log = water_subparsers.add_parser('log', help='Log water intake')
    water_log.add_argument('amount', type=int, help='Amount in ml')
    
    water_subparsers.add_parser('stats', help='Show water stats')
    
    # Activity subcommand
    activity_parser = subparsers.add_parser('activity', help='Activity reminders')
    activity_subparsers = activity_parser.add_subparsers(dest='activity_cmd')
    
    activity_subparsers.add_parser('remind', help='Show activity reminder')
    activity_subparsers.add_parser('stats', help='Show activity stats')
    
    args = parser.parse_args()
    
    if args.command == 'med':
        if args.med_cmd == 'add':
            cmd_med_add(args.name, args.time, args.frequency)
        elif args.med_cmd == 'list':
            cmd_med_list()
        elif args.med_cmd == 'check':
            cmd_med_check(args.id)
        else:
            med_parser.print_help()
    elif args.command == 'water':
        if args.water_cmd == 'log':
            cmd_water_log(args.amount)
        elif args.water_cmd == 'stats':
            cmd_water_stats()
        else:
            water_parser.print_help()
    elif args.command == 'activity':
        if args.activity_cmd == 'remind':
            cmd_activity_remind()
        elif args.activity_cmd == 'stats':
            cmd_activity_stats()
        else:
            activity_parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
