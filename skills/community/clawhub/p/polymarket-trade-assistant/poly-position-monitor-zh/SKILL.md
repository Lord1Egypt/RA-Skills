---
name: poly-position-monitor-zh
version: 1.0.2
description: 监控 Polymarket 持仓和挂单。检测价格异常、成交量暴涨、巨鲸活动和仓位变化，通过终端、Telegram 和邮件发送告警。当用户要求监控 Polymarket 持仓、追踪钱包活动、设置持仓告警、或监视持仓市场异动时使用此技能。
metadata: {"openclaw": {"emoji": "👁️", "requires": {"bins": ["python3"]}, "envVars": [{"name": "POLY_API_KEY", "required": false, "description": "CLOB API key for order monitoring (optional, can use config file)"}, {"name": "POLY_SECRET", "required": false, "description": "CLOB API secret"}, {"name": "POLY_PASSPHRASE", "required": false, "description": "CLOB API passphrase"}]}}
---

# Polymarket 持仓监控

实时监控 Polymarket 钱包持仓。检测所有持仓市场的 5 类异常，通过终端、Telegram 和邮件推送告警。

## 异常类型

1. **价格波动** — 5/15/60/240 分钟窗口内相对价格变化超过阈值
2. **成交量异动** — 交易量相对滚动均值暴涨或暴跌
3. **大额流入** — 新开仓位或仓位规模显著变化
4. **巨鲸活动** — 监控地址在用户持仓市场发生交易
5. **挂单变化** — 挂单被成交、部分成交或取消

## 工作流程

按顺序执行以下 6 个步骤。

### 第 1 步：配置

复制示例配置并填入凭证：

```bash
cp scripts/config.example.json ~/polymarket-monitoring/config.json
```

编辑 `~/polymarket-monitoring/config.json`：

1. **user_addresses**：添加用户的 Polymarket 钱包地址
2. **watched_addresses**：添加需要监控的巨鲸/知名地址（附标签）
3. **clob_auth**：添加 API 凭证用于挂单监控（见下方）
4. **thresholds**：按需调整告警阈值（见 [references/alert-thresholds.md](references/alert-thresholds.md)）
5. **notifications**：启用 Telegram 和/或邮件通知

**获取 CLOB API 凭证：**

```python
from py_clob_client.client import ClobClient
client = ClobClient("https://clob.polymarket.com", chain_id=137, key="YOUR_PRIVATE_KEY")
creds = client.create_or_derive_api_creds()
print(creds)  # {"apiKey": "...", "secret": "...", "passphrase": "..."}
```

**设置 Telegram Bot：**
1. 在 Telegram 中搜索 @BotFather，创建 Bot 并获取 token
2. 向 Bot 发送一条消息，然后调用 `https://api.telegram.org/bot<TOKEN>/getUpdates` 获取 chat_id
3. 将 `telegram.enabled` 设为 `true`，填入 `bot_token` 和 `chat_id`

### 第 2 步：安装依赖

```bash
pip install py-clob-client
```

仅挂单监控需要此依赖。持仓追踪、价格分析、成交量追踪和巨鲸检测仅使用 Python 标准库。

### 第 3 步：初始快照

运行持仓获取脚本，验证连通性并查看当前持仓：

```bash
python scripts/fetch_positions.py <wallet_address>
```

输出所有活跃仓位、对应市场、当前价值和盈亏。确认输出无误后再启动监控。

### 第 4 步：验证连接

逐个测试各组件：

```bash
# 测试价格历史（使用第 3 步输出中的 asset_id）
python scripts/fetch_price_history.py <token_id>

# 测试市场成交（使用第 3 步输出中的 condition_id）
python scripts/fetch_market_activity.py trades --market <condition_id>

# 测试挂单获取（需要认证）
python scripts/fetch_orders.py --config ~/polymarket-monitoring/config.json
```

如果已配置 Telegram，监控首次运行时会发送测试告警。

### 第 5 步：启动监控

```bash
python scripts/monitor.py --config ~/polymarket-monitoring/config.json
```

监控持续运行，每隔 `interval_seconds`（默认 60 秒）检查一次。

**选项：**
- `--once` — 运行单次检查后退出（适合 cron 定时任务）
- `--interval 30` — 覆盖检查间隔为 30 秒

**Cron 定时任务**（替代持续运行模式）：
```bash
# 每 2 分钟检查一次
*/2 * * * * cd {baseDir} && python scripts/monitor.py --config ~/polymarket-monitoring/config.json --once >> ~/polymarket-monitoring/cron.log 2>&1
```

**优雅退出：** Ctrl-C 保存最终状态后退出。

### 第 6 步：日常管理

**查看告警历史：**
```bash
# 最近告警（JSON Lines 格式）
tail -20 ~/polymarket-monitoring/alerts.jsonl

# 按类型筛选
grep '"CRITICAL"' ~/polymarket-monitoring/alerts.jsonl
grep '"whale"' ~/polymarket-monitoring/alerts.jsonl
```

**查看状态快照：**
```bash
ls ~/polymarket-monitoring/snapshot-*.json
cat ~/polymarket-monitoring/monitor-state.json
```

**增删监控地址：** 编辑 config.json 中的 `watched_addresses`，下次检查周期自动生效。

**调整阈值：** 编辑 config.json 中的 `thresholds`。调参指南见 [references/alert-thresholds.md](references/alert-thresholds.md)。

## 故障排除

- **未找到持仓**：确认钱包地址正确，且在 Polymarket 上有活跃（未赎回）仓位
- **价格历史为空**：token_id（asset_id）可能无效。确认仓位的 asset_id 对应有效的 CLOB 代币
- **挂单获取失败**：验证 API 凭证。如需要可用 `create_or_derive_api_creds()` 重新生成
- **Telegram 不发送**：检查 bot token 和 chat_id。确保用户已先向 Bot 发送过至少一条消息
- **告警过多**：在 config.json 中调高阈值。将通知的 `min_level` 设为 "ALERT" 或 "CRITICAL"
- **速率限制**：增大 `interval_seconds`。监控每个市场每个周期约发起 3 次 API 调用

## 参考文件

- [references/polymarket-api.md](references/polymarket-api.md) — API 端点文档
- [references/alert-thresholds.md](references/alert-thresholds.md) — 阈值调参指南
- [references/output-template.md](references/output-template.md) — 告警格式规范
