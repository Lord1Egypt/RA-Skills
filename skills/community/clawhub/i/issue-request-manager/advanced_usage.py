"""
Issue Request Manager 高级使用示例
展示更复杂的使用场景和功能组合
"""

from skills.issue_request_manager import *
import json
from datetime import datetime, timedelta

def advanced_demo():
    """高级功能演示"""
    print("=== Issue Request Manager 高级功能演示 ===\n")
    
    # 1. 创建复杂的Issue场景
    print("1. 创建复杂的Issue场景")
    
    # 创建一个需要多方协作的复杂Issue
    complex_issue = create_issue(
        title="电商平台用户注册流程优化",
        description="需要优化用户注册流程，包括手机号验证、邮箱验证、密码强度检测等环节",
        issue_type="feature",
        priority="high",
        assignee="产品经理",
        labels=["ecommerce", "user-flow", "security"]
    )
    print(f"   ✓ 创建复杂Issue: {complex_issue['id']} - {complex_issue['title']}")
    
    # 添加详细的评论
    reply_to_issue(complex_issue['id'], "需要前端和后端团队共同参与", "产品经理")
    reply_to_issue(complex_issue['id'], "我来负责前端部分", "前端开发")
    reply_to_issue(complex_issue['id'], "我来负责后端API开发", "后端开发")
    print("   ✓ 添加了多轮评论协作")
    
    # 2. 状态变更演示
    print("\n2. 状态变更演示")
    
    # 模拟开发流程
    tracker.update_issue_status(complex_issue['id'], "in progress", "开始设计方案")
    print("   ✓ Issue状态更新为进行中")
    
    tracker.update_issue_status(complex_issue['id'], "review", "设计方案已完成，等待评审")
    print("   ✓ Issue状态更新为评审中")
    
    # 3. 优先级调整
    print("\n3. 优先级调整演示")
    set_priority(complex_issue['id'], "critical")
    print("   ✓ Issue优先级调整为紧急")
    
    # 4. 分配给不同团队
    print("\n4. 团队分配演示")
    assign_issue(complex_issue['id'], "全栈开发团队")
    print("   ✓ Issue已分配给全栈开发团队")
    
    # 5. 搜索和筛选功能
    print("\n5. 搜索和筛选功能演示")
    
    # 按标签搜索
    tagged_issues = responder.search_issues("ecommerce")
    print(f"   按标签'eCommerce'搜索找到 {len(tagged_issues)} 个Issue")
    
    # 按优先级筛选
    high_priority_issues = tracker.get_issues_by_priority("high")
    print(f"   高优先级Issue共 {len(high_priority_issues)} 个")
    
    # 按状态筛选
    open_issues = tracker.get_issues_by_status("open")
    print(f"   开放状态Issue共 {len(open_issues)} 个")
    
    # 6. 评论和历史记录
    print("\n6. 评论和历史记录查看")
    comments = responder.get_issue_comments(complex_issue['id'])
    print(f"   Issue共有 {len(comments)} 条评论")
    
    # 查看状态历史
    history = tracker.get_issue_history(complex_issue['id'])
    print(f"   状态变更历史 {len(history)} 条")
    
    # 7. 微信通知集成演示
    print("\n7. 微信通知集成演示")
    
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
            
            # 发送详细的通知
            recipients = ["product_manager", "tech_lead", "qa_lead"]
            
            # 通知复杂Issue创建
            notify_new_issue(notifier, complex_issue, recipients)
            print("   ✓ 复杂Issue创建通知已发送")
            
            # 通知状态变更
            notify_issue_update(notifier, complex_issue, "status_changed", recipients)
            print("   ✓ 状态变更通知已发送")
            
            # 通知优先级变更
            notify_issue_update(notifier, complex_issue, "priority_changed", recipients)
            print("   ✓ 优先级变更通知已发送")
            
            print("   ✓ 高级微信通知功能演示完成")
        else:
            print("   ⚠ 微信通知未配置，跳过通知演示")
            
    except Exception as e:
        print(f"   ⚠ 微信通知演示出错: {e}")
    
    # 8. 数据导出和分析
    print("\n8. 数据分析演示")
    
    # 获取所有Issue统计
    all_issues = database.list_issues()
    print(f"   总Issue数: {len(all_issues)}")
    
    # 按类型统计
    type_stats = {}
    for issue in all_issues:
        issue_type = issue.get('type', 'unknown')
        type_stats[issue_type] = type_stats.get(issue_type, 0) + 1
    
    print("   Issue类型分布:")
    for issue_type, count in type_stats.items():
        print(f"   - {issue_type}: {count}")
    
    # 按优先级统计
    priority_stats = {}
    for issue in all_issues:
        priority = issue.get('priority', 'unknown')
        priority_stats[priority] = priority_stats.get(priority, 0) + 1
    
    print("   优先级分布:")
    for priority, count in priority_stats.items():
        print(f"   - {priority}: {count}")
    
    # 按状态统计
    status_stats = {}
    for issue in all_issues:
        status = issue.get('status', 'unknown')
        status_stats[status] = status_stats.get(status, 0) + 1
    
    print("   状态分布:")
    for status, count in status_stats.items():
        print(f"   - {status}: {count}")
    
    # 9. 问题关闭演示
    print("\n9. 问题关闭演示")
    close_issue(complex_issue['id'], "注册流程优化已完成，通过测试验证")
    final_status = track_issue(complex_issue['id'])
    print(f"   ✓ Issue {final_status['id']} 已关闭，状态: {final_status['status']}")
    
    # 10. 最终报告
    print("\n10. 最终报告")
    print("   ✅ 高级功能演示完成")
    print("   ✅ 多种Issue类型处理")
    print("   ✅ 完整的协作流程")
    print("   ✅ 丰富的数据分析")
    print("   ✅ 微信通知集成")
    print("   ✅ 状态和历史记录跟踪")
    
    print("\n=== 高级演示完成 ===")

def main():
    """主函数"""
    advanced_demo()

if __name__ == "__main__":
    main()