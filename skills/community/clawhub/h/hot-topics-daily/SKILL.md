---
name: hot-topics-daily
description: 每日热搜速览推送 - 自动抓取微博、知乎、百度、B站、抖音、今日头条热搜并发送到 Discord。支持配置平台开关和显示条数。
version: 2.0.0
metadata:
  openclaw:
    requires:
      bins: ["node"]
---

# 每日热搜速览推送 v2.0

自动抓取 6 个国内主流平台热搜，定时推送到 Discord。

## 支持平台

| 平台 | Emoji | 数据 |
|------|-------|------|
| 微博热搜 | 🔥 | 热度值 |
| 知乎热榜 | 💡 | 热度值 |
| 百度热搜 | 🔍 | 热度值 |
| B站热门 | 📺 | 标题 |
| 抖音热点 | 🎵 | 热度值 |
| 今日头条 | 📰 | 标题 |

## 使用方式

### 手动推送
```bash
node ~/.openclaw/workspace/skills/hot-topics-daily/scripts/push.cjs
```

### 自动推送（Cron）
- **时间**: 每天 8:35
- **目标**: Discord 子区 `1482246566055120898`

## 配置 (`config.json`)

```json
{
  "discord": { "threadId": "1482246566055120898" },
  "api": {
    "baseUrl": "https://60s.viki.moe/v2",
    "timeout": 10000
  },
  "platforms": [
    { "name": "微博热搜", "key": "weibo", "emoji": "🔥", "enabled": true },
    { "name": "知乎热榜", "key": "zhihu", "emoji": "💡", "enabled": true },
    { "name": "百度热搜", "key": "baidu/hot", "emoji": "🔍", "enabled": true },
    { "name": "B站热门", "key": "bili", "emoji": "📺", "enabled": true },
    { "name": "抖音热点", "key": "douyin", "emoji": "🎵", "enabled": true },
    { "name": "今日头条", "key": "toutiao", "emoji": "📰", "enabled": true }
  ],
  "display": {
    "itemsPerPlatform": 5,
    "maxTitleLength": 40
  }
}
```

### 启用/禁用平台
修改对应平台的 `enabled` 为 `true/false`。

### 调整条数
修改 `display.itemsPerPlatform`（默认 5）。

## 数据源

使用 [60s.viki.moe](https://github.com/vikiboss/60s) 免费开源 API，无需 API Key。

## 文件结构

```
skills/hot-topics-daily/
├── SKILL.md           # 技能说明
├── config.json        # 配置文件
└── scripts/
    ├── push.cjs       # 主推送脚本
    └── global_news_fetcher.py  # 国际新闻（备用）
```

## 更新日志

### v2.0.0 (2026-03-29)
- ✅ 新增抖音、今日头条支持
- ✅ 重写推送脚本，支持 http/https
- ✅ 错误处理：平台失败不阻塞其他平台
- ✅ 新增超时控制
- ✅ 重写 SKILL.md

### v1.0.0 (2026-03-13)
- 初始版本
