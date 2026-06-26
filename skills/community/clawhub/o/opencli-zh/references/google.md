# Google

## 常用模式

### 网页搜索
```bash
opencli google search "OpenClaw"
```

### 新闻搜索
```bash
opencli google news --limit 10
```

### 搜索建议
```bash
opencli google suggest "openclaw"
```

### 趋势
```bash
opencli google trends
```

## 最小说明

- Google 相关命令属于公开 API，通常不依赖浏览器登录态。
- 若结果异常卡住，常见原因是浏览器链路或扩展连接状态异常。
