#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
考勤数据汇总脚本
读取最新的考勤数据并生成汇总报告
"""

import json
import os
import sys
import io

# 设置控制台编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from datetime import datetime

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'attendance')

def load_latest_data():
    """加载最新的考勤数据文件"""
    files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith('attendance_') and f.endswith('.json')])
    if not files:
        print("❌ 未找到考勤数据文件")
        return None
    
    latest_file = os.path.join(DATA_DIR, files[-1])
    print(f"📁 加载数据：{latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_report(data):
    """生成考勤汇总报告"""
    print("\n" + "="*60)
    print("📊 考勤汇总报告")
    print("="*60)
    
    work_date = data.get('workDate', 'N/A')
    summary = data.get('summary', {})
    
    print(f"\n📅 考勤日期：{work_date}")
    print(f"🕐 导出时间：{data.get('exportTime', 'N/A')}")
    
    print(f"\n📈 总体统计:")
    print(f"  部门数量：{summary.get('totalDepartments', 0)}")
    print(f"  员工总数：{summary.get('totalUsers', 0)}")
    print(f"  有考勤记录：{summary.get('usersWithAttendance', 0)}")
    print(f"  无考勤记录：{summary.get('totalUsers', 0) - summary.get('usersWithAttendance', 0)}")
    print(f"  考勤记录总数：{summary.get('totalRecords', 0)}")
    
    # 统计打卡情况
    reports = data.get('attendanceReports', [])
    
    normal_count = 0
    late_count = 0
    early_count = 0
    absent_count = 0
    leave_count = 0
    not_signed_count = 0
    
    for report in reports:
        attendance_list = report.get('attendanceList', [])
        approve_list = report.get('approveList', [])
        
        # 检查是否有请假
        if approve_list:
            leave_count += 1
            continue
        
        # 统计打卡情况
        has_on_duty = False
        has_off_duty = False
        is_late = False
        is_early = False
        is_not_signed = False
        
        for att in attendance_list:
            check_type = att.get('check_type')
            time_result = att.get('time_result')
            
            if check_type == 'OnDuty':
                has_on_duty = True
                if time_result == 'Late':
                    is_late = True
                elif time_result == 'NotSigned':
                    is_not_signed = True
            
            if check_type == 'OffDuty':
                has_off_duty = True
                if time_result == 'Early':
                    is_early = True
                elif time_result == 'NotSigned':
                    is_not_signed = True
        
        if is_not_signed:
            not_signed_count += 1
        elif is_late:
            late_count += 1
        elif is_early:
            early_count += 1
        elif has_on_duty and has_off_duty:
            normal_count += 1
        else:
            absent_count += 1
    
    print(f"\n✅ 打卡情况:")
    print(f"  正常打卡：{normal_count} 人")
    print(f"  迟到：{late_count} 人")
    print(f"  早退：{early_count} 人")
    print(f"  缺卡：{not_signed_count} 人")
    print(f"  请假：{leave_count} 人")
    print(f"  缺勤：{absent_count} 人")
    
    # 列出迟到人员
    late_users = []
    for report in reports:
        for att in report.get('attendanceList', []):
            if att.get('time_result') == 'Late':
                late_users.append({
                    'name': report.get('name'),
                    'check_type': att.get('check_type'),
                    'plan_time': att.get('plan_check_time'),
                    'actual_time': att.get('user_check_time')
                })
    
    if late_users:
        print(f"\n⚠️  迟到人员 ({len(late_users)} 人次):")
        for u in late_users:
            print(f"  - {u['name']}: {u['check_type']} 应打卡 {u['plan_time'][:16]}, 实际 {u['actual_time'][:16] if u['actual_time'] else 'N/A'}")
    
    # 列出请假人员
    leave_users = []
    for report in reports:
        if report.get('approveList'):
            for leave in report['approveList']:
                leave_users.append({
                    'name': report.get('name'),
                    'type': leave.get('sub_type'),
                    'duration': f"{leave.get('duration')} {leave.get('duration_unit')}",
                    'from': leave.get('begin_time', '')[:10],
                    'to': leave.get('end_time', '')[:10]
                })
    
    if leave_users:
        print(f"\n📝 请假人员 ({len(leave_users)} 人次):")
        for u in leave_users:
            print(f"  - {u['name']}: {u['type']} {u['duration']} ({u['from']} 至 {u['to']})")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    data = load_latest_data()
    if data:
        generate_report(data)
