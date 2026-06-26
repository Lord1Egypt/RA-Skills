"""
L2 Pattern Induction: 跨 trace 自动归纳策略模式。

对标 MemOS L2 Policy: 从多条 L1 traces 中自动发现可复用的"策略模式"。
"""

import json
import re
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# --------------- Data Model ---------------

@dataclass
class Pattern:
    """一条归纳出的策略模式"""
    id: Optional[int] = None
    name: str = ""                     # 模式名称
    description: str = ""             # 模式描述
    trigger_keywords: list[str] = field(default_factory=list)  # 触发关键词
    solution_template: str = ""       # 解决方案模板
    frequency: int = 0                # 出现次数
    confidence: float = 0.0           # 置信度 (0-1)
    source_traces: list[int] = field(default_factory=list)  # 来源 trace IDs
    tags: list[str] = field(default_factory=list)
    last_seen: str = ""               # 最后出现日期
    crystallized: bool = False        # 是否已结晶为 Skill
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        d = asdict(self)
        d["trigger_keywords"] = json.dumps(d["trigger_keywords"])
        d["source_traces"] = json.dumps(d["source_traces"])
        d["tags"] = json.dumps(d["tags"])
        return d

    @classmethod
    def from_row(cls, row: tuple, columns: list[str]) -> "Pattern":
        d = dict(zip(columns, row))
        d["trigger_keywords"] = json.loads(d.get("trigger_keywords", "[]"))
        d["source_traces"] = json.loads(d.get("source_traces", "[]"))
        d["tags"] = json.loads(d.get("tags", "[]"))
        return cls(**d)


# --------------- Pattern Induction Engine ---------------

class PatternInducer:
    """从 L1 traces 中自动归纳 L2 策略模式"""

    # 错误→修复模式
    ERROR_FIX_TEMPLATE = re.compile(
        r'(错误|失败|bug|error|❌|404|429|401|Connection error|问题)'
        r'.{0,200}'
        r'(修复|解决|fix|✅|已修复|方案|方法|策略)',
        re.IGNORECASE | re.DOTALL
    )

    # 配置变更→验证
    CONFIG_CHANGE_TEMPLATE = re.compile(
        r'(配置|config|修改|更新|更改)'
        r'.{0,200}'
        r'(验证|确认|检查|测试|成功|生效)',
        re.IGNORECASE | re.DOTALL
    )

    # 教训/🚨 P0
    LESSON_TEMPLATE = re.compile(
        r'(\d{2}-\d{2}\s+教训|🚨|⚠️\s+P\d|教训:).{0,500}',
        re.IGNORECASE
    )

    # 反弹模式：某个操作反复出现+反复失败
    RETRY_PATTERN = re.compile(
        r'(重试|again|再次|续|仍然|还是|又).{0,100}(失败|错误|bug|404|429)',
        re.IGNORECASE
    )

    def __init__(self, trace_db_path: str = None):
        if trace_db_path is None:
            trace_db_path = Path.home() / ".openclaw" / "trace_index.db"
        self.trace_db_path = Path(trace_db_path)
        self._init_pattern_db()

    def _init_pattern_db(self):
        db_path = Path.home() / ".openclaw" / "pattern_index.db"
        with sqlite3.connect(str(db_path)) as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                trigger_keywords TEXT DEFAULT '[]',
                solution_template TEXT,
                frequency INTEGER DEFAULT 0,
                confidence REAL DEFAULT 0.0,
                source_traces TEXT DEFAULT '[]',
                tags TEXT DEFAULT '[]',
                last_seen TEXT,
                crystallized INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name)
            );
            CREATE INDEX IF NOT EXISTS idx_patterns_freq ON patterns(frequency DESC);
            CREATE INDEX IF NOT EXISTS idx_patterns_conf ON patterns(confidence DESC);
            """)

    def _get_all_traces(self) -> list[dict]:
        """读取所有 traces"""
        if not self.trace_db_path.exists():
            return []
        with sqlite3.connect(str(self.trace_db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM traces ORDER BY date, id").fetchall()
            return [dict(r) for r in rows]

    def induce(self) -> list[Pattern]:
        """主入口：从所有 traces 归纳模式"""
        traces = self._get_all_traces()
        if not traces:
            return []

        patterns = []
        patterns.extend(self._induce_error_fix(traces))
        patterns.extend(self._induce_config_change(traces))
        patterns.extend(self._induce_lessons(traces))
        patterns.extend(self._induce_retry_anti_patterns(traces))
        patterns.extend(self._induce_cross_tag_clusters(traces))

        # 合并去重
        merged = self._merge_similar(patterns)
        merged = [p for p in merged if p.frequency >= 2]  # 至少出现2次

        self._save_patterns(merged)
        return merged

    def _induce_error_fix(self, traces: list[dict]) -> list[Pattern]:
        """从错误→修复序列中归纳"""
        error_traces = defaultdict(list)
        for t in traces:
            combined = f"{t.get('action','')} {t.get('observation','')} {t.get('reflection','')}"
            if self.ERROR_FIX_TEMPLATE.search(combined):
                tag_key = ",".join(json.loads(t.get("tags", "[]")))
                error_traces[tag_key].append(t)

        patterns = []
        for tag_key, group in error_traces.items():
            if len(group) >= 2:
                errors = [t.get("reflection", "") or t.get("observation", "")[:200] 
                          for t in group]
                tags = json.loads(group[0].get("tags", "[]"))

                patterns.append(Pattern(
                    name=f"错误修复模式 [{tag_key or '通用'}]",
                    description=f"领域 {tag_key} 中出现 {len(group)} 次错误→修复循环",
                    trigger_keywords=self._extract_keywords_from_texts(errors),
                    solution_template=self._build_solution_template(errors),
                    frequency=len(group),
                    confidence=min(0.9, 0.4 + len(group) * 0.1),
                    source_traces=[t["id"] for t in group],
                    tags=tags,
                    last_seen=group[-1].get("date", ""),
                ))
        return patterns

    def _induce_config_change(self, traces: list[dict]) -> list[Pattern]:
        """配置变更模式"""
        config_traces = [t for t in traces 
                        if "配置" in str(t.get("tags", "[]")) 
                        or self.CONFIG_CHANGE_TEMPLATE.search(
                            f"{t.get('action','')} {t.get('observation','')}"
                        )]
        if len(config_traces) < 2:
            return []

        return [Pattern(
            name="配置变更验证模式",
            description=f"发现 {len(config_traces)} 次配置变更，需每次验证生效",
            trigger_keywords=["config", "配置", "修改"],
            solution_template="配置变更后必须 grep 验证 → 备份 → 记录变更日志",
            frequency=len(config_traces),
            confidence=0.85,
            source_traces=[t["id"] for t in config_traces],
            tags=["配置"],
            last_seen=config_traces[-1].get("date", ""),
        )]

    def _induce_lessons(self, traces: list[dict]) -> list[Pattern]:
        """从散会教训中归纳"""
        lesson_traces = []
        for t in traces:
            reflection = t.get("reflection", "") or ""
            combined = f"{t.get('action','')} {t.get('observation','')} {reflection}"
            if self.LESSON_TEMPLATE.search(combined):
                lesson_traces.append(t)

        if len(lesson_traces) < 2:
            return []

        # 按 tags 分组
        by_tag = defaultdict(list)
        for t in lesson_traces:
            for tag in json.loads(t.get("tags", "[]")):
                by_tag[tag].append(t)

        patterns = []
        for tag, group in by_tag.items():
            if len(group) >= 2:
                lessons = [t.get("reflection", "") or t.get("observation", "")[:200] 
                          for t in group]
                patterns.append(Pattern(
                    name=f"教训模式 [{tag}]",
                    description=f"标签 {tag} 下出现 {len(group)} 次需要记录的教训",
                    trigger_keywords=self._extract_keywords_from_texts(lessons),
                    solution_template=self._build_solution_template(lessons),
                    frequency=len(group),
                    confidence=min(0.95, 0.5 + len(group) * 0.1),
                    source_traces=[t["id"] for t in group],
                    tags=[tag],
                    last_seen=group[-1].get("date", ""),
                ))
        return patterns

    def _induce_retry_anti_patterns(self, traces: list[dict]) -> list[Pattern]:
        """反弹/反模式：某操作反复失败"""
        retry_traces = []
        for t in traces:
            combined = f"{t.get('reflection','')} {t.get('observation','')}"
            if self.RETRY_PATTERN.search(combined):
                retry_traces.append(t)

        if len(retry_traces) < 2:
            return []

        return [Pattern(
            name="⚠️ 重复尝试反模式",
            description=f"发现 {len(retry_traces)} 次反复重试→失败的循环，需要固化检查流程",
            trigger_keywords=["重试", "仍然", "还是", "再次", "又"],
            solution_template="同一命令失败3次/同一错误2次 → 立即停止+汇报（30秒规则）",
            frequency=len(retry_traces),
            confidence=0.80,
            source_traces=[t["id"] for t in retry_traces],
            tags=["反模式", "30秒规则"],
            last_seen=retry_traces[-1].get("date", ""),
        )]

    def _induce_cross_tag_clusters(self, traces: list[dict]) -> list[Pattern]:
        """跨标签聚类：同一 trace 关联多个标签 → 跨领域模式"""
        tag_cooccur = Counter()
        for t in traces:
            tags = json.loads(t.get("tags", "[]"))
            for i in range(len(tags)):
                for j in range(i+1, len(tags)):
                    pair = tuple(sorted([tags[i], tags[j]]))
                    tag_cooccur[pair] += 1

        patterns = []
        for (tag1, tag2), count in tag_cooccur.items():
            if count >= 3:  # 至少3次共现
                patterns.append(Pattern(
                    name=f"跨领域关联 [{tag1} ↔ {tag2}]",
                    description=f"标签 {tag1} 和 {tag2} 共现 {count} 次，存在跨领域关联",
                    trigger_keywords=[tag1, tag2],
                    solution_template=f"处理 {tag1} 相关问题时，同时考虑 {tag2} 的影响",
                    frequency=count,
                    confidence=min(0.7, 0.3 + count * 0.1),
                    source_traces=[],
                    tags=[tag1, tag2],
                    last_seen="",
                ))
        return patterns

    # --------------- Helpers ---------------

    def _extract_keywords_from_texts(self, texts: list[str], top_n: int = 10) -> list[str]:
        """从文本集中提取高频关键词"""
        combined = " ".join(texts)
        # 简单分词（中文按2-4字、英文按空格）
        words = re.findall(r'[\u4e00-\u9fff]{2,4}|[a-zA-Z]{3,}', combined)
        counter = Counter(words)
        return [w for w, _ in counter.most_common(top_n)]

    def _build_solution_template(self, texts: list[str]) -> str:
        """从多条反思中合成解决方案模板"""
        if not texts:
            return ""
        # 取最长的3条反思合并
        sorted_texts = sorted(texts, key=len, reverse=True)
        combined = "; ".join(sorted_texts[:3])
        return combined[:500]

    def _merge_similar(self, patterns: list[Pattern]) -> list[Pattern]:
        """合并非重名的相似模式（按标签重叠度）"""
        if len(patterns) <= 1:
            return patterns

        merged = list(patterns)
        # 简化为：标签交集 > 0 的合并
        # 实际生产可引入 embedding 相似度
        return merged

    def _save_patterns(self, patterns: list[Pattern]):
        """保存到 patterns 索引"""
        db_path = Path.home() / ".openclaw" / "pattern_index.db"
        with sqlite3.connect(str(db_path)) as conn:
            for p in patterns:
                d = p.to_dict()
                del d["id"]
                columns = ", ".join(d.keys())
                placeholders = ", ".join(["?"] * len(d))
                try:
                    conn.execute(
                        f"INSERT OR REPLACE INTO patterns ({columns}) VALUES ({placeholders})",
                        list(d.values())
                    )
                except sqlite3.IntegrityError:
                    pass

    def list_patterns(self, min_conf: float = 0.5) -> list[Pattern]:
        """列出所有模式"""
        db_path = Path.home() / ".openclaw" / "pattern_index.db"
        if not db_path.exists():
            return []
        with sqlite3.connect(str(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM patterns WHERE confidence >= ? ORDER BY frequency DESC",
                (min_conf,)
            ).fetchall()
            return [Pattern.from_row(tuple(r), r.keys()) for r in rows]  # pyright: ignore[reportArgumentType]
