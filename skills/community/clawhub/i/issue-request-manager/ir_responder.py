"""
Issue Request Responder Module
负责回复和交互Issue Request
"""

from datetime import datetime
from typing import Dict, Any, List

class IRResponder:
    def __init__(self):
        self.issues_db = {}
        
    def reply_to_issue(self, issue_id: str, content: str, 
                      author: str = "user") -> Dict[str, Any]:
        """
        回复指定Issue
        
        Args:
            issue_id: Issue ID
            content: 回复内容
            author: 回复作者
            
        Returns:
            更新后的Issue信息
        """
        issue = self.issues_db.get(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")
            
        # 添加评论
        comment = {
            "author": author,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        issue["comments"].append(comment)
        issue["updated_at"] = datetime.now().isoformat()
        
        return issue
    
    def add_comment(self, issue_id: str, comment_content: str, 
                   author: str = "user") -> Dict[str, Any]:
        """
        向Issue添加评论
        
        Args:
            issue_id: Issue ID
            comment_content: 评论内容
            author: 评论作者
            
        Returns:
            更新后的Issue信息
        """
        return self.reply_to_issue(issue_id, comment_content, author)
    
    def assign_issue(self, issue_id: str, assignee: str) -> Dict[str, Any]:
        """
        分配Issue给指定用户
        
        Args:
            issue_id: Issue ID
            assignee: 被分配的用户
            
        Returns:
            更新后的Issue信息
        """
        issue = self.issues_db.get(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")
            
        issue["assignee"] = assignee
        issue["updated_at"] = datetime.now().isoformat()
        
        # 添加系统评论
        comment = {
            "author": "system",
            "content": f"Issue已分配给 {assignee}",
            "timestamp": datetime.now().isoformat()
        }
        issue["comments"].append(comment)
        
        return issue
    
    def set_priority(self, issue_id: str, priority: str) -> Dict[str, Any]:
        """
        设置Issue优先级
        
        Args:
            issue_id: Issue ID
            priority: 新优先级
            
        Returns:
            更新后的Issue信息
        """
        issue = self.issues_db.get(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")
            
        old_priority = issue["priority"]
        issue["priority"] = priority
        issue["updated_at"] = datetime.now().isoformat()
        
        # 添加系统评论
        comment = {
            "author": "system",
            "content": f"优先级已从 {old_priority} 更改为 {priority}",
            "timestamp": datetime.now().isoformat()
        }
        issue["comments"].append(comment)
        
        return issue
    
    def close_issue(self, issue_id: str, closing_comment: str = "") -> Dict[str, Any]:
        """
        关闭Issue
        
        Args:
            issue_id: Issue ID
            closing_comment: 关闭评论
            
        Returns:
            更新后的Issue信息
        """
        issue = self.issues_db.get(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")
            
        issue["status"] = "closed"
        issue["updated_at"] = datetime.now().isoformat()
        
        # 添加关闭评论
        if closing_comment:
            comment = {
                "author": "system",
                "content": closing_comment,
                "timestamp": datetime.now().isoformat()
            }
            issue["comments"].append(comment)
        
        return issue
    
    def get_issue_comments(self, issue_id: str) -> List[Dict[str, Any]]:
        """
        获取Issue的所有评论
        
        Args:
            issue_id: Issue ID
            
        Returns:
            评论列表
        """
        issue = self.issues_db.get(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")
            
        return issue["comments"]
    
    def search_issues(self, query: str) -> List[Dict[str, Any]]:
        """
        搜索Issue
        
        Args:
            query: 搜索关键词
            
        Returns:
            匹配的Issue列表
        """
        results = []
        query_lower = query.lower()
        
        for issue in self.issues_db.values():
            # 搜索标题、描述和标签
            if (query_lower in issue["title"].lower() or 
                query_lower in issue["description"].lower() or
                any(query_lower in label.lower() for label in issue["labels"])):
                results.append(issue)
                
        return results

# 示例使用
if __name__ == "__main__":
    responder = IRResponder()
    
    # 模拟Issue数据
    test_issue = {
        "id": "#abcdef12",
        "title": "API文档缺失",
        "description": "缺少API文档导致开发困难",
        "type": "task",
        "priority": "medium",
        "status": "open",
        "assignee": None,
        "labels": ["documentation", "api"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "comments": []
    }
    
    responder.issues_db[test_issue["id"]] = test_issue
    
    # 回复Issue
    replied = responder.reply_to_issue("#abcdef12", "我来处理这个问题", "developer1")
    print(f"回复后的Issue: {replied}")
    
    # 分配Issue
    assigned = responder.assign_issue("#abcdef12", "developer1")
    print(f"分配后的Issue: {assigned}")
    
    # 设置优先级
    prioritized = responder.set_priority("#abcdef12", "high")
    print(f"优先级修改后的Issue: {prioritized}")