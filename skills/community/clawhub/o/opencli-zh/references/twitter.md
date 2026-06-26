# Twitter / X

## 常用模式

### 时间线
```bash
opencli twitter timeline --limit 10
```

### 书签
```bash
opencli twitter bookmarks --limit 10
```

### 搜索
```bash
opencli twitter search "OpenClaw" --limit 10
```

### 用户主页
```bash
opencli twitter profile <username>
```

### 线程
```bash
opencli twitter thread <tweet-id>
```

### 通知
```bash
opencli twitter notifications --limit 10
```

## 最小说明

- 依赖浏览器登录态；若 X/Twitter 已掉登录，结果可能为空或异常。
- 写操作（post / reply / like / follow / block / delete）外部可见，且部分动作不可逆。
- `article` 子命令用于读取推文长文内容。
