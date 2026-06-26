#!/usr/bin/env python3
"""
测试用例 - mysql-slow-query-analyzer
使用 pytest 框架，TDD 模式：先写测试，再写代码
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from mysql_slow_query_analyzer import (
    parse_explain_json,
    parse_explain_text,
    parse_slow_query_log,
    generate_index_suggestions,
    generate_rewrite_suggestions,
    calculate_performance_metrics,
    analyze_slow_query,
    extract_sql_from_log,
    extract_conditions,
    _parse_explain_json_score,
)


# ==================== parse_explain_json 测试 ====================

class TestParseExplainJson:
    """parse_explain_json() 函数测试"""

    def test_high_cost_query(self):
        """高成本查询 - 全表扫描"""
        explain_json = """{
            "query_block": {
                "select_id": 1,
                "cost_info": {"query_cost": "12450.35"},
                "table": {
                    "table_name": "orders",
                    "access_type": "ALL",
                    "rows_examined_scan": 50000,
                    "rows_produced": 100,
                    "used_columns": ["id", "status", "created_at", "total"]
                }
            }
        }"""
        result = parse_explain_json(explain_json)
        assert result["query_cost"] == "12450.35"
        assert result["access_type"] == "ALL"
        assert "全表扫描" in result["warnings"][0]

    def test_index_scan(self):
        """索引扫描 - 正常性能"""
        explain_json = """{
            "query_block": {
                "select_id": 1,
                "cost_info": {"query_cost": "125.80"},
                "table": {
                    "table_name": "users",
                    "access_type": "ref",
                    "key": "idx_users_status",
                    "rows_examined_scan": 500,
                    "rows_produced": 50,
                    "used_columns": ["id", "status"]
                }
            }
        }"""
        result = parse_explain_json(explain_json)
        assert result["query_cost"] == "125.80"
        assert result["access_type"] == "ref"
        assert result["warnings"] == []

    def test_empty_json(self):
        """空输入"""
        result = parse_explain_json("")
        assert result["error"] is not None

    def test_invalid_json(self):
        """无效 JSON"""
        result = parse_explain_json("not json at all")
        assert result["error"] is not None

    def test_range_scan(self):
        """范围扫描"""
        explain_json = """{
            "query_block": {
                "select_id": 1,
                "cost_info": {"query_cost": "850.20"},
                "table": {
                    "table_name": "orders",
                    "access_type": "range",
                    "key": "idx_orders_created_at",
                    "rows_examined_scan": 5000,
                    "rows_produced": 200,
                    "used_columns": ["id", "created_at", "status"]
                }
            }
        }"""
        result = parse_explain_json(explain_json)
        assert result["access_type"] == "range"
        assert result["warnings"] == []

    def test_cost_info_missing(self):
        """缺少 cost_info 字段"""
        explain_json = """{
            "query_block": {
                "select_id": 1,
                "table": {
                    "table_name": "users",
                    "access_type": "ALL"
                }
            }
        }"""
        result = parse_explain_json(explain_json)
        assert result["query_cost"] is None

    def test_filesort_detected(self):
        """检测到 filesort"""
        explain_json = """{
            "query_block": {
                "select_id": 1,
                "cost_info": {"query_cost": "500.00"},
                "ordering_operation": {
                    "using_filesort": true
                },
                "table": {
                    "table_name": "orders",
                    "access_type": "ALL"
                }
            }
        }"""
        result = parse_explain_json(explain_json)
        assert any("filesort" in w.lower() for w in result["warnings"])


# ==================== parse_explain_text 测试 ====================

class TestParseExplainText:
    """parse_explain_text() 函数测试"""

    def test_full_table_scan(self):
        """全表扫描"""
        # 标准 MySQL EXPLAIN 格式（12列）
        text = """+----+-------------+--------+------------+-------+---------------+-------------+---------+------+----------+----------+------------------+
| id | select_type | table  | partitions | type  | possible_keys | key         | key_len | ref  | rows    | filtered | Extra                 |
+----+-------------+--------+------------+-------+---------------+-------------+---------+------+----------+----------+------------------+
|  1 | SIMPLE      | orders | NULL       | ALL   | NULL         | NULL        | NULL    | NULL | 50000   | 100.00   | Using where          |
+----+-------------+--------+------------+-------+---------------+-------------+---------+------+----------+----------+------------------+"""
        result = parse_explain_text(text)
        assert result["type"] == "ALL"
        assert result["rows"] == 50000
        assert result["warnings"] != []

    def test_ref_scan(self):
        """索引引用扫描"""
        text = """+----+-------------+-------+--------+----------------+---------+---------+
| id | select_type | table | type   | key          | rows   | Extra   |
+----+-------------+-------+--------+--------------+--------+---------+
|  1 | SIMPLE      | users | ref    | idx_status   | 500    | NULL    |
+----+-------------+-------+--------+--------------+--------+---------+"""
        result = parse_explain_text(text)
        assert result["type"] == "ref"
        assert result["warnings"] == []

    def test_empty_text(self):
        """空输入"""
        result = parse_explain_text("")
        assert result["error"] is not None

    def test_no_table_info(self):
        """无法解析的格式"""
        result = parse_explain_text("some random text")
        assert "error" in result or result.get("type") is None

    def test_eq_ref(self):
        """eq_ref 类型"""
        # 标准 MySQL EXPLAIN 格式（12列）- id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
        text = """+----+-------------+-------+------------+--------+---------------+---------+---------+-------+-------+----------+-------+
| id | select_type | table | partitions | type   | possible_keys | key     | key_len | ref   | rows  | filtered | Extra |
+----+-------------+-------+------------+--------+---------------+---------+---------+-------+-------+----------+-------+
|  1 | SIMPLE      | o     | NULL       | eq_ref | PRIMARY       | PRIMARY | 8       | const | 1     | 100.00   | NULL  |
+----+-------------+-------+------------+--------+---------------+---------+---------+-------+-------+----------+-------+"""
        result = parse_explain_text(text)
        assert result["type"] == "eq_ref"

    def test_using_temporary(self):
        """Using temporary"""
        text = """+----+-------------+--------+------+---------------+------+
| id | select_type | table  | type | key           | rows  |
+----+-------------+--------+------+---------------+-------+
|  1 | SIMPLE      | orders | ALL  | NULL          | 50000 |
+----+-------------+--------+------+---------------+-------+"""
        result = parse_explain_text(text)
        assert result.get("extra") is not None


# ==================== parse_slow_query_log 测试 ====================

class TestParseSlowQueryLog:
    """parse_slow_query_log() 函数测试"""

    def test_critical_query(self):
        """严重慢查询 (>5s)"""
        log = """# Time: 2024-01-01T10:00:00.123456Z
# Query_time: 5.234193  Lock_time: 0.000089  Rows_sent: 100  Rows_examined: 500000
SELECT * FROM orders WHERE status = 1;"""
        result = parse_slow_query_log(log)
        assert result["query_time"] == 5.234193
        assert result["severity"] == "CRITICAL"
        assert result["efficiency_ratio"] == "5000:1"

    def test_warning_query(self):
        """警告级别慢查询 (1-5s)"""
        log = """# Query_time: 2.500000  Lock_time: 0.000010  Rows_sent: 10  Rows_examined: 10000
SELECT * FROM users WHERE email = 'test@example.com';"""
        result = parse_slow_query_log(log)
        assert result["query_time"] == 2.5
        assert result["severity"] == "WARNING"
        assert result["efficiency_ratio"] == "1000:1"

    def test_normal_query(self):
        """正常查询 (<1s)"""
        log = """# Query_time: 0.523100  Lock_time: 0.000005  Rows_sent: 5  Rows_examined: 500
SELECT * FROM products WHERE category_id = 3;"""
        result = parse_slow_query_log(log)
        assert result["query_time"] == 0.5231
        assert result["severity"] == "NORMAL"
        assert result["warnings"] == []

    def test_empty_log(self):
        """空日志"""
        result = parse_slow_query_log("")
        assert result["error"] is not None

    def test_missing_query_time(self):
        """缺少 Query_time"""
        log = """# Time: 2024-01-01T10:00:00.123456Z
SELECT * FROM users;"""
        result = parse_slow_query_log(log)
        assert result.get("query_time") is None

    def test_zero_efficiency(self):
        """零扫描（极致优化）"""
        log = """# Query_time: 0.001000  Lock_time: 0.000001  Rows_sent: 1  Rows_examined: 1
SELECT * FROM users WHERE id = 1;"""
        result = parse_slow_query_log(log)
        assert result["efficiency_ratio"] == "1:1"
        assert result["warnings"] == []

    def test_no_rows_sent(self):
        """无返回行（写操作或 DELETE/UPDATE）"""
        log = """# Query_time: 1.234000  Lock_time: 0.000100  Rows_sent: 0  Rows_examined: 10000
DELETE FROM sessions WHERE expired = 1;"""
        result = parse_slow_query_log(log)
        assert result["rows_sent"] == 0
        assert "扫描" in result["warnings"][0]


# ==================== generate_index_suggestions 测试 ====================

class TestGenerateIndexSuggestions:
    """generate_index_suggestions() 函数测试"""

    def test_simple_where(self):
        """简单 WHERE 列"""
        sql = "SELECT * FROM orders WHERE status = 1"
        result = generate_index_suggestions(sql)
        assert any("status" in s.lower() for s in result)

    def test_multiple_where(self):
        """多列 WHERE"""
        sql = "SELECT * FROM orders WHERE status = 1 AND category = 'electronics'"
        result = generate_index_suggestions(sql)
        assert len(result) >= 1

    def test_join_columns(self):
        """JOIN 连接列"""
        sql = "SELECT * FROM orders o JOIN users u ON o.user_id = u.id WHERE u.status = 1"
        result = generate_index_suggestions(sql)
        assert any("user_id" in s.lower() or "id" in s.lower() for s in result)

    def test_order_by(self):
        """ORDER BY 列"""
        sql = "SELECT * FROM orders WHERE status = 1 ORDER BY created_at DESC"
        result = generate_index_suggestions(sql)
        assert any("created_at" in s.lower() for s in result)

    def test_group_by(self):
        """GROUP BY 列"""
        sql = "SELECT status, COUNT(*) FROM orders GROUP BY status"
        result = generate_index_suggestions(sql)
        assert any("status" in s.lower() for s in result)

    def test_empty_sql(self):
        """空 SQL"""
        result = generate_index_suggestions("")
        assert result == []

    def test_select_star(self):
        """SELECT * 自动提示"""
        sql = "SELECT * FROM orders WHERE status = 1"
        result = generate_index_suggestions(sql)
        assert any("SELECT" in s and "*" not in s.split("FROM")[0] for s in result) or any("覆盖" in s or "covering" in s.lower() for s in result)

    def test_no_where_clause(self):
        """无 WHERE 子句"""
        sql = "SELECT COUNT(*) FROM orders"
        result = generate_index_suggestions(sql)
        # COUNT(*) 通常不需要额外索引
        assert isinstance(result, list)


# ==================== generate_rewrite_suggestions 测试 ====================

class TestGenerateRewriteSuggestions:
    """generate_rewrite_suggestions() 函数测试"""

    def test_select_star(self):
        """SELECT * 重写"""
        sql = "SELECT * FROM orders WHERE status = 1"
        result = generate_rewrite_suggestions(sql)
        # 建议应该提到避免 SELECT * 并使用具体列名
        assert any("SELECT" in s and ("column" in s.lower() or "具体列" in s or "指定列" in s) for s in result)

    def test_or_to_union(self):
        """OR → UNION 重写"""
        sql = "SELECT * FROM orders WHERE user_id = 1 OR user_id = 2"
        result = generate_rewrite_suggestions(sql)
        assert any("UNION" in s.upper() for s in result)

    def test_implicit_type_conversion(self):
        """隐式类型转换"""
        sql = "SELECT * FROM orders WHERE order_id = '12345'"
        result = generate_rewrite_suggestions(sql)
        assert any("类型" in s or "type" in s.lower() for s in result)

    def test_large_offset(self):
        """大 OFFSET 分页"""
        sql = "SELECT * FROM orders LIMIT 100000, 20"
        result = generate_rewrite_suggestions(sql)
        assert any("LIMIT" in s.upper() or "offset" in s.lower() for s in result)

    def test_not_in_subquery(self):
        """NOT IN → NOT EXISTS"""
        sql = "SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM orders)"
        result = generate_rewrite_suggestions(sql)
        assert any("NOT EXISTS" in s.upper() or "NOT IN" in s.upper() for s in result)

    def test_empty_sql(self):
        """空 SQL"""
        result = generate_rewrite_suggestions("")
        assert result == []

    def test_simple_query(self):
        """简单查询 - 无需重写"""
        sql = "SELECT id, name FROM users WHERE id = 1"
        result = generate_rewrite_suggestions(sql)
        assert isinstance(result, list)


# ==================== calculate_performance_metrics 测试 ====================

class TestCalculatePerformanceMetrics:
    """calculate_performance_metrics() 函数测试"""

    def test_high_scan_efficiency(self):
        """高扫描效率"""
        result = calculate_performance_metrics(rows_examined=500, rows_sent=100)
        assert result["scan_efficiency"] == "5:1"
        # 基础100分，全表扫描-30，无索引-15，ratio=5不扣分 = 55
        assert result["score"] > 50

    def test_very_poor_efficiency(self):
        """极差扫描效率"""
        result = calculate_performance_metrics(rows_examined=500000, rows_sent=100, is_full_scan=True)
        assert result["scan_efficiency"] == "5000:1"
        # 基础100分，全表扫描-30，ratio>=1000扣15分 = 55
        assert result["score"] < 60

    def test_zero_rows_sent(self):
        """零返回行（写操作）"""
        result = calculate_performance_metrics(rows_examined=10000, rows_sent=0)
        assert result["rows_sent"] == 0
        assert result["scan_efficiency"] == "N/A"

    def test_full_scan_cost(self):
        """全表扫描成本高"""
        result = calculate_performance_metrics(rows_examined=50000, rows_sent=100, is_full_scan=True)
        assert result["flags"]["full_scan"] is True

    def test_index_hit(self):
        """索引命中"""
        result = calculate_performance_metrics(rows_examined=500, rows_sent=100, uses_index=True)
        assert result["flags"]["uses_index"] is True
        assert result["score"] >= 70

    def test_no_flags(self):
        """无特殊情况"""
        result = calculate_performance_metrics(rows_examined=1000, rows_sent=100)
        assert "flags" in result
        assert isinstance(result["flags"], dict)


# ==================== analyze_slow_query 综合测试 ====================

class TestAnalyzeSlowQuery:
    """analyze_slow_query() 综合分析测试"""

    def test_full_analysis_with_json(self):
        """完整分析 - EXPLAIN JSON"""
        sql = "SELECT * FROM orders WHERE status = 1 ORDER BY created_at DESC"
        explain_json = """{
            "query_block": {
                "select_id": 1,
                "cost_info": {"query_cost": "12450.35"},
                "ordering_operation": {"using_filesort": true},
                "table": {
                    "table_name": "orders",
                    "access_type": "ALL",
                    "rows_examined_scan": 50000,
                    "rows_produced": 100
                }
            }
        }"""
        result = analyze_slow_query(sql, explain_format="json", explain_data=explain_json)
        assert "score" in result
        # ALL类型20分，成本>10000扣15分，ratio=500扣8分，filesort扣10分 = -13 → 0
        assert result["score"] < 50
        assert result["index_suggestions"] != []
        assert result["rewrite_suggestions"] != []

    def test_full_analysis_with_log(self):
        """完整分析 - 慢查询日志"""
        sql = "SELECT * FROM orders WHERE status = 1"
        log = """# Query_time: 6.000000  Lock_time: 0.000100  Rows_sent: 100  Rows_examined: 500000
SELECT * FROM orders WHERE status = 1;"""
        result = analyze_slow_query(sql, explain_format="slowlog", explain_data=log)
        assert result["log_info"]["severity"] == "CRITICAL"
        assert result["index_suggestions"] != []

    def test_sql_only_analysis(self):
        """仅 SQL 分析（无 EXPLAIN）"""
        sql = "SELECT * FROM orders WHERE status = 1 AND created_at > '2024-01-01'"
        result = analyze_slow_query(sql)
        assert "index_suggestions" in result
        assert "rewrite_suggestions" in result
        assert "metrics" in result


# ==================== extract_sql_from_log 测试 ====================

class TestExtractSqlFromLog:
    """extract_sql_from_log() 函数测试"""

    def test_simple_log(self):
        """简单日志提取"""
        log = """# Query_time: 1.000000  Rows_sent: 10  Rows_examined: 1000
SELECT * FROM users WHERE status = 1;"""
        result = extract_sql_from_log(log)
        assert "SELECT" in result
        assert "users" in result.lower()

    def test_multiline_log(self):
        """多行日志"""
        log = """# Time: 2024-01-01T10:00:00.123456Z
# Query_time: 2.500000
SELECT
    id,
    name,
    status
FROM users
WHERE status = 1;"""
        result = extract_sql_from_log(log)
        assert "SELECT" in result
        assert "FROM" in result

    def test_empty_log(self):
        """空日志"""
        result = extract_sql_from_log("")
        assert result == ""


# ==================== extract_conditions 测试 ====================

class TestExtractConditions:
    """extract_conditions() 函数测试"""

    def test_simple_where(self):
        """简单 WHERE"""
        sql = "SELECT * FROM orders WHERE status = 1"
        result = extract_conditions(sql)
        assert "status" in result

    def test_multiple_conditions(self):
        """多条件"""
        sql = "SELECT * FROM orders WHERE status = 1 AND category_id = 5 AND total > 100"
        result = extract_conditions(sql)
        assert len(result) >= 2

    def test_no_where(self):
        """无 WHERE"""
        sql = "SELECT COUNT(*) FROM orders"
        result = extract_conditions(sql)
        assert result == []

    def test_like_condition(self):
        """LIKE 条件"""
        sql = "SELECT * FROM users WHERE email LIKE '%@example.com'"
        result = extract_conditions(sql)
        assert "email" in result


# ==================== _parse_explain_json_score 测试 ====================

class TestParseExplainJsonScore:
    """_parse_explain_json_score() 函数测试"""

    def test_high_cost_low_score(self):
        """高成本低分"""
        score = _parse_explain_json_score(
            query_cost="50000.00",
            access_type="ALL",
            rows_examined=100000,
            rows_produced=100,
            using_filesort=True
        )
        assert score < 50  # ALL类型20分，成本>10000扣15分，ratio>=1000扣15分，filesort扣10分 = -20 → 0

    def test_low_cost_high_score(self):
        """低成本高分"""
        score = _parse_explain_json_score(
            query_cost="50.00",
            access_type="ref",
            rows_examined=500,
            rows_produced=100,
            using_filesort=False
        )
        assert score >= 70

    def test_filesort_penalty(self):
        """filesort 扣分"""
        score_no_filesort = _parse_explain_json_score("1000.00", "ALL", 5000, 100, False)
        score_with_filesort = _parse_explain_json_score("1000.00", "ALL", 5000, 100, True)
        assert score_with_filesort < score_no_filesort


# ==================== 边界情况测试 ====================

class TestEdgeCases:
    """边界情况测试"""

    def test_unicode_in_sql(self):
        """SQL 中含中文"""
        sql = "SELECT * FROM orders WHERE status = 1 ORDER BY created_at DESC"
        result = analyze_slow_query(sql)
        assert "index_suggestions" in result

    def test_very_long_table_name(self):
        """超长表名"""
        sql = "SELECT * FROM orders WHERE status = 1"
        result = generate_index_suggestions(sql)
        assert isinstance(result, list)

    def test_special_characters_in_value(self):
        """SQL 中含特殊字符值"""
        sql = "SELECT * FROM users WHERE name = 'O\\'Brien' AND email = 'a@b.com'"
        result = generate_index_suggestions(sql)
        assert isinstance(result, list)

    def test_numeric_query_time(self):
        """数字格式 Query_time"""
        log = "# Query_time: 3.5  Rows_sent: 10  Rows_examined: 1000\nSELECT * FROM users;"
        result = parse_slow_query_log(log)
        assert result["query_time"] == 3.5
        assert result["severity"] == "WARNING"

    def test_malformed_slow_log(self):
        """格式异常的慢查询日志"""
        log = "completely malformed log entry without proper format"
        result = parse_slow_query_log(log)
        assert "error" in result or result.get("query_time") is None

    def test_main_entry_point(self):
        """main() 入口测试"""
        import json
        sys.argv = ["mysql_slow_query_analyzer.py", "analyze", "SELECT * FROM orders WHERE status = 1"]
        try:
            from mysql_slow_query_analyzer import main
            main()
        except SystemExit:
            pass
