#!/usr/bin/env python3
"""
快速导入测试
确保所有核心模块可以正常导入
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试导入"""
    modules = [
        "src.core.config",
        "src.core.device",
        "src.core.discovery",
        "src.core.memory",
        "src.core.storage",
        "src.core.sync",
        "src.protocols.communication",
        "src.protocols.websocket_server",
        "src.protocols.websocket_client"
    ]
    
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"[OK] {module_name}")
        except ImportError as e:
            print(f"[FAIL] {module_name}: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("=== PAO 系统模块导入测试 ===\n")
    
    success = test_imports()
    
    print()
    if success:
        print("[OK] 所有模块导入成功！")
        sys.exit(0)
    else:
        print("[FAIL] 部分模块导入失败")
        sys.exit(1)