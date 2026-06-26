#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HealthSkill 1.0 一键激活脚本（Python 版）
用户运行此脚本即可完成全部配置
"""

import os
import json
import subprocess
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_DIR = os.path.join(SKILL_DIR, "config")

print("🏥 HealthSkill 1.0 激活向导")
print("=" * 40)
print()

# -------------------------
# Step 1: 获取用户飞书 ID
# -------------------------
print("📱 Step 1: 获取飞书用户 ID")
print("-" * 40)

user_config_path = os.path.join(CONFIG_DIR, "user_config.json")
with open(user_config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

saved_id = config.get("feishu_user_id", "")

if saved_id and saved_id != "ou_your_user_id_here":
    print(f"✅ 已配置用户 ID: {saved_id}")
    feishu_user_id = saved_id
else:
    print("❌ 未配置用户 ID")
    print()
    print("请在飞书对话框中发送：'激活健康打卡'")
    print("我会自动获取你的 ID 并保存。")
    print()
    
    user_input = input("或直接输入你的飞书 ID (以 ou_ 开头，直接回车跳过): ").strip()
    
    if user_input and user_input.startswith("ou_"):
        config["feishu_user_id"] = user_input
        with open(user_config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 已保存用户 ID: {user_input}")
        feishu_user_id = user_input
    else:
        print("⚠️ 跳过此步骤，请稍后手动配置")
        feishu_user_id = None

print()

# -------------------------
# Step 2: 配置 cron 任务
# -------------------------
print("⏰ Step 2: 配置每日自动提醒")
print("-" * 40)

script_path = os.path.join(SCRIPT_DIR, "daily_health_reminder.sh")
log_dir = os.path.join(SKILL_DIR, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "health_reminder.log")

cron_line = f"0 9 * * * {script_path} >> {log_file} 2>&1"

# 检查当前 cron
try:
    current_cron = subprocess.check_output("crontab -l 2>/dev/null", shell=True).decode("utf-8")
except:
    current_cron = ""

if "daily_health_reminder" in current_cron:
    print("⚠️ 定时任务已存在，跳过添加")
else:
    # 添加 cron
    new_cron = current_cron.strip() + "\n" + cron_line
    subprocess.run(f"echo '{new_cron}' | crontab -", shell=True)
    print("✅ 已添加定时任务：每天 9:00 自动推送")

print()

# -------------------------
# Step 3: 测试发送
# -------------------------
print("🧪 Step 3: 测试发送")
print("-" * 40)

test_choice = input("是否发送测试消息？(y/n): ").strip().lower()

if test_choice == "y":
    if feishu_user_id:
        print("发送测试消息...")
        os.system(f'"{script_path}"')
    else:
        print("⚠️ 未配置用户 ID，无法发送测试消息")
else:
    print("跳过测试")

print()

# -------------------------
# 完成
# -------------------------
print("🎉 激活完成！")
print()
print("配置信息：")
print(f"  - 用户 ID: {feishu_user_id or '未配置'}")
print(f"  - 定时任务: 每天 9:00")
print(f"  - 脚本路径: {script_path}")
print()
print("如需取消每日提醒，请运行：")
print("  crontab -e")
print("  删除包含 daily_health_reminder 的行")
