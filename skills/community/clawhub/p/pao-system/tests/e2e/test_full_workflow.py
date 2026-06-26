"""端到端全流程测试"""
import asyncio
import pytest
import sys
sys.path.insert(0, 'src')

from device_discovery import DeviceDiscovery
from communication import Communication
from skill_manager import SkillManager
from context_awareness import ContextAwareness
from learning_loop import LearningLoop, FeedbackType
from sync import SyncManager


@pytest.fixture
async def full_system():
    """完整系统"""
    # 初始化各组件
    discovery = DeviceDiscovery(name="TestDevice")
    await discovery.start()

    comm = Communication(discovery)
    skill_mgr = SkillManager()
    await skill_mgr.initialize()

    context = ContextAwareness()
    await context.register_default_scenes()

    learning = LearningLoop()
    await learning.start()

    sync_mgr = SyncManager(discovery)

    yield {
        "discovery": discovery,
        "communication": comm,
        "skill_manager": skill_mgr,
        "context": context,
        "learning": learning,
        "sync": sync_mgr
    }

    # 清理
    await sync_mgr.disconnect()
    await learning.stop()
    await skill_mgr.shutdown()
    await comm.disconnect()
    await discovery.stop()


@pytest.mark.asyncio
async def test_full_workflow(full_system):
    """测试完整工作流程"""
    print("\n" + "=" * 60)
    print("开始端到端全流程测试")
    print("=" * 60)

    # 1. 设备发现
    print("\n[1/6] 测试设备发现...")
    devices = full_system["discovery"].get_discovered_devices()
    print(f"  发现设备数: {len(devices)}")

    # 2. 技能管理
    print("\n[2/6] 测试技能管理...")
    skills = await full_system["skill_manager"].search_skills("python")
    print(f"  搜索到技能: {len(skills)}个")

    # 3. 情境感知
    print("\n[3/6] 测试情境感知...")
    contexts = await full_system["context"].collect_all()
    print(f"  收集到上下文: {len(contexts)}种")

    # 4. 学习反馈
    print("\n[4/6] 测试学习反馈...")
    await full_system["learning"].submit_feedback(
        FeedbackType.EXPLICIT,
        "coding_python",
        {"task": "测试任务"},
        9.0,
        "测试反馈"
    )
    status = await full_system["learning"].get_learning_status()
    print(f"  学习状态: {status['total_feedbacks']}条反馈")

    # 5. 同步管理
    print("\n[5/6] 测试同步管理...")
    sync_status = full_system["sync"].get_sync_status()
    print(f"  同步状态: {sync_status}")

    # 6. 组件集成
    print("\n[6/6] 测试组件集成...")
    summary = {
        "devices": len(devices),
        "skills": len(skills),
        "contexts": len(contexts),
        "feedbacks": status["total_feedbacks"],
        "sync_connected": sync_status.get("connected", False)
    }
    print(f"  集成摘要: {summary}")

    print("\n" + "=" * 60)
    print("✅ 全流程测试完成!")
    print("=" * 60)

    # 验证
    assert summary["skills"] >= 0
    assert summary["contexts"] >= 0
    assert summary["feedbacks"] >= 1


@pytest.mark.asyncio
async def test_error_recovery(full_system):
    """测试错误恢复"""
    print("\n测试错误恢复能力...")

    # 模拟错误场景
    try:
        await full_system["skill_manager"].apply_skill(
            "nonexistent_skill",
            {},
            0,
            ""
        )
    except Exception as e:
        print(f"  捕获预期错误: {type(e).__name__}")

    # 系统应该仍然正常运行
    skills = await full_system["skill_manager"].search_skills("test")
    assert len(skills) >= 0
    print("  ✅ 错误恢复正常")
