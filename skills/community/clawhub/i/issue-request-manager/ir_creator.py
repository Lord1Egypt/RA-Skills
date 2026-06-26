"""
Issue Request Creator Module
负责创建和初始化Issue Request
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any

class IRCreator:
    def __init__(self):
        self.issues_db = {}
        
    def create_issue(self, title: str, description: str = "", 
                    issue_type: str = "task", priority: str = "medium",
                    assignee: str = None, labels: list = None) -> Dict[str, Any]:
        """
        创建新的Issue Request
        
        Args:
            title: 问题标题
            description: 问题描述
            issue_type: 问题类型 (bug, feature, task)
            priority: 优先级 (low, medium, high, critical)
            assignee: 指派给的用户
            labels: 标签列表
            
        Returns:
            包含新创建Issue信息的字典
        """
        # 生成唯一ID
        issue_id = f"#{uuid.uuid4().hex[:8]}"
        
        # 创建Issue对象
        issue = {
            "id": issue_id,
            "title": title,
            "description": description,
            "type": issue_type,
            "priority": priority,
            "status": "open",
            "assignee": assignee,
            "labels": labels or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "comments": []
        }
        
        # 保存到数据库
        self.issues_db[issue_id] = issue
        
        return issue
    
    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        """获取指定Issue的信息"""
        return self.issues_db.get(issue_id)
    
    def list_issues(self) -> list:
        """列出所有Issue"""
        return list(self.issues_db.values())

# 示例使用
if __name__ == "__main__":
    creator = IRCreator()
    
    # 创建示例Issue
    issue = creator.create_issue(
        title="登录页面样式问题",
        description="用户登录页面的按钮样式在移动端显示不正确",
        issue_type="bug",
        priority="high",
        assignee="developer1",
        labels=["frontend", "mobile"]
    )
    
    print(f"创建的Issue: {issue}")