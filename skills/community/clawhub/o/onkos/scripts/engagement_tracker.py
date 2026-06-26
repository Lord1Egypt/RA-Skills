#!/usr/bin/env python3
"""
追读力追踪器 - 读者视角的叙事张力评估
Agent评估+脚本计算: 智能体负责主观评分，脚本负责数据存储/聚合/趋势计算
数据存储在 novel_memory.db 的 engagement_metrics 表中
支持: 章节评分、趋势分析、节奏模式检测、叙事债务报告
"""

import os
import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class EngagementTracker:
    """追读力追踪器 - 读者视角叙事评估"""

    # 节奏类型定义
    PACE_TYPES = {"buildup", "climax", "relief", "transition"}

    # 节奏建议规则
    PACING_RULES = [
        {"consecutive": 3, "pace": "buildup", "suggest": "climax", "msg": "连续铺垫过久，建议安排高潮"},
        {"consecutive": 2, "pace": "climax", "suggest": "relief", "msg": "连续高潮后需要缓冲"},
        {"consecutive": 3, "pace": "relief", "suggest": "buildup", "msg": "连续舒缓过久，建议推进紧张感"},
        {"consecutive": 2, "pace": "transition", "suggest": "buildup", "msg": "连续过渡章节，节奏拖沓"},
    ]

    def __init__(self, db_path: str):
        """
        初始化追读力追踪器

        Args:
            db_path: SQLite 数据库路径
        """
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._ensure_tables()

    def _ensure_tables(self):
        """确保所需表存在"""
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS engagement_metrics (
                chapter INTEGER PRIMARY KEY,
                engagement_score REAL,
                hook_strength REAL,
                tension_level REAL,
                pace_type TEXT,
                reader_pull REAL,
                notes TEXT DEFAULT '',
                scored_at TEXT
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_engagement_chapter
            ON engagement_metrics(chapter)
        """)
        self.conn.commit()

    def score_chapter(self, chapter: int,
                      engagement_score: float = None,
                      hook_strength: float = None,
                      tension_level: float = None,
                      pace_type: str = None,
                      notes: str = "") -> Dict[str, Any]:
        """
        存储章节追读力评分（由智能体评估后调用）

        Args:
            chapter: 章节编号
            engagement_score: 读者投入度(0-10)
            hook_strength: 本章伏笔钩力(0-10)
            tension_level: 紧张度(0-10)
            pace_type: 节奏类型(buildup/climax/relief/transition)
            notes: 智能体备注

        Returns:
            包含reader_pull的评分结果
        """
        # 计算综合读者拉力
        reader_pull = self._compute_reader_pull(
            engagement_score, hook_strength, tension_level
        )

        now = datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO engagement_metrics
            (chapter, engagement_score, hook_strength, tension_level,
             pace_type, reader_pull, notes, scored_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (chapter, engagement_score, hook_strength, tension_level,
              pace_type, reader_pull, notes, now))
        self.conn.commit()

        return {
            "chapter": chapter,
            "engagement_score": engagement_score,
            "hook_strength": hook_strength,
            "tension_level": tension_level,
            "pace_type": pace_type,
            "reader_pull": round(reader_pull, 2),
            "notes": notes
        }

    def _compute_reader_pull(self, engagement_score: float = None,
                             hook_strength: float = None,
                             tension_level: float = None) -> float:
        """
        计算综合读者拉力

        公式: reader_pull = 0.4 * engagement + 0.35 * hook + 0.25 * tension
        缺失维度用5.0（中等）填充

        Args:
            engagement_score: 读者投入度
            hook_strength: 伏笔钩力
            tension_level: 紧张度

        Returns:
            综合读者拉力(0-10)
        """
        e = engagement_score if engagement_score is not None else 5.0
        h = hook_strength if hook_strength is not None else 5.0
        t = tension_level if tension_level is not None else 5.0

        # 边界裁剪
        e = max(0.0, min(10.0, e))
        h = max(0.0, min(10.0, h))
        t = max(0.0, min(10.0, t))

        return 0.4 * e + 0.35 * h + 0.25 * t

    def get_chapter_score(self, chapter: int) -> Optional[Dict[str, Any]]:
        """获取单章追读力评分"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM engagement_metrics WHERE chapter = ?", (chapter,))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_trend(self, from_chapter: int = None,
                  to_chapter: int = None) -> Dict[str, Any]:
        """
        获取追读力趋势

        Args:
            from_chapter: 起始章节（默认最早章节）
            to_chapter: 结束章节（默认最新章节）

        Returns:
            趋势数据（含指标、变化率、趋势方向）
        """
        cur = self.conn.cursor()
        sql = "SELECT * FROM engagement_metrics WHERE 1=1"
        params = []
        if from_chapter is not None:
            sql += " AND chapter >= ?"
            params.append(from_chapter)
        if to_chapter is not None:
            sql += " AND chapter <= ?"
            params.append(to_chapter)
        sql += " ORDER BY chapter"

        cur.execute(sql, params)
        rows = [dict(row) for row in cur.fetchall()]

        if not rows:
            return {"chapters": [], "trend": "no_data", "avg_pull": 0}

        # 计算趋势
        pulls = [r["reader_pull"] for r in rows if r.get("reader_pull") is not None]
        avg_pull = round(sum(pulls) / len(pulls), 2) if pulls else 0

        # 简单线性趋势判断（最近1/3 vs 最早1/3）
        if len(pulls) >= 3:
            third = max(1, len(pulls) // 3)
            early_avg = sum(pulls[:third]) / third
            late_avg = sum(pulls[-third:]) / third
            diff = late_avg - early_avg
            if diff > 0.5:
                trend = "rising"
            elif diff < -0.5:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        # 各指标平均值
        metrics = {}
        for field in ["engagement_score", "hook_strength", "tension_level", "reader_pull"]:
            values = [r[field] for r in rows if r.get(field) is not None]
            if values:
                metrics[field] = {
                    "avg": round(sum(values) / len(values), 2),
                    "min": round(min(values), 2),
                    "max": round(max(values), 2)
                }

        return {
            "chapters": rows,
            "chapter_count": len(rows),
            "trend": trend,
            "avg_pull": avg_pull,
            "metrics": metrics
        }

    def get_pacing_report(self, from_chapter: int = None,
                          to_chapter: int = None) -> Dict[str, Any]:
        """
        节奏模式检测

        检测连续同类型节奏并给出建议

        Args:
            from_chapter: 起始章节
            to_chapter: 结束章节

        Returns:
            节奏报告（含序列、建议、问题）
        """
        cur = self.conn.cursor()
        sql = "SELECT chapter, pace_type, reader_pull FROM engagement_metrics WHERE pace_type IS NOT NULL"
        params = []
        if from_chapter is not None:
            sql += " AND chapter >= ?"
            params.append(from_chapter)
        if to_chapter is not None:
            sql += " AND chapter <= ?"
            params.append(to_chapter)
        sql += " ORDER BY chapter"

        cur.execute(sql, params)
        rows = [dict(row) for row in cur.fetchall()]

        if not rows:
            return {"sequence": [], "suggestions": [], "issues": []}

        # 构建节奏序列
        sequence = [{"chapter": r["chapter"], "pace_type": r["pace_type"],
                     "reader_pull": r.get("reader_pull")} for r in rows]

        # 检测连续同类型
        suggestions = []
        issues = []
        consecutive_count = 1
        for i in range(1, len(sequence)):
            if sequence[i]["pace_type"] == sequence[i-1]["pace_type"]:
                consecutive_count += 1
            else:
                consecutive_count = 1

            # 检查规则
            for rule in self.PACING_RULES:
                if (consecutive_count >= rule["consecutive"] and
                        sequence[i]["pace_type"] == rule["pace"]):
                    suggestions.append({
                        "chapter": sequence[i]["chapter"],
                        "current": rule["pace"],
                        "suggest": rule["suggest"],
                        "msg": rule["msg"],
                        "consecutive_count": consecutive_count
                    })

        # 检测节奏缺失（有评分但无pace_type的章节）
        cur.execute("""
            SELECT chapter FROM engagement_metrics
            WHERE pace_type IS NULL
            AND chapter BETWEEN COALESCE(?, 0) AND COALESCE(?, 999999)
            ORDER BY chapter
        """, (from_chapter, to_chapter))
        missing_pace = [row[0] for row in cur.fetchall()]
        if missing_pace:
            issues.append({
                "type": "missing_pace",
                "chapters": missing_pace,
                "msg": f"{len(missing_pace)}个章节缺少节奏分类"
            })

        # 节奏类型分布
        pace_dist = {}
        for r in rows:
            pt = r["pace_type"]
            pace_dist[pt] = pace_dist.get(pt, 0) + 1

        return {
            "sequence": sequence,
            "suggestions": suggestions,
            "issues": issues,
            "pace_distribution": pace_dist,
            "total_scored": len(rows)
        }

    def get_debt_report(self, current_chapter: int) -> Dict[str, Any]:
        """
        叙事债务报告

        聚合: 超期伏笔 + 紧张度累积 + 遗忘风险

        Args:
            current_chapter: 当前章节

        Returns:
            叙事债务报告
        """
        debt = {
            "current_chapter": current_chapter,
            "total_debt_score": 0.0,
            "overdue_hooks": [],
            "forgotten_hooks": [],
            "tension_accumulation": [],
            "summary": {}
        }

        # 从hook_tracker获取超期伏笔（含urgency）
        try:
            from hook_tracker import HookTracker
            tracker = HookTracker(str(self.db_path))
            try:
                # 计算urgency
                tracker.compute_urgency(current_chapter)

                # 超期伏笔
                overdue = tracker.get_overdue_hooks(current_chapter)
                debt["overdue_hooks"] = overdue

                # 遗忘风险伏笔
                forgotten = tracker.get_forgotten_hooks(current_chapter, threshold=50)
                # 筛选高风险
                high_risk = [h for h in forgotten if h.get("forget_risk") == "high"]
                debt["forgotten_hooks"] = high_risk

                # 总债务分数 = 超期伏笔urgency之和 + 遗忘风险惩罚
                overdue_urgency_sum = sum(h.get("urgency", 0) for h in overdue)
                forgotten_penalty = len(high_risk) * 0.5
                debt["total_debt_score"] = round(overdue_urgency_sum + forgotten_penalty, 2)
            finally:
                tracker.close()
        except Exception:
            pass

        # 紧张度累积检测（连续高紧张度章节）
        cur = self.conn.cursor()
        cur.execute("""
            SELECT chapter, tension_level, pace_type
            FROM engagement_metrics
            WHERE chapter <= ? AND tension_level IS NOT NULL
            ORDER BY chapter DESC
            LIMIT 10
        """, (current_chapter,))
        recent = [dict(row) for row in cur.fetchall()]

        high_tension_count = 0
        for r in recent:
            if r["tension_level"] >= 7.0:
                high_tension_count += 1
            else:
                break

        if high_tension_count >= 3:
            debt["tension_accumulation"] = recent[:high_tension_count]
            debt["issues"] = debt.get("issues", [])
            debt["issues"].append({
                "type": "tension_overload",
                "msg": f"连续{high_tension_count}章高紧张度，读者疲劳风险",
                "suggest": "安排relief章节缓冲"
            })

        # 摘要
        debt["summary"] = {
            "overdue_count": len(debt["overdue_hooks"]),
            "forgotten_count": len(debt["forgotten_hooks"]),
            "total_debt_score": debt["total_debt_score"],
            "debt_level": self._classify_debt(debt["total_debt_score"])
        }

        return debt

    def _classify_debt(self, score: float) -> str:
        """债务等级分类"""
        if score <= 2.0:
            return "healthy"
        elif score <= 5.0:
            return "moderate"
        elif score <= 10.0:
            return "high"
        else:
            return "critical"

    def get_recent_metrics(self, current_chapter: int,
                           limit: int = 5) -> List[Dict[str, Any]]:
        """获取最近N章的追读力指标"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT chapter, engagement_score, hook_strength, tension_level,
                   pace_type, reader_pull
            FROM engagement_metrics
            WHERE chapter <= ?
            ORDER BY chapter DESC
            LIMIT ?
        """, (current_chapter, limit))
        return [dict(row) for row in cur.fetchall()]

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "score":
            chapter = params.get("chapter")
            if chapter is None:
                raise ValueError("score需要chapter参数")
            return self.score_chapter(
                int(chapter),
                float(params["engagement_score"]) if params.get("engagement_score") is not None else None,
                float(params["hook_strength"]) if params.get("hook_strength") is not None else None,
                float(params["tension_level"]) if params.get("tension_level") is not None else None,
                params.get("pace_type"),
                params.get("notes", "")
            )

        elif action == "trend":
            from_ch = params.get("from_chapter")
            to_ch = params.get("to_chapter")
            return self.get_trend(
                int(from_ch) if from_ch is not None else None,
                int(to_ch) if to_ch is not None else None
            )

        elif action == "pacing":
            from_ch = params.get("from_chapter")
            to_ch = params.get("to_chapter")
            return self.get_pacing_report(
                int(from_ch) if from_ch is not None else None,
                int(to_ch) if to_ch is not None else None
            )

        elif action == "debt":
            current_chapter = params.get("current_chapter")
            if current_chapter is None:
                raise ValueError("debt需要current_chapter参数")
            return self.get_debt_report(int(current_chapter))

        elif action == "get":
            chapter = params.get("chapter")
            if chapter is None:
                raise ValueError("get需要chapter参数")
            score = self.get_chapter_score(int(chapter))
            return {"score": score} if score else {"score": None}

        else:
            raise ValueError(f"未知操作: {action}")

    def close(self):
        """关闭连接"""
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(description='追读力追踪器')
    parser.add_argument('--db-path', required=True, help='数据库路径')
    parser.add_argument('--action', required=True,
                       choices=['score', 'trend', 'pacing', 'debt', 'get'],
                       help='操作类型')
    parser.add_argument('--chapter', type=int, help='章节编号')
    parser.add_argument('--engagement-score', type=float, help='读者投入度(0-10)')
    parser.add_argument('--hook-strength', type=float, help='伏笔钩力(0-10)')
    parser.add_argument('--tension-level', type=float, help='紧张度(0-10)')
    parser.add_argument('--pace-type', choices=['buildup', 'climax', 'relief', 'transition'],
                       help='节奏类型')
    parser.add_argument('--from-chapter', type=int, help='起始章节')
    parser.add_argument('--to-chapter', type=int, help='结束章节')
    parser.add_argument('--current-chapter', type=int, help='当前章节')
    parser.add_argument('--notes', help='备注')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    tracker = EngagementTracker(args.db_path)
    try:
        skip_keys = {"db_path", "action", "output"}
        params = {k: v for k, v in vars(args).items()
                  if v is not None and k not in skip_keys and not k.startswith('_')}
        result = tracker.execute_action(args.action, params)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    finally:
        tracker.close()


if __name__ == '__main__':
    main()
