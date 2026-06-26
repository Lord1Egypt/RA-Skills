#!/usr/bin/env python3
"""
InStreet 自动回复分析报告
分析回复成功率、时段分布、响应效率
"""

import json
import re
from datetime import datetime, timedelta
from collections import defaultdict

def parse_instreet_log():
    """解析InStreet回复日志"""
    log_file = "/tmp/instreet_reply.log"
    
    # 如果日志不存在，返回模拟数据用于演示
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"⚠️  日志文件不存在: {log_file}")
        print("   使用模拟数据演示...\n")
        return generate_mock_data()
    
    stats = {
        "total_runs": 0,
        "total_replies": 0,
        "successful_replies": 0,
        "failed_replies": 0,
        "hourly_distribution": defaultdict(int),
        "mode_distribution": {"morning_rush": 0, "normal": 0},
        "avg_processing_time": 0,
        "backlog_trend": []
    }
    
    current_run = None
    
    for line in lines:
        # 解析运行开始
        if "MoltbookAgent Auto-Reply 启动" in line:
            stats["total_runs"] += 1
            time_match = re.search(r'\[(.*?)\]', line)
            if time_match:
                current_run = datetime.strptime(time_match.group(1), "%Y-%m-%d %H:%M")
                hour = current_run.hour
                stats["hourly_distribution"][hour] += 1
        
        # 解析模式
        if "早高峰模式激活" in line:
            stats["mode_distribution"]["morning_rush"] += 1
        elif "常规模式" in line:
            stats["mode_distribution"]["normal"] += 1
        
        # 解析回复结果
        if "✅ 成功" in line:
            stats["successful_replies"] += 1
            stats["total_replies"] += 1
        elif "❌ 失败" in line:
            stats["failed_replies"] += 1
            stats["total_replies"] += 1
        
        # 解析完成统计
        if "完成:" in line:
            match = re.search(r'(\d+)/(\d+)', line)
            if match:
                success, total = int(match.group(1)), int(match.group(2))
                stats["backlog_trend"].append({"success": success, "total": total})
    
    return stats

def generate_mock_data():
    """生成模拟数据用于演示"""
    return {
        "total_runs": 48,
        "total_replies": 156,
        "successful_replies": 142,
        "failed_replies": 14,
        "hourly_distribution": {6: 2, 7: 4, 8: 6, 9: 5, 10: 4, 11: 3, 
                                12: 3, 13: 3, 14: 3, 15: 3, 16: 3, 17: 3,
                                18: 2, 19: 2, 20: 2, 21: 1, 22: 1, 23: 1},
        "mode_distribution": {"morning_rush": 12, "normal": 36},
        "backlog_trend": [
            {"success": 3, "total": 3}, {"success": 2, "total": 3},
            {"success": 3, "total": 3}, {"success": 1, "total": 3},
            {"success": 3, "total": 3}
        ]
    }

def generate_report(stats):
    """生成分析报告"""
    print("\n" + "="*60)
    print("📊 InStreet 自动回复分析报告")
    print("="*60)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    # 总体统计
    success_rate = (stats["successful_replies"] / stats["total_replies"] * 100) if stats["total_replies"] else 0
    print(f"\n📈 总体统计:")
    print(f"   运行次数: {stats['total_runs']}")
    print(f"   总回复数: {stats['total_replies']}")
    print(f"   成功回复: {stats['successful_replies']}")
    print(f"   失败回复: {stats['failed_replies']}")
    print(f"   成功率: {success_rate:.1f}%")
    
    # 时段分布
    print(f"\n🕐 时段分布:")
    morning = sum(stats["hourly_distribution"].get(h, 0) for h in range(6, 9))
    daytime = sum(stats["hourly_distribution"].get(h, 0) for h in range(9, 18))
    evening = sum(stats["hourly_distribution"].get(h, 0) for h in range(18, 24))
    
    print(f"   早高峰 (06-09): {morning} 次 ({morning/stats['total_runs']*100:.0f}%)")
    print(f"   白天时段 (09-18): {daytime} 次 ({daytime/stats['total_runs']*100:.0f}%)")
    print(f"   晚间时段 (18-24): {evening} 次 ({evening/stats['total_runs']*100:.0f}%)")
    
    # 模式分析
    print(f"\n⚡ 模式分析:")
    rush = stats["mode_distribution"]["morning_rush"]
    normal = stats["mode_distribution"]["normal"]
    print(f"   早高峰模式: {rush} 次")
    print(f"   常规模式: {normal} 次")
    
    # 积压趋势
    if stats["backlog_trend"]:
        recent = stats["backlog_trend"][-5:]
        avg_success = sum(r["success"] for r in recent) / len(recent)
        avg_total = sum(r["total"] for r in recent) / len(recent)
        print(f"\n📉 最近5次处理:")
        print(f"   平均处理: {avg_success:.1f}/{avg_total:.1f} 条")
        print(f"   完成率: {avg_success/avg_total*100:.0f}%")
    
    # 建议
    print(f"\n💡 优化建议:")
    if success_rate < 90:
        print(f"   ⚠️  成功率偏低，检查API稳定性或频率限制")
    if stats["mode_distribution"]["morning_rush"] > stats["total_runs"] * 0.4:
        print(f"   🌅 早高峰任务占比高，考虑延长早高峰时间窗口")
    
    print("="*60)

if __name__ == "__main__":
    stats = parse_instreet_log()
    generate_report(stats)
