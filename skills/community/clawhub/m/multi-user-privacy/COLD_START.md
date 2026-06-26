# 冷启动流程文档

## 概述

冷启动（Cold Start）是指在 `.user-context.json` 配置文件不存在时，通过第一个用户触发管理员设置的流程。

## 设计目标

1. **零配置启动** - 新实例无需预先配置即可使用
2. **灵活设置** - 第一个用户可以设置自己或他人为管理员
3. **安全可靠** - 只有第一个用户可以设置，防止恶意覆盖
4. **用户友好** - 提供交互式向导和清晰的说明

---

## 流程图

```
全新 OpenClaw 实例
        │
        ▼
┌─────────────────┐
│ 第一个用户对话   │
│ (任意用户)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ cold-start.js   │
│ 检测配置文件     │
│ 不存在 → 冷启动  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 创建冷启动标志   │
│ .cold-start-in-progress │
│ 记录第一个用户   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 显示设置说明     │
│ 引导用户设置     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌──────────┐ ┌──────────┐
│ 设置自己  │ │ 设置他人  │
│ 为 admin  │ │ 为 admin  │
└────┬─────┘ └────┬─────┘
     │            │
     └──────┬─────┘
            │
            ▼
┌─────────────────┐
│ 验证：只有第一个 │
│ 用户可以设置     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 创建配置文件     │
│ .user-context.json │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 清除冷启动标志   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 完成！正常使用   │
└─────────────────┘
```

---

## 文件说明

### 冷启动标志文件

**位置：** `~/.openclaw/workspace/.cold-start-in-progress`

**内容：**
```json
{
  "firstUser": {
    "id": "ou_xxx",
    "name": "用户昵称",
    "timestamp": "2026-03-04T10:30:00.000Z"
  },
  "startTime": 1709548200000,
  "status": "awaiting-admin-setup"
}
```

**作用：**
- 记录第一个用户信息
- 防止其他用户篡改设置
- 超时自动失效（24 小时）

### 配置文件

**位置：** `~/.openclaw/workspace/.user-context.json`

**冷启动创建的格式：**
```json
{
  "_comment": "Multi-User Privacy Configuration - Role-based access control",
  "_version": "0.2.0",
  "_createdAt": "2026-03-04T10:30:00.000Z",
  "_setupBy": "ou_xxx",
  
  "users": [
    {
      "id": "ou_yyy",
      "name": "老刘",
      "role": "admin"
    }
  ],
  
  "privacyMode": "strict"
}
```

**说明：**
- `_setupBy` 记录是谁设置了管理员（第一个用户）
- `_createdAt` 记录创建时间
- 其他字段与普通配置相同

---

## 使用场景

### 场景 1: 新实例部署（推荐）

```bash
# 1. 安装技能
npx clawhub install multi-user-privacy

# 2. 重启 OpenClaw
openclaw gateway restart

# 3. 第一个用户开始对话
# → 自动触发冷启动流程

# 4. 按提示设置管理员
# → 完成！
```

### 场景 2: 第一个用户设置自己为管理员

```bash
# 查看冷启动状态
node ~/.openclaw/skills/multi-user-privacy/scripts/cold-start.js status
# 输出：{"status": "not-started"}

# 第一个用户触发冷启动
node ~/.openclaw/skills/multi-user-privacy/scripts/cold-start.js start "ou_xxx" "张三"
# 输出：{"success": true, "isFirstUser": true}

# 设置自己为管理员
node ~/.openclaw/skills/multi-user-privacy/scripts/cold-start.js setup "ou_xxx" "张三" "ou_xxx"
# 输出：{"success": true, "admin": {"id": "ou_xxx", "name": "张三", "role": "admin"}}
```

### 场景 3: 第一个用户指定他人为管理员

```bash
# 第一个用户触发冷启动
node cold-start.js start "ou_xxx" "张三"

# 指定他人为管理员（如老板）
node cold-start.js setup "ou_boss123" "老板" "ou_xxx"
# 输出：{"success": true, "admin": {"id": "ou_boss123", "name": "老板", "role": "admin"}}
```

### 场景 4: 非第一个用户尝试设置（应失败）

```bash
# 冷启动已触发，第一个用户是 ou_xxx

# 第二个用户尝试设置
node cold-start.js setup "ou_yyy" "李四" "ou_yyy"
# 输出：{"success": false, "message": "只有第一个用户可以设置管理员"}
```

---

## CLI 命令

### 查看状态

```bash
node cold-start.js status
```

**输出示例：**
```json
{
  "status": "not-started",
  "message": "冷启动未开始，第一个用户将自动触发"
}
```

### 开始冷启动

```bash
node cold-start.js start <userId> [userName]
```

**示例：**
```bash
node cold-start.js start "ou_xxx" "张三"
```

### 设置管理员

```bash
node cold-start.js setup <adminId> <adminName> <setupByUserId>
```

**示例（设置自己）：**
```bash
node cold-start.js setup "ou_xxx" "张三" "ou_xxx"
```

**示例（指定他人）：**
```bash
node cold-start.js setup "ou_boss123" "老板" "ou_xxx"
```

### 取消冷启动

```bash
node cold-start.js cancel <userId>
```

### 查看设置说明

```bash
node cold-start.js instructions
```

---

## 交互式向导

```bash
bash ~/.openclaw/skills/multi-user-privacy/scripts/setup-admin-interactive.sh
```

**向导流程：**
1. 检查是否已配置
2. 选择设置方式（自己/他人）
3. 输入账号信息
4. 确认并保存
5. 完成！

---

## 安全机制

### 1. 唯一设置权

**规则：** 只有第一个用户可以设置管理员

**实现：**
- 冷启动标志记录第一个用户 ID
- 设置时验证 `setupByUserId === firstUser.id`
- 不匹配则拒绝

### 2. 超时失效

**规则：** 冷启动状态 24 小时后自动失效

**实现：**
- 检查 `startTime + 24h < now`
- 超时则清除标志，需重新触发

### 3. 防重复设置

**规则：** 配置一旦创建，不可通过冷启动覆盖

**实现：**
- 检查 `.user-context.json` 是否存在
- 存在则拒绝冷启动设置
- 需手动删除配置文件才能重置

### 4. 审计日志

**规则：** 所有冷启动操作记录日志

**位置：** `~/.openclaw/workspace/memory/cold-start-audit.log`

**内容：**
```
[2026-03-04 10:30:00] Cold start triggered by ou_xxx
[2026-03-04 10:31:00] Admin setup: ou_boss123 (admin) by ou_xxx
[2026-03-04 10:31:00] Cold start completed
```

---

## 故障排除

### 问题：冷启动标志残留

```bash
# 手动清除
rm ~/.openclaw/workspace/.cold-start-in-progress
```

### 问题：配置文件损坏

```bash
# 删除并重新配置
rm ~/.openclaw/workspace/.user-context.json
bash setup-admin-interactive.sh
```

### 问题：忘记管理员账号

```bash
# 查看配置
cat ~/.openclaw/workspace/.user-context.json
```

---

## 最佳实践

1. **尽快设置** - 第一个用户对话后立即设置管理员
2. **记录账号** - 保存管理员账号 ID 到安全位置
3. **备份配置** - 定期备份 `.user-context.json`
4. **审计日志** - 定期检查 `cold-start-audit.log`

---

## 版本历史

- v0.2.0 (2026-03-04): 冷启动功能首次实现
- v0.2.1 (2026-03-04): 添加超时失效机制
- v0.2.2 (2026-03-04): 添加交互式向导
