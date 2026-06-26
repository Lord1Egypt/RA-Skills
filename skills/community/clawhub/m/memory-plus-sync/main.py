#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Plus Sync - 兼容层入口
版本: 2.0.0

提供向后兼容性，支持原有命令行接口
"""

import sys
import os
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Memory Plus Sync 工具 - 版本 2.0.0")
        print("用法: python main.py <命令> [参数]")
        print("")
        print("命令:")
        print("  sync          - 同步多渠道消息")
        print("  monitor       - 监控记忆系统")
        print("  health        - 健康检查")
        print("  mcp           - 启动 MCP 服务器")
        print("  test          - 运行测试")
        print("")
        print("示例:")
        print("  python main.py sync --channels feishu --hours 2")
        print("  python main.py mcp --host 0.0.0.0 --port 8000")
        return
    
    command = sys.argv[1]
    
    if command == "sync":
        from memory_plus import MemoryPlus
        mp = MemoryPlus()
        if mp.connect():
            print("✅ 同步功能已集成到 MCP 服务器")
            print("请使用 MCP 服务器进行记忆操作")
            mp.close()
    
    elif command == "monitor":
        from monitor import MemoryMonitor
        monitor = MemoryMonitor()
        monitor.run_once()
    
    elif command == "health":
        # 简单的健康检查
        print("🏥 执行健康检查...")
        try:
            from memory_plus import MemoryPlus
            mp = MemoryPlus()
            if mp.connect():
                print("✅ 数据库连接正常")
                mp.close()
            else:
                print("❌ 数据库连接失败")
        except Exception as e:
            print(f"⚠️  健康检查异常: {e}")
        
        print("✅ 基础功能检查完成")
    
    elif command == "mcp":
        # 启动 MCP 服务器
        os.system(f"python {Path(__file__).parent}/mcp_server.py {' '.join(sys.argv[2:])}")
    
    elif command == "test":
        # 运行测试
        test_script = Path(__file__).parent / "test_full_workflow.py"
        if test_script.exists():
            os.system(f"python {test_script}")
        else:
            print("⚠️  测试脚本未找到")
    
    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
