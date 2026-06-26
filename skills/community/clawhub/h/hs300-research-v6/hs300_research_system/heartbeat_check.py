#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300多因子投研系统 v3.0 - OpenClaw心跳检查脚本

每天早晨 08:30 自动执行分析，生成报告并发送到聊天

v3.0 升级:
- 8大类因子体系（估值/质量/成长/动量/趋势/波动率/技术/量能）
- 财务数据获取（PE/PB/ROE/毛利率/营收增长/利润增长）
"""

import os
import sys
import glob
import subprocess
from datetime import datetime

# 配置
EXECUTE_HOUR = 8      # 执行小时
EXECUTE_MINUTE = 30   # 执行分钟
VERSION = "v3.0"

# 标记文件
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MARKER_FILE = os.path.join(SCRIPT_DIR, '.last_exec_date_v3')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')

os.chdir(SCRIPT_DIR)


def check_time():
    """检查是否到执行时间"""
    now = datetime.now()
    if now.hour == EXECUTE_HOUR and abs(now.minute - EXECUTE_MINUTE) <= 5:
        return True
    return False


def already_executed_today():
    """检查今天是否已经执行过"""
    if not os.path.exists(MARKER_FILE):
        return False
    try:
        with open(MARKER_FILE, 'r', encoding='utf-8') as f:
            last_date = f.read().strip()
            return last_date == datetime.now().strftime('%Y-%m-%d')
    except:
        return False


def mark_executed():
    """标记今天已执行"""
    try:
        with open(MARKER_FILE, 'w', encoding='utf-8') as f:
            f.write(datetime.now().strftime('%Y-%m-%d'))
    except:
        pass


def get_latest_report():
    """获取最新报告"""
    try:
        report_files = glob.glob(os.path.join(OUTPUT_DIR, '沪深300投研日报_v3_*.md'))
        if not report_files:
            report_files = glob.glob(os.path.join(OUTPUT_DIR, '沪深300投研日报_v2_*.md'))
        if not report_files:
            return None
        report_files.sort(key=os.path.getmtime, reverse=True)
        return report_files[0]
    except:
        return None


def run_analysis():
    """执行分析"""
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n{'='*60}")
    print(f"[{time_str}]  沪深300投研系统 {VERSION} - 定时任务开始")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, 'run_analysis_v3.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=600  # 10分钟超时（因为有网络请求）
        )
        
        if result.returncode == 0:
            mark_executed()
            print(f"[{time_str}]  [OK] 分析执行完成\n")
            
            report_file = get_latest_report()
            if report_file:
                print(f"[{time_str}]  📊 投研日报：\n")
                with open(report_file, 'r', encoding='utf-8') as f:
                    print(f.read())
                print(f"\n{'='*70}")
                print(f"[{time_str}]  [DONE] 报告完成！")
            return True
        else:
            print(f"[{time_str}]  [ERROR] 分析执行失败")
            print(f"stderr: {result.stderr[:1000] if result.stderr else '无'}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[{time_str}]  [TIMEOUT] 分析超时")
        return False
    except Exception as e:
        print(f"[{time_str}]  [EXCEPTION] 执行出错: {e}")
        return False


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['run', 'force', '--run', '-f']:
        run_analysis()
        return 0
    
    if len(sys.argv) > 1 and sys.argv[1] in ['check', '--check', '-c']:
        now = datetime.now()
        s1 = "[OK] 到执行时间" if check_time() else "[--] 未到执行时间"
        s2 = "[OK] 今日已执行" if already_executed_today() else "[--] 今日未执行"
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {s1}, {s2}")
        return 0
    
    if check_time() and not already_executed_today():
        run_analysis()
        return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
