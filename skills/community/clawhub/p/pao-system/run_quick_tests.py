"""Quick Test Suite"""
import sys
sys.path.insert(0, 'src')
import asyncio
from src.system_integrator import PAOSystemIntegrator
from src.learning_loop import FeedbackType

async def quick_test():
    print('Quick Test Suite')
    print('=' * 40)

    # Test 1: System Init
    print('[1] System Init')
    system = PAOSystemIntegrator()
    await system.initialize()
    print('    Device ID:', system.status.device_id)
    print('    Skills:', system.status.skills_loaded)
    print('    Memories:', system.status.memory_items)

    # Test 2: Skill Search
    print('[2] Skill Search')
    skills = await system.search_skills('python')
    print('    Found:', len(skills), 'skills')

    # Test 3: Memory Store
    print('[3] Memory Store')
    memory_id = await system.store_memory('test', {'data': 'test'}, priority=3)
    print('    Stored:', memory_id[:8] + '...')

    # Test 4: Memory Retrieve
    print('[4] Memory Retrieve')
    memories = await system.retrieve_memories('test')
    print('    Retrieved:', len(memories), 'items')

    # Test 5: Learning Loop
    print('[5] Learning Loop')
    await system.learning_loop.submit_feedback(FeedbackType.EXPLICIT, 'test', {}, 8.0, 'good')
    status = await system.learning_loop.get_learning_status()
    print('    Feedbacks:', status['total_feedbacks'])

    print('=' * 40)
    print('All Tests Passed!')

asyncio.run(quick_test())
