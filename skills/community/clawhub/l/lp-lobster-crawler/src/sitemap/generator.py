"""站点地图生成、更新与查询。

站点地图以 JSON 格式存储，记录每个站点已知的内容 URL 及其元信息。
格式：
{
    "site": "webnovel",
    "generated_at": "2026-03-20T12:00:00",
    "entries": [
        {
            "url": "https://...",
            "external_id": "12345",
            "title": "...",
            "content_type": "novel",
            "last_modified": "2026-03-19T10:00:00",
            "status": "active"
        }
    ]
}
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def create_sitemap(site: str, entries: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """创建新的站点地图。

    Args:
        site: 站点名称。
        entries: 初始条目列表。

    Returns:
        站点地图字典。
    """
    return {
        "site": site,
        "generated_at": datetime.utcnow().isoformat(),
        "entries": entries or [],
    }


def add_entry(
    sitemap: dict[str, Any],
    url: str,
    external_id: str,
    title: str = "",
    content_type: str = "novel",
    last_modified: str | None = None,
    status: str = "active",
) -> bool:
    """向站点地图添加条目（去重）。

    Args:
        sitemap: 站点地图字典。
        url: 内容 URL。
        external_id: 外部 ID。
        title: 标题。
        content_type: 内容类型。
        last_modified: 最后修改时间 ISO 格式。
        status: 状态。

    Returns:
        True 表示新增，False 表示已存在（已更新）。
    """
    for entry in sitemap["entries"]:
        if entry["external_id"] == external_id:
            # 更新已有条目
            entry["url"] = url
            entry["title"] = title
            entry["last_modified"] = last_modified
            entry["status"] = status
            return False

    sitemap["entries"].append({
        "url": url,
        "external_id": external_id,
        "title": title,
        "content_type": content_type,
        "last_modified": last_modified or datetime.utcnow().isoformat(),
        "status": status,
    })
    return True


def remove_entry(sitemap: dict[str, Any], external_id: str) -> bool:
    """从站点地图移除条目。

    Args:
        sitemap: 站点地图字典。
        external_id: 要移除的外部 ID。

    Returns:
        True 表示已移除，False 表示未找到。
    """
    before = len(sitemap["entries"])
    sitemap["entries"] = [e for e in sitemap["entries"] if e["external_id"] != external_id]
    return len(sitemap["entries"]) < before


def query_entries(
    sitemap: dict[str, Any],
    content_type: str | None = None,
    status: str | None = None,
) -> list[dict[str, Any]]:
    """查询站点地图条目。

    Args:
        sitemap: 站点地图字典。
        content_type: 按内容类型过滤。
        status: 按状态过滤。

    Returns:
        匹配的条目列表。
    """
    results = sitemap["entries"]
    if content_type:
        results = [e for e in results if e.get("content_type") == content_type]
    if status:
        results = [e for e in results if e.get("status") == status]
    return results


def save_sitemap(sitemap: dict[str, Any], path: str | Path) -> None:
    """将站点地图保存为 JSON 文件。

    Args:
        sitemap: 站点地图字典。
        path: 输出文件路径。
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    sitemap["generated_at"] = datetime.utcnow().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sitemap, f, ensure_ascii=False, indent=2)


def load_sitemap(path: str | Path) -> dict[str, Any]:
    """从 JSON 文件加载站点地图。

    Args:
        path: JSON 文件路径。

    Returns:
        站点地图字典。

    Raises:
        FileNotFoundError: 文件不存在。
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Sitemap file not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)
