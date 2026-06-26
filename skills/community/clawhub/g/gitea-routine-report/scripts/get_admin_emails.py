"""
用途：根据 owner/repo 查询仓库 owner 的注册邮箱，供报告邮件默认收件人使用。
输入：repo_full_name（owner/repo）或命令行参数 --repo。
输出：函数返回邮箱字符串；命令行模式输出包含 repo 与 admin_email 的 JSON。
"""

import requests
import os
import json
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/gitea-routine-report/.env"))
GITEA_URL = os.getenv("GITEA_URL")
GITEA_TOKEN = os.getenv("GITEA_TOKEN")
HEADERS = {"Authorization": f"token {GITEA_TOKEN}"}


def get_admin_email(repo_full_name: str) -> str:
    """获取仓库创建人（owner）的注册邮箱"""
    owner = repo_full_name.split("/")[0]
    url = f"{GITEA_URL}/api/v1/users/{owner}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("email", "")
    return ""


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=str, required=True)
    args = parser.parse_args()
    email = get_admin_email(args.repo)
    print(json.dumps({"repo": args.repo, "admin_email": email}))