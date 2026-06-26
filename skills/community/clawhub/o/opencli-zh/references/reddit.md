# Reddit

## 常用模式

### 热门
```bash
opencli reddit hot --limit 10
opencli reddit hot --subreddit programming
```

### 搜索
```bash
opencli reddit search "AI" --sort top --time week
```

### 子版块
```bash
opencli reddit subreddit rust --sort top --time month
```

### 阅读帖子
```bash
opencli reddit read --post-id <id>
```

### 我的收藏
```bash
opencli reddit saved --limit 10
```

## 最小说明

- Reddit 许多 URL 支持后缀 `.json` 直取 REST 数据，是 Tier 2 Cookie 策略的黄金标杆。
- 搜索支持 `--sort` (top/new/relevance) 和 `--time` (hour/day/week/month/year/all) 过滤。
- 写操作（upvote / comment / subscribe / save）外部可见。
