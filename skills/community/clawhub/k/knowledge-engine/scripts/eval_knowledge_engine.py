#!/usr/bin/env python3
"""
Knowledge Engine - 评估器
基于 Anthropic Evals 框架：Trial → Transcript → Outcome

六项测试：
1. Storage   — 概念存储完整性
2. Retrieval — 搜索召回率与精确率
3. Association — 关联发现能力
4. Confidence — 使用驱动的置信度调整
5. Synthesis — 蒸馏发现洞察
6. Pruning   — 低价值概念清理
"""

import json
import os
import sys
import sqlite3
import shutil
import tempfile
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from concept_manager import (
    get_db, _make_id, add_concept, search_concepts, link_concepts,
    add_belief, update_belief, auto_adjust_confidence,
    get_all_usage_stats, log_usage, hierarchical_search
)
from concept_synthesis import distill, reflection, generative_synthesis


class EvalRunner:
    """评估运行器"""
    
    def __init__(self):
        self.results = []
        self.transcript = []
        self._setup_test_db()
    
    def _setup_test_db(self):
        """创建测试用的临时数据库"""
        self.test_dir = tempfile.mkdtemp(prefix="ke_eval_")
        self.test_db = os.path.join(self.test_dir, "test.db")
        self.test_concepts_dir = os.path.join(self.test_dir, "concepts")
        self.test_beliefs_dir = os.path.join(self.test_dir, "beliefs")
        self.test_insights_dir = os.path.join(self.test_dir, "insights")
        os.makedirs(self.test_concepts_dir)
        os.makedirs(self.test_beliefs_dir)
        os.makedirs(self.test_insights_dir)
        
        # Monkey-patch paths for testing
        import concept_manager as cm
        self._orig_db_path = cm.DB_PATH
        self._orig_concepts_dir = cm.CONCEPTS_DIR
        self._orig_beliefs_dir = cm.BELIEFS_DIR
        cm.DB_PATH = self.test_db
        cm.CONCEPTS_DIR = self.test_concepts_dir
        cm.BELIEFS_DIR = self.test_beliefs_dir
        
        import concept_synthesis as cs
        self._orig_insights_dir = cs.INSIGHTS_DIR
        self._orig_delta_log = cs.DELTA_LOG
        cs.INSIGHTS_DIR = self.test_insights_dir
        cs.DELTA_LOG = os.path.join(self.test_dir, "delta.md")
    
    def _teardown(self):
        """清理测试数据库"""
        import concept_manager as cm
        import concept_synthesis as cs
        cm.DB_PATH = self._orig_db_path
        cm.CONCEPTS_DIR = self._orig_concepts_dir
        cm.BELIEFS_DIR = self._orig_beliefs_dir
        cs.INSIGHTS_DIR = self._orig_insights_dir
        cs.DELTA_LOG = self._orig_delta_log
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def _log(self, trial, message, outcome=None):
        self.transcript.append({
            "trial": trial,
            "time": datetime.now().isoformat(),
            "message": message,
            "outcome": outcome
        })
    
    def run_all(self):
        print("=" * 60)
        print("🧠 Knowledge Engine 评估")
        print("=" * 60)
        
        self.eval_storage()
        self.eval_retrieval()
        self.eval_association()
        self.eval_confidence()
        self.eval_synthesis()
        self.eval_pruning()
        
        self._print_report()
        self._teardown()
        return self.results
    
    # ─── Trial 1: Storage ───
    
    def eval_storage(self):
        trial = "STORAGE"
        self._log(trial, "开始存储测试")
        
        # Test 1a: 基本存储
        cid = add_concept("测试概念A", "来源A", "上下文A", ["标签1"], "high")
        conn = get_db()
        row = conn.execute("SELECT * FROM concepts WHERE id=?", (cid,)).fetchone()
        pass_1a = row is not None and row["concept"] == "测试概念A"
        self._log(trial, f"1a 基本存储: concept={row['concept'] if row else 'MISSING'}", 
                  "PASS" if pass_1a else "FAIL")
        
        # Test 1b: 文件持久化
        card_file = os.path.join(self.test_concepts_dir, f"{cid}.json")
        pass_1b = os.path.exists(card_file)
        self._log(trial, f"1b 文件持久化: file_exists={pass_1b}", "PASS" if pass_1b else "FAIL")
        
        # Test 1c: 标签存储
        tags = json.loads(row["tags"])
        pass_1c = "标签1" in tags
        self._log(trial, f"1c 标签存储: tags={tags}", "PASS" if pass_1c else "FAIL")
        
        # Test 1d: 重复添加（更新而非重复）
        add_concept("测试概念A", "新来源", "新上下文", ["标签2"], "medium")
        count = conn.execute("SELECT COUNT(*) as cnt FROM concepts WHERE concept='测试概念A'").fetchone()["cnt"]
        pass_1d = count == 1
        self._log(trial, f"1d 去重: count={count}", "PASS" if pass_1d else "FAIL")
        
        # Test 1e: 大量存储
        for i in range(20):
            add_concept(f"批量概念{i}", f"来源{i}", f"上下文{i}", ["批量"], "medium")
        total = conn.execute("SELECT COUNT(*) as cnt FROM concepts").fetchone()["cnt"]
        pass_1e = total >= 21  # 20 + 1 original
        self._log(trial, f"1e 批量存储: total={total}", "PASS" if pass_1e else "FAIL")
        
        conn.close()
        passed = sum([pass_1a, pass_1b, pass_1c, pass_1d, pass_1e])
        self.results.append({"trial": trial, "passed": passed, "total": 5, 
                            "score": passed/5})
    
    # ─── Trial 2: Retrieval ───
    
    def eval_retrieval(self):
        trial = "RETRIEVAL"
        self._log(trial, "开始检索测试")
        
        # Setup: 添加测试数据
        add_concept("分发能力是核心竞争力", "测试", "AI时代稀缺资源", ["创业", "分发"], "high")
        add_concept("品味是最后的差异化", "测试", "AI复制不了品味", ["创业", "产品"], "high")
        add_concept("Agent记忆系统设计", "测试", "持久化是瓶颈", ["AI", "工程"], "medium")
        add_concept("周末去公园散步", "测试", "跟技术无关", ["生活"], "low")
        
        # Test 2a: 精确搜索
        results = search_concepts("分发")
        pass_2a = any("分发" in r["concept"] for r in results)
        self._log(trial, f"2a 精确搜索 '分发': found={len(results)}", 
                  "PASS" if pass_2a else "FAIL")
        
        # Test 2b: 语义相关搜索
        results = search_concepts("创业")
        pass_2b = len(results) >= 2  # 至少找到2个创业相关
        self._log(trial, f"2b 语义搜索 '创业': found={len(results)}", 
                  "PASS" if pass_2b else "FAIL")
        
        # Test 2c: 不相关内容不返回
        results = search_concepts("Agent 记忆")
        has_irrelevant = any("公园" in r["concept"] for r in results)
        pass_2c = not has_irrelevant
        self._log(trial, f"2c 过滤无关: irrelevant_in_results={has_irrelevant}", 
                  "PASS" if pass_2c else "FAIL")
        
        # Test 2d: 标签过滤
        results = search_concepts("", tags=["AI"])
        pass_2d = all("AI" in json.loads(r["tags"]) for r in results)
        self._log(trial, f"2d 标签过滤 'AI': found={len(results)}, all_tagged={pass_2d}", 
                  "PASS" if pass_2d else "FAIL")
        
        # Test 2e: 空查询返回所有
        results = search_concepts("")
        pass_2e = len(results) >= 20
        self._log(trial, f"2e 空查询: found={len(results)}", 
                  "PASS" if pass_2e else "FAIL")
        
        passed = sum([pass_2a, pass_2b, pass_2c, pass_2d, pass_2e])
        self.results.append({"trial": trial, "passed": passed, "total": 5,
                            "score": passed/5})
    
    # ─── Trial 3: Association ───
    
    def eval_association(self):
        trial = "ASSOCIATION"
        self._log(trial, "开始关联测试")
        
        # Test 3a: 基本关联
        ok = link_concepts("分发能力是核心竞争力", "品味是最后的差异化", "related")
        pass_3a = ok is True
        self._log(trial, f"3a 基本关联: ok={ok}", "PASS" if pass_3a else "FAIL")
        
        # Test 3b: 关联持久化
        conn = get_db()
        from_id = _make_id("分发能力是核心竞争力")
        to_id = _make_id("品味是最后的差异化")
        link = conn.execute(
            "SELECT * FROM concept_links WHERE from_concept=? AND to_concept=?",
            (from_id, to_id)
        ).fetchone()
        pass_3b = link is not None
        self._log(trial, f"3b 关联持久化: found={link is not None}", "PASS" if pass_3b else "FAIL")
        
        # Test 3c: 重复关联不报错
        ok2 = link_concepts("分发能力是核心竞争力", "品味是最后的差异化", "related")
        count = conn.execute(
            "SELECT COUNT(*) as cnt FROM concept_links WHERE from_concept=? AND to_concept=?",
            (from_id, to_id)
        ).fetchone()["cnt"]
        pass_3c = count == 1
        self._log(trial, f"3c 去重关联: count={count}", "PASS" if pass_3c else "FAIL")
        
        # Test 3d: 图谱查询
        graph_row = conn.execute(
            "SELECT COUNT(*) as cnt FROM concept_links"
        ).fetchone()["cnt"]
        pass_3d = graph_row >= 1
        self._log(trial, f"3d 图谱查询: links={graph_row}", "PASS" if pass_3d else "FAIL")
        
        conn.close()
        passed = sum([pass_3a, pass_3b, pass_3c, pass_3d])
        self.results.append({"trial": trial, "passed": passed, "total": 4,
                            "score": passed/4})
    
    # ─── Trial 4: Confidence Adjustment ───
    
    def eval_confidence(self):
        trial = "CONFIDENCE"
        self._log(trial, "开始置信度测试")
        
        conn = get_db()
        test_id = _make_id("Agent记忆系统设计")
        
        # Test 4a: 模拟高频率使用
        for i in range(6):
            log_usage(test_id, 'search_hit', f'query_{i}')
        
        # Check usage logged
        hit_count = conn.execute(
            "SELECT COUNT(*) as cnt FROM usage_log WHERE concept_id=? AND action='search_hit'",
            (test_id,)
        ).fetchone()["cnt"]
        pass_4a = hit_count >= 6
        self._log(trial, f"4a 使用记录: hits={hit_count}", "PASS" if pass_4a else "FAIL")
        
        # Test 4b: 自动升级
        # Set concept to 'low' so it can be upgraded
        conn.execute("UPDATE concepts SET confidence='low' WHERE id=?", (test_id,))
        conn.commit()
        # Need to re-log hits after concept change (they persist in usage_log)
        result = auto_adjust_confidence(conn, dry_run=False)
        upgraded = any(test_id == u[0] for u in result['upgrades'])
        pass_4b = upgraded
        self._log(trial, f"4b 自动升级: upgraded={upgraded}, upgrades={len(result['upgrades'])}", 
                  "PASS" if pass_4b else "FAIL")
        
        # Test 4c: 零使用降级
        # 创建一个老概念（修改 created_at 为 30 天前）
        old_id = _make_id("周末去公园散步")
        old_date = (datetime.now() - timedelta(days=20)).isoformat()
        conn.execute("UPDATE concepts SET created_at=? WHERE id=?", (old_date, old_id))
        conn.commit()
        
        result2 = auto_adjust_confidence(conn, dry_run=False)
        downgraded = any(old_id == d[0] for d in result2['downgrades'])
        pass_4c = downgraded
        self._log(trial, f"4c 零使用降级: downgraded={downgraded}", 
                  "PASS" if pass_4c else "FAIL")
        
        # Test 4d: 全局统计
        stats = get_all_usage_stats(days=30)
        pass_4d = test_id in stats and stats[test_id]['search_hit'] >= 6
        self._log(trial, f"4d 全局统计: tracked_concepts={len(stats)}", 
                  "PASS" if pass_4d else "FAIL")
        
        conn.close()
        passed = sum([pass_4a, pass_4b, pass_4c, pass_4d])
        self.results.append({"trial": trial, "passed": passed, "total": 4,
                            "score": passed/4})
    
    # ─── Trial 5: Synthesis ───
    
    def eval_synthesis(self):
        trial = "SYNTHESIS"
        self._log(trial, "开始蒸馏测试")
        
        conn = get_db()
        
        # Test 5a: Reflection — 被挑战的信念
        bid = add_belief("测试信念", "测试推理", "high")
        update_belief(bid, status="challenged", note="被事实推翻了")
        rules = reflection(conn, days=7)
        pass_5a = len(rules) >= 1
        self._log(trial, f"5a Reflection: rules_found={len(rules)}", 
                  "PASS" if pass_5a else "FAIL")
        
        # Test 5b: Generative Synthesis — 主题聚合
        insights = generative_synthesis(conn, days=7)
        themes = [i for i in insights if i["type"] == "generative"]
        pass_5b = len(themes) >= 1
        self._log(trial, f"5b 主题聚合: themes={len(themes)}", 
                  "PASS" if pass_5b else "FAIL")
        
        # Test 5c: 关联发现
        connections = [i for i in insights if i["type"] == "connection"]
        pass_5c = len(connections) >= 1
        self._log(trial, f"5c 关联发现: connections={len(connections)}", 
                  "PASS" if pass_5c else "FAIL")
        
        # Test 5d: 完整蒸馏
        try:
            report = distill(conn, days=7)
            pass_5d = report is not None and len(report) > 0
        except Exception as e:
            pass_5d = False
            self._log(trial, f"5d 完整蒸馏: ERROR {e}", "FAIL")
        self._log(trial, f"5d 完整蒸馏: report_len={len(report) if report else 0}", 
                  "PASS" if pass_5d else "FAIL")
        
        conn.close()
        passed = sum([pass_5a, pass_5b, pass_5c, pass_5d])
        self.results.append({"trial": trial, "passed": passed, "total": 4,
                            "score": passed/4})
    
    # ─── Trial 6: Pruning ───
    
    def eval_pruning(self):
        trial = "PRUNING"
        self._log(trial, "开始清理测试")
        
        conn = get_db()
        
        # Test 6a: 标记废弃
        old_date = (datetime.now() - timedelta(days=35)).isoformat()
        conn.execute(
            "UPDATE concepts SET created_at=?, status='active' WHERE id=?",
            (old_date, _make_id("周末去公园散步"))
        )
        conn.commit()
        
        result = auto_adjust_confidence(conn, dry_run=False)
        deprecated_ids = [d[0] for d in result['deprecations']]
        pass_6a = _make_id("周末去公园散步") in deprecated_ids
        self._log(trial, f"6a 自动废弃: deprecated={len(deprecated_ids)}", 
                  "PASS" if pass_6a else "FAIL")
        
        # Test 6b: 废弃概念不在活跃搜索中
        results = search_concepts("公园", status="active")
        pass_6b = not any("公园" in r["concept"] for r in results)
        self._log(trial, f"6b 废弃隐藏: in_active_results={not pass_6b}", 
                  "PASS" if pass_6b else "FAIL")
        
        # Test 6c: 分层检索排除废弃
        hier = hierarchical_search(conn, recent_k=5)
        active_ids = {r["id"] for r in hier["recent"]}
        park_id = _make_id("周末去公园散步")
        pass_6c = park_id not in active_ids
        self._log(trial, f"6c 分层排除: excluded={pass_6c}", 
                  "PASS" if pass_6c else "FAIL")
        
        conn.close()
        passed = sum([pass_6a, pass_6b, pass_6c])
        self.results.append({"trial": trial, "passed": passed, "total": 3,
                            "score": passed/3})
    
    # ─── Report ───
    
    def _print_report(self):
        print("\n" + "=" * 60)
        print("📊 评估报告")
        print("=" * 60)
        
        total_passed = 0
        total_tests = 0
        
        for r in self.results:
            pct = r["score"] * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            status = "✅" if pct >= 80 else "⚠️" if pct >= 60 else "❌"
            print(f"\n  {status} {r['trial']:12s} {bar} {pct:5.1f}% ({r['passed']}/{r['total']})")
            
            # Show failures
            trial_logs = [t for t in self.transcript if t["trial"] == r["trial"] and t["outcome"] == "FAIL"]
            for log in trial_logs:
                print(f"     ❌ {log['message']}")
            
            total_passed += r["passed"]
            total_tests += r["total"]
        
        overall = total_passed / total_tests * 100 if total_tests > 0 else 0
        print(f"\n{'=' * 60}")
        print(f"  总分: {total_passed}/{total_tests} ({overall:.1f}%)")
        
        if overall >= 90:
            print("  评级: 🏆 优秀 — 系统核心功能健全")
        elif overall >= 75:
            print("  评级: 👍 良好 — 主要功能正常，有改进空间")
        elif overall >= 60:
            print("  评级: ⚠️  及格 — 存在明显问题需要修复")
        else:
            print("  评级: ❌ 不及格 — 需要重大修复")
        
        print(f"{'=' * 60}")
        
        # Save transcript
        transcript_file = os.path.join(self.test_dir, "transcript.json")
        with open(transcript_file, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": self.results,
                "overall_score": overall,
                "transcript": self.transcript
            }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    runner = EvalRunner()
    runner.run_all()
