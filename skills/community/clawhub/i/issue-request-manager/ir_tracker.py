"""
Issue Request Tracker Module
负责跟踪和监控Issue Request的状态
"""

from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict

class IRTracker:
    def __init__(self):
        self.issues_db = {}
        self.status_history = defaultdict(list)
        
    def track_issue(self, issue_id: str) -> Dict[str, Any]:
        """
        跟踪指定Issue的状态
        
        Args:
            issue_id: Issue ID
            
        Returns:
            Issue的当前状态信息
        """
        issue = self.issues_db.get(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")
            
        return {
            "id": issue["id"],
            "title": issue["title"],
            "status": issue["status"],
            "priority": issue["priority"],
            "assignee": issue["assignee"],
            "created_at": issue["created_at"],
            "updated_at": issue["updated_at"],
            "comments_count": len(issue["comments"]),
            "labels": issue["labels"]
        }
    
    def get_issue_history(self, issue_id: str) -> List[Dict[str, Any]]:
        """
        获取Issue的历史记录
        
        Args:
            issue_id: Issue ID
            
        Returns:
            历史记录列表
        """
        return self.status_history.get(issue_id, [])
    
    def update_issue_status(self, issue_id: str, new_status: str, 
                          comment: str = "") -> Dict[str, Any]:
        """
        更新Issue状态
        
        Args:
            issue_id: Issue ID
            new_status: 新状态
            comment: 状态变更评论
            
        Returns:
            更新后的Issue信息
        """
        issue = self.issues_db.get(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")
            
        # 记录状态变更历史
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": new_status,
            "comment": comment
        }
        self.status_history[issue_id].append(history_entry)
        
        # 更新Issue状态
        issue["status"] = new_status
        issue["updated_at"] = datetime.now().isoformat()
        
        # 如果有评论，添加到评论列表
        if comment:
            issue["comments"].append({
                "author": "system",
                "content": comment,
                "timestamp": datetime.now().isoformat()
            })
            
        return issue
    
    def get_issues_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        根据状态获取Issue列表
        
        Args:
            status: 状态值
            
        Returns:
            指定状态的Issue列表
        """
        return [issue for issue in self.issues_db.values() 
                if issue["status"] == status]
    
    def get_issues_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """
        根据优先级获取Issue列表
        
        Args:
            priority: 优先级
            
        Returns:
            指定优先级的Issue列表
        """
        return [issue for issue in self.issues_db.values() 
                if issue["priority"] == priority]
    
    def get_overdue_issues(self) -> List[Dict[str, Any]]:
        """
        获取逾期未处理的Issue
        
        Returns:
            逾期Issue列表
        """
        # 这里可以添加更复杂的逾期逻辑，例如基于创建时间和优先级
        overdue = []
        for issue in self.issues_db.values():
            # 简单示例：假设超过7天的为逾期
            created_time = datetime.fromisoformat(issue["created_at"])
            if (datetime.now() - created_time).days > 7:
                overdue.append(issue)
        return overdue

# 示例使用
if __name__ == "__main__":
    tracker = IRTracker()
    
    # 模拟一些Issue数据
    test_issues = [
        {"id": "#12345678", "title": "登录页面问题", "status": "open", "priority": "high"},
        {"id": "#87654321", "title": "文档更新", "status": "in progress", "priority": "medium"}
    ]
    
    for issue in test_issues:
        tracker.issues_db[issue["id"]] = issue
    
    # 跟踪Issue
    tracked = tracker.track_issue("#12345678")
    print(f"跟踪的Issue: {tracked}")
    
    # 更新状态
    updated = tracker.update_issue_status("#12345678", "in progress", "正在处理中...")
    print(f"更新后的Issue: {updated}")