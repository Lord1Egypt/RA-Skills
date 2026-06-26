---
name: news-aggregator-skill
description: 每日简报生成 skill。自动抓取 28 个来源的实时内容，生成 CEO 风格的深度分析简报。触发条件：用户请求"每日简报"、"科技新闻"、"AI 简报"。核心功能：RSS 抓取 → JSON 数据 → AI 生成 CEO 简报。
---

# News Aggregator Skill

每日简报生成：抓取 28 个来源 → 生成 CEO 风格简报。

## 工作流程

```bash
# 1. 抓取数据（任意来源组合）
python3 scripts/daily_briefing.py --profile <profile>

# 2. 生成 CEO 简报
python3 scripts/generate_ceo_briefing.py --date YYYY-MM-DD
```

输出：`reports/YYYY-MM-DD/ceo_briefing.md`
```

## 可用简报模板

| Profile | 来源 | 用途 |
|---------|------|------|
| `general` | HN + PH + GitHub + V2EX + 左翼媒体 | 综合早报（CEO 风格） |
| `insights` | HN + PH + GitHub（精选） | 高价值洞察 |
| `finance` | WallStreetCN + 36Kr + 腾讯 | 财经日报 |
| `tech` | GitHub + HN + Product Hunt | 科技日报 |
| `ai_daily` | HF Papers + AI Newsletters | AI 深度日报 |
| `social` | Weibo + V2EX | 吃瓜日报 |
| `github` | GitHub Trending | GitHub 精选 |
| `reading_list` | Essays + Podcasts | 阅读/听力清单 |

## 关键文件

| 文件 | 作用 |
|------|------|
| `scripts/generate_ceo_briefing.py` | 读取 JSON + instruction → AI 生成 CEO 简报 |
| `scripts/daily_briefing.py` | 抓取多来源数据，输出 unified JSON |
| `references/briefing_general.md` | CEO 简报 instruction（AI 阅读此文件生成内容） |
| `scripts/fetch_news.py` | 单来源抓取器 |

## Instruction 参考（AI 使用）

对于 CEO 风格简报生成，AI 会自动读取 `references/briefing_general.md`，该文件定义了：
- Executive Summary（今日要点）格式
- 按主题分组而非排行榜
- Impact 分析而非热度数字
- 读后思考题

如需调整简报格式，修改 `references/briefing_general.md` 即可。

## 指令文件

- `references/briefing_general.md` - CEO 综合早报
- `references/briefing_finance.md` - 财经日报
- `references/briefing_tech.md` - 科技日报
- `references/briefing_ai_daily.md` - AI 深度日报
- `references/briefing_social.md` - 社交/吃瓜日报
- `references/briefing_github.md` - GitHub 精选

---
楚泉 & lorra 共同出品
