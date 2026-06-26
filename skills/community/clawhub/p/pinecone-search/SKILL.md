---
name: pinecone-search
description: Pinecone vector search and document upload tool for knowledge base management
tags:
  - pinecone
  - database
  - search
  - vector
  - knowledge-base
  - upload
  - embedding
keywords:
  - 规范
  - 标准
  - 施工
  - 查询资料
  - 知识库
  - 向量搜索
  - pinecone
  - vector search
  - 上传文档
  - markdown
  - txt
version: 1.1.0
author: deki18
license: MIT
homepage: https://github.com/deki18/pinecone-search
repository: https://github.com/deki18/pinecone-search
type: skill
environment_variables:
  required:
    - PINECONE_API_KEY
    - EMBEDDING_API_KEY
    - EMBEDDING_BASE_URL
  optional:
    - EMBEDDING_MODEL
    - INDEX_NAME
    - NAMESPACE
---

# Pinecone Search

Pinecone 向量搜索与文档上传工具，支持 TXT、Markdown 格式文件的上传、分块、向量嵌入和搜索。

## 功能特性

- 📤 **文档上传**: 支持 TXT、Markdown 文件上传
- 🧩 **智能分块**: 递归字符分割，保持语义完整
- 🔢 **向量嵌入**: OpenAI 兼容 API，批量嵌入
- 🔍 **向量搜索**: 基于 Pinecone 的相似度搜索
- 📊 **上传统计**: 详细的文件和块级别统计信息
- 🏷️ **命名空间**: 支持多项目隔离

## 安装

```bash
pip install -r requirements.txt
cp config.example.env .env
# 编辑 .env 文件，填入你的 API Key
```

## 配置

编辑 `.env` 文件：

```env
PINECONE_API_KEY=your_pinecone_api_key
EMBEDDING_API_KEY=your_embedding_api_key
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_MODEL=text-embedding-3-large
INDEX_NAME=your-index-name
NAMESPACE=（可选，默认为default）
```

## 使用

### 上传文档

```bash
# 上传单个文件
python upload.py path/to/file.txt

# 上传多个文件
python upload.py file1.txt file2.md

# 上传整个目录
python upload.py ./docs/ --recursive

# 指定命名空间
python upload.py ./docs/ --namespace project-a

# 自定义分块大小
python upload.py ./docs/ --chunk-size 512 --overlap 100

# 预览模式（不实际上传）
python upload.py ./docs/ --dry-run

# JSON 格式输出（供 agent 使用）
python upload.py ./docs/ --json
```

### 搜索知识库

```bash
# 基础搜索
python search.py "查询内容"

# 返回更多结果
python search.py "查询内容" --top-k 10

# 按命名空间过滤
python search.py "查询" --namespace project-a

# 按文件类型过滤
python search.py "查询" --file-type markdown

# 按文件名过滤
python search.py "查询" --filename "施工规范"

# 设置相似度阈值
python search.py "查询" --min-score 0.7

# 纯向量搜索（禁用混合搜索）
python search.py "查询" --no-hybrid

# 显示详细分数
python search.py "查询" --verbose

# 组合使用
python search.py "混凝土标准" --file-type markdown --min-score 0.6 --top-k 5
```

## 触发关键词

- 规范、标准
- 查询资料、知识库
- 上传文档、添加文件、pineone

## 示例

### 上传示例

```bash
python upload.py "施工规范.md" --namespace construction
```

输出：

```
📤 正在上传文件: 施工规范.md

============================================================
📊 上传统计报告
============================================================

🏢 Workspace: workspace
📁 Namespace: construction
📄 总文件数: 1
🧩 总块数: 15
✅ 成功上传: 15
❌ 失败: 0
⏱️  耗时: 3.25 秒
⚡ 平均速度: 4.62 chunks/秒

📋 文件详情:
------------------------------------------------------------
  📄 施工规范.md
     路径: D:\docs\施工规范.md
     类型: markdown
     块数: 15
     Token数: 12580
     成功: 15

============================================================
```

### 搜索示例

```bash
python search.py "混凝土浇筑标准是什么？"
```

输出：

```
🔍 正在搜索: 混凝土浇筑标准是什么？
📋 过滤条件: 混合搜索(候选集=20)

======================================================================
【结果 #1】
匹配度: 0.8934
来源: D:\docs\施工规范.md
文件名: 施工规范.md
标题: 混凝土施工规范
文件类型: markdown
块索引: 1/15
内容:
  混凝土浇筑应符合以下标准：
  1. 浇筑前应检查模板和钢筋
  2. 混凝土应连续浇筑，避免冷缝
  ...
----------------------------------------------------------------------
```

### 详细分数示例（使用 --verbose）

```bash
python search.py "混凝土标准" --verbose --min-score 0.6
```

输出：

```
🔍 正在搜索: 混凝土标准
📋 过滤条件: 相似度≥0.6 | 混合搜索(候选集=20)

======================================================================
【结果 #1】
🏆 混合分数: 0.8234
📊 向量分数: 0.8012
📝 BM25分数: 0.8756
来源: D:\docs\施工规范.md
...
```

## 技术细节

### 文本分割策略

参考 LangChain RecursiveCharacterTextSplitter：
1. 优先按段落分割 (`\n\n`)
2. 其次按句子分割 (`\n`、`。`、`. `)
3. 最后按字符分割

### 向量嵌入

- 支持 OpenAI text-embedding-3-large/small
- 批量嵌入：30 条/批次
- 指数退避重试机制

### Pinecone 上传

- 自适应批次大小（2MB 限制自动减半）
- 元数据包含：文件名、路径、块索引、token 数量
- 支持命名空间隔离

### 混合搜索（向量 + 关键词 BM25）

搜索流程：
1. **向量召回**：从 Pinecone 召回 20 个最相似的候选结果
2. **关键词匹配**：使用简化版 BM25 算法计算关键词匹配分数
3. **混合排序**：综合向量分数（70%）和 BM25 分数（30%）重新排序
4. **返回 Top-K**：返回最终排序后的前 K 个结果

混合搜索优势：
- 结合语义理解（向量）和精确匹配（关键词）
- 提高长尾查询的准确性
- 对专业术语和特定词汇更敏感

## 返回给 Agent 的 JSON 格式

```json
{
  "workspace": "workspace",
  "namespace": "construction",
  "total_files": 1,
  "total_chunks": 15,
  "successful_chunks": 15,
  "failed_chunks": 0,
  "duration_seconds": 3.25,
  "files": [
    {
      "filename": "施工规范.md",
      "source": "D:\\docs\\施工规范.md",
      "file_type": "markdown",
      "chunks": 15,
      "successful": 15,
      "failed": 0,
      "tokens": 12580
    }
  ]
}
```
