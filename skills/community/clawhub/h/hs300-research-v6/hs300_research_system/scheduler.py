#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300多因子投研系统 - 定时任务调度器
每天早晨8点自动执行分析
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# 项目目录
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_CMD = sys.executable


def run_analysis():
    """执行分析任务"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行投研分析...")
    print(f"{'='*60}\n")
    
    try:
        # 切换到项目目录并运行分析脚本
        os.chdir(PROJECT_DIR)
        result = subprocess.run(
            [PYTHON_CMD, 'run_analysis.py'],
            capture_output=False,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 分析执行成功！")
        else:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 分析执行失败，返回码: {result.returncode}")
            
    except Exception as e:
        print(f"执行出错: {e}")
    
    print(f"\n{'='*60}")
    print(f"下一次执行时间：明天 08:00")
    print(f"{'='*60}\n")


def main():
    """主函数 - 使用schedule库进行定时调度"""
    
    print("=" * 60)
    print("    沪深300多因子投研系统 - 定时任务调度器")
    print("=" * 60)
    print(f"\n启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"执行时间: 每天 08:00")
    print(f"项目目录: {PROJECT_DIR}")
    print(f"Python路径: {PYTHON_CMD}")
    print()
    print("提示: 按 Ctrl+C 停止调度器")
    print("=" * 60)
    print()
    
    # 检查是否安装了schedule库
    try:
        import schedule
    except ImportError:
        print("正在安装 schedule 库...")
        subprocess.run([PYTHON_CMD, '-m', 'pip', 'install', 'schedule'], capture_output=True)
        import schedule
    
    # 设置定时任务 - 每天8点执行
    schedule.every().day.at("08:00").do(run_analysis)
    
    print(f"定时任务已设置: 每天 08:00 执行分析")
    print()
    
    # 显示下次执行时间
    next_run = schedule.next_run()
    if next_run:
        print(f"下次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 测试运行一次（可选）
    print("是否立即执行一次测试？(y/n): ", end='')
    try:
        choice = input().strip().lower()
        if choice == 'y' or choice == 'yes':
            run_analysis()
    except:
        print("\n跳过测试运行")
    
    print("\n调度器运行中... (按 Ctrl+C 停止)")
    print("-" * 60)
    
    # 主循环
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        print("\n\n调度器已停止")
        sys.exit(0)


if __name__ == '__main__':
    main()
