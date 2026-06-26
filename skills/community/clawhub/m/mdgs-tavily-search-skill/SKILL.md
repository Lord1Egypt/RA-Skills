---
name: mdgs-tavily-search-skill
description: 使用 Tavily API 进行网络搜索、网页内容提取、抓取、映射和研究。当用户需要搜索信息、获取网页内容、从网站抓取数据、绘制网站地图或进行深度研究时使用此技能。AI 应根据任务自动选择最合适的模式。
---

# Mdgs Tavily Search Skill

使用 Tavily API 进行网络搜索和信息提取。

## 快速开始

### 前置要求

首先安装依赖：
```bash
npm install @tavily/core
```

设置 API Key：
```bash
export TAVILY_API_KEY="tvly-your-api-key"
```

### 初始化客户端

```javascript
const { tavily } = require("@tavily/core");

const apiKey = process.env.TAVILY_API_KEY;
if (!apiKey) {
  throw new Error("请配置 TAVILY_API_KEY 环境变量。访问 https://tavily.com 获取 API Key");
}

const tvly = tavily({ apiKey });
```

## 模式选择指南

AI 应根据任务类型自动选择合适的模式：

| 任务类型 | 推荐模式 | 说明 |
|---------|---------|------|
| 快速问答、信息检索 | search | 获取搜索结果和答案 |
| 获取特定网页内容 | extract | 提取单个 URL 的主要内容 |
| 批量抓取网站内容 | crawl | 抓取整个网站或多个页面 |
| 了解网站结构 | map | 获取网站的页面地图 |
| 深度研究主题 | research | 综合多个来源的深度研究 |

## 模式详解

### 1. 搜索网页 (search)

适用于：快速问答、信息检索、新闻搜索

```javascript
const response = await tvly.search("Who is Leo Messi?");
console.log(response);
```

**选项：**
```javascript
const response = await tvly.search("Python 教程", {
  searchDepth: "basic", // "basic" 或 "advanced"
  maxResults: 10,
  includeAnswer: true,
  includeRawContent: false,
  includeImages: false
});
```

### 2. 提取网页 (extract)

适用于：获取特定网页的详细内容

```javascript
const response = await tvly.extract("https://en.wikipedia.org/wiki/Artificial_intelligence");
console.log(response);
```

**选项：**
```javascript
const response = await tvly.extract("https://example.com", {
  includeImages: true
});
```

### 3. 抓取网页 (crawl)

适用于：批量抓取网站内容、深度内容获取

```javascript
const response = await tvly.crawl("https://docs.tavily.com", { 
  instructions: "Find all pages on the Python SDK" 
});
console.log(response);
```

**选项：**
```javascript
const response = await tvly.crawl("https://example.com", {
  instructions: "提取所有产品页面",
  maxDepth: 2,
  maxPages: 10
});
```

### 4. 绘制网页映射 (map)

适用于：了解网站结构、发现相关页面

```javascript
const response = await tvly.map("https://docs.tavily.com");
console.log(response);
```

**选项：**
```javascript
const response = await tvly.map("https://example.com", {
  depth: 2,
  maxPages: 20
});
```

### 5. 创建研究任务 (research)

适用于：深度研究、综合多来源分析

```javascript
const response = await tvly.research("What are the latest developments in AI?");
console.log(response);
```

**选项：**
```javascript
const response = await tvly.research("最新 AI 发展动态", {
  depth: "extensive", // "basic" 或 "extensive"
  maxSources: 10
});
```

## 使用脚本

项目提供了封装好的脚本：

### 搜索
```bash
node scripts/tavily.js search "搜索内容" [--depth basic|advanced] [--max-results N]
```

### 提取
```bash
node scripts/tavily.js extract "https://example.com"
```

### 抓取
```bash
node scripts/tavily.js crawl "https://example.com" --instructions "提取所有页面"
```

### 映射
```bash
node scripts/tavily.js map "https://example.com" [--depth N]
```

### 研究
```bash
node scripts/tavily.js research "研究主题" [--depth basic|extensive]
```

## API Key 配置

**重要：** 使用此技能前必须配置 API Key。

1. 访问 [tavily.com](https://tavily.com) 注册账号
2. 获取 API Key
3. 设置环境变量：
   ```bash
   export TAVILY_API_KEY="tvly-your-actual-api-key"
   ```

或在脚本/代码中直接传入：
```javascript
const tvly = tavily({ apiKey: "tvly-your-actual-api-key" });
```

## 响应格式

### search response
```json
{
  "answer": "回答文本",
  "results": [{ "title": "", "url": "", "content": "", "score": 0.95 }],
  "images": []
}
```

### extract response
```json
{
  "results": [{ "url": "", "content": "", "raw_content": "" }]
}
```

### crawl response
```json
{
  "results": [{ "url": "", "content": "" }]
}
```

### map response
```json
{
  "results": [{ "url": "", "title": "" }]
}
```

### research response
```json
{
  "answer": "综合研究报告",
  "findings": [{ "content": "", "sources": [] }]
}
```
