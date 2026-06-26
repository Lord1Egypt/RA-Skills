# Multi-User Privacy v0.4.0 - 完整版

## 🎉 所有改进已完成

### ✅ P0 优先级（核心安全）
1. ✅ **记忆文件物理隔离** - 普通用户无法访问 MEMORY.md
2. ✅ **防绕过机制** - 封装 fs 模块，防止直接文件访问
3. ✅ **全局消息拦截** - 所有消息必经隐私检查

### ✅ P1 优先级（功能完善）
1. ✅ **配置统一管理** - .privacy-config.json 统一配置
2. ✅ **上下文自动识别** - OpenClaw 启动时自动激活
3. ✅ **项目归属检查** - 防止越权操作
4. ✅ **增强日志审计** - JSON 格式 + 查看工具

---

## 📦 文件结构

```
/home/user/.openclaw/skills/multi-user-privacy/
├── SKILL.md                      # 技能说明
├── privacy-guard.js              # 核心检查逻辑
├── scripts/
│   ├── auto-inject.js            # 自动注入（启动时加载）
│   ├── view-logs.js              # 日志查看工具
│   └── inject-hook.js            # 手动注入脚本
└── projects-config-template.json # 项目配置模板

/home/user/.openclaw/workspace/
├── .privacy-config.json          # 统一配置文件
├── .projects-config.json         # 项目归属配置
├── memory/
│   ├── MEMORY.md                 # 仅管理员可访问
│   ├── users/                    # 用户独立记忆目录
│   │   ├── ou_xxx.md
│   │   └── ou_yyy.md
│   └── 2026-03-11.md            # 共享当日记忆
└── logs/
    ├── privacy-guard.json        # JSON 格式日志
    └── privacy-guard.log         # 简化版日志
```

---

## 🚀 启动方式

### 方式 1：自动启动（推荐）

在 OpenClaw 主入口添加：

```javascript
// 在 main.js 或 index.js 开头
require('./skills/multi-user-privacy/scripts/auto-inject');
```

### 方式 2：手动启动

```bash
node /home/user/.openclaw/skills/multi-user-privacy/scripts/auto-inject.js
```

---

## 📋 使用示例

### 1. 对话前检查

```javascript
const context = { chat_id: 'user:ou_xxx' };
const checkedContext = global.privacyGuard.checkAndInject(context);
```

### 2. 回复前检查

```javascript
const check = global.privacyGuard.checkReplyBeforeSend(response, userId);
if (!check.allowed) {
    response = rewriteResponse(response);
}
```

### 3. 项目权限检查

```javascript
const perm = global.privacyGuard.checkProjectPermission(userId, 'hazmat-news', 'write');
if (!perm.allowed) {
    throw new Error('无权限操作此项目');
}
```

### 4. 保存用户记忆（隔离）

```javascript
global.privacyGuard.saveUserMemory(userId, '记忆内容');
```

### 5. 查看日志

```bash
# 查看最近 10 条
node scripts/view-logs.js

# 查看最近 50 条
node scripts/view-logs.js 50

# 只看失败的
node scripts/view-logs.js --failures

# 查看特定用户
node scripts/view-logs.js --user=ou_xxx
```

---

## 🔒 安全机制

### 1. 记忆隔离

| 用户类型 | 可访问文件 |
|---------|-----------|
| 管理员 | MEMORY.md + 当日记忆 + TOOLS.md + 所有用户记忆 |
| 普通用户 | 自己的记忆 + 当日记忆 + TOOLS.md |

### 2. 文件系统封装

```javascript
// 尝试直接读取 MEMORY.md（会被拦截）
fs.readFileSync('MEMORY.md');
// ❌ Error: [PrivacyGuard] 未授权访问：MEMORY.md
```

### 3. 全局消息拦截

所有消息必经检查，无法绕过：
- ✅ 对话前自动识别身份
- ✅ 回复前自动检查敏感词
- ✅ 文件操作自动检查权限

---

## 📊 测试结果

```
=== v0.4.0 完整功能测试 ===

测试 1: 记忆文件隔离
✅ 管理员记忆：1 个文件
✅ 普通用户记忆：1 个文件

测试 2: 记忆访问权限
✅ 管理员访问 MEMORY.md: true
✅ 普通用户访问 MEMORY.md: false

测试 3: 项目归属检查
✅ 孙哥操作 hazmat: true
✅ 第三方操作 hazmat: false

测试 4: 隐私检查
✅ 安全消息：true
✅ 敏感消息拦截：true

测试 5: 配置加载
✅ 项目配置：1 个项目

🎉 v0.4.0 所有功能测试通过！
```

---

## 🎯 配置说明

### .privacy-config.json

```json
{
  "admin": {
    "id": "ou_b96f5424607baf3a0455b55e0f4a2213",
    "name": "老刘",
    "role": "admin"
  },
  "users": [...],
  "privacy": {
    "mode": "strict",
    "forbiddenTerms": ["老刘", "主人", "管理员"],
    "isolationPatterns": ["其他账号", "另一个用户"]
  },
  "autoCheck": {
    "enabled": true,
    "hookOnStartup": true,
    "blockOnFailure": true
  }
}
```

### .projects-config.json

```json
{
  "projects": {
    "hazmat-news": {
      "name": "危化品新闻采集系统",
      "owner": "ou_ba3410ec9024501b3383141a5ba7bec4",
      "collaborators": ["ou_b96f5424607baf3a0455b55e0f4a2213"]
    }
  }
}
```

---

## 🐛 故障排查

### 问题 1：自动注入未生效

```bash
# 检查是否在主入口添加了 require
grep -n "auto-inject" ~/.openclaw/runtime/main.js

# 手动测试
node ~/.openclaw/skills/multi-user-privacy/scripts/auto-inject.js
```

### 问题 2：记忆文件权限错误

```bash
# 检查目录权限
ls -la ~/.openclaw/workspace/memory/users/

# 修复权限
chmod 750 ~/.openclaw/workspace/memory/users/
```

### 问题 3：日志查看失败

```bash
# 检查日志文件
ls -la ~/.openclaw/logs/privacy-guard.*

# 手动查看
cat ~/.openclaw/logs/privacy-guard.log | tail -20
```

---

## 📈 更新日志

- **v0.4.0 (2026-03-11)**: 🎉 完整版
  - 记忆文件物理隔离
  - 配置统一管理
  - 防绕过机制（fs 封装）
  - 全局消息拦截
  - 自动注入启动

- v0.3.1: P0 优先级改进
- v0.3.0: 集成 conversation-isolator
- v0.2.0: 基于角色的权限管理
- v0.1.0: 初始版本

---

**版本：** v0.4.0  
**状态：** ✅ 所有 P0+P1 改进完成  
**测试：** ✅ 全部通过
