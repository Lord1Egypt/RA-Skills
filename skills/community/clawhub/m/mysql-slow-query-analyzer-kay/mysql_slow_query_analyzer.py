#!/usr/bin/env python3
"""
MySQL Slow Query Analyzer / MySQL 慢查询分析与优化
支持: EXPLAIN 解析 | 慢查询日志分析 | 索引建议 | SQL 重写建议 | 性能评分

模块结构:
  - analyzer_parser.py     : EXPLAIN JSON/TEXT 解析、慢查询日志解析
  - analyzer_suggestions.py: 索引建议、SQL 重写建议、性能指标计算
"""

import re
import json
import sys
from typing import Optional, Dict, Any

from analyzer_parser import (
    parse_explain_json,
    parse_explain_text,
    parse_slow_query_log,
    extract_sql_from_log,
    extract_conditions,
    _parse_explain_json_score,
)
from analyzer_suggestions import (
    generate_index_suggestions,
    generate_rewrite_suggestions,
    calculate_performance_metrics,
)


# ==================== 综合分析 ====================

def analyze_slow_query(
    sql: str,
    explain_format: str = "json",
    explain_data: Optional[str] = None
) -> Dict[str, Any]:
    """
    综合分析慢查询
    整合 EXPLAIN 解析 + 索引建议 + SQL 重写 + 性能指标
    """
    result = {
        "sql": sql,
        "explain_format": explain_format,
        "explain_result": None,
        "index_suggestions": generate_index_suggestions(sql),
        "rewrite_suggestions": generate_rewrite_suggestions(sql),
        "metrics": None,
        "log_info": None,
        "score": None,
    }

    if explain_data:
        if explain_format == "json":
            result["explain_result"] = parse_explain_json(explain_data)
        elif explain_format == "text":
            result["explain_result"] = parse_explain_text(explain_data)
        elif explain_format == "slowlog":
            result["log_info"] = parse_slow_query_log(explain_data)
            if result["log_info"].get("extracted_sql") and not sql.strip():
                sql = result["log_info"]["extracted_sql"]

    re_val = None
    rs_val = None
    if explain_data and explain_format in ("json", "slowlog"):
        parsed = result["explain_result"] if explain_format != "slowlog" else result["log_info"]
        if parsed:
            re_val = parsed.get("rows_examined") or parsed.get("rows_examined_scan")
            rs_val = parsed.get("rows_produced") or parsed.get("rows_sent")

    if re_val is None and rs_val is None:
        re_match = re.search(r'\bLIMIT\b\s+(\d+)', sql, re.IGNORECASE)
        rs_val = int(re_match.group(1)) if re_match else 100
        re_val = rs_val * 50

    if re_val is not None and rs_val is not None:
        full_scan = result["explain_result"].get("access_type") == "ALL" if result["explain_result"] else False
        uses_index = result["explain_result"].get("key_used") is not None if result["explain_result"] else False
        result["metrics"] = calculate_performance_metrics(
            int(re_val), int(rs_val), full_scan, uses_index
        )
        result["score"] = result["metrics"]["score"]

    return result


# ==================== CLI 入口 ====================

def _format_report(data: Dict[str, Any], fmt: str = "text") -> str:
    """格式化输出报告"""
    if fmt == "json":
        clean = {k: v for k, v in data.items() if v is not None}
        return json.dumps(clean, ensure_ascii=False, indent=2, default=str)

    lines = []
    lines.append("📊 **MySQL 慢查询分析报告**\n")

    if data.get("explain_result"):
        er = data["explain_result"]
        if er.get("error"):
            lines.append(f"❌ 解析错误: {er['error']}\n")
        else:
            score = er.get("score")
            if score is not None:
                lines.append(f"⚡ 性能评分: {score}/100")
            if er.get("query_cost"):
                lines.append(f"💰 查询成本: {er['query_cost']}")
            if er.get("access_type"):
                lines.append(f"🔍 访问类型: {er['access_type']}")
            if er.get("key_used"):
                lines.append(f"📇 使用索引: {er['key_used']}")
            lines.append("")

    if data.get("log_info"):
        li = data["log_info"]
        if not li.get("error"):
            lines.append(f"⏱️ 查询时间: {li.get('query_time')}s ({li.get('severity', 'UNKNOWN')})")
            lines.append(f"🔒 锁等待: {li.get('lock_time')}s")
            lines.append(f"📊 扫描行数: {li.get('rows_examined', 'N/A'):,}")
            lines.append(f"📨 返回行数: {li.get('rows_sent', 'N/A'):,}")
            lines.append(f"📈 扫描效率: {li.get('efficiency_ratio', 'N/A')}")
            lines.append("")

    if data.get("metrics"):
        m = data["metrics"]
        lines.append(f"⚡ 性能评分: {m['score']}/100 — {m.get('recommendation', '')}")
        lines.append(f"📊 扫描效率: {m.get('scan_efficiency', 'N/A')}")
        lines.append("")

    if data.get("index_suggestions"):
        lines.append("💡 **索引建议**:")
        for s in data["index_suggestions"]:
            lines.append(f"  {s}")
        lines.append("")

    if data.get("rewrite_suggestions"):
        lines.append("🔧 **重写建议**:")
        for s in data["rewrite_suggestions"]:
            lines.append(f"  {s}")
        lines.append("")

    warnings = []
    for src in [data.get("explain_result"), data.get("log_info")]:
        if src and src.get("warnings"):
            warnings.extend(src["warnings"])
    if warnings:
        lines.append("⚠️ **警告**:")
        for w in warnings:
            lines.append(f"  {w}")

    return "\n".join(lines).strip()


def main():
    if len(sys.argv) < 2:
        print("MySQL Slow Query Analyzer - 用法:")
        print("  python mysql_slow_query_analyzer.py explain-json '<JSON>'")
        print("  python mysql_slow_query_analyzer.py explain-text '<TEXT>'")
        print("  python mysql_slow_query_analyzer.py slowlog '<LOG>'")
        print("  python mysql_slow_query_analyzer.py index-advice '<SQL>'")
        print("  python mysql_slow_query_analyzer.py rewrite '<SQL>'")
        print("  python mysql_slow_query_analyzer.py analyze '<SQL>'")
        print("  python mysql_slow_query_analyzer.py help")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "help":
        print(__doc__ or "MySQL Slow Query Analyzer")
        sys.exit(0)

    args = " ".join(sys.argv[2:]) if len(sys.argv) >= 3 else ""

    if cmd == "explain-json":
        result = parse_explain_json(args)
        print(_format_report({"explain_result": result}))

    elif cmd == "explain-text":
        result = parse_explain_text(args)
        print(_format_report({"explain_result": result}))

    elif cmd == "slowlog":
        result = parse_slow_query_log(args)
        print(_format_report({"log_info": result}))

    elif cmd == "index-advice":
        result = generate_index_suggestions(args)
        print("💡 索引建议:")
        for s in result:
            print(f"  {s}")

    elif cmd == "rewrite":
        result = generate_rewrite_suggestions(args)
        print("🔧 重写建议:")
        for s in result:
            print(f"  {s}")

    elif cmd == "analyze":
        result = analyze_slow_query(args)
        print(_format_report(result))

    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
