"""
Comprehensive Test: All Karpathy Pipeline Phases
"""
import asyncio
import sys
import importlib.util
from pathlib import Path
import os

# 设置 UTF-8 输出
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 加载所有 pipeline modules
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

# 加载所有 skill __init__.py
skills_dir = Path(__file__).parent.parent.parent

# Phase 1
p1_init = skills_dir / "karpathy-query-feedback" / "scripts" / "__init__.py"
p1 = load_module("karpathy_query_feedback", p1_init)

# Phase 2
p2_init = skills_dir / "karpathy-compile" / "scripts" / "__init__.py"
p2 = load_module("karpathy_compile", p2_init)

# Phase 3
p3_init = skills_dir / "karpathy-lint" / "scripts" / "__init__.py"
p3 = load_module("karpathy_lint", p3_init)

# Phase 4
p4_init = skills_dir / "dual-retrieval" / "scripts" / "__init__.py"
p4 = load_module("dual_retrieval", p4_init)

QueryFeedbackPipeline = p1.QueryFeedbackPipeline
CompilePipeline = p2.CompilePipeline
LintPipeline = p3.LintPipeline
DualRetrievalPipeline = p4.DualRetrievalPipeline


async def test_phase1():
    """Phase 1: Query → Wiki回流"""
    print("\n" + "="*60)
    print("Phase 1: karpathy-query-feedback (Query → Wiki)")
    print("="*60)
    
    pipeline = QueryFeedbackPipeline()
    
    # 测试查询
    query = "python programming language"
    print(f"\n[Query] {query}")
    
    result = await pipeline.query_and_save(query, mode="lexical", top_k=3)
    
    print(f"[Results] {len(result.get('entries', []))} entries")
    if result.get('wiki_file'):
        print(f"[Wiki] Saved to: {result['wiki_file']}")
    
    return result


async def test_phase2():
    """Phase 2: Wiki → Knowledge Points"""
    print("\n" + "="*60)
    print("Phase 2: karpathy-compile (Wiki → Knowledge Points)")
    print("="*60)
    
    pipeline = CompilePipeline()
    
    # 使用上面 Phase 1 保存的 wiki
    wiki_file = Path(__file__).parent.parent.parent / "knowledge" / "wiki" / "wiki-2026-04-05.md"
    
    if wiki_file.exists():
        print(f"\n[Wiki File] {wiki_file}")
        result = await pipeline.compile_wiki(wiki_file)
        print(f"[Knowledge Points] {len(result.get('knowledge_points', []))} generated")
        if result.get('output_file'):
            print(f"[Output] Saved to: {result['output_file']}")
        return result
    else:
        print(f"[WARN] Wiki file not found: {wiki_file}")
        return {}


async def test_phase3():
    """Phase 3: Lint (Quality Check)"""
    print("\n" + "="*60)
    print("Phase 3: karpathy-lint (Quality Check)")
    print("="*60)
    
    pipeline = LintPipeline()
    
    # 使用上面 Phase 2 保存的 knowledge points
    kp_file = Path(__file__).parent.parent.parent / "knowledge" / "knowledge-points" / "knowledge-points-2026-04-05.md"
    
    if kp_file.exists():
        print(f"\n[Knowledge Points File] {kp_file}")
        report = await pipeline.run_lint(kp_file)
        print(f"[Issues Found] {report.get('total_issues', 0)}")
        print(f"[Knowledge Points] {report.get('total_knowledge_points', 0)}")
        print(f"[Health] {report.get('health_score', 'N/A')}")
        return report
    else:
        print(f"[WARN] Knowledge points file not found: {kp_file}")
        return {}


async def test_phase4():
    """Phase 4: Dual Retrieval (M-Flow + QMD)"""
    print("\n" + "="*60)
    print("Phase 4: dual-retrieval (M-Flow + QMD)")
    print("="*60)
    
    pipeline = DualRetrievalPipeline(merge_strategy="score_weighted")
    
    # QMD 统计
    qmd_stats = pipeline.qmd_searcher.get_stats()
    print(f"\n[QMD] {qmd_stats['document_count']} docs, {qmd_stats['collection_count']} collections")
    
    # 测试查询
    query = "python programming"
    print(f"\n[Query] {query}")
    
    result = await pipeline.search(query, mflow_top_k=3, qmd_top_k=5, final_top_k=5)
    
    print(f"[M-Flow] {len(result.mflow_results)} results")
    print(f"[QMD] {len(result.qmd_results)} results")
    print(f"[Merged] {len(result.merged_results)} results")
    
    return result


async def main():
    print("="*60)
    print("Karpathy 4-Phase Pipeline - Comprehensive Test")
    print("="*60)
    
    results = {}
    
    # Phase 1
    try:
        results['phase1'] = await test_phase1()
    except Exception as e:
        print(f"[ERROR] Phase 1 failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Phase 2
    try:
        results['phase2'] = await test_phase2()
    except Exception as e:
        print(f"[ERROR] Phase 2 failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Phase 3
    try:
        results['phase3'] = await test_phase3()
    except Exception as e:
        print(f"[ERROR] Phase 3 failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Phase 4
    try:
        results['phase4'] = await test_phase4()
    except Exception as e:
        print(f"[ERROR] Phase 4 failed: {e}")
        import traceback
        traceback.print_exc()
    
    # 汇总
    print("\n" + "="*60)
    print("Pipeline Test Summary")
    print("="*60)
    print(f"Phase 1 (Query → Wiki): {'PASS' if results.get('phase1') else 'FAIL'}")
    print(f"Phase 2 (Wiki → KPs): {'PASS' if results.get('phase2') else 'FAIL'}")
    print(f"Phase 3 (Lint): {'PASS' if results.get('phase3') else 'FAIL'}")
    print(f"Phase 4 (Dual Retrieval): {'PASS' if results.get('phase4') else 'FAIL'}")
    
    print("\n=== All Tests Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
