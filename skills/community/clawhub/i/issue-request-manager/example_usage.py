"""
Issue Request Manager 使用示例
演示如何使用Issue Request管理技能
"""

from skills.issue_request_manager import *

def main():
    print("=== Issue Request Manager 使用示例 ===\n")
    
    # 1. 创建Issue Request
    print("1. 创建Issue Request:")
    issue1 = create_issue(
        title="登录页面样式问题",
        description="用户登录页面的按钮样式在移动端显示不正确",
        issue_type="bug",
        priority="high",
        assignee="developer1",
        labels=["frontend", "mobile"]
    )
    print(f"   创建的Issue: {issue1['id']} - {issue1['title']}")
    print(f"   状态: {issue1['status']}")
    print(f"   优先级: {issue1['priority']}\n")
    
    # 2. 创建另一个Issue
    print("2. 创建第二个Issue:")
    issue2 = create_issue(
        title="API文档缺失",
        description="缺少API文档导致开发困难",
        issue_type="task",
        priority="medium",
        assignee="doc_writer",
        labels=["documentation", "api"]
    )
    print(f"   创建的Issue: {issue2['id']} - {issue2['title']}")
    print(f"   状态: {issue2['status']}")
    print(f"   优先级: {issue2['priority']}\n")
    
    # 3. 跟踪Issue状态
    print("3. 跟踪Issue状态:")
    tracked_issue1 = track_issue(issue1['id'])
    print(f"   Issue {tracked_issue1['id']}: {tracked_issue1['title']}")
    print(f"   当前状态: {tracked_issue1['status']}")
    print(f"   分配给: {tracked_issue1['assignee']}")
    print(f"   评论数量: {tracked_issue1['comments_count']}\n")
    
    # 4. 回复Issue
    print("4. 回复Issue:")
    reply1 = reply_to_issue(issue1['id'], "我正在调查此问题", "developer1")
    print(f"   已为Issue {reply1['id']} 添加回复")
    
    reply2 = reply_to_issue(issue1['id'], "请提供更多详细信息", "manager")
    print(f"   已为Issue {reply1['id']} 添加回复\n")
    
    # 5. 分配Issue
    print("5. 分配Issue:")
    assigned = assign_issue(issue2['id'], "developer2")
    print(f"   Issue {assigned['id']} 已分配给 {assigned['assignee']}\n")
    
    # 6. 设置优先级
    print("6. 设置优先级:")
    prioritized = set_priority(issue2['id'], "high")
    print(f"   Issue {prioritized['id']} 优先级已设为 {prioritized['priority']}\n")
    
    # 7. 更新状态
    print("7. 更新Issue状态:")
    tracker.update_issue_status(issue1['id'], "in progress", "开始处理...")
    updated_issue1 = track_issue(issue1['id'])
    print(f"   Issue {updated_issue1['id']} 状态已更新为 {updated_issue1['status']}\n")
    
    # 8. 搜索Issue
    print("8. 搜索Issue:")
    search_results = responder.search_issues("登录")
    print(f"   搜索'登录'找到 {len(search_results)} 个结果")
    for result in search_results:
        print(f"   - {result['id']}: {result['title']}")
    
    # 9. 查看评论
    print("\n9. 查看评论:")
    comments = responder.get_issue_comments(issue1['id'])
    print(f"   Issue {issue1['id']} 共有 {len(comments)} 条评论:")
    for i, comment in enumerate(comments, 1):
        print(f"   {i}. [{comment['author']}] {comment['content']}")
    
    # 10. 关闭Issue
    print("\n10. 关闭Issue:")
    closed = close_issue(issue1['id'], "问题已修复并验证")
    final_status = track_issue(issue1['id'])
    print(f"   Issue {final_status['id']} 状态已更新为 {final_status['status']}")
    
    print("\n=== 示例完成 ===")

if __name__ == "__main__":
    main()