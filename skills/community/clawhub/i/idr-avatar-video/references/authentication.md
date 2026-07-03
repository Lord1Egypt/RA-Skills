---
name: 认证
description: 生成视频如何配置API认证
---

# 认证

## API Token

每一个请求都会要求认证信息.

### 获取你的 Token

1. 在网站 [idr.ai](https://www.neural-avatar.com) 注册
2. 复制 API key

### 配置

设置环境变量:

```bash
export IDR_USER_TOKEN="your_token_here"
```

### API Request Format

所有请求都使用这个请求头:

```bash
curl -X GET "http://a1.neural-avatar.com:8004/video/speaker" \
  -H "Authorization: YOUR_TOKEN"
```
