---
name: rag-memory
description: "智能记忆系统，支持 SQLite（零配置）和 Milvus（向量搜索）后端。用于存储、检索和管理 AI 助手的记忆，支持语义搜索和自动备份。"
homepage: https://github.com/openclaw/skills
metadata: { "openclaw": { "emoji": "🧠", "requires": { "bins": ["python3"] } } }
---

# RAG Memory Skill - 智能记忆系统

## 📚 描述

支持多种后端的智能记忆系统，可选择：
- **SQLite**（默认）：开箱即用，无需额外服务
- **Milvus**：向量数据库，支持语义搜索
- **ChromaDB**：轻量级向量数据库（待实现）

## 🏗️ 架构

### SQLite 模式（默认）
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  OpenClaw   │ ──> │ RAG Memory   │ ──> │   SQLite    │
│  (记忆请求)  │     │   (技能模块)  │     │  (本地 DB)  │
└─────────────┘     └──────────────┘     └─────────────┘
```

### Milvus 模式（可选）
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  OpenClaw   │ ──> │ RAG Memory   │ ──> │   Milvus    │
│  (记忆请求)  │     │   (技能模块)  │     │ (向量存储)  │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           v
                    ┌──────────────┐
                    │   Ollama     │
                    │  (可选)      │
                    │  嵌入生成     │
                    └──────────────┘
```

## 🔧 配置

### 快速开始（SQLite - 无需配置）
```bash
# 直接使用，零配置
python -c "from rag_memory import store, search; store('测试记忆')"
```

### Milvus 模式（高级用户）
```bash
# 环境变量配置
export RAG_MEMORY_BACKEND=milvus
export MILVUS_URL=http://localhost:19530
export OLLAMA_URL=http://localhost:11434  # 可选，用于向量搜索

# 安装依赖
pip install pymilvus
```

### 所有环境变量
```bash
RAG_MEMORY_BACKEND=sqlite          # sqlite | milvus | chromadb
RAG_MEMORY_SQLITE_DB=./memory.db   # SQLite 数据库路径
MILVUS_URL=http://localhost:19530  # Milvus 服务地址
OLLAMA_URL=http://localhost:11434  # Ollama 服务地址（可选）
RAG_MEMORY_COLLECTION=openclaw_memory  # 集合名称
RAG_MEMORY_BACKUP_DIR=./memory_backup  # 备份目录
```

### 依赖

**最小依赖（SQLite 模式）**：
```bash
pip install requests
```

**完整依赖（Milvus 模式）**：
```bash
pip install requests pymilvus
```

## 📖 使用方法

### Python API
```python
from rag_memory import store, search

# 存储记忆
memory_id = store("今天讨论了 RAG 系统", {"type": "conversation", "topic": "RAG"})

# 搜索记忆
results = search("RAG 系统讨论", top_k=3)

# 删除记忆
from rag_memory import get_memory
get_memory().delete_memory(memory_id)
```

### 功能说明

| 函数 | 说明 | 参数 | 返回值 |
|------|------|------|--------|
| `store()` | 存储记忆 | content: str, metadata: Dict | memory_id: int |
| `search()` | 搜索记忆 | query: str, top_k: int | List[Dict] |
| `get_memory()` | 获取实例 | - | RAGMemory |

## 📊 记忆数据结构

```json
{
  "id": 1,
  "content": "今天讨论了 RAG 系统",
  "timestamp": "2026-03-18T15:30:00",
  "metadata": {
    "type": "conversation",
    "topic": "RAG"
  },
  "distance": 0.85  // 仅 Milvus 模式有
}
```

## 🔄 后端对比

| 特性 | SQLite | Milvus |
|------|--------|--------|
| 安装难度 | ⭐ 零配置 | ⭐⭐⭐ 需要 Docker |
| 向量搜索 | ❌ 不支持 | ✅ 支持 |
| 搜索方式 | 最近优先 | 语义相似度 |
| 适用场景 | 个人使用 | 生产环境 |
| 资源占用 | 低 | 中 - 高 |

## ⚠️ 注意事项

1. **SQLite 模式**：开箱即用，无需额外配置
2. **Milvus 模式**：需要 Docker 运行 Milvus 服务
3. **Ollama**：可选，用于向量嵌入生成
4. **备份机制**：自动备份到 JSON 文件

## 🐛 故障排除

### 问题：无法导入 pymilvus
```bash
# 仅 Milvus 模式需要
pip install pymilvus
```

### 问题：无法连接 Milvus
```bash
# 检查 Milvus 服务
docker ps | grep milvus
curl http://localhost:19530/v1/version
```

### 问题：嵌入生成失败
```bash
# 检查 Ollama 服务（可选功能）
curl http://localhost:11434/api/tags
ollama pull bge-m3  # 如需使用
```

## 📦 发布到 ClawHub

### 打包
```bash
cd /app/skills/rag-memory
tar -czf rag-memory.tar.gz SKILL.md rag_memory.py
```

### 上传
1. 访问 https://clawhub.com
2. 创建开发者账号
3. 上传 `rag-memory.tar.gz`
4. 填写技能描述和配置说明

### 用户安装
```bash
openclaw skills install rag-memory
```

## 📝 更新日志

- **2026-03-18**: 初始版本，替代文件记忆系统
- 自动备份到 JSON 文件
- 语义搜索功能
- 元数据支持
