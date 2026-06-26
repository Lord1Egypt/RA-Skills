# 记忆自动保存系统 - 使用指南

## 系统概述

已实现三层防护的自动记忆保存系统：

### 1. Bootstrap Hook 提醒 ✅
- 每次会话开始时注入记忆管理提醒
- 提醒 AI 定期检查 token 使用率
- 轻量级，不影响性能

### 2. 定时任务自动检查 ✅
- 每 30 分钟自动检查活跃会话
- Token 使用率 ≥ 70% 自动保存
- 真正的自动化，不依赖 AI

### 3. 手动触发 ✅
- 用户随时可以说"保存记忆"
- 或直接运行命令

## 定时任务详情

**任务名称：** 记忆自动保存检查

**运行频率：** 每 30 分钟

**触发条件：**
- Token 使用率 ≥ 70%
- 距上次保存 > 30 分钟（冷却期）

**保存位置：**
- `~/clawd/memory/daily/YYYY-MM-DD.md`
- 自动生成 L0/L1 分层文件

**任务 ID：** c6282835-0a36-402e-b0e5-b28be76c9459

## 手动命令

### 检查会话状态

```bash
# 正常检查（70% 阈值）
node ~/clawd/scripts/memory-session-checker.js

# Dry run（不实际保存）
node ~/clawd/scripts/memory-session-checker.js --dry-run

# 自定义阈值
node ~/clawd/scripts/memory-session-checker.js --threshold=0.6

# 自定义冷却期
node ~/clawd/scripts/memory-session-checker.js --cooldown=20
```

### 查看保存历史

```bash
# 查看最近 10 次保存
node ~/clawd/scripts/memory-session-checker.js history

# 查看最近 20 次
node ~/clawd/scripts/memory-session-checker.js history 20
```

### 管理定时任务

```bash
# 查看所有任务
openclaw cron list

# 查看任务运行历史
openclaw cron runs c6282835-0a36-402e-b0e5-b28be76c9459

# 手动触发一次
openclaw cron run c6282835-0a36-402e-b0e5-b28be76c9459

# 禁用任务
openclaw cron update c6282835-0a36-402e-b0e5-b28be76c9459 --disabled

# 启用任务
openclaw cron update c6282835-0a36-402e-b0e5-b28be76c9459 --enabled

# 删除任务
openclaw cron remove c6282835-0a36-402e-b0e5-b28be76c9459
```

## 工作流程

```
每 30 分钟
    ↓
检查活跃会话
    ↓
Token ≥ 70%?
    ↓
   是 → 检查冷却期
         ↓
        已过 → 自动保存
               ├─ 追加到今日日志
               ├─ 生成分层文件
               └─ 记录历史
    ↓
   否 → 跳过
```

## 实际效果

### 场景 1: 正常对话

```
[对话进行中...]
Token: 50k/200k (25%)
↓
[30 分钟后检查]
Token: 120k/200k (60%)
↓
未达到阈值，继续
```

### 场景 2: 长对话触发

```
[长对话进行中...]
Token: 150k/200k (75%)
↓
[30 分钟后检查]
✅ 达到 70% 阈值
↓
🤖 自动保存记忆
↓
📝 追加到 ~/clawd/memory/daily/2026-02-20.md
↓
🔄 生成分层文件
↓
✅ 保存完成
```

### 场景 3: 冷却期保护

```
[刚保存完 10 分钟]
Token: 145k/200k (72.5%)
↓
[检查触发]
⏭️  跳过: 距上次保存仅 10 分钟
↓
继续对话
```

## 状态文件

**位置：** `~/clawd/.memory-checker-state.json`

**内容：**
```json
{
  "lastSave": {
    "agent:main:main": 1771533737755
  },
  "history": [
    {
      "sessionKey": "agent:main:main",
      "sessionId": "29cd433f-5273-489b-af56-5a816fdcccbb",
      "timestamp": 1771533737755,
      "usage": 0.75,
      "file": "/Users/mrying/clawd/memory/daily/2026-02-20.md"
    }
  ]
}
```

## 配置调整

### 修改阈值

编辑 `~/clawd/scripts/memory-session-checker.js`：

```javascript
this.threshold = options.threshold || 0.70; // 改为 0.60 = 60%
```

### 修改冷却期

```javascript
this.cooldownMinutes = options.cooldownMinutes || 30; // 改为 20 分钟
```

### 修改检查频率

```bash
# 删除旧任务
openclaw cron remove c6282835-0a36-402e-b0e5-b28be76c9459

# 创建新任务（每 15 分钟）
openclaw cron add \
  --name "记忆自动保存检查" \
  --every 15m \
  --session isolated \
  --message "运行记忆检查: node ~/clawd/scripts/memory-session-checker.js" \
  --no-deliver
```

## 监控和调试

### 查看当前会话状态

```bash
openclaw sessions --active 60 --json
```

### 测试检查脚本

```bash
# Dry run 测试
node ~/clawd/scripts/memory-session-checker.js --dry-run

# 低阈值测试（模拟触发）
node ~/clawd/scripts/memory-session-checker.js --threshold=0.3 --dry-run
```

### 查看定时任务日志

```bash
openclaw cron runs c6282835-0a36-402e-b0e5-b28be76c9459
```

## 故障排除

### 问题 1: 定时任务未运行

**检查：**
```bash
openclaw cron list
```

**确认：**
- Status 是否为 enabled
- Next 时间是否正确

**解决：**
```bash
# 手动触发测试
openclaw cron run c6282835-0a36-402e-b0e5-b28be76c9459
```

### 问题 2: 保存失败

**检查：**
```bash
# 手动运行脚本
node ~/clawd/scripts/memory-session-checker.js --dry-run
```

**常见原因：**
- 目录权限问题
- 脚本路径错误
- 依赖缺失

### 问题 3: 触发过于频繁

**调整阈值：**
```bash
# 提高到 80%
node ~/clawd/scripts/memory-session-checker.js --threshold=0.8
```

**或延长冷却期：**
```bash
# 延长到 60 分钟
node ~/clawd/scripts/memory-session-checker.js --cooldown=60
```

## 最佳实践

1. **保持默认配置** - 70% 阈值 + 30 分钟冷却期已经很合理
2. **定期检查历史** - 每周查看一次保存历史
3. **重要对话手动保存** - 不要完全依赖自动化
4. **监控任务状态** - 确保定时任务正常运行

## 与分层记忆系统集成

保存后的文件会自动生成分层：

```bash
# 搜索记忆（使用 L1 节省 tokens）
node ~/clawd/skills/layered-memory/index.js search "关键词" l1

# 读取今天的记忆
node ~/clawd/skills/layered-memory/index.js read ~/clawd/memory/daily/2026-02-20.md l1

# 查看统计
node ~/clawd/skills/layered-memory/index.js stats
```

## 总结

✅ **完全自动化** - 定时任务每 30 分钟检查
✅ **智能触发** - 70% 阈值 + 冷却期保护
✅ **可靠保存** - 自动追加到日志并生成分层
✅ **灵活配置** - 可调整阈值、频率、冷却期
✅ **完整监控** - 历史记录、状态文件、任务日志

从现在开始，你再也不用担心记忆丢失了！🎉
