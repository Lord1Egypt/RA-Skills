"""
End-to-End Test: Karpathy 4-Phase Pipeline
"""
import asyncio
import sys
import importlib.util
from pathlib import Path
import os
import io

# 设置 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

skills_dir = Path(__file__).parent.parent.parent

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

# 加载所有模块
p1 = load_module("karpathy_query_feedback", skills_dir / "karpathy-query-feedback" / "scripts" / "__init__.py")
p2 = load_module("karpathy_compile", skills_dir / "karpathy-compile" / "scripts" / "__init__.py")
p3 = load_module("karpathy_lint", skills_dir / "karpathy-lint" / "scripts" / "__init__.py")
p4 = load_module("dual_retrieval", skills_dir / "dual-retrieval" / "scripts" / "__init__.py")

QueryFeedbackPipeline = p1.QueryFeedbackPipeline
CompilePipeline = p2.CompilePipeline
LintPipeline = p3.LintPipeline
DualRetrievalPipeline = p4.DualRetrievalPipeline


async def run_e2e_test():
    """完整端到端测试"""
    print("="*60)
    print("Karpathy 4-Phase Pipeline End-to-End Test")
    print("="*60)
    
    results = {}
    test_query = "openclaw memory system"
    
    # Phase 1: Query → Wiki
    print("\n[Phase 1] Query → Wiki")
    print("-"*40)
    try:
        p1_pipeline = QueryFeedbackPipeline()
        p1_result = await p1_pipeline.query_and_save(test_query, mode="lexical", top_k=3)
        entries = p1_result.get('entries', [])
        print(f"  ✅ Generated {len(entries)} wiki entries")
        if p1_result.get('wiki_file'):
            print(f"  📄 Wiki file: {p1_result['wiki_file']}")
        results['phase1'] = 'PASS'
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        results['phase1'] = 'FAIL'
        return results
    
    # Phase 2: Wiki → Knowledge Points
    print("\n[Phase 2] Wiki → Knowledge Points")
    print("-"*40)
    try:
        p2_pipeline = CompilePipeline()
        kps = await p2_pipeline.compile(max_entries_per_point=3, min_entries_for_distillation=1)
        print(f"  ✅ Generated {len(kps)} knowledge points")
        for kp in kps:
            print(f"     - {kp.title} (confidence: {kp.confidence})")
        results['phase2'] = 'PASS'
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        results['phase2'] = 'FAIL'
    
    # Phase 3: Lint
    print("\n[Phase 3] Quality Check (Lint)")
    print("-"*40)
    try:
        p3_pipeline = LintPipeline()
        # 获取最新的 knowledge points 文件
        kp_dir = skills_dir / "knowledge" / "knowledge-points"
        kp_files = list(kp_dir.glob("knowledge-points-*.md"))
        if kp_files:
            latest_kp = max(kp_files, key=lambda p: p.stat().st_mtime)
            report = p3_pipeline.run_lint(latest_kp)
            print(f"  ✅ Lint completed")
            print(f"     - Issues: {report.get('total_issues', 0)}")
            print(f"     - Knowledge Points: {report.get('total_knowledge_points', 0)}")
            print(f"     - Health: {report.get('health_score', 'N/A')}")
            results['phase3'] = 'PASS'
        else:
            print(f"  ⚠️ No knowledge points file found")
            results['phase3'] = 'SKIP'
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        results['phase3'] = 'FAIL'
    
    # Phase 4: Dual Retrieval
    print("\n[Phase 4] Dual Retrieval (M-Flow + QMD)")
    print("-"*40)
    try:
        p4_pipeline = DualRetrievalPipeline(merge_strategy="score_weighted")
        qmd_stats = p4_pipeline.qmd_searcher.get_stats()
        print(f"  📊 QMD: {qmd_stats['document_count']} docs, {qmd_stats['collection_count']} collections")
        
        # 用同一查询测试检索
        p4_result = await p4_pipeline.search(test_query, mflow_top_k=3, qmd_top_k=5, final_top_k=5)
        print(f"  ✅ Retrieval completed")
        print(f"     - M-Flow: {len(p4_result.mflow_results)} results")
        print(f"     - QMD: {len(p4_result.qmd_results)} results")
        print(f"     - Merged: {len(p4_result.merged_results)} results")
        results['phase4'] = 'PASS'
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        results['phase4'] = 'FAIL'
    
    # 汇总
    print("\n" + "="*60)
    print("E2E Test Summary")
    print("="*60)
    for phase, status in results.items():
        icon = "✅" if status == "PASS" else ("⚠️" if status == "SKIP" else "❌")
        print(f"  {icon} {phase.upper()}: {status}")
    
    all_pass = all(s == "PASS" for s in results.values())
    print(f"\n{'🎉 ALL PHASES PASSED!' if all_pass else '⚠️ SOME PHASES FAILED'}")
    
    return results


if __name__ == "__main__":
    asyncio.run(run_e2e_test())
