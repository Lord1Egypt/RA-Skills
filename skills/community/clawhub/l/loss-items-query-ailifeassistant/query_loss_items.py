#!/usr/bin/env python3
import sys
import requests
import json
import os
from urllib.parse import urlencode

def main():
    # 从环境变量读取 Token（安全！不要硬编码）
    token = os.getenv("LOSS_API_TOKEN")
    if not token:
        print(json.dumps({"error": "缺少 LOSS_API_TOKEN 环境变量"}))
        sys.exit(1)

    # 默认参数
    params = {
        "page": 1,
        "size": 20,
        "status": "pending",
        "sort": "due_remind_at",
        "include_deleted": "false"
    }

    # 解析命令行参数（OpenClaw 会自动传）
    for arg in sys.argv[1:]:
        if arg.startswith("--page="):
            params["page"] = int(arg.split("=")[1])
        elif arg.startswith("--size="):
            params["size"] = int(arg.split("=")[1])
        elif arg.startswith("--status="):
            params["status"] = arg.split("=")[1]
        elif arg.startswith("--sort="):
            params["sort"] = arg.split("=")[1]
        elif arg.startswith("--include_deleted="):
            params["include_deleted"] = arg.split("=")[1]

    url = "https://pre-detailailifeast.alibaba-inc.com/api/v1/loss-items/"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))  # 返回原始 JSON，Skill 会自动总结
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
