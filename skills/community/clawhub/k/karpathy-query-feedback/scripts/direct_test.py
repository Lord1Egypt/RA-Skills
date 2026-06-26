"""
Quick test for Phase 1 Pipeline
"""
import asyncio
import sys
import importlib.util
from pathlib import Path

# 动态加载 __init__.py
scripts_path = Path(__file__).parent / "__init__.py"
spec = importlib.util.spec_from_file_location("scripts", scripts_path)
scripts_module = importlib.util.module_from_spec(spec)
sys.modules["scripts"] = scripts_module
spec.loader.exec_module(scripts_module)

QueryFeedbackPipeline = scripts_module.QueryFeedbackPipeline
WikiEntry = scripts_module.WikiEntry

async def test():
    print("=== Phase 1 Test ===")
    
    # Create pipeline
    pipeline = QueryFeedbackPipeline()
    print("[OK] Pipeline created")
    
    # Test WikiEntry
    entry = WikiEntry("test", "Python is a language", ["python"], "2026-04-05")
    print(f"[OK] WikiEntry: {entry.to_markdown_row()}")
    
    # Add test data
    test_data = [
        "Machine learning is AI",
        "Deep learning uses neural networks",
        "Python is for data science"
    ]
    for item in test_data:
        await pipeline.memory.add(item)
    await pipeline.memory.memorize()
    print(f"[OK] Added {len(test_data)} items")
    
    # Query
    result = await pipeline.query_and_save("Python", mode="hybrid", top_k=5)
    print(f"[OK] Query: {result['entries_count']} results")
    if result["saved_path"]:
        print(f"[OK] Saved to: {result['saved_path']}")
    
    print("=== Phase 1 Test Complete ===")

if __name__ == "__main__":
    asyncio.run(test())
