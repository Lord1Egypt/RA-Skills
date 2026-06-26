# Data Schemas

Complete field definitions for each item type returned by `news_cli.py`.

## News Item

Returned by `news`, `daily`, `all`, and `search --type news`.

| Field | Type | Description |
|---|---|---|
| `id` | number | 文章ID |
| `title` | string | 标题 |
| `subtitle` | string | 副标题 |
| `url` | string | 原文链接 |
| `thumb` | string | 缩略图URL |
| `source` | string | 来源（仅 news/daily 命令） |
| `author` | string | 作者（仅 news/daily 命令） |
| `create_time` | string | 发布时间 |
| `pv` | number | 阅读量 |
| `description` | string | 摘要 |
| `content` | string | 正文纯文本，Markdown 格式（`###` 标题、`>` 引用块） |
| `images` | array | 正文配图 `[{src, alt}]` |
| `videos` | array | 正文视频 `[{src}]` |
| `links` | array | 正文外部链接 `[{text, href}]` |

`content`/`images`/`videos`/`links` 仅在未使用 `--no-content` 时出现。

## Product Item

Returned by `search --type products`.

| Field | Type | Description |
|---|---|---|
| `id` | string | 产品ID |
| `name` | string | 产品名称 |
| `url` | string | 产品页链接 |
| `logo` | string | 产品Logo URL |
| `category` | array | 分类标签 |
| `tags` | array | 关键词标签 |
| `pv` | number | 浏览量 |
| `description` | string | 产品简介 |

## Model Item

Returned by `search --type models`.

| Field | Type | Description |
|---|---|---|
| `id` | string | 模型ID |
| `name` | string | 模型名称 |
| `full_name` | string | 完整名称（含组织前缀，如 `Qwen/Qwen3-8B`） |
| `provider` | string | 提供者/组织 |
| `tags` | array | 标签 |
| `category` | array | 分类 |
| `downloads` | number | 下载量 |
| `likes` | number | 点赞数 |
| `description` | string | 模型简介 |

## MCP Item

Returned by `search --type mcp`.

| Field | Type | Description |
|---|---|---|
| `id` | string | MCP 服务 ID |
| `name` | string | 服务名称 |
| `tag` | string | 语言/类型标签 |
| `downloads` | number | 下载量 |
| `rating` | number | 评分 |
| `provider` | string | 提供者 |
| `description` | string | 服务简介 |
