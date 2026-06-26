#!/usr/bin/env python3
"""
LLM Memory Integration - 自动化测试套件
测试所有核心模块的导入和基本功能

运行方式：
    python3 tests/test_all.py
    pytest tests/test_all.py -v
"""

import sys
import os
import unittest
from pathlib import Path

# 添加 src 目录到路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


class TestModuleImports(unittest.TestCase):
    """测试所有核心模块是否可以正常导入"""
    
    def test_sqlite_ext_import(self):
        """测试 sqlite_ext 模块导入"""
        from core import sqlite_ext
        self.assertTrue(hasattr(sqlite_ext, 'connect'))
        self.assertTrue(hasattr(sqlite_ext, 'print_sqlite_status'))
    
    def test_sqlite_vec_import(self):
        """测试 sqlite_vec 模块导入"""
        from core import sqlite_vec
        self.assertTrue(hasattr(sqlite_vec, 'connect'))
        self.assertTrue(hasattr(sqlite_vec, 'is_vec_available'))
    
    def test_vector_ops_import(self):
        """测试 vector_ops 模块导入"""
        from core import vector_ops
        self.assertTrue(hasattr(vector_ops, 'VectorOps'))
        self.assertTrue(hasattr(vector_ops, 'cosine_similarity'))
    
    def test_ann_import(self):
        """测试 ann 模块导入"""
        from core import ann
        self.assertTrue(hasattr(ann, 'ANNIndex'))
        self.assertTrue(hasattr(ann, 'BruteForceANN'))
        self.assertTrue(hasattr(ann, 'IVFIndex'))
        self.assertTrue(hasattr(ann, 'LSHIndex'))
        self.assertTrue(hasattr(ann, 'HNSWIndex'))
        self.assertTrue(hasattr(ann, 'create_ann_index'))
    
    def test_cpu_optimizer_import(self):
        """测试 cpu_optimizer 模块导入"""
        from core import cpu_optimizer
        self.assertTrue(hasattr(cpu_optimizer, 'CPUOptimizer'))
        self.assertTrue(hasattr(cpu_optimizer, 'get_optimizer'))
    
    def test_hardware_optimize_import(self):
        """测试 hardware_optimize 模块导入"""
        from core import hardware_optimize
        self.assertTrue(hasattr(hardware_optimize, 'HardwareOptimizer'))
        self.assertTrue(hasattr(hardware_optimize, 'AMXAccelerator'))
    
    def test_hugepage_manager_import(self):
        """测试 hugepage_manager 模块导入"""
        from core import hugepage_manager
        self.assertTrue(hasattr(hugepage_manager, 'HugePageManager'))
    
    def test_numa_optimizer_import(self):
        """测试 numa_optimizer 模块导入"""
        from core import numa_optimizer
        self.assertTrue(hasattr(numa_optimizer, 'NUMATopology'))
        self.assertTrue(hasattr(numa_optimizer, 'NUMAOptimizer'))
        self.assertTrue(hasattr(numa_optimizer, 'check_numa_status'))
    
    def test_cache_aware_scheduler_import(self):
        """测试 cache_aware_scheduler 模块导入"""
        from core import cache_aware_scheduler
        self.assertTrue(hasattr(cache_aware_scheduler, 'CacheTopology'))
        self.assertTrue(hasattr(cache_aware_scheduler, 'CacheAwareScheduler'))
        self.assertTrue(hasattr(cache_aware_scheduler, 'check_cas_status'))
    
    def test_irq_isolator_import(self):
        """测试 irq_isolator 模块导入"""
        from core import irq_isolator
        self.assertTrue(hasattr(irq_isolator, 'IRQTopology'))
        self.assertTrue(hasattr(irq_isolator, 'IRQIsolator'))
        self.assertTrue(hasattr(irq_isolator, 'check_irq_status'))
    
    def test_fma_accelerator_import(self):
        """测试 fma_accelerator 模块导入"""
        from core import fma_accelerator
        self.assertTrue(hasattr(fma_accelerator, 'FMADetector'))
        self.assertTrue(hasattr(fma_accelerator, 'FMAAccelerator'))
        self.assertTrue(hasattr(fma_accelerator, 'check_fma_status'))
    
    def test_quantization_import(self):
        """测试 quantization 模块导入"""
        from core import quantization
        self.assertTrue(hasattr(quantization, 'INT8Quantizer'))
        self.assertTrue(hasattr(quantization, 'FP16Quantizer'))
    
    def test_all_core_import(self):
        """测试从 core 导入所有模块"""
        from core import (
            sqlite3, connect, get_vec_version, is_vec_available,
            VectorOps, ANNIndex, BruteForceANN, LSHIndex, HNSWIndex, IVFIndex,
            CPUOptimizer, HardwareOptimizer, HugePageManager,
            NUMAOptimizer, CacheAwareScheduler, IRQIsolator
        )
        # 如果导入成功，测试通过
        self.assertTrue(True)


class TestANNFunctionality(unittest.TestCase):
    """测试 ANN 模块功能"""
    
    def test_brute_force_ann(self):
        """测试暴力搜索 ANN"""
        import numpy as np
        from core.ann import BruteForceANN
        
        # 创建测试数据
        vectors = np.random.randn(100, 128).astype(np.float32)
        query = np.random.randn(128).astype(np.float32)
        
        # 构建索引
        index = BruteForceANN(dim=128)
        index.build(vectors)
        
        # 搜索
        ids, scores = index.search(query, k=10)
        
        self.assertEqual(len(ids), 10)
        self.assertEqual(len(scores), 10)
    
    def test_create_ann_index_auto(self):
        """测试自动选择 ANN 算法"""
        import numpy as np
        from core.ann import create_ann_index
        
        vectors = np.random.randn(1000, 128).astype(np.float32)
        query = np.random.randn(128).astype(np.float32)
        
        # 自动选择
        index = create_ann_index(vectors, algorithm='auto')
        ids, scores = index.search(query, k=5)
        
        self.assertEqual(len(ids), 5)


class TestVectorOps(unittest.TestCase):
    """测试向量操作功能"""
    
    def test_cosine_similarity(self):
        """测试余弦相似度"""
        import numpy as np
        from core.vector_ops import cosine_similarity
        
        v1 = np.array([1, 0, 0], dtype=np.float32)
        v2 = np.array([1, 0, 0], dtype=np.float32)
        v3 = np.array([0, 1, 0], dtype=np.float32)
        
        # 相同向量
        sim1 = cosine_similarity(v1, v2)
        self.assertAlmostEqual(sim1, 1.0, places=5)
        
        # 正交向量
        sim2 = cosine_similarity(v1, v3)
        self.assertAlmostEqual(sim2, 0.0, places=5)


class TestSystemOptimizers(unittest.TestCase):
    """测试系统级优化器"""
    
    def test_numa_status(self):
        """测试 NUMA 状态检查"""
        from core.numa_optimizer import check_numa_status
        
        status = check_numa_status()
        self.assertIn('topology', status)
        self.assertIn('optimization', status)
    
    def test_cas_status(self):
        """测试 CAS 状态检查"""
        from core.cache_aware_scheduler import check_cas_status
        
        status = check_cas_status()
        self.assertIn('topology', status)
        self.assertIn('kernel_params', status)
    
    def test_irq_status(self):
        """测试 IRQ 状态检查"""
        from core.irq_isolator import check_irq_status
        
        status = check_irq_status()
        self.assertIn('topology', status)
        self.assertIn('isolation_plan', status)
    
    def test_hugepage_status(self):
        """测试大页内存状态检查"""
        from core.hugepage_manager import HugePageManager
        
        manager = HugePageManager()
        stats = manager.get_stats()
        
        self.assertIn('supported', stats)
        self.assertIn('total_pages', stats)
    
    def test_fma_status(self):
        """测试 FMA 状态检查"""
        from core.fma_accelerator import check_fma_status
        
        status = check_fma_status()
        self.assertIn('detection', status)
        self.assertIn('optimization', status)
        self.assertIn('fma3', status['detection'])
        self.assertIn('fma4', status['detection'])
    
    def test_kunpeng_status(self):
        """测试鲲鹏状态检查"""
        from core.kunpeng_optimizer import check_kunpeng_status
        
        status = check_kunpeng_status()
        self.assertIn('detection', status)
        self.assertIn('optimization', status)
        self.assertIn('is_arm64', status['detection'])
        self.assertIn('is_kunpeng', status['detection'])


class TestSQLiteImplementations(unittest.TestCase):
    """测试 SQLite 实现选择"""
    
    def test_detect_implementations(self):
        """测试 SQLite 实现检测"""
        from core.sqlite_ext import detect_sqlite_implementations
        
        implementations = detect_sqlite_implementations()
        self.assertIsInstance(implementations, dict)
        # 至少应该有标准库 sqlite3
        self.assertIn('sqlite3', implementations)
    
    def test_get_best_sqlite(self):
        """测试获取最优 SQLite 实现"""
        from core.sqlite_ext import get_best_sqlite
        
        module, info = get_best_sqlite()
        self.assertIsNotNone(module)
        self.assertIn('description', info)
        self.assertIn('supports_extension', info)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestModuleImports))
    suite.addTests(loader.loadTestsFromTestCase(TestANNFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestVectorOps))
    suite.addTests(loader.loadTestsFromTestCase(TestSystemOptimizers))
    suite.addTests(loader.loadTestsFromTestCase(TestSQLiteImplementations))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 60)
    print("LLM Memory Integration - 自动化测试")
    print("=" * 60)
    print()
    
    success = run_tests()
    
    print()
    print("=" * 60)
    if success:
        print("✅ 所有测试通过")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
