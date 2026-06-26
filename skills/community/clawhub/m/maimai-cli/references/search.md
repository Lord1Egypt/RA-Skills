# 搜索与发现

## 搜索内容与联系人

```bash
maimai search AI
maimai search 裁员 --section gossips
maimai search 字节 --section contacts
maimai search 大模型 --limit 10
```

支持的 `--section`：
- `all`
- `feeds`
- `gossips`
- `contacts`

适用场景：
- “搜一下某个话题”
- “找某个联系人”
- “查脉脉上关于某公司/某岗位的讨论”

## 搜索翻页

```bash
maimai search QUERY --page 2 --page-size 10
maimai search QUERY --offset 10 --limit 10
```

注意：
- 帮助里已注明当前 Web API 可能忽略 `--offset`
- 用户反馈翻页没变化时，优先改用 `--page`

## 搜索后的常见下一步

```bash
maimai refs
maimai detail 1 --kind gossip
maimai profile 1
```

推荐流程：
1. 先搜索拿到结果
2. 用 `maimai refs` 看短索引映射
3. 再展开详情、评论或资料卡
