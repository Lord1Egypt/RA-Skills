#!/usr/bin/env python3
"""
MySQL Slow Query Analyzer - Parser Module
EXPLAIN JSON/TEXT 解析 | 慢查询日志解析
"""

import re
import json
from typing import Optional, List, Dict, Any


# ==================== 工具函数 ====================

def extract_sql_from_log(log: str) -> str:
    """从慢查询日志中提取 SQL 语句"""
    if not log.strip():
        return ""
    lines = log.splitlines()
    sql_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        sql_lines.append(stripped)
    return " ".join(sql_lines).rstrip(";").strip()


def extract_conditions(sql: str) -> List[str]:
    """从 SQL WHERE 子句提取所有列名"""
    match = re.search(
        r'\bWHERE\b(.+?)(?:\bGROUP BY\b|\bORDER BY\b|\bHAVING\b|\bLIMIT\b|$)',
        sql, re.IGNORECASE | re.DOTALL
    )
    if not match:
        return []
    where_clause = match.group(1)
    col_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=|!=|<|>|<=|>=|LIKE|IN\b|IS\b)'
    cols = re.findall(col_pattern, where_clause, re.IGNORECASE)
    seen = set()
    result = []
    for c in cols:
        if c.lower() not in seen:
            seen.add(c.lower())
            result.append(c)
    return result


def _extract_join_columns(sql: str) -> List[str]:
    """提取 JOIN 连接的列名"""
    on_pattern = r'\bON\b\s+([a-zA-Z_][a-zA-Z0-9_]*)\.[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\.[a-zA-Z_][a-zA-Z0-9_]*'
    matches = re.findall(on_pattern, sql, re.IGNORECASE)
    cols = []
    for m in matches:
        cols.extend([c for c in m if c.lower() not in ("and", "or", "on")])
    return list(set(cols))


def _parse_explain_json_score(
    query_cost: Optional[str],
    access_type: str,
    rows_examined: int,
    rows_produced: int,
    using_filesort: bool
) -> int:
    """
    根据 EXPLAIN JSON 信息计算性能评分 (0-100)
    """
    score = 100

    type_scores = {
        "SYSTEM": 100, "CONST": 95, "EQ_REF": 85,
        "REF": 75, "RANGE": 65, "INDEX": 55, "ALL": 20
    }
    type_pts = type_scores.get(access_type.upper(), 40)
    score = type_pts

    try:
        cost = float(query_cost) if query_cost else 0
        if cost > 100000:
            score -= 25
        elif cost > 10000:
            score -= 15
        elif cost > 1000:
            score -= 8
        elif cost > 100:
            score -= 3
    except (ValueError, TypeError):
        pass

    if rows_produced > 0:
        ratio = rows_examined / rows_produced
        if ratio >= 10000:
            score -= 25
        elif ratio >= 1000:
            score -= 15
        elif ratio >= 100:
            score -= 8
        elif ratio >= 10:
            score -= 3

    if using_filesort:
        score -= 10

    return max(0, min(100, score))


# ==================== EXPLAIN JSON 解析 ====================

def parse_explain_json(explain_json: str) -> Dict[str, Any]:
    """
    解析 MySQL EXPLAIN FORMAT=JSON 输出
    """
    if not explain_json.strip():
        return {"error": "Empty input", "warnings": [], "suggestions": []}

    result = {
        "error": None,
        "query_cost": None,
        "access_type": None,
        "key_used": None,
        "rows_examined": None,
        "rows_produced": None,
        "warnings": [],
        "suggestions": [],
        "score": None,
    }

    try:
        data = json.loads(explain_json)
    except json.JSONDecodeError:
        result["error"] = "Invalid JSON format"
        return result

    qb = data.get("query_block", data)
    cost_info = qb.get("cost_info", {})
    query_cost = cost_info.get("query_cost")
    result["query_cost"] = query_cost

    ordering = qb.get("ordering_operation", {})
    using_filesort = ordering.get("using_filesort", False) if isinstance(ordering, dict) else False

    table_info = qb.get("table", {})
    if isinstance(table_info, dict):
        access_type = table_info.get("access_type", "UNKNOWN")
        result["access_type"] = access_type
        result["key_used"] = table_info.get("key")
        rows_examined = table_info.get("rows_examined_scan") or table_info.get("rows_examined", 0)
        rows_produced = table_info.get("rows_produced", 0)
        result["rows_examined"] = rows_examined
        result["rows_produced"] = rows_produced
        table_name = table_info.get("table_name", "unknown")

        warnings, suggestions = _analyze_access_type(
            access_type, table_name, table_info, query_cost
        )
        result["warnings"] = warnings
        result["suggestions"] = suggestions

    extra_from_table = table_info.get("extra", "") if isinstance(table_info, dict) else ""
    if not using_filesort and isinstance(extra_from_table, str) and "filesort" in extra_from_table.lower():
        using_filesort = True

    result["using_filesort"] = using_filesort

    if using_filesort and not any("filesort" in w.lower() for w in result["warnings"]):
        result["warnings"].append("🔴 Using filesort: ORDER BY 未走索引，大数据量时严重性能问题")
        result["suggestions"].append("🔧 在 ORDER BY 列上建立索引，或调整为联合索引")

    score = _parse_explain_json_score(
        query_cost,
        result["access_type"] or "ALL",
        result["rows_examined"] or 0,
        result["rows_produced"] or 0,
        using_filesort
    )
    result["score"] = score
    result["using_filesort"] = using_filesort

    return result


def _analyze_access_type(
    access_type: str,
    table_name: str,
    table_info: Dict,
    query_cost: Optional[str]
) -> tuple:
    """根据访问类型生成警告和建议"""
    warnings = []
    suggestions = []
    type_lower = access_type.lower()

    if type_lower == "all":
        warnings.append(f"🔴 全表扫描: {table_name} 使用 ALL 类型，数据量大时性能极差")
        suggestions.append(f"🔧 在 {table_name} 的 WHERE/JOIN/ORDER BY 列上建立索引")
        try:
            rows = int(table_info.get("rows_examined_scan") or 0)
            if rows > 10000:
                warnings.append(f"🔴 扫描行数过多: {rows:,} 行")
                suggestions.append(f"🔧 检查是否可以使用覆盖索引减少回表")
        except (ValueError, TypeError):
            pass

    elif type_lower == "index":
        warnings.append(f"🟡 索引全扫描: {table_name} 使用 index 类型，仍需扫描全部索引")
        suggestions.append(f"🔧 考虑在 WHERE 列上建索引改为 range 或 ref 访问")

    elif type_lower == "range":
        suggestions.append(f"✅ 范围扫描: {table_name} 使用 range，性能良好")

    elif type_lower in ("ref", "eq_ref", "const"):
        suggestions.append(f"✅ 索引访问: {table_name} 使用 {access_type}，性能优秀")

    extra = table_info.get("extra", "")
    if isinstance(extra, str):
        if "Using filesort" in extra:
            warnings.append("🔴 Using filesort: ORDER BY 未走索引，大数据量时严重性能问题")
            suggestions.append("🔧 在 ORDER BY 列上建立索引，或调整为联合索引")
        if "Using temporary" in extra:
            warnings.append("🟡 Using temporary: 使用临时表，建议优化 GROUP BY 或 DISTINCT")
            suggestions.append("🔧 检查 GROUP BY 列是否有索引")

    try:
        if query_cost and float(query_cost) > 10000:
            warnings.append(f"🔴 查询成本极高: {query_cost}")
    except (ValueError, TypeError):
        pass

    return warnings, suggestions


# ==================== EXPLAIN TEXT 解析 ====================

def parse_explain_text(explain_text: str) -> Dict[str, Any]:
    """
    解析 MySQL EXPLAIN (Traditional/TAB) 格式
    """
    if not explain_text.strip():
        return {"error": "Empty input", "warnings": [], "suggestions": []}

    result = {
        "error": None,
        "type": None,
        "table": None,
        "key": None,
        "rows": None,
        "warnings": [],
        "suggestions": [],
        "extra": [],
    }

    lines = explain_text.strip().splitlines()
    data_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("+---") or "select_type" in stripped.lower():
            continue
        data_lines.append(stripped)

    if not data_lines:
        result["error"] = "Cannot parse EXPLAIN output: no data rows found"
        return result

    row = data_lines[0]
    fields = [f.strip() for f in row.split("|")[1:-1]]

    if len(fields) < 7:
        result["error"] = f"Unexpected EXPLAIN format: only {len(fields)} fields"
        return result

    n = len(fields)
    if n == 7:
        result["type"] = fields[3] if len(fields) > 3 else None
        result["table"] = fields[2] if len(fields) > 2 else None
        result["key"] = fields[4] if len(fields) > 4 else None
        result["rows"] = int(fields[5]) if len(fields) > 5 and fields[5].isdigit() else None
        result["extra"] = [fields[6].strip()] if len(fields) > 6 and fields[6].strip() else []
    elif n == 9:
        result["type"] = fields[3] if len(fields) > 3 else None
        result["table"] = fields[2] if len(fields) > 2 else None
        result["key"] = fields[5] if len(fields) > 5 else None
        result["rows"] = int(fields[6]) if len(fields) > 6 and fields[6].isdigit() else None
        result["extra"] = [fields[8].strip()] if len(fields) > 8 and fields[8].strip() else []
    elif n >= 11:
        result["type"] = fields[4] if len(fields) > 4 else None
        result["table"] = fields[2] if len(fields) > 2 else None
        result["key"] = fields[6] if len(fields) > 6 else None
        result["rows"] = int(fields[9]) if len(fields) > 9 and fields[9].isdigit() else None
        result["extra"] = [e.strip() for e in fields[11].split(",") if e.strip()] if len(fields) > 11 else []
    else:
        result["type"] = fields[3] if len(fields) > 3 else None
        result["table"] = fields[2] if len(fields) > 2 else None
        result["key"] = fields[4] if len(fields) > 4 else None
        result["rows"] = int(fields[5]) if len(fields) > 5 and fields[5].isdigit() else None

    access_type = result["type"]
    warnings, suggestions = _analyze_access_type(
        access_type, result["table"] or "unknown",
        {"extra": " ".join(result["extra"]) if result["extra"] else ""}, None
    )
    result["warnings"] = warnings
    result["suggestions"] = suggestions

    return result


# ==================== 慢查询日志解析 ====================

def parse_slow_query_log(log: str) -> Dict[str, Any]:
    """
    解析 MySQL 慢查询日志条目
    """
    if not log.strip():
        return {"error": "Empty input", "warnings": [], "suggestions": []}

    result = {
        "error": None,
        "query_time": None,
        "lock_time": None,
        "rows_sent": None,
        "rows_examined": None,
        "severity": None,
        "efficiency_ratio": None,
        "warnings": [],
        "suggestions": [],
        "extracted_sql": "",
    }

    query_time_match = re.search(r'Query_time:\s*([\d.]+)', log, re.IGNORECASE)
    lock_time_match = re.search(r'Lock_time:\s*([\d.]+)', log, re.IGNORECASE)
    rows_sent_match = re.search(r'Rows_sent:\s*(\d+)', log, re.IGNORECASE)
    rows_examined_match = re.search(r'Rows_examined:\s*(\d+)', log, re.IGNORECASE)

    if query_time_match:
        try:
            result["query_time"] = float(query_time_match.group(1))
        except ValueError:
            pass

    if lock_time_match:
        try:
            result["lock_time"] = float(lock_time_match.group(1))
        except ValueError:
            pass

    if rows_sent_match:
        try:
            result["rows_sent"] = int(rows_sent_match.group(1))
        except ValueError:
            pass

    if rows_examined_match:
        try:
            result["rows_examined"] = int(rows_examined_match.group(1))
        except ValueError:
            pass

    result["extracted_sql"] = extract_sql_from_log(log)

    qt = result["query_time"]
    if qt is not None:
        if qt > 5.0:
            result["severity"] = "CRITICAL"
        elif qt > 1.0:
            result["severity"] = "WARNING"
        else:
            result["severity"] = "NORMAL"
    else:
        result["severity"] = "UNKNOWN"

    re_val = result["rows_examined"]
    rs_val = result["rows_sent"]
    if re_val is not None and re_val > 0:
        if rs_val is not None and rs_val > 0:
            ratio = re_val / rs_val
            result["efficiency_ratio"] = f"{int(ratio)}:1"
            if ratio > 1000:
                result["warnings"].append(
                    f"🔴 扫描效率极差: 每{int(ratio)}行才返回1行，大量无效扫描"
                )
                result["suggestions"].append(
                    "🔧 检查 WHERE 条件是否走索引，避免全表扫描"
                )
            elif ratio > 100:
                result["warnings"].append(
                    f"🟡 扫描效率较差: {int(ratio)}:1，建议优化"
                )
        elif rs_val == 0:
            result["efficiency_ratio"] = "N/A"
            result["warnings"].append("📝 扫描10000行但未返回数据（写操作或 DELETE/UPDATE）")
    elif re_val == 0 and rs_val == 0:
        result["efficiency_ratio"] = "N/A"

    return result
