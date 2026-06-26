---
name: openclaw-intelligence-officer
description: 行业情报官 - 定时采集 GitHub Trending、X(Twitter)、知乎、36kr、掘金等平台热点，AI 摘要后推送到指定渠道。集成 fxtwitter API 和 RSSHub。
---

# OpenClaw Intelligence Officer v1.0

行业情报官 - 自动化的行业情报采集与推送系统

## 功能

- 🤖 **自动采集**: GitHub Trending、X (Twitter)、知乎、36kr、掘金等
- 📝 **AI 摘要**: 提取关键信息，生成摘要
- 🔔 **多渠道推送**: 飞书、钉钉、Telegram、邮件
- ⏰ **定时任务**: 可配置采集频率

## 数据源

### 优先级 P0

| 平台 | 采集方式 | 频率建议 |
|------|---------|---------|
| GitHub Trending | RSS / API | 每日 2 次 |
| X (Twitter) | fxtwitter API | 每日 2 次 |
| 知乎热榜 | RSSHub | 每日 2 次 |

### 优先级 P1

| 平台 | 采集方式 | 频率建议 |
|------|---------|---------|
| 36kr | RSS | 每日 1 次 |
| 掘金 | RSS | 每日 1 次 |
| 微博热搜 | RSSHub | 每日 1 次 |
| 微信读书榜 | RSSHub | 每周 1 次 |

## 配置

### 环境变量

```bash
# 必填
FXTWITTER_API_TOKEN=your_token  # 可选，无则用公开接口

# 推送配置 (至少配置一个)
FEISHU_WEBHOOK=your_webhook
DINGTALK_WEBHOOK=your_webhook
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email
SMTP_PASS=your_password
TO_EMAIL=target@example.com
```

### 采集源配置

在 `memory/intelligence/sources.yaml` 中配置:

```yaml
sources:
  - name: github-trending
    url: https://github.com/trending?since=weekly
    enabled: true
    priority: p0
    tags: [AI, 开源]
    
  - name: x-ai-news
    query: "AI OR LLM OR Agent"
    enabled: true
    priority: p0
    tags: [AI, 大模型]
    
  - name: zhihu-hot
    url: https://www.zhihu.com/hot
    enabled: true
    priority: p0
    tags: [科技, 热点]
```

## 采集流程

```
定时触发 (Cron)
    │
    ▼
获取采集源列表 (按优先级)
    │
    ▼
并行抓取各平台数据
    │
    ├── GitHub → 解析 trending 页面
    ├── X → fxtwitter API
    └── RSS → 解析 XML
    │
    ▼
AI 摘要生成
    │
    ├── 提取标题、链接、描述
    ├── 生成一句话摘要
    └── 分类打标签
    │
    ▼
格式化输出
    │
    ├── Markdown 格式
    └── HTML 格式
    │
    ▼
推送到目标渠道
    │
    ├── 飞书 Webhook
    ├── 钉钉 Webhook
    └── Telegram Bot
```

## 输出格式

### 飞书/钉钉卡片

```markdown
## 📊 行业情报 {日期}

### 🔥 GitHub Trending
1. **[项目名]** - ⭐1234
   描述文本...
   Tags: #AI #开源

2. **[项目名]** - ⭐987
   ...

### 🐦 X 热点
1. @username: 推文内容...
   链接

### 📰 知乎热榜
1. 问题标题
   热度和链接
```

## 目录结构

```
memory/intelligence/
├── sources.yaml       # 采集源配置
├── cache/            # 缓存已推送内容 (去重)
│   └── sent.json
├── logs/            # 采集日志
│   └── 2026-03-24.md
└── summaries/       # 生成的摘要
    └── 2026-03-24.md
```

## 使用方式

### 手动触发采集

```bash
# 采集并推送到默认渠道
openclaw intelligence fetch

# 仅采集不推送 (预览)
openclaw intelligence fetch --dry-run

# 指定采集源
openclaw intelligence fetch --source github-trending
```

### 配置定时任务

```bash
# 每日 9:00 和 15:00 采集
openclaw cron add --schedule "0 9,15 * * *" --task intelligence
```

### 查看历史

```bash
# 查看今日情报
cat memory/intelligence/summaries/2026-03-24.md

# 查看指定日期
openclaw intelligence history --date 2026-03-23
```

## 依赖

- `curl` - HTTP 请求
- `python3` - 解析和摘要
- `xmllint` - RSS 解析 (可选)
- `fxtwitter` - Twitter/X 数据采集

## 扩展

### 添加新数据源

在 `sources.yaml` 添加:

```yaml
- name: my-source
  url: https://example.com/feed
  type: rss  # 或 html, api
  enabled: true
  priority: p1
  tags: [自定义]
```

### 添加新推送渠道

实现对应的 Webhook 发送函数:

```python
def send_to_dingtalk(webhook, message):
    # 实现钉钉推送
    pass

def send_to_telegram(token, chat_id, message):
    # 实现 Telegram 推送
    pass
```

## 设计原则

1. **去重优先**: 同一内容 24 小时内不重复推送
2. **优先级**: P0 每日 2 次，P1 每日 1 次
3. **失败容忍**: 单个源失败不影响其他源
4. **可预览**: 支持 dry-run 先看再发
5. **可追溯**: 所有历史记录本地保存

## 相关项目

- [RSSHub](https://github.com/DIYgod/RSSHub) - 万物皆可 RSS
- [Huginn](https://github.com/huginn/huginn) - 自动化监控
- [TrendRadar](https://github.com/sansan0/TrendRadar) - AI 舆情监控
