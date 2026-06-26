#!/usr/bin/env python3
"""
principles-agent CLI - OpenClaw 集成入口
基于第一性原理分析复杂问题
用法: principles "你的目标描述"
"""

import argparse
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from orchestrator import PrinciplesOrchestrator


def main():
    parser = argparse.ArgumentParser(
        description="principles-agent - 基于第一性原理的迭代式 Agent (OpenClaw)"
    )
    parser.add_argument(
        "prompt",
        help="目标描述，例如: '设计一个基于第一性原理的多 Agent 系统'"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=5,
        help="最大迭代精炼次数"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="输出报告文件路径"
    )
    args = parser.parse_args()

    # principles-agent 完全依赖 OpenClaw 提供 LLM 调用
    # 在 OpenClaw 运行环境中，llm_call 由主 Agent 注入
    if 'llm_call' not in globals():
        raise RuntimeError(
            "principles-agent 必须在 OpenClaw 会话中运行。"
            "LLM 调用由 OpenClaw 主 Agent 提供，skill 不直接调用外部 API。"
        )

    llm_call = globals()['llm_call']

    orchestrator = PrinciplesOrchestrator(
        llm_call=llm_call,
        max_iterations=args.max_iterations
    )

    print(f"🚀 Starting principles analysis for: {args.prompt[:50]}{'...' if len(args.prompt) > 50 else ''}")
    print("=" * 60)

    result = orchestrator.run(args.prompt)
    report = orchestrator.generate_report(result)

    print("\n" + "=" * 60)
    print(f"✅ Complete! Iterations: {result.iteration_count}")
    print(f"Global validation: {'PASSED' if result.global_validation_passed else 'FAILED'}")
    print(f"Tasks: {len(result.tasks)}, Truths: {len(result.truths)}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}")
    else:
        print("\n" + "=" * 60)
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
