#!/usr/bin/env python3
"""
GitLab MR Review Pipeline - 配置初始化脚本
创建并验证配置文件
"""

import json
import os
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "gitlab-mr-review-pipeline"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_input(prompt, required=True, default=None):
    """获取用户输入"""
    while True:
        if default:
            value = input(f"{prompt} [{default}]: ").strip()
            if not value:
                value = default
        else:
            value = input(f"{prompt}: ").strip()
        
        if value or not required:
            return value
        print("❌ 此项为必填项")


def validate_gitlab_token(token, host):
    """验证 GitLab Token（简单验证）"""
    import urllib.request
    import urllib.error
    
    try:
        url = f"{host}/api/v4/user"
        req = urllib.request.Request(url, headers={"PRIVATE-TOKEN": token})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                user = json.loads(response.read().decode())
                return True, user.get('username', 'unknown')
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "Token 无效"
        elif e.code == 404:
            return False, "GitLab 地址不可访问"
    except Exception as e:
        return False, str(e)
    
    return False, "未知错误"


def validate_repository(token, host, repo):
    """验证仓库是否可访问"""
    import urllib.request
    import urllib.error
    import urllib.parse
    
    try:
        url = f"{host}/api/v4/projects/{urllib.parse.quote(repo, safe='')}"
        req = urllib.request.Request(url, headers={"PRIVATE-TOKEN": token})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                project = json.loads(response.read().decode())
                return True, project.get('name', repo)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, f"仓库 '{repo}' 不存在或无访问权限"
        elif e.code == 401:
            return False, "Token 无权限访问该仓库"
    except Exception as e:
        return False, str(e)
    
    return False, "未知错误"


def create_config():
    """创建配置文件"""
    print("\n📝 GitLab MR Review Pipeline - 配置初始化\n")
    
    # GitLab 配置
    print("=== GitLab 配置 ===")
    gitlab_host = get_input("GitLab 地址（如 http://gitlab.example.com）")
    gitlab_token = get_input("GitLab Access Token")
    
    # 验证 GitLab Token
    print("\n正在验证 GitLab Token...")
    valid, result = validate_gitlab_token(gitlab_token, gitlab_host)
    if not valid:
        print(f"❌ 验证失败：{result}")
        return None
    print(f"✓ GitLab 认证成功，用户：{result}")
    
    # 邮箱配置
    print("\n=== 邮箱配置 ===")
    email_provider = get_input("邮箱服务商（163/qq/126 等）", default="163")
    email_address = get_input("邮箱地址")
    email_auth_code = get_input("邮箱授权码（非登录密码）")
    
    # 仓库列表
    print("\n=== 监控仓库配置 ===")
    print("请输入要监控的仓库列表（格式：owner/repo，多个用逗号分隔）")
    repos_input = get_input("仓库列表（如 owner/repo1,owner/repo2）")
    repositories = [r.strip() for r in repos_input.split(",") if r.strip()]
    
    if not repositories:
        print("❌ 至少需要一个仓库")
        return None
    
    # 验证仓库
    print("\n正在验证仓库...")
    valid_repos = []
    for repo in repositories:
        valid, result = validate_repository(gitlab_token, gitlab_host, repo)
        if valid:
            print(f"✓ {repo}: {result}")
            valid_repos.append(repo)
        else:
            print(f"⚠ {repo}: {result}（跳过）")
    
    if not valid_repos:
        print("❌ 所有仓库都不可访问，无法继续")
        return None
    
    # 构建配置
    config = {
        "gitlab": {
            "host": gitlab_host,
            "access_token": gitlab_token
        },
        "email": {
            "provider": email_provider,
            "address": email_address,
            "auth_code": email_auth_code
        },
        "repositories": valid_repos
    }
    
    return config


def save_config(config):
    """保存配置文件"""
    # 创建配置目录
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    # 保存配置
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # 设置文件权限
    os.chmod(CONFIG_FILE, 0o600)
    
    print(f"\n✓ 配置文件已保存：{CONFIG_FILE}")
    print("✓ 文件权限已设置为 600（仅所有者可读写）")


def main():
    """主函数"""
    # 检查配置是否已存在
    if CONFIG_FILE.exists():
        print(f"⚠ 配置文件已存在：{CONFIG_FILE}")
        choice = input("是否覆盖现有配置？(y/N): ").strip().lower()
        if choice != 'y':
            print("已取消")
            return 1
    
    # 创建配置
    config = create_config()
    if not config:
        print("\n❌ 配置创建失败")
        return 1
    
    # 保存配置
    save_config(config)
    
    print("\n✅ 配置初始化完成！")
    print("\n下一步：运行 pipeline.py 开始 MR 审核")
    print("  python3 skills/gitlab-mr-review-pipeline/scripts/pipeline.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
