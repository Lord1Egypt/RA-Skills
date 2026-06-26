#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300投研系统 v2.0 - 定时任务执行脚本
每天早晨8:30自动运行，生成报告并发送到聊天
"""

import os
import sys
import subprocess
from datetime import datetime

# 系统路径
WORKSPACE = r"D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\hs300_research_system"
SCRIPT_PATH = os.path.join(WORKSPACE, "run_final_v2.py")
PYTHON_EXE = sys.executable


def run_research():
    """执行投研分析并返回报告内容"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行沪深300投研分析...")
    
    try:
        os.chdir(WORKSPACE)
        
        # 运行分析脚本
        result = subprocess.run(
            [PYTHON_EXE, SCRIPT_PATH],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 分析完成！")
            
            # 找到最新生成的报告文件
            output_dir = os.path.join(WORKSPACE, 'output')
            if os.path.exists(output_dir):
                reports = [f for f in os.listdir(output_dir) if f.startswith('沪深300投研日报_v2')]
                if reports:
                    latest_report = sorted(reports)[-1]
                    report_path = os.path.join(output_dir, latest_report)
                    
                    # 读取报告内容
                    with open(report_path, 'r', encoding='utf-8') as f:
                        report_content = f.read()
                    
                    return report_content
                else:
                    return "报告生成成功，但未找到输出文件。"
            else:
                return result.stdout
        else:
            print(f"执行失败，错误码: {result.returncode}")
            print(f"错误输出: {result.stderr}")
            return f"投研分析执行失败，请检查日志。错误: {result.stderr[:200]}"
            
    except Exception as e:
        print(f"执行异常: {e}")
        import traceback
        traceback.print_exc()
        return f"投研分析执行异常: {str(e)}"


def check_time():
    """检查是否为执行时间（早晨8:25-8:35之间）"""
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    
    # 8:25-8:35之间执行
    return current_hour == 8 and 25 <= current_minute <= 35


if __name__ == '__main__':
    # 方式1: 直接执行
    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        report = run_research()
        print("\n" + "="*70)
        print("投研日报")
        print("="*70)
        print(report)
        print("="*70)
    
    # 方式2: 检查时间后执行（由心跳每分钟调用）
    elif len(sys.argv) > 1 and sys.argv[1] == 'check':
        if check_time():
            print(run_research())
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 非执行时间，跳过。")
    
    # 默认显示帮助
    else:
        print("="*70)
        print("沪深300投研系统 v2.0 - 定时任务工具")
        print("="*70)
        print("")
        print("用法:")
        print("  python schedule_task_v2.py run      # 立即执行一次")
        print("  python schedule_task_v2.py check    # 检查时间并执行（用于心跳）")
        print("")
        print("设置: 每天早晨 8:30 自动运行")
        print("="*70)
