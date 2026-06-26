"""
测试所有工作区的连通性
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from task_distributor import TaskDistributor
from src.protocols.task_protocol import WorkerInfo

async def main():
    dist = TaskDistributor("ws_main", "PAO系统")
    
    # 注册所有工作区
    workers = [
        WorkerInfo("ws_aitest", "智能测试1.0", "localhost", 8767, "online", ["ai_skills_testing"]),
        WorkerInfo("ws_dataquery", "数据查询与统计", "localhost", 8768, "online", ["data_query"]),
        WorkerInfo("ws_agent", "通用Agent能力", "localhost", 8769, "online", ["general_agent"]),
    ]
    
    for w in workers:
        dist.register_worker(w)
    
    print("=" * 60)
    print("[TEST] 测试所有工作区连通性")
    print("=" * 60)
    
    # 测试数据查询工作区
    print("\n[1] 测试数据查询与统计工作区...")
    result = await dist.dispatch("echo测试", {"msg": "Hello from PAO"}, workers=["ws_dataquery"], task_type="echo")
    print(f"    状态: {result.results[0].status if result.results else 'N/A'}")
    print(f"    结果: {result.results[0].result if result.results else 'N/A'}")
    
    # 测试通用Agent工作区
    print("\n[2] 测试通用Agent能力工作区...")
    result = await dist.dispatch("echo测试", {"msg": "Hello from PAO"}, workers=["ws_agent"], task_type="echo")
    print(f"    状态: {result.results[0].status if result.results else 'N/A'}")
    print(f"    结果: {result.results[0].result if result.results else 'N/A'}")
    
    # 测试智能测试工作区
    print("\n[3] 测试智能测试1.0工作区...")
    result = await dist.dispatch("echo测试", {"msg": "Hello from PAO"}, workers=["ws_aitest"], task_type="echo")
    print(f"    状态: {result.results[0].status if result.results else 'N/A'}")
    print(f"    结果: {result.results[0].result if result.results else 'N/A'}")
    
    print("\n" + "=" * 60)
    print("[DONE] 连通性测试完成")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())