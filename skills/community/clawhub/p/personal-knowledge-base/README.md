# Personal Knowledge Base (个人知识库)

[English](#english) | [中文](#中文)

---

## 中文介绍

### 什么是个人知识库？

个人知识库是一个基于 RAG（检索增强生成）和文本向量化技术的知识管理系统。它能够将你的文档、笔记、PDF、PPT 等文件转换为向量存储，实现智能问答和知识检索。

### 能做什么？

- **创建知识库**：为不同主题创建独立的知识库
- **文件导入**：支持多种文件格式的导入和向量化
- **智能问答**：基于 RAG 技术回答用户问题
- **知识检索**：快速找到相关内容片段
- **文本块查看**：查看任意文件的分割内容

### 支持的文件格式

| 格式 | 扩展名 |
|------|--------|
| 文本文件 | .txt |
| PDF 文档 | .pdf |
| Word 文档 | .doc, .docx |
| Markdown | .md, .markdown |
| PowerPoint | .ppt, .pptx |

### 如何配置？

#### 1. 环境变量配置（推荐）

```bash
# Windows PowerShell
$env:ZHIPUAI_API_KEY="your-api-key-here"

# Windows CMD
set ZHIPUAI_API_KEY=your-api-key-here

# Linux/Mac
export ZHIPUAI_API_KEY="your-api-key-here"
```

#### 2. 配置文件（备选）

编辑 `config.txt` 文件：

```txt
# 知识库根目录
workspace_root=D:\Nancy\MyWork\WorkBuddyWorkSpace\MyKnowledgeBase

# 嵌入模型名称
embedding_model=embedding-3

# 智谱LLM模型名称
ZHIPUAI_LLM_MODEL=glm-4-flash

# 知识库缺省文本块大小
DEFAULT_CHUNK_SIZE=1000

# 默认检索的文本块最多数量
DEFAULT_TOP_K=3

# 相似度过滤阈值
DEFAULT_SIMILARITY_THRESHOLD=0.5
```

### 使用示例

以下是用户可以通过自然语言使用技能的示例：

---

#### 1. 创建知识库

**用户问题**：帮我创建一个知识库，名称为"人工智能"，文本块长度为500

**执行结果**：Skill 会在你的知识库根目录下建立一个新的子目录"人工智能"，并在其中创建 sourcefiles 和 vectordb 两个子目录。知识库的文本块大小设置为500（每个文本块约500个字符）。

---

#### 2. 保存文件到知识库

**用户问题**：把这个PDF文件导入到"人工智能"知识库

**执行结果**：Skill 会将文件复制到知识库的 sourcefiles 目录，然后自动将文件内容分割为文本块，生成向量并存储到 vectordb 目录。返回提示告知用户成功添加的文件名和生成的文本块数量。

---

#### 3. 更新知识库中的文件

**用户问题**：在"人工智能"知识库中更新这份文档

**执行结果**：Skill 会先删除该文件原有的向量数据，然后重新导入新文件，生成新的向量存储。确保知识库中的内容保持最新。

---

#### 4. 知识问答

**用户问题**：查询"人工智能"知识库：什么是大语言模型？

**执行结果**：Skill 会在知识库中检索与问题相关的文本块，然后结合这些问题和检索到的内容生成答案。返回 AI 的回答以及参考的知识来源文件。

---

#### 5. 列举知识库

**用户问题**：我目前有哪些知识库？

**执行结果**：Skill 会列出所有已创建的知识库，显示每个知识库的名称、包含的文件数量、文本块大小等基本信息。

---

#### 6. 列举知识库中的文件

**用户问题**："人工智能"知识库中有哪些文件？

**执行结果**：Skill 会列出指定知识库中的所有文件，显示每个文件的名称、文本块数量、导入时间等信息。

---

#### 7. 删除知识库中的文件

**用户问题**：删除"人工智能"知识库中的abc.pdf文件

**执行结果**：Skill 会从向量数据库中删除该文件的所有文本块，并从 sourcefiles 目录中删除原始文件。删除后，该文件将无法再被检索。

---

#### 8. 查看文件文本块

**用户问题**：查看"人工智能"知识库中"Agentic AI技术.ppt"的第5个文本块内容

**执行结果**：Skill 会读取并显示指定文件的第5个文本块的内容，方便用户查看文档的详细分割情况。

### 技术原理

```
用户问题 → 向量化 → FAISS 向量检索 → 相关文本块 → LLM 生成答案
```

1. **文本分割**：将文档按 chunk_size 分块，相邻块有 10% 重叠
2. **向量化**：使用智谱 AI embedding-3 模型将文本转为向量
3. **向量存储**：使用 FAISS 索引存储和检索向量
4. **相似度检索**：根据用户查询找到最相关的文本块
5. **答案生成**：将相关内容和问题一起发送给 LLM 生成答案

### 目录结构

```
知识库根目录/
└── {知识库名称}/
    ├── sourcefiles/          # 原始文件
    └── vectordb/            # 向量数据库
        ├── faiss_index.bin   # FAISS 索引
        ├── faiss_metadata.pkl # 向量元数据
        └── kb_metadata.pkl   # 知识库元数据
```

### 依赖要求

```
faiss-cpu
langchain
langchain-community
langchain-text-splitters
pypdf
python-docx
python-pptx
markdown
zhipuai
docx2txt
```

---

## English

### What is Personal Knowledge Base?

Personal Knowledge Base is a knowledge management system based on RAG (Retrieval-Augmented Generation) and text vectorization technology. It can convert your documents, notes, PDFs, PPTs and other files into vector storage, enabling intelligent Q&A and knowledge retrieval.

### What Can It Do?

- **Create Knowledge Base**: Create separate knowledge bases for different topics
- **Import Files**: Support import and vectorization of multiple file formats
- **Intelligent Q&A**: Answer user questions based on RAG technology
- **Knowledge Retrieval**: Quickly find relevant content fragments
- **View Text Chunks**: View segmented content of any file

### Supported File Formats

| Format | Extensions |
|--------|------------|
| Text File | .txt |
| PDF | .pdf |
| Word Document | .doc, .docx |
| Markdown | .md, .markdown |
| PowerPoint | .ppt, .pptx |

### How to Configure?

#### 1. Environment Variable (Recommended)

```bash
# Windows PowerShell
$env:ZHIPUAI_API_KEY="your-api-key-here"

# Windows CMD
set ZHIPUAI_API_KEY=your-api-key-here

# Linux/Mac
export ZHIPUAI_API_KEY="your-api-key-here"
```

#### 2. Config File (Alternative)

Edit `config.txt`:

```txt
# Knowledge base root directory
workspace_root=D:\Nancy\MyWork\WorkBuddyWorkSpace\MyKnowledgeBase

# Embedding model name
embedding_model=embedding-3

# Zhipu LLM model name
ZHIPUAI_LLM_MODEL=glm-4-flash

# Default chunk size
DEFAULT_CHUNK_SIZE=1000

# Default top-k for retrieval
DEFAULT_TOP_K=3

# Similarity threshold
DEFAULT_SIMILARITY_THRESHOLD=0.5
```

### Usage Examples

Here are examples of how users can interact with the skill using natural language:

---

#### 1. Create Knowledge Base

**User Request**: Create a knowledge base named "AI Knowledge" with chunk size of 500

**Result**: The skill will create a new subdirectory named "AI Knowledge" under your knowledge base root directory, with sourcefiles and vectordb subdirectories. The chunk size is set to 500 characters per chunk.

---

#### 2. Import File to Knowledge Base

**User Request**: Import this PDF file into the "AI Knowledge" knowledge base

**Result**: The skill will copy the file to the sourcefiles directory, then automatically split the content into chunks, generate vectors, and store them in the vectordb directory. It will return a message showing the filename and number of chunks created.

---

#### 3. Update File in Knowledge Base

**User Request**: Update this document in the "AI Knowledge" knowledge base

**Result**: The skill will first delete the existing vector data for that file, then re-import the new file with updated vectors. This ensures your knowledge base stays current.

---

#### 4. Knowledge Q&A

**User Request**: Query the "AI Knowledge" knowledge base: What is a large language model?

**Result**: The skill will search for relevant text chunks in the knowledge base, then generate an answer based on the retrieved content and your question. It returns the AI's answer along with the source files used.

---

#### 5. List Knowledge Bases

**User Request**: What knowledge bases do I have?

**Result**: The skill will display all created knowledge bases with their basic information including name, file count, chunk size, etc.

---

#### 6. List Files in Knowledge Base

**User Request**: What files are in the "AI Knowledge" knowledge base?

**Result**: The skill will list all files in the specified knowledge base, showing each file's name, chunk count, and import time.

---

#### 7. Delete File from Knowledge Base

**User Request**: Delete abc.pdf file from the "AI Knowledge" knowledge base

**Result**: The skill will remove all text chunks for that file from the vector database and delete the original file from sourcefiles. After deletion, the file can no longer be retrieved.

---

#### 8. View Text Chunk Content

**User Request**: Show me the 5th text chunk of "Agentic AI Technology.ppt" in the "AI Knowledge" knowledge base

**Result**: The skill will retrieve and display the content of the 5th text chunk, allowing you to see how the document has been segmented.

### Technical Principle

```
User Query → Vectorization → FAISS Retrieval → Relevant Chunks → LLM Answer
```

1. **Text Splitting**: Split documents by chunk_size with 10% overlap
2. **Vectorization**: Use Zhipu AI embedding-3 model to convert text to vectors
3. **Vector Storage**: Use FAISS index for vector storage and retrieval
4. **Similarity Search**: Find most relevant text chunks based on user query
5. **Answer Generation**: Send relevant content and question to LLM for answer

### Directory Structure

```
Knowledge Base Root/
└── {Knowledge Base Name}/
    ├── sourcefiles/          # Original files
    └── vectordb/            # Vector database
        ├── faiss_index.bin   # FAISS index
        ├── faiss_metadata.pkl # Vector metadata
        └── kb_metadata.pkl   # Knowledge base metadata
```

### Dependencies

```
faiss-cpu
langchain
langchain-community
langchain-text-splitters
pypdf
python-docx
python-pptx
markdown
zhipuai
docx2txt
```
