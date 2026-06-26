#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300多因子投研系统 - OpenClaw定时任务入口脚本

使用方法:
1. 在OpenClaw心跳配置中设置定时任务
2. 每天早晨8点自动调用此脚本执行分析
"""

import os
import sys
import subprocess
from datetime import datetime

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def main():
    """OpenClaw定时任务入口"""
    
    print("=" * 70)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 沪深300多因子投研系统 - OpenClaw定时任务")
    print("=" * 70)
    print()
    
    # 执行分析脚本
    try:
        result = subprocess.run(
            [sys.executable, 'run_analysis.py'],
            capture_output=False,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            print()
            print("=" * 70)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ OpenClaw定时任务执行成功！")
            print("=" * 70)
            return 0
        else:
            print()
            print("=" * 70)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ OpenClaw定时任务执行失败")
            print("=" * 70)
            return 1
            
    except Exception as e:
        print(f"执行出错: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
