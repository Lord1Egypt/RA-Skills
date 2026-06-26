# OpenClaw Official Docs Search

Real-time search of the latest official OpenClaw docs with compact Markdown output for safer config, CLI, gateway, channels, and skills workflows.
实时检索 OpenClaw 官方最新文档，并返回紧凑 Markdown，适合更安全地处理配置、CLI、Gateway、渠道与 Skills 场景。

## Subtitle | 副标题

Answer from the latest official OpenClaw docs and reduce risk in config edits and feature usage.
基于官方最新文档回答问题，降低配置修改和功能使用中的错误风险。

## Quick Intro | 快速简介

OpenClaw Official Docs Search helps agents answer OpenClaw questions from official, up-to-date documentation instead of stale model memory. It combines official search, on-demand page retrieval, main-content extraction, and Markdown conversion into a lightweight ClawHub-ready package.
OpenClaw Official Docs Search 帮助 Agent 基于 OpenClaw 官方最新文档回答问题，而不是依赖模型过时记忆。它将官方搜索、按需抓取、正文提取和 Markdown 转换整合为一个轻量、可直接用于 ClawHub 发布的打包版本。

## High-Risk Reminder | 高风险提醒

- Before editing OpenClaw config files or giving operational instructions, verify the latest official docs first.
- 在修改 OpenClaw 配置文件或给出运维指导前，先核对官方最新文档。

## Store Listing Copy | 上架文案

- **Short Title:** OpenClaw Official Docs Search
- **短标题：** OpenClaw 官方文档实时检索
- **Subtitle:** Answer from the latest official OpenClaw docs and reduce risk in config edits and feature usage.
- **副标题：** 基于官方最新文档回答问题，降低配置修改和功能使用中的错误风险。
- **Short Description:** Real-time search of the latest official OpenClaw docs with compact Markdown output for safer config, CLI, gateway, channels, and skills workflows.
- **短简介：** 实时检索 OpenClaw 官方最新文档，并返回紧凑 Markdown，适合更安全地处理配置、CLI、Gateway、渠道与 Skills 场景。
- **Core Selling Point 1:** Answer from official docs, not stale model memory.
- **核心卖点 1：** 基于官方文档回答，而不是依赖模型过时记忆。
- **Core Selling Point 2:** Save tokens with cleaned search results and main-content-only extraction.
- **核心卖点 2：** 通过清洗搜索结果和只提取正文来节约 Token。
- **Core Selling Point 3:** Use it first for high-risk OpenClaw tasks such as config edits and command generation.
- **核心卖点 3：** 在配置修改、命令生成等高风险 OpenClaw 任务中优先使用。
- **High-Risk Reminder:** Before editing OpenClaw config files or giving operational instructions, verify the latest official docs first.
- **高风险提醒：** 在修改 OpenClaw 配置文件或给出运维指导前，先核对官方最新文档。

## Why Download This | 为什么值得下载

- Get real-time access to the latest official OpenClaw docs
- 实时获取 OpenClaw 官方最新文档
- Reduce hallucinations caused by outdated model memory
- 降低由模型过时记忆带来的幻觉和错误回答
- Save tokens by returning cleaned, focused documentation content instead of raw search payloads or full HTML pages
- 通过返回清洗后的重点内容而不是原始搜索结果或整页 HTML，减少 Token 消耗
- Return clean Markdown instead of noisy raw HTML or full-page dumps
- 返回整洁的 Markdown，而不是噪音很多的原始 HTML 或整页内容
- Read only the page you need, keeping responses fast and token-efficient
- 按需只读取目标页面，让响应更快、更省 Token
- Fit common OpenClaw support, setup, CLI, gateway, and skills questions out of the box
- 开箱即用，适合 OpenClaw 配置、CLI、Gateway、Skills 和支持类问题

## Three Reasons Users Install It | 用户为什么会安装它

- They need answers grounded in official OpenClaw docs, not approximate model recall
- 他们需要基于 OpenClaw 官方文档的答案，而不是模型模糊回忆
- They want fresher, more trustworthy responses for support and implementation tasks
- 他们希望在支持、接入和实施场景中得到更及时、更可信的回答
- They need a practical doc-search skill that works immediately without building custom retrieval
- 他们需要一个无需自建检索系统、拿来就能用的文档检索技能

## Key Advantages | 核心优势

- Official-source first: queries OpenClaw's official documentation workflow before summarizing
- 官方来源优先：先查询 OpenClaw 官方文档，再进行总结
- Real-time retrieval: fetches current pages on demand instead of relying on packaged snapshots
- 实时检索：按需抓取当前页面，而不是依赖打包时的静态快照
- LLM-friendly output: extracts `#content-area` and converts it into compact Markdown
- 模型友好：提取 `#content-area` 主内容并转换为紧凑 Markdown
- Token-efficient by design: removes noisy metadata, strips highlight tags, cleans repeated titles, and avoids full-page output
- 具备节约 Token 的设计：删除冗余元数据、去除高亮标签、清理重复标题，并避免整页输出
- Better search precision: prefers English queries for stronger official search hit rates
- 更高搜索命中率：优先使用英文关键词，提高官方搜索精度
- Lightweight and practical: avoids site mirroring and focuses on the exact document the user needs
- 轻量实用：不镜像整个站点，只聚焦用户真正需要的那一篇文档

## How It Saves Tokens | 如何节约 Token

- Formats search responses into compact Markdown instead of returning raw JSON
- 将搜索响应整理为紧凑 Markdown，而不是直接返回原始 JSON
- Keeps only high-value fields such as breadcrumbs, page path, and cleaned content
- 只保留高价值字段，如导航路径、页面路径和清洗后的内容
- Removes highlight HTML like `<mark>` and other noisy tags from search snippets
- 移除搜索片段中的 `<mark>` 等高亮 HTML 标签和其他噪音标签
- Collapses extra line breaks and repeated titles to reduce wasted context
- 压缩多余换行和重复标题，减少无效上下文占用
- Fetches only one target page when needed instead of loading large document sets
- 需要详情时只抓取单篇目标页面，而不是加载大量文档
- Extracts only `#content-area` from the page rather than returning full site chrome
- 只提取页面的 `#content-area` 主体内容，不返回整站导航和外层结构

## Included Files | 包含文件

- `SKILL.md` — skill metadata and runtime instructions
- `SKILL.md` — 技能元信息与运行说明
- `src/search.ts` — source implementation
- `src/search.ts` — 源码实现
- `dist/search.js` — compiled runtime build
- `dist/search.js` — 编译后的运行文件
- `package.json` / `package-lock.json` — dependency manifest
- `package.json` / `package-lock.json` — 依赖与打包清单
- `tsconfig.json` — TypeScript build configuration
- `tsconfig.json` — TypeScript 编译配置

## What This Skill Does | 这个技能能做什么

- Real-time searches the latest OpenClaw official docs through the official search endpoint
- 通过官方搜索接口实时检索 OpenClaw 最新官方文档
- Prefers English queries for higher search precision
- 优先使用英文关键词，以提高搜索命中率
- Fetches a specific documentation page on demand
- 按需抓取指定文档页面
- Extracts the `#content-area` main article region
- 提取 `#content-area` 主正文区域
- Converts noisy HTML into compact Markdown for LLM consumption
- 将噪音较多的 HTML 转成适合 LLM 使用的紧凑 Markdown

## Intended Use | 典型用途

- Answer questions using the latest official OpenClaw documentation instead of stale embedded knowledge
- 用最新官方文档回答问题，而不是依赖过时的模型内置知识
- Retrieve specific documentation pages on demand in real time
- 实时按需获取特定文档页面
- Reduce token usage compared with loading full documentation pages
- 相比加载整页文档，更能节省 Token 消耗

## Best For | 适合谁用

- ClawHub skills that need trustworthy OpenClaw answers
- 需要可靠 OpenClaw 答案的 ClawHub 技能
- AI assistants that must look up current setup or configuration details
- 需要查询当前配置或接入细节的 AI 助手
- Support and operations workflows that benefit from fast, source-linked doc retrieval
- 需要快速定位官方来源文档的支持和运维流程
- Teams that want fresher documentation answers without building a custom crawler
- 希望获得更新鲜文档答案、又不想自建爬虫或检索系统的团队

## When To Use This Skill | 什么时候应优先调用此技能

- For high-risk OpenClaw tasks, invoke this skill first before answering, generating steps, or editing files
- 对于高风险的 OpenClaw 任务，应先调用此技能，再回答、生成步骤或修改文件
- Before modifying any OpenClaw configuration file, check the latest official docs first
- 在修改任何 OpenClaw 配置文件之前，先查官方最新文档
- Before using an OpenClaw feature you are not fully sure about, read the official docs first
- 当需要使用某个不完全确定的 OpenClaw 功能时，先阅读官方文档
- Before generating configuration examples, commands, setup steps, or integration instructions
- 在生成配置示例、命令示例、接入步骤或集成说明之前
- When answering questions about config, CLI, channels, gateway, skills, diagnostics, deployment, or operations
- 当需要回答配置、CLI、渠道、Gateway、Skills、诊断、部署或运维相关问题时
- When stale memory could lead to hallucinated, outdated, or incompatible OpenClaw guidance
- 当模型的过时记忆可能导致错误、过时或版本不兼容的 OpenClaw 指导时

## High-Risk Rule | 高风险任务规则

- If the task involves config changes, command generation, gateway or skills parameter adjustment, channel integration, or operational guidance, verify the latest official docs first instead of relying on memory
- 如果任务涉及配置修改、命令生成、Gateway 或 Skills 参数调整、渠道接入或运维指导，应先核对官方最新文档，而不是依赖模型记忆

## Example Questions | 示例问题

- How do I configure an OpenClaw skill?
- 如何配置 OpenClaw 的 Skill？
- Where is the latest documentation for channels or gateway setup?
- 最新的渠道接入或 Gateway 配置文档在哪里？
- What does the official doc say about diagnostics or deployment options?
- 官方文档对诊断或部署选项是怎么说明的？
- Can you find the current OpenClaw CLI documentation and summarize it?
- 能帮我找到当前的 OpenClaw CLI 文档并做个总结吗？

## Safety Notes | 安全说明

- This skill is intended for public documentation lookup only
- 此技能仅用于公开文档检索
- It does not request secrets, credentials, or local private files
- 不会请求密钥、凭证或本地私有文件
- It avoids bulk site mirroring and is designed for on-demand retrieval
- 不会批量镜像整个站点，而是以按需检索为主
