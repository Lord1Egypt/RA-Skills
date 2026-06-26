---
name: openclaw-config-rollback
description: "OpenClaw 配置回滚管理 - 备份、超时保护、自动回滚"
metadata:
  { "openclaw": { "emoji": "🔄", "requires": { "bins": ["bash"] }, "install": "自动安装（脚本已内置）" } }
---

# Config Rollback Skill

OpenClaw 配置回滚管理技能，提供配置修改前的自动备份、超时保护和自动回滚功能。

---

## 🎯 功能

- **配置备份** - 修改前自动备份到 `~/.openclaw/backups/`
- **超时保护** - 5 分钟倒计时，超时自动回滚
- **状态管理** - 跟踪配置修改状态
- **待验证事项** - 动态记录验证事项
- **启动自检** - Gateway 启动后自动验证配置

---

## 📋 使用方式

### 1. 准备修改配置

```bash
~/.openclaw/scripts/prepare-config-change.sh "修改描述" "验证事项 1,验证事项 2"
```

**参数：**
- `修改描述` - 简要描述修改内容（必需）
- `验证事项` - 逗号分隔的验证事项列表（可选）

**示例：**
```bash
~/.openclaw/scripts/prepare-config-change.sh "启用 obsidian 技能" "验证技能状态，验证 Gateway 启动"
```

**输出：**
- 备份文件路径
- 回滚截止时间（5 分钟后）
- 下一步操作提示

---

### 2. 修改配置

编辑 `~/.openclaw/openclaw.json`

---

### 3. 重启 Gateway

**必须在 5 分钟内完成：**

```bash
openclaw gateway restart
```

---

## 🔄 自动回滚机制

### 守护进程

**脚本：** `~/.openclaw/scripts/rollback-guardian.sh`

**Cron 任务：** 每分钟执行一次

```bash
*/1 * * * * ~/.openclaw/scripts/rollback-guardian.sh
```

### 工作逻辑

| 状态 | 行为 |
|------|------|
| 无配置修改 | 直接退出（安静模式） |
| Gateway 正常运行 | 清除状态文件（任务完成） |
| Gateway 未运行 + 未超时 | 继续等待 |
| Gateway 未运行 + 超时 | 执行回滚 |

---

## 📁 相关文件

| 文件 | 作用 |
|------|------|
| `scripts/prepare-config-change.sh` | 修改准备脚本 |
| `scripts/rollback-guardian.sh` | 超时回滚守护 |
| `scripts/config-alias.sh` | 交互式助手 |
| `backups/` | 配置备份目录 |
| `docs/PENDING_VERIFICATION.md` | 待验证事项记录 |

---

## 🚨 紧急回滚

```bash
cp $(ls -t ~/.openclaw/backups/*.json | head -1) ~/.openclaw/openclaw.json
openclaw gateway restart
```

---

## 🔧 安装

### 自动安装（推荐）

```bash
openclaw skills enable openclaw-config-rollback
```

### 手动安装

1. **复制脚本**
   ```bash
   # 脚本已在工作区
   ls ~/.openclaw/workspace/skills/config-rollback/scripts/
   ```

2. **设置权限**
   ```bash
   chmod +x ~/.openclaw/workspace/skills/config-rollback/scripts/*.sh
   ```

3. **设置 Cron**
   ```bash
   (crontab -l 2>/dev/null | grep -v "rollback-guardian"; echo "*/1 * * * * ~/.openclaw/workspace/skills/config-rollback/scripts/rollback-guardian.sh") | crontab -
   ```

4. **验证**
   ```bash
   crontab -l | grep rollback
   ```

---

## 📊 配置流程

```
修改配置
    ↓
执行 prepare-config-change.sh
├─ 自动备份到 backups/
├─ 创建状态文件 .config-modified-state
└─ 记录到 PENDING_VERIFICATION.md
    ↓
5 分钟倒计时开始
    ↓
守护进程每分钟检查
├─ 无状态文件 → 直接退出（安静模式）
├─ Gateway 正常运行 → 清除状态文件 ✅
├─ Gateway 未运行 + 未超时 → 继续等待
└─ Gateway 未运行 + 超时 → 自动回滚 ⚠️
```

---

## 🎯 最佳实践

### 修改前
1. 执行 `prepare-config-change.sh`
2. 记录修改原因到 `docs/CONFIG_CHANGELOG.md`

### 修改后
3. **5 分钟内**重启 Gateway
4. 查看 Discord 上的 BOOT.md 自检报告
5. 更新 `PENDING_VERIFICATION.md` 中的验证状态

---

## ⚠️ 注意事项

1. **修改前必须执行准备脚本** - 否则没有备份和超时保护
2. **5 分钟内必须重启** - 否则会自动回滚
3. **验证事项与修改目的关联** - 不是固定的验证内容

---

## 📚 相关文档

- `docs/CONFIG_QUICKREF.md` - 快速参考
- `CONFIG_CHANGE_RULES.md` - 详细规则
- `docs/CONFIG_MEMORY_SYSTEM.md` - 记忆系统设计
- `skills/brain2claw-content-manager/work/cases/001-config-management-flow.md` - 设计案例

---

**版本：** 1.0.2  
**作者：** 小麦 🌲  
**日期：** 2026-03-16
