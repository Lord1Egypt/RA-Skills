#!/usr/bin/env python3
"""
MaskClaw Behavior Monitor Demo
行为监控演示脚本

Usage:
    python scripts/behavior_monitor_demo.py --user-id user_001 --action send_message
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.behavior_monitor import (
    log_action_to_chain,
    TraceChainLogger,
    get_pending_chains
)


def demo_basic_logging():
    """基础日志记录演示"""
    print("=" * 60)
    print("MaskClaw Behavior Monitor - 基础日志演示")
    print("=" * 60)

    print("\n📝 模拟记录行为链...")

    scenario_tag = "钉钉发送病历截图给同事"

    print("\n🔄 步骤 1: Agent 尝试操作")
    chain_1 = log_action_to_chain(
        user_id="demo_user",
        action="share_or_send",
        resolution="block",
        scenario_tag=scenario_tag,
        app_context="钉钉",
        field="medical_record",
        value_preview="screenshot.png",
        rule_type="H",
        pii_type="MedicalRecord",
        relationship_tag="同事",
        agent_intent="发送病历截图到钉钉对话",
        quality_score=3.6,
        quality_flag="pass",
        base_dir="memory/logs",
        auto_flush=False,
    )
    print(f"   添加动作: resolution={chain_1['final_resolution']}, action_count={chain_1['action_count']}")

    print("\n🔄 步骤 2: 用户拒绝操作")
    chain_2 = log_action_to_chain(
        user_id="demo_user",
        action="share_or_send",
        resolution="correction",
        scenario_tag=scenario_tag,
        app_context="钉钉",
        field="medical_record",
        value_preview="screenshot.png",
        correction_type="user_denied",
        rule_type="H",
        pii_type="MedicalRecord",
        relationship_tag="同事",
        agent_intent="发送病历截图到钉钉对话",
        quality_score=3.6,
        quality_flag="pass",
        base_dir="memory/logs",
        auto_flush=True,
    )
    print(f"   用户纠错: correction_type={chain_2['has_correction']}, "
          f"correction_count={chain_2['correction_count']}")

    print("\n✅ 行为链记录完成!")


def demo_api_usage():
    """API 使用演示"""
    print("\n" + "=" * 60)
    print("MaskClaw Behavior Monitor - API 使用示例")
    print("=" * 60)

    code_example = '''
from scripts.behavior_monitor import log_action_to_chain

# 1. 记录 Agent 操作
log_action_to_chain(
    user_id="user_001",
    action="share_or_send",
    resolution="block",
    scenario_tag="钉钉发送病历截图给同事",
    app_context="钉钉",
    field="medical_record",
    pii_type="MedicalRecord",
    relationship_tag="同事",
    correction_type="user_denied",
    auto_flush=True,
)

# 2. 查询待处理的行为链
from scripts.behavior_monitor import get_pending_chains
pending = get_pending_chains("user_001")
for chain in pending:
    print(f"场景: {chain['scenario_tag']}")
    print(f"纠错次数: {chain['correction_count']}")
'''
    print(code_example)


def demo_correction_types():
    """纠错类型演示"""
    print("\n" + "=" * 60)
    print("MaskClaw Behavior Monitor - 纠错类型说明")
    print("=" * 60)

    correction_types = [
        ("user_denied", "用户明确拒绝", "Agent 的操作被用户直接拒绝"),
        ("user_modified", "用户修正", "用户修改了 Agent 提出的值，信号最强"),
        ("user_interrupted", "用户中断", "用户主动中断操作"),
    ]

    print("\n| 纠错类型 | 说明 | 含义 |")
    print("|:---------|:-----|:------|")
    for ctype, name, meaning in correction_types:
        print(f"| `{ctype}` | {name} | {meaning} |")


def demo_log_format():
    """日志格式示例"""
    print("\n" + "=" * 60)
    print("MaskClaw Behavior Monitor - 日志格式示例")
    print("=" * 60)

    sample_trace = {
        "chain_id": "user_001_钉钉发送病历_1700000001",
        "user_id": "user_001",
        "app_context": "钉钉",
        "scenario_tag": "钉钉发送病历截图给同事",
        "rule_type": "H",
        "action_count": 2,
        "has_correction": True,
        "correction_count": 1,
        "final_resolution": "correction",
        "processed": False,
        "actions": [
            {
                "action_index": 0,
                "action": "share_or_send",
                "resolution": "block",
                "is_correction": False
            },
            {
                "action_index": 1,
                "action": "share_or_send",
                "resolution": "correction",
                "correction_type": "user_denied",
                "is_correction": True
            }
        ]
    }

    print("\n📋 session_trace.jsonl 示例:")
    print(json.dumps(sample_trace, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="MaskClaw Behavior Monitor Demo")
    parser.add_argument("--user-id", "-u", type=str, default="demo_user",
                        help="用户 ID")
    parser.add_argument("--action", "-a", type=str, default="send_message",
                        help="操作类型")
    parser.add_argument("--scenario", "-s", type=str, default="测试场景",
                        help="场景标签")
    parser.add_argument("--demo", "-d", action="store_true",
                        help="运行演示模式")

    args = parser.parse_args()

    if args.demo or not args.action:
        demo_basic_logging()
        demo_api_usage()
        demo_correction_types()
        demo_log_format()
    else:
        print(f"📝 用户: {args.user_id}")
        print(f"📝 操作: {args.action}")
        print(f"📝 场景: {args.scenario}")
        print("\n🔄 记录行为...")
        log_action_to_chain(
            user_id=args.user_id,
            action=args.action,
            resolution="ask",
            scenario_tag=args.scenario,
            app_context="unknown",
            auto_flush=True,
        )
        print("✅ 记录完成!")


if __name__ == "__main__":
    main()
