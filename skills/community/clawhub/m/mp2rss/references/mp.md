# 微信公众号（MP）订阅与文章管理

本文档供 Agent 在用户询问**公众号**订阅、列出、搜索、取消订阅、查文章等需求时按需读取。

**调用前提**：先确认登录态（见 [auth.md](auth.md)）；未登录时不要直接调本节命令。

> 本文档中所有用作"某个公众号"占位的地方一律写作 `<公众号名>` 或具名形式（如「财经早知道」），避免歧义。

---

## Subscribe

```
mp2rss mp subscribe <article-url> [-o json]
```

订阅一个公众号。⚠️ **传入的是文章 URL**（`https://mp.weixin.qq.com/s/...`），不是公众号名、不是二维码、不是公众号主页链接。从公众号任意一篇文章里复制链接即可，Mp2rss 会从该文章解析出所属公众号并把整个公众号订阅到你的 Feed。

```bash
mp2rss mp subscribe https://mp.weixin.qq.com/s/abcDEFghIJKlmnop
mp2rss mp subscribe https://mp.weixin.qq.com/s/abc -o json
```

### JSON shape

```json
{
  "ok": true,
  "articleUrl": "https://mp.weixin.qq.com/s/..."
}
```

### Agent 处理

- 用户给的不是 `mp.weixin.qq.com/s/...` URL → **反问**索要任意一篇文章链接，不要直接试
- 用户给的是公众号名 → 不能搜索 + 订阅，必须用户提供文章 URL
- 订阅成功后建议跟一句 `mp list -q <推断的公众号名>` 让用户看到刚订阅的条目（可选）

---

## List

```
mp2rss mp list [-q <keyword>] [-p <page>] [--page-size <n>] [-o json]
```

列出当前 Feed Key 名下的所有订阅。

| Flag | 默认 | 说明 |
|------|------|------|
| `-q, --query` | — | 按公众号名模糊搜索（与 `mp search` 等价） |
| `-p, --page` | 1 | 页码 |
| `--page-size` | 20 | 每页条数（最大 50） |
| `-o, --output` | table | `table` / `json` |

```bash
mp2rss mp list
mp2rss mp list -q 财经
mp2rss mp list -p 2 --page-size 50
mp2rss mp list -o json | jq '.items[].mpName'
```

### JSON shape

```json
{
  "items": [
    {
      "mpId": 123456,
      "mpName": "某公众号",
      "mpAvatarUrl": "https://...",
      "createdAt": 1705000000000,
      "mpLastArticleAt": 1705000050000
    }
  ],
  "total": 42,
  "page": 1,
  "pageSize": 20
}
```

⚠️ **`mpId` 是 int64**，JS 环境解析前先正则替换为字符串（见 [SKILL.md - mpId 是 int64](../SKILL.md#-mpid-是-int64) 段）。

---

## Search

```
mp2rss mp search <keyword> [-p <page>] [--page-size <n>] [-o json]
```

`mp2rss mp list -q <keyword>` 的语法糖，flag 集与输出与 `list` 完全一致。

```bash
mp2rss mp search 财经
mp2rss mp search 财经 -o json
```

### Agent 注意

`mp search` **只在已订阅源中模糊查找**，不会发现公众号、不会订阅新号。用户要"搜公众号订阅"指的就是这个；要订阅新公众号必须走 `mp subscribe + 文章 URL` 路径。

---

## Remove

```
mp2rss mp remove <mpId> [-y] [-o json]
```

按 mpId 取消订阅。`-y` 跳过交互式确认（适合脚本调用）。

```bash
mp2rss mp remove 123456            # 会交互式确认
mp2rss mp remove 123456 -y         # 直接执行
mp2rss mp remove 123456 -y -o json
```

### JSON shape

```json
{
  "ok": true,
  "mpId": 123456
}
```

### Agent 处理

- **取消订阅前必须先确认 mpId**：用 `mp list -q <name> -o json` 或 `mp search <name> -o json` 拿到准确 mpId 再调 remove
- 用户只给公众号名时，不要凭名字猜 mpId
- 若 `items` 多条匹配 → 列给用户让其挑选哪个，不要默认删第一个
- 自动化脚本场景统一加 `-y`，否则 Agent 会卡在交互式 prompt

---

## Articles

```
mp2rss mp articles <mpId> [-p <page>] [--page-size <n>] [-o json]
```

按 mpId 查询公众号历史文章。

| Flag | 默认 | 说明 |
|------|------|------|
| `-p, --page` | 1 | 页码 |
| `--page-size` | 100 | 每页条数（最大 100） |
| `-o, --output` | table | `table` / `json` |

```bash
mp2rss mp articles 123456
mp2rss mp articles 123456 -p 2 --page-size 100
mp2rss mp articles 123456 -o json | jq '.items[].title'
```

### JSON shape

```json
{
  "items": [
    {
      "mpId": 123456,
      "articleId": "article-id-string",
      "title": "文章标题",
      "summary": "文章摘要",
      "coverImageUrl": "https://...",
      "originalUrl": "https://mp.weixin.qq.com/s/...",
      "contentMarkdown": "# Markdown 正文",
      "publishedAt": 1705000000000,
      "updatedAt": 1705000010000
    }
  ]
}
```

⚠️ **没有分页字段**（无 `total` / `page` / `pageSize`）；`items` 为空数组即视为本页结束。Agent 翻页直接 `-p N` 试到空为止。

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `mpId` | int64 | 公众号 ID（同样字符串化处理） |
| `articleId` | string | 文章唯一 ID |
| `title` | string | 文章标题 |
| `summary` | string | 文章摘要（可能为空） |
| `coverImageUrl` | string | 封面图 URL（可能为空） |
| `originalUrl` | string | 原文链接（`mp.weixin.qq.com/s/...`） |
| `contentMarkdown` | string | Markdown 格式正文 |
| `publishedAt` | int64 | 发布时间，unix 毫秒 |
| `updatedAt` | int64 | 更新时间，unix 毫秒 |

---

## Agent 综合注意事项

- **结构化解析统一 `-o json`**
- **字段命名 camelCase**：`mpId` / `mpName` / `mpAvatarUrl` / `mpLastArticleAt` / `articleId` / `originalUrl` / `contentMarkdown` / `publishedAt`
- **mpId 是 int64**：JS 解析前先字符串化（见 [SKILL.md](../SKILL.md#-mpid-是-int64)）
- **时间字段统一 unix 毫秒**（int64 number）
- **取消订阅前先 list/search 确认 mpId**
- **文章列表无分页字段**，靠 `--page-size`（最大 100）+ `-p` 翻页
- 错误码处理见 [errors.md](errors.md)
