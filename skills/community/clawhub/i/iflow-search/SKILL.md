---
name: iflow-search
description: "Web search, image search, and webpage content fetch via the iFlow Search API. / 通过 iFlow Search API 提供网页搜索、图片搜索和网页内容抓取能力。"
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: [IFLOW_API_KEY]
      bins: [bash, curl]
    primaryEnv: IFLOW_API_KEY
    homepage: https://github.com/iflow-ai/iflow-skills/tree/main/skills/iflow-search
---

# iFlow Search

## Summary

iFlow Search is a community skill that exposes the iFlow Search API as three callable scripts inside an agent:

- **Web Search** — keyword search over the iFlow web index, returning title / snippet / link
- **Image Search** — keyword image search, returning image URL, source page, and title
- **Web Fetch** — convert a URL into LLM-friendly text content

## Use Cases

- Pull fresh web results for topics past the model's training cutoff
- Search for images by keyword (reference shots, product images, screenshots)
- Read a known URL as cleaned markdown for downstream summarization
- Chain `web search → choose links → fetch each` to build a small research dossier

## Requirements

- `bash` and `curl` available in `PATH`
- `IFLOW_API_KEY` exported in the shell that launches the agent

## Setup

1. Create an API key at https://platform.iflow.cn/profile?tab=apiKey
2. Export it in your shell **before** starting the agent:

```bash
echo 'export IFLOW_API_KEY="YOUR_IFLOW_API_KEY"' >> ~/.zshrc
source ~/.zshrc
```

Do not pass the key as a CLI argument. Do not commit the key to any file.

## Capabilities

| Script | Purpose | Required args |
|---|---|---|
| `scripts/web_search.sh <keywords> [num]` | Web search | `keywords` |
| `scripts/image_search.sh <keywords> [num]` | Image search | `keywords` |
| `scripts/web_fetch.sh <url>` | Fetch + clean a URL | `url` |

See the Chinese section below for full parameter docs, examples, and error codes.

---

# 心流搜索 Skill

## 概述

心流搜索 Skill 是一个联网搜索技能，基于心流搜索 API，提供三大核心能力：

- **网页搜索**：根据关键词搜索网络，返回相关网页的标题、摘要和链接
- **图片搜索**：根据关键词搜索图片，返回图片 URL 和来源
- **网页内容抓取**：将指定 URL 的网页转换为大模型友好的文本内容

## 使用场景

- 用户需要搜索最新的网络信息
- 用户需要查找特定主题的图片
- 用户提供了一个 URL，需要获取网页内容进行分析
- 用户需要综合多个网页的信息来回答问题

## 能力说明

### 1. 网页搜索 (webSearch)

搜索网络并返回结构化的搜索结果。

**调用脚本**：`scripts/web_search.sh`

**参数**：
- `keywords`（必填）：搜索关键词
- `num`（可选，默认 10）：返回结果数量

**返回结果**：每条结果包含 `title`（标题）、`snippet`（摘要）、`link`（链接）

**使用示例**：
```bash
# 搜索 Python 异步编程教程
bash scripts/web_search.sh "Python 异步编程教程" 10
```

### 2. 图片搜索 (imageSearch)

搜索图片并返回图片链接。

**调用脚本**：`scripts/image_search.sh`

**参数**：
- `keywords`（必填）：搜索关键词
- `num`（可选，默认 10）：返回结果数量

**返回结果**：每条结果包含 `url`（图片 URL）、`refUrl`（来源页面）、`title`（图片标题，可能为空）

**使用示例**：
```bash
# 搜索风景图片
bash scripts/image_search.sh "风景壁纸" 5
```

### 3. 网页内容抓取 (webFetch)

将 URL 转换为大模型友好的文本内容。

**调用脚本**：`scripts/web_fetch.sh`

**参数**：
- `url`（必填）：目标网页 URL

**返回结果**：包含 `title`（标题）、`content`（正文内容）、`url`（实际 URL）、`fromCache`（是否命中缓存）

**使用示例**：
```bash
# 抓取网页内容
bash scripts/web_fetch.sh "https://example.com/article"
```

## 前置要求

使用前需设置 `IFLOW_API_KEY` 环境变量。在调用任何搜索能力之前，必须先检查该环境变量是否已设置：

```bash
echo "$IFLOW_API_KEY"
```

如果为空，提示用户：

> 搜索功能需要设置 IFLOW_API_KEY 环境变量才能使用。请按以下步骤操作：
> 1. 访问 https://platform.iflow.cn 注册并获取 API Key
> 2. 将 API Key 写入 shell 配置文件以持久生效：`echo 'export IFLOW_API_KEY=your_api_key' >> ~/.zshrc`
> 3. 在当前终端执行 `source ~/.zshrc` 使其立即生效（否则仅在新打开的终端窗口中才会生效）

设置完成后再继续执行搜索操作。

## 调用示例

### 搜索最新新闻

用户：「帮我搜一下最近的 AI 新闻」

```bash
bash scripts/web_search.sh "AI 人工智能 最新新闻" 10
```

### 搜索图片

用户：「帮我找一些猫咪图片」

```bash
bash scripts/image_search.sh "猫咪 可爱" 5
```

### 抓取网页内容

用户：「帮我看看这个网页的内容：https://example.com」

```bash
bash scripts/web_fetch.sh "https://example.com"
```

### 先搜索再抓取

用户：「帮我搜一下 Python 异步编程，找一篇好的教程详细看看」

1. 先用网页搜索找到相关结果：
```bash
bash scripts/web_search.sh "Python 异步编程 教程" 10
```

2. 从搜索结果中挑选合适的链接，用网页抓取获取详细内容：
```bash
bash scripts/web_fetch.sh "从搜索结果中获取的链接"
```

## 最佳实践

1. **先搜索，再抓取**：先用 `webSearch` 找到相关网页，再用 `webFetch` 获取详细内容
2. **精炼关键词**：使用具体、明确的关键词以获得更精准的搜索结果
3. **控制结果数量**：根据需要设置 `num` 参数，避免请求过多无用结果

## 错误处理

- `PARAM_INVALID`：检查请求参数是否正确
- `INVALID_APIKEY`：检查 API Key 是否有效
- `USER_RATE_LIMIT`：降低请求频率，限制为 1000 RPM
- `SYSTEM_ERROR`：服务端异常，稍后重试
