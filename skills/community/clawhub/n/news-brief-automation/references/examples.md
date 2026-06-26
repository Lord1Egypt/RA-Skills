# Examples

## Example 1: Hacker News recurring brief

Use a cron prompt like:

```md
# Hacker News 定时简报

目标：每天北京时间 10:00、12:00、14:00、16:00、18:00 获取 Hacker News 最新值得关注的资讯，整理后发给用户。

执行要求：

1. 优先查看 Hacker News 首页与 newest：
   - https://news.ycombinator.com/
   - https://news.ycombinator.com/newest
2. 必要时打开文章链接补充上下文，但不要陷入长篇阅读。
3. 选择 5-10 条最值得看的内容，优先：AI / 开发工具 / 开源 / infra / 数据工程 / 安全。
4. 输出为中文，包含：标题、今日重点、值得关注条目。
5. 发布前检查 `reports/hackernews/` 最近一份报告并去重：
   - 只保留新出现、新上升、或有明显新进展的条目。
   - 如果大多重复，就改发增量短版。
6. 保存到 `reports/hackernews/YYYY-MM-DD-HH00.md`。
7. 保存后，把相同 Markdown 发给用户。
8. 如果本轮没有强新内容，就说明这一轮偏平，并给 3 条仍值得看的链接。
```

## Example 2: GitHub + Hugging Face daily trends

Use a cron prompt like:

```md
# 每日 GitHub / Hugging Face 趋势榜

目标：每天北京时间 10:00 获取 GitHub 和 Hugging Face 的趋势内容，整理成 Markdown 保存到工作区，并发给用户。

执行要求：

1. 获取 GitHub Trending 与 Hugging Face 热门内容。
2. 输出为中文，分为：GitHub 趋势、Hugging Face 趋势、今日观察。
3. 发布前检查 `reports/trends/` 最近一份报告并去重：
   - 同一项目若昨日已写且无明显变化，不要重复展开。
   - 优先写新上榜、新冲高、或最值得关注的变化。
4. 至少覆盖 GitHub 5 个项目、Hugging Face 5 个条目；若新增不多，可明确说明。
5. 保存到 `reports/trends/YYYY-MM-DD.md`。
6. 保存后，把完整 Markdown 发给用户。
7. 若某个站点不可用，要在文中说明，并尽量完成可访问部分。
```

## Design notes

- “先保存，后发送” 很重要：这样后续去重才有稳定依据。
- 高频简报不要强凑条数；增量价值比表面完整更重要。
- 对热点榜单，用户通常更在意“为什么值得看”，不是机械抄榜。
- 输出格式要固定，便于后续迁移到 cron、agent session、或别的自动化系统。
