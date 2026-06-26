---
name: meeting-notes-assistant
description: 会议纪要智能助手。使用本地 Whisper 音频转写（离线、隐私安全），生成结构化会议纪要（时间、议题、结论、待办、关键词），提取 Action Items。支持 Word / PDF / 邮件输出，适合录音转写、会议归档与待办分发。触发关键词：「整理会议纪要」、「生成会议纪要」、「录音转纪要」。
version: "1.0.0"
author: "Meeting Notes Assistant Team"
tags: ["会议", "转写", "纪要", "Whisper", "AI"]
license: "MIT"
---

# Meeting Notes Assistant v1.0.0

## 功能概述

智能会议纪要助手，基于本地 Whisper 离线转写，提供：

### 核心功能
1. **离线语音转写** - 本地 Whisper（base / small / large-v3），数据不上云，隐私安全
2. **多语言支持** - 中文、英语、日语、韩语自动识别
3. **结构化纪要** - 时间、议题、结论、待办、关键词、Action Items
4. **智能解析** - AI 自动提取会议要点，规则解析兜底
5. **文档导出** - Word / PDF 专业排版
6. **历史存储** - 本地 SQLite 存储，支持关键词搜索
7. **模板管理** - 简洁版、专业版、立项会、周会、月度复盘等模板
8. **批量处理** - 目录级批量转写、批量纪要生成，支持递归扫描

### 核心优势
- ✅ **完全离线**：音频文件仅在您的电脑上处理，无需网络连接
- ✅ **隐私安全**：数据不上云，适用于敏感会议场景
- ✅ **零配置使用**：无需申请 API 密钥，安装即用
- ✅ **高准确率**：Whisper large-v3 模型准确率达 95%+
- ✅ **多领域适配**：内置金融词典，支持自定义领域术语

## 触发词

- "整理会议纪要"
- "生成会议纪要"
- "录音转会议纪要"
- "帮我做个会议记录"
- "用立项会模板" / "用周会模板" / "用月度复盘模板"
- 直接上传音频文件、文档、飞书链接、网页链接

## 推荐使用流程

### 场景 A：录音转纪要
1. 提供音频文件（.mp3 / .m4a / .wav / .ogg）
2. 先转写，再生成结构化纪要
3. 预览后导出 Word / PDF / 飞书 / 邮件

**飞书用户快速开始**：详见 [FEISHU_QUICK_START.md](./FEISHU_QUICK_START.md)

### 场景 B：文档或链接转纪要
1. 提供文字稿、飞书文档链接或网页链接
2. 直接生成结构化纪要
3. 选择分发方式

## 快速上手（命令行）

### 1) 安装依赖

```bash
pip install -r requirements.txt
```

**关于 Whisper 模型：**
- 安装时只包含 `base` 和 `small` 模型
- `large-v3` 模型（最高准确率，约 3GB）在首次使用时自动下载
- **large-v3 下载说明**：首次选择 large-v3 模型时，系统会提示下载确认
  - 下载大小：约 3GB
  - 下载时间：5-15 分钟（取决于网络速度）
  - 下载地址：https://openaipublic.azureedge.net/main/whisper/large-v3.pt
  - 适用场景：专业会议、长音频、最高准确率要求
- 如果您有 GPU（如 RTX 3060+），推荐使用 `large-v3` 模型
- 模型下载位置：`~/.cache/whisper/`（Linux/Mac）或 `C:\Users\<用户名>\.cache\whisper\`（Windows）

### 2) 常用脚本

```bash
# 语音转文字（推荐直接输出转写文本文件）
# 小模型（推荐日常使用，速度和准确率平衡）
python scripts/transcribe_audio.py demo.m4a --model small

# 大模型（最高准确率，需要 GPU）
python scripts/transcribe_audio.py demo.m4a --model large-v3

# 基础模型（快速测试）
python scripts/transcribe_audio.py demo.m4a --model base

# 生成结构化纪要
python scripts/generate_notes.py transcript.txt --output notes.json

# Windows PowerShell 下如需附带会议信息，建议改用 JSON 文件
python scripts/generate_notes.py transcript.txt --meeting-info-file meeting-info.json --output notes.json

# 导出 Word（内置模板）
python scripts/export_word.py notes.json --template simple --output notes.docx

# 导出 Word（templates.py 管理的模板，如"周会"）
python scripts/export_word.py notes.json --template 周会 --output weekly-notes.docx

# 导出 PDF
python scripts/export_pdf.py notes.json --output notes.pdf

# 查看历史会议
python scripts/storage.py list --limit 10
```

### 3) 配置 LLM（必做，否则纪要内容为空）

`generate_notes.py` 默认调用 OpenAI 兼容接口。在 `~/.workbuddy/meeting-notes-config.json` 中配置：

```json
{
  "llm_base_url": "https://api.openai.com/v1",
  "llm_api_key": "sk-your-key-here",
  "llm_model": "gpt-4o-mini"
}
```

国内兼容接口示例（通义千问、DeepSeek、智谱等）：
```json
{
  "llm_base_url": "https://api.deepseek.com/v1",
  "llm_api_key": "sk-your-deepseek-key",
  "llm_model": "deepseek-chat"
}
```

也可以用环境变量覆盖：`OPENAI_API_BASE` / `OPENAI_API_KEY` / `LLM_MODEL`

若无 API Key，使用 `--no-llm` 参数回退到规则解析（内容较少）：
```bash
python scripts/generate_notes.py transcript.txt --no-llm --output notes.json
```

### 4) 配置邮件发送（可选）

首次发送邮件前，可先运行 SMTP 配置向导：

```bash
python scripts/send_email.py --config
```

也可指定自定义配置文件路径（联调推荐）：

```bash
python scripts/send_email.py --config --config-path smoke-test/email-config.json
```

配置会写入 `~/.workbuddy/meeting-notes-config.json` 的 `email` 字段，并保留已有的 LLM 配置。

### 5) 配置文件位置

- 配置文件：`~/.workbuddy/meeting-notes-config.json`
- 会议主库：`~/.workbuddy/meeting_notes.db`
- 频道库：`~/.workbuddy/meeting_channels.db`
- 模板目录：`~/.workbuddy/meeting_notes_templates/`

### 6) 指定隔离数据库目录（联调 / smoke test 推荐）

`storage.py` / `channels.py` / `meeting_analytics.py` 已支持 `--db-dir` 参数，也兼容环境变量 `WORKBUDDY_HOME`。

```bash
python scripts/storage.py --db-dir smoke-test/real-audio/home/.workbuddy list --limit 10
python scripts/channels.py --db-dir smoke-test/real-audio/home/.workbuddy meetings 1
python scripts/meeting_analytics.py --db-dir smoke-test/real-audio/home/.workbuddy --period week
```

## 目录结构

### scripts/

- `transcribe_audio.py`：语音转文字
- `generate_notes.py`：生成结构化纪要 JSON
- `export_word.py`：导出 Word 文档
- `export_pdf.py`：导出 PDF 文档（Windows 自动优先 reportlab / fpdf2）
- `publish_feishu.py`：生成飞书文档 / 群聊 / 任务所需载荷
- `send_email.py`：发送会议纪要邮件（支持 `--config` SMTP 配置向导）
- `storage.py`：历史会议保存、搜索、列表、删除（支持 `--db-dir`）
- `templates.py`：模板管理
- `channels.py`：频道分组管理（支持 `--db-dir`、`update` 修改描述/颜色）
- `meeting_analytics.py`：会议频率与关键词分析（支持 `--db-dir`）
- `sentiment_analysis.py`：情绪分析（繁简转换 + 口语友好分句 + 逐句聚合）
- `ai_skills.py`：销售 / 招聘 / 技术评审 / 金融交流等场景提取
- `export_bitable.py`：导出飞书多维表格 JSON（支持 `--field-lang zh/en` 字段名切换）

### references/

- `template_guide.md`：Word 模板占位符与结构说明

### assets/

- 预留模板、Logo、附件素材目录

## 典型命令

### 导出专业版 Word

```bash
python scripts/export_word.py notes.json --template professional --output notes.docx
```

### 导出模板管理器中的 Word 模板

```bash
python scripts/export_word.py notes.json --template 技术评审 --output tech-review.docx
```

### 导出自定义 .docx 占位符模板

```bash
python scripts/export_word.py notes.json --template custom --template-path my-template.docx --output custom-notes.docx
```

### 导出飞书多维表格数据

```bash
python scripts/export_bitable.py notes.json --format json --field-lang zh
python scripts/export_bitable.py notes.json --format records --field-lang en
```

### 配置并发送邮件

```bash
python scripts/send_email.py --config
python scripts/send_email.py notes.json --to demo@example.com -a notes.docx
```

### 会议分析

```bash
python scripts/meeting_analytics.py --period week --limit 50
```

### 情绪分析

```bash
python scripts/sentiment_analysis.py transcript.txt
```

### 频道管理

```bash
python scripts/channels.py create 产品例会 --description 产品周会
python scripts/channels.py update 1 --description 重点客户复盘频道 --color "#FF6B6B"
python scripts/channels.py add 12 1
python scripts/channels.py meetings 1
```

## 使用示例

### 示例 1：语音转纪要

```text
用户：帮我整理会议纪要
AI：请提供会议录音或相关文档（音频 / 链接）
用户：[上传录音]
AI：好的，已识别语音。现在生成会议纪要...
```

### 示例 2：文档链接

```text
用户：https://xxx.feishu.cn/doc/xxx
AI：好的，已读取会议内容。正在生成结构化纪要...
```

### 示例 3：会议后分发

```text
用户：把这份纪要导出 Word 再发飞书
AI：先生成结构化纪要，再输出 Word，并给出飞书发布内容
```

## 合规声明

### 数据隐私
- ✅ **完全本地处理**：音频文件仅在您的电脑上处理，完全离线，不上传任何云端
- ✅ **隐私安全**：适用于敏感会议场景，无需担心数据泄露
- ⚠️ **LLM 解析**：转写文本会发送到 LLM API，请查看其隐私政策
- ⚠️ **无 API Key**：不配置 LLM 时可使用规则解析，但内容较少

详细隐私声明：[PRIVACY.md](./PRIVACY.md)

### 免责声明
- ⚠️ 转写结果仅供参考，不能保证 100% 准确
- ⚠️ 重要文档建议人工复核
- ⚠️ 专业术语可能存在错误识别
- ❌ 禁止用于非法用途（如未经授权的录音）

详细免责声明：[DISCLAIMER.md](./DISCLAIMER.md)

### 使用限制
- ❌ 禁止用于窃听、监控他人
- ❌ 禁止用于侵犯他人隐私
- ❌ 禁止用于违反法律法规的用途
- ✅ 请仅在合法合规的场景下使用

## 开源许可
本工具采用 MIT 许可证，详见：[LICENSE](./LICENSE)

## 前置条件

### 运行环境
- Python 3.8+
- 至少 4GB 内存（建议 8GB+）
- 首次使用 large-v3 模型需要下载约 3GB 文件

### 依赖项
- openai-whisper >= 20231117
- openai >= 1.0.0
- python-docx >= 1.1.0
- 其他依赖见 `requirements.txt`

## 最佳实践

### Whisper 模型选择指南

| 模型 | 大小 | 准确率 | 速度 | 推荐场景 |
|------|------|--------|------|----------|
| **tiny** | ~39MB | 最低（~80%） | 最快（<1分钟/10分钟音频） | 快速测试、简单对话 |
| **base** | ~140MB | 较低（~85%） | 快（<2分钟/10分钟音频） | 日常使用 |
| **small** | ~460MB | 高（~90%） | 中等（~5分钟/10分钟音频） | **推荐日常使用**，准确率足够，速度快 |
| **large-v3** | ~2.88GB | 最高（~95%） | 慢（~15分钟/10分钟音频，GPU 可加速） | 专业需求、重要会议，需要 GPU 支持 |

**使用建议：**
- **无 GPU**：使用 `small` 模型（已包含在安装包中）
- **有 GPU（RTX 3060+）**：使用 `large-v3` 模型（最高准确率）
- **首次使用 large-v3**：运行时会自动下载约 3GB 模型文件
- **金融等专业领域**：强烈推荐 `large-v3` 或 `small`，避免使用 `tiny` 和 `base`

### 模型对比测试结果（解放南路 3.m4a，59分钟金融会议音频）

| 模型 | 转写时间 | 字符数 | 金融术语识别率 | 适用性 |
|------|---------|--------|--------------|--------|
| **base** | ~2 分钟 | 13,966 | 4.2%（2/48） | ❌ 不推荐 |
| **small** | ~5 分钟 | 13,966 | 64.6%（31/48） | ✅ 推荐 |
| **large-v3** | 59 分钟（GPU） | 13,743 | 70.8%（34/48） | ✅ 专业推荐 |

**结论：**
- base 模型几乎无法识别专业术语（5G/华为/小米全错）
- small 模型识别率较高，适合日常使用
- large-v3 模型对"股权质押/估值/新能源/光伏/风电/产能过剩"等术语识别准确，长句理解更好

### 技术细节
### 技术细节

- 本地 Whisper 更建议使用 Python 3.11 环境；Windows 下脚本会优先尝试自动接入 `imageio-ffmpeg` 提供的 ffmpeg。
- `transcribe_audio.py` 已支持 `--model` 与 `--output`，适合直接串联"音频 -> 转写文本 -> 纪要"，且默认会做繁体转简体后处理。
- Windows PowerShell 下传 `--meeting-info` JSON 字符串容易受引用影响，建议优先使用 `--meeting-info-file`。
- `sentiment_analysis.py` 已改为繁简转换 + 口语友好分句 + 逐句聚合，会先按换行/标点切分，再对超长口语段按长度阈值拆分，避免把整段长文本当成一句导致误判。
- `ai_skills.py` 已支持金融场景自动识别，适合证券 / 理财 / 量化 / 机构交流录音；`--text` 与 `--json`（如 `notes.json`）两类输入都会先做结构化文本归一，再执行场景识别与字段提取。
- `storage.py` / `channels.py` / `meeting_analytics.py` 可通过 `--db-dir` 指向同一隔离数据目录，避免联调时读到不同数据库。
- `export_word.py` / `export_pdf.py` / `publish_feishu.py` / `export_bitable.py` 已兼容 `generate_notes.py` 产出的 `content` / `assignee` / `deadline` 字段，也兼容字符串形式的 `action_items`。
- `export_word.py` 已同时支持两类模板：1）`templates.py` 管理的 JSON 模板（`--template <模板名>`）；2）用户自带 `.docx` 占位符模板（`--template custom --template-path <模板文件>`），其中 `{{action_items}}` 会输出三列表格，详细占位符见 `references/template_guide.md`。
- `export_pdf.py` 在 Windows 下会默认按 `reportlab -> fpdf2 -> html` 的顺序自动导出，避免先尝试 `weasyprint` 时反复撞系统动态库缺失；非 Windows 仍会优先尝试 `weasyprint`。
- 若本机连本地 PDF 引擎也未安装，`export_pdf.py` 才会继续回退输出 HTML 预览文件。
- `export_bitable.py` 已支持 `--field-lang zh/en`；中文模式会输出 `会议标题` / `时间` / `参会人` 等字段，便于直接导入飞书多维表格。
- `storage.py` / `channels.py` / `meeting_analytics.py` 可通过 `--db-dir` 指向同一隔离数据目录，避免联调时读到不同数据库。
- `export_word.py` / `export_pdf.py` / `publish_feishu.py` / `export_bitable.py` 已兼容 `generate_notes.py` 产出的 `content` / `assignee` / `deadline` 字段，也兼容字符串形式的 `action_items`。
- `export_word.py` 已同时支持两类模板：1）`templates.py` 管理的 JSON 模板（`--template <模板名>`）；2）用户自带 `.docx` 占位符模板（`--template custom --template-path <模板文件>`），其中 `{{action_items}}` 会输出三列表格，详细占位符见 `references/template_guide.md`。
- `export_pdf.py` 在 Windows 下会默认按 `reportlab -> fpdf2 -> html` 的顺序自动导出，避免先尝试 `weasyprint` 时反复撞系统动态库缺失；非 Windows 仍会优先尝试 `weasyprint`。
- 若本机连本地 PDF 引擎也未安装，`export_pdf.py` 才会继续回退输出 HTML 预览文件。
- `export_bitable.py` 已支持 `--field-lang zh/en`；中文模式会输出 `会议标题` / `时间` / `参会人` 等字段，便于直接导入飞书多维表格。
- 飞书脚本当前输出的是可直接复用的载荷 / 任务清单，便于在工作流里继续调用。

## 配置管理

查看当前配置：`cat ~/.workbuddy/meeting-notes-config.json`

修改配置：说 "修改会议纪要配置"

重置配置：说 "重置会议纪要配置"
