#!/usr/bin/env python3
"""
MBTI Guru v1.4 - 全面功能测试
测试：恢复、中断、保存、记录、比较
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

from lib.telegram_handler import (
    handle_message, handle_start, handle_resume, handle_history,
    handle_status, handle_cancel, handle_callback,
    get_user_state, clear_user_state,
    save_session, load_session, get_incomplete_session, delete_session
)
from lib.history import save_test_result, get_test_history, compare_tests
from lib.scorer import calculate_type, calculate_clarity
from datetime import datetime

CHAT_ID = 123456  # 测试用chat_id

def print_test(name):
    print(f"\n{'='*50}")
    print(f"测试: {name}")
    print('='*50)

def cleanup():
    """清理测试数据"""
    clear_user_state(CHAT_ID)
    # 删除测试会话文件
    import glob
    for f in glob.glob(f"data/sessions/{CHAT_ID}_*.json"):
        os.remove(f)
    for f in glob.glob(f"data/history/{CHAT_ID}/*.json"):
        os.remove(f)

def test_1_save_and_resume():
    """测试1: 保存和恢复"""
    print_test("保存和恢复")
    
    cleanup()
    
    # 1. 开始测试
    print("\n[1] 开始测试...")
    result = handle_start(CHAT_ID)
    print(f"状态: {result.get('state')}")
    assert result['state'] == 'selecting_version', "应该进入版本选择状态"
    
    # 2. 选择版本
    print("\n[2] 选择版本 70题...")
    result = handle_message(CHAT_ID, "1")
    print(f"状态: {result.get('state')}")
    assert result['state'] == 'testing', "应该进入测试状态"
    
    # 3. 回答几题
    print("\n[3] 回答10题...")
    for i in range(10):
        result = handle_message(CHAT_ID, "A" if i % 2 == 0 else "B")
        if i == 9:
            print(f"已答: {i+1}题")
    
    # 4. 检查状态
    state = get_user_state(CHAT_ID)
    print(f"\n[4] 当前进度: {state.current_index}/{len(state.questions)}")
    print(f"    已保存session_id: {state.session_id}")
    assert state.current_index == 10, "应该已回答10题"
    
    # 5. 模拟中断（不清除状态）
    print("\n[5] 模拟中断...")
    session_id = state.session_id
    
    # 6. 重新开始
    print("\n[6] 重新开始并恢复...")
    clear_user_state(CHAT_ID)
    
    # 手动设置一个未完成的会话
    if session_id:
        # 验证会话存在
        session_data = load_session(session_id)
        print(f"    Session存在: {session_data is not None}")
        print(f"    进度: {session_data['current_index']}/{session_data['questions_total']}")
    
    # 使用resume恢复
    result = handle_resume(CHAT_ID)
    print(f"恢复后状态: {result['state']}")
    
    state = get_user_state(CHAT_ID)
    print(f"恢复后进度: {state.current_index}/{len(state.questions)}")
    assert state.current_index == 10, "恢复后应该从第10题开始"
    
    print("\n✅ 保存和恢复测试通过!")
    return True

def test_2_interrupt():
    """测试2: 中断"""
    print_test("中断")
    
    cleanup()
    
    # 1. 开始测试
    print("\n[1] 开始测试...")
    handle_message(CHAT_ID, "1")
    
    # 2. 回答几题
    print("\n[2] 回答5题...")
    for i in range(5):
        handle_message(CHAT_ID, "A")
    
    # 3. 取消
    print("\n[3] 取消测试...")
    result = handle_cancel(CHAT_ID)
    print(f"消息: {result['message'][:50]}...")
    
    # 4. 验证状态已清除
    state = get_user_state(CHAT_ID)
    print(f"状态: {state.state}")
    assert state.state == "idle", "状态应该重置为idle"
    
    # 5. 尝试恢复（应该失败）
    print("\n[4] 尝试恢复已取消的测试...")
    result = handle_resume(CHAT_ID)
    # 应该返回版本选择界面
    print(f"结果: {result['message'][:50]}...")
    
    print("\n✅ 中断测试通过!")
    return True

def test_3_auto_save():
    """测试3: 自动保存"""
    print_test("自动保存")
    
    cleanup()
    
    # 1. 开始测试
    print("\n[1] 开始测试...")
    handle_message(CHAT_ID, "1")
    
    # 2. 回答10题（应该触发保存）
    print("\n[2] 回答10题（触发自动保存）...")
    for i in range(10):
        result = handle_message(CHAT_ID, "A" if i % 2 == 0 else "B")
    
    state = get_user_state(CHAT_ID)
    print(f"Session ID: {state.session_id}")
    assert state.session_id is not None, "应该有session_id"
    
    # 3. 验证session文件存在
    if state.session_id:
        session_data = load_session(state.session_id)
        print(f"Session文件存在: {session_data is not None}")
        print(f"保存的进度: {session_data['current_index']}/{session_data['questions_total']}")
        assert session_data['current_index'] == 10, "保存的进度应该是10"
    
    print("\n✅ 自动保存测试通过!")
    return True

def test_4_history():
    """测试4: 历史记录"""
    print_test("历史记录")
    
    cleanup()
    
    # 1. 完成一个测试
    print("\n[1] 完成一个测试...")
    handle_message(CHAT_ID, "1")  # 70题版本
    
    # 回答所有70题
    for i in range(70):
        result = handle_message(CHAT_ID, "A" if i % 2 == 0 else "B")
        if result['action'] == 'complete':
            print(f"测试完成! 类型: {result.get('type_code')}")
            break
    
    # 2. 检查历史
    print("\n[2] 查看历史...")
    result = handle_history(CHAT_ID)
    print(f"历史消息: {result['message'][:100]}...")
    
    history = get_test_history(CHAT_ID)
    print(f"历史记录数: {len(history)}")
    assert len(history) >= 1, "应该有至少1条历史"
    
    print("\n✅ 历史记录测试通过!")
    return True

def test_5_compare():
    """测试5: 比较功能"""
    print_test("比较功能")
    
    # 创建两个测试记录
    test1 = {
        "test_id": "test1",
        "type_code": "INFP",
        "scores": {"EI": 70, "SN": 65, "TF": 75, "JP": 60},
        "date": "2026-03-25"
    }
    
    test2 = {
        "test_id": "test2", 
        "type_code": "INFJ",
        "scores": {"EI": 80, "SN": 70, "TF": 65, "JP": 55},
        "date": "2026-03-27"
    }
    
    # 测试比较
    result = compare_tests(test1, test2)
    print(f"类型变化: {result['type_change']}")
    print(f"EI变化: {result['dimension_changes']['EI']['label']}")
    print(f"SN变化: {result['dimension_changes']['SN']['label']}")
    
    assert result['type_change'] == "INFP → INFJ", "类型应该变化"
    
    print("\n✅ 比较功能测试通过!")
    return True

def test_6_status():
    """测试6: 状态查询"""
    print_test("状态查询")
    
    cleanup()
    
    # 1. 空闲状态
    print("\n[1] 空闲状态...")
    result = handle_status(CHAT_ID)
    print(f"消息: {result['message']}")
    assert "空闲" in result['message'], "应该显示空闲"
    
    # 2. 测试中状态
    print("\n[2] 测试中状态...")
    handle_message(CHAT_ID, "1")
    for i in range(5):
        handle_message(CHAT_ID, "A")
    
    result = handle_status(CHAT_ID)
    print(f"消息: {result['message']}")
    assert "测试进行中" in result['message'], "应该显示测试进行中"
    
    # 3. 清理
    handle_cancel(CHAT_ID)
    
    print("\n✅ 状态查询测试通过!")
    return True

def test_7_version_selection():
    """测试7: 版本选择"""
    print_test("版本选择")
    
    cleanup()
    
    versions = {"1": 70, "2": 93, "3": 144, "4": 200}
    
    for key, expected_count in versions.items():
        clear_user_state(CHAT_ID)
        print(f"\n测试版本 {key} ({expected_count}题)...")
        result = handle_message(CHAT_ID, key)
        state = get_user_state(CHAT_ID)
        actual_count = len(state.questions)
        print(f"  题目数: {actual_count}")
        assert actual_count == expected_count, f"应该是{expected_count}题"
    
    handle_cancel(CHAT_ID)
    
    print("\n✅ 版本选择测试通过!")
    return True

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("MBTI Guru v1.4 - 全面功能测试")
    print("="*60)
    
    tests = [
        ("版本选择", test_7_version_selection),
        ("自动保存", test_3_auto_save),
        ("保存和恢复", test_1_save_and_resume),
        ("中断", test_2_interrupt),
        ("状态查询", test_6_status),
        ("历史记录", test_4_history),
        ("比较功能", test_5_compare),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ {name} 测试失败: {e}")
            results.append((name, False))
    
    # 清理
    cleanup()
    
    # 打印结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + ("全部测试通过! 🎉" if all_passed else "有测试失败"))
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
