# AGENTS.md — 需求迭代工作流操作员指南

## 概述

这是一个人机协作的需求迭代工作流。人的角色从"告诉 agent 做什么"转变为"工程化条件，让好的结果通过迭代自然出现"。

## 三阶段

| 阶段 | 触发 | 产出物 |
|------|------|--------|
| Phase 1: 需求访谈 | "讨论需求"、"需求访谈" | specs/*.md |
| Phase 2: 计划 | "开始计划"、"可以拆任务了" | IMPLEMENTATION_PLAN.md |
| Phase 3: 迭代执行 | "开始执行"、"迭代构建" | 代码 + git commits |

---

## Phase 1: 需求访谈

### 何时触发
用户说"讨论需求"、"需求访谈"、"帮我理清需求"

### 操作步骤
1. **开场**：告诉用户你会通过结构化提问来理清需求
2. **追问**：用 requirements-interview.md 模板提问
3. **记录**：把讨论结果写入 specs/topic-xxx.md
4. **确认**：每个 topic 完成后确认用户认可
5. **收尾**：全部 topic 完备后，让用户确认整体

### 关键原则
- 问 Outcome，不问功能
- 用"一个句子，不带and"拆分 Topic
- 每个 spec 的验收标准必须可测试

### 验收清单
- [ ] 每个 Topic 有 specs/*.md
- [ ] 每个 spec 有明确的验收标准
- [ ] 边界情况已识别
- [ ] 用户已确认

---

## Phase 2: 计划

### 何时触发
用户说"开始计划"、"可以拆任务了"

### 操作步骤
1. 读取所有 specs/*.md
2. 如有现有代码，研究 codebase
3. 使用 planning-prompt.md 生成任务列表
4. 产出 IMPLEMENTATION_PLAN.md
5. 向用户确认计划

### 关键原则
- 只做计划，不写代码
- 任务要小到一次迭代可完成
- 按依赖关系排序

### 验收清单
- [ ] 所有 specs 都有对应任务
- [ ] 任务按优先级排列
- [ ] 用户已确认计划

---

## Phase 3: 迭代执行

### 何时触发
用户说"开始执行"、"迭代构建"

### 操作步骤
1. 读取 IMPLEMENTATION_PLAN.md
2. 选最高优先级未完成任务
3. 使用 build-prompt.md 执行
4. 验证 → 提交 → 更新 plan
5. 循环直到完成或用户停止

### 关键原则
- 一次一任务，不要扩散
- 每次迭代后立即验证和提交
- 遇到阻塞记录原因，继续下一任务

### 验证清单（每轮迭代）
- [ ] 任务完成，验收标准满足
- [ ] git commit 已创建
- [ ] IMPLEMENTATION_PLAN.md 已更新
- [ ] 用户知道当前进度

### 报告模板（每次迭代后）
```
✅ 已完成：[任务标题]
📝 Commit: [commit hash]
📋 进度：X/Y 任务完成

🔜 下一个：[任务标题]
```

---

## 沟通原则

### 不要阻塞对话
Ralph Loop 运行时不同步监控。让用户知道：
- "Loop 正在运行，我会周期性检查进度"
- "你可以随时问我进度"
- 不要 sleep 等待

### 遇到问题
1. 记录到 plan 注释
2. 标记 blocked
3. 报告用户："任务X因[原因]阻塞，我跳过继续做任务Y"

### 用户可以随时
- 问进度
- 修改计划
- 停止迭代
- 增加/删除任务

---

## 文件结构

```
[项目目录]/
├── specs/
│   ├── topic-a.md
│   └── topic-b.md
├── IMPLEMENTATION_PLAN.md
└── （项目代码）

skills/iterate-planning/
├── SKILL.md
├── AGENTS.md
└── templates/
    ├── requirements-interview.md
    ├── planning-prompt.md
    └── build-prompt.md
```
