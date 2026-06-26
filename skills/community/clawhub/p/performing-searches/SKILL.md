---
name: "performing-searches"
description: "Provides concurrent web search and code search capabilities for Agents with hybrid retrieval. Supports searching multiple keywords simultaneously, Embedding re-ranking to improve relevance to ~80%. Use when users need to search the web, look up programming documentation, or mention SearXNG, MCP search, or local search."
version: "1.1.2"
author: "sebrinass"
tags: ["search", "mcp", "searxng", "agent", "local"]
category: "search"
env:
  required:
    - name: "SEARXNG_URL"
      description: "SearXNG 实例地址"
      example: "http://localhost:8080"
  optional:
    - name: "EMBEDDING_API_KEY"
      description: "Embedding API 密钥（启用混合检索）"
    - name: "EMBEDDING_BASE_URL"
      description: "Embedding API 端点（OpenAI 兼容）"
    - name: "MCP_HTTP_PORT"
      description: "HTTP 模式端口"
      default: "3000"
    - name: "SEARCH_TIMEOUT_MS"
      description: "搜索超时（毫秒）"
      default: "30000"
    - name: "CONTEXT7_API_KEY"
      description: "Context7 API Key（代码搜索）"
source: "https://github.com/sebrinass/mcp-augmented-search"
homepage: "https://github.com/sebrinass/mcp-augmented-search"
---

# Augmented Search

为 Agent 提供高效的本地联网搜索和代码搜索能力。

## 快速开始

**前置条件**: SearXNG 实例（必需）

**Docker 方式（推荐）**:

```bash
docker run -d --name searxng -p 8080:8080 searxng/searxng:latest
docker run -d --name augmented-search -p 3000:3000 \
  -e SEARXNG_URL=http://host.docker.internal:8080 \
  ghcr.io/sebrinass/mcp-augmented-search:latest
```

**npm 方式**:

```bash
npm install -g augmented-search
SEARXNG_URL=http://localhost:8080 augmented-search
```

## 提供的工具

### search — 思考 + 并发搜索

支持混合检索和链接去重，一次请求最多搜索 3 个关键词。

**必填参数：**
- `thought` — 当前思考内容
- `thoughtNumber` — 当前思考步骤编号
- `totalThoughts` — 预计总思考步骤数
- `nextThoughtNeeded` — 是否需要继续思考

**可选参数：**
- `searchedKeywords` — 搜索关键词列表（最多 3 个并发）
- `site` — 限制搜索域名

### read — URL 内容提取

读取网页内容，支持 JS 渲染降级和正文提取。

**参数：**
- `urls` — URL 数组
- `startChar` / `maxLength` — 分页读取
- `section` — 提取指定章节
- `paragraphRange` — 段落范围
- `readHeadings` — 仅返回标题列表

### library_search — 搜索编程库

搜索编程库，获取 Context7 兼容的库 ID。

**参数：**
- `query` — 用户问题（用于相关性排序）
- `libraryName` — 库名，如 `react`

### library_docs — 查询库文档

查询库的文档和代码示例。

**参数：**
- `libraryId` — 库 ID，如 `/facebook/react`
- `query` — 用户问题

## 配置

### 必填

| 变量 | 说明 |
|------|------|
| `SEARXNG_URL` | SearXNG 实例地址 |

### 常用可选

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `EMBEDDING_BASE_URL` | - | Embedding API 端点（启用混合检索） |
| `MCP_HTTP_PORT` | - | HTTP 模式端口 |
| `SEARCH_TIMEOUT_MS` | 30000 | 搜索超时（毫秒） |

完整配置请参阅 [GitHub 仓库配置文档](https://github.com/sebrinass/mcp-augmented-search/blob/main/docs/configuration.md)。

## 性能建议

| 模式 | 页数 | 超时 | 相关性 |
|------|------|------|--------|
| 纯文本 | 1 | 10-15秒 | ~50% |
| 混合检索 | 3 | 30-60秒 | ~80% |

**其他建议：**
- 搜索关键词并发不超过 3 个
- 在 SearXNG 配置中过滤视频网站以提升结果质量

## 工具使用示例

### 使用 mcporter 调用

```bash
# 列出工具
mcporter list http://localhost:3000/mcp

# 调用搜索
mcporter call http://localhost:3000/mcp.search \
  thought="搜索测试" \
  thoughtNumber=1 \
  totalThoughts=1 \
  nextThoughtNeeded=false \
  searchedKeywords='["hello world"]'

# 调用 URL 读取
mcporter call http://localhost:3000/mcp.read \
  urls='["https://example.com"]'

# 调用代码库搜索
mcporter call http://localhost:3000/mcp.library_search \
  query="如何使用 React hooks" \
  libraryName="react"

# 调用代码文档查询
mcporter call http://localhost:3000/mcp.library_docs \
  libraryId="/facebook/react" \
  query="useEffect cleanup"
```

### 使用 REST API

```bash
# 健康检查
curl http://localhost:3000/health

# 搜索
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"thought":"测试","thoughtNumber":1,"totalThoughts":1,"nextThoughtNeeded":false,"searchedKeywords":["hello"]}'

# 读取 URL
curl -X POST http://localhost:3000/api/read \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://example.com"]}'
```

## 详细安装

完整安装指南请参阅 [GitHub 安装文档](https://github.com/sebrinass/mcp-augmented-search/blob/main/skill/reference/installation.md)，包含：
- Docker 完整安装
- npm + 已有 SearXNG
- SearXNG 配置详解
- OpenClaw 集成
- 常见问题

## 资源链接

- [安装指南](https://github.com/sebrinass/mcp-augmented-search/blob/main/skill/reference/installation.md) — 完整安装说明
- [配置参考](https://github.com/sebrinass/mcp-augmented-search/blob/main/docs/configuration.md) — 完整环境变量说明
- [GitHub 仓库](https://github.com/sebrinass/mcp-augmented-search)
- [SearXNG 文档](https://docs.searxng.org)
- [Docker 镜像](https://ghcr.io/sebrinass/mcp-augmented-search)
