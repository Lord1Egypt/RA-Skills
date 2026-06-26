#!/usr/bin/env python3
"""
MySQL Slow Query Analyzer - Suggestions Module
索引建议 | SQL 重写建议 | 性能指标计算
"""

import re
from typing import List, Dict, Any

from analyzer_parser import extract_conditions, _extract_join_columns


# ==================== 索引建议 ====================

def generate_index_suggestions(sql: str) -> List[str]:
    """
    根据 SQL 生成索引建议
    """
    if not sql.strip():
        return []

    suggestions = []

    # 1. WHERE 列
    where_cols = extract_conditions(sql)
    for col in where_cols:
        suggestions.append(f"📇 INDEX 建议: 在表上添加 INDEX idx_{col} ({col})")

    # 2. JOIN 列
    join_cols = _extract_join_columns(sql)
    for col in join_cols:
        if col.lower() not in [c.lower() for c in where_cols]:
            suggestions.append(f"🔗 JOIN 索引: 在 {col} 列建立索引优化连接")

    # 3. ORDER BY 列
    order_match = re.search(r'\bORDER BY\b\s+(.+?)(?:\bLIMIT\b|GROUP BY|HAVING|$)', sql, re.IGNORECASE | re.DOTALL)
    if order_match:
        order_cols_raw = order_match.group(1).strip()
        order_cols = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)(?:\s+(?:ASC|DESC))?', order_cols_raw, re.IGNORECASE)
        for col in order_cols:
            suggestions.append(f"📑 ORDER BY 索引: 在 {col} 列建立索引消除 filesort")

    # 4. GROUP BY 列
    group_match = re.search(r'\bGROUP BY\b\s+(.+?)(?:\bHAVING\b|\bORDER BY\b|\bLIMIT\b|$)', sql, re.IGNORECASE | re.DOTALL)
    if group_match:
        group_cols = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)', group_match.group(1), re.IGNORECASE)
        for col in group_cols:
            if col.lower() not in [c.lower() for c in where_cols]:
                suggestions.append(f"📊 GROUP BY 索引: 在 {col} 列建立索引")

    # 5. SELECT * 建议
    if re.search(r'\bSELECT\s+\*', sql, re.IGNORECASE):
        table_match = re.search(r'\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*)', sql, re.IGNORECASE)
        table = table_match.group(1) if table_match else "TABLE"
        all_cols = list(set(where_cols))
        if all_cols:
            suggestions.append(
                f"✅ 覆盖索引: CREATE INDEX idx_covering ON {table}("
                + ", ".join(all_cols) + "); -- 覆盖查询避免回表"
            )

    # 去重
    seen = set()
    unique = []
    for s in suggestions:
        if s not in seen:
            seen.add(s)
            unique.append(s)
    return unique


# ==================== SQL 重写建议 ====================

def generate_rewrite_suggestions(sql: str) -> List[str]:
    """
    根据 SQL 生成重写建议
    """
    if not sql.strip():
        return []

    suggestions = []
    sql_upper = sql.upper()

    # 1. SELECT * → 指定列
    if re.search(r'\bSELECT\s+\*', sql_upper):
        table_match = re.search(r'\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*)', sql, re.IGNORECASE)
        table = table_match.group(1) if table_match else "TABLE"
        suggestions.append(
            "🔧 避免 SELECT *: 改为 SELECT column1, column2 FROM " + table
            + " -- 减少网络传输和内存占用"
        )

    # 2. OR → UNION
    or_match = re.search(r'\bWHERE\b\s+(.+?)\s+\bOR\b\s+(.+)', sql, re.IGNORECASE | re.DOTALL)
    if or_match:
        left = or_match.group(1).strip()
        right = or_match.group(2).strip()
        col_match = re.search(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', left)
        if col_match:
            col = col_match.group(1)
            val_match = re.search(r'=\s*([^\s;]+)', right)
            if val_match:
                val = val_match.group(1)
                suggestions.append(
                    f"🔧 OR → UNION: WHERE {col} = value1 UNION SELECT ... WHERE {col} = {val}"
                    " -- UNION 可利用索引，OR 不能"
                )

    # 3. 隐式类型转换
    type_conv_match = re.search(
        r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\'([^\']+)\'',
        sql
    )
    if type_conv_match:
        type_match = re.search(
            r'([a-zA-Z_][a-zA-Z0-9_]*)_id\s*=\s*\'([^\']+)\'', sql
        )
        col = type_match.group(1) if type_match else type_conv_match.group(1)
        if col:
            suggestions.append(
                f"🔧 隐式类型转换: {col} = 'value' (字符串) → {col} = value (数字)"
                " -- 避免类型转换导致索引失效"
            )

    # 4. 大 OFFSET 分页
    offset_match = re.search(r'\bLIMIT\s+(\d+)\s*,\s*(\d+)', sql, re.IGNORECASE)
    if offset_match:
        offset = int(offset_match.group(1))
        page_size = int(offset_match.group(2))
        if offset > 1000:
            table_match = re.search(r'\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*)', sql, re.IGNORECASE)
            table = table_match.group(1) if table_match else "TABLE"
            suggestions.append(
                f"🔧 深度分页优化: LIMIT {offset}, {page_size} → WHERE id > last_id LIMIT {page_size}"
                " -- 游标分页避免大 OFFSET"
            )

    # 5. NOT IN → NOT EXISTS
    not_in_match = re.search(r'\bWHERE\b\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+\bNOT IN\b', sql, re.IGNORECASE)
    if not_in_match:
        col = not_in_match.group(1)
        suggestions.append(
            f"🔧 NOT IN → NOT EXISTS: WHERE {col} NOT IN (subquery)"
            " -- NOT EXISTS 在有索引时性能更好"
        )

    # 6. 子查询 → JOIN
    if re.search(r'\bWHERE\b\s+\S+\s+\bIN\b\s*\(\s*SELECT\b', sql, re.IGNORECASE):
        suggestions.append(
            "🔧 子查询 → JOIN: WHERE col IN (SELECT ...) → SELECT ... JOIN (SELECT DISTINCT col FROM ...)"
            " -- JOIN 通常比子查询更高效"
        )

    return suggestions


# ==================== 性能指标计算 ====================

def calculate_performance_metrics(
    rows_examined: int,
    rows_sent: int,
    is_full_scan: bool = False,
    uses_index: bool = False
) -> Dict[str, Any]:
    """
    计算性能指标
    """
    metrics = {
        "rows_examined": rows_examined,
        "rows_sent": rows_sent,
        "scan_efficiency": None,
        "score": 100,
        "flags": {
            "full_scan": is_full_scan,
            "uses_index": uses_index,
        },
        "recommendation": None,
    }

    if rows_sent > 0:
        ratio = rows_examined / rows_sent
        metrics["scan_efficiency"] = f"{int(ratio)}:1"
    else:
        metrics["scan_efficiency"] = "N/A"

    score = 100
    if is_full_scan:
        score -= 30
    if not uses_index:
        score -= 15

    if rows_sent > 0:
        ratio = rows_examined / rows_sent
        if ratio >= 10000:
            score -= 20
        elif ratio >= 1000:
            score -= 15
        elif ratio >= 100:
            score -= 8
        elif ratio >= 10:
            score -= 3

    metrics["score"] = max(0, min(100, score))

    if metrics["score"] >= 80:
        metrics["recommendation"] = "✅ 性能优秀"
    elif metrics["score"] >= 60:
        metrics["recommendation"] = "🟡 性能一般，可进一步优化"
    elif metrics["score"] >= 40:
        metrics["recommendation"] = "⚠️ 性能较差，建议优化"
    else:
        metrics["recommendation"] = "🔴 性能极差，亟需优化"

    return metrics
