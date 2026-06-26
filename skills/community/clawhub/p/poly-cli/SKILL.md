---
name: polymarket-cli
description: "Operate Polymarket from terminal with the `polymarket` Rust CLI (v0.1.5). Covers market/event/tag/series discovery, CLOB order book queries (single & batch), wallet & approval management, order placement/cancelation (GTC/FOK/GTD/FAK), portfolio & on-chain data, CTF operations, rewards/earnings, bridge deposits, sports metadata, API key management, and JSON output for automation."
---

# Polymarket CLI

使用本技能时，按用户目标直接执行对应命令；默认先收集必要参数并返回可复现结果。

## 快速决策

1. 先判断请求类型：
   - **只读**：市场浏览、价格、盘口、持仓查询、历史数据、tags/series/comments、sports、rewards 查询。
   - **写操作**：下单、撤单、approve、split/merge/redeem、API key 管理、bridge deposit、wallet reset。
2. 只读请求可直接执行。
3. 写操作先做预检（余额/参数/网络），然后执行并回读结果。

## 环境检查与安装

按顺序执行：

```bash
polymarket --version
```

若未安装，优先一键脚本：

```bash
curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
```

或 Homebrew：

```bash
brew tap Polymarket/polymarket-cli https://github.com/Polymarket/polymarket-cli
brew install polymarket
```

无法使用以上方式时，回退源码安装：

```bash
git clone https://github.com/Polymarket/polymarket-cli
cd polymarket-cli
cargo install --path .
```

## 标准执行流程

### 1) 读取需求并标准化参数

最少明确：
- 市场标识（slug / market id / condition id / token id）
- 方向与数量（buy/sell, amount/size）
- 价格类型（limit/market）
- 输出格式（table/json）

如要脚本集成，统一使用：`-o json`。

### 2) 只读查询模式（默认）

常用命令：

```bash
polymarket markets search "bitcoin" --limit 5
polymarket markets get <slug-or-id>
polymarket clob book <TOKEN_ID>
polymarket clob midpoint <TOKEN_ID>
polymarket clob spread <TOKEN_ID>
polymarket -o json clob price-history <TOKEN_ID> --interval 1d

# 批量查询
polymarket clob batch-prices <TOKEN_ID1>,<TOKEN_ID2>
polymarket clob books <TOKEN_ID1>,<TOKEN_ID2>

# 元数据
polymarket tags list
polymarket series list
polymarket comments list --event <EVENT_ID>
```

### 3) 交易前预检

全局选项（所有子命令均可用）：
- `--private-key <KEY>` — 覆盖环境变量/配置文件中的私钥
- `--signature-type <TYPE>` — 签名类型：`eoa`（默认）、`proxy`、`gnosis-safe`

执行：

```bash
polymarket wallet show
polymarket approve check
polymarket clob balance --asset-type collateral
polymarket clob account-status
```

核对点：
- 钱包地址是否符合预期
- 是否完成 approvals
- 是否有足够 USDC / MATIC（链上写操作 gas）
- 签名类型是否匹配（proxy 钱包需要 `--signature-type proxy`）

### 4) 写操作执行

示例：

```bash
# 限价单
polymarket clob create-order --token <TOKEN_ID> --side buy --price 0.50 --size 10
# 指定 order type
polymarket clob create-order --token <TOKEN_ID> --side buy --price 0.50 --size 10 --order-type FOK
# 仅挂单
polymarket clob create-order --token <TOKEN_ID> --side sell --price 0.60 --size 5 --post-only

# 市价单
polymarket clob market-order --token <TOKEN_ID> --side buy --amount 5

# 批量下单
polymarket clob post-orders <JSON_FILE>

# 撤单
polymarket clob cancel <ORDER_ID>
polymarket clob cancel-orders <ORDER_ID1>,<ORDER_ID2>

# 授权
polymarket approve set

# Bridge 充值
polymarket bridge deposit
```

执行后立即回读验证：

```bash
polymarket clob orders
polymarket clob order <ORDER_ID>
polymarket clob trades
```

## 输出约定

- 给人看：table（默认）
- 给程序：json（`-o json`）
- 失败时：记录命令、stderr、退出码；不要静默吞错。

## 参考资料

- 命令速查：`references/commands.md`
- 故障排查：`references/troubleshooting.md`
