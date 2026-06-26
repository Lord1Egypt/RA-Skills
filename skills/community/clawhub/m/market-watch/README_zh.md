# market-watch

[English](README.md) | **中文**

**给 OpenClaw agent 用的实时行情监控与警报系统。**

通过 HTTP 轮询监控任意 USDT 交易对加密货币价格和 A 股行情，同时监控金十数据、华尔街见闻、CoinDesk、CoinTelegraph、The Block、Decrypt 等新闻源的关键词命中。当价格触达条件或新闻命中关键词时，自动通知 agent，由 agent 主动联系用户。

交易所 symbol 映射在启动时自动从各交易所公开 API 拉取，每小时刷新一次。任意 USDT 交易对的加密货币均自动支持，无需手动添加 symbol 映射或重启 daemon。

> 这是一个 [OpenClaw](https://github.com/openclaw) AgentSkill，任何 OpenClaw agent 即插即用。

---

## 实际使用场景

### 价格警报

**周五晚上。** BTC 在 $67K 附近震荡，你觉得跌破 $65K 是个不错的进场机会。但你不会无脑挂限价单——上次 BTC 在暴跌中到过这个价位，抄底的人被套了半年。你要的不是自动成交，而是有人叫你起来看一眼当时的情况。

你跟 agent 说：

> "BTC 跌破 65K 通知我。我想加仓，但到时候帮我先看看是什么情况——如果是恐慌性抛售可能还会跌，如果只是技术回调就可以进。"

三天后，凌晨 4 点。BTC 跌到 $64,800。守护进程捕获。agent 醒来——但它不是简单告诉你"到价了"，而是查看了最新新闻、funding rate、清算数据，然后给你发消息：

> "BTC 跌破 65K，现在 $64,800。快速看了一圈：触发原因是 Binance 一笔 $120M 的连环清算，funding rate 翻负，没有基本面利空。看起来是技术性超卖，不是趋势反转。按你的计划，现在可以考虑加仓那 0.1 BTC。"

### 新闻警报

**战争第三周。** 你持有黄金，整个持仓逻辑建立在战争溢价之上。你不怕打仗继续——怕的是突然停火，金价一天跌 5%，你没来得及跑。

你跟 agent 说：

> "帮我盯着停火和和谈的消息。但不要每条提到'停火'的新闻都推给我——外交官一天说十次这个词，什么都没发生。只有看起来像是真正有进展的消息才通知我。"

两天后，一条快讯弹出：*"伊朗最高领袖通过瑞士渠道向美方传递信息，愿意在霍尔木兹海峡问题上做出让步。"*

守护进程命中关键词。agent 读完全文，想了一下，判断：这不是日常的外交辞令——有具体的渠道（瑞士）、具体的让步内容（霍尔木兹）。这是实质性信号。于是联系你：

> "截获一条可能影响你黄金仓位的消息：伊朗通过瑞士渠道释放和谈信号，愿意在霍尔木兹问题上让步。这跟之前'呼吁和平'的套话不一样——有具体渠道和具体议题。如果属实，战争溢价可能快速回撤。建议考虑先减部分黄金仓位锁定利润。"

---

## 功能

| 功能 | 状态 |
|------|------|
| **价格警报** — HTTP 轮询 Binance / Hyperliquid / OKX / Bitget / CoinGecko | ✅ |
| **A 股警报** — pytdx TCP 轮询（盘中 4 秒间隔） | ✅ |
| **新闻警报** — 金十、华尔街见闻、CoinDesk、CoinTelegraph、The Block、Decrypt | ✅ |
| **守护进程管理** — 后台运行，launchd 看门狗自动重启 | ✅ |

---

## 快速开始

### 1. 安装依赖

```bash
pip3 install requests pytdx
```

### 2. 注册价格警报

```bash
SKILL="$HOME/.openclaw/skills/market-watch/scripts"

python3 "$SKILL/register-price-alert.py" \
  --agent your-agent-id \
  --asset ETH \
  --market crypto \
  --condition ">=" \
  --target 2150 \
  --context-summary "ETH 减仓窗口：卖 3.5 枚 ETH 换 HYPE" \
  --session-key "agent:your-agent:feishu:direct:ou_xxx" \
  --reply-channel feishu \
  --reply-to "user:ou_xxx"
```

### 3. 注册新闻警报

```bash
python3 "$SKILL/register-news-alert.py" \
  --agent your-agent-id \
  --keywords "BTC ETF,BlackRock,比特币" \
  --keyword-mode any \
  --sources "coindesk,cointelegraph,jin10" \
  --context-summary "盯 ETF 审批进展，可能触发价格波动" \
  --session-key "agent:your-agent:feishu:direct:ou_xxx" \
  --reply-channel feishu \
  --reply-to "user:ou_xxx"

# 一次性（发现一条就停，适合等待明确事件）
python3 "$SKILL/register-news-alert.py" \
  --agent your-agent-id \
  --keywords "停火,ceasefire,Iran deal" \
  --one-shot \
  --context-summary "等停火消息，判断是否影响风险资产"

# 只盯 RSS 源（不用金十/华尔街见闻）
python3 "$SKILL/register-news-alert.py" \
  --agent your-agent-id \
  --keywords "HYPE,Hyperliquid" \
  --sources "coindesk,cointelegraph,theblock,decrypt"
```

> 注册后自动拉起守护进程，无需手动启动。

### 4. 手动管理守护进程

```bash
DAEMON="$HOME/.openclaw/skills/market-watch/scripts/daemon.sh"

bash "$DAEMON" start   --agent your-agent-id   # 按需启动（检查活跃警报类型）
bash "$DAEMON" stop    --agent your-agent-id   # 停止两个进程
bash "$DAEMON" status  --agent your-agent-id   # 查看两个进程状态
bash "$DAEMON" log     --agent your-agent-id   # 查看两个进程日志
```

### 5. 取消警报

```bash
SCRIPT="$HOME/.openclaw/skills/market-watch/scripts/cancel-alert.py"

python3 "$SCRIPT" --agent your-agent-id --list              # 列出活跃警报
python3 "$SCRIPT" --agent your-agent-id --id eth-1741234    # 按 ID 取消
python3 "$SCRIPT" --agent your-agent-id --asset ETH         # 取消所有 ETH 警报
python3 "$SCRIPT" --agent your-agent-id --type price        # 取消所有价格警报
python3 "$SCRIPT" --agent your-agent-id --type news         # 取消所有新闻警报
python3 "$SCRIPT" --agent your-agent-id --all               # 取消全部
```

### 6.（macOS）安装看门狗

每 5 分钟检查一次，崩溃后自动重启：

```bash
bash "$HOME/.openclaw/skills/market-watch/scripts/install-watchdog.sh" install --agent your-agent-id
```

---

## 数据源

### 价格数据

| 交易所 | 协议 | 支持资产 | 延迟 |
|--------|------|---------|------|
| Binance | HTTP ticker（5s 轮询） | 全部 USDT 交易对（动态发现） | ~100ms |
| Hyperliquid | HTTP allMids（5s 轮询） | 全部 HL 上线资产（动态发现） | ~100ms |
| OKX | HTTP ticker（5s 轮询） | 全部 USDT SPOT（动态发现） | ~100ms |
| Bitget | HTTP ticker（5s 轮询） | 全部 USDT SPOT（动态发现） | ~100ms |
| CoinGecko | HTTP 轮询（30s 兜底） | 全资产 fallback（动态发现） | ~30s |
| pytdx | TCP 请求-响应 | A 股（沪深） | ~200ms |

**动态 symbol 发现：** 启动时自动从各交易所公开 API 拉取完整交易对列表，每小时刷新。无硬编码 symbol 表，任何 USDT 交易对的币种即开即用。

**取价优先级（按 EXCHANGE_PRIORITY 顺序，动态计算每个资产的可用交易所）：**
- 绝大多数主流币：Binance → Hyperliquid → OKX → Bitget → CoinGecko
- HYPE：Hyperliquid → OKX → Bitget → CoinGecko（Binance 无 HYPEUSDT 交易对）
- XAUT：OKX → CoinGecko
- A 股（如 `601899`）：仅 pytdx（交易时段：周一至周五 9:30–11:30 / 13:00–15:00）

### 新闻数据

| 来源 | 类型 | 说明 |
|------|------|------|
| 金十数据 | HTTP 轮询 | ⚠️ 非官方接口，格式随时可能变更 |
| 华尔街见闻 | HTTP 轮询 | ⚠️ 非官方接口，同上 |
| CoinDesk | RSS feed | `https://www.coindesk.com/arc/outboundfeeds/rss/` |
| CoinTelegraph | RSS feed | `https://cointelegraph.com/rss` |
| The Block | RSS feed | `https://www.theblock.co/rss.xml` |
| Decrypt | RSS feed | `https://decrypt.co/feed` |

> ⚠️ **金十和华尔街见闻是非官方接口。** 可能随时加防爬或改变响应格式。代码内置降级处理：某一源失败时，其余数据源继续正常工作。

---

## 架构

```
┌────────────────────────────────────────────────────────────────┐
│                    AI Agent（OpenClaw）                         │
│  register-price-alert.py / register-news-alert.py             │
└──────────────────────────┬─────────────────────────────────────┘
                           │ 写入 alert 到 JSON
                           ▼
┌────────────────────────────────────────────────────────────────┐
│         market-alerts.json（共享状态文件）                      │
│    ~/.openclaw/agents/{agent}/private/                         │
└─────────┬─────────────────────────────────────┬───────────────┘
          │ 每 5 秒读取                          │ 每 5 分钟读取
          ▼                                      ▼
┌─────────────────────┐         ┌──────────────────────────────┐
│  price-monitor.py   │         │  news-monitor.py              │
│  （守护进程）        │         │  （守护进程）                 │
│                     │         │                               │
│  HTTP 轮询 5s：     │         │  HTTP 轮询（默认 5min）：     │
│  Binance → HL       │         │  金十 / 华尔街见闻            │
│  → OKX → Bitget     │         │  CoinDesk / CoinTelegraph    │
│  → CoinGecko        │         │  The Block / Decrypt         │
│                     │         │                               │
│  A 股 4s（盘中）：  │         │  关键词匹配（any/all）        │
│  pytdx TCP          │         │  hash 去重（滚动窗口 1000）   │
└──────────┬──────────┘         └──────────────┬───────────────┘
           │                                   │
           └─────────────┬─────────────────────┘
                         │ openclaw agent --deliver
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                  Agent session 收到：                           │
│  [MARKET_ALERT 触发] / [NEWS_ALERT 触发]                      │
│  • 触达条件 / 命中关键词 + 来源                                │
│  • 注册时的 context_summary                                    │
│  • transcript_file 路径用于完整上下文回溯                      │
└────────────────────────────────────────────────────────────────┘
```

**关键设计决策：**

- **HTTP 轮询而非 WebSocket** — 省代理流量，重连逻辑简单，无状态
- **JSON 文件共享状态** — 零 IPC 复杂度，agent 和 daemon 通过文件系统通信
- **无活跃警报自动退出** — 两个 daemon 各自独立按需拉起，不常驻
- **价格警报：默认一次性触发** — 触发后标记 `triggered`，停止监控
- **新闻警报：默认持续监控** — 不断扫描直到取消或设置 `--one-shot`
- **hash 去重滚动窗口** — 每个警报保留最近 1000 个 hash，防止内存无限增长
- **上下文回溯** — alert 携带 `transcript_file` + `transcript_msg_id`，agent 可精确还原用户意图

---

## 文件结构

```
market-watch/
├── SKILL.md                        # OpenClaw agent 指令（agent 运行时自动加载）
├── README.md                       # 英文说明
├── README_zh.md                    # 本文件
├── scripts/
│   ├── register-price-alert.py    # 注册价格警报 + 自动拉起 daemon
│   ├── register-news-alert.py     # 注册新闻关键词警报 + 自动拉起 daemon
│   ├── cancel-alert.py            # 列出 / 取消活跃警报（支持 --type news）
│   ├── price-monitor.py           # 后台守护进程 — 取价、检查条件
│   ├── news-monitor.py            # 后台守护进程 — 抓新闻、关键词匹配
│   ├── daemon.sh                  # 进程生命周期：start/stop/restart/status/log/ensure
│   └── install-watchdog.sh        # macOS launchd 看门狗（崩溃自动重启）
└── references/
    └── exchange-api.md            # 交易所和新闻源 HTTP API 参考
```

---

## 警报数据格式

警报存储在 `~/.openclaw/agents/{agent}/private/market-alerts.json`：

### 价格警报
```json
{
  "id":                "eth-1741234567",
  "type":              "price",
  "status":            "active",
  "asset":             "ETH",
  "market":            "crypto",
  "condition":         ">=",
  "target_price":      2150,
  "one_shot":          true,
  "context_summary":   "ETH 减仓窗口：卖 3.5 枚 ETH 换 HYPE",
  "session_key":       "agent:your-agent:feishu:direct:ou_xxx",
  "agent_id":          "your-agent",
  "reply_channel":     "feishu",
  "reply_to":          "user:ou_xxx",
  "created_at":        "2026-03-12T13:00:00"
}
```

### 新闻警报
```json
{
  "id":                "news-1741234567",
  "type":              "news",
  "status":            "active",
  "keywords":          ["BTC ETF", "BlackRock", "比特币"],
  "keyword_mode":      "any",
  "sources":           ["coindesk", "cointelegraph", "jin10"],
  "poll_interval":     300,
  "one_shot":          false,
  "context_summary":   "盯 ETF 审批进展",
  "session_key":       "agent:your-agent:feishu:direct:ou_xxx",
  "agent_id":          "your-agent",
  "reply_channel":     "feishu",
  "reply_to":          "user:ou_xxx",
  "created_at":        "2026-03-12T13:00:00"
}
```

**状态流转：** `active` → `triggered`（条件触达 / 关键词命中）| `cancelled`（手动取消）

---

## 给 AI Agent 的指引

本 skill 附带 `SKILL.md`，OpenClaw agent 运行时会自动加载。运行时不需要读这个 README。

**什么时候激活：**
- 用户说"帮我盯 BTC"、"ETH 到 2150 通知我"、"set a price alert"
- 用户说"帮我盯 ETF 相关新闻"、"停火消息出来通知我"、"monitor BlackRock news"
- 用户要取消或查看当前警报
- 收到 `[MARKET_ALERT 触发]` 或 `[NEWS_ALERT 触发]`

**任意加密货币：**
- 只要该币在 Binance/OKX/Bitget 有 USDT 交易对，或在 Hyperliquid/CoinGecko 上架，即可直接使用，无需改代码
- Symbol 映射每小时自动刷新；只有极新上线的币（上线不足1小时）才需要重启 daemon 立即生效

---

## 运行时文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 警报数据库 | `~/.openclaw/agents/{agent}/private/market-alerts.json` | 共享警报状态 |
| 新闻去重状态 | `~/.openclaw/agents/{agent}/private/news-monitor-state.json` | hash 去重窗口 |
| 价格进程 PID | `/tmp/market-watch-{agent}-price.pid` | price-monitor PID |
| 新闻进程 PID | `/tmp/market-watch-{agent}-news.pid` | news-monitor PID |
| 价格日志 | `/tmp/market-watch-{agent}.log` | 轮转日志（512KB × 3） |
| 新闻日志 | `/tmp/market-watch-{agent}-news.log` | 轮转日志（512KB × 4） |
| 看门狗配置 | `~/Library/LaunchAgents/com.openclaw.market-watch.{agent}.plist` | macOS launchd 配置 |

---

## 环境要求

- Python 3.10+
- `requests`（`pip3 install requests`）
- `pytdx`（`pip3 install pytdx`）— A 股实时行情
- [OpenClaw](https://github.com/openclaw) agent 运行时（提供 `openclaw agent --deliver`）
- macOS 或 Linux（launchd 看门狗仅 macOS；Linux 可用 cron 替代）

---

## License

MIT
