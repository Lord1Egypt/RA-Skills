#!/usr/bin/env python3
"""Learning Optimizer - Analyze and optimize learning patterns"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

EFFICIENCY_PATTERNS = {
    "长时间连续学习": {
        "issues": ["注意力下降", "疲劳累积", "效率递减"],
        "suggestions": [
            "使用番茄工作法（25分钟学习+5分钟休息）",
            "每90分钟进行15分钟大休息",
            "交替不同科目保持新鲜感",
            "设置明确的小目标"
        ]
    },
    "容易分心": {
        "issues": ["注意力分散", "频繁中断", "深度思考不足"],
        "suggestions": [
            "清理学习环境，移除干扰物",
            "使用专注APP或白噪音",
            "手机静音或放在另一个房间",
            "设定专注时间段，告知他人勿扰"
        ]
    },
    "时间不规律": {
        "issues": ["生物钟混乱", "难以形成习惯", "效率不稳定"],
        "suggestions": [
            "固定每天的学习时间",
            "找到个人高效时段（晨型/夜型）",
            "建立学习仪式感",
            "使用习惯追踪工具"
        ]
    },
    "缺乏计划": {
        "issues": ["目标不清晰", "时间浪费", "进度失控"],
        "suggestions": [
            "制定每日/每周学习计划",
            "使用优先级矩阵（重要vs紧急）",
            "设定SMART目标",
            "定期回顾和调整计划"
        ]
    }
}

TIME_ALLOCATION_RULES = {
    "高": 0.4,  # 40% of time
    "中": 0.3,  # 30% of time
    "低": 0.2,  # 20% of time
    "复习": 0.1  # 10% of time
}


def storage_root() -> Path:
    root = Path(os.environ.get("LEARNING_OPTIMIZER_HOME", "~/.learning-optimizer")).expanduser()
    root.mkdir(parents=True, exist_ok=True)
    return root


def append_log(name, data):
    path = storage_root() / name
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
    return path


def cmd_analyze(schedule, subjects):
    """Analyze study patterns"""
    print("=" * 60)
    print("📊 学习模式分析")
    print("=" * 60)
    print(f"\n当前安排: {schedule}")
    print(f"学习科目: {subjects}")
    
    subject_list = [s.strip() for s in subjects.split(",")]
    
    # Simple analysis
    print("\n📈 分析结果：")
    
    # Check time distribution
    if "小时" in schedule:
        try:
            hours = int(''.join(filter(str.isdigit, schedule)))
            if hours < 1:
                print("   ⚠️ 学习时间偏少，建议每天至少1小时")
            elif hours > 4:
                print("   ⚠️ 单次学习时间较长，建议分段进行")
            else:
                print("   ✅ 学习时间适中")
        except:
            pass
    
    # Check subject diversity
    if len(subject_list) > 3:
        print("   ⚠️ 科目较多，注意避免频繁切换导致的效率损失")
    elif len(subject_list) == 1:
        print("   ℹ️ 单一科目学习，注意适当休息和科目交替")
    else:
        print("   ✅ 科目数量适中")
    
    print("\n🔍 潜在优化点：")
    print("   1. 记录一周的实际学习时间")
    print("   2. 识别最高效的学习时段")
    print("   3. 统计各科目时间分配")
    print("   4. 记录分心因素和频率")
    
    # Save analysis
    data = {
        "type": "analysis",
        "schedule": schedule,
        "subjects": subject_list,
        "timestamp": datetime.now().isoformat()
    }
    
    path = append_log("analysis_log.jsonl", data)
    print(f"\n💾 分析记录已保存: {path}")

def cmd_optimize(problem, current):
    """Get optimization suggestions"""
    print("=" * 60)
    print("🎯 学习优化建议")
    print("=" * 60)
    print(f"\n当前问题: {problem}")
    print(f"当前做法: {current}")
    
    # Find matching pattern
    matched_pattern = None
    for pattern, data in EFFICIENCY_PATTERNS.items():
        if pattern in problem or any(issue in problem for issue in data["issues"]):
            matched_pattern = pattern
            break
    
    if matched_pattern:
        pattern_data = EFFICIENCY_PATTERNS[matched_pattern]
        print(f"\n📋 识别模式: {matched_pattern}")
        print("\n🔴 主要问题:")
        for issue in pattern_data["issues"]:
            print(f"   • {issue}")
        
        print("\n💡 优化建议:")
        for i, suggestion in enumerate(pattern_data["suggestions"], 1):
            print(f"   {i}. {suggestion}")
    else:
        print("\n💡 通用优化建议:")
        print("   1. 建立固定的学习时间和地点")
        print("   2. 使用番茄工作法提高专注")
        print("   3. 定期回顾和调整学习方法")
        print("   4. 保证充足的睡眠和休息")
    
    print("\n🔄 实施步骤:")
    print("   第1周：选择1个建议尝试")
    print("   第2周：记录效果和感受")
    print("   第3周：根据需要调整")
    print("   第4周：固化有效方法")
    
    # Save optimization
    data = {
        "type": "optimization",
        "problem": problem,
        "current": current,
        "pattern": matched_pattern,
        "timestamp": datetime.now().isoformat()
    }
    
    path = append_log("optimization_log.jsonl", data)
    print(f"\n💾 优化记录已保存: {path}")

def cmd_allocate(total, priorities):
    """Generate time allocation plan"""
    print("=" * 60)
    print("⏰ 时间分配方案")
    print("=" * 60)
    print(f"\n总可用时间: {total}分钟")
    print(f"优先级设置: {priorities}")
    
    # Parse priorities
    priority_list = [p.strip() for p in priorities.split(",")]
    
    # Calculate allocation
    allocation = {}
    remaining = int(total)
    
    for p in priority_list:
        if "高" in p:
            subject = p.replace("高", "").strip()
            time_alloc = int(total * TIME_ALLOCATION_RULES["高"])
            allocation[subject] = time_alloc
            remaining -= time_alloc
        elif "中" in p:
            subject = p.replace("中", "").strip()
            time_alloc = int(total * TIME_ALLOCATION_RULES["中"])
            allocation[subject] = time_alloc
            remaining -= time_alloc
        elif "低" in p:
            subject = p.replace("低", "").strip()
            time_alloc = int(total * TIME_ALLOCATION_RULES["低"])
            allocation[subject] = time_alloc
            remaining -= time_alloc
    
    # Remaining for review
    if remaining > 0:
        allocation["复习/总结"] = remaining
    
    print("\n📊 分配方案:")
    for subject, time_alloc in allocation.items():
        percentage = time_alloc / int(total) * 100
        bar_len = 15
        filled = int(percentage / 100 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"   {subject:10} | {bar} | {time_alloc}分钟 ({percentage:.0f}%)")
    
    print("\n💡 使用建议:")
    print("   • 高优先级科目在高效时段学习")
    print("   • 中优先级科目作为过渡")
    print("   • 预留复习时间巩固记忆")
    print("   • 根据实际效果调整比例")
    
    # Save allocation
    data = {
        "type": "allocation",
        "total": total,
        "priorities": priority_list,
        "allocation": allocation,
        "timestamp": datetime.now().isoformat()
    }
    
    path = append_log("allocation_log.jsonl", data)
    print(f"\n💾 分配方案已保存: {path}")


def cmd_data():
    """Show the local storage directory."""
    print(json.dumps({
        "storage_root": str(storage_root()),
        "logs": [
            "analysis_log.jsonl",
            "optimization_log.jsonl",
            "allocation_log.jsonl"
        ]
    }, ensure_ascii=False, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Learning Optimizer")
    subparsers = parser.add_subparsers(dest='command')
    
    # analyze
    analyze_parser = subparsers.add_parser('analyze', help='Analyze study patterns')
    analyze_parser.add_argument('--schedule', required=True)
    analyze_parser.add_argument('--subjects', required=True)
    
    # optimize
    optimize_parser = subparsers.add_parser('optimize', help='Get optimization suggestions')
    optimize_parser.add_argument('--problem', required=True)
    optimize_parser.add_argument('--current', required=True)
    
    # allocate
    allocate_parser = subparsers.add_parser('allocate', help='Time allocation plan')
    allocate_parser.add_argument('--total', type=int, required=True)
    allocate_parser.add_argument('--priorities', required=True)

    subparsers.add_parser('data', help='Show local storage path')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        cmd_analyze(args.schedule, args.subjects)
    elif args.command == 'optimize':
        cmd_optimize(args.problem, args.current)
    elif args.command == 'allocate':
        cmd_allocate(args.total, args.priorities)
    elif args.command == 'data':
        cmd_data()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
