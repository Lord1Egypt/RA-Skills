#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试调度器功能
"""

import time
from datetime import datetime, timedelta

print("=" * 60)
print("    测试纯Python调度器功能")
print("=" * 60)
print()

# 测试时间计算
print("1. 测试时间计算...")

test_cases = [
    ("08:00", "2026-04-23 07:30:00"),  # 还没到时间，今天执行
    ("08:00", "2026-04-23 09:30:00"),  # 已经过了，明天执行
    ("12:00", "2026-04-23 11:00:00"),
    ("12:00", "2026-04-23 13:00:00"),
]

for run_time, current_time_str in test_cases:
    now = datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S")
    target_time = datetime.strptime(run_time, "%H:%M").time()
    today_target = datetime.combine(now.date(), target_time)
    
    if now < today_target:
        next_run = today_target
    else:
        next_run = datetime.combine(now.date() + timedelta(days=1), target_time)
    
    print(f"   设置时间: {run_time}, 当前时间: {current_time_str}")
    print(f"   → 下次执行: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

# 测试运行分析脚本
print("2. 测试运行分析脚本...")
print()
print("   正在执行快速测试（模拟5秒后执行）...")
print()

# 倒计时演示
for i in range(5, 0, -1):
    print(f"   {i} 秒后执行...", end='\r')
    time.sleep(1)

print("   现在开始执行分析！")
print()

import subprocess
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_DIR)

result = subprocess.run(
    [sys.executable, 'run_analysis.py'],
    capture_output=False,
    text=True,
    encoding='utf-8',
    errors='ignore',
    timeout=120
)

print()
print("=" * 60)
if result.returncode == 0:
    print("✅ 调度器测试成功！")
else:
    print(f"❌ 测试失败，返回码: {result.returncode}")
print("=" * 60)
print()
print("提示:")
print("  - 正式使用请运行: 启动每日调度.bat")
print("  - 或后台运行: 后台启动调度器.vbs")
print()
