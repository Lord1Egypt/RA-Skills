---
name: github-trending
description: 每日 GitHub Trending 热榜推送，支持日榜和月度汇总
license: MIT
---

# GitHub Trending Skill

当用户说“今天的 GitHub 热榜”“GitHub trending”“今日最火的仓库”时，自动抓取 GitHub Trending 数据并推送中文摘要。

## 执行方式

### 每日热榜
调用 `scripts/daily.py`，带参数 `language`（默认 All）和 `limit`（默认 10）：
- 命令：`python scripts/daily.py --language All --limit 10`
- 或导入运行：`from scripts.daily import run; run(language="All", limit=10)`

### 月度汇总
调用 `scripts/monthly.py`，带参数 `language`（默认 All）和 `limit`（默认 10）：
- 命令：`python scripts/monthly.py --language All --limit 10`
- 或导入运行：`from scripts.monthly import run; run(language="All", limit=10)`

## 输出格式
返回 markdown 格式的中文热榜，每条包含：
- 仓库名（加粗）
- 描述
- 编程语言
- 总 star 数
- 今日/本月增长

## 触发时机
- 用户说“今日 GitHub 热榜”
- 用户说“GitHub trending”
- 用户说“今天最火的仓库”
- 用户说“上月最火的仓库” → 触发 monthly 模式

## 注意事项
- 月度模式抓取 10 种语言，每次请求间隔 3 秒防限流
- 网络失败时返回缓存数据并附带提示
- 所有时间使用 UTC
