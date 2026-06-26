#!/usr/bin/env python3
"""
test_handler.py — Meeting Ops Copilot 测试套件
运行方式：python3 tests/test_handler.py
"""
import sys
import json
from pathlib import Path

# 确保 handler.py 在路径中
sys.path.insert(0, str(Path(__file__).parent.parent))

from handler import handle, build_briefing, build_minutes, build_followup, split_list, parse_raw_text_to_points, extract_action_items


def test_split_list():
    assert split_list("a|b|c") == ["a", "b", "c"]
    assert split_list("a| b | c") == ["a", "b", "c"]
    assert split_list("") == []
    assert split_list("单条") == ["单条"]
    print("  ✅ split_list PASS")


def test_parse_raw_text():
    text = "讨论了A功能延期的风险；决定启用备选方案；张三分头对接供应商"
    points = parse_raw_text_to_points(text)
    assert len(points) >= 2
    assert "A功能" in points[0]
    print("  ✅ parse_raw_text_to_points PASS")


def test_extract_action_items():
    raw = "张三分头对接供应商；李四负责测试并提交报告；王五协调测试环境"
    items = extract_action_items(raw, "", "")
    assert len(items) >= 2
    owners = [item["owner"] for item in items]
    assert "张三" in owners
    assert "李四" in owners
    print("  ✅ extract_action_items PASS")


def test_briefing_boss_mode():
    result = build_briefing(
        meeting_topic="Q2 产品规划评审",
        meeting_date="2026-04-05",
        agenda="Q2目标对齐|技术方案选型|资源评估",
        participants="产品经理|研发负责人|设计负责人"
    )
    assert result["status"] == "success"
    assert result["task"] == "briefing"
    assert result["mode"] == "boss"
    sections = result["sections"]
    assert "conclusion" in sections
    assert "key_points" in sections
    assert "risks" in sections
    assert "suggested_actions" in sections
    assert len(sections["key_points"]) == 3
    assert len(sections["decisions_needed"]) == 3
    assert result["briefing_text"]
    print("  ✅ briefing_boss_mode PASS")


def test_minutes_executor_mode():
    result = build_minutes(
        meeting_topic="周例会",
        meeting_date="2026-03-31",
        raw_text="讨论了A功能延期的风险；决定启用备选方案；张三分头对接供应商；李四负责测试",
        decisions="启用备选方案",
        participants="张三|李四|王五",
        mode="executor"
    )
    assert result["status"] == "success"
    assert result["task"] == "minutes"
    assert "discussion_points" in result["minutes"]
    assert "decisions" in result["minutes"]
    assert "action_items" in result["minutes"]
    assert len(result["minutes"]["action_items"]) >= 2
    assert result["minutes_text"]
    # 检查待办提取
    items = result["minutes"]["action_items"]
    owners = [item["owner"] for item in items]
    assert "张三" in owners
    print("  ✅ minutes_executor_mode PASS")


def test_minutes_boss_mode():
    result = build_minutes(
        meeting_topic="Q2规划评审",
        meeting_date="2026-04-05",
        raw_text="确认Q2目标为DAU增长30%；技术方案采用微服务架构",
        decisions="Q2目标确认|采用微服务架构",
        participants="产品|研发",
        mode="boss"
    )
    assert result["status"] == "success"
    assert result["mode"] == "boss"
    assert result["minutes"]["decisions"] == ["Q2目标确认", "采用微服务架构"]
    print("  ✅ minutes_boss_mode PASS")


def test_followup_executor_mode():
    action_items = [
        {"task": "对接供应商", "owner": "张三", "deadline": "2026-04-10", "priority": "high"},
        {"task": "测试并提交报告", "owner": "李四", "deadline": "2026-04-12", "priority": "high"},
    ]
    result = build_followup(
        meeting_topic="周例会",
        meeting_date="2026-03-31",
        decisions="启用备选方案",
        action_items=action_items,
        mode="executor"
    )
    assert result["status"] == "success"
    assert result["task"] == "followup"
    assert result["draft_email"]
    assert result["draft_message"]
    assert "Subject:" in result["draft_email"]
    assert "对接供应商" in result["draft_email"]
    print("  ✅ followup_executor_mode PASS")


def test_followup_boss_mode():
    action_items = [
        {"task": "确认Q2目标", "owner": "产品", "deadline": "2026-04-07", "priority": "high"},
    ]
    result = build_followup(
        meeting_topic="Q2规划评审",
        meeting_date="2026-04-05",
        decisions="Q2目标确认为DAU+30%",
        action_items=action_items,
        mode="boss"
    )
    assert result["status"] == "success"
    assert result["mode"] == "boss"
    assert "DAU" in result["draft_email"]
    print("  ✅ followup_boss_mode PASS")


def test_handle_main_entry():
    """通过 handle() 主入口调用，测试完整流程"""
    result = handle(
        topic="",
        user_input="",
        args={
            "task": "briefing",
            "meeting_topic": "Q2 产品规划评审",
            "meeting_date": "2026-04-05",
            "mode": "boss",
            "agenda": "Q2目标对齐|技术方案选型",
            "participants": "产品经理|研发负责人"
        }
    )
    assert result["status"] == "success"
    assert result["sections"]["conclusion"]
    print("  ✅ handle_main_entry PASS")


def test_validation_missing_agenda():
    result = handle(
        topic="测试会议",
        user_input="",
        args={
            "task": "briefing",
            "meeting_topic": "测试会议",
            "meeting_date": "2026-03-31",
            "mode": "boss",
            "agenda": ""
        }
    )
    assert result["status"] == "error"
    assert "需要提供 agenda" in result["message"]
    print("  ✅ validation_missing_agenda PASS")


def test_validation_missing_topic():
    result = handle(
        topic="",
        user_input="",
        args={
            "task": "minutes",
            "meeting_topic": "",
            "meeting_date": "2026-03-31",
            "mode": "executor",
            "raw_text": "some discussion text"
        }
    )
    assert result["status"] == "error"
    print("  ✅ validation_missing_topic PASS")


def test_validation_unknown_task():
    result = handle(
        topic="测试",
        user_input="",
        args={
            "task": "unknown_task",
            "meeting_topic": "测试",
            "meeting_date": "2026-03-31",
            "mode": "boss"
        }
    )
    assert result["status"] == "error"
    assert "不支持的任务类型" in result["message"]
    print("  ✅ validation_unknown_task PASS")




def test_validation_whitespace_raw_text():
    # DEF-001: 纯空格字符串应被正确拒绝
    result = handle(
        topic="",
        user_input="",
        args={
            "task": "minutes",
            "meeting_topic": "测试会议",
            "meeting_date": "2026-03-31",
            "mode": "executor",
            "raw_text": "   "  # 纯空格
        }
    )
    assert result["status"] == "error", "纯空格 raw_text 应返回 error"
    assert "raw_text" in result["message"]
    print("  ✅ test_validation_whitespace_raw_text PASS")


def test_validation_empty_raw_text():
    # DEF-001: 空字符串应被正确拒绝
    result = handle(
        topic="",
        user_input="",
        args={
            "task": "minutes",
            "meeting_topic": "测试会议",
            "meeting_date": "2026-03-31",
            "mode": "executor",
            "raw_text": ""
        }
    )
    assert result["status"] == "error", "空 raw_text 应返回 error"
    assert "raw_text" in result["message"]
    print("  ✅ test_validation_empty_raw_text PASS")

def run_all_tests():
    print("=" * 60)
    print("🧪 Meeting Ops Copilot — 测试套件")
    print("=" * 60)
    tests = [
        ("split_list", test_split_list),
        ("parse_raw_text", test_parse_raw_text),
        ("extract_action_items", test_extract_action_items),
        ("briefing_boss_mode", test_briefing_boss_mode),
        ("minutes_executor_mode", test_minutes_executor_mode),
        ("minutes_boss_mode", test_minutes_boss_mode),
        ("followup_executor_mode", test_followup_executor_mode),
        ("followup_boss_mode", test_followup_boss_mode),
        ("handle_main_entry", test_handle_main_entry),
        ("validation_missing_agenda", test_validation_missing_agenda),
        ("validation_missing_topic", test_validation_missing_topic),
        ("validation_unknown_task", test_validation_unknown_task),
        ("validation_whitespace_raw_text", test_validation_whitespace_raw_text),
        ("validation_empty_raw_text", test_validation_empty_raw_text),
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            print(f"\n▶ {name}")
            fn()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            failed += 1
    print("\n" + "=" * 60)
    print(f"结果：{passed} 通过，{failed} 失败")
    print("=" * 60)
    return failed == 0


if __name__ == "__main__":
    ok = run_all_tests()
    sys.exit(0 if ok else 1)
