#!/usr/bin/env python3
"""
弧线管理器 - 管理创作弧线和阶段
支持: 创建弧线/阶段、分配章节、追踪进度、检查完成度
数据存储在 novel_memory.db 的 arcs 表中
改进: progress 和 suggest-next 的 --chapter 参数改为可选，未提供时自动推断
"""

import os
import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class ArcManager:
    """弧线管理器"""

    def __init__(self, db_path: str, project_path: str = None):
        self.db_path = Path(db_path)
        self.project_path = Path(project_path) if project_path else self.db_path.parent.parent
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._ensure_tables()

    def _ensure_tables(self):
        """确保所需表存在（支持独立使用，无需依赖 MemoryEngine 先建表）"""
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS arcs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                arc_type TEXT NOT NULL DEFAULT 'arc',
                start_chapter INTEGER NOT NULL,
                end_chapter INTEGER,
                phase_id TEXT,
                description TEXT DEFAULT '',
                created_at TEXT,
                updated_at TEXT
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_arcs_type ON arcs(arc_type)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_arcs_phase ON arcs(phase_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_arcs_start ON arcs(start_chapter)")

        # scenes_content 表用于自动推断最新章节
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scenes_content (
                id INTEGER PRIMARY KEY,
                content TEXT,
                tags TEXT,
                chapter INTEGER,
                location TEXT,
                characters TEXT,
                mood TEXT,
                events TEXT
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_scenes_chapter ON scenes_content(chapter)")

        self.conn.commit()

    def create_phase(self, phase_id: str, title: str,
                     start_chapter: int, end_chapter: int = None,
                     description: str = "") -> str:
        """创建阶段"""
        now = datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO arcs (id, title, arc_type, start_chapter, end_chapter,
                phase_id, description, created_at, updated_at)
            VALUES (?, ?, 'phase', ?, ?, NULL, ?, ?, ?)
        """, (phase_id, title, start_chapter, end_chapter, description, now, now))
        self.conn.commit()
        return phase_id

    def create_arc(self, arc_id: str, title: str,
                   start_chapter: int, end_chapter: int = None,
                   phase_id: str = None, description: str = "") -> str:
        """创建弧线"""
        now = datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO arcs (id, title, arc_type, start_chapter, end_chapter,
                phase_id, description, created_at, updated_at)
            VALUES (?, ?, 'arc', ?, ?, ?, ?, ?, ?)
        """, (arc_id, title, start_chapter, end_chapter, phase_id, description, now, now))
        self.conn.commit()
        return arc_id

    def get_arc(self, arc_id: str) -> Optional[Dict[str, Any]]:
        """获取弧线"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM arcs WHERE id = ?", (arc_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_active_arc(self, chapter: int) -> Optional[Dict[str, Any]]:
        """获取指定章节的活跃弧线"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM arcs
            WHERE arc_type = 'arc'
            AND start_chapter <= ?
            AND (end_chapter IS NULL OR end_chapter >= ?)
            ORDER BY start_chapter DESC LIMIT 1
        """, (chapter, chapter))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_active_phase(self, chapter: int) -> Optional[Dict[str, Any]]:
        """获取指定章节的活跃阶段"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM arcs
            WHERE arc_type = 'phase'
            AND start_chapter <= ?
            AND (end_chapter IS NULL OR end_chapter >= ?)
            ORDER BY start_chapter DESC LIMIT 1
        """, (chapter, chapter))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_arcs_in_phase(self, phase_id: str) -> List[Dict[str, Any]]:
        """获取阶段下的所有弧线"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM arcs WHERE arc_type = 'arc' AND phase_id = ?
            ORDER BY start_chapter
        """, (phase_id,))
        return [dict(row) for row in cur.fetchall()]

    def list_phases(self) -> List[Dict[str, Any]]:
        """列出所有阶段"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM arcs WHERE arc_type = 'phase' ORDER BY start_chapter")
        return [dict(row) for row in cur.fetchall()]

    def list_arcs(self, phase_id: str = None) -> List[Dict[str, Any]]:
        """列出弧线"""
        cur = self.conn.cursor()
        if phase_id:
            cur.execute("""
                SELECT * FROM arcs WHERE arc_type = 'arc' AND phase_id = ?
                ORDER BY start_chapter
            """, (phase_id,))
        else:
            cur.execute("SELECT * FROM arcs WHERE arc_type = 'arc' ORDER BY start_chapter")
        return [dict(row) for row in cur.fetchall()]

    def complete_arc(self, arc_id: str, end_chapter: int) -> bool:
        """完成弧线"""
        now = datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE arcs SET end_chapter = ?, updated_at = ? WHERE id = ?
        """, (end_chapter, now, arc_id))
        self.conn.commit()
        return cur.rowcount > 0

    def get_latest_chapter(self) -> int:
        """从 scenes_content 表查询已存储的最新章节号"""
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT MAX(chapter) FROM scenes_content")
            row = cur.fetchone()
            return row[0] if row and row[0] is not None else 0
        except sqlite3.OperationalError:
            return 0

    def get_progress(self, current_chapter: int = None) -> Dict[str, Any]:
        """
        获取整体进度

        Args:
            current_chapter: 当前章节号（可选，未提供时自动推断）
        """
        auto_inferred = current_chapter is None
        if current_chapter is None:
            current_chapter = self.get_latest_chapter()

        cur = self.conn.cursor()
        result = {
            "current_chapter": current_chapter,
            "auto_inferred": auto_inferred,
            "active_phase": None,
            "active_arc": None,
            "phases": [],
            "arcs": [],
        }

        # 当前阶段
        phase = self.get_active_phase(current_chapter)
        if phase:
            result["active_phase"] = phase

        # 当前弧线
        arc = self.get_active_arc(current_chapter)
        if arc:
            result["active_arc"] = arc

        # 所有阶段
        phases = self.list_phases()
        for p in phases:
            status = "进行中"
            if p.get("end_chapter") and p["end_chapter"] < current_chapter:
                status = "已完成"
            elif p["start_chapter"] > current_chapter:
                status = "未开始"
            p["status"] = status
            result["phases"].append(p)

        # 所有弧线
        arcs = self.list_arcs()
        for a in arcs:
            status = "进行中"
            if a.get("end_chapter") and a["end_chapter"] < current_chapter:
                status = "已完成"
            elif a["start_chapter"] > current_chapter:
                status = "未开始"
            a["status"] = status
            result["arcs"].append(a)

        return result

    def suggest_next_arc(self, current_chapter: int = None) -> Optional[Dict[str, Any]]:
        """
        建议下一个弧线（含追读力维度）

        Args:
            current_chapter: 当前章节号（可选，未提供时自动推断）
        """
        if current_chapter is None:
            current_chapter = self.get_latest_chapter()

        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM arcs
            WHERE arc_type = 'arc'
            AND start_chapter > ?
            ORDER BY start_chapter LIMIT 1
        """, (current_chapter,))
        row = cur.fetchone()

        result = {"current_chapter": current_chapter}

        if row:
            result["next_arc"] = dict(row)

        # 追读力维度建议
        engagement_tips = self._get_engagement_tips(current_chapter)
        if engagement_tips:
            result["engagement_tips"] = engagement_tips

        if not row:
            result["suggestion"] = None
            result["message"] = "暂无待开始的弧线，可使用 create-arc-am 创建"

        return result

    def _get_engagement_tips(self, current_chapter: int) -> List[str]:
        """基于追读力数据的创作建议"""
        tips = []
        try:
            from engagement_tracker import EngagementTracker
            tracker = EngagementTracker(str(self.db_path))
            try:
                # 债务报告
                debt = tracker.get_debt_report(current_chapter)
                debt_level = debt.get("summary", {}).get("debt_level", "healthy")
                if debt_level in ("high", "critical"):
                    overdue = debt.get("overdue_hooks", [])[:3]
                    if overdue:
                        descs = [h.get("desc", "")[:20] for h in overdue]
                        tips.append(f"叙事债务{debt_level}: 建议优先回收伏笔「{'、'.join(descs)}」")

                # 节奏建议
                pacing = tracker.get_pacing_report(
                    from_chapter=max(1, current_chapter - 10),
                    to_chapter=current_chapter
                )
                for suggestion in pacing.get("suggestions", []):
                    tips.append(suggestion.get("msg", ""))

                # 趋势
                trend_data = tracker.get_trend(
                    from_chapter=max(1, current_chapter - 10),
                    to_chapter=current_chapter
                )
                if trend_data.get("trend") == "declining":
                    tips.append("追读力近期下降趋势，建议增加冲突或悬念")
            finally:
                tracker.close()
        except Exception:
            pass
        return tips

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "create-phase":
            phase_id = params.get("phase_id") or params.get("arc_id")
            title = params.get("title") or params.get("arc_title")
            start_chapter = params.get("start_chapter")
            if not phase_id or not title or start_chapter is None:
                raise ValueError("create-phase需要phase_id/title/start_chapter")
            pid = self.create_phase(phase_id, title,
                                     int(start_chapter),
                                     int(params["end_chapter"]) if params.get("end_chapter") else None,
                                     params.get("description", ""))
            return {"phase_id": pid}

        elif action == "create-arc":
            arc_id = params.get("arc_id")
            title = params.get("title") or params.get("arc_title")
            start_chapter = params.get("start_chapter")
            if not arc_id or not title or start_chapter is None:
                raise ValueError("create-arc需要arc_id/title/start_chapter")
            aid = self.create_arc(arc_id, title,
                                   int(start_chapter),
                                   int(params["end_chapter"]) if params.get("end_chapter") else None,
                                   params.get("phase_id"),
                                   params.get("description", ""))
            return {"arc_id": aid}

        elif action == "complete-arc":
            arc_id = params.get("arc_id")
            end_chapter = params.get("end_chapter")
            if not arc_id or end_chapter is None:
                raise ValueError("complete-arc需要arc_id和end_chapter")
            success = self.complete_arc(arc_id, int(end_chapter))
            return {"success": success}

        elif action == "progress":
            chapter = params.get("chapter") or params.get("current_chapter")
            if chapter is None:
                chapter = self.get_latest_chapter()
            return self.get_progress(int(chapter) if chapter else 1)

        elif action == "suggest-next":
            chapter = params.get("chapter") or params.get("current_chapter")
            if chapter is None:
                chapter = self.get_latest_chapter()
            return self.suggest_next_arc(int(chapter) if chapter else 1)

        else:
            raise ValueError(f"未知操作: {action}")

    def close(self):
        """关闭连接"""
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(description='弧线管理器')
    parser.add_argument('--db-path', required=True, help='数据库路径')
    parser.add_argument('--action', required=True,
                       choices=['create-phase', 'create-arc', 'get-arc',
                               'get-active', 'get-active-phase', 'list-phases',
                               'list-arcs', 'complete-arc', 'progress',
                               'suggest-next'],
                       help='操作类型')
    parser.add_argument('--arc-id', help='弧线ID')
    parser.add_argument('--arc-title', help='弧线标题')
    parser.add_argument('--phase-id', help='阶段ID')
    parser.add_argument('--start-chapter', type=int, help='起始章节')
    parser.add_argument('--end-chapter', type=int, help='结束章节')
    parser.add_argument('--description', help='描述')
    parser.add_argument('--chapter', type=int, help='当前章节（可选，未提供时自动推断）')
    parser.add_argument('--project-path', help='项目根路径')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    manager = ArcManager(args.db_path, args.project_path)
    try:
        result = None

        if args.action == 'create-phase':
            if args.arc_id and args.arc_title and args.start_chapter is not None:
                pid = manager.create_phase(args.arc_id, args.arc_title,
                                           args.start_chapter, args.end_chapter,
                                           args.description or "")
                result = {"phase_id": pid}

        elif args.action == 'create-arc':
            if args.arc_id and args.arc_title and args.start_chapter is not None:
                aid = manager.create_arc(args.arc_id, args.arc_title,
                                         args.start_chapter, args.end_chapter,
                                         args.phase_id, args.description or "")
                result = {"arc_id": aid}

        elif args.action == 'get-arc':
            if args.arc_id:
                result = manager.get_arc(args.arc_id)

        elif args.action == 'get-active':
            chapter = args.chapter if args.chapter is not None else manager.get_latest_chapter()
            if chapter > 0:
                result = manager.get_active_arc(chapter)

        elif args.action == 'get-active-phase':
            chapter = args.chapter if args.chapter is not None else manager.get_latest_chapter()
            if chapter > 0:
                result = manager.get_active_phase(chapter)

        elif args.action == 'list-phases':
            result = {"phases": manager.list_phases()}

        elif args.action == 'list-arcs':
            result = {"arcs": manager.list_arcs(args.phase_id)}

        elif args.action == 'complete-arc':
            if args.arc_id and args.end_chapter is not None:
                success = manager.complete_arc(args.arc_id, args.end_chapter)
                result = {"success": success}

        elif args.action == 'progress':
            # --chapter 可选，未提供时自动推断
            result = manager.get_progress(args.chapter)

        elif args.action == 'suggest-next':
            # --chapter 可选，未提供时自动推断
            result = manager.suggest_next_arc(args.chapter)

        manager.close()
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


    finally:
        manager.close()
if __name__ == '__main__':
    main()
