#!/usr/bin/env python3
"""
project-nerve 自学习引擎

从操作记录中持续学习，记录错误、成功模式和用户纠正，
并基于积累的数据提供改进建议和统计分析。

灵感来源: self-improving-agent (255K 下载量)
"""

import json
import os
import sys
import hashlib
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
)


# ============================================================
# 数据文件路径
# ============================================================

LEARNING_FILE = "learning.json"


# ============================================================
# 数据读写
# ============================================================

def _get_learning_data() -> Dict[str, Any]:
    """读取学习数据文件。

    Returns:
        包含 patterns 列表的字典。
    """
    data = read_json_file(get_data_file(LEARNING_FILE))
    if isinstance(data, dict) and "patterns" in data:
        return data
    return {"patterns": [], "metadata": {"created_at": now_iso(), "version": "1.0"}}


def _save_learning_data(data: Dict[str, Any]) -> None:
    """保存学习数据到文件。

    Args:
        data: 学习数据字典。
    """
    data["metadata"] = data.get("metadata", {})
    data["metadata"]["updated_at"] = now_iso()
    write_json_file(get_data_file(LEARNING_FILE), data)


# ============================================================
# 模式指纹计算（用于聚合相似模式）
# ============================================================

def _compute_fingerprint(pattern_type: str, category: str, context: Dict[str, Any]) -> str:
    """计算模式指纹，用于识别和聚合相似的模式。

    基于类型、分类和关键上下文信息生成哈希指纹。
    相同指纹的模式会被聚合（计数递增）而非重复存储。

    Args:
        pattern_type: 模式类型（error / success / correction）。
        category: 分类标签（如 api_failure, platform_choice 等）。
        context: 上下文字典，包含与模式相关的详细信息。

    Returns:
        16 位十六进制指纹字符串。
    """
    # 提取用于指纹计算的关键字段
    key_parts = [pattern_type, category]

    # 根据不同类型提取不同的关键信息
    if pattern_type == "error":
        key_parts.append(context.get("source", ""))
        key_parts.append(context.get("error_type", ""))
        key_parts.append(context.get("action", ""))
    elif pattern_type == "success":
        key_parts.append(context.get("source", ""))
        key_parts.append(context.get("action", ""))
        key_parts.append(context.get("task_type", ""))
    elif pattern_type == "correction":
        key_parts.append(context.get("field", ""))
        key_parts.append(context.get("original_value", ""))
        key_parts.append(context.get("corrected_value", ""))

    raw = "|".join(str(p) for p in key_parts)
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:16]


# ============================================================
# 模式匹配与聚合
# ============================================================

def _find_matching_pattern(
    patterns: List[Dict[str, Any]], fingerprint: str
) -> Optional[int]:
    """查找与指纹匹配的已有模式索引。

    Args:
        patterns: 模式列表。
        fingerprint: 待匹配的指纹。

    Returns:
        匹配的模式在列表中的索引，未找到返回 None。
    """
    for i, p in enumerate(patterns):
        if p.get("fingerprint") == fingerprint:
            return i
    return None


def _record_pattern(
    pattern_type: str,
    category: str,
    context: Dict[str, Any],
    lesson: str,
) -> Dict[str, Any]:
    """记录一条学习模式。

    若已存在指纹相同的模式，则递增计数并更新时间戳；
    否则创建新的模式记录。

    Args:
        pattern_type: 模式类型（error / success / correction）。
        category: 分类标签。
        context: 上下文信息。
        lesson: 从该模式中总结的经验教训。

    Returns:
        记录的模式字典。
    """
    data = _get_learning_data()
    patterns = data["patterns"]

    fingerprint = _compute_fingerprint(pattern_type, category, context)
    existing_idx = _find_matching_pattern(patterns, fingerprint)

    if existing_idx is not None:
        # 聚合：递增计数，更新时间戳
        patterns[existing_idx]["count"] += 1
        patterns[existing_idx]["last_seen"] = now_iso()
        # 如果提供了新的经验教训，更新之
        if lesson and lesson != patterns[existing_idx].get("lesson", ""):
            patterns[existing_idx]["lesson"] = lesson
        pattern = patterns[existing_idx]
    else:
        # 创建新模式
        now = now_iso()
        pattern = {
            "id": generate_id("LRN"),
            "type": pattern_type,
            "category": category,
            "context": context,
            "lesson": lesson,
            "fingerprint": fingerprint,
            "count": 1,
            "first_seen": now,
            "last_seen": now,
        }
        patterns.append(pattern)

    data["patterns"] = patterns
    _save_learning_data(data)
    return pattern


# ============================================================
# 操作实现：记录错误
# ============================================================

def record_error(data: Dict[str, Any]) -> None:
    """记录操作中遇到的错误。

    用于追踪 API 失败、超时、解析错误等问题模式。
    相同来源和类型的错误会被聚合计数。

    必填字段: category（错误分类，如 api_failure / timeout / parse_error）
    可选字段: source（平台名称）, error_type（具体错误类型）,
              action（触发错误的操作）, message（错误详情）, lesson（经验总结）

    Args:
        data: 错误信息字典。
    """
    category = data.get("category", "").strip()
    if not category:
        output_error("错误分类（category）为必填字段", code="VALIDATION_ERROR")
        return

    context = {
        "source": data.get("source", ""),
        "error_type": data.get("error_type", ""),
        "action": data.get("action", ""),
        "message": data.get("message", ""),
    }
    lesson = data.get("lesson", "")

    pattern = _record_pattern("error", category, context, lesson)

    output_success({
        "message": f"已记录错误模式: {category}",
        "pattern_id": pattern["id"],
        "count": pattern["count"],
        "aggregated": pattern["count"] > 1,
    })


# ============================================================
# 操作实现：记录成功
# ============================================================

def record_success(data: Dict[str, Any]) -> None:
    """记录成功的操作模式。

    用于追踪有效的平台选择、成功的查询方式等。
    帮助系统学习哪些操作在什么场景下效果最好。

    必填字段: category（成功分类，如 platform_choice / query_pattern / fetch_success）
    可选字段: source（平台名称）, action（操作类型）,
              task_type（任务类型）, details（详细信息）, lesson（经验总结）

    Args:
        data: 成功信息字典。
    """
    category = data.get("category", "").strip()
    if not category:
        output_error("成功分类（category）为必填字段", code="VALIDATION_ERROR")
        return

    context = {
        "source": data.get("source", ""),
        "action": data.get("action", ""),
        "task_type": data.get("task_type", ""),
        "details": data.get("details", ""),
    }
    lesson = data.get("lesson", "")

    pattern = _record_pattern("success", category, context, lesson)

    output_success({
        "message": f"已记录成功模式: {category}",
        "pattern_id": pattern["id"],
        "count": pattern["count"],
        "aggregated": pattern["count"] > 1,
    })


# ============================================================
# 操作实现：记录用户纠正
# ============================================================

def record_correction(data: Dict[str, Any]) -> None:
    """记录用户对自动行为的纠正。

    当用户覆盖自动检测结果（如更改推荐平台、调整优先级）时记录，
    帮助系统逐步学习用户偏好。

    必填字段: category（纠正分类，如 platform_override / priority_change）
    可选字段: field（被纠正的字段名）, original_value（原始值）,
              corrected_value（纠正后的值）, reason（纠正原因）, lesson（经验总结）

    Args:
        data: 纠正信息字典。
    """
    category = data.get("category", "").strip()
    if not category:
        output_error("纠正分类（category）为必填字段", code="VALIDATION_ERROR")
        return

    context = {
        "field": data.get("field", ""),
        "original_value": data.get("original_value", ""),
        "corrected_value": data.get("corrected_value", ""),
        "reason": data.get("reason", ""),
    }
    lesson = data.get("lesson", "")

    pattern = _record_pattern("correction", category, context, lesson)

    output_success({
        "message": f"已记录用户纠正: {category}",
        "pattern_id": pattern["id"],
        "count": pattern["count"],
        "aggregated": pattern["count"] > 1,
    })


# ============================================================
# 操作实现：建议
# ============================================================

def _generate_error_suggestions(patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """基于错误模式生成改进建议。

    分析高频错误，识别问题集中的平台和操作，
    提出针对性的改进建议。

    Args:
        patterns: 错误类型的模式列表。

    Returns:
        建议列表，每项包含 type、message、severity、based_on。
    """
    suggestions = []
    if not patterns:
        return suggestions

    # 按平台统计错误次数
    source_errors: Dict[str, int] = {}
    for p in patterns:
        src = p.get("context", {}).get("source", "未知")
        source_errors[src] = source_errors.get(src, 0) + p.get("count", 1)

    # 找出错误最多的平台
    if source_errors:
        worst_source = max(source_errors, key=source_errors.get)  # type: ignore
        worst_count = source_errors[worst_source]
        if worst_count >= 3:
            # 找到可替代的平台
            all_sources = list(source_errors.keys())
            alternatives = [s for s in all_sources if s != worst_source and source_errors[s] < worst_count // 2]
            alt_text = ""
            if alternatives:
                alt_text = f"，建议优先使用 {alternatives[0]}"
            suggestions.append({
                "type": "reliability",
                "message": f"{worst_source} 的 API 最近频繁出错（{worst_count} 次）{alt_text}",
                "severity": "高" if worst_count >= 5 else "中",
                "based_on": f"{worst_count} 次错误记录",
            })

    # 按错误类型统计
    error_types: Dict[str, int] = {}
    for p in patterns:
        et = p.get("context", {}).get("error_type", "")
        if et:
            error_types[et] = error_types.get(et, 0) + p.get("count", 1)

    # 超时相关建议
    timeout_count = error_types.get("timeout", 0)
    if timeout_count >= 2:
        suggestions.append({
            "type": "performance",
            "message": f"检测到 {timeout_count} 次超时，建议检查网络连接或增加超时设置",
            "severity": "中",
            "based_on": f"{timeout_count} 次超时记录",
        })

    # 认证相关建议
    auth_count = error_types.get("auth_failure", 0) + error_types.get("unauthorized", 0)
    if auth_count >= 1:
        suggestions.append({
            "type": "configuration",
            "message": f"检测到 {auth_count} 次认证失败，建议检查 API 密钥是否过期",
            "severity": "高",
            "based_on": f"{auth_count} 次认证错误",
        })

    return suggestions


def _generate_correction_suggestions(patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """基于用户纠正模式生成偏好建议。

    分析用户经常覆盖的自动决策，识别用户偏好，
    提出自动化改进建议。

    Args:
        patterns: 纠正类型的模式列表。

    Returns:
        建议列表。
    """
    suggestions = []
    if not patterns:
        return suggestions

    # 分析平台覆盖模式
    platform_overrides: Dict[str, Dict[str, int]] = {}
    for p in patterns:
        ctx = p.get("context", {})
        if ctx.get("field") == "platform" or p.get("category") == "platform_override":
            original = ctx.get("original_value", "")
            corrected = ctx.get("corrected_value", "")
            if original and corrected:
                key = f"{original}->{corrected}"
                if key not in platform_overrides:
                    platform_overrides[key] = {"count": 0, "original": original, "corrected": corrected}
                platform_overrides[key]["count"] += p.get("count", 1)

    # 生成平台偏好建议
    for key, info in platform_overrides.items():
        if info["count"] >= 2:
            suggestions.append({
                "type": "preference",
                "message": (
                    f"用户倾向于将任务从 {info['original']} 改到 {info['corrected']}"
                    f"（已纠正 {info['count']} 次），建议调整自动检测逻辑"
                ),
                "severity": "低",
                "based_on": f"{info['count']} 次平台覆盖",
            })

    # 分析优先级纠正模式
    priority_corrections = [
        p for p in patterns
        if p.get("context", {}).get("field") == "priority" or p.get("category") == "priority_change"
    ]
    total_prio_corrections = sum(p.get("count", 1) for p in priority_corrections)
    if total_prio_corrections >= 3:
        suggestions.append({
            "type": "preference",
            "message": f"用户经常调整任务优先级（共 {total_prio_corrections} 次），建议优化优先级自动判断逻辑",
            "severity": "中",
            "based_on": f"{total_prio_corrections} 次优先级纠正",
        })

    return suggestions


def _generate_success_suggestions(patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """基于成功模式生成优化建议。

    分析高效的操作模式，提炼可复用的最佳实践。

    Args:
        patterns: 成功类型的模式列表。

    Returns:
        建议列表。
    """
    suggestions = []
    if not patterns:
        return suggestions

    # 找出使用最频繁的成功平台
    source_success: Dict[str, int] = {}
    for p in patterns:
        src = p.get("context", {}).get("source", "")
        if src:
            source_success[src] = source_success.get(src, 0) + p.get("count", 1)

    if source_success:
        best_source = max(source_success, key=source_success.get)  # type: ignore
        best_count = source_success[best_source]
        if best_count >= 5:
            suggestions.append({
                "type": "optimization",
                "message": f"{best_source} 是最常成功使用的平台（{best_count} 次），可作为默认首选",
                "severity": "低",
                "based_on": f"{best_count} 次成功记录",
            })

    return suggestions


def suggest(data: Optional[Dict[str, Any]] = None) -> None:
    """基于积累的学习数据生成改进建议。

    分析错误模式、用户纠正和成功模式，综合生成
    可操作的改进建议。

    可选字段: type（过滤建议类型: error / correction / success / all）

    Args:
        data: 可选的过滤参数。
    """
    # 检查订阅（高级建议为付费功能）
    sub = check_subscription()
    is_paid = sub["tier"] == "paid"

    learning = _get_learning_data()
    patterns = learning.get("patterns", [])

    if not patterns:
        output_success({
            "message": "暂无学习数据，请在使用过程中积累操作记录后再查看建议",
            "suggestions": [],
            "total_patterns": 0,
        })
        return

    # 按类型分组
    errors = [p for p in patterns if p.get("type") == "error"]
    successes = [p for p in patterns if p.get("type") == "success"]
    corrections = [p for p in patterns if p.get("type") == "correction"]

    # 生成建议
    filter_type = ""
    if data:
        filter_type = data.get("type", "").strip().lower()

    all_suggestions = []

    if not filter_type or filter_type in ("error", "all"):
        all_suggestions.extend(_generate_error_suggestions(errors))

    if not filter_type or filter_type in ("correction", "all"):
        if is_paid:
            all_suggestions.extend(_generate_correction_suggestions(corrections))
        elif corrections:
            all_suggestions.append({
                "type": "upgrade_hint",
                "message": f"检测到 {len(corrections)} 条用户纠正记录，升级付费版可获得个性化偏好建议",
                "severity": "低",
                "based_on": f"{len(corrections)} 条纠正记录",
            })

    if not filter_type or filter_type in ("success", "all"):
        if is_paid:
            all_suggestions.extend(_generate_success_suggestions(successes))

    # 按严重程度排序
    severity_order = {"高": 0, "中": 1, "低": 2}
    all_suggestions.sort(key=lambda s: severity_order.get(s.get("severity", "低"), 2))

    output_success({
        "message": f"基于 {len(patterns)} 条学习记录生成了 {len(all_suggestions)} 条建议",
        "total_patterns": len(patterns),
        "pattern_breakdown": {
            "errors": len(errors),
            "successes": len(successes),
            "corrections": len(corrections),
        },
        "suggestions": all_suggestions,
    })


# ============================================================
# 操作实现：统计
# ============================================================

def stats(data: Optional[Dict[str, Any]] = None) -> None:
    """显示学习数据统计信息。

    展示错误率、常见模式、纠正频率等统计数据，
    帮助了解系统的学习进度和数据质量。

    可选字段: type（按类型过滤: error / success / correction）

    Args:
        data: 可选的过滤参数。
    """
    learning = _get_learning_data()
    patterns = learning.get("patterns", [])

    if not patterns:
        output_success({
            "message": "暂无学习数据",
            "total_patterns": 0,
            "stats": {},
        })
        return

    # 基本统计
    type_counts = {"error": 0, "success": 0, "correction": 0}
    type_total_events = {"error": 0, "success": 0, "correction": 0}
    source_stats: Dict[str, Dict[str, int]] = {}
    category_stats: Dict[str, int] = {}

    for p in patterns:
        ptype = p.get("type", "unknown")
        count = p.get("count", 1)

        if ptype in type_counts:
            type_counts[ptype] += 1
            type_total_events[ptype] += count

        # 按来源统计
        src = p.get("context", {}).get("source", "未指定")
        if src not in source_stats:
            source_stats[src] = {"error": 0, "success": 0, "correction": 0, "total": 0}
        if ptype in source_stats[src]:
            source_stats[src][ptype] += count
        source_stats[src]["total"] += count

        # 按分类统计
        cat = p.get("category", "未分类")
        category_stats[cat] = category_stats.get(cat, 0) + count

    # 计算错误率
    total_events = sum(type_total_events.values())
    error_rate = 0.0
    if total_events > 0:
        error_rate = round(type_total_events["error"] / total_events * 100, 1)

    # 每个来源的错误率
    source_error_rates: Dict[str, float] = {}
    for src, st in source_stats.items():
        if st["total"] > 0:
            source_error_rates[src] = round(st["error"] / st["total"] * 100, 1)

    # 最常见的模式（按计数排序）
    top_patterns = sorted(patterns, key=lambda p: p.get("count", 1), reverse=True)[:10]
    top_summary = []
    for p in top_patterns:
        top_summary.append({
            "type": p.get("type", ""),
            "category": p.get("category", ""),
            "count": p.get("count", 1),
            "source": p.get("context", {}).get("source", ""),
            "lesson": p.get("lesson", ""),
        })

    # 时间范围
    first_seen_dates = [p.get("first_seen", "") for p in patterns if p.get("first_seen")]
    last_seen_dates = [p.get("last_seen", "") for p in patterns if p.get("last_seen")]
    time_range = {}
    if first_seen_dates:
        time_range["earliest"] = min(first_seen_dates)
    if last_seen_dates:
        time_range["latest"] = max(last_seen_dates)

    result = {
        "message": f"共有 {len(patterns)} 个独立模式，{total_events} 次事件记录",
        "total_patterns": len(patterns),
        "total_events": total_events,
        "type_breakdown": {
            "patterns": type_counts,
            "events": type_total_events,
        },
        "error_rate": f"{error_rate}%",
        "source_stats": source_stats,
        "source_error_rates": source_error_rates,
        "top_categories": dict(sorted(category_stats.items(), key=lambda x: x[1], reverse=True)[:10]),
        "top_patterns": top_summary,
        "time_range": time_range,
    }

    output_success(result)


# ============================================================
# 操作实现：重置
# ============================================================

def reset(data: Optional[Dict[str, Any]] = None) -> None:
    """重置学习数据。

    可选择重置全部数据或仅重置指定类型的数据。
    此操作不可撤销。

    可选字段: type（仅重置指定类型: error / success / correction）,
              confirm（确认重置，必须为 true）

    Args:
        data: 可选参数。
    """
    if not data or not data.get("confirm"):
        output_error(
            "重置操作不可撤销，请传入 confirm: true 确认操作",
            code="CONFIRMATION_REQUIRED",
        )
        return

    filter_type = ""
    if data:
        filter_type = data.get("type", "").strip().lower()

    learning = _get_learning_data()
    patterns = learning.get("patterns", [])
    original_count = len(patterns)

    if filter_type and filter_type in ("error", "success", "correction"):
        # 仅删除指定类型
        patterns = [p for p in patterns if p.get("type") != filter_type]
        removed = original_count - len(patterns)
        learning["patterns"] = patterns
        _save_learning_data(learning)
        output_success({
            "message": f"已重置 {filter_type} 类型的学习数据，移除 {removed} 条记录",
            "removed": removed,
            "remaining": len(patterns),
        })
    else:
        # 重置全部
        learning["patterns"] = []
        _save_learning_data(learning)
        output_success({
            "message": f"已重置全部学习数据，移除 {original_count} 条记录",
            "removed": original_count,
            "remaining": 0,
        })


# ============================================================
# 便捷 API（供其他模块调用）
# ============================================================

def quick_record_error(source: str, action: str, error_type: str, message: str) -> None:
    """快速记录错误（供其他脚本内部调用的便捷方法）。

    Args:
        source: 平台来源。
        action: 触发错误的操作。
        error_type: 错误类型。
        message: 错误信息。
    """
    try:
        context = {
            "source": source,
            "error_type": error_type,
            "action": action,
            "message": message,
        }
        _record_pattern("error", error_type, context, message)
    except Exception:
        # 学习记录失败不应影响主流程
        pass


def quick_record_success(source: str, action: str, task_type: str = "") -> None:
    """快速记录成功（供其他脚本内部调用的便捷方法）。

    Args:
        source: 平台来源。
        action: 操作类型。
        task_type: 任务类型。
    """
    try:
        context = {
            "source": source,
            "action": action,
            "task_type": task_type,
        }
        _record_pattern("success", "operation_success", context, "")
    except Exception:
        # 学习记录失败不应影响主流程
        pass


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("project-nerve 自学习引擎")
    args = parser.parse_args()

    action = args.action.lower().replace("-", "_")

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "record_error": lambda: record_error(data or {}),
        "record_success": lambda: record_success(data or {}),
        "record_correction": lambda: record_correction(data or {}),
        "suggest": lambda: suggest(data),
        "stats": lambda: stats(data),
        "reset": lambda: reset(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join([
            "record-error", "record-success", "record-correction",
            "suggest", "stats", "reset",
        ])
        output_error(
            f"未知操作: {args.action}，支持的操作: {valid_actions}",
            code="INVALID_ACTION",
        )


if __name__ == "__main__":
    main()
