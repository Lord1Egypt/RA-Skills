"""
Three-Tier Retriever: 三级记忆检索器。

对标 MemOS 三级检索：Skill → Trace/Episode → World Model

检索优先级：
Tier 1: Skill（结晶化的可调用能力）— 精确匹配
Tier 2: Trace/Episode（具体经历/痕迹）— 语义相似
Tier 3: World Model（压缩原则/环境认知）— 兜底推理
"""

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class RetrievalResult:
    """单条检索结果"""
    tier: int                          # 1=Skill, 2=Trace, 3=WorldModel
    source: str                        # 来源路径
    content: str                       # 内容
    score: float                       # 相关性分数
    id: Optional[int] = None           # 数据库ID
    extra: dict = field(default_factory=dict)


class ThreeTierRetriever:
    """三层记忆检索器"""

    def __init__(
        self,
        trace_db: str = None,
        pattern_db: str = None,
        workspace_root: str = None,
    ):
        if workspace_root is None:
            workspace_root = str(Path.home() / ".openclaw" / "workspace")
        self.workspace_root = Path(workspace_root)

        if trace_db is None:
            trace_db = Path.home() / ".openclaw" / "trace_index.db"
        self.trace_db_path = Path(trace_db)

        if pattern_db is None:
            pattern_db = Path.home() / ".openclaw" / "pattern_index.db"
        self.pattern_db_path = Path(pattern_db)

    def retrieve(self, query: str, max_results: int = 10, 
                 adaptive: bool = True) -> list[RetrievalResult]:
        """主检索入口：按 Skill → Trace → WorldModel 三层依次返回。
        
        adaptive=True 时启用自适应降级：
          Tier 4: 换词重搜（同义词扩展）
          Tier 5: grep MEMORY.md 原始文件兜底
        """
        results = []
        search_log = []  # [(tier, query, count)]

        # Tier 1: Skill 精确匹配
        r = self._retrieve_skills(query, max_results=max_results // 2)
        results.extend(r)
        search_log.append((1, query, len(r)))

        # Tier 2: Trace 语义匹配（关键词 + 标签）
        r = self._retrieve_traces(query, max_results=max_results)
        results.extend(r)
        search_log.append((2, query, len(r)))

        # Tier 3: World Model 原则检索
        r = self._retrieve_world_model(query, max_results=max_results // 3)
        results.extend(r)
        search_log.append((3, query, len(r)))

        # 去重 + 排序
        results = self._deduplicate(results)
        results.sort(key=lambda r: (r.tier, -r.score))

        best_score = results[0].score if results else 0.0
        has_results = len(results) > 0 and best_score > 0.1

        # ── 自适应降级：如果前三层没命中或质量太低 ──
        if adaptive and (not has_results or best_score < 0.3):
            # Tier 4: 换词重搜（同义词扩展 + 分词重组）
            expanded_queries = self._expand_query(query)
            for eq in expanded_queries[:2]:  # 最多试2个变体
                if eq == query:
                    continue
                r = self._retrieve_traces(eq, max_results=max_results)
                r2 = self._retrieve_world_model(eq, max_results=2)
                fallback_results = r + r2
                if fallback_results:
                    search_log.append((4, eq, len(fallback_results)))
                    results.extend(fallback_results)
                    results = self._deduplicate(results)
                    results.sort(key=lambda r: (r.tier, -r.score))
                    best_score = results[0].score if results else 0.0
                    if best_score >= 0.3:
                        break

        # ── Tier 5: 终极兜底 — grep MEMORY.md 原文 ──
        if adaptive and (not has_results or best_score < 0.2):
            r = self._grep_memory_md(query, limit=5)
            if r:
                search_log.append((5, "grep MEMORY.md", len(r)))
                results.extend(r)
                results = self._deduplicate(results)
                results.sort(key=lambda r: (r.tier, -r.score))

        # 记录搜索日志用于反馈系统分析
        self._log_search(query, search_log)

        return results[:max_results]

    # --------- Tier 1: Skill ---------

    def _retrieve_skills(self, query: str, max_results: int = 5) -> list[RetrievalResult]:
        """在 skills/ 目录中搜索匹配的 Skill"""
        skills_dir = self.workspace_root / "skills"
        if not skills_dir.exists():
            return []

        results = []
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            try:
                content = skill_md.read_text(encoding="utf-8")
            except Exception:
                continue

            # 计算关键词匹配度
            content_lower = content.lower()
            desc_match = self._text_overlap_score(query_terms, content_lower[:500])
            full_match = self._text_overlap_score(query_terms, content_lower)

            score = desc_match * 0.6 + full_match * 0.4
            if score > 0.05:
                results.append(RetrievalResult(
                    tier=1,
                    source=f"skills/{skill_dir.name}",
                    content=self._extract_description(content),
                    score=score,
                ))

        results.sort(key=lambda r: -r.score)
        return results[:max_results]

    # --------- Tier 2: Trace ---------

    def _retrieve_traces(self, query: str, max_results: int = 10) -> list[RetrievalResult]:
        """在 L1 traces 和 patterns 中检索"""
        results = []

        # 从 traces DB 检索
        if self.trace_db_path.exists():
            results.extend(self._search_traces_db(query, max_results))

        # 从 patterns DB 检索
        if self.pattern_db_path.exists():
            results.extend(self._search_patterns_db(query, max_results // 3))

        return results

    def _search_traces_db(self, query: str, limit: int) -> list[RetrievalResult]:
        """SQLite FTS-like 关键词搜索 traces"""
        query_terms = [t for t in query.lower().split() if len(t) > 1]
        if not query_terms:
            # fallback: 返回最高价值 traces
            return self._top_value_traces(limit)

        with sqlite3.connect(str(self.trace_db_path)) as conn:
            conn.row_factory = sqlite3.Row

            # 构建 LIKE 查询
            conditions = []
            params = []
            for term in query_terms:
                like_str = f"%{term}%"
                conditions.append(
                    "(action LIKE ? OR observation LIKE ? OR reflection LIKE ? OR tags LIKE ?)"
                )
                params.extend([like_str, like_str, like_str, like_str])

            where = " OR ".join(conditions)
            rows = conn.execute(
                f"SELECT * FROM traces WHERE {where} "
                f"ORDER BY value_score DESC, date DESC LIMIT ?",
                params + [limit]
            ).fetchall()

            results = []
            for r in rows:
                d = dict(r)
                score = self._calculate_trace_relevance(query_terms, d)
                content_parts = []
                if d.get("action"):
                    content_parts.append(f"动作: {d['action']}")
                if d.get("observation"):
                    content_parts.append(f"观察: {d['observation'][:300]}")
                if d.get("reflection"):
                    content_parts.append(f"反思: {d['reflection'][:300]}")

                results.append(RetrievalResult(
                    tier=2,
                    source=d.get("source_file", f"trace/{d.get('date','')}"),
                    content="\n".join(content_parts),
                    score=score,
                    id=d["id"],
                    extra={"date": d.get("date", ""), "value": d.get("value_score", 0)},
                ))

        results.sort(key=lambda r: -r.score)
        return results

    def _top_value_traces(self, limit: int) -> list[RetrievalResult]:
        """返回价值最高的 traces"""
        with sqlite3.connect(str(self.trace_db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM traces ORDER BY value_score DESC LIMIT ?",
                (limit,)
            ).fetchall()

            return [RetrievalResult(
                tier=2,
                source=r["source_file"] or f"trace/{r['date']}",
                content=f"动作: {r['action']}\n观察: {r['observation'][:200]}",
                score=r["value_score"],
                id=r["id"],
            ) for r in rows]

    def _search_patterns_db(self, query: str, limit: int) -> list[RetrievalResult]:
        """检索 L2 patterns"""
        if not self.pattern_db_path.exists():
            return []

        query_terms = [t for t in query.lower().split() if len(t) > 1]
        with sqlite3.connect(str(self.pattern_db_path)) as conn:
            conn.row_factory = sqlite3.Row

            conditions = []
            params = []
            for term in query_terms:
                like_str = f"%{term}%"
                conditions.append("(name LIKE ? OR description LIKE ? OR tags LIKE ? OR trigger_keywords LIKE ?)")
                params.extend([like_str, like_str, like_str, like_str])

            where = " OR ".join(conditions)
            rows = conn.execute(
                f"SELECT * FROM patterns WHERE {where} ORDER BY frequency DESC LIMIT ?",
                params + [limit]
            ).fetchall()

            results = []
            for r in rows:
                solution = r["solution_template"] or "" if "solution_template" in r.keys() else ""
                results.append(RetrievalResult(
                    tier=2,
                    source=f"pattern/{r['name']}",
                    content=f"{r['description']}\n方案: {solution[:300]}",
                    score=r["confidence"],
                    id=r["id"],
                    extra={"frequency": r["frequency"]},
                ))
            return results

    # --------- Tier 3: World Model ---------

    def _retrieve_world_model(self, query: str, max_results: int = 3) -> list[RetrievalResult]:
        """检索 SOUL.md, AGENTS.md, MEMORY.md 等世界模型文件"""
        wm_files = [
            self.workspace_root / "SOUL.md",
            self.workspace_root / "AGENTS.md",
            self.workspace_root / "MEMORY.md",
        ]
        
        # ⭐ WAL/Buffer sources (from proactive-agent v3.1.0)
        session_state = self.workspace_root / "SESSION-STATE.md"
        if session_state.exists():
            wm_files.append(session_state)
        
        working_buffer = self.workspace_root / "memory" / "working-buffer.md"
        if working_buffer.exists():
            wb_content = working_buffer.read_text(encoding="utf-8")
            if "ACTIVE" in wb_content or "TEST" in wb_content:
                wm_files.append(working_buffer)  # 活跃 buffer 优先搜索

        results = []
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        for wm_file in wm_files:
            if not wm_file.exists():
                continue
            try:
                content = wm_file.read_text(encoding="utf-8")
            except Exception:
                continue

            # 分段落匹配
            sections = self._split_md_sections(content)
            for heading, body in sections:
                text = f"{heading} {body[:500]}"
                score = self._text_overlap_score(query_terms, text.lower())
                if score > 0.05:
                    results.append(RetrievalResult(
                        tier=3,
                        source=f"{wm_file.name}#{heading[:50]}" if heading else wm_file.name,
                        content=f"## {heading}\n{body[:500]}" if heading else body[:500],
                        score=score * 0.8,  # Tier 3 略降权
                    ))

        results.sort(key=lambda r: -r.score)
        return results[:max_results]

    # --------- Helpers ---------

    @staticmethod
    def _text_overlap_score(query_terms: set, text: str) -> float:
        """计算关键词重叠度"""
        if not query_terms:
            return 0.0
        hits = sum(1 for t in query_terms if t in text)
        return hits / len(query_terms)

    @staticmethod
    def _extract_description(skill_content: str) -> str:
        """提取 SKILL.md 的描述部分"""
        import re
        # 提取 frontmatter description 或第一个 ## 段
        m = re.search(r'description:\s*(.+)', skill_content)
        if m:
            return m.group(1)
        # fallback: 取前200字符
        return skill_content[:200].strip()

    @staticmethod
    def _split_md_sections(content: str) -> list[tuple[str, str]]:
        """分割 markdown 为标题+内容"""
        import re
        sections = []
        lines = content.split("\n")
        current_heading = ""
        current_body = []

        for line in lines:
            m = re.match(r'^#{1,4}\s+(.+)', line)
            if m:
                if current_body:
                    sections.append((current_heading, "\n".join(current_body)))
                current_heading = m.group(1)
                current_body = []
            else:
                current_body.append(line)

        if current_body:
            sections.append((current_heading, "\n".join(current_body)))

        return sections if sections else [("", content)]

    @staticmethod
    def _calculate_trace_relevance(query_terms: list[str], trace: dict) -> float:
        """计算 trace 与查询的相关性"""
        text_fields = [
            trace.get("action", ""),
            trace.get("observation", ""),
            trace.get("reflection", ""),
            trace.get("tags", "[]"),
        ]
        combined = " ".join(text_fields).lower()

        hits = sum(1 for t in query_terms if t in combined)
        base_score = hits / len(query_terms) if query_terms else 0.5

        # 价值分加权
        value = trace.get("value_score", 0.3)
        return base_score * 0.7 + value * 0.3

    @staticmethod
    def _deduplicate(results: list[RetrievalResult]) -> list[RetrievalResult]:
        """去重（按 source+content 前50字）"""
        seen = set()
        unique = []
        for r in results:
            key = (r.source, r.content[:50])
            if key not in seen:
                seen.add(key)
                unique.append(r)
        return unique

    # ── Adaptive Fallback Tier 4-5 ──

    @staticmethod
    def _expand_query(query: str) -> list[str]:
        """关键词扩展：同义词映射 + 分词变体"""
        import re
        
        # 同义词映射表
        SYNONYMS = {
            "报销": ["发票", "expense", "费用"],
            "配置": ["config", "设置", "修改"],
            "错误": ["bug", "失败", "error", "教训"],
            "心跳": ["heartbeat", "保活"],
            "资产": ["基金", "股票", "资产表", "汇丰", "致富"],
            "同步": ["syncthing", "sync", "复制"],
            "归档": ["archive", "备份"],
            "汇率": ["USD", "HKD", "CNY", "exchange"],
            "教训": ["lesson", "经验", "反思"],
        }
        
        queries = [query]
        
        # 词替换变体：每个中文词替换为同义词
        for word, synonyms in SYNONYMS.items():
            if word in query:
                for syn in synonyms[:2]:
                    queries.append(query.replace(word, syn))
        
        # 分词重组：只取前几个关键词
        words = re.findall(r'[\u4e00-\u9fff]{2,6}|[a-zA-Z]{3,}', query)
        if len(words) >= 3:
            # 去掉第一个词再搜
            queries.append(" ".join(words[1:]))
            # 只保留前两个词
            queries.append(" ".join(words[:2]))
        
        # 去重
        seen = set()
        unique = []
        for q in queries:
            if q not in seen:
                seen.add(q)
                unique.append(q)
        return unique

    def _grep_memory_md(self, query: str, limit: int = 5) -> list[RetrievalResult]:
        """Tier 5: grep MEMORY.md 原始文件兜底"""
        import subprocess, re
        
        memory_md = self.workspace_root / "MEMORY.md"
        if not memory_md.exists():
            return []
        
        # 中文：滑动2字gram；英文：3+字母
        keywords = []
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', query)
        for i in range(len(chinese_chars) - 1):
            bigram = ''.join(chinese_chars[i:i+2])
            if bigram not in keywords:
                keywords.append(bigram)
        keywords.extend(re.findall(r'[a-zA-Z]{3,}', query))
        
        if not keywords:
            keywords = [query]
        
        # 按常见度排序，优先用2-4字中文词
        keywords.sort(key=lambda w: -len(w) if any('\u4e00' <= c <= '\u9fff' for c in w) else len(w))
        
        # 用第一个（最长的）关键词 grep
        try:
            result = subprocess.run(
                ["grep", "-n", "-i", "-A", "2", "-B", "1", keywords[0], str(memory_md)],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                blocks = result.stdout.strip().split("--")
                grep_results = []
                for i, block in enumerate(blocks[:limit]):
                    block = block.strip()
                    if not block:
                        continue
                    score = 0.15 + (0.05 * (1 - i / max(len(blocks), 1)))
                    grep_results.append(RetrievalResult(
                        tier=5,
                        source="MEMORY.md (grep)",
                        content=block[:400],
                        score=score,
                        extra={"method": "grep", "keyword": keywords[0]},
                    ))
                return grep_results
        except Exception:
            pass
        
        return []

    def _log_search(self, query: str, search_log: list):
        """记录搜索过程到 feedback 系统，用于分析检索效果"""
        try:
            from pathlib import Path
            import sqlite3, time
            
            db_path = Path.home() / ".openclaw" / "feedback.db"
            with sqlite3.connect(str(db_path)) as conn:
                for tier, q, count in search_log:
                    conn.execute(
                        """INSERT OR IGNORE INTO search_log 
                           (query, tier, result_count, searched_at) 
                           VALUES (?, ?, ?, ?)""",
                        (q[:300], tier, count, time.time())
                    )
        except Exception:
            pass  # 搜索日志不影响主流程

    # ── Feedback-Driven Strategy Adjustment ──

    def should_retry_with_different_strategy(self, query: str) -> bool:
        """检查上次类似查询的反馈，决定是否换策略"""
        try:
            import sqlite3
            from pathlib import Path
            
            db_path = Path.home() / ".openclaw" / "feedback.db"
            if not db_path.exists():
                return False
            
            with sqlite3.connect(str(db_path)) as conn:
                # 查找相似查询的 skipped 比例
                query_words = set(query.lower().split())
                rows = conn.execute(
                    "SELECT query, was_used FROM reference_log ORDER BY retrieved_at DESC LIMIT 20"
                ).fetchall()
                
                skipped = 0
                total = 0
                for q, was_used in rows:
                    q_words = set((q or "").lower().split())
                    if query_words & q_words:  # 有关键词交集
                        total += 1
                        if not was_used:
                            skipped += 1
                
                # 如果过去类似查询有超过50%被跳过，建议换策略
                if total >= 3 and skipped / total > 0.5:
                    return True
        except Exception:
            pass
        
        return False
