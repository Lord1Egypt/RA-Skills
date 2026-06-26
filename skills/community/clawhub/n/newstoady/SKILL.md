---
name: NewsToday
description: |
  NewsToday solves information overload for users who want to stay informed without spending an hour checking scattered sources. Instead of manually browsing Weibo, Zhihu, Baidu, and news apps separately, NewsToday aggregates, deduplicates, and summarizes the most important stories into a single readable briefing delivered at the right time.

  Every morning, NewsToday pushes a curated briefing of 10 top stories spanning politics, finance, technology, international affairs, and society — pulled from both RSS feeds (Sina News, The Paper, 36Kr, BBC Chinese, Reuters Chinese) and real-time WebSearch, each with a 2-sentence summary and source attribution. Every evening, a recap highlights what developed throughout the day and previews tomorrow's key events. Breaking news alerts fire automatically every 2 hours during daytime whenever a major story breaks — earthquakes, market crashes, political announcements — so users never miss what matters.

  Users can tune their experience by setting topic preferences — weighting finance over entertainment, or boosting international coverage — so every briefing reflects what actually matters to them. Supports Chinese and English output. Deliverable via Telegram, Feishu, Slack, or Discord. No registration required for on-demand queries; optional user profile unlocks personalized daily push and breaking alerts.

  Trigger words: 早报, 晚报, 今日新闻, 新闻摘要, 热榜, 热搜, 追踪, 最新消息, 突发, 微博热搜, 知乎热榜, X热帖, 科技新闻, 财经新闻, AI早报, AI最新, 人工智能动态, 军事新闻, 军事动态, 头条, 订阅新闻, morning briefing, daily news, news summary, Chinese news, trending, breaking news, news push, hot topics, topic tracking, international news, AI news, military news.
keywords: 新闻推送, 早报, 新闻摘要, 每日新闻, 今日新闻, 热榜, 热搜, 订阅新闻, 晚报, 突发新闻, 微博热搜, 知乎热榜, 百度热搜, X热帖, 头条, 科技新闻, 财经新闻, 娱乐新闻, 体育新闻, 社会新闻, 国际新闻, 军事新闻, 地区冲突, 国防政策, AI早报, AI新闻, 大模型动态, 人工智能, 话题追踪, 最新消息, RSS新闻, 新闻聚合, 资讯, 快讯, 要闻, 每天新闻, 看新闻, 新闻助手, 资讯助手, 新闻机器人, 每日资讯, news push, daily briefing, news summary, Chinese news, morning briefing, evening news, trending, hot topics, breaking news, topic tracking, news aggregator, RSS feeds, personalized news, military news, AI news, news bot, daily news bot, news digest, news alert, China news, top stories, news reader
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# NewsToday

> 私人新闻助手 — 早报 · 晚报 · RSS聚合 · 突发提醒 · 话题追踪 · 个性化推送

## 何时使用

- 用户说"早报""今天新闻""新闻摘要""今天发生了什么"
- 用户问"热搜""微博热榜""知乎热榜""X热帖"
- 用户说"AI 早报""AI 最新""人工智能动态"
- 用户想看某类新闻：科技、AI、财经、娱乐、体育、社会、国际、军事
- 用户说"追踪 XX""XX 最新消息""XX 怎么样了"
- 用户说"开启推送""订阅早报""每天推新闻"
- 用户说"突发""重大消息""有什么大事"

---

## 🌐 语言规则

- 默认中文；用户英文提问切英文
- 新闻标题保留原文，摘要用回复语言改写

---

## 📋 功能说明

### 早报
从 RSS（新浪/澎湃/36氪/BBC中文/Reuters中文）+ WebSearch 双源聚合，去重后选10条覆盖不同领域，按用户话题偏好加权排序。头部显示今日条数和预估阅读时长。第1条为**头条**（重要性最高，3-4句详细摘要+影响分析），其余9条常规格式（标题、来源、2句摘要）。财经类每条含影响评级：📈 利好 / 📉 利空 / ➡️ 中性。

### 晚报
收官3-5条当日重要新闻 + 1-2条热点最新进展 + 明日日程预告。

### 突发新闻提醒
每2小时检测（08:00-22:00），仅在满足阈值（7级以上地震、市场熔断、重大政策等）时推送，不骚扰用户。

### 热榜聚合
搜索微博热搜 + 知乎热榜 + 百度热搜 + X（Twitter）热帖，去重合并，标注来源，多平台共同热点置顶。X 热帖作为第三方实时信号，补充国内平台之前的舆情风向；若 X 数据不可用则静默降级，不影响其他来源输出。

### 话题追踪
搜索 `{关键词} 最新 {日期}` + `{关键词} 进展` + `{关键词} 官方回应`，时间线倒序输出，含各方反应。

### 深读
用户回复序号或说"详细说说 XX"时，多角度搜索，交叉验证，呈现详细经过、各方反应、延伸阅读。

### AI 早报（独立模式）
用户说"AI 早报""AI 最新""人工智能动态"时触发独立模式：专门搜索 `AI 最新进展 {日期}`、`大模型 新闻`、`OpenAI Anthropic Google DeepMind 动态`，输出 5 条 AI 专项摘要，含产品发布、研究突破、行业动向，与常规早报格式一致但信源更聚焦。

### 分类浏览

| 分类 | 搜索词 |
|------|--------|
| 科技 | 科技新闻 今日、AI新闻 |
| AI | AI 最新进展、大模型 新闻、OpenAI Anthropic 动态 |
| 财经 | 财经新闻 今日、股市 |
| 娱乐 | 娱乐新闻 今日 |
| 体育 | 体育新闻 今日、赛事结果 |
| 社会 | 社会新闻 今日、民生 |
| 国际 | 国际新闻 今日、外交 |
| 军事 | 军事新闻 今日、地区冲突、国防政策、军事演习 |

---

## 🔧 脚本说明

```bash
# 注册（可选，解锁个性化推送）
node scripts/register.js <userId> [language] [topics] [channel]
# 示例：
node scripts/register.js alice zh 科技,财经,国际 telegram
node scripts/register.js bob en tech,finance telegram

# 话题偏好
node scripts/preference.js show <userId>
node scripts/preference.js set <userId> <话题> <权重0-1>
node scripts/preference.js reset <userId>

# 手动触发（不需要注册）
node scripts/morning-push.js [userId]
node scripts/evening-push.js [userId]
node scripts/rss-fetch.js [--lang zh|en] [--topics 科技,财经,国际]
node scripts/breaking-alert.js <userId>

# 推送管理
node scripts/push-toggle.js on <userId> [--morning 08:00] [--evening 20:00] [--channel telegram]
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`

---

## ⚠️ 注意事项

1. 每条新闻必须标注来源媒体
2. 涉及争议内容呈现多方视角，不做立场判断
3. 不注册可直接使用早晚报；注册后可按话题个性化、开启突发提醒
4. 用户数据仅存储推送偏好和话题权重（`data/users/<userId>.json`），不含新闻内容
5. RSS 源无法访问时自动降级为 WebSearch，不影响正常使用
