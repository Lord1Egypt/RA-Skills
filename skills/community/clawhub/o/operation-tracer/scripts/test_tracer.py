"""
operation-tracer 测试用例
验证追踪器和分析器的完整功能。
"""
import os
import sys
import time
import json
import tempfile
import unittest
from pathlib import Path

# 添加 scripts 目录到 path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from tracer import OperationTracer, Span
from analyzer import TraceAnalyzer


class TestOperationTracer(unittest.TestCase):
    """追踪器测试"""

    def setUp(self):
        """创建临时数据库"""
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp_dir, "test_traces.db")
        self.tracer = OperationTracer(db_path=self.db_path)

    def tearDown(self):
        """清理临时文件"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_start_span_returns_id(self):
        """start_span 返回 span_id"""
        span_id = self.tracer.start_span("test_op", "tool_call")
        self.assertIsNotNone(span_id)
        self.assertEqual(len(span_id), 8)

    def test_start_span_with_metadata(self):
        """start_span 支持元数据"""
        span_id = self.tracer.start_span(
            "read_file", "tool_call", {"path": "/tmp/test"}
        )
        spans = self.tracer.get_active_spans()
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0].name, "read_file")
        self.assertEqual(spans[0].metadata["path"], "/tmp/test")
        self.assertEqual(spans[0].metadata["operation_type"], "tool_call")

    def test_end_span_persists_to_sqlite(self):
        """end_span 持久化到 SQLite"""
        span_id = self.tracer.start_span("test_op", "tool_call")
        time.sleep(0.01)  # 确保有耗时
        self.tracer.end_span(span_id, result="done", status="success")

        # 验证活跃列表已清空
        self.assertEqual(len(self.tracer.get_active_spans()), 0)

        # 验证数据库中有记录
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT * FROM traces WHERE id = ?", (span_id,))
        row = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], span_id)  # id
        self.assertEqual(row[3], "test_op")  # operation_name
        self.assertEqual(row[7], "success")  # status

    def test_end_span_unknown_id_ignored(self):
        """end_span 对未知 span_id 静默忽略"""
        # 不应抛出异常
        self.tracer.end_span("nonexistent", result="ignored")

    def test_multiple_spans(self):
        """支持多个并发 span"""
        id1 = self.tracer.start_span("op1", "tool_call")
        id2 = self.tracer.start_span("op2", "llm_call")
        id3 = self.tracer.start_span("op3", "error")

        self.assertEqual(len(self.tracer.get_active_spans()), 3)

        self.tracer.end_span(id1, status="success")
        self.assertEqual(len(self.tracer.get_active_spans()), 2)

        self.tracer.end_span(id2, status="error", result="timeout")
        self.tracer.end_span(id3, status="success")
        self.assertEqual(len(self.tracer.get_active_spans()), 0)


class TestTraceAnalyzer(unittest.TestCase):
    """分析器测试"""

    def setUp(self):
        """创建临时数据库并填充测试数据"""
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp_dir, "test_traces.db")
        self.tracer = OperationTracer(db_path=self.db_path)
        self.analyzer = TraceAnalyzer(db_path=self.db_path)

        # 填充测试数据
        self.span1 = self.tracer.start_span("read_file", "tool_call", {"path": "/a"})
        time.sleep(0.02)
        self.tracer.end_span(self.span1, result="ok", status="success")

        self.span2 = self.tracer.start_span("web_search", "tool_call")
        time.sleep(0.05)
        self.tracer.end_span(self.span2, result="timeout", status="error")

        self.span3 = self.tracer.start_span("gpt4", "llm_call")
        time.sleep(0.01)
        self.tracer.end_span(self.span3, result="response", status="success")

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_get_summary(self):
        """get_summary 返回正确统计"""
        summary = self.analyzer.get_summary()

        self.assertEqual(summary["total_spans"], 3)
        self.assertGreater(summary["avg_duration_ms"], 0)
        self.assertIn("read_file", summary["by_operation"])
        self.assertIn("web_search", summary["by_operation"])
        self.assertEqual(summary["by_operation"]["web_search"]["error_count"], 1)
        self.assertIn("success", summary["by_status"])
        self.assertIn("error", summary["by_status"])
        self.assertEqual(summary["by_status"]["success"], 2)
        self.assertEqual(summary["by_status"]["error"], 1)
        self.assertIn("tool_call", summary["by_type"])
        self.assertIn("llm_call", summary["by_type"])

    def test_get_slow_operations(self):
        """get_slow_operations 返回慢操作"""
        # 阈值设为 0ms，所有操作都应返回
        slow = self.analyzer.get_slow_operations(threshold_ms=0, limit=10)
        self.assertEqual(len(slow), 3)
        # 应按耗时降序排列
        self.assertGreaterEqual(slow[0]["duration_ms"], slow[1]["duration_ms"])

        # 高阈值应返回空
        slow_high = self.analyzer.get_slow_operations(threshold_ms=999999)
        self.assertEqual(len(slow_high), 0)

    def test_get_error_operations(self):
        """get_error_operations 返回错误操作"""
        errors = self.analyzer.get_error_operations()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["operation_name"], "web_search")
        self.assertEqual(errors[0]["error"], "timeout")

    def test_export_json(self):
        """export 支持 JSON 格式"""
        data = self.analyzer.export(format="json")
        parsed = json.loads(data)
        self.assertEqual(len(parsed), 3)
        # 验证字段完整
        first = parsed[0]
        self.assertIn("id", first)
        self.assertIn("timestamp", first)
        self.assertIn("operation_type", first)
        self.assertIn("operation_name", first)
        self.assertIn("duration_ms", first)
        self.assertIn("status", first)

    def test_export_csv(self):
        """export 支持 CSV 格式"""
        data = self.analyzer.export(format="csv")
        lines = data.strip().split("\n")
        self.assertEqual(len(lines), 4)  # header + 3 rows
        self.assertIn("id", lines[0])
        self.assertIn("operation_name", lines[0])

    def test_export_unsupported_format(self):
        """export 不支持的格式抛出异常"""
        with self.assertRaises(ValueError):
            self.analyzer.export(format="xml")

    def test_cleanup(self):
        """cleanup 清理旧数据"""
        # 手动插入一条旧数据（timestamp 设为 30 天前）
        import sqlite3
        old_timestamp = time.time() - (30 * 24 * 60 * 60)
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """INSERT INTO traces (id, timestamp, operation_type, operation_name, duration_ms, metadata, result, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            ("old_span", old_timestamp, "tool_call", "old_op", 100, "{}", "old", "success"),
        )
        conn.commit()
        conn.close()

        # 清理 7 天前的数据
        result = self.analyzer.cleanup(days=7)
        self.assertEqual(result["deleted"], 1)
        self.assertEqual(result["days"], 7)

        # 验证旧数据已删除，新数据保留
        summary = self.analyzer.get_summary()
        self.assertEqual(summary["total_spans"], 3)  # 只剩原来的3条


if __name__ == "__main__":
    unittest.main()
