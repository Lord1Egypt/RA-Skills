"""
Test Phase 3 Lint Pipeline
"""
import asyncio
import sys
import importlib.util
from pathlib import Path

# 动态加载 karpathy-lint
scripts_path = Path(__file__).parent / "__init__.py"
spec = importlib.util.spec_from_file_location("lint_scripts", scripts_path)
module = importlib.util.module_from_spec(spec)
sys.modules["lint_scripts"] = module
spec.loader.exec_module(module)

LintPipeline = module.LintPipeline
KnowledgePointParser = module.KnowledgePointParser


async def test():
    print("=== Phase 3 Lint Pipeline Test ===")
    
    # Test Parser first
    print("\n[1] Testing KnowledgePointParser...")
    parser = KnowledgePointParser()
    points = parser.parse_kp_file()
    print(f"    Found {len(points)} knowledge points")
    
    if points:
        print(f"    First point: {points[0].get('title', 'unknown')}")
        print(f"    Tags: {points[0].get('tags', [])}")
        print(f"    Confidence: {points[0].get('confidence', 'unknown')}")
    
    # Test LintPipeline
    print("\n[2] Testing LintPipeline...")
    pipeline = LintPipeline()
    report = await pipeline.run_lint()
    
    print(f"\n[RESULT] Knowledge Points: {report.total_points}")
    print(f"[RESULT] Issues Found: {report.issues_found}")
    
    if report.issues:
        print("\n[ISSUES]")
        for issue in report.issues:
            print(f"  [{issue.severity}] {issue.title}")
            print(f"    {issue.description}")
            if issue.suggestion:
                print(f"    Suggestion: {issue.suggestion}")
    
    # 保存报告
    report_path = pipeline.kp_path / "lint-report.md"
    report_path.write_text(report.to_markdown(), encoding="utf-8")
    print(f"\n[INFO] Report saved to {report_path}")
    
    print("\n=== Phase 3 Test Complete ===")


if __name__ == "__main__":
    asyncio.run(test())
