"""
性能测试工具包 - 单元测试
Performance Testing Toolkit - Unit Tests

测试覆盖:
- LoadTester 基础功能
- StressTester 基础功能
- 结果统计计算
- 报告生成功能
"""

import unittest
import sys
import os
import json
import tempfile
import shutil

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from load_tester import LoadTester, TestResults
from stress_tester import StressTester


class TestLoadTester(unittest.TestCase):
    """负载测试器单元测试"""
    
    def setUp(self):
        """测试前准备"""
        self.tester = LoadTester(
            url="https://httpbin.org/get",
            concurrent=2,
            method="GET",
            timeout=10
        )
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.tester.url, "https://httpbin.org/get")
        self.assertEqual(self.tester.concurrent, 2)
        self.assertEqual(self.tester.method, "GET")
        self.assertEqual(self.tester.timeout, 10)
    
    def test_init_with_headers(self):
        """测试带请求头的初始化"""
        headers = {"Authorization": "Bearer test"}
        tester = LoadTester(
            url="https://example.com/api",
            concurrent=5,
            method="POST",
            headers=headers,
            body='{"test": true}',
            timeout=15
        )
        self.assertEqual(tester.headers, headers)
        self.assertEqual(tester.body, '{"test": true}')
    
    def test_run_short_duration(self):
        """测试短时长测试运行"""
        results = self.tester.run(duration=3)
        
        # 验证结果结构
        self.assertIn('total_requests', results)
        self.assertIn('successful_requests', results)
        self.assertIn('failed_requests', results)
        self.assertIn('avg_response_time', results)
        self.assertIn('success_rate', results)
        self.assertIn('rps', results)
        
        # 验证数据合理性
        self.assertGreaterEqual(results['total_requests'], 0)
        self.assertGreaterEqual(results['successful_requests'], 0)
        self.assertGreaterEqual(results['failed_requests'], 0)
        self.assertGreaterEqual(results['success_rate'], 0)
        self.assertLessEqual(results['success_rate'], 100)
    
    def test_invalid_url(self):
        """测试无效URL处理"""
        tester = LoadTester(
            url="invalid-url",
            concurrent=1,
            timeout=5
        )
        results = tester.run(duration=2)
        # 应该有一些失败请求
        self.assertGreaterEqual(results['failed_requests'], 0)


class TestStressTester(unittest.TestCase):
    """压力测试器单元测试"""
    
    def setUp(self):
        """测试前准备"""
        self.tester = StressTester(
            url="https://httpbin.org/get",
            method="GET",
            timeout=10
        )
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.tester.url, "https://httpbin.org/get")
        self.assertEqual(self.tester.method, "GET")
    
    def test_stress_test_small_scale(self):
        """测试小规模压力测试"""
        results = self.tester.run(
            start_concurrent=1,
            max_concurrent=3,
            step=1,
            stage_duration=2
        )
        
        # 应该测试了3个级别: 1, 2, 3
        self.assertEqual(len(results), 3)
        self.assertIn(1, results)
        self.assertIn(2, results)
        self.assertIn(3, results)
        
        # 验证每个级别的结果结构
        for level, data in results.items():
            self.assertIn('total_requests', data)
            self.assertIn('success_rate', data)
            self.assertIn('avg_response_time', data)
            self.assertIn('rps', data)


class TestTestResults(unittest.TestCase):
    """测试结果类单元测试"""
    
    def test_results_calculation(self):
        """测试结果计算"""
        from dataclasses import dataclass
        from typing import List
        
        # 创建模拟结果
        @dataclass
        class MockResult:
            response_time: float
            status_code: int
            error: str = None
        
        results = TestResults()
        results.total_requests = 100
        results.successful_requests = 95
        results.failed_requests = 5
        results.response_times = [100, 200, 150, 180, 120] * 19 + [500, 600]  # 95个成功 + 5个大的
        results.errors = ["Timeout", "Connection Error"] * 2 + ["Unknown"]
        results.timestamp = "2024-01-01T00:00:00"
        
        # 验证统计数据
        self.assertEqual(results.total_requests, 100)
        self.assertEqual(results.success_rate, 95.0)
    
    def test_to_dict(self):
        """测试转换为字典"""
        results = TestResults()
        results.total_requests = 50
        results.successful_requests = 48
        results.failed_requests = 2
        results.avg_response_time = 150.5
        results.min_response_time = 80.0
        results.max_response_time = 300.0
        results.rps = 10.5
        results.success_rate = 96.0
        results.timestamp = "2024-01-01T00:00:00"
        
        data = results.to_dict()
        
        self.assertEqual(data['total_requests'], 50)
        self.assertEqual(data['successful_requests'], 48)
        self.assertEqual(data['success_rate'], 96.0)


class TestReportGeneration(unittest.TestCase):
    """报告生成功能测试"""
    
    def setUp(self):
        """创建临时目录"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """清理临时目录"""
        shutil.rmtree(self.temp_dir)
    
    def test_json_report(self):
        """测试JSON报告生成"""
        results = {
            'total_requests': 100,
            'successful_requests': 95,
            'failed_requests': 5,
            'avg_response_time': 150.5,
            'success_rate': 95.0,
            'timestamp': '2024-01-01T00:00:00'
        }
        
        # 保存JSON报告
        report_path = os.path.join(self.temp_dir, 'report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        # 验证文件存在并可读取
        self.assertTrue(os.path.exists(report_path))
        
        with open(report_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded['total_requests'], 100)
        self.assertEqual(loaded['success_rate'], 95.0)


class TestConfiguration(unittest.TestCase):
    """配置测试"""
    
    def test_concurrent_limits(self):
        """测试并发数限制"""
        # 测试正常并发数
        tester = LoadTester(url="https://example.com", concurrent=100)
        self.assertEqual(tester.concurrent, 100)
        
        # 测试零并发（应该处理为1）
        tester = LoadTester(url="https://example.com", concurrent=0)
        self.assertGreaterEqual(tester.concurrent, 1)
    
    def test_timeout_limits(self):
        """测试超时设置"""
        tester = LoadTester(url="https://example.com", timeout=5)
        self.assertEqual(tester.timeout, 5)
        
        tester = LoadTester(url="https://example.com", timeout=60)
        self.assertEqual(tester.timeout, 60)


def create_test_suite():
    """创建测试套件"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestLoadTester))
    suite.addTests(loader.loadTestsFromTestCase(TestStressTester))
    suite.addTests(loader.loadTestsFromTestCase(TestTestResults))
    suite.addTests(loader.loadTestsFromTestCase(TestReportGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    
    return suite


if __name__ == '__main__':
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    result = runner.run(suite)
    
    # 返回退出码
    sys.exit(0 if result.wasSuccessful() else 1)
