#!/usr/bin/env python3
# 简单测试脚本

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shared_memory_controller import SharedMemoryController

print("🧪 测试共享记忆同步系统")
print("=" * 50)

# 初始化控制器
controller = SharedMemoryController()

# 测试1: 系统状态
print("\n1. 测试系统状态...")
status = controller.get_status()
print(f"   共享文件夹状态:")
print(f"   - Hermes → OpenClaw: {status['shared_folder']['hermes_to_openclaw']} 个文件")
print(f"   - OpenClaw → Hermes: {status['shared_folder']['openclaw_to_hermes']} 个文件")
print(f"   - 已处理文件: {status['shared_folder']['processed_files']} 个")

# 测试2: Hermes 记忆导出
print("\n2. 测试 Hermes 记忆导出...")
from hermes_exporter import HermesMemoryExporter
exporter = HermesMemoryExporter()
memories = exporter.read_memory_md()
print(f"   读取到 {len(memories['system_memories'])} 条系统记忆")
print(f"   用户配置: {len(memories['user_profile'])} 个字段")

# 测试3: 导出重要记忆
print("\n3. 测试导出重要记忆...")
important_memories = exporter.export_important_memories(min_importance=7)
print(f"   导出 {len(important_memories)} 条重要记忆到共享文件夹")

# 检查导出文件
import glob
export_files = glob.glob(str(exporter.hermes_memory_dir.parent / '.shared-memory' / 'hermes' / 'to_openclaw' / '*.json'))
print(f"   导出文件: {len(export_files)} 个")

print("\n✅ 测试完成!")
print("=" * 50)
print("\n下一步:")
print("1. 运行双向同步: python shared_memory_cli.py sync-bidirectional")
print("2. 清理记忆: python shared_memory_cli.py cleanup")
print("3. 查看详细状态: python shared_memory_cli.py status")