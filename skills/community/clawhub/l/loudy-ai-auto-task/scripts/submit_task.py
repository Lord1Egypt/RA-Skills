#!/usr/bin/env python3
"""
提交任务作品链接
"""
import requests
import json
import os

API_BASE = "https://api.loudy.ai/app-api/open-api/v1"
LOUDY_API_KEY = os.environ.get("LOUDY_API_KEY", "")

def submit_task(earning_pool_id: int, task_link: str, language_type: str = "zh_CN"):
    """
    提交任务作品链接
    
    Args:
        earning_pool_id: 奖池ID
        task_link: 作品链接 (推文URL)
        language_type: 语言类型
    
    Returns:
        提交结果
    """
    url = f"{API_BASE}/earning-pool-tasks/submit"
    headers = {
        "X-API-Key": LOUDY_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "earningPoolId": earning_pool_id,
        "taskLink": [task_link],
        "languageType": language_type
    }
    
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    if data.get("code") != 0 and data.get("code") != 200:
        print(f"Error: {data.get('msg')}")
        return None
    
    return data.get("data")

def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python submit_task.py <earning_pool_id> <task_link>")
        sys.exit(1)
    
    pool_id = int(sys.argv[1])
    link = sys.argv[2]
    
    result = submit_task(pool_id, link)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
