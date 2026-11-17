# 工具对照表

| MCP 工具 | CLI | 风险等级 | 说明 |
|----------|-----|----------|------|
| `health_check` | `health` | 只读 | 后端 `/health` |
| `doctor` | `doctor` | 只读 | 环境检查，不回显密钥 |
| `login` | `login` | 凭证 | 优先用环境变量；只返回脱敏 token；缓存到 `backend/.helix-agent-token` |
| `logout` | `logout` | 只读 | 清除本地 token 缓存与进程内 `HELIX_ACCESS_TOKEN` |
| `list_strategies` | `strategies` | 只读 | 含参数说明 |
| `list_markets` | `markets --exchange ...` | 只读 | 需已登录 |
| `explain_parameters` | `params` | 只读 | 参数词典 |
| `get_runtime_mode` | `mode` | 只读 | 来源：`/api/bot/status.use_testnet` |
| `get_bot_status` | `status` | 只读 | 状态 / 余额 / 仓位 |
| `get_recent_trades` | `trades` | 只读 | 最近成交 |
| `preview_bot_config` | `preview ...` | 只读 | 预览，不下单 |
| `save_exchange_credentials` | `save-credentials ...` | 凭证 | 需要 `confirm_save_credentials` |
| `start_bot` | `start ...` | 交易 | 默认测试网；实盘需双重确认 |
| `update_bot_config` | `update-config ...` | 交易 | 实盘模式需双重确认 |
| `stop_bot` | `stop ...` | 破坏性 | 默认保留仓位；平仓前先问；`close_all` 需 `confirm_close_all` |

## 通用调用示例

```bash
cd backend
python -m app.agent call doctor --args '{}'
python -m app.agent mode
python -m app.agent call list_markets --args '{"exchange":"okx"}'
```
