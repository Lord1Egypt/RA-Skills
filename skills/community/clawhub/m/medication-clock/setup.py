#!/usr/bin/env python3
"""
优甲乐服药提醒系统 - 安装和配置脚本
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_openclaw_installed():
    """检查 OpenClaw 是否已安装"""
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ OpenClaw 已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ OpenClaw 未正确安装")
            return False
    except FileNotFoundError:
        print("❌ OpenClaw 未安装或不在 PATH 中")
        return False
    except Exception as e:
        print(f"❌ 检查 OpenClaw 时出错: {e}")
        return False

def setup_data_directory():
    """设置数据目录"""
    data_dir = Path.home() / ".openclaw" / "medication_data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建默认配置文件
    default_settings = {
        "reminder_enabled": True,
        "first_reminder_time": "06:30",
        "reminder_interval": 15,
        "on_time_window": 30,
        "notification_channel": "current"
    }
    
    settings_file = data_dir / "settings.json"
    if not settings_file.exists():
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=2)
        print(f"✅ 已创建默认配置文件: {settings_file}")
    
    # 创建空记录文件
    records_file = data_dir / "medication-records.json"
    if not records_file.exists():
        with open(records_file, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        print(f"✅ 已创建记录文件: {records_file}")
    
    # 创建统计文件
    stats_file = data_dir / "stats.json"
    if not stats_file.exists():
        default_stats = {
            "total_days": 0,
            "on_time_days": 0,
            "missed_days": 0,
            "current_streak": 0,
            "best_streak": 0,
            "last_taken": None
        }
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(default_stats, f, ensure_ascii=False, indent=2)
        print(f"✅ 已创建统计文件: {stats_file}")
    
    return data_dir

def create_openclaw_cron_jobs():
    """创建 OpenClaw cron 任务"""
    print("\n📅 设置每日提醒任务...")
    
    # 这里应该调用 OpenClaw 的 cron API
    # 由于我们无法直接访问 OpenClaw 的 cron API，这里提供配置说明
    
    cron_config = {
        "name": "medication-reminder-first",
        "description": "优甲乐首次提醒 (6:30)",
        "schedule": {
            "kind": "cron",
            "expr": "30 6 * * *",
            "tz": "Asia/Shanghai"
        },
        "payload": {
            "kind": "agentTurn",
            "message": "⏰ 服药提醒：请服用优甲乐。回复 /medication taken 确认服药。"
        },
        "delivery": {
            "mode": "announce",
            "channel": "current"
        }
    }
    
    print("📋 **需要手动创建的 cron 任务配置：**")
    print(json.dumps(cron_config, ensure_ascii=False, indent=2))
    
    print("\n🔧 **安装步骤：**")
    print("1. 在 OpenClaw 控制台中，使用以下命令创建首次提醒：")
    print(f"   openclaw cron add --json '{json.dumps(cron_config)}'")
    print("\n2. 需要创建重复提醒任务（每15分钟）：")
    print("   这需要更复杂的 cron 表达式或使用 OpenClaw 的重复任务功能")
    
    return False  # 返回 False 表示需要手动配置

def create_command_alias():
    """创建命令别名"""
    print("\n🔗 设置命令别名...")
    
    # 获取脚本路径
    script_dir = Path(__file__).parent
    integration_script = script_dir / "openclaw_integration.py"
    
    if not integration_script.exists():
        print(f"❌ 找不到集成脚本: {integration_script}")
        return False
    
    # 使脚本可执行
    integration_script.chmod(0o755)
    
    # 创建简单的包装脚本
    wrapper_content = f'''#!/bin/bash
# 优甲乐服药提醒命令包装
cd "{script_dir}"
python3 openclaw_integration.py "$@"
'''
    
    wrapper_path = script_dir / "medication_wrapper.sh"
    with open(wrapper_path, 'w', encoding='utf-8') as f:
        f.write(wrapper_content)
    wrapper_path.chmod(0o755)
    
    print(f"✅ 已创建命令包装脚本: {wrapper_path}")
    print(f"\n📝 **使用方法：**")
    print(f"   可以直接运行: python3 {integration_script} <command>")
    print(f"   或使用包装: {wrapper_path} <command>")
    
    return True

def create_openclaw_skill_config():
    """创建 OpenClaw Skill 配置文件"""
    print("\n🎭 创建 OpenClaw Skill 配置...")
    
    skill_config = {
        "name": "medication-reminder",
        "description": "优甲乐服药提醒与记录系统",
        "commands": {
            "medication": {
                "description": "管理优甲乐服药提醒和记录",
                "handler": "openclaw_integration.handle_medication_command",
                "examples": [
                    "/medication start - 启动每日提醒",
                    "/medication taken - 记录服药",
                    "/medication status - 查看状态",
                    "/medication report - 生成报告"
                ]
            }
        },
        "cronJobs": [
            {
                "name": "medication-first-reminder",
                "schedule": "30 6 * * *",
                "message": "⏰ 服药提醒：请服用优甲乐。回复 /medication taken 确认服药。"
            }
        ],
        "dataFiles": [
            "medication-records.json",
            "stats.json",
            "settings.json"
        ]
    }
    
    config_file = Path(__file__).parent / "openclaw-skill-config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(skill_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已创建 Skill 配置文件: {config_file}")
    return True

def print_usage_instructions():
    """打印使用说明"""
    print("\n" + "="*60)
    print("🎉 优甲乐服药提醒系统安装完成！")
    print("="*60)

    print("\n📋 **系统功能：**")
    print("✅ 每日6:30首次服药提醒")
    print("✅ 每15分钟重复提醒，直到确认")
    print("✅ 自动记录服药时间和状态")
    print("✅ 服药依从性统计和报表")
    print("✅ 数据导出功能（CSV格式）")

    print("\n🔧 **后续配置步骤：**")
    print("1. **设置 OpenClaw cron 任务**：")
    print("   需要在 OpenClaw 中手动创建每日提醒任务")

    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    print(f"\n2. **测试系统功能**：")
    print(f"   cd {script_dir}")
    print(f"   python3 openclaw_integration.py status")
    print(f"   python3 openclaw_integration.py taken")

    print("\n3. **集成到 OpenClaw 命令系统**：")
    print("   需要将本 Skill 注册到 OpenClaw 的 skill-creator")

    print("\n📁 **数据存储位置：**")
    print(f"   记录文件：{Path.home()}/.openclaw/medication_data/")

    print("\n💡 **快速开始：**")
    print("   1. 启动提醒：/medication start")
    print("   2. 记录服药：/medication taken")
    print("   3. 查看状态：/medication status")
    print("   4. 生成报告：/medication report 30")

    print("\n❓ **获取帮助：**")
    print("   /medication help")

def main():
    """主安装函数"""
    print("🔄 开始安装优甲乐服药提醒系统...")
    
    # 检查 OpenClaw
    if not check_openclaw_installed():
        print("\n⚠️  请先安装 OpenClaw：")
        print("   npm install -g openclaw")
        print("   或参考：https://docs.openclaw.ai/installation")
        sys.exit(1)
    
    # 设置数据目录
    data_dir = setup_data_directory()
    
    # 创建命令别名
    create_command_alias()
    
    # 创建 Skill 配置
    create_openclaw_skill_config()
    
    # 创建 cron 任务（需要手动配置）
    create_openclaw_cron_jobs()
    
    # 打印使用说明
    print_usage_instructions()
    
    print("\n✅ 安装完成！请按照上述说明完成后续配置。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 安装被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 安装过程中出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)