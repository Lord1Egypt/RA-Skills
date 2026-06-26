# Milestone Execution

**多阶段任务执行器** — 让你控制节奏，AI 在独立工作会话中逐阶段执行任务。

---

## 核心理念

大型任务往往让人望而生畏——不知道 AI 在干什么、做到哪一步了、能不能随时停下。

**Milestone Execution** 的设计：**你控制行动权，AI 在单一独立会话里执行所有 milestone，完成后汇报等你指令。**

```
你（控制层）                      AI 工作会话（执行层）
─────────────────────────────────────────────────────
    │                                    │
    │  开始任务                          │ spawn
    │ ─────────────────────────────────► │
    │                                    │
    │                        执行 Milestone 1
    │                                    │
    │  ◄──────── sessions_yield 暂停 ──── │
    │  收到汇报，等你确认                 │
    │                                    │
    │  "继续"                            │
    │ ─────────────────────────────────► │
    │                        执行 Milestone 2
    │                                    │
    │  ◄──────── sessions_yield 暂停 ──── │
    │  收到汇报，等你确认                 │
    │                                    │
    │  ...（重复直到全部完成）            │
    │                                    │
    │                        sessions_yield 永久挂起
```

---

## 特性

### ✅ 单一会话完成所有 milestone
所有阶段在**同一个工作会话**中执行，保持上下文连贯。

### ✅ 主动汇报
每个 milestone 完成后自动汇报：
- 完成的内容
- 产生的文件
- 用时
- 整体进度条

### ✅ 你掌控节奏
- **"继续"** — 执行下一阶段
- **"retry"** — 重试当前阶段
- **"skip"** — 跳过当前阶段
- **"rollback"** — 回滚到上一个完成的阶段
- **"修改 X"** — 调整当前方向
- **"停止"** — 立即结束

### ✅ 崩溃恢复
工作会话异常中断？状态文件保存了进度，可以从断点恢复。

### ✅ 并行 milestone
对于完全独立的 milestone（如同时修改前端和后端），可以选择并行执行。

---

## 快速开始

### 指令

| 指令 | 行为 |
|------|------|
| `开始 [任务描述]` | 启动工作会话，开始执行 |
| `继续` | 执行下一个 milestone |
| `停下` | 停止当前操作 |
| `汇报` | 查看当前进度 |
| `retry` | 重试当前 milestone |
| `skip` | 跳过当前 milestone |
| `rollback` | 回滚到上一个完成的 milestone |
| `修改 [内容]` | 调整当前 milestone |
| `恢复` | 从中断恢复 |

### 示例

```
你：开始 重构用户模块
AI：启动工作会话执行 Milestone 1
     ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Milestone 1/4 完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 已完成：
   • 分析了用户模块现有代码结构
   • 识别出耦合严重的 UserService

📁 输出文件：
   • user-module-analysis.md

⏱️ 用时：2分30秒

🎯 整体进度：
   [██░░░░░░░░░░░░░░░░] 25%
   Milestone 1: ✅
   Milestone 2: 🔄 即将开始
   Milestone 3: ⏳ 等待中
   Milestone 4: ⏳ 等待中

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ "继续" 执行下一阶段
→ "retry" 重试当前
→ "skip" 跳过当前
→ "停止" 结束任务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 工作会话生命周期

```
1. 你说"开始 [任务]"
2. spawn 工作会话（单一会话）
3. 执行 Milestone 1 → sessions_yield 暂停
4. 你说"继续"
5. 执行 Milestone 2 → sessions_yield 暂停
6. ...（重复直到所有 milestone 完成）
7. 最终汇报 → sessions_yield 永久挂起
```

---

## 项目结构

```
milestone-execution/
├── SKILL.md                    # Skill 定义
├── README.md                   # 本文件
└── scripts/
    ├── milestone-executor       # 核心执行脚本
    ├── start.js                # 旧版启动器（已弃用）
    └── state.js                # 旧版状态管理（已弃用）
```

---

## 技术细节

### 状态文件

`.milestone-state.json` 保存任务进度：

```json
{
  "task": "重构用户模块",
  "totalMilestones": 4,
  "currentMilestone": 2,
  "workSessionKey": "agent:main:xxxxx",
  "milestones": [
    { "id": 1, "task": "调研现状", "status": "completed", "output": "..." },
    { "id": 2, "task": "重构数据层", "status": "pending", "dependsOn": [1] }
  ],
  "createdAt": "2026-04-06T05:00:00+08:00",
  "lastUpdated": "2026-04-06T05:05:00+08:00"
}
```

### 工作会话 prompt

工作会话通过 `sessions_yield` 主动暂停，不占用 AI 资源。汇报通过 `sessions_send` 推送到主会话。

---

## 适用场景

- ✅ 多步骤重构
- ✅ 大型代码审查
- ✅ 需要逐步确认的构建任务
- ✅ 任何可拆解的复杂任务
- ✅ 需要后台运行同时你可以做其他事

## 不适用

- ❌ 单步简单任务（直接做完不汇报）
- ❌ 需要实时反馈才能继续的操作
- ❌ 极度危险的操作

---

## License

MIT-0 - Free to use, modify, and redistribute. No attribution required.

---

**版本：** 3.0.0  
**作者：** Saskia (AI Assistant)  
**用户：** Siesta
