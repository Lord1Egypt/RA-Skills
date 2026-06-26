# 列表阅读

## 推荐流

```bash
maimai feed
maimai feed --type recommended --limit 10
maimai feed --offset 10 --limit 10
maimai feed --page 2 --page-size 10
```

适用场景：
- “帮我看看推荐流”
- “继续翻下一页”
- “抓前 20 条推荐”

## 其他 feed

```bash
maimai feed --type recommended
maimai feed --type following
```

说明：
- 默认 `--type` 是 `recommended`
- 实际可用类型取决于 CLI 支持和当前账号可见内容

## 热榜

```bash
maimai hot-rank
maimai hot-rank --limit 20
```

适用场景：
- “看下今天脉脉热榜”
- “脉脉现在都在讨论什么”

## 公司圈

```bash
maimai company-feed
maimai company-feed 123456
maimai company-feed --limit 20
```

适用场景：
- “看当前公司圈”
- “看某个公司 gossip-discuss 圈子”

如果自动解析当前公司圈失败，尤其是出现 HTTP 406/404，让用户打开浏览器里的公司圈页面，从 URL 复制 `webcid`：

```text
https://maimai.cn/company/gossip_discuss?webcid=<webcid>
```

然后显式传入：

```bash
maimai company-feed <webcid> --limit 20
```

## 结构化输出

```bash
maimai feed --limit 5 --json
maimai hot-rank --yaml
maimai company-feed --raw
```

选择建议：
- 人工阅读优先默认输出
- 脚本处理优先 `--json`
- 字段排查可用 `--yaml`
- 仅在用户明确需要完整字段时才用 `--raw`
