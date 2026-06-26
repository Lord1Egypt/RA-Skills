---
name: news_daily_report
description: 每日综合新闻简报 - 自动抓取并生成包含科技、财经、热点的综合报告
---

# 综合新闻简报 (news-daily-report)

每天自动生成综合新闻简报，包含四大板块：综合热门、科技简报、财经动态、热点追踪。

## 功能

- **每日速览**：抓取 Hacker News、微博、V2EX 热榜各 5 条
- **科技简报**：GitHub Trending、Product Hunt、36氪 各 5 条
- **财经动态**：华尔街见闻、腾讯新闻 各 5 条
- **热点追踪**：微博热搜、V2EX 热榜综合热度最高的 5 条

## 触发方式

在对话中说：
- "生成今日新闻简报"
- "综合新闻报告"
- "今日新闻"
- "新闻汇总"

## 执行步骤

1. 设置代理（如需要）：
   ```bash
   export HTTP_PROXY=http://192.168.110.9:7890
   export HTTPS_PROXY=http://192.168.110.9:7890
   ```

2. 进入 skill 目录并抓取数据：
   ```bash
   cd ~/.openclaw/workspace/技能/news-aggregator-skill
   python3 scripts/fetch_news.py --source hackernews,weibo,v2ex --limit 15
   python3 scripts/fetch_news.py --source github,producthunt,36kr --limit 15
   python3 scripts/fetch_news.py --source wallstreetcn,tencent --limit 10
   ```

3. 读取 JSON 结果，按四大板块整理成 markdown 格式

4. 保存报告到 `reports/YYYY-MM-DD/` 目录

5. （可选）创建飞书文档并写入

## 依赖

- Python 3.8+
- news-aggregator-skill（已安装）
- 代理网络访问

## 输出示例

```markdown
#### 1. [科技标题](链接)
> **来源**: 36Kr | **重要性**: ⭐⭐⭐⭐
> **内容说明**：
> *   细节1
> *   细节2
```

---
**版本**: 1.0.0  
**作者**: 桃贼  
**标签**: 新闻、简报、每日、汇总