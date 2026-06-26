#!/usr/bin/env python3
"""
project-nerve 数据源连接器

管理 Trello、GitHub Issues、Linear、Notion、Obsidian 等平台的连接配置。
支持连接、测试、列表、断开操作。
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    write_json_file,
    SUPPORTED_PLATFORMS,
)


# ============================================================
# 数据文件路径
# ============================================================

SOURCES_FILE = "sources.json"


def _get_sources() -> List[Dict[str, Any]]:
    """读取所有已连接的数据源配置。"""
    data = read_json_file(get_data_file(SOURCES_FILE))
    if isinstance(data, list):
        return data
    return []


def _save_sources(sources: List[Dict[str, Any]]) -> None:
    """保存数据源配置到文件。"""
    write_json_file(get_data_file(SOURCES_FILE), sources)


def _find_source(sources: List[Dict], source_id: str) -> Optional[Dict]:
    """根据 ID 查找数据源。"""
    for s in sources:
        if s.get("id") == source_id:
            return s
    return None


def _find_source_by_platform(sources: List[Dict], platform: str) -> Optional[Dict]:
    """根据平台类型查找数据源。"""
    for s in sources:
        if s.get("platform") == platform:
            return s
    return None


# ============================================================
# HTTP 请求工具
# ============================================================

def _http_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    data: Optional[bytes] = None,
    timeout: int = 15,
) -> Dict[str, Any]:
    """发送 HTTP 请求。

    Args:
        url: 请求地址。
        method: HTTP 方法。
        headers: 请求头。
        data: 请求体。
        timeout: 超时秒数。

    Returns:
        包含 status、body、headers 的响应字典。
    """
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return {
                "status": resp.status,
                "body": body,
                "headers": dict(resp.headers),
            }
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")
        except Exception:
            pass
        return {
            "status": e.code,
            "body": body,
            "headers": {},
            "error": str(e),
        }
    except urllib.error.URLError as e:
        return {
            "status": 0,
            "body": "",
            "headers": {},
            "error": f"网络错误: {e.reason}",
        }
    except Exception as e:
        return {
            "status": 0,
            "body": "",
            "headers": {},
            "error": f"请求失败: {e}",
        }


# ============================================================
# 平台适配器 — 连接测试
# ============================================================

def _test_trello(config: Dict[str, Any]) -> Dict[str, Any]:
    """测试 Trello API 连接。

    需要 api_key 和 token。
    通过访问 /1/members/me 端点验证凭据。

    Args:
        config: 包含 api_key 和 token 的配置字典。

    Returns:
        测试结果字典，包含 success、message、user_info。
    """
    api_key = config.get("api_key") or os.environ.get("PNC_TRELLO_API_KEY", "")
    token = config.get("token") or os.environ.get("PNC_TRELLO_TOKEN", "")

    if not api_key or not token:
        return {"success": False, "message": "缺少 Trello API Key 或 Token，请设置 PNC_TRELLO_API_KEY 和 PNC_TRELLO_TOKEN 环境变量"}

    url = f"https://api.trello.com/1/members/me?key={api_key}&token={token}"
    resp = _http_request(url)

    if resp["status"] == 200:
        try:
            user = json.loads(resp["body"])
            return {
                "success": True,
                "message": f"Trello 连接成功，用户: {user.get('fullName', user.get('username', '未知'))}",
                "user_info": {"name": user.get("fullName", ""), "username": user.get("username", "")},
            }
        except json.JSONDecodeError:
            return {"success": True, "message": "Trello 连接成功"}
    else:
        return {"success": False, "message": f"Trello 连接失败 (HTTP {resp['status']}): {resp.get('error', resp['body'][:200])}"}


def _test_github(config: Dict[str, Any]) -> Dict[str, Any]:
    """测试 GitHub API 连接。

    需要 personal access token。
    通过访问 /user 端点验证凭据。

    Args:
        config: 包含 token 的配置字典。

    Returns:
        测试结果字典。
    """
    token = config.get("token") or os.environ.get("PNC_GITHUB_TOKEN", "")

    if not token:
        return {"success": False, "message": "缺少 GitHub Token，请设置 PNC_GITHUB_TOKEN 环境变量"}

    url = "https://api.github.com/user"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "project-nerve/1.0",
    }
    resp = _http_request(url, headers=headers)

    if resp["status"] == 200:
        try:
            user = json.loads(resp["body"])
            return {
                "success": True,
                "message": f"GitHub 连接成功，用户: {user.get('login', '未知')}",
                "user_info": {"login": user.get("login", ""), "name": user.get("name", "")},
            }
        except json.JSONDecodeError:
            return {"success": True, "message": "GitHub 连接成功"}
    else:
        return {"success": False, "message": f"GitHub 连接失败 (HTTP {resp['status']}): {resp.get('error', resp['body'][:200])}"}


def _test_linear(config: Dict[str, Any]) -> Dict[str, Any]:
    """测试 Linear API 连接。

    需要 API key。
    通过 GraphQL API 查询 viewer 验证凭据。

    Args:
        config: 包含 api_key 的配置字典。

    Returns:
        测试结果字典。
    """
    api_key = config.get("api_key") or os.environ.get("PNC_LINEAR_API_KEY", "")

    if not api_key:
        return {"success": False, "message": "缺少 Linear API Key，请设置 PNC_LINEAR_API_KEY 环境变量"}

    url = "https://api.linear.app/graphql"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }
    query = '{"query": "{ viewer { id name email } }"}'
    resp = _http_request(url, method="POST", headers=headers, data=query.encode("utf-8"))

    if resp["status"] == 200:
        try:
            result = json.loads(resp["body"])
            viewer = result.get("data", {}).get("viewer", {})
            name = viewer.get("name", "未知")
            return {
                "success": True,
                "message": f"Linear 连接成功，用户: {name}",
                "user_info": {"name": name, "email": viewer.get("email", "")},
            }
        except (json.JSONDecodeError, KeyError):
            return {"success": True, "message": "Linear 连接成功"}
    else:
        return {"success": False, "message": f"Linear 连接失败 (HTTP {resp['status']}): {resp.get('error', resp['body'][:200])}"}


def _test_obsidian(config: Dict[str, Any]) -> Dict[str, Any]:
    """测试 Obsidian Vault 可访问性。

    验证 vault 路径是否存在，并统计带有任务标签的笔记数量。

    Args:
        config: 包含 vault_path 和 task_tag 的配置字典。

    Returns:
        测试结果字典，包含 success、message、user_info。
    """
    vault_path = config.get("vault_path") or os.environ.get("PNC_OBSIDIAN_VAULT_PATH", "")
    task_tag = config.get("task_tag", "#task")

    if not vault_path:
        return {"success": False, "message": "缺少 Obsidian Vault 路径，请设置 PNC_OBSIDIAN_VAULT_PATH 环境变量或提供 vault_path"}

    vault_path = os.path.expanduser(vault_path)
    if not os.path.isdir(vault_path):
        return {"success": False, "message": f"Obsidian Vault 路径不存在: {vault_path}"}

    # 扫描 .md 文件，统计带任务标签的笔记数量
    task_note_count = 0
    total_md_count = 0
    for root, _dirs, files in os.walk(vault_path):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            total_md_count += 1
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read(4096)  # 只读取前 4KB 检查标签
                if task_tag in content or "- [ ]" in content or "- [x]" in content:
                    task_note_count += 1
            except (IOError, UnicodeDecodeError):
                continue

    return {
        "success": True,
        "message": f"Obsidian Vault 连接成功，共 {total_md_count} 个笔记，其中 {task_note_count} 个包含任务",
        "user_info": {
            "vault_path": vault_path,
            "total_notes": total_md_count,
            "task_notes": task_note_count,
            "task_tag": task_tag,
        },
    }


def _connect_obsidian(config: Dict[str, Any]) -> Dict[str, Any]:
    """验证 Obsidian Vault 配置。

    检查 vault 路径是否存在，扫描带有任务标签的笔记。

    Args:
        config: Obsidian 配置字典。

    Returns:
        包含 vault_path 和 task_tag 的已验证配置。
    """
    return _test_obsidian(config)


def _test_notion(config: Dict[str, Any]) -> Dict[str, Any]:
    """测试 Notion API 连接。

    需要 integration token 和 database_id。
    通过查询数据库验证凭据。

    Args:
        config: 包含 token 和 database_id 的配置字典。

    Returns:
        测试结果字典。
    """
    token = config.get("token") or os.environ.get("PNC_NOTION_TOKEN", "")
    database_id = config.get("database_id") or os.environ.get("PNC_NOTION_DATABASE_ID", "")

    if not token:
        return {"success": False, "message": "缺少 Notion Integration Token，请设置 PNC_NOTION_TOKEN 环境变量"}
    if not database_id:
        return {"success": False, "message": "缺少 Notion Database ID，请设置 PNC_NOTION_DATABASE_ID 环境变量"}

    url = f"https://api.notion.com/v1/databases/{database_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    resp = _http_request(url, headers=headers)

    if resp["status"] == 200:
        try:
            db = json.loads(resp["body"])
            title_parts = db.get("title", [])
            db_title = ""
            for part in title_parts:
                db_title += part.get("plain_text", "")
            return {
                "success": True,
                "message": f"Notion 连接成功，数据库: {db_title or database_id}",
                "user_info": {"database_title": db_title, "database_id": database_id},
            }
        except (json.JSONDecodeError, KeyError):
            return {"success": True, "message": "Notion 连接成功"}
    else:
        return {"success": False, "message": f"Notion 连接失败 (HTTP {resp['status']}): {resp.get('error', resp['body'][:200])}"}


# ============================================================
# 平台测试路由
# ============================================================

_PLATFORM_TESTERS = {
    "trello": _test_trello,
    "github": _test_github,
    "linear": _test_linear,
    "notion": _test_notion,
    "obsidian": _test_obsidian,
}


# ============================================================
# 操作实现
# ============================================================

def connect_source(data: Dict[str, Any]) -> None:
    """连接新数据源。

    必填字段: platform
    可选字段: name, api_key, token, database_id, repo（GitHub 仓库如 owner/repo）, board_id（Trello）

    Args:
        data: 数据源配置字典。
    """
    platform = data.get("platform", "").strip().lower()
    if platform not in SUPPORTED_PLATFORMS:
        valid = "、".join(SUPPORTED_PLATFORMS)
        output_error(f"不支持的平台: {platform!r}，支持的平台: {valid}", code="INVALID_PLATFORM")
        return

    # 检查订阅限制
    sub = check_subscription()
    sources = _get_sources()

    if len(sources) >= sub["max_sources"]:
        if sub["tier"] == "free":
            output_error(
                f"免费版最多连接 {sub['max_sources']} 个数据源，当前已有 {len(sources)} 个。"
                "请升级至付费版（¥99/月）以连接更多数据源。",
                code="LIMIT_EXCEEDED",
            )
        else:
            output_error(
                f"已达到数据源数量上限 {sub['max_sources']} 个。",
                code="LIMIT_EXCEEDED",
            )
        return

    # 检查是否已存在同平台连接
    existing = _find_source_by_platform(sources, platform)
    if existing:
        output_error(
            f"已存在 {platform} 平台的连接（ID: {existing['id']}）。如需重新连接，请先断开现有连接。",
            code="DUPLICATE_SOURCE",
        )
        return

    # 测试连接
    tester = _PLATFORM_TESTERS.get(platform)
    if tester:
        test_result = tester(data)
        if not test_result["success"]:
            output_error(test_result["message"], code="CONNECTION_FAILED")
            return

    # 保存配置
    now = now_iso()
    source_config = {
        "id": generate_id("SRC"),
        "platform": platform,
        "name": data.get("name", f"{platform} 数据源"),
        "config": {},
        "connected_at": now,
        "updated_at": now,
        "status": "active",
    }

    # 按平台保存不同的配置字段（不保存敏感凭据，使用环境变量）
    if platform == "trello":
        source_config["config"]["board_id"] = data.get("board_id", "")
        source_config["config"]["env_key"] = "PNC_TRELLO_API_KEY"
        source_config["config"]["env_token"] = "PNC_TRELLO_TOKEN"
    elif platform == "github":
        source_config["config"]["repo"] = data.get("repo", "")
        source_config["config"]["env_token"] = "PNC_GITHUB_TOKEN"
    elif platform == "linear":
        source_config["config"]["team_id"] = data.get("team_id", "")
        source_config["config"]["env_key"] = "PNC_LINEAR_API_KEY"
    elif platform == "notion":
        source_config["config"]["database_id"] = data.get("database_id") or os.environ.get("PNC_NOTION_DATABASE_ID", "")
        source_config["config"]["env_token"] = "PNC_NOTION_TOKEN"
    elif platform == "obsidian":
        vault_path = data.get("vault_path") or os.environ.get("PNC_OBSIDIAN_VAULT_PATH", "")
        source_config["config"]["vault_path"] = os.path.expanduser(vault_path)
        source_config["config"]["task_tag"] = data.get("task_tag", "#task")
        source_config["config"]["env_vault_path"] = "PNC_OBSIDIAN_VAULT_PATH"

    sources.append(source_config)
    _save_sources(sources)

    output_success({
        "message": f"{platform} 数据源已连接",
        "source": source_config,
    })


def test_source(data: Dict[str, Any]) -> None:
    """测试数据源连接。

    必填字段: platform 或 id

    Args:
        data: 包含平台或数据源 ID 的字典。
    """
    source_id = data.get("id")
    platform = data.get("platform", "").strip().lower()

    if source_id:
        sources = _get_sources()
        source = _find_source(sources, source_id)
        if not source:
            output_error(f"未找到 ID 为 {source_id} 的数据源", code="NOT_FOUND")
            return
        platform = source["platform"]

    if platform not in SUPPORTED_PLATFORMS:
        valid = "、".join(SUPPORTED_PLATFORMS)
        output_error(f"不支持的平台: {platform!r}，支持的平台: {valid}", code="INVALID_PLATFORM")
        return

    tester = _PLATFORM_TESTERS.get(platform)
    if not tester:
        output_error(f"平台 {platform} 暂不支持连接测试", code="NOT_SUPPORTED")
        return

    test_result = tester(data)
    if test_result["success"]:
        output_success({
            "platform": platform,
            "message": test_result["message"],
            "user_info": test_result.get("user_info", {}),
        })
    else:
        output_error(test_result["message"], code="CONNECTION_FAILED")


def list_sources(data: Optional[Dict[str, Any]] = None) -> None:
    """列出所有已连接的数据源。

    Args:
        data: 可选的过滤条件字典。
    """
    sources = _get_sources()

    if data:
        platform_filter = data.get("platform", "").strip().lower()
        if platform_filter:
            sources = [s for s in sources if s.get("platform") == platform_filter]

        status_filter = data.get("status", "").strip().lower()
        if status_filter:
            sources = [s for s in sources if s.get("status") == status_filter]

    # 构建摘要信息
    platform_stats = {}
    for p in SUPPORTED_PLATFORMS:
        count = sum(1 for s in sources if s.get("platform") == p)
        if count > 0:
            platform_stats[p] = count

    # 脱敏输出（不显示敏感配置）
    display_list = []
    for s in sources:
        display = {
            "id": s.get("id"),
            "platform": s.get("platform"),
            "name": s.get("name"),
            "status": s.get("status"),
            "connected_at": s.get("connected_at"),
            "updated_at": s.get("updated_at"),
        }
        display_list.append(display)

    output_success({
        "total": len(display_list),
        "platform_stats": platform_stats,
        "sources": display_list,
    })


def disconnect_source(data: Dict[str, Any]) -> None:
    """断开数据源连接。

    必填字段: id 或 platform

    Args:
        data: 包含数据源 ID 或平台名称的字典。
    """
    source_id = data.get("id")
    platform = data.get("platform", "").strip().lower()

    sources = _get_sources()
    original_count = len(sources)

    if source_id:
        sources = [s for s in sources if s.get("id") != source_id]
    elif platform:
        sources = [s for s in sources if s.get("platform") != platform]
    else:
        output_error("请提供数据源 ID（id）或平台名称（platform）", code="VALIDATION_ERROR")
        return

    if len(sources) == original_count:
        output_error("未找到匹配的数据源", code="NOT_FOUND")
        return

    removed_count = original_count - len(sources)
    _save_sources(sources)
    output_success({
        "message": f"已断开 {removed_count} 个数据源连接",
        "remaining": len(sources),
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("project-nerve 数据源连接器")
    args = parser.parse_args()

    action = args.action.lower().replace("-", "_")

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "connect": lambda: connect_source(data or {}),
        "test": lambda: test_source(data or {}),
        "list_sources": lambda: list_sources(data),
        "list": lambda: list_sources(data),
        "disconnect": lambda: disconnect_source(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(["connect", "test", "list-sources", "disconnect"])
        output_error(f"未知操作: {args.action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
