#!/usr/bin/env python3
# Thinking Module Initialization Script
# 首次运行此脚本以初始化思考模块

import sys
import os
from pathlib import Path

# Auto-detect workspace path
if "NEURAL_MEMORY_PATH" in os.environ:
    workspace = os.environ["NEURAL_MEMORY_PATH"]
elif "OPENCLAW_STATE_DIR" in os.environ:
    workspace = os.path.join(os.environ["OPENCLAW_STATE_DIR"], "neural-memory")
else:
    workspace = os.path.join(Path.home(), ".openclaw", "neural-memory")

# Add workspace to Python path
if workspace not in sys.path:
    sys.path.insert(0, workspace)

try:
    from thinking import ThinkingModule

    print("=" * 60)
    print("OpenClaw Neural Memory Initialization / 神经记忆初始化")
    print("=" * 60)
    print(f"Storage path / 存储路径: {workspace}")

    # Create module instance
    thinking = ThinkingModule(base_path=workspace)

    # Build from existing memory (if any)
    thinking.initialize_from_existing_memory()

    # Save initial state
    thinking.save()

    # Show stats
    stats = thinking.get_thinking_stats()
    print("\nInitialization complete! Stats / 初始化完成！统计:")
    print(f"  Total neurons / 神经元总数: {stats['neurons_count']}")
    print(f"  Total synapses / 突触总数: {stats['synapses_count']}")
    print(f"  Protected neurons / 受保护神经元: {stats['protected_neurons_count']}")
    print(f"  Thinking sessions / 思考会话: {stats['thinking_sessions']}")

    # Test thinking
    print("\nTesting thinking / 测试思考功能...")
    test_concept = "test"
    result = thinking.think(test_concept, mode='associative', max_depth=2)

    if result.get('results'):
        print(f"Test success! Query '{test_concept}' found {len(result['results'])} related concepts")
        print("  Top associations / 最强关联:")
        for i, r in enumerate(result['results'][:3], 1):
            print(f"    {i}. {r['neuron'].name} (activation: {r['activation']:.3f})")
    else:
        print("Test: No related concepts found (normal if system just initialized)")
        print("测试：未找到相关概念（如果系统刚初始化，这是正常的）")

    print("\n" + "=" * 60)
    print("Initialization script completed / 初始化脚本执行完毕")
    print("=" * 60)

except ImportError as e:
    print(f"Error: Cannot import thinking module / 错误: 无法导入 thinking 模块: {e}")
    print("Please ensure all files are correctly created / 请确保所有文件已正确创建")
    sys.exit(1)
except Exception as e:
    print(f"Initialization failed / 初始化失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)