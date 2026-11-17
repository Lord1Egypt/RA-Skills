---
name: ola-tool-cruise-finder
title: Cruise Finder Tool
description: A powerful tool that assists users in finding the best cruises based on their preferences and requirements.
kind: Tool
version: 0.1.0
published_with: cruiseskillbridge
---

# Cruise Finder Tool

> A powerful tool that assists users in finding the best cruises based on their preferences and requirements.

这是一个 **Tool** 技能，通过 [CruiseSkillBridge](https://cruiseskillbridge.com) 一键发布。

## 能力

- 描述这个技能能做什么（请替换为你的真实内容）。
- 列出关键输入与输出。
- 说明适用场景。

## 用法

当需要提交分析请求时，向以下 API 发送 **POST** 请求（JSON body）：

```
https://httpbin.org/post
```

示例 body：

```json
{ "input": "...", "skill": "ola-tool-cruise-finder" }
```

> 发布到 CruiseSkillBridge 后，上述 URL 会自动替换为网关地址，调用将计入控制台统计。

## 关于

由 [CruiseSkillBridge](https://cruiseskillbridge.com) 发布 —— 全球唯一邮轮领域技能 分发 · 发布 · 洞察：
一键发布、分发洞察、网关调用统计。

## 已发布的 MCP Tools

以下 Tools 已纳入 CruiseSkillBridge 发布与统计：

- **product_search** — 按关键词搜索邮轮产品。

> MCP 接入经 CruiseSkillBridge 网关转发，remotes URL 已自动替换，无需手动配置。

## CruiseSkillBridge 网关 API（发布时自动注入）

以下地址已替换为 CruiseSkillBridge 网关，调用将自动计量：

- **invoke** (*)
  - 网关：`https://cruise-mcp.olavacations.com/api/gw/s/4e6b4800-96f1-48f6-bf19-4dcb946cab31/invoke`
  - 上游：`https://cruise-mcp.olavacations.com/api/gw/mcp/4e6b4800-96f1-48f6-bf19-4dcb946cab31`
