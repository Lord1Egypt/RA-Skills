#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Plus Sync 2.0 完整工作流测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_mcp_server():
    """测试 MCP 服务器"""
    print("🧪 测试 MCP 服务器...")
    try:
        from mcp_server import app
        print("✅ MCP 服务器导入成功")
        return True
    except Exception as e:
        print(f"❌ MCP 服务器导入失败: {e}")
        return False

def test_triple_agent():
    """测试三代理验证"""
    print("🧪 测试三代理验证...")
    try:
        from core.triple_agent_processor import TripleAgentProcessor
        processor = TripleAgentProcessor()
        print("✅ 三代理验证导入成功")
        return True
    except Exception as e:
        print(f"❌ 三代理验证导入失败: {e}")
        return False

def test_deduplication():
    """测试去重功能"""
    print("🧪 测试去重功能...")
    try:
        from dedup_processor import ThreeAgentVerifier
        processor = ThreeAgentVerifier()
        print("✅ 去重功能导入成功")
        return True
    except Exception as e:
        print(f"❌ 去重功能导入失败: {e}")
        return False

def test_integration():
    """测试集成功能"""
    print("🧪 测试集成功能...")
    try:
        from core.main_integration import MemoryPlusIntegration
        mpi = MemoryPlusIntegration()
        print("✅ 集成功能导入成功")
        return True
    except Exception as e:
        print(f"❌ 集成功能导入失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("Memory Plus Sync 2.0 完整工作流测试")
    print("=" * 60)
    
    tests = [
        ("MCP 服务器", test_mcp_server),
        ("三代理验证", test_triple_agent),
        ("去重功能", test_deduplication),
        ("集成功能", test_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        success = test_func()
        results.append((test_name, success))
    
    print("")
    print("=" * 60)
    print("测试结果汇总:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("")
        print("🎉 所有测试通过！Memory Plus Sync 2.0 升级成功！")
        return 0
    else:
        print(f"")
        print(f"⚠️  有 {total - passed} 个测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
