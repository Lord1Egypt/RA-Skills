#!/usr/bin/env python3
"""创意工作台功能测试脚本"""
import requests
import json
import time

API_BASE = "http://localhost:50000"

def test_api(endpoint, method="GET", data=None):
    """测试API端点"""
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=data, headers=headers, timeout=5)
        else:
            return False, f"不支持的HTTP方法: {method}"
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"请求失败: {str(e)}"

def run_tests():
    """运行所有测试"""
    print("=== 创意工作台功能测试 ===\n")
    
    # 1. 测试状态获取
    print("1. 测试状态获取...")
    success, result = test_api("/state.json")
    if success:
        print(f"   ✅ 状态获取成功: {result.get('status', 'unknown')}")
    else:
        print(f"   ❌ 状态获取失败: {result}")
    
    # 2. 测试重置功能
    print("\n2. 测试重置功能...")
    success, result = test_api("/reset", "POST")
    if success:
        print(f"   ✅ 重置成功: {result.get('status', 'unknown')}")
    else:
        print(f"   ❌ 重置失败: {result}")
    
    # 3. 测试初始化任务
    print("\n3. 测试初始化任务...")
    data = {
        "topic": "测试创意工作台功能",
        "demand": "测试需求描述",
        "rounds": 1
    }
    success, result = test_api("/init", "POST", data)
    if success:
        print(f"   ✅ 初始化成功: {result.get('status', 'unknown')}")
    else:
        print(f"   ❌ 初始化失败: {result}")
    
    # 4. 测试开始轮次
    print("\n4. 测试开始轮次...")
    data = {"round": 0, "theme": "测试主题"}
    success, result = test_api("/round/start", "POST", data)
    if success:
        print(f"   ✅ 开始轮次成功: {result.get('current_round', -1)}")
    else:
        print(f"   ❌ 开始轮次失败: {result}")
    
    # 5. 测试记录思考
    print("\n5. 测试记录思考...")
    data = {"round": 0, "content": "测试思考内容"}
    success, result = test_api("/log/thinking", "POST", data)
    if success:
        print(f"   ✅ 记录思考成功")
    else:
        print(f"   ❌ 记录思考失败: {result}")
    
    # 6. 测试记录搜索
    print("\n6. 测试记录搜索...")
    data = {
        "round": 0,
        "kw": "测试关键词",
        "findings": "测试搜索发现，这是一个测试搜索内容，用于验证搜索功能是否正常工作。",
        "source_url": "https://www.baidu.com/s?wd=测试",
        "platform": "百度"
    }
    success, result = test_api("/log/search", "POST", data)
    if success:
        print(f"   ✅ 记录搜索成功")
    else:
        print(f"   ❌ 记录搜索失败: {result}")
    
    # 7. 测试添加创意
    print("\n7. 测试添加创意...")
    data = {
        "round": 0,
        "ideas": [
            {
                "发现": "测试发现内容",
                "创意": "测试创意名称",
                "创意描述": "测试创意描述，这是一个测试创意。"
            }
        ]
    }
    success, result = test_api("/idea/add", "POST", data)
    if success:
        print(f"   ✅ 添加创意成功")
    else:
        print(f"   ❌ 添加创意失败: {result}")
    
    # 8. 测试评分筛选
    print("\n8. 测试评分筛选...")
    data = {
        "round": 0,
        "evaluations": [
            {
                "idx": 0,
                "total": 95,
                "feedback": "测试反馈内容"
            }
        ]
    }
    success, result = test_api("/idea/evaluate", "POST", data)
    if success:
        print(f"   ✅ 评分筛选成功: 入围{result.get('progress', {}).get('qualified', 0)}个创意")
    else:
        print(f"   ❌ 评分筛选失败: {result}")
    
    # 9. 测试反馈
    print("\n9. 测试反馈...")
    data = {"round": 0, "content": "测试反馈内容"}
    success, result = test_api("/round/feedback", "POST", data)
    if success:
        print(f"   ✅ 反馈成功")
    else:
        print(f"   ❌ 反馈失败: {result}")
    
    # 10. 测试完成任务
    print("\n10. 测试完成任务...")
    success, result = test_api("/done", "POST")
    if success:
        print(f"   ✅ 完成任务成功: {result.get('status', 'unknown')}")
    else:
        print(f"   ❌ 完成任务失败: {result}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    run_tests()