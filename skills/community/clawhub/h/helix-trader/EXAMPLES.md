# 对话示例

## 0）用户要启动机器人（最常见）

```text
用户: 帮我启动这个机器人
Agent: 调用 doctor（含 network）
Agent: 如需则跑 setup / 起后端 / login
Agent: 问：你想用哪个交易所的测试网？OKX 还是 Binance？
用户: OKX
Agent: 若未保存凭证 → 引导两步保存测试网 Key
Agent: 调用 list_strategies
Agent: 说明有两个策略，默认推荐趋势跟随；你要趋势还是突破？
用户: 你推荐的就行
Agent: 调用 preview_bot_config（trend_following_core + okx）
Agent: 展示预览摘要，请用户确认
用户: 确认启动
Agent: 调用 start_bot
Agent: 主动问：本机还有网页控制台，要不要一起启动？
```

## 1）先预览，策略由 Agent 推荐

```text
用户: 帮我启动机器人，先预览配置；策略你推荐一个就行
Agent: 问交易所 → list_strategies → 推荐趋势 → preview_bot_config
Agent: 汇报预览，明确尚未 start_bot，等确认。
```

## 2）查询运行模式

```text
用户: 现在是模拟盘还是实盘？
Agent: 调用 get_runtime_mode
Agent: 回答 testnet / live / not_configured；不要猜。
```

## 3）解释参数

```text
用户: 杠杆和仓位比例是什么意思？
Agent: 调用 explain_parameters
Agent: 用自然语言解释影响与风险，不承诺收益。
```

## 4）状态与成交

```text
用户: 看看现在机器人状态和最近成交。
Agent: 调用 get_bot_status
Agent: 调用 get_recent_trades
```

## 5）OKX Passphrase

```text
用户: OKX 的 Passphrase 怎么填？
Agent: 解释这是创建 API Key 时设置的 API 密码短语，不是登录密码。
Agent: 引导本地保存，不回显密钥。
```

## 6）从测试网切到实盘

```text
用户: 我想从模拟盘切到实盘。
Agent: 调用 get_runtime_mode
Agent: 先停止 → 保存实盘凭证 → preview → 用户确认后 start（需实盘双重确认）
```

## 7）停止——平仓前必须先问

```text
用户: 停止机器人。
Agent: 调用 get_bot_status
Agent: （有仓）问：只停止策略保留仓位，还是同时平掉机器人仓位？
用户: 先只停，仓位留着。
Agent: 调用 stop_bot，参数 close_all=false 且 confirm_stop_keep_positions=true
```

```text
用户: 停止机器人并平掉机器人仓位。
Agent: 说明 close_all 只平机器人管理的仓，不平启动前已有仓
用户: 确认。
Agent: 调用 stop_bot，参数 close_all=true 且 confirm_close_all=true
```
