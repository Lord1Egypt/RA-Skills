#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康报告系统 - 一键初始化配置脚本
小白专用！交互式问答，5 分钟完成配置
"""

import json
import os
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_ROOT / 'config'

# 确保配置目录存在
CONFIG_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("👋 欢迎使用健康报告系统！")
print("=" * 60)
print()
print("这是一个交互式配置向导，只需回答几个问题，")
print("即可生成您的专属健康档案！")
print()
print("按 Enter 键开始...")
input()

# 收集用户信息
config = {
    "user_profile": {},
    "condition_standards": {
        "胆结石": {
            "fat_min_g": 40,
            "fat_max_g": 50,
            "fiber_min_g": 25,
            "water_min_ml": 2000
        },
        "糖尿病": {
            "fat_min_g": 40,
            "fat_max_g": 55,
            "fiber_min_g": 30,
            "water_min_ml": 2000
        },
        "高血压": {
            "fat_min_g": 40,
            "fat_max_g": 55,
            "fiber_min_g": 25,
            "water_min_ml": 2000,
            "sodium_max_mg": 2000
        },
        "健身减脂": {
            "fat_min_g": 40,
            "fat_max_g": 60,
            "fiber_min_g": 25,
            "water_min_ml": 2500
        }
    },
    "scoring_weights": {
        "diet": 0.45,
        "water": 0.35,
        "weight": 0.20,
        "exercise_bonus": 0.10
    },
    "exercise_standards": {
        "weekly_target_minutes": 150
    }
}

print("-" * 60)
print("1️⃣  您的姓名或昵称？")
print("-" * 60)
name = input("   > ").strip()
while not name:
    print("   请告诉我您的名字~")
    name = input("   > ").strip()
config["user_profile"]["name"] = name
print()

print("-" * 60)
print("2️⃣  性别和年龄？")
print("-" * 60)
gender = input("   性别（男/女）> ").strip()
while gender not in ["男", "女"]:
    print("   请输入'男'或'女'")
    gender = input("   性别 > ").strip()

age = input("   年龄 > ").strip()
while not age.isdigit():
    print("   请输入数字年龄")
    age = input("   年龄 > ").strip()

config["user_profile"]["gender"] = gender
config["user_profile"]["age"] = int(age)
print()

print("-" * 60)
print("3️⃣  身高和当前体重？")
print("-" * 60)
height = input("   身高（厘米，如 172）> ").strip()
while not height.isdigit():
    print("   请输入数字")
    height = input("   身高（厘米）> ").strip()

weight = input("   当前体重（公斤，如 65）> ").strip()
while True:
    try:
        config["user_profile"]["current_weight_kg"] = float(weight)
        break
    except ValueError:
        print("   请输入数字（可以是小数）")
        weight = input("   当前体重（公斤）> ").strip()

config["user_profile"]["height_cm"] = int(height)
print()

print("-" * 60)
print("4️⃣  目标体重？")
print("-" * 60)
target = input("   目标体重（公斤）> ").strip()
while True:
    try:
        config["user_profile"]["target_weight_kg"] = float(target)
        break
    except ValueError:
        print("   请输入数字（可以是小数）")
        target = input("   目标体重（公斤）> ").strip()
print()

print("-" * 60)
print("5️⃣  健康状况？")
print("-" * 60)
print("   请选择（输入数字）：")
print("   1. 胆结石（低脂高纤饮食）")
print("   2. 糖尿病（控制碳水）")
print("   3. 高血压（低盐饮食）")
print("   4. 健身减脂（高蛋白，运动导向）")
print("   5. 无特殊状况（均衡健康）")

condition_map = {
    "1": "胆结石",
    "2": "糖尿病",
    "3": "高血压",
    "4": "健身减脂",
    "5": "均衡健康"
}

condition = input("   选择 > ").strip()
while condition not in condition_map:
    print("   请输入 1-5 的数字")
    condition = input("   选择 > ").strip()

config["user_profile"]["condition"] = condition_map[condition]
print()

print("-" * 60)
print("6️⃣  有没有不吃/过敏的食物？")
print("-" * 60)
print("   （多个食物用逗号分隔，如：海鲜，鱼，蛙）")
print("   （没有请直接按 Enter）")

dislike = input("   不吃的食物 > ").strip()
if dislike:
    config["user_profile"]["dietary_preferences"] = {
        "dislike": [f.strip() for f in dislike.split(",") if f.strip()]
    }
else:
    config["user_profile"]["dietary_preferences"] = {
        "dislike": []
    }

allergies = input("   过敏食物 > ").strip()
if allergies:
    config["user_profile"]["dietary_preferences"]["allergies"] = [
        f.strip() for f in allergies.split(",") if f.strip()
    ]
else:
    config["user_profile"]["dietary_preferences"]["allergies"] = []

print()

print("-" * 60)
print("7️⃣  活动量评估？")
print("-" * 60)
print("   请选择（输入数字）：")
print("   1. 久坐不动（办公室工作，几乎不运动）")
print("   2. 轻度活动（每周 1-3 次轻度运动）")
print("   3. 中度活动（每周 3-5 次中等运动）")
print("   4. 重度活动（每周 6-7 次高强度运动）")
print("   5. 专业运动员（每天训练）")

activity_map = {
    "1": 1.2,
    "2": 1.375,
    "3": 1.55,
    "4": 1.725,
    "5": 1.9
}

activity = input("   选择 > ").strip()
while activity not in activity_map:
    print("   请输入 1-5 的数字")
    activity = input("   选择 > ").strip()

config["user_profile"]["activity_level"] = activity_map[activity]
print()

# 保存配置文件
config_file = CONFIG_DIR / 'user_config.json'
with open(config_file, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)

print("=" * 60)
print("✅ 配置完成！")
print("=" * 60)
print()
print("已为您创建健康档案：")
print(f"  - 姓名：{config['user_profile']['name']}")
print(f"  - 性别：{config['user_profile']['gender']}")
print(f"  - 年龄：{config['user_profile']['age']}岁")
print(f"  - 身高：{config['user_profile']['height_cm']}cm")
print(f"  - 当前体重：{config['user_profile']['current_weight_kg']}kg")
print(f"  - 目标体重：{config['user_profile']['target_weight_kg']}kg")
print(f"  - 健康状况：{config['user_profile']['condition']}")
print(f"  - 活动系数：{config['user_profile']['activity_level']}")
print()
print(f"配置文件已保存到：{config_file}")
print()
print("-" * 60)
print("下一步：配置消息推送（可选）")
print("-" * 60)
print()
print("如果您希望通过钉钉/飞书/Telegram 接收健康报告，")
print("请编辑 config/.env 文件填写 Webhook 地址。")
print()
print("如果不需要推送，可以跳过此步骤。")
print()
print("编辑 .env 文件：")
print(f"  nano {CONFIG_DIR / '.env'}")
print()
print("=" * 60)
print("🎉 恭喜！配置全部完成！")
print("=" * 60)
print()
print("使用指南：")
print("  1. 在 memory/目录下创建今日记录文件")
print("     例如：memory/2026-03-14.md")
print()
print("  2. 记录您的健康数据（体重/饮食/饮水/运动）")
print()
print("  3. 运行报告生成命令：")
print(f"     python3 {SCRIPT_DIR / 'health_report_pro.py'} \\")
print("       /root/.openclaw/workspace/memory/2026-03-14.md \\")
print("       2026-03-14")
print()
print("  4. 设置定时任务（每天 22:00 自动推送）：")
print("     crontab -e")
print("     0 22 * * * bash {SCRIPT_DIR / 'daily_health_report_pro.sh'}")
print()
print("祝您健康快乐！💪")
print()
