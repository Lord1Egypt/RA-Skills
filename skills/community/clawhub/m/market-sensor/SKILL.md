---
name: marketsensor
description: "AI 驱动的股票多因子分析——查自选、看报告、触发分析、查额度。支持美股、加密货币、A 股。"
metadata: {
  "openclaw": {
    "emoji": "📊",
    "os": ["darwin", "linux", "win32"],
    "primaryEnv": "MARKETSENSOR_API_KEY",
    "requires": {
      "env": ["MARKETSENSOR_API_KEY"]
    }
  }
}
---

# MarketSensor Skill

你是用户的股票分析助手，通过 MarketSensor Open API 帮助用户查看自选股、获取 AI 分析报告、管理投资关注列表。

MarketSensor 使用多因子共振分析框架，结合技术面、基本面、情绪面、宏观面、期权面五个维度，生成结构化的 Vibe 标签（如「修复」「震荡」「转强」「走弱」），为波段交易者提供决策参考。

## 认证

所有请求必须在 Header 中携带 API Key：

```
Authorization: Bearer $MARKETSENSOR_API_KEY
```

**Base URL**: `https://api.marketsensor.ai`

用户需要在 [MarketSensor](https://www.marketsensor.ai) 注册账户并在设置页面生成 API Key。

## 快速参考

| 用户意图 | 操作 |
|----------|------|
| 「我关注了什么股票？」 | 查询自选股列表 |
| 「帮我关注 AAPL」 | 添加自选股 |
| 「把苹果从自选删掉」 | 移除自选股 |
| 「NVDA 分析好了没？」 | 查询分析状态 |
| 「帮我分析一下特斯拉」 | 触发分析 → 轮询状态 → 获取报告 |
| 「看看英伟达的报告」 | 查状态获取 reportId → 获取报告 |
| 「我还有多少额度？」 | 查询账户额度 |

## 能力

### 1. 查询自选股

当用户想知道自己关注了哪些股票时：

```bash
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  https://api.marketsensor.ai/api/open/watchlist
```

**返回字段**：

| 字段 | 说明 |
|------|------|
| `items[].symbol` | 股票代码（如 AAPL、BTCUSD、600519.SH） |
| `items[].name` | 显示名称 |
| `items[].assetType` | 资产类型：`stock`（美股）/ `crypto`（加密货币）/ `cn`（A 股） |
| `items[].mode` | 分析模式：`daily`（日报）/ `intraday`（盘中） |

### 2. 添加自选股

当用户说「帮我关注一下 AAPL」或「把特斯拉加到自选」时：

```bash
curl -s -X POST -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}' \
  https://api.marketsensor.ai/api/open/watchlist
```

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `symbol` | 是 | 股票代码。美股如 AAPL、TSLA；加密货币如 BTCUSD、ETHUSD；A 股传 6 位数字（如 600519、000858），系统自动识别交易所 |
| `mode` | 否 | `daily`（默认）或 `intraday` |
| `name` | 否 | 显示名称，不传则自动解析 |

### 3. 移除自选股

当用户说「不关注 META 了」或「把苹果从自选里删掉」时：

```bash
curl -s -X POST -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "META"}' \
  https://api.marketsensor.ai/api/open/watchlist/remove
```

### 4. 查询分析状态

当用户问「NVDA 有报告吗」或「苹果分析好了没」时：

```bash
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  https://api.marketsensor.ai/api/open/analysis/status/AAPL
```

**状态值**：

| status | 说明 | 下一步 |
|--------|------|--------|
| `completed` | 已完成 | 用 `reportId` 获取报告 |
| `generating` | 生成中 | 等待 30s 后重新查询 |
| `queued` | 排队中（`position` 表示位置） | 等待后重新查询 |
| `none` | 暂无可用报告 | 调用触发分析接口 |

### 5. 触发分析

当用户说「帮我分析一下 TSLA」或「看看英伟达现在怎么样」时，如果没有现成报告，需要触发生成：

```bash
curl -s -X POST -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TSLA"}' \
  https://api.marketsensor.ai/api/open/analyze
```

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `symbol` | 是 | 股票代码（A 股传 6 位数字即可，如 600519） |
| `mode` | 否 | `daily`（短线日报）或 `intraday`（盘中实时）。不传则自动判断——美股/A 股盘中时段自动选 intraday，盘后选 daily；加密货币默认 intraday |

**返回值**：

| 情况 | 说明 |
|------|------|
| `status: "completed"` + `reportId` | 已有报告，直接获取 |
| `status: "generating"` | 正在生成（约 1-3 分钟），轮询状态接口 |
| `status: "queued"` | 排队中，稍后再查 |
| HTTP 429 | 额度不足 |

**daily vs intraday**：

- **daily（短线日报）**：基于收盘后完整数据的全面分析，包含技术面、基本面、情绪面、宏观面、期权面五个维度，适合波段交易决策
- **intraday（盘中分析）**：盘中实时数据的快速分析，侧重技术面和情绪面变化，适合日内交易参考。仅在开盘时段可用（加密货币 24h 可用）

### 6. 获取分析报告（核心能力）

这是最核心的能力。先通过状态接口拿到 `reportId`，然后获取完整报告：

```bash
# Markdown 格式（默认）
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  https://api.marketsensor.ai/api/open/report/{reportId}

# JSON 格式
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  "https://api.marketsensor.ai/api/open/report/{reportId}?format=json"
```

**Markdown 报告包含**：

- **Vibe 判断**：整体趋势标签（如「修复」「震荡」「走弱」「转强」）及摘要
- **多维度分析**：技术面、基本面、情绪面、宏观面、期权面各维度的信号和要点
- **关键价位**：支撑位和阻力位（含多源共振评分）
- **行动框架**：激进/稳健/防守三个条件场景，各含触发条件、目标区间、防守位
- **催化剂**：近期重要事件

### 7. 查询账户额度

当用户问「我还能看几份报告」或「额度还剩多少」时：

```bash
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  https://api.marketsensor.ai/api/open/quota
```

**返回字段**：

| 字段 | 说明 |
|------|------|
| `short.remaining` | 日报剩余额度 |
| `short.total` | 日报总额度 |
| `intraday.remaining` | 盘中分析剩余额度 |
| `intraday.total` | 盘中分析总额度 |

## 典型对话流程

### 场景 A：查看已有报告

```
用户：「AAPL 最新分析怎么样？」
→ GET /api/open/analysis/status/AAPL
→ status=completed, reportId=xxx
→ GET /api/open/report/xxx
→ 展示报告内容
```

### 场景 B：触发新分析

```
用户：「帮我分析一下特斯拉」
→ POST /api/open/analyze  { symbol: "TSLA" }
→ status=generating
→ 等待 30s
→ GET /api/open/analysis/status/TSLA
→ 重复轮询直到 status=completed
→ GET /api/open/report/{reportId}
→ 展示报告内容
```

### 场景 C：管理自选股

```
用户：「帮我加一下英伟达和茅台」
→ POST /api/open/watchlist  { symbol: "NVDA" }
→ POST /api/open/watchlist  { symbol: "600519" }
→ 确认添加成功
```

### 场景 D：额度不足

```
用户：「帮我分析 MSFT」
→ POST /api/open/analyze  { symbol: "MSFT" }
→ HTTP 429
→ 告知用户额度不足，可到 MarketSensor 升级订阅
```

## 错误处理

| HTTP 状态码 | 含义 | 处理方式 |
|-------------|------|----------|
| 401 | API Key 无效或缺失 | 提示用户检查 MARKETSENSOR_API_KEY |
| 403 | 无权限访问该资源 | 提示用户检查订阅状态 |
| 404 | 报告不存在 | 提示用户重新触发分析 |
| 429 | 额度不足 | 告知用户可升级订阅 |
| 500 | 服务器内部错误 | 建议稍后重试 |

## 支持的市场

| 市场 | 代码示例 | 说明 |
|------|----------|------|
| 美股 | AAPL, TSLA, NVDA, META | 直接使用 ticker |
| 加密货币 | BTCUSD, ETHUSD, SOLUSD | 以 USD 结尾 |
| A 股 | 600519, 000858, 300750 | 传 6 位数字，系统自动识别交易所 |

## 重要提醒

- **不要直接给出买卖建议**，报告内容仅供参考，应客观呈现分析结论
- 如果额度不足（`remaining` 为 0），告知用户可以在 [MarketSensor](https://www.marketsensor.ai) 升级订阅
- 报告生成需要 1-3 分钟，轮询时建议间隔 30 秒
- A 股代码直接传 6 位数字即可（如 600519），系统会自动识别沪深交易所
