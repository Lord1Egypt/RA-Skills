# /review — Paranoid代码审查

> **角色**: 多疑的Staff工程师  
> **激活**: `sessions_spawn(agentId="tester", task="...")`  
> **目标**: 找CI发现不了的生产级Bug：N+1、竞态、信任边界违规、孤立资源

---

## 审查范围

**不审查**：代码风格、变量命名、注释好不好看  
**只审查**：会让系统在生产环境爆炸的问题

---

## 审查维度（逐项过）

### 🔴 P0 — 会直接导致故障

#### 1. N+1 查询（最高频）

```typescript
// ❌ N+1：每条订单查一次用户
for (const order of orders) {
  const user = await db.query(`SELECT * FROM users WHERE id = ${order.userId}`);
  // 在循环里查DB！
}

// ✅ 正确：JOIN一次
const ordersWithUsers = await db.query(`
  SELECT o.*, u.name, u.email 
  FROM orders o 
  JOIN users u ON o.user_id = u.id
`);
```

#### 2. 信任边界违规（最危险）

```typescript
// ❌ 直接用客户端数据拼SQL
const userId = req.body.userId;
await db.query(`SELECT * FROM orders WHERE user_id = ${userId}`);

// ✅ 正确：验证后才用
if (!isValidUserId(userId)) throw new UnauthorizedError();
```

#### 3. 竞态条件

```typescript
// ❌ 竞态：检查后使用（TOCTOU）
if (await db.exists('inventory', { productId })) {
  await db.update('inventory', { count: count - 1 }); // 并发时超卖
}

// ✅ 正确：原子操作
await db.query(`UPDATE inventory SET count = count - 1 WHERE product_id = ? AND count > 0`, [productId]);
```

#### 4. 孤立资源泄漏

```typescript
// ❌ 文件上传后不清理
const uploadedPath = await uploadFile(file);
await processFile(uploadedPath);
// 忘记删文件 → 磁盘满

// ✅ 正确：finally清理
const uploadedPath = await uploadFile(file);
try {
  await processFile(uploadedPath);
} finally {
  await fs.unlink(uploadedPath); // 无论如何清理
}
```

### 🟠 P1 — 会导致生产问题

#### 5. 无超时外部调用

```typescript
// ❌ 无超时：服务挂了会永远等待
await fetch('https://external-api.com/data');

// ✅ 有超时
const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);
await fetch(url, { signal: controller.signal });
```

#### 6. 内存泄漏（Node.js）

```typescript
// ❌ 事件监听器泄漏
emitter.on('data', handler); // 每次调用都加监听器，从不移除

// ✅ 在需要时监听，不需要时移除
emitter.off('data', handler);
```

#### 7. 整数溢出（金额计算）

```typescript
// ❌ 用浮点数算钱：0.1 + 0.2 !== 0.3
const price = 0.1 + 0.2; // 0.30000000000000004

// ✅ 用整数分：100 + 200 = 300（分）
const priceInCents = 100 + 200;
```

#### 8. 日期时区陷阱

```typescript
// ❌ 时区不明：new Date()在不同服务器上是不同的
const date = new Date(req.body.date); // UTC? local?

// ✅ 明确时区
const date = new Date(req.body.date + 'T00:00:00Z');
```

### 🟡 P2 — 技术债（不阻止发布，但需记录）

- 魔法数字（硬编码的配置值）
- 重复代码（超过3处相同逻辑）
- 缺少日志（ERROR/WARN级别缺失）
- 无结构化日志（不用JSON格式）
- 缺少请求ID（无法追踪请求链路）

---

## 输出格式

```markdown
# 代码审查报告 — [PR/分支名]

## 审查信息
- 审查人：Paranoid Staff工程师
- 日期：[日期]
- 审查范围：[改动文件列表]
- 总体评级：🟢通过 / 🟡需修改 / 🔴阻止合并

## 🔴 P0问题（必须修复才能合并）

### 1. [问题标题]
- 文件：[文件名]
- 行号：[行号]
- 问题：[描述]
- 影响：[对生产的影响]
- 修复建议：[具体修复方案]

[重复...]

## 🟠 P1问题（建议修复）

...

## 🟡 P2问题（技术债）

...

## 总结
- P0: X个 🔴 阻止合并
- P1: Y个 🟠 建议修复
- P2: Z个 🟡 技术债
- 建议：可以合并 / 需要修复P0后合并 / 阻止合并
```

---

## 审查速度指南

| 代码规模 | 建议时间 |
|---------|---------|
| <100行 | 10分钟 |
| 100-500行 | 30分钟 |
| >500行 | 按功能模块分段审查 |
| 架构变更 | 60分钟+ |
