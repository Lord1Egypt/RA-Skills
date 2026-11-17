"""
Operation Tracer - SQLite 操作追踪器
记录工具调用、LLM调用、错误和压缩操作的追踪跨度。
"""
import sqlite3
import time
import json
import uuid
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field


@dataclass
class Span:
    """追踪跨度"""
    id: str
    name: str
    start_time: float
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    metadata: dict = field(default_factory=dict)
    result: Optional[str] = None
    status: str = "running"  # running / success / error


class OperationTracer:
    """操作追踪器"""

    def __init__(self, db_path: str = "traces/agent_traces.db"):
        self.db_path = db_path
        self._active_spans: dict[str, Span] = {}
        self._ensure_db()

    def _ensure_db(self):
        """确保数据库和表存在"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS traces (
                id TEXT PRIMARY KEY,
                timestamp REAL NOT NULL,
                operation_type TEXT,
                operation_name TEXT,
                duration_ms REAL,
                metadata TEXT,
                result TEXT,
                status TEXT DEFAULT 'running'
            )
        """)
        conn.commit()
        conn.close()

    def start_span(self, name: str, op_type: str, metadata: dict = None) -> str:
        """开始追踪一个操作

        Args:
            name: 操作名称
            op_type: 操作类型（tool_call / llm_call / error / compression）
            metadata: 附加元数据

        Returns:
            span_id: 追踪跨度ID
        """
        span_id = str(uuid.uuid4())[:8]
        span = Span(
            id=span_id,
            name=name,
            start_time=time.time(),
            metadata=metadata or {},
        )
        span.metadata["operation_type"] = op_type
        self._active_spans[span_id] = span
        return span_id

    def end_span(self, span_id: str, result: Any = None, status: str = "success"):
        """结束追踪

        Args:
            span_id: 追踪跨度ID
            result: 操作结果
            status: 状态（success / error）
        """
        if span_id not in self._active_spans:
            return

        span = self._active_spans[span_id]
        span.end_time = time.time()
        span.duration_ms = (span.end_time - span.start_time) * 1000
        span.result = str(result) if result is not None else None
        span.status = status

        # 持久化到 SQLite
        self._save_span(span)

        # 从活跃列表移除
        self._active_spans.pop(span_id, None)

    def _save_span(self, span: Span):
        """保存 span 到数据库"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """INSERT OR REPLACE INTO traces
               (id, timestamp, operation_type, operation_name, duration_ms, metadata, result, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                span.id,
                span.start_time,
                span.metadata.get("operation_type", "unknown"),
                span.name,
                span.duration_ms,
                json.dumps(span.metadata, ensure_ascii=False),
                span.result,
                span.status,
            ),
        )
        conn.commit()
        conn.close()

    def get_active_spans(self) -> list:
        """获取当前活跃的 span"""
        return list(self._active_spans.values())
