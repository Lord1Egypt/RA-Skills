# Little Steve Content Inbox

You know how it goes. You're scrolling through Twitter, a newsletter, a Reddit thread — and you find something worth reading. But not right now. So you forward it to yourself on Telegram. Then you find another one. And another.

Three weeks later, your chat history is a graveyard of links. Hundreds of them. You scroll past them every day, meaning to get back to them, never quite doing it. The good stuff is buried. The motivation is gone.

**Little Steve Content Inbox** is built for exactly this problem.

It's not a read-later app. It's not a bookmark manager. It's a lightweight inbox that lives inside your chat, so saving something is as natural as sending a message — and so is coming back to it.

Save links, notes, and images directly in conversation. Browse by status. Star the ones worth keeping. Get gently nudged to clear your backlog. The content you actually care about, organized and within reach — not silently rotting in a scroll.

## Key Capabilities

- Archive multiple content types: links, notes, images (video reserved)
- Status management: `unread` / `read` / `starred`
- Paginated browsing: 10 items per page with "more" for next page
- View full details by ID
- Delete items by ID
- Auto-detect content type from input
- Source domain extraction for links

## Dependency

- `jq`

macOS:
```bash
brew install jq
```

## Common Commands

```bash
# Add a link
bash scripts/inbox.sh add --type link --title "Interesting article" --url "https://example.com/article" --tags "tech"

# Add a note
bash scripts/inbox.sh add --type note --title "Quick thought" --content "Something to remember"

# Add an image
bash scripts/inbox.sh add --type image --title "Screenshot" --media-path "/path/to/image.png"

# List all (newest first, 10 per page)
bash scripts/inbox.sh list --status all

# List unread only
bash scripts/inbox.sh list --status unread

# Next page
bash scripts/inbox.sh more

# View detail
bash scripts/inbox.sh view --id 1

# Mark as read
bash scripts/inbox.sh status --id 1 --status read

# Star / bookmark
bash scripts/inbox.sh status --id 1 --status starred

# Delete
bash scripts/inbox.sh delete --id 1
```

## Data Files

- `data/items.json` — archived content
- `data/view-state.json` — pagination state

---

# 小史内容收件箱

你一定有过这种经历。

刷 X、逛论坛、读 Newsletter，看到一篇好文章——"这个待会儿看"。
然后转发给自己，扔进 Telegram。
再刷，再看到，再转。

一周后，那个对话框里躺了几十条链接。你每次打开都看一眼，然后划走。
再过两周，根本不想打开了。

那些你曾经觉得"值得读"的东西，就这么烂在聊天记录里。

**小史内容收件箱**，是为了解决这个问题。

不是什么高端的稍后阅读工具，也不是又一个收藏夹。
它就住在你的 IM 里，存内容就像发消息一样自然，查内容也一样。

一句话收录链接、文字、截图。按状态分类——未读、已读、收藏。
需要的时候翻一翻，不需要的时候它就在那里安静等着。
偶尔还会提醒你：那些你存下来的东西，还没有看完呢。

内容是用来读的，不是用来沉的。

## 主要能力

- 多类型内容归档：链接、文字、图片（视频预留）
- 状态管理：`unread`（未读）/ `read`（已读）/ `starred`（收藏）
- 分页浏览：每页10条，输入"更多"翻页
- 按 ID 查看完整详情
- 按 ID 删除
- 自动识别内容类型
- 链接自动提取来源域名

## 依赖

- `jq`

macOS:
```bash
brew install jq
```

## 常用命令

```bash
# 收录链接
bash scripts/inbox.sh add --type link --title "有趣的文章" --url "https://example.com/article" --tags "tech"

# 记录文字
bash scripts/inbox.sh add --type note --title "随手记" --content "要记住的事情"

# 归档图片
bash scripts/inbox.sh add --type image --title "截图" --media-path "/path/to/image.png"

# 查看全部（最新优先，每页10条）
bash scripts/inbox.sh list --status all

# 查看未读
bash scripts/inbox.sh list --status unread

# 下一页
bash scripts/inbox.sh more

# 查看详情
bash scripts/inbox.sh view --id 1

# 标记已读
bash scripts/inbox.sh status --id 1 --status read

# 收藏
bash scripts/inbox.sh status --id 1 --status starred

# 删除
bash scripts/inbox.sh delete --id 1
```

## 数据文件

- `data/items.json` — 归档内容
- `data/view-state.json` — 分页状态
