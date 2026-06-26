---
name: newslatest
description: 获取各大平台热点新闻榜单数据。通过 Rust NewsLatest 服务 API 获取新闻热点，支持多个新闻源。触发场景：(1) 用户请求"热点新闻"、"热搜榜"、"热门话题"；(2) 指定平台新闻如"知乎热搜"、"B站热门"、"微博热搜"等；(3) 获取某平台的热门内容。
---

# NewsLatest 新闻热点

通过 Rust 服务获取各大平台的热点新闻榜单。

## API 基础

- **Base URL**: `https://newslatest-server.up.railway.app`
- **端点**: `GET /news/{source}`
- **参数**: `no_cache=false`（可选，强制刷新缓存）

## 支持的新闻源（共16个）

| source | 名称 | 分类 |
|--------|------|------|
| `bilibili` | 哔哩哔哩 | 娱乐/视频 |
| `weibo` | 微博 | 社交/热搜 |
| `zhihu` | 知乎 | 问答/热榜 |
| `github` | GitHub | 技术/开源 |
| `juejin` | 掘金 | 技术/开发者 |
| `douyin` | 抖音 | 娱乐/短视频 |
| `36kr` | 36氪 | 科技/创业 |
| `ithome` | IT之家 | 科技/数码 |
| `segmentfault` | SegmentFault | 技术/开发者 |
| `oschina` | 开源中国 | 技术/开源 |
| `infoq` | InfoQ | 技术/架构 |
| `ruanyifeng` | 阮一峰博客 | 技术/周刊 |
| `csdn` | CSDN | 技术/博客 |
| `stcn` | 证券时报 | 财经/股市 |
| `caixin` | 财新网 | 财经/新闻 |
| `baidu` | 百度 | 综合/热搜 |

## 使用方式

### 1. 调用 API 获取数据

**单平台调用**：
```
https://newslatest-server.up.railway.app/news/{source}
```

**综合新闻调用（新增）**：
```
https://newslatest-server.up.railway.app/news/combined?sources=baidu,weibo,zhihu
```
- `sources` 参数支持多个平台，用逗号分隔
- 推荐组合：baidu,weibo,zhihu（综合热搜）
- 其他组合：github,juejin,ithome（技术热点）

### 2. 解析响应

**单平台响应 JSON 结构**：

```json
{
  "success": true,
  "data": {
    "title": "平台名称",
    "description": "平台描述",
    "name": "source名",
    "total": 20,
    "ttl_minutes": 45,
    "update_time": "2026-03-25T06:00:00Z",
    "items": [
      {
        "title": "标题",
        "desc": "简介",
        "author": "作者",
        "cover": "封面图URL",
        "hot": 热度值,
        "url": "链接地址",
        "mobile_url": "移动端链接"
      }
    ]
  }
}
```

**综合新闻响应 JSON 结构**（combined API）：

```json
{
  "success": true,
  "data": {
    "data": {
      "baidu": {
        "title": "百度热搜",
        "description": "百度实时热搜榜单",
        "name": "baidu",
        "total": 20,
        "ttl_minutes": 5,
        "update_time": "2026-03-26T00:56:28.694128858+00:00",
        "items": [
          {
            "id": "1",
            "title": "标题",
            "desc": "简介",
            "author": "作者",
            "cover": "封面图URL",
            "hot": 热度值,
            "url": "链接地址",
            "mobile_url": "移动端链接"
          }
        ]
      },
      "weibo": { ... },
      "zhihu": { ... }
    },
    "sources": ["baidu", "weibo", "zhihu"],
    "total_items": 60
  }
}
```

### 3. 格式化输出

从 `data.items` 提取新闻列表，按热度值降序排列，按以下格式输出：

```
📊 {平台名称} 热榜 - 更新于 {update_time}
---
1. {标题} (热度: {热度})
{描述}
{外部链接}
2. {标题} (热度: {热度})
{描述}
{外部链接}
...
```

**格式说明**：
- 每条新闻占3行
- 第1行：序号 + 标题 + 热度
- 第2行：描述（desc 字段，如果为空则显示"暂无描述"）
- 第3行：外部链接（mobile_url）

**处理规则**：
- 如果 desc 为空或 null，显示"暂无描述"
- 如果 hot 为空或 null，显示"热度: 暂无"
- 取 mobile_url 作为外部连接，如果没有则用 url

## 示例输出

```
📊 知乎热榜 - 更新于 2026-03-25 14:59

1. 如何看待郑钦文因为球童递错毛巾要求换回，被外网球迷批评？ (热度 1044)
2. 纹身店称可免费给65岁以上老人纹联系方式，防止失智老人走丢 (热度 244)
3. 杨过为什么一次次救郭芙，断臂了也不报仇？ (热度 205)
...
```

## 多平台聚合

用户若请求"今日热点"或"综合热搜"，可同时拉取多个平台（建议：baidu + weibo + zhihu），合并展示。

## 注意事项

- 每次请求间隔建议 >= 30 秒，避免频繁调用
- `no_cache=fasle` 默认使用缓存数据
- `ttl_minutes` 字段表示缓存有效时间
- 优先使用 `web_fetch` 工具调用 API
- 若 API 返回 `success: false`，提示用户稍后重试
