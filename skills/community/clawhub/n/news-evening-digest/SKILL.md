---
name: news-evening-digest
description: 每天晚上 8 点自动推送全球新闻晚报到 QQ 和飞书，参考 World Monitor 数据源
author: Jake
version: 1.0.0
---

# 全球新闻晚报推送

每天晚上 8 点自动抓取全球新闻，生成摘要并推送到 QQ 和飞书。

## 功能

- 🌍 **全球热点**：地缘政治、军事冲突、重大事件（参考 World Monitor）
- 💻 **科技动态**：AI、大模型、OpenClaw 等科技新闻
- 📈 **财经要闻**：股市、加密货币、央行政策、大宗商品
- 🌦️ **天气灾害**：全球极端天气、自然灾害
- 🗺️ **地缘监控**：伊朗局势、军事部署、核设施动态

## 数据源

### 主要来源
- **World Monitor** (worldmonitor.app) - 全球情报仪表板
- **Tavily Search** - 实时新闻搜索
- **RSS 聚合** - 435+ 新闻源

### 重点关注
- 伊朗 - 以色列 - 美国冲突
- 全球军事动态
- 经济与市场波动
- 科技行业重大事件

## 配置

### 环境变量

```bash
# 飞书机器人 Webhook（必需）
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx"

# QQ 推送开关（可选，默认开启）
export QQ_ENABLED="true"

# World Monitor API（可选）
export WORLD_MONITOR_API="https://api.worldmonitor.app"
```

### 定时任务

使用 OpenClaw cron 设置每天 20:00 执行：

```bash
openclaw cron add \
  --name "全球新闻晚报" \
  --schedule "0 20 * * *" \
  --tz "Asia/Shanghai" \
  --command "python ~/.openclaw/workspace/skills/news-evening-digest/scripts/fetch_and_digest.py"
```

## 手动运行

```bash
python ~/.openclaw/workspace/skills/news-evening-digest/scripts/fetch_and_digest.py
```

## 推送格式

```
📰 全球新闻晚报 | 03 月 13 日 20:00

━━━━━━━━━━━━━━━━━━━━

🌍 全球热点 (7 天焦点)

• 伊朗局势：第 13 天军事冲突持续
  - 伊朗导弹袭击以色列北部，30+ 人受伤
  - 美军加油机伊拉克坠毁，4 人丧生
  - 油价突破$100/桶，全球股市下跌
  - 320 万人流离失所，人道危机加剧

• 俄乌冲突：最新军事与外交进展
• 全球经济：制裁与能源市场波动
• 自然灾害：全球极端天气事件监测

💻 科技动态

• Kimi：长文本处理能力持续优化
• DeepSeek：开源模型性能再突破
• OpenClaw：AI Agent 自动化工具新进展
• 全球 AI：大模型竞争白热化

📈 财经要闻

• 全球股市：主要指数今日走势
• 加密货币：比特币及主流币种动态
• 央行政策：各国货币政策最新动向
• 大宗商品：原油、黄金等价格变化

🌦️ 天气与灾害

• 极端天气：全球主要气象事件
• 自然灾害：地震、火山、洪水监测

━━━━━━━━━━━━━━━━━━━━

🗺️ 数据来源：World Monitor、Tavily Search、网络聚合
🤖 由 OpenClaw AI 自动整理
📊 查看实时情报：worldmonitor.app
```

## 脚本说明

### fetch_and_digest.py

主脚本，负责：
1. 从 World Monitor 抓取实时数据
2. 使用 Tavily Search 搜索最新新闻
3. 生成结构化摘要
4. 推送到 QQ 和飞书

### 推送渠道

- **QQ** - 通过 QQBot 技能推送
- **飞书** - 通过飞书机器人 Webhook 推送
- **可选扩展** - 微信、Telegram、Discord 等

## 安全注意事项

- 所有 API 密钥存储在 `~/.openclaw/.env`
- 不推送敏感个人信息
- 新闻来源经过事实核查
- 避免推送未证实的谣言

---

*Created: 2026-03-13*
*Last Updated: 2026-03-13*
