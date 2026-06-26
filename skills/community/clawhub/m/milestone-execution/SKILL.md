---
name: milestone-execution
version: 3.0.0
description: "多阶段任务执行器 - 用户控制节奏，AI在独立工作会话中逐阶段执行任务。每个 milestone 完成后暂停汇报，用户确认后再继续下一阶段。"
---

# Milestone Execution v3.0

**核心理念：** 用户控制节奏，AI 在单一独立工作会话中逐阶段执行任务。

---

## 架构

```
┌─────────────────────────────────────────────────────┐
│  主会话（控制层）                                     │
│  • 接收用户指令："开始"、"继续"、"停下"等             │
│  • 运行 exec 执行 milestone-executor 脚本             │
│  • 脚本自动 spawn 工作会话、管理状态                  │
└──────────────────────┬──────────────────────────────┘
                       │ sessions_send / sessions_yield
┌──────────────────────▼──────────────────────────────┐
│  工作会话（执行层）- 单一会话执行所有 milestone        │
│  • 执行当前 milestone                                 │
│  • 完成后 sessions_yield 暂停等待主会话指令           │
└─────────────────────────────────────────────────────┘
```

---

## 用户指令与脚本行为

| 用户指令 | 主会话行为 |
|---------|-----------|
| `开始 [任务描述]` | 运行 `milestone-executor start "任务" "m1\|m2\|m3"` |
| `继续` | 运行 `milestone-executor continue <workSessionKey>` |
| `停下` | 运行 `milestone-executor stop <workSessionKey>` |
| `汇报` | 运行 `milestone-executor status` |
| `retry` | 运行 `milestone-executor retry <workSessionKey>` |
| `skip` | 运行 `milestone-executor skip <workSessionKey>` |
| `rollback` | 运行 `milestone-executor rollback` |
| `修改 [内容]` | 运行 `milestone-executor modify <workSessionKey> "内容"` |
| `恢复` | 运行 `milestone-executor recover` |

---

## 执行脚本

**milestone-executor** 是核心脚本，负责：
1. 状态文件管理（`.milestone-state.json`）
2. 调用 sessions_spawn 启动工作会话
3. 调用 sessions_send 向工作会话发指令
4. 返回 JSON 格式的状态给主会话

---

## 工作会话行为（必须严格遵循）

工作会话启动后进入**里程碑执行循环**：

```
1. 读取 .milestone-state.json 获取当前 milestone
2. 执行当前 milestone（调用工具、修改文件等）
3. 更新状态文件（status: running → completed）
4. 生成汇报，调用 sessions_send 发送到主会话
5. 调用 sessions_yield() 暂停
6. 等待主会话通过 sessions_send 发来指令
7. 根据指令决定下一步：
   - "continue" → 执行下一个 milestone（回到步骤2）
   - "retry" → 重新执行当前 milestone（回到步骤2）
   - "skip" → 跳过当前，执行下一个（回到步骤2）
   - "rollback" → 恢复到上一个完成的 milestone（更新状态文件，回到步骤2）
   - "modify: ..." → 更新任务方向（更新状态文件，回到步骤2）
   - "stop" → 清理状态，永久暂停
8. 所有 milestone 完成后：
   - 生成最终汇报
   - 调用 sessions_send 发送到主会话
   - 永久暂停（sessions_yield）
```

---

## 状态文件

```json
// .milestone-state.json
{
  "task": "任务名称",
  "totalMilestones": 3,
  "currentMilestone": 2,
  "workSessionKey": "agent:main:xxxxx",
  "milestones": [
    { "id": 1, "status": "completed", "output": "完成内容", "duration": "2m30s" },
    { "id": 2, "status": "pending", "task": "第二个 milestone", "dependsOn": [1] }
  ],
  "createdAt": "2026-04-06T05:00:00+08:00",
  "lastUpdated": "2026-04-06T05:05:00+08:00"
}
```

---

## 汇报格式

### Milestone 完成时
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Milestone {n}/{total} 完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 已完成：
   • [具体完成内容]

📁 输出文件：
   • [相关文件]

⏱️ 用时：{duration}

🎯 整体进度：
   [{bar}] {percent}%
   Milestone 1: ✅
   Milestone 2: ✅
   Milestone 3: 🔄 即将开始
   Milestone 4: ⏳ 等待中
   Milestone 5: ⏳ 等待中

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ "继续" 执行下一阶段
→ "retry" 重试当前
→ "skip" 跳过当前
→ "rollback" 回滚
→ "修改 X" 调整当前方向
→ "停止" 结束任务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 任务全部完成
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 任务完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📜 Milestone 历史：
   [1] ✅ 阶段1 - {time}
   [2] ✅ 阶段2 - {time}

总用时：{total_duration}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 并行 Milestone

对于完全独立的 milestone（如同时修改前端和后端）：

```
检测到可并行的 milestone：
  • Milestone 2 - 独立（用户模块）
  • Milestone 4 - 独立（管理后台）

是否并行执行？[是/否/仅Milestone X]
```

**并行执行时：**
- 两个 milestone 同时在各自的工作会话中运行
- 都完成后统一汇报
- 一个失败不影响另一个

---

## 崩溃恢复

当工作会话异常中断时：
1. 检测到 `.milestone-state.json` 存在但 workSessionKey 指向的会话已不存在
2. 主会话询问用户："检测到上次任务中断，是否恢复？"
3. 用户说"恢复" → 从状态文件读取状态，用 `milestone-executor recover` 重建工作会话
4. 继续执行当前 milestone

---

## 实现要点（强制规则）

1. **单一会话**：所有 milestone 在**同一个**工作会话中执行
2. **sessions_yield**：每个 milestone 完成后**必须**调用 `sessions_yield()` 暂停
3. **sessions_send**：通过 sessions_send 与主会话通信
4. **状态持久化**：`.milestone-state.json` 保存进度
5. **工作会话永不自发结束**：除非收到 "stop" 指令或所有 milestone 完成

---

## 注意事项

- 工作会话是独立的，有自己的上下文
- 状态文件用于崩溃恢复
- 汇报推送到主会话（当前 chat）
- 不要在主会话直接执行任务，全部委托给工作会话
- **绝对规则**：一个任务 = 一个工作会话 = 多个 milestone
