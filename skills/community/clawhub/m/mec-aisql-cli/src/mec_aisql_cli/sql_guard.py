"""SQL 类型守卫模块

本模块用于在 Bot 自动化模式中检查 SQL 是否为统计类查询,
防止非统计类 SQL (如 DML/DDL/纯 SELECT) 被自动执行。

== AI Bot 使用指南 ==

Bot 模式 (``mec-aisql bot``) 会强制调用 ``check_sql_type()`` 检查生成的 SQL,
仅允许以下类型的 SQL 通过:

  - **statistical** (统计类): 含 COUNT/SUM/AVG/MAX/MIN/GROUP BY/DISTINCT 等聚合特征
  - 其他类型 (select_only/dml/ddl/dangerous/empty/unknown) 均被阻断

检查逻辑顺序:
  1. 空检查 → empty
  2. 危险关键字 (INSERT/UPDATE/DELETE/DROP/ALTER/TRUNCATE/...) → dml/ddl/dangerous
  3. 必须以 SELECT 或 WITH 开头 → 否则 unknown
  4. 检查聚合函数 (COUNT/SUM/AVG/...)
  5. 检查 GROUP BY
  6. 检查 DISTINCT
  7. 仅当无聚合无 GROUP BY 无 DISTINCT 时, 才检查 SELECT * → select_only
  8. 有聚合或 GROUP BY → statistical (放行)
  9. 有 DISTINCT → statistical (放行)
  10. 以上都不满足 → select_only (阻断)

关键设计: CTE 子查询中的 ``SELECT *`` 不会影响外层有聚合的查询,
因为 Step 7 仅在无聚合时才检查 ``SELECT *``。
"""
import re
from dataclasses import dataclass, field
from typing import List


# 聚合函数列表: SQL 中出现这些函数则判定为统计类查询
# 包含标准聚合 (COUNT/SUM/AVG/MAX/MIN) 和 Spark 高级聚合 (PERCENTILE/COLLECT_LIST/...)
AGG_FUNCS = {
    "count", "sum", "avg", "average", "max", "min",
    "stddev", "stddev_pop", "stddev_samp", "variance", "var_pop", "var_samp",
    "percentile", "percentile_approx", "collect_list", "collect_set",
    "corr", "covar_pop", "covar_samp", "histogram_numeric",
    "approx_count_distinct", "grouping",
}

# 危险关键字列表: Bot 模式中禁止出现的 SQL 操作
# 包含 DML (INSERT/UPDATE/DELETE)、DDL (DROP/ALTER/TRUNCATE) 和其他危险操作
BLOCKED_KEYWORDS = [
    r"\binsert\b\s+(into|overwrite)",
    r"\bupdate\b\s+",
    r"\bdelete\b\s+from",
    r"\bdrop\b\s+(table|database|view|function)",
    r"\balter\b\s+",
    r"\btruncate\b\s+",
    r"\bmerge\b\s+into",
    r"\bgrant\b\s+",
    r"\brevoke\b\s+",
    r"\bmsck\b\s+repair",
    r"\brepair\b\s+table",
    r"\bload\b\s+data",
    # CREATE TABLE ... AS SELECT 是允许的 (CTAS), 但纯 CREATE TABLE 不允许
    r"\bcreate\b\s+table\b(?!\s+.*\bas\s+select)",
    r"\bset\b\s+spark",
    r"\badd\b\s+jar",
    r"\bsource\b\s+",
]


@dataclass
class GuardResult:
    """SQL 类型守卫检查结果

    Attributes:
        allowed:             是否允许 Bot 自动执行此 SQL
        sql_type:            SQL 类型 (statistical/select_only/dml/ddl/dangerous/empty/unknown)
        reason:              判定原因说明
        aggregate_functions: 检测到的聚合函数列表 (如 ["COUNT", "SUM"])
        has_group_by:        是否包含 GROUP BY 子句
        has_distinct:        是否包含 DISTINCT 关键字
        blocked_keywords:    触发的危险关键字列表 (仅当被阻断时)
    """
    allowed: bool
    sql_type: str = ""  # statistical | select_only | dml | ddl | dangerous | empty | unknown
    reason: str = ""
    aggregate_functions: List[str] = field(default_factory=list)
    has_group_by: bool = False
    has_distinct: bool = False
    blocked_keywords: List[str] = field(default_factory=list)


def check_sql_type(sql: str) -> GuardResult:
    """检查 SQL 是否为统计类查询 (适合 Bot 自动化执行)

    统计类查询必须满足以下条件:
        1. 是 SELECT 或 WITH (CTE) 语句
        2. 包含至少一个聚合函数 或 GROUP BY 子句 或 DISTINCT 关键字
        3. 不包含任何 DML/DDL/危险关键字

    Args:
        sql: 待检查的 SQL 语句字符串

    Returns:
        GuardResult 对象, 包含 allowed/sql_type/reason 等字段

    判定规则:

        - **statistical**: 含聚合函数/GROUP BY/DISTINCT → ``allowed=True``
        - **select_only**: 纯 SELECT 无聚合 → ``allowed=False``
        - **dml**: INSERT/UPDATE/DELETE → ``allowed=False``
        - **ddl**: DROP/ALTER/TRUNCATE → ``allowed=False``
        - **dangerous**: GRANT/REVOKE/LOAD 等其他危险操作 → ``allowed=False``
        - **empty**: SQL 为空 → ``allowed=False``
        - **unknown**: 非 SELECT/WITH 开头 → ``allowed=False``
    """
    if not sql or not sql.strip():
        return GuardResult(allowed=False, sql_type="empty", reason="SQL 为空")

    # 规范化: 去除首尾空白和末尾分号
    normalized = sql.strip().rstrip(";").strip()
    lower = normalized.lower()

    # ---- Step 1: 检查危险关键字 (DML/DDL/危险操作) ----
    # 命中任一关键字则阻断, 不再检查后续
    blocked = []
    for pattern in BLOCKED_KEYWORDS:
        if re.search(pattern, lower, re.IGNORECASE):
            blocked.append(pattern)

    if blocked:
        # 根据匹配到的关键字分类
        if any("insert" in p or "update" in p or "delete" in p for p in blocked):
            sql_type = "dml"
        elif any("drop" in p or "alter" in p or "truncate" in p for p in blocked):
            sql_type = "ddl"
        else:
            sql_type = "dangerous"
        return GuardResult(
            allowed=False,
            sql_type=sql_type,
            reason=f"SQL 包含被禁止的操作 ({sql_type})，Bot 自动化仅允许统计类查询",
            blocked_keywords=blocked,
        )

    # ---- Step 2: 必须以 SELECT 或 WITH (CTE) 开头 ----
    if not re.match(r"^\s*(select|with)\b", lower, re.IGNORECASE):
        return GuardResult(
            allowed=False,
            sql_type="unknown",
            reason="Bot 自动化仅允许 SELECT 或 WITH 语句",
        )

    # ---- Step 3: 检查聚合函数 (COUNT/SUM/AVG/...) ----
    found_aggs = []
    for func in AGG_FUNCS:
        if re.search(rf"\b{func}\s*\(", lower, re.IGNORECASE):
            found_aggs.append(func.upper())

    # ---- Step 4: 检查 GROUP BY ----
    has_group_by = bool(re.search(r"\bgroup\s+by\b", lower, re.IGNORECASE))

    # ---- Step 5: 检查 DISTINCT (去重查询, 视为统计类) ----
    has_distinct = bool(re.search(r"\bselect\s+distinct\b", lower, re.IGNORECASE))

    # ---- Step 6: SELECT * 仅在无聚合时才阻断 ----
    # 注意: CTE 子查询中的 SELECT * 不影响外层有聚合的查询
    # 例如: WITH t AS (SELECT * FROM a) SELECT COUNT(*) FROM t → 应放行
    if not found_aggs and not has_group_by and not has_distinct:
        if re.search(r"\bselect\s+\*", lower, re.IGNORECASE):
            return GuardResult(
                allowed=False,
                sql_type="select_only",
                reason="禁止 SELECT *，统计类查询必须明确指定聚合字段",
            )

    # ---- Step 7: 判定是否为统计类 ----
    if found_aggs or has_group_by:
        agg_desc = ", ".join(found_aggs) if found_aggs else ("GROUP BY" if has_group_by else "")
        return GuardResult(
            allowed=True,
            sql_type="statistical",
            reason=f"统计类查询 ({agg_desc})" if agg_desc else "统计类查询",
            aggregate_functions=found_aggs,
            has_group_by=has_group_by,
            has_distinct=has_distinct,
        )

    # 有 DISTINCT 但无聚合函数 → 也视为统计类 (去重统计)
    if has_distinct:
        return GuardResult(
            allowed=True,
            sql_type="statistical",
            reason="统计类查询 (DISTINCT 去重)",
            has_distinct=True,
        )

    # 以上都不满足 → 纯 SELECT, 阻断
    return GuardResult(
        allowed=False,
        sql_type="select_only",
        reason="非统计类查询 (缺少聚合函数或 GROUP BY)，Bot 自动化不允许执行",
        aggregate_functions=[],
        has_group_by=False,
    )


def format_guard_result(result: GuardResult) -> str:
    """格式化守卫结果为可读文本 (用于 CLI 输出)

    Args:
        result: check_sql_type() 返回的 GuardResult 对象
    Returns:
        多行文本, 包含 PASS/BLOCK 状态、SQL 类型、原因、聚合函数等信息
    """
    status = "PASS" if result.allowed else "BLOCK"
    lines = [f"[SQL GUARD] {status} | Type: {result.sql_type}"]
    lines.append(f"  Reason: {result.reason}")
    if result.aggregate_functions:
        lines.append(f"  Aggregates: {', '.join(result.aggregate_functions)}")
    if result.has_group_by:
        lines.append(f"  GROUP BY: yes")
    if result.has_distinct:
        lines.append(f"  DISTINCT: yes")
    if result.blocked_keywords:
        lines.append(f"  Blocked: {len(result.blocked_keywords)} pattern(s)")
    return "\n".join(lines)
