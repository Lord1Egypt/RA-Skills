#!/usr/bin/env python3
"""
Model Usage Monitor Skill - Setup Script
自动安装和配置模型使用监控
"""

import json
import os
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
LIB_DIR = os.path.join(WORKSPACE_DIR, ".lib")

def load_config():
    """加载技能配置"""
    config_path = os.path.join(SKILL_DIR, "config.json")
    with open(config_path, 'r') as f:
        return json.load(f)

def install_monitor_script():
    """安装监控脚本到 .lib 目录"""
    src = os.path.join(SKILL_DIR, "monitor.py")
    dst = os.path.join(LIB_DIR, "model_usage_monitor_v2.py")
    
    with open(src, 'r') as f:
        content = f.read()
    
    with open(dst, 'w') as f:
        f.write(content)
    
    print(f"✅ 监控脚本已安装: {dst}")
    return dst

def setup_cron_job(config):
    """设置自动监控 Cron Job"""
    # 检查是否已存在
    result = subprocess.run(
        ["openclaw", "cron", "list"],
        capture_output=True,
        text=True
    )
    
    if "model-usage-monitor" in result.stdout:
        print("ℹ️  Cron Job 已存在，跳过创建")
        return
    
    # 创建 Cron Job
    cmd = [
        "openclaw", "cron", "create",
        "--name", "model-usage-monitor",
        "--cron", config["check_interval"],
        "--message", "执行模型使用监控检查: python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py --alert-check",
        "--agent", "main",
        "--model", config["model"],
        "--session", config["session_target"],
        "--no-deliver",
        "--description", "每小时检查模型使用告警"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Cron Job 已创建: 每小时自动检查")
    else:
        print(f"⚠️  Cron Job 创建失败: {result.stderr}")

def test_monitor():
    """测试监控脚本"""
    script = os.path.join(LIB_DIR, "model_usage_monitor_v2.py")
    result = subprocess.run(
        ["python3", script, "--alert-check"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ 监控脚本测试通过")
        print(f"   输出: {result.stdout.strip()}")
    else:
        print(f"⚠️  监控脚本测试失败: {result.stderr}")

def main():
    print("🚀 安装 Model Usage Monitor Skill...")
    print("-" * 50)
    
    # 加载配置
    config = load_config()
    print(f"📋 配置加载完成")
    
    # 确保 .lib 目录存在
    os.makedirs(LIB_DIR, exist_ok=True)
    
    # 安装脚本
    install_monitor_script()
    
    # 设置 Cron Job
    setup_cron_job(config)
    
    # 测试
    print("-" * 50)
    test_monitor()
    
    print("-" * 50)
    print("✅ 安装完成!")
    print("\n使用方式:")
    print("  python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py")
    print("  python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py --live")

if __name__ == "__main__":
    main()
