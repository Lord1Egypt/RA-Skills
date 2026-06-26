#!/usr/bin/env python3
"""
PingCode API Client - 更新工作项（分配负责人、设置时间）
"""

import requests
import json
import sys
import os
import argparse
from datetime import datetime

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

def get_workitem_detail(access_token, workitem_id):
    """获取工作项详情"""
    url = f"{BASE_URL}/v1/project/work_items"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {"page_size": 100}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get("values", []):
            item_id = item.get("id", "")
            if item_id == workitem_id or item_id.startswith(workitem_id):
                return item
        return None
    except requests.exceptions.RequestException as e:
        print(f"查找工作项失败: {e}", file=sys.stderr)
        return None

def update_workitem(access_token, workitem_id, updates):
    """更新工作项"""
    url = f"{BASE_URL}/v1/project/work_items/{workitem_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.patch(url, headers=headers, json=updates, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"更新工作项失败: {e}", file=sys.stderr)
        return None

def format_datetime(date_str):
    """格式化日期字符串为 Unix 时间戳（秒）"""
    if not date_str:
        return None
    
    # 支持多种输入格式
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            # 转换为 Unix 时间戳（秒）
            return int(dt.timestamp())
        except ValueError:
            continue
    
    # 如果输入是纯数字，直接作为时间戳返回
    try:
        return int(date_str)
    except ValueError:
        pass
    
    return None

def main():
    parser = argparse.ArgumentParser(description='更新 PingCode 工作项')
    parser.add_argument('--workitem_id', required=True, help='工作项 ID（完整 ID 或前 8 位）')
    parser.add_argument('--assignee_id', help='负责人用户 ID')
    parser.add_argument('--start_date', help='开始时间（格式: YYYY-MM-DD 或 YYYY-MM-DD HH:MM）')
    parser.add_argument('--due_date', help='截止时间（格式: YYYY-MM-DD 或 YYYY-MM-DD HH:MM）')
    parser.add_argument('--status', help='状态名称')
    parser.add_argument('--priority', help='优先级名称')
    args = parser.parse_args()
    
    if not any([args.assignee_id, args.start_date, args.due_date, args.status, args.priority]):
        print("错误：请至少提供一个要更新的字段", file=sys.stderr)
        sys.exit(1)
    
    # 获取访问令牌
    token = get_access_token()
    if not token:
        sys.exit(1)
    
    # 查找工作项
    print(f"正在查找工作项 {args.workitem_id}...")
    workitem = get_workitem_detail(token, args.workitem_id)
    
    if not workitem:
        print(f"错误：未找到工作项 {args.workitem_id}", file=sys.stderr)
        sys.exit(1)
    
    workitem_id = workitem.get("id")
    workitem_title = workitem.get("title", "未命名")
    
    print(f"找到工作项: [{workitem_id[:8]}] {workitem_title}")
    
    # 构建更新内容
    updates = {}
    
    # 更新负责人（需要提供用户 ID）
    if args.assignee_id:
        updates["assignee_id"] = args.assignee_id
    
    # 更新开始时间
    if args.start_date:
        formatted = format_datetime(args.start_date)
        if not formatted:
            print(f"错误：开始时间格式不正确 '{args.start_date}'", file=sys.stderr)
            sys.exit(1)
        updates["start_at"] = formatted
    
    # 更新截止时间
    if args.due_date:
        formatted = format_datetime(args.due_date)
        if not formatted:
            print(f"错误：截止时间格式不正确 '{args.due_date}'", file=sys.stderr)
            sys.exit(1)
        updates["end_at"] = formatted
    
    # 更新状态
    if args.status:
        updates["status"] = {"name": args.status}
    
    # 更新优先级
    if args.priority:
        updates["priority"] = {"name": args.priority}
    
    # 执行更新
    print(f"\n正在更新工作项...")
    print(f"更新内容: {json.dumps(updates, indent=2, ensure_ascii=False)}")
    
    result = update_workitem(token, workitem_id, updates)
    
    if result:
        print(f"\n✅ 更新成功！")
        print(f"工作项: [{workitem_id[:8]}] {workitem_title}")
        if args.assignee_id:
            print(f"负责人 ID: {args.assignee_id[:8]}...")
        if args.start_date:
            print(f"开始时间: {args.start_date}")
        if args.due_date:
            print(f"截止时间: {args.due_date}")
        if args.status:
            print(f"状态: {args.status}")
        if args.priority:
            print(f"优先级: {args.priority}")
    else:
        print(f"\n❌ 更新失败，请检查 API 权限或参数格式", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
