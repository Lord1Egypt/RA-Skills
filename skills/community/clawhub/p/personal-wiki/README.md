# personal-wiki

> 基于 Karpathy LLM Wiki 范式构建的 Claude Code 个人知识库 skill。

## 理念

不同于传统笔记工具（Notion/Obsidian）的**人写 LLM 读**，这个 skill 实现的是 **LLM 写、人查询**的范式：

- **输入**：原始内容（IMA 笔记、印象笔记、本地 PDF/PPT/Word）
- **处理**：Claude Code 自动分析、分类、提炼、写入结构化 Wiki 页面
- **输出**：本地 Markdown 知识库，随时可查询、可更新

## 功能

| 操作 | 触发词 | 说明 |
|------|--------|------|
| **Ingest** | "处理新内容"、"帮我 ingest" | 从三个来源拉取新内容写入 Wiki |
| **Query** | "wiki 里有没有关于 XX" | 检索 Wiki 综合回答 |
| **Lint** | "检查知识库"、"整理 wiki" | 发现孤立页面、内容矛盾等问题 |
| **Demo 生成** | "帮我做一个 XX 客户的 demo" | 基于模板替换客户信息 |

## 安装

### 1. 安装 skill

```bash
# 克隆仓库
git clone <repo-url>
cd personal-wiki-skill

# 将 SKILL.md 复制到 Claude Code skills 目录
mkdir -p ~/.claude/skills/personal-wiki
cp SKILL.md ~/.claude/skills/personal-wiki/SKILL.md

# （可选）初始化 Wiki 目录
mkdir -p ~/wiki/raw ~/wiki/pages
cp wiki-template/schema.md ~/wiki/schema.md
cp wiki-template/index.md ~/wiki/index.md
cp wiki-template/log.md ~/wiki/log.md
```

### 2. 配置 IMA 凭证

前往 [ima.qq.com/agent-interface](https://ima.qq.com/agent-interface) 获取 API 凭证：

```bash
mkdir -p ~/.config/ima
echo "YOUR_CLIENT_ID" > ~/.config/ima/client_id
echo "YOUR_API_KEY" > ~/.config/ima/api_key
```

### 3. 配置印象笔记 Token

前往 [app.yinxiang.com/api/DeveloperToken.action](https://app.yinxiang.com/api/DeveloperToken.action) 生成开发者 Token：

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
export EVERNOTE_TOKEN="S=s12:U=xxx:E=xxx:..."
export EVERNOTE_HOST="app.yinxiang.com"  # 印象笔记用此域名；国际版 Evernote 用 www.evernote.com
```

> **注意**：印象笔记开发者 Token 有效期约 2 周，需定期续期。

### 4. 安装 Python 依赖（处理本地文件时需要）

```bash
pip3 install evernote2 python-pptx python-docx
# pdftotext: macOS 自带；Linux: apt install poppler-utils
```

### 5. 自定义 Wiki 路径（可选）

Wiki 默认位于 `~/wiki/`。如需修改：

```bash
export WIKI_DIR="/path/to/your/wiki"
```

## 使用方法

安装完成后，在 Claude Code 中直接用自然语言触发：

```
# Ingest IMA 新内容
处理一下 IMA 的新内容

# Ingest 指定印象笔记
把"项目复盘 2026Q1"这篇笔记加入知识库

# Ingest 本地文件（先把文件放到 ~/wiki/raw/）
处理一下 raw 里的文件

# 查询
wiki 里有没有关于 SAP AI 的内容？

# Lint
帮我检查一下知识库

# Demo 定制
帮我做一个针对[客户名]（[行业]行业）的 demo
```

## Wiki 结构

```
~/wiki/
├── raw/              ← 放入待处理文件（PDF/PPT/Word/MD）
├── schema.md         ← 分类和格式规则（首次运行前请阅读）
├── index.md          ← 总目录（自动维护）
├── log.md            ← 处理记录（去重依据）
└── pages/            ← 知识页面
    ├── [主题A].md
    ├── [主题B].md
    └── Demo_Script_[场景].md
```

## Wiki 页面类型

### 知识页面

标准结构：`核心摘要` → `详细内容` → `关联主题` → `来源记录`

### Demo Script 页面

在知识页面基础上，顶部附加：
- **替换清单**：所有占位符及替换说明（如 `[客户名]`、`[行业]`）
- **行业定制要点**：当前行业特点 + 其他行业调整建议

Demo Script 设计为可复用模板，每次针对新客户时由 Claude 自动替换占位符。

## 来源说明

- **IMA（腾讯ima）**：通过 OpenAPI 读取笔记全文。注意：IMA 知识库（KB）API 仅返回摘要，需保存为"笔记"才能获取全文
- **印象笔记**：通过官方 Python SDK（`evernote2`）读取，按需指定笔记标题处理
- **本地文件**：放入 `~/wiki/raw/`，支持 `.pptx`、`.pdf`、`.docx`、`.md`、`.txt`

## 许可

MIT
