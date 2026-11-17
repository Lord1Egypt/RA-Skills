---
name: polymarket-btc-5m-arbitrage
description: Read-only Polymarket BTC 5-minute market scanner that reports candidate complementary-price edges; it never places orders, moves funds, or charges users.
version: 1.0.2
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "📊"
    homepage: "https://clawhub.ai/whh110112/skills/polymarket-btc-5m-arbitrage"
    envVars: []
    permissions:
      network:
        - "https://gamma-api.polymarket.com"
        - "https://clob.polymarket.com"
      filesystem: "read-only; skill directory only"
      secrets: []
      external_writes: []
      trading: "none"
---

# Polymarket BTC 5分钟市场扫描器

⚠️ **资金与交易警告**

- 这是只读扫描器，不是自动交易机器人。
- 它只调用 Polymarket 的公开市场数据接口；不会下单、撤单、做市、转账或扣费。
- 它不读取或要求私钥、API key、钱包凭据、第三方计费凭据或其他秘密。
- “候选价差”不是无风险收益承诺，仍可能受到手续费、滑点、延迟、部分成交、市场规则和结算争议影响。
- 运行前请确认你遵守所在地区及 Polymarket 的法律、合规和服务条款要求。

## 能力与权限声明

| 能力 | 本版本行为 |
| --- | --- |
| 网络 | 仅向 gamma-api.polymarket.com 和 clob.polymarket.com 发起公开数据 GET 请求 |
| 文件 | 不读取工作区外文件；脚本本身不写文件 |
| 环境变量 | 不需要任何环境变量 |
| 秘密 | 不接收、不打印、不上传私钥或 API key |
| 外部副作用 | 无订单、支付、消息发送或其他写操作 |

metadata.openclaw.permissions 是给安装者和审计器看的能力声明；真正的网络/文件系统隔离仍应由运行时沙箱或主机策略执行。

## 使用方法

单次扫描：

    python3 {baseDir}/scripts/polymarket_btc_5m_bot.py --once

输出 JSON，便于下游审计或人工复核：

    python3 {baseDir}/scripts/polymarket_btc_5m_bot.py --once --json

持续轮询必须显式指定间隔；即便如此仍然只读：

    python3 {baseDir}/scripts/polymarket_btc_5m_bot.py --interval 30

## 判断口径

脚本分别读取 Up/Down 两个互补 token 的最佳卖价，并仅报告：

    Up ask + Down ask + fee_buffer < 1

这只是候选筛选条件，不执行交易，也不保证能以显示价格成交。脚本不会把同一个 token 的 bid/ask 误称为互补套利。

## 明确不支持的功能

本版本不支持自动交易、限价单、市价单、自动做市、第三方计费或任何付款流程。若要另行开发真实交易执行器，应使用独立 skill，加入显式的 dry-run 默认值、单次订单确认、额度上限、密钥托管、审计日志和单独的安全评审；不要把私钥重新加回本 skill。

## 参考

- references/api-reference.md：只读接口范围
- references/trading-strategy.md：候选价差与风险说明
