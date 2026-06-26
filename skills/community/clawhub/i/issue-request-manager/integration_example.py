"""
Issue Request Manager 与微信通知集成示例
展示如何在实际场景中使用Issue Request管理技能和微信通知
"""

from skills.issue_request_manager import *
import json
import time
from datetime import datetime

def setup_and_demo():
    """设置并演示完整流程"""
    print("=== Issue Request 管理与微信通知集成演示 ===\n")
    
    # 1. 创建Issue管理器实例
    print("1. 初始化Issue Request管理器")
    manager = get_ir_manager()
    print("   ✓ 管理器初始化成功\n")
    
    # 2. 创建多个测试Issue
    print("2. 创建测试Issue")
    issues = []
    
    # 创建Bug Issue
    bug_issue = create_issue(
        title="移动端登录页面样式问题",
        description="用户在手机上登录时，按钮显示异常，无法点击",
        issue_type="bug",
        priority="high",
        assignee="前端开发团队",
        labels=["frontend", "mobile", "bug"]
    )
    issues.append(bug_issue)
    print(f"   ✓ 创建Bug Issue: {bug_issue['id']} - {bug_issue['title']}")
    
    # 创建Feature Issue
    feature_issue = create_issue(
        title="新增用户个人中心功能",
        description="需要添加用户个人中心页面，包含个人信息编辑、设置等功能",
        issue_type="feature",
        priority="medium",
        assignee="产品团队",
        labels=["backend", "feature"]
    )
    issues.append(feature_issue)
    print(f"   ✓ 创建Feature Issue: {feature_issue['id']} - {feature_issue['title']}")
    
    # 创建Task Issue
    task_issue = create_issue(
        title="更新项目文档",
        description="更新API文档和开发指南到最新版本",
        issue_type="task",
        priority="low",
        assignee="文档组",
        labels=["documentation", "task"]
    )
    issues.append(task_issue)
    print(f"   ✓ 创建Task Issue: {task_issue['id']} - {task_issue['title']}\n")
    
    # 3. 跟踪所有Issue
    print("3. 跟踪所有Issue状态")
    for issue in issues:
        tracked = track_issue(issue['id'])
        print(f"   Issue {tracked['id']}: {tracked['title']}")
        print(f"   状态: {tracked['status']}, 优先级: {tracked['priority']}")
        print(f"   分配给: {tracked['assignee']}")
        print(f"   标签: {', '.join(tracked['labels'])}")
        print()
    
    # 4. 模拟Issue交互过程
    print("4. 模拟Issue交互过程")
    
    # 回复Bug Issue
    reply1 = reply_to_issue(bug_issue['id'], "正在调查问题原因", "前端开发")
    print(f"   ✓ 为Bug Issue添加回复")
    
    # 分配Feature Issue
    assigned1 = assign_issue(feature_issue['id'], "后端开发团队")
    print(f"   ✓ Feature Issue已分配给后端团队")
    
    # 更新Task Issue优先级
    prioritized = set_priority(task_issue['id'], "medium")
    print(f"   ✓ Task Issue优先级已提升")
    
    # 更新Bug Issue状态
    tracker.update_issue_status(bug_issue['id'], "in progress", "开始修复...")
    print(f"   ✓ Bug Issue状态已更新为进行中")
    
    # 5. 演示搜索功能
    print("5. 搜索功能演示")
    search_results = responder.search_issues("登录")
    print(f"   搜索'登录'找到 {len(search_results)} 个结果:")
    for result in search_results:
        print(f"   - {result['id']}: {result['title']}")
    
    # 6. 显示评论
    print("\n6. 显示Issue评论")
    comments = responder.get_issue_comments(bug_issue['id'])
    print(f"   Bug Issue共有 {len(comments)} 条评论:")
    for i, comment in enumerate(comments, 1):
        print(f"   {i}. [{comment['author']}] {comment['content']}")
    
    # 7. 模拟微信通知（如果配置了）
    print("\n7. 微信通知模拟")
    try:
        # 从配置文件读取微信配置
        with open('skills/issue-request-manager/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        wechat_config = config.get('default_settings', {}).get('wechat_notification', {})
        
        if wechat_config.get('enabled', False) and wechat_config.get('corp_id'):
            notifier = init_wechat_notifier(
                corp_id=wechat_config['corp_id'],
                secret=wechat_config['secret'],
                agent_id=wechat_config['agent_id']
            )
            
            # 发送通知示例
            recipients = ["manager", "team_lead"]  # 实际使用时替换为真实用户
            
            # 通知新Issue创建
            notify_new_issue(notifier, bug_issue, recipients)
            print("   ✓ 新Issue创建通知已发送")
            
            # 通知状态变更
            notify_issue_update(notifier, bug_issue, "status_changed", recipients)
            print("   ✓ Issue状态变更通知已发送")
            
            print("   ✓ 微信通知功能正常")
        else:
            print("   ⚠ 微信通知未配置，跳过通知发送")
            
    except Exception as e:
        print(f"   ⚠ 微信通知演示出错: {e}")
    
    # 8. 最终状态检查
    print("\n8. 最终状态检查")
    final_bug_status = track_issue(bug_issue['id'])
    print(f"   Bug Issue最终状态: {final_bug_status['status']}")
    
    final_feature_status = track_issue(feature_issue['id'])
    print(f"   Feature Issue最终状态: {final_feature_status['status']}")
    
    final_task_status = track_issue(task_issue['id'])
    print(f"   Task Issue最终状态: {final_task_status['status']}")
    
    print("\n=== 演示完成 ===")
    print("这个示例展示了:")
    print("✓ Issue创建、跟踪、回复的完整流程")
    print("✓ 多种Issue类型的管理")
    print("✓ 评论系统和状态变更记录")
    print("✓ 搜索和筛选功能")
    print("✓ 微信通知集成（如已配置）")

def main():
    """主函数"""
    setup_and_demo()

if __name__ == "__main__":
    main()