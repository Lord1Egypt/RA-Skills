#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KD Skill Test Script
测试 WorkflowManager 的基本功能
"""

import sys
sys.path.insert(0, r'C:\Users\kkk49\.agents\skills\kd')

from scripts import WorkflowManager

def test_workflow():
    print("="*60)
    print("KD Skill Test - WorkflowManager")
    print("="*60)
    
    # 测试1: 初始化
    print("\n[Test 1] 初始化 WorkflowManager")
    try:
        workflow = WorkflowManager('xiaohongshu', interactive=False)
        print(f"  Platform: {workflow.platform}")
        print(f"  Interactive: {workflow.interactive}")
        keywords = workflow.platform_config.get('keywords', [])
        print(f"  Keywords count: {len(keywords)}")
        print("  [PASS] 初始化成功")
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False
    
    # 测试2: Step 1
    print("\n[Test 2] Step 1: 搜索爆款")
    try:
        manual_trending = [
            '成都周边采摘攻略',
            '周末亲子游玩推荐', 
            '枇杷采摘节来了',
            '带爸妈去体验采摘'
        ]
        result = workflow._run_step1(manual_trending=manual_trending)
        print(f"  Selected keywords: {result.get('selected_keywords', [])}")
        print(f"  Final selection: {len(result.get('final_selection', []))} items")
        print("  [PASS] Step 1 完成")
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False
    
    # 测试3: Step 2
    print("\n[Test 3] Step 2: 读取规则")
    try:
        result = workflow._run_step2()
        rules_count = len(result.get('rules_summary', []))
        print(f"  Rules count: {rules_count}")
        print(f"  Rules file exists: {result.get('rules_exists', False)}")
        print("  [PASS] Step 2 完成")
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False
    
    # 测试4: Step 3
    print("\n[Test 4] Step 3: 外网搜索")
    try:
        # 手动提供外网爆款数据
        manual_external = ['Village Farm Life Cooking']
        result = workflow._run_step3(manual_external=manual_external)
        print(f"  Final selection: {len(result.get('final_selection', []))} items")
        print("  [PASS] Step 3 完成")
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False
    
    # 测试5: Step 4
    print("\n[Test 5] Step 4: 同质化检查")
    try:
        result = workflow._run_step4()
        print(f"  Skipped: {result.get('skipped', False)}")
        print(f"  Themes to avoid: {len(result.get('themes_to_avoid', []))}")
        print("  [PASS] Step 4 完成")
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False
    
    # 测试6: Step 5
    print("\n[Test 6] Step 5: 格式检查")
    try:
        result = workflow._run_step5()
        print(f"  Format confirmed: {result.get('format_confirmed', False)}")
        print(f"  Is new file: {result.get('is_new_file', False)}")
        print("  [PASS] Step 5 完成")
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False
    
    print("\n" + "="*60)
    print("All tests passed!")
    print("="*60)
    return True

if __name__ == '__main__':
    success = test_workflow()
    sys.exit(0 if success else 1)
