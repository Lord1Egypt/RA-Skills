#!/usr/bin/env python3
"""memory-guardian: Tag-based routing engine (v0.4.5).

Routes queries to relevant memory files using tag-based routing,
keyword coarse filtering, and dynamic N mechanism.

Usage:
  python3 memory_router.py --query "..." [--workspace <path>] [--top-n <n>]
  python3 memory_router.py --build-index [--workspace <path>]
"""

import argparse
import json
import math
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from mg_utils import load_meta, CST, TAG_DIR_MAP, _DEFAULT_CATEGORY

# ─── Configuration ───────────────────────────────────────────

# Canonical tag categories — single source of truth.
# These MUST match ingest _CLASSIFICATION_RULES primary tags and mg_utils.TAG_DIR_MAP.
CANONICAL_TAGS = ["project", "tech", "social", "personal", "misc"]

# Tag → keywords for routing query matching (broader than ingest classification rules)
TAG_KEYWORDS = {
    "project": ["项目", "project", "计划", "plan", "任务", "task",
                "里程碑", "milestone", "迭代", "sprint", "进度",
                "开发", "编码", "版本", "release", "v0.", "v1.", "skill"],
    "tech": ["技术", "tech", "代码", "code", "bug", "api", "框架",
             "framework", "架构", "architecture", "部署", "deploy",
             "数据库", "database", "缓存", "cache", "算法", "schema",
             "设计模式", "数据结构", "索引", "路由", "测试", "test",
             "debug", "性能优化", "performance", "重构", "refactor"],
    "social": ["社区", "帖子", "评论", "回复", "推广", "讨论", "论坛",
               "instreet", "虾评", "小组帖", "广场帖", "neuro", "SimonClaw",
               "jarvis", "skilly", "人", "person", "朋友", "friend",
               "同事", "colleague", "关系", "relationship", "沟通"],
    "personal": ["偏好", "preference", "喜欢", "like", "习惯", "habit",
                 "不喜欢", "dislike", "风格", "style", "讨厌", "hate",
                 "日常", "个人", "风清", "owner", "偏好设置", "作息"],
}

# Subdirectory mapping — derived from TAG_DIR_MAP (single source of truth)
TAG_SUBDIRS = {}
for _tag, _dir in TAG_DIR_MAP.items():
    TAG_SUBDIRS[_dir] = f"memory/{_dir}"
TAG_SUBDIRS["misc"] = f"memory/{_DEFAULT_CATEGORY}"

# Dynamic N configuration
MAX_CATEGORIES = 3
BUDGET_HIGH = 0.4   # >40% budget → load 3 categories
BUDGET_LOW = 0.2    # <20% budget → load 1 category
# else → load 2 categories

# Routing log max entries
ROUTING_LOG_MAX = 50

# Minimum tag match score to include a category
MIN_TAG_SCORE = 0.1


def _extract_tokens(text):
    """Extract indexable tokens from text.

    Chinese chars → bigrams; English words → lowercase.
    """
    tokens = []
    # Split into Chinese and non-Chinese segments
    for segment in re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z0-9]+', text):
        if re.match(r'[\u4e00-\u9fff]+', segment):
            # Chinese: bigrams
            chars = segment
            for i in range(len(chars) - 1):
                tokens.append(chars[i:i+2])
            if len(chars) == 1:
                tokens.append(chars)
        else:
            if len(segment) >= 2:
                tokens.append(segment.lower())
    return tokens


# ─── Index Building ──────────────────────────────────────────

def build_inverted_index(meta, workspace):
    """Build inverted index from meta.json entries.

    Returns:
        dict: {keyword: [memory_ids...]}
        dict: {tag: [memory_ids...]}
        dict: {memory_id: tag_info}
    """
    inverted = defaultdict(list)
    tag_index = defaultdict(list)
    tag_info = {}

    for mem in meta.get("memories", []):
        mid = mem.get("id", "")
        if not mid:
            continue

        tags = mem.get("tags", [])
        content = mem.get("content", "").lower()
        file_path = mem.get("file_path", "")

        # Primary tag from classification or first tag
        primary = None
        classification = mem.get("classification", {})
        if isinstance(classification, dict):
            primary = classification.get("primary_tag")
        if not primary and tags:
            primary = tags[0]
        if not primary:
            primary = "misc"

        tag_info[mid] = {
            "primary_tag": primary,
            "tags": tags,
            "file_path": file_path,
            "decay_score": mem.get("decay_score", 0.5),
            "last_accessed": mem.get("last_accessed", ""),
            "access_count": mem.get("access_count", 0),
            "signal_level": mem.get("signal_level", "none"),
            "reactivation_count": mem.get("reactivation_count", 0),
        }

        # Index by tag
        for tag in tags:
            tag_index[tag].append(mid)
        if primary not in tag_index or mid not in tag_index[primary]:
            tag_index[primary].append(mid)

        # Index by content keywords (extract significant words)
        # Chinese: split into bigrams; English: split by non-word chars
        words = _extract_tokens(content)
        for word in set(words):
            inverted[word].append(mid)

    return dict(inverted), dict(tag_index), tag_info


def build_category_activity(meta):
    """Compute activity scores per category (tag).

    Activity = weighted sum of recent access signals.

    Returns:
        dict: {tag: activity_score}
    """
    activity = defaultdict(float)
    now = datetime.now(CST)

    for mem in meta.get("memories", []):
        classification = mem.get("classification", {})
        primary = None
        if isinstance(classification, dict):
            primary = classification.get("primary_tag")
        if not primary:
            tags = mem.get("tags", [])
            primary = tags[0] if tags else "misc"

        # Access count contributes to activity
        access_count = mem.get("access_count", 0)
        reactivation_count = mem.get("reactivation_count", 0)

        # Recent access bonus
        last_accessed = mem.get("last_accessed", "")
        recency_bonus = 0.0
        if last_accessed:
            try:
                dt = datetime.fromisoformat(last_accessed)
                hours_ago = (now - dt).total_seconds() / 3600
                if hours_ago < 0:
                    hours_ago = 0
                # Exponential decay: 1.0 at 0h, ~0.5 at 24h
                recency_bonus = math.exp(-hours_ago / 48)
            except (ValueError, TypeError):
                pass

        activity[primary] += (access_count * 0.1 + reactivation_count * 0.3
                              + recency_bonus * 0.5)

    return dict(activity)


# ─── Routing Logic ───────────────────────────────────────────

def _score_tag_match(query, tag):
    """Score how well a query matches a tag.

    Uses TAG_KEYWORDS for keyword matching.

    Returns:
        float: Score in [0.0, 1.0]
    """
    query_lower = query.lower()
    keywords = TAG_KEYWORDS.get(tag, [])

    if not keywords:
        return 0.0

    matches = sum(1 for kw in keywords if kw.lower() in query_lower)
    if matches == 0:
        return 0.0
    # Score: at least 1 match gives MIN_TAG_SCORE, scales up
    # Use log to avoid large keyword lists penalizing single matches
    score = 0.2 + 0.8 * min(matches / 3.0, 1.0)  # 1 match → 0.47, 3+ → 1.0
    return round(score, 4)


def _score_content_relevance(query, memory_ids, inverted_index):
    """Score content relevance for a set of memory IDs.

    Returns:
        float: Average relevance score.
    """
    if not memory_ids:
        return 0.0

    query_words = set(_extract_tokens(query))
    if not query_words:
        return 0.1  # Minimum score for non-empty result set

    total_score = 0.0
    for mid in memory_ids:
        hits = sum(1 for word in query_words if mid in inverted_index.get(word, []))
        score = hits / max(len(query_words), 1)
        total_score += score

    return total_score / len(memory_ids)


def compute_dynamic_n(token_budget_ratio):
    """Compute how many categories to load based on token budget.

    Args:
        token_budget_ratio: Available budget as ratio (0.0 to 1.0).

    Returns:
        int: Number of categories (1, 2, or 3).
    """
    if token_budget_ratio > BUDGET_HIGH:
        return MAX_CATEGORIES
    elif token_budget_ratio < BUDGET_LOW:
        return 1
    else:
        return 2


def route(query, meta, workspace, token_budget_ratio=0.5, top_n=None):
    """Route a query to relevant memory categories.

    Args:
        query: User query or task description.
        meta: Loaded meta.json dict.
        workspace: Workspace root path.
        token_budget_ratio: Available context budget ratio (0.0-1.0).
        top_n: Override dynamic N (None = use budget).

    Returns:
        dict: Routing result with categories, files, and log.
    """
    now = datetime.now(CST).isoformat()

    # Build indices
    inverted_index, tag_index, tag_info = build_inverted_index(meta, workspace)
    activity = build_category_activity(meta)

    # Score all categories
    category_scores = {}
    for tag in TAG_KEYWORDS:
        tag_score = _score_tag_match(query, tag)
        if tag_score < MIN_TAG_SCORE:
            continue

        # Content relevance bonus
        memory_ids = tag_index.get(tag, [])
        content_score = _score_content_relevance(query, memory_ids, inverted_index)

        # Activity bonus
        act = activity.get(tag, 0.0)
        activity_bonus = min(act / 10.0, 0.3)  # Cap activity bonus at 0.3

        # Combined score: tag match (40%) + content (30%) + activity (30%)
        combined = tag_score * 0.4 + content_score * 0.3 + activity_bonus
        category_scores[tag] = round(combined, 4)

    # Sort by score descending
    sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)

    # Determine N (dynamic or override)
    n = top_n if top_n is not None else compute_dynamic_n(token_budget_ratio)
    n = min(n, len(sorted_categories))

    # Select top-N categories
    selected = sorted_categories[:n]

    # Collect files to load
    files_to_load = []
    seen_files = set()
    for tag, score in selected:
        subdir = TAG_SUBDIRS.get(tag, f"memory/{tag}")
        full_subdir = os.path.join(workspace, subdir)

        # Add subdirectory files
        if os.path.isdir(full_subdir):
            for fname in sorted(os.listdir(full_subdir)):
                if fname.endswith(".md") and not fname.startswith("_"):
                    fpath = os.path.join(subdir, fname)
                    if fpath not in seen_files:
                        files_to_load.append(fpath)
                        seen_files.add(fpath)

        # Also add memory files referenced in tag_info
        for mid, info in tag_info.items():
            if info.get("primary_tag") == tag and info.get("file_path"):
                fp = info["file_path"]
                if fp not in seen_files and os.path.exists(os.path.join(workspace, fp)):
                    files_to_load.append(fp)
                    seen_files.add(fp)

    # Build routing log entry
    log_entry = {
        "timestamp": now,
        "query_preview": query[:80],
        "token_budget_ratio": token_budget_ratio,
        "dynamic_n": n,
        "all_scores": dict(sorted_categories),
        "selected": [(tag, score) for tag, score in selected],
        "files_count": len(files_to_load),
    }

    return {
        "query": query,
        "categories": selected,
        "files": files_to_load,
        "dynamic_n": n,
        "scores": category_scores,
        "log": log_entry,
    }


def append_routing_log(meta_path, log_entry):
    """Append a routing log entry to meta.json.

    Keeps only last ROUTING_LOG_MAX entries.
    """
    meta = load_meta(meta_path)
    logs = meta.get("routing_log", [])
    logs.append(log_entry)
    if len(logs) > ROUTING_LOG_MAX:
        meta["routing_log"] = logs[-ROUTING_LOG_MAX:]
    else:
        meta["routing_log"] = logs

    from mg_utils import save_meta
    save_meta(meta_path, meta)


# ─── CLI ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Memory routing engine")
    parser.add_argument("--query", "-q", help="Query to route")
    parser.add_argument("--workspace", "-w", default=".",
                        help="Workspace root path")
    parser.add_argument("--top-n", "-n", type=int, default=None,
                        help="Override dynamic N")
    parser.add_argument("--budget", "-b", type=float, default=0.5,
                        help="Token budget ratio (0.0-1.0)")
    parser.add_argument("--build-index", action="store_true",
                        help="Build and display index stats")

    args = parser.parse_args()
    meta_path = os.path.join(args.workspace, "meta.json")

    if not os.path.exists(meta_path):
        print(f"Error: meta.json not found at {meta_path}")
        sys.exit(1)

    meta = load_meta(meta_path)

    if args.build_index:
        inverted, tag_idx, tag_info = build_inverted_index(meta, args.workspace)
        activity = build_category_activity(meta)
        print(f"Inverted index: {len(inverted)} keywords")
        print(f"Tag index: {len(tag_idx)} tags")
        print(f"Tagged memories: {len(tag_info)}")
        print(f"\nCategory activity:")
        for tag, score in sorted(activity.items(), key=lambda x: x[1], reverse=True):
            count = len(tag_idx.get(tag, []))
            print(f"  {tag}: {score:.2f} ({count} memories)")
        return

    if args.query:
        result = route(args.query, meta, args.workspace,
                       args.budget, args.top_n)
        print(f"Query: {result['query'][:80]}")
        print(f"Dynamic N: {result['dynamic_n']}")
        print(f"\nCategory scores:")
        for tag, score in sorted(result['scores'].items(),
                                  key=lambda x: x[1], reverse=True):
            selected = " ✓" if (tag, score) in result['categories'] else ""
            print(f"  {tag}: {score:.4f}{selected}")
        print(f"\nFiles to load ({len(result['files'])}):")
        for f in result['files']:
            print(f"  {f}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
