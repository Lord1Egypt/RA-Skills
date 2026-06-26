# Hacker News

## 常用模式

### 热门
```bash
opencli hackernews top --limit 10
```

### 最新
```bash
opencli hackernews new --limit 10
```

### Ask HN
```bash
opencli hackernews ask --limit 10
```

### Show HN
```bash
opencli hackernews show --limit 10
```

### Jobs
```bash
opencli hackernews jobs --limit 10
```

### 搜索
```bash
opencli hackernews search "OpenClaw" --limit 10
```

### 用户
```bash
opencli hackernews user <username>
```

## 最小说明

- Hacker News 多数命令属于公开 API 读操作，不依赖浏览器登录态。
- 若搜索结果不理想，常见原因是查询词过宽，或更适合改用 top / new / ask / show 分流查看。
