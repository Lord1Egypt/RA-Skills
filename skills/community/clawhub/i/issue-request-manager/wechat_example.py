"""
微信通知功能使用示例
演示如何使用微信通知功能
"""

from skills.issue_request_manager import *
import json

def setup_wechat_notifier():
    """设置微信通知器"""
    # 注意：实际使用时需要替换为真实的微信企业ID、密钥和应用ID
    notifier = init_wechat_notifier(
        corp_id="your_corp_id_here",  # 替换为实际的CorpID
        secret="your_secret_here",     # 替换为实际的Secret
        agent_id=1000001               # 替换为实际的应用ID
    )
    return notifier

def demonstrate_wechat_notifications():
    """演示微信通知功能"""
    print("=== 微信通知功能演示 ===\n")
    
    # 1. 创建测试Issue
    print("1. 创建测试Issue:")
    test_issue = create_issue(
        title="测试Issue - 微信通知演示",
        description="这是一个用于演示微信通知功能的测试Issue",
        issue_type="task",
        priority="medium",
        assignee="developer_test",
        labels=["test", "notification"]
    )
    print(f"   创建的Issue: {test_issue['id']} - {test_issue['title']}\n")
    
    # 2. 初始化微信通知器（如果配置了微信）
    try:
        # 从配置文件读取微信配置
        with open('skills/issue-request-manager/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        wechat_config = config.get('default_settings', {}).get('wechat_notification', {})
        
        if wechat_config.get('enabled', False) and wechat_config.get('corp_id'):
            print("2. 微信通知配置已启用")
            notifier = init_wechat_notifier(
                corp_id=wechat_config['corp_id'],
                secret=wechat_config['secret'],
                agent_id=wechat_config['agent_id']
            )
            
            # 3. 发送新Issue创建通知
            print("3. 发送新Issue创建通知:")
            recipients = ["user1", "user2"]  # 替换为实际的接收者
            success = notify_new_issue(notifier, test_issue, recipients)
            print(f"   通知发送{'成功' if success else '失败'}\n")
            
            # 4. 模拟Issue状态变更通知
            print("4. 模拟Issue状态变更通知:")
            tracker.update_issue_status(test_issue['id'], "in progress", "开始处理...")
            success = notify_issue_update(notifier, test_issue, "status_changed", recipients)
            print(f"   状态变更通知发送{'成功' if success else '失败'}\n")
            
            # 5. 模拟Issue分配通知
            print("5. 模拟Issue分配通知:")
            assign_issue(test_issue['id'], "new_developer")
            success = notify_issue_update(notifier, test_issue, "assigned", recipients)
            print(f"   分配通知发送{'成功' if success else '失败'}\n")
            
            # 6. 模拟Issue关闭通知
            print("6. 模拟Issue关闭通知:")
            close_issue(test_issue['id'], "问题已解决并验证")
            success = notify_issue_closed(notifier, test_issue, recipients)
            print(f"   关闭通知发送{'成功' if success else '失败'}\n")
        else:
            print("2. 微信通知未配置或未启用")
            print("   请在config.json中配置微信企业ID、密钥和应用ID以启用通知功能。\n")
            
    except Exception as e:
        print(f"2. 微信通知演示出现错误: {e}")
        print("   这可能是由于缺少配置或网络连接问题。\n")

def main():
    """主函数"""
    print("Issue Request Manager - 微信通知功能演示")
    print("=" * 50)
    
    # 演示基本功能
    demonstrate_wechat_notifications()
    
    print("=" * 50)
    print("演示完成！")
    print("\n使用说明:")
    print("- 在config.json中配置企业微信参数以启用通知功能")
    print("- 调用相应函数发送不同类型的通知")
    print("- 接收者列表应包含企业微信中的用户账号")

if __name__ == "__main__":
    main()