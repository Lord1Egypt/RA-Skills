"""
Trace Analyzer - 追踪数据分析器
提供追踪数据的统计、查询、导出和清理功能。
"""
import sqlite3
import json
import time
from typing import Optional


class TraceAnalyzer:
    """追踪数据分析器"""

    def __init__(self, db_path: str = "traces/agent_traces.db"):
        self.db_path = db_path

    def get_summary(self) -> dict:
        """获取追踪摘要

        Returns:
            摘要 dict，包含：
            - total_spans: 总追踪数
            - avg_duration_ms: 平均耗时
            - by_operation: 按操作名统计
            - by_status: 按状态统计
            - by_type: 按类型统计
        """
        conn = sqlite3.connect(self.db_path)

        # 总体统计
        cursor = conn.execute("SELECT COUNT(*), AVG(duration_ms) FROM traces")
        total_count, avg_duration = cursor.fetchone()

        # 按操作名统计
        cursor = conn.execute("""
            SELECT operation_name, COUNT(*), AVG(duration_ms),
                   SUM(CASE WHEN status='error' THEN 1 ELSE 0 END)
            FROM traces GROUP BY operation_name
        """)
        by_operation = {}
        for name, count, avg_ms, err_count in cursor.fetchall():
            by_operation[name] = {
                "count": count,
                "avg_duration_ms": round(avg_ms or 0, 2),
                "error_count": err_count,
            }

        # 按状态统计
        cursor = conn.execute(
            "SELECT status, COUNT(*) FROM traces GROUP BY status"
        )
        by_status = dict(cursor.fetchall())

        # 按类型统计
        cursor = conn.execute("""
            SELECT operation_type, COUNT(*), AVG(duration_ms)
            FROM traces GROUP BY operation_type
        """)
        by_type = {}
        for op_type, count, avg_ms in cursor.fetchall():
            by_type[op_type] = {
                "count": count,
                "avg_duration_ms": round(avg_ms or 0, 2),
            }

        conn.close()

        return {
            "total_spans": total_count or 0,
            "avg_duration_ms": round(avg_duration or 0, 2),
            "by_operation": by_operation,
            "by_status": by_status,
            "by_type": by_type,
        }

    def get_slow_operations(self, threshold_ms: float = 1000, limit: int = 10) -> list:
        """获取耗时最长的操作

        Args:
            threshold_ms: 耗时阈值（毫秒）
            limit: 返回数量限制

        Returns:
            慢操作列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT id, operation_name, operation_type, duration_ms, timestamp, status
            FROM traces
            WHERE duration_ms > ?
            ORDER BY duration_ms DESC
            LIMIT ?
        """, (threshold_ms, limit))

        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "operation_name": row[1],
                "operation_type": row[2],
                "duration_ms": row[3],
                "timestamp": row[4],
                "status": row[5],
            })

        conn.close()
        return results

    def get_error_operations(self, limit: int = 10) -> list:
        """获取错误操作列表

        Args:
            limit: 返回数量限制

        Returns:
            错误操作列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT id, operation_name, operation_type, duration_ms, timestamp, result
            FROM traces
            WHERE status = 'error'
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))

        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "operation_name": row[1],
                "operation_type": row[2],
                "duration_ms": row[3],
                "timestamp": row[4],
                "error": row[5],
            })

        conn.close()
        return results

    def export(self, format: str = "json") -> str:
        """导出追踪数据

        Args:
            format: "json" 或 "csv"

        Returns:
            导出的数据字符串
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT id, timestamp, operation_type, operation_name,
                   duration_ms, metadata, result, status
            FROM traces ORDER BY timestamp
        """)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if format == "json":
            return json.dumps(rows, ensure_ascii=False, indent=2)
        elif format == "csv":
            if not rows:
                return ""
            headers = list(rows[0].keys())
            lines = [",".join(headers)]
            for row in rows:
                lines.append(",".join(str(row.get(h, "")) for h in headers))
            return "\n".join(lines)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def cleanup(self, days: int = 7):
        """清理旧追踪数据

        Args:
            days: 保留天数

        Returns:
            清理结果 dict
        """
        cutoff = time.time() - (days * 24 * 60 * 60)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("DELETE FROM traces WHERE timestamp < ?", (cutoff,))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        return {"deleted": deleted, "days": days}
