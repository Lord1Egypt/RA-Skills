# -*- coding: utf-8 -*-
"""
gitea_api.py — paper-kb 系统的 Gitea API 封装（共用模块）

职责：
  - 读取 .env 配置（GITEA_URL / GITEA_ADMIN_TOKEN）
  - 封装所有 Gitea REST API 调用
  - 提供 users.json（用户映射表）的读写，带并发冲突重试

users.json 存放位置：
  {GITEA_BOT_USERNAME}/system-config 仓库根目录下的 users.json
"""
from __future__ import annotations

import base64
import json
import os
import time
from pathlib import Path

import requests


# ---------------------------------------------------------------- env 加载

def _load_env() -> None:
    """加载 skill 根目录下的 .env 文件（scripts/ 的上一级）。"""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    here = Path(__file__).resolve().parent
    for candidate in (here / ".env", here.parent / ".env"):
        if candidate.exists():
            load_dotenv(candidate)
            return


_load_env()

GITEA_URL = os.environ.get("GITEA_URL", "http://43.156.243.152:3000").rstrip("/")
ADMIN_TOKEN = os.environ.get("GITEA_ADMIN_TOKEN", "")
BOT_USERNAME = os.environ.get("GITEA_BOT_USERNAME", "AIFusionBot")

SYSTEM_REPO = "system-config"
USERS_FILE = "users.json"

_HEADERS = {
    "Authorization": f"token {ADMIN_TOKEN}",
    "Content-Type": "application/json",
}


class GiteaError(Exception):
    """Gitea API 调用失败。"""


# ---------------------------------------------------------------- 基础请求

def _api(method: str, path: str, *, json_body: dict | None = None,
         params: dict | None = None, ok_codes: tuple = (200, 201, 204)):
    """发起一次 Gitea API 请求，返回 (status_code, parsed_json_or_None)。"""
    url = f"{GITEA_URL}/api/v1{path}"
    resp = requests.request(
        method, url, headers=_HEADERS, json=json_body, params=params, timeout=30
    )
    data = None
    if resp.content:
        try:
            data = resp.json()
        except ValueError:
            data = None
    return resp.status_code, data


# ---------------------------------------------------------------- 用户与权限

def token_is_site_admin() -> bool:
    """检测当前 token 的账号是否为 Gitea 站点管理员。

    管理员才能访问 /admin/users 列表；403 即非管理员。
    """
    code, _ = _api("GET", "/admin/users", params={"limit": 1})
    return code == 200


def get_user(username: str) -> dict | None:
    """查询 Gitea 用户。存在返回用户信息 dict，不存在返回 None。"""
    code, data = _api("GET", f"/users/{username}")
    if code == 200:
        return data
    return None


# ---------------------------------------------------------------- 仓库操作

def repo_exists(owner: str, repo: str) -> bool:
    code, _ = _api("GET", f"/repos/{owner}/{repo}")
    return code == 200


def create_own_repo(name: str, private: bool, description: str) -> None:
    """以 token 所属账号（AIFusionBot）身份创建仓库。409 = 已存在，视为成功。"""
    code, data = _api("POST", "/user/repos", json_body={
        "name": name,
        "private": private,
        "description": description,
        "auto_init": True,
        "default_branch": "main",
    })
    if code in (201, 409):
        return
    raise GiteaError(f"创建仓库 {name} 失败 (HTTP {code}): {data}")


def create_repo_for_user(username: str, name: str, description: str) -> dict:
    """用站点管理员身份，给指定用户创建私有仓库。

    返回: {"created": True/False(已存在), "html_url": 仓库地址}
    """
    if repo_exists(username, name):
        return {
            "created": False,
            "html_url": f"{GITEA_URL}/{username}/{name}",
        }
    code, data = _api("POST", f"/admin/users/{username}/repos", json_body={
        "name": name,
        "private": True,
        "description": description,
        "auto_init": True,
        "default_branch": "main",
    })
    if code == 201:
        return {"created": True, "html_url": data.get("html_url", f"{GITEA_URL}/{username}/{name}")}
    if code == 409:
        return {"created": False, "html_url": f"{GITEA_URL}/{username}/{name}"}
    if code == 403:
        raise GiteaError(
            "权限不足：当前 token 的账号不是 Gitea 站点管理员，"
            "无法为其他用户创建仓库。请在 Gitea 管理后台将该账号设为管理员。"
        )
    raise GiteaError(f"为用户 {username} 创建仓库失败 (HTTP {code}): {data}")


# ---------------------------------------------------------------- 文件操作

def get_file(owner: str, repo: str, path: str) -> tuple[str, str] | None:
    """读取仓库文件。返回 (内容字符串, sha)；文件不存在返回 None。"""
    code, data = _api("GET", f"/repos/{owner}/{repo}/contents/{path}")
    if code == 200 and data and data.get("content") is not None:
        content = base64.b64decode(data["content"]).decode("utf-8")
        return content, data["sha"]
    return None


def put_file(owner: str, repo: str, path: str, content: str,
             message: str, sha: str | None = None) -> int:
    """创建或更新文件。新建不传 sha，更新必须传 sha。返回 HTTP 状态码。"""
    body = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
    }
    if sha:
        body["sha"] = sha
        code, data = _api("PUT", f"/repos/{owner}/{repo}/contents/{path}", json_body=body)
    else:
        code, data = _api("POST", f"/repos/{owner}/{repo}/contents/{path}", json_body=body)
        if code == 422:
            # 文件其实已存在（并发或重复初始化），改走更新
            existing = get_file(owner, repo, path)
            if existing:
                return put_file(owner, repo, path, content, message, sha=existing[1])
    if code not in (200, 201):
        raise GiteaError(f"写入文件 {owner}/{repo}/{path} 失败 (HTTP {code}): {data}")
    return code


def ensure_file(owner: str, repo: str, path: str, content: str, message: str) -> bool:
    """文件不存在时创建；已存在则跳过（不覆盖）。返回是否新建。"""
    if get_file(owner, repo, path) is not None:
        return False
    put_file(owner, repo, path, content, message)
    return True


# ---------------------------------------------------------------- users.json

def ensure_system_repo() -> None:
    """确保 system-config 仓库和 users.json 存在（首次运行自举）。"""
    if not repo_exists(BOT_USERNAME, SYSTEM_REPO):
        create_own_repo(
            SYSTEM_REPO, private=True,
            description="paper-kb 系统配置：用户映射表",
        )
        # auto_init 后稍等仓库就绪
        time.sleep(1)
    if get_file(BOT_USERNAME, SYSTEM_REPO, USERS_FILE) is None:
        put_file(
            BOT_USERNAME, SYSTEM_REPO, USERS_FILE,
            json.dumps({}, ensure_ascii=False, indent=2),
            "init users.json",
        )


def read_users() -> dict:
    """读取用户映射表。system-config 不存在时返回空表（不自动创建）。"""
    result = get_file(BOT_USERNAME, SYSTEM_REPO, USERS_FILE)
    if result is None:
        return {}
    content, _ = result
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {}


def write_users(mutate_fn, max_retries: int = 3) -> dict:
    """读-改-写 users.json，带版本冲突重试。

    Args:
        mutate_fn: 接收当前 users dict，原地修改或返回新 dict。

    Returns:
        写入后的完整 users dict。
    """
    last_error: Exception | None = None
    for _ in range(max_retries):
        result = get_file(BOT_USERNAME, SYSTEM_REPO, USERS_FILE)
        if result is None:
            ensure_system_repo()
            result = get_file(BOT_USERNAME, SYSTEM_REPO, USERS_FILE)
            if result is None:
                raise GiteaError("无法读取 users.json，请检查 system-config 仓库")
        content, sha = result
        try:
            users = json.loads(content)
        except json.JSONDecodeError:
            users = {}
        returned = mutate_fn(users)
        if isinstance(returned, dict):
            users = returned
        try:
            put_file(
                BOT_USERNAME, SYSTEM_REPO, USERS_FILE,
                json.dumps(users, ensure_ascii=False, indent=2),
                "update users.json", sha=sha,
            )
            return users
        except GiteaError as exc:  # sha 冲突等，重读重试
            last_error = exc
            time.sleep(0.5)
    raise GiteaError(f"users.json 写入失败（重试{max_retries}次）: {last_error}")


# ---------------------------------------------------------------- 二进制文件

def put_file_bytes(owner: str, repo: str, path: str, raw: bytes,
                   message: str) -> int:
    """创建或更新二进制文件（如 PDF）。"""
    body = {
        "message": message,
        "content": base64.b64encode(raw).decode("ascii"),
    }
    existing = get_file_sha(owner, repo, path)
    if existing:
        body["sha"] = existing
        code, data = _api("PUT", f"/repos/{owner}/{repo}/contents/{path}", json_body=body)
    else:
        code, data = _api("POST", f"/repos/{owner}/{repo}/contents/{path}", json_body=body)
    if code not in (200, 201):
        raise GiteaError(f"写入二进制文件 {owner}/{repo}/{path} 失败 (HTTP {code}): {data}")
    return code


def get_file_sha(owner: str, repo: str, path: str) -> str | None:
    """只取文件 sha（不解码内容，适用于二进制大文件）。"""
    code, data = _api("GET", f"/repos/{owner}/{repo}/contents/{path}")
    if code == 200 and data:
        return data.get("sha")
    return None
