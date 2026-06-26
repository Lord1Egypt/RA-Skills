"""
限流器测试
"""

import unittest
import time
import threading
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/market-data-hub/src')

from limiter import TokenBucket


class TestTokenBucket(unittest.TestCase):
    """TokenBucket限流器测试"""
    
    def test_init(self):
        """测试初始化"""
        bucket = TokenBucket(rate=1.0, capacity=10)
        
        self.assertEqual(bucket.rate, 1.0)
        self.assertEqual(bucket.capacity, 10)
        self.assertEqual(bucket.tokens, 10)
    
    def test_acquire_success(self):
        """测试成功获取令牌"""
        bucket = TokenBucket(rate=10.0, capacity=5)
        
        # 应该能获取5个
        for _ in range(5):
            self.assertTrue(bucket.acquire())
    
    def test_acquire_fail(self):
        """测试获取令牌失败"""
        bucket = TokenBucket(rate=0.1, capacity=2)
        
        # 获取2个
        self.assertTrue(bucket.acquire())
        self.assertTrue(bucket.acquire())
        
        # 第三个应该失败
        self.assertFalse(bucket.acquire())
    
    def test_token_refill(self):
        """测试令牌补充"""
        bucket = TokenBucket(rate=10.0, capacity=5)
        
        # 消耗所有令牌
        for _ in range(5):
            bucket.acquire()
        
        self.assertFalse(bucket.acquire())
        
        # 等待令牌补充
        time.sleep(0.3)  # 等待补充约3个令牌
        
        # 应该能获取到补充的令牌
        self.assertTrue(bucket.acquire())
    
    def test_multiple_tokens(self):
        """测试一次获取多个令牌"""
        bucket = TokenBucket(rate=10.0, capacity=10)
        
        # 一次性获取5个
        self.assertTrue(bucket.acquire(tokens=5))
        
        # 剩余5个
        self.assertTrue(bucket.acquire(tokens=5))
        
        # 没有剩余
        self.assertFalse(bucket.acquire())
    
    def test_get_available_tokens(self):
        """测试获取可用令牌数"""
        bucket = TokenBucket(rate=10.0, capacity=10)
        
        # 初始状态
        self.assertEqual(bucket.get_available_tokens(), 10)
        
        # 消耗3个
        bucket.acquire(tokens=3)
        # 使用近似相等，因为令牌是浮点数
        self.assertAlmostEqual(bucket.get_available_tokens(), 7, places=1)
    
    def test_reset(self):
        """测试重置"""
        bucket = TokenBucket(rate=10.0, capacity=10)
        
        # 消耗令牌
        for _ in range(5):
            bucket.acquire()
        
        # 重置
        bucket.reset()
        
        # 应该回到满状态
        self.assertEqual(bucket.get_available_tokens(), 10)
    
    def test_thread_safety(self):
        """测试线程安全"""
        bucket = TokenBucket(rate=1000.0, capacity=100)
        results = []
        
        def acquire_tokens():
            for _ in range(10):
                results.append(bucket.acquire())
                time.sleep(0.001)
        
        # 启动多个线程
        threads = [threading.Thread(target=acquire_tokens) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # 验证结果
        self.assertEqual(len(results), 50)
        # 前100个应该都是True（容量是100）
        true_count = sum(results)
        self.assertGreaterEqual(true_count, 50)  # 因为rate很高，应该都能成功


if __name__ == '__main__':
    unittest.main(verbosity=2)
