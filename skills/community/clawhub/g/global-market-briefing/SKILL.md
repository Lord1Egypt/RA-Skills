---
name: global-market-briefing
slug: global-market-briefing
version: 1.0.0
description: "每日财经早报：A股行情 + RSS全球新闻聚合，自动生成Markdown简报"
homepage: https://clawhub.com/skills/global-market-briefing
---

# 全球财经早报 Global Market Briefing

每日自动生成财经早报，覆盖 A 股行情 + 国内/国际新闻。

## 能力

- **A股盘前行情** — 上证/深证/创业板/科创50/上证50 五大指数
- **新闻聚合** — 中国新闻网 RSS（财经/时政/国际/滚动/要闻 5个源）
- **自动分类** — 按关键词自动归入财经/时政/国际/其他
- **Markdown输出** — 完整版存本地 + 精简版推微信
- **链接索引** — 每条新闻含原文链接

## 输出

- **微信推送**: 各分类精简版（前3条 + 总数）
- **本地存档**: 完整MD文件（每类15条，含链接）

## Quick Start

### 1. 安装依赖

```bash
pip install requests
```

### 2. 安装 skill

```bash
clawhub install global-market-briefing
```

### 3. 手动运行

```bash
python3 <skill_path>/scripts/morning_briefing.py
```

### 4. 定时推送

```yaml
schedule: "30 9 * * 1-6"  # 周一到周六 9:30
payload:
  kind: agentTurn
  message: "运行：exec python3 <skill_path>/scripts/morning_briefing.py"
  toolsAllow: ["exec"]
  timeoutSeconds: 60
```

## 数据源

- 中国新闻网 RSS (https://www.chinanews.com.cn/rss/)
- 腾讯财经行情 (qt.gtimg.cn)

## 配置

输出目录在脚本中修改 `OUTPUT_DIR` 变量，默认 `~/Desktop/早间新闻/`。
