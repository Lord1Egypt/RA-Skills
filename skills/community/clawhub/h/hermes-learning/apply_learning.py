#!/usr/bin/env python3
"""
Hermes 学习材料应用脚本 - 阶段4修复版
修复：evolution.db 全局路径、batch_size 膨胀、反馈数据结构
"""

import json
import sys
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime

HERMES_SHARED = Path.home() / ".hermes" / "shared"
LEARNING_DIR = Path(__file__).parent
STRATEGIES_FILE = LEARNING_DIR / "strategies.json"
EFFECTS_FILE = LEARNING_DIR / "learning_effects.json"

# 全局统一的 evolution.db 路径（不再依赖动态查找工作区）
EVOLUTION_DB_DIR = Path.home() / ".workbuddy" / "memory"
EVOLUTION_DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = EVOLUTION_DB_DIR / "evolution.db"

def _ensure_evolution_db():
    """确保 evolution.db 存在且表结构正确"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'general',
                importance INTEGER NOT NULL DEFAULT 3,
                tags TEXT DEFAULT '[]',
                source TEXT DEFAULT 'manual',
                created_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL
            )
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS concept_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_a TEXT NOT NULL,
                concept_b TEXT NOT NULL,
                relation TEXT NOT NULL DEFAULT 'related',
                weight REAL NOT NULL DEFAULT 1.0,
                created_at TEXT NOT NULL,
                UNIQUE(concept_a, concept_b, relation)
            )
        """)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️  evolution.db 初始化失败: {e}")
        return False

# 启动时确保 db 存在
DB_READY = _ensure_evolution_db()

def load_summary():
    """加载学习摘要"""
    summary_path = HERMES_SHARED / "memory_summary.json"
    if summary_path.exists():
        with open(summary_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_strategies():
    """加载策略库"""
    if STRATEGIES_FILE.exists():
        with open(STRATEGIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "version": "3.0",
        "last_updated": None,
        "success_patterns": [],
        "avoid_patterns": [],
        "optimizations": []
    }

def save_strategies(strategies):
    """保存策略库"""
    strategies["last_updated"] = datetime.now().isoformat()
    with open(STRATEGIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(strategies, f, ensure_ascii=False, indent=2)

def load_effects():
    """加载效果追踪"""
    if EFFECTS_FILE.exists():
        with open(EFFECTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"applied_sessions": [], "total_applied": 0, "feedback_sent": 0}

def save_effects(effects):
    """保存效果追踪"""
    with open(EFFECTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(effects, f, ensure_ascii=False, indent=2)

def generate_pattern_id(content):
    """为模式生成唯一ID"""
    return hashlib.md5(content.encode()).hexdigest()[:8]

def pattern_exists(patterns, pattern_id):
    """检查模式是否已存在"""
    return any(p.get("id") == pattern_id for p in patterns)

def add_to_evolution_db(content, category, importance=4, tags=None, source="hermes_learning"):
    """将学习到的模式写入 evolution.db（全局路径）"""
    if not DB_READY:
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        mem_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        # 检查是否已存在
        c.execute("SELECT id FROM memories WHERE hash = ?", (mem_hash,))
        if c.fetchone():
            conn.close()
            return False  # 已存在，不重复添加
        
        # 插入新记忆
        c.execute("""
            INSERT INTO memories (hash, content, category, importance, tags, source, created_at, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mem_hash, content, category, importance,
            json.dumps(tags or [], ensure_ascii=False), source,
            datetime.now().isoformat(), datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️  写入 evolution.db 失败: {e}")
        return False

def add_concept_link(concept_a, concept_b, relation="related", weight=1.0):
    """在 concept_links 表中建立概念关联（全局路径）"""
    if not DB_READY:
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # 检查是否已存在
        c.execute("""
            SELECT id FROM concept_links 
            WHERE concept_a = ? AND concept_b = ? AND relation = ?
        """, (concept_a, concept_b, relation))
        
        if c.fetchone():
            # 更新权重
            c.execute("""
                UPDATE concept_links SET weight = weight + ?
                WHERE concept_a = ? AND concept_b = ? AND relation = ?
            """, (weight, concept_a, concept_b, relation))
        else:
            # 插入新关联
            c.execute("""
                INSERT INTO concept_links (concept_a, concept_b, relation, weight, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (concept_a, concept_b, relation, weight, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️  写入 concept_links 失败: {e}")
        return False

def apply_success_patterns(strategies, examples):
    """应用成功模式 - 同时写入 strategies.json 和 evolution.db"""
    added = 0
    db_added = 0
    
    for ex in examples:
        content = ex.get("content", "")
        if not content:
            continue
        
        pattern_id = generate_pattern_id(content)
        if pattern_exists(strategies["success_patterns"], pattern_id):
            continue
        
        # 添加到策略库
        strategies["success_patterns"].append({
            "id": pattern_id,
            "pattern": content[:100] + "..." if len(content) > 100 else content,
            "full_content": content,
            "source": ex.get("source", "hermes"),
            "timestamp": ex.get("timestamp", datetime.now().isoformat()),
            "applied_count": 0,
            "confidence": 0.9
        })
        added += 1
        
        # 同步到 evolution.db
        if add_to_evolution_db(
            content=f"[Hermes成功模式] {content}",
            category="success_pattern",
            importance=5,
            tags=["hermes", "success_pattern", pattern_id],
            source="hermes_learning"
        ):
            db_added += 1
        
        # 建立概念关联
        add_concept_link("Hermes学习", content[:30], relation="learned_from", weight=0.9)
    
    return added, db_added

def apply_avoid_patterns(strategies, examples):
    """应用避免模式"""
    added = 0
    db_added = 0
    
    for ex in examples:
        content = ex.get("content", "")
        if not content:
            continue
        
        pattern_id = generate_pattern_id(content)
        if pattern_exists(strategies["avoid_patterns"], pattern_id):
            continue
        
        strategies["avoid_patterns"].append({
            "id": pattern_id,
            "pattern": content[:100] + "..." if len(content) > 100 else content,
            "full_content": content,
            "source": ex.get("source", "hermes"),
            "timestamp": ex.get("timestamp", datetime.now().isoformat()),
            "reason": "hermes_identified"
        })
        added += 1
        
        # 同步到 evolution.db（标记为 avoid）
        if add_to_evolution_db(
            content=f"[Hermes避免模式] {content}",
            category="avoid_pattern",
            importance=4,
            tags=["hermes", "avoid_pattern", pattern_id],
            source="hermes_learning"
        ):
            db_added += 1
    
    return added, db_added

def apply_optimizations(strategies, recommendations):
    """应用优化建议"""
    added = 0
    
    for rec in recommendations:
        suggestion = rec.get("suggestion", "")
        if not suggestion:
            continue
        
        exists = any(o.get("suggestion") == suggestion for o in strategies["optimizations"])
        if exists:
            continue
        
        opt_id = generate_pattern_id(suggestion)
        strategies["optimizations"].append({
            "id": opt_id,
            "suggestion": suggestion,
            "type": rec.get("type", "general"),
            "priority": rec.get("priority", "medium"),
            "status": "pending",
            "related_tasks": rec.get("metadata", {}).get("related_tasks", []) if isinstance(rec.get("metadata"), dict) else [],
            "timestamp": datetime.now().isoformat()
        })
        added += 1
        
        # 优化建议也写入 evolution.db
        add_to_evolution_db(
            content=f"[Hermes优化建议] {suggestion}",
            category="optimization",
            importance=4 if rec.get("priority") == "medium" else 5,
            tags=["hermes", "optimization", opt_id],
            source="hermes_learning"
        )
    
    return added

def check_avoid_patterns(content):
    """
    前置检查：检测内容是否包含应避免的模式
    可在其他脚本中调用进行前置检查
    """
    strategies = load_strategies()
    avoid_patterns = strategies.get("avoid_patterns", [])
    
    warnings = []
    for pattern in avoid_patterns:
        pattern_text = pattern.get("full_content", "")
        if any(keyword in content for keyword in pattern_text.split()[:5]):
            warnings.append({
                "pattern_id": pattern.get("id"),
                "pattern": pattern.get("pattern"),
                "reason": pattern.get("reason")
            })
    
    return warnings

# ── 阶段3：双向反馈闭环 ───────────────────────────────────────────────────────
def read_workbuddy_feedback():
    """读取 WorkBuddy 发来的效果反馈"""
    feedback_file = HERMES_SHARED / "workbuddy_feedback.json"
    if feedback_file.exists():
        try:
            with open(feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def analyze_feedback_effectiveness():
    """分析 WorkBuddy 反馈，评估学习效果"""
    feedback_list = read_workbuddy_feedback()
    if not feedback_list:
        return None
    
    # 分析最近10条反馈
    recent = feedback_list[-10:]
    
    total_predictions = sum(f.get("data", {}).get("predictions_made", 0) for f in recent)
    total_knowledge = sum(f.get("data", {}).get("new_knowledge", 0) for f in recent)
    
    # 计算预测准确率（基于反馈中的置信度）
    confidences = []
    for f in recent:
        for p in f.get("data", {}).get("predictions", []):
            confidences.append(p.get("confidence", 0))
    
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    return {
        "feedback_count": len(feedback_list),
        "recent_analyzed": len(recent),
        "total_predictions": total_predictions,
        "total_knowledge": total_knowledge,
        "avg_prediction_confidence": avg_confidence,
        "last_feedback_time": recent[-1].get("timestamp") if recent else None
    }

def send_learning_effect_report():
    """生成学习效果报告回传给 Hermes"""
    effects = load_effects()
    strategies = load_strategies()
    feedback_analysis = analyze_feedback_effectiveness()
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "source": "apply_learning",
        "type": "learning_effect_summary",
        "data": {
            "total_applied": effects.get("total_applied", 0),
            "total_sessions": len(effects.get("applied_sessions", [])),
            "strategies_count": {
                "success": len(strategies.get("success_patterns", [])),
                "avoid": len(strategies.get("avoid_patterns", [])),
                "optimization": len(strategies.get("optimizations", []))
            },
            "workbuddy_feedback": feedback_analysis
        }
    }
    
    # 写入共享目录供 Hermes 读取
    report_path = HERMES_SHARED / "learning_effect_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return report

def apply_learnings():
    """应用学习材料 - 阶段3完整实现"""
    summary = load_summary()
    strategies = load_strategies()
    effects = load_effects()
    
    print("🚀 应用 Hermes 学习材料 (阶段3 - 双向反馈闭环)...")
    print("=" * 60)
    
    total_added = {"success": 0, "avoid": 0, "optimization": 0}
    db_added = {"success": 0, "avoid": 0}
    
    # 处理关键洞察
    for insight in summary.get("key_insights", []):
        title = insight.get("title", "")
        examples = insight.get("examples", [])
        
        if title == "成功任务模式":
            count, db_count = apply_success_patterns(strategies, examples)
            total_added["success"] = count
            db_added["success"] = db_count
            print(f"✅ 成功模式: +{count} 条 (DB: +{db_count})")
            
        elif title == "常见失败模式":
            count, db_count = apply_avoid_patterns(strategies, examples)
            total_added["avoid"] = count
            db_added["avoid"] = db_count
            print(f"⚠️  避免模式: +{count} 条 (DB: +{db_count})")
    
    # 处理优化建议
    recommendations = summary.get("top_recommendations", [])
    feedback_path = LEARNING_DIR / "memory_feedback.json"
    if feedback_path.exists():
        with open(feedback_path, 'r', encoding='utf-8') as f:
            feedback = json.load(f)
            for fb in feedback:
                if fb.get("type") == "suggestion":
                    recommendations.append({
                        "suggestion": fb.get("content", ""),
                        "type": "optimization",
                        "priority": fb.get("priority", "medium"),
                        "metadata": fb.get("metadata", {})
                    })
    
    count = apply_optimizations(strategies, recommendations)
    total_added["optimization"] = count
    print(f"🔧 优化建议: +{count} 条")
    
    # 阶段3：读取 WorkBuddy 反馈并分析
    feedback_analysis = analyze_feedback_effectiveness()
    if feedback_analysis:
        print(f"📊 WorkBuddy 反馈分析:")
        print(f"   - 累计反馈: {feedback_analysis['feedback_count']} 条")
        print(f"   - 近期预测: {feedback_analysis['total_predictions']} 次")
        print(f"   - 平均置信度: {feedback_analysis['avg_prediction_confidence']:.1%}")
    
    # 保存策略库
    save_strategies(strategies)
    
    # 记录本次应用
    session_record = {
        "timestamp": datetime.now().isoformat(),
        "hermes_update_time": summary.get("last_update"),
        "total_memories": summary.get("total_memories", 0),
        "added": total_added,
        "db_added": db_added,
        "feedback_analysis": feedback_analysis,
        "current_totals": {
            "success_patterns": len(strategies["success_patterns"]),
            "avoid_patterns": len(strategies["avoid_patterns"]),
            "optimizations": len(strategies["optimizations"])
        }
    }
    effects["applied_sessions"].append(session_record)
    effects["total_applied"] = sum(
        s["added"]["success"] + s["added"]["avoid"] + s["added"]["optimization"]
        for s in effects["applied_sessions"]
    )
    save_effects(effects)
    
    # 阶段3：生成效果报告回传 Hermes
    effect_report = send_learning_effect_report()
    
    print("=" * 60)
    print(f"📊 策略库总计:")
    print(f"   成功模式: {len(strategies['success_patterns'])}")
    print(f"   避免模式: {len(strategies['avoid_patterns'])}")
    print(f"   优化建议: {len(strategies['optimizations'])}")
    if DB_READY:
        print(f"📊 已同步到 evolution.db ({DB_PATH})")
    print(f"🎉 学习材料应用完成！")
    print(f"📄 应用报告: {HERMES_SHARED / 'learning_applied_report.json'}")
    print(f"📊 效果报告: {HERMES_SHARED / 'learning_effect_report.json'}")

def show_summary():
    """显示摘要和策略库状态"""
    summary = load_summary()
    strategies = load_strategies()
    effects = load_effects()
    feedback_analysis = analyze_feedback_effectiveness()
    
    print("📚 Hermes 学习摘要")
    print("=" * 50)
    print(f"最后更新: {summary.get('last_update', '未知')}")
    print(f"总记忆: {summary.get('total_memories', 0)}")
    
    for insight in summary.get("key_insights", []):
        print(f"\n{insight.get('title', '未知')}:")
        print(f"  {insight.get('description', '')}")
        print(f"  示例: {len(insight.get('examples', []))}")
    
    print("\n" + "=" * 50)
    print("📊 策略库状态")
    print(f"版本: {strategies.get('version', 'unknown')}")
    print(f"最后更新: {strategies.get('last_updated', '从未')}")
    print(f"成功模式: {len(strategies.get('success_patterns', []))}")
    print(f"避免模式: {len(strategies.get('avoid_patterns', []))}")
    print(f"优化建议: {len(strategies.get('optimizations', []))}")
    print(f"\n累计应用会话: {len(effects.get('applied_sessions', []))}")
    print(f"累计学习条目: {effects.get('total_applied', 0)}")
    
    if feedback_analysis:
        print(f"\n📊 WorkBuddy 反馈:")
        print(f"   累计反馈: {feedback_analysis['feedback_count']} 条")
        print(f"   平均预测置信度: {feedback_analysis['avg_prediction_confidence']:.1%}")
    
    if DB_READY:
        try:
            conn = sqlite3.connect(str(DB_PATH))
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM memories WHERE source = 'hermes_learning'")
            count = c.fetchone()[0]
            conn.close()
            print(f"\nevolution.db 中 Hermes 学习条目: {count}")
        except Exception as e:
            print(f"\nevolution.db 查询失败: {e}")

def list_strategies():
    """列出所有策略"""
    strategies = load_strategies()
    
    print("📋 成功模式列表")
    print("=" * 50)
    for i, p in enumerate(strategies.get("success_patterns", []), 1):
        print(f"{i}. [{p.get('id')}] {p.get('pattern')[:60]}...")
        print(f"   来源: {p.get('source')}, 置信度: {p.get('confidence')}")
    
    print("\n📋 避免模式列表")
    print("=" * 50)
    for i, p in enumerate(strategies.get("avoid_patterns", []), 1):
        print(f"{i}. [{p.get('id')}] {p.get('pattern')[:60]}...")
        print(f"   原因: {p.get('reason')}")
    
    print("\n📋 优化建议列表")
    print("=" * 50)
    for i, opt in enumerate(strategies.get("optimizations", []), 1):
        status_icon = "⏳" if opt.get('status') == 'pending' else "✅"
        print(f"{i}. {status_icon} [{opt.get('priority', 'medium')}] {opt.get('suggestion')[:50]}...")

def check_content(content):
    """CLI 工具：检查内容是否包含应避免的模式"""
    warnings = check_avoid_patterns(content)
    if warnings:
        print("⚠️  检测到应避免的模式:")
        for w in warnings:
            print(f"  - [{w['pattern_id']}] {w['pattern']}")
            print(f"    原因: {w['reason']}")
        return 1
    else:
        print("✅ 未检测到应避免的模式")
        return 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "apply":
            apply_learnings()
        elif sys.argv[1] == "list":
            list_strategies()
        elif sys.argv[1] == "status":
            show_summary()
        elif sys.argv[1] == "check":
            content = sys.argv[2] if len(sys.argv) > 2 else ""
            sys.exit(check_content(content))
        elif sys.argv[1] == "feedback":
            # 阶段3：查看反馈分析
            analysis = analyze_feedback_effectiveness()
            if analysis:
                print(json.dumps(analysis, ensure_ascii=False, indent=2))
            else:
                print("暂无 WorkBuddy 反馈数据")
        else:
            print(f"未知命令: {sys.argv[1]}")
            print("用法: apply_learning.py [apply|list|status|check <内容>|feedback]")
    else:
        show_summary()
