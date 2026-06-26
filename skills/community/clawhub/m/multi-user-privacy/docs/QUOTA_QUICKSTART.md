# 配额管理快速入门

> 5 分钟上手配额管理功能

---

## 🚀 快速开始

### 1️⃣ 查看当前配额配置

```bash
cd /home/user/.openclaw/skills/multi-user-privacy

# 查看所有用户配额
node scripts/quota-manager.js list
```

**示例输出:**
```
📊 配额数据库 (2 个用户)

👑 ou_b96f5424607baf3a0455b55e0f4a2213
   磁盘：0MB / ∞
   Token: 0 / ∞
   消息：0 / ∞
   创建：2026-03-12T02:00:13.266Z

👤 default
   磁盘：0MB / 100MB
   Token: 0 / 100000
   消息：0 / 1000
   创建：2026-03-12T00:00:00.000Z
```

---

### 2️⃣ 查看特定用户配额

```bash
# 查看管理员配额
node scripts/quota-manager.js info ou_b96f5424607baf3a0455b55e0f4a2213

# 查看普通用户配额
node scripts/quota-manager.js info ou_xxx123
```

---

### 3️⃣ 设置用户配额

#### 设置普通用户配额

```bash
node scripts/quota-manager.js set <user_id> \
  --disk=100 \
  --token=100000 \
  --message=1000
```

**示例:**
```bash
node scripts/quota-manager.js set ou_xxx123 --disk=50 --token=50000 --message=500
```

#### 设置管理员（无限配额）

```bash
node scripts/quota-manager.js set <user_id> --admin
```

**示例:**
```bash
node scripts/quota-manager.js set ou_xxx123 --admin
```

---

### 4️⃣ 重置用户配额

```bash
# 重置用户使用量（不改变配额限制）
node scripts/quota-manager.js reset ou_xxx123
```

---

## 📊 配额类型说明

| 参数 | 说明 | 默认值 | 单位 |
|------|------|--------|------|
| `--disk` | 磁盘空间配额 | 100 | MB |
| `--token` | Token 配额 | 100,000 | 个 |
| `--message` | 每日消息配额 | 1,000 | 条/天 |
| `--admin` | 管理员模式（无限配额） | - | - |

**特殊值:** `-1` 表示无限配额

---

## 🔍 常见场景

### 场景 1: 新用户注册

```bash
# 为新用户设置默认配额
node scripts/quota-manager.js set ou_new_user --disk=100 --token=100000 --message=1000
```

### 场景 2: 提升用户配额

```bash
# 提升为高级用户
node scripts/quota-manager.js set ou_user123 --disk=500 --token=500000 --message=5000
```

### 场景 3: 用户配额用尽

```bash
# 查看配额使用情况
node scripts/quota-manager.js info ou_user123

# 重置配额（如果确认需要）
node scripts/quota-manager.js reset ou_user123
```

### 场景 4: 授予管理员权限

```bash
# 设置管理员（无限配额）
node scripts/quota-manager.js set ou_trusted_user --admin
```

---

## 🧪 测试配额功能

```bash
# 运行测试套件
node scripts/test-quota.js
```

**测试内容:**
- ✅ 管理员无限配额
- ✅ 普通用户配额检查
- ✅ 配额超限检测
- ✅ Token 配额管理
- ✅ 磁盘配额管理

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `.quota-db.json` | 配额数据库 |
| `.quota-exceeded.log` | 配额超限日志 |
| `scripts/quota-manager.js` | 配额管理 CLI |
| `scripts/test-quota.js` | 测试脚本 |

---

## ⚠️ 注意事项

1. **管理员账号:** `ou_b96f5424607baf3a0455b55e0f4a2213` 自动获得无限配额
2. **每日重置:** 消息配额每 24 小时自动重置
3. **配额超限:** 超限后请求会被自动拒绝
4. **日志记录:** 所有配额操作都会记录日志

---

## 🆘 故障排查

### 问题：配额设置不生效

**解决:**
```bash
# 检查配额数据库
cat .quota-db.json | jq '<user_id>'

# 重新设置
node scripts/quota-manager.js set <user_id> --disk=100 --token=100000 --message=1000
```

### 问题：无法查看配额

**解决:**
```bash
# 检查文件权限
ls -la .quota-db.json

# 修复权限
chmod 644 .quota-db.json
```

---

## 📞 更多帮助

```bash
# 查看 CLI 帮助
node scripts/quota-manager.js

# 查看完整文档
cat docs/QUOTA_MANAGEMENT.md
```
