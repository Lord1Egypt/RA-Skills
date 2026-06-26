"""
快导(KD) Skill - 测试套件
"""

import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from test_config import test_config
from test_excel import test_excel
from test_generator import test_generator
from test_format import test_format

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("快导(KD) Skill 测试套件")
    print("=" * 60)
    
    tests = [
        ("配置管理测试", test_config),
        ("Excel管理测试", test_excel),
        ("脚本生成测试", test_generator),
        ("格式检查测试", test_format)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"开始: {name}")
        print('='*60)
        try:
            test_func()
            results.append((name, "✅ 通过"))
            print(f"✅ {name} 通过")
        except Exception as e:
            results.append((name, f"❌ 失败: {e}"))
            print(f"❌ {name} 失败: {e}")
    
    # 打印测试报告
    print("\n" + "=" * 60)
    print("测试报告")
    print("=" * 60)
    for name, result in results:
        print(f"{name}: {result}")
    
    passed = sum(1 for _, r in results if "通过" in r)
    print(f"\n总计: {passed}/{len(results)} 通过")

if __name__ == "__main__":
    run_all_tests()
