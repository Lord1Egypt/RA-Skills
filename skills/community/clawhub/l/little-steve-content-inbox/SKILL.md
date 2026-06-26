---
name: little-steve-content-inbox
version: 0.1.5
description: Little Steve Content Inbox: stop letting good content rot in your chat history. Save links, notes, and images right in your IM, manage read status, and actually get back to them. / 小史内容收件箱：别让好内容烂在聊天记录里。在 IM 里直接收录链接、文字、截图，按状态管理，真正回看。
homepage: https://github.com/EchoOfZion/little-steve-content-inbox
requires:
  bins:
    - jq
---

# Little Steve Content Inbox

A lightweight content archiving and review tool for IM workflows. Archive links, notes, and images sent in chat, manage their read status, and browse with pagination.

## Data Files

- `skills/little-steve-content-inbox/data/items.json`
- `skills/little-steve-content-inbox/data/view-state.json`

## Agent Command Conventions

1. Add link
```bash
bash {baseDir}/scripts/inbox.sh add --type link --title "Article title" --url "https://example.com/article" --tags "tech,ai"
```

2. Add note
```bash
bash {baseDir}/scripts/inbox.sh add --type note --title "Quick thought" --content "Some text content to save"
```

3. Add image
```bash
bash {baseDir}/scripts/inbox.sh add --type image --title "Screenshot" --media-path "/path/to/image.png"
```

4. List items (default: all, 10 per page)
```bash
bash {baseDir}/scripts/inbox.sh list --status all
bash {baseDir}/scripts/inbox.sh list --status unread
bash {baseDir}/scripts/inbox.sh list --status read
bash {baseDir}/scripts/inbox.sh list --status starred
```

5. Next page
```bash
bash {baseDir}/scripts/inbox.sh more
```

6. View item detail
```bash
bash {baseDir}/scripts/inbox.sh view --id <id>
```

7. Update status
```bash
bash {baseDir}/scripts/inbox.sh status --id <id> --status read
bash {baseDir}/scripts/inbox.sh status --id <id> --status starred
bash {baseDir}/scripts/inbox.sh status --id <id> --status unread
```

8. Delete item
```bash
bash {baseDir}/scripts/inbox.sh delete --id <id>
```

## Content Types

- `link` — web URL (article, tweet, page)
- `note` — plain text
- `image` — local image file
- `video` — (reserved for future use)

## Status Enum

- `unread` — new, not yet reviewed
- `read` — reviewed
- `starred` — bookmarked / favorited

## IM Output Format

- List: newest first, 10 items per page
- Per item: `[status][type] #ID title` (compact, no URL/path in list)
- Footer: `-- more: N total, showing X-Y --` or `-- end: N total --`
- Full URL/path only shown in detail view (`view --id`)

## Important: Explicit Intent Only

**Do NOT auto-archive.** Only run `add` when the user explicitly asks to save/archive content using keywords such as: 收录, 归档, 保存, 记录, archive, save, bookmark. If the user simply shares a URL, text, or image in conversation without these keywords, treat it as normal chat — do not archive it.

## IM Natural Language Mapping

| User says | Command |
|---|---|
| 收录/Archive/Save `<url>` | `add --type link --url <url> --title <extracted>` |
| 记录/Save/Note `<text>` | `add --type note --title <summary> --content <text>` |
| 归档图片 / Archive image | `add --type image --title <desc> --media-path <path>` |
| Inbox / Content list | `list --status all` |
| Unread list | `list --status unread` |
| Read list | `list --status read` |
| Starred / Favorites | `list --status starred` |
| More | `more` |
| View #ID | `view --id <id>` |
| Mark read #ID | `status --id <id> --status read` |
| Mark unread #ID | `status --id <id> --status unread` |
| Star #ID | `status --id <id> --status starred` |
| Unstar #ID | `status --id <id> --status unread` |
| Delete #ID | `delete --id <id>` |

---

# 小史内容收件箱

面向聊天工作流的轻量内容归档与回看工具。将聊天中发送的链接、文字、图片统一归档，按状态管理，分页浏览，随时可查。

## 数据文件

- `skills/little-steve-content-inbox/data/items.json`
- `skills/little-steve-content-inbox/data/view-state.json`

## Agent 执行约定

1. 收录链接
```bash
bash {baseDir}/scripts/inbox.sh add --type link --title "文章标题" --url "https://example.com/article" --tags "tech,ai"
```

2. 记录文字
```bash
bash {baseDir}/scripts/inbox.sh add --type note --title "随手记" --content "要保存的文字内容"
```

3. 归档图片
```bash
bash {baseDir}/scripts/inbox.sh add --type image --title "截图" --media-path "/path/to/image.png"
```

4. 查看列表（默认全部，每页10条）
```bash
bash {baseDir}/scripts/inbox.sh list --status all
bash {baseDir}/scripts/inbox.sh list --status unread
bash {baseDir}/scripts/inbox.sh list --status read
bash {baseDir}/scripts/inbox.sh list --status starred
```

5. 下一页
```bash
bash {baseDir}/scripts/inbox.sh more
```

6. 查看详情
```bash
bash {baseDir}/scripts/inbox.sh view --id <id>
```

7. 更新状态
```bash
bash {baseDir}/scripts/inbox.sh status --id <id> --status read
bash {baseDir}/scripts/inbox.sh status --id <id> --status starred
bash {baseDir}/scripts/inbox.sh status --id <id> --status unread
```

8. 删除
```bash
bash {baseDir}/scripts/inbox.sh delete --id <id>
```

## 内容类型

- `link` — 网页链接（文章、推文、页面）
- `note` — 纯文字
- `image` — 本地图片文件
- `video` — （预留）

## 状态枚举

- `unread` — 未读
- `read` — 已读
- `starred` — 收藏

## IM 输出规范

- 列表：最新优先，每页10条
- 每条显示：`[状态][类型] #ID 标题`（精简，列表不显示 URL/路径）
- 页脚：`-- more: 共N条, 显示X-Y --` 或 `-- end: 共N条 --`
- 完整 URL/路径仅在详情视图中显示（`view --id`）

## 重要：仅在明确指令时收录

**不要自动收录。** 只有当用户明确使用"收录、归档、保存、记录、archive、save、bookmark"等关键词时才执行 `add`。如果用户只是在聊天中分享链接、文字或图片，但没有使用这些关键词，按正常对话处理，不要归档。

## IM 自然语言映射

| 用户说 | 对应命令 |
|---|---|
| 收录 / 归档 `<url>` | `add --type link --url <url> --title <提取>` |
| 记录 / 保存 `<文字>` | `add --type note --title <摘要> --content <文字>` |
| 归档图片 | `add --type image --title <描述> --media-path <路径>` |
| 内容列表 / 收件箱 | `list --status all` |
| 未读列表 | `list --status unread` |
| 已读列表 | `list --status read` |
| 收藏列表 | `list --status starred` |
| 更多 | `more` |
| 查看 #ID | `view --id <id>` |
| 已读 #ID | `status --id <id> --status read` |
| 未读 #ID | `status --id <id> --status unread` |
| 收藏 #ID | `status --id <id> --status starred` |
| 取消收藏 #ID | `status --id <id> --status unread` |
| 删除 #ID | `delete --id <id>` |
