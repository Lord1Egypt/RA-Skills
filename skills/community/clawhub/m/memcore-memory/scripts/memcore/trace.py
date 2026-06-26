"""
L1 Trace: 结构化步骤级记忆记录。

对标 MemOS L1: action + observation + reflection + value_score

将非结构化的每日 markdown 日志解析为结构化 trace entries，
同时保持向后兼容——不修改原文件，增量写入结构化索引。
"""

import json
import re
import sqlite3
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# --------------- Data Model ---------------

@dataclass
class TraceEntry:
    """单条记忆痕迹"""
    id: Optional[int] = None
    date: str = ""                      # YYYY-MM-DD
    session_id: str = ""                 # 会话标识（对话轮次）
    action: str = ""                    # 做了什么
    observation: str = ""               # 观察/结果
    reflection: str = ""                # 反思/教训
    value_score: float = 0.0           # 价值评分 (0.0-1.0)
    tags: list[str] = field(default_factory=list)  # 领域标签
    feedback_count: int = 0            # 被引用次数
    feedback_score: float = 0.0        # 累计反馈分
    source_file: str = ""              # 来源文件
    source_lines: str = ""             # 来源行号范围
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["tags"] = json.dumps(d["tags"])
        return d

    @classmethod
    def from_row(cls, row: tuple, columns: list[str]) -> "TraceEntry":
        d = dict(zip(columns, row))
        d["tags"] = json.loads(d.get("tags", "[]"))
        return cls(**d)


# --------------- Daily Log Parser ---------------

class DailyLogParser:
    """解析现有 memory/YYYY-MM-DD.md 文件 → 结构化 traces"""

    # 匹配模式：以 ## 开头的标题或 --- 分隔的段落
    SECTION_PAT = re.compile(r'^#{2,4}\s+(.+)$', re.MULTILINE)
    LESSON_PAT = re.compile(r'(教训|lesson|🚨|⚠️|💡|经验|错误)', re.IGNORECASE)
    ACTION_PAT = re.compile(r'(完成|执行|运行|修改|创建|删除|安装|配置|提交)', re.IGNORECASE)
    ERROR_PAT  = re.compile(r'(错误|失败|bug|error|❌|404|429|401|Connection error)', re.IGNORECASE)
    FIX_PAT    = re.compile(r'(修复|修复方案|解决|fix|✅|已修复)', re.IGNORECASE)

    @classmethod
    def parse_file(cls, filepath: Path) -> list[TraceEntry]:
        """解析单日日志 → trace entries"""
        if not filepath.exists():
            return []

        content = filepath.read_text(encoding="utf-8")
        entries = []
        sections = cls._split_sections(content)
        date_str = cls._extract_date(filepath)

        for i, (heading, body) in enumerate(sections):
            if not body.strip():
                continue

            entry = TraceEntry(
                date=date_str,
                session_id=f"{date_str}-{i:04d}",
                action=cls._extract_action(heading, body),
                observation=cls._extract_observation(body),
                reflection=cls._extract_reflection(body),
                value_score=cls._compute_value(heading, body),
                tags=cls._extract_tags(heading, body),
                source_file=str(filepath),
            )
            entries.append(entry)

        return entries

    @classmethod
    def _split_sections(cls, content: str) -> list[tuple[str, str]]:
        """将 markdown 按 ## 标题分段"""
        sections = []
        lines = content.split("\n")
        current_heading = ""
        current_body = []

        for line in lines:
            m = cls.SECTION_PAT.match(line)
            if m:
                if current_body:
                    sections.append((current_heading, "\n".join(current_body)))
                current_heading = m.group(1)
                current_body = []
            elif current_heading or line.strip():
                current_body.append(line)

        if current_body:
            sections.append((current_heading, "\n".join(current_body)))

        # 如果没有标题，整个文件作为一个段落
        if not sections and content.strip():
            sections.append(("", content.strip()))

        return sections

    @classmethod
    def _extract_date(cls, filepath: Path) -> str:
        """从文件名提取日期"""
        m = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.stem)
        return m.group(1) if m else ""

    @classmethod
    def _extract_action(cls, heading: str, body: str) -> str:
        """提取动作描述"""
        text = f"{heading} {body[:500]}"
        actions = cls.ACTION_PAT.findall(text)
        if actions:
            return "; ".join(actions[:3])
        # fallback: 取标题或前200字符
        return heading or body[:200].strip()

    @classmethod
    def _extract_observation(cls, body: str) -> str:
        """提取观察/结果"""
        # 取正文前500字作为观察
        lines = [l.strip() for l in body.split("\n") if l.strip() and not l.startswith("#")]
        return " ".join(lines[:5])[:500]

    @classmethod
    def _extract_reflection(cls, body: str) -> str:
        """提取反思/教训"""
        # 查找含关键词的段落
        for line in body.split("\n"):
            if cls.LESSON_PAT.search(line):
                return line.strip()[:300]
        return ""

    @classmethod
    def _compute_value(cls, heading: str, body: str) -> float:
        """计算初始价值评分"""
        score = 0.3  # 基线

        text = f"{heading} {body}"

        # 教训/错误相关：高价值
        if cls.LESSON_PAT.search(text):
            score += 0.3
        if cls.ERROR_PAT.search(text):
            score += 0.2  # 从错误中学到的最有价值
        if cls.FIX_PAT.search(text):
            score += 0.15

        # 内容长度：太短可能价值低，太长也有价值
        body_len = len(body)
        if 100 < body_len < 2000:
            score += 0.1
        elif body_len >= 2000:
            score += 0.05

        return min(score, 1.0)

    @classmethod
    def parse_session_state(cls, filepath: Path) -> list[TraceEntry]:
        """Parse SESSION-STATE.md (WAL Protocol) into high-priority traces.
        
        Extracts decisions, corrections, proper nouns, and specific values
        from the active session state file.
        """
        if not filepath.exists():
            return []
        
        content = filepath.read_text(encoding="utf-8")
        entries = []
        today = date.today().isoformat()
        
        # Extract key context table rows
        table_rows = re.findall(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', content)
        for i, (col1, col2, col3) in enumerate(table_rows):
            col1, col2, col3 = col1.strip(), col2.strip(), col3.strip()
            if col1 == "项目" or col1.startswith("-"):
                continue
            if col1 and col2:
                entry = TraceEntry(
                    date=today,
                    session_id=f"wal-{today}-{i:04d}",
                    action=f"WAL: {col1}",
                    observation=f"值: {col2} (来源: {col3})",
                    reflection=f"会话关键上下文: {col1} = {col2}",
                    value_score=0.75,
                    tags=["WAL", "session-state"],
                    source_file=str(filepath),
                )
                entries.append(entry)
        
        # Extract correction records
        correction_section = re.search(r'## 修正记录\n\n(.*?)(?=## |\Z)', content, re.DOTALL)
        if correction_section:
            corrections = [c.strip("> ") for c in correction_section.group(1).split("\n") if c.strip() and not c.startswith(">")]
            for i, corr in enumerate(corrections):
                if corr:
                    entries.append(TraceEntry(
                        date=today,
                        session_id=f"wal-corr-{today}-{i:04d}",
                        action="WAL 修正记录",
                        observation=corr[:500],
                        reflection=corr[:300],
                        value_score=0.85,
                        tags=["WAL", "correction"],
                        source_file=str(filepath),
                    ))
        
        return entries

    @classmethod
    def _extract_tags(cls, heading: str, body: str) -> list[str]:
        """提取领域标签"""
        text = f"{heading} {body}"
        tags = set()

        tag_map = {
            "报销": ["报销", "发票", "expense", "OCR"],
            "资产": ["资产", "基金", "股票", "汇丰", "致富", "恒生"],
            "配置": ["config", "配置文件", "模型", "model", "fallback"],
            "教训": ["教训", "错误", "🚨", "修复"],
            "同步": ["Syncthing", "同步", "sync"],
            "心跳": ["心跳", "heartbeat"],
            "归档": ["归档", "archive"],
            "代码": ["脚本", "python", "代码", "实现"],
            "汇率": ["汇率", "USD", "HKD", "CNY", "exchange"],
        }

        for tag, keywords in tag_map.items():
            for kw in keywords:
                if kw.lower() in text.lower():
                    tags.add(tag)
                    break

        return sorted(tags)


# --------------- Trace Index (SQLite) ---------------

class TraceIndex:
    """L1 traces 的 SQLite 索引"""

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS traces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        session_id TEXT NOT NULL,
        action TEXT,
        observation TEXT,
        reflection TEXT,
        value_score REAL DEFAULT 0.0,
        tags TEXT DEFAULT '[]',
        feedback_count INTEGER DEFAULT 0,
        feedback_score REAL DEFAULT 0.0,
        source_file TEXT,
        source_lines TEXT,
        created_at REAL,
        UNIQUE(session_id)
    );
    CREATE INDEX IF NOT EXISTS idx_traces_date ON traces(date);
    CREATE INDEX IF NOT EXISTS idx_traces_value ON traces(value_score DESC);
    CREATE INDEX IF NOT EXISTS idx_traces_tags ON traces(tags);
    """

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path.home() / ".openclaw" / "trace_index.db"
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.executescript(self.SCHEMA)

    def insert(self, entry: TraceEntry) -> int:
        """插入或更新一条 trace"""
        d = entry.to_dict()
        del d["id"]  # let DB auto-assign
        columns = ", ".join(d.keys())
        placeholders = ", ".join(["?"] * len(d))
        values = list(d.values())

        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                f"INSERT OR REPLACE INTO traces ({columns}) VALUES ({placeholders})",
                values
            )
            return conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    def insert_batch(self, entries: list[TraceEntry]) -> int:
        """批量插入"""
        count = 0
        with sqlite3.connect(str(self.db_path)) as conn:
            for entry in entries:
                d = entry.to_dict()
                del d["id"]
                columns = ", ".join(d.keys())
                placeholders = ", ".join(["?"] * len(d))
                try:
                    conn.execute(
                        f"INSERT OR REPLACE INTO traces ({columns}) VALUES ({placeholders})",
                        list(d.values())
                    )
                    count += 1
                except sqlite3.IntegrityError:
                    pass
        return count

    def search_by_date(self, dt: str, limit: int = 50) -> list[TraceEntry]:
        """按日期检索"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM traces WHERE date = ? ORDER BY value_score DESC LIMIT ?",
                (dt, limit)
            ).fetchall()
            return [TraceEntry.from_row(tuple(r), r.keys()) for r in rows]  # pyright: ignore[reportArgumentType]

    def search_by_tag(self, tag: str, limit: int = 20) -> list[TraceEntry]:
        """按标签检索"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM traces WHERE tags LIKE ? ORDER BY value_score DESC LIMIT ?",
                (f"%{tag}%", limit)
            ).fetchall()
            return [TraceEntry.from_row(tuple(r), r.keys()) for r in rows]  # pyright: ignore[reportArgumentType]

    def top_by_value(self, limit: int = 20) -> list[TraceEntry]:
        """价值最高的 traces"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM traces ORDER BY value_score DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [TraceEntry.from_row(tuple(r), r.keys()) for r in rows]  # pyright: ignore[reportArgumentType]

    def update_feedback(self, trace_id: int, score_delta: float):
        """更新反馈数据"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """UPDATE traces SET 
                   feedback_count = feedback_count + 1,
                   feedback_score = feedback_score + ?,
                   value_score = MIN(1.0, value_score + ?)
                WHERE id = ?""",
                (score_delta, score_delta * 0.1, trace_id)
            )

    def decay_values(self, decay_rate: float = 0.01):
        """全局价值衰减（未被访问的痕迹缓慢贬值）"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                "UPDATE traces SET value_score = MAX(0.05, value_score - ?) "
                "WHERE feedback_count = 0 AND value_score > 0.1",
                (decay_rate,)
            )

    def count(self) -> int:
        with sqlite3.connect(str(self.db_path)) as conn:
            return conn.execute("SELECT COUNT(*) FROM traces").fetchone()[0]

    def date_range(self) -> tuple[str, str]:
        with sqlite3.connect(str(self.db_path)) as conn:
            row = conn.execute(
                "SELECT MIN(date), MAX(date) FROM traces"
            ).fetchone()
            return (row[0] or "", row[1] or "")
