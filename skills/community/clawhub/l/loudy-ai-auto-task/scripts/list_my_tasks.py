#!/usr/bin/env python3
"""
查询当前用户的任务列表（分页）
"""
import requests
import json
import os
import sys

API_BASE = "https://api.loudy.ai/app-api/open-api/v1"
LOUDY_API_KEY = os.environ.get("LOUDY_API_KEY", "")

def fetch_my_tasks(page_no: int = 1, page_size: int = 10, earning_pool_id: int = None, task_status: str = None):
    """
    查询当前用户的任务列表
    
    Args:
        page_no: 页码，从1开始
        page_size: 每页条数，最大100
        earning_pool_id: 奖池ID（可选）
        task_status: 任务状态（可选）
    
    Returns:
        任务列表和分页信息
    """
    url = f"{API_BASE}/earning-pool-tasks"
    headers = {
        "X-API-Key": LOUDY_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    params = {
        "pageNo": str(page_no),
        "pageSize": str(page_size)
    }
    
    if earning_pool_id:
        params["earningPoolId"] = str(earning_pool_id)
    if task_status:
        params["taskStatus"] = str(task_status)
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if data.get("code") != 0 and data.get("code") != 200:
        print(f"Error: {data.get('msg')}")
        return None
    
    return data.get("data")

def main():
    page_no = 1
    page_size = 10
    
    if len(sys.argv) >= 2:
        page_no = int(sys.argv[1])
    if len(sys.argv) >= 3:
        page_size = int(sys.argv[2])
    
    result = fetch_my_tasks(page_no, page_size)
    
    if result:
        print(f"总计: {result.get('total')} 条任务")
        print(json.dumps(result.get('list', []), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
