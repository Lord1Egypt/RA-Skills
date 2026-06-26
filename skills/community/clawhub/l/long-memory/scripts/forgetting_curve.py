#!/usr/bin/env python3
"""遗忘曲线权重：基于艾宾浩斯遗忘曲线调整检索优先级"""

import argparse
import math
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"

# 艾宾浩斯遗忘曲线参数
# 记忆保持率 = e^(-t/S)，S = 稳定性指数
# 初始 S=1，每次回忆（检索命中）S 乘以 2
STABILITY_INITIAL = 1.0
STABILITY_BOOST = 2.0
MIN_RECALL_SCORE = 0.01


def calculate_recall_score(date_str: str, access_count: int = 1) -> float:
    """
    计算记忆回忆分数（0-1，越高越容易回忆）
    
    基于艾宾浩斯遗忘曲线：
    - 越新的记忆分数越高
    - 被多次检索过的记忆更稳定（遗忘更慢）
    """
    try:
        memory_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return 0.5

    days_elapsed = (datetime.now() - memory_date).days
    stability = STABILITY_INITIAL * (STABILITY_BOOST ** (access_count - 1))
    
    recall = math.exp(-days_elapsed / max(stability, 0.1))
    return max(recall, MIN_RECALL_SCORE)


def score_memories(memory_dir: Path, top_n: int = 20) -> list[dict]:
    """给所有记忆文件评分"""
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return []

    import re, json
    from pathlib import Path
    
    scores = []
    for fp in sorted(conv_dir.glob("*.md")):
        content = fp.read_text(encoding="utf-8")
        date_str = fp.stem
        
        # 估算访问次数（从摘要和蒸馏中推断）
        access_count = 1
        # 如果在 MEMORY.md 中被引用过
        memory_md = memory_dir.parent / "MEMORY.md"
        if memory_md.exists():
            mm_content = memory_md.read_text(encoding="utf-8")
            # 简单启发式：如果日期出现在 MEMORY.md 中
            if date_str in mm_content:
                access_count += 2

        recall = calculate_recall_score(date_str, access_count)
        
        # 额外加权：有决策标记的记忆更重要
        has_decisions = "**关键决策" in content or "**重要" in content
        has_todos = bool(re.findall(r'- \[ \]', content))
        
        importance = 1.0
        if has_decisions:
            importance += 0.3
        if has_todos:
            importance += 0.2

        # 话题数量
        topic_count = len(re.findall(r'###\s*话题[：:]', content))
        if topic_count > 3:
            importance += 0.1

        final_score = recall * importance

        scores.append({
            "date": date_str,
            "recall_score": round(recall, 4),
            "importance": round(importance, 2),
            "final_score": round(final_score, 4),
            "days_ago": (datetime.now() - datetime.strptime(date_str, "%Y-%m-%d")).days,
            "access_count": access_count,
            "has_decisions": has_decisions,
            "has_todos": has_todos,
        })

    return sorted(scores, key=lambda x: -x["final_score"])


def print_scores(scores: list[dict], top_n: int = 20):
    if not scores:
        print("📭 没有记忆记录")
        return

    print("=" * 70)
    print("🧠 记忆遗忘曲线分析")
    print("=" * 70)
    print(f"\n{'日期':<12} {'天数':>5} {'回忆率':>8} {'重要性':>8} {'综合分':>8} {'访问':>5} 标记")
    print("-" * 70)

    for s in scores[:top_n]:
        # 回忆率可视化
        recall_bar = "█" * int(s["recall_score"] * 20)
        markers = []
        if s["has_decisions"]:
            markers.append("🎯")
        if s["has_todos"]:
            markers.append("📋")
        marker_str = " ".join(markers) if markers else ""

        print(f"{s['date']:<12} {s['days_ago']:>4}d  "
              f"{s['recall_score']:>7.2%} {s['importance']:>7.2f} "
              f"{s['final_score']:>7.3f} {s['access_count']:>4}x  "
              f"{marker_str} {recall_bar}")

    # 分析
    fresh = [s for s in scores if s["days_ago"] <= 7]
    stale = [s for s in scores if s["days_ago"] > 30]
    print(f"\n📊 分析：")
    print(f"  7天内：{len(fresh)} 条（新鲜记忆，回忆率 >50%）")
    print(f"  30天外：{len(stale)} 条（建议定期回顾以巩固）")

    low_recall = [s for s in scores if s["recall_score"] < 0.1 and s["has_decisions"]]
    if low_recall:
        print(f"  ⚠️ {len(low_recall)} 条含决策的记忆回忆率 <10%，建议蒸馏保存")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="遗忘曲线权重")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    scores = score_memories(md, args.top)

    if args.json:
        import json
        print(json.dumps(scores, ensure_ascii=False, indent=2))
    else:
        print_scores(scores, args.top)
