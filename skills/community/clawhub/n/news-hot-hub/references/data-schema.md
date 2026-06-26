# 数据格式规范

## 目录

1. [通用输出格式](#通用输出格式)
2. [知乎数据格式](#知乎数据格式)
3. [微博数据格式](#微博数据格式)
4. [今日头条数据格式](#今日头条数据格式)
5. [V2EX 数据格式](#v2ex-数据格式)
6. [36氪数据格式](#36氪数据格式)
7. [AIBase 数据格式](#aibase-数据格式)
8. [聚合输出格式](#聚合输出格式)
9. [错误格式](#错误格式)

---

## 通用输出格式

所有平台脚本的标准输出遵循统一的 JSON 结构：

```json
{
  "type": "<data_type>",
  "timestamp": "YYYY-MM-DD HH:MM:SS ±HHMM",
  "count": <int>,
  "data": [...]
}
```

| 字段        | 类型   | 说明                                            |
| ----------- | ------ | ----------------------------------------------- |
| `type`      | string | 数据类型标识（如 `hot_search`, `hot_question`） |
| `timestamp` | string | 获取时间，带时区                                |
| `count`     | int    | data 数组元素数量                               |
| `data`      | array  | 数据条目数组                                    |

### 输出约定

- JSON 输出到 **stdout**
- 错误信息输出到 **stderr**
- 退出码：`0` 成功，`1` 失败
- 编码：UTF-8，`ensure_ascii=False`

---

## 知乎数据格式

### hot_search（热搜榜）

```json
{
  "title": "话题标题",
  "url": "https://www.zhihu.com/search?q=...",
  "query": "原始搜索词"
}
```

### hot_question（热门话题）

```json
{
  "title": "问题标题",
  "url": "https://www.zhihu.com/question/...",
  "heat": "1234 万热度",
  "excerpt": "问题描述摘要"
}
```

### hot_video（热门视频）

```json
{
  "title": "视频标题",
  "url": "https://www.zhihu.com/zvideo/...",
  "heat": "567 万热度",
  "author": "作者名"
}
```

### topic（关键词搜索）

```json
{
  "title": "问题标题",
  "url": "https://www.zhihu.com/question/...",
  "answer_count": 150,
  "follower_count": 2300
}
```

### all（全部热榜）

```json
{
  "type": "all",
  "timestamp": "...",
  "hot_search": { "count": 25, "data": [...] },
  "hot_question": { "count": 50, "data": [...] },
  "hot_video": { "count": 50, "data": [...] }
}
```

---

## 微博数据格式

> V2 待实现，以下为规划格式

### hot_search（热搜榜）

```json
{
  "title": "热搜话题",
  "url": "https://s.weibo.com/weibo?q=...",
  "rank": 1,
  "heat": "5678901",
  "category": "热|新|沸"
}
```

---

## 今日头条数据格式

> V2 待实现，以下为规划格式

### hot_search（热榜）

```json
{
  "title": "新闻标题",
  "url": "https://www.toutiao.com/trending/...",
  "heat": "999999",
  "source": "来源媒体"
}
```

---

## V2EX 数据格式

> V2 待实现，以下为规划格式

### hot_search（热门主题）

```json
{
  "title": "帖子标题",
  "url": "https://www.v2ex.com/t/...",
  "node": "程序员",
  "replies": 42,
  "author": "用户名"
}
```

---

## 36氪数据格式

> V2 待实现，以下为规划格式

### hot_search（热门新闻）

```json
{
  "title": "文章标题",
  "url": "https://36kr.com/p/...",
  "summary": "文章摘要",
  "publish_time": "2026-03-24 10:00:00",
  "author": "作者/机构"
}
```

---

## AIBase 数据格式

### news / hot-search（AI 新闻资讯）

```json
{
  "id": 26543,
  "title": "文章标题",
  "subtitle": "文章副标题",
  "url": "https://news.aibase.cn/news/26543",
  "thumb": "https://pic.newsz.com/.../thumb.jpg",
  "source": "AIbase基地",
  "create_time": "2026-03-25 14:11:57",
  "pv": 7359,
  "description": "文章摘要描述",
  "content": "<div>...</div>"
}
```

### daily（AI 日报）

```json
{
  "id": 1234,
  "title": "日报标题",
  "subtitle": "日报副标题",
  "url": "https://news.aibase.cn/daily/1234",
  "thumb": "https://pic.newsz.com/.../thumb.jpg",
  "source": "AIbase基地",
  "create_time": "2026-03-25 08:00:00",
  "pv": 12345,
  "description": "日报摘要",
  "content": "<div>...</div>"
}
```

| 字段          | 类型   | 说明                    |
| ------------- | ------ | ----------------------- |
| `id`          | int    | 文章唯一 ID             |
| `title`       | string | 文章标题                |
| `subtitle`    | string | 副标题                  |
| `url`         | string | 文章链接                |
| `thumb`       | string | 封面图 URL              |
| `source`      | string | 来源名称                |
| `create_time` | string | 发布时间                |
| `pv`          | int    | 浏览量                  |
| `description` | string | 摘要                    |
| `content`     | string | 正文 HTML（需自行解析） |

### all（新闻 + 日报合并）

```json
{
  "news": {
    "type": "news",
    "timestamp": "...",
    "count": 20,
    "data": [...]
  },
  "daily": {
    "type": "daily",
    "timestamp": "...",
    "count": 20,
    "data": [...]
  }
}
```

> `hot-search` 是 `news` 的别名，用于兼容 hub.py 的统一调度接口。

---

## 聚合输出格式

### hub.py fetch / all 输出

JSON Lines 格式（每行一个平台结果）：

```jsonl
{"platform": "知乎", "success": true, "data": {...}}
{"platform": "微博", "success": false, "error": "脚本尚未实现"}
```

| 字段       | 类型   | 说明                               |
| ---------- | ------ | ---------------------------------- |
| `platform` | string | 平台中文名                         |
| `success`  | bool   | 是否成功获取                       |
| `data`     | object | 成功时返回的数据（同平台脚本输出） |
| `error`    | string | 失败时的错误信息                   |

### hub.py compare 输出

```json
{
  "summary": "跨平台热点词频分析",
  "timestamp": "...",
  "platforms_total": 5,
  "platforms_success": 3,
  "top_keywords": [
    {
      "keyword": "AI",
      "platforms": 3,
      "total_mentions": 8,
      "platform_names": ["知乎", "微博", "36氪"]
    }
  ],
  "per_platform": {
    "知乎": { "status": "ok", "titles": ["...", "..."] },
    "微博": { "status": "unavailable", "error": "..." }
  }
}
```

---

## 错误格式

### 脚手架（未实现）响应

```json
{
  "error": "not_implemented",
  "message": "XXX 抓取待 V2 实现"
}
```

### 运行时错误

```json
{
  "platform": "知乎",
  "success": false,
  "error": "HTTP error: 401 Unauthorized"
}
```
