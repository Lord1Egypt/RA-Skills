"""
Debug M-Flow search results format
"""
import asyncio
import sys
import importlib.util
from pathlib import Path

# 加载 M-Flow
mflow_path = Path(__file__).parent.parent.parent / "m_flow"
mflow_skill_path = Path(__file__).parent.parent.parent / "m-flow-memory"
sys.path.insert(0, str(mflow_path))
sys.path.insert(0, str(mflow_skill_path))

spec = importlib.util.spec_from_file_location("mflow_scripts", mflow_skill_path / "scripts" / "__init__.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
MFlowMemory = module.MFlowMemory

async def test():
    print("=== Debug M-Flow Search Results ===")
    
    memory = MFlowMemory(log_level="ERROR")
    
    # 添加测试数据
    test_data = [
        "Machine learning is AI",
        "Deep learning uses neural networks",
        "Python is for data science"
    ]
    for item in test_data:
        await memory.add(item)
    await memory.memorize()
    
    # 搜索
    print("\nTesting search...")
    r = await memory.search("Python", mode="lexical", top_k=5)
    print(f"Result type: {type(r)}")
    print(f"Result len: {len(r) if hasattr(r, '__len__') else 'N/A'}")
    print(f"Result content: {repr(r)[:500]}")
    
    if r:
        print(f"\nFirst item type: {type(r[0])}")
        print(f"First item: {repr(r[0])[:500]}")

if __name__ == "__main__":
    asyncio.run(test())
