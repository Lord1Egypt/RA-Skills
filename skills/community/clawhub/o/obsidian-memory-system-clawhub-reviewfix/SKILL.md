---
name: "obsidian-memory-system"
version: "3.1.2"
description: >
  Obsidian persistent memory system: AI-delivered session continuity, task tracking, decision records, and project context for AI agents. Payment verification via clawtip. No vault content, note files, or credentials are collected or transmitted.
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

# obsidian-memory-system

Interact in the user's language. Supports Chinese, English, and other languages based on user input.

## 技能概述

Obsidian 永久记忆系统。本技能通过 clawtip 完成支付验证后，**由 AI 模型在对话中**交付工作日志、任务追踪、决策记录和跨会话的项目上下文管理。

### 服务交付方式

本技能是 **AI 对话交付型** 服务：
- `create_order.py` — 创建本地订单文件（仅用于 clawtip 支付验证）
- 支付由 **clawtip** 官方钱包处理
- `service.py` — 验证支付凭证后，指示 AI 在对话中执行记忆管理

### 交付内容

| # | 服务 | 说明 |
|---|------|------|
| 1 | 工作日志 | 结构化日记创建、任务追踪和进度记录 |
| 2 | 决策记录 | 架构和设计决策的文档化 |
| 3 | 会话连续性 | 跨 AI 会话的上下文保持 |
| 4 | 知识管理 | 笔记组织和链接、模板化写作 |
| 5 | 定期回顾 | 周/月报、记忆整理和精炼 |

---

## 环境变量配置

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `CLAWTIP_PAY_TO` | 是 | clawtip 商户收款地址 |

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
> 仅包含 orderNo、amount、question。不涉及任何笔记内容。

**成功：** `ORDER_NO=... AMOUNT=... QUESTION=... INDICATOR=...`
**失败：** `Order creation failed: <详情>` → 终止。

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

成功后，AI 将在对话中交付记忆管理服务。

---

## 数据处理说明

### 本地存储
| 文件 | 路径 | 内容 |
|------|------|------|
| 订单文件 | `~/.openclaw/skills/orders/{indicator}/{order_no}.json` | orderNo、amount、question、加密凭证 |

### 远程传输
本技能自身不发起任何远程 HTTP 请求。

### 绝不收集或传输
Obsidian 库内容、笔记文件、模板、项目文件或凭证。

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 3.1.1 | 2026-07-28 | Fix SkillSpector: inline file_utils/SM4; service delivery specification; English error messages |
| 3.1.0 | 2026-07-28 | Switch to official clawtip wallet |
| 3.0.37 | 2026-07-27 | Fix ClawHub audit |
