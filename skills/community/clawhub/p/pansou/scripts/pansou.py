#!/usr/bin/env python3
"""PanSou 网盘搜索 CLI —— OpenClaw Skill 封装。

环境变量:
    PANSOU_URL   服务地址 (如 http://localhost:8888)，必填
    PANSOU_USER  用户名 (认证启用时需要)
    PANSOU_PWD   密码   (认证启用时需要)

Token 存储在 ~/.config/pansou/token.json 中。
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path


try:
    import requests
except ImportError:
    print("错误: 缺少 requests 依赖", file=sys.stderr)
    print("请运行: uv pip install requests", file=sys.stderr)
    sys.exit(1)

# ── 路径 & 配置 ──────────────────────────────────────────────
TOKEN_FILE = Path.home() / ".config" / "pansou" / "token.json"

PANSOU_URL = os.environ.get("PANSOU_URL", "").rstrip("/")
PANSOU_USER = os.environ.get("PANSOU_USER") or ""
PANSOU_PWD = os.environ.get("PANSOU_PWD") or ""
TIMEOUT = 60

# ── Token 管理 ────────────────────────────────────────────────

def load_token() -> Optional[str]:
    """从 token.json 读取 token，如果过期返回 None。"""
    if not TOKEN_FILE.exists():
        return None
    try:
        data = json.loads(TOKEN_FILE.read_text())
        return data.get("token")
    except Exception:
        return None


def save_token(token: str) -> None:
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps({"token": token}, ensure_ascii=False, indent=2))


def login() -> str:
    """登录获取 JWT token 并保存到文件。"""
    if not PANSOU_USER or not PANSOU_PWD:
        print("错误: 服务启用了认证，但未配置 PANSOU_USER / PANSOU_PWD", file=sys.stderr)
        sys.exit(1)
    try:
        resp = requests.post(
            f"{PANSOU_URL}/api/auth/login",
            json={"username": PANSOU_USER, "password": PANSOU_PWD},
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)
    data = resp.json()
    if "error" in data:
        print(f"登录失败: {data['error']}", file=sys.stderr)
        sys.exit(1)
    token = data.get("token")
    if not token:
        print(f"登录响应无 token: {data}", file=sys.stderr)
        sys.exit(1)
    save_token(token)
    return token


def get_token() -> str:
    """获取有效 token，过期自动重新登录。"""
    token = load_token()
    if token:
        return token
    return login()


def auth_header(token: str) -> Dict[str, str]:
    """返回带认证的请求头。"""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }


# ── API 调用 ──────────────────────────────────────────────────

def health() -> Dict[str, Any]:
    """健康检查（无需认证）。"""
    if not PANSOU_URL:
        print("错误: 请设置环境变量 PANSOU_URL", file=sys.stderr)
        sys.exit(1)
    try:
        resp = requests.get(f"{PANSOU_URL}/api/health", timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def verify() -> Dict[str, Any]:
    """验证当前 token 是否有效，无效自动重新登录。"""
    token = load_token()
    if not token:
        print("未找到 token，正在登录...")
        login()
        return {"valid": True, "message": "登录成功"}
    try:
        resp = requests.post(
            f"{PANSOU_URL}/api/auth/verify",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            timeout=TIMEOUT,
        )
        data = resp.json()
        if data.get("valid"):
            return data
        # token 无效，重新登录
        print("Token 已失效，正在重新登录...")
        TOKEN_FILE.unlink(missing_ok=True)
        login()
        return {"valid": True, "message": "已重新登录"}
    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def search(
    keyword: str,
    channels: Optional[List[str]] = None,
    concurrency: Optional[int] = None,
    refresh: bool = False,
    res: str = "merge",
    src: str = "all",
    plugins: Optional[List[str]] = None,
    cloud_types: Optional[List[str]] = None,
    ext: Optional[Dict[str, Any]] = None,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    use_get: bool = False,
) -> Dict[str, Any]:
    """搜索网盘资源。"""
    if not keyword:
        print("错误: 关键词不能为空", file=sys.stderr)
        sys.exit(1)

    if use_get:
        # GET 方式：参数通过 URL query 传递
        from urllib.parse import urlencode
        params: Dict[str, Any] = {"kw": keyword, "res": res, "src": src}
        if channels:
            params["channels"] = ",".join(channels)
        if concurrency:
            params["conc"] = concurrency
        if refresh:
            params["refresh"] = "true"
        if plugins:
            params["plugins"] = ",".join(plugins)
        if cloud_types:
            params["cloud_types"] = ",".join(cloud_types)
        if ext:
            params["ext"] = json.dumps(ext, ensure_ascii=False)
        if include or exclude:
            f: Dict[str, Any] = {}
            if include:
                f["include"] = include
            if exclude:
                f["exclude"] = exclude
            params["filter"] = json.dumps(f, ensure_ascii=False)

        try:
            resp = requests.get(
                f"{PANSOU_URL}/api/search?{urlencode(params, doseq=True)}",
                headers={},
                timeout=TIMEOUT,
            )
        except requests.RequestException as e:
            print(f"请求失败: {e}", file=sys.stderr)
            sys.exit(1)

        if resp.status_code == 401:
            try:
                token = get_token()
                resp = requests.get(
                    f"{PANSOU_URL}/api/search?{urlencode(params, doseq=True)}",
                    headers=auth_header(token),
                    timeout=TIMEOUT,
                )
            except requests.RequestException as e:
                print(f"请求失败: {e}", file=sys.stderr)
                sys.exit(1)

        data = resp.json()
        if "error" in data:
            print(f"搜索失败: {data['error']}", file=sys.stderr)
            sys.exit(1)
        return data

    # POST 方式
    payload: Dict[str, Any] = {"kw": keyword, "res": res, "src": src}
    if channels:
        payload["channels"] = channels
    if concurrency:
        payload["conc"] = concurrency
    if refresh:
        payload["refresh"] = True
    if plugins:
        payload["plugins"] = plugins
    if cloud_types:
        payload["cloud_types"] = cloud_types
    if ext:
        payload["ext"] = ext
    if include or exclude:
        f: Dict[str, Any] = {}
        if include:
            f["include"] = include
        if exclude:
            f["exclude"] = exclude
        payload["filter"] = f

    # 优先尝试无认证请求（服务未启用认证时使用）
    headers_no_auth = {"Content-Type": "application/json", "Accept": "application/json"}
    try:
        resp = requests.post(
            f"{PANSOU_URL}/api/search",
            json=payload,
            headers=headers_no_auth,
            timeout=TIMEOUT,
        )
    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 401 表示需要认证，尝试登录后重试
    if resp.status_code == 401:
        try:
            token = get_token()
            resp = requests.post(
                f"{PANSOU_URL}/api/search",
                json=payload,
                headers=auth_header(token),
                timeout=TIMEOUT,
            )
        except requests.RequestException as e:
            print(f"请求失败: {e}", file=sys.stderr)
            sys.exit(1)

    data = resp.json()
    if "error" in data:
        print(f"搜索失败: {data['error']}", file=sys.stderr)
        sys.exit(1)
    return data


# ── CLI ───────────────────────────────────────────────────────

def main():
    if not PANSOU_URL:
        print("错误: 请设置环境变量 PANSOU_URL", file=sys.stderr)
        sys.exit(1)

    args = sys.argv[1:]
    if not args:
        print("用法: pansou.py <command> [options]")
        print("命令: health, search, login")
        sys.exit(1)

    cmd = args[0]

    if cmd == "health":
        result = health()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "login":
        token = login()
        print("登录成功，token 已保存")

    elif cmd == "verify":
        result = verify()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "search":
        if len(args) < 2:
            print("用法: pansou.py search <关键词> [选项]", file=sys.stderr)
            sys.exit(1)

        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("keyword")
        parser.add_argument("--channels", help="TG频道，逗号分隔")
        parser.add_argument("--conc", type=int, help="并发数")
        parser.add_argument("--refresh", action="store_true", help="强制刷新")
        parser.add_argument("--res", default="merge", choices=["all", "results", "merge"])
        parser.add_argument("--src", default="all", choices=["all", "tg", "plugin"])
        parser.add_argument("--plugins", help="插件，逗号分隔")
        parser.add_argument("--cloud-types", help="网盘类型，逗号分隔")
        parser.add_argument("--include", help="包含关键词，逗号分隔")
        parser.add_argument("--exclude", help="排除关键词，逗号分隔")
        parser.add_argument("--get", action="store_true", help="使用 GET 方式请求")

        a = parser.parse_args(args[1:])

        result = search(
            keyword=a.keyword,
            channels=a.channels.split(",") if a.channels else None,
            concurrency=a.conc,
            refresh=a.refresh,
            res=a.res,
            src=a.src,
            plugins=a.plugins.split(",") if a.plugins else None,
            cloud_types=a.cloud_types.split(",") if a.cloud_types else None,
            include=a.include.split(",") if a.include else None,
            exclude=a.exclude.split(",") if a.exclude else None,
            use_get=a.get,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
