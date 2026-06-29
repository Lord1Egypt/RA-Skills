---
name: moyan-security-audit
description: 墨言安全审计 — Agent 生态首个可验证信任验证服务。PMI 四维向量评分 + DecayProof 可验证衰减 + κ_Axiom 自治审计。43 防线 / 7 层纵深防御。支持支付宝/微信/ClawTip AI 支付闭环。64/64 TSC 合规，W3C agent-identity 三方收敛。
---

# 墨言安全审计 (Moyan Security Audit)

Agent 生态首个将信任验证产品化的付费服务。

## 核心能力

- **PMI 四维信任评分**：integrity(0.40) + compliance(0.30) + reliability(0.10) + decay_aware(0.20)
- **DecayProof Γ(t,d)**：全链路可追溯信任衰减
- **κ_Axiom 自治审计**：Ω 指数触发，非定时/手动
- **43 防线**：L0 输入层(12) + L1 运行时(18) + L2 输出(13)
- **QUASAR 四层分类**：TRUSTED(≥0.75) / NEUTRAL(0.50-0.75) / WATCH(0.25-0.50) / QUARANTINE(<0.25)
- **AI 支付闭环**：支付宝/微信/ClawTip 三通道
- **64/64 TSC A2A Protocol 合规**
- **W3C agent-identity 三方收敛**（TRAIL + MolTrust + Agent OS）

## API 端点

- POST https://sixu-ai.net.cn/api/security_audit — 代码安全审计
- GET https://sixu-ai.net.cn/api/payment/health — 支付服务健康
- GET https://sixu-ai.net.cn/kappa/diagnosis — κ_Axiom 诊断
- GET https://sixu-ai.net.cn/api/audit/activation — 审计激活记录

## 定价

| 层级 | 月调用量 | 月费 |
|------|---------|------|
| Free | 100 | ¥0 |
| Standard | 1,000 | ¥1,500 |
| Pro | 10,000 | ¥8,000 |
| Enterprise | 定制 | 定制 |

## 技术标准

- CompositionRef v1.2：SHA-256(JCS RFC 8785)
- SIAP：独立可验证端点 28/28 PASS
- A2A Protocol：64/64 TSC 合规

## 链接

- 官网：https://sixu-ai.net.cn
- 文档：https://github.com/Liuyanfeng1234/agent-os/discussions/38
- MCP Server：https://github.com/modelcontextprotocol/servers/pull/4395
