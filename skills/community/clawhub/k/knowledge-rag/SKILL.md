---
name: knowledge-rag
version: "1.6.0"
description: "个人知识库：存笔记、搜内容。用自然语言搜本地文档，不用记文件名。跟 AI 说'把这段存到知识库'自动保存并建索引。推荐搭配 Bilibili Auto Transcript：视频转录自动入库，转完即搜。"
metadata:
  openclaw:
    emoji: "📖"
    requires:
      bins: ["python3", "ollama"]
    install:
      - id: "ollama"
        kind: "system"
        label: "安装 Ollama（向量引擎）"
        url: "https://ollama.com/download"
      - id: "embed-model"
        kind: "shell"
        label: "下载推荐向量模型（千问3 Embedding 8B，约 4.7GB）"
        command: "ollama pull qwen3-embedding:8b"
      - id: "pip-deps"
        kind: "shell"
        label: "创建虚拟环境并安装 Python 依赖"
        command: "cd {{SKILL_DIR}} && python3 -m venv .venv && .venv/bin/pip install numpy requests fastapi pydantic uvicorn PyPDF2 pdfplumber python-docx"
      - id: "auto-index-cron"
        kind: "shell"
        optional: true
        label: "（可选）开启自动索引——每30分钟扫描新文件"
        command: "echo '提示：安装后可运行 openclaw cron add 定时运行 index_knowledge.py 实现自动索引'"
---

# 📖 Knowledge RAG

用自然语言搜索你的笔记和文档，像问 ChatGPT 一样问你的私人知识库。

---

## 🚀 安装启动

```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 拉取推荐模型（千问3 Embedding，中文最优）
ollama pull qwen3-embedding:8b

# 3. 创建虚拟环境并安装依赖
python3 -m venv .venv
.venv/bin/pip install numpy requests fastapi pydantic uvicorn PyPDF2 pdfplumber python-docx

# 4. 启动
.venv/bin/python3 start.py
```

打开 `http://localhost:5777` → 文件丢到 `~/workspace/knowledge/` → 管理页点「重新索引」→ 搜索页开搜。

### 可选：开启自动索引
新增文件后不用每次都手动点重新索引，设个定时任务每30分钟自动扫描：
```bash
openclaw cron add \
  --name "knowledge-rag 自动索引" \
  --every 1800000 \
  --message "运行索引检查：cd ~/.openclaw/workspace/skills/knowledge-rag && .venv/bin/python3 scripts/index_knowledge.py" \
  --silent
```

---

## 📂 知识库目录

```
~/workspace/knowledge/
  ├── notes/            ← 技术笔记、读书笔记
  ├── bilibili/         ← B站转录
  ├── wechat-articles/  ← 公众号文章
  ├── other/            ← 其他文档
  └── （可建任意子目录，去设置页添加）
```

支持 `.txt` / `.md` / `.pdf`（文字版）/ `.docx` 文件。

---

## 🔍 搜索方式

### 直接问我
> "帮我搜笔记里关于 Docker 的部分"  
> "知识库里有没有讲 Transformer 的文章？"

我会自动调搜索，带原文回答。

### 命令行
```bash
.venv/bin/python3 scripts/query_knowledge.py "你的问题"
.venv/bin/python3 scripts/query_knowledge.py "微服务" --source bilibili --top 5
.venv/bin/python3 scripts/query_knowledge.py --stats
```

新增文件后运行索引即可：
```bash
.venv/bin/python3 scripts/index_knowledge.py          # 增量
.venv/bin/python3 scripts/index_knowledge.py --force  # 全量重建
```

---

## 📝 Agent 存知识规范

当用户说"把这段存到知识库"，按以下规则操作：

| 内容类型 | 存放目录 | 文件名 |
|---------|---------|--------|
| 技术笔记、概念解释 | `notes/` | 中文描述.md |
| B站视频转录 | `bilibili/` | 自动处理 |
| 公众号、网页文章 | `wechat-articles/` | 文章标题.md |
| 其他 | `other/` | 内容摘要.md |

保存后运行 `.venv/bin/python3 scripts/index_knowledge.py` 更新索引。

---

## 🔧 切换模型

在设置页修改 `embed_model` 字段：

| 场景 | 模型 | 大小 |
|------|------|------|
| ✅ 推荐（质量最高） | `qwen3-embedding:8b` | 4.7GB | 中文优秀，检索质量最高 |
| 轻量（CPU友好） | `qwen3-embedding:0.6b` | 640MB | 对 CPU 友好，中文不错 |
| 多语言 | `bge-m3` | 1.2GB |
| 最小体积 | `nomic-embed-text` | 274MB |

改完后点「重新索引」，系统自动检测并全量重建。

---

## 🧑‍💻 环境检测（给 AI 助手的指引）

用户首次使用或出问题时，按顺序排查：

1. **Ollama 是否安装？** → `ollama --version`，否则引导去 https://ollama.com/download
2. **千问3 模型是否下载？** → `ollama list | grep qwen3-embedding`，否则 `ollama pull qwen3-embedding:8b`
3. **索引模型是否匹配？** → 读 `~/workspace/knowledge/.rag_data/model_meta.json`，不匹配则提示重建

快速诊断：
```bash
curl -s http://localhost:8768/api/stats | .venv/bin/python3 -c "
import sys,json; d=json.load(sys.stdin)
em = d.get('embed_model',{})
print(f'配置: {em.get(\"current\",\"?\")} | 索引: {em.get(\"stored\",\"?\")} ({em.get(\"stored_dim\",\"?\")}维)')
print(f'状态: {\"✅ 正常\" if not em.get(\"mismatch\") else \"❌ 不匹配\"}')"
```

---

## ⚠️ 注意事项

- 依赖 Ollama，首次下载模型约 640MB 需联网
- PDF 支持**文字版** PDF（PyPDF2 优先提取，失败自动降级到 pdfplumber），纯图像版 PDF 暂不支持
- DOCX 支持通过 python-docx 提取段落文字和表格内容
- PDF/DOCX 解析需先创建虚拟环境：`python3 -m venv .venv && .venv/bin/pip install PyPDF2 pdfplumber python-docx`
- 仅支持纯文本内容，不支持图片和 PDF 中的图像
- 删除文件后运行「重新索引」即可从搜索结果移除（增量索引自动清理已删除文件，无需 --force）
- 数据全部在 `~/workspace/knowledge/`，卸载不丢

## 🎯 推荐搭配

**Bilibili Auto Transcript** — 装了这个 skill 后，B站视频转录完自动存到知识库，不用手动操作：

```bash
clawhub install bilibili-auto-transcript
```

转录的文件自动进 `~/workspace/knowledge/bilibili/`，转完即搜。

---

## 📦 开源 & 交流

- **GitHub**：[github.com/54Lynnn/knowledge-rag](https://github.com/54Lynnn/knowledge-rag)（⭐️ Star 支持）
- **ClawHub**：[clawhub.ai/54lynnn/knowledge-rag](https://clawhub.ai/54lynnn/knowledge-rag)
- **QQ 群**：120363664（欢迎扫码加入交流）