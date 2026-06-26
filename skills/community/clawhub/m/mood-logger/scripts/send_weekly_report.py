#!/usr/bin/env python3
"""
心情周报发送工具 - 生成并发送周报给用户

用法:
    python3 send_weekly_report.py

说明:
    生成上周的心情周报，并通过 OpenClaw 消息系统发送
"""

import subprocess
import sys
import os

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_SCRIPT = os.path.join(SCRIPT_DIR, "weekly_mood_report.py")

def main():
    # 生成周报
    result = subprocess.run(
        [sys.executable, REPORT_SCRIPT],
        capture_output=True,
        text=True,
        cwd=SCRIPT_DIR
    )
    
    if result.returncode != 0:
        print(f"生成报告失败: {result.stderr}")
        return
    
    # 提取报告内容（去掉第一行"正在生成周报..."）
    lines = result.stdout.strip().split('\n')
    # 找到第一个 # 开头的行（报告标题）
    report_start = 0
    for i, line in enumerate(lines):
        if line.startswith('# '):
            report_start = i
            break
    
    report = '\n'.join(lines[report_start:])
    print(report)

if __name__ == "__main__":
    main()
