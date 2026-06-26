---
name: HuggingFace Papers
description: |-
  获取 HuggingFace Papers 热门 AI 论文，自动翻译摘要为中文，生成带趋势分析的双语报告。

  支持 DeepLX 和 OpenAI 兼容 LLM 两种翻译后端，自动降级。可保存为 Markdown 文件，方便导入 Obsidian 等笔记工具。

  使用场景:
  1. 用户想查看 HuggingFace 上的热门论文
  2. 用户问"最近有什么 AI 论文推荐"或"有什么新论文"
  3. 用户需要了解某个领域的最新研究动态
  4. 用户想要 AI/ML 论文的摘要和趋势分析

  **注意事项：**
  - 脚本默认通过 DeepLX API 将论文摘要翻译为中文
  - 论文标题保留英文原文
  - **必须保留完整摘要**，不得自行缩写或概括
  - 中文摘要和英文原文摘要同时显示
  - 使用 `--no-translate` 参数可输出纯英文报告
  - upvotes 数值和论文链接保持原样
  
  **输出规则：**
  - 运行脚本后，将报告同时 **保存为本地 .md 文件**（存入 skill 目录下的 `reports/` 文件夹）
  - 文件命名格式：`HuggingFace_本周热门论文_YYYY-MM-DD.md`
  - 保存完成后，告知用户文件路径，方便放入 Obsidian

  **工作流程:**
  1. 运行 `scripts/get_papers.py` 获取论文数据
  2. 运行 `scripts/generate_report.py --output reports/<文件名>.md` 生成报告并保存到文件
  3. 将报告内容输出给用户，并告知文件路径方便放入 Obsidian
required_environment_variables:
  - DEEPLX_URL — DeepLX 翻译 API 端点（使用 DeepLX 后端时必需）
  - OPENAI_API_KEY — OpenAI 兼容 API 密钥（使用 OpenAI 后端时必需）
  - OPENAI_BASE_URL — OpenAI 兼容 API 地址（可选，默认 https://api.openai.com/v1）
  - OPENAI_MODEL — 翻译用模型名（可选，默认 gpt-4o-mini）
  - TRANSLATE_BACKEND — 翻译后端选择（可选，默认 deeplx）
---

# HuggingFace Papers Skill

获取 HuggingFace Papers (https://huggingface.co/papers) 热门 AI 论文并生成分析报告。

## 使用场景

当用户询问以下问题时，使用本 skill：

1. "最近有什么热门论文？"
2. "有什么 AI 论文推荐？"
3. "帮我看看 HuggingFace 上的热门论文"
4. "本周/本月有什么新论文？"
5. "介绍一下最近的 AI 研究趋势"

## 依赖

- Python 3.8+
- `python-dotenv` — 加载 `.env` 文件

```bash
pip3 install python-dotenv
```

## 使用方法

### 前置条件：配置翻译后端

脚本支持 **DeepLX** 和 **OpenAI 兼容 API** 两种翻译后端，通过 `.env` 文件配置：

```bash
cp .env.example .env
# 然后编辑 .env
```

#### 方式一：DeepLX（默认）

```env
TRANSLATE_BACKEND="deeplx"
DEEPLX_URL="https://api.deeplx.org/你的token/translate"
```

#### 方式二：OpenAI 兼容 LLM

兼容任何 OpenAI 格式的 API（OpenAI、Azure、硅基流动、DeepSeek 等）：

```env
TRANSLATE_BACKEND="openai"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_API_KEY="sk-your-key-here"
OPENAI_MODEL="gpt-4o-mini"
```

> **降级策略**：主后端失败时自动降级到另一后端，都失败则保留英文原文。

`.env` 已加入 `.gitignore`，不会提交到 GitHub。

### 常用命令

```bash
# 获取论文列表（默认今日热门）
python3 scripts/get_papers.py

# 生成完整分析报告并保存到本地（推荐）
mkdir -p reports && python3 scripts/generate_report.py --period weekly --output reports/HuggingFace_本周热门论文_$(date +%Y-%m-%d).md

# 只查看不保存
python3 scripts/generate_report.py

# 指定时间范围和数量
python3 scripts/generate_report.py --period weekly --limit 10

# 输出纯英文报告（不翻译）
python3 scripts/generate_report.py --period weekly --no-translate

# 保存到文件
python3 scripts/generate_report.py --period weekly --output report.md
```

脚本在 skill 目录下的 `scripts/` 文件夹中，所有命令均从 skill 根目录执行。

## 参数说明

### generate_report.py

| 参数 | 说明 | 默认值 |
|:---|:---|:---|
| `--period` | 时间范围: daily/weekly/monthly | weekly |
| `--limit` | 论文数量 | 10 |
| `--output` | 输出文件路径 | stdout |
| `--no-translate` | 不翻译为中文，输出英文原文 | false |

### get_papers.py

| 参数 | 说明 | 默认值 |
|:---|:---|:---|
| `--period` | 时间范围: daily/weekly/monthly | daily |
| `--limit` | 返回论文数量 | 10 |
| `--format` | 输出格式: md/json | md |
| `--output` | 输出文件路径 | stdout |

## 输出语言

- **默认中文**：脚本通过 DeepLX API 自动将论文摘要翻译为中文，中文摘要与英文原文同时显示
- **论文标题**：保留英文原文
- **保留原始数据**：upvotes 数值和论文链接保持原样
- **英文模式**：使用 `--no-translate` 参数跳过翻译，输出纯英文原文

## DeepLX 翻译

报告使用 DeepLX API 将摘要自动翻译为中文：
- 批量翻译，逐条显示进度
- 单条翻译失败时自动降级，保留英文原文
- 无需手动翻译，开箱即用

## 网络问题处理

如果获取失败：
1. 检查网络连接
2. 稍后重试
