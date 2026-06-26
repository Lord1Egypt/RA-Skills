#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cache_utils.py - 搜索结果缓存工具

提供基于文件的缓存机制，支持 TTL 过期和手动清除。

Usage:
    from cache_utils import get_cached, set_cached, invalidate_cache

    cached = get_cached("arxiv_query_hash")
    if cached:
        print(cached)
    else:
        results = do_search()
        set_cached("arxiv_query_hash", results, ttl=3600)
"""
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

# 缓存目录
CACHE_DIR = Path("~/.cache/openclaw/search").expanduser()

# 默认 TTL（秒）
DEFAULT_TTL = 3600  # 1小时

# 最大缓存条目数
MAX_CACHE_ENTRIES = 1000


def _get_cache_path(key: str) -> Path:
    """根据 key 获取缓存文件路径"""
    # MD5 哈希确保路径安全
    hash_key = hashlib.md5(key.encode()).hexdigest()
    return CACHE_DIR / f"{hash_key}.json"


def get_cached(key: str) -> Optional[Dict[str, Any]]:
    """
    获取缓存的结果。

    Args:
        key: 缓存键（通常是查询的哈希）

    Returns:
        缓存的数据（如果存在且未过期），否则返回 None
    """
    cache_path = _get_cache_path(key)

    if not cache_path.exists():
        return None

    # 检查是否过期
    try:
        stat = cache_path.stat()
        age = time.time() - stat.st_mtime

        with open(cache_path, "r", encoding="utf-8") as f:
            cached_data = json.load(f)

        # 检查 TTL
        ttl = cached_data.get("_ttl", DEFAULT_TTL)
        if age > ttl:
            cache_path.unlink()
            return None

        # 返回数据（移除内部元数据）
        data = cached_data.get("data", {})
        data["_cached"] = True
        data["_cache_age"] = int(age)
        return data

    except (json.JSONDecodeError, OSError):
        return None


def set_cached(key: str, data: Dict[str, Any], ttl: int = DEFAULT_TTL) -> bool:
    """
    设置缓存。

    Args:
        key: 缓存键
        data: 要缓存的数据
        ttl: 过期时间（秒）

    Returns:
        True 如果成功，False 如果失败
    """
    cache_path = _get_cache_path(key)

    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        cache_entry = {
            "data": data,
            "_ttl": ttl,
            "_created_at": time.time(),
            "_key": key
        }

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache_entry, f, ensure_ascii=False)

        # 清理旧缓存
        _cleanup_old_entries()

        return True

    except (OSError, TypeError) as e:
        return False


def invalidate_cache(key: str) -> bool:
    """删除指定缓存"""
    cache_path = _get_cache_path(key)
    try:
        if cache_path.exists():
            cache_path.unlink()
            return True
        return False
    except OSError:
        return False


def clear_all_cache() -> int:
    """清除所有缓存，返回删除的条目数"""
    count = 0
    try:
        for path in CACHE_DIR.glob("*.json"):
            path.unlink()
            count += 1
    except OSError:
        pass
    return count


def _cleanup_old_entries():
    """清理超过 MAX_CACHE_ENTRIES 的旧缓存"""
    try:
        entries = sorted(
            CACHE_DIR.glob("*.json"),
            key=lambda p: p.stat().st_mtime
        )

        # 删除最旧的条目直到在限制内
        while len(entries) > MAX_CACHE_ENTRIES:
            oldest = entries.pop(0)
            oldest.unlink()
    except OSError:
        pass


def cache_key_from_query(provider: str, query: str, **kwargs) -> str:
    """
    根据查询生成缓存键。

    Args:
        provider: 搜索提供商 (google, arxiv, etc.)
        query: 搜索查询
        **kwargs: 其他参数（如 max_results, time_filter 等）

    Returns:
        缓存键字符串
    """
    # 构建规范化查询字符串
    parts = [provider, query]
    for k, v in sorted(kwargs.items()):
        if v is not None:
            parts.append(f"{k}={v}")

    return "|".join(parts)


# ── 缓存装饰器 ────────────────────────────────────────────────────────────

def cached(ttl: int = DEFAULT_TTL, key_prefix: str = ""):
    """
    缓存装饰器。

    Usage:
        @cached(ttl=1800, key_prefix="arxiv")
        def search_arxiv(query, max_results):
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key_parts = [key_prefix, str(args), str(kwargs)]
            cache_key = hashlib.md5("|".join(str(p) for p in key_parts).encode()).hexdigest()

            # 尝试获取缓存
            cached_result = get_cached(cache_key)
            if cached_result is not None:
                return cached_result

            # 执行函数
            result = func(*args, **kwargs)

            # 缓存结果
            set_cached(cache_key, result, ttl=ttl)

            return result

        return wrapper
    return decorator


if __name__ == "__main__":
    # 测试
    print("=== 缓存工具测试 ===")

    # 测试设置和获取
    test_data = {"results": ["a", "b", "c"], "count": 3}
    test_key = "test_key_123"

    print(f"设置缓存: {test_key}")
    set_cached(test_key, test_data, ttl=60)

    print(f"获取缓存: {get_cached(test_key)}")
    print(f"删除缓存: {invalidate_cache(test_key)}")
    print(f"获取已删除的缓存: {get_cached(test_key)}")

    print(f"\n清除所有缓存: {clear_all_cache()} 条")