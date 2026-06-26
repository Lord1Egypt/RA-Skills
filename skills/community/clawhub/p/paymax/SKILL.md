---
name: payment
description: 支付 Skill，识别用户支付/付款/结账意图，或接收其他 skill（如打赏 skill）的调用，执行 scripts/payment_api.py 调用收款码 API，获取 tradeCode 并醒目展示给用户。TRIGGER when: 用户说"我要支付"、"我要付款"、"去支付"、"帮我支付"、"结账"、"付钱"、"买单"，或被其他 skill 携带 amount 参数调用。DO NOT TRIGGER when: 用户表达打赏/送礼物/赞赏意图（由 tip skill 处理）。
---

# 支付 Skill

## 职责

识别用户支付意图，或接收其他 skill 的调用，通过执行 `scripts/payment_api.py` 调用收款码 API，获取 tradeCode 并展示给用户。

---

## 触发条件

**方式一：用户直接触发**

用户消息中包含以下意图时触发：
- 我要支付 / 我要付款
- 去支付 / 去付款
- 帮我支付
- 结账 / 付钱 / 买单

**方式二：被其他 skill 调用**

其他 skill（如打赏 skill）确认后，携带参数调用本 skill 执行支付。

---

## 接收的参数

| 参数名 | 类型 | 是否必填 | 来源 | 说明 |
|--------|------|----------|------|------|
| amount | number | 用户直接触发时需收集 | 用户输入 / 调用方传入 | 支付金额 |
| order_type | string | ❌ 可选 | 调用方传入 | 订单类型，如 `tip` |
| payee | string | ❌ 可选 | 调用方传入 | 收款方 |
| description | string | ❌ 可选 | 调用方传入 | 支付描述 |

---

## 处理流程

1. **接收触发**（用户直接触发 或 其他 skill 调用）

2. **检查 amount 是否存在**
   - 缺失 → 追问："请问您要支付多少金额？"

3. **检测运行环境，选择合适的脚本版本执行**

   可用脚本（两者输出格式完全相同，选一即可）：
   - `scripts/payment_api.py`（Python 版）
   - `scripts/payment_api.js`（Node.js 版）

   **环境检测优先级与命令选择规则（按顺序尝试）：**

   ```
   1. 检测 node 是否可用          → 可用则优先使用 Node.js 版本：
      node ~/.claude/skills/payment/scripts/payment_api.js --amount {amount} ...

   2. 检测 python3 是否可用       → 可用则使用 python3 执行 Python 版本：
      python3 ~/.claude/skills/payment/scripts/payment_api.py --amount {amount} ...

   3. 检测 python 是否可用        → 可用则使用 python 执行 Python 版本：
      python ~/.claude/skills/payment/scripts/payment_api.py --amount {amount} ...

   4. 三者均不可用                → 直接告知用户：
      "当前环境缺少 Node.js 和 Python，无法执行支付脚本，请联系管理员配置运行环境。"
   ```

   **检测命令示例：**
   ```bash
   # 检测 node
   node --version 2>/dev/null

   # 检测 python3
   python3 --version 2>/dev/null

   # 检测 python
   python --version 2>/dev/null
   ```

   **完整调用示例（Node.js）：**
   ```bash
   node ~/.claude/skills/payment/scripts/payment_api.js \
     --amount {amount} \
     [--order_type {order_type}] \
     [--payee {payee}] \
     [--description {description}]
   ```

   **完整调用示例（Python）：**
   ```bash
   python3 ~/.claude/skills/payment/scripts/payment_api.py \
     --amount {amount} \
     [--order_type {order_type}] \
     [--payee {payee}] \
     [--description {description}]
   ```

4. **解析脚本输出**
   - 第一行为 `SUCCESS` → 提取 `tradeCode` 和 `tradeLink`，展示成功结果
   - 第一行为 `FAIL` → 提取 `message`，展示失败提示
   - 脚本执行异常（非零退出码且无有效输出）→ 展示服务不可用提示

---

## 脚本输出格式

**成功：**
```
SUCCESS
tradeCode=62254562871846512
tradeLink=https://pay-h5.4199191.xyz/pyment/62254562871846512
```

**失败：**
```
FAIL
message=错误原因描述
```

---

## 回复话术

**追问金额：**
```
请问您要支付多少金额？
```

**正在处理：**
```
正在为您创建支付请求...
```

**成功（tradeCode 必须完整、准确、醒目展示）：**
```
✅ 支付请求创建成功！

🔢 交易码（tradeCode）：{tradeCode}
🔗 支付链接：{tradeLink}

请复制交易码或点击链接完成支付～
```

**API 返回失败（resultCode ≠ 1）：**
```
❌ 支付请求失败：{message}，请稍后重试。
```

**脚本执行异常（网络错误/超时等）：**
```
❌ 支付服务暂时不可用，请稍后再试或联系客服。
```

---

## 重要约束

1. **tradeCode 是最关键的输出，必须完整、准确、醒目地展示给用户，禁止修改其值**
2. tradeLink 作为辅助信息一并展示
3. 失败时给出友好提示，不向用户暴露技术细节（如 HTTP 状态码、堆栈信息等）
4. 被其他 skill 调用时，将最终结果（tradeCode + tradeLink 或错误信息）返回给调用方展示

---

## 示例对话

**示例 1：用户直接支付**
```
用户：我要支付
助手：请问您要支付多少金额？
用户：100 元
助手：正在为您创建支付请求...

✅ 支付请求创建成功！

🔢 交易码（tradeCode）：62254562871846512
🔗 支付链接：https://pay-h5.4199191.xyz/pyment/62254562871846512

请复制交易码或点击链接完成支付～
```

**示例 2：API 失败**
```
用户：帮我付款 200 元
助手：正在为您创建支付请求...

❌ 支付请求失败：服务繁忙，请稍后重试。
```

**示例 3：被打赏 skill 调用（内部流程，不直接对话）**
```
# 打赏 skill 传入参数：
# amount=50, order_type="tip", payee="主播小明", description="打赏主播小明50元"
# 支付 skill 执行后返回 tradeCode 和 tradeLink，由打赏 skill 展示给用户
```
