# RAG Memory - 智能记忆系统

> 🧠 为 AI 助手设计的智能记忆管理技能，支持多种后端存储方案

## ✨ 特性

- 🎯 **多后端支持**：SQLite（默认）、Milvus（可选）
- 🚀 **开箱即用**：SQLite 模式零配置
- 🔍 **语义搜索**：Milvus 模式支持向量相似度搜索
- 💾 **自动备份**：所有记忆自动备份到 JSON 文件
- 🔒 **隐私优先**：本地存储，数据不出境
- 📦 **易于集成**：简单的 Python API

## 🚀 快速开始

### 安装
```bash
openclaw skills install rag-memory
```

### 使用
```python
from rag_memory import store, search

# 存储记忆
memory_id = store("今天天气很好", {"type": "observation", "category": "weather"})

# 搜索记忆
results = search("天气", top_k=3)
for r in results:
    print(f"- {r['content']}")
```

## 📖 详细使用

### 存储记忆
```python
from rag_memory import store

# 简单存储
memory_id = store("这是一条记忆")

# 带元数据存储
memory_id = store(
    "用户设置了提醒",
    {
        "type": "reminder",
        "priority": "high",
        "category": "task"
    }
)
```

### 搜索记忆
```python
from rag_memory import search

# 基本搜索
results = search("提醒事项", top_k=5)

# 处理结果
for result in results:
    print(f"ID: {result['id']}")
    print(f"内容：{result['content']}")
    print(f"时间：{result['timestamp']}")
    print(f"元数据：{result['metadata']}")
    print(f"相似度：{result['distance']}")  # 仅 Milvus 模式
```

### 高级功能
```python
from rag_memory import get_memory

memory = get_memory()

# 删除记忆
memory.delete_memory(memory_id)

# 清空所有记忆
memory.clear_all()
```

## ⚙️ 配置

### 默认配置（SQLite）
无需任何配置，安装即可使用。

### 高级配置（Milvus）
```bash
# 环境变量
export RAG_MEMORY_BACKEND=milvus
export MILVUS_URL=http://localhost:19530
export OLLAMA_URL=http://localhost:11434  # 可选，用于向量搜索

# 安装依赖
pip install pymilvus
```

### 所有环境变量
| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `RAG_MEMORY_BACKEND` | `sqlite` | 后端类型：sqlite/milvus |
| `RAG_MEMORY_SQLITE_DB` | `./memory.db` | SQLite 数据库路径 |
| `MILVUS_URL` | `http://localhost:19530` | Milvus 服务地址 |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama 服务地址 |
| `RAG_MEMORY_COLLECTION` | `openclaw_memory` | 集合名称 |
| `RAG_MEMORY_BACKUP_DIR` | `./memory_backup` | 备份目录 |

## 📊 后端对比

| 特性 | SQLite | Milvus |
|------|--------|--------|
| 安装难度 | ⭐ 零配置 | ⭐⭐⭐ 需要 Docker |
| 向量搜索 | ❌ | ✅ |
| 搜索方式 | 时间优先 | 语义相似度 |
| 资源占用 | 低 | 中 - 高 |
| 适用场景 | 个人使用 | 生产环境 |

## 🗂️ 数据结构

### 记忆对象
```json
{
  "id": 1,
  "content": "今天天气很好",
  "timestamp": "2026-03-18T15:30:00",
  "metadata": {
    "type": "observation",
    "category": "weather"
  },
  "distance": 0.85
}
```

### 元数据建议
```python
# 对话记录
{"type": "conversation", "topic": "RAG", "participants": ["user", "assistant"]}

# 任务提醒
{"type": "reminder", "priority": "high", "due": "2026-03-19"}

# 用户偏好
{"type": "preference", "category": "settings"}

# 项目信息
{"type": "project", "name": "RAG System", "status": "active"}
```

## 🔧 故障排除

### 问题：无法导入 pymilvus
```bash
# 仅 Milvus 模式需要
pip install pymilvus

# 或切换回 SQLite 模式
export RAG_MEMORY_BACKEND=sqlite
```

### 问题：无法连接 Milvus
```bash
# 检查服务状态
docker ps | grep milvus
curl http://localhost:19530/v1/version
```

### 问题：嵌入生成失败
```bash
# 检查 Ollama 服务（可选功能）
curl http://localhost:11434/api/tags

# 拉取模型（如需使用）
ollama pull bge-m3
```

## 📦 开发

### 本地测试
```bash
cd /app/skills/rag-memory
python rag_memory.py
```

### 打包
```bash
tar -czf rag-memory.tar.gz SKILL.md rag_memory.py README.md
```

## 📝 更新日志

### v1.0.0 (2026-03-18)
- ✅ SQLite 后端支持
- ✅ Milvus 后端支持
- ✅ 自动备份功能
- ✅ 语义搜索（Milvus 模式）
- ✅ 元数据支持

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 支持

- 文档：https://docs.openclaw.ai/skills/rag-memory
- 社区：https://discord.com/invite/clawd
- ClawHub：https://clawhub.com/skills/rag-memory
