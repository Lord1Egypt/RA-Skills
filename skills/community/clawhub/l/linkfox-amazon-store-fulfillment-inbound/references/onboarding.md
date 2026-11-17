# 认证、授权和算力引导

## 业务前置条件

- 已安装并完成 `linkfox-amazon-store-auth` 的店铺授权。
- 调用时使用已授权店铺的 `sellerId` 和 `region`；不传入 raw access token。
- Amazon 应用和卖家授权包含 `Amazon Fulfillment` role。
- 创建入库计划前，MSKU 已在目标 marketplace 创建且符合 FBA 入库条件。涉及创建/检查 listing 时还需 Product Listing 权限。

## LinkFox auth 场景

以下任一情况视为 auth 场景：

- `errcode=401`；
- 消息包含 `authorized error`、`鉴权失败`、`未授权` 或 `unauthorized`；
- `LINKFOX_AGENT_API_KEY` 与 `LINKFOXAGENT_API_KEY` 均为空。

处理顺序：

1. 已配置 key：先让用户重启会话；仍失败时重新获取 key，或换手机号重新注册。
2. 未配置：可访问 <https://agent.linkfox.com/> 自助获取 key，或使用手机号流程。
3. 手机号流程：
   - `python scripts/onboarding.py send-code <phone>`
   - 获取验证码后运行 `python scripts/onboarding.py login <phone> <code>`
4. 配置返回的 `api_key`并重启会话：
   - Windows PowerShell：`setx LINKFOX_AGENT_API_KEY "<key>"`
   - macOS zsh：`echo 'export LINKFOX_AGENT_API_KEY="<key>"' >> ~/.zshrc && source ~/.zshrc`
   - Linux bash：`echo 'export LINKFOX_AGENT_API_KEY="<key>"' >> ~/.bashrc && source ~/.bashrc`

## LinkFox billing 场景

`errcode=402` 或消息包含 `算力`、`余额`、`quota`、`insufficient`、`充值`、`套餐到期` 时：

1. `python scripts/onboarding.py list-plans`
2. 校验 `plan_id` 属于返回清单，支付方式属于该套餐 `available_methods`。
3. `python scripts/onboarding.py order <plan_id> <method>`
4. 展示优先级：PNG 二维码 > `pay_url` > `ascii_qr`。
5. 用户确认付款后可调用 `python scripts/onboarding.py query <order_id>`；不主动轮询。

`errcode=403` 通常是 Amazon role、marketplace 或资源权限问题，不归入 LinkFox auth/billing 引导。完整用法见 `python scripts/onboarding.py --help`。
