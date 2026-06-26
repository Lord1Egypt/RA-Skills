"""
Issue Request Manager 测试文件
"""

# 测试导入
try:
    from skills.issue_request_manager import *
    print("✓ 成功导入Issue Request Manager模块")
except ImportError as e:
    print(f"✗ 导入失败: {e}")

# 测试基本功能
try:
    # 创建测试Issue
    test_issue = create_issue(
        title="测试Issue",
        description="这是用于测试的Issue",
        issue_type="task",
        priority="medium"
    )
    print("✓ 成功创建测试Issue")
    print(f"  Issue ID: {test_issue['id']}")
    print(f"  标题: {test_issue['title']}")
    
    # 跟踪测试Issue
    tracked = track_issue(test_issue['id'])
    print("✓ 成功跟踪Issue")
    print(f"  状态: {tracked['status']}")
    
    # 回复测试Issue
    replied = reply_to_issue(test_issue['id'], "测试回复", "tester")
    print("✓ 成功回复Issue")
    print(f"  评论数: {len(replied['comments'])}")
    
    print("\n✓ 所有基本功能测试通过!")
    
except Exception as e:
    print(f"✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()