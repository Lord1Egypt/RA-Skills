# 小红书 / Xiaohongshu

## 常用模式

### 搜索
```bash
opencli xiaohongshu search "美食"
```

### 推荐 Feed
```bash
opencli xiaohongshu feed --limit 10
```

### 通知
```bash
opencli xiaohongshu notifications
```

### 笔记详情
```bash
opencli xiaohongshu note <note-id-or-url>
```

### 用户主页
```bash
opencli xiaohongshu user <user-id>
```

## 最小说明

- 小红书重度依赖浏览器登录态；个人数据（通知、Feed）在未登录时不可用。
- 搜索使用 Pinia Store + XHR 拦截策略，若结果异常通常与登录态、站点请求校验或风控有关。
- 创作者系列命令（`creator-notes` / `creator-profile` / `creator-stats`）需要创作者身份。
