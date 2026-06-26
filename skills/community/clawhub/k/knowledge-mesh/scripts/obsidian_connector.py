#!/usr/bin/env python3
"""
knowledge-mesh Obsidian 知识库集成模块

将 Obsidian 笔记库作为知识源接入统一搜索系统，
支持笔记搜索、索引构建、Wikilink/标签解析和增量同步。

用法:
    python3 obsidian_connector.py --action connect --data '{"vault_path":"/path/to/vault"}'
    python3 obsidian_connector.py --action search --data '{"query":"python async"}'
    python3 obsidian_connector.py --action index --data '{"vault_path":"/path/to/vault"}'
    python3 obsidian_connector.py --action list-notes
    python3 obsidian_connector.py --action sync
"""

import json
import math
import os
import re
import sys
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from utils import (
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    truncate_text,
    write_json_file,
)


# ============================================================
# 常量
# ============================================================

# Obsidian 索引数据文件
OBSIDIAN_INDEX_FILE = "obsidian_index.json"

# 支持索引的文件扩展名
OBSIDIAN_EXTENSIONS = {".md", ".markdown"}

# 最大索引笔记数
MAX_NOTES = 5000

# 单个文件最大大小（字节）
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

# 正则表达式：Obsidian 特性解析
RE_WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
RE_TAG = re.compile(r"(?:^|\s)#([a-zA-Z0-9_\u4e00-\u9fff][a-zA-Z0-9_/\u4e00-\u9fff]*)")
RE_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
RE_CALLOUT = re.compile(r"^>\s*\[!(\w+)\]\s*(.*?)$", re.MULTILINE)

# 搜索相关性权重
TITLE_MATCH_WEIGHT = 3.0
TAG_MATCH_WEIGHT = 2.0
CONTENT_MATCH_WEIGHT = 1.0
BACKLINK_BONUS = 0.5

# 停用词
STOP_WORDS = {
    "the", "a", "an", "is", "are", "in", "on", "for", "to", "of",
    "and", "or", "not", "with", "it", "this", "that", "be", "was",
    "的", "了", "在", "是", "我", "有", "和", "就", "不",
}


# ============================================================
# Obsidian 特性解析
# ============================================================

def _parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """解析 YAML frontmatter。

    Args:
        content: 笔记原始内容。

    Returns:
        (frontmatter 字典, 去除 frontmatter 后的内容) 元组。
    """
    match = RE_FRONTMATTER.match(content)
    if not match:
        return {}, content

    fm_text = match.group(1)
    body = content[match.end():]

    # 简单 YAML 解析（不依赖 PyYAML）
    frontmatter = {}
    current_key = None
    current_list = None

    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # 检查是否为列表项
        if line.startswith("- ") and current_key:
            value = line[2:].strip().strip('"').strip("'")
            if current_list is not None:
                current_list.append(value)
            continue

        # 检查键值对
        if ":" in line:
            idx = line.index(":")
            key = line[:idx].strip()
            value = line[idx + 1:].strip()

            current_key = key

            if not value:
                # 可能是列表的开始
                current_list = []
                frontmatter[key] = current_list
            else:
                # 去除引号
                value = value.strip('"').strip("'")
                # 尝试转换为布尔/数字
                if value.lower() in ("true", "yes"):
                    frontmatter[key] = True
                elif value.lower() in ("false", "no"):
                    frontmatter[key] = False
                else:
                    try:
                        frontmatter[key] = int(value)
                    except ValueError:
                        try:
                            frontmatter[key] = float(value)
                        except ValueError:
                            # 处理列表格式 [item1, item2]
                            if value.startswith("[") and value.endswith("]"):
                                items = [v.strip().strip('"').strip("'")
                                         for v in value[1:-1].split(",")]
                                frontmatter[key] = [i for i in items if i]
                            else:
                                frontmatter[key] = value
                current_list = None

    return frontmatter, body


def _extract_wikilinks(content: str) -> List[str]:
    """提取所有 [[wikilinks]]。

    Args:
        content: 笔记内容。

    Returns:
        链接目标列表（不含别名部分）。
    """
    return RE_WIKILINK.findall(content)


def _extract_tags(content: str) -> List[str]:
    """提取所有 #tags。

    Args:
        content: 笔记内容。

    Returns:
        标签列表（不含 # 前缀）。
    """
    return RE_TAG.findall(content)


def _extract_callouts(content: str) -> List[Dict[str, str]]:
    """提取 Obsidian 样式的 callout 块。

    Args:
        content: 笔记内容。

    Returns:
        callout 信息列表。
    """
    callouts = []
    for match in RE_CALLOUT.finditer(content):
        callouts.append({
            "type": match.group(1),
            "title": match.group(2).strip(),
        })
    return callouts


def _tokenize(text: str) -> List[str]:
    """将文本分词为词语列表。

    Args:
        text: 原始文本。

    Returns:
        小写词语列表。
    """
    if not text:
        return []
    tokens = re.findall(r"[a-zA-Z0-9_]{2,}|[\u4e00-\u9fff]+", text.lower())
    return [t for t in tokens if t not in STOP_WORDS and len(t) >= 2]


# ============================================================
# 笔记扫描与解析
# ============================================================

def _scan_vault(vault_path: str) -> List[str]:
    """扫描 Obsidian vault 中的所有笔记文件。

    Args:
        vault_path: vault 根目录路径。

    Returns:
        笔记文件绝对路径列表。
    """
    notes = []
    abs_vault = os.path.abspath(vault_path)

    for root, dirs, files in os.walk(abs_vault):
        # 跳过隐藏目录和 Obsidian 配置目录
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for f in files:
            _, ext = os.path.splitext(f)
            if ext.lower() in OBSIDIAN_EXTENSIONS:
                filepath = os.path.join(root, f)
                notes.append(filepath)

                if len(notes) >= MAX_NOTES:
                    return notes

    return notes


def _read_note(filepath: str) -> Optional[str]:
    """安全读取笔记文件内容。

    Args:
        filepath: 文件路径。

    Returns:
        文件文本内容，读取失败返回 None。
    """
    try:
        size = os.path.getsize(filepath)
        if size > MAX_FILE_SIZE:
            return None
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except (IOError, OSError):
        return None


def _parse_note(filepath: str, vault_path: str) -> Optional[Dict[str, Any]]:
    """解析单个笔记文件，提取元数据和内容。

    Args:
        filepath: 笔记文件路径。
        vault_path: vault 根目录路径。

    Returns:
        笔记信息字典，失败返回 None。
    """
    content = _read_note(filepath)
    if content is None:
        return None

    # 解析 frontmatter
    frontmatter, body = _parse_frontmatter(content)

    # 提取 Obsidian 特性
    wikilinks = _extract_wikilinks(body)
    tags = _extract_tags(body)
    callouts = _extract_callouts(body)

    # 从 frontmatter 中补充标签
    fm_tags = frontmatter.get("tags", [])
    if isinstance(fm_tags, str):
        fm_tags = [fm_tags]
    elif not isinstance(fm_tags, list):
        fm_tags = []
    all_tags = list(set(tags + fm_tags))

    # 文件基本信息
    filename = os.path.basename(filepath)
    name_without_ext = os.path.splitext(filename)[0]
    rel_path = os.path.relpath(filepath, vault_path)

    # 获取文件修改时间
    try:
        mtime = os.path.getmtime(filepath)
        modified_at = datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%S")
    except (OSError, ValueError):
        modified_at = ""

    # 分词
    tokens = _tokenize(f"{name_without_ext} {body}")

    return {
        "filepath": filepath,
        "rel_path": rel_path,
        "title": name_without_ext,
        "content": body,
        "frontmatter": frontmatter,
        "tags": all_tags,
        "wikilinks": wikilinks,
        "callouts": callouts,
        "tokens": tokens,
        "token_count": len(tokens),
        "modified_at": modified_at,
        "size": os.path.getsize(filepath),
    }


# ============================================================
# 索引持久化
# ============================================================

def _get_index_file() -> str:
    """获取 Obsidian 索引文件路径。"""
    return get_data_file(OBSIDIAN_INDEX_FILE)


def _load_index() -> Dict[str, Any]:
    """加载 Obsidian 索引数据。

    Returns:
        索引数据字典。
    """
    data = read_json_file(_get_index_file())
    if not isinstance(data, dict):
        data = {}

    if "vault_path" not in data:
        data["vault_path"] = ""
    if "notes" not in data:
        data["notes"] = {}
    if "backlink_graph" not in data:
        data["backlink_graph"] = {}
    if "tag_index" not in data:
        data["tag_index"] = {}
    if "last_sync" not in data:
        data["last_sync"] = ""
    if "total_notes" not in data:
        data["total_notes"] = 0

    return data


def _save_index(data: Dict[str, Any]) -> None:
    """保存 Obsidian 索引数据。"""
    write_json_file(_get_index_file(), data)


# ============================================================
# 搜索引擎
# ============================================================

def _search_notes(
    query: str,
    index_data: Dict[str, Any],
    max_results: int = 20,
) -> List[Dict[str, Any]]:
    """在索引中搜索笔记。

    使用多级相关性评分：标题匹配 > 标签匹配 > 内容匹配。

    Args:
        query: 搜索查询。
        index_data: 索引数据。
        max_results: 最大返回结果数。

    Returns:
        排序后的搜索结果列表。
    """
    notes = index_data.get("notes", {})
    backlink_graph = index_data.get("backlink_graph", {})

    if not notes:
        return []

    query_tokens = _tokenize(query)
    query_lower = query.lower()

    if not query_tokens:
        return []

    results = []

    for note_id, note in notes.items():
        score = 0.0
        matched_in = []

        title = note.get("title", "")
        tags = note.get("tags", [])
        content_preview = note.get("content_preview", "")
        tokens = note.get("tokens_sample", [])

        # 标题匹配（权重最高）
        title_lower = title.lower()
        title_match_count = 0
        for qt in query_tokens:
            if qt in title_lower:
                title_match_count += 1
        if title_match_count > 0:
            score += TITLE_MATCH_WEIGHT * (title_match_count / len(query_tokens))
            matched_in.append("title")

        # 标签匹配
        tags_lower = [t.lower() for t in tags]
        tag_match_count = 0
        for qt in query_tokens:
            for tag in tags_lower:
                if qt in tag:
                    tag_match_count += 1
                    break
        if tag_match_count > 0:
            score += TAG_MATCH_WEIGHT * (tag_match_count / len(query_tokens))
            matched_in.append("tags")

        # 内容匹配
        content_lower = content_preview.lower()
        content_match_count = 0
        for qt in query_tokens:
            if qt in content_lower:
                content_match_count += 1
        if content_match_count > 0:
            score += CONTENT_MATCH_WEIGHT * (content_match_count / len(query_tokens))
            matched_in.append("content")

        # token 精确匹配加分
        if tokens:
            token_set = set(tokens)
            token_matches = sum(1 for qt in query_tokens if qt in token_set)
            if token_matches > 0:
                score += 0.5 * (token_matches / len(query_tokens))

        # 反向链接加分（被更多笔记引用的笔记更权威）
        backlink_count = len(backlink_graph.get(title, []))
        if backlink_count > 0:
            score += BACKLINK_BONUS * min(backlink_count / 5.0, 1.0)

        if score > 0:
            results.append({
                "id": note_id,
                "source": "obsidian",
                "title": title,
                "url": f"obsidian://open?vault={os.path.basename(index_data.get('vault_path', ''))}&file={note.get('rel_path', '')}",
                "snippet": truncate_text(content_preview, 300),
                "author": note.get("frontmatter", {}).get("author", ""),
                "created_at": note.get("modified_at", ""),
                "score": round(score, 4),
                "tags": tags,
                "matched_in": matched_in,
                "backlink_count": backlink_count,
                "filepath": note.get("filepath", ""),
            })

    # 按分数降序排序
    results.sort(key=lambda r: r.get("score", 0), reverse=True)
    return results[:max_results]


# ============================================================
# 索引构建
# ============================================================

def _build_index(vault_path: str) -> Dict[str, Any]:
    """构建 Obsidian vault 的完整索引。

    Args:
        vault_path: vault 根目录路径。

    Returns:
        索引数据字典。
    """
    note_files = _scan_vault(vault_path)

    notes = {}
    backlink_graph = {}  # {被链接的笔记: [链接来源笔记]}
    tag_index = {}  # {标签: [笔记ID]}
    skipped = 0

    for filepath in note_files:
        parsed = _parse_note(filepath, vault_path)
        if parsed is None:
            skipped += 1
            continue

        note_id = generate_id("ON")
        title = parsed["title"]

        # 存储笔记信息（不保存完整内容，只保存预览和采样 token）
        notes[note_id] = {
            "filepath": parsed["filepath"],
            "rel_path": parsed["rel_path"],
            "title": title,
            "content_preview": truncate_text(parsed["content"], 500),
            "frontmatter": parsed["frontmatter"],
            "tags": parsed["tags"],
            "wikilinks": parsed["wikilinks"],
            "tokens_sample": parsed["tokens"][:100],  # 保存前100个token用于搜索
            "token_count": parsed["token_count"],
            "modified_at": parsed["modified_at"],
            "size": parsed["size"],
            "mtime": os.path.getmtime(filepath) if os.path.exists(filepath) else 0,
        }

        # 构建反向链接图
        for link_target in parsed["wikilinks"]:
            if link_target not in backlink_graph:
                backlink_graph[link_target] = []
            backlink_graph[link_target].append(title)

        # 构建标签索引
        for tag in parsed["tags"]:
            if tag not in tag_index:
                tag_index[tag] = []
            tag_index[tag].append(note_id)

    index_data = {
        "vault_path": os.path.abspath(vault_path),
        "notes": notes,
        "backlink_graph": backlink_graph,
        "tag_index": tag_index,
        "last_sync": now_iso(),
        "total_notes": len(notes),
        "skipped": skipped,
    }

    return index_data


# ============================================================
# 操作实现
# ============================================================

def action_connect(data: Dict[str, Any]) -> None:
    """连接到 Obsidian vault。

    验证 vault 路径存在，扫描结构并返回摘要信息。

    Args:
        data: 包含 vault_path 的字典。
    """
    vault_path = data.get("vault_path", "").strip()

    if not vault_path:
        # 尝试从环境变量读取
        vault_path = os.environ.get("KM_OBSIDIAN_VAULT_PATH", "").strip()

    if not vault_path:
        output_error(
            "请提供 Obsidian vault 路径（vault_path）或设置 KM_OBSIDIAN_VAULT_PATH 环境变量",
            code="VALIDATION_ERROR",
        )
        return

    abs_path = os.path.abspath(vault_path)

    if not os.path.isdir(abs_path):
        output_error(f"Vault 路径不存在或不是目录: {abs_path}", code="PATH_NOT_FOUND")
        return

    # 扫描 vault 结构
    note_files = _scan_vault(abs_path)

    # 检查是否有 .obsidian 配置目录
    obsidian_config = os.path.join(abs_path, ".obsidian")
    has_obsidian_config = os.path.isdir(obsidian_config)

    # 统计目录结构
    dir_counter = Counter()
    tag_counter = Counter()
    total_size = 0

    for filepath in note_files[:200]:  # 快速扫描前200个
        rel_dir = os.path.dirname(os.path.relpath(filepath, abs_path))
        if rel_dir:
            dir_counter[rel_dir] += 1
        else:
            dir_counter["(root)"] += 1
        total_size += os.path.getsize(filepath)

        # 快速提取标签
        content = _read_note(filepath)
        if content:
            tags = _extract_tags(content)
            for tag in tags:
                tag_counter[tag] += 1

    top_dirs = [{"dir": d, "count": c} for d, c in dir_counter.most_common(10)]
    top_tags = [{"tag": t, "count": c} for t, c in tag_counter.most_common(10)]

    output_success({
        "message": f"成功连接到 Obsidian vault: {abs_path}",
        "vault_path": abs_path,
        "has_obsidian_config": has_obsidian_config,
        "total_notes": len(note_files),
        "total_size_kb": round(total_size / 1024, 1),
        "top_directories": top_dirs,
        "top_tags": top_tags,
        "status": "connected",
    })


def action_search(data: Dict[str, Any]) -> None:
    """在 Obsidian vault 中搜索笔记。

    Args:
        data: 包含 query 的字典，可选 max_results。
    """
    query = data.get("query", "").strip()
    if not query:
        output_error("请提供搜索关键词（query）", code="VALIDATION_ERROR")
        return

    max_results = data.get("max_results", 20)

    index_data = _load_index()
    if not index_data.get("notes"):
        output_error(
            "Obsidian 索引为空，请先执行 index 操作构建索引",
            code="NO_INDEX",
        )
        return

    results = _search_notes(query, index_data, max_results)

    output_success({
        "query": query,
        "source": "obsidian",
        "total": len(results),
        "vault_path": index_data.get("vault_path", ""),
        "results": results,
    })


def action_index(data: Dict[str, Any]) -> None:
    """构建 Obsidian vault 的完整索引。

    Args:
        data: 包含 vault_path 的字典。
    """
    vault_path = data.get("vault_path", "").strip()

    if not vault_path:
        vault_path = os.environ.get("KM_OBSIDIAN_VAULT_PATH", "").strip()

    if not vault_path:
        output_error(
            "请提供 Obsidian vault 路径（vault_path）或设置 KM_OBSIDIAN_VAULT_PATH 环境变量",
            code="VALIDATION_ERROR",
        )
        return

    abs_path = os.path.abspath(vault_path)
    if not os.path.isdir(abs_path):
        output_error(f"Vault 路径不存在: {abs_path}", code="PATH_NOT_FOUND")
        return

    # 构建索引
    index_data = _build_index(abs_path)
    _save_index(index_data)

    # 统计信息
    total_tags = len(index_data.get("tag_index", {}))
    total_backlinks = sum(
        len(sources) for sources in index_data.get("backlink_graph", {}).values()
    )

    output_success({
        "message": f"索引构建完成: {index_data['total_notes']} 篇笔记",
        "vault_path": abs_path,
        "total_notes": index_data["total_notes"],
        "skipped": index_data.get("skipped", 0),
        "total_tags": total_tags,
        "total_backlinks": total_backlinks,
        "last_sync": index_data["last_sync"],
    })


def action_list_notes(data: Optional[Dict[str, Any]] = None) -> None:
    """列出已索引的 Obsidian 笔记。"""
    index_data = _load_index()
    notes = index_data.get("notes", {})

    if not notes:
        output_error("Obsidian 索引为空，请先执行 index 操作", code="NO_INDEX")
        return

    note_list = []
    for note_id, note in notes.items():
        note_list.append({
            "id": note_id,
            "title": note.get("title", ""),
            "rel_path": note.get("rel_path", ""),
            "tags": note.get("tags", []),
            "token_count": note.get("token_count", 0),
            "modified_at": note.get("modified_at", ""),
            "size": note.get("size", 0),
            "wikilinks_count": len(note.get("wikilinks", [])),
        })

    # 按修改时间倒序
    note_list.sort(key=lambda n: n.get("modified_at", ""), reverse=True)

    # 标签统计
    tag_index = index_data.get("tag_index", {})
    top_tags = sorted(tag_index.items(), key=lambda x: len(x[1]), reverse=True)[:10]

    output_success({
        "vault_path": index_data.get("vault_path", ""),
        "total_notes": len(note_list),
        "last_sync": index_data.get("last_sync", ""),
        "top_tags": [{"tag": t, "note_count": len(ids)} for t, ids in top_tags],
        "notes": note_list,
    })


def action_sync(data: Optional[Dict[str, Any]] = None) -> None:
    """增量同步：重新索引自上次同步以来变化的文件。

    通过比较文件的 mtime 来检测变化。
    """
    index_data = _load_index()
    vault_path = index_data.get("vault_path", "")

    if not vault_path:
        # 尝试从环境变量读取
        vault_path = os.environ.get("KM_OBSIDIAN_VAULT_PATH", "").strip()

    if not vault_path or not os.path.isdir(vault_path):
        output_error(
            "未找到已连接的 vault，请先执行 connect 或 index 操作",
            code="NO_VAULT",
        )
        return

    notes = index_data.get("notes", {})

    # 扫描当前 vault 文件
    current_files = _scan_vault(vault_path)
    current_paths = {os.path.abspath(f) for f in current_files}

    # 已索引的文件路径映射
    indexed_paths = {}
    for note_id, note in notes.items():
        fp = note.get("filepath", "")
        if fp:
            indexed_paths[fp] = note_id

    added = 0
    updated = 0
    removed = 0

    # 检查新增和更新的文件
    for filepath in current_files:
        abs_fp = os.path.abspath(filepath)

        if abs_fp in indexed_paths:
            # 已索引，检查是否更新
            note_id = indexed_paths[abs_fp]
            old_mtime = notes[note_id].get("mtime", 0)
            try:
                current_mtime = os.path.getmtime(abs_fp)
            except OSError:
                continue

            if current_mtime > old_mtime:
                # 文件已更新，重新解析
                parsed = _parse_note(abs_fp, vault_path)
                if parsed:
                    notes[note_id].update({
                        "title": parsed["title"],
                        "content_preview": truncate_text(parsed["content"], 500),
                        "frontmatter": parsed["frontmatter"],
                        "tags": parsed["tags"],
                        "wikilinks": parsed["wikilinks"],
                        "tokens_sample": parsed["tokens"][:100],
                        "token_count": parsed["token_count"],
                        "modified_at": parsed["modified_at"],
                        "size": parsed["size"],
                        "mtime": current_mtime,
                    })
                    updated += 1
        else:
            # 新文件，添加索引
            parsed = _parse_note(abs_fp, vault_path)
            if parsed:
                note_id = generate_id("ON")
                notes[note_id] = {
                    "filepath": abs_fp,
                    "rel_path": parsed["rel_path"],
                    "title": parsed["title"],
                    "content_preview": truncate_text(parsed["content"], 500),
                    "frontmatter": parsed["frontmatter"],
                    "tags": parsed["tags"],
                    "wikilinks": parsed["wikilinks"],
                    "tokens_sample": parsed["tokens"][:100],
                    "token_count": parsed["token_count"],
                    "modified_at": parsed["modified_at"],
                    "size": parsed["size"],
                    "mtime": os.path.getmtime(abs_fp) if os.path.exists(abs_fp) else 0,
                }
                added += 1

    # 检查已删除的文件
    ids_to_remove = []
    for note_id, note in notes.items():
        fp = note.get("filepath", "")
        if fp and fp not in current_paths:
            ids_to_remove.append(note_id)

    for note_id in ids_to_remove:
        del notes[note_id]
        removed += 1

    # 重建反向链接图和标签索引
    backlink_graph = {}
    tag_index = {}
    for note_id, note in notes.items():
        title = note.get("title", "")
        for link_target in note.get("wikilinks", []):
            if link_target not in backlink_graph:
                backlink_graph[link_target] = []
            backlink_graph[link_target].append(title)
        for tag in note.get("tags", []):
            if tag not in tag_index:
                tag_index[tag] = []
            tag_index[tag].append(note_id)

    index_data["notes"] = notes
    index_data["backlink_graph"] = backlink_graph
    index_data["tag_index"] = tag_index
    index_data["last_sync"] = now_iso()
    index_data["total_notes"] = len(notes)

    _save_index(index_data)

    output_success({
        "message": f"同步完成: 新增 {added}, 更新 {updated}, 删除 {removed}",
        "added": added,
        "updated": updated,
        "removed": removed,
        "total_notes": len(notes),
        "last_sync": index_data["last_sync"],
    })


# ============================================================
# 公开 API（供其他模块调用）
# ============================================================

def search_obsidian(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """搜索 Obsidian vault（供 source_searcher 调用）。

    Args:
        query: 搜索查询。
        max_results: 最大返回结果数。

    Returns:
        标准化搜索结果列表。
    """
    index_data = _load_index()
    if not index_data.get("notes"):
        return []

    return _search_notes(query, index_data, max_results)


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("knowledge-mesh Obsidian 知识库集成")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "connect": lambda: action_connect(data or {}),
        "search": lambda: action_search(data or {}),
        "index": lambda: action_index(data or {}),
        "list-notes": lambda: action_list_notes(data),
        "sync": lambda: action_sync(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
