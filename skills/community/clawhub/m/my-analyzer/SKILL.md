---
name: rag-skill
description: 基于 Chroma、Ollama 与 MCP 的本地 RAG 检索技能，用于 OpenClaw 查询私有知识库与 PDF 文档。
version: 0.1.0
author: Jiwei Xu
license: MIT
tags:
  - rag
  - mcp
  - chroma
  - ollama
  - retrieval
---

# RAG 检索技能（RAG Skill）

该 Skill 用于将 OpenClaw 与本地 RAG（Retrieval-Augmented Generation）知识库连接，使 Agent 可以查询本地 PDF、项目文档、会议记录、技术资料以及私有知识库，而不仅仅依赖模型自身参数知识。

本 Skill 基于：

- Chroma 向量数据库
- Ollama Embedding 模型
- MCP（Model Context Protocol）工具接口
- OpenClaw Agent Skill 机制

实现 OpenClaw 与本地知识库的标准化集成。

---

# 使用场景

当用户提出以下类型问题时，应使用本 Skill：

- 查询本地 PDF 文档
- 查询私有项目资料
- 查询技术文档
- 查询会议记录
- 查询本地知识库
- 查询向量数据库中的内容
- 检索企业内部资料
- 基于本地文档进行问答

例如：

- “查询 CircularAI Phase 3 的相关内容”
- “从我的本地知识库中搜索 MCP 集成方案”
- “根据 PDF 总结该项目的主要问题”
- “检索与 Agentic RAG 相关的资料”

对于普通闲聊、公开常识问题或不需要文档检索的问题，不应使用本 Skill。

---

# 系统架构

整体流程如下：

```text
用户问题
  ↓
OpenClaw Agent
  ↓
MCP Tool 调用
  ↓
rag_query
  ↓
Chroma 向量数据库
  ↓
Ollama Embedding
  ↓
返回相关文档片段
  ↓
OpenClaw 生成最终回答
```

本 Skill 的核心目标是：

```text
让 OpenClaw 能够访问本地私有知识库。
```

---

# MCP 工具

本 Skill 暴露以下 MCP Tool：

```text
rag_query
```

输入：

```json
{
  "query": "用户问题",
  "k": 3
}
```

输出：

```json
{
  "query": "用户问题",
  "results": [
    {
      "content": "检索到的文档内容",
      "metadata": {
        "source": "文档名称",
        "page": 1
      }
    }
  ]
}
```

---

# 环境要求

需要以下环境：

- Python 3.10+
- Ollama
- Chroma
- OpenClaw
- MCP Python SDK

需要安装的 Python 包：

```bash
pip install mcp chromadb langchain-community langchain-ollama
```

需要提前下载 embedding 模型：

```bash
ollama pull bge-m3
```

启动 Ollama：

```bash
ollama serve
```

---

# OpenClaw 配置

需要在 OpenClaw 配置文件中注册 MCP Server：

```json
{
  "mcpServers": {
    "rag": {
      "command": "python",
      "args": [
        "/absolute/path/to/rag_mcp_server.py"
      ]
    }
  }
}
```

推荐使用绝对路径。

因为 OpenClaw 启动 MCP Server 时的工作目录可能并不是当前目录，使用相对路径可能导致无法找到 Chroma 数据库。

---

# 回答规则

使用本 Skill 时：

- 优先基于检索结果回答
- 尽量保留文档来源信息
- 不要编造不存在的文档
- 不要伪造页码或引用
- 如果没有检索到有效结果，应明确说明
- 如果结果可信度较低，应说明“证据不足”

---

# 安全说明

本 Skill 默认仅访问本地数据。

其设计目标是：

- 不上传本地文件
- 不调用外部云 API
- 不执行危险 Shell 命令
- 不访问 SSH Key
- 不需要 sudo 权限

所有文档均保留在本地 Chroma 数据库中。

用户在修改 Skill 或 MCP Server 后，应自行检查代码安全性。

---

# 局限性

本 Skill 只能检索：

```text
已经被向量化并写入 Chroma 数据库的文档
```

如果文档尚未建立 embedding，则无法被检索。

检索效果依赖：

- chunk 切分策略
- embedding 模型质量
- 查询语句质量
- 向量数据库更新情况
- metadata 完整性

建议在新增文档后重新构建向量数据库。

---

# 适用对象

本 Skill 适用于：

- OpenClaw 用户
- 本地 RAG 系统开发者
- 私有知识库场景
- 企业内部 Agent
- 本地 AI 助手
- Agentic RAG 系统
- MCP Tool 开发者

尤其适合：

```text
OpenClaw + MCP + Chroma + Ollama
```

的本地 Agent 架构。
