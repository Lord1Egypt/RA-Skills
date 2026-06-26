#!/usr/bin/env python3
"""
上下文检索器 - 2000章架构核心组件
6级分层摘要（book→phase→arc→volume→chapter→scene）
事实相关性引擎 + 章节范围预过滤 + 智能上下文预算分配
"""

import os
import json
import sqlite3
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# 检测 numpy 可用性
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class ContextRetriever:
    """上下文检索器 - 6级分层上下文组装"""

    # 上下文预算分配（总预算 ~12000 字符）
    BUDGET = {
        "book_summary": 600,       # 全书摘要
        "current_state": 800,      # 当前状态
        "phase_summary": 400,      # 阶段摘要
        "arc_summary": 600,        # 弧线摘要
        "volume_summary": 800,     # 卷摘要
        "prev_chapter_summary": 1200,  # 前章摘要
        "current_chapter_summary": 800,  # 当前章已有内容摘要
        "related_scenes": 2500,    # 相关场景片段
        "relevant_facts": 2500,    # 相关事实
        "hooks": 600,              # 活跃伏笔（缩减200给engagement）
        "continuity_notes": 400,   # 连续性提示（缩减100给engagement）
        "engagement": 500,         # 追读力上下文
    }

    def __init__(self, db_path: str, project_path: str = None):
        """
        初始化上下文检索器

        Args:
            db_path: SQLite 数据库路径
            project_path: 项目根路径
        """
        self.db_path = Path(db_path)
        self.project_path = Path(project_path) if project_path else self.db_path.parent.parent
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")

    def _read_project_config(self) -> Dict[str, Any]:
        """读取项目配置"""
        config_path = self.project_path / "data" / "project_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"settings": {"chapters_per_volume": 20}}

    def _read_constraints(self) -> Dict[str, Any]:
        """读取项目约束规则"""
        config = self._read_project_config()
        return config.get("constraints", {})

    def _get_volume_for_chapter(self, chapter: int) -> int:
        """计算卷号"""
        config = self._read_project_config()
        cpv = config.get("settings", {}).get("chapters_per_volume", 20)
        return (chapter - 1) // cpv + 1

    def _truncate(self, text: str, budget: int) -> str:
        """按字符预算截断文本"""
        if not text:
            return ""
        if len(text) <= budget:
            return text
        # 优先在句号处截断
        truncated = text[:budget]
        last_punct = max(
            truncated.rfind("。"),
            truncated.rfind("！"),
            truncated.rfind("？"),
            truncated.rfind(".")
        )
        if last_punct > budget * 0.6:
            return truncated[:last_punct + 1] + "..."
        return truncated + "..."

    # ==================== 6级分层查询 ====================

    def _get_book_summary(self) -> str:
        """L0: 全书摘要"""
        cur = self.conn.cursor()
        cur.execute("SELECT content FROM summaries WHERE level='book' AND range_desc='全书'")
        row = cur.fetchone()
        return row["content"] if row else ""

    def _get_current_state(self) -> str:
        """L0: 当前状态（滚动更新）"""
        cur = self.conn.cursor()
        cur.execute("SELECT content FROM summaries WHERE level='book' AND range_desc='current_state'")
        row = cur.fetchone()
        return row["content"] if row else ""

    def _get_phase_summary(self, chapter: int) -> str:
        """L1: 阶段摘要"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT s.content FROM summaries s
            JOIN arcs a ON s.range_desc = a.id
            WHERE s.level = 'phase'
            AND a.arc_type = 'phase'
            AND a.start_chapter <= ? AND (a.end_chapter IS NULL OR a.end_chapter >= ?)
        """, (chapter, chapter))
        row = cur.fetchone()
        return row["content"] if row else ""

    def _get_arc_summary(self, chapter: int) -> str:
        """L2: 弧线摘要"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT s.content FROM summaries s
            JOIN arcs a ON s.range_desc = a.id
            WHERE s.level = 'arc'
            AND a.arc_type = 'arc'
            AND a.start_chapter <= ? AND (a.end_chapter IS NULL OR a.end_chapter >= ?)
        """, (chapter, chapter))
        row = cur.fetchone()
        return row["content"] if row else ""

    def _get_volume_summary(self, volume: int) -> str:
        """L3: 卷摘要"""
        cur = self.conn.cursor()
        cur.execute("SELECT content FROM summaries WHERE level='volume' AND range_desc=?",
                   (str(volume),))
        row = cur.fetchone()
        return row["content"] if row else ""

    def _get_chapter_summary(self, chapter: int) -> str:
        """L4: 章节摘要"""
        cur = self.conn.cursor()
        cur.execute("SELECT content FROM summaries WHERE level='chapter' AND range_desc=?",
                   (str(chapter),))
        row = cur.fetchone()
        return row["content"] if row else ""

    def _get_recent_scenes(self, chapter: int, limit: int = 5) -> List[Dict[str, Any]]:
        """L5: 最近场景片段"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, content, chapter, location, characters, mood, events
            FROM scenes_content
            WHERE chapter = ? OR chapter = ?
            ORDER BY chapter DESC, id DESC
            LIMIT ?
        """, (chapter, max(1, chapter - 1), limit))
        return [dict(row) for row in cur.fetchall()]

    def _get_related_scenes(self, query: str, chapter: int,
                            top_k: int = 5) -> List[Dict[str, Any]]:
        """语义/关键词搜索相关场景"""
        try:
            from memory_engine import MemoryEngine
            engine = MemoryEngine(str(self.db_path), project_path=str(self.project_path))
            try:
                # 搜索范围: 当前弧线章节范围
                cur = self.conn.cursor()
                cur.execute("""
                    SELECT start_chapter, end_chapter FROM arcs
                    WHERE arc_type = 'arc' AND start_chapter <= ?
                    AND (end_chapter IS NULL OR end_chapter >= ?)
                """, (chapter, chapter))
                arc_row = cur.fetchone()
                chapter_range = None
                if arc_row:
                    chapter_range = (arc_row[0], arc_row[1] or chapter + 50)
                results = engine.search(query, top_k=top_k, chapter_range=chapter_range)
                return results
            finally:
                engine.close()
        except Exception:
            return []

    def _get_relevant_facts(self, chapter: int,
                            entities: List[str] = None,
                            max_facts: int = 80) -> List[Dict[str, Any]]:
        """事实相关性检索"""
        try:
            from fact_engine import FactEngine
            fact_engine = FactEngine(str(self.db_path), project_path=str(self.project_path))
            try:
                return fact_engine.get_relevant_facts(chapter, entities, max_facts)
            finally:
                fact_engine.close()
        except Exception:
            return []

    def _get_active_hooks(self, chapter: int) -> List[Dict[str, Any]]:
        """获取活跃伏笔"""
        try:
            from hook_tracker import HookTracker
            tracker = HookTracker(str(self.db_path))
            try:
                return tracker.get_open_hooks(chapter)
            finally:
                tracker.close()
        except Exception:
            return []

    def _get_engagement_context(self, chapter: int) -> Dict[str, Any]:
        """获取追读力上下文（最近评分+债务摘要+紧迫伏笔）"""
        try:
            from engagement_tracker import EngagementTracker
            tracker = EngagementTracker(str(self.db_path))
            try:
                # 最近5章评分
                recent = tracker.get_recent_metrics(chapter, limit=5)
                # 债务摘要
                debt = tracker.get_debt_report(chapter)
                return {
                    "recent_metrics": recent,
                    "debt_summary": debt.get("summary", {}),
                    "debt_level": debt.get("summary", {}).get("debt_level", "healthy")
                }
            finally:
                tracker.close()
        except Exception:
            return {}

    # ==================== 上下文组装 ====================

    def retrieve_for_creation(self, chapter: int, query: str = "",
                              mentioned_entities: List[str] = None,
                              max_chars: int = 12000,
                              max_facts: int = 80) -> Dict[str, Any]:
        """
        为创作组装完整上下文（2000章架构核心方法）

        6级分层摘要 + 事实相关性 + 伏笔状态 + 连续性提示

        Args:
            chapter: 目标章节
            query: 创作意图/大纲描述
            mentioned_entities: 大纲中提及的实体
            max_chars: 上下文字符预算上限

        Returns:
            结构化上下文字典
        """
        volume = self._get_volume_for_chapter(chapter)
        context = {}
        total_chars = 0

        # L0: 全书摘要
        text = self._get_book_summary()
        context["book_summary"] = self._truncate(text, self.BUDGET["book_summary"])
        total_chars += len(context["book_summary"])

        # L0: 当前状态
        text = self._get_current_state()
        context["current_state"] = self._truncate(text, self.BUDGET["current_state"])
        total_chars += len(context["current_state"])

        # L1: 阶段摘要
        text = self._get_phase_summary(chapter)
        context["phase_summary"] = self._truncate(text, self.BUDGET["phase_summary"])
        total_chars += len(context["phase_summary"])

        # L2: 弧线摘要
        text = self._get_arc_summary(chapter)
        context["arc_summary"] = self._truncate(text, self.BUDGET["arc_summary"])
        total_chars += len(context["arc_summary"])

        # L3: 卷摘要
        text = self._get_volume_summary(volume)
        context["volume_summary"] = self._truncate(text, self.BUDGET["volume_summary"])
        total_chars += len(context["volume_summary"])

        # L4: 前章摘要
        if chapter > 1:
            text = self._get_chapter_summary(chapter - 1)
            context["prev_chapter_summary"] = self._truncate(text, self.BUDGET["prev_chapter_summary"])
        else:
            context["prev_chapter_summary"] = ""
        total_chars += len(context["prev_chapter_summary"])

        # L4: 当前章已有内容摘要（续写场景）
        text = self._get_chapter_summary(chapter)
        context["current_chapter_summary"] = self._truncate(text, self.BUDGET["current_chapter_summary"])
        total_chars += len(context["current_chapter_summary"])

        # L5: 相关场景
        if query:
            scenes = self._get_related_scenes(query, chapter, top_k=5)
        else:
            scenes = self._get_recent_scenes(chapter, limit=5)
        scene_texts = []
        remaining_budget = self.BUDGET["related_scenes"]
        for scene in scenes:
            scene_text = f"[第{scene.get('chapter','')}章] {scene.get('content','')[:200]}"
            if len(scene_text) > remaining_budget:
                break
            scene_texts.append(scene_text)
            remaining_budget -= len(scene_text)
        context["related_scenes"] = "\n".join(scene_texts)
        total_chars += len(context["related_scenes"])

        # 事实相关性
        facts = self._get_relevant_facts(chapter, mentioned_entities, max_facts=max_facts)
        fact_texts = []
        remaining_budget = self.BUDGET["relevant_facts"]
        for fact in facts:
            fact_text = f"[{fact.get('category','')}] {fact.get('entity','')}.{fact.get('attribute','')} = {fact.get('value','')}"
            if len(fact_text) > remaining_budget:
                break
            fact_texts.append(fact_text)
            remaining_budget -= len(fact_text)
        context["relevant_facts"] = "\n".join(fact_texts)
        total_chars += len(context["relevant_facts"])

        # 活跃伏笔
        hooks = self._get_active_hooks(chapter)
        hook_texts = []
        remaining_budget = self.BUDGET["hooks"]
        for hook in hooks[:10]:
            hook_text = f"[{hook.get('priority','')}] 第{hook.get('planted_chapter','')}章埋: {hook.get('desc','')}"
            if len(hook_text) > remaining_budget:
                break
            hook_texts.append(hook_text)
            remaining_budget -= len(hook_text)
        context["hooks"] = "\n".join(hook_texts)
        total_chars += len(context["hooks"])

        # 连续性提示
        continuity = self._build_continuity_notes(chapter, facts, hooks)
        context["continuity_notes"] = self._truncate(continuity, self.BUDGET["continuity_notes"])
        total_chars += len(context["continuity_notes"])

        # 追读力上下文
        engagement_ctx = self._get_engagement_context(chapter)
        engagement_text = self._format_engagement_text(engagement_ctx)
        context["engagement"] = self._truncate(engagement_text, self.BUDGET["engagement"])
        context["engagement_data"] = engagement_ctx
        total_chars += len(context["engagement"])

        context["metadata"] = {
            "chapter": chapter,
            "volume": volume,
            "total_chars": total_chars,
            "budget_used_pct": round(total_chars / max_chars * 100, 1),
            "facts_count": len(facts),
            "hooks_count": len(hooks),
            "scenes_count": len(scenes),
        }

        # 约束规则（从 project_config.json 读取）
        constraints = self._read_constraints()
        if constraints:
            context["constraints"] = constraints

        return context

    def _build_continuity_notes(self, chapter: int, facts: List[Dict],
                                hooks: List[Dict]) -> str:
        """构建连续性提示"""
        notes = []

        # 伏笔超期预警
        overdue = [h for h in hooks if h.get("expected_resolve") and
                   h["expected_resolve"] < chapter and h.get("status") == "open"]
        if overdue:
            notes.append(f"[伏笔预警] {len(overdue)}个伏笔已超期未收线")

        # 事实矛盾检测
        entity_attrs = {}
        for f in facts:
            key = (f.get("entity", ""), f.get("attribute", ""))
            if key in entity_attrs:
                notes.append(f"[矛盾风险] {f['entity']}.{f['attribute']} 存在多个值")
            else:
                entity_attrs[key] = f.get("value", "")

        # 位置连续性
        recent_scenes = self._get_recent_scenes(chapter, limit=3)
        if recent_scenes and len(recent_scenes) >= 2:
            locations = [s.get("location", "") for s in recent_scenes if s.get("location")]
            if len(set(locations)) > 1:
                notes.append(f"[位置变化] 近期场景位置: {' → '.join(locations)}")

        return "\n".join(notes)

    def _format_engagement_text(self, engagement_ctx: Dict[str, Any]) -> str:
        """格式化追读力上下文为文本"""
        if not engagement_ctx:
            return ""

        parts = []
        recent = engagement_ctx.get("recent_metrics", [])
        if recent:
            pace_list = []
            for m in recent:
                ch = m.get("chapter", "?")
                pt = m.get("pace_type", "-")
                rp = m.get("reader_pull", "-")
                pace_list.append(f"第{ch}章({pt},拉力{rp})")
            parts.append("近期节奏: " + " → ".join(pace_list))

        debt_summary = engagement_ctx.get("debt_summary", {})
        debt_level = engagement_ctx.get("debt_level", "healthy")
        if debt_level != "healthy":
            overdue = debt_summary.get("overdue_count", 0)
            forgotten = debt_summary.get("forgotten_count", 0)
            parts.append(f"[债务{debt_level}] 超期{overdue}个,遗忘{forgotten}个")

        return "\n".join(parts)

    def format_context(self, context: Dict[str, Any]) -> str:
        """将结构化上下文格式化为可读文本"""
        parts = []

        if context.get("book_summary"):
            parts.append(f"=== 全书概览 ===\n{context['book_summary']}")
        if context.get("current_state"):
            parts.append(f"=== 当前进展 ===\n{context['current_state']}")
        if context.get("phase_summary"):
            parts.append(f"=== 当前阶段 ===\n{context['phase_summary']}")
        if context.get("arc_summary"):
            parts.append(f"=== 当前弧线 ===\n{context['arc_summary']}")
        if context.get("volume_summary"):
            parts.append(f"=== 当前卷 ===\n{context['volume_summary']}")
        if context.get("prev_chapter_summary"):
            parts.append(f"=== 前章回顾 ===\n{context['prev_chapter_summary']}")
        if context.get("current_chapter_summary"):
            parts.append(f"=== 本章已有内容 ===\n{context['current_chapter_summary']}")
        if context.get("related_scenes"):
            parts.append(f"=== 相关场景 ===\n{context['related_scenes']}")
        if context.get("relevant_facts"):
            parts.append(f"=== 相关事实 ===\n{context['relevant_facts']}")
        if context.get("hooks"):
            parts.append(f"=== 活跃伏笔 ===\n{context['hooks']}")
        if context.get("continuity_notes"):
            parts.append(f"=== 连续性提示 ===\n{context['continuity_notes']}")
        if context.get("engagement"):
            parts.append(f"=== 追读力 ===\n{context['engagement']}")

        return "\n\n".join(parts)

    def close(self):
        """关闭连接"""
        self.conn.close()


    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        # 自动推断章节号
        chapter = params.get("chapter")
        if chapter is None:
            try:
                from fact_engine import FactEngine
                fe = FactEngine(self.db_path, project_path=params.get("project_path"))
                try:
                    chapter = fe.get_latest_chapter()
                finally:
                    fe.close()
            except Exception:
                chapter = 1
            if chapter == 0:
                chapter = 1
        else:
            chapter = int(chapter)

        if action == "for-creation":
            entities_str = params.get("entities")
            entities = [e.strip() for e in entities_str.split(",") if e.strip()] if entities_str else None
            max_facts = int(params.get("max_facts", 80))
            context = self.retrieve_for_creation(
                chapter, params.get("query", ""), entities,
                int(params.get("max_chars", 12000)),
                max_facts=max_facts
            )
            fmt = params.get("format", "structured")
            if fmt == "text":
                return {
                    "text": self.format_context(context),
                    "metadata": context.get("metadata", {})
                }
            return context

        elif action == "for-review":
            context = self.retrieve_for_creation(
                chapter, params.get("query", ""), None,
                int(params.get("max_chars", 12000))
            )
            return context

        elif action == "hierarchy":
            prev_ch = max(1, chapter - 1)
            volume = self._get_volume_for_chapter(chapter)
            return {
                "L0_book": bool(self._get_book_summary()),
                "L0_current_state": bool(self._get_current_state()),
                "L1_phase": bool(self._get_phase_summary(chapter)),
                "L2_arc": bool(self._get_arc_summary(chapter)),
                "L3_volume": bool(self._get_volume_summary(volume)),
                "L4_prev_chapter": bool(self._get_chapter_summary(prev_ch)),
                "L4_current_chapter": bool(self._get_chapter_summary(chapter)),
                "chapter": chapter,
                "volume": volume,
            }

        elif action == "budget-report":
            context = self.retrieve_for_creation(chapter, params.get("query", ""))
            report = {}
            for key in ["book_summary", "current_state", "phase_summary", "arc_summary",
                         "volume_summary", "prev_chapter_summary", "current_chapter_summary",
                         "related_scenes", "relevant_facts", "hooks", "continuity_notes"]:
                budget = self.BUDGET.get(key, 0)
                used = len(context.get(key, ""))
                report[key] = {
                    "budget": budget,
                    "used": used,
                    "pct": round(used / budget * 100, 1) if budget > 0 else 0
                }
            return report

        else:
            raise ValueError(f"未知操作: {action}")

def main():
    parser = argparse.ArgumentParser(description='上下文检索器')
    parser.add_argument('--db-path', required=True, help='数据库路径')
    parser.add_argument('--action', required=True,
                       choices=['for-creation', 'for-review', 'hierarchy',
                               'budget-report'],
                       help='操作类型')
    parser.add_argument('--chapter', type=int, default=None, help='目标章节（省略时自动推断）')
    parser.add_argument('--query', help='创作意图/大纲')
    parser.add_argument('--entities', help='提及实体(逗号分隔)')
    parser.add_argument('--project-path', help='项目根路径')
    parser.add_argument('--max-chars', type=int, default=12000, help='上下文字符上限')
    parser.add_argument('--format', choices=['structured', 'text'], default='structured',
                       help='输出格式')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    retriever = ContextRetriever(args.db_path, args.project_path)

    try:
        skip_keys = {"db_path", "project_path", "action", "output"}
        params = {k: v for k, v in vars(args).items()
                  if v is not None and k not in skip_keys and not k.startswith('_')}
        result = retriever.execute_action(args.action, params)
    finally:
        retriever.close()

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
