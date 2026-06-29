---
name: nba-analyst
version: 1.0.0
description: NBA 全能数据分析助手。查询比分、排名、球员数据、球队信息、球员/球队对比、AI深度分析、生成可视化HTML报告。全中文界面，零API Key。
author: bettermen
tags: [nba, basketball, sports, data, analysis, chinese]
platform: [python]
agent_created: true
---

# NBA Analyst -- NBA 数据分析助手

## 触发场景

用户查询以下内容时自动激活:
- NBA 比分、赛程、排名
- NBA 球员/球队信息、数据统计
- 球员/球队对比分析
- 比赛详情、Box Score
- 生成 NBA 分析报告

## 触发词

`NBA` `nba` `篮球数据` `篮球分析` `比分` `排名` `球队` `球员` `赛程` `选秀`
`詹姆斯` `库里` `杜兰特` `字母哥` `约基奇` `东契奇` `湖人` `勇士` `凯尔特人` `篮网` `掘金` `热火` `尼克斯` `火箭` `马刺` `快船` `雄鹿` `76人` `太阳` `雷霆`

## 使用方式

**自然语言 (推荐):**
```
今天NBA比分怎么样
詹姆斯本赛季数据
西部排名
湖人对勇士历史战绩
库里最近10场表现
```

**结构化命令:**
```
/nba scoreboard          # 今日比分
/nba standings           # 联盟排名
/nba standings west      # 西部排名
/nba player 詹姆斯       # 球员信息
/nba team 湖人           # 球队信息
/nba compare 詹姆斯 库里  # 球员对比
/nba report 詹姆斯       # 生成球员报告
/nba report team 湖人    # 生成球队报告
/nba report today        # 今日比赛报告
```

## 输出格式

- **纯文本查询**: 表格 + AI 简要分析
- **报告模式**: 完整 HTML 报告 (含图表 + AI 深度解读)
- **对比模式**: 双栏对比 + AI 评述

## 依赖安装

```bash
pip install nba_api pandas numpy matplotlib requests
```

## 注意事项

- 数据来源于 NBA.com 官方公开 API，使用需遵守 NBA.com Terms of Use
- 无需 API Key，完全免费
- 首版覆盖 2025-26 赛季数据，历史数据可达 1996 赛季
- NBA.com 可能在休赛期限流或暂停部分端点
