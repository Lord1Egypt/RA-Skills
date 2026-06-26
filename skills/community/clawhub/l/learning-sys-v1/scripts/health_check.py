#!/usr/bin/env python3
"""
学习体系升级维护脚本
定期检查知识图谱的健康度，输出需要关注的领域
"""
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

KNOWLEDGE_MAP = Path.home() / ".openclaw/workspace/notes/areas/ai-knowledge-map.md"
DEEP_DIVES = Path.home() / ".openclaw/workspace/notes/areas/deep-dives"
WEEKLY_REVIEWS = Path.home() / ".openclaw/workspace/notes/areas/weekly-reviews"
MEMORY_DIR = Path.home() / ".openclaw/workspace/memory"

def parse_knowledge_map():
    """解析知识图谱，返回各领域掌握程度统计"""
    if not KNOWLEDGE_MAP.exists():
        return None
    
    content = KNOWLEDGE_MAP.read_text()
    stats = {"🔴": 0, "🟡": 0, "🟢": 0}
    topics = []
    
    for line in content.split("\n"):
        if "|" in line and any(emoji in line for emoji in ["🔴", "🟡", "🟢"]):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                topic = parts[1]
                level = "🔴" if "🔴" in parts[2] else "🟡" if "🟡" in parts[2] else "🟢"
                stats[level] += 1
                topics.append({"topic": topic, "level": level})
    
    return {"stats": stats, "topics": topics}

def check_deep_dives():
    """检查深度笔记状态"""
    if not DEEP_DIVES.exists():
        return {"count": 0, "recent": [], "stale": []}
    
    notes = list(DEEP_DIVES.glob("*.md"))
    now = datetime.now()
    recent = []
    stale = []
    
    for note in notes:
        mtime = datetime.fromtimestamp(note.stat().st_mtime)
        age_days = (now - mtime).days
        info = {"name": note.stem, "age_days": age_days}
        if age_days <= 7:
            recent.append(info)
        elif age_days > 30:
            stale.append(info)
    
    return {"count": len(notes), "recent": recent, "stale": stale}

def check_recent_activity(days=7):
    """检查最近的 memory 日志中的学习相关活动"""
    now = datetime.now()
    activity = {"prs": 0, "research": 0, "reviews": 0}
    
    for i in range(days):
        date = now - timedelta(days=i)
        log_file = MEMORY_DIR / f"{date.strftime('%Y-%m-%d')}.md"
        if log_file.exists():
            content = log_file.read_text()
            activity["prs"] += content.lower().count("pr #") + content.lower().count("pr#")
            activity["research"] += content.count("调研") + content.count("research")
            activity["reviews"] += content.count("复盘") + content.count("review")
    
    return activity

def generate_health_report():
    """生成学习体系健康报告"""
    km = parse_knowledge_map()
    dives = check_deep_dives()
    activity = check_recent_activity()
    
    report = []
    report.append("# 学习体系健康报告")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    if km:
        total = sum(km["stats"].values())
        report.append("## 知识图谱")
        report.append(f"- 总主题数: {total}")
        report.append(f"- 🔴 入门: {km['stats']['🔴']} ({km['stats']['🔴']*100//max(total,1)}%)")
        report.append(f"- 🟡 熟悉: {km['stats']['🟡']} ({km['stats']['🟡']*100//max(total,1)}%)")
        report.append(f"- 🟢 精通: {km['stats']['🟢']} ({km['stats']['🟢']*100//max(total,1)}%)")
        
        beginner_topics = [t["topic"] for t in km["topics"] if t["level"] == "🔴"]
        if beginner_topics:
            report.append(f"\n待深入 (🔴): {', '.join(beginner_topics[:5])}")
    
    report.append(f"\n## 深度笔记")
    report.append(f"- 总数: {dives['count']}")
    report.append(f"- 本周新增: {len(dives['recent'])}")
    if dives["stale"]:
        report.append(f"- 超过30天未更新: {len(dives['stale'])}")
    
    report.append(f"\n## 本周活动")
    report.append(f"- PR 相关: {activity['prs']}")
    report.append(f"- 调研相关: {activity['research']}")
    report.append(f"- 复盘相关: {activity['reviews']}")
    
    # 建议
    report.append(f"\n## 建议")
    if km and km["stats"]["🔴"] > km["stats"]["🟡"]:
        report.append("- ⚠️ 入门级主题过多，建议本周选 1-2 个深入研究")
    if dives["count"] == 0 or len(dives["recent"]) == 0:
        report.append("- ⚠️ 本周无深度笔记，建议从最近的调研/PR 中选题")
    if activity["reviews"] == 0:
        report.append("- ⚠️ 本周无实战复盘，建议对最近的 PR 做复盘总结")
    
    return "\n".join(report)

if __name__ == "__main__":
    print(generate_health_report())
