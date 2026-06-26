#!/usr/bin/env python3
"""
PingCode API Client - 获取项目列表
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

def get_projects(access_token, limit=100):
    """获取项目列表"""
    url = f"{BASE_URL}/v1/agile/projects"
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
        print(f"获取项目失败: {e}", file=sys.stderr)
        return None

def format_projects(data):
    """格式化项目输出"""
    if not data or "values" not in data:
        return "没有找到项目"
    
    projects = data["values"]
    total = data.get("total", len(projects))
    
    if not projects:
        return "当前没有可访问的项目"
    
    output = [f"📁 项目列表 (共 {total} 个)\n"]
    
    for idx, project in enumerate(projects, 1):
        name = project.get("name", "未命名")
        project_id = project.get("id", "未知ID")
        short_id = project_id[:8] if len(project_id) > 8 else project_id
        
        # 获取项目状态
        status_obj = project.get("status") or {}
        status = status_obj.get("name", "未分类") if isinstance(status_obj, dict) else "未分类"
        
        # 获取项目类型
        type_obj = project.get("type") or {}
        proj_type = type_obj.get("name", "未分类") if isinstance(type_obj, dict) else "未分类"
        
        # 获取负责人
        owner_obj = project.get("owner") or {}
        owner_name = "未设置"
        if isinstance(owner_obj, dict):
            owner_name = owner_obj.get("display_name", "未设置")
        
        # 获取描述
        description = project.get("description", "")
        desc_text = description[:50] + "..." if description and len(description) > 50 else (description or "暂无描述")
        
        # 状态图标
        status_icon = "🟢"
        if "归档" in status or "archive" in status.lower():
            status_icon = "📦"
        elif "关闭" in status or "closed" in status.lower():
            status_icon = "🔴"
        
        output.append(f"{idx}. {status_icon} [{short_id}] {name}")
        output.append(f"   类型: {proj_type} | 状态: {status} | 负责人: {owner_name}")
        if desc_text:
            output.append(f"   描述: {desc_text}")
        output.append("")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description='获取 PingCode 项目列表')
    parser.add_argument('--limit', type=int, default=100, help='返回数量限制')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出')
    args = parser.parse_args()
    
    # 获取访问令牌
    token = get_access_token()
    if not token:
        sys.exit(1)
    
    # 获取项目列表
    projects_data = get_projects(token, limit=args.limit)
    if not projects_data:
        sys.exit(1)
    
    # 输出结果
    if args.json:
        print(json.dumps(projects_data, indent=2, ensure_ascii=False))
    else:
        result = format_projects(projects_data)
        print(result)

if __name__ == "__main__":
    main()
