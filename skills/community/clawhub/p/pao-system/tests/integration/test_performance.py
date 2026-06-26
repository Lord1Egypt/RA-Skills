"""性能测试"""
import pytest
import asyncio
import time
import psutil
import sys
sys.path.insert(0, 'src')

from skill_manager import SkillManager
from context_awareness import ContextAwareness
from learning_loop import LearningLoop


@pytest.fixture
async def skill_manager():
    """技能管理器"""
    manager = SkillManager()
    await manager.initialize()
    yield manager
    await manager.shutdown()


@pytest.fixture
async def context_awareness():
    """情境感知"""
    awareness = ContextAwareness()
    await awareness.register_default_scenes()
    yield awareness


@pytest.fixture
async def learning_loop():
    """学习循环"""
    loop = LearningLoop()
    await loop.start()
    yield loop
    await loop.stop()


@pytest.mark.asyncio
async def test_skill_search_performance(skill_manager):
    """测试技能搜索性能"""
    start = time.time()

    for _ in range(100):
        await skill_manager.search_skills("python")

    elapsed = time.time() - start
    print(f"\n技能搜索100次耗时: {elapsed:.3f}s")

    assert elapsed < 5.0, "技能搜索性能不达标"


@pytest.mark.asyncio
async def test_context_collection_performance(context_awareness):
    """测试上下文收集性能"""
    start = time.time()

    for _ in range(50):
        await context_awareness.collect_all()

    elapsed = time.time() - start
    print(f"\n上下文收集50次耗时: {elapsed:.3f}s")

    assert elapsed < 3.0, "上下文收集性能不达标"


@pytest.mark.asyncio
async def test_feedback_processing_performance(learning_loop):
    """测试反馈处理性能"""
    start = time.time()

    for i in range(100):
        await learning_loop.submit_feedback(
            "explicit",
            f"skill_{i % 5}",
            {"task": f"task_{i}"},
            8.0 + (i % 2),
            "good"
        )

    elapsed = time.time() - start
    print(f"\n反馈处理100次耗时: {elapsed:.3f}s")

    assert elapsed < 5.0, "反馈处理性能不达标"


def test_memory_usage():
    """测试内存使用"""
    process = psutil.Process()
    mem_info = process.memory_info()

    print(f"\n当前内存使用: {mem_info.rss / 1024 / 1024:.2f} MB")

    # 内存使用应该小于100MB
    assert mem_info.rss / 1024 / 1024 < 100, "内存使用超标"


def test_cpu_usage():
    """测试CPU使用"""
    process = psutil.Process()
    cpu_percent = process.cpu_percent(interval=1)

    print(f"\n当前CPU使用率: {cpu_percent:.1f}%")

    # CPU使用率应该小于10%
    assert cpu_percent < 10, "CPU使用率过高"
