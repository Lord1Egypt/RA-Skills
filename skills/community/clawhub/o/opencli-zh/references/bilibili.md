# Bilibili

## 常用模式

### 热门
```bash
opencli bilibili hot --limit 10
```

### 排行榜
```bash
opencli bilibili ranking --limit 10
```

### 搜索
```bash
opencli bilibili search "rust"
```

### 动态
```bash
opencli bilibili feed --limit 10
```

### 历史
```bash
opencli bilibili history --limit 20
```

### 收藏夹
```bash
opencli bilibili favorite
```

### 字幕
```bash
opencli bilibili subtitle --bvid BV1xxx
```

## 最小说明

- 热门、排行、搜索通常较稳；动态、历史、收藏夹等个人数据更依赖登录态。
- 若 Bilibili 已掉登录，涉及个人数据的命令结果可能为空或异常。
- 字幕命令支持 `--lang zh-CN` 指定语言。
