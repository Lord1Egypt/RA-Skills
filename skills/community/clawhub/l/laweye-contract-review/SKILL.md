---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_9fb6b6bf616311f1832e5254006c9bbf
    ReservedCode1: +pmMfZyL7yrADTh++CmFzj8+k1a4+LvbwUJj5i+YyJwnZ1hc8MQFvLv/Np5DBB8V6cr17pGi67FI/zYG6Rdx7mTiPpx29o2Nr631lrywvu8R57EyjXrD2PlsP7Zr4mxlLcrRI6zToqoAE1fvqEkhDDHnMzUMIWjLpRYvRm755S/+Y60RpfiXV0wuFKg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_9fb6b6bf616311f1832e5254006c9bbf
    ReservedCode2: +pmMfZyL7yrADTh++CmFzj8+k1a4+LvbwUJj5i+YyJwnZ1hc8MQFvLv/Np5DBB8V6cr17pGi67FI/zYG6Rdx7mTiPpx29o2Nr631lrywvu8R57EyjXrD2PlsP7Zr4mxlLcrRI6zToqoAE1fvqEkhDDHnMzUMIWjLpRYvRm755S/+Y60RpfiXV0wuFKg=
---

# 法眼·AI合同审查

## 概述

法眼（LawEye）是一款 AI 驱动的智能合同审查技能，基于规则引擎 + 模式匹配 + 法规知识库，自动检测合同中的风险条款、模糊表述、法律陷阱，并给出修改建议和法条引用。支持全球多法域审查。

## 适用场景

- 合同签署前的快速风险扫描
- 合同条款合规性审查
- 多版本合同对比分析
- 合同谈判中的条款攻防建议

## 审查维度

| 维度 | 说明 |
|------|------|
| 合规性 | 条款是否符合相关法律法规（民法典、UCC、CISG、GDPR 等） |
| 风险等级 | 高/中/低 三级风险标记，含量化统计 |
| 模糊条款 | 识别表述不清、留有解释空间的条款 |
| 违约责任 | 违约金比例、责任对等性、赔偿上限 |
| 争议解决 | 管辖法院、仲裁条款、适用法律的明确性 |
| 知识产权 | IP 归属、使用许可范围、保密义务 |
| 数据与隐私 | 数据收集、处理、跨境传输合规性 |

## 支持的法域

- **中国大陆**：民法典、合同法、电子签名法、个人信息保护法
- **美国**：UCC（统一商法典）、各州合同法、CFAA
- **英国**：UK Consumer Rights Act、Unfair Contract Terms Act
- **欧盟**：GDPR、CESL（共同欧洲买卖法）、数字服务法
- **日本**：民法（債権法改正）、消费者契约法
- **新加坡**：Sale of Goods Act、Electronic Transactions Act
- **阿联酋**：UAE Civil Code、DIFC Contract Law

## 支付协议（AI收）

本技能采用支付宝 AI 收 HTTP 402 协议，按次计费。

| 项目 | 值 |
|------|-----|
| 单价 | ¥0.50 / 次 |
| 支付协议 | `alipay_` 短链协议 |
| 网关地址 | `http://8.145.54.67:3000` |
| 技能路径 | `/skill/contract-review` |
| 支付确认路径 | `/pay-confirm` |

### 支付流程

```
1. 客户端发起审查请求  POST /skill/contract-review
2. 服务端返回 402 Payment Required
   Header: X-Payment-Needed: true
   Header: X-Short-Link: alipay_XXXXXXXXXXXXXXXX
3. 用户完成支付宝支付
4. 客户端携带支付凭证回传  POST /pay-confirm
   Header: X-Payment-Credential: <支付凭证>
5. 服务端验证通过 → 执行合同审查 → 返回结果
```

### HTTP 请求头规范

| 头名称 | 说明 |
|--------|------|
| `X-Payment-Needed` | 服务端返回：`true` 表示需要支付 |
| `X-Short-Link` | 服务端返回：支付宝短链 URL 供用户支付 |
| `X-Payment-Credential` | 客户端回传：支付完成后的凭证字符串 |
| `X-Service-Tier` | 可选，`basic`（快速扫描）或 `pro`（深度审查） |

## 审查服务档位

### 基础档（basic = ¥0.50）
- 合同正文风险扫描（最多 20 页）
- 风险条款标记与统计
- 简要修改建议
- 输出 JSON 格式审查报告

### 专业档（pro = ¥1.00 - 预留）
- 全部基础功能
- 逐条法条引用（民法典、UCC、CISG 等）
- 修改建议含具体措辞模板
- 文本对比（修改前后 diff）
- 输出 PDF 审查报告

## 数据底座

所有法规数据、合同模板、陷阱模式、审查规则存储于 `references/contract-review.json`，结构如下：

```json
{
  "legal_frameworks": { ... },   // 全球法域法规要点
  "contract_templates": { ... },  // 合同类型模板
  "trap_patterns": [ ... ],       // 陷阱条款识别规则
  "legal_references": [ ... ],    // 法规引用库
  "review_dimensions": [ ... ]    // 审查维度定义
}
```

## 使用示例

### 请求

```bash
curl -X POST http://8.145.54.67:3000/skill/contract-review \
  -H "Content-Type: application/json" \
  -H "X-Service-Tier: basic" \
  -d '{"contract_text": "第一条 委托事项...", "jurisdiction": "CN"}'
```

### 响应（支付后）

```json
{
  "service": "法眼·AI合同审查",
  "tier": "basic",
  "risks_found": 5,
  "risk_stats": {"高": 2, "中": 2, "低": 1},
  "jurisdiction": "CN",
  "summary": "检测到 5 处风险条款...",
  "details": [
    {
      "clause": "第二条 违约责任",
      "rule": "违约责任不对等",
      "risk": "高",
      "issue": "违约责任条款存在不对等",
      "suggestion": "建议将违约金比例调整为双方对等",
      "legal_ref": "民法典第585条"
    }
  ]
}
```

## 部署文件

技能包包含以下文件：

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 本文件，技能定义与接口规范 |
| `references/contract-review.json` | 数据底座（法条、模板、陷阱规则） |
| `contract_reviewer.py` | 合同审查引擎（部署时使用） |
| `laweye_server.py` | HTTP 服务端（部署时使用） |
| `deploy.sh` | 一键部署脚本（Ubuntu/Debian） |

## 许可

MIT License — 详见 LICENSE 文件
*（内容由AI生成，仅供参考）*
