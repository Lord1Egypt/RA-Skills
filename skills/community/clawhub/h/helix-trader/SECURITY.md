# Agent 安全规则

1. **绝不公开密钥**  
   不要把 API Key、Secret、Passphrase、JWT、`.env` 内容、账户截图或 IP 白名单细节发到聊天、Issue、公开列表或公开帖子。

2. **只报告有无，不回显值**  
   环境检查可以说某变量「已配置 / 缺失」，绝不要打印具体值。

3. **优先本地私密输入**  
   凭证优先来自本机 `.env`、环境变量，或交互式 CLI（`--prompt`）。若用户在可信私有会话中明确提供密钥，调用 `save_exchange_credentials`，且不要回显。

4. **默认测试网**  
   默认 `use_testnet=true`。实盘需要同时满足：
   - 本机 `HELIX_ALLOW_LIVE_TRADING=true`
   - 工具参数 `confirm_live_trading=true`
   - 用户明确确认

5. **破坏性操作必须确认**  
   「停止机器人 / 关掉策略」本身只表示停策略（`close_all=false`）。  
   若有仓位且用户未选择是否平仓，必须先问。  
   平仓：`close_all=true` + `confirm_close_all=true`。  
   有仓且只停策略：`close_all=false` + `confirm_stop_keep_positions=true`。

6. **禁止收益承诺话术**  
   只解释风险与行为，不说稳赚、高胜率、保证回本。

7. **不确定时停下说明**  
   出现凭证、权限或交易所错误时，先停下，用人话说明本机下一步。
