#!/usr/bin/env python3
"""
PingCode API Client - 获取指定项目的全部工作项
"""

import requests
import json
import sys
import os
import argparse

# PingCode API 配置
BASE_URL = "https://open.pingcode.com"

# 从环境变量读取凭证
CLIENT_ID = os.environ.get("PINGCODE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("PINGCODE_CLIENT_SECRET")

def get_access_token():
    """获取企业令牌"""
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
        return None

def get_project_by_name(access_token, project_name):
    """通过项目名称查找项目 ID"""
    url = f"{BASE_URL}/v1/agile/projects"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {"page_size": 100, "page_index": 0}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        for project in data.get("values", []):
            if project_name.lower() in project.get("name", "").lower():
                return project.get("id")
        return None
    except requests.exceptions.RequestException as e:
        print(f"查找项目失败: {e}", file=sys.stderr)
        return None

def get_project_workitems(access_token, project_id, limit=100):
    """获取指定项目的工作项列表"""
    url = f"{BASE_URL}/v1/project/work_items"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "project_id": project_id,
        "page_size": limit,
        "page_index": 0
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取工作项失败: {e}", file=sys.stderr)
        return None

def format_workitems(data, project_name=""):
    """格式化工作项输出"""
    if not data or "values" not in data:
        return "没有找到工作项"
    
    items = data["values"]
    total = data.get("total", len(items))
    
    if not items:
        return "该项目下没有工作项"
    
    project_info = f" - {project_name}" if project_name else ""
    output = [f"📋 项目工作项{project_info} (共 {total} 条)\n"]
    
    for item in items:
        title = item.get("title", "无标题")
        item_id = item.get("id", "未知ID")[:8]
        
        # 获取状态
        status_obj = item.get("status") or {}
        status = status_obj.get("name", "未分类") if isinstance(status_obj, dict) else "未分类"
        
        # 获取优先级
        priority_obj = item.get("priority") or {}
        priority = priority_obj.get("name", "普通") if isinstance(priority_obj, dict) else "普通"
        
        # 获取负责人
        assignee_obj = item.get("assignee") or {}
        assignee = assignee_obj.get("display_name", "未分配") if isinstance(assignee_obj, dict) else "未分配"
        
        # 获取类型
        type_obj = item.get("type") or {}
        item_type = type_obj.get("name", "未分类") if isinstance(type_obj, dict) else "未分类"
        
        # 状态图标
        status_icon = "⬜"
        if any(s in status for s in ["完成", "done", "closed", "已关闭"]):
            status_icon = "✅"
        elif any(s in status for s in ["进行中", "progress", "处理中"]):
            status_icon = "🔄"
        elif any(s in status for s in ["延期", "delay"]):
            status_icon = "⚠️"
        
        output.append(f"{status_icon} [{item_id}] {title}")
        output.append(f"   类型: {item_type} | 状态: {status} | 优先级: {priority}")
        output.append(f"   负责人: {assignee}")
        output.append("")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description='获取 PingCode 指定项目的全部工作项')
    parser.add_argument('--project_id', help='项目 ID')
    parser.add_argument('--project_name', help='项目名称（模糊匹配）')
    parser.add_argument('--limit', type=int, default=100, help='返回数量限制')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出')
    args = parser.parse_args()
    
    if not args.project_id and not args.project_name:
        print("错误：请提供 --project_id 或 --project_name", file=sys.stderr)
        sys.exit(1)
    
    # 获取访问令牌
    token = get_access_token()
    if not token:
        sys.exit(1)
    
    project_id = args.project_id
    project_name = args.project_name or ""
    
    # 如果提供了项目名称，查找对应的项目 ID
    if not project_id and args.project_name:
        project_id = get_project_by_name(token, args.project_name)
        if not project_id:
            print(f"错误：未找到项目名称包含 '{args.project_name}' 的项目", file=sys.stderr)
            sys.exit(1)
        project_name = args.project_name
    
    # 获取工作项
    workitems_data = get_project_workitems(token, project_id, limit=args.limit)
    if not workitems_data:
        sys.exit(1)
    
    # 输出结果
    if args.json:
        print(json.dumps(workitems_data, indent=2, ensure_ascii=False))
    else:
        result = format_workitems(workitems_data, project_name=project_name)
        print(result)

if __name__ == "__main__":
    main()
