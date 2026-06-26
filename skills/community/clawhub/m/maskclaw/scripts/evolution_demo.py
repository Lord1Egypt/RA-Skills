#!/usr/bin/env python3
"""
MaskClaw Skill Evolution Demo
规则自进化演示脚本

Usage:
    python scripts/evolution_demo.py --user-id user_001 --draft-name "钉钉隐私规则"
"""

import argparse
import json
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))


def demo_evolution_flow():
    """进化流程演示"""
    print("=" * 60)
    print("MaskClaw Skill Evolution - 爬山法进化流程")
    print("=" * 60)

    print("""
    ┌─────────────────────────────────────────────────────────────┐
    │  第 1 步：agent 对 skill 做一个小改动                         │
    │         （比如：加一条"必须核对输入数据"的规则）               │
    ├─────────────────────────────────────────────────────────────┤
    │  第 2 步：用改动后的 skill 跑 10 个测试用例                   │
    ├─────────────────────────────────────────────────────────────┤
    │  第 3 步：用 checklist 给每个输出打分                         │
    │         （4 个检查项全过 = 100 分，3 个过 = 75 分...）        │
    ├─────────────────────────────────────────────────────────────┤
    │  第 4 步：算平均分                                           │
    │         - 比上一轮高 → 保留改动                               │
    │         - 比上一轮低 → 撤销改动                              │
    ├─────────────────────────────────────────────────────────────┤
    │  第 5 步：重复，直到连续 3 轮分数超过 90% 或你喊停            │
    └─────────────────────────────────────────────────────────────┘
    """)


def demo_evolution_stages():
    """进化阶段说明"""
    print("\n" + "=" * 60)
    print("MaskClaw Skill Evolution - 进化阶段说明")
    print("=" * 60)

    stages = [
        ("init", "初始化", "创建 SOP 草稿，生成初始内容"),
        ("mutate", "变异", "对 SOP 做小幅改动"),
        ("test", "测试", "运行批量测试用例验证"),
        ("evaluate", "评估", "Checklist 评分 + 爬山决策"),
        ("evolving", "进化中", "迭代优化中"),
        ("sandbox", "沙盒", "最终沙盒验证"),
        ("ready", "就绪", "达标待发布"),
        ("published", "已发布", "正式生效"),
    ]

    print("\n| 阶段 | 名称 | 说明 |")
    print("|:-----|:-----|:-----|")
    for stage, name, desc in stages:
        print(f"| `{stage}` | {name} | {desc} |")


def demo_api_usage():
    """API 使用演示"""
    print("\n" + "=" * 60)
    print("MaskClaw Skill Evolution - API 使用示例")
    print("=" * 60)

    code_example = '''
from scripts.evolution_mechanic import SOPEvolution

# 1. 初始化进化引擎
engine = SOPEvolution(
    logs_root="memory/logs",
    memory_root="memory",
    user_skills_root="user_skills",
)

# 2. 运行完整流水线
result = engine.run_pipeline(
    user_id="user_001",
    draft_name="钉钉隐私规则",
    app_context="钉钉",
    task_goal="安全发送工作消息",
    step="all",
)

# 3. 检查结果
if result["success"]:
    print(f"迭代次数: {result['evolve']['total_iterations']}")
    print(f"最终分数: {result['evolve']['final_score']}")
    print(f"达标: {result['evolve']['reached_threshold']}")
'''
    print(code_example)


def demo_output_example():
    """输出示例"""
    print("\n" + "=" * 60)
    print("MaskClaw Skill Evolution - 输出示例")
    print("=" * 60)

    sample_output = {
        "success": True,
        "user_id": "user_001",
        "draft_name": "钉钉隐私规则",
        "evolve": {
            "success": True,
            "total_iterations": 5,
            "final_score": 92.5,
            "reached_threshold": True,
            "terminated_reason": "consecutive_high",
            "history": [
                {"iteration": 1, "score": 75.2, "decision": "accept"},
                {"iteration": 2, "score": 81.3, "decision": "accept"},
                {"iteration": 3, "score": 88.6, "decision": "accept"},
                {"iteration": 4, "score": 92.5, "decision": "accept"},
            ]
        },
        "sandbox": {
            "success": True,
            "sandbox_passed": True,
        },
        "publish": {
            "success": True,
            "skill_name": "dingtalk-privacy-rule",
            "version": "v1.0.0",
        }
    }

    print("\n📋 完整流水线输出示例:")
    print(json.dumps(sample_output, indent=2, ensure_ascii=False))


def demo_sub_modules():
    """子模块说明"""
    print("\n" + "=" * 60)
    print("MaskClaw Skill Evolution - 子模块")
    print("=" * 60)

    modules = [
        ("SemanticEvaluator", "LLM-as-a-Judge", "快速验证逻辑正确性"),
        ("ChecklistEvaluator", "4项检查评分", "标准化 SOP 质量评估"),
        ("FinalSandbox", "严格验证", "发布前最后一道关卡"),
    ]

    print("\n| 模块 | 名称 | 功能 |")
    print("|:-----|:-----|:-----|")
    for name, title, desc in modules:
        print(f"| `{name}` | {title} | {desc} |")


def main():
    parser = argparse.ArgumentParser(description="MaskClaw Skill Evolution Demo")
    parser.add_argument("--user-id", "-u", type=str, default="demo_user",
                        help="用户 ID")
    parser.add_argument("--draft-name", "-d", type=str, default="测试规则",
                        help="草稿名称")
    parser.add_argument("--step", "-s", type=str, default="all",
                        choices=["rebuild", "init", "evolve", "sandbox", "publish", "all"],
                        help="流水线步骤")
    parser.add_argument("--demo", "-D", action="store_true",
                        help="运行演示模式")

    args = parser.parse_args()

    if args.demo or args.step == "all":
        demo_evolution_flow()
        demo_evolution_stages()
        demo_api_usage()
        demo_output_example()
        demo_sub_modules()
    else:
        print(f"📝 用户: {args.user_id}")
        print(f"📝 草稿: {args.draft_name}")
        print(f"📝 步骤: {args.step}")
        print("\n⚠️ 需要完整的模型服务才能运行演示")
        print("   请运行: python scripts/evolution_demo.py --demo")


if __name__ == "__main__":
    main()
