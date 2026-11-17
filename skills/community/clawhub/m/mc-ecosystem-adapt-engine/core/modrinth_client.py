# -*- coding: utf-8 -*-
"""Modrinth API 客户端 - 联网查询模组信息

V1.0.2: 优化缓存系统
- 带 TTL 的内存缓存（自动过期）
- 磁盘持久化缓存（避免重复请求）
- 缓存命中统计
- 智能缓存更新策略

用于在本地数据库未收录时，通过 Modrinth API 实时查询模组的最新版本。
支持：模组搜索、版本获取、文件下载链接生成。
"""

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

# Modrinth API 基础 URL
MODRINTH_API = "https://api.modrinth.com/v2"

# 加载器名称映射（内部名称 -> Modrinth 名称）
LOADER_MAP = {
    "neoforge": "neoforge",
    "forge": "forge",
    "fabric": "fabric",
    "quilt": "quilt",
    "liteloader": "liteloader",
}

# 请求超时时间（秒）
REQUEST_TIMEOUT = 10

# 缓存配置
CACHE_TTL = {
    "search": 3600,      # 搜索结果缓存 1 小时
    "version": 7200,     # 版本信息缓存 2 小时
    "project": 86400,    # 项目详情缓存 24 小时
}
MAX_CACHE_SIZE = 500     # 最大缓存条目数
DISK_CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / ".api_cache"

# 内存缓存：带 TTL 的字典
_search_cache: Dict[str, Tuple[float, Optional[List[Dict]]]] = {}
_version_cache: Dict[str, Tuple[float, List[Dict]]] = {}
_project_cache: Dict[str, Tuple[float, Optional[Dict]]] = {}

# 缓存统计
_cache_hits = 0
_cache_misses = 0


def _init_disk_cache() -> Path:
    """初始化磁盘缓存目录"""
    DISK_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return DISK_CACHE_DIR


def _get_disk_cache_path(cache_key: str) -> Path:
    """获取磁盘缓存文件路径"""
    hash_key = hashlib.md5(cache_key.encode()).hexdigest()
    return DISK_CACHE_DIR / f"{hash_key}.json"


def _load_disk_cache(cache_key: str, max_age: int) -> Optional[Any]:
    """从磁盘加载缓存"""
    try:
        cache_path = _get_disk_cache_path(cache_key)
        if not cache_path.exists():
            return None

        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if time.time() - data.get("timestamp", 0) > max_age:
            cache_path.unlink(missing_ok=True)
            return None

        return data.get("value")
    except Exception:
        return None


def _save_disk_cache(cache_key: str, value: Any) -> None:
    """保存缓存到磁盘"""
    try:
        _init_disk_cache()
        cache_path = _get_disk_cache_path(cache_key)
        data = {
            "timestamp": time.time(),
            "value": value,
            "key": cache_key[:100],
        }
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        logger.debug(f"磁盘缓存保存失败: {e}")


def _cleanup_memory_cache(cache_dict: Dict, max_size: int = MAX_CACHE_SIZE) -> None:
    """清理内存缓存（LRU + TTL）"""
    if len(cache_dict) < max_size:
        return

    now = time.time()
    expired_keys = [k for k, (expire_at, _) in cache_dict.items() if expire_at < now]
    for k in expired_keys:
        del cache_dict[k]

    if len(cache_dict) >= max_size:
        sorted_items = sorted(cache_dict.items(), key=lambda x: x[1][0])
        to_remove = len(sorted_items) - max_size // 2
        for k, _ in sorted_items[:to_remove]:
            del cache_dict[k]


def _http_get(url: str, headers: Optional[Dict] = None) -> Tuple[int, Any]:
    """发送 HTTP GET 请求

    Args:
        url: 请求 URL
        headers: 附加请求头

    Returns:
        (status_code, response_data) 元组；出错返回 (0, None)
    """
    default_headers = {
        "User-Agent": "MC-Skill/1.0 (crash-analyzer)",
        "Accept": "application/json",
        "Cache-Control": "public, max-age=3600",
    }
    if headers:
        default_headers.update(headers)

    req = Request(url, headers=default_headers)
    try:
        with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return resp.status, data
    except URLError as e:
        logger.warning(f"网络请求失败: {url} - {e}")
        return 0, None
    except json.JSONDecodeError as e:
        logger.warning(f"JSON 解析失败: {url} - {e}")
        return 0, None


def _get_cached_or_fetch(
    cache_dict: Dict,
    cache_key: str,
    ttl: int,
    fetch_func,
    *args,
    **kwargs
) -> Tuple[Any, bool]:
    """智能缓存获取：内存 -> 磁盘 -> API

    Args:
        cache_dict: 内存缓存字典
        cache_key: 缓存键
        ttl: 缓存有效期（秒）
        fetch_func: 数据获取函数
        *args, **kwargs: fetch_func 的参数

    Returns:
        (数据, 是否来自缓存) 元组
    """
    global _cache_hits, _cache_misses
    now = time.time()

    # 1. 检查内存缓存
    if cache_key in cache_dict:
        expire_at, value = cache_dict[cache_key]
        if expire_at > now:
            _cache_hits += 1
            return value, True
        else:
            del cache_dict[cache_key]

    # 2. 检查磁盘缓存
    disk_value = _load_disk_cache(cache_key, ttl)
    if disk_value is not None:
        cache_dict[cache_key] = (now + ttl, disk_value)
        _cache_hits += 1
        return disk_value, True

    # 3. 请求 API
    _cache_misses += 1
    result = fetch_func(*args, **kwargs)

    # 4. 写入缓存
    cache_dict[cache_key] = (now + ttl, result)
    _save_disk_cache(cache_key, result)

    # 5. 清理缓存
    _cleanup_memory_cache(cache_dict)

    return result, False


def search_mod(
    query: str,
    mc_version: str = "",
    loader: str = "",
    limit: int = 5,
    timeout: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """搜索模组（通过 Modrinth API，带缓存）

    Args:
        query: 模组名称关键词，如 "create"
        mc_version: Minecraft 版本筛选（可选）
        loader: 加载器筛选，如 "neoforge"（可选）
        limit: 返回结果数量上限
        timeout: 本次请求超时时间（秒）

    Returns:
        匹配的模组项目列表
    """
    cache_key = f"search:{query.lower()}:{mc_version}:{loader}:{limit}"

    def _do_search():
        params = {
            "query": query,
            "limit": limit,
            "facets": json.dumps([["project_type:mod"]]),
        }
        if mc_version:
            params["facets"] = json.dumps([
                ["project_type:mod"],
                [f"versions:{mc_version}"],
            ])
        if loader:
            loader_name = LOADER_MAP.get(loader, loader)
            facets_list = [["project_type:mod"]]
            if mc_version:
                facets_list.append([f"versions:{mc_version}"])
            facets_list.append([f"categories:{loader_name}"])
            params["facets"] = json.dumps(facets_list)

        url = f"{MODRINTH_API}/search?{urlencode(params)}"
        if timeout:
            global REQUEST_TIMEOUT
            old_timeout = REQUEST_TIMEOUT
            REQUEST_TIMEOUT = timeout

        status, data = _http_get(url)

        if timeout:
            REQUEST_TIMEOUT = old_timeout

        results = []
        if status == 200 and data:
            hits = data.get("hits", [])
            for hit in hits:
                results.append({
                    "project_id": hit.get("project_id", ""),
                    "title": hit.get("title", ""),
                    "description": hit.get("description", ""),
                    "categories": hit.get("categories", []),
                    "versions": hit.get("versions", []),
                    "loaders": hit.get("loaders", []),
                    "downloads": hit.get("downloads", 0),
                    "slug": hit.get("slug", ""),
                })
        return results

    result, _ = _get_cached_or_fetch(
        _search_cache, cache_key, CACHE_TTL["search"], _do_search
    )
    return result or []


def get_project_info(project_id: str) -> Optional[Dict[str, Any]]:
    """获取 Modrinth 项目详细信息（带缓存）

    Args:
        project_id: Modrinth 项目 ID 或 slug

    Returns:
        项目信息字典；失败返回 None
    """
    cache_key = f"project:{project_id}"

    def _do_fetch():
        url = f"{MODRINTH_API}/project/{project_id}"
        status, data = _http_get(url)
        if status == 200 and data:
            return {
                "project_id": data.get("id", ""),
                "title": data.get("title", ""),
                "slug": data.get("slug", ""),
                "description": data.get("description", ""),
                "categories": data.get("categories", []),
                "client_side": data.get("client_side", ""),
                "server_side": data.get("server_side", ""),
                "downloads": data.get("downloads", 0),
                "follows": data.get("follows", 0),
            }
        return None

    result, _ = _get_cached_or_fetch(
        _project_cache, cache_key, CACHE_TTL["project"], _do_fetch
    )
    return result


def get_versions(
    project_id: str,
    mc_version: str = "",
    loader: str = "",
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """获取模组版本列表（带缓存）

    Args:
        project_id: Modrinth 项目 ID 或 slug
        mc_version: MC 版本筛选（可选）
        loader: 加载器筛选（可选）
        limit: 返回数量上限

    Returns:
        版本信息列表
    """
    cache_key = f"version:{project_id}:{mc_version}:{loader}:{limit}"

    def _do_fetch():
        params = {}
        if mc_version:
            params["game_versions"] = json.dumps([mc_version])
        if loader:
            loader_name = LOADER_MAP.get(loader, loader)
            params["loaders"] = json.dumps([loader_name])
        params["limit"] = str(limit)

        url = f"{MODRINTH_API}/project/{project_id}/version"
        if params:
            url += f"?{urlencode(params)}"

        status, data = _http_get(url)

        results = []
        if status == 200 and data:
            for ver in data:
                results.append({
                    "version_id": ver.get("id", ""),
                    "version_number": ver.get("version_number", ""),
                    "date_published": ver.get("date_published", ""),
                    "game_versions": ver.get("game_versions", []),
                    "loaders": ver.get("loaders", []),
                    "files": [
                        {
                            "hashes": f.get("hashes", {}),
                            "url": f.get("url", ""),
                            "filename": f.get("filename", ""),
                            "filesize": f.get("size", 0),
                            "primary": f.get("primary", False),
                        }
                        for f in ver.get("files", [])
                    ],
                    "version_type": ver.get("version_type", "release"),
                    "downloads": ver.get("downloads", 0),
                    "changelog": ver.get("changelog", "")[:200],
                })
        return results

    result, _ = _get_cached_or_fetch(
        _version_cache, cache_key, CACHE_TTL["version"], _do_fetch
    )
    return result or []


def get_latest_recommended_version(
    mod_id: str,
    mc_version: str,
    loader: str,
    max_cache_age: int = 86400,
) -> Optional[Dict[str, Any]]:
    """获取模组在指定环境下的最新推荐版本

    这是最常用的高级查询接口：
    1. 先通过名称搜索项目（带缓存）
    2. 再获取符合条件的版本列表（带缓存）
    3. 从中选出最优版本

    Args:
        mod_id: 模组 ID / 关键词，如 "create"
        mc_version: 目标 MC 版本，如 "1.21.1"
        loader: 目标加载器，如 "neoforge"
        max_cache_age: 缓存最大有效期（秒），默认1天

    Returns:
        推荐版本信息字典
    """
    loader_name = LOADER_MAP.get(loader, loader)
    matches = []

    # Step 1: 搜索项目（使用缓存）
    search_results = search_mod(mod_id, mc_version, loader_name, limit=5)
    if not search_results:
        search_results = search_mod(mod_id, limit=5)
        matches.append("放宽条件重新搜索")

    if not search_results:
        matches.append("未找到任何项目")
        return {
            "mod_id": mod_id,
            "status": "not_found",
            "note": f"Modrinth 上未找到与 '{mod_id}' 匹配的模组",
            "matches": matches,
        }

    # 选择最匹配的项目（优先按下载量排序）
    best = max(search_results, key=lambda x: x.get("downloads", 0))
    project_id = best["project_id"]
    project_title = best["title"]
    matches.append(f"选中项目: {project_title} ({project_id})")

    # Step 2: 获取版本列表（使用缓存）
    versions = get_versions(project_id, mc_version, loader_name, limit=20)
    if not versions:
        versions = get_versions(project_id, mc_version, limit=20)
        matches.append("放宽条件获取版本（不限加载器）")
    if not versions:
        versions = get_versions(project_id, loader=loader_name, limit=20)
        matches.append("放宽条件获取版本（不限MC版本）")
    if not versions:
        versions = get_versions(project_id, limit=20)
        matches.append("放宽条件获取版本（不限MC版本和加载器）")

    if not versions:
        matches.append("未找到任何版本")
        return {
            "mod_id": mod_id,
            "project_id": project_id,
            "project_title": project_title,
            "status": "not_found",
            "note": f"项目存在但未找到适配 {mc_version} + {loader} 的版本",
            "matches": matches,
        }

    # Step 3: 分类版本类型
    release_versions = [v for v in versions if v.get("version_type") == "release"]
    beta_versions = [v for v in versions if v.get("version_type") == "beta"]
    alpha_versions = [v for v in versions if v.get("version_type") == "alpha"]

    latest_release = release_versions[0] if release_versions else None
    latest_beta = beta_versions[0] if beta_versions else None
    latest_alpha = alpha_versions[0] if alpha_versions else None
    latest_any = versions[0]

    recommended = latest_release or latest_beta or latest_alpha or latest_any
    download_file = None
    for f in recommended.get("files", []):
        if f.get("primary"):
            download_file = f
            break
    if not download_file and recommended.get("files"):
        download_file = recommended["files"][0]

    matches.append(f"最新 release: {latest_release['version_number'] if latest_release else '无'}")
    if latest_beta:
        matches.append(f"最新 beta: {latest_beta['version_number']}")

    return {
        "mod_id": mod_id,
        "project_id": project_id,
        "project_title": project_title,
        "latest_version": latest_any["version_number"],
        "latest_version_id": latest_any["version_id"],
        "release_version": latest_release["version_number"] if latest_release else None,
        "beta_version": latest_beta["version_number"] if latest_beta else None,
        "alpha_version": latest_alpha["version_number"] if latest_alpha else None,
        "recommended_version": recommended["version_number"],
        "recommended_version_id": recommended["version_id"],
        "download_url": download_file["url"] if download_file else "",
        "download_filename": download_file["filename"] if download_file else "",
        "download_size": download_file["filesize"] if download_file else 0,
        "game_versions": recommended.get("game_versions", []),
        "loaders": recommended.get("loaders", []),
        "matches": matches,
        "status": "ok",
        "note": "来自 Modrinth 查询（已启用智能缓存）",
    }


def clear_cache() -> None:
    """清空所有缓存（内存 + 磁盘）"""
    global _search_cache, _version_cache, _project_cache, _cache_hits, _cache_misses
    _search_cache.clear()
    _version_cache.clear()
    _project_cache.clear()
    _cache_hits = 0
    _cache_misses = 0

    # 清理磁盘缓存
    try:
        if DISK_CACHE_DIR.exists():
            for f in DISK_CACHE_DIR.glob("*.json"):
                f.unlink()
        logger.info("Modrinth 查询缓存已清空（内存 + 磁盘）")
    except Exception as e:
        logger.warning(f"磁盘缓存清理失败: {e}")


def get_cache_stats() -> Dict[str, Any]:
    """获取缓存统计信息"""
    total = _cache_hits + _cache_misses
    hit_rate = (_cache_hits / total * 100) if total > 0 else 0

    disk_count = 0
    try:
        if DISK_CACHE_DIR.exists():
            disk_count = len(list(DISK_CACHE_DIR.glob("*.json")))
    except Exception:
        pass

    return {
        "memory_entries": {
            "search": len(_search_cache),
            "version": len(_version_cache),
            "project": len(_project_cache),
        },
        "disk_entries": disk_count,
        "cache_hits": _cache_hits,
        "cache_misses": _cache_misses,
        "hit_rate": f"{hit_rate:.1f}%",
        "total_queries": total,
    }


def is_cache_available() -> bool:
    """检查缓存系统是否可用"""
    try:
        _init_disk_cache()
        return True
    except Exception:
        return False
