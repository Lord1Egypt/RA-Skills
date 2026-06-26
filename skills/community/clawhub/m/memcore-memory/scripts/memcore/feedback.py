"""
Feedback Loop: 记忆反馈闭环。

对标 MemOS 的双通道反馈：
- Step-level（模型↔环境：工具调用成功/失败）
- Task-level（人类↔模型：显式/隐式评分）

实现：
- 记忆引用追踪（哪些 trace/pattern 被使用了）
- 反馈信号归一化
- 价值反向传播（高价值记忆升值，未引用记忆衰减）
"""

import json
import sqlite3
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


@dataclass
class FeedbackEvent:
    """一次反馈事件"""
    trace_id: int                      # 目标 trace ID
    feedback_type: str                 # "explicit" | "implicit" | "error" | "success"
    score: float                       # -1.0 到 1.0
    source: str = ""                   # 来源（"user", "tool_result", "reflection"）
    note: str = ""                     # 备注
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "feedback_type": self.feedback_type,
            "score": self.score,
            "source": self.source,
            "note": self.note,
            "timestamp": self.timestamp,
        }


class FeedbackLoop:
    """记忆反馈闭环管理器"""

    # 反馈分映射到 trace value 的权重
    FEEDBACK_WEIGHTS = {
        "explicit": 0.15,    # 用户显式评价
        "implicit": 0.05,    # 隐式（使用了记忆）
        "error": 0.20,       # 错误反馈（价值高）
        "success": 0.03,     # 成功反馈
    }

    # ── VFM 评分维度 (proactive-agent v3.1.0) ──
    VFM_DIMENSIONS = {
        "frequency":      {"weight": 3.0, "desc": "高频使用"},
        "failure_reduction": {"weight": 3.0, "desc": "避免失败"},
        "user_burden":    {"weight": 2.0, "desc": "减轻用户负担"},
        "self_cost":      {"weight": 2.0, "desc": "节省自身成本"},
    }
    VFM_THRESHOLD = 50  # 低于此分的改动不执行

    # 衰减参数
    DECAY_RATE = 0.005        # 每次全局衰减率
    DECAY_INTERVAL_HOURS = 24 # 衰减间隔

    def __init__(self, trace_db: str = None, pattern_db: str = None):
        if trace_db is None:
            trace_db = Path.home() / ".openclaw" / "trace_index.db"
        self.trace_db_path = Path(trace_db)

        if pattern_db is None:
            pattern_db = Path.home() / ".openclaw" / "pattern_index.db"
        self.pattern_db_path = Path(pattern_db)

        self._init_feedback_db()

    def _init_feedback_db(self):
        db_path = Path.home() / ".openclaw" / "feedback.db"
        with sqlite3.connect(str(db_path)) as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS feedback_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trace_id INTEGER NOT NULL,
                feedback_type TEXT NOT NULL,
                score REAL NOT NULL,
                source TEXT DEFAULT '',
                note TEXT DEFAULT '',
                timestamp REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_fb_trace ON feedback_events(trace_id);
            CREATE INDEX IF NOT EXISTS idx_fb_time ON feedback_events(timestamp);

            CREATE TABLE IF NOT EXISTS reference_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trace_id INTEGER,
                pattern_id INTEGER,
                query TEXT,
                retrieved_at REAL NOT NULL,
                was_used INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS search_log (
                query TEXT,
                tier INTEGER,
                result_count INTEGER,
                searched_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS decay_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                last_decay_at REAL NOT NULL
            );
            INSERT OR IGNORE INTO decay_state (id, last_decay_at) VALUES (1, 0);
            """)

    # --------- 记录反馈 ---------

    def record_explicit(self, trace_id: int, score: float, note: str = ""):
        """记录显式用户反馈（如用户说"这条有用"/"不对"）"""
        self._apply_feedback(FeedbackEvent(
            trace_id=trace_id,
            feedback_type="explicit",
            score=max(-1.0, min(1.0, score)),
            source="user",
            note=note,
        ))

    def record_implicit(self, trace_id: int, was_used: bool = True):
        """记录隐式反馈（某条记忆被检索/引用）"""
        if was_used:
            self._apply_feedback(FeedbackEvent(
                trace_id=trace_id,
                feedback_type="implicit",
                score=0.05,  # 小正向
                source="retrieval",
            ))
        self._log_reference(trace_id=trace_id, was_used=was_used)

    def record_error_feedback(self, trace_id: int, error_desc: str = ""):
        """记录错误反馈（某条教训再次被触发）"""
        self._apply_feedback(FeedbackEvent(
            trace_id=trace_id,
            feedback_type="error",
            score=0.3,  # 错误反馈权重高——从错误中学到的最有价值
            source="tool_result",
            note=error_desc,
        ))

    def record_success_feedback(self, trace_id: int):
        """记录成功反馈（遵循某条策略成功）"""
        self._apply_feedback(FeedbackEvent(
            trace_id=trace_id,
            feedback_type="success",
            score=0.03,
            source="tool_result",
        ))

    # --------- 检索引用追踪 ---------

    def log_retrieval(self, query: str, results: list):
        """记录一次检索事件（哪些 traces 被返回了）"""
        now = time.time()
        db_path = Path.home() / ".openclaw" / "feedback.db"
        with sqlite3.connect(str(db_path)) as conn:
            for r in results:
                if hasattr(r, 'id') and r.id:
                    conn.execute(
                        "INSERT INTO reference_log (trace_id, query, retrieved_at) VALUES (?,?,?)",
                        (r.id, query[:200], now)
                    )
                if hasattr(r, 'extra') and r.extra.get("pattern_id"):
                    conn.execute(
                        "INSERT INTO reference_log (pattern_id, query, retrieved_at) VALUES (?,?,?)",
                        (r.extra["pattern_id"], query[:200], now)
                    )

    def mark_used(self, trace_ids: list[int]):
        """标记哪些 traces 实际被使用了"""
        db_path = Path.home() / ".openclaw" / "feedback.db"
        with sqlite3.connect(str(db_path)) as conn:
            for tid in trace_ids:
                conn.execute(
                    "UPDATE reference_log SET was_used = 1 WHERE trace_id = ?",
                    (tid,)
                )
                # 隐式正向反馈
                self.record_implicit(tid, was_used=True)

    # --------- 衰减 ---------

    def vfm_score_trace(self, trace: dict) -> dict:
        """VFM 四维评分 (proactive-agent v3.1.0)"""
        dims = {}
        freq = trace.get("feedback_count", 0) + 1
        dims["frequency"] = min(10, freq) * 7
        text = " ".join([trace.get("action",""), trace.get("reflection",""),
                        trace.get("observation","")]).lower()
        error_kw = sum(1 for kw in ["error","bug","fix","fail","wrong"]
                      if kw in text)
        dims["failure_reduction"] = min(30, error_kw * 10)
        refl_len = len(trace.get("reflection", ""))
        dims["user_burden"] = 18 if 20 < refl_len <= 100 else (12 if 100 < refl_len <= 300 else 6)
        used = trace.get("feedback_count", 0)
        dims["self_cost"] = min(20, used * 5)
        total = sum(dims.values())
        return {"total": total, "dimensions": dims, "verdict": "adopt" if total >= 50 else "skip"}

    def apply_decay_if_needed(self):
        """如果到了衰减周期，全局衰减未引用记忆"""
        db_path = Path.home() / ".openclaw" / "feedback.db"
        with sqlite3.connect(str(db_path)) as conn:
            row = conn.execute("SELECT last_decay_at FROM decay_state WHERE id=1").fetchone()
            if not row:
                return

            last_decay = row[0]
            now = time.time()
            interval_seconds = self.DECAY_INTERVAL_HOURS * 3600

            if now - last_decay < interval_seconds:
                return

            # 执行衰减
            if self.trace_db_path.exists():
                with sqlite3.connect(str(self.trace_db_path)) as conn2:
                    # 衰减未被引用的 traces
                    conn2.execute(
                        """UPDATE traces SET value_score = MAX(0.05, value_score - ?)
                           WHERE feedback_count = 0 
                           AND created_at < ?""",
                        (self.DECAY_RATE, now - interval_seconds)
                    )

            conn.execute("UPDATE decay_state SET last_decay_at = ? WHERE id=1", (now,))

    # --------- 统计 ---------

    def get_stats(self) -> dict:
        """反馈统计概览"""
        db_path = Path.home() / ".openclaw" / "feedback.db"
        with sqlite3.connect(str(db_path)) as conn:
            total_feedback = conn.execute(
                "SELECT COUNT(*) FROM feedback_events"
            ).fetchone()[0]

            total_refs = conn.execute(
                "SELECT COUNT(*) FROM reference_log"
            ).fetchone()[0]

            used_refs = conn.execute(
                "SELECT COUNT(*) FROM reference_log WHERE was_used = 1"
            ).fetchone()[0]

            use_rate = used_refs / total_refs if total_refs > 0 else 0

        return {
            "total_feedback": total_feedback,
            "total_references": total_refs,
            "used_references": used_refs,
            "use_rate": use_rate,
            "last_decay": self._get_last_decay(),
        }

    # --------- Internal ---------

    def _apply_feedback(self, event: FeedbackEvent):
        """应用反馈到 trace value"""
        # 保存事件
        db_path = Path.home() / ".openclaw" / "feedback.db"
        with sqlite3.connect(str(db_path)) as conn:
            conn.execute(
                """INSERT INTO feedback_events 
                   (trace_id, feedback_type, score, source, note, timestamp) 
                   VALUES (?,?,?,?,?,?)""",
                (event.trace_id, event.feedback_type, event.score,
                 event.source, event.note, event.timestamp)
            )

        # 更新 trace 的 value_score
        if self.trace_db_path.exists():
            weight = self.FEEDBACK_WEIGHTS.get(event.feedback_type, 0.05)
            delta = event.score * weight
            with sqlite3.connect(str(self.trace_db_path)) as conn:
                conn.execute(
                    """UPDATE traces SET 
                       feedback_count = feedback_count + 1,
                       feedback_score = feedback_score + ?,
                       value_score = MIN(1.0, MAX(0.05, value_score + ?))
                    WHERE id = ?""",
                    (event.score, delta, event.trace_id)
                )

    def _log_reference(self, trace_id: int = None, pattern_id: int = None, was_used: bool = False):
        """记录检索引用"""
        db_path = Path.home() / ".openclaw" / "feedback.db"
        with sqlite3.connect(str(db_path)) as conn:
            conn.execute(
                "INSERT INTO reference_log (trace_id, pattern_id, retrieved_at, was_used) VALUES (?,?,?,?)",
                (trace_id, pattern_id, time.time(), 1 if was_used else 0)
            )

    def _get_last_decay(self) -> str:
        db_path = Path.home() / ".openclaw" / "feedback.db"
        with sqlite3.connect(str(db_path)) as conn:
            row = conn.execute("SELECT last_decay_at FROM decay_state WHERE id=1").fetchone()
            if row and row[0] > 0:
                return datetime.fromtimestamp(row[0]).isoformat()
            return "never"
