---
name: wechat-article
version: 1.0.0
description: 微信公众号文章抓取工具。使用场景：(1) 抓取公众号文章列表和内容，(2) 搜索公众号，(3) 获取文章链接。当用户提到微信公众号文章、公众号抓取、微信文章采集时使用此技能。
---

# 微信公众号文章抓取

## 快速开始

### 1. 抓取公众号文章列表

```bash
python3 ~/.openclaw/skills/wechat-article/scripts/wechat_article.py "公众号名称" [文章数量]
```

示例：
```bash
python3 ~/.openclaw/skills/wechat-article/scripts/wechat_article.py "分析派迈缇" 10
```

### 2. 获取 Cookie

Cookie 获取步骤：
1. 登录 https://mp.weixin.qq.com
2. F12 → Network → 刷新页面
3. 点击任意请求 → Headers → 复制 Request Headers 中的 Cookie

## 配置

Cookie 保存在：`~/.openclaw/skills/wechat-article/scripts/wechat_cookie.env`

## 注意事项

- Cookie 会过期，如失效需重新获取
- 搜索公众号需要先在脚本中更新 Cookie
