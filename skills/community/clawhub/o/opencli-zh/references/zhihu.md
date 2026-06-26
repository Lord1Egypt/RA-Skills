# 知乎 / Zhihu

## 常用模式

### 热榜
```bash
opencli zhihu hot --limit 10
```

### 搜索
```bash
opencli zhihu search "AI"
```

### 问题详情
```bash
opencli zhihu question <question-id>
```

## 最小说明

- 知乎依赖浏览器登录态进行 Cookie 认证。
- 热榜是最稳定的命令；搜索和问题详情偶有 Cookie 过期导致的空结果。
