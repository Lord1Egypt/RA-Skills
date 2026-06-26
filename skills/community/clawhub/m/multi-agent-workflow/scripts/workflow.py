#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多Agent协作工作流 - 增强版
支持任务拆分、角色分配、结果汇总
"""
import argparse
import json
import sys
import uuid
from datetime import datetime
from typing import Dict, List, Optional

# ─────────────────────────────────────────────
# Agent角色定义
# ─────────────────────────────────────────────

ROLES = {
    "content_expert": {
        "name": "内容专家",
        "tasks": ["写文章", "写文案", "内容策划", "写小红书", "写知乎", "写抖音"],
        "model": "iflow",
        "capabilities": ["内容创作", "文案撰写", "选题策划"]
    },
    "researcher": {
        "name": "研究员",
        "tasks": ["数据分析", "市场研究", "竞品分析", "调查", "研究"],
        "model": "iflow",
        "capabilities": ["数据分析", "行业研究", "竞品分析"]
    },
    "developer": {
        "name": "开发者",
        "tasks": ["写代码", "调试", "开发", "编程", "代码"],
        "model": "iflow",
        "capabilities": ["代码开发", "自动化", "工具开发"]
    },
    "reviewer": {
        "name": "审核员",
        "tasks": ["审核内容", "审核代码", "质量把控", "检查"],
        "model": "iflow",
        "capabilities": ["质量审核", "风险评估", "代码Review"]
    }
}

# ─────────────────────────────────────────────
# 任务管理
# ─────────────────────────────────────────────

class TaskManager:
    """任务管理器"""
    
    def __init__(self):
        self.tasks = {}
        self.results = {}
    
    def create_task(self, description: str, role: str) -> str:
        """创建任务"""
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        self.tasks[task_id] = {
            "id": task_id,
            "description": description,
            "role": role,
            "role_name": ROLES.get(role, {}).get("name", "未知"),
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        return task_id
    
    def update_status(self, task_id: str, status: str, result: str = ""):
        """更新任务状态"""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
            if result:
                self.results[task_id] = result
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        return self.tasks.get(task_id)
    
    def list_tasks(self) -> List[Dict]:
        return list(self.tasks.values())
    
    def aggregate_results(self) -> Dict:
        """汇总所有任务结果"""
        return {
            "total": len(self.tasks),
            "completed": sum(1 for t in self.tasks.values() if t["status"] == "completed"),
            "failed": sum(1 for t in self.tasks.values() if t["status"] == "failed"),
            "pending": sum(1 for t in self.tasks.values() if t["status"] == "pending"),
            "results": self.results
        }

# ─────────────────────────────────────────────
# 任务分配
# ─────────────────────────────────────────────

def assign_task(task: str) -> str:
    """根据任务描述分配角色"""
    task_lower = task.lower()
    
    # 内容类
    if any(k in task_lower for k in ["写", "文章", "内容", "文案", "小红书", "知乎", "抖音"]):
        return "content_expert"
    # 研究类
    elif any(k in task_lower for k in ["分析", "研究", "调查", "分析"]):
        return "researcher"
    # 开发类
    elif any(k in task_lower for k in ["代码", "开发", "程序", "编程", "写代码"]):
        return "developer"
    # 审核类
    elif any(k in task_lower for k in ["审核", "检查", "把控", "review"]):
        return "reviewer"
    # 默认分配
    else:
        return "researcher"

def split_task(main_task: str, sub_task_count: int = 3) -> List[Dict]:
    """拆分复杂任务"""
    # 简单拆分逻辑
    return [
        {
            "id": i + 1,
            "description": f"{main_task} - 第{i+1}部分",
            "role": assign_task(main_task)
        }
        for i in range(sub_task_count)
    ]

# ─────────────────────────────────────────────
# CLI入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="多Agent协作工作流")
    parser.add_argument("--task", required=True, help="任务描述")
    parser.add_argument("--split", type=int, default=1, help="拆分为多个子任务")
    parser.add_argument("--role", default="auto", help="指定角色（auto自动分配）")
    parser.add_argument("--status", action="store_true", help="查看当前状态")
    
    args = parser.parse_args()
    
    if args.status:
        # 显示状态
        print(json.dumps({"status": "status_mode", "note": "查看任务状态"}, ensure_ascii=False, indent=2))
        return
    
    manager = TaskManager()
    
    if args.split > 1:
        # 拆分任务
        subtasks = split_task(args.task, args.split)
        print(json.dumps({
            "main_task": args.task,
            "subtasks": subtasks,
            "note": "请使用 --subtask-id 指定子任务ID"
        }, ensure_ascii=False, indent=2))
    else:
        # 分配任务
        role = args.role if args.role != "auto" else assign_task(args.task)
        role_info = ROLES.get(role, {})
        
        result = {
            "task": args.task,
            "assigned_role": role,
            "role_name": role_info.get("name", "未知"),
            "capabilities": role_info.get("capabilities", []),
            "status": "ready_to_execute",
            "note": "此配置可用于调用OpenClaw的sessions_spawn执行"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
