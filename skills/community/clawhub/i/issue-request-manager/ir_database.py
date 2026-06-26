"""
Issue Request Database Module
负责Issue Request的数据持久化和管理
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

class IRDatabase:
    def __init__(self, db_path: str = "data/issues.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.issues = self._load_database()
        
    def _load_database(self) -> Dict[str, Any]:
        """从文件加载数据库"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_database(self):
        """保存数据库到文件"""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.issues, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"保存数据库失败: {e}")
    
    def save_issue(self, issue: Dict[str, Any]) -> bool:
        """保存单个Issue"""
        try:
            self.issues[issue["id"]] = issue
            self._save_database()
            return True
        except Exception as e:
            print(f"保存Issue失败: {e}")
            return False
    
    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        """获取指定Issue"""
        return self.issues.get(issue_id)
    
    def list_issues(self) -> List[Dict[str, Any]]:
        """列出所有Issue"""
        return list(self.issues.values())
    
    def update_issue(self, issue_id: str, updated_fields: Dict[str, Any]) -> bool:
        """更新Issue字段"""
        try:
            if issue_id in self.issues:
                self.issues[issue_id].update(updated_fields)
                self.issues[issue_id]["updated_at"] = datetime.now().isoformat()
                self._save_database()
                return True
        except Exception as e:
            print(f"更新Issue失败: {e}")
        return False
    
    def delete_issue(self, issue_id: str) -> bool:
        """删除Issue"""
        try:
            if issue_id in self.issues:
                del self.issues[issue_id]
                self._save_database()
                return True
        except Exception as e:
            print(f"删除Issue失败: {e}")
        return False
    
    def get_issues_by_status(self, status: str) -> List[Dict[str, Any]]:
        """根据状态获取Issue"""
        return [issue for issue in self.issues.values() if issue.get("status") == status]
    
    def get_issues_by_assignee(self, assignee: str) -> List[Dict[str, Any]]:
        """根据负责人获取Issue"""
        return [issue for issue in self.issues.values() if issue.get("assignee") == assignee]
    
    def search_issues(self, query: str) -> List[Dict[str, Any]]:
        """搜索Issue"""
        results = []
        query_lower = query.lower()
        
        for issue in self.issues.values():
            if (query_lower in issue.get("title", "").lower() or 
                query_lower in issue.get("description", "").lower() or
                any(query_lower in label.lower() for label in issue.get("labels", []))):
                results.append(issue)
                
        return results

# 示例使用
if __name__ == "__main__":
    # 创建数据库实例
    db = IRDatabase("test_data/issues.json")
    
    # 创建测试Issue
    test_issue = {
        "id": "#test123",
        "title": "测试Issue",
        "description": "这是一个测试Issue",
        "type": "task",
        "priority": "medium",
        "status": "open",
        "assignee": "test_user",
        "labels": ["test"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "comments": []
    }
    
    # 保存Issue
    success = db.save_issue(test_issue)
    print(f"保存成功: {success}")
    
    # 获取Issue
    retrieved = db.get_issue("#test123")
    print(f"获取的Issue: {retrieved}")
    
    # 列出所有Issue
    all_issues = db.list_issues()
    print(f"所有Issue: {all_issues}")