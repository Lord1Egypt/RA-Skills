# 子Agent执行：双阶段Review + Monitor机制

> 从 mu-dev-workflow SKILL.md §阶段4 拆出。派发子Agent时读取此文件。

## 🚨 子Agent Task 体积铁律（防截断）

> **根因**：task 描述过长会导致子Agent context 超限，2分钟内退出且无任何实质输出——这是截断信号，不是完成。

### 四条硬规则

| 规则 | 内容 |
|---|---|
| **task 字数上限** | task 描述 ≤ 2000字（约4K tokens）。超限必须拆分或改用文件传参 |
| **大任务用文件传参** | 内容规格、prompt铁律、章节内容、代码片段 → 写入 `/tmp/` 文件，task 里只给路径和读取指令 |
| **超3步必拆串行** | 单次 task 超过3个主要步骤 → 拆成串行子Agent，前一个完成后主Agent再派下一个 |
| **截断识别** | 子Agent < 5分钟完成 且 输出 < 100字 = 截断信号，主Agent必须重派（精简 task 或文件传参）|

### 文件传参模式（超长内容标准做法）

```bash
# 主Agent：把大内容写到文件
cat > /tmp/task-spec.md << 'EOF'
[内容规格/prompt铁律/章节内容]
EOF

# task 描述里只写：
# 「先读 /tmp/task-spec.md，按其中规格执行」
```

### 截断 vs 正常完成判断

| 信号 | 判断 | 动作 |
|---|---|---|
| 运行时间 < 5min，输出 < 100字 | 截断 | 精简task重派 |
| 运行时间 < 5min，输出含「I'll start...」「Now I have...」 | 截断 | 文件传参重派 |
| 运行时间 > 10min，输出完整 | 正常完成 | 继续 |

---

## 执行模式选择

**简单任务**（1-2个文件，规格清晰）→ **主会话直接执行**

**复杂任务**（多文件、多步骤、>30分钟）→ **子Agent执行 + 双阶段 Review + Monitor**

## 共享目录约定（跨 Agent 任务传递标准）

```
./shared/
├── tasks/      # 任务描述文件（main 写入，executor 读取）
│   └── TASK-<id>.md
├── board/      # 任务状态看板（executor 更新，main/monitor 读取）
│   └── BOARD.md
└── knowledge/  # 跨 Agent 共享知识（任何 Agent 可写）
```

**任务文件格式**（`shared/tasks/TASK-<id>.md`）：
```markdown
# TASK-<id>：[任务名]

**状态**：pending / running / done / failed
**指派给**：executor
**截止**：预计完成时间

## 任务描述
[完整任务说明]

## 验收标准
- [ ] 条件1
- [ ] 条件2

## 产出物路径
[期望的输出文件路径]
```

**看板更新规则**：
- executor 开始任务 → 更新 BOARD.md 状态为 `running`
- executor 完成 → 更新为 `done`，写入产出物路径
- executor 卡住 → 更新为 `blocked`，写明原因

## 子Agent 双阶段 Review 流程

```
派发实现Agent → 完成 → 派发[规格审查Agent] → 通过 → 派发[质量审查Agent] → 通过 → 标记完成
                                         ↓ 不通过                    ↓ 不通过
                               实现Agent修复 → 重新审查      实现Agent修复 → 重新审查
```

### 规格审查 Agent 指令模板
```
你是代码审查员。请对比以下设计文档和实现代码，检查：
1. 是否实现了设计要求的所有功能（不多不少）
2. 是否遗漏了任何需求
3. 是否有多余的未要求功能

设计文档：[粘贴]
实现代码/变更：[粘贴 git diff]

输出：✅ 规格合规 / ❌ 发现问题（列举）
```

### 质量审查 Agent 指令模板
```
你是代码质量审查员。请审查以下代码：
1. 可读性：命名是否清晰？
2. 简洁性：有没有重复/冗余逻辑？
3. 健壮性：边界情况处理了吗？
4. 一致性：和现有代码风格是否一致？

代码：[粘贴]

输出：✅ 质量通过 / ❌ 问题（按重要性排列）
```

## Monitor Agent 机制（超长任务专用）

**触发条件**：预计执行时间 > 30 分钟的任务，必须同步启动 Monitor Agent。

**Monitor 职责**：
- 每 5 分钟读一次 `shared/board/BOARD.md`，检查 executor 状态
- 发现 `blocked` 或超时未更新（>10分钟无变化）→ 立即通知 main
- 不干预 executor 执行，只做观察和上报

### Monitor Agent 指令模板
```
你是 Monitor Agent，负责监督一个后台任务的执行状态。

任务看板路径：./shared/board/BOARD.md
监控的任务ID：TASK-<id>
超时阈值：10分钟无状态更新视为异常

执行步骤：
1. 每隔5分钟读取 BOARD.md
2. 检查任务状态：
   - running + 最后更新 < 10分钟前 → 正常，继续等待
   - done → 任务完成，向 main 报告结果，结束监控
   - blocked / failed → 立即通过可用的消息通道通知 main："⚠️ TASK-<id> 异常：<原因>"
   - running + 最后更新 > 10分钟前 → 视为卡死，通知 main

监控时长上限：<预计时长 × 2>，超出后强制告警。
```

### 三角协作流程
```
main ──写任务──→ shared/tasks/TASK-<id>.md
  │
  ├── spawn executor（读任务，执行，写看板）
  └── spawn monitor（监控看板，异常报 main）

monitor ──读──→ shared/board/BOARD.md ←──写── executor
│
└──异常时──→ 可用消息通道 → main
```

## 处理子Agent 状态
- **完成**：进入规格审查
- **完成但有疑虑**：先读疑虑，再决定是否先修复再审查
- **需要更多信息**：补充上下文，重新派发
- **卡住了**：拆更小任务，或换更强模型，不要强行重试
