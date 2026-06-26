# 新闻智能体 API 参考

## 认证

### SSO 模式（生产环境）

通过网关注入 Base64 编码的用户信息请求头：

| 请求头 | 说明 |
|--------|------|
| UserId | 用户 ID |
| AccountName | 用户姓名 |
| AccountCode | 账号编码 |
| Email | 邮箱 |
| RoleCodes | 角色编码 |

### 开发模式

```http
Authorization: Bearer PharmaBlock Gateway
```

网关检测到此 Token 会注入模拟用户信息。

---

## 新闻文章 API

### 获取文章列表

```http
GET /api/v1/articles?page=1&page_size=20&keyword=&category_id=&start_date=&end_date=&analyzed=
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认 1 |
| page_size | int | 否 | 每页数量，1-100，默认 20 |
| category_id | int | 否 | 分类 ID |
| keyword | string | 否 | 标题搜索关键词 |
| start_date | date | 否 | 开始日期 YYYY-MM-DD |
| end_date | date | 否 | 结束日期 YYYY-MM-DD |
| analyzed | bool | 否 | 是否已分析 |

**响应：**

```json
{
  "code": 200,
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "title": "文章标题",
        "summary": "AI 摘要",
        "source": "来源",
        "source_url": "原文链接",
        "category_id": 1,
        "category_name": "行业动态",
        "category_color": "#409eff",
        "keywords": ["关键词1", "关键词2"],
        "published_at": "2026-03-17 10:30:00",
        "image_url": null,
        "analyzed": true
      }
    ],
    "total": 156,
    "page": 1,
    "page_size": 20
  }
}
```

### 获取文章详情

```http
GET /api/v1/articles/{article_id}
```

返回文章完整信息，含 `content` 正文。

---

## 分类 API

### 获取分类列表

```http
GET /api/v1/categories
```

**响应：**

```json
{
  "code": 200,
  "success": true,
  "data": [
    {"id": 1, "name": "行业动态", "icon": "📰", "color": "#409eff", "sort_order": 1}
  ]
}
```

---

## 仪表盘 API

### 获取仪表盘聚合数据

```http
GET /api/v1/dashboard
```

**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| total_articles | int | 文章总数 |
| today_articles | int | 今日新增 |
| category_distribution | array | 分类分布 [{name, color, count}] |
| hot_keywords | array | 热词 TOP10 [{keyword, count}] |
| latest_articles | array | 最新 5 篇文章 |
| daily_counts | array | 近 7 日采集量 [{date, count}] |

---

## 词云 API

### 生成词云

```http
GET /api/v1/wordcloud/generate?source=keywords&top_n=80&category_id=&start_date=&end_date=
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| source | string | `keywords`（关键词）或 `content`（全文分词） |
| top_n | int | 词数量，默认 80 |
| category_id | int | 分类筛选 |
| start_date | date | 开始日期 |
| end_date | date | 结束日期 |

**响应：** `{words: [{text, value}], image: "base64...", total_articles: N}`

---

## 趋势 API

### 关键词趋势

```http
GET /api/v1/trends/keyword?keyword=创新药&days=30
```

**响应：** `[{date: "2026-03-17", count: 5}, ...]`

### 热词排行

```http
GET /api/v1/trends/hot?days=7&top_n=20&category_id=
```

**响应：** `[{keyword: "创新药", count: 23}, ...]`

### 分类趋势

```http
GET /api/v1/trends/category?days=30
```

**响应：** `[{date: "2026-03-17", category_id: 1, count: 5}, ...]`

---

## 任务 API

### 触发采集

```http
POST /api/v1/tasks/crawl
```

### 触发分析

```http
POST /api/v1/tasks/analyze
```

### 触发趋势统计

```http
POST /api/v1/tasks/trend
```

### 查看任务状态

```http
GET /api/v1/tasks/status
```

**响应：**

```json
{
  "data": {
    "crawl": {"running": false, "last_run": "2026-03-17 08:00", "processed": 12, "error": null},
    "analyze": {"running": false, "last_run": "2026-03-17 08:10", "processed": 8, "error": null}
  }
}
```

---

## 认证 API

### 获取当前用户

```http
GET /api/v1/auth/me
```

### 用户登出

```http
POST /api/v1/auth/logout
```

---

## 数据模型

### NewsArticle

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| title | string | 标题 |
| content | text | 正文 |
| summary | text | LLM 摘要 |
| source | string | 来源 |
| source_url | string | 原文链接 |
| url_hash | string | URL SHA256 去重 |
| category_id | int | 分类 FK |
| keywords | json | 关键词列表 |
| published_at | datetime | 发布时间 |
| crawled_at | datetime | 采集时间 |
| analyzed | bool | 是否已分析 |
| image_url | string | 封面图 |

### KeywordTrend

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| keyword | string | 关键词 |
| date | date | 日期 |
| count | int | 出现次数 |
| category_id | int | 分类 FK |

唯一约束：`(keyword, date)`
