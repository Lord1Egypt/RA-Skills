---
name: daily-news
version: 2.0.0
description: 每日新闻自动采集与报告生成。使用 web_search (freshness=oneDay) 替代旧版 Bing/Tavily 方案，确保新闻均为24小时内真实最新。
metadata:
  author: OpenClaw
  category: automation
  triggers:
    - 每日新闻
    - 新闻日报
    - yesterday news
    - daily news
---

# 每日新闻自动采集 v2.0

## 架构变更

### v1.0 旧方案（已废弃）
| 组件 | 方式 | 致命问题 |
|------|------|---------|
| `daily_news_query.py` | Bing 爬虫 (requests+bs4) | ❌ 无法可靠过滤旧闻，混入2023/2024年旧内容 |
| `daily_news_query.py` | Bing 爬虫 | ❌ 大量网页噪声（"网站地图"、"无障碍链接"等） |
| `daily_news_tavily.py` | Tavily API | ❌ 完全无时间过滤，可能返回任何时间的内容 |

### v2.0 新方案
| 组件 | 方式 | 优势 |
|------|------|------|
| Agent + `web_search` | OpenClaw 内置工具 | ✅ `freshness=oneDay` 严格24小时过滤 |
| | | ✅ 权威媒体源（新华社/央视/澎湃等） |
| | | ✅ 零外部依赖，无需额外配置 |

---

## 触发方式

1. **用户手动触发**: 用户说"每日新闻"、"新闻日报"、"daily news"等
2. **定时触发**: OpenClaw cron 任务，每日工作日 08:30 自动执行（任务名：`每日新闻日报 (v2.0)`）

---

## 执行流程

### 步骤 1: 确定日期

```python
from datetime import datetime, timedelta
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y年%m月%d日')
yesterday_short = f"{yesterday.month}月{yesterday.day}日"
```

### 步骤 2: 7轮 web_search 查询

对以下每个类别，**依次**调用 `web_search`，每轮必须带 `freshness: "oneDay"`：

| # | Emoji | 类别 | 搜索关键词 |
|---|-------|------|-----------|
| 1 | 🌍 | 全球政治军事 | `{yesterday_short} 全球 政治 军事 国际 冲突 外交` |
| 2 | 🇨🇳 | 中国政治军事 | `{yesterday_short} 中国 政治 军事 政策 官方` |
| 3 | 💰 | 全球财经 | `{yesterday_short} 全球 财经 股市 美股 原油 黄金 汇率` |
| 4 | 📈 | 中国财经 | `{yesterday_short} 中国 A股 宏观经济 政策 LPR` |
| 5 | 🤖 | AI/人工智能 | `{yesterday_short} AI 人工智能 大模型 技术突破` |
| 6 | 🔭 | 科技领域 | `{yesterday_short} 科技 半导体 新能源 航天 机器人` |
| 7 | 📱 | 消费电子家电 | `{yesterday_short} 消费电子 家电 手机 电视` |

调用示例：
```
web_search:
  query: "5月20日 全球 政治 军事 国际 冲突 外交"
  freshness: "oneDay"     ← 必须！严格24小时过滤
  count: 10
  channel: "bocha"
```

### 步骤 3: 内容筛选与清洗

**排除规则：**
- ❌ 排除娱乐/体育/游戏/电竞内容
- ❌ 排除往年旧闻（描述中出现 2025年、2024年等往年日期）
- ❌ 排除网页噪声（"网站地图"、"无障碍"、"首页"等）

**保留规则：**
- ✅ 优先权威媒体源：新华社、央视新闻、澎湃新闻、上海证券报、财新网、中国证券报等
- ✅ 保留包含具体数据、人物、事件的条目
- ✅ 跨类别去重

### 步骤 4: 生成报告

按固定模板生成 Markdown 报告：

```markdown
# 📰 {yesterday_str} 全球 & 中国核心新闻汇总

📅 生成时间：{当前时间}
🔍 数据源：Web Search（freshness=oneDay 严格24小时过滤）
✅ 已过滤旧闻/娱乐/体育/游戏内容

---

## 🌍 一、全球昨日政治军事新闻
- [新闻条目]
...

## 🇨🇳 二、中国昨日政治军事新闻
...

## 💰 三、全球昨日财经股市新闻
（含美股收盘、大宗商品、汇率数据）
...

## 📈 四、中国昨日财经股市新闻
（含A股收盘、LPR、重要政策）
...

## 🤖 五、全球昨日人工智能领域新闻
...

## 🔭 六、全球昨日科技领域新闻
...

## 📱 七、消费电子家电行业新闻
...

---
## 📌 今日一句话总结
> [一句话概括当日最重要新闻]
```

### 步骤 5: 保存

报告保存到: `memory/daily_news_{YYYY-MM-DD}.md`

---

## 相关文件

| 文件 | 状态 | 说明 |
|------|------|------|
| `skills/daily-news/SKILL.md` | ✅ 当前 | 本技能文档 |
| `daily_news_query.py` | ⚠️ 已废弃 | 旧版 Bing 爬虫方案 |
| `daily_news_tavily.py` | ⚠️ 已废弃 | 旧版 Tavily API 方案 |
| `memory/daily_news_*.md` | ✅ 历史存档 | 每日报告存档 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | 2026-05-21 | 改用 web_search(freshness=oneDay)，废弃 Bing/Tavily 方案 |
| v1.0 | 2026-04-21 | 初始版本：Bing 爬虫 + Tavily API 双方案 |
