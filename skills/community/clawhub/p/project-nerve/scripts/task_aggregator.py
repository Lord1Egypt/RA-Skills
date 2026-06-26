#!/usr/bin/env python3
"""
project-nerve 任务聚合器

从所有已连接的平台获取任务数据，统一格式化后提供搜索、阻碍分析和优先级排序功能。
支持 Trello、GitHub Issues、Linear、Notion、Obsidian 五个平台。
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    format_task_table,
    get_data_file,
    is_overdue,
    load_input_data,
    normalize_priority,
    normalize_status,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    parse_date,
    read_json_file,
    write_json_file,
    SUPPORTED_PLATFORMS,
)


# ============================================================
# 数据文件路径
# ============================================================

SOURCES_FILE = "sources.json"
TASKS_CACHE_FILE = "tasks_cache.json"


def _get_sources() -> List[Dict[str, Any]]:
    """读取所有已连接的活跃数据源。"""
    data = read_json_file(get_data_file(SOURCES_FILE))
    if isinstance(data, list):
        return [s for s in data if s.get("status") == "active"]
    return []


def _get_cached_tasks() -> List[Dict[str, Any]]:
    """读取缓存的任务数据。"""
    data = read_json_file(get_data_file(TASKS_CACHE_FILE))
    if isinstance(data, list):
        return data
    return []


def _save_cached_tasks(tasks: List[Dict[str, Any]]) -> None:
    """保存任务数据到缓存文件。"""
    write_json_file(get_data_file(TASKS_CACHE_FILE), tasks)


# ============================================================
# HTTP 请求工具
# ============================================================

def _http_get(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 15) -> Dict[str, Any]:
    """发送 HTTP GET 请求。

    Args:
        url: 请求地址。
        headers: 请求头。
        timeout: 超时秒数。

    Returns:
        包含 status 和 body 的响应字典。
    """
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, headers=headers, method="GET")
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


def _http_post(url: str, headers: Optional[Dict[str, str]] = None,
               data: Optional[bytes] = None, timeout: int = 15) -> Dict[str, Any]:
    """发送 HTTP POST 请求。"""
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
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
# 平台适配器 — 任务获取
# ============================================================

def _fetch_trello_tasks(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从 Trello 获取卡片并转换为统一格式。

    Args:
        source: 数据源配置。

    Returns:
        统一格式的任务列表。
    """
    api_key = os.environ.get("PNC_TRELLO_API_KEY", "")
    token = os.environ.get("PNC_TRELLO_TOKEN", "")
    board_id = source.get("config", {}).get("board_id", "")

    if not api_key or not token:
        return []

    tasks = []

    # 获取看板列表（用于映射状态）
    lists_map = {}
    if board_id:
        url = f"https://api.trello.com/1/boards/{board_id}/lists?key={api_key}&token={token}"
        resp = _http_get(url)
        if resp["status"] == 200:
            try:
                for lst in json.loads(resp["body"]):
                    lists_map[lst["id"]] = lst.get("name", "")
            except (json.JSONDecodeError, KeyError):
                pass

    # 获取卡片
    if board_id:
        url = f"https://api.trello.com/1/boards/{board_id}/cards?key={api_key}&token={token}&fields=name,desc,idList,labels,due,dateLastActivity,shortUrl,idMembers"
        resp = _http_get(url)
        if resp["status"] == 200:
            try:
                cards = json.loads(resp["body"])
                for card in cards:
                    list_name = lists_map.get(card.get("idList", ""), "")
                    labels = [lb.get("name", "") for lb in card.get("labels", []) if lb.get("name")]
                    # 从标签推断优先级
                    priority_str = ""
                    for lb in labels:
                        if lb.lower() in ("urgent", "high", "medium", "low", "紧急", "高", "中", "低"):
                            priority_str = lb
                            break

                    tasks.append({
                        "id": f"trello-{card.get('id', '')}",
                        "source": "trello",
                        "source_id": card.get("id", ""),
                        "title": card.get("name", ""),
                        "description": card.get("desc", ""),
                        "status": normalize_status(list_name),
                        "priority": normalize_priority(priority_str),
                        "assignee": "",
                        "labels": labels,
                        "due_date": (card.get("due") or "")[:10] if card.get("due") else "",
                        "created_at": card.get("dateLastActivity", ""),
                        "updated_at": card.get("dateLastActivity", ""),
                        "url": card.get("shortUrl", ""),
                    })
            except (json.JSONDecodeError, KeyError):
                pass

    return tasks


def _fetch_github_issues(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从 GitHub 获取 Issues 并转换为统一格式。

    Args:
        source: 数据源配置。

    Returns:
        统一格式的任务列表。
    """
    token = os.environ.get("PNC_GITHUB_TOKEN", "")
    repo = source.get("config", {}).get("repo", "")

    if not token or not repo:
        return []

    tasks = []
    url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&sort=updated&direction=desc"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "project-nerve/1.0",
    }
    resp = _http_get(url, headers=headers)

    if resp["status"] == 200:
        try:
            issues = json.loads(resp["body"])
            for issue in issues:
                # 跳过 Pull Request（GitHub Issues API 也会返回 PR）
                if issue.get("pull_request"):
                    continue

                labels = [lb.get("name", "") for lb in issue.get("labels", []) if lb.get("name")]
                # 从标签推断优先级
                priority_str = ""
                for lb in labels:
                    lb_lower = lb.lower()
                    if lb_lower in ("urgent", "high", "medium", "low", "p0", "p1", "p2", "p3", "critical", "blocker"):
                        priority_str = lb
                        break

                state = issue.get("state", "open")
                assignee = ""
                if issue.get("assignee"):
                    assignee = issue["assignee"].get("login", "")

                tasks.append({
                    "id": f"github-{issue.get('id', '')}",
                    "source": "github",
                    "source_id": str(issue.get("number", "")),
                    "title": issue.get("title", ""),
                    "description": (issue.get("body") or "")[:500],
                    "status": normalize_status(state),
                    "priority": normalize_priority(priority_str),
                    "assignee": assignee,
                    "labels": labels,
                    "due_date": "",
                    "created_at": issue.get("created_at", ""),
                    "updated_at": issue.get("updated_at", ""),
                    "url": issue.get("html_url", ""),
                })
        except (json.JSONDecodeError, KeyError):
            pass

    return tasks


def _fetch_linear_issues(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从 Linear 获取 Issues 并转换为统一格式。

    Args:
        source: 数据源配置。

    Returns:
        统一格式的任务列表。
    """
    api_key = os.environ.get("PNC_LINEAR_API_KEY", "")

    if not api_key:
        return []

    tasks = []
    team_id = source.get("config", {}).get("team_id", "")

    # 构建 GraphQL 查询
    team_filter = ""
    if team_id:
        team_filter = f', filter: {{ team: {{ id: {{ eq: "{team_id}" }} }} }}'

    query_str = json.dumps({
        "query": f"""{{
            issues(first: 100, orderBy: updatedAt{team_filter}) {{
                nodes {{
                    id
                    identifier
                    title
                    description
                    priority
                    state {{ name }}
                    assignee {{ name }}
                    labels {{ nodes {{ name }} }}
                    dueDate
                    createdAt
                    updatedAt
                    url
                }}
            }}
        }}"""
    })

    url = "https://api.linear.app/graphql"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }
    resp = _http_post(url, headers=headers, data=query_str.encode("utf-8"))

    if resp["status"] == 200:
        try:
            result = json.loads(resp["body"])
            issues = result.get("data", {}).get("issues", {}).get("nodes", [])

            # Linear 优先级数值映射: 0=无, 1=紧急, 2=高, 3=中, 4=低
            linear_priority_map = {0: "低", 1: "紧急", 2: "高", 3: "中", 4: "低"}

            for issue in issues:
                priority_num = issue.get("priority", 0)
                state_name = ""
                if issue.get("state"):
                    state_name = issue["state"].get("name", "")
                assignee_name = ""
                if issue.get("assignee"):
                    assignee_name = issue["assignee"].get("name", "")
                labels = []
                if issue.get("labels") and issue["labels"].get("nodes"):
                    labels = [lb.get("name", "") for lb in issue["labels"]["nodes"] if lb.get("name")]

                tasks.append({
                    "id": f"linear-{issue.get('id', '')}",
                    "source": "linear",
                    "source_id": issue.get("identifier", ""),
                    "title": issue.get("title", ""),
                    "description": (issue.get("description") or "")[:500],
                    "status": normalize_status(state_name),
                    "priority": linear_priority_map.get(priority_num, "中"),
                    "assignee": assignee_name,
                    "labels": labels,
                    "due_date": (issue.get("dueDate") or "")[:10],
                    "created_at": issue.get("createdAt", ""),
                    "updated_at": issue.get("updatedAt", ""),
                    "url": issue.get("url", ""),
                })
        except (json.JSONDecodeError, KeyError):
            pass

    return tasks


def _fetch_notion_tasks(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从 Notion 数据库获取页面并转换为统一格式。

    Args:
        source: 数据源配置。

    Returns:
        统一格式的任务列表。
    """
    token = os.environ.get("PNC_NOTION_TOKEN", "")
    database_id = source.get("config", {}).get("database_id", "") or os.environ.get("PNC_NOTION_DATABASE_ID", "")

    if not token or not database_id:
        return []

    tasks = []
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    body = json.dumps({"page_size": 100}).encode("utf-8")
    resp = _http_post(url, headers=headers, data=body)

    if resp["status"] == 200:
        try:
            result = json.loads(resp["body"])
            pages = result.get("results", [])

            for page in pages:
                props = page.get("properties", {})

                # 提取标题（尝试常见属性名）
                title = ""
                for key in ("Name", "名称", "Title", "标题", "Task", "任务"):
                    prop = props.get(key, {})
                    if prop.get("type") == "title":
                        title_parts = prop.get("title", [])
                        title = "".join(p.get("plain_text", "") for p in title_parts)
                        break

                # 提取状态
                status_str = ""
                for key in ("Status", "状态", "Stage", "阶段"):
                    prop = props.get(key, {})
                    if prop.get("type") == "status":
                        status_obj = prop.get("status")
                        if status_obj:
                            status_str = status_obj.get("name", "")
                        break
                    elif prop.get("type") == "select":
                        select_obj = prop.get("select")
                        if select_obj:
                            status_str = select_obj.get("name", "")
                        break

                # 提取优先级
                priority_str = ""
                for key in ("Priority", "优先级"):
                    prop = props.get(key, {})
                    if prop.get("type") == "select":
                        select_obj = prop.get("select")
                        if select_obj:
                            priority_str = select_obj.get("name", "")
                        break

                # 提取负责人
                assignee = ""
                for key in ("Assignee", "负责人", "Owner"):
                    prop = props.get(key, {})
                    if prop.get("type") == "people":
                        people = prop.get("people", [])
                        if people:
                            assignee = people[0].get("name", "")
                        break

                # 提取截止日期
                due_date = ""
                for key in ("Due", "截止日期", "Due Date", "Deadline"):
                    prop = props.get(key, {})
                    if prop.get("type") == "date":
                        date_obj = prop.get("date")
                        if date_obj:
                            due_date = (date_obj.get("start") or "")[:10]
                        break

                # 提取标签
                labels = []
                for key in ("Tags", "标签", "Labels"):
                    prop = props.get(key, {})
                    if prop.get("type") == "multi_select":
                        for opt in prop.get("multi_select", []):
                            labels.append(opt.get("name", ""))
                        break

                page_url = page.get("url", "")
                created_time = page.get("created_time", "")
                updated_time = page.get("last_edited_time", "")

                tasks.append({
                    "id": f"notion-{page.get('id', '')}",
                    "source": "notion",
                    "source_id": page.get("id", ""),
                    "title": title,
                    "description": "",
                    "status": normalize_status(status_str),
                    "priority": normalize_priority(priority_str),
                    "assignee": assignee,
                    "labels": labels,
                    "due_date": due_date,
                    "created_at": created_time,
                    "updated_at": updated_time,
                    "url": page_url,
                })
        except (json.JSONDecodeError, KeyError):
            pass

    return tasks


def _parse_obsidian_frontmatter(content: str) -> Dict[str, str]:
    """解析 Obsidian 笔记的 YAML frontmatter。

    提取 frontmatter 中的 status、priority、assignee、due_date 字段。

    Args:
        content: 笔记完整文本内容。

    Returns:
        包含解析到的字段的字典。
    """
    result: Dict[str, str] = {}
    if not content.startswith("---"):
        return result

    parts = content.split("---", 2)
    if len(parts) < 3:
        return result

    frontmatter = parts[1]
    for line in frontmatter.strip().split("\n"):
        line = line.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip().strip('"').strip("'")
        if key in ("status", "priority", "assignee", "due_date", "due"):
            mapped_key = "due_date" if key == "due" else key
            result[mapped_key] = value

    return result


def _fetch_obsidian_tasks(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从 Obsidian Vault 扫描任务。

    扫描 vault 中所有 .md 文件，提取 markdown 复选框格式的任务：
    - [ ] 未完成任务
    - [x] 已完成任务

    同时解析 frontmatter 中的 priority、assignee、due_date 等字段。

    Args:
        source: 数据源配置。

    Returns:
        统一格式的任务列表。
    """
    vault_path = source.get("config", {}).get("vault_path", "") or os.environ.get("PNC_OBSIDIAN_VAULT_PATH", "")
    task_tag = source.get("config", {}).get("task_tag", "#task")

    if not vault_path:
        return []

    vault_path = os.path.expanduser(vault_path)
    if not os.path.isdir(vault_path):
        return []

    tasks = []
    # 用于生成唯一 ID 的计数器
    task_counter = 0

    for root, _dirs, files in os.walk(vault_path):
        # 跳过 .obsidian 配置目录
        if ".obsidian" in root:
            continue

        for fname in files:
            if not fname.endswith(".md"):
                continue

            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
            except (IOError, UnicodeDecodeError):
                continue

            # 解析 frontmatter 获取全局属性
            fm = _parse_obsidian_frontmatter(content)

            # 计算相对路径（作为来源标识）
            rel_path = os.path.relpath(fpath, vault_path)
            note_title = os.path.splitext(fname)[0]

            # 获取文件修改时间
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%dT%H:%M:%S")
            except (OSError, ValueError):
                mtime = ""

            # 扫描 markdown 复选框
            checkbox_pattern = re.compile(r"^(\s*)-\s+\[([ xX])\]\s+(.+)$", re.MULTILINE)
            for match in checkbox_pattern.finditer(content):
                checked = match.group(2).lower() == "x"
                task_text = match.group(3).strip()

                # 跳过空任务
                if not task_text:
                    continue

                task_counter += 1
                task_id = f"obsidian-{task_counter}-{hash(fpath + task_text) & 0xFFFFFFFF:08x}"

                # 从任务文本中提取内联标签
                labels = re.findall(r"#(\w+)", task_text)
                # 移除标签后的纯文本作为标题
                clean_title = re.sub(r"\s*#\w+", "", task_text).strip()
                if not clean_title:
                    clean_title = task_text

                # 尝试从任务文本中提取截止日期（如 📅 2026-03-20 或 due:2026-03-20）
                due_date = fm.get("due_date", "")
                due_match = re.search(r"(?:📅|due:|截止:?)\s*(\d{4}-\d{2}-\d{2})", task_text)
                if due_match:
                    due_date = due_match.group(1)

                tasks.append({
                    "id": task_id,
                    "source": "obsidian",
                    "source_id": rel_path,
                    "title": clean_title,
                    "description": f"来自笔记: {note_title}",
                    "status": "已完成" if checked else normalize_status(fm.get("status", "待办")),
                    "priority": normalize_priority(fm.get("priority", "")),
                    "assignee": fm.get("assignee", ""),
                    "labels": labels,
                    "due_date": due_date,
                    "created_at": mtime,
                    "updated_at": mtime,
                    "url": f"obsidian://open?vault={os.path.basename(vault_path)}&file={rel_path}",
                })

    return tasks


# ============================================================
# 平台获取路由
# ============================================================

_PLATFORM_FETCHERS = {
    "trello": _fetch_trello_tasks,
    "github": _fetch_github_issues,
    "linear": _fetch_linear_issues,
    "notion": _fetch_notion_tasks,
    "obsidian": _fetch_obsidian_tasks,
}


# ============================================================
# 去重逻辑
# ============================================================

def _word_set(text: str) -> set:
    """提取文本中的词集合（中文按字，英文按单词）。

    Args:
        text: 输入文本。

    Returns:
        词集合。
    """
    if not text:
        return set()
    # 提取英文单词和中文字符
    words = set(re.findall(r"[a-zA-Z0-9]+", text.lower()))
    # 添加中文字符
    for ch in text:
        if "\u4e00" <= ch <= "\u9fff":
            words.add(ch)
    return words


def _title_similarity(t1: str, t2: str) -> float:
    """计算两个标题的相似度（基于词重叠比率）。

    Args:
        t1: 标题一。
        t2: 标题二。

    Returns:
        相似度 0.0~1.0。
    """
    s1 = _word_set(t1)
    s2 = _word_set(t2)
    if not s1 or not s2:
        return 0.0
    intersection = s1 & s2
    union = s1 | s2
    return len(intersection) / len(union) if union else 0.0


def _dedup_tasks(tasks: List[Dict[str, Any]], threshold: float = 0.8) -> List[Dict[str, Any]]:
    """对任务列表去重（基于标题相似度）。

    当两个来自不同平台的任务标题相似度超过阈值时，保留更新时间较晚的那个。

    Args:
        tasks: 原始任务列表。
        threshold: 相似度阈值。

    Returns:
        去重后的任务列表。
    """
    if not tasks:
        return tasks

    result = []
    seen_indices = set()

    for i in range(len(tasks)):
        if i in seen_indices:
            continue

        best = tasks[i]
        for j in range(i + 1, len(tasks)):
            if j in seen_indices:
                continue

            # 只对不同平台的任务做去重
            if tasks[i]["source"] == tasks[j]["source"]:
                continue

            sim = _title_similarity(tasks[i]["title"], tasks[j]["title"])
            if sim >= threshold:
                seen_indices.add(j)
                # 保留更新时间较晚的
                if tasks[j].get("updated_at", "") > best.get("updated_at", ""):
                    best = tasks[j]

        result.append(best)

    return result


# ============================================================
# 操作实现
# ============================================================

def fetch_all(data: Optional[Dict[str, Any]] = None) -> None:
    """从所有已连接平台获取任务并缓存。

    Args:
        data: 可选参数（platform 过滤）。
    """
    sources = _get_sources()
    if not sources:
        output_error("暂无已连接的数据源，请先使用 source_connector 连接平台", code="NO_SOURCES")
        return

    platform_filter = ""
    if data:
        platform_filter = data.get("platform", "").strip().lower()

    all_tasks = []
    fetch_errors = []

    # 尝试导入自学习引擎（可选依赖）
    try:
        from learning_engine import quick_record_error, quick_record_success
        has_learning = True
    except ImportError:
        has_learning = False

    for source in sources:
        platform = source.get("platform", "")
        if platform_filter and platform != platform_filter:
            continue

        fetcher = _PLATFORM_FETCHERS.get(platform)
        if not fetcher:
            fetch_errors.append(f"平台 {platform} 暂不支持")
            continue

        try:
            tasks = fetcher(source)
            all_tasks.extend(tasks)
            # 记录成功
            if has_learning and tasks:
                quick_record_success(platform, "fetch", f"获取到 {len(tasks)} 个任务")
        except Exception as e:
            fetch_errors.append(f"{platform} 获取失败: {e}")
            # 记录错误
            if has_learning:
                quick_record_error(platform, "fetch", "fetch_failure", str(e))

    # 去重
    all_tasks = _dedup_tasks(all_tasks)

    # 按更新时间倒序排列
    all_tasks.sort(key=lambda t: t.get("updated_at", ""), reverse=True)

    # 检查显示限制
    sub = check_subscription()
    display_limit = sub["max_tasks_display"]
    truncated = len(all_tasks) > display_limit
    display_tasks = all_tasks[:display_limit]

    # 缓存所有任务
    _save_cached_tasks(all_tasks)

    # 统计
    status_stats = {}
    for task in all_tasks:
        status = task.get("status", "待办")
        status_stats[status] = status_stats.get(status, 0) + 1

    source_stats = {}
    for task in all_tasks:
        src = task.get("source", "未知")
        source_stats[src] = source_stats.get(src, 0) + 1

    result = {
        "total": len(all_tasks),
        "displayed": len(display_tasks),
        "truncated": truncated,
        "status_stats": status_stats,
        "source_stats": source_stats,
        "tasks": display_tasks,
        "table": format_task_table(display_tasks),
    }

    if fetch_errors:
        result["warnings"] = fetch_errors

    output_success(result)


def search_tasks(data: Dict[str, Any]) -> None:
    """在缓存的任务中搜索。

    搜索字段: keyword（标题/描述）、status、priority、source、assignee

    Args:
        data: 搜索条件字典。
    """
    tasks = _get_cached_tasks()
    if not tasks:
        output_error("暂无缓存任务数据，请先执行 fetch-all 获取任务", code="NO_DATA")
        return

    keyword = data.get("keyword", "").strip().lower()
    status_filter = data.get("status", "").strip()
    priority_filter = data.get("priority", "").strip()
    source_filter = data.get("source", "").strip().lower()
    assignee_filter = data.get("assignee", "").strip().lower()

    filtered = tasks

    if keyword:
        filtered = [
            t for t in filtered
            if keyword in t.get("title", "").lower()
            or keyword in t.get("description", "").lower()
            or keyword in " ".join(t.get("labels", [])).lower()
        ]

    if status_filter:
        normalized = normalize_status(status_filter)
        filtered = [t for t in filtered if t.get("status") == normalized]

    if priority_filter:
        normalized = normalize_priority(priority_filter)
        filtered = [t for t in filtered if t.get("priority") == normalized]

    if source_filter:
        filtered = [t for t in filtered if t.get("source") == source_filter]

    if assignee_filter:
        filtered = [t for t in filtered if assignee_filter in (t.get("assignee") or "").lower()]

    sub = check_subscription()
    display_limit = sub["max_tasks_display"]
    display_tasks = filtered[:display_limit]

    output_success({
        "total": len(filtered),
        "displayed": len(display_tasks),
        "query": {k: v for k, v in data.items() if v},
        "tasks": display_tasks,
        "table": format_task_table(display_tasks),
    })


def find_blockers(data: Optional[Dict[str, Any]] = None) -> None:
    """查找阻碍任务（逾期或高优先级进行中任务）。

    阻碍判定条件：
    1. 已逾期的未完成任务
    2. 优先级为「紧急」或「高」且状态为「进行中」超过 7 天的任务

    Args:
        data: 可选参数。
    """
    if not require_blocker_feature():
        return

    tasks = _get_cached_tasks()
    if not tasks:
        output_error("暂无缓存任务数据，请先执行 fetch-all 获取任务", code="NO_DATA")
        return

    blockers = []
    now = datetime.now()

    for task in tasks:
        status = task.get("status", "")
        if status in ("已完成", "已关闭"):
            continue

        reasons = []

        # 条件1：逾期
        due_date = task.get("due_date", "")
        if due_date and is_overdue(due_date):
            reasons.append(f"已逾期（截止日期: {due_date}）")

        # 条件2：高优先级长时间进行中
        priority = task.get("priority", "")
        if priority in ("紧急", "高") and status == "进行中":
            updated = parse_date(task.get("updated_at", ""))
            if updated and (now - updated).days > 7:
                reasons.append(f"高优先级任务进行中超过 7 天（上次更新: {task.get('updated_at', '')[:10]}）")

        if reasons:
            blocker = dict(task)
            blocker["blocker_reasons"] = reasons
            blockers.append(blocker)

    # 按优先级排序：紧急 > 高 > 中 > 低
    priority_order = {"紧急": 0, "高": 1, "中": 2, "低": 3}
    blockers.sort(key=lambda t: priority_order.get(t.get("priority", "中"), 2))

    output_success({
        "total": len(blockers),
        "blockers": blockers,
        "table": format_task_table(blockers),
        "summary": f"发现 {len(blockers)} 个阻碍/风险任务" if blockers else "未发现阻碍任务",
    })


def require_blocker_feature() -> bool:
    """检查阻碍分析功能的订阅要求。"""
    sub = check_subscription()
    if "blocker_analysis" not in sub["features"]:
        output_error(
            "「阻碍分析」为付费版功能。当前为免费版，请升级至付费版（¥99/月）以使用此功能。",
            code="SUBSCRIPTION_REQUIRED",
        )
        return False
    return True


def sort_by_priority(data: Optional[Dict[str, Any]] = None) -> None:
    """按优先级排序所有任务（逾期优先，然后按优先级）。

    Args:
        data: 可选参数（可指定 status 过滤）。
    """
    tasks = _get_cached_tasks()
    if not tasks:
        output_error("暂无缓存任务数据，请先执行 fetch-all 获取任务", code="NO_DATA")
        return

    # 过滤已完成/已关闭的任务
    active_tasks = [t for t in tasks if t.get("status") not in ("已完成", "已关闭")]

    if data and data.get("status"):
        normalized = normalize_status(data["status"])
        active_tasks = [t for t in active_tasks if t.get("status") == normalized]

    # 排序规则：逾期在前，然后按优先级
    priority_order = {"紧急": 0, "高": 1, "中": 2, "低": 3}

    def sort_key(task: Dict) -> tuple:
        overdue_score = 0
        due = task.get("due_date", "")
        if due and is_overdue(due):
            overdue_score = -1  # 逾期排在前面
        prio = priority_order.get(task.get("priority", "中"), 2)
        return (overdue_score, prio)

    active_tasks.sort(key=sort_key)

    sub = check_subscription()
    display_limit = sub["max_tasks_display"]
    display_tasks = active_tasks[:display_limit]

    output_success({
        "total": len(active_tasks),
        "displayed": len(display_tasks),
        "tasks": display_tasks,
        "table": format_task_table(display_tasks),
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("project-nerve 任务聚合器")
    args = parser.parse_args()

    action = args.action.lower().replace("-", "_")

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "fetch_all": lambda: fetch_all(data),
        "fetch": lambda: fetch_all(data),
        "search": lambda: search_tasks(data or {}),
        "blockers": lambda: find_blockers(data),
        "priorities": lambda: sort_by_priority(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(["fetch-all", "search", "blockers", "priorities"])
        output_error(f"未知操作: {args.action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
