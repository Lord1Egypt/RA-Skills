---
name: "innovation-research"
version: "1.1.1"
description: >
  Technology innovation research: AI-delivered technology stack analysis, patent landscape review, competitive comparison, and emerging technology evaluation. Payment verification via clawtip. No user source code, project files, or credentials are collected or transmitted.
metadata:
  author: "Yujin"
  category: "expert"
  permissions:
    - "credential.read"
    - "filesystem.read"
    - "filesystem.write"
  requires:
    - "clawtip"
  workflow:
    create_order:
      script: scripts/create_order.py
      args: ["{question}"]
      outputs: ["order_no", "amount", "indicator"]
    pay:
      requires: clawtip
      args: ["{order_no}", "{indicator}"]
    service:
      script: scripts/service.py
      args: ["{order_no}"]
---

# innovation-research

请使用中文与用户交互。

## 技能概述

技术调研与创新研究服务。本技能通过 clawtip 完成支付验证后，**由 AI 模型在对话中交付调研结果**，包括技术栈分析、专利地图审查、竞品对比和新兴技术评估。

### 服务交付方式

本技能是 **AI 交付型** 服务：
- `create_order.py` — 创建本地订单文件（用于 clawtip 支付验证）
- 支付由 **clawtip** 官方钱包处理
- `service.py` — 验证支付凭证后，**指示 AI 在对话中**输出调研报告
- 实际的调研分析由 AI 模型在对话上下文中完成，不依赖外部脚本

### 免费使用

本技能为全付费服务。如需免费调研能力，可使用其他通用 AI 工具。

---

## 环境变量配置

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `CLAWTIP_PAY_TO` | 是 | clawtip 商户收款地址 |
| `CLAWTIP_SM4_KEY` | 是 | SM4 加密密钥 |

---

## 前置条件

```bash
openclaw skills install clawtip
```

---

## 🛒 第一阶段：创建订单

```bash
python3 scripts/create_order.py "<question>"
```

> 本地订单文件路径：`~/.openclaw/skills/orders/{indicator}/{order_no}.json`
> 包含字段：orderNo、amount、question。仅用于支付验证，不涉及调研数据。

**成功：** `ORDER_NO=... AMOUNT=... QUESTION=... INDICATOR=...`
**失败：** `订单创建失败: <详情>` → 终止。

---

## 💳 第二阶段：支付处理

### 沙箱测试

```bash
npx --yes @clawtip/clawtip-sandbox-cli@1.0.0 pay -o <ORDER_NO> -i <INDICATOR> -v 1.0.12
```

### 生产环境

调用 **clawtip** 钱包：`{"orderNo": "<ORDER_NO>", "indicator": "<INDICATOR>"}`

---

## 🚀 第三阶段：服务执行

```bash
python3 scripts/service.py "<order_no>"
```

| 字段 | 值 | 说明 |
|------|-----|------|
| PAY_STATUS | SUCCESS / ERROR | 支付验证状态 |
| AUTHORIZATION_RESULT | verified | 授权通过，AI 开始交付调研 |

成功后，AI 模型将在对话中输出：
1. **技术栈分析** — 框架对比、架构评估、技术选型建议
2. **专利地图审查** — 相关专利分布、创新热点、空白区域
3. **竞品对比** — 功能对比、市场份额、差异化分析
4. **新兴技术评估** — 成熟度、适用场景、发展趋势

---

## 数据处理说明

### 本地存储
| 文件 | 路径 | 内容 |
|------|------|------|
| 订单文件 | `~/.openclaw/skills/orders/{indicator}/{order_no}.json` | orderNo、amount、question、加密支付凭证 |

订单文件仅存在用户本地文件系统，用于 clawtip 支付验证。不包含任何技术调研数据、专利信息或项目文件。

### 远程传输
本技能自身不发起任何远程 HTTP 请求。支付验证由 **clawtip** 官方钱包处理。

### 绝不收集或传输
源代码、项目文件、专利信息、公司信息、商业秘密或个人身份信息。

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 1.1.1 | 2026-07-28 | Fix SkillSpector findings: inline file_utils and SM4; clarify AI-delivered service model |
| 1.1.0 | 2026-07-28 | Switch to official clawtip wallet; remove api.ideaidea.com.cn |
| 1.0.21 | 2026-07-27 | Fix ClawHub audit |
| 1.0.1 | 2026-07-20 | Fix payment flow |
| 1.0.0 | 2026-07-19 | Initial release |
