---
name: polymarket-telegram-picks
description: 每日拉取 Polymarket 体育/赛事赔率，经 AI 分析后推送值得下注的推荐到 Telegram
user-invocable: true
---

# Polymarket 每日赔率分析与 Telegram 推送

## 功能说明

当用户或定时任务触发「今日 Polymarket 分析」「Polymarket 赔率推送」「执行每日推荐」等请求时，按以下流程执行：

1. **拉取当日未开赛 NBA 赔率**：运行本技能目录下的 `scripts/fetch_polymarket.py`，获取当日（中国时间）、且尚未开赛的 Polymarket NBA 比赛及赔率数据。
2. **AI 分析**：根据脚本输出的结构化数据，结合你自己的判断（赔率价值、热度、流动性等），筛选出你认为值得下注的球队/选项，并简要说明理由。
3. **推送到 Telegram**：将你的分析结论（推荐列表 + 理由）通过 `scripts/send_telegram.py` 发送到用户配置的 Telegram 对话。

## 执行步骤

1. 在技能目录下执行：
   ```bash
   python3 scripts/fetch_polymarket.py
   ```
   或使用工作区中本技能路径下的 `scripts/fetch_polymarket.py`。脚本会输出当日、未开赛的 NBA 比赛摘要（事件标题、开赛时间、选项与隐含概率等）。

2. 阅读脚本输出，从中挑选你认为有下注价值的项目（例如某方赔率被低估、或与你的判断存在价值差）。用简洁中文写出推荐列表与理由。

3. 将上述分析结论作为内容，调用推送脚本：
   ```bash
   python3 scripts/send_telegram.py "你的分析内容（推荐赛事 + 理由）"
   ```
   或通过 stdin 传入：
   ```bash
   echo "你的分析内容" | python3 scripts/send_telegram.py
   ```

## 环境与配置

- **Telegram 推送**依赖环境变量（或在 `config/config.json` 中配置）：
  - `TELEGRAM_BOT_TOKEN`：Bot 的 token（由 @BotFather 获取）
  - `TELEGRAM_CHAT_ID`：接收消息的聊天 ID（私聊或群组）
- 若未配置，`send_telegram.py` 会报错并提示配置方式；分析步骤仍可执行，仅推送会失败。

## 定时任务（每日 8 点中国时间）

在 OpenClaw 中可使用 cron 在每天北京时间 8:00 触发一次本流程，例如：

```bash
openclaw cron add --name "Polymarket每日推送" \
  --cron "0 8 * * *" \
  --session main \
  --message "请执行今日 Polymarket 赔率分析并推送到 Telegram"
```

若使用系统 crontab（不经过 OpenClaw 会话），可配置为 8 点运行 `scripts/run_daily.py`（该脚本会拉取数据、可选调用本地/远程 LLM 分析、再推送 Telegram），详见 README。

## 输出格式建议

推送至 Telegram 的内容建议包含：

- 日期
- 今日推荐项（赛事/问题 + 推荐选项 + 简要理由）
- 可选：风险提示（预测市场有风险等）

分析结论完全由你（AI）基于当前赔率与上下文自行判断，无需与任何外部投注建议绑定。
