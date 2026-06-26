# 详情、评论、图片与资料卡

## 短索引机制

列表命令执行后，CLI 会缓存最近一次列表的引用表，因此 `1`、`2`、`3` 这种 `ITEM_ID` 常常可以直接表示“刚才列表里的第几项”。

先查看缓存：

```bash
maimai refs
```

重要注意：
- 短索引只对“最近一次列表命令”的缓存可靠，例如刚跑完 `hot-rank`、`feed`、`company-feed` 或 `search` 后的 `1`、`2`。
- 运行 `comments` 后，评论短索引会写入独立缓存；帖子短索引仍用 `maimai refs` 查看，评论短索引用 `maimai refs --scope comments` 查看。
- 如果用户给的是 raw gossip id，例如 `36744330`，通常还需要 `--egid`；raw feed id 通常还需要 `--efid`。
- 不要把“热榜第 11 条”的短索引和“帖子真实 ID”混用。先用 `maimai refs` 确认当前 `1/11/18` 指向谁。
- 当命令提示需要 `egid` 或 `efid` 时，优先重新拉原列表恢复短索引；若已知道真实 ID，则必须显式补 `--egid` / `--efid`。

## 查看详情

```bash
maimai detail 1 --kind gossip
maimai detail 10 --kind feed
maimai detail 1 --kind feed --efid E880GEffW92s1hDji5EuDQ
maimai detail 1 --kind gossip --egid 31fcf8e65f2f42ab8dc8facc472e89c2
maimai detail 36744330 --kind gossip --egid 31fcf8e65f2f42ab8dc8facc472e89c2
```

适用场景：
- “展开第 1 条看看”
- “把刚才那条帖子详情给我”
- “用真实 `efid` / `egid` 直接查”

## 查看评论

```bash
maimai comments 1 --kind gossip
maimai comments 10 --kind feed
maimai comments 1 --kind gossip --page 1 --limit 20
maimai refs --scope comments
maimai comments 1 --kind feed --cid 1
maimai comments 1 --kind feed --cid COMMENT_ID
maimai comments 36744330 --kind gossip --egid 31fcf8e65f2f42ab8dc8facc472e89c2
```

适用场景：
- “看评论区”
- “继续翻评论”
- “查看某条评论的回复”

## 查看或下载图片

```bash
maimai images 1 --kind gossip
maimai images 10 --kind feed
maimai images 1 --download ./maimai-images
maimai images 1 --download ./maimai-images --thumb
```

适用场景：
- “看这条帖子配图”
- “把这条图片下载下来”
- “先下载缩略图快速预览”

## 查看资料卡

```bash
maimai me
maimai profile MMID
maimai profile 1
maimai profile MMID --trackable-token TOKEN
```

适用场景：
- “看我当前账号信息”
- “查看搜索结果里第 1 个联系人”
- “读取某个人的资料卡”

注意：
- `profile` 的 `MMID` 也可以是最近列表中的短索引
- 某些资料链接自带 `trackable_token`，补上它通常更稳
