---
name: markdown-ai-rewriter
description: 基于 markdown-ai-rewriter 的 Markdown AI 改写 Skill（保留结构、章节/全文模式、多模型、图片生成、视频生成、音乐生成）
version: 1.2.5
author: Ping Si <sipingme@gmail.com>
user-invocable: true
requires:
  - node: ">=18.0.0"
  - npm: ">=8.0.0"
  - env:
      OPENAI_API_KEY: "OpenAI API Key（与 --provider openai 对应）"
      ANTHROPIC_API_KEY: "Anthropic API Key（与 --provider anthropic 对应）"
      AZURE_OPENAI_API_KEY: "Azure OpenAI API Key（与 --provider azure-openai 对应）"
      AZURE_OPENAI_ENDPOINT: "Azure OpenAI Endpoint（可选；或使用 --base-url）"
      GEMINI_API_KEY: "Gemini API Key（与 --provider gemini 对应）"
      DEEPSEEK_API_KEY: "DeepSeek API Key（与 --provider deepseek 对应）"
      OPENROUTER_API_KEY: "OpenRouter API Key（与 --provider openrouter 对应）"
      QWEN_API_KEY: "Qwen API Key（与 --provider qwen 对应）"
      GLM_API_KEY: "GLM API Key（与 --provider glm 对应）"
      DOUBAO_API_KEY: "豆包 API Key（与 --provider doubao 对应；视频生成使用 Seedance）"
      WENXIN_API_KEY: "文心 API Key（与 --provider wenxin 对应）"
      MINIMAX_API_KEY: "MiniMax API Key（与 --provider minimax 对应；视频生成使用 Hailuo）"
      KLING_API_KEY: "可灵 API Key（视频生成 --video-provider kling）"
      RUNWAY_API_KEY: "Runway API Key（视频生成 --video-provider runway）"
      SHARED_OPENAI_KEY: "可选：内置共享 OpenAI Key 场景使用，见下文"
      MINIMAX_BASE_URL: "可选：MiniMax API Base URL，默认 https://api.minimaxi.com/v1"
tags:
  - markdown
  - ai
  - rewriter
  - content
  - openai
  - anthropic
  - azure-openai
  - gemini
  - deepseek
  - openrouter
  - qwen
  - glm
  - doubao
  - wenxin
  - minimax
  - video
  - image
  - music
repository: https://github.com/sipingme/markdown-ai-rewriter
---

# Markdown AI Rewriter Skill

本 Skill 对应 npm 包 **[markdown-ai-rewriter](https://www.npmjs.com/package/markdown-ai-rewriter)**（当前对齐 **v1.2.5**）：在 **尽量保留标题、代码块、表格、图片等结构** 的前提下，用大模型改写正文（润色、降重、换风格等），并支持 **图片生成**（图生图）、**视频生成**（文生视频）和 **音乐生成**（文生音乐）。

## 🚀 安装后快速开始

安装完成后，运行以下命令查看可用功能：

```bash
md-rewrite rewrite -i article.md -o out.md -p openai -v
```

输出示例：
```
📋 功能状态：
   ⬚ 文章改写 (--rewrite)
   ⬚ 图片生成 (--process-images)
   ⬚ 视频生成 (--generate-video)

⚠️  未启用任何功能。请使用以下选项启用：
   --rewrite         启用文章改写
   --process-images  启用图片生成
   --generate-video  启用视频生成
```

**重要**：v0.5.2 起，默认不启用任何功能，需要显式指定要启用的功能。

## 核心特点（先看这个）

**一句话定位**：这是一个面向生产场景的 Markdown 改写 Skill，重点是"**改写质量** + **结构稳定** + **成本可控**"。

- **结构稳定优先**：尽量保留标题层级、代码块、表格、图片位置，减少"改完排版坏掉"。
- **双模式可切换**：`section` 适合中长文批量与控成本，`full` 适合短文叙事连贯。
- **多模型一套命令**：同一 CLI 只换 `-p` 和环境变量，就能切换 11 个 Provider。
- **图片生成**：支持 MiniMax、OpenAI、Gemini、豆包等图片生成。
- **视频生成**：支持 MiniMax Hailuo、豆包 Seedance、可灵、Runway 等视频生成。
- **音乐生成**：支持 MiniMax Music 2.5+ 音乐生成（纯音乐/带歌词）。
- **可落地到流水线**：适合接在抓取、清洗、发布前的"内容标准化"环节。

## 最适合的使用场景

- 你已经有 Markdown 初稿，要做润色/降重/统一风格；
- 你在做批量内容处理，希望速度和费用可控；
- 你需要兼顾国内外多个模型平台，在可用性和成本之间灵活切换；
- 你需要为文章自动生成配图、视频或背景音乐。

---

## 与旧版差异（务必知晓）

| 项目 | 当前版本 (v0.5.2) |
|------|----------|
| **默认行为** | **默认不启用任何功能**，需显式使用 `--rewrite`、`--process-images`、`--generate-video` 启用。 |
| 改写模式 | 仅 **`section`（章节，默认）** 与 **`full`（全文）**；已移除「按块/段落」模式。 |
| 模型 | **OpenAI**、**Anthropic**、**Azure OpenAI**、**Gemini**、**DeepSeek**、**OpenRouter**、**Qwen**、**GLM**、**豆包**、**文心**、**MiniMax**。 |
| 图片生成 | 支持 MiniMax、OpenAI、Gemini、豆包、Nano-Banana 等。 |
| 视频生成 | 支持 MiniMax Hailuo、豆包 Seedance 2.0/1.5/1.0、可灵、Runway Gen-4.5。 |
| 音乐生成 | 支持 MiniMax Music 2.5+（纯音乐/带歌词/自动歌词）。 |
| 章节模式 | 按标题分章并行改写；**`-c / --concurrency` 对章节模式生效**。 |
| CLI 版本号 | 从安装的包的 `package.json` 读取，与 npm 版本一致。 |

---

## 安装

全局或项目内安装均可：

```bash
npm install -g markdown-ai-rewriter
# 或
npm install markdown-ai-rewriter
```

使用 **OpenAI** 或 **MiniMax** 时，需安装 peer 依赖 **`openai`**：

```bash
npm install openai
```

使用 **Anthropic** 时：

```bash
npm install @anthropic-ai/sdk
```

可执行命令：`markdown-ai-rewrite` 或 `md-rewrite`。

---

## 环境变量

| 变量 | 用途 |
|------|------|
| `OPENAI_API_KEY` | `--provider openai` |
| `ANTHROPIC_API_KEY` | `--provider anthropic` |
| `AZURE_OPENAI_API_KEY` | `--provider azure-openai` |
| `GEMINI_API_KEY` | `--provider gemini` |
| `DEEPSEEK_API_KEY` | `--provider deepseek` |
| `OPENROUTER_API_KEY` | `--provider openrouter` |
| `QWEN_API_KEY` | `--provider qwen` |
| `GLM_API_KEY` | `--provider glm` |
| `DOUBAO_API_KEY` | `--provider doubao` |
| `WENXIN_API_KEY` | `--provider wenxin` |
| `MINIMAX_API_KEY` | `--provider minimax`（文本改写）；`--video-provider minimax`（视频生成） |
| `KLING_API_KEY` | `--video-provider kling`（可灵视频生成） |
| `RUNWAY_API_KEY` | `--video-provider runway`（Runway 视频生成） |
| `AZURE_OPENAI_ENDPOINT` | `azure-openai` 可选 endpoint（也可用 `--base-url`） |
| `MINIMAX_BASE_URL` | 可选；默认 `https://api.minimaxi.com/v1`，可按 MiniMax 文档覆盖 |
| `SHARED_OPENAI_KEY` | 可选；仅在 **未传 `apiKey`** 且代码里允许使用共享 Key 时由库内部使用（需配合 `QuotaManager` 等逻辑，见包内 README）；**常规 CLI 用法请直接设置上述各厂商 Key。** |

---

## 何时使用本 Skill

**适合触发**：

- 用户要「改写 / 润色 / 降重 / 换风格」**已有 Markdown**，且希望 **保留文档结构**；
- 提到「章节改写」「全文改写」「技术文档 / 博客 / 公众号稿」等；
- 需要指定 **casual / formal / technical / creative / custom** 风格。

**不适合**：

- 从零「写一篇新文章」且输入不是 Markdown 改写流程；
- 纯格式转换（如 MD→HTML）；
- 仅分析结构、不做改写。

**触发关键词示例**：「重写这篇 md」「改成正式一点」「全文连贯改写」「按章节改」「用 MiniMax / OpenAI / Claude」。

---

## 两种改写模式（CLI：`--mode`）

| 模式 | 说明 | 典型场景 |
|------|------|----------|
| `section`（默认） | 按指定级别标题切分，分章调用模型；可带上下文章摘要；成本与速度较可控。 | 中长文档、多章节技术文 |
| `full` | 整篇一次请求（全文模式会对图片做占位符保护再还原）；语气通常最连贯。 | 短文、强叙事、整篇语气统一 |

- `--section-level 1|2|3`：仅章节模式有效，表示按几级标题切分（默认 1 级 `#`）。
- `--mode full` 时 token 消耗可能更大，适合长文时谨慎使用。

---

## 标准 CLI 示例

### 文章改写

```bash
# 章节模式 + OpenAI（注意：需要 --rewrite 显式启用改写）
export OPENAI_API_KEY="sk-..."
md-rewrite rewrite \
  -i input.md \
  -o output.md \
  -p openai \
  --rewrite \
  -s casual \
  -c 3 \
  -v

# 全文模式
md-rewrite rewrite -i input.md -o out.md -p openai --rewrite --mode full -v

# 二级标题分章
md-rewrite rewrite -i input.md -o out.md -p openai --rewrite --section-level 2

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
md-rewrite rewrite -i input.md -o out.md -p anthropic --rewrite -s formal

# DeepSeek
export DEEPSEEK_API_KEY="..."
md-rewrite rewrite -i input.md -o out.md -p deepseek --rewrite

# MiniMax（需 npm install openai）
export MINIMAX_API_KEY="..."
md-rewrite rewrite -i input.md -o out.md -p minimax --rewrite -m MiniMax-M2.1 -s casual
```

### 图片生成

```bash
# 只生成图片（不改写文章）
export MINIMAX_API_KEY="..."
md-rewrite rewrite -i input.md -o out.md -p minimax --process-images -v

# 改写 + 图片生成
md-rewrite rewrite -i input.md -o out.md -p openai --rewrite --process-images -v

# 指定图片 Provider
md-rewrite rewrite -i input.md -o out.md -p openai --process-images --image-provider doubao
```

### 视频生成

```bash
# 只生成视频（不改写文章）
export MINIMAX_API_KEY="..."
md-rewrite rewrite -i input.md -o out.md -p minimax --generate-video -v

# 改写 + 视频生成
md-rewrite rewrite -i input.md -o out.md -p openai --rewrite --generate-video -v

# 指定视频 Provider（豆包 Seedance）
export DOUBAO_API_KEY="..."
md-rewrite rewrite -i input.md -o out.md -p openai --generate-video --video-provider doubao

# 可灵视频
export KLING_API_KEY="..."
md-rewrite rewrite -i input.md -o out.md -p openai --generate-video --video-provider kling

# Runway 视频
export RUNWAY_API_KEY="..."
md-rewrite rewrite -i input.md -o out.md -p openai --generate-video --video-provider runway
```

### 音乐生成

```bash
# 纯音乐（无人声）- 从 prompt 生成
export MINIMAX_API_KEY="..."
md-rewrite music --prompt "Indie folk, melancholic, introspective" --instrumental -o bgm.mp3

# 带歌词的歌曲
md-rewrite music --prompt "Pop, upbeat, energetic" --lyrics "[verse]\nHello world\n[chorus]\nLa la la" -o song.mp3

# 从文件读取歌词
md-rewrite music --prompt "Rock, powerful" --lyrics-file lyrics.txt -o song.mp3

# 自动生成歌词（从 prompt 自动生成）
md-rewrite music --prompt "Jazz, smooth, romantic" --auto-lyrics -o song.mp3

# 从 Markdown 生成背景音乐
md-rewrite music -i article.md --instrumental -o bgm.mp3 -v
```

### 组合使用

```bash
# 改写 + 图片 + 视频（全功能）
md-rewrite rewrite -i input.md -o out.md -p openai \
  --rewrite \
  --process-images \
  --generate-video \
  -v
```

常用参数速查：`-i/-o` 输入输出，`-p` 厂商，`-k` 显式传 Key（也可全靠环境变量），`-m` 模型，`--base-url`（通用 endpoint 覆盖），`-s` 风格，`-t` 温度，`--max-tokens`，`--preserve-length`，`-c` 并发，`--mode`，`--section-level`，`--rewrite`，`--process-images`，`--generate-video`，`--video-provider`，`--image-provider`。完整列表以 `md-rewrite rewrite --help` 为准。

---

## 编程 API（TypeScript）

```typescript
import { MarkdownRewriter } from 'markdown-ai-rewriter';

const rewriter = new MarkdownRewriter({
  provider: 'openai', // 'anthropic' | 'azure-openai' | 'gemini' | 'deepseek' | 'openrouter' | 'qwen' | 'glm' | 'doubao' | 'wenxin' | 'minimax' | 'custom'
  apiKey: process.env.OPENAI_API_KEY,
  model: 'gpt-4o-mini',
  mode: 'section',       // 或 'full'
  sectionLevel: 1,
  concurrency: 3,
  verbose: true,
  enableRewrite: true,   // v0.5.2 起需要显式启用改写
  minimaxBaseUrl: process.env.MINIMAX_BASE_URL, // 仅 minimax 时可选
  options: {
    style: 'casual',
    temperature: 0.7,
    maxTokens: 2000,
  },
  // 图片生成配置（可选）
  imageProcessing: {
    provider: 'minimax',
    apiKey: process.env.MINIMAX_API_KEY,
  },
  // 视频生成配置（可选）
  videoProcessing: {
    provider: 'minimax', // 'minimax' | 'doubao' | 'kling' | 'runway'
    apiKey: process.env.MINIMAX_API_KEY,
    duration: 6,
  },
});

const result = await rewriter.rewrite(markdownString);
// result.rewritten, result.blocksProcessed, result.blocksRewritten
// result.imageProcessing, result.videoProcessing
```

`custom` 提供方可使用 `customProvider` 注入，详见 npm 包 README。

---

## 输出与行为说明

- **章节 / 全文** 均基于当前实现的解析与重组逻辑；**标题、代码块、表格**等会尽量保留；**图片**在全文模式下通过占位符机制处理。
- 列表、引用等是否逐条保留，与模型输出有关；若强约束，请在 `--prompt` 中明确要求。
- 统计字段 `blocksProcessed` / `blocksRewritten` 在章节模式下对应**章节单元**等粒度，与旧版「按段落块计数」的日志**不完全相同**。

---

## 常见问题

**1. 提示缺少 API Key**  
请设置与 `-p` 一致的环境变量，或使用 `-k` 传入。

**2. MiniMax 报错找不到模块**  
执行 `npm install openai`（MiniMax 使用 OpenAI 兼容客户端）。

**3. 改写后结构不满意**  
尝试切换 `--mode section` / `full`、调整 `--section-level`、缩小 `--max-tokens`、或在 `--prompt` 中强调「保留所有 Markdown 列表与表格结构」。

**4. 费用**  
以各云厂商定价为准；OpenAI 小模型、MiniMax 与 Anthropic 价差较大，README 中有量级参考。

---

## 与其他工具串联（示例）

```bash
convert-url --url "https://example.com/article" --output article.md

markdown-ai-rewrite rewrite -i article.md -o article-rewritten.md -p openai -s casual
```

发布等步骤按你的流水线工具执行即可。

---

## 维护说明

| 项目 | 值 |
|------|-----|
| 对齐包版本 | 1.2.5 |
| 仓库 | https://github.com/sipingme/markdown-ai-rewriter |
| npm | https://www.npmjs.com/package/markdown-ai-rewriter |
| 许可证 | MIT |
| 维护者 | Ping Si <sipingme@gmail.com> |

---

## 相关项目

- [news-to-markdown](https://github.com/sipingme/news-to-markdown) — 网页/新闻转 Markdown  
- [wechat-md-publisher](https://github.com/sipingme/wechat-md-publisher) — Markdown 发布到微信  
