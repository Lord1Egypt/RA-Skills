<p align="center">
  <h1 align="center">📖 Knowledge RAG</h1>
  <p align="center">把你的笔记和文档变成 AI 知识库，像聊天一样搜索</p>
  <p align="center">
    <a href="https://clawhub.ai/54lynnn/knowledge-rag"><img src="https://img.shields.io/badge/ClawHub-knowledge--rag-6c5ce7" alt="ClawHub"></a>
    <a href="https://github.com/54Lynnn/knowledge-rag"><img src="https://img.shields.io/github/stars/54Lynnn/knowledge-rag" alt="GitHub Stars"></a>
  </p>
</p>

---

## 这是什么

一个**本地运行的 RAG（检索增强生成）知识库系统**。把你的 `.txt` / `.md` / `.pdf` / `.docx` 文件丢进来，用自然语言搜索，像问 ChatGPT 一样问你的私人知识库。

**跟大多数 RAG 工具不同：**

- **极简部署** — 不需要 Docker，不需要数据库，一台机器一个 Ollama 就够了
- **Trae/OpenClaw Agent 集成** — 在 IDE 里直接让 AI 搜你的知识库并带原文回答
- **B站转录自动入库** — 配合 bilibili-auto-transcript，视频转录完自动进知识库

---

## 快速开始

```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 拉取推荐模型（千问3 Embedding 8B）
ollama pull qwen3-embedding:8b

# 3. 创建虚拟环境并安装依赖
python3 -m venv .venv
.venv/bin/pip install numpy requests fastapi pydantic uvicorn PyPDF2 pdfplumber python-docx

# 4. 启动
.venv/bin/python3 start.py
```

打开 `http://localhost:5777` → 把文件丢到 `~/workspace/knowledge/` → 点「重新索引」→ 开搜。

---

## 架构

```
┌─────────────────────────────────────────────────┐
│                 浏览器 (index.html)              │
└──────────────────┬──────────────────────────────┘
                   │ HTTP
┌──────────────────▼──────────────────────────────┐
│         TypeScript Express (server.ts)           │
│   Web 层：静态文件、配置读写、请求路由            │
└──────────────────┬──────────────────────────────┘
                   │ HTTP Proxy
┌──────────────────▼──────────────────────────────┐
│          Python FastAPI (knowledge_api.py)       │
│   RAG 层：搜索、索引、管理、统计 API             │
└──────┬─────────────────────────────┬────────────┘
       │                             │
┌──────▼──────┐            ┌────────▼──────────┐
│ index_      │            │ query_            │
│ knowledge.py│            │ knowledge.py      │
│ 索引构建    │            │ 向量搜索+混合打分  │
└──────┬──────┘            └────────┬──────────┘
       │                            │
       └──────────┬─────────────────┘
                  │ SQLite
       ┌──────────▼──────────┐
       │  chunks.db          │
       │  (文本 + 向量 BLOB) │
       └─────────────────────┘
```

## 知识库目录结构

```
~/workspace/knowledge/
  ├── notes/            ← 技术笔记、读书笔记
  ├── bilibili/         ← B站转录（配合 bilibili-auto-transcript）
  ├── wechat-articles/  ← 公众号文章
  ├── other/            ← 其他文档
  └── （可建任意子目录，去设置页添加）
```

支持的文件格式：`.txt` / `.md` / `.pdf`（文字版）/ `.docx`

---

## 核心特性

| 特性 | 说明 |
|------|------|
| **SQLite 存储** | 文本 + 向量存同一张表，原子写入，不会崩溃后数据不一致 |
| **增量索引** | hash 比对 + mtime 快速跳过，只处理变更文件，删除的文件自动清理 |
| **混合搜索** | 向量余弦相似度 + 查询扩展 + 标题/文本关键词加成 |
| **标题提取** | Markdown H1、PDF/DOCX 首行自动识别为标题，提高匹配精度 |
| **文件解析** | PDF（PyPDF2 + pdfplumber 降级）、DOCX（含表格内容） |
| **删除单条** | API 支持按文件名删除索引，无需全量重建 |
| **Web 界面** | 搜索 + 管理（统计、索引、配置）一体 |
| **多模型支持** | 可切换 embedding 模型，切换后自动全量重建 |

---

## 切换模型

在 `~/workspace/knowledge/.knowledge-config.json` 中修改 `embed_model` 字段：

| 场景 | 模型 | 大小 |
|------|------|------|
| 推荐（质量最高） | `qwen3-embedding:8b` | 4.7GB |
| 轻量（CPU 友好） | `qwen3-embedding:0.6b` | 640MB |
| 多语言 | `bge-m3` | 1.2GB |
| 最小体积 | `nomic-embed-text` | 274MB |

改完后重新索引，系统自动检测并全量重建。

---

## CLI 用法

```bash
# 索引
.venv/bin/python3 scripts/index_knowledge.py          # 增量更新
.venv/bin/python3 scripts/index_knowledge.py --force  # 全量重建

# 搜索
.venv/bin/python3 scripts/query_knowledge.py "你的问题"
.venv/bin/python3 scripts/query_knowledge.py "微服务" --source bilibili --top 5
.venv/bin/python3 scripts/query_knowledge.py --stats
```

---

## 在 OpenClaw/Trae 中使用

本项目同时也是 **OpenClaw 生态的 Skill**。如果你在用 OpenClaw 或 Trae IDE：

```bash
# 直接从 ClawHub 安装
clawhub install knowledge-rag
```

安装后，你的 AI Agent 会自动获得「搜索知识库」的能力，还可以配合 bilibili-auto-transcript 实现「转录完自动入库」。

---

## 注意事项

- 依赖 [Ollama](https://ollama.com/download)，首次下载模型约 4.7GB（8B）或 640MB（0.6B）需联网
- PDF 支持**文字版** PDF，纯图像版 PDF 暂不支持
- PDF/DOCX 解析需先创建虚拟环境：`python3 -m venv .venv && .venv/bin/pip install PyPDF2 pdfplumber python-docx`
- 数据全部在 `~/workspace/knowledge/`，卸载不丢

---

## 交流

- [GitHub Issues](https://github.com/54Lynnn/knowledge-rag/issues) — 反馈问题
- QQ 群：120363664

如果这个项目对你有帮助，欢迎 ⭐️ Star 支持！
