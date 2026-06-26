"""
Bootstrap Context Generator: 生成 MEMORY_BRIEF.md 替代全量 MEMORY.md 注入。

策略：
- MEMORY.md（14KB≈3500 tokens）→ MEMORY_BRIEF.md（≤500 tokens）
- 启动时只注入精简简报，需要时通过三层检索按需获取
- MEMORY.md 保持完整不修改，随时可回退
"""

import json
import sqlite3
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Optional


def count_tokens(text: str) -> int:
    """粗略估算 token 数（中文 ~0.5 tokens/字，英文 ~1.3 tokens/词）"""
    import re
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    return int(chinese_chars * 0.5 + english_words * 1.3 + len(text) * 0.1)  # 标点/换行


def generate_brief(
    trace_db: str = None,
    pattern_db: str = None,
    workspace_root: str = None,
    max_tokens: int = 500,
) -> str:
    """
    生成启动简报。
    返回的文本直接写入 MEMORY_BRIEF.md，被注入 session 上下文。
    """
    if workspace_root is None:
        workspace_root = Path.home() / ".openclaw" / "workspace"
    else:
        workspace_root = Path(workspace_root)

    if trace_db is None:
        trace_db = Path.home() / ".openclaw" / "trace_index.db"
    else:
        trace_db = Path(trace_db)

    if pattern_db is None:
        pattern_db = Path.home() / ".openclaw" / "pattern_index.db"
    else:
        pattern_db = Path(pattern_db)

    today = date.today()

    sections = []

    # ── §1 身份核心（固定，约 50 tokens） ──
    soul = workspace_root / "SOUL.md"
    identity = ""
    if soul.exists():
        content = soul.read_text(encoding="utf-8")
        # 只取第一段核心
        for line in content.split("\n"):
            if line.startswith("- **Name:**") or line.startswith("- **What to call"):
                identity += line.strip() + "\n"
        identity = identity.strip()

    if identity:
        sections.append(f"## 身份\n{identity}")

    # ── §2 活跃模式（L2 patterns，价值最高的 5 个） ──
    if Path(pattern_db).exists():
        patterns = _get_top_patterns(pattern_db, limit=5)
        if patterns:
            lines = ["## 活跃模式"]
            for p in patterns[:5]:
                name = p["name"].replace("[", "(").replace("]", ")")
                desc = (p.get("description") or "")[:80]
                freq = p.get("frequency", 0)
                lines.append(f"- {name}：{desc}（{freq}次）")
            sections.append("\n".join(lines))

    # ── §3 近期高价值教训（L1 traces，最近 7 天 top 3） ──
    if Path(trace_db).exists():
        traces = _get_recent_high_value(trace_db, days=7, limit=3)
        if traces:
            lines = ["## 近期教训"]
            for t in traces:
                date_str = t.get("date", "")
                reflection = (t.get("reflection") or "")[:100]
                if reflection:
                    lines.append(f"- [{date_str}] {reflection}")
            if len(lines) > 1:
                sections.append("\n".join(lines))

    # ── §4 任务板 ──
    taskboard = workspace_root / "memory" / "taskboard.md"
    if taskboard.exists():
        tasks = taskboard.read_text(encoding="utf-8")
        # 只取未完成项
        pending = [l for l in tasks.split("\n") if l.strip().startswith("- [ ]")]
        if pending:
            lines = ["## 待办"] + pending[:5]
            sections.append("\n".join(lines))

    # ── §5 系统健康（最近一次反馈统计） ──
    feedback_db = Path.home() / ".openclaw" / "feedback.db"
    if feedback_db.exists():
        stats = _get_feedback_summary(feedback_db)
        if stats:
            sections.append(stats)

    # ── 组装 + token 裁剪 ──
    brief = (
        f"# MEMORY BRIEF {today.isoformat()}\n"
        f"（MemCore 自动生成，完整记忆见 MEMORY.md 或 mos search）\n\n"
        + "\n\n".join(sections)
    )

    # Token 预算控制：如果超了，逐步裁剪
    while count_tokens(brief) > max_tokens:
        # 裁剪模式描述长度
        brief = _trim_brief(brief, max_tokens)

    return brief


def _get_top_patterns(pattern_db: str, limit: int = 5) -> list[dict]:
    """获取最活跃的 patterns"""
    try:
        with sqlite3.connect(pattern_db) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM patterns WHERE confidence >= 0.7 ORDER BY frequency DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [dict(r) for r in rows]
    except Exception:
        return []


def _get_recent_high_value(trace_db: str, days: int = 7, limit: int = 3) -> list[dict]:
    """获取近期高价值 traces"""
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    try:
        with sqlite3.connect(trace_db) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """SELECT * FROM traces 
                   WHERE date >= ? AND value_score >= 0.5 AND reflection != '' 
                   ORDER BY value_score DESC LIMIT ?""",
                (cutoff, limit)
            ).fetchall()
            return [dict(r) for r in rows]
    except Exception:
        return []


def _get_feedback_summary(feedback_db: str) -> Optional[str]:
    """反馈系统简要统计"""
    try:
        with sqlite3.connect(feedback_db) as conn:
            total = conn.execute("SELECT COUNT(*) FROM feedback_events").fetchone()[0]
            refs = conn.execute("SELECT COUNT(*) FROM reference_log").fetchone()[0]
            used = conn.execute(
                "SELECT COUNT(*) FROM reference_log WHERE was_used = 1"
            ).fetchone()[0]

        if total > 0 or refs > 0:
            use_rate = used / refs if refs > 0 else 0
            return f"## 系统健康\n反馈: {total} | 引用: {refs} | 命中率: {use_rate:.0%}"
    except Exception:
        pass
    return None


def _trim_brief(brief: str, max_tokens: int) -> str:
    """Token 超限时裁剪"""
    lines = brief.split("\n")
    result = []
    for line in lines:
        result.append(line)
        if count_tokens("\n".join(result)) > max_tokens:
            result.pop()
            break

    # 确保有关闭提示
    trimmed = "\n".join(result)
    if len(trimmed) < len(brief):
        trimmed += "\n\n<!-- 已裁剪，完整内容用 mos search 检索 -->"
    return trimmed


# ── CLI 入口 ──

def main():
    brief = generate_brief()
    brief_path = Path.home() / ".openclaw" / "workspace" / "MEMORY_BRIEF.md"

    # 写入文件
    brief_path.write_text(brief, encoding="utf-8")

    token_count = count_tokens(brief)

    print(brief)
    print(f"\n{'='*50}")
    print(f"📄 已写入: {brief_path}")
    print(f"📊 Token 估算: ~{token_count} (原 MEMORY.md ~3500, 节省 {int((1 - token_count/3500) * 100)}%)")


if __name__ == "__main__":
    main()
