# Polymarket CLI 命令速查 (v0.1.5)

## 0) 全局选项

```bash
polymarket --help
polymarket --version
polymarket -o json <subcommand>        # JSON 输出
polymarket --private-key <KEY> <cmd>   # 覆盖环境变量/配置文件私钥
polymarket --signature-type <TYPE> <cmd>  # eoa | proxy | gnosis-safe
```

## 1) 市场与事件（只读）

```bash
polymarket markets list --limit 10
polymarket markets search "election"
polymarket markets get <slug-or-id>
polymarket markets tags <market_id>

polymarket events list --tag politics --active true
polymarket events get <event_id>
```

## 2) CLOB 只读查询

```bash
# 健康检查
polymarket clob ok
polymarket clob time                     # 服务器时间
polymarket clob geoblock                 # 地理封锁检查

# 单 token 查询
polymarket clob price <TOKEN_ID> --side buy
polymarket clob midpoint <TOKEN_ID>
polymarket clob spread <TOKEN_ID>
polymarket clob book <TOKEN_ID>
polymarket clob last-trade <TOKEN_ID>
polymarket clob tick-size <TOKEN_ID>
polymarket clob fee-rate <TOKEN_ID>
polymarket clob neg-risk <TOKEN_ID>
polymarket clob price-history <TOKEN_ID> --interval 1d --fidelity 30

# 批量查询（逗号分隔多个 token ID）
polymarket clob batch-prices <TOKEN_IDS>
polymarket clob midpoints <TOKEN_IDS>
polymarket clob spreads <TOKEN_IDS>
polymarket clob books <TOKEN_IDS>
polymarket clob last-trades <TOKEN_IDS>

# 市场列表
polymarket clob market <CONDITION_ID>        # 按 condition ID 查单个市场
polymarket clob markets                      # 列出 CLOB 市场
polymarket clob sampling-markets             # 奖励资格市场
polymarket clob simplified-markets           # 精简详情
polymarket clob sampling-simp-markets        # 精简奖励资格市场
```

## 3) 钱包与授权（有写操作）

```bash
polymarket wallet create
polymarket wallet import <private_key>
polymarket wallet show
polymarket wallet address                # 仅显示地址
polymarket wallet reset                  # 删除所有配置和密钥（慎用）

polymarket approve check
polymarket approve set
```

## 4) 下单撤单（写操作）

```bash
# 创建订单
polymarket clob create-order --token <TOKEN_ID> --side buy --price 0.50 --size 10
polymarket clob create-order --token <TOKEN_ID> --side buy --price 0.50 --size 10 --order-type FOK
polymarket clob create-order --token <TOKEN_ID> --side sell --price 0.60 --size 5 --post-only

# Order types: GTC (默认), FOK (全部成交或取消), GTD (指定过期时间), FAK (尽量成交剩余取消)
# --post-only: 仅挂单，不吃单

# 市价单
polymarket clob market-order --token <TOKEN_ID> --side buy --amount 5

# 批量下单
polymarket clob post-orders <JSON_FILE>

# 撤单
polymarket clob cancel <ORDER_ID>
polymarket clob cancel-orders <ORDER_ID1>,<ORDER_ID2>
polymarket clob cancel-market <CONDITION_ID>   # 撤销某市场全部订单
polymarket clob cancel-all

# 查询
polymarket clob orders                         # 所有挂单
polymarket clob order <ORDER_ID>               # 单个订单详情
polymarket clob trades                         # 成交记录
polymarket clob balance --asset-type collateral
polymarket clob update-balance                 # 刷新链上余额授权
polymarket clob account-status                 # 账户状态
```

## 5) 链上数据（只读）

```bash
polymarket data positions <WALLET_ADDRESS>
polymarket data closed-positions <WALLET_ADDRESS>
polymarket data value <WALLET_ADDRESS>
polymarket data activity <WALLET_ADDRESS>
polymarket data traded <WALLET_ADDRESS>          # 参与过的市场数
polymarket data trades <WALLET_ADDRESS> --limit 50
polymarket data holders <MARKET_ID>              # token 持有人排行
polymarket data open-interest <MARKET_ID>
polymarket data volume <EVENT_ID>                # 事件实时交易量
polymarket data leaderboard --period month --order-by pnl --limit 10
polymarket data builder-leaderboard
polymarket data builder-volume
```

## 6) CTF（写操作）

```bash
polymarket ctf split --condition <CONDITION_ID> --amount 10
polymarket ctf split --condition <CONDITION_ID> --amount 10 --collateral <ADDRESS> --partition "1,2" --parent-collection <COLLECTION_ID>
polymarket ctf merge --condition <CONDITION_ID> --amount 10
polymarket ctf redeem --condition <CONDITION_ID>
polymarket ctf redeem-neg-risk --condition <CONDITION_ID>

# 辅助计算
polymarket ctf condition-id --oracle <ADDR> --question <ID> --outcomes <COUNT>
polymarket ctf collection-id --condition <CONDITION_ID> --index-set <SET>
polymarket ctf position-id --collateral <ADDR> --collection <COLLECTION_ID>
```

## 7) 奖励与 API 密钥（认证）

```bash
# 奖励查询
polymarket clob rewards
polymarket clob earnings --date 2026-03-15
polymarket clob earnings-markets
polymarket clob reward-percentages
polymarket clob current-rewards
polymarket clob market-reward <CONDITION_ID>
polymarket clob order-scoring <ORDER_ID>
polymarket clob orders-scoring <ORDER_ID1>,<ORDER_ID2>

# API 密钥管理
polymarket clob api-keys
polymarket clob create-api-key
polymarket clob delete-api-key

# 通知
polymarket clob notifications
polymarket clob delete-notifications <ID1>,<ID2>
```

## 8) Bridge

```bash
polymarket bridge deposit                      # 获取充值地址（EVM/Solana/Bitcoin）
polymarket bridge supported-assets             # 支持的链和代币
polymarket bridge status <ADDRESS>             # 查询充值交易状态
```

## 9) 元数据（只读）

```bash
# Tags
polymarket tags list
polymarket tags get <TAG_ID_OR_SLUG>
polymarket tags related <TAG_ID>
polymarket tags related-tags <TAG_ID>

# Series
polymarket series list
polymarket series get <SERIES_ID>

# Comments
polymarket comments list --event <EVENT_ID>
polymarket comments get <COMMENT_ID>
polymarket comments by-user <WALLET_ADDRESS>

# Profiles
polymarket profiles get <WALLET_ADDRESS>

# Sports
polymarket sports list
polymarket sports market-types
polymarket sports teams
```

## 10) 工具命令

```bash
polymarket status       # API 健康检查
polymarket setup        # 引导式首次设置（钱包、代理、授权）
polymarket upgrade      # 更新到最新版本
polymarket shell        # 启动交互式 shell
```
