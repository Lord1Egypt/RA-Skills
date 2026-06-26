#!/usr/bin/env python3
"""
持续学习套件 - 定时任务安装脚本（跨平台）

v2.0 - 使用Python调度器替代Windows任务计划程序
优势：纯Python实现、开机自启动、微信通知、跨平台一致
"""
import subprocess
import sys
import platform
from pathlib import Path

WORKSPACE = Path.cwd()
SCHEDULER_SCRIPT = WORKSPACE / "skills/continuous-learning/setup/schedule_runner.py"
START_SCRIPT = WORKSPACE / "skills/continuous-learning/setup/schedule_start.bat"
AUTOSTART_SCRIPT = WORKSPACE / "skills/continuous-learning/setup/install_autostart_en.bat"


def is_windows():
    """检测是否为Windows"""
    return platform.system() == 'Windows'


def main():
    print("=" * 60)
    print("OpenClaw持续学习套件 - 定时任务安装")
    print("=" * 60)

    # 验证文件存在
    if not SCHEDULER_SCRIPT.exists():
        print(f"❌ 找不到调度器脚本: {SCHEDULER_SCRIPT}")
        print("请确保已正确安装continuous-learning技能包")
        sys.exit(1)

    if not START_SCRIPT.exists():
        print(f"❌ 找不到启动脚本: {START_SCRIPT}")
        sys.exit(1)

    if not AUTOSTART_SCRIPT.exists():
        print(f"❌ 找不到自动启动脚本: {AUTOSTART_SCRIPT}")
        sys.exit(1)

    print("\n✅ 找到所需脚本文件")
    print(f"  - 调度器: {SCHEDULER_SCRIPT}")
    print(f"  - 启动脚本: {START_SCRIPT}")
    print(f"  - 自动启动: {AUTOSTART_SCRIPT}")

    # 安装Python调度器
    print("\n" + "=" * 60)
    print("Python调度器（v2.0 - 新方案）")
    print("=" * 60)
    print("\n✅ Python调度器已包含在技能包")
    print("\n使用方法：")
    print("  1. 手动启动：双击 schedule_start.bat")
    print("  2. 开机自动启动：双击 install_autostart_en.bat")
    print("\n定时任务：")
    print("  - 同步MemPalace: 每天 23:00")
    print("  - 做梦分析: 每天 02:00")
    print("\n✨ v2.0优势：")
    print("  - ✅ 纯Python实现，无需系统权限")
    print("  - ✅ 支持开机自动启动")
    print("  - ✅ 支持微信任务通知")
    print("  - ✅ 精确时间匹配（每小时轮询）")
    print("  - ✅ 跨平台一致体验")
    print("\n与v1.0对比：")
    print("  v1.0: Windows任务计划程序（schtasks）")
    print("  v2.0: Python schedule库 + PowerShell命令")
    print("\n现在可以：")
    print("  1. 立即启动：双击 schedule_start.bat")
    print("  2. 设置开机自启：双击 install_autostart_en.bat")

if __name__ == "__main__":
    main()
