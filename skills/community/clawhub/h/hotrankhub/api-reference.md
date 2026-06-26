# API 参考文档

本文档提供 HotRank Hub API 的完整参考，包括所有端点、请求/响应格式、错误码等信息。

## 目录

1. [基础信息](#基础信息)
2. [认证](#认证)
3. [端点列表](#端点列表)
4. [响应格式](#响应格式)
5. [错误码](#错误码)
6. [速率限制](#速率限制)
7. [最佳实践](#最佳实践)

---

## 基础信息

### 基础 URL

```
https://airouter.tech/api
```

### 支持的协议

- HTTPS (推荐)
- HTTP (仅用于开发环境)

### 数据格式

- **请求格式**: 无需特殊格式，直接 GET 请求
- **响应格式**: JSON (UTF-8 编码)
- **缓存策略**: 服务端缓存 5 分钟

---

## 认证

HotRank Hub API 目前**不需要认证**，可以直接调用。

未来可能会根据使用情况添加可选的 API Key 认证，用于：
- 更高的速率限制
- 访问高级功能
- 使用统计和分析

---

## 端点列表

### 1. 获取热榜数据

获取指定平台的热榜数据。

```
GET /api/{source_id}
```

#### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `source_id` | string | 是 | 数据源 ID，如 `weibo`、`zhihu` |

#### 查询参数

无

#### 请求示例

```bash
# 获取微博热搜
curl https://airouter.tech/api/weibo

# 获取知乎热榜
curl https://airouter.tech/api/zhihu

# 获取 GitHub 趋势
curl https://airouter.tech/api/github-trending
```

#### 响应示例

```json
{
  "code": 200,
  "msg": "请求成功",
  "data": [
    {
      "id": "1",
      "title": "热搜标题",
      "desc": "热搜描述内容",
      "hot": 1000000,
      "url": "https://weibo.com/search?q=...",
      "mobileUrl": "https://m.weibo.com/search?q=..."
    },
    {
      "id": "2",
      "title": "第二条热搜",
      "desc": "描述信息",
      "hot": 800000,
      "url": "https://weibo.com/search?q=...",
      "mobileUrl": "https://m.weibo.com/search?q=..."
    }
  ],
  "timestamp": 1709500000000
}
```

---

### 2. 完整数据源列表

支持的 47 个数据源，详见 `sources.json` 文件。

#### 按类别分类

**社交媒体 (Social)**
- `weibo` - 微博热搜
- `zhihu` - 知乎热榜
- `zhihu-daily` - 知乎日报
- `baidu` - 百度热搜
- `baidutieba` - 百度贴吧
- `xiaohongshu` - 小红书
- `quark` - 夸克热搜

**短视频/视频 (Video)**
- `douyin` - 抖音热点
- `kuaishou` - 快手热榜
- `bilibili` - B站热门
- `qqvideo` - 腾讯视频

**科技资讯 (Tech)**
- `github` - GitHub 今日热榜
- `github-trending` - GitHub 趋势
- `hello-github` - HelloGitHub
- `juejin` - 掘金
- `csdn` - CSDN
- `v2ex` - V2EX
- `hackernews` - Hacker News
- `ithome` - IT之家
- `36kr` - 36氪
- `huxiu` - 虎嗅
- `sspai` - 少数派
- `ifanr` - 爱范儿
- `coolapk` - 酷安
- `freebuf` - FreeBuf
- `linuxdo` - Linux.do

**财经新闻 (Finance)**
- `xueqiu` - 雪球
- `wallstreetcn` - 华尔街见闻
- `jin10` - 金十数据
- `cls` - 财联社

**游戏娱乐 (Entertainment)**
- `steam` - Steam 热销
- `hupu` - 虎扑
- `douban-movic` - 豆瓣电影
- `lol` - 英雄联盟
- `netease-music` - 网易云音乐
- `qq` - QQ音乐

**新闻资讯 (News)**
- `toutiao` - 今日头条
- `netease` - 网易新闻
- `thepaper` - 澎湃新闻
- `cankaoxiaoxi` - 参考消息

**生活方式 (Lifestyle)**
- `weread` - 微信读书
- `smzdm` - 什么值得买
- `dongchedi` - 懂车帝
- `history-today` - 历史上的今天

**社区论坛 (Community)**
- `woshipm` - 人人都是产品经理

---

## 响应格式

### 成功响应

```typescript
{
  code: 200;
  msg: string;
  data: HotListItem[];
  timestamp: number;
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | number | 状态码，200 表示成功 |
| `msg` | string | 响应消息 |
| `data` | array | 热榜数据列表 |
| `timestamp` | number | 时间戳（毫秒） |

### 热榜条目字段

每个热榜条目 (`HotListItem`) 包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string/number | 是 | 唯一标识 |
| `title` | string | 是 | 热搜标题 |
| `desc` | string | 否 | 热搜描述 |
| `hot` | number/string | 否 | 热度值 |
| `url` | string | 否 | PC 端链接 |
| `mobileUrl` | string | 否 | 移动端链接 |

### TypeScript 类型定义

```typescript
interface ApiResponse<T = HotListItem[]> {
  code: number;
  msg: string;
  data: T;
  timestamp: number;
}

interface HotListItem {
  id: string | number;
  title: string;
  desc?: string;
  hot?: number | string;
  url?: string;
  mobileUrl?: string;
}
```

---

## 错误码

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 404 | 资源不存在（无效的数据源 ID） |
| 500 | 服务器内部错误 |
| 503 | 服务暂时不可用 |

### API 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 404 | 数据源不存在 |
| 500 | 服务器内部错误 |

### 错误响应示例

#### 无效的数据源

```json
{
  "code": 404,
  "msg": "数据源不存在",
  "data": null,
  "timestamp": 1709500000000
}
```

#### 服务器错误

```json
{
  "code": 500,
  "msg": "服务器内部错误",
  "data": null,
  "timestamp": 1709500000000
}
```

---

## 速率限制

### 当前限制

- **无严格限制**：目前 API 没有严格的速率限制
- **建议频率**：建议每分钟不超过 60 次请求
- **缓存策略**：数据每 5 分钟更新一次

### 最佳实践

1. **实现本地缓存**：避免重复请求相同数据
2. **批量获取**：使用并发请求获取多个平台数据
3. **错误重试**：实现指数退避重试机制
4. **合理间隔**：避免过于频繁的轮询

### 未来计划

可能会根据使用情况添加：
- 基于用户级别的速率限制
- API Key 认证机制
- 更细粒度的访问控制

---

## 最佳实践

### 1. 错误处理

```javascript
async function getHotList(source) {
  try {
    const response = await fetch(`https://airouter.tech/api/${source}`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    if (data.code !== 200) {
      throw new Error(`API Error: ${data.msg}`);
    }

    return data.data;
  } catch (error) {
    console.error(`获取 ${source} 热榜失败:`, error);
    return [];
  }
}
```

### 2. 本地缓存

```javascript
const CACHE_KEY = 'hotrankhub_cache';
const CACHE_TIME = 5 * 60 * 1000; // 5分钟

async function getHotListWithCache(source) {
  const cache = localStorage.getItem(`${CACHE_KEY}_${source}`);
  if (cache) {
    const { data, timestamp } = JSON.parse(cache);
    if (Date.now() - timestamp < CACHE_TIME) {
      return data;
    }
  }

  const response = await fetch(`https://airouter.tech/api/${source}`);
  const data = await response.json();

  localStorage.setItem(`${CACHE_KEY}_${source}`, JSON.stringify({
    data: data.data,
    timestamp: Date.now()
  }));

  return data.data;
}
```

### 3. 并发请求

```javascript
async function fetchMultipleSources(sources) {
  const results = await Promise.allSettled(
    sources.map(source =>
      fetch(`https://airouter.tech/api/${source}`)
        .then(r => r.json())
    )
  );

  return results.map((result, i) => ({
    source: sources[i],
    status: result.status,
    data: result.status === 'fulfilled' ? result.value.data : null,
    error: result.status === 'rejected' ? result.reason.message : null
  }));
}
```

### 4. 请求去重

```javascript
const pendingRequests = new Map();

async function dedupedFetch(source) {
  if (pendingRequests.has(source)) {
    return pendingRequests.get(source);
  }

  const promise = fetch(`https://airouter.tech/api/${source}`)
    .then(r => r.json())
    .finally(() => {
      pendingRequests.delete(source);
    });

  pendingRequests.set(source, promise);
  return promise;
}
```

---

## 常见问题

### Q: 数据多久更新一次？

A: 所有数据源每 5 分钟自动更新一次。

### Q: 为什么有些平台数据获取失败？

A: 可能原因：
- 平台接口变更
- 网络请求超时
- 数据源暂时不可用

建议实现错误处理和重试机制。

### Q: 支持哪些浏览器？

A: API 支持所有现代浏览器：
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Q: 如何获取历史数据？

A: 目前不支持历史数据查询，仅提供实时热榜数据。

---

## 更新日志

### v1.0.0 (2026-03-19)

- 初始版本发布
- 支持 47 个数据源
- 提供标准化 JSON API
- 实现服务端缓存

---

## 技术支持

如有问题或建议，请联系：

- **网站**: https://airouter.tech
- **文档**: [SKILL.md](./SKILL.md)
- **示例**: [examples.md](./examples.md)