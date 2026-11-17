---
name: ola-cp-recommendations
title: Cruise Product Recommendations
description: 根据用户的偏好和历史选择，为您推荐最适合的邮轮产品，确保您找到理想的航行体验。
kind: MCP
version: 0.1.0
published_with: cruiseskillbridge
---

# Cruise Product Recommendations

> 根据用户的偏好和历史选择，为您推荐最适合的邮轮产品，确保您找到理想的航行体验。

这是一个 **MCP** 技能，通过 [CruiseSkillBridge](https://cruiseskillbridge.com) 一键发布。

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
{ "input": "...", "skill": "ola-cp-recommendations" }
```

> 发布到 CruiseSkillBridge 后，上述 URL 会自动替换为网关地址，调用将计入控制台统计。

## 关于

由 [CruiseSkillBridge](https://cruiseskillbridge.com) 发布 —— 全球唯一邮轮领域技能 分发 · 发布 · 洞察：
一键发布、分发洞察、网关调用统计。

## 已发布的 MCP Tools

以下 Tools 已纳入 CruiseSkillBridge 发布与统计：

- **product_search** — 按关键词搜索邮轮产品。

> MCP 接入经 CruiseSkillBridge 网关转发，remotes URL 已自动替换，无需手动配置。
