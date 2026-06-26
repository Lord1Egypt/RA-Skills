"""PAO系统自动化测试"""
import sys
from pathlib import Path

# Add project root to path for package imports
_project_root = Path(__file__).parent.parent
sys.path.insert(0, str(_project_root))

def test_imports():
    """测试导入"""
    print('[1] Testing Imports...')
    from src.system_integrator import PAOSystemIntegrator
    from src.skill_manager import SkillManager
    from src.context_awareness import ContextAwareness
    from src.learning_loop import LearningLoop, FeedbackType
    from src.core.memory import MemorySystem
    print('    All imports OK')
    return True

def test_config():
    """测试配置"""
    print('[2] Testing Config...')
    from src.core.config import ConfigManager, PAOConfig
    config = PAOConfig()
    print('    Config OK - Device:', config.device_id)
    return True

def test_skill_manager():
    """测试技能管理"""
    print('[3] Testing Skill Manager...')
    from src.skill_manager import SkillManager, SkillCategory
    import asyncio
    async def run():
        manager = SkillManager()
        await manager.initialize()
        skills = await manager.search_skills('python')
        return len(skills)
    result = asyncio.run(run())
    print('    Skill Manager OK - Found', result, 'skills')
    return True

def test_memory():
    """测试记忆系统"""
    print('[4] Testing Memory System...')
    from src.core.memory import MemorySystem
    import asyncio
    async def run():
        mem = MemorySystem()
        await mem.load()
        mid = await mem.add_memory('test', {'data': 'test'}, priority=2)
        results = await mem.search_memories('test')
        return mid, len(results)
    mid, count = asyncio.run(run())
    print('    Memory OK - Stored', mid[:8], ', Found', count)
    return True

def test_learning_loop():
    """测试学习循环"""
    print('[5] Testing Learning Loop...')
    from src.learning_loop import LearningLoop, FeedbackType
    import asyncio
    async def run():
        loop = LearningLoop()
        await loop.start()
        await loop.submit_feedback(FeedbackType.EXPLICIT, 'test', {}, 8.0, 'good')
        status = await loop.get_learning_status()
        await loop.stop()
        return status['total_feedbacks']
    count = asyncio.run(run())
    print('    Learning Loop OK -', count, 'feedbacks')
    return True

if __name__ == '__main__':
    print('=' * 50)
    print('PAO System Automation Tests')
    print('=' * 50)

    tests = [
        test_imports,
        test_config,
        test_skill_manager,
        test_memory,
        test_learning_loop,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print('    FAILED:', e)
            failed += 1

    print('=' * 50)
    print(f'Results: {passed} passed, {failed} failed')
    print('=' * 50)
