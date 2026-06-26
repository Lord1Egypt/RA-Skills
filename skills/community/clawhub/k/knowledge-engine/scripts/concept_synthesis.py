#!/usr/bin/env python3
"""
Knowledge Engine - 概念蒸馏器
从底层概念往上蒸馏，形成洞察层次

三层结构：
- L1 具体事实（raw concepts）
- L2 可复用洞察（insights）  
- L3 元认知规律（meta-patterns）

两个机制：
- Reflection：从失败/被挑战的信念中提炼规则
- Generative Agents：从周期性观察中合成高级洞察
"""

import json
import os
import sys
import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from concept_manager import get_db, _make_id, add_concept, search_concepts, auto_adjust_confidence, get_all_usage_stats

INSIGHTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "memory", "insights")
DELTA_LOG = os.path.join(os.path.dirname(__file__), "..", "..", "..", "memory", "delta-log.md")


def ensure_dirs():
    os.makedirs(INSIGHTS_DIR, exist_ok=True)


def reflection(conn, days=7):
    """
    Reflection 机制：从被挑战/被推翻的信念中提炼规则
    事件驱动的纠错型记忆
    """
    since = (datetime.now() - timedelta(days=days)).isoformat()
    
    # 找到被挑战的信念
    challenged = conn.execute("""
        SELECT * FROM beliefs 
        WHERE status IN ('challenged', 'superseded')
        AND updated_at > ?
        ORDER BY updated_at DESC
    """, (since,)).fetchall()
    
    # 找到被标记为 inactive 的概念
    inactive = conn.execute("""
        SELECT * FROM concepts
        WHERE status = 'inactive' OR status = 'superseded'
        AND updated_at > ?
    """, (since,)).fetchall()
    
    rules = []
    
    for belief in challenged:
        challenges = json.loads(belief["challenges"])
        if challenges:
            rule = {
                "type": "reflection",
                "trigger": belief["belief"],
                "challenges": [c.get("note", "") for c in challenges],
                "lesson": f"当信念「{belief['belief']}」被挑战时，要注意：{'；'.join([c.get('note', '') for c in challenges[:3]])}",
                "created_at": datetime.now().isoformat()
            }
            rules.append(rule)
    
    return rules


def generative_synthesis(conn, days=7):
    """
    Generative Agents 机制：从周期性观察中合成高级洞察
    周期性的认知升华
    """
    since = (datetime.now() - timedelta(days=days)).isoformat()
    
    # 收集这段时间的所有概念
    concepts = conn.execute("""
        SELECT * FROM concepts
        WHERE created_at > ?
        ORDER BY created_at DESC
    """, (since,)).fetchall()
    
    if not concepts:
        return []
    
    # 按标签聚合
    tag_groups = {}
    for c in concepts:
        tags = json.loads(c["tags"])
        for tag in tags:
            if tag not in tag_groups:
                tag_groups[tag] = []
            tag_groups[tag].append(dict(c))
    
    # 找到出现频率最高的标签组合
    insights = []
    for tag, group in sorted(tag_groups.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
        if len(group) >= 2:
            # 这个标签下有多个概念，可能形成更高层洞察
            concept_names = [g["concept"] for g in group]
            insight = {
                "type": "generative",
                "theme": tag,
                "concepts": concept_names,
                "count": len(group),
                "suggestion": f"在「{tag}」主题下出现了 {len(group)} 个相关概念，可能需要提炼更高层的洞察",
                "created_at": datetime.now().isoformat()
            }
            insights.append(insight)
    
    # 找到被频繁关联的概念
    links = conn.execute("""
        SELECT from_concept, to_concept, relation, COUNT(*) as freq
        FROM concept_links
        WHERE created_at > ?
        GROUP BY from_concept, to_concept
        ORDER BY freq DESC
        LIMIT 5
    """, (since,)).fetchall()
    
    for link in links:
        from_row = conn.execute("SELECT concept FROM concepts WHERE id=?", (link["from_concept"],)).fetchone()
        to_row = conn.execute("SELECT concept FROM concepts WHERE id=?", (link["to_concept"],)).fetchone()
        if from_row and to_row:
            insight = {
                "type": "connection",
                "from": from_row["concept"],
                "to": to_row["concept"],
                "relation": link["relation"],
                "suggestion": f"「{from_row['concept']}」和「{to_row['concept']}」之间存在强关联，可能是一个统一洞察的两个侧面",
                "created_at": datetime.now().isoformat()
            }
            insights.append(insight)
    
    return insights


def auto_distill_levels(conn, days=14):
    """
    L1→L2→L3 自动蒸馏
    
    L1 → L2: 当同一主题下有 >=3 个 L1 概念，自动生成 L2 洞察
    L2 → L3: 当有 >=2 个 L2 洞察指向同一元规律，自动生成 L3 元规律
    
    所有层级都是概念卡片，通过 level 标签区分
    """
    since = (datetime.now() - timedelta(days=days)).isoformat()
    now = datetime.now().isoformat()
    
    results = {"l1_to_l2": [], "l2_to_l3": []}
    
    # ─── L1 → L2 ───
    # 找所有 L1 概念（没有 level 标签或 level=l1 的概念）
    all_concepts = conn.execute("""
        SELECT * FROM concepts WHERE status='active' ORDER BY created_at DESC
    """).fetchall()
    
    l1_concepts = []
    for c in all_concepts:
        tags = json.loads(c["tags"]) if isinstance(c["tags"], str) else c["tags"]
        if "level:l2" not in tags and "level:l3" not in tags:
            l1_concepts.append(dict(c))
    
    # 按标签聚合 L1 概念
    tag_groups = {}
    for c in l1_concepts:
        tags = [t for t in (json.loads(c["tags"]) if isinstance(c["tags"], str) else c["tags"]) 
                if not t.startswith("level:")]
        for tag in tags:
            if tag not in tag_groups:
                tag_groups[tag] = []
            tag_groups[tag].append(c)
    
    for tag, group in tag_groups.items():
        if len(group) >= 3:
            # 检查是否已存在对应的 L2（用 level:l2 + 主题标签 匹配）
            existing_l2 = conn.execute("""
                SELECT * FROM concepts 
                WHERE status='active' AND tags LIKE '%level:l2%'
                AND tags LIKE ?
            """, (f"%{tag}%",)).fetchone()
            
            if not existing_l2:
                # 提炼共性而非简单拼接名字
                concept_names = [g["concept"] for g in group]
                # 从上下文中提取关键词
                contexts = [g.get("context", "") for g in group if g.get("context")]
                
                # 生成简洁的 L2 名字（不包含 L1 的完整名字）
                l2_name = f"[L2] {tag}领域：从{len(group)}个事实提炼的深层模式"
                
                l2_context = f"从以下 L1 概念蒸馏而来（{now[:10]}）：\n" + "\n".join(
                    f"- {g['concept']}" for g in group[:5]
                )
                
                add_concept(
                    l2_name,
                    source="auto-distill:L1→L2",
                    context=l2_context,
                    tags=[tag, "level:l2", "洞察"],
                    confidence="medium",
                    force=True  # L2 洞察不走循环检测，避免被 L1 合并
                )
                results["l1_to_l2"].append(l2_name)
    
    # ─── L2 → L3 ───
    # 找所有 L2 洞察（重新查询，可能刚生成了新的）
    all_concepts_updated = conn.execute("""
        SELECT * FROM concepts WHERE status='active' ORDER BY created_at DESC
    """).fetchall()
    
    l2_concepts = []
    for c in all_concepts_updated:
        tags = json.loads(c["tags"]) if isinstance(c["tags"], str) else c["tags"]
        if "level:l2" in tags:
            l2_concepts.append({"id": c["id"], "concept": c["concept"], "tags": tags})
    
    # 按共享标签找 L2 之间的共性
    if len(l2_concepts) >= 2:
        l2_tag_overlap = {}
        for c in l2_concepts:
            tags_raw = c["tags"]
            if isinstance(tags_raw, str):
                tags_raw = json.loads(tags_raw)
            tags = set(t for t in tags_raw if t not in ("level:l2", "洞察"))
            for tag in tags:
                if len(tag) < 2:
                    continue  # 跳过单字符标签（数据污染）
                if tag not in l2_tag_overlap:
                    l2_tag_overlap[tag] = []
                l2_tag_overlap[tag].append(c)
        
        for tag, group in l2_tag_overlap.items():
            if len(group) >= 2:
                # 检查是否已存在对应的 L3
                existing_l3 = conn.execute("""
                    SELECT * FROM concepts 
                    WHERE status='active' AND tags LIKE '%level:l3%'
                    AND tags LIKE ?
                """, (f"%{tag}%",)).fetchone()
                
                if not existing_l3:
                    l3_name = f"[L3] 元规律：{tag}领域的跨维度底层逻辑"
                    l3_context = f"从以下 L2 洞察进一步提炼（{now[:10]}）：\n" + "\n".join(
                        f"- {g['concept']}" for g in group
                    )
                    
                    add_concept(
                        l3_name,
                        source="auto-distill:L2→L3",
                        context=l3_context,
                        tags=[tag, "level:l3", "元规律"],
                        confidence="low",  # L3 初始置信度低，需要人工验证
                        force=True
                    )
                    results["l2_to_l3"].append(l3_name)
    
    return results


def distill(conn, days=7):
    """
    主入口：执行完整的蒸馏流程
    """
    ensure_dirs()
    now = datetime.now()
    
    print(f"🧠 Knowledge Engine 蒸馏 [{now.strftime('%Y-%m-%d')}]\n")
    
    # Step 1: Reflection
    print("📝 Step 1: Reflection — 从失败中学习")
    rules = reflection(conn, days)
    if rules:
        for r in rules:
            print(f"   ⚠️  {r['lesson']}")
    else:
        print("   (没有被挑战的信念)")
    
    # Step 2: Generative Synthesis
    print("\n🔬 Step 2: Generative Synthesis — 从观察中提炼")
    insights = generative_synthesis(conn, days)
    for ins in insights:
        if ins["type"] == "generative":
            print(f"   📊 主题「{ins['theme']}」下有 {ins['count']} 个概念: {', '.join(ins['concepts'][:3])}...")
        elif ins["type"] == "connection":
            print(f"   🔗 强关联: {ins['from']} ↔ {ins['to']}")
    
    # Step 2.5: Auto-distill L1→L2→L3
    print("\n🏗️  Step 2.5: Auto-distill — L1→L2→L3 自动蒸馏")
    distill_results = auto_distill_levels(conn, days=days*2)  # 回顾更长时间
    if distill_results["l1_to_l2"]:
        print(f"   L1→L2 生成 {len(distill_results['l1_to_l2'])} 个洞察:")
        for name in distill_results["l1_to_l2"]:
            print(f"     📊 {name[:60]}")
    else:
        print("   L1→L2: 暂无足够聚合的 L1 概念")
    
    if distill_results["l2_to_l3"]:
        print(f"   L2→L3 生成 {len(distill_results['l2_to_l3'])} 个元规律:")
        for name in distill_results["l2_to_l3"]:
            print(f"     🏛️  {name[:60]}")
    else:
        print("   L2→L3: 暂无足够聚合的 L2 洞察")
    
    # Step 3: Auto-adjust confidence
    print("\n⚡ Step 3: Auto-adjust — 基于使用频率调整置信度")
    adjustments = auto_adjust_confidence(conn, dry_run=False)
    if adjustments['upgrades']:
        for cid, name, old, new in adjustments['upgrades']:
            print(f"   ⬆️  {name}: {old} → {new}")
    if adjustments['downgrades']:
        for cid, name, old, new in adjustments['downgrades']:
            print(f"   ⬇️  {name}: {old} → {new}")
    if adjustments['deprecations']:
        for cid, name in adjustments['deprecations']:
            print(f"   🗑️  {name} → deprecated")
    if not adjustments['upgrades'] and not adjustments['downgrades'] and not adjustments['deprecations']:
        print("   (无需调整)")
    
    # Step 3.5: Belief decay
    print("\n💭 Step 3.5: Belief Decay — 信念时间衰减")
    from concept_manager import get_beliefs_with_decay
    beliefs = get_beliefs_with_decay()
    decayed = [b for b in beliefs if b["decay_note"]]
    if decayed:
        for b in decayed[:5]:
            print(f"   📉 [{b['effective_confidence']}] {b['belief'][:40]} — {b['decay_note']}")
    else:
        print("   (无衰减信念)")
    
    # Step 4: Usage heatmap
    print("\n📊 Step 4: 使用热力图 (近7天)")
    all_stats = get_all_usage_stats(days=7)
    if all_stats:
        for cid, s in sorted(all_stats.items(), key=lambda x: x[1]['total'], reverse=True)[:10]:
            concept = conn.execute("SELECT concept FROM concepts WHERE id=?", (cid,)).fetchone()
            name = concept['concept'] if concept else cid
            bar = '█' * min(s['total'], 20)
            print(f"   {name}: {bar} ({s['total']})")
    else:
        print("   (本周无使用记录)")
    
    # Step 5: 生成蒸馏报告
    print("\n📄 Step 5: 生成报告")
    report = generate_report(rules, insights, now, distill_results, decayed)
    
    # 保存
    report_file = os.path.join(INSIGHTS_DIR, f"{now.strftime('%Y-%m-%d')}-distillation.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    with open(DELTA_LOG, "a", encoding="utf-8") as f:
        f.write(report + "\n---\n")
    
    print(f"\n📄 蒸馏报告已保存: {report_file}")
    
    # 追加到每日记录
    conn.execute("""
        INSERT INTO daily_entries (date, entry_type, title, content, concepts_added, beliefs_updated, delta, created_at)
        VALUES (?, 'distillation', ?, ?, '[]', '[]', ?, ?)
    """, (now.strftime("%Y-%m-%d"), f"{now.strftime('%Y-%m-%d')} 蒸馏报告", 
          json.dumps({"rules": rules, "insights": insights, "distill": distill_results}, ensure_ascii=False),
          report, now.isoformat()))
    conn.commit()
    conn.close()
    
    return report


def generate_report(rules, insights, now, distill_results=None, decayed_beliefs=None):
    lines = [f"# {now.strftime('%Y-%m-%d')} 蒸馏报告\n"]
    
    if rules:
        lines.append("## 💡 从失败中提炼的规则")
        for r in rules:
            lines.append(f"- {r['lesson']}")
        lines.append("")
    
    themes = [i for i in insights if i["type"] == "generative"]
    connections = [i for i in insights if i["type"] == "connection"]
    
    if themes:
        lines.append("## 📊 主题聚合")
        for t in themes:
            lines.append(f"- **{t['theme']}** ({t['count']} 个概念): {', '.join(t['concepts'][:5])}")
        lines.append("")
    
    if connections:
        lines.append("## 🔗 值得深挖的关联")
        for c in connections:
            lines.append(f"- {c['from']} ↔ {c['to']} ({c['relation']})")
        lines.append("")
    
    if distill_results:
        if distill_results.get("l1_to_l2"):
            lines.append("## 🏗️ L1→L2 自动蒸馏")
            for name in distill_results["l1_to_l2"]:
                lines.append(f"- {name}")
            lines.append("")
        
        if distill_results.get("l2_to_l3"):
            lines.append("## 🏛️ L2→L3 元规律")
            for name in distill_results["l2_to_l3"]:
                lines.append(f"- {name}")
            lines.append("")
    
    if decayed_beliefs:
        lines.append("## 💭 信念衰减")
        for b in decayed_beliefs[:5]:
            lines.append(f"- [{b['effective_confidence']}] {b['belief']} — {b['decay_note']}")
        lines.append("")
    
    if not rules and not themes and not connections and not distill_results:
        lines.append("本期没有需要蒸馏的内容。\n")
    
    lines.append("## 下一步")
    lines.append("- 审视上方的主题聚合，看能否提炼出更高层的洞察")
    lines.append("- 对强关联的概念对，考虑是否要创建一个新的统一概念")
    lines.append("- 被挑战的信念是否需要更新为新的信念")
    lines.append("- 检查 L3 元规律是否准确，低置信度需要人工验证")
    lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Knowledge Engine - 概念蒸馏")
    parser.add_argument("--days", type=int, default=7, help="回顾多少天")
    
    args = parser.parse_args()
    conn = get_db()
    distill(conn, args.days)


if __name__ == "__main__":
    main()
