#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动绑定用户 ID 脚本 + 自动配置 cron
当用户发送"激活健康打卡"时，自动完成所有配置
"""

import os
import sys
import json
import subprocess
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_DIR = os.path.join(SKILL_DIR, "config")

def main():
    parser = argparse.ArgumentParser(description="自动绑定用户飞书ID并配置定时任务")
    parser.add_argument("--sender-id", required=True, help="发送者的飞书 ID (ou_xxx)")
    parser.add_argument("--setup-cron", action="store_true", help="同时配置 cron 定时任务")
    args = parser.parse_args()
    
    user_id = args.sender_id
    
    if not user_id.startswith("ou_"):
        print(f"❌ 无效的用户 ID: {user_id}")
        sys.exit(1)
    
    # 1. 保存用户 ID 到配置
    user_config_path = os.path.join(CONFIG_DIR, "user_config.json")
    with open(user_config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    old_id = config.get("feishu_user_id", "")
    config["feishu_user_id"] = user_id
    
    with open(user_config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    if old_id and old_id != user_id:
        print(f"✅ 用户 ID 已更新: {old_id} → {user_id}")
    elif old_id == user_id:
        print(f"✅ 用户 ID 已是最新: {user_id}")
    else:
        print(f"✅ 已绑定用户 ID: {user_id}")
    
    # 2. 自动配置 cron（如果需要）
    setup_cron = args.setup_cron
    if not setup_cron:
        # 检查 cron 是否已存在
        try:
            cron_list = os.popen("crontab -l 2>/dev/null").read()
        except:
            cron_list = ""
        
        if "daily_health_reminder" not in cron_list:
            setup_cron = True  # 没有cron，自动配置
    
    if setup_cron:
        # 查找提醒脚本路径
        script_path = os.path.join(SCRIPT_DIR, "daily_health_reminder.py")
        if not os.path.exists(script_path):
            script_path = os.path.join(SCRIPT_DIR, "daily_health_reminder.sh")
        
        if os.path.exists(script_path):
            log_dir = os.path.join(SKILL_DIR, "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "health_reminder.log")
            
            cron_line = f"0 9 * * * {script_path} >> {log_file} 2>&1"
            
            # 添加 cron
            try:
                current_cron = subprocess.check_output("crontab -l 2>/dev/null", shell=True).decode("utf-8")
            except:
                current_cron = ""
            
            if "daily_health_reminder" not in current_cron:
                new_cron = current_cron.strip() + "\n" + cron_line
                subprocess.run(f"echo '{new_cron}' | crontab -", shell=True)
                print("✅ 定时任务已配置：每天 9:00 自动推送")
            else:
                print("✅ 定时任务已存在")
        else:
            print("⚠️ 提醒脚本未找到")
    else:
        # 检查 cron
        try:
            cron_list = os.popen("crontab -l 2>/dev/null").read()
        except:
            cron_list = ""
        
        if "daily_health_reminder" not in cron_list:
            print()
            print("💡 定时任务尚未配置")
            print("   运行以下命令启用每日提醒：")
            print(f"   python3 {SCRIPT_DIR}/activate_health_skill.py")
        else:
            print("✅ 定时任务已配置，每天 9:00 会自动推送")

if __name__ == "__main__":
    main()
