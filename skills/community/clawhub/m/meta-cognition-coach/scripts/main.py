#!/usr/bin/env python3
"""Meta-Cognition Coach - Develop thinking-about-thinking skills"""

import argparse
import json
from datetime import datetime

REFLECTION_PROMPTS = {
    "planning": [
        "在开始这个任务之前，你做了什么计划？",
        "你预计会遇到什么困难？",
        "你打算如何分配时间？",
        "你有哪些资源可以利用？"
    ],
    "monitoring": [
        "你现在进展如何？",
        "你遇到了什么意外情况？",
        "你的方法有效吗？",
        "你需要调整策略吗？"
    ],
    "evaluation": [
        "你完成任务的方式是什么？",
        "哪些地方做得好？为什么？",
        "哪些地方可以改进？",
        "下次你会怎么做 differently？"
    ]
}

STRATEGY_SUGGESTIONS = {
    "理解困难": [
        "尝试用自己的话解释概念",
        "画思维导图建立联系",
        "找具体例子帮助理解",
        "教给别人来检验理解"
    ],
    "记忆困难": [
        "使用间隔重复法",
        "建立联想和故事",
        "多感官参与（说、写、画）",
        "定期自测检验记忆"
    ],
    "应用困难": [
        "从简单例子开始",
        "分析题目结构",
        "总结解题步骤",
        "多做变式练习"
    ],
    "注意力问题": [
        "番茄工作法（25分钟专注）",
        "减少环境干扰",
        "明确小目标",
        "适当休息恢复精力"
    ]
}

def cmd_reflect(task, approach):
    """Generate reflection prompts"""
    print("=" * 60)
    print("🤔 学习反思引导")
    print("=" * 60)
    print(f"\n任务: {task}")
    print(f"当前方法: {approach}")
    print("\n💭 请思考以下问题：\n")
    
    # Select relevant prompts
    prompts = REFLECTION_PROMPTS["planning"] + REFLECTION_PROMPTS["monitoring"]
    
    for i, prompt in enumerate(prompts[:4], 1):
        print(f"{i}. {prompt}")
    
    print("\n📝 建议：")
    print("   • 写下你的思考，不要只在脑子里想")
    print("   • 诚实面对困难，这是改进的开始")
    print("   • 关注过程，而不是结果对错")
    
    # Save reflection
    data = {
        "type": "reflection",
        "task": task,
        "approach": approach,
        "prompts": prompts[:4],
        "timestamp": datetime.now().isoformat()
    }
    
    with open("reflection_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
    
    print("\n💾 反思记录已保存")

def cmd_strategy(subject, difficulty):
    """Suggest learning strategies"""
    print("=" * 60)
    print("🎯 学习策略建议")
    print("=" * 60)
    print(f"\n科目: {subject}")
    print(f"困难类型: {difficulty}")
    
    # Find matching strategies
    strategies = []
    for key, value in STRATEGY_SUGGESTIONS.items():
        if key in difficulty or any(k in difficulty for k in key):
            strategies = value
            break
    
    if not strategies:
        strategies = STRATEGY_SUGGESTIONS["理解困难"]
    
    print("\n💡 尝试以下策略：\n")
    for i, strategy in enumerate(strategies, 1):
        print(f"{i}. {strategy}")
    
    print("\n🔄 元认知提示：")
    print("   • 选择1-2个策略尝试")
    print("   • 记录使用感受和效果")
    print("   • 根据反馈调整策略")
    print("   • 建立适合自己的策略库")
    
    # Save strategy
    data = {
        "type": "strategy",
        "subject": subject,
        "difficulty": difficulty,
        "strategies": strategies,
        "timestamp": datetime.now().isoformat()
    }
    
    with open("strategy_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
    
    print("\n💾 策略记录已保存")

def cmd_monitor(goal, progress):
    """Self-monitoring guidance"""
    print("=" * 60)
    print("📊 自我监控")
    print("=" * 60)
    print(f"\n目标: {goal}")
    print(f"当前进度: {progress}")
    
    # Simple progress analysis
    try:
        # Try to extract numbers
        goal_num = int(''.join(filter(str.isdigit, goal)) or 100)
        progress_num = int(''.join(filter(str.isdigit, progress)) or 0)
        percentage = min(progress_num / goal_num * 100, 100)
        
        bar_len = 20
        filled = int(percentage / 100 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        
        print(f"\n进度: [{bar}] {percentage:.0f}%")
        
        if percentage < 30:
            status = "起步阶段，保持节奏"
        elif percentage < 70:
            status = "进行中，继续加油"
        else:
            status = "即将完成，冲刺阶段"
        
        print(f"状态: {status}")
    except:
        print("\n进度: 请自行评估完成度")
    
    print("\n🤔 监控问题：")
    print("   1. 你的实际进度符合预期吗？")
    print("   2. 什么因素影响了你的进度？")
    print("   3. 你需要调整计划吗？")
    print("   4. 有什么可以优化的地方？")
    
    print("\n⏰ 下一步行动：")
    print("   • 设定下一个小目标")
    print("   • 预估完成时间")
    print("   • 识别可能的障碍")
    print("   • 准备应对策略")

def main():
    parser = argparse.ArgumentParser(description="Meta-Cognition Coach")
    subparsers = parser.add_subparsers(dest='command')
    
    # reflect
    reflect_parser = subparsers.add_parser('reflect', help='Learning reflection')
    reflect_parser.add_argument('--task', required=True)
    reflect_parser.add_argument('--approach', required=True)
    
    # strategy
    strategy_parser = subparsers.add_parser('strategy', help='Strategy suggestions')
    strategy_parser.add_argument('--subject', required=True)
    strategy_parser.add_argument('--difficulty', required=True)
    
    # monitor
    monitor_parser = subparsers.add_parser('monitor', help='Self-monitoring')
    monitor_parser.add_argument('--goal', required=True)
    monitor_parser.add_argument('--progress', required=True)
    
    args = parser.parse_args()
    
    if args.command == 'reflect':
        cmd_reflect(args.task, args.approach)
    elif args.command == 'strategy':
        cmd_strategy(args.subject, args.difficulty)
    elif args.command == 'monitor':
        cmd_monitor(args.goal, args.progress)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
