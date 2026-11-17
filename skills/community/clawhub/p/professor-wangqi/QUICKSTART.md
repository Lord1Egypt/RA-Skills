# 王琦教授中医体质学术助手 - 使用指南

## 当前状态

✅ **已完成**：
- Skill骨架搭建
- 知识卡Schema设计
- 术语表定义
- 评测集设计（20个测试用例）
- 脚本开发（提取、索引、检索、问答）
- SCI论文知识卡提取（12篇）
- 诊疗经验知识卡提取（25篇）
- 向量索引构建（36个文档）
- 健康检查脚本

---

## 使用模式

### 模式一：作为Skill被外部LLM调用（推荐）

当本skill被Claude Code等外部LLM调用时，**只执行检索，不调用内置LLM**：

```bash
# 检索相关知识片段
python scripts/retrieve.py "痰湿质与肥胖" --format context

# JSON格式输出（便于程序解析）
python scripts/retrieve.py "痰湿质与肥胖" --format json

# 指定结果数量
python scripts/retrieve.py "痰湿质与肥胖" --n-results 10
```

**工作流程：**
```
用户提问 → Claude Code → 调用 retrieve.py → 返回检索结果
    ↓
Claude Code 基于检索结果生成回答（使用Claude自己的LLM）
```

**优势：**
- 不重复调用LLM，节省资源
- 外部LLM质量更高，回答效果更好
- 检索和生成分离，职责清晰

### 模式二：独立使用（测试/演示）

当需要独立测试时，可使用内置LLM：

```bash
# 单次问答
python scripts/ask.py "痰湿质与肥胖有什么关系？"

# 交互模式
python scripts/ask.py --interactive
```

**注意：** 此模式仅用于测试，生产环境应使用模式一。

---

## 快速开始

### Step 1: 安装依赖

```bash
cd D:\Codefield\Python\wangqi-skills\professor-wangqi
pip install -r requirements.txt
```

### Step 2: 健康检查

```bash
python scripts/health_check.py
```

检查项包括：
- Python版本
- 环境变量配置
- 依赖包安装
- LLM服务连接
- Embedding服务
- ChromaDB状态
- 知识卡数量

### Step 3: 检索测试

```bash
# 测试检索功能
python scripts/retrieve.py "什么是气虚质？" --n-results 3
```

### Step 4: 问答测试（可选）

```bash
# 使用内置LLM测试
python scripts/ask.py "什么是气虚质？"
```

---

## 环境配置

项目根目录 `.env` 文件：

```env
# Chat模型配置（仅独立模式需要）
API_KEY=sk-lm-xxx
BASE_URL=http://localhost:1234/v1
MODEL_NAME=qwen/qwen3.6-35b-a3b

# Embedding模型配置（检索必需）
EMBEDDING_MODEL=text-embedding-nomic-embed-text-v1.5
EMBEDDING_BASE_URL=http://localhost:1234/v1
EMBEDDING_API_KEY=sk-lm-xxx
EMBEDDING_DIMENSIONS=768
```

---

## 数据统计

| 数据类型 | 数量 | 状态 |
|----------|------|------|
| SCI论文 | 12篇 | ✅ 已提取 |
| 诊疗经验 | 25篇 | ✅ 已提取 |
| 知识卡总数 | 37张 | ✅ 已生成 |
| 向量索引 | 36文档 | ✅ 已构建 |
| 测试用例 | 20个 | ✅ 已设计 |

---

## 脚本说明

| 脚本 | 功能 | 用法 |
|------|------|------|
| `retrieve.py` | **检索接口（推荐）** | `python retrieve.py "问题" --format context` |
| `health_check.py` | **健康检查** | `python health_check.py` |
| `ask.py` | 问答（测试用） | `python ask.py "问题"` |
| `build_local_index.py` | 构建向量索引 | `python build_local_index.py --cards data/cards/` |
| `extract_knowledge_cards.py` | 提取知识卡 | `python extract_knowledge_cards.py --input data/ --output cards/` |
| `run_tests.py` | 运行测试 | `python run_tests.py --verbose` |

---

## 检索输出格式

### context格式（供LLM使用）

```
[论文] 《文献标题》 (年份)
文献内容...

---

[诊疗经验] 《文献标题》
文献内容...
```

### json格式（程序解析）

```json
[
  {
    "content": "文献内容...",
    "source_type": "paper",
    "title": "文献标题",
    "source_file": "原始文件.pdf",
    "year": "2023",
    "distance": 0.26,
    "relevance_score": 0.74
  }
]
```

---

## 问题排查

### 检索返回空结果

```bash
# 检查ChromaDB状态
python scripts/health_check.py

# 如果ChromaDB为空，重建索引
python scripts/build_local_index.py --cards data/cards/ --collection wangqi_knowledge
```

### Embedding服务连接失败

```bash
# 检查服务是否运行
curl http://localhost:1234/v1/models

# 检查环境变量
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('EMBEDDING_BASE_URL'))"
```

### 编码问题

```bash
# 使用JSON格式避免编码问题
python scripts/retrieve.py "问题" --format json
```
