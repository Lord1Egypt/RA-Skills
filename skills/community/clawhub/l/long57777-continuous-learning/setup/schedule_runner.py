#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw定时任务调度器
替代不稳定的openclaw cron系统

版本：v2.0（通用版）
使用相对路径，适用于所有用户
"""

import schedule
import time
import subprocess
import os
import sys
from datetime import datetime
from pathlib import Path

# 获取工作区根目录（自动查找）
def find_workspace_root():
    """查找工作区根目录"""
    current = Path(os.getcwd())

    # 查找包含 .learnings 或 skills 目录的根目录
    for parent in [current] + list(current.parents):
        if (parent / ".learnings").exists() or (parent / "skills").exists():
            return parent

    # 如果找不到，使用当前目录
    return current

WORKSPACE = find_workspace_root()

# 脚本路径（相对路径）
SYNC_SCRIPT = WORKSPACE / "skills" / "continuous-learning" / "sync" / "sync_notification.py"
DREAM_SCRIPT = WORKSPACE / "skills" / "continuous-learning" / "dream" / "dream_cycle.py"
CONFIG_FILE = WORKSPACE / "skills" / "continuous-learning" / "config" / "dream_config.json"

def run_sync():
    """执行同步MemPalace任务"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行同步MemPalace任务")
    print(f"{'='*60}")
    try:
        subprocess.run(['python', str(SYNC_SCRIPT)], check=True, timeout=300,
                      cwd=str(WORKSPACE))
    except Exception as e:
        print(f"❌ 同步任务失败: {e}")

def run_dream():
    """执行做梦任务"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行做梦任务")
    print(f"{'='*60}")
    try:
        subprocess.run(['python', str(DREAM_SCRIPT)], check=True, timeout=600,
                      cwd=str(WORKSPACE))
    except Exception as e:
        print(f"❌ 做梦任务失败: {e}")

def load_notification_config():
    """加载通知配置"""
    try:
        if CONFIG_FILE.exists():
            import json
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('notification', {})
    except:
        pass
    return {}

def send_startup_notification():
    """发送启动通知（如果配置了）"""
    try:
        notification_config = load_notification_config()

        # 检查是否启用了通知
        if not notification_config.get('enabled', False):
            return

        # 获取配置的目标用户
        target_user = notification_config.get('to', '')
        account_id = notification_config.get('account_id', '')
        channel = notification_config.get('channel', 'openclaw-weixin')

        if not target_user:
            print("⚠️ 未配置通知目标用户，跳过启动通知")
            return

        # 构造消息
        message = (
            f'🚀 OpenClaw定时调度器已启动\n\n'
            f'⏰ 启动时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
            f'📋 下次任务:\n'
            f'- 同步MemPalace: 每天23:00\n'
            f'- 做梦任务: 每天02:00'
        )

        # 使用openclaw命令发送
        cmd = [
            'openclaw',
            'message', 'send',
            '--target', target_user,
            '--message', message,
            '--channel', channel
        ]

        if account_id:
            cmd.extend(['--account', account_id])

        result = subprocess.run(cmd, timeout=30, cwd=str(WORKSPACE),
                                capture_output=True, text=True,
                                encoding='utf-8', errors='replace')

        if result.returncode == 0:
            print("✅ 启动通知发送成功")
        else:
            print(f"⚠️ 启动通知失败: {result.stderr}")
    except Exception as e:
        print(f"⚠️ 启动通知发送失败: {e}")

def main():
    """主函数"""
    print("╔" + "═"*58 + "╗")
    print("║" + " "*15 + "OpenClaw定时任务调度器" + " "*18 + "║")
    print("╚" + "═"*58 + "╝")
    print(f"\n启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python路径: {sys.executable}")
    print(f"工作目录: {WORKSPACE}")
    print()

    # 检查脚本是否存在
    if not SYNC_SCRIPT.exists():
        print(f"❌ 脚本不存在: {SYNC_SCRIPT}")
        print(f"提示：确保已安装continuous-learning技能包")
        return

    if not DREAM_SCRIPT.exists():
        print(f"❌ 脚本不存在: {DREAM_SCRIPT}")
        print(f"提示：确保已安装continuous-learning技能包")
        return

    print("✅ 脚本检查通过")
    print(f"  - 同步脚本: {SYNC_SCRIPT.relative_to(WORKSPACE)}")
    print(f"  - 做梦脚本: {DREAM_SCRIPT.relative_to(WORKSPACE)}")
    print()

    # 设置定时任务
    schedule.every().day.at("23:00").do(run_sync)
    schedule.every().day.at("02:00").do(run_dream)

    print("📅 定时任务已设置:")
    print("  - 同步MemPalace: 每天 23:00")
    print("  - 做梦任务: 每天 02:00")
    print()

    # 发送启动通知（如果配置了）
    print("📤 尝试发送启动通知（如已配置）...")
    send_startup_notification()
    print()

    print("🔄 进入轮询模式（每分钟检查一次）...")
    print("按 Ctrl+C 停止")
    print()

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        print("\n\n🛑 用户停止调度器")
        print(f"停止时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()
