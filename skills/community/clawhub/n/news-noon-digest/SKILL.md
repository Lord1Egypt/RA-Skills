---
name: news-noon-digest
description: 每日中午12点自动推送新闻午报到QQ和飞书，包含全球热点、科技动态、财经要闻
---

# 新闻午报推送

每天中午12点自动抓取全球新闻，生成摘要并推送到QQ和飞书。

## 功能

- 🌍 全球热点：地缘政治、军事冲突、重大事件
- 💻 科技动态：AI、Kimi、DeepSeek、OpenClaw 等科技新闻
- 📈 财经要闻：股市、加密货币、央行政策

## 配置

### 环境变量

```bash
# 飞书机器人 Webhook（必需）
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx"

# QQ推送开关（可选，默认开启）
export QQ_ENABLED="true"
```

### 定时任务

使用 OpenClaw cron 设置每天12点执行：

```bash
openclaw cron add \
  --name "新闻午报" \
  --schedule "0 12 * * *" \
  --tz "Asia/Shanghai" \
  --command "python ~/.openclaw/workspace/skills/news-noon-digest/scripts/fetch_and_digest.py"
```

## 手动运行

```bash
python ~/.openclaw/workspace/skills/news-noon-digest/scripts/fetch_and_digest.py
```

## 输出示例

```
📰 新闻午报 | 03月08日 12:00

━━━━━━━━━━━━━━━━━━━━

🌍 全球热点

• 中东局势：伊朗核设施动态持续受关注
• 俄乌冲突：最新军事与外交进展
• 全球经济：制裁与能源市场波动
• 自然灾害：全球极端天气事件监测

💻 科技动态

• Kimi：长文本处理能力持续优化
• DeepSeek：开源模型性能再突破
• OpenClaw：AI Agent 自动化工具新进展
• 全球AI：大模型竞争白热化

📈 财经要闻

• 全球股市：主要指数今日走势
• 加密货币：比特币及主流币种动态
• 央行政策：各国货币政策最新动向
• 大宗商品：原油、黄金等价格变化

━━━━━━━━━━━━━━━━━━━━

💡 数据来源：World Monitor、网络聚合
🤖 由 OpenClaw AI 自动整理
```
