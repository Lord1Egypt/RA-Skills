#!/usr/bin/env python3
"""
PingCode API Client - 获取当前用户的任务列表
"""

import requests
import json
import sys
import os
import argparse

# PingCode API 配置
BASE_URL = "https://open.pingcode.com"

# 从环境变量读取凭证（不要硬编码）
CLIENT_ID = os.environ.get("PINGCODE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("PINGCODE_CLIENT_SECRET")

def get_access_token():
    """获取企业令牌 (Client Credentials)"""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("错误：请设置环境变量 PINGCODE_CLIENT_ID 和 PINGCODE_CLIENT_SECRET", file=sys.stderr)
        sys.exit(1)
    
    url = f"{BASE_URL}/v1/auth/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"获取令牌失败: {e}", file=sys.stderr)
        # 不打印 response.text，避免泄露敏感信息
        return None

def get_my_tasks(access_token, limit=20):
    """获取我的工作项列表"""
    url = f"{BASE_URL}/v1/project/work_items"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "page_size": limit,
        "page_index": 0
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取任务失败: {e}", file=sys.stderr)
        return None

def format_tasks(data, assignee_filter=None):
    """格式化任务输出"""
    if not data or "values" not in data:
        return "没有找到任务"
    
    tasks = data["values"]
    total = data.get("total", len(tasks))
    
    if not tasks:
        return "当前没有分配给你的任务"
    
    # 过滤指定负责人的任务
    if assignee_filter:
        filtered_tasks = []
        for task in tasks:
            assignee_obj = task.get("assignee") or {}
            assignee_name = ""
            if isinstance(assignee_obj, dict):
                assignee_name = assignee_obj.get("display_name", "")
            # 模糊匹配
            if assignee_filter.lower() in assignee_name.lower():
                filtered_tasks.append(task)
        tasks = filtered_tasks
        if not tasks:
            return f"没有找到负责人包含 '{assignee_filter}' 的工作项"
    
    filter_info = f" (负责人筛选: {assignee_filter})" if assignee_filter else ""
    output = [f"📋 你的工作项列表 (共 {total} 条，显示 {len(tasks)} 条){filter_info}\n"]
    
    for task in tasks:
        title = task.get("title", "无标题")
        task_id = task.get("id", "未知ID")[:8] if task.get("id") else "未知ID"
        
        # 安全获取字段
        status_obj = task.get("status") or {}
        status = status_obj.get("name", "未分类") if isinstance(status_obj, dict) else "未分类"
        
        priority_obj = task.get("priority") or {}
        priority = priority_obj.get("name", "普通") if isinstance(priority_obj, dict) else "普通"
        
        # 获取负责人
        assignee_obj = task.get("assignee") or {}
        assignee_name = "未分配"
        if isinstance(assignee_obj, dict):
            assignee_name = assignee_obj.get("display_name", "未分配")
        
        # 获取项目
        project_obj = task.get("project") or {}
        project_name = "无项目"
        if isinstance(project_obj, dict):
            project_name = project_obj.get("name", "无项目")
        
        # 状态图标
        status_icon = "⬜"
        if "完成" in status or "done" in status.lower():
            status_icon = "✅"
        elif "进行" in status or "progress" in status.lower():
            status_icon = "🔄"
        elif "延期" in status or "delay" in status.lower():
            status_icon = "⚠️"
        
        output.append(f"{status_icon} [{task_id}] {title}")
        output.append(f"   项目: {project_name} | 状态: {status} | 优先级: {priority}")
        output.append(f"   负责人: {assignee_name}\n")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description='获取 PingCode 工作项列表')
    parser.add_argument('--assignee', help='按负责人名称筛选')
    parser.add_argument('--limit', type=int, default=20, help='返回数量限制')
    args = parser.parse_args()
    
    # 获取访问令牌
    token = get_access_token()
    if not token:
        sys.exit(1)
    
    # 获取任务列表
    tasks_data = get_my_tasks(token, limit=args.limit)
    if not tasks_data:
        sys.exit(1)
    
    # 格式化输出
    result = format_tasks(tasks_data, assignee_filter=args.assignee)
    print(result)

if __name__ == "__main__":
    main()
