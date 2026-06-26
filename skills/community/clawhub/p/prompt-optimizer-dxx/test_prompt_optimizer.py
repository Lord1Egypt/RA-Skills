#!/usr/bin/env python3
"""
Prompt Optimizer v3.1 测试用例
运行: python test_prompt_optimizer.py
"""

import sys
import time
from prompt_optimizer import PromptOptimizer, OptimizationResult, __version__


def test(name: str, condition: bool, error_msg: str = ""):
    """测试辅助函数"""
    if condition:
        print(f"  ✅ {name}")
        return True
    else:
        print(f"  ❌ {name}: {error_msg}")
        return False


def run_tests():
    """运行所有测试"""
    optimizer = PromptOptimizer(use_cache=True)
    passed = 0
    failed = 0
    
    print(f"\n🧪 Prompt Optimizer v{__version__} 测试\n")
    
    # ============ 版本测试 ============
    print("📌 版本信息测试:")
    
    if test("版本号存在", __version__ and len(__version__) > 0):
        passed += 1
    else:
        failed += 1
    
    # ============ 基础功能测试 ============
    print("\n📌 基础功能测试:")
    
    if test("基础优化", 
            len(optimizer.optimize("帮我写个排序").optimized) > 10):
        passed += 1
    else:
        failed += 1
    
    try:
        optimizer.optimize("")
        test("空 prompt 检测", False, "应该抛出异常")
        failed += 1
    except ValueError:
        test("空 prompt 检测", True)
        passed += 1
    
    try:
        optimizer.optimize("   ")
        test("空白 prompt 检测", False, "应该抛出异常")
        failed += 1
    except ValueError:
        test("空白 prompt 检测", True)
        passed += 1
    
    # ============ 任务类型测试 ============
    print("\n📌 任务类型测试:")
    
    tests = [
        ("帮我写个排序", "写代码"),
        ("审查这段代码", "代码审查"),
        ("重构这段代码", "改写代码"),
        ("帮我写个文档", "写文档"),
        ("写一段推广文案", "写文案"),
        ("帮我总结一下", "总结摘要"),
        ("翻译成英文", "翻译"),
        ("查一下深圳天气", "查资料"),
        ("分析一下这份数据", "数据分析"),
        ("给我几个创业想法", "头脑风暴"),
        ("计算 123+456", "数学计算"),
        ("聊聊AI的发展", "对话聊天"),
        ("你好", "通用任务"),
    ]
    
    for prompt, expected_type in tests:
        result = optimizer.optimize(prompt)
        if test(f"'{prompt}' → {expected_type}", 
                result.task_type == expected_type,
                f"实际: {result.task_type}"):
            passed += 1
        else:
            failed += 1
    
    # ============ 缓存功能测试 ============
    print("\n📌 缓存功能测试:")
    
    optimizer.clear_cache()
    
    prompt = "帮我写个排序"
    result1 = optimizer.optimize(prompt, use_cache=True)
    
    result2 = optimizer.optimize(prompt, use_cache=True)
    
    if test("缓存命中", result2.cached == True):
        passed += 1
    else:
        failed += 1
    
    result3 = optimizer.optimize(prompt, use_cache=False)
    if test("禁用缓存", result3.cached == False):
        passed += 1
    else:
        failed += 1
    
    stats = optimizer.get_stats()
    if test("缓存统计", "cache" in stats and stats["cache"]["hits"] >= 1):
        passed += 1
    else:
        failed += 1
    
    # ============ 增强功能测试 ============
    print("\n📌 增强功能测试:")
    
    result = optimizer.optimize("帮我写个排序")
    if test("代码任务添加角色", 
            "你是一个专业工程师" in result.optimized):
        passed += 1
    else:
        failed += 1
    
    if test("审查任务添加角色", 
            "代码审查专家" in optimizer.optimize("审查这段代码").optimized):
        passed += 1
    else:
        failed += 1
    
    result = optimizer.optimize("帮我写个排序")
    if test("检测缺失编程语言", 
            "编程语言" in result.missing_info):
        passed += 1
    else:
        failed += 1
    
    # ============ 输出格式测试 ============
    print("\n📌 输出格式测试:")
    
    result = optimizer.optimize("帮我写个排序")
    d = result.to_dict()
    if test("to_dict 转换", 
            isinstance(d, dict) and "original" in d):
        passed += 1
    else:
        failed += 1
    
    json_str = result.to_json()
    if test("to_json 转换", 
            isinstance(json_str, str) and "original" in json_str):
        passed += 1
    else:
        failed += 1
    
    # ============ 统计功能测试 ============
    print("\n📌 统计功能测试:")
    
    stats = optimizer.get_stats()
    if test("统计信息含版本", 
            "version" in stats and stats["version"] == __version__):
        passed += 1
    else:
        failed += 1
    
    if test("统计任务类型数", stats["total_task_types"] > 0):
        passed += 1
    else:
        failed += 1
    
    # ============ 缓存管理测试 ============
    print("\n📌 缓存管理测试:")
    
    optimizer.clear_cache()
    stats = optimizer.get_stats()
    if test("清空缓存", stats["cache"]["hits"] == 0 and stats["cache"]["size"] == 0):
        passed += 1
    else:
        failed += 1
    
    # ============ 性能测试 ============
    print("\n📌 性能测试:")
    
    prompts = [f"帮我写个{p}" for p in ["排序", "查找", "冒泡", "快速", "归并"]]
    
    start = time.time()
    for p in prompts:
        optimizer.optimize(p, use_cache=True)
    batch_time = time.time() - start
    
    if test("批量处理", batch_time < 1.0):
        passed += 1
    else:
        failed += 1
    
    # ============ 配置分离测试 ============
    print("\n📌 配置分离测试:")
    
    from config_data import TASK_PATTERNS, LANGUAGE_PATTERNS, FORMAT_PATTERNS
    
    if test("配置分离-task_patterns", isinstance(TASK_PATTERNS, dict) and len(TASK_PATTERNS) > 0):
        passed += 1
    else:
        failed += 1
    
    if test("配置分离-language_patterns", isinstance(LANGUAGE_PATTERNS, dict) and len(LANGUAGE_PATTERNS) > 0):
        passed += 1
    else:
        failed += 1
    
    # ============ 汇总 ============
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)