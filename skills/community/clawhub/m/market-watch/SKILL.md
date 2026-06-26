---
name: "market-watch"
version: "1.2.1"
description: "Market monitoring and alert system for prices and news. Use when the user asks to watch a price, monitor market conditions, get notified when an asset hits a target, or keep an eye on breaking news. Covers any USDT-paired crypto and A-shares (real-time via TongDaXin)."
repository: "https://github.com/hchen13/market-watch"
---

# Market Watch Skill

两类监控，共享同一套 alert 数据结构和通知回路：

| 类型 | 数据源 | 状态 |
|------|--------|------|
| **价格盯盘** | HTTP 轮询（Binance/Hyperliquid/OKX/Bitget）+ CoinGecko fallback + pytdx（A股） | ✅ 已实现 |
| **新闻盯盘** | 金十数据、华尔街见闻（HTTP polling）+ CoinDesk/CoinTelegraph/The Block/Decrypt（RSS） | ✅ 已实现 |

---

## 数据源和精度

### 价格源

| 来源 | 协议 | 资产 | 延迟 |
|------|------|------|------|
| Binance | HTTP ticker（5s 轮询） | 任意 USDT 交易对（动态发现） | ~100ms |
| Hyperliquid | HTTP allMids（5s 轮询） | 全部 HL 上线资产（动态发现） | ~100ms |
| OKX | HTTP ticker（5s 轮询） | 任意 USDT SPOT（动态发现） | ~100ms |
| Bitget | HTTP ticker（5s 轮询） | 任意 USDT SPOT（动态发现） | ~100ms |
| pytdx | TCP 轮询（盘中 4s） | A股（沪深） | ~200ms |
| CoinGecko | HTTP 轮询（30s） | 全资产 fallback（动态发现） | 30s |

**动态交易对发现：** 守护进程启动时自动从各交易所拉取完整交易对列表，每小时刷新一次。任意 USDT 交易对的加密货币均自动支持，无需手动添加 symbol 映射。

**Asset → Exchange 优先级（按 EXCHANGE_PRIORITY 顺序，动态计算每个资产的可用交易所）：**
- 绝大多数主流币: Binance → Hyperliquid → OKX → Bitget → CoinGecko
- HYPE: Hyperliquid → OKX → Bitget → CoinGecko（Binance 无 HYPEUSDT 交易对）
- XAUT: OKX → CoinGecko（地区限制可能影响 OKX）
- 任何新上线或长尾币种：自动检查各交易所，无需改代码

### 新闻源

| 来源 | 类型 | 说明 |
|------|------|------|
| 金十数据 | HTTP 轮询 | ⚠️ 非官方接口，格式随时可能变更 |
| 华尔街见闻 | HTTP 轮询 | ⚠️ 非官方接口，同上 |
| CoinDesk | RSS 2.0 | 官方 RSS feed |
| CoinTelegraph | RSS 2.0 | 官方 RSS feed |
| The Block | RSS 2.0 | 官方 RSS feed |
| Decrypt | RSS / Atom | 官方 feed |

---

## Alert 数据结构

所有警报存入 `~/.openclaw/agents/{agent}/private/market-alerts.json`。

**公共字段（所有类型）：**
```json
{
  "id":               "eth-1741234567",
  "type":             "price",           // "price" | "news"
  "status":           "active",          // active | triggered | cancelled
  "one_shot":         true,
  "context_summary":  "ETH减仓窗口：减3.5枚，套出换HYPE",
  "session_key":      "agent:laok:feishu:direct:ou_xxx",
  "agent_id":         "laok",
  "reply_channel":    "feishu",
  "reply_to":         "user:ou_xxx",
  "transcript_file":  "/path/to/session.jsonl",
  "transcript_msg_id": "msg-id",
  "created_at":       "2026-03-12T13:00:00"
}
```

**价格类额外字段：**
```json
{
  "asset":        "ETH",
  "market":       "crypto",    // "crypto" | "astock"
  "condition":    ">=",        // >= | <= | > | <
  "target_price": 2150
}
```

**新闻类额外字段：**
```json
{
  "keywords":     ["BTC ETF", "BlackRock", "比特币"],
  "keyword_mode": "any",       // "any" | "all"
  "sources":      ["coindesk", "cointelegraph", "jin10"],
  "poll_interval": 300         // 秒，默认 300
}
```

---

## 价格盯盘工作流

### 设置价格警报

```bash
SKILL="$HOME/.openclaw/skills/market-watch/scripts"

python3 "$SKILL/register-price-alert.py" \
  --agent laok \
  --asset ETH \
  --market crypto \
  --condition ">=" \
  --target 2150 \
  --context-summary "ETH减仓窗口：减3.5枚ETH（OKX），套出约\$7,500买HYPE" \
  --session-key "agent:laok:feishu:direct:ou_xxx" \
  --reply-channel feishu \
  --reply-to "user:ou_xxx"
```

**参数说明：**
- `--market`: `crypto`（加密）或 `astock`（A股，代码如 `600519`）
- `--condition`: `>=` / `<=` / `>` / `<`
- `--session-key`: 用户的当前 session key（稳定标识，用于触发时找到正确 session）
- `--reply-to`: 飞书通知目标，格式 `user:ou_xxx`
- `--transcript-msg-id`: **推荐填入**当前对话的 message_id（触发时用于追溯设盘上下文）。agent 在注册警报时应传入当前消息的 ID，否则触发通知中「消息ID」字段将为空，无法精准跳转到设盘时的对话记录。

---

## 新闻盯盘工作流

### 设置新闻关键词警报

```bash
# 基础用法：监控任一关键词命中
python3 "$SKILL/register-news-alert.py" \
  --agent laok \
  --keywords "BTC ETF,BlackRock,ETF通过" \
  --keyword-mode any \
  --context-summary "盯 ETF 审批进展，可能触发价格上涨" \
  --session-key "agent:laok:feishu:direct:ou_xxx" \
  --reply-channel feishu \
  --reply-to "user:ou_xxx"

# 一次性警报（发现即停，适合等待明确事件）
python3 "$SKILL/register-news-alert.py" \
  --agent laok \
  --keywords "停火,ceasefire,Iran deal" \
  --one-shot \
  --context-summary "等停火消息，判断是否影响风险资产"

# 仅监控特定来源
python3 "$SKILL/register-news-alert.py" \
  --agent laok \
  --keywords "HYPE,Hyperliquid" \
  --sources "coindesk,cointelegraph,theblock,decrypt"

# 全部命中模式（需要所有关键词同时出现在同一条新闻中）
python3 "$SKILL/register-news-alert.py" \
  --agent laok \
  --keywords "BTC,ETF,SEC" \
  --keyword-mode all
```

**参数说明：**
- `--keywords`: 关键词，逗号分隔（支持中英文）
- `--keyword-mode`: `any`（任一命中）| `all`（全部命中），默认 `any`
- `--sources`: 数据源，逗号分隔，可选：`jin10, wallstreetcn, coindesk, cointelegraph, theblock, decrypt`（默认全部）
- `--poll-interval`: 轮询间隔（秒），默认 300（5分钟）
- `--one-shot`: 触发一次后自动停止（新闻警报默认持续监控）

---

## 守护进程管理

```bash
DAEMON="$HOME/.openclaw/skills/market-watch/scripts/daemon.sh"

bash "$DAEMON" start    # 按需启动（检查活跃警报类型，只启动需要的进程）
bash "$DAEMON" stop     # 停止两个进程
bash "$DAEMON" restart  # 重启
bash "$DAEMON" status   # 状态 + 活跃警报列表
bash "$DAEMON" log      # 两个进程的最近 40 行日志
bash "$DAEMON" log --lines 100  # 更多日志
```

**文件路径:**
- 价格进程 PID：`/tmp/market-watch-{agent}-price.pid`
- 新闻进程 PID：`/tmp/market-watch-{agent}-news.pid`
- 价格日志：`/tmp/market-watch-{agent}.log`
- 新闻日志：`/tmp/market-watch-{agent}-news.log`
- 警报数据：`~/.openclaw/agents/{agent}/private/market-alerts.json`
- 新闻去重：`~/.openclaw/agents/{agent}/private/news-monitor-state.json`

---

## 查看和取消警报

```bash
python3 "$SKILL/cancel-alert.py" --agent laok --list            # 列出全部活跃警报
python3 "$SKILL/cancel-alert.py" --agent laok --id eth-1741234  # 按 ID 取消
python3 "$SKILL/cancel-alert.py" --agent laok --asset ETH       # 取消资产所有警报
python3 "$SKILL/cancel-alert.py" --agent laok --type price      # 取消所有价格警报
python3 "$SKILL/cancel-alert.py" --agent laok --type news       # 取消所有新闻警报
python3 "$SKILL/cancel-alert.py" --agent laok --all             # 取消全部
```

---

## 收到 `[MARKET_ALERT 触发]` 时

注入消息格式：`[MARKET_ALERT 触发 · 请处理后联系用户]`

处理步骤：
1. 读取 `context_summary`（设盘时的上下文核心）
2. 如需更多细节，读取 `transcript_file` 指定位置
3. **以自己的口吻主动告知用户**：条件已触达，当前价格是多少
4. 结合当前市场给出简要判断，询问是否执行操作

---

## 收到 `[NEWS_ALERT 触发]` 时

注入消息格式：`[NEWS_ALERT 触发 · 需要你判断]`

**你不是传话筒，你是过滤器+分析师。** 关键词匹配只是粗筛，大量命中可能是噪音。你的工作是精筛。

处理步骤：
1. 阅读通知里附带的**完整新闻正文**
2. 读取 `设盘背景`（用户当初为什么要盯这个关键词、他关心的是什么）
3. **判断相关性**：这条新闻是否真的跟用户关心的事情相关？还是关键词碰巧命中了无关内容？
4. **决策**：
   - 确实相关且重要 → 联系用户，附上你的分析和建议
   - 相关但不紧急 → 可以记录下来，等积累到足够有价值时再汇报
   - 噪音（关键词碰巧命中但内容无关）→ **不联系用户，直接忽略**
   - 拿不准 → 宁可不发，避免噪音打扰

**批量命中时**（一轮多条）：逐条判断，只挑真正有价值的告知用户，不要一股脑全转发。

---

## 注意事项

- **任意加密货币**：只要该币在 Binance/OKX/Bitget 有 USDT 交易对，或在 Hyperliquid/CoinGecko 上架，即可直接使用，无需改代码或重启 daemon
- **交易对列表刷新**：启动时自动拉取，每小时刷新一次；如某个交易所加载失败，保留上次缓存继续运行
- **HYPE**: 优先用 Hyperliquid HTTP（allMids 含 HYPE 现货 mid price）→ OKX → Bitget → CoinGecko
- **XAUT**: 仅 OKX 有，可能因地区限制失败，CoinGecko 兜底
- **A股**: 只在交易时段（9:30-11:30 / 13:00-15:00）轮询，非交易时段自动跳过
- **金十/华尔街见闻**: 非官方接口，接口变更时 monitor 会静默跳过，不影响 RSS 源继续工作
- **新闻警报默认持续监控**：不会自动停止，需要手动 cancel 或设置 `--one-shot`
- **价格警报默认一次性触发**：触发后标记 triggered，停止监控
