---
name: personal-knowledge-base
description: 管理个人知识库，基于RAG和文本向量化技术，支持文件的保存、向量化、检索、问答、删除等功能
---

# 个人知识库技能

本技能提供基于RAG（检索增强生成）和文本向量化技术的个人知识库管理能力。

## 何时使用

当用户表达以下意图时，使用此技能：
1. 创建新知识库：「创建知识库abc」或「创建知识库abc，文本块长度为200」
2. 保存文件到知识库：「把文件xxx保存到我的知识库aabb」
3. 更新知识库文件：「在知识库abc中更新xxx文件」
4. 在知识库中查询知识或信息：「查知识库aabb：xxx」
5. 列举知识库：「当前我有哪些知识库」
6. 列举知识库文件：「知识库aabb下有哪些文件」
7. 删除知识库文件：「删除知识库aabb下的xx文件」
8. 查询文本块：「查看知识库aabb中xx文件的第n个文本块内容」

## 配置文件

技能目录下的 `config.txt` 文件包含大部分配置参数。

### ZHIPUAI_API_KEY 配置方式

**推荐方式**：通过环境变量配置（优先级更高）

```bash
# Windows PowerShell
$env:ZHIPUAI_API_KEY="your-api-key-here"

# Windows CMD
set ZHIPUAI_API_KEY=your-api-key-here

# Linux/Mac
export ZHIPUAI_API_KEY="your-api-key-here"
```

**备选方式**：在 `config.txt` 中配置（向后兼容）

```
ZHIPUAI_API_KEY=your-api-key-here
```

**优先级**：环境变量 > config.txt

> **注意**：出于安全考虑，推荐使用环境变量方式配置 API Key，避免敏感信息明文保存在配置文件中。

### 其他配置项说明

| 参数 | 说明 |
|------|------|
| workspace_root | 知识库根目录 |
| embedding_model | 嵌入模型名称 |
| ZHIPUAI_LLM_MODEL | 智谱LLM模型名称 |
| DEFAULT_CHUNK_SIZE | 知识库缺省文本块大小 |
| DEFAULT_TOP_K | 默认检索的文本块最大数量 |
| DEFAULT_SIMILARITY_THRESHOLD | 相似度阈值 |

## 支持的文件格式

- **文本文件** (.txt)
- **PDF文件** (.pdf)
- **Word文档** (.doc, .docx)
- **Markdown文件** (.md, .markdown)
- **PowerPoint演示文稿** (.ppt, .pptx)

## 目录结构要求

知识库目录应按以下结构组织：
```
知识库根目录/
└── {知识库名称}/
    ├── sourcefiles/    # 原始文件存储目录
    └── vectordb/       # 向量数据库存储目录
        ├── faiss_index.bin
        ├── faiss_metadata.pkl
        └── kb_metadata.pkl    # 知识库元数据（包含文本块大小）
```

## 使用方法

### 1. 创建新知识库

当用户表示「创建知识库abc」时：

1. 解析知识库名称（如abc）
2. 在知识库根目录下创建 `abc` 目录
3. 在 `abc` 目录下创建 `sourcefiles` 和 `vectordb` 子目录
4. 在 `vectordb` 目录下生成空的向量库和索引文件
5. 保存文本块大小元数据（若用户指定了文本块长度则使用该值，否则使用config.txt中的DEFAULT_CHUNK_SIZE）
6. 重叠大小自动计算为：文本块大小 × 10%

使用示例：
```python
from scripts.knowledge_base_manager import KnowledgeBaseManager

# 创建知识库，指定文本块大小为500
result = KnowledgeBaseManager.create_knowledge_base(
    knowledge_base_name="abc",
    workspace_root="d:/Nancy/MyWork/WorkBuddyWorkSpace/MyKnowledgeBase",
    chunk_size=500  # 可选，不指定则使用config.txt中的DEFAULT_CHUNK_SIZE
)
print(result)
# 输出: {'success': True, 'message': "成功创建知识库 'abc'，文本块大小: 500", ...}
```

### 2. 保存文件到知识库

当用户表示「把文件（上传的文件或指定路径的文件）保存到我的知识库aabb」时：

1. 检查知识库是否存在，若不存在返回「知识库不存在，请先创建」
2. 找到工作区知识库根目录的`/aabb` 子目录
3. 确保 `sourcefiles` 目录存在（如不存在则创建）
4. 检查文件是否已存在于sourcefiles目录中：
   - 如果文件已存在，返回「文件已经存在」，不执行后续向量化操作
5. 复制原始文件到sourcefiles目录
6. 从知识库的元数据中读取文本块大小
7. 使用文本块大小进行文本分割（重叠大小 = 文本块大小 × 10%）
8. 将文本内容分割切块、向量化，存储到vectordb目录

使用示例：
```python
from scripts.knowledge_base_manager import create_knowledge_base_manager

# 创建知识库管理器
manager = create_knowledge_base_manager(
    knowledge_base_name="aabb",
    workspace_root="d:/Nancy/MyWork/WorkBuddyWorkSpace/MyKnowledgeBase"
)

# 添加文件到知识库
result = manager.add_file_to_knowledge_base("path/to/file.pdf")
print(result)
```

### 3. 更新知识库中的文件

当用户表示「在知识库abc中更新xxx文件」时：

1. 检查知识库是否存在，若不存在返回「知识库不存在，请先创建」
2. 检查知识库中是否存在该文件，若不存在返回「知识库中不存在该文件」
3. 删除该文件的源文件（sourcefiles目录下）
4. 删除该文件在向量库中的所有文本块
5. 将新文件添加到知识库

使用示例：
```python
from scripts.knowledge_base_manager import create_knowledge_base_manager

manager = create_knowledge_base_manager(
    knowledge_base_name="abc",
    workspace_root="d:/Nancy/MyWork/WorkBuddyWorkSpace/MyKnowledgeBase"
)

# 更新文件
result = manager.update_file_in_knowledge_base("path/to/new_file.pdf")
print(result)
```

### 4. 检索并回答问题

当用户表示「查知识库aabb：xxx」时：

1. 创建指定知识库（aabb）的向量数据库管理器
2. 将问题xxx向量化
3. 在向量库中检索与问题最相似的文本片段
4. 用检索到的内容,结合用户的问题，进行理解和思考，然后合理组织语言，回答用户的问题

使用示例：
```python
# 查询知识库
result = manager.answer_question("xxx")
print(result["answer"])
print(result["source_files"])
```

### 5. 列举知识库

当用户表示「当前我有哪些知识库」时：

1. 检查知识库根目录
2. 返回所有知识库列表（每个知识库包含：名称、文件数量、文本块大小、简单描述）

使用示例：
```python
from scripts.knowledge_base_manager import KnowledgeBaseCatalog

catalog = KnowledgeBaseCatalog()
# 获取简要列表
kb_list = catalog.list_knowledge_bases()
print(kb_list)

# 获取详细信息
kb_list_detailed = catalog.list_knowledge_bases_detailed()
for kb in kb_list_detailed:
    print(f"知识库: {kb['name']}, 文件数: {kb['file_count']}, 文本块大小: {kb['chunk_size']}, 描述: {kb['description']}")
```

### 6. 列举知识库下的文件

当用户表示「知识库aabb下有哪些文件」时：

1. 创建指定知识库的向量数据库管理器
2. 从向量库的元数据中获取所有文件的名称和相关信息
3. 返回文件列表（每个文件包含：文件名、文本块数量、导入日期时间）

使用示例：
```python
manager = create_knowledge_base_manager("aabb")
files = manager.list_files_in_knowledge_base()
for f in files:
    print(f"文件: {f['filename']}, 文本块数: {f['chunk_count']}, 导入时间: {f['import_time']}")
```

### 7. 删除知识库下的某个文件

当用户表示「删除知识库aabb下的xx文件」时：

1. 创建指定知识库的向量数据库管理器
2. 检查vectordb目录下的向量库中是否存在该文件的文本块
3. 如果存在，删除向量库中该文件相关的所有文本块
4. 删除sourcefiles目录下的原始文件
5. 如果向量库中没有这个文件，返回「aabb知识库中不存在这个文件」

使用示例：
```python
result = manager.remove_file_from_knowledge_base("xx.pdf")
print(result)
```

### 8. 查询指定文本块内容

当用户表示「查看知识库aabb中xx文件的第n个文本块内容」时：

1. 创建指定知识库（aabb）的向量数据库管理器
2. 检查vectordb目录下的向量库元数据中是否存在该文件
3. 如果文件存在，获取该文件的第n个文本块内容
4. 返回文本块内容，如果索引超出范围则返回错误提示

使用示例：
```python
# 查询指定文件的第3个文本块
result = manager.get_chunk_by_index("xx.pdf", 3)
print(result["content"])  # 文本块内容
print(result["total_chunks"])  # 文件总文本块数
```

## 配置参数

以下参数可在创建KnowledgeBaseManager时配置：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| knowledge_base_name | 必填 | 知识库名称 |
| workspace_root | config.txt配置 | 知识库根目录 |
| embedding_model | "embedding-3" | 嵌入模型 |
| chunk_size | 从知识库元数据加载 | 文本块大小 |
| vector_size | 2048 | 嵌入向量维度（固定值） |
| similarity_threshold | 0.5 | 相似度阈值 |
| top_k | 3 | 默认检索的文本块数量 |

**注意**：
- 文本块重叠大小会在运行时自动计算：`chunk_overlap = int(chunk_size * 0.1)`
- 每个知识库可以有不同的文本块大小设置，存储在知识库的元数据文件中

## 依赖要求

- Python 3.8+
- faiss-cpu
- langchain
- langchain-community
- langchain-text-splitters
- pypdf
- python-docx
- python-pptx (支持PPT文件)
- docx2txt (用于Word文档解析)
- zhipuai (智谱AI SDK，可选)

安装依赖：
```bash
pip install faiss-cpu langchain langchain-community langchain-text-splitters pypdf python-docx python-pptx markdown zhipuai docx2txt
```

## 注意事项

1. **文件去重**：通过文件哈希值判断文件是否已存在于向量库中，避免重复向量化
2. **文本分割**：使用RecursiveCharacterTextSplitter进行智能文本分块，支持中英文混合场景
3. **相似度过滤**：检索结果会根据相似度阈值进行过滤，确保返回内容相关性
4. **向量库重建**：删除文件时会重建FAISS索引，确保数据一致性
5. **知识库元数据**：每个知识库独立保存文本块大小设置，确保文件分割一致性
6. **知识库存在性检查**：创建管理器时会自动检查知识库是否存在，不存在则抛出异常
