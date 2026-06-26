# Polymarket BTC 5m Bot v2

全自动 Polymarket BTC 5分钟 Up/Down 纸交易机器人 + Web 控制面板。

> **纸交易模式**：不花真实 USDC，模拟真实交易环境，用于策略验证。

---

## 功能特性

| 功能 | 说明 |
|------|------|
| 🤖 AI 决策 | 支持 MiniMax / OpenAI / SiliconFlow 等任意 OpenAI-compatible API |
| 📊 双信号系统 | AI 分析 + 价差套利，取交集才交易 |
| 💻 Web 面板 | 实时状态、持仓、胜率、AI 思考记录 |
| 🛡️ 风险保护 | 止盈止损、点差保护、深度保护 |
| 📈 自动交易 | 每 15 秒扫描市场，30 秒 AI 决策 |

---

## 系统要求

- Python 3.10+
- 网络可访问 Polymarket API 和 Binance
- Polymarket API Key（纸交易模式也需要）
- AI API Key（可选，不填则使用规则策略）

---

## 快速开始

### 1. 安装依赖

```bash
cd polymarket-btc-bot
bash scripts/install.sh
```

### 2. 配置环境变量

```bash
cp references/.env.example .env
nano .env   # 编辑填入你的配置
```

**关键配置项：**

```bash
# Polymarket API（必须）
POLYMARKET_API_KEY=your_key
POLYMARKET_API_SECRET=your_secret
POLYMARKET_WALLET_ADDRESS=0x...

# AI 决策（可选，不填自动回退规则策略）
AI_PROVIDER=minimax
AI_BASE_URL=https://api.minimax.chat/v1
AI_API_KEY=sk-cp-your-key
AI_MODEL=MiniMax-M2.7
```

### 3. 启动 Bot

```bash
# 终端窗口 1：启动交易 Bot
bash scripts/bot_start.sh

# 终端窗口 2：启动控制面板
bash scripts/panel_start.sh
```

### 4. 打开控制面板

访问：**http://localhost:18095**

---

## AI 厂商配置指南

### MiniMax（推荐国内用户）

```bash
AI_PROVIDER=minimax
AI_BASE_URL=https://api.minimax.chat/v1
AI_API_KEY=sk-cp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AI_MODEL=MiniMax-M2.7
```

从 https://api.minimax.chat 注册获取 API Key。

### OpenAI

```bash
AI_PROVIDER=openai
AI_BASE_URL=https://api.openai.com/v1
AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AI_MODEL=gpt-4o-mini
```

### 硅基流动（免费额度）

```bash
AI_PROVIDER=siliconflow
AI_BASE_URL=https://api.siliconflow.cn/v1
AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AI_MODEL=deepseek-ai/DeepSeek-V3
```

### 不使用 AI（规则策略）

```bash
AI_ENABLED=false
# Bot 将比较 BTC 现价 vs 今开价格做决策
```

---

## 策略说明

Bot 同时运行两套信号，**必须两者都同意才开仓**：

### 信号 1：AI 决策

输入：
- BTC 当前价格、24h 高低点、日内变化
- 15 分钟 K 线形态（趋势/震荡）
- 3 分钟成交量变化
- 当前持仓状态和浮盈

输出：`BUY_UP` / `BUY_DOWN` / `HOLD`

### 信号 2：价差套利策略

```
BTC_5m_change = (BTC当前 - BTC_5min前) / BTC_5min前
signal = BTC_5m_change * 10   # 放大 10 倍
price_gap = PM_UP_price - 0.5  # Polymarket 定价偏离 50-50
divergence = signal - price_gap
```

条件：
- `divergence > 0.003` → 买入 UP
- `divergence < -0.003` → 买入 DOWN

### HOLD 条件（不开仓）

以下任一条件成立则观望：
- AI 信号 = HOLD
- 策略信号无明显偏离
- 当前已有持仓
- 剩余时间 < 3 分钟
- 点差 > 6%

---

## 控制面板功能

| 区域 | 内容 |
|------|------|
| 账户状态 | 总资金、可用现金、已实现盈亏 |
| 当前持仓 | 方向、价格、浮盈、剩余时间 |
| AI 思考记录 | 最新决策、AI 推理过程 |
| OpenClaw 信号 | Simmer 外部信号状态 |
| 交易开关 | 一键暂停/恢复交易 |

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `bot.py` | 交易 Bot 核心（独立运行） |
| `status_server.py` | Web 控制面板服务 |
| `scripts/bot_start.sh` | Bot 启动脚本 |
| `scripts/panel_start.sh` | 面板启动脚本 |
| `scripts/install.sh` | 安装依赖脚本 |
| `references/.env.example` | 环境变量模板 |
| `references/STRATEGY.md` | 策略逻辑详解 |
| `assets/public/` | 前端文件（HTML/CSS/JS）|

---

## 故障排查

### 面板打不开

```bash
# 检查端口是否在监听
ss -tlnp | grep 18095

# 检查面板进程
ps aux | grep status_server | grep -v grep

# 查看日志
tail -f bot.log
```

### AI 决策报错 500

- 检查 `AI_API_KEY` 是否正确
- 检查 `AI_BASE_URL` 是否与 `AI_PROVIDER` 匹配
- MiniMax 用户：确认 Base URL 是 `https://api.minimax.chat/v1`（不是 `/v1/chat/completions`）

### Bot 不下单

- 检查 Polymarket API Key 是否有效
- 检查余额是否充足（纸交易也需要有效 Key）
- 检查 `trading_enabled` 控制开关是否为 true

### decision_signal.json 报错

- 这是 Simmer 信号引擎的输出文件
- 无此文件时 AI 思考记录会显示错误
- 解决方法：配置 `SIMMER_API_KEY` 并启动 `simmer_bridge.py`

---

## 从 v1 升级

v2 主要改进：

1. **修复 MiniMax API 500 错误**：`response_format` 参数已移除
2. **多 AI 厂商支持**：环境变量配置，无需改代码
3. **路径可配置**：`BOT_DATA_DIR` 等支持自定义
4. **面板端口可配置**：`PANEL_PORT` 环境变量

**升级方法**：直接替换 `bot.py` 和 `status_server.py`，更新 `.env` 即可。
