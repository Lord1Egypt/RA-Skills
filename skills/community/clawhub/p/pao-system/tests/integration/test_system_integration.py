"""系统集成测试"""
import asyncio
import pytest
import sys
sys.path.insert(0, 'src')

from system_integrator import PAOSystemIntegrator, create_pao_system


@pytest.fixture
async def system():
    """PAO系统"""
    system = PAOSystemIntegrator()
    yield system
    await system.stop()


@pytest.mark.asyncio
async def test_system_initialization(system):
    """测试系统初始化"""
    print("\n" + "=" * 60)
    print("测试1: 系统初始化")
    print("=" * 60)

    success = await system.initialize()

    assert success, "系统初始化失败"
    assert system.status.initialized, "系统未标记为已初始化"
    print(f"✅ 设备ID: {system.status.device_id}")
    print(f"✅ 技能数量: {system.status.skills_loaded}")
    print(f"✅ 记忆数量: {system.status.memory_items}")


@pytest.mark.asyncio
async def test_system_start_stop(system):
    """测试系统启动停止"""
    print("\n" + "=" * 60)
    print("测试2: 系统启动/停止")
    print("=" * 60)

    await system.initialize()
    await system.start()
    assert system._running, "系统未标记为运行中"
    print("✅ 系统已启动")

    await system.stop()
    assert not system._running, "系统未标记为已停止"
    print("✅ 系统已停止")


@pytest.mark.asyncio
async def test_skill_operations(system):
    """测试技能操作"""
    print("\n" + "=" * 60)
    print("测试3: 技能操作")
    print("=" * 60)

    await system.initialize()

    # 搜索技能
    skills = await system.search_skills("python")
    print(f"✅ 搜索到 {len(skills)} 个技能")

    # 使用技能
    if skills:
        skill = skills[0]
        result = await system.apply_skill(
            skill.name,
            {"task": "测试任务"},
            8.5,
            "测试反馈"
        )
        print(f"✅ 技能使用结果: {result}")


@pytest.mark.asyncio
async def test_context_operations(system):
    """测试上下文操作"""
    print("\n" + "=" * 60)
    print("测试4: 上下文操作")
    print("=" * 60)

    await system.initialize()

    context = await system.get_current_context()
    print(f"✅ 收集到 {len(context.get('contexts', []))} 种上下文")
    print(f"✅ 识别场景: {context.get('scene')}")


@pytest.mark.asyncio
async def test_memory_operations(system):
    """测试记忆操作"""
    print("\n" + "=" * 60)
    print("测试5: 记忆操作")
    print("=" * 60)

    await system.initialize()

    # 存储记忆
    memory_id = await system.store_memory(
        "test_memory",
        {"content": "测试内容", "timestamp": "2026-04-16"},
        priority=5
    )
    print(f"✅ 存储记忆: {memory_id}")

    # 检索记忆
    memories = await system.retrieve_memories("测试")
    print(f"✅ 检索到 {len(memories)} 条记忆")


@pytest.mark.asyncio
async def test_system_diagnostics(system):
    """测试系统诊断"""
    print("\n" + "=" * 60)
    print("测试6: 系统诊断")
    print("=" * 60)

    await system.initialize()

    diagnostics = await system.run_diagnostics()

    print(f"系统状态: {diagnostics['system']}")
    print(f"组件状态:")
    for name, status in diagnostics["components"].items():
        print(f"  - {name}: {status['status']}")

    assert diagnostics["system"]["initialized"], "系统未初始化"


@pytest.mark.asyncio
async def test_full_workflow():
    """完整工作流测试"""
    print("\n" + "=" * 60)
    print("完整工作流测试")
    print("=" * 60)

    system = PAOSystemIntegrator()

    try:
        # 初始化
        await system.initialize()
        print("✅ 系统初始化完成")

        # 启动
        await system.start()
        print("✅ 系统启动完成")

        # 执行操作
        skills = await system.search_skills("test")
        print(f"✅ 技能搜索: {len(skills)} 个")

        context = await system.get_current_context()
        print(f"✅ 上下文收集: {len(context.get('contexts', []))} 种")

        memory_id = await system.store_memory("workflow_test", {"step": 1})
        print(f"✅ 记忆存储: {memory_id}")

        # 获取状态
        status = system.get_system_status()
        print(f"✅ 系统状态: 初始化={status.initialized}, 运行中={system._running}")

        # 诊断
        diagnostics = await system.run_diagnostics()
        errors = diagnostics.get("errors", [])
        print(f"✅ 诊断完成: {len(errors)} 个错误")

        print("\n" + "=" * 60)
        print("✅ 完整工作流测试通过!")
        print("=" * 60)

    finally:
        await system.stop()
