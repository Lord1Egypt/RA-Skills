#!/usr/bin/env python
"""
Prompt-Router 集成测试

测试场景：
1. 简单任务 → 应该走快速路径
2. 复杂任务 → 应该降级到 LLM
3. 边界情况 → 置信度阈值测试
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
from integration import route_prompt

# 测试用例
TEST_CASES = [
    # (消息，期望匹配的技能，期望 should_invoke)
    ("搜索 Python 教程", "multi-search-engine", True),
    ("查找资料", "multi-search-engine", True),
    ("查询天气", "multi-search-engine", True),
    ("搜索新闻", "multi-search-engine", True),
    ("打开浏览器访问 GitHub", "github-trending-cn", True),
    ("GitHub 热门项目", "github-trending-cn", True),
    ("创建 Excel 表格", "Excel / XLSX", True),
    ("读取 Excel 文件", "Excel / XLSX", True),
    ("生成 PPT", "ppt-generator", True),
    ("改写这篇文章", None, False),  # humanizer 未匹配到
    ("帮我写一篇文章", None, False),  # 复杂任务，应该降级
    ("北京今天天气怎么样", None, False),  # 无 weather 技能
    ("读取 config.json", None, False),  # 无 read 技能
    ("创建一个完整的自动化工作流", "task-decomposer", True),  # 匹配到任务分解
]

def run_tests():
    print("=" * 80)
    print("Prompt-Router 集成测试")
    print("=" * 80)
    print()
    
    total = len(TEST_CASES)
    passed = 0
    failed = 0
    
    for message, expected_skill, expected_invoke in TEST_CASES:
        result = route_prompt(message)
        
        # 检查匹配
        matched_correctly = False
        if expected_skill is None:
            matched_correctly = not result["matched"]
        else:
            matched_correctly = (
                result["matched"] and 
                result["skill_name"] == expected_skill
            )
        
        # 检查 should_invoke
        invoke_correct = result["should_invoke"] == expected_invoke
        
        # 总体通过
        test_passed = matched_correctly and invoke_correct
        
        if test_passed:
            passed += 1
            status = "[PASS]"
        else:
            failed += 1
            status = "[FAIL]"
        
        # 输出结果
        print(f"{status} | {message[:30]:<30}")
        if not test_passed:
            print(f"       期望：skill={expected_skill}, invoke={expected_invoke}")
            print(f"       实际：skill={result['skill_name']}, invoke={result['should_invoke']}, conf={result['confidence']:.2f}")
        else:
            print(f"       → {result['skill_name'] or 'LLM 降级'} (conf={result['confidence']:.2f})")
        print()
    
    # 汇总
    print("=" * 80)
    print(f"测试结果：{passed}/{total} 通过 ({passed/total*100:.1f}%)")
    print(f"         {failed} 个失败")
    print("=" * 80)
    
    # 性能测试
    print()
    print("性能测试:")
    import time
    
    router_calls = 100
    start = time.time()
    for _ in range(router_calls):
        route_prompt("搜索 Python 教程")
    elapsed = time.time() - start
    avg_latency = elapsed / router_calls * 1000  # ms
    
    print(f"  路由 {router_calls} 次，总耗时 {elapsed*1000:.2f}ms")
    print(f"  平均延迟：{avg_latency:.2f}ms")
    print()
    
    return failed == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
