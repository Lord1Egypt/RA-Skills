# Polymarket CLI 故障排查

## 1) `command not found: polymarket`

- 确认安装：`brew install polymarket` 或 `curl -sSL ... | sh`
- 确认 PATH：`which polymarket`

## 2) 钱包相关失败 / 无法签名

- 检查配置：`polymarket wallet show`
- 检查私钥来源优先级：
  1. `--private-key`
  2. `POLYMARKET_PRIVATE_KEY`
  3. `~/.config/polymarket/config.json`

## 3) 下单失败（认证/余额/授权）

依次检查：

```bash
polymarket clob account-status
polymarket clob balance --asset-type collateral
polymarket clob update-balance               # 刷新链上余额授权
polymarket approve check
```

若未授权，执行 `polymarket approve set`（会产生链上交易，需要 MATIC gas）。

## 4) 网络或 API 异常

```bash
polymarket status
polymarket clob ok
```

若 API 短时故障：重试只读命令；写操作必须等状态恢复后再继续。

## 5) JSON 脚本解析失败

- 强制 JSON 输出：`-o json`
- 检查 stderr 与退出码，不要只解析 stdout。

## 6) 风控建议

- 先小额验证再放量。
- 写操作执行前再次回显参数（token、side、price/amount、size）。
- 完成后立即 `clob orders` / `clob trades` 回读校验。

## 7) 签名类型不匹配

症状：交易签名失败、返回 invalid signature 或 unauthorized 错误。

排查：
- `polymarket wallet show` 查看当前钱包类型
- 如果使用 proxy 钱包，需要加 `--signature-type proxy`
- 如果使用 Gnosis Safe 多签，需要加 `--signature-type gnosis-safe`
- 默认为 `eoa`（Externally Owned Account）

```bash
# 示例：proxy 钱包下单
polymarket --signature-type proxy clob create-order --token <TOKEN_ID> --side buy --price 0.50 --size 10
```

## 8) Bridge 充值问题

排查步骤：

```bash
polymarket bridge supported-assets         # 确认支持的链和代币
polymarket bridge deposit                  # 获取充值地址
polymarket bridge status <ADDRESS>         # 查询充值状态
```

常见问题：
- 充值未到账：用 `bridge status` 检查交易确认数
- 不支持的资产：先用 `supported-assets` 确认
- 地址错误：每次充值前重新获取地址确认
