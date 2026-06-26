"""
调用智能测试1.0工作区执行AI Skills Testing验收PAO系统
"""
import asyncio
import sys
import os
from pathlib import Path

# 添加项目路径（使用相对路径定位）
_project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(_project_root))

# 获取Skill目录的相对路径
SKILL_DIR = Path(__file__).parent.resolve()

from task_distributor import TaskDistributor
from src.protocols.task_protocol import WorkerInfo

async def main():
    # 创建分发器
    dist = TaskDistributor("ws_main", "PAO系统")
    
    # 注册智能测试1.0工作区（目标工作区）
    dist.register_worker(WorkerInfo(
        ws_id="ws_aitest",
        ws_name="智能测试1.0",
        host="localhost",
        port=8767,
        status="online",
        capabilities=["ai_skills_testing"]
    ))
    
    print("=" * 60)
    print("[CALL] 正在向智能测试1.0发送AI Skills Testing任务...")
    print("   目标工作区: ws_aitest (智能测试 1.0)")
    print("   任务: 验收 PAO 系统")
    print("=" * 60)
    
    # 分发AI Testing任务（使用动态获取的路径）
    result = await dist.dispatch(
        task_action="AI Skills Testing - 验收PAO系统",
        task_params={
            "skill_path": str(SKILL_DIR),
            "skill_name": "pao",
            "test_type": "full"
        },
        workers=["ws_aitest"],
        task_type="ai_test",
        priority=8
    )
    
    print("\n" + "=" * 60)
    print("[RESULT] 任务执行结果")
    print("=" * 60)
    print(f"任务ID: {result.task_id}")
    print(f"任务动作: {result.task_action}")
    print(f"总工作区数: {result.total_workers}")
    print(f"成功: {result.completed_count}")
    print(f"失败: {result.failed_count}")
    
    for r in result.results:
        print(f"\n--- {r.worker_name} ({r.worker_ws}) ---")
        print(f"状态: {r.status}")
        if r.error:
            print(f"错误: {r.error}")
        if r.result:
            print(f"结果: {r.result}")
    
    print("\n[SUMMARY] 聚合结果:")
    print(result.aggregated_result)

if __name__ == "__main__":
    asyncio.run(main())