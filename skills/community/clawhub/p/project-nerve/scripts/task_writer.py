#!/usr/bin/env python3
"""
project-nerve 任务写入器

在指定平台上创建、更新、移动任务和添加评论。
支持自动检测最适合的平台（含 Obsidian），也可手动指定。
"""

import json
import os
import sys
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

from utils import (
    generate_id,
    get_data_file,
    load_input_data,
    normalize_priority,
    normalize_status,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    SUPPORTED_PLATFORMS,
)


# ============================================================
# 数据文件路径
# ============================================================

SOURCES_FILE = "sources.json"


def _get_sources() -> List[Dict[str, Any]]:
    """读取所有已连接的活跃数据源。"""
    data = read_json_file(get_data_file(SOURCES_FILE))
    if isinstance(data, list):
        return [s for s in data if s.get("status") == "active"]
    return []


def _find_source_by_platform(sources: List[Dict], platform: str) -> Optional[Dict]:
    """根据平台类型查找数据源配置。"""
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
    """发送 HTTP 请求并返回响应。

    Args:
        url: 请求地址。
        method: HTTP 方法。
        headers: 请求头。
        data: 请求体。
        timeout: 超时秒数。

    Returns:
        包含 status 和 body 的响应字典。
    """
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return {"status": resp.status, "body": body}
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")
        except Exception:
            pass
        return {"status": e.code, "body": body, "error": str(e)}
    except Exception as e:
        return {"status": 0, "body": "", "error": str(e)}


# ============================================================
# 平台自动检测
# ============================================================

# 关键词到平台的映射规则
_PLATFORM_KEYWORDS: Dict[str, List[str]] = {
    "github": ["bug", "fix", "pr", "pull request", "merge", "commit", "branch", "issue",
                "代码", "修复", "缺陷", "分支", "合并"],
    "obsidian": ["note", "notes", "wiki", "knowledge", "vault", "memo", "journal",
                  "笔记", "知识", "日记", "备忘", "本地"],
    "notion": ["doc", "document", "design", "page", "database",
                "文档", "设计", "数据库", "规划", "在线"],
    "linear": ["sprint", "story", "epic", "cycle", "roadmap", "feature",
                "迭代", "用户故事", "史诗", "路线图", "功能"],
    "trello": [],  # 默认平台
}


def _detect_platform(title: str, description: str = "") -> str:
    """根据任务标题和描述自动检测最适合的平台。

    匹配规则：
    - 代码/Bug/PR 相关 → GitHub
    - 文档/设计 相关 → Notion
    - Sprint/Story 相关 → Linear
    - 默认 → Trello

    Args:
        title: 任务标题。
        description: 任务描述。

    Returns:
        推荐的平台名称。
    """
    text = f"{title} {description}".lower()

    best_platform = "trello"
    best_score = 0

    for platform, keywords in _PLATFORM_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in text:
                score += 1
        if score > best_score:
            best_score = score
            best_platform = platform

    return best_platform


# ============================================================
# 平台适配器 — 创建任务
# ============================================================

def _create_trello_card(source: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
    """在 Trello 创建卡片。

    Args:
        source: 数据源配置。
        task_data: 任务数据（title, description, due_date 等）。

    Returns:
        创建结果字典。
    """
    api_key = os.environ.get("PNC_TRELLO_API_KEY", "")
    token = os.environ.get("PNC_TRELLO_TOKEN", "")
    board_id = source.get("config", {}).get("board_id", "")

    if not api_key or not token:
        return {"success": False, "message": "缺少 Trello 凭据"}

    # 获取第一个列表作为默认列表
    list_id = task_data.get("list_id", "")
    if not list_id and board_id:
        url = f"https://api.trello.com/1/boards/{board_id}/lists?key={api_key}&token={token}"
        resp = _http_request(url)
        if resp["status"] == 200:
            try:
                lists = json.loads(resp["body"])
                if lists:
                    list_id = lists[0]["id"]
            except (json.JSONDecodeError, KeyError, IndexError):
                pass

    if not list_id:
        return {"success": False, "message": "无法确定 Trello 列表，请指定 list_id 或 board_id"}

    # 创建卡片
    params = f"key={api_key}&token={token}"
    create_url = f"https://api.trello.com/1/cards?{params}"
    card_data = {
        "name": task_data.get("title", ""),
        "desc": task_data.get("description", ""),
        "idList": list_id,
    }
    if task_data.get("due_date"):
        card_data["due"] = task_data["due_date"]

    body = json.dumps(card_data).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    resp = _http_request(create_url, method="POST", headers=headers, data=body)

    if resp["status"] in (200, 201):
        try:
            card = json.loads(resp["body"])
            return {
                "success": True,
                "message": f"Trello 卡片已创建: {card.get('name', '')}",
                "task_id": card.get("id", ""),
                "url": card.get("shortUrl", ""),
            }
        except json.JSONDecodeError:
            return {"success": True, "message": "Trello 卡片已创建"}
    else:
        return {"success": False, "message": f"Trello 创建失败 (HTTP {resp['status']}): {resp.get('error', '')}"}


def _create_github_issue(source: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
    """在 GitHub 创建 Issue。

    Args:
        source: 数据源配置。
        task_data: 任务数据。

    Returns:
        创建结果字典。
    """
    token = os.environ.get("PNC_GITHUB_TOKEN", "")
    repo = source.get("config", {}).get("repo", "")

    if not token or not repo:
        return {"success": False, "message": "缺少 GitHub 凭据或仓库信息"}

    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "project-nerve/1.0",
    }

    issue_data = {
        "title": task_data.get("title", ""),
        "body": task_data.get("description", ""),
    }

    # 添加标签
    labels = task_data.get("labels", [])
    priority = task_data.get("priority", "")
    if priority:
        labels.append(f"priority:{priority}")
    if labels:
        issue_data["labels"] = labels

    # 添加负责人
    assignee = task_data.get("assignee", "")
    if assignee:
        issue_data["assignees"] = [assignee]

    body = json.dumps(issue_data).encode("utf-8")
    resp = _http_request(url, method="POST", headers=headers, data=body)

    if resp["status"] in (200, 201):
        try:
            issue = json.loads(resp["body"])
            return {
                "success": True,
                "message": f"GitHub Issue 已创建: #{issue.get('number', '')} {issue.get('title', '')}",
                "task_id": str(issue.get("number", "")),
                "url": issue.get("html_url", ""),
            }
        except json.JSONDecodeError:
            return {"success": True, "message": "GitHub Issue 已创建"}
    else:
        return {"success": False, "message": f"GitHub 创建失败 (HTTP {resp['status']}): {resp.get('error', '')}"}


def _create_linear_issue(source: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
    """在 Linear 创建 Issue。

    Args:
        source: 数据源配置。
        task_data: 任务数据。

    Returns:
        创建结果字典。
    """
    api_key = os.environ.get("PNC_LINEAR_API_KEY", "")

    if not api_key:
        return {"success": False, "message": "缺少 Linear API Key"}

    team_id = source.get("config", {}).get("team_id", "")
    if not team_id:
        return {"success": False, "message": "缺少 Linear Team ID，请在数据源配置中指定 team_id"}

    # Linear 优先级映射: 紧急=1, 高=2, 中=3, 低=4
    priority_map = {"紧急": 1, "高": 2, "中": 3, "低": 4}
    priority = priority_map.get(normalize_priority(task_data.get("priority", "")), 3)

    mutation = json.dumps({
        "query": """mutation CreateIssue($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                success
                issue {
                    id
                    identifier
                    title
                    url
                }
            }
        }""",
        "variables": {
            "input": {
                "teamId": team_id,
                "title": task_data.get("title", ""),
                "description": task_data.get("description", ""),
                "priority": priority,
            }
        }
    })

    url = "https://api.linear.app/graphql"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }
    resp = _http_request(url, method="POST", headers=headers, data=mutation.encode("utf-8"))

    if resp["status"] == 200:
        try:
            result = json.loads(resp["body"])
            issue_create = result.get("data", {}).get("issueCreate", {})
            if issue_create.get("success"):
                issue = issue_create.get("issue", {})
                return {
                    "success": True,
                    "message": f"Linear Issue 已创建: {issue.get('identifier', '')} {issue.get('title', '')}",
                    "task_id": issue.get("identifier", ""),
                    "url": issue.get("url", ""),
                }
            else:
                return {"success": False, "message": "Linear 创建失败: API 返回失败状态"}
        except (json.JSONDecodeError, KeyError):
            return {"success": False, "message": "Linear 创建失败: 响应解析错误"}
    else:
        return {"success": False, "message": f"Linear 创建失败 (HTTP {resp['status']}): {resp.get('error', '')}"}


def _create_notion_page(source: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
    """在 Notion 数据库创建页面。

    Args:
        source: 数据源配置。
        task_data: 任务数据。

    Returns:
        创建结果字典。
    """
    token = os.environ.get("PNC_NOTION_TOKEN", "")
    database_id = source.get("config", {}).get("database_id", "") or os.environ.get("PNC_NOTION_DATABASE_ID", "")

    if not token or not database_id:
        return {"success": False, "message": "缺少 Notion 凭据或数据库 ID"}

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    # 构建页面数据
    properties = {
        "Name": {
            "title": [
                {"text": {"content": task_data.get("title", "")}}
            ]
        }
    }

    page_data = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }

    # 添加内容块
    description = task_data.get("description", "")
    if description:
        page_data["children"] = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": description}}]
                }
            }
        ]

    body = json.dumps(page_data).encode("utf-8")
    resp = _http_request(url, method="POST", headers=headers, data=body)

    if resp["status"] in (200, 201):
        try:
            page = json.loads(resp["body"])
            return {
                "success": True,
                "message": f"Notion 页面已创建: {task_data.get('title', '')}",
                "task_id": page.get("id", ""),
                "url": page.get("url", ""),
            }
        except json.JSONDecodeError:
            return {"success": True, "message": "Notion 页面已创建"}
    else:
        return {"success": False, "message": f"Notion 创建失败 (HTTP {resp['status']}): {resp.get('error', '')}"}


def _create_obsidian_task(source: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
    """在 Obsidian Vault 中创建任务笔记。

    在 vault 中创建新的 markdown 文件，包含 frontmatter 元数据
    和 markdown 复选框格式的任务项。

    Args:
        source: 数据源配置。
        task_data: 任务数据（title, description, priority, due_date 等）。

    Returns:
        创建结果字典。
    """
    vault_path = source.get("config", {}).get("vault_path", "") or os.environ.get("PNC_OBSIDIAN_VAULT_PATH", "")
    task_tag = source.get("config", {}).get("task_tag", "#task")

    if not vault_path:
        return {"success": False, "message": "缺少 Obsidian Vault 路径"}

    vault_path = os.path.expanduser(vault_path)
    if not os.path.isdir(vault_path):
        return {"success": False, "message": f"Obsidian Vault 路径不存在: {vault_path}"}

    title = task_data.get("title", "未命名任务")
    description = task_data.get("description", "")
    priority = task_data.get("priority", "中")
    due_date = task_data.get("due_date", "")
    assignee = task_data.get("assignee", "")
    labels = task_data.get("labels", [])

    # 生成安全的文件名
    safe_title = title.replace("/", "_").replace("\\", "_").replace(":", "_")
    safe_title = safe_title.replace("\"", "").replace("*", "").replace("?", "")
    safe_title = safe_title.replace("<", "").replace(">", "").replace("|", "")
    if len(safe_title) > 100:
        safe_title = safe_title[:100]

    # 确保任务目录存在
    tasks_dir = os.path.join(vault_path, "tasks")
    os.makedirs(tasks_dir, exist_ok=True)

    # 生成文件路径（避免重名）
    filename = f"{safe_title}.md"
    filepath = os.path.join(tasks_dir, filename)
    counter = 1
    while os.path.exists(filepath):
        filename = f"{safe_title}_{counter}.md"
        filepath = os.path.join(tasks_dir, filename)
        counter += 1

    # 构建 frontmatter
    now = now_iso()
    fm_lines = ["---"]
    fm_lines.append(f"status: 待办")
    if priority:
        fm_lines.append(f"priority: {priority}")
    if assignee:
        fm_lines.append(f"assignee: {assignee}")
    if due_date:
        fm_lines.append(f"due_date: {due_date}")
    fm_lines.append(f"created: {now}")
    if labels:
        fm_lines.append(f"tags: [{', '.join(labels)}]")
    fm_lines.append("---")
    fm_lines.append("")

    # 构建笔记内容
    content_lines = list(fm_lines)
    content_lines.append(f"# {title}")
    content_lines.append("")
    content_lines.append(f"- [ ] {title} {task_tag}")
    content_lines.append("")

    if description:
        content_lines.append("## 描述")
        content_lines.append("")
        content_lines.append(description)
        content_lines.append("")

    if due_date:
        content_lines.append(f"📅 截止日期: {due_date}")
        content_lines.append("")

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(content_lines))

        rel_path = os.path.relpath(filepath, vault_path)
        vault_name = os.path.basename(vault_path)
        obsidian_url = f"obsidian://open?vault={vault_name}&file={rel_path}"

        return {
            "success": True,
            "message": f"Obsidian 任务笔记已创建: {title}",
            "task_id": rel_path,
            "url": obsidian_url,
        }
    except IOError as e:
        return {"success": False, "message": f"Obsidian 文件写入失败: {e}"}


# ============================================================
# 平台创建路由
# ============================================================

_PLATFORM_CREATORS = {
    "trello": _create_trello_card,
    "github": _create_github_issue,
    "linear": _create_linear_issue,
    "notion": _create_notion_page,
    "obsidian": _create_obsidian_task,
}


# ============================================================
# 操作实现
# ============================================================

def create_task(data: Dict[str, Any]) -> None:
    """创建任务。

    必填字段: title
    可选字段: platform, description, priority, assignee, labels, due_date

    若未指定 platform，将根据标题和描述自动检测最适合的平台。

    Args:
        data: 任务数据字典。
    """
    title = data.get("title", "").strip()
    if not title:
        output_error("任务标题（title）为必填字段", code="VALIDATION_ERROR")
        return

    sources = _get_sources()
    if not sources:
        output_error("暂无已连接的数据源，请先使用 source_connector 连接平台", code="NO_SOURCES")
        return

    # 确定目标平台
    platform = data.get("platform", "").strip().lower()
    if not platform:
        platform = _detect_platform(title, data.get("description", ""))

    # 检查平台是否已连接
    source = _find_source_by_platform(sources, platform)
    if not source:
        # 回退到第一个可用平台
        available = [s["platform"] for s in sources]
        if platform not in available:
            source = sources[0]
            platform = source["platform"]
        else:
            output_error(f"平台 {platform} 未连接", code="NOT_CONNECTED")
            return

    creator = _PLATFORM_CREATORS.get(platform)
    if not creator:
        output_error(f"平台 {platform} 暂不支持创建任务", code="NOT_SUPPORTED")
        return

    # 尝试导入自学习引擎（可选依赖）
    try:
        from learning_engine import quick_record_error, quick_record_success
        has_learning = True
    except ImportError:
        has_learning = False

    result = creator(source, data)
    if result["success"]:
        # 记录成功模式
        if has_learning:
            quick_record_success(platform, "create", data.get("title", ""))
        output_success({
            "message": result["message"],
            "platform": platform,
            "task_id": result.get("task_id", ""),
            "url": result.get("url", ""),
            "auto_detected": not data.get("platform"),
        })
    else:
        # 记录错误模式
        if has_learning:
            quick_record_error(platform, "create", "create_failure", result.get("message", ""))
        output_error(result["message"], code="CREATE_FAILED")


def update_task(data: Dict[str, Any]) -> None:
    """更新任务状态或属性。

    必填字段: source（平台）, source_id（平台任务ID）
    可选字段: status, priority, title, description

    Args:
        data: 包含平台和任务 ID 的更新数据字典。
    """
    platform = data.get("source", "").strip().lower()
    source_id = data.get("source_id", "").strip()

    if not platform or not source_id:
        output_error("平台（source）和任务 ID（source_id）为必填字段", code="VALIDATION_ERROR")
        return

    sources = _get_sources()
    source = _find_source_by_platform(sources, platform)
    if not source:
        output_error(f"平台 {platform} 未连接", code="NOT_CONNECTED")
        return

    # 根据平台执行更新
    if platform == "github":
        _update_github_issue(source, source_id, data)
    elif platform == "trello":
        _update_trello_card(source, source_id, data)
    elif platform == "linear":
        _update_linear_issue(source, source_id, data)
    elif platform == "notion":
        _update_notion_page(source, source_id, data)
    else:
        output_error(f"平台 {platform} 暂不支持更新操作", code="NOT_SUPPORTED")


def _update_github_issue(source: Dict, source_id: str, data: Dict) -> None:
    """更新 GitHub Issue。"""
    token = os.environ.get("PNC_GITHUB_TOKEN", "")
    repo = source.get("config", {}).get("repo", "")
    if not token or not repo:
        output_error("缺少 GitHub 凭据", code="AUTH_ERROR")
        return

    url = f"https://api.github.com/repos/{repo}/issues/{source_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "project-nerve/1.0",
    }

    update_data = {}
    if data.get("title"):
        update_data["title"] = data["title"]
    if data.get("description"):
        update_data["body"] = data["description"]
    if data.get("status"):
        status = normalize_status(data["status"])
        if status in ("已完成", "已关闭"):
            update_data["state"] = "closed"
        else:
            update_data["state"] = "open"

    if not update_data:
        output_error("未提供任何待更新的字段", code="VALIDATION_ERROR")
        return

    body = json.dumps(update_data).encode("utf-8")
    resp = _http_request(url, method="PATCH", headers=headers, data=body)

    if resp["status"] == 200:
        output_success({"message": f"GitHub Issue #{source_id} 已更新", "platform": "github"})
    else:
        output_error(f"GitHub 更新失败 (HTTP {resp['status']})", code="UPDATE_FAILED")


def _update_trello_card(source: Dict, source_id: str, data: Dict) -> None:
    """更新 Trello 卡片。"""
    api_key = os.environ.get("PNC_TRELLO_API_KEY", "")
    token = os.environ.get("PNC_TRELLO_TOKEN", "")
    if not api_key or not token:
        output_error("缺少 Trello 凭据", code="AUTH_ERROR")
        return

    params = f"key={api_key}&token={token}"
    url = f"https://api.trello.com/1/cards/{source_id}?{params}"

    update_data = {}
    if data.get("title"):
        update_data["name"] = data["title"]
    if data.get("description"):
        update_data["desc"] = data["description"]
    if data.get("due_date"):
        update_data["due"] = data["due_date"]

    if not update_data:
        output_error("未提供任何待更新的字段", code="VALIDATION_ERROR")
        return

    body = json.dumps(update_data).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    resp = _http_request(url, method="PUT", headers=headers, data=body)

    if resp["status"] == 200:
        output_success({"message": f"Trello 卡片 {source_id} 已更新", "platform": "trello"})
    else:
        output_error(f"Trello 更新失败 (HTTP {resp['status']})", code="UPDATE_FAILED")


def _update_linear_issue(source: Dict, source_id: str, data: Dict) -> None:
    """更新 Linear Issue。"""
    api_key = os.environ.get("PNC_LINEAR_API_KEY", "")
    if not api_key:
        output_error("缺少 Linear API Key", code="AUTH_ERROR")
        return

    input_data = {}
    if data.get("title"):
        input_data["title"] = data["title"]
    if data.get("description"):
        input_data["description"] = data["description"]
    if data.get("priority"):
        priority_map = {"紧急": 1, "高": 2, "中": 3, "低": 4}
        input_data["priority"] = priority_map.get(normalize_priority(data["priority"]), 3)

    if not input_data:
        output_error("未提供任何待更新的字段", code="VALIDATION_ERROR")
        return

    mutation = json.dumps({
        "query": """mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
            issueUpdate(id: $id, input: $input) {
                success
            }
        }""",
        "variables": {"id": source_id, "input": input_data}
    })

    url = "https://api.linear.app/graphql"
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    resp = _http_request(url, method="POST", headers=headers, data=mutation.encode("utf-8"))

    if resp["status"] == 200:
        output_success({"message": f"Linear Issue {source_id} 已更新", "platform": "linear"})
    else:
        output_error(f"Linear 更新失败 (HTTP {resp['status']})", code="UPDATE_FAILED")


def _update_notion_page(source: Dict, source_id: str, data: Dict) -> None:
    """更新 Notion 页面属性。"""
    token = os.environ.get("PNC_NOTION_TOKEN", "")
    if not token:
        output_error("缺少 Notion Token", code="AUTH_ERROR")
        return

    url = f"https://api.notion.com/v1/pages/{source_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    properties = {}
    if data.get("title"):
        properties["Name"] = {"title": [{"text": {"content": data["title"]}}]}

    if not properties:
        output_error("未提供任何待更新的字段", code="VALIDATION_ERROR")
        return

    body = json.dumps({"properties": properties}).encode("utf-8")
    resp = _http_request(url, method="PATCH", headers=headers, data=body)

    if resp["status"] == 200:
        output_success({"message": f"Notion 页面 {source_id[:8]}... 已更新", "platform": "notion"})
    else:
        output_error(f"Notion 更新失败 (HTTP {resp['status']})", code="UPDATE_FAILED")


def move_task(data: Dict[str, Any]) -> None:
    """移动任务状态（等同于 update + status）。

    必填字段: source, source_id, status

    Args:
        data: 包含平台、任务 ID 和目标状态的字典。
    """
    if not data.get("status"):
        output_error("目标状态（status）为必填字段", code="VALIDATION_ERROR")
        return

    update_task(data)


def comment_task(data: Dict[str, Any]) -> None:
    """给任务添加评论。

    必填字段: source, source_id, comment

    Args:
        data: 包含平台、任务 ID 和评论内容的字典。
    """
    platform = data.get("source", "").strip().lower()
    source_id = data.get("source_id", "").strip()
    comment = data.get("comment", "").strip()

    if not platform or not source_id or not comment:
        output_error("平台（source）、任务 ID（source_id）和评论内容（comment）为必填字段", code="VALIDATION_ERROR")
        return

    sources = _get_sources()
    source = _find_source_by_platform(sources, platform)
    if not source:
        output_error(f"平台 {platform} 未连接", code="NOT_CONNECTED")
        return

    if platform == "github":
        _comment_github_issue(source, source_id, comment)
    elif platform == "trello":
        _comment_trello_card(source, source_id, comment)
    elif platform == "linear":
        _comment_linear_issue(source, source_id, comment)
    elif platform == "notion":
        _comment_notion_page(source, source_id, comment)
    else:
        output_error(f"平台 {platform} 暂不支持评论功能", code="NOT_SUPPORTED")


def _comment_github_issue(source: Dict, source_id: str, comment: str) -> None:
    """给 GitHub Issue 添加评论。"""
    token = os.environ.get("PNC_GITHUB_TOKEN", "")
    repo = source.get("config", {}).get("repo", "")
    if not token or not repo:
        output_error("缺少 GitHub 凭据", code="AUTH_ERROR")
        return

    url = f"https://api.github.com/repos/{repo}/issues/{source_id}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "project-nerve/1.0",
    }
    body = json.dumps({"body": comment}).encode("utf-8")
    resp = _http_request(url, method="POST", headers=headers, data=body)

    if resp["status"] in (200, 201):
        output_success({"message": f"已在 GitHub Issue #{source_id} 添加评论", "platform": "github"})
    else:
        output_error(f"GitHub 评论失败 (HTTP {resp['status']})", code="COMMENT_FAILED")


def _comment_trello_card(source: Dict, source_id: str, comment: str) -> None:
    """给 Trello 卡片添加评论。"""
    api_key = os.environ.get("PNC_TRELLO_API_KEY", "")
    token = os.environ.get("PNC_TRELLO_TOKEN", "")
    if not api_key or not token:
        output_error("缺少 Trello 凭据", code="AUTH_ERROR")
        return

    params = f"key={api_key}&token={token}&text={urllib.request.quote(comment)}"
    url = f"https://api.trello.com/1/cards/{source_id}/actions/comments?{params}"
    resp = _http_request(url, method="POST")

    if resp["status"] in (200, 201):
        output_success({"message": f"已在 Trello 卡片 {source_id} 添加评论", "platform": "trello"})
    else:
        output_error(f"Trello 评论失败 (HTTP {resp['status']})", code="COMMENT_FAILED")


def _comment_linear_issue(source: Dict, source_id: str, comment: str) -> None:
    """给 Linear Issue 添加评论。"""
    api_key = os.environ.get("PNC_LINEAR_API_KEY", "")
    if not api_key:
        output_error("缺少 Linear API Key", code="AUTH_ERROR")
        return

    mutation = json.dumps({
        "query": """mutation CreateComment($input: CommentCreateInput!) {
            commentCreate(input: $input) {
                success
            }
        }""",
        "variables": {"input": {"issueId": source_id, "body": comment}}
    })

    url = "https://api.linear.app/graphql"
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    resp = _http_request(url, method="POST", headers=headers, data=mutation.encode("utf-8"))

    if resp["status"] == 200:
        output_success({"message": f"已在 Linear Issue {source_id} 添加评论", "platform": "linear"})
    else:
        output_error(f"Linear 评论失败 (HTTP {resp['status']})", code="COMMENT_FAILED")


def _comment_notion_page(source: Dict, source_id: str, comment: str) -> None:
    """在 Notion 页面添加评论（作为子块追加）。"""
    token = os.environ.get("PNC_NOTION_TOKEN", "")
    if not token:
        output_error("缺少 Notion Token", code="AUTH_ERROR")
        return

    url = f"https://api.notion.com/v1/blocks/{source_id}/children"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    body = json.dumps({
        "children": [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": f"[评论] {comment}"}}]
            }
        }]
    }).encode("utf-8")
    resp = _http_request(url, method="PATCH", headers=headers, data=body)

    if resp["status"] == 200:
        output_success({"message": f"已在 Notion 页面 {source_id[:8]}... 添加评论", "platform": "notion"})
    else:
        output_error(f"Notion 评论失败 (HTTP {resp['status']})", code="COMMENT_FAILED")


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("project-nerve 任务写入器")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "create": lambda: create_task(data or {}),
        "update": lambda: update_task(data or {}),
        "move": lambda: move_task(data or {}),
        "comment": lambda: comment_task(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
