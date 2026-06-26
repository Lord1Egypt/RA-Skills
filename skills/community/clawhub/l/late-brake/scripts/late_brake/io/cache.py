# -*- coding: utf-8 -*-
"""
Late Brake - Loaded Data Cache

存储解析分割后的完整圈速数据，避免重复解析
缓存文件: .{filename}.lb.json
"""

import json
import os
from typing import Optional, List
from late_brake.models import Lap


def cache_file_path(source_file: str) -> str:
    """生成缓存文件路径"""
    source_file_norm = os.path.normpath(source_file)
    dirname = os.path.dirname(source_file_norm)
    basename = os.path.basename(source_file_norm)
    cache_basename = f".{basename}.lb.json"
    cache_path = os.path.join(dirname, cache_basename)
    cache_path = os.path.normpath(cache_path)
    # After normalization, verify cache is still within the normalized source directory
    # This prevents traversal even if original source_file contained ../ tricks
    source_dir_norm = os.path.normpath(dirname) + os.sep
    if not cache_path.startswith(source_dir_norm):
        raise ValueError(f"缓存路径生成失败，源文件路径可能包含非法路径遍历字符: {source_file}")
    return cache_path


def save_cached_laps(source_file: str, laps: List[Lap], track_id: str) -> None:
    """保存分割后的圈速到缓存"""
    cache_path = cache_file_path(source_file)
    data = {
        "source_file": source_file,
        "track_id": track_id,
        "laps": [lap.model_dump() for lap in laps]
    }
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_cached_laps(source_file: str) -> Optional[dict]:
    """加载缓存，如果缓存不存在或过期返回 None"""
    cache_path = cache_file_path(source_file)
    if not os.path.exists(cache_path):
        return None

    # 检查源文件修改时间，缓存比源文件新才有效
    source_mtime = os.path.getmtime(source_file)
    cache_mtime = os.path.getmtime(cache_path)
    if cache_mtime < source_mtime:
        return None

    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, KeyError):
        return None


def remove_cached_laps(source_file: str) -> None:
    """删除已有缓存，强制下次重新解析"""
    cache_path = cache_file_path(source_file)
    if os.path.exists(cache_path):
        os.remove(cache_path)
