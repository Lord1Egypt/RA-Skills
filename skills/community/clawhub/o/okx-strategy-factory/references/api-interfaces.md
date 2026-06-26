# onchainos CLI 接口参考

策略代码通过 `subprocess` 调用 `onchainos` CLI 与链上交互。**这是唯一的执行方式**，不存在 SDK 或 Python 包。

## 运行时

| 环境 | 路径 | 架构 |
|------|------|------|
| 本地 Mac | `Agentic Wallet/onchainos` | arm64 |
| VPS | `/usr/local/bin/onchainos` | amd64 |

认证通过环境变量：`OKX_API_KEY` / `OKX_SECRET_KEY` / `OKX_PASSPHRASE`（从 1Password 获取）。

## 标准 Wrapper

所有策略必须使用统一的 CLI wrapper 模式（参考 `grid-trading/references/eth_grid_v1.py`）：

```python
import subprocess, json, os

def onchainos_cmd(args: list[str], timeout: int = 30) -> dict | None:
    """Run onchainos CLI command, return parsed JSON."""
    env = os.environ.copy()
    env.setdefault("OKX_API_KEY", os.environ.get("OKX_API_KEY", ""))
    env.setdefault("OKX_SECRET_KEY", os.environ.get("OKX_SECRET_KEY", ""))
    env.setdefault("OKX_PASSPHRASE", os.environ.get("OKX_PASSPHRASE", ""))
    try:
        result = subprocess.run(
            ["onchainos"] + args,
            capture_output=True, text=True, timeout=timeout, env=env,
        )
        output = result.stdout.strip() if result.stdout else ""
        if output:
            try:
                data = json.loads(output)
                if isinstance(data, dict) and "ok" in data:
                    return data
                return {"ok": True, "data": data if isinstance(data, list) else [data]}
            except json.JSONDecodeError:
                pass
        if result.returncode != 0:
            stderr = result.stderr.strip() if result.stderr else ""
            log(f"onchainos rc={result.returncode}: {' '.join(args[:3])} "
                f"{'stderr=' + stderr[:150] if stderr else 'no output'}")
    except subprocess.TimeoutExpired:
        log(f"onchainos timeout: {' '.join(args[:3])}")
    except Exception as e:
        log(f"onchainos error: {e}")
    return None
```

## 命令速查

### Wallet（钱包操作）

```bash
# 登录 & 状态
onchainos wallet login <email> --locale zh-CN
onchainos wallet verify <otp>
onchainos wallet status
onchainos wallet addresses                       # 所有地址，按链分组
onchainos wallet addresses --chain <chainId>     # 指定链

# 余额（⚠️ 返回 UI 单位）
onchainos wallet balance                         # 所有链概览
onchainos wallet balance --chain <chainId>       # 指定链
onchainos wallet balance --chain <chainId> --token-address <addr>  # 指定 token

# 转账（⚠️ amount 用 UI 单位："0.1" = 0.1 ETH）
onchainos wallet send --amount <amt> --receipt <addr> --chain <chainId>
onchainos wallet send --amount <amt> --receipt <addr> --chain <chainId> --contract-token <tokenAddr>  # ERC-20

# 合约调用（TEE 签名）
onchainos wallet contract-call --to <addr> --chain <chainId> --input-data <hex>
onchainos wallet contract-call --to <addr> --chain <chainId> --input-data <hex> --value <amount>  # payable
onchainos wallet contract-call --to <addr> --chain <chainId> --input-data <hex> --mev-protection  # 防 MEV

# 交易历史
onchainos wallet history
onchainos wallet history --tx-hash <hash> --chain <chainId> --address <addr>
```

### Swap（DEX 聚合交易）

```bash
# 询价（⚠️ amount 用最小单位 wei/lamports）
onchainos swap quote --from <tokenAddr> --to <tokenAddr> --amount <minimalUnits> --chain <chainId>

# 授权（EVM 需要，Solana 不需要）
onchainos swap approve --token <tokenAddr> --amount <minimalUnits> --chain <chainId>

# 执行 swap（返回 tx calldata，需要通过 wallet contract-call 签名广播）
onchainos swap swap --from <tokenAddr> --to <tokenAddr> --amount <minimalUnits> --chain <chainId> --wallet <walletAddr>

# 支持的链 & 流动性源
onchainos swap chains
onchainos swap liquidity --chain <chainId>
```

**原生代币地址**:
- EVM: `0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee`
- Solana: `11111111111111111111111111111111`

### Market（行情数据）

```bash
# 价格
onchainos market price --address <tokenAddr> --chain <chainId>
onchainos market prices --tokens "<chainId>:<addr>,<chainId>:<addr>"  # 批量

# K线（⚠️ Solana 用 wSOL SPL 地址）
onchainos market kline --address <tokenAddr> --chain <chainId> --bar <1m|5m|15m|1H|4H|1D> --limit <count>

# 指数价格（聚合多源）
onchainos market index --address <tokenAddr> --chain <chainId>
```

### Gateway（交易基础设施）

```bash
# Gas
onchainos gateway gas --chain <chainId>                                    # 当前 gas price
onchainos gateway gas-limit --from <addr> --to <addr> --chain <chainId>    # 估算 gas limit
onchainos gateway gas-limit --from <addr> --to <addr> --data <calldata> --chain <chainId>

# 模拟（不上链，验证交易可行性）
onchainos gateway simulate --from <addr> --to <contract> --data <calldata> --chain <chainId>

# 广播（需要已签名的 tx）
onchainos gateway broadcast --signed-tx <hex> --address <addr> --chain <chainId>

# 订单追踪
onchainos gateway orders --address <addr> --chain <chainId>
onchainos gateway orders --address <addr> --chain <chainId> --order-id <id>
```

### Security（安全扫描）

```bash
# Token 风险检测（蜜罐、rug pull）
onchainos security token-scan --tokens "<chainId>:<addr>,<chainId>:<addr>"

# DApp/URL 钓鱼检测
onchainos security dapp-scan --domain <domain>

# 交易预执行安全检查
onchainos security tx-scan --chain <chainId> --from <addr> --to <contract> --data <calldata>

# 授权查询
onchainos security approvals --address <addr> --chain <chainId>
```

### Token（代币数据）

```bash
# 搜索 & 信息
onchainos token search --query <term> --chains "<chainId1>,<chainId2>"
onchainos token info --address <addr> --chain <chainId>
onchainos token price-info --address <addr> --chain <chainId>      # 价格 + 市值 + 流动性

# 持有者分析
onchainos token holders --address <addr> --chain <chainId>
onchainos token holders --address <addr> --chain <chainId> --tag-filter <whale|kol|smart_money|sniper>

# 流动性池
onchainos token liquidity --address <addr> --chain <chainId>

# 高级风险信息（创建者、持仓集中度）
onchainos token advanced-info --address <addr> --chain <chainId>
```

### Portfolio（公开地址查询）

```bash
onchainos portfolio total-value --address <addr> --chains "<chainId1>,<chainId2>"
onchainos portfolio all-balances --address <addr> --chains "<chainIds>"
onchainos portfolio token-balances --address <addr> --tokens "<chainId>:<addr>,<chainId>:<addr>"  # 最多 20 个
```

## ⚠️ 关键陷阱

| 陷阱 | 说明 | 正确做法 |
|------|------|----------|
| **单位混用** | `wallet send` 用 UI 单位，`swap` 用最小单位 (wei) | 每个命令查本表确认单位 |
| **EVM approve** | EVM swap 前必须 approve，Solana 不需要 | 根据链判断是否 approve |
| **合约地址大小写** | onchainos 要求小写 | `.lower()` 处理 |
| **K线 Solana** | `market kline` 用 wSOL SPL 地址，不是原生地址 | 区分原生 vs SPL 地址 |
| **Gas 估算不可靠** | DEX API 返回的 gas 值不准 | 让 onchainos 内部估算，不要手动传 gas |
| **签名方式** | 用 `wallet contract-call` 签名，不是 gateway broadcast | 策略代码不直接签名 |

## 策略代码的标准执行流程

以 swap 为例（参考 grid-trading 实盘代码）：

```
1. onchainos swap quote      → 获取报价 + priceImpact
2. 检查 priceImpact < tolerance  → 超出则放弃
3. onchainos swap approve    → EVM 授权（Solana 跳过）
4. onchainos swap swap       → 获取 tx calldata
5. onchainos gateway simulate → 预检交易（大额操作建议做）
6. onchainos wallet contract-call → TEE 签名 + 广播
7. 验证返回 txHash           → 记录到 state.json
```

**完整示例见 `grid-trading/references/eth_grid_v1.py`** — 这是经过实盘验证的代码，新策略应复用其 wrapper 和执行模式。
