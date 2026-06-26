---
name: junyi-doc-reader
description: 大文档归档与检索管线（v5）。支持本地文件（Word/PDF/TXT/Markdown）和飞书云文档，转换、分块、可选 LLM 增强，输出结构化 Markdown 和索引，存入 Obsidian。触发词：读大文档、归档文档、junyi-doc-reader、doc-reader、文档索引、帮我读这个PDF、把文档存到Obsidian、帮我把飞书文档存到Obsidian、帮我把飞书工作日志按日期拆分、archive document、index document
---

# junyi-doc-reader (v5)

大文档归档与检索管线。将大文档安全地转为结构化 Markdown，生成分块索引，可选 LLM 提炼摘要。v5 新增飞书云文档支持。

## When to Use

- 用户要求归档/阅读/索引一个大文档（Word、PDF、TXT、Markdown）
- 用户要求把文档存到 Obsidian
- 用户要求把飞书文档存到 Obsidian
- 用户要求把飞书工作日志按日期拆分
- 文档超过 context 窗口限制，需要分块处理

## Supported Sources

| 源 | 输入 | 说明 |
|----|------|------|
| **local**（默认） | 文件路径 | .docx/.pdf/.txt/.md |
| **feishu**（v5 新增） | 飞书文档链接或 doc_token | 通过 API 抓取 |

### Source Auto-Detection

Agent 根据用户输入自动判断：
1. 包含 `feishu.cn/docx/` 或 `feishu.cn/wiki/` → 提取 doc_token → `--source feishu`
2. 本地文件路径 → `--source local`
3. 用户同时要求"按日期拆分" → 追加 `--split-by date`
4. 无法判断 → 追问用户

### Supported Local Formats

| 格式 | 转换工具 | 备注 |
|------|----------|------|
| .docx | pandoc | 推荐格式，需安装 pandoc |
| .pdf | pdftotext | 需安装 poppler，扫描件暂不支持 |
| .txt | 直接读取 | 自动检测编码（UTF-8/GBK） |
| .md | 跳过转换 | 直接进入分块 |

## Three Modes

| 模式 | 说明 | 需要 API |
|------|------|---------|
| `archive-only` | 转换 + 分块 + 原文归档 | 否 |
| `archive+index` | 上述 + 结构化索引 | 否 |
| `archive+index+insights` | 上述 + LLM 摘要/关键词/分类 | 是 |

**自动降级规则：**
- 未设 `DOC_READER_API_KEY` → archive-only
- `DOC_READER_ALLOW_EXTERNAL=false`（默认）→ 不外发文档给 LLM
- API 失败 → 保留已完成产物，降级继续

## Usage

### Local File

```bash
python3 scripts/pipeline.py <input_file> --output <output_dir> \
  [--mode archive-only|archive+index|archive+index+insights] \
  [--split-by year|topic|chapter|none]
```

### Feishu Document (v5)

```bash
python3 scripts/pipeline.py --source feishu --doc-token XXX --account YYY \
  --output <output_dir> [--mode ...] [--split-by date] [--dry-run]
```

**脚本路径相对于 skill 目录：** `~/.openclaw/shared-skills/junyi-doc-reader/`

### Examples

```bash
# 基础归档（本地文件）
python3 ~/.openclaw/shared-skills/junyi-doc-reader/scripts/pipeline.py \
  /path/to/document.docx \
  --output /path/to/obsidian/vault/文档名/

# 带 LLM 增强 + 按章节分文件
DOC_READER_API_KEY="sk-xxx" DOC_READER_ALLOW_EXTERNAL=true \
python3 ~/.openclaw/shared-skills/junyi-doc-reader/scripts/pipeline.py \
  /path/to/document.pdf \
  --output /path/to/obsidian/vault/文档名/ \
  --mode archive+index+insights \
  --split-by chapter

# 飞书文档归档（v5 新增）
python3 ~/.openclaw/shared-skills/junyi-doc-reader/scripts/pipeline.py \
  --source feishu --doc-token M2HXdBKTgo29ymxeUiWc13ANnlb --account steward \
  --output /path/to/obsidian/vault/文档名/

# 飞书工作日志按日期拆分（v5 新增）
python3 ~/.openclaw/shared-skills/junyi-doc-reader/scripts/pipeline.py \
  --source feishu --doc-token Abc123 --account steward \
  --output /path/to/obsidian/vault/日志/ \
  --split-by date

# 预览日期拆分（不写入）
python3 ~/.openclaw/shared-skills/junyi-doc-reader/scripts/pipeline.py \
  --source feishu --doc-token Abc123 --account steward \
  --output /path/to/obsidian/vault/日志/ \
  --split-by date --dry-run
```

### Parameter Validation Rules

| 条件 | 校验 |
|------|------|
| source=local | 必须提供 input_file |
| source=feishu | 必须提供 --doc-token 和 --account |
| source=local + --doc-token | 报错：参数冲突 |
| --split-by date + source=local | 报错：date 拆分仅支持飞书源 |
| source=feishu + mode=insights | 必须设置 DOC_READER_ALLOW_EXTERNAL=true |

### Environment Variables

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DOC_READER_API_KEY` | LLM API 密钥 | (无) |
| `DOC_READER_API_URL` | API endpoint | `https://api.openai.com/v1/chat/completions` |
| `DOC_READER_MODEL` | 模型名 | `claude-haiku-4-5-20251001` |
| `DOC_READER_ALLOW_EXTERNAL` | 是否允许外发文档 | `false` |

## Output Structure

### Local File / Feishu Standard Mode

```
output_dir/
├── manifest.json          # 任务元数据
├── source.md              # 完整原文 Markdown
├── source_meta.json       # 飞书版本锚点（仅飞书源）
├── ROOT_INDEX.md          # 全局导航目录
├── chunks.jsonl           # 分块数据（机器可读）
├── processing_report.md   # 处理报告
├── converted.md           # 中间转换结果
├── state.json             # 状态文件（用于断点恢复）
├── parts/                 # 分文件（仅 --split-by 时生成）
│   ├── 2024.md
│   └── 2025.md
└── indexes/               # 分层索引（仅 insights 模式）
    ├── by-year.md
    └── by-topic.md
```

### Feishu Daily Notes Mode (--split-by date)

```
output_dir/
├── manifest.json          # 任务元数据
├── source_meta.json       # 飞书版本锚点
├── converted.md           # normalize 后的完整 Markdown
├── _daily_index.md        # daily notes 索引
├── 2026-03-01.md          # 受管区块写入
├── 2026-03-02.md
└── ...
```

Daily notes 使用受管区块（`<!-- doc-reader:start/end -->`）写入，不覆盖用户已手写的内容。

### Key Files for Agent Use

- **ROOT_INDEX.md** — 先读这个了解文档结构
- **chunks.jsonl** — 精确检索定位，每行一个 JSON chunk
- **source.md** — 需要全文搜索时使用
- **manifest.json** — 查看处理状态和警告

### chunks.jsonl Format

```json
{"chunk_id": "ch-0001", "heading_path": ["第一章", "引言"], "char_start": 0, "char_end": 4500, "text": "..."}
```

Enriched chunks additionally have: `summary`, `key_points`, `keywords`, `classification`, `confidence`.

## Crash Recovery

Pipeline 自动保存进度到 `state.json`。如果中断，重新运行相同命令即可从上次完成的步骤恢复。

## Security & Privacy

本 Skill 的两类「敏感能力」均为**功能必需**且**用户授权**，遵循最小权限原则：

### 1. 本地凭据访问（仅飞书源）

- **读取范围**：仅 `~/.openclaw/openclaw.json` 中 `channels.feishu.accounts[<account>].appId` / `.appSecret` 两个字段
- **触发条件**：用户显式使用 `--source feishu --account <name>` 时
- **使用方式**：仅在内存中用于换取 Feishu tenant_access_token，不落盘、不打日志、不外传
- **网络出口白名单**：仅 `open.feishu.cn`（飞书官方 API），无任何第三方 endpoint
- **本地源（默认）**：完全不读取 openclaw.json，纯本地文件处理

### 2. 外发文档内容到 LLM（默认关闭）

- **默认状态**：`DOC_READER_ALLOW_EXTERNAL=false`，文档内容**不会**离开本机
- **基础管线**（archive-only / archive+index 模式）**完全离线**运行
- **启用 LLM 增强**需要用户主动设置全部四个环境变量：
  - `DOC_READER_API_KEY`（用户自己的 LLM API 密钥）
  - `DOC_READER_API_URL`（用户指定 endpoint，无硬编码生产 URL）
  - `DOC_READER_MODEL`（用户指定模型）
  - `DOC_READER_ALLOW_EXTERNAL=true`（显式同意外发）
- **传输内容**：只发 chunk 文本到用户配置的 endpoint，不带凭据、文件路径或元数据
- **可审计**：用户可在运行前检查 `chunks.jsonl`，明确知道会传输哪些内容

### 3. 文件系统写入

- 仅写入用户通过 `--output` 指定的目录
- 不修改用户其他文件，不读取无关路径
- Daily notes 模式使用受管区块（`<!-- doc-reader:start/end -->`）写入，不覆盖用户已手写内容

### 总结

| 能力 | 默认行为 | 启用方式 |
|------|---------|---------|
| 读 openclaw.json | 仅 `--source feishu` 时读飞书凭据 | 用户显式选择飞书源 |
| 调用飞书 API | 仅 `--source feishu` 时 | 用户显式选择飞书源 |
| 外发到 LLM | **关闭** | 设置 4 个环境变量 |
| 写本地文件 | 仅 `--output` 指定目录 | 用户指定路径 |

## Dependencies

- Python 3.9+
- pandoc（处理 .docx，`brew install pandoc`）
- poppler（处理 .pdf，`brew install poppler`）
- 无第三方 Python 包依赖（使用 stdlib urllib）

## Agent Workflow

### Local File

1. 确认用户要处理的文件路径和目标目录
2. 检查文件格式是否支持
3. 根据是否配置了 API key 确定模式
4. 运行 `python3 scripts/pipeline.py <file> -o <dir>` 一次完成所有步骤
5. 检查 `manifest.json` 确认状态
6. 向用户报告：处理了多少块、生成了哪些文件、有无警告
7. 如需写入 Obsidian，将 output_dir 内容复制到 vault 目标路径

### Feishu Document (v5)

1. 从用户输入中提取 doc_token（从 feishu.cn/docx/XXX 或 /wiki/XXX 链接中提取）
2. 确定 account 名（通常是当前 agent 的飞书账号名，如 steward / engineer）
3. 确定目标目录和 split 方式（用户要求按日期拆分→ --split-by date）
4. 运行 `python3 scripts/pipeline.py --source feishu --doc-token XXX --account YYY -o <dir> [--split-by date]`
5. 检查 `manifest.json` 确认状态
6. 向用户报告结果
