# Session Keys — ERC-4337 Delegated Access

> 源自 OpenClaw/Bagman，适配 Green Vault 安全模块。

## 概述

对于需要链上操作的 AI Agent，使用 ERC-4337 会话密钥代替原始私钥。会话密钥具有时间限制、金额限制和操作白名单。

---

## 1. 会话密钥设计原则

| 属性 | 说明 |
|------|------|
| 时间限制 | 密钥在 N 小时后自动失效 |
| 金额限制 | 每笔/每日交易上限 |
| 操作白名单 | 仅允许调用指定合约的指定方法 |
| 可撤销 | 操作员可随时撤销 |

## 2. ZeroDev SDK 示例

```typescript
import { createKernelAccount, createZeroDevPaymasterClient } from "@zerodev/sdk"
import { signerToSessionKeyValidator } from "@zerodev/session-key"

// 创建有限权限的会话密钥
const sessionKeyValidator = await signerToSessionKeyValidator(publicClient, {
  signer: sessionKeySigner,
  validatorData: {
    permissions: [
      {
        target: USDC_ADDRESS,           // 仅允许 USDC 合约
        functionName: "transfer",        // 仅允许 transfer 方法
        valueLimit: BigInt(0),
        args: [
          { operator: ParamOperator.EQUAL, value: ALLOWED_RECIPIENT },
          { operator: ParamOperator.LESS_THAN_OR_EQUAL, value: parseUnits("100", 6) }
        ]
      }
    ],
    validAfter: Math.floor(Date.now() / 1000),
    validUntil: Math.floor(Date.now() / 1000) + 3600 * 24, // 24 小时有效
  }
})
```

## 3. 会话密钥生命周期

```
Operator 签发 → Agent 使用 → 定时过期 → Operator 轮换
                    ↓
              异常检测 → 立即撤销
```

### 签发

```bash
# 操作员通过 1Password 存储新会话密钥
op item create --vault "Agent-Wallets" \
  --category "API Credential" \
  --title "agent-session-$(date +%Y%m%d)" \
  --field "session-key[password]=0x..." \
  --field "expires=$(date -d '+24 hours' --iso-8601=seconds)" \
  --field "spending-cap=500 USDC" \
  --field "allowed-contracts=0xUSDC,0xDEX"
```

### 撤销

```bash
# 紧急撤销
op item delete "agent-session-compromised" --vault "Agent-Wallets"
# 链上撤销（通过主钱包）
# cast send $KERNEL_ACCOUNT "disableValidator(address)" $SESSION_KEY_VALIDATOR
```

## 4. 不同场景的权限模板

| Agent 类型 | 允许操作 | 限额 | 有效期 |
|-----------|---------|------|--------|
| Trading Bot | swap, transfer USDC | 1000 USDC/日 | 24h |
| Payment Agent | transfer 指定 token | 100 USDC/笔 | 8h |
| DeFi Monitor | 只读（view functions） | 0 | 7d |
| NFT Agent | mint, transfer NFT | 0.1 ETH/笔 | 12h |
