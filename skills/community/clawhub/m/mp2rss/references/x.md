# X（Twitter）订阅与内容拉取

本文档供 Agent 在用户询问 X / Twitter 账号订阅、推文、长文相关需求时按需读取。

**调用前提**：先确认登录态（见 [auth.md](auth.md)）；未登录时不要直接调本节命令。

---

## ⚠️ 关键边界：X 订阅必须在 Web 控制台完成

X 账号的**搜索**与**订阅 / 取消订阅**仅由 Web 控制台 <https://mp2rss.bugcode.dev/> 提供，**CLI 与 Open API 都不暴露这些写类端点**。

CLI 在 `x` 子命令组下**只覆盖读类**三件事：

| 子命令 | 作用 |
|--------|------|
| `mp2rss x list`     | 列出当前 Feed Key 已订阅的 X 账号 |
| `mp2rss x posts`    | 拉取已订阅 X 账号的推文流 |
| `mp2rss x articles` | 拉取已订阅 X 账号的长文流 |

### Agent 路由策略

- 用户说「订阅 X 上的 @xxx」「订阅这个推特账号」「在 mp2rss 里加个 X 号」
  → **不要尝试 CLI**，告诉用户去 Web 控制台「订阅管理 → X」搜索并订阅，之后回到这里可用 CLI 列出/拉内容。
- 用户说「取消订阅 X 账号 xxx」
  → 同上，引导去 Web 控制台。
- 用户说「我订阅了哪些 X 号」「拉一下 @elonmusk 的推文」
  → 走本文档的 `x list` / `x posts` 流程。

---

## xUserId vs @handle

X 的业务键是 `xUserId`（X 平台的数字 user_id，字符串形态），**不是** `@handle`：

- `@handle` 用户可随时改，订阅指向会失效；
- `xUserId` 是 X 平台稳定的唯一 ID。

CLI 与 Open API 的所有 X 读类端点（`x posts` / `x articles`）**只接受 `xUserId`**。用户给的是 `@handle` 或显示名时，Agent 必须先 `mp2rss x list -o json` 查出对应 `xUserId` 再调用。

```bash
mp2rss x list -o json | jq -r '.items[] | "\(.xUserId)\t@\(.xUsername)\t\(.xDisplayName)"'
```

---

## List

```
mp2rss x list [-q <keyword>] [-p <page>] [--page-size <n>] [-o json]
```

列出当前 Feed Key 名下已订阅的全部 X 账号。

| Flag | 默认 | 说明 |
|------|------|------|
| `-q, --query` | — | 按 `xDisplayName` / `xUsername` 模糊匹配 |
| `-p, --page` | 1 | 页码 |
| `--page-size` | 20 | 每页条数（最大 50） |
| `-o, --output` | table | `table` / `json` |

```bash
mp2rss x list
mp2rss x list -q elon
mp2rss x list -p 2 --page-size 20
mp2rss x list -o json | jq '.items[].xUserId'
```

### JSON shape

```json
{
  "items": [
    {
      "sourceType": "x",
      "xUserId": "44196397",
      "xUsername": "elonmusk",
      "xDisplayName": "Elon Musk",
      "xVerified": true,
      "createdAt": 1776640000000,
      "xLastItemAt": 1776854096000
    }
  ],
  "total": 1,
  "page": 1,
  "pageSize": 20
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `sourceType` | string | 固定 `"x"` |
| `xUserId` | string | X 数字 user_id（字符串形态） |
| `xUsername` | string | X handle，不含 `@` |
| `xDisplayName` | string | X 显示名 |
| `xVerified` | bool | 是否已认证 |
| `createdAt` | int64 | 订阅创建时间，unix 毫秒 |
| `xLastItemAt` | int64? | 最近一条推文/长文收录时间，unix 毫秒，可能为 null |

---

## Posts

```
mp2rss x posts <xUserId> [-p <page>] [--page-size <n>] [-o json]
```

按 `postedAt DESC` 拉取已订阅 X 账号的推文流。**仅允许查询已订阅的 xUserId**，未订阅返回 exit code 4（`X account is not subscribed`）。

| Flag | 默认 | 说明 |
|------|------|------|
| `-p, --page` | 1 | 页码 |
| `--page-size` | 20 | 每页条数（**最大 50**） |
| `-o, --output` | table | `table` / `json` |

```bash
mp2rss x posts 44196397
mp2rss x posts 44196397 -p 2 --page-size 20
mp2rss x posts 44196397 -o json | jq '.items[].content'
```

### JSON shape

```json
{
  "items": [
    {
      "postId": "1234567890",
      "content": "hello world",
      "media": [{ "url": "https://x.com/img.jpg", "type": "photo" }],
      "retweetedPost": null,
      "quotedPost": { "id": "99", "content": "..." },
      "threadPosts": [{ "content": "reply 1" }],
      "postedAt": 1746864000000
    }
  ],
  "total": 42,
  "page": 1,
  "pageSize": 20
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `postId` | string | 推文业务 ID |
| `content` | string | 推文正文（明文，未渲染 HTML） |
| `media` | array | 媒体附件数组；无媒体或解析失败为 `[]` |
| `media[].url` | string | 媒体资源 URL |
| `media[].type` | string | `photo` / `video` / `animated_gif` 等 |
| `retweetedPost` | object? | 转推原推文对象；无则 null |
| `quotedPost` | object? | 引用的推文对象；无则 null |
| `threadPosts` | array | Thread 系列推文数组；无则 `[]` |
| `postedAt` | int64 | 发布时间，unix 毫秒 |

::: tip 结构化 vs 渲染
本端点返回的是**结构化原始数据**（含 media / quotedPost / threadPosts 嵌套），供 Agent 自定义渲染。
如果用户只想在阅读器里订阅来看，请引导走 Web 控制台「账户设置」复制的 Feed 链接（公开 RSS / Atom / JSON Feed 层），不要让 Agent 重新拼装。
:::

---

## Articles

```
mp2rss x articles <xUserId> [-p <page>] [--page-size <n>] [-o json]
```

按 `publishedAt DESC` 拉取已订阅 X 账号的长文（X Articles）流。订阅闭环校验同 `x posts`，未订阅返回 exit code 4。

| Flag | 默认 | 说明 |
|------|------|------|
| `-p, --page` | 1 | 页码 |
| `--page-size` | 20 | 每页条数（**最大 50**） |
| `-o, --output` | table | `table` / `json` |

```bash
mp2rss x articles 44196397
mp2rss x articles 44196397 -o json | jq '.items[].url'
```

### JSON shape

```json
{
  "items": [
    {
      "url": "https://x.com/elonmusk/article/...",
      "title": "My take on...",
      "description": "summary",
      "contentMarkdown": "# Heading\n\nfull body markdown source",
      "coverUrl": "https://...",
      "publishedAt": 1747353600000
    }
  ],
  "total": 8,
  "page": 1,
  "pageSize": 20
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `url` | string | 长文原始 URL |
| `title` | string | 标题 |
| `description` | string | 摘要 |
| `contentMarkdown` | string? | 长文 markdown 原文，可能为 null |
| `coverUrl` | string? | 封面图 URL |
| `publishedAt` | int64 | 发布时间，unix 毫秒 |

---

## Agent 综合注意事项

- **xUserId 是字符串**，不要按整数处理（与 `mpId` 不同；handle 起源是数字，但 API 契约统一为字符串）
- **不接受 `@handle`**：从 `x list` 输出里取 `xUserId` 再调 posts / articles
- **写类操作不可达**：用户要订阅/取消订阅 X，**统一引导到 Web 控制台**，不要尝试构造 CLI 写命令
- **结构化解析统一 `-o json`**
- **字段命名 camelCase**：`xUserId` / `xUsername` / `xDisplayName` / `xLastItemAt` / `postId` / `postedAt` / `publishedAt`
- **时间字段统一 unix 毫秒**（int64 number）
- **页大小上限 50**（`x posts` / `x articles` 最大都是 50，注意与 `mp articles` 的 100 不同）
- 错误码处理见 [errors.md](errors.md)；典型场景：未订阅返回 exit 4，message `X account is not subscribed`
