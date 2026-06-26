# Paper Management System

自动化 PDF 文献管理工具——索引、搜索、AI 提炼、飞书通知。

## 功能特性

- 📄 **自动索引**：扫描 PDF 文件，提取元数据（标题、作者、DOI）
- 🔍 **智能搜索**：按关键词、年份、作者搜索文献
- 🤖 **AI 提炼**：基于 PDF 全文生成结构化摘要
- 📚 **自动重命名**：按 `第一作者_年份_关键词.pdf` 规范命名
- 🔄 **增量处理**：仅处理新文件，不重复索引
- 🗑️ **Hash 去重**：自动跳过重复文件
- 📬 **飞书通知**：处理完成后自动推送结果（需配置 notify）

## 目录结构

```
paper-management-system/
├── README.md
├── SKILL.md
├── .env.example
├── config.example.yaml
├── scripts/
│   ├── auto_index.sh        # 定时索引入口（cron）
│   ├── paper_manager.py     # 索引+重命名核心
│   ├── extract_fulltext.py  # PDF 全文提取
│   ├── ai_summarize.py     # AI 摘要生成
│   └── config.py           # 配置管理
├── papers/                  # PDF 文件目录（需手动创建或配置）
├── downloads/               # 下载目录（自动移动新文件）
├── data/                   # 数据库目录
└── logs/                   # 日志目录
```

## 安装步骤

### 1. 克隆或解压

```bash
git clone https://github.com/crayfish-ai/paper-management-system.git
cd paper-management-system
```

### 2. 配置

```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml，填入必要配置
```

或使用环境变量（推荐）：

```bash
export PAPERMGR_PAPERS_DIR=/path/to/your/papers
export PAPERMGR_DOWNLOADS_DIR=/path/to/downloads
export PAPERMGR_DATABASE_PATH=/path/to/data/index.db
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置定时任务

```bash
# 每30分钟运行一次
*/30 * * * * /path/to/paper-management-system/scripts/auto_index.sh
```

## 配置说明

| 配置项 | 环境变量 | 说明 | 默认值 |
|--------|---------|------|--------|
| papers.dir | PAPERMGR_PAPERS_DIR | PDF 存储目录 | `./papers` |
| downloads.dir | PAPERMGR_DOWNLOADS_DIR | 下载目录 | `./downloads` |
| database.path | PAPERMGR_DATABASE_PATH | SQLite 数据库路径 | `./data/index.db` |
| ai.enabled | PAPERMGR_AI_ENABLED | 启用 AI 提炼 | false |
| ai.api_key | OPENAI_API_KEY | OpenAI API Key | - |
| notification.enabled | PAPERMGR_NOTIFICATION_ENABLED | 启用通知 | false |

## 使用流程

### 自动流程（cron）

1. 将 PDF 文件放入 `downloads/` 目录
2. `auto_index.sh` 自动：
   - 移动文件到 `papers/` 目录
   - 索引新 PDF（提取元数据）
   - 按规范重命名
   - 提取全文
   - 生成 AI 摘要（如启用）

### 手动命令

```bash
# 索引所有 PDF
python3 scripts/paper_manager.py index

# 按规范重命名
python3 scripts/paper_manager.py rename

# 搜索文献
python3 scripts/paper_manager.py search "瘢痕"

# 查看状态
python3 scripts/paper_manager.py status
```

## 依赖

- Python 3.8+
- PyMuPDF（PDF 元数据提取）
- sqlite3（内置）
- OpenAI API（可选，用于 AI 摘要）

## 与 OpenClaw 集成

本系统可作为 OpenClaw skill 使用，通过 `feishu-relay` 发送飞书通知。
