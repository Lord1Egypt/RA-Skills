# 配额管理功能文档

> **版本：** v1.0.0  
> **启用日期：** 2026-03-12  
> **状态：** ✅ 生产就绪

---

## 📋 概述

配额管理系统为多用户环境提供资源限制和隔离，确保公平使用系统资源。

### 核心功能

- ✅ **身份识别**：自动区分管理员和普通用户
- ✅ **无限配额**：管理员享有无限资源配额
- ✅ **资源限制**：普通用户受磁盘、Token、消息数限制
- ✅ **超限处理**：配额用尽时自动拒绝请求
- ✅ **每日重置**：消息配额每日自动重置
- ✅ **详细日志**：所有配额操作记录在案

---

## 🎯 配额类型

| 配额类型 | 管理员 | 普通用户默认值 | 说明 |
|---------|--------|---------------|------|
| 磁盘配额 | ∞ | 100 MB | 文件存储、会话数据等 |
| Token 配额 | ∞ | 100,000 | LLM API 调用 token 数 |
| 消息配额 | ∞ | 1,000 条/天 | 每日消息数量限制 |
| Session 超时 | ∞ | 24 小时 | 会话空闲超时时间 |
| 最大并发 | ∞ | 5 | 同时进行的会话数 |

---

## 👥 用户身份

### 管理员

- **账号 ID:** `ou_b96f5424607baf3a0455b55e0f4a2213`
- **权限:** 无限配额，所有限制豁免
- **标识:** `isAdmin: true`

### 普通用户

- **权限:** 受默认配额限制
- **标识:** `isAdmin: false`
- **可配置:** 可通过配额管理器调整

---

## 🛠️ 使用指南

### 1. 查看配额使用情况

```bash
# 查看指定用户配额
cd /home/user/.openclaw/skills/multi-user-privacy
node scripts/quota-manager.js info <user_id>

# 示例：查看管理员配额
node scripts/quota-manager.js info ou_b96f5424607baf3a0455b55e0f4a2213

# 示例：查看普通用户配额
node scripts/quota-manager.js info ou_xxx123
```

### 2. 设置用户配额

```bash
# 设置普通用户配额
node scripts/quota-manager.js set <user_id> --disk=100 --token=100000 --message=1000

# 设置管理员（无限配额）
node scripts/quota-manager.js set <user_id> --admin

# 示例：为用户设置自定义配额
node scripts/quota-manager.js set ou_xxx123 --disk=50 --token=50000 --message=500
```

### 3. 重置用户配额

```bash
# 重置用户配额使用量（不改变配额限制）
node scripts/quota-manager.js reset <user_id>

# 示例：重置用户配额
node scripts/quota-manager.js reset ou_xxx123
```

### 4. 列出所有用户配额

```bash
# 查看所有用户的配额配置和使用情况
node scripts/quota-manager.js list
```

### 5. 通过 subagent-integration 查看

```bash
# 查看用户配额使用
node subagent-integration.js quota <user_id>

# 示例
node subagent-integration.js quota ou_b96f5424607baf3a0455b55e0f4a2213
```

---

## 📊 配置文件

### 配额数据库

**位置:** `/home/user/.openclaw/skills/multi-user-privacy/.quota-db.json`

**结构:**

```json
{
  "user_id": {
    "diskQuotaMB": 100,
    "tokenQuota": 100000,
    "messageQuota": 1000,
    "sessionTimeoutHours": 24,
    "maxConcurrentSessions": 5,
    "isAdmin": false,
    "used": {
      "disk": 0,
      "tokens": 0,
      "messages": 0,
      "lastReset": "2026-03-12T00:00:00.000Z"
    },
    "createdAt": "2026-03-12T00:00:00.000Z"
  }
}
```

**特殊值:** `-1` 表示无限配额

---

## 🔧 程序化使用

### QuotaManager API

```javascript
const { QuotaManager } = require('./subagent-integration.js');

const qm = new QuotaManager();

// 检查配额
const allowed = qm.checkQuota(userId, 'message', 1);
if (!allowed) {
  console.log('配额不足');
}

// 使用配额
qm.useQuota(userId, 'token', 1000);

// 获取使用情况
const usage = qm.getQuotaUsage(userId);
console.log(usage.used.messages);  // 已用消息数
console.log(usage.quota.messageQuota);  // 消息配额
```

### 配额类型

- `'disk'` - 磁盘空间 (MB)
- `'token'` - API Token 数
- `'message'` - 消息数量

---

## ⚠️ 配额超限处理

### 自动处理

当用户配额用尽时：

1. **请求拒绝:** 新请求会被自动拒绝
2. **日志记录:** 超限事件记录到 `.quota-exceeded.log`
3. **用户通知:** 控制台输出警告信息

### 超限日志

**位置:** `/home/user/.openclaw/skills/multi-user-privacy/.quota-exceeded.log`

**格式:**

```json
{
  "timestamp": "2026-03-12T10:00:00.000Z",
  "userId": "ou_xxx123",
  "quotaType": "message",
  "usage": {
    "used": { "messages": 1000 },
    "quota": { "messageQuota": 1000 }
  },
  "action": "blocked"
}
```

### 解决方法

1. **等待重置:** 消息配额每日自动重置
2. **手动重置:** 管理员使用 `reset` 命令
3. **提升配额:** 管理员调整用户配额限制

---

## 🔄 自动重置

### 消息配额

- **重置周期:** 每 24 小时
- **重置时间:** 距上次重置 24 小时后
- **自动触发:** 配额检查时自动判断

### 其他配额

- **磁盘配额:** 不清空，需手动清理或删除文件
- **Token 配额:** 不清空，按周期（如月度）手动重置

---

## 📈 监控与告警

### 日志文件

| 日志文件 | 说明 |
|---------|------|
| `.quota-db.json` | 配额数据库 |
| `.quota-exceeded.log` | 配额超限记录 |
| `logs/privacy-guard.log` | 综合隐私和配额日志 |

### 监控命令

```bash
# 实时监控配额超限
tail -f .quota-exceeded.log

# 查看配额数据库
cat .quota-db.json | jq
```

---

## 🧪 测试

### 运行测试套件

```bash
cd /home/user/.openclaw/skills/multi-user-privacy
node scripts/test-quota.js
```

### 测试覆盖

- ✅ 管理员无限配额
- ✅ 普通用户配额检查
- ✅ 配额超限检测
- ✅ Token 配额管理
- ✅ 磁盘配额管理
- ✅ 每日重置逻辑

---

## 🔐 安全考虑

### 管理员保护

- 管理员账号硬编码在代码中
- 自动分配无限配额
- 不受任何配额限制

### 用户隔离

- 每个用户独立配额账户
- 无法查看其他用户配额
- 配额数据存储在受保护目录

### 防滥用

- 配额超限自动拒绝
- 所有操作记录日志
- 支持行为分析和告警

---

## 📝 最佳实践

### 配额设置建议

| 用户类型 | 磁盘 | Token | 消息 | 说明 |
|---------|------|-------|------|------|
| 测试用户 | 10MB | 10,000 | 100 | 短期测试 |
| 普通用户 | 100MB | 100,000 | 1,000 | 日常使用 |
| 高级用户 | 500MB | 500,000 | 5,000 | 重度使用 |
| VIP 用户 | 1GB | 1,000,000 | 10,000 | 特殊权限 |

### 监控建议

1. **每日检查:** 查看配额超限日志
2. **每周审查:** 分析用户配额使用趋势
3. **每月调整:** 根据使用情况优化配额设置

### 告警阈值

建议设置告警当用户使用量达到：

- **80%:** 提醒用户注意使用
- **90%:** 警告即将超限
- **100%:** 自动拒绝并通知管理员

---

## 🆘 故障排查

### 问题：配额检查始终通过

**原因:** 可能是管理员账号或配置错误

**解决:**
```bash
# 检查用户是否为管理员
node scripts/quota-manager.js info <user_id>

# 检查配额数据库
cat .quota-db.json | jq '<user_id>'
```

### 问题：配额不重置

**原因:** 时间计算逻辑问题

**解决:**
```bash
# 手动重置
node scripts/quota-manager.js reset <user_id>
```

### 问题：配额扣减不生效

**原因:** 代码中可能调用了错误的 API

**解决:**
```bash
# 检查日志
grep "配额扣减" logs/privacy-guard.log
```

---

## 📚 相关文件

- `subagent-integration.js` - 配额管理核心实现
- `scripts/quota-manager.js` - 配额管理 CLI 工具
- `scripts/test-quota.js` - 配额功能测试脚本
- `.quota-db.json` - 配额数据库
- `.quota-exceeded.log` - 配额超限日志

---

## 📞 支持

如有问题，请查看日志或联系管理员。
