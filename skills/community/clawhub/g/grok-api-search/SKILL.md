---
name: grok-api-search
description: 使用 Grok API 进行网络搜索。默认使用中转端点节省成本。
author: jarvis
license: MIT
tags:
  - search
  - grok
  - web
  - api
---

# Grok API 搜索技能

使用 Grok 模型的网络搜索能力，获取实时信息。默认使用中转 API 端点，成本更低。

## 功能

- 实时网络搜索
- 默认使用中转 API（节省成本）
- 返回带来源的搜索结果

## 中转 API 配置教程

### 什么是中转 API？

中转 API 是第三方提供的 API 代理服务，相比官方 API 有以下优势：

- 成本更低（通常 5-7 折）
- 国内网络直连，更稳定
- 无需配置代理

### 推荐中转服务

**apipro.maynor1024.live**（默认）

网站：https://apipro.maynor1024.live/

### 配置方式

**方式一：使用中转 API（推荐）**

```
export GROK_API_KEY="your-api-key"
```

获取 API Key：
1. 访问 https://apipro.maynor1024.live/
2. 注册账号
3. 获取 API Key

**方式二：使用官方 xAI API**

```
export GROK_API_KEY="your-xai-api-key"
export GROK_API_URL="https://api.x.ai/v1"
```

获取方式：访问 https://console.x.ai/

注意：官方 API 需要科学上网。

**方式三：使用其他中转服务**

支持任何 OpenAI 兼容的中转服务：

```
export GROK_API_KEY="your-api-key"
export GROK_API_URL="https://your-proxy.com/v1"
```

## 使用方法

```
./grok-search.sh "搜索内容"
```

## 触发场景

- 用户说"搜索xxx"
- 用户需要实时信息
- 用户问最新新闻

## 常见问题

### Q: 中转 API 安全吗？

A: 选择可信的中转服务很重要。apipro.maynor1024.live 是社区常用的中转服务。

### Q: 为什么推荐中转？

A: 
- 官方 API 需要国外网络
- 国内访问不稳定
- 中转服务通常更便宜

### Q: 支持中文搜索吗？

A: 完全支持！Grok 对中文理解很好。
