#!/usr/bin/env python3
"""
Knowledge Engine - 概念管理器
用纯标准库（sqlite3 + json）构建个人知识系统
"""

import sqlite3
import json
import os
import sys
import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path

# 数据库路径
DB_PATH = os.environ.get(
    "KNOWLEDGE_DB",
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "memory", "knowledge.db")
)

CONCEPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "memory", "concepts")
BELIEFS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "memory", "beliefs")


def ensure_dirs():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(CONCEPTS_DIR, exist_ok=True)
    os.makedirs(BELIEFS_DIR, exist_ok=True)


def get_db():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    _init_schema(conn)
    return conn


def _init_schema(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS concepts (
            id TEXT PRIMARY KEY,
            concept TEXT NOT NULL,
            source TEXT,
            context TEXT,
            tags TEXT DEFAULT '[]',
            confidence TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'active',
            related TEXT DEFAULT '[]',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS concept_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_concept TEXT NOT NULL,
            to_concept TEXT NOT NULL,
            relation TEXT DEFAULT 'related',
            created_at TEXT NOT NULL,
            UNIQUE(from_concept, to_concept, relation)
        );

        CREATE TABLE IF NOT EXISTS beliefs (
            id TEXT PRIMARY KEY,
            belief TEXT NOT NULL,
            reasoning TEXT,
            confidence TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'active',
            challenges TEXT DEFAULT '[]',
            updates TEXT DEFAULT '[]',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS daily_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            entry_type TEXT DEFAULT 'reading',
            title TEXT,
            content TEXT,
            concepts_added TEXT DEFAULT '[]',
            beliefs_updated TEXT DEFAULT '[]',
            delta TEXT,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_concepts_status ON concepts(status);
        CREATE INDEX IF NOT EXISTS idx_concepts_tags ON concepts(tags);
        CREATE INDEX IF NOT EXISTS idx_beliefs_status ON beliefs(status);
        CREATE INDEX IF NOT EXISTS idx_daily_date ON daily_entries(date);

        -- 使用追踪：每次搜索命中、每次关联引用都记录
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_id TEXT NOT NULL,
            action TEXT NOT NULL,  -- 'search_hit', 'link_ref', 'graph_view', 'mentioned'
            query TEXT,            -- 搜索时的 query
            context TEXT,          -- 触发上下文
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_usage_concept ON usage_log(concept_id);
        CREATE INDEX IF NOT EXISTS idx_usage_action ON usage_log(action);
        CREATE INDEX IF NOT EXISTS idx_usage_created ON usage_log(created_at);
    """)
    conn.commit()


# ─── 使用追踪 ───

def log_usage(concept_id, action, query="", context=""):
    """记录概念使用"""
    conn = get_db()
    conn.execute(
        "INSERT INTO usage_log (concept_id, action, query, context, created_at) VALUES (?, ?, ?, ?, ?)",
        (concept_id, action, query, context, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_concept_stats(concept_id, days=30):
    """获取概念使用统计"""
    conn = get_db()
    since = (datetime.now() - timedelta(days=days)).isoformat()
    
    stats = {}
    for action in ['search_hit', 'link_ref', 'graph_view', 'mentioned']:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM usage_log WHERE concept_id=? AND action=? AND created_at>?",
            (concept_id, action, since)
        ).fetchone()
        stats[action] = row['cnt']
    
    stats['total'] = sum(stats.values())
    
    # 最近一次使用
    last = conn.execute(
        "SELECT created_at FROM usage_log WHERE concept_id=? ORDER BY created_at DESC LIMIT 1",
        (concept_id,)
    ).fetchone()
    stats['last_used'] = last['created_at'] if last else None
    
    # 概念创建时间
    concept = conn.execute("SELECT created_at FROM concepts WHERE id=?", (concept_id,)).fetchone()
    stats['created_at'] = concept['created_at'] if concept else None
    
    # 存在天数
    if stats['created_at']:
        created = datetime.fromisoformat(stats['created_at'])
        stats['age_days'] = (datetime.now() - created).days
    else:
        stats['age_days'] = 0
    
    conn.close()
    return stats


def get_all_usage_stats(days=30):
    """获取所有概念的使用统计"""
    conn = get_db()
    since = (datetime.now() - timedelta(days=days)).isoformat()
    
    # 按概念聚合
    rows = conn.execute("""
        SELECT concept_id, action, COUNT(*) as cnt
        FROM usage_log
        WHERE created_at > ?
        GROUP BY concept_id, action
    """, (since,)).fetchall()
    
    stats = {}
    for row in rows:
        cid = row['concept_id']
        if cid not in stats:
            stats[cid] = {'search_hit': 0, 'link_ref': 0, 'graph_view': 0, 'mentioned': 0, 'total': 0}
        stats[cid][row['action']] = row['cnt']
        stats[cid]['total'] += row['cnt']
    
    conn.close()
    return stats


def auto_adjust_confidence(conn, dry_run=False):
    """
    基于使用频率自动调整置信度
    规则：
    - 30天内被搜索命中 >= 5 次 → 升级
    - 30天内总使用 >= 10 次 → 升级
    - 30天内零使用且存在 > 14 天 → 降级
    - 60天内零使用且存在 > 30 天 → 标记 deprecated
    """
    now = datetime.now()
    d30 = (now - timedelta(days=30)).isoformat()
    d60 = (now - timedelta(days=60)).isoformat()
    d14 = (now - timedelta(days=14)).isoformat()
    
    concepts = conn.execute("SELECT * FROM concepts WHERE status='active'").fetchall()
    
    upgrades = []
    downgrades = []
    deprecations = []
    
    for c in concepts:
        cid = c['id']
        created = datetime.fromisoformat(c['created_at'])
        age_days = (now - created).days
        
        # 统计使用
        search_hits = conn.execute(
            "SELECT COUNT(*) as cnt FROM usage_log WHERE concept_id=? AND action='search_hit' AND created_at>?",
            (cid, d30)
        ).fetchone()['cnt']
        
        total_uses_30d = conn.execute(
            "SELECT COUNT(*) as cnt FROM usage_log WHERE concept_id=? AND created_at>?",
            (cid, d30)
        ).fetchone()['cnt']
        
        total_uses_60d = conn.execute(
            "SELECT COUNT(*) as cnt FROM usage_log WHERE concept_id=? AND created_at>?",
            (cid, d60)
        ).fetchone()['cnt']
        
        # 升级规则
        if search_hits >= 5 or total_uses_30d >= 10:
            current = c['confidence']
            if current == 'low':
                new_conf = 'medium'
            elif current == 'medium':
                new_conf = 'high'
            else:
                new_conf = None
            
            if new_conf:
                upgrades.append((cid, c['concept'], current, new_conf))
                if not dry_run:
                    conn.execute(
                        "UPDATE concepts SET confidence=?, updated_at=? WHERE id=?",
                        (new_conf, now.isoformat(), cid)
                    )
        
        # 降级规则：30天零使用 + 存在超过14天
        elif total_uses_30d == 0 and age_days > 14:
            current = c['confidence']
            if current == 'high':
                new_conf = 'medium'
            elif current == 'medium':
                new_conf = 'low'
            else:
                new_conf = None
            
            if new_conf:
                downgrades.append((cid, c['concept'], current, new_conf))
                if not dry_run:
                    conn.execute(
                        "UPDATE concepts SET confidence=?, updated_at=? WHERE id=?",
                        (new_conf, now.isoformat(), cid)
                    )
        
        # 废弃规则：60天零使用 + 存在超过30天
        if total_uses_60d == 0 and age_days > 30:
            deprecations.append((cid, c['concept']))
            if not dry_run:
                conn.execute(
                    "UPDATE concepts SET status='deprecated', updated_at=? WHERE id=?",
                    (now.isoformat(), cid)
                )
    
    if not dry_run:
        conn.commit()
    
    return {'upgrades': upgrades, 'downgrades': downgrades, 'deprecations': deprecations}


# ─── 概念管理 ───

def find_similar_concepts(concept, tags=None, threshold=0.4):
    """
    循环检测：查找与新概念相似的已有概念
    返回 [(concept_id, concept_name, similarity_score), ...]
    
    相似度计算：基于关键词重叠 + 语义分组
    """
    conn = get_db()
    new_words = set(_tokenize(concept))
    new_tags = set(t.lower() for t in (tags or []))
    
    active = conn.execute("SELECT * FROM concepts WHERE status='active'").fetchall()
    
    similar = []
    for row in active:
        existing_words = set(_tokenize(row["concept"]))
        existing_tags = set(t.lower() for t in json.loads(row["tags"]))
        
        # Jaccard 相似度（关键词）
        if new_words and existing_words:
            keyword_sim = len(new_words & existing_words) / len(new_words | existing_words)
        else:
            keyword_sim = 0
        
        # 标签重叠
        if new_tags and existing_tags:
            tag_sim = len(new_tags & existing_tags) / len(new_tags | existing_tags)
        else:
            tag_sim = 0
        
        # 综合分数（关键词权重更高）
        score = keyword_sim * 0.7 + tag_sim * 0.3
        
        # 额外检查：一个概念是否包含另一个（中文子串匹配）
        if concept in row["concept"] or row["concept"] in concept:
            score = max(score, 0.6)
        
        if score >= threshold:
            similar.append((row["id"], row["concept"], round(score, 2)))
    
    conn.close()
    similar.sort(key=lambda x: x[2], reverse=True)
    return similar[:5]


def add_concept(concept, source="", context="", tags=None, confidence="medium", related=None, force=False):
    conn = get_db()
    now = datetime.now().isoformat()
    concept_id = _make_id(concept)

    tags_json = json.dumps(tags or [], ensure_ascii=False)
    related_json = json.dumps(related or [], ensure_ascii=False)

    # 循环检测：检查相似概念（除非 force=True）
    if not force:
        similar = find_similar_concepts(concept, tags)
        if similar:
            best_match = similar[0]
            if best_match[2] >= 0.6:
                # 高相似度：自动合并到已有概念
                print(f"🔄 检测到重复概念 (相似度 {best_match[2]}): 「{concept}」≈ 「{best_match[1]}」")
                print(f"   自动合并到已有概念，更新上下文和标签")
                # 合并逻辑：更新已有概念
                existing_row = conn.execute("SELECT * FROM concepts WHERE id=?", (best_match[0],)).fetchone()
                existing_tags = set(json.loads(existing_row["tags"]))
                new_tags_set = set(tags or [])
                merged_tags = list(existing_tags | new_tags_set)
                
                merge_context = ""
                if context:
                    merge_context = f"\n[{now[:10]}] {context}"
                
                conn.execute("""
                    UPDATE concepts SET
                        context = context || ?,
                        tags = ?,
                        confidence = CASE 
                            WHEN ? = 'high' OR confidence = 'high' THEN 'high'
                            WHEN ? = 'medium' OR confidence = 'medium' THEN 'medium'
                            ELSE 'low'
                        END,
                        updated_at = ?
                    WHERE id = ?
                """, (merge_context, json.dumps(merged_tags, ensure_ascii=False), 
                      confidence, confidence, now, best_match[0]))
                
                # 更新 JSON 文件
                card = dict(existing_row)
                card["tags"] = merged_tags
                card["context"] = (existing_row["context"] or "") + merge_context
                card["updated_at"] = now
                card_path = os.path.join(CONCEPTS_DIR, f"{best_match[0]}.json")
                with open(card_path, "w", encoding="utf-8") as f:
                    json.dump(card, f, ensure_ascii=False, indent=2)
                
                conn.commit()
                conn.close()
                return best_match[0]
            elif best_match[2] >= 0.4:
                # 中等相似度：警告但不阻止
                print(f"⚠️  注意：「{concept}」与 「{best_match[1]}」 有相似性 (分数 {best_match[2]})")
                print(f"   如确认是新概念，使用 force=True 跳过检查")

    # Check if exact same ID exists
    existing = conn.execute("SELECT id FROM concepts WHERE id=?", (concept_id,)).fetchone()
    if existing:
        conn.execute("""
            UPDATE concepts SET
                context = context || ?,
                tags = ?,
                confidence = ?,
                updated_at = ?
            WHERE id = ?
        """, (f"\n[{now[:10]}] {context}" if context else "", tags_json, confidence, now, concept_id))
        print(f"📝 更新概念: {concept}")
    else:
        conn.execute("""
            INSERT INTO concepts (id, concept, source, context, tags, confidence, status, related, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?, ?)
        """, (concept_id, concept, source, context, tags_json, confidence, related_json, now, now))
        print(f"✨ 新概念: {concept}")

    # Also save as JSON file
    card = {
        "id": concept_id,
        "concept": concept,
        "source": source,
        "context": context,
        "tags": tags or [],
        "confidence": confidence,
        "status": "active",
        "related": related or [],
        "created_at": now,
        "updated_at": now
    }
    card_path = os.path.join(CONCEPTS_DIR, f"{concept_id}.json")
    with open(card_path, "w", encoding="utf-8") as f:
        json.dump(card, f, ensure_ascii=False, indent=2)

    conn.commit()
    conn.close()
    return concept_id


def search_concepts(query="", tags=None, status="active", limit=20):
    conn = get_db()

    if tags:
        results = []
        all_concepts = conn.execute(
            "SELECT * FROM concepts WHERE status=? ORDER BY updated_at DESC",
            (status,)
        ).fetchall()
        for row in all_concepts:
            row_tags = json.loads(row["tags"])
            if any(t in row_tags for t in tags):
                if not query or _text_match(query, row["concept"] + " " + (row["context"] or "")):
                    results.append(dict(row))
        conn.close()
        return results[:limit]

    if query:
        # Simple BM25-like scoring with SQLite
        words = _tokenize(query)
        if not words:
            results = conn.execute(
                "SELECT * FROM concepts WHERE status=? ORDER BY updated_at DESC LIMIT ?",
                (status, limit)
            ).fetchall()
            conn.close()
            return [dict(r) for r in results]

        # Build a simple relevance score
        all_concepts = conn.execute(
            "SELECT * FROM concepts WHERE status=?", (status,)
        ).fetchall()

        scored = []
        for row in all_concepts:
            text = f"{row['concept']} {row['context'] or ''} {row['source'] or ''}".lower()
            tags_text = " ".join(json.loads(row["tags"])).lower()
            full_text = text + " " + tags_text

            score = 0
            for word in words:
                if word in full_text:
                    score += 1
                if word in row["concept"].lower():
                    score += 3  # Title match is worth more
            if score > 0:
                scored.append((score, dict(row)))

        scored.sort(key=lambda x: x[0], reverse=True)
        conn.close()
        return [item[1] for item in scored[:limit]]

    results = conn.execute(
        "SELECT * FROM concepts WHERE status=? ORDER BY updated_at DESC LIMIT ?",
        (status, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in results]


def link_concepts(from_concept, to_concept, relation="related"):
    conn = get_db()
    now = datetime.now().isoformat()

    # Find concept IDs by name
    from_id = _find_concept_id(conn, from_concept)
    to_id = _find_concept_id(conn, to_concept)

    if not from_id:
        print(f"❌ 找不到概念: {from_concept}")
        conn.close()
        return False
    if not to_id:
        print(f"❌ 找不到概念: {to_concept}")
        conn.close()
        return False

    try:
        conn.execute(
            "INSERT INTO concept_links (from_concept, to_concept, relation, created_at) VALUES (?, ?, ?, ?)",
            (from_id, to_id, relation, now)
        )
        print(f"🔗 关联: {from_concept} --[{relation}]--> {to_concept}")
    except sqlite3.IntegrityError:
        print(f"ℹ️  关联已存在: {from_concept} --[{relation}]--> {to_concept}")

    conn.commit()
    conn.close()
    return True


# ─── 信念管理 ───

def add_belief(belief, reasoning="", confidence="medium"):
    conn = get_db()
    now = datetime.now().isoformat()
    belief_id = f"belief-{now[:10].replace('-', '')}-{len(conn.execute('SELECT id FROM beliefs').fetchall()) + 1:03d}"

    conn.execute("""
        INSERT INTO beliefs (id, belief, reasoning, confidence, status, challenges, updates, created_at, updated_at)
        VALUES (?, ?, ?, ?, 'active', '[]', '[]', ?, ?)
    """, (belief_id, belief, reasoning, confidence, now, now))

    card = {
        "id": belief_id,
        "belief": belief,
        "reasoning": reasoning,
        "confidence": confidence,
        "status": "active",
        "challenges": [],
        "updates": [],
        "created_at": now,
        "updated_at": now
    }
    card_path = os.path.join(BELIEFS_DIR, f"{belief_id}.json")
    with open(card_path, "w", encoding="utf-8") as f:
        json.dump(card, f, ensure_ascii=False, indent=2)

    conn.commit()
    conn.close()
    print(f"💭 新信念 [{belief_id}]: {belief}")
    return belief_id


def update_belief(belief_id, status=None, note="", confidence=None):
    conn = get_db()
    now = datetime.now().isoformat()

    row = conn.execute("SELECT * FROM beliefs WHERE id=?", (belief_id,)).fetchone()
    if not row:
        print(f"❌ 找不到信念: {belief_id}")
        conn.close()
        return False

    updates = json.loads(row["updates"])
    challenges = json.loads(row["challenges"])

    if note:
        if status == "challenged" or status == "superseded":
            challenges.append({"note": note, "date": now})
        else:
            updates.append({"note": note, "date": now})

    conn.execute("""
        UPDATE beliefs SET
            status = COALESCE(?, status),
            confidence = COALESCE(?, confidence),
            challenges = ?,
            updates = ?,
            updated_at = ?
        WHERE id = ?
    """, (status, confidence, json.dumps(challenges, ensure_ascii=False),
          json.dumps(updates, ensure_ascii=False), now, belief_id))

    conn.commit()
    conn.close()
    print(f"🔄 更新信念 [{belief_id}]: status={status or 'unchanged'}")
    return True


def get_beliefs_with_decay(days_threshold=30):
    """
    信念时间衰减：返回带有效置信度的信念列表
    
    衰减规则：
    - 最近 7 天内：置信度不变
    - 7-30 天：每 7 天降一级（high→medium→low）
    - 30 天以上 + 零更新：标记为 stale
    - 被挑战的信念：额外降一级
    - 有近期更新的信念：置信度不变或提升
    """
    conn = get_db()
    now = datetime.now()
    beliefs = conn.execute("SELECT * FROM beliefs WHERE status='active' ORDER BY updated_at DESC").fetchall()
    
    result = []
    for b in beliefs:
        updated = datetime.fromisoformat(b["updated_at"])
        age_days = (now - updated).days
        
        original_conf = b["confidence"]
        effective_conf = original_conf
        decay_note = ""
        
        # 被挑战过 → 额外降一级
        challenges = json.loads(b["challenges"])
        if challenges:
            if original_conf == "high":
                effective_conf = "medium"
            elif original_conf == "medium":
                effective_conf = "low"
            decay_note = "曾被挑战"
        
        # 时间衰减
        if age_days > 30:
            effective_conf = "low"
            decay_note += f" 超过{age_days}天未更新"
        elif age_days > 14:
            if effective_conf == "high":
                effective_conf = "medium"
            decay_note += f" {age_days}天未更新，自动降级"
        elif age_days > 7:
            decay_note += f" {age_days}天未更新"
        
        # 有近期更新 → 提升
        updates = json.loads(b["updates"])
        if updates:
            last_update = updates[-1]
            last_update_date = datetime.fromisoformat(last_update["date"])
            if (now - last_update_date).days < 7:
                if original_conf == "medium" and effective_conf != "high":
                    effective_conf = "medium"  # 保持不降
                    decay_note = "近期有更新，保持置信度"
        
        result.append({
            "id": b["id"],
            "belief": b["belief"],
            "reasoning": b["reasoning"],
            "original_confidence": original_conf,
            "effective_confidence": effective_conf,
            "status": b["status"],
            "age_days": age_days,
            "decay_note": decay_note.strip(),
            "challenges_count": len(challenges),
            "updates_count": len(updates),
            "created_at": b["created_at"],
            "updated_at": b["updated_at"]
        })
    
    conn.close()
    # 按有效置信度排序：high > medium > low
    conf_order = {"high": 0, "medium": 1, "low": 2}
    result.sort(key=lambda x: (conf_order.get(x["effective_confidence"], 3), x["age_days"]))
    return result


# ─── 分层检索（Hierarchical Retrieval）───

def hierarchical_search(conn, query="", recent_k=5, semantic_k=5, summary_k=2, days=7):
    """
    三层分层检索：Recent + Semantic + Summary
    - Recent: 最近 N 条，保持对话连贯
    - Semantic: 语义相关（当前用关键词，升级后用向量）
    - Summary: 最近的蒸馏/洞察摘要
    """
    results = {"recent": [], "semantic": [], "summary": []}
    
    # 1. Recent: 最近 N 条活跃概念
    recent = conn.execute("""
        SELECT * FROM concepts 
        WHERE status='active'
        ORDER BY updated_at DESC
        LIMIT ?
    """, (recent_k,)).fetchall()
    results["recent"] = [dict(r) for r in recent]
    
    # 2. Semantic: 关键词匹配（未来升级为向量搜索）
    if query:
        semantic = search_concepts(query, limit=semantic_k)
        # 去重：排除已经在 recent 中的
        recent_ids = {r["id"] for r in results["recent"]}
        results["semantic"] = [s for s in semantic if s["id"] not in recent_ids]
    
    # 3. Summary: 最近的蒸馏报告
    since = (datetime.now() - timedelta(days=days)).isoformat()
    summaries = conn.execute("""
        SELECT * FROM daily_entries
        WHERE entry_type IN ('synthesis', 'distillation')
        AND created_at > ?
        ORDER BY date DESC
        LIMIT ?
    """, (since, summary_k)).fetchall()
    results["summary"] = [dict(s) for s in summaries]
    
    return results


def show_hierarchical(conn, query="", recent_k=5, semantic_k=5, summary_k=2):
    """展示分层检索结果"""
    results = hierarchical_search(conn, query, recent_k, semantic_k, summary_k)
    
    print(f"\n{'='*50}")
    print(f"🧠 分层检索" + (f' [{query}]' if query else ''))
    print(f"{'='*50}")
    
    if results["recent"]:
        print(f"\n📌 Recent (最近 {len(results['recent'])} 条):")
        for r in results["recent"]:
            tags = ", ".join(json.loads(r["tags"])) if r.get("tags") else ""
            print(f"   • {r['concept']} ({r['confidence']})" + (f" [{tags}]" if tags else ""))
    
    if results["semantic"]:
        print(f"\n🔍 Semantic (语义相关 {len(results['semantic'])} 条):")
        for r in results["semantic"]:
            tags = ", ".join(json.loads(r["tags"])) if r.get("tags") else ""
            print(f"   • {r['concept']} ({r['confidence']})" + (f" [{tags}]" if tags else ""))
    
    if results["summary"]:
        print(f"\n📋 Summary (最近 {len(results['summary'])} 条摘要):")
        for s in results["summary"]:
            print(f"   [{s['date']}] {s['title'] or '(无标题)'}")
    
    if not results["recent"] and not results["semantic"] and not results["summary"]:
        print("\n  (无结果)")
    
    return results


# ─── 图谱 ───

def show_graph(concept_name=None):
    conn = get_db()

    if concept_name:
        concept_id = _find_concept_id(conn, concept_name)
        if not concept_id:
            print(f"❌ 找不到概念: {concept_name}")
            conn.close()
            return

        # Show this concept and its connections
        row = conn.execute("SELECT * FROM concepts WHERE id=?", (concept_id,)).fetchone()
        if not row:
            conn.close()
            return

        print(f"\n{'='*50}")
        print(f"📌 {row['concept']}")
        print(f"   来源: {row['source']}")
        print(f"   置信度: {row['confidence']}")
        print(f"   标签: {', '.join(json.loads(row['tags']))}")
        if row['context']:
            print(f"   上下文: {row['context'][:100]}...")
        print()

        # Outgoing links
        out_links = conn.execute("""
            SELECT cl.to_concept, cl.relation, c.concept as target_name
            FROM concept_links cl
            JOIN concepts c ON c.id = cl.to_concept
            WHERE cl.from_concept = ?
        """, (concept_id,)).fetchall()

        # Incoming links
        in_links = conn.execute("""
            SELECT cl.from_concept, cl.relation, c.concept as source_name
            FROM concept_links cl
            JOIN concepts c ON c.id = cl.from_concept
            WHERE cl.to_concept = ?
        """, (concept_id,)).fetchall()

        if out_links:
            print("  ➡️  指向:")
            for link in out_links:
                print(f"     --[{link['relation']}]--> {link['target_name']}")

        if in_links:
            print("  ⬅️  被指向:")
            for link in in_links:
                print(f"     {link['source_name']} --[{link['relation']}]--> 本概念")

        if not out_links and not in_links:
            print("  (暂无关联)")

    else:
        # Show full graph overview
        concepts = conn.execute("SELECT * FROM concepts WHERE status='active' ORDER BY updated_at DESC").fetchall()
        links = conn.execute("""
            SELECT cl.from_concept, cl.to_concept, cl.relation,
                   c1.concept as from_name, c2.concept as to_name
            FROM concept_links cl
            JOIN concepts c1 ON c1.id = cl.from_concept
            JOIN concepts c2 ON c2.id = cl.to_concept
        """).fetchall()

        print(f"\n{'='*50}")
        print(f"🧠 知识图谱概览")
        print(f"   概念数: {len(concepts)}")
        print(f"   关联数: {len(links)}")
        print(f"{'='*50}\n")

        for c in concepts:
            tags = json.loads(c["tags"])
            tag_str = f" [{', '.join(tags)}]" if tags else ""
            print(f"  📌 {c['concept']} ({c['confidence']}){tag_str}")

        if links:
            print(f"\n  关联:")
            for link in links:
                print(f"    {link['from_name']} --[{link['relation']}]--> {link['to_name']}")

    conn.close()


def show_summary():
    conn = get_db()

    concepts = conn.execute("SELECT * FROM concepts WHERE status='active' ORDER BY updated_at DESC").fetchall()
    beliefs = conn.execute("SELECT * FROM beliefs WHERE status='active' ORDER BY updated_at DESC").fetchall()
    challenged = conn.execute("SELECT * FROM beliefs WHERE status='challenged'").fetchall()
    recent = conn.execute("SELECT * FROM daily_entries ORDER BY date DESC LIMIT 5").fetchall()

    print(f"\n{'='*50}")
    print(f"🧠 Knowledge Engine 摘要")
    print(f"{'='*50}")
    print(f"\n📌 活跃概念: {len(concepts)}")
    for c in concepts[:10]:
        print(f"   • {c['concept']} ({c['confidence']})")

    print(f"\n💭 活跃信念: {len(beliefs)}")
    for b in beliefs[:10]:
        print(f"   • {b['belief']} [{b['confidence']}]")

    if challenged:
        print(f"\n⚠️  被挑战的信念: {len(challenged)}")
        for b in challenged:
            print(f"   • {b['belief']}")

    if recent:
        print(f"\n📅 最近记录:")
        for entry in recent:
            print(f"   [{entry['date']}] {entry['title'] or '(无标题)'}")

    conn.close()


# ─── 辅助函数 ───

def _make_id(text):
    """从文本生成 ID"""
    # Use hash for consistent IDs
    import hashlib
    clean = re.sub(r'[^\w\u4e00-\u9fff]', '-', text.lower().strip())
    clean = re.sub(r'-+', '-', clean).strip('-')[:50]
    h = hashlib.md5(text.encode()).hexdigest()[:8]
    return f"{clean}-{h}"


def _find_concept_id(conn, name):
    """通过名称查找概念 ID"""
    row = conn.execute("SELECT id FROM concepts WHERE concept=?", (name,)).fetchone()
    if row:
        return row["id"]
    # Try fuzzy match
    row = conn.execute("SELECT id FROM concepts WHERE concept LIKE ?", (f"%{name}%",)).fetchone()
    return row["id"] if row else None


def _tokenize(text):
    """简单分词"""
    # Chinese: split by character for matching
    # English: split by space/punctuation
    text = text.lower()
    words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z0-9]+', text)
    return [w for w in words if len(w) > 1]


def _text_match(query, text):
    """简单文本匹配"""
    query_lower = query.lower()
    text_lower = text.lower()
    return query_lower in text_lower


# ─── CLI ───

def main():
    parser = argparse.ArgumentParser(description="Knowledge Engine - 个人知识管理")
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="添加概念")
    p_add.add_argument("--concept", required=True)
    p_add.add_argument("--source", default="")
    p_add.add_argument("--context", default="")
    p_add.add_argument("--tags", default="")
    p_add.add_argument("--confidence", default="medium")

    # search
    p_search = sub.add_parser("search", help="搜索概念")
    p_search.add_argument("--query", default="")
    p_search.add_argument("--tags", default="")
    p_search.add_argument("--limit", type=int, default=20)

    # link
    p_link = sub.add_parser("link", help="关联概念")
    p_link.add_argument("--from", dest="from_concept", required=True)
    p_link.add_argument("--to", dest="to_concept", required=True)
    p_link.add_argument("--relation", default="related")

    # believe
    p_believe = sub.add_parser("believe", help="记录信念")
    p_believe.add_argument("--belief", required=True)
    p_believe.add_argument("--reasoning", default="")
    p_believe.add_argument("--confidence", default="medium")

    # update-belief
    p_ub = sub.add_parser("update-belief", help="更新信念")
    p_ub.add_argument("--id", required=True)
    p_ub.add_argument("--status", default=None)
    p_ub.add_argument("--note", default="")
    p_ub.add_argument("--confidence", default=None)

    # hierarchical
    p_hier = sub.add_parser("hierarchical", help="分层检索")
    p_hier.add_argument("--query", default="")
    p_hier.add_argument("--recent", type=int, default=5)
    p_hier.add_argument("--semantic", type=int, default=5)
    p_hier.add_argument("--summary", type=int, default=2)

    # graph
    p_graph = sub.add_parser("graph", help="知识图谱")
    p_graph.add_argument("--concept", default=None)

    # summary
    sub.add_parser("summary", help="摘要")

    # stats
    p_stats = sub.add_parser("stats", help="使用统计")
    p_stats.add_argument("--days", type=int, default=30)
    p_stats.add_argument("--concept", default=None)

    # auto-adjust
    p_aa = sub.add_parser("auto-adjust", help="自动调整置信度")
    p_aa.add_argument("--dry-run", action="store_true")

    # prune
    p_prune = sub.add_parser("prune", help="清理废弃概念")
    p_prune.add_argument("--days", type=int, default=60)
    p_prune.add_argument("--dry-run", action="store_true")

    # similar
    p_sim = sub.add_parser("similar", help="查找相似概念")
    p_sim.add_argument("--concept", required=True)
    p_sim.add_argument("--threshold", type=float, default=0.3)

    # beliefs-decay
    sub.add_parser("beliefs-decay", help="信念衰减报告")

    # eval
    sub.add_parser("eval", help="运行评估套件")

    args = parser.parse_args()

    if args.command == "add":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
        add_concept(args.concept, args.source, args.context, tags, args.confidence)

    elif args.command == "search":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else None
        results = search_concepts(args.query, tags, limit=args.limit)
        if results:
            print(f"\n🔍 找到 {len(results)} 个概念:\n")
            for r in results:
                tags_str = ", ".join(json.loads(r["tags"])) if r["tags"] else ""
                print(f"  📌 {r['concept']} ({r['confidence']})")
                if tags_str:
                    print(f"     标签: {tags_str}")
                if r["context"]:
                    print(f"     {r['context'][:80]}...")
                print()
                # 记录搜索命中
                log_usage(r['id'], 'search_hit', args.query)
        else:
            print("没有找到匹配的概念")

    elif args.command == "link":
        link_concepts(args.from_concept, args.to_concept, args.relation)

    elif args.command == "believe":
        add_belief(args.belief, args.reasoning, args.confidence)

    elif args.command == "update-belief":
        update_belief(args.id, args.status, args.note, args.confidence)

    elif args.command == "hierarchical":
        conn = get_db()
        show_hierarchical(conn, args.query, args.recent, args.semantic, args.summary)
        conn.close()

    elif args.command == "graph":
        show_graph(args.concept)

    elif args.command == "summary":
        show_summary()

    elif args.command == "stats":
        conn = get_db()
        if args.concept:
            cid = _find_concept_id(conn, args.concept)
            if cid:
                stats = get_concept_stats(cid, args.days)
                print(f"\n📊 概念使用统计 [{args.concept}] ({args.days}天)")
                print(f"   搜索命中: {stats['search_hit']}")
                print(f"   关联引用: {stats['link_ref']}")
                print(f"   图谱查看: {stats['graph_view']}")
                print(f"   总使用: {stats['total']}")
                print(f"   存在天数: {stats['age_days']}")
                print(f"   最近使用: {stats['last_used'] or '从未'}")
            else:
                print(f"❌ 找不到概念: {args.concept}")
        else:
            all_stats = get_all_usage_stats(args.days)
            print(f"\n📊 全局使用统计 ({args.days}天)")
            if all_stats:
                for cid, s in sorted(all_stats.items(), key=lambda x: x[1]['total'], reverse=True):
                    concept = conn.execute("SELECT concept FROM concepts WHERE id=?", (cid,)).fetchone()
                    name = concept['concept'] if concept else cid
                    print(f"   {name}: {s['total']}次 (搜索{s['search_hit']} 关联{s['link_ref']})")
            else:
                print("   (无使用记录)")
        conn.close()

    elif args.command == "auto-adjust":
        conn = get_db()
        result = auto_adjust_confidence(conn, dry_run=args.dry_run)
        prefix = "[DRY RUN] " if args.dry_run else ""
        if result['upgrades']:
            print(f"\n{prefix}⬆️  升级:")
            for cid, name, old, new in result['upgrades']:
                print(f"   {name}: {old} → {new}")
        if result['downgrades']:
            print(f"\n{prefix}⬇️  降级:")
            for cid, name, old, new in result['downgrades']:
                print(f"   {name}: {old} → {new}")
        if result['deprecations']:
            print(f"\n{prefix}🗑️  废弃:")
            for cid, name in result['deprecations']:
                print(f"   {name}")
        if not result['upgrades'] and not result['downgrades'] and not result['deprecations']:
            print(f"\n{prefix}无需调整")
        conn.close()

    elif args.command == "prune":
        conn = get_db()
        since = (datetime.now() - timedelta(days=args.days)).isoformat()
        deprecated = conn.execute(
            "SELECT * FROM concepts WHERE status='deprecated' AND updated_at < ?",
            (since,)
        ).fetchall()
        if deprecated:
            print(f"\n🗑️  清理 {len(deprecated)} 个废弃概念:")
            for c in deprecated:
                print(f"   • {c['concept']}")
                if not args.dry_run:
                    # 删除关联
                    conn.execute("DELETE FROM concept_links WHERE from_concept=? OR to_concept=?", (c['id'], c['id']))
                    # 删除使用记录
                    conn.execute("DELETE FROM usage_log WHERE concept_id=?", (c['id'],))
                    # 删除概念
                    conn.execute("DELETE FROM concepts WHERE id=?", (c['id'],))
                    # 删除文件
                    card_path = os.path.join(CONCEPTS_DIR, f"{c['id']}.json")
                    if os.path.exists(card_path):
                        os.remove(card_path)
            if not args.dry_run:
                conn.commit()
                print(f"   ✅ 已清理")
            else:
                print(f"   [DRY RUN] 未实际删除")
        else:
            print("没有需要清理的废弃概念")
        conn.close()

    elif args.command == "similar":
        results = find_similar_concepts(args.concept, threshold=args.threshold)
        if results:
            print(f"\n🔍 与「{args.concept}」相似的概念:")
            for cid, name, score in results:
                bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
                print(f"   {bar} {score} — {name}")
        else:
            print(f"没有找到与「{args.concept}」相似的概念")

    elif args.command == "beliefs-decay":
        beliefs = get_beliefs_with_decay()
        if beliefs:
            print(f"\n💭 信念衰减报告\n")
            for b in beliefs:
                marker = "⚠️" if b["challenges_count"] > 0 else "💭"
                conf_bar = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(b["effective_confidence"], "⚪")
                print(f"  {marker} {conf_bar} [{b['effective_confidence']}] {b['belief']}")
                print(f"     原始置信度: {b['original_confidence']} | 存在: {b['age_days']}天 | 挑战: {b['challenges_count']}次")
                if b["decay_note"]:
                    print(f"     📉 {b['decay_note']}")
                print()
        else:
            print("没有活跃信念")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
