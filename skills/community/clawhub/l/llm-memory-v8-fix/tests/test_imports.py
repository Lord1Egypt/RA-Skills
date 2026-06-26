#!/usr/bin/env python3
"""
CI/CD 导入测试
快速检查所有核心模块是否可以正常导入

用于 CI/CD 流程中的快速验证
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def test_imports():
    """测试所有核心模块导入"""
    errors = []
    
    # 核心模块列表
    modules = [
        'core.sqlite_ext',
        'core.sqlite_vec',
        'core.vector_ops',
        'core.cpu_optimizer',
        'core.numba_accel',
        'core.cache_optimizer',
        'core.gpu_ops',
        'core.ann',
        'core.quantization',
        'core.hardware_optimize',
        'core.hugepage_manager',
        'core.numa_optimizer',
        'core.cache_aware_scheduler',
        'core.irq_isolator',
        'core.async_ops',
        'core.distributed_search',
    ]
    
    print("=" * 60)
    print("CI/CD 导入测试")
    print("=" * 60)
    print()
    
    for mod in modules:
        try:
            __import__(mod)
            print(f"✅ {mod}")
        except Exception as e:
            print(f"❌ {mod}: {e}")
            errors.append((mod, str(e)))
    
    print()
    print("=" * 60)
    print(f"总计: {len(modules)} 个模块, {len(errors)} 个错误")
    print("=" * 60)
    
    return len(errors) == 0


def test_core_init():
    """测试 core.__init__ 导入"""
    print("\n测试 core.__init__ 导入...")
    try:
        import core
        # 检查关键导出
        assert hasattr(core, 'sqlite3'), "缺少 sqlite3"
        assert hasattr(core, 'connect'), "缺少 connect"
        assert hasattr(core, 'ANNIndex'), "缺少 ANNIndex"
        assert hasattr(core, 'CPUOptimizer'), "缺少 CPUOptimizer"
        print("✅ core 模块导入成功")
        return True
    except Exception as e:
        print(f"❌ core 模块导入失败: {e}")
        return False


def test_ann_classes():
    """测试 ANN 类定义顺序"""
    print("\n测试 ANN 类定义顺序...")
    try:
        from core.ann import ANNIndex, BruteForceANN, IVFIndex, LSHIndex, HNSWIndex
        
        # 检查继承关系
        assert issubclass(BruteForceANN, ANNIndex), "BruteForceANN 不是 ANNIndex 的子类"
        assert issubclass(IVFIndex, ANNIndex), "IVFIndex 不是 ANNIndex 的子类"
        assert issubclass(LSHIndex, ANNIndex), "LSHIndex 不是 ANNIndex 的子类"
        assert issubclass(HNSWIndex, ANNIndex), "HNSWIndex 不是 ANNIndex 的子类"
        
        print("✅ ANN 类定义顺序正确")
        return True
    except Exception as e:
        print(f"❌ ANN 类定义顺序错误: {e}")
        return False


def main():
    """主函数"""
    results = []
    
    results.append(test_imports())
    results.append(test_core_init())
    results.append(test_ann_classes())
    
    print()
    print("=" * 60)
    if all(results):
        print("✅ 所有检查通过")
        return 0
    else:
        print("❌ 部分检查失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
