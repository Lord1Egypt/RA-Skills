# 分层记忆系统 - 实用集成方案

## 问题回顾

原计划的自动触发器无法真正自动化，因为：
- AI 无法主动执行外部脚本
- OpenClaw hooks 主要用于 bootstrap 阶段
- 需要在系统层面集成才能实现真正的自动化

## 实用方案（三层防护）

### 方案 1: Bootstrap Hook 提醒 ✅ (已实现)

**作用：** 每次会话开始时提醒 AI 注意记忆管理

**实现：**
- 在 `agent:bootstrap` 时注入提醒文档
- AI 会看到记忆管理的命令和阈值
- 提醒 AI 定期检查 token 使用率

**优点：**
- 轻量级，不影响性能
- 每次会话都会提醒
- AI 可以主动检查和保存

**局限：**
- 依赖 AI 主动执行
- 不是完全自动化

### 方案 2: 定时任务检查 ⭐ (推荐新增)

**作用：** 定期检查会话状态，自动保存记忆

**实现：**
```bash
# 添加定时任务，每 30 分钟检查一次
cron add --name "Memory Auto-Save" \
  --schedule "*/30 * * * *" \
  --command "node ~/clawd/scripts/memory-session-checker.js"
```

**工作流程：**
1. 定时任务每 30 分钟运行
2. 检查当前会话的 token 使用率
3. 如果达到阈值（如 70%），触发保存
4. 保存后通知用户

**优点：**
- 真正的自动化
- 不依赖 AI 主动执行
- 可靠的后台保护

**需要开发：**
- `memory-session-checker.js` - 检查会话状态
- 与 OpenClaw session API 集成
- 保存逻辑

### 方案 3: 用户手动触发 ✅ (已实现)

**作用：** 用户随时可以手动保存

**命令：**
```bash
# 方式 1: 对话中说
"保存记忆"

# 方式 2: 直接运行
node ~/clawd/skills/layered-memory/index.js extract --save

# 方式 3: 更新 MEMORY.md
vim ~/clawd/MEMORY.md
node ~/clawd/scripts/generate-layers-simple.js ~/clawd/MEMORY.md
```

## 推荐实施步骤

### Step 1: 启用 Bootstrap Hook (5分钟)

```bash
cd ~/clawd/skills/layered-memory

# 创建 hooks 目录结构（已完成）
# 安装 hook（需要调试）
openclaw hooks install .
openclaw hooks enable layered-memory
```

### Step 2: 创建定时检查脚本 (15分钟)

创建 `~/clawd/scripts/memory-session-checker.js`：

```javascript
// 检查当前会话状态
// 如果 token > 70%，自动保存记忆
// 发送通知给用户
```

### Step 3: 添加定时任务 (2分钟)

```bash
# 每 30 分钟检查一次
cron add --name "Memory Auto-Save" \
  --schedule "*/30 * * * *" \
  --command "node ~/clawd/scripts/memory-session-checker.js"
```

### Step 4: 测试验证 (10分钟)

1. 测试 bootstrap hook 是否生效
2. 测试定时任务是否运行
3. 模拟高 token 场景

## 实际效果

**会话开始：**
```
[Bootstrap Hook 注入]
AI 看到记忆管理提醒
AI 知道要定期检查 token
```

**会话进行中：**
```
[定时任务每 30 分钟检查]
Token < 70% → 继续
Token ≥ 70% → 自动保存 → 通知用户
```

**用户主动：**
```
用户: "保存记忆"
AI: 立即执行保存命令
```

## 优势

1. **三层防护** - Bootstrap 提醒 + 定时检查 + 手动触发
2. **真正自动化** - 定时任务不依赖 AI
3. **灵活可靠** - 多种触发方式
4. **轻量级** - 不影响对话性能

## 下一步

1. 调试 hook 安装（可选，不影响核心功能）
2. 开发 `memory-session-checker.js`（核心）
3. 添加定时任务
4. 测试验证

## 总结

原来的"完全自动触发器"思路是对的，但实现方式需要调整：
- ❌ 不能依赖 AI 在每次回复后执行脚本
- ✅ 应该用定时任务在后台检查
- ✅ Bootstrap hook 作为辅助提醒
- ✅ 保留手动触发作为兜底

这样才是真正可靠的自动化方案！
