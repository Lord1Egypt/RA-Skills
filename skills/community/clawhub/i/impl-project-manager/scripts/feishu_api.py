#!/usr/bin/env python3
"""飞书 API 基础工具 — 获取 tenant_access_token"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

# 飞书应用配置
APP_ID = os.environ.get("FEISHU_APP_ID", "cli_aa9d0e7045f81cc8")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "oZ6exMRCZ9imHRkF28agUhxHFArbltk8")
TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

# Token 缓存文件
TOKEN_CACHE = os.path.join(os.path.dirname(__file__), ".feishu_token_cache")


def get_token(force=False):
    """获取 tenant_access_token，带缓存和自动刷新"""
    # 读缓存
    if not force and os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, "r") as f:
            cache = json.load(f)
        if cache.get("expire_time", 0) > time.time() + 300:  # 提前5分钟刷新
            return cache["token"]

    # 请求新 token
    data = json.dumps({
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }).encode("utf-8")

    req = urllib.request.Request(
        TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"❌ 获取 token 失败: HTTP {e.code}", file=sys.stderr)
        print(e.read().decode("utf-8"), file=sys.stderr)
        sys.exit(1)

    if result.get("code") != 0:
        print(f"❌ 获取 token 失败: {result}", file=sys.stderr)
        sys.exit(1)

    token = result["tenant_access_token"]
    expire_time = time.time() + result.get("expire", 7200)

    # 写缓存
    with open(TOKEN_CACHE, "w") as f:
        json.dump({"token": token, "expire_time": expire_time}, f)

    return token


def api_request(url, method="GET", body=None):
    """通用飞书 API 请求"""
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"❌ API 请求失败: {method} {url}", file=sys.stderr)
        print(f"   HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "token"

    if action == "token":
        print(get_token())
    elif action == "test":
        # 测试 API 连通性
        token = get_token()
        print(f"✅ Token 获取成功: {token[:20]}...")
    else:
        print(f"未知动作: {action}", file=sys.stderr)
        sys.exit(1)