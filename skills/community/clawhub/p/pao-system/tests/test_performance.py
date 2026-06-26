"""性能优化测试"""
import sys
from pathlib import Path

# Add project root to path for package imports
_project_root = Path(__file__).parent.parent
sys.path.insert(0, str(_project_root))

import time
import asyncio
import psutil

def test_performance_monitor():
    """测试性能监控"""
    print('[1] Performance Monitor')
    from src.performance import PerformanceMonitor, timed

    monitor = PerformanceMonitor()
    process = psutil.Process()

    # 模拟操作
    mem_before = process.memory_info().rss / 1024 / 1024
    time.sleep(0.01)
    mem_after = process.memory_info().rss / 1024 / 1024

    monitor.record("test_op", 10.5, mem_before, mem_after)

    avg = monitor.get_average_duration("test_op")
    print(f'    Average duration: {avg:.2f}ms')
    print('    OK')
    return True

def test_cache_manager():
    """测试缓存管理"""
    print('[2] Cache Manager')
    from src.performance import CacheManager

    cache = CacheManager(ttl_seconds=1)

    # 测试缓存
    cache.set("key1", {"data": "test"})
    result = cache.get("key1")
    assert result is not None
    print(f'    Cache hit: {result}')

    # 测试TTL
    time.sleep(1.1)
    result = cache.get("key1")
    assert result is None
    print('    TTL expired: OK')

    # 测试统计
    cache.set("key2", "value")
    cache.get("key2")  # hit
    cache.get("missing")  # miss
    stats = cache.get_stats()
    print(f'    Stats: {stats}')
    print('    OK')
    return True

def test_query_optimizer():
    """测试查询优化"""
    print('[3] Query Optimizer')
    from src.performance import QueryOptimizer

    optimizer = QueryOptimizer()

    # 生成查询键
    key1 = QueryOptimizer.generate_query_key("SELECT * FROM users", {"id": 1})
    key2 = QueryOptimizer.generate_query_key("SELECT * FROM users", {"id": 1})
    key3 = QueryOptimizer.generate_query_key("SELECT * FROM users", {"id": 2})

    assert key1 == key2  # 相同查询应生成相同键
    assert key1 != key3   # 不同参数应生成不同键
    print(f'    Key generation: OK')

    # 测试缓存
    optimizer.cache_query_result(key1, [{"id": 1, "name": "test"}])
    cached = optimizer.get_cached_query(key1)
    assert cached is not None
    print(f'    Query cache: OK')
    print('    OK')
    return True

def test_memory_optimizer():
    """测试内存优化"""
    print('[4] Memory Optimizer')
    from src.performance import MemoryOptimizer

    optimizer = MemoryOptimizer()

    current_mb = optimizer.get_current_memory_mb()
    print(f'    Current memory: {current_mb:.2f}MB')

    optimizer.track_peak()
    peak_mb = optimizer.get_peak_memory_mb()
    print(f'    Peak memory: {peak_mb:.2f}MB')

    # 测试GC建议
    suggested = optimizer.suggest_gc(threshold_mb=1)  # 低阈值触发GC
    print(f'    GC suggested: {suggested}')

    print('    OK')
    return True

def test_timed_decorator():
    """测试计时装饰器"""
    print('[5] Timed Decorator')
    from src.performance import timed

    @timed("test_operation")
    def slow_function():
        time.sleep(0.01)
        return "result"

    result = slow_function()
    assert result == "result"
    print(f'    Decorated function result: {result}')
    print('    OK')
    return True

def test_data_compressor():
    """测试数据压缩"""
    print('[6] Data Compressor')
    from src.performance import DataCompressor

    compressor = DataCompressor()

    original = "  这是一段   测试文本   "
    compressed = compressor.compress(original)
    decompressed = compressor.decompress(compressed)

    assert original.replace("   ", " ").strip() == decompressed.strip()
    print(f'    Compression ratio: {len(compressed)/len(original):.2f}')
    print('    OK')
    return True

async def test_async_timed():
    """测试异步计时"""
    print('[7] Async Timed Decorator')
    from src.performance import timed

    @timed("async_operation")
    async def async_task():
        await asyncio.sleep(0.01)
        return "async_result"

    result = await async_task()
    assert result == "async_result"
    print(f'    Async decorated function result: {result}')
    print('    OK')
    return True

def run_performance_tests():
    """运行所有性能测试"""
    print('=' * 50)
    print('PAO Performance Optimization Tests')
    print('=' * 50)

    tests = [
        test_performance_monitor,
        test_cache_manager,
        test_query_optimizer,
        test_memory_optimizer,
        test_timed_decorator,
        test_data_compressor,
        lambda: asyncio.run(test_async_timed()),
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f'    FAILED: {e}')
            failed += 1

    print('=' * 50)
    print(f'Results: {passed} passed, {failed} failed')
    print('=' * 50)

if __name__ == '__main__':
    run_performance_tests()
