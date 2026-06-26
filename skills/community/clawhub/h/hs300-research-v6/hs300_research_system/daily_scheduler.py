#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300多因子投研系统 - 纯Python每日调度器
不依赖Windows任务计划，纯Python实现
每天早晨8点自动执行
"""

import os
import sys
import time
import subprocess
import threading
from datetime import datetime, timedelta

# 项目目录
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_DIR)

# 配置
RUN_TIME = "08:00"  # 每天执行时间
PYTHON_CMD = sys.executable
ANALYSIS_SCRIPT = "run_analysis.py"

# 运行状态
is_running = True
next_run_time = None


def run_analysis_task():
    """执行分析任务"""
    print(f"\n{'='*70}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行投研分析")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            [PYTHON_CMD, ANALYSIS_SCRIPT],
            capture_output=False,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 分析执行完成！")
        else:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 分析执行失败")
            
    except Exception as e:
        print(f"执行出错: {e}")
    
    # 计算下次执行时间
    calculate_next_run()
    print(f"\n下次执行时间: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")


def calculate_next_run():
    """计算下次执行时间"""
    global next_run_time
    
    now = datetime.now()
    target_time = datetime.strptime(RUN_TIME, "%H:%M").time()
    
    # 今天的目标时间
    today_target = datetime.combine(now.date(), target_time)
    
    if now < today_target:
        # 今天还没到时间，今天执行
        next_run_time = today_target
    else:
        # 今天已经过了，明天执行
        next_run_time = datetime.combine(now.date() + timedelta(days=1), target_time)
    
    return next_run_time


def format_time_remaining(seconds):
    """格式化剩余时间显示"""
    if seconds < 60:
        return f"{int(seconds)} 秒"
    elif seconds < 3600:
        return f"{int(seconds/60)} 分 {int(seconds%60)} 秒"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours} 时 {minutes} 分"


def main():
    """主调度函数"""
    global is_running, next_run_time
    
    print("\n" + "=" * 70)
    print("          沪深300多因子投研系统 - 每日自动调度器")
    print("=" * 70)
    print(f"\n启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"执行时间: 每天 {RUN_TIME}")
    print(f"项目目录: {PROJECT_DIR}")
    print(f"\n提示: 按 Ctrl+C 停止调度器")
    print("=" * 70 + "\n")
    
    # 计算下次执行时间
    calculate_next_run()
    print(f"⏰ 下次执行时间: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 询问是否立即执行一次
    try:
        choice = input("\n是否立即执行一次分析？(Y/N): ").strip().upper()
        if choice in ['Y', 'YES', '是']:
            run_analysis_task()
        else:
            time_remaining = (next_run_time - datetime.now()).total_seconds()
            print(f"\n等待下次执行，剩余时间: {format_time_remaining(time_remaining)}")
    except KeyboardInterrupt:
        print("\n\n用户中断，程序退出")
        return
    except:
        pass
    
    print("\n" + "-" * 70)
    print("调度器运行中... (按 Ctrl+C 停止)")
    print("-" * 70 + "\n")
    
    # 主循环
    try:
        while is_running:
            now = datetime.now()
            
            # 检查是否到执行时间（允许30秒误差）
            time_diff = abs((now - next_run_time).total_seconds())
            if time_diff < 30:
                run_analysis_task()
                # 执行完后等待1分钟，避免重复执行
                time.sleep(60)
                continue
            
            # 显示剩余时间（每小时显示一次）
            time_remaining = (next_run_time - now).total_seconds()
            if int(time_remaining) % 3600 == 0 and time_remaining > 0:
                print(f"[{now.strftime('%H:%M:%S')}] 距离下次执行: {format_time_remaining(time_remaining)}")
            
            # 每秒检查一次
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("调度器已停止")
        print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
