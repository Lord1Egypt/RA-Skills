#!/usr/bin/env python3
"""Quick initialization for Neural Memory / 神经记忆快速初始化"""

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

# Force utf-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from thinking import ThinkingModule

print("Initializing neural memory (quick mode) / 正在初始化神经记忆（快速模式）...")
print(f"Storage path / 存储路径: {workspace}")

thinking = ThinkingModule(base_path=workspace)

# Load neurons only, don't create initial synapse connections
thinking.storage._load_neurons()
print(f"Loaded / 已加载 {len(thinking.storage.get_all_neurons())} neurons / 个神经元")

# Create synapses from KnowledgeConnections if available
knowledge_file = os.path.join(thinking.storage.base_path, "memory_long_term", "KnowledgeConnections.md")
if os.path.exists(knowledge_file):
    print("Creating synapses from KnowledgeConnections / 正在从 KnowledgeConnections 创建突触...")
    synapse_count = thinking.synapse_manager.initialize_from_knowledge_connections(knowledge_file)
    print(f"Created / 创建了 {synapse_count} synapses / 个突触")

# Save
thinking.save()
print("Data saved / 数据已保存")

# Stats
stats = thinking.get_thinking_stats()
print(f"\nFinal stats / 最终统计:")
print(f"  Neurons / 神经元数: {stats['neurons_count']}")
print(f"  Synapses / 突触数: {stats['synapses_count']}")
print(f"  Protected / 受保护神经元: {stats['protected_neurons_count']}")

print("\nInitialization complete! / 初始化完成！")