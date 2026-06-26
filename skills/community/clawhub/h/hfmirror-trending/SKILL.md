---
name: hfmirror-trending
version: "1.0.0"
description: 通过 HF-Mirror 公开 API 获取 Hugging Face 实时热门趋势，并生成结构化中文 Markdown 报告。适用于各种对话式 AI 代理。
author: shunshiwei
tags:
  - huggingface
  - hf-mirror
  - trending
  - ai
  - chinese
license: MIT
python: ">=3.6"
dependencies: []
---

# hfmirror_trending (跨平台通用版)

此 Skill 使 AI 代理能够自主获取并解析 HF-Mirror (`hf-mirror.com`) 的实时热点趋势。

> **数据来源说明**：本 Skill 调用 `https://hf-mirror.com/api/trending` —— 这是 HF-Mirror 提供的**公开、免登录 REST API**，无需任何 Token 或账号授权，不涉及任何登录后数据抓取或绕过访问限制的行为。

## 适用场景

当用户发起关于 Hugging Face 或者是huggingface mirror最近热门模型、数据集或项目的询问时。例如：
- “最近有哪些模型比较流行？”
- “hugging face上最近比较火的模型有哪些？”
- “推送今天的huggingface mirror热榜。”
- “帮我解析一下 HF-Mirror 的趋势。”

## 代理工作流 (Agent Workflow)

AI 代理在处理上述指令时，应遵循以下通用的端到端逻辑：

1. **自动拉取与解析**: 代理应调用本 Skill 根目录下的处理脚本，利用其内置的网络请求功能。
   ```bash
   python scripts/summarize.py --fetch [out_path.md]
   ```
   *注意：脚本兼容 Python 3，可以在 Windows (PowerShell/CMD)、Linux (Shell) 或 macOS 环境下直接运行。*

2. **精美报告生成**: 脚本会自动从 `https://hf-mirror.com/api/trending` 抓取 JSON，并直接生成结构化的中文 Markdown。

3. **智能推送**: 代理读取生成的文件内容，并将其作为精美的消息推送给用户。

## 核心设计 (跨平台与环境解耦)

- **路径无关**: 代理应根据其所在的环境，通过相对路径或 Skill 环境配置来定位 `scripts/summarize.py`。
- **零依赖**: 脚本仅使用 Python 3 标准库（`json`, `urllib`, `os`, `sys`），无需安装任何第三方包，在最精简的容器或 CLI 环境中亦可直接运行。
- **动态抓取**: 内置 `--fetch` 参数，消除了手动准备中间文件的需求，实现了从 API 到报告的一键转化。
- **合规访问**: 使用具名 User-Agent (`hfmirror-trending-skill/1.0`) 标识请求来源，遵循公开 API 最佳实践。

## 核心输出字段说明

- **模型 ID**: 唯一的模型标识符。
- **下载量与点赞数**: 反映社区热度。
- **参数规模**: 自动换算（如 7B, 27B），帮助用户评估部署成本。
- **任务标签**: 区分 ASR, TTS, OCR 等不同 AI 领域。
