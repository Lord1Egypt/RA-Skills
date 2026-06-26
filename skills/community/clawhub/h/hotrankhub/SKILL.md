---
name: hotrank-hub
description: 聚合 47 个平台热榜数据的 API 服务
version: 1.0.0
author: HotRank Hub Team
---

# HotRank Hub - 热榜数据 API 服务

## 概述

HotRank Hub 是一个聚合全网热榜数据的 API 服务，提供 **47 个平台**的实时热搜、热榜数据。通过标准化的 HTTP API，您可以轻松获取微博、知乎、抖音、B站、GitHub 等平台的热门内容。

## 核心能力

### 📊 数据聚合

- **47 个数据源**：覆盖社交媒体、科技资讯、财经新闻、游戏娱乐等多个领域
- **实时更新**：数据每5分钟自动更新，确保获取最新热点
- **标准化格式**：统一的数据结构，易于集成和解析

### 🔍 平台覆盖

HotRank Hub 聚合 **47 个平台**的热榜数据，完整列表如下：

**社交媒体（7个）**：微博热搜、知乎热榜、知乎日报、百度热搜、百度贴吧、小红书、夸克热搜

**短视频/视频（4个）**：抖音热点、快手热榜、B站热门、腾讯视频

**科技资讯（16个）**：GitHub、GitHub趋势、HelloGitHub、掘金、CSDN、V2EX、Linux.do、Hacker News、IT之家、36氪、虎嗅、少数派、爱范儿、酷安、FreeBuf

**财经新闻（4个）**：雪球、华尔街见闻、金十数据、财联社

**游戏娱乐（6个）**：Steam、虎扑、豆瓣电影、英雄联盟、网易云音乐、QQ音乐

**新闻资讯（4个）**：今日头条、网易新闻、澎湃新闻、参考消息

**生活方式（4个）**：微信读书、什么值得买、懂车帝、历史上的今天

**社区论坛（2个）**：人人都是产品经理

**共计 47 个数据源，覆盖中文互联网主流平台。**

## API 基础信息

### 基础 URL

```
https://airouter.tech/api
```

### 响应格式

所有 API 返回 **JSON 格式**，包含以下字段：

```typescript
{
  "code": 200,          // 状态码
  "msg": "请求成功",     // 响应消息
  "data": [...],        // 热榜数据列表
  "timestamp": 1709500000000  // 时间戳
}
```

### 数据字段

每个热榜条目包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string/number | 唯一标识 |
| `title` | string | 热搜标题 |
| `desc` | string | 热搜描述 |
| `hot` | number/string | 热度值 |
| `url` | string | PC端链接 |
| `mobileUrl` | string | 移动端链接 |

## 核心工具

### 1. 获取热榜数据

```
GET /api/{source_id}
```

**参数：**
- `source_id` (路径参数)：数据源 ID，如 `weibo`、`zhihu`、`bilibili`

**示例：**

```bash
# 获取微博热搜
curl https://airouter.tech/api/weibo

# 获取知乎热榜
curl https://airouter.tech/api/zhihu
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "请求成功",
  "data": [
    {
      "id": "1",
      "title": "热搜标题",
      "desc": "热搜描述",
      "hot": 1000000,
      "url": "https://weibo.com/...",
      "mobileUrl": "https://weibo.com/..."
    }
  ],
  "timestamp": 1709500000000
}
```

### 2. 数据源列表

完整的 47 个数据源列表请参考 `sources.json` 文件。

每个数据源包含：
- `id`：数据源唯一标识
- `name`：平台名称
- `category`：类别分类
- `apiPath`：API 端点路径

## 使用示例

### 基础示例

```javascript
// 获取微博热搜
const response = await fetch('https://airouter.tech/api/weibo');
const data = await response.json();
console.log(data);

// 获取 GitHub 趋势
const githubData = await fetch('https://airouter.tech/api/github-trending');
const trending = await githubData.json();
```

### 高级示例

#### 跨平台对比

```javascript
// 对比微博和知乎的热榜
const [weibo, zhihu] = await Promise.all([
  fetch('https://airouter.tech/api/weibo').then(r => r.json()),
  fetch('https://airouter.tech/api/zhihu').then(r => r.json())
]);

// 找出共同热点
const weiboTitles = new Set(weibo.data.map(item => item.title));
const common = zhihu.data.filter(item => weiboTitles.has(item.title));
```

#### 生成热点报告

```javascript
// 获取多个平台数据并生成报告
const platforms = ['weibo', 'zhihu', 'douyin'];
const reports = await Promise.all(
  platforms.map(p =>
    fetch(`https://airouter.tech/api/${p}`)
      .then(r => r.json())
  )
);

// 汇总分析
const summary = reports.map((report, i) => ({
  platform: platforms[i],
  topItems: report.data.slice(0, 5)
}));
```

## 最佳实践

### 1. 缓存策略

**Why:** 减少不必要的 API 调用，提升响应速度

**How:**

```javascript
const CACHE_KEY = 'hotrankhub_cache';
const CACHE_TIME = 5 * 60 * 1000; // 5分钟

async function getHotList(source) {
  const cache = localStorage.getItem(`${CACHE_KEY}_${source}`);
  if (cache) {
    const { data, timestamp } = JSON.parse(cache);
    if (Date.now() - timestamp < CACHE_TIME) {
      return data;
    }
  }

  const response = await fetch(`/api/${source}`);
  const data = await response.json();

  localStorage.setItem(`${CACHE_KEY}_${source}`, JSON.stringify({
    data,
    timestamp: Date.now()
  }));

  return data;
}
```

### 2. 错误处理

**Why:** 确保应用的健壮性和用户体验

**How:**

```javascript
try {
  const response = await fetch('/api/weibo');
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  const data = await response.json();
  // 处理数据
} catch (error) {
  console.error('获取热榜失败:', error);
  // 显示友好的错误提示
  showToast('获取数据失败，请稍后重试');
}
```

### 3. 并发请求

**Why:** 提升多平台数据获取效率

**How:**

```javascript
// 同时获取多个平台数据
const sources = ['weibo', 'zhihu', 'bilibili'];
const results = await Promise.allSettled(
  sources.map(s => fetch(`/api/${s}`).then(r => r.json()))
);

// 处理结果
results.forEach((result, i) => {
  if (result.status === 'fulfilled') {
    console.log(`${sources[i]}: ${result.value.data.length} items`);
  } else {
    console.error(`${sources[i]} failed:`, result.reason);
  }
});
```

## 限制与注意事项

- **缓存时间**：API 默认缓存 5 分钟
- **请求频率**：建议合理控制请求频率，避免过度调用
- **数据准确性**：数据来源于第三方平台，不保证 100% 准确

## 技术支持

如有问题，请联系：
- **网站**：https://airouter.tech
- **文档**：完整 API 文档请参考 `api-reference.md`
- **示例**：更多使用示例请参考 `examples.md`