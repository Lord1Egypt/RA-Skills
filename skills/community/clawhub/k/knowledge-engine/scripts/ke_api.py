#!/usr/bin/env python3
"""
Knowledge Engine - 子 Agent API
为其他脚本和子 agent 提供轻量级 Python 接口

用法：
    from ke_api import ke
    
    # 搜索
    results = ke.search("分发", limit=5)
    
    # 添加概念（带循环检测）
    ke.concept("新概念", source="HN", tags=["创业"])
    
    # 获取信念（带时间衰减）
    beliefs = ke.beliefs(top=5)
    
    # 分层检索
    context = ke.context("创业", recent=3, semantic=5)
    
    # 快速摘要
    summary = ke.summary()
"""

import sys
import os
import json
from datetime import datetime

# 确保能导入同目录的 concept_manager
sys.path.insert(0, os.path.dirname(__file__))
from concept_manager import (
    get_db, add_concept, search_concepts, link_concepts,
    add_belief, update_belief, get_beliefs_with_decay,
    find_similar_concepts, hierarchical_search,
    show_summary, log_usage, get_all_usage_stats,
    _find_concept_id, _tokenize
)
from concept_synthesis import distill, reflection, generative_synthesis


class KnowledgeEngineAPI:
    """轻量级知识引擎接口，供子 agent 使用"""
    
    def search(self, query, tags=None, limit=10):
        """
        搜索概念，返回简洁结果
        
        返回: [{"concept": "...", "confidence": "...", "context": "...", "tags": [...]}]
        """
        results = search_concepts(query, tags=tags, limit=limit)
        # 记录使用
        for r in results:
            log_usage(r["id"], "search_hit", query)
        return results
    
    def concept(self, name, source="", context="", tags=None, confidence="medium", force=False):
        """
        添加或更新概念（自动循环检测）
        
        force=True 跳过重复检查
        返回: concept_id
        """
        return add_concept(name, source, context, tags, confidence, force=force)
    
    def link(self, from_name, to_name, relation="related"):
        """关联两个概念"""
        return link_concepts(from_name, to_name, relation)
    
    def belief(self, text, reasoning="", confidence="medium"):
        """记录信念"""
        return add_belief(text, reasoning, confidence)
    
    def challenge_belief(self, belief_id, note):
        """挑战一个信念"""
        return update_belief(belief_id, status="challenged", note=note)
    
    def beliefs(self, top=10):
        """
        获取信念列表（带时间衰减）
        
        返回: [{"belief": "...", "effective_confidence": "...", "age_days": N, ...}]
        """
        all_beliefs = get_beliefs_with_decay()
        return all_beliefs[:top]
    
    def context(self, query="", recent=5, semantic=5, summary=2):
        """
        分层检索：获取供 agent 使用的上下文
        
        返回: {
            "recent": [...],     # 最近的概念
            "semantic": [...],   # 语义相关的概念
            "summary": [...]     # 最近的蒸馏报告
        }
        """
        conn = get_db()
        results = hierarchical_search(conn, query, recent, semantic, summary)
        conn.close()
        return results
    
    def similar(self, concept_name, tags=None, threshold=0.3):
        """查找相似概念（循环检测的非破坏性版本）"""
        return find_similar_concepts(concept_name, tags, threshold)
    
    def summary(self):
        """
        获取知识引擎摘要
        
        返回: {"concepts": N, "beliefs": N, "challenged": N, 
               "top_concepts": [...], "top_beliefs": [...]}
        """
        conn = get_db()
        concepts = conn.execute("SELECT * FROM concepts WHERE status='active' ORDER BY updated_at DESC").fetchall()
        beliefs = conn.execute("SELECT * FROM beliefs WHERE status='active' ORDER BY updated_at DESC").fetchall()
        challenged = conn.execute("SELECT * FROM beliefs WHERE status='challenged'").fetchall()
        
        result = {
            "concepts_count": len(concepts),
            "beliefs_count": len(beliefs),
            "challenged_count": len(challenged),
            "top_concepts": [
                {"concept": c["concept"], "confidence": c["confidence"], "tags": json.loads(c["tags"])}
                for c in concepts[:10]
            ],
            "top_beliefs": [
                {"belief": b["belief"], "confidence": b["confidence"]}
                for b in beliefs[:5]
            ],
        }
        conn.close()
        return result
    
    def distill(self, days=7):
        """执行蒸馏流程"""
        conn = get_db()
        report = distill(conn, days)
        conn.close()
        return report
    
    def stats(self, days=30):
        """获取使用统计"""
        return get_all_usage_stats(days)


# 全局单例
ke = KnowledgeEngineAPI()


# ─── 命令行快速入口 ───

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Knowledge Engine API — 快速查询")
    parser.add_argument("action", choices=["search", "summary", "beliefs", "context", "similar", "stats"],
                       help="操作类型")
    parser.add_argument("query", nargs="?", default="", help="搜索词")
    parser.add_argument("--top", type=int, default=10, help="返回数量")
    parser.add_argument("--tags", default="", help="标签过滤（逗号分隔）")
    
    args = parser.parse_args()
    
    if args.action == "search":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else None
        results = ke.search(args.query, tags=tags, limit=args.top)
        for r in results:
            tags_str = ", ".join(r.get("tags", []))
            print(f"  📌 {r['concept']} ({r['confidence']})" + (f" [{tags_str}]" if tags_str else ""))
            if r.get("context"):
                print(f"     {r['context'][:80]}")
    
    elif args.action == "summary":
        s = ke.summary()
        print(f"📌 活跃概念: {s['concepts_count']}")
        print(f"💭 活跃信念: {s['beliefs_count']}")
        print(f"⚠️  被挑战: {s['challenged_count']}")
        if s["top_concepts"]:
            print("\n热门概念:")
            for c in s["top_concepts"][:5]:
                print(f"  • {c['concept']} ({c['confidence']})")
    
    elif args.action == "beliefs":
        beliefs = ke.beliefs(top=args.top)
        for b in beliefs:
            marker = "⚠️" if b["challenges_count"] > 0 else "💭"
            print(f"  {marker} [{b['effective_confidence']}] {b['belief']}")
            if b["decay_note"]:
                print(f"     📉 {b['decay_note']}")
    
    elif args.action == "context":
        ctx = ke.context(args.query, recent=5, semantic=5, summary=2)
        if ctx["recent"]:
            print("📌 Recent:")
            for r in ctx["recent"]:
                print(f"  • {r['concept']}")
        if ctx["semantic"]:
            print("🔍 Semantic:")
            for r in ctx["semantic"]:
                print(f"  • {r['concept']}")
    
    elif args.action == "similar":
        if not args.query:
            print("用法: ke_api.py similar <概念名称>")
        else:
            results = ke.similar(args.query)
            if results:
                for cid, name, score in results:
                    print(f"  🔗 {name} (相似度 {score})")
            else:
                print("没有找到相似概念")
    
    elif args.action == "stats":
        stats = ke.stats(days=args.top)
        for cid, s in sorted(stats.items(), key=lambda x: x[1]['total'], reverse=True)[:10]:
            print(f"  {cid}: {s['total']}次")
