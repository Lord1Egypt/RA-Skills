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

**直接执行：** 如果用户在初始请求中同时提供了 `<question>` 和已支付完成的 `<order_no>`，可跳过第一阶段和第二阶段，直接进入 **🚀 第三阶段：服务执行**。

---

## 🛒 第一阶段：创建订单

本阶段会调用远程服务生成订单，并在本地生成 **订单文件**（供 `clawtip` 技能读取）。

### 1. 所需参数

- `<question>`：用户的完整创作需求（主题、字数、风格等，用户原话）

### 2. 执行命令

**务必在参数两侧加引号，以防命令注入漏洞**。

```bash
python3 skills/human-style-writer/scripts/create_order.py "<question>"
```

### 3. 输出处理

**成功时**，脚本将向标准输出打印以下键值对：

```
ORDER_NO=<订单号>
INDICATOR=<skill 标识，MD5(skill_name)>
AMOUNT=<金额，单位分>
ORDER_FILE=<订单文件绝对路径>
```

提取 `ORDER_NO` 和 `INDICATOR` 两个值，进入 **💳 第二阶段：支付处理**。

> **关于 `AMOUNT` 字段：** 单位为**人民币分**。`AMOUNT=10` 表示需支付 **0.10 元**。向用户展示费用时请换算。

**失败时**，脚本以代码 `1` 退出，并打印 `订单创建失败: <错误详情>`。

> [!CAUTION]
> **强制停止 — 不允许任何后续操作。**
> 如果脚本以非零代码退出或输出包含 `订单创建失败:`：
> - ❌ 不得进入第二阶段或第三阶段
> - ❌ 不得代表用户重试
> - ✅ 用通俗语言向用户报告失败原因，然后停止

---

## 💳 第二阶段：支付处理

**操作：** 调用 `clawtip` 技能处理支付。若该技能未安装，告知用户运行：

```bash
clawhub install clawtip
```

并重启 OpenClaw session。

**调用 `clawtip` 时只需传入两个参数：**

- `order_no`：第一阶段输出的 `ORDER_NO`
- `indicator`：第一阶段输出的 `INDICATOR`

`clawtip` 会自动：
1. 从 `~/.openclaw/skills/orders/{indicator}/{order_no}.json` 读取订单信息（第一阶段已写好）
2. 发起支付请求
3. 将支付凭证 `payCredential` 写回**同一订单文件**

**等待 `clawtip` 返回结果后：**

- 如 `clawtip` 输出包含 `已获取到支付凭证` 和 `订单号: <ORDER_NO>`：进入 **🚀 第三阶段：服务执行**（用该订单号）
- 如 `clawtip` 输出 `授权链接:` 或 `鉴权链接:`：提示用户完成授权/扫码支付后再继续
- 如 `clawtip` 输出网络/系统异常：向用户报告错误，停止流程

---

## 🚀 第三阶段：服务执行

`clawtip` 成功写入 `payCredential` 后，执行 AI 创作服务。脚本会自动从订单文件读取 `question` 和 `payCredential`，你只需提供订单号。

### 1. 所需参数

- `<order_no>`：第一阶段生成的订单号

### 2. 执行命令

可选传入 `--style` 参数（`general` / `emotional` / `technical` / `news`，默认 `general`）。

```bash
python3 skills/human-style-writer/scripts/ai_create.py "<order_no>" --style general
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
2. **`SUCCESS` 状态：** 脚本输出完整文章 Markdown 正文，将其呈现给用户。
3. **`FAIL` 状态：** 说明 `clawtip` 支付凭证解密后是失败状态。**必须回头检查 `clawtip` 原始输出** 中是否有 `授权链接:` 或 `鉴权链接:`，如有则按 clawtip 协议走授权/鉴权流程，再重试第三阶段。
4. **`ERROR` 状态：** 提取 `ERROR_INFO` 值，向用户告知错误原因，不得继续。

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
