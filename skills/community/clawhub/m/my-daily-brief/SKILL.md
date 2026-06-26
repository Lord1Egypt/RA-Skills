---
name: my-daily-brief
description: >
  每日早报技能，生成天气+热点简报。
  Use when: 用户说“今日简报”“今天热点”，或早上8点定时触发。
  NOT for: 详细天气预报、深度新闻分析。
---

# Daily Brief Skill

## When to Run
- 用户说“今日简报”“今天热点”“有什么新闻”
- 每天早上 11:22（通过 cron 定时触发）
- 需要快速了解今日信息时

## Workflow
1. 获取北京天气：
   curl "https://wttr.in/Beijin?format=3"
2. 获取百度首页上热搜词条前 50条 标题
3. 按指定格式整理输出

## Output Format
📅 今日简报
🌤 天气：{天气结果}
🔥 百度 热搜：
1. {标题}
2. {标题}
...