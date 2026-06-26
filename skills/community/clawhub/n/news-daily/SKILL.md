---
name: news-daily
description: 获取新闻热榜（国内、国际、科技、AI）并发送到飞书。不依赖本地工程，直接从 RSS 获取数据。
---

# 新闻日报 Skill

## 功能

- 从多个 RSS 源获取新闻（国内、国际、科技、AI）
- 格式化为飞书卡片消息（标题可点击）
- 支持定时自动发送

## 安装

```bash
cp -r ~/.openclaw/workspace/skills/news-daily /path/to/your/openclaw/workspace/skills/
```

## 配置

### 1. 创建飞书机器人 Webhook

1. 打开飞书群 → 群设置 → 群机器人 → 添加机器人
2. 选择 "自定义机器人"
3. 复制 Webhook 地址

### 2. 配置 Webhook

方式一：环境变量（推荐）
```bash
export NEWS_DAILY_WEBHOOK="你的Webhook地址"
```

方式二：配置文件
```bash
vim ~/.openclaw/workspace/skills/news-daily/scripts/config.json
```

```json
{
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
  "date": "today",
  "categories": {
    "国内": 10,
    "国际": 10,
    "科技": 10,
    "AI": 10
  }
}
```

## 使用

### 手动执行

```bash
python3 ~/.openclaw/workspace/skills/news-daily/scripts/fetch_and_send.py
```

### 配置定时任务

```bash
openclaw config set hooks.internal.entries.news-daily.enabled true
openclaw config set hooks.internal.entries.news-daily.systemEvent "news-daily"
openclaw config set hooks.internal.entries.news-daily.action.kind "exec"
openclaw config set hooks.internal.entries.news-daily.action.command "python3 ~/.openclaw/workspace/skills/news-daily/scripts/fetch_and_send.py"
openclaw gateway restart
```

## RSS 源

| 分类 | 来源 |
|------|------|
| 国内 | 中国新闻网、人民日报 |
| 国际 | 纽约时报、BBC、卫报 |
| 科技 | 36氪、少数派、TechCrunch、The Verge |
| AI | InfoQ、机器之心、MIT 科技评论、VentureBeat |

详细说明见 [README.md](./README.md)
