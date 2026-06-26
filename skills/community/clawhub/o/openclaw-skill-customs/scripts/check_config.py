#!/usr/bin/env python3
"""
验证 Leap API 配置是否正确。
用法: python scripts/check_config.py

零外部依赖 — 仅使用 Python 标准库。
"""
import json
import os
import sys
import urllib.request
import urllib.error

DEFAULT_BASE_URL = "https://platform.daofeiai.com"


def check_config():
    """检查 API Key 和 Base URL 配置"""
    api_key = os.environ.get("LEAP_API_KEY", "")
    base_url = DEFAULT_BASE_URL

    results = {
        "api_key_set": bool(api_key),
        "base_url": base_url,
        "connection_ok": False,
        "auth_ok": False,
        "errors": [],
    }

    if not api_key:
        results["errors"].append(
            "LEAP_API_KEY 未配置。\n"
            "  请在 OpenClaw skill 设置界面配置 LEAP_API_KEY 环境变量。"
        )
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return False

    # 测试连通性和认证
    url = f"{base_url}/api/v1/process/tasks?limit=1"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            results["connection_ok"] = True
            if resp.status == 200:
                results["auth_ok"] = True
    except urllib.error.HTTPError as e:
        results["connection_ok"] = True
        if e.code == 401:
            results["errors"].append("API Key 无效或已过期，请检查后重新配置。")
        elif e.code == 403:
            results["errors"].append("API Key 权限不足，请联系管理员。")
        else:
            results["errors"].append(f"API 返回异常状态码: {e.code}")
    except urllib.error.URLError as e:
        results["errors"].append(f"无法连接到 {base_url}，请检查网络或服务状态：{e}")
    except Exception as e:
        results["errors"].append(f"未知错误: {e}")

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results["auth_ok"]


if __name__ == "__main__":
    success = check_config()
    sys.exit(0 if success else 1)
