# memory-integration

记忆集成插件，为 OpenClaw 星型记忆架构提供记忆同步与增强搜索服务。

## 🎯 功能

- **记忆同步**：将 OpenClaw 原生记忆（MEMORY.md, memory/*.md）同步到共现图和语义向量库
- **增强搜索**：提供语义搜索 + 共现关联搜索的统一接口
- **增量同步**：仅同步新增或修改的记忆片段，避免重复处理
- **记忆标识**：为每个记忆片段生成唯一 ID，支持跨系统引用
- **统一接口**：通过标准适配器与其他插件（共现引擎、语义向量库、自我改进系统）交互

## 📦 安装

```bash
# 从 ClawHub 安装
clawhub install memory-integration

# 或从本地目录安装
clawhub install ./skills/memory-integration
```

## ⚙️ 配置

环境变量：
- `MEMORY_SYNC_CONFIG`：同步配置文件路径（默认：`~/workspace/integration/memory_sync_config.json`）
- `SYNC_INTERVAL_HOURS`：增量同步间隔（默认：24 小时）
- `ENABLE_SEMANTIC_SYNC`：是否启用语义向量同步（默认：true）
- `ENABLE_COOCCURRENCE_SYNC`：是否启用共现图同步（默认：true）

配置文件示例 (`memory_sync_config.json`)：
```json
{
  "last_sync": "2026-03-18T10:00:00",
  "file_hashes": {
    "/path/to/memory/2026-03-18.md": "abc123..."
  }
}
```

## 🚀 快速开始

```python
from integration.adapter.memory_integration_adapter import MemoryIntegrationAdapter

# 初始化
adapter = MemoryIntegrationAdapter()

# 同步所有记忆
result = adapter.sync_all_memories()
print(f"同步了 {result['synced_count']} 条新记忆")

# 增强搜索
query = "插件升级"
results = adapter.search(query, max_results=10)
for result in results:
    print(f"记忆 ID: {result['memory_id']}, 相似度: {result['score']:.3f}")
```

## 🔌 适配器接口

插件提供标准适配器 `MemoryIntegrationAdapter`，包含以下方法：

- `sync_all_memories()`: 同步所有记忆文件到关联存储
- `sync_memory_file(file_path)`: 同步单个记忆文件
- `search(query, max_results=10)`: 执行增强搜索（语义 + 共现）
- `record_cooccurrence(memory_id1, memory_id2, strength=1.0)`: 记录记忆共现
- `get_memory_by_id(memory_id)`: 根据 ID 获取记忆内容
- `health_check()`: 检查插件健康状态

## 📁 文件结构

```
memory-integration/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── memory_integration.py   # 核心集成类
│   └── __init__.py
├── config/
│   └── default_config.json     # 默认配置
└── references/
    └── integration_guide.md    # 集成指南
```

## 🔗 依赖关系

- **共现引擎插件** (co-occurrence-engine)：提供共现图存储与查询
- **语义向量库插件** (semantic-vector-store)：提供向量嵌入与相似度搜索
- **OpenClaw 原生记忆**：MEMORY.md 与 memory/*.md 文件

## 📈 版本历史

- **v0.1.0** (2026-03-18)：初始版本，提供记忆同步与增强搜索基础功能

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 到 ClawHub 仓库。