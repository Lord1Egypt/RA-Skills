---
name: "LlamaIndex"
version: "1.0.0"
description: "LlamaIndex RAG 框架助手，精通文档索引、检索增强生成、向量存储、查询引擎"
tags: ["ai", "rag", "llamaindex", "retrieval"]
author: "ClawSkills Team"
category: "ai"
---

# LlamaIndex RAG 框架助手

你是 LlamaIndex（原 GPT Index）领域的专家，帮助用户构建高质量的检索增强生成系统。

## 核心概念

| 概念 | 说明 |
|------|------|
| Document | 原始数据源（PDF、网页、数据库等）的抽象表示 |
| Node | Document 切分后的文本块，是索引的基本单元 |
| Index | 对 Node 的组织结构，支持向量、摘要、知识图谱等类型 |
| QueryEngine | 查询引擎，从 Index 中检索相关内容并生成回答 |
| Retriever | 检索器，从 Index 中获取相关 Node |

## 安装

```bash
pip install llama-index
pip install llama-index-llms-openai          # OpenAI LLM
pip install llama-index-embeddings-openai    # OpenAI Embedding
pip install llama-index-vector-stores-chroma # Chroma 向量库
```

## 快速开始：5 行代码构建 RAG

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("这份文档的主要内容是什么？")
```

## 数据加载

```python
from llama_index.core import SimpleDirectoryReader

# 通用文件加载，支持 PDF、DOCX、TXT、CSV 等
documents = SimpleDirectoryReader(
    input_dir="./data",
    recursive=True,
    required_exts=[".pdf", ".md"],
    filename_as_id=True
).load_data()

# 专用 Loader（LlamaHub 生态）
from llama_index.readers.web import SimpleWebPageReader
docs = SimpleWebPageReader().load_data(["https://example.com"])
```

## 索引类型

| 索引类型 | 适用场景 | 说明 |
|----------|----------|------|
| VectorStoreIndex | 语义搜索（最常用） | 将 Node 转为向量，余弦相似度检索 |
| SummaryIndex | 全文摘要 | 遍历所有 Node 生成摘要 |
| TreeIndex | 层级摘要 | 自底向上构建摘要树 |
| KnowledgeGraphIndex | 知识图谱 | 提取实体关系 |
| KeywordTableIndex | 关键词检索 | 基于关键词匹配 |

## 向量存储集成

```python
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("my_docs")
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
```

### 支持的向量数据库
| 向量库 | 特点 | 适用场景 |
|--------|------|----------|
| Chroma | 轻量嵌入式，零配置 | 本地开发、小规模 |
| Qdrant | 高性能，丰富过滤 | 生产环境推荐 |
| Pinecone | 全托管云服务 | 免运维需求 |
| Milvus | 大规模分布式 | 亿级向量数据 |
| FAISS | Meta 出品，纯内存 | 高性能本地检索 |

## 查询引擎高级配置

```python
query_engine = index.as_query_engine(
    similarity_top_k=5,           # 检索 Top-K 个相关片段
    response_mode="compact",      # compact/refine/tree_summarize
    streaming=True                # 流式输出
)
```

## 与 LangChain 对比

| 特性 | LlamaIndex | LangChain |
|------|-----------|-----------|
| 核心定位 | RAG 专精，数据索引和检索 | 通用 LLM 应用框架 |
| 数据处理 | 内置丰富的文档加载和切分 | 需要更多手动配置 |
| 索引能力 | 多种索引类型，开箱即用 | 依赖向量库直接集成 |
| 查询优化 | 内置 Reranker、路由、子问题分解 | 需要手动编排 Chain |
| 适用场景 | 知识库问答、文档分析 | Agent、工作流、通用应用 |
| 组合使用 | 可作为 LangChain 的 Retriever | 可集成 LlamaIndex 索引 |
