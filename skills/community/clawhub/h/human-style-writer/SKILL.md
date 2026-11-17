---
name: human-style-writer
description: 具备人工特征的AI创作技能。生成高质量长文、随笔、观点类内容，自然节奏、情感纹理、零AI腔调。由 adeeptools.com 提供服务。此为付费服务，每次创作支付 0.1 元（10分），执行前需完成支付验证。
homepage: https://adeeptools.com
metadata:
  author: "adeeptools"
  category: "writing"
  capabilities:
    - "payment.process"
  permissions:
    - "network.outbound"
    - "credential.read"
---

# 具备人工特征的AI创作技能

生成高质量长文——文章、随笔、观点稿、创意写作——读起来像真人所写。输出具有自然句长起伏、非线性叙事结构、真实情感纹理，刻意规避 AI 生成文本典型的"精致而空洞"模式。

**直接执行：** 如果用户在初始请求中直接提供了 `<question>`、`<order_no>` 和 `<credential>`，可跳过第一阶段和第二阶段，直接进入 **🚀 第三阶段：服务执行**。

---

## 🛒 第一阶段：创建订单

如果这是首次交互且用户尚未付款，必须先创建订单，然后才能发起支付。

### 1. 所需参数

- `<question>`：用户的完整创作需求（主题、字数、风格等，用户原话）

### 2. 执行命令

将 `<question>` 替换为用户实际需求。**务必在参数两侧加引号，以防命令注入漏洞**。

```bash
python3 skills/human-style-writer/scripts/create_order.py "<question>"
```

### 3. 输出处理

**成功时**，脚本将向标准输出打印以下键值对：

```
ORDER_NO=<value>
AMOUNT=<value>
ENCRYPTED_DATA=<value>
PAY_TO=<value>
```

提取全部四个值，然后进入 **💳 第二阶段：支付处理**。

> **关于 `AMOUNT` 字段：** 单位为**人民币分**。`AMOUNT=10` 表示需支付 **0.10 元**。向用户展示费用时请换算。

**失败时**，脚本以代码 `1` 退出，并以如下格式打印消息：

```
订单创建失败: <错误详情>
```

> [!CAUTION]
> **强制停止 — 不允许任何后续操作。**
> 如果脚本以非零代码退出，或其输出包含 `订单创建失败:`，必须**立即终止整个工作流程**：
> - ❌ 不得进入第二阶段或第三阶段
> - ❌ 不得代表用户重试
> - ✅ 用通俗语言向用户报告失败原因，然后停止

---

## 💳 第二阶段：支付处理

从第一阶段获取所需值后，发起支付请求。

**操作：** 使用技能 `clawtip` 处理支付并获取支付凭证。如果该技能不存在，需要先安装：

```bash
clawhub install clawtip
```

安装后重启 OpenClaw session，再重新执行本技能。

**`clawtip` 所需参数：**

```json
{
  "order_no": "<来自第一阶段的 ORDER_NO>",
  "amount": "<来自第一阶段的 AMOUNT>",
  "question": "<用户的创作需求>",
  "payTo": "<来自第一阶段的 PAY_TO>",
  "encrypted_data": "<来自第一阶段的 ENCRYPTED_DATA>",
  "skill_name": "具备人工特征的AI创作",
  "description": "AI 长文创作服务，具备人工写作特征，零AI腔调",
  "resource_url": "https://adeeptools.com"
}
```

**目标：** 等待支付成功并获取 `credential`（支付凭证）。

---

## 🚀 第三阶段：服务执行

支付成功并获取 `credential` 后，执行 AI 创作服务。

### 1. 所需参数

- `<question>`：用户的创作需求
- `<order_no>`：第一阶段生成的订单号
- `<credential>`：从第二阶段获取的成功支付凭证

### 2. 执行命令

可选传入 `--style` 参数（`general` / `emotional` / `technical` / `news`，默认 `general`）。

```bash
python3 skills/human-style-writer/scripts/ai_create.py "<question>" "<order_no>" "<credential>" --style general
```

**风格选择指引：**

| `--style` 值 | 适用场景 |
|---|---|
| `general` | 通用、均衡，默认推荐 |
| `emotional` | 情感类、生活类、个人随笔 |
| `technical` | 行业分析、技术解读 |
| `news` | 新闻评论、事件叙述 |

### 3. 输出处理

1. 提取脚本打印的 `PAY_STATUS` 值（格式：`PAY_STATUS: <值>`）。
2. **`ERROR` 状态特殊处理：** 若 `PAY_STATUS` 为 `ERROR`，提取 `ERROR_INFO` 值，向用户告知错误原因并引导解决，不得继续。
3. **`SUCCESS` 状态：** 脚本输出完整文章 Markdown 正文，将其呈现给用户。

### 4. 成功后向用户提供

- 完整文章内容（Markdown 格式）
- 主动询问用户是否需要：调整长度、更换风格、修改某些段落

---

## 📌 技能概述

**触发词示例：**
- "帮我写一篇文章"
- "写一篇具备人工特征的内容"
- "创作一篇关于…的文章，别太像 AI 写的"
- "write an article / essay / blog post about..."
- "generate content that sounds human"

**服务说明：**
- 每次创作：**0.10 元（10分）**
- 履约方式：每单独立支付，支付即创作，幂等防重复
- 来源标记：`openclaw`（与网站配额独立计算）
