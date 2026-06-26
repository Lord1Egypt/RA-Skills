#!/usr/bin/env python3
"""
knowledge-mesh 本地知识索引构建器

对本地 .md/.txt/.py 等文件构建 TF-IDF 倒排索引，
支持全文搜索、索引管理和重建。

用法:
    python3 index_builder.py --action index --data '{"paths":["./docs"],"patterns":["*.md","*.txt"]}'
    python3 index_builder.py --action search-local --data '{"query":"async python"}'
    python3 index_builder.py --action list-indexed
    python3 index_builder.py --action rebuild
    python3 index_builder.py --action delete --data '{"doc_id":"DOC20260319..."}'
"""

import fnmatch
import math
import os
import re
import sys
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

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
    require_paid_feature,
    truncate_text,
    write_json_file,
)


# ============================================================
# 常量
# ============================================================

# 索引数据文件
INDEX_DATA_FILE = "index_data.json"
# 文档元数据文件
DOC_METADATA_FILE = "doc_metadata.json"

# 支持索引的文件扩展名
INDEXABLE_EXTENSIONS = {".md", ".txt", ".py", ".js", ".ts", ".java", ".go", ".rs", ".rb", ".sh", ".yaml", ".yml", ".json", ".toml", ".cfg", ".ini", ".html", ".css", ".sql", ".markdown"}

# Obsidian 特性正则表达式
RE_WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
RE_TAG_OBSIDIAN = re.compile(r"(?:^|\s)#([a-zA-Z0-9_\u4e00-\u9fff][a-zA-Z0-9_/\u4e00-\u9fff]*)")
RE_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Wikilink 和标签的额外权重
WIKILINK_WEIGHT = 2.0
TAG_WEIGHT = 3.0

# 默认 glob 模式
DEFAULT_PATTERNS = ["*.md", "*.txt", "*.py"]

# 停用词
STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "can", "shall",
    "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "and",
    "but", "or", "not", "so", "if", "then", "than", "too", "very",
    "just", "about", "up", "out", "no", "it", "its", "this", "that",
    "i", "me", "my", "we", "our", "you", "your", "he", "she",
    "they", "them", "their", "what", "which", "who", "how", "when",
    "where", "why", "all", "each", "every", "both",
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
    "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
    "你", "会", "着", "没有", "看", "好", "自己", "这", "他", "她",
    "import", "from", "def", "class", "return", "self", "none",
    "true", "false", "pass", "elif", "else", "try", "except",
}

# 单次索引最大文件数
MAX_INDEX_FILES = 500

# 单个文件最大大小（字节）
MAX_FILE_SIZE = 1024 * 1024  # 1MB


# ============================================================
# 文本分词
# ============================================================

def _tokenize(text: str) -> List[str]:
    """将文本分词为词语列表。

    Args:
        text: 原始文本。

    Returns:
        小写词语列表（去停用词）。
    """
    if not text:
        return []
    tokens = re.findall(r"[a-zA-Z0-9_]{2,}|[\u4e00-\u9fff]+", text.lower())
    return [t for t in tokens if t not in STOP_WORDS and len(t) >= 2]


def _tokenize_with_positions(text: str) -> List[Tuple[str, int]]:
    """分词并记录每个词的起始位置。

    Args:
        text: 原始文本。

    Returns:
        (词语, 位置) 元组列表。
    """
    if not text:
        return []
    result = []
    for match in re.finditer(r"[a-zA-Z0-9_]{2,}|[\u4e00-\u9fff]+", text.lower()):
        token = match.group(0)
        if token not in STOP_WORDS and len(token) >= 2:
            result.append((token, match.start()))
    return result


# ============================================================
# 文件扫描
# ============================================================

def _match_patterns(filename: str, patterns: List[str]) -> bool:
    """检查文件名是否匹配任一 glob 模式。

    Args:
        filename: 文件名。
        patterns: glob 模式列表。

    Returns:
        是否匹配。
    """
    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def _scan_files(
    paths: List[str],
    patterns: Optional[List[str]] = None,
) -> List[str]:
    """扫描指定路径下匹配模式的文件。

    Args:
        paths: 待扫描的目录或文件路径列表。
        patterns: glob 模式列表，默认 ["*.md", "*.txt", "*.py"]。

    Returns:
        匹配的文件绝对路径列表。
    """
    if patterns is None:
        patterns = DEFAULT_PATTERNS

    matched_files = []

    for path in paths:
        abs_path = os.path.abspath(path)

        if os.path.isfile(abs_path):
            # 检查扩展名
            _, ext = os.path.splitext(abs_path)
            if ext.lower() in INDEXABLE_EXTENSIONS or _match_patterns(os.path.basename(abs_path), patterns):
                matched_files.append(abs_path)
        elif os.path.isdir(abs_path):
            for root, dirs, files in os.walk(abs_path):
                # 跳过隐藏目录和常见忽略目录
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {"node_modules", "__pycache__", "venv", ".git"}]
                for f in files:
                    if _match_patterns(f, patterns):
                        filepath = os.path.join(root, f)
                        matched_files.append(filepath)

        if len(matched_files) >= MAX_INDEX_FILES:
            break

    return matched_files[:MAX_INDEX_FILES]


def _read_file_content(filepath: str) -> Optional[str]:
    """安全读取文件内容。

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


# ============================================================
# Obsidian 特性解析
# ============================================================

def _extract_wikilinks(content: str) -> List[str]:
    """提取 Obsidian [[wikilinks]] 作为额外关键词信号。

    Args:
        content: 文件内容。

    Returns:
        链接目标列表。
    """
    return RE_WIKILINK.findall(content)


def _extract_obsidian_tags(content: str) -> List[str]:
    """提取 Obsidian #tags 作为高权重关键词。

    Args:
        content: 文件内容。

    Returns:
        标签列表（不含 # 前缀）。
    """
    return RE_TAG_OBSIDIAN.findall(content)


def _parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """解析 YAML frontmatter 元数据。

    解析日期、分类、作者等字段用于过滤。

    Args:
        content: 文件内容。

    Returns:
        (frontmatter 字典, 去除 frontmatter 后的内容) 元组。
    """
    match = RE_FRONTMATTER.match(content)
    if not match:
        return {}, content

    fm_text = match.group(1)
    body = content[match.end():]

    frontmatter = {}
    current_key = None
    current_list = None

    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("- ") and current_key and current_list is not None:
            value = line[2:].strip().strip('"').strip("'")
            current_list.append(value)
            continue

        if ":" in line:
            idx = line.index(":")
            key = line[:idx].strip()
            value = line[idx + 1:].strip()
            current_key = key

            if not value:
                current_list = []
                frontmatter[key] = current_list
            else:
                value = value.strip('"').strip("'")
                if value.startswith("[") and value.endswith("]"):
                    items = [v.strip().strip('"').strip("'")
                             for v in value[1:-1].split(",")]
                    frontmatter[key] = [i for i in items if i]
                else:
                    frontmatter[key] = value
                current_list = None

    return frontmatter, body


def _get_obsidian_extra_tokens(content: str) -> Tuple[List[Tuple[str, float]], Dict[str, Any]]:
    """从文件内容中提取 Obsidian 特性的额外 token 和元数据。

    Wikilinks 作为加权 token（权重 2.0），
    Tags 作为高权重 token（权重 3.0），
    Frontmatter 作为过滤元数据。

    Args:
        content: 文件内容。

    Returns:
        (加权token列表, frontmatter字典) 元组。
    """
    extra_tokens = []

    # 提取 wikilinks 并分词
    wikilinks = _extract_wikilinks(content)
    for link in wikilinks:
        link_tokens = _tokenize(link)
        for token in link_tokens:
            extra_tokens.append((token, WIKILINK_WEIGHT))

    # 提取标签
    tags = _extract_obsidian_tags(content)
    for tag in tags:
        tag_tokens = _tokenize(tag)
        for token in tag_tokens:
            extra_tokens.append((token, TAG_WEIGHT))
        # 完整标签也作为 token
        if len(tag) >= 2:
            extra_tokens.append((tag.lower(), TAG_WEIGHT))

    # 解析 frontmatter
    frontmatter, _ = _parse_frontmatter(content)

    return extra_tokens, frontmatter


# ============================================================
# 倒排索引构建
# ============================================================

def _build_inverted_index(
    documents: Dict[str, str],
) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, Dict[str, Any]]]:
    """构建倒排索引和文档元数据。

    Args:
        documents: {doc_id: content} 映射。

    Returns:
        (倒排索引, 文档元数据) 元组。
        倒排索引格式: {term: [{doc_id, tf, positions}]}
        文档元数据格式: {doc_id: {path, size, token_count, indexed_at}}
    """
    inverted_index = {}
    doc_metadata = {}
    doc_count = len(documents)

    for doc_id, content in documents.items():
        tokens_with_pos = _tokenize_with_positions(content)
        tokens = [t for t, _ in tokens_with_pos]
        token_count = len(tokens)

        if token_count == 0:
            continue

        # 统计词频和位置
        term_info = {}
        for token, pos in tokens_with_pos:
            if token not in term_info:
                term_info[token] = {"count": 0, "positions": []}
            term_info[token]["count"] += 1
            term_info[token]["positions"].append(pos)

        # 提取 Obsidian 特性的额外加权 token
        extra_tokens, frontmatter = _get_obsidian_extra_tokens(content)
        for token, weight in extra_tokens:
            if token not in term_info:
                term_info[token] = {"count": 0, "positions": []}
            # 加权计数：wikilinks 和标签获得额外权重
            term_info[token]["count"] += int(weight)

        # 构建倒排索引条目
        for term, info in term_info.items():
            tf = 1 + math.log(info["count"]) if info["count"] > 0 else 0
            entry = {
                "doc_id": doc_id,
                "tf": round(tf, 4),
                "positions": info["positions"][:20],  # 最多保留 20 个位置
            }
            if term not in inverted_index:
                inverted_index[term] = []
            inverted_index[term].append(entry)

        doc_metadata[doc_id] = {
            "token_count": token_count,
            "unique_terms": len(term_info),
            "frontmatter": frontmatter if frontmatter else None,
        }

    return inverted_index, doc_metadata


def _search_index(
    query: str,
    inverted_index: Dict[str, List[Dict[str, Any]]],
    doc_metadata_map: Dict[str, Dict[str, Any]],
    max_results: int = 20,
) -> List[Dict[str, Any]]:
    """在倒排索引中搜索。

    Args:
        query: 查询字符串。
        inverted_index: 倒排索引。
        doc_metadata_map: 文档元数据。
        max_results: 最大返回结果数。

    Returns:
        排序后的搜索结果列表。
    """
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    doc_count = len(doc_metadata_map)
    if doc_count == 0:
        return []

    # 计算每个查询词的 IDF
    term_idf = {}
    for qt in query_tokens:
        df = len(inverted_index.get(qt, []))
        term_idf[qt] = math.log(doc_count / (1 + df)) if doc_count > 0 else 0

    # 累计文档分数
    doc_scores = {}
    doc_matches = {}

    for qt in query_tokens:
        postings = inverted_index.get(qt, [])
        idf_val = term_idf.get(qt, 0)

        for posting in postings:
            did = posting["doc_id"]
            tf_val = posting.get("tf", 0)
            score = tf_val * idf_val

            if did not in doc_scores:
                doc_scores[did] = 0.0
                doc_matches[did] = []
            doc_scores[did] += score
            doc_matches[did].append(qt)

    # 排序
    ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    results = []

    for doc_id, score in ranked[:max_results]:
        meta = doc_metadata_map.get(doc_id, {})
        results.append({
            "doc_id": doc_id,
            "path": meta.get("path", ""),
            "filename": os.path.basename(meta.get("path", "")),
            "score": round(score, 4),
            "matched_terms": doc_matches.get(doc_id, []),
            "token_count": meta.get("token_count", 0),
            "indexed_at": meta.get("indexed_at", ""),
        })

    return results


# ============================================================
# 索引持久化
# ============================================================

def _load_index() -> Dict[str, List[Dict[str, Any]]]:
    """加载已有的倒排索引。"""
    data = read_json_file(get_data_file(INDEX_DATA_FILE))
    if isinstance(data, dict):
        return data
    return {}


def _save_index(index: Dict[str, List[Dict[str, Any]]]) -> None:
    """保存倒排索引。"""
    write_json_file(get_data_file(INDEX_DATA_FILE), index)


def _load_doc_metadata() -> Dict[str, Dict[str, Any]]:
    """加载文档元数据。"""
    data = read_json_file(get_data_file(DOC_METADATA_FILE))
    if isinstance(data, dict):
        return data
    return {}


def _save_doc_metadata(metadata: Dict[str, Dict[str, Any]]) -> None:
    """保存文档元数据。"""
    write_json_file(get_data_file(DOC_METADATA_FILE), metadata)


# ============================================================
# 操作实现
# ============================================================

def action_index(data: Dict[str, Any]) -> None:
    """索引本地文件。

    Args:
        data: 包含 paths（目录/文件列表）和可选 patterns（glob 模式）的字典。
    """
    if not require_paid_feature("local_index", "本地知识索引"):
        return

    paths = data.get("paths", [])
    if not paths:
        output_error("请提供待索引的路径列表（paths）", code="VALIDATION_ERROR")
        return

    if isinstance(paths, str):
        paths = [paths]

    patterns = data.get("patterns", DEFAULT_PATTERNS)

    # 扫描文件
    files = _scan_files(paths, patterns)
    if not files:
        output_error("未找到匹配的文件", code="NO_FILES")
        return

    # 读取文件内容
    documents = {}
    file_meta = {}
    skipped = 0

    for filepath in files:
        content = _read_file_content(filepath)
        if content is None:
            skipped += 1
            continue

        doc_id = generate_id("DOC")
        documents[doc_id] = content
        file_meta[doc_id] = {
            "path": filepath,
            "size": os.path.getsize(filepath),
            "indexed_at": now_iso(),
        }

    if not documents:
        output_error("所有文件均无法读取", code="READ_ERROR")
        return

    # 构建索引
    inverted_index, build_meta = _build_inverted_index(documents)

    # 合并到现有索引
    existing_index = _load_index()
    existing_meta = _load_doc_metadata()

    # 合并倒排索引
    for term, postings in inverted_index.items():
        if term not in existing_index:
            existing_index[term] = []
        existing_index[term].extend(postings)

    # 合并元数据
    for doc_id, meta in file_meta.items():
        bm = build_meta.get(doc_id, {})
        existing_meta[doc_id] = {
            **meta,
            "token_count": bm.get("token_count", 0),
            "unique_terms": bm.get("unique_terms", 0),
        }

    # 保存
    _save_index(existing_index)
    _save_doc_metadata(existing_meta)

    output_success({
        "message": f"索引完成：成功 {len(documents)} 个文件，跳过 {skipped} 个",
        "indexed_count": len(documents),
        "skipped_count": skipped,
        "total_terms": len(existing_index),
        "total_documents": len(existing_meta),
    })


def action_search_local(data: Dict[str, Any]) -> None:
    """在本地索引中搜索。

    Args:
        data: 包含 query 的字典，可选 max_results。
    """
    if not require_paid_feature("local_index", "本地知识索引"):
        return

    query = data.get("query", "").strip()
    if not query:
        output_error("请提供搜索关键词（query）", code="VALIDATION_ERROR")
        return

    max_results = data.get("max_results", 20)

    inverted_index = _load_index()
    doc_metadata = _load_doc_metadata()

    if not inverted_index or not doc_metadata:
        output_error("本地索引为空，请先执行 index 操作构建索引", code="NO_INDEX")
        return

    results = _search_index(query, inverted_index, doc_metadata, max_results)

    output_success({
        "query": query,
        "total": len(results),
        "results": results,
    })


def action_list_indexed(data: Optional[Dict[str, Any]] = None) -> None:
    """列出已索引的文档。"""
    doc_metadata = _load_doc_metadata()

    docs = []
    for doc_id, meta in doc_metadata.items():
        docs.append({
            "doc_id": doc_id,
            "path": meta.get("path", ""),
            "filename": os.path.basename(meta.get("path", "")),
            "size": meta.get("size", 0),
            "token_count": meta.get("token_count", 0),
            "indexed_at": meta.get("indexed_at", ""),
        })

    # 按索引时间倒序
    docs.sort(key=lambda d: d.get("indexed_at", ""), reverse=True)

    inverted_index = _load_index()

    output_success({
        "total_documents": len(docs),
        "total_terms": len(inverted_index),
        "documents": docs,
    })


def action_rebuild(data: Optional[Dict[str, Any]] = None) -> None:
    """重建索引：根据已记录的文件路径重新索引。"""
    if not require_paid_feature("local_index", "本地知识索引"):
        return

    doc_metadata = _load_doc_metadata()
    if not doc_metadata:
        output_error("无已索引文档，无需重建", code="NO_INDEX")
        return

    # 收集已有路径
    paths = []
    for meta in doc_metadata.values():
        p = meta.get("path", "")
        if p and os.path.exists(p):
            paths.append(p)

    if not paths:
        output_error("所有已索引文件均不存在，无法重建", code="FILES_MISSING")
        return

    # 清空现有索引
    _save_index({})
    _save_doc_metadata({})

    # 重新读取和索引
    documents = {}
    file_meta = {}
    skipped = 0

    for filepath in paths:
        content = _read_file_content(filepath)
        if content is None:
            skipped += 1
            continue

        doc_id = generate_id("DOC")
        documents[doc_id] = content
        file_meta[doc_id] = {
            "path": filepath,
            "size": os.path.getsize(filepath),
            "indexed_at": now_iso(),
        }

    if not documents:
        output_error("所有文件均无法读取", code="READ_ERROR")
        return

    inverted_index, build_meta = _build_inverted_index(documents)

    # 保存
    final_meta = {}
    for doc_id, meta in file_meta.items():
        bm = build_meta.get(doc_id, {})
        final_meta[doc_id] = {
            **meta,
            "token_count": bm.get("token_count", 0),
            "unique_terms": bm.get("unique_terms", 0),
        }

    _save_index(inverted_index)
    _save_doc_metadata(final_meta)

    output_success({
        "message": f"索引重建完成：成功 {len(documents)} 个文件，跳过 {skipped} 个",
        "indexed_count": len(documents),
        "skipped_count": skipped,
        "total_terms": len(inverted_index),
        "total_documents": len(final_meta),
    })


def action_delete(data: Dict[str, Any]) -> None:
    """删除指定文档的索引。

    Args:
        data: 包含 doc_id 的字典。
    """
    doc_id = data.get("doc_id", "").strip()
    if not doc_id:
        output_error("请提供文档ID（doc_id）", code="VALIDATION_ERROR")
        return

    doc_metadata = _load_doc_metadata()
    if doc_id not in doc_metadata:
        output_error(f"未找到文档: {doc_id}", code="NOT_FOUND")
        return

    # 从元数据中删除
    removed_meta = doc_metadata.pop(doc_id)
    _save_doc_metadata(doc_metadata)

    # 从倒排索引中清除该文档的条目
    inverted_index = _load_index()
    terms_to_remove = []
    for term, postings in inverted_index.items():
        inverted_index[term] = [p for p in postings if p.get("doc_id") != doc_id]
        if not inverted_index[term]:
            terms_to_remove.append(term)

    for term in terms_to_remove:
        del inverted_index[term]

    _save_index(inverted_index)

    output_success({
        "message": f"文档 {doc_id} 的索引已删除",
        "removed_path": removed_meta.get("path", ""),
        "remaining_documents": len(doc_metadata),
        "remaining_terms": len(inverted_index),
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("knowledge-mesh 本地知识索引")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "index": lambda: action_index(data or {}),
        "search-local": lambda: action_search_local(data or {}),
        "list-indexed": lambda: action_list_indexed(data),
        "rebuild": lambda: action_rebuild(data),
        "delete": lambda: action_delete(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
